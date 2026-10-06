"""Temsil dondurma pipeline'ı — P1 prob girdisi (analiz S2'nin işi).

Anayasa md. "problar eğitime karışmaz": burada yakalanan her tensör anında
detach edilip numpy'a KOPYALANIR; kayıttan ajana geri giden hiçbir yol
yoktur (numpy kopyası gradyan taşıyamaz). Sızıntısızlık testi:
tests/test_snapshot.py::test_recording_does_not_touch_training
(kayıtlı ve kayıtsız eğitim → bit-eş ağırlık hash'i).

Kayıt içeriği (tur başına):
  h            — GRU hidden state (prob girdisi)
  energy, pos  — ajanın gerçek iç/fiziksel durumu (P1 hedef (b) ground truth)
  action, turn — bağlam
  world_hash   — her kaydın hangi dünya durumuna ait olduğunun kanıtı
                 (Beş Kapı / KAPI 5: bit-eş tekrar denetimi)
"""

import json

import numpy as np


class SnapshotRecorder:
    def __init__(self, stride: int = 1, hash_every: int = 250):
        self.stride = stride
        self.hash_every = hash_every  # world.state_hash pahalı; seyrek al
        self.rows = {"turn": [], "h": [], "energy": [], "pos": [], "action": []}
        self.world_hashes: list[tuple[int, str]] = []
        self.start_pos = None
        self.world_config = None
        self._count = 0

    def note_start(self, world) -> None:
        """Epizot başlangıcı: spawn konumu + dünya config damgası (M-10)."""
        import dataclasses
        self.start_pos = world.entity_pos[0].copy()
        self.world_config = dataclasses.asdict(world.cfg)

    def capture(self, world, agent, homeo, action: int) -> None:
        self._count += 1
        if self._count % self.stride:
            return
        h = agent.h
        h_np = (np.zeros(agent.cfg.memory_dim, dtype=np.float32) if h is None
                else h.detach().cpu().numpy().reshape(-1).copy())
        self.rows["turn"].append(world.turn)
        self.rows["h"].append(h_np)
        self.rows["energy"].append(float(homeo.energy))
        self.rows["pos"].append(world.entity_pos[0].copy())
        self.rows["action"].append(action)
        if self._count % self.hash_every == 0:
            self.world_hashes.append((world.turn, world.state_hash()))

    def save(self, path: str, agent, extra_meta: dict | None = None) -> None:
        import dataclasses
        meta = {
            "n_frames": len(self.rows["turn"]),
            "stride": self.stride,
            "memory_dim": agent.cfg.memory_dim,
            "obs_radius": agent.cfg.obs_radius,
            "agent_config": dataclasses.asdict(agent.cfg),  # replay sadakati
            "world_config": self.world_config,              # M-10 damgası
            "start_pos": (None if self.start_pos is None
                          else self.start_pos.tolist()),
            "agent_weight_hash": agent.core.weight_hash(),
            "world_hashes": self.world_hashes,
            **(extra_meta or {}),
        }
        np.savez_compressed(
            path,
            turn=np.array(self.rows["turn"], dtype=np.int64),
            h=np.stack(self.rows["h"]) if self.rows["h"] else np.zeros((0, 0)),
            energy=np.array(self.rows["energy"], dtype=np.float64),
            pos=np.stack(self.rows["pos"]) if self.rows["pos"] else np.zeros((0, 2)),
            action=np.array(self.rows["action"], dtype=np.int64),
            meta=np.frombuffer(json.dumps(meta).encode(), dtype=np.uint8),
        )


def load(path: str) -> dict:
    data = np.load(path)
    out = {k: data[k] for k in ("turn", "h", "energy", "pos", "action")}
    out["meta"] = json.loads(bytes(data["meta"]).decode())
    return out
