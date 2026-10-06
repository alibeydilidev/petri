"""S2.5 altyapı testleri: stay taban çizgisi, spawn randomizasyonu,
yeni-config snapshot replay sadakati."""

import glob

import numpy as np

from agent.config import a2_config
from probes.p1_self_model import replay_twins, snap_cfg
from training.gen_s2_data import run_curriculum
from training.loop import run_episode
from training.snapshot import load as load_snap


def test_stay_baseline_lifetime_matches_math():
    # Saf-tasarruf tavanı: max_energy / base_metabolism (tehlike yoksa).
    # m=1.0 → tam 100 tur. (Tehlike turu 500'de doğar; 100 < 500 güvenli.)
    cfg = a2_config(base_metabolism=1.0)
    r = run_episode("stay", world_seed=11, cfg=cfg, max_turns=1500)
    assert r["lifetime"] == 100
    assert r["harvest_count"] == 0


def test_spawn_seed_deterministic_and_varying():
    cfg = a2_config()
    r1 = run_episode("random", world_seed=5, cfg=cfg, max_turns=200,
                     random_rng=np.random.default_rng(3), spawn_seed=42)
    r2 = run_episode("random", world_seed=5, cfg=cfg, max_turns=200,
                     random_rng=np.random.default_rng(3), spawn_seed=42)
    assert r1 == r2, "aynı spawn_seed bit-eş sonuç vermedi"
    r3 = run_episode("random", world_seed=5, cfg=cfg, max_turns=200,
                     random_rng=np.random.default_rng(3), spawn_seed=43)
    assert isinstance(r3["harvest_count"], int)  # farklı spawn geçerli koşum


def test_replay_fidelity_with_overrides_and_spawn(tmp_path):
    # Yeni config (metabolizma/ufuk) + spawn randomizasyonu ile üretilen
    # snapshot, meta'daki config'le bit-eş replay edilebilmeli. Config
    # meta'ya yazılmasaydı enerji sadakat assert'i patlardı.
    run_curriculum(2, [(48, 200), (12, 200)], [0, 200], eval_episodes=2,
                   cap=100, out_dir=str(tmp_path),
                   cfg_overrides={"base_metabolism": 1.0, "mpc_horizon": 7},
                   spawn_randomize=True)
    files = glob.glob(str(tmp_path / "s2_seed2_ck200_ep*.npz"))
    assert len(files) == 2
    for f in files:
        snap = load_snap(f)
        cfg = snap_cfg(snap)
        assert cfg.base_metabolism == 1.0 and cfg.mpc_horizon == 7
        assert snap["meta"]["start_pos"] is not None
        h_twins, start = replay_twins(snap)  # sadakat bozuksa raise
        assert np.array_equal(start, np.array(snap["meta"]["start_pos"]))
