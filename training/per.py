"""K-110 — Öncelikli deneyim tekrarı (PER) tamponu.

PL-12'ye (kapalı-döngü karşı-olgusal kalibrasyon kararsızlığı) cevap:
model-kaybı orantılı örnekleme az öğrenilmiş geçişleri sıcak tutar;
hafif eylem tabakalaması (per_stratify_prob olasılıkla: rastgele bir
eylem seç, o eylemi İÇEREN pencerelerden örnekle) azınlık eylemlerin
veriden silinmesini engeller. Önem-ağırlığı (IS/β) bilinçli olarak yok —
bu DQN değil; sapma kabul edilir ve beyan edilir.

İçerik vermez: hangi eylemin "iyi" olduğunu söylemez, yalnız hangi
deneyimin tekrar görüleceğini seçer. Determinizm: adanmış numpy
Generator (ajan seed'inden türetilir).
"""

import numpy as np


class PERBuffer:
    def __init__(self, capacity: int, alpha: float,
                 rng: np.random.Generator, n_actions: int = 6):
        self.capacity = capacity
        self.alpha = alpha
        self.rng = rng
        self.n_actions = n_actions
        self.items: list = []            # (obs W×D, act W×A, tgt W×D, h0)
        self.prios = np.zeros(0)
        self.action_mask = np.zeros((0, n_actions), dtype=bool)
        self.grid_change = np.zeros(0)   # K-110rev: pencere kayma zenginliği
        self.spatial_weight = 0.0        # 0 → eski davranış bit-eş
        self._pos = 0

    def __len__(self) -> int:
        return len(self.items)

    def push(self, item, priority: float, actions_present: np.ndarray,
             grid_change: float = 0.0) -> None:
        if len(self.items) < self.capacity:
            self.items.append(item)
            self.prios = np.append(self.prios, priority)
            self.action_mask = np.vstack([self.action_mask,
                                          actions_present[None, :]])
            self.grid_change = np.append(self.grid_change, grid_change)
        else:  # halka tampon (FIFO üzerine yaz)
            self.items[self._pos] = item
            self.prios[self._pos] = priority
            self.action_mask[self._pos] = actions_present
            self.grid_change[self._pos] = grid_change
            self._pos = (self._pos + 1) % self.capacity

    def sample(self, k: int) -> tuple[np.ndarray, list]:
        n = len(self.items)
        idx = np.empty(k, dtype=np.int64)
        for i in range(k):
            pool = np.arange(n)
            if self.rng.random() < getattr(self, "stratify_prob", 0.0):
                a = int(self.rng.integers(0, self.n_actions))
                cand = np.flatnonzero(self.action_mask[:n, a])
                if cand.size:
                    pool = cand
            w = self.prios[pool] ** self.alpha + 1e-8
            if self.spatial_weight > 0.0:  # K-110rev
                w = w * (1.0 + self.spatial_weight * self.grid_change[pool])
            idx[i] = int(self.rng.choice(pool, p=w / w.sum()))
        return idx, [self.items[j] for j in idx]

    def update(self, idx: np.ndarray, priorities: np.ndarray) -> None:
        self.prios[idx] = priorities
