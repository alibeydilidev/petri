"""Nakit testi — standart enstrüman (S2.8 iş 3).

Soru: ajan, GÖRDÜĞÜ kaynağı hasada çevirebiliyor mu? (Bilgi katmanı
calibN ile ölçülür; bu enstrüman KULLANIM katmanını ölçer — M-16.)

Protokol: kaynak tam Chebyshev d ∈ {1,2,3} mesafede (yön seed'li
rastgele), enerji 50, 12 tur bütçe, öğrenmesiz klon; hasat oldu/olmadı.
Ön-kayıtlı çıta (FINDINGS S2.8): d=1 VE d=2'de havuzlanmış oran ≥ %70.
"""

import numpy as np

from agent.homeostasis import Homeostasis
from training.loop import encode_obs
from world.grid import World


def _offset_at_chebyshev(d: int, rng: np.random.Generator) -> np.ndarray:
    """Tam Chebyshev-d ofset: bir eksen ±d, diğeri U[-d, d]."""
    while True:
        off = rng.integers(-d, d + 1, size=2)
        if np.abs(off).max() == d:
            return off


def cash_test(agent, wcfg, distances=(1, 2, 3), trials: int = 20,
              seed_base: int = 0, max_steps: int = 12,
              start_energy: float = 50.0) -> dict:
    """Dönüş: {"1": oran, "2": oran, "3": oran} (mesafe → hasat oranı)."""
    cfg = agent.cfg
    out = {}
    for d in distances:
        rng = np.random.default_rng(600_000 + seed_base * 100 + d)
        hits = 0
        for i in range(trials):
            world = World(wcfg, n_entities=1,
                          seed=int(rng.integers(0, 2**31 - 1)))
            k = int(rng.integers(0, wcfg.resource_a_count))
            world.entity_pos[0] = (world.res_a[k]
                                   + _offset_at_chebyshev(d, rng)) \
                % wcfg.grid_size
            homeo = Homeostasis(cfg)
            homeo.energy = start_energy
            clone = agent.eval_clone(eval_seed=610_000 + seed_base * 1000
                                     + d * 100 + i)
            obs = encode_obs(world.observe(0, cfg.obs_radius),
                             homeo.energy, cfg)
            for _ in range(max_steps):
                a = clone.act(obs)
                delta = world.step(np.array([a]))
                homeo.apply_turn(a, float(delta[0]))
                if delta[0] > 0:
                    hits += 1
                    break
                clone.observe_step(obs, a)
                obs = encode_obs(world.observe(0, cfg.obs_radius),
                                 max(homeo.energy, 0.0), cfg)
        out[str(d)] = hits / trials
    return out
