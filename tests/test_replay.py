"""Replay kayıt/yükleme ve viewer render'ının duman testi."""

import numpy as np

from replay import recorder as rec
from replay.viewer import _render_frame, record
from world.config import WorldConfig
from world.grid import N_ACTIONS, World


def test_record_load_roundtrip(tmp_path):
    path = str(tmp_path / "demo.npz")
    record(path, turns=300, seed=42, stride=10, n_entities=5)
    data = rec.load(path)
    assert len(data["turns"]) == 31  # tur 0 + her 10 turda bir
    assert int(data["turns"][-1]) == 300
    assert data["entity"].shape == (31, 5, 2)
    assert data["meta"]["seed"] == 42
    assert len(data["meta"]["final_state_hash"]) == 64


def test_record_is_deterministic(tmp_path):
    p1, p2 = str(tmp_path / "r1.npz"), str(tmp_path / "r2.npz")
    record(p1, turns=200, seed=42, stride=1, n_entities=5)
    record(p2, turns=200, seed=42, stride=1, n_entities=5)
    d1, d2 = rec.load(p1), rec.load(p2)
    assert d1["meta"]["final_state_hash"] == d2["meta"]["final_state_hash"]
    assert np.array_equal(d1["entity"], d2["entity"])
    assert np.array_equal(d1["res_a"], d2["res_a"])


def test_render_frame_smoke(tmp_path):
    path = str(tmp_path / "demo.npz")
    record(path, turns=600, seed=42, stride=100, n_entities=5)
    data = rec.load(path)
    out = _render_frame(data, len(data["turns"]) - 1, color=False)
    lines = out.splitlines()
    assert len(lines) == 65  # başlık + 64 satır
    assert all(len(line) == 64 for line in lines[1:])
    assert "B" in out and "a" in out  # kaynaklar görünür
    # tur 600 > 500: tehlike doğmuş ve (ömür 250) hâlâ canlı olmalı
    assert "!" in out
