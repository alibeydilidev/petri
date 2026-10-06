"""Kayma sadakati testi — standart enstrüman (S2.9 iş 2; M-17 gereği
karşı-olgusal kullanım dağılımında koşar).

Soru: model, ÖZ-HAREKET altında egosantrik gözlem kaymasını üretiyor mu?
(S2.8 Test A'nın standartlaştırılmışı; FINDINGS "öz-hareket modeli yok"
ara sonucunun üretici-enstrüman ayağı.)

Protokol: kaynak, ajanın {UP,DOWN,LEFT,RIGHT} yönünde tam d ∈ {1,2,3}
hücre eksen-hizalı mesafede; 4 STAY bağlam adımı; kaynağa DOĞRU tek adım.
Skor: tahmini ch0 kütlesi doğru yeni göreli konumda mı (d=1 → merkez,
d>1 → aynı eksende d−1)? Ön-kayıtlı çıta (FINDINGS S2.9):
medyan(doğru-yer kütlesi) / medyan(eski-yer kütlesi) > 1
(S2.8 tabanı ≈ 0.08/0.71 ≈ 0.11).
"""

import numpy as np
import torch

from agent.homeostasis import Homeostasis
from training.loop import encode_obs
from world.grid import DOWN, LEFT, N_ACTIONS, RIGHT, STAY, UP, World

_DIR_DELTA = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


@torch.no_grad()
def shift_test(agent, wcfg, distances=(1, 2, 3), trials_per: int = 5,
               seed_base: int = 0, context_steps: int = 4,
               start_energy: float = 50.0) -> dict:
    """Dönüş: {"correct_mass", "old_mass", "ratio", "per_cell": {...}}"""
    cfg = agent.cfg
    r = cfg.obs_radius
    rng = np.random.default_rng(650_000 + seed_base)
    stay_oh = torch.zeros(1, 1, N_ACTIONS)
    stay_oh[0, 0, STAY] = 1.0

    correct_all, old_all = [], []
    per_cell = {}
    for direction in (UP, DOWN, LEFT, RIGHT):
        dy, dx = _DIR_DELTA[direction]
        for d in distances:
            cm, om = [], []
            for _ in range(trials_per):
                world = World(wcfg, n_entities=1,
                              seed=int(rng.integers(0, 2**31 - 1)))
                k = int(rng.integers(0, wcfg.resource_a_count))
                # Kaynak, ajanın `direction` yönünde d hücre ötesinde
                # olacak şekilde ajanı yerleştir.
                world.entity_pos[0] = (world.res_a[k]
                                       - d * np.array([dy, dx])) \
                    % wcfg.grid_size
                Homeostasis(cfg)  # (maliyet muhasebesi teste girmiyor)
                obs = encode_obs(world.observe(0, r), start_energy, cfg)
                h = None
                for _ in range(context_steps):
                    _, h = agent.core(obs.view(1, 1, -1), stay_oh, h)
                a_oh = torch.zeros(1, 1, N_ACTIONS)
                a_oh[0, 0, direction] = 1.0
                pred, _ = agent.core(obs.view(1, 1, -1), a_oh, h)
                grid = pred[0, 0, :-1].reshape(4, 2 * r + 1,
                                               2 * r + 1).clamp(0, 1)
                old_pos = (r + d * dy, r + d * dx)
                new_pos = (r + (d - 1) * dy, r + (d - 1) * dx)
                cm.append(float(grid[0][new_pos]))
                om.append(float(grid[0][old_pos]))
            per_cell[f"dir{direction}_d{d}"] = {
                "correct": float(np.median(cm)), "old": float(np.median(om))}
            correct_all += cm
            old_all += om
    c_med = float(np.median(correct_all))
    o_med = float(np.median(old_all))
    return {"correct_mass": c_med, "old_mass": o_med,
            "ratio": c_med / (o_med + 1e-9), "per_cell": per_cell}
