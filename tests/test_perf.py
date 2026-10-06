"""S0 bitti-tanımı: 10K tur < 60 sn (5 varlık, rastgele eylemler)."""

import time

import numpy as np

from world.config import WorldConfig
from world.grid import N_ACTIONS, World

def test_10k_turns_under_60s(capsys):
    n = 5
    w = World(WorldConfig(), n_entities=n, seed=42)
    acts = np.random.default_rng(7).integers(0, N_ACTIONS, size=(10_000, n))
    t0 = time.perf_counter()
    for t in range(10_000):
        w.step(acts[t])
    elapsed = time.perf_counter() - t0
    with capsys.disabled():
        print(f"\n[S0 perf] 10.000 tur, {n} varlık: {elapsed:.3f} sn "
              f"({10_000 / elapsed:,.0f} tur/sn)")
    assert elapsed < 60.0, f"10K tur {elapsed:.1f} sn — 60 sn sınırı aşıldı"
