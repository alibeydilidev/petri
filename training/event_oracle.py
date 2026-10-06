"""S3-C fizibilite oracle'ı — asimetrik olay görevi (M-01, M-22).

**İKİ SORU (M-22):**
  (i)  DEĞER: kutbu bilmek hayatta kalmayı ölçülebilir biçimde
       artırıyor mu? (bilmeyen `deaf` ↔ tam bilen `god`)
  (ii) KANAL YETERLİ Mİ: mükemmel konvansiyonlu bir yayın, o değerin
       ne kadarını yakalıyor? (`told`)

**Üçüncü soru — B görevinde eksik olan, ders alınan (M-22'nin şerhi):**
  (iii) KANAL GEREKLİ Mİ: ajan kendi ipucuyla (ya da acıdan öğrenerek)
        değerin çoğunu zaten alıyorsa kanal gereksizdir ve tuzak boştur.
        `own` ve `own_infer` kolları tam bunu sınar.

Ajan DEĞİL, ölçüm aletidir → KERNEL_BUDGET'a bit yazmaz.

**Merdiven (M-06 — tek değişken: KUTUP BİLGİSİ):**
  `none`      — olaylar kapalı; taban ömür çıpası
  `deaf`      — olay var, kutup bilgisi yok → sabit STAY (1/K isabet)
  `own`       — yalnız kendi ipucu bitini kullanır (K/2 aday → 1/2)
  `own_infer` — `own` + acıdan öğrenme denemesi (süre=1 kilidinin sınavı)
  `told`      — kendi biti + menzildeki ortağın bitini yayınla/duy → tam
  `god`       — kutbu doğrudan bilir (tavan)

**BEYAN (M-09):** tüm kollara olayın NE ZAMAN aktif olduğu verilir;
merdivenin tek değişkeni HANGİ EYLEMİN güvenli olduğudur. Zamanlama
öncüden okunabilir bir bilgidir ve burada değişken değildir.
`told` kolu ayrıca sembol→bit konvansiyonunu HEDİYE alır (B oracle'ının
SYM_B geleneği): bu kol, öğrenilmiş bir dilin ULAŞABİLECEĞİ TAVANI
ölçer, tipik performansını değil.

Kullanım:
  python3 -m training.event_oracle --out runs/s3c_event_oracle.json
"""

import argparse
import dataclasses
import json
import pathlib

import numpy as np

from agent.channel import NO_SIGNAL
from agent.config import AgentConfig
from agent.homeostasis import Homeostasis
from training.b_oracle import BASE_CFG, Coordinator, _cheb
from world.config import WorldConfig, config_hash
from world.grid import STAY, World

MAX_TURNS = 3000
LEVELS = ("none", "deaf", "own", "own_infer", "told", "god")


