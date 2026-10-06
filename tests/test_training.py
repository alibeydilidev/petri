"""Eğitim determinizmi + snapshot sızıntısızlığı (Beş Kapı KAPI 2/5 altyapısı)."""

import numpy as np

from agent.config import a2_config
from training import snapshot as snap
from training.loop import OnlineAgent, run_episode
from training.snapshot import SnapshotRecorder


def _short_train(with_snapshot: bool):
    cfg = a2_config()
    agent = OnlineAgent(cfg, torch_seed=1, np_seed=2)
    recs = []
    for ep in range(2):
        rec = SnapshotRecorder(stride=1) if with_snapshot else None
        run_episode(agent, world_seed=100 + ep, cfg=cfg, max_turns=120,
                    snapshot=rec)
        recs.append(rec)
    return agent, recs


def test_training_bit_identical_repeat():
    a1, _ = _short_train(False)
    a2, _ = _short_train(False)
    assert a1.core.weight_hash() == a2.core.weight_hash(), \
        "aynı seed'le eğitim bit-eş değil"


def test_recording_does_not_touch_training():
    # Dondurma gerçekten dondurma: kayıt açıkken ve kapalıyken eğitim
    # bit-eş ağırlık üretmeli (tek unutulmuş detach bunu bozar).
    a_plain, _ = _short_train(False)
    a_rec, _ = _short_train(True)
    assert a_plain.core.weight_hash() == a_rec.core.weight_hash(), \
        "snapshot kaydı eğitime dokundu — sızıntı!"


def test_snapshot_roundtrip(tmp_path):
    agent, recs = _short_train(True)
    p = str(tmp_path / "snap.npz")
    recs[-1].save(p, agent, {"note": "test"})
    data = snap.load(p)
    n = data["meta"]["n_frames"]
    assert n > 0
    assert data["h"].shape == (n, agent.cfg.memory_dim)
    assert data["energy"].shape == (n,)
    assert data["pos"].shape == (n, 2)
    assert data["meta"]["agent_weight_hash"] == agent.core.weight_hash()
    assert len(data["meta"]["world_hashes"]) >= 0  # meta alanı mevcut
    assert np.all(np.diff(data["turn"]) == 1)


def test_random_policy_episode_runs():
    cfg = a2_config()
    rng = np.random.default_rng(0)
    r = run_episode("random", world_seed=5, cfg=cfg, max_turns=400,
                    random_rng=rng)
    assert 0 < r["lifetime"] <= 400
