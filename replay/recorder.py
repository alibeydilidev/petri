"""Replay kaydı: simülasyon durumunu tur tur .npz dosyasına biriktirir.

Kayıt eğitim/simülasyon sürecinde tutulur, izleme ayrı süreçte
(replay/viewer.py) yapılır — canlı izleme simülasyonu yavaşlatmaz.
"""

import json

import numpy as np

from world.grid import World

# Aynı anda aktif olabilecek tehlike üst sınırı (duration < spawn_every
# olduğu sürece 1'dir; config oynarsa diye pay bırakıldı). Kayıtta sabit
# genişlikli dizi için padding: pozisyon -1 = boş slot.
MAX_HAZARDS = 8


class Recorder:
    def __init__(self, world: World):
        self.world = world
        self.frames_entity = []
        self.frames_res_a = []
        self.frames_res_b = []
        self.frames_hazard = []
        self.turns = []
        self.capture()  # başlangıç durumu (tur 0)

    def capture(self) -> None:
        w = self.world
        self.turns.append(w.turn)
        self.frames_entity.append(w.entity_pos.copy())
        self.frames_res_a.append(w.res_a.copy())
        self.frames_res_b.append(w.res_b.copy())
        hz = np.full((MAX_HAZARDS, 2), -1, dtype=np.int64)
        k = min(w.hazard_pos.shape[0], MAX_HAZARDS)
        hz[:k] = w.hazard_pos[:k]
        self.frames_hazard.append(hz)

    def save(self, path: str) -> None:
        w = self.world
        meta = {
            "seed": w.seed,
            "n_entities": w.n_entities,
            "grid_size": w.cfg.grid_size,
            "hazard_radius": w.cfg.hazard_radius,
            "final_state_hash": w.state_hash(),
        }
        np.savez_compressed(
            path,
            turns=np.array(self.turns, dtype=np.int64),
            entity=np.stack(self.frames_entity),
            res_a=np.stack(self.frames_res_a),
            res_b=np.stack(self.frames_res_b),
            hazard=np.stack(self.frames_hazard),
            meta=np.frombuffer(json.dumps(meta).encode(), dtype=np.uint8),
        )


def load(path: str) -> dict:
    data = np.load(path)
    meta = json.loads(bytes(data["meta"]).decode())
    return {
        "turns": data["turns"],
        "entity": data["entity"],
        "res_a": data["res_a"],
        "res_b": data["res_b"],
        "hazard": data["hazard"],
        "meta": meta,
    }
