"""S0 anayasal test: aynı seed → bit-eş simülasyon.

FINDINGS.md Beş Kapı / KAPI 5'in altyapısı budur: pozitif bulgu iddiası
sıfırdan koşumda aynı turda aynı hash'i üretmek zorunda.
"""

import numpy as np

from world.config import WorldConfig
from world.grid import N_ACTIONS, World

TURNS = 3000
CHECK_EVERY = 250
N = 5


def _action_stream(seed: int, turns: int, n: int) -> np.ndarray:
    return np.random.default_rng(seed).integers(0, N_ACTIONS, size=(turns, n))


def _run(world_seed: int, action_seed: int, turns: int = TURNS):
    w = World(WorldConfig(), n_entities=N, seed=world_seed)
    acts = _action_stream(action_seed, turns, N)
    hashes = {}
    for t in range(turns):
        w.step(acts[t])
        if w.turn % CHECK_EVERY == 0:
            hashes[w.turn] = w.state_hash()
    return w, hashes


def test_same_seed_bit_identical():
    w1, h1 = _run(world_seed=42, action_seed=7)
    w2, h2 = _run(world_seed=42, action_seed=7)
    assert h1 == h2, "aynı seed + aynı eylemler bit-eş değil"
    assert w1.state_hash() == w2.state_hash()


def test_different_world_seed_diverges():
    w1, _ = _run(world_seed=42, action_seed=7, turns=500)
    w2, _ = _run(world_seed=43, action_seed=7, turns=500)
    assert w1.state_hash() != w2.state_hash()


def test_hash_covers_rng_state():
    # Adım atmadan yalnız RNG'yi ilerletmek bile hash'i değiştirmeli;
    # yoksa "bit-eş" iddiası RNG'yi dışarıda bırakır.
    w = World(WorldConfig(), n_entities=N, seed=42)
    h0 = w.state_hash()
    w.rng.integers(0, 10)
    assert w.state_hash() != h0


def test_snapshot_resume_bit_identical():
    # 500 tur koş, durumu al; kesintisiz devamla, geri-yüklenmiş kopyanın
    # devamı bit-eş olmalı (S5 uzun koşum/checkpoint güvencesi).
    acts = _action_stream(7, 1000, N)
    w1 = World(WorldConfig(), n_entities=N, seed=42)
    for t in range(500):
        w1.step(acts[t])
    snap = w1.state_dict()

    w2 = World(WorldConfig(), n_entities=N, seed=0)
    w2.load_state(snap)
    assert w2.state_hash() == w1.state_hash()

    for t in range(500, 1000):
        w1.step(acts[t])
        w2.step(acts[t])
    assert w1.state_hash() == w2.state_hash()
