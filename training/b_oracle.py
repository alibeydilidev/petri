"""S3 / PL-24 + PL-25 — B kaynağı koordinasyon oracle'ı.

**İKİ SORU (M-22: fizibilite iki sorudur):**

  (i)  SÜRDÜRÜLEBİLİRLİK — koordinasyon OLURSA B ekonomik mi?
       (PL-24: `runs/s3_b_oracle.json`'ı üreten kod repoda YOKTU;
        economy v3'ün B=180 kararı öksüz bir sonuç dosyasına
        dayanıyordu — KAPI 5 açıktı. Bu modül onu kapatır.)

  (ii) KEŞFEDİLEBİLİRLİK — koordinasyon BULUNABİLİR mi?
       (PL-25: hiç ölçülmemişti. İlk nefes koşumunun "B-açılış 0"ı
        sıfır güçlü bir ölçümdü: şans-keşfi olasılığı 20K turda
        0.002 idi, yani gözlenen sıfır saf şansın öngördüğü değerdi.)

Bu modül AJAN DEĞİLDİR, ölçüm aletidir → KERNEL_BUDGET'a bit yazmaz
(`training/oracle.py` emsali). Politikalar scripted ve deterministiktir.

**MERDİVEN (M-06 — tek değişken, katman katman):**

  L0 `random`  — şans tabanı; analitik hesabın ampirik karşılığı.
  L1 `vision`  — gördüğü B'ye yürü + INTERACT + bekle. KANAL YOK.
  L2 `signal`  — L1 + kanal: B'yi gören SYM_B yayar; duyan yerel
                 tarama moduna geçer. Kanal YÖN ve KİMLİK taşımaz
                 (PL-21b/c) → duyan sinyale doğru YÜRÜYEMEZ; aldığı
                 tek bilgi "Chebyshev 8 içinde biri var", yani arama
                 uzayı 4096 hücreden 17x17=289 hücreye daralır (~14x).
  L3 `god`     — her iki ajan B konumlarını BİLİR, randevulaşır.
                 Koordinasyon tavanı = sürdürülebilirlik sorusu.

**BEYAN (önemli):** L2, `SYM_B` konvansiyonunu HEDİYE alır — hangi
sembolün "burada B var" demek olduğu ajanın KEŞFETMESİ gereken şeydir
(H3/H4'ün konusu). Oracle'a verilmesi bilinçlidir: L2, MÜKEMMEL
PAYLAŞILAN KONVANSİYON altındaki TAVANI ölçer. L2 bile öğrenilebilir
bir hızda açılış üretemiyorsa, öğrenilmiş hiçbir dil üretemez —
o zaman eksik olan ajan değil, dünyanın kalibrasyonudur.

Kullanım:
  python3 -m training.b_oracle --stage sustain  --out runs/s3_b_oracle_v2.json
  python3 -m training.b_oracle --stage discover --out runs/s3_b_discover.json
  python3 -m training.b_oracle --stage calib    --out runs/s3_b_calib.json
"""

import argparse
import dataclasses
import json
import pathlib

import numpy as np

from agent.channel import NO_SIGNAL
from agent.config import AgentConfig
from agent.homeostasis import Homeostasis
from world.config import WorldConfig, config_hash
from world.grid import DOWN, INTERACT, LEFT, RIGHT, STAY, UP, World

SYM_B = 0            # oracle konvansiyonu (yukarıdaki beyana bakınız)
MAX_TURNS = 3000     # v1 1500'de sansürlüydü; sansür oranı raporlanır

# S3 ekolojisiyle aynı ekonomi/maliyetler (roster COMMON: metabolizma 0.6).
BASE_CFG = dict(obs_radius=4, memory_dim=128, learning_rate=5e-4,
                base_metabolism=0.6, channel_open=True)


def _wrap(d: int, g: int) -> int:
    """Toroidal işaretli fark: (-g/2, g/2]."""
    d %= g
    return d - g if d > g // 2 else d


def _step_toward(pos, target, g: int) -> int | None:
    """Hedefe bir adım (büyük eksen önce; kararlı eşitlik bozumu).
    Hedefteysek None."""
    dy = _wrap(int(target[0]) - int(pos[0]), g)
    dx = _wrap(int(target[1]) - int(pos[1]), g)
    if dy == 0 and dx == 0:
        return None
    if abs(dy) >= abs(dx):
        return DOWN if dy > 0 else UP
    return RIGHT if dx > 0 else LEFT


