"""S2 veri üretimi + P1 prob makinesi testleri."""

import glob

import numpy as np

from agent.config import a2_config
from probes.p1_self_model import (probe_loeo, replay_twins,
                                  unwrap_displacement)
from training.gen_s2_data import run_curriculum
from training.snapshot import load as load_snap

TINY_PHASES = [(48, 250), (12, 250)]
TINY_CKPTS = [0, 250]


def test_checkpoints_zero_touch(tmp_path):
    # Checkpoint değerlendirmesi (eval_clone + snapshot) eğitim gidişatını
    # DEĞİŞTİREMEZ: snapshot'lı ve snapshot'sız koşum bit-eş ağırlık vermeli.
    a_with = run_curriculum(0, TINY_PHASES, TINY_CKPTS, eval_episodes=1,
                            cap=120, out_dir=str(tmp_path))
    a_without = run_curriculum(0, TINY_PHASES, TINY_CKPTS, eval_episodes=1,
                               cap=120, out_dir=None)
    assert a_with.core.weight_hash() == a_without.core.weight_hash(), \
        "checkpoint değerlendirmesi eğitime dokundu — zero-touch ihlali!"


def test_replay_fidelity(tmp_path):
    # replay_twins pozisyon/enerji sadakatini içeride assert eder;
    # burada uçtan uca gerçek bir snapshot üzerinde koşturuyoruz.
    run_curriculum(1, TINY_PHASES, TINY_CKPTS, eval_episodes=1,
                   cap=120, out_dir=str(tmp_path))
    files = glob.glob(str(tmp_path / "s2_seed1_ck250_ep0.npz"))
    assert files
    snap = load_snap(files[0])
    cfg = a2_config()
    h_twins, start = replay_twins(snap, cfg)  # sadakat bozuksa raise eder
    n = len(snap["action"])
    for ht in h_twins.values():
        assert ht.shape == (n, cfg.memory_dim)
    disp = unwrap_displacement(snap["pos"], start)
    assert np.all(np.abs(np.diff(np.vstack([[0, 0], disp]), axis=0)) <= 1), \
        "yer değiştirme adımı 1'den büyük — unwrap hatalı"


def test_probe_recovers_planted_signal():
    rng = np.random.default_rng(0)
    W_true = rng.normal(size=(64, 2))
    groups = []
    for _ in range(5):
        X = rng.normal(size=(150, 64))
        y = X @ W_true + 0.1 * rng.normal(size=(150, 2))
        groups.append((X, y))
    r2 = np.mean(probe_loeo(groups))
    assert r2 > 0.9, f"prob ekili sinyali bulamadı: R²={r2:.3f}"

    shuffled = [(X, y[rng.permutation(len(y))]) for X, y in groups]
    r2s = np.mean(probe_loeo(shuffled))
    assert r2s < 0.05, f"karıştırılmış etikette R² şanstan yüksek: {r2s:.3f}"
