"""Fizik birim testleri: hareket/sarma, kaynak A/B, tehlike, drift."""

import numpy as np

from world.config import WorldConfig
from world.grid import DOWN, INTERACT, LEFT, RIGHT, STAY, UP, World

N = 5
STAY_ALL = np.zeros(N, dtype=np.int64)


def _world(**cfg_kw) -> World:
    return World(WorldConfig(**cfg_kw), n_entities=N, seed=42)


def _park_all(w: World, far=(50, 50)) -> None:
    """Tüm varlıkları kaynak/tehlikeden uzak sabit hücreye koy."""
    w.entity_pos[:] = far
    w.res_a[:] = (10, 10)
    # B kaynakları ayrı hücrelere: testler (20,20)'deki res_b[0]'ı kullanır.
    w.res_b[:] = [(20, 20 + 3 * k) for k in range(len(w.res_b))]
    w.hazard_pos = np.zeros((0, 2), dtype=np.int64)
    w.hazard_expires = np.zeros((0,), dtype=np.int64)


def test_toroidal_wrap():
    w = _world()
    _park_all(w)
    w.entity_pos[0] = (0, 0)
    acts = STAY_ALL.copy()
    acts[0] = UP
    w.step(acts)
    assert tuple(w.entity_pos[0]) == (63, 0)
    acts[0] = LEFT
    w.step(acts)
    assert tuple(w.entity_pos[0]) == (63, 63)
    acts[0] = DOWN
    w.step(acts)
    acts[0] = RIGHT
    w.step(acts)
    assert tuple(w.entity_pos[0]) == (0, 0)


def test_nontoroidal_clips():
    w = _world(toroidal=False)
    _park_all(w)
    w.entity_pos[0] = (0, 5)
    acts = STAY_ALL.copy()
    acts[0] = UP
    w.step(acts)
    assert tuple(w.entity_pos[0]) == (0, 5)


def test_resource_a_harvest_and_relocate():
    w = _world()
    _park_all(w)
    w.res_a[0] = (5, 5)
    w.entity_pos[0] = (5, 5)
    acts = STAY_ALL.copy()
    acts[0] = INTERACT
    deltas = w.step(acts)
    assert deltas[0] == w.cfg.resource_a_energy
    assert not ((w.res_a == (5, 5)).all(axis=1)).any(), "hasat edilen A taşınmadı"
    assert len(w.res_a) == w.cfg.resource_a_count


def test_resource_b_single_agent_fails():
    w = _world()
    _park_all(w)
    w.entity_pos[0] = (20, 20)
    acts = STAY_ALL.copy()
    acts[0] = INTERACT
    deltas = w.step(acts)
    assert deltas[0] == 0.0
    assert ((w.res_b == (20, 20)).all(axis=1)).any(), "B tek ajanla açılmamalı"


def test_resource_b_two_agents_same_turn():
    w = _world()
    _park_all(w)
    w.entity_pos[0] = (20, 20)
    w.entity_pos[1] = (20, 20)
    acts = STAY_ALL.copy()
    acts[0] = acts[1] = INTERACT
    deltas = w.step(acts)
    share = w.cfg.resource_b_energy / 2
    assert deltas[0] == share and deltas[1] == share
    assert not ((w.res_b == (20, 20)).all(axis=1)).any(), "açılan B taşınmadı"


def test_resource_b_sync_window():
    # sync_window=2: ardışık iki turdaki etkileşimler sayılır.
    w = _world()
    _park_all(w)
    w.entity_pos[0] = (20, 20)
    w.entity_pos[1] = (20, 20)
    acts = STAY_ALL.copy()
    acts[0] = INTERACT
    d1 = w.step(acts)
    assert d1.sum() == 0.0
    acts = STAY_ALL.copy()
    acts[1] = INTERACT
    d2 = w.step(acts)
    assert d2[0] == d2[1] == w.cfg.resource_b_energy / 2


def test_resource_b_outside_window_fails():
    # Aradaki boş tur pencereyi (2) aşar: t ve t+2 senkron sayılmaz.
    w = _world()
    _park_all(w)
    w.entity_pos[0] = (20, 20)
    w.entity_pos[1] = (20, 20)
    acts = STAY_ALL.copy()
    acts[0] = INTERACT
    w.step(acts)
    w.step(STAY_ALL)  # boş tur
    acts = STAY_ALL.copy()
    acts[1] = INTERACT
    d = w.step(acts)
    assert d.sum() == 0.0
    assert ((w.res_b == (20, 20)).all(axis=1)).any()


def test_hazard_drain_inside_not_outside():
    w = _world()
    _park_all(w)
    w.hazard_pos = np.array([[30, 30]], dtype=np.int64)
    w.hazard_expires = np.array([10_000], dtype=np.int64)
    w.entity_pos[0] = (30 + w.cfg.hazard_radius, 30)      # sınırda: içeride
    w.entity_pos[1] = (30 + w.cfg.hazard_radius + 2, 30)  # dışarıda (adım sonrası da)
    deltas = w.step(STAY_ALL)
    assert deltas[0] == -w.cfg.hazard_drain_per_turn
    assert deltas[1] == 0.0


def test_hazard_spawn_and_expiry():
    w = _world(hazard_spawn_every=10, hazard_duration=5)
    _park_all(w)
    for _ in range(10):
        w.step(STAY_ALL)
    assert w.hazard_pos.shape[0] == 1, "tur 10'da tehlike doğmalı"
    for _ in range(5):
        w.step(STAY_ALL)
    assert w.hazard_pos.shape[0] == 0, "tur 15'te tehlike ölmeli"


def test_resource_a_drift():
    w = _world()
    _park_all(w)
    before = w.res_a.copy()
    for _ in range(w.cfg.resource_a_drift_every):
        w.step(STAY_ALL)
    assert not np.array_equal(before, w.res_a), "A kaynakları drift etmedi"
    assert len(w.res_a) == w.cfg.resource_a_count