def run_episode(level: str, wcfg: WorldConfig, seed: int,
                n_agents: int = 2, max_turns: int = MAX_TURNS) -> dict:
    """Tek epizot; ilk ölüme kadar (pencere), ajan-turu ve isabet sayar."""
    world = World(wcfg, n_entities=n_agents, seed=seed)
    cfg = AgentConfig(**BASE_CFG)
    # Olay dışı davranış TÜM kollarda aynı: b_oracle'ın doğrulanmış
    # hayatta-kalma politikası (`noB`) — tek değişken kutup bilgisidir.
    coords = [Coordinator("noB", cfg, wcfg.grid_size, idx=k)
              for k in range(n_agents)]
    homeo = [Homeostasis(cfg) for _ in range(n_agents)]
    heard: list[list[tuple[int, int]]] = [[] for _ in range(n_agents)]
    # told: sembol -> (bit, değer) mükemmel konvansiyonu (hediye).
    # sembol = 2*bit + değer  →  {0,1,2,3}
    inbox: list[dict[int, int]] = [{} for _ in range(n_agents)]
    last_penalty = [False] * n_agents
    lifespans: list[int | None] = [None] * n_agents
    window: int | None = None

    hits = misses = 0
    turn = 0
    for turn in range(1, max_turns + 1):
        ev = world.events
        acts, sigs = [], []
        for i in range(n_agents):
            if not homeo[i].alive:
                acts.append(STAY)
                sigs.append(NO_SIGNAL)
                continue
            sig = NO_SIGNAL
            # --- yayın: olay zamanlandığı tur kendi bitini duyur ------
            if level == "told" and ev.pending(turn) \
                    and turn == ev.starts_at - wcfg.event_lead + 1:
                cue = ev.cue_for(i)
                if cue is not None:
                    sig = 2 * cue[0] + cue[1]
            # --- olay aktifse: eylem = kutup tahmini ------------------
            if ev.active(turn) and level != "none":
                acts.append(_choose(level, ev, i, inbox[i],
                                    last_penalty[i]))
                sigs.append(sig)
                continue
            a, _ = coords[i].act(world, i, homeo[i].energy, heard[i],
                                 [j for j in range(n_agents)
                                  if homeo[j].alive])
            acts.append(a)
            sigs.append(sig)

        active = ev.active(turn)
        safe = ev.safe_action() if active else None
        deltas = world.step(np.array(acts), np.array(sigs))

        for i in range(n_agents):
            if not homeo[i].alive:
                continue
            extra = cfg.signal_energy_cost if sigs[i] != NO_SIGNAL else 0.0
            homeo[i].apply_turn(acts[i], float(deltas[i]) - extra)
            heard[i] = world.heard(i, wcfg.signal_range)
            for _sender, sym in heard[i]:
                if 0 <= sym < 4:
                    inbox[i][sym // 2] = sym % 2
            last_penalty[i] = active and acts[i] != safe
            if active:
                if acts[i] == safe:
                    hits += 1
                else:
                    misses += 1
            if not homeo[i].alive and lifespans[i] is None:
                lifespans[i] = turn
        if not ev.pending(turn) and not active:
            inbox = [{} for _ in range(n_agents)]   # olay bitti, kutu boşalt
        if window is None and any(l is not None for l in lifespans):
            window = turn                 # ilk ölüm: koordinasyon penceresi
        if all(l is not None for l in lifespans):
            break

    # M-24: "pencere = min(n ömür)" n büyüdükçe TÜM farkları sıkıştırır →
    # DEĞER ölçüsü olarak geçersiz. Kişi-başı ömür n'den bağımsızdır.
    return {"window": window or turn,
            "lifespans": [l if l is not None else turn for l in lifespans],
            "hits": hits, "misses": misses, "censored": turn >= max_turns}


def _choose(level: str, ev, i: int, inbox: dict[int, int],
            was_penalized: bool) -> int:
    """Olay aktifken hangi eylem? Merdivenin TEK değişkeni."""
    if level == "deaf":
        return STAY
    if level == "god":
        return ev.safe_action()
    cands = ev.candidates(i)                      # kendi ipucu: K/2 aday
    if level == "told":
        cue = ev.cue_for(i)
        merged = dict(inbox)
        if cue is not None:
            merged[cue[0]] = cue[1]
        full = [p for p in range(ev.cfg.event_polarities)
                if all((p >> b) & 1 == v for b, v in merged.items())]
        if len(full) == 1:
            return full[0]
        cands = full or cands
    if level == "own_infer" and was_penalized and len(cands) > 1:
        return cands[1]        # geçen tur yanmıştı → diğer adayı dene
    return cands[0]


def sweep(level: str, wcfg: WorldConfig, episodes: int = 48,
          n_agents: int = 2) -> dict:
    rows = [run_episode(level, wcfg, seed=9000 + e, n_agents=n_agents)
            for e in range(episodes)]
    win = np.array([r["window"] for r in rows], dtype=float)
    lives = np.array([x for r in rows for x in r["lifespans"]], dtype=float)
    h = sum(r["hits"] for r in rows)
    m = sum(r["misses"] for r in rows)
    return {"level": level, "episodes": episodes,
            # BİRİNCİL değer ölçüsü: kişi-başı ömür (n'den bağımsız, M-24)
            "median_lifespan": float(np.median(lives)),
            "mean_lifespan": round(float(lives.mean()), 1),
            # İKİNCİL: koordinasyon penceresi (ilk ölüme kadar) — n'e bağlı
            "median_window": float(np.median(win)),
            "hit_rate": round(h / (h + m), 3) if h + m else None,
            "event_turns": h + m,
            "censored": int(sum(r["censored"] for r in rows))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--episodes", type=int, default=48)
    a = ap.parse_args()

    base = dataclasses.replace(WorldConfig(), resource_a_count=24,
                               event_every=30, event_lead=8,
                               event_duration=1, event_penalty=25.0,
                               event_polarities=4)
    out = {"world": dataclasses.asdict(base),
           "config_hash": config_hash(base), "ladder": [], "range_sweep": []}

    for n, rng_ in ((2, 8), (5, 8), (5, 32)):
        w = dataclasses.replace(base, signal_range=rng_)
        print(f"=== MERDİVEN n={n}, menzil={rng_} ===")
        print(f"{'kol':>10} | {'kişi-başı ömür':>14} | {'isabet':>7}")
        print("-" * 40)
        res = {}
        for lvl in LEVELS:
            ww = dataclasses.replace(w, event_every=0) if lvl == "none" else w
            r = sweep(lvl, ww, a.episodes, n_agents=n)
            r.update(n_agents=n, signal_range=rng_)
            res[lvl] = r
            out["ladder"].append(r)
            print(f"{lvl:>10} | {r['median_lifespan']:>14.0f} | "
                  f"{str(r['hit_rate']):>7}")
        d, g = res["deaf"]["median_lifespan"], res["god"]["median_lifespan"]
        o, t = res["own"]["median_lifespan"], res["told"]["median_lifespan"]
        c = {"n_agents": n, "signal_range": rng_, "value_god_over_deaf": g / d,
             "necessity_own_share": (o - d) / (g - d),
             "sufficiency_told_share": (t - d) / (g - d),
             "lock1_own_infer_equals_own":
                 res["own_infer"]["median_lifespan"] == o}
        out.setdefault("criteria", []).append(c)
        print(f"  (i) değer {c['value_god_over_deaf']:.2f} | "
              f"(ii) gereklilik {c['necessity_own_share']:.3f} | "
              f"(iii) yeterlilik {c['sufficiency_told_share']:.3f}\n")

    print("=== MENZİL KALİBRASYONU (n=5) ===")
    print(f"{'menzil':>7} | {'told ömür':>9} | {'isabet':>7}")
    print("-" * 30)
    for rng_ in (8, 12, 16, 20, 24, 32):
        w = dataclasses.replace(base, signal_range=rng_)
        r = sweep("told", w, a.episodes, n_agents=5)
        r.update(signal_range=rng_, n_agents=5)
        out["range_sweep"].append(r)
        print(f"{rng_:>7} | {r['median_lifespan']:>9.0f} | "
              f"{str(r['hit_rate']):>7}")

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nyazıldı: {a.out}")


if __name__ == "__main__":
    main()
