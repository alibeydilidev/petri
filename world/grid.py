"""PETRI dünya fiziği: grid + kaynak + tehlike.

Determinizm anayasaldır: tüm rastgelelik bu modül içindeki tek
numpy.random.Generator'dan (PCG64) akar. `random`, `time` veya global
`np.random` bu dosyada kullanılamaz.

S0 sınırı: burada ajan zihni yoktur. Dünya, dışarıdan eylem vektörü alan
"varlık"ların (entity) fiziksel bedenlerini yürütür ve tur başına enerji
deltaları döndürür. Metabolizma, ölüm ve öğrenme S1'in (agent/) işidir.
"""

import hashlib
import json

import numpy as np

from world.config import WorldConfig

# Eylem uzayı (fizik seviyesi): dur, 4 yön, etkileşim (hasat).
STAY, UP, DOWN, LEFT, RIGHT, INTERACT = range(6)
N_ACTIONS = 6

# (satır, sütun) delta; INTERACT hareket ettirmez.
_MOVES = np.array(
    [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [0, 0]], dtype=np.int64
)


class World:
    """Deterministik, tur bazlı 64x64 (varsayılan) toroidal grid dünya."""

    def __init__(self, config: WorldConfig | None = None, n_entities: int = 5,
                 seed: int | None = None):
        self.cfg = config if config is not None else WorldConfig()
        self.n_entities = n_entities
        self.reset(self.cfg.seed if seed is None else seed)

    # ------------------------------------------------------------------ setup

    def reset(self, seed: int) -> None:
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.turn = 0
        self.entity_pos = self._sample_cells(self.n_entities)
        self.res_a = self._sample_cells(self.cfg.resource_a_count)
        self.res_b = self._sample_cells(self.cfg.resource_b_count)
        self.hazard_pos = np.zeros((0, 2), dtype=np.int64)
        self.hazard_expires = np.zeros((0,), dtype=np.int64)
        # B senkron durumu: B başına {entity_id: son etkileşim turu}
        self.b_sync: list[dict[int, int]] = [
            {} for _ in range(self.cfg.resource_b_count)
        ]
        # Teşhis sayacı — dinamiğe girmez, state_dict/state_hash DIŞINDA
        # (last_signals emsali). Amacı: B açılışını ekolojide enerji
        # deltasından geri-çıkarmak zorunda kalmamak (katılımcı sayısı
        # değişince delta eşiği yanıltır).
        self.b_openings_total = 0
        # S3-C: asimetrik olay sistemi (PL-05 açıldı). Kapalıyken
        # (event_every=0) hiçbir duruma/hash'e dokunmaz.
        from world.events import EventSystem
        self.events = EventSystem(self.cfg, self.n_entities)

    def _sample_cells(self, count: int) -> np.ndarray:
        """Birbirinden farklı `count` hücre örnekler, (count, 2) döner."""
        flat = self.rng.choice(self.cfg.grid_size * self.cfg.grid_size,
                               size=count, replace=False)
        return np.stack(divmod(flat, self.cfg.grid_size), axis=1).astype(np.int64)

    # ------------------------------------------------------------------ physics

    def step(self, actions, signals=None) -> np.ndarray:
        """Bir tur ilerletir. `actions`: (n_entities,) int, 0..5.
        `signals` (S3): (n_entities,) int, -1=yok, 0..15=sembol. Sinyaller
        dünya DURUMUNU değiştirmez (state_hash dışı, geçici enformasyon);
        aynı turda menzildeki diğer varlıklarca `heard()` ile duyulur.
        Enerji maliyeti homeostazın işi.

        Dönüş: (n_entities,) float64 enerji deltası (hasat kazançları
        eksi tehlike emmesi). Sabit metabolizma/eylem maliyeti dünyaya
        değil homeostaza (S1) aittir.
        """
        self.last_signals = (np.full(self.n_entities, -1, dtype=np.int64)
                             if signals is None
                             else np.asarray(signals, dtype=np.int64))
        actions = np.asarray(actions, dtype=np.int64)
        if actions.shape != (self.n_entities,):
            raise ValueError(f"actions shape {actions.shape} != ({self.n_entities},)")
        if actions.min() < 0 or actions.max() >= N_ACTIONS:
            raise ValueError("action out of range")

        self.turn += 1
        deltas = np.zeros(self.n_entities, dtype=np.float64)

        self._apply_moves(actions)
        self._apply_interacts(actions, deltas)
        self._apply_hazard_drain(deltas)
        # S3-C: küresel olay — konumun rolü YOK, yalnız doğru EYLEM.
        self.events.apply_drain(self.turn, actions, deltas)
        self._scheduled_events()
        self.events.schedule(self.turn, self.rng, self._sample_cells)
        return deltas

    def _apply_moves(self, actions: np.ndarray) -> None:
        pos = self.entity_pos + _MOVES[actions]
        if self.cfg.toroidal:
            pos %= self.cfg.grid_size
        else:
            np.clip(pos, 0, self.cfg.grid_size - 1, out=pos)
        self.entity_pos = pos

    def _apply_interacts(self, actions: np.ndarray, deltas: np.ndarray) -> None:
        interactors = np.flatnonzero(actions == INTERACT)  # artan sıra → deterministik
        touched_b: set[int] = set()
        for i in interactors:
            pos = self.entity_pos[i]
            # Kaynak A: tek varlık yeter; hasat edilen A yeni hücreye taşınır (PL-02a).
            a_hits = np.flatnonzero((self.res_a == pos).all(axis=1))
            if a_hits.size:
                deltas[i] += self.cfg.resource_a_energy
                self.res_a[a_hits[0]] = self._sample_cells(1)[0]
                continue
            # Kaynak B: senkron pencere içinde >= min_agents farklı varlık gerekir.
            b_hits = np.flatnonzero((self.res_b == pos).all(axis=1))
            if b_hits.size:
                k = int(b_hits[0])
                self.b_sync[k][int(i)] = self.turn
                touched_b.add(k)

        for k in sorted(touched_b):
            sync = self.b_sync[k]
            # Pencere dışına düşen girişleri at (sync_window=2 → bu tur ve önceki).
            for eid in sorted(sync):
                if self.turn - sync[eid] > self.cfg.resource_b_sync_window - 1:
                    del sync[eid]
            if len(sync) >= self.cfg.resource_b_min_agents:
                participants = sorted(sync)
                share = self.cfg.resource_b_energy / len(participants)  # PL-02b
                for eid in participants:
                    deltas[eid] += share
                self.res_b[k] = self._sample_cells(1)[0]
                sync.clear()
                self.b_openings_total += 1  # teşhis sayacı (state dışı)

    def _apply_hazard_drain(self, deltas: np.ndarray) -> None:
        if not self.hazard_pos.shape[0]:
            return
        # Toroidal Chebyshev mesafe: her varlık x her tehlike.
        d = np.abs(self.entity_pos[:, None, :] - self.hazard_pos[None, :, :])
        if self.cfg.toroidal:
            d = np.minimum(d, self.cfg.grid_size - d)
        inside = (d.max(axis=2) <= self.cfg.hazard_radius).any(axis=1)
        deltas[inside] -= self.cfg.hazard_drain_per_turn

    def _scheduled_events(self) -> None:
        # Kaynak A drift'i: tüm A kaynakları yeni hücrelere.
        if self.turn % self.cfg.resource_a_drift_every == 0:
            self.res_a = self._sample_cells(self.cfg.resource_a_count)
        # Tehlike ömrü doldu mu?
        alive = self.hazard_expires > self.turn
        self.hazard_pos = self.hazard_pos[alive]
        self.hazard_expires = self.hazard_expires[alive]
        # Yeni tehlike doğumu.
        if self.turn % self.cfg.hazard_spawn_every == 0:
            center = self._sample_cells(1)
            self.hazard_pos = np.concatenate([self.hazard_pos, center])
            self.hazard_expires = np.concatenate([
                self.hazard_expires,
                np.array([self.turn + self.cfg.hazard_duration], dtype=np.int64),
            ])

    def respawn_entity(self, entity_id: int) -> None:
        """Bir varlığın bedenini yeni bir hücreye taşır (S3 halefiyeti).

        Rastgelelik dünyanın TEK generator'ından akar (anayasa). S3 ilk
        nefes koşumunda halef doğum yeri dünya DIŞINDAKİ bir rng'den
        çekiliyordu; koşum tekrarlanabilirdi ama dünya durumu artık
        (world_seed, eylem dizisi)'nin fonksiyonu değildi — ekolojinin
        state_hash denetimi dünya seed'inden yeniden kurulamıyordu.
        """
        self.entity_pos[entity_id] = self._sample_cells(1)[0]

    # ------------------------------------------------------------------ signals

    def heard(self, entity_id: int, range_: int) -> list[tuple[int, int]]:
        """Bu tur menzil içinde duyulan sinyaller: [(gönderen, sembol)].
        Kendi sinyalini duymaz (PL-21). Deterministik sıra (id artan)."""
        sig = getattr(self, "last_signals", None)
        if sig is None:
            return []
        out = []
        me = self.entity_pos[entity_id]
        g = self.cfg.grid_size
        for j in range(self.n_entities):
            if j == entity_id or sig[j] < 0:
                continue
            d = np.abs(self.entity_pos[j] - me)
            if self.cfg.toroidal:
                d = np.minimum(d, g - d)
            if d.max() <= range_:
                out.append((j, int(sig[j])))
        return out

    # ------------------------------------------------------------------ observation

    # Gözlem kanal sırası (KERNEL_BUDGET K-101: kanal ayrımı bir prior'dır).
    OBS_CHANNELS = ("res_a", "res_b", "hazard", "entity")

    def observe(self, entity_id: int, radius: int) -> np.ndarray:
        """Ajan-merkezli, menzil-kısıtlı gözlem: (4, 2r+1, 2r+1) float32.

        Kanallar: kaynak A, kaynak B, tehlike bölgesi, diğer varlıklar.
        Merkez hücre gözlemcinin kendisidir; kendi bedeni entity
        kanalına YAZILMAZ (kendilik bilgisi gözleme gömülmez — öz-model
        problarla aranacak, verilmeyecek).
        """
        g = self.cfg.grid_size
        w = 2 * radius + 1
        cy, cx = self.entity_pos[entity_id]
        ys = (np.arange(cy - radius, cy + radius + 1)) % g
        xs = (np.arange(cx - radius, cx + radius + 1)) % g
        obs = np.zeros((4, w, w), dtype=np.float32)

        def paint(channel: int, cells: np.ndarray) -> None:
            for (y, x) in cells:
                dy = (y - cy + radius) % g
                dx = (x - cx + radius) % g
                if 0 <= dy < w and 0 <= dx < w:
                    obs[channel, dy, dx] = 1.0

        paint(0, self.res_a)
        paint(1, self.res_b)
        others = np.delete(self.entity_pos, entity_id, axis=0)
        paint(3, others)
        # Tehlike: merkez değil, bölge (Chebyshev yarıçapı) boyanır.
        for k in range(self.hazard_pos.shape[0]):
            hy, hx = self.hazard_pos[k]
            dy = np.abs(ys - hy)
            dy = np.minimum(dy, g - dy) if self.cfg.toroidal else dy
            dx = np.abs(xs - hx)
            dx = np.minimum(dx, g - dx) if self.cfg.toroidal else dx
            mask = (dy[:, None] <= self.cfg.hazard_radius) & \
                   (dx[None, :] <= self.cfg.hazard_radius)
            obs[2][mask] = 1.0
        # S3-C / PL-27(c): olay öncüsü AYRI KANAL AÇMADAN tehlike
        # kanalına yazılır (sıfır yeni prior biti). Ajan-merkezli ve
        # ÖZELdir — "her ajana olayın farklı parçası". Ayırt etme işi
        # ajanda: öncü yalıtık hücre, enerji çekmez, yalnız uyarı
        # penceresinde yanar.
        for dy_, dx_ in self.events.percept_cells(entity_id, self.turn):
            y, x = radius + dy_, radius + dx_
            if 0 <= y < w and 0 <= x < w:
                obs[2, y, x] = 1.0
        return obs

    # ------------------------------------------------------------------ state

    def state_dict(self) -> dict:
        """Dünyanın TAM durumu (RNG dahil). JSON-serileştirilebilir.

        Olay durumu YALNIZ olaylar açıkken eklenir — kapalıyken S0'dan
        beri kayıtlı hash'ler (ör. 23679df4...) bit-eş korunur."""
        extra = {"events": self.events.state_dict()} if self.events.enabled \
            else {}
        return {
            **extra,
            "seed": self.seed,
            "turn": self.turn,
            "n_entities": self.n_entities,
            "entity_pos": self.entity_pos.tolist(),
            "res_a": self.res_a.tolist(),
            "res_b": self.res_b.tolist(),
            "hazard_pos": self.hazard_pos.tolist(),
            "hazard_expires": self.hazard_expires.tolist(),
            "b_sync": [sorted(d.items()) for d in self.b_sync],
            "rng": _jsonable(self.rng.bit_generator.state),
        }

    def load_state(self, state: dict) -> None:
        if state["n_entities"] != self.n_entities:
            raise ValueError("n_entities mismatch")
        self.seed = state["seed"]
        self.turn = state["turn"]
        self.entity_pos = np.array(state["entity_pos"], dtype=np.int64).reshape(-1, 2)
        self.res_a = np.array(state["res_a"], dtype=np.int64).reshape(-1, 2)
        self.res_b = np.array(state["res_b"], dtype=np.int64).reshape(-1, 2)
        self.hazard_pos = np.array(state["hazard_pos"], dtype=np.int64).reshape(-1, 2)
        self.hazard_expires = np.array(state["hazard_expires"], dtype=np.int64)
        self.b_sync = [dict((int(k), int(v)) for k, v in items)
                       for items in state["b_sync"]]
        if "events" in state:
            self.events.load_state(state["events"])
        rng_state = json.loads(json.dumps(state["rng"]))
        rng_state["state"]["state"] = int(rng_state["state"]["state"])
        rng_state["state"]["inc"] = int(rng_state["state"]["inc"])
        self.rng = np.random.default_rng(0)
        self.rng.bit_generator.state = rng_state

    def state_hash(self) -> str:
        """Tam durumun SHA-256'sı. Bit-eş determinizm iddiasının ölçüsü."""
        blob = json.dumps(self.state_dict(), sort_keys=True).encode()
        return hashlib.sha256(blob).hexdigest()


def _jsonable(obj):
    """PCG64 state sözlüğündeki numpy/int128 değerleri JSON'a uygun hale getirir."""
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (np.integer,)):
        return int(obj)
    return obj