def _cheb(a, b, g: int) -> int:
    return max(abs(_wrap(int(a[0]) - int(b[0]), g)),
               abs(_wrap(int(a[1]) - int(b[1]), g)))


# Politika sabitleri. M-20: taban, ölçülen yetinin ZORLUĞUNDA seçilir —
# B'yi kovalarken açlıktan ölen bir politika keşfedilebilirliği değil
# intiharı ölçer. İlk duman testinde tam bu oldu (ömür 63 tur = "her tur
# hareket" tavanı), düzeltildi.
MAX_B_WAIT = 25      # B üstünde ortak beklemenin üst sınırı (tur)
B_COOLDOWN = 60      # vazgeçilen B'yi yeniden hedeflememe süresi
SEARCH_BUDGET = 45   # L2: sinyal sonrası yerel tarama bütçesi (tur)

# L2 yerel raster: menzil 8 → hedef 17x17 kutuda. Gözlem yarıçapı 4
# (9x9 görüş) ile 9 ara nokta kutuyu tam kaplar.
_WAYPOINTS = [(dy, dx) for dy in (-8, 0, 8) for dx in (-8, 0, 8)]


class Coordinator:
    """Bir oracle sakini. Seviyeye göre yalnız B STRATEJİSİ değişir;
    hayatta kalma mantığı (A hasadı + düşük-enerji önceliği) tüm
    seviyelerde AYNIdır — M-06 gereği merdivende tek değişken."""

    def __init__(self, level: str, cfg: AgentConfig, grid: int, idx: int = 0):
        self.level, self.cfg, self.g = level, cfg, grid
        self.r = cfg.obs_radius
        # Tarama FAZI ajana göre kaydırılır. Aynı fazda iki lawnmower
        # birlikte doğuya gider → BAĞIL HIZ SIFIR → hiç karşılaşmazlar;
        # ilk sürümde `pair` kolunun 0/48 çıkmasının sebebi buydu
        # (dünyanın değil politikanın özelliği — enstrüman kusuru).
        self._east = (idx * grid // 2) % grid
        self._down = 0
        self._wait = 0          # B üstünde beklenen tur
        self._cooldown = 0      # vazgeçilen B'yi yok sayma sayacı
        self._search = 0        # L2: yerel tarama kalan turu
        self._wp: list[tuple[int, int]] = []   # L2: ara nokta kuyruğu
        self._anchor: tuple[int, int] | None = None   # L2b: sıcak çapa
        # L2b feneri daha uzun yanar: tarama ~32 tur sürüyor, 25 turluk
        # yayın penceresi randevuya matematiksel olarak yetmiyordu.
        self._max_wait = 60 if level == "beacon" else MAX_B_WAIT

    # ---------------------------------------------------------- algılama
    def _visible(self, obs: np.ndarray, ch: int) -> list[tuple[int, int]]:
        """Gözlemdeki hücrelerin BAĞIL (dy, dx) ofsetleri."""
        return [(int(y) - self.r, int(x) - self.r)
                for y, x in np.argwhere(obs[ch] > 0.5)]

    @staticmethod
    def _nearest(offsets: list[tuple[int, int]]) -> tuple[int, int]:
        """Chebyshev'e göre en yakın; eşitlik kararlı bozulur."""
        return min(offsets, key=lambda o: (max(abs(o[0]), abs(o[1])),
                                           o[0], o[1]))

    def _scan(self) -> int:
        """Lawnmower taraması (training/oracle.py ile aynı desen)."""
        if self._down > 0:
            self._down -= 1
            return DOWN
        self._east += 1
        if self._east >= self.g:
            self._east = 0
            self._down = 2 * self.r
            return DOWN
        return RIGHT

    def _local_search(self, pos) -> int:
        """L2: sinyal duyuldu → yayıncı Chebyshev 8 içinde. Kanal YÖN
        taşımadığı için (PL-21b) sinyale doğru yürünemez; yapılabilecek
        en iyi şey 17x17 kutuyu ara noktalardan taramaktır."""
        self._search -= 1
        while self._wp:
            tgt = ((self._wp[0][0]) % self.g, (self._wp[0][1]) % self.g)
            step = _step_toward(pos, tgt, self.g)
            if step is not None:
                return step
            self._wp.pop(0)            # ara noktaya varıldı → sıradaki
        self._search = 0
        return self._scan()

    # ---------------------------------------------------------- politika
    def act(self, world: World, i: int, energy: float,
            heard: list[tuple[int, int]],
            alive_ids: list[int] | None = None) -> tuple[int, int]:
        """(eylem, sembol) döndürür. `alive_ids` yalnız Tanrı-gözü
        randevusunda kullanılır (diğer seviyeler onu göremez)."""
        alive_ids = alive_ids if alive_ids is not None \
            else list(range(world.n_entities))
        if self.level == "random":
            return int(world.rng.integers(0, 6)), NO_SIGNAL

        obs = world.observe(i, self.r)
        pos = world.entity_pos[i]
        sig = NO_SIGNAL
        if self._cooldown > 0:
            self._cooldown -= 1

        # En yakın A: god'da Tanrı-gözü, diğerlerinde yalnız GÖRÜNÜR olan.
        if self.level == "god" and len(world.res_a):
            near_a = self._nearest(
                [(_wrap(int(c[0]) - int(pos[0]), self.g),
                  _wrap(int(c[1]) - int(pos[1]), self.g))
                 for c in world.res_a])
        else:
            vis_a = self._visible(obs, 0)
            near_a = self._nearest(vis_a) if vis_a else None

        # --- (1) B HEDEFİ (merdivenin tek değişkeni) ----------------------
        b_target, b_wait_est = None, 0
        if self.level == "god":
            # Tanrı-gözü randevu: İKİ ajanın da AYNI B'yi seçmesi için
            # paylaşılan minimax kuralı — varış süreleri dengelensin diye
            # max(d1,d2)'yi küçülten B. (İlk sürüm "mutlak sıradaki ilk B"
            # idi; erken varan 35+ tur bekleyip ölüyordu.)
            # Randevu, min_agents kadar EN YAKIN ajanı buluşturacak B'yi
            # seçer (n>2'de herkesin gelmesi gereksiz ve pahalı).
            need_k = world.cfg.resource_b_min_agents
            best, bd, best_ds = None, None, None
            for k in range(len(world.res_b)):
                c = world.res_b[k]
                ds = sorted(_cheb(world.entity_pos[j], c, self.g)
                            for j in alive_ids)[:need_k]
                key = (max(ds), int(c[0]), int(c[1]))
                if bd is None or key < bd:
                    best, bd, best_ds = c, key, ds
            b_target = best
            b_wait_est = max(best_ds) - min(best_ds)
        elif self.level in ("vision", "signal", "beacon") \
                and self._cooldown == 0:
            vis_b = self._visible(obs, 1)
            if vis_b:
                dy, dx = self._nearest(vis_b)
                b_target = ((int(pos[0]) + dy) % self.g,
                            (int(pos[1]) + dx) % self.g)
                b_wait_est = self._max_wait
                if self.level in ("signal", "beacon"):
                    sig = SYM_B          # gördüm → yayınla (konvansiyon)

        # --- (2) HAYATTA KALMA: B'ye gidip beklemeye yetecek enerji var mı?
        # Sabit eşik yerine MESAFE-DUYARLI ihtiyaç (sabit eşik god'u A ile
        # B arasında salındırıp öldürüyordu — duman testi bulgusu).
        if b_target is not None:
            d = _cheb(pos, b_target, self.g)
            need = d * (self.cfg.base_metabolism + self.cfg.move_energy_cost) \
                + b_wait_est * 2.1 + 10.0
            if energy < need and near_a is not None:
                b_target = None          # önce karnını doyur

        if b_target is not None:
            step = _step_toward(pos, b_target, self.g)
            if step is None:             # B'nin ÜSTÜNDEYİZ → aç ve bekle
                self._wait += 1
                if self._wait > self._max_wait:   # ortak gelmedi → vazgeç
                    self._wait, self._cooldown = 0, B_COOLDOWN
                else:
                    return INTERACT, (SYM_B if self.level in
                                      ("signal", "beacon") else sig)
            else:
                self._wait = 0
                return step, sig

        # --- (3) A hasadı -------------------------------------------------
        if near_a is not None:
            if near_a == (0, 0):
                return INTERACT, sig
            tgt = ((int(pos[0]) + near_a[0]) % self.g,
                   (int(pos[1]) + near_a[1]) % self.g)
            return _step_toward(pos, tgt, self.g) or STAY, sig

        # --- (3b) EŞLEŞME kontrolü (L2c `pair`): kanala HİÇ ihtiyaç yok --
        # Ajanlar birbirini gözlem kanalı 3'ten görür. Ortağa yaklaşıp
        # AYNI hücreye gelince, iki özdeş deterministik politika özdeş
        # gözlem alır → özdeş hareket eder → birlikte kalır; sonra her
        # bulunan B otomatik açılır. Bu kol, "B basıncı iletişimi mi yoksa
        # GÖRSEL TAKİBİ mi seçer" sorusunun ayıracıdır (H3/H4 için kritik).
        if self.level == "pair":
            vis_e = self._visible(obs, 3)
            if vis_e:
                dy, dx = self._nearest(vis_e)
                if (dy, dx) != (0, 0):
                    tgt = ((int(pos[0]) + dy) % self.g,
                           (int(pos[1]) + dx) % self.g)
                    return _step_toward(pos, tgt, self.g) or STAY, sig

        # --- (4) arama ----------------------------------------------------
        if self.level in ("signal", "beacon"):
            if heard and (self._search == 0 or self.level == "beacon"):
                # L2b FENER: her duyuşta çapayı TAZELE. Yayıncı çapanın
                # Chebyshev 8'i içinde olduğundan 17x17 kutu onu KESİN
                # kapsar; sinyal kesilince çapaya dönmek aramayı sıcak
                # bölgede tutar (L2'de çapa yenilenmiyordu).
                self._anchor = (int(pos[0]), int(pos[1]))
                self._search = SEARCH_BUDGET
                self._wp = [((self._anchor[0] + dy) % self.g,
                             (self._anchor[1] + dx) % self.g)
                            for dy, dx in _WAYPOINTS]
            if self._search > 0:
                return self._local_search(pos), sig
        return self._scan(), sig


def run_pair(level: str, wcfg: WorldConfig, seed: int,
             max_turns: int = MAX_TURNS, n_agents: int = 2) -> dict:
    """n koordinatör, koordinasyon penceresi kapanana kadar.

    Pencere = en az `resource_b_min_agents` ajan HAYATTAysa açık. Ölen
    ikame EDİLMEZ (oracle, ekoloji değil). M-21 gereği n parametrik:
    2-ajan sonucu 5-ajan rejimine otomatik taşınmaz — çift sayısı
    C(n,2) ile büyür, karşılaşma oranı onunla birlikte.
    """
    world = World(wcfg, n_entities=n_agents, seed=seed)
    cfg = AgentConfig(**BASE_CFG)
    coords = [Coordinator(level, cfg, wcfg.grid_size, idx=k)
              for k in range(n_agents)]
    homeo = [Homeostasis(cfg) for _ in range(n_agents)]
    heard: list[list[tuple[int, int]]] = [[] for _ in range(n_agents)]

    pair_turns = 0
    first_opening = None
    alive = list(range(n_agents))
    for turn in range(1, max_turns + 1):
        acts, sigs = [], []
        for i, c in enumerate(coords):
            if not homeo[i].alive:       # ölü beden: hareketsiz, sessiz
                acts.append(STAY)
                sigs.append(NO_SIGNAL)
                continue
            a, s = c.act(world, i, homeo[i].energy, heard[i], alive)
            acts.append(a)
            sigs.append(s)
        before = world.b_openings_total
        deltas = world.step(np.array(acts), np.array(sigs))
        if world.b_openings_total > before and first_opening is None:
            first_opening = turn
        for i in range(n_agents):
            if not homeo[i].alive:
                continue
            extra = cfg.signal_energy_cost if sigs[i] != NO_SIGNAL else 0.0
            homeo[i].apply_turn(acts[i], float(deltas[i]) - extra)
            heard[i] = world.heard(i, wcfg.signal_range)
        alive = [i for i in range(n_agents) if homeo[i].alive]
        pair_turns = turn
        if len(alive) < wcfg.resource_b_min_agents:
            break

    return {"pair_lifetime": pair_turns,
            "openings": world.b_openings_total,
            "first_opening": first_opening,
            "censored": pair_turns >= max_turns
            and len(alive) >= wcfg.resource_b_min_agents}


def sweep(level: str, wcfg: WorldConfig, episodes: int = 12,
          n_agents: int = 2) -> dict:
    rows = [run_pair(level, wcfg, seed=9000 + e, n_agents=n_agents)
            for e in range(episodes)]
    life = np.array([r["pair_lifetime"] for r in rows], dtype=float)
    op = np.array([r["openings"] for r in rows], dtype=float)
    firsts = [r["first_opening"] for r in rows if r["first_opening"]]
    total_turns = float(life.sum())
    return {
        "level": level,
        "episodes": episodes,
        "median_pair_lifetime": float(np.median(life)),
        "median_openings": float(np.median(op)),
        "total_openings": int(op.sum()),
        "total_pair_turns": int(total_turns),
        # ASIL keşfedilebilirlik ölçüsü: 1000 çift-turu başına açılış
        "openings_per_1000_pair_turns": round(1000 * op.sum() / total_turns, 3)
        if total_turns else 0.0,
        "episodes_with_opening": int((op > 0).sum()),
        "median_turns_to_first": float(np.median(firsts)) if firsts else None,
        "censored_episodes": int(sum(r["censored"] for r in rows)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["sustain", "discover", "calib"],
                    required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--episodes", type=int, default=12)
    a = ap.parse_args()

    base = dataclasses.replace(WorldConfig(), resource_a_count=24)
    out: dict = {"stage": a.stage, "max_turns": MAX_TURNS,
                 "base_world": dataclasses.asdict(base),
                 "base_config_hash": config_hash(base), "results": []}

    if a.stage == "sustain":
        # PL-24: B enerjisi süpürmesi, KOORDİNASYON TAVANI (L3) altında.
        for b in (75.0, 135.0, 180.0, 225.0, 270.0):
            wcfg = dataclasses.replace(base, resource_b_energy=b)
            r = sweep("god", wcfg, a.episodes)
            r["b_energy"] = b
            r["per_agent_gain"] = b / 2
            r["config_hash"] = config_hash(wcfg)
            out["results"].append(r)
            print(f"[sustain] B={b:>5} | çift-ömür {r['median_pair_lifetime']:>6} "
                  f"| açılış {r['median_openings']:>5} | sansür "
                  f"{r['censored_episodes']}/{a.episodes}", flush=True)

    elif a.stage == "discover":
        # PL-25: keşfedilebilirlik merdiveni, MEVCUT config'de (B=180).
        # noB = B'yi hiç kovalamayan hayatta-kalma kontrolü. M-15/M-20
        # gereği CİHAZ DOĞRULAMASI: S2.7 tek-ajan oracle'ı aynı ekonomide
        # (m=0.6/24/A=45) ~197 tur yaşıyordu; noB bunu yakalamıyorsa
        # politika bozuktur ve merdivenin hiçbir basamağı okunamaz.
        for level in ("random", "noB", "vision", "signal", "beacon",
                      "pair", "god"):
            r = sweep(level, base, a.episodes)
            out["results"].append(r)
            print(f"[discover] {level:>7} | açılış/1000 çift-turu "
                  f"{r['openings_per_1000_pair_turns']:>7} | epizot-ile-açılış "
                  f"{r['episodes_with_opening']}/{a.episodes} | ilk açılış "
                  f"{r['median_turns_to_first']} | çift-ömür "
                  f"{r['median_pair_lifetime']}", flush=True)

    else:  # calib — basıncı doğurabilecek dünya ayarları (Ali'ye girdi)
        for n_b in (3, 8, 20):
            for rng_ in (8, 16):
                wcfg = dataclasses.replace(base, resource_b_count=n_b,
                                           signal_range=rng_)
                for level in ("vision", "signal"):
                    r = sweep(level, wcfg, a.episodes)
                    r.update(resource_b_count=n_b, signal_range=rng_,
                             config_hash=config_hash(wcfg))
                    out["results"].append(r)
                    print(f"[calib] B_n={n_b:>2} menzil={rng_:>2} {level:>6} "
                          f"| açılış/1000 "
                          f"{r['openings_per_1000_pair_turns']:>7} | "
                          f"{r['episodes_with_opening']}/{a.episodes} epizot",
                          flush=True)

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nyazıldı: {a.out}")


if __name__ == "__main__":
    main()
