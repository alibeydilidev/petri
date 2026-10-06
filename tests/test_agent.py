"""S1 organ testleri: çekirdek bütçesi/nedenselliği, homeostaz, MPC."""

import numpy as np
import torch

from agent.config import a2_config
from agent.homeostasis import Homeostasis
from agent.mpc import MPCPlanner
from agent.predictive_core import PredictiveCore, obs_dim
from world.grid import INTERACT, N_ACTIONS, STAY, UP


def test_param_budget_under_500k():
    # Dokümandaki 5 roster profili (population/ S3'te; burada sadece değerler).
    roster = [(6, 64), (3, 256), (4, 128), (5, 96), (3, 192)]
    for r, m in roster:
        core = PredictiveCore(a2_config(obs_radius=r, memory_dim=m))
        assert core.n_params() < 500_000, \
            f"obs_radius={r}, memory_dim={m}: {core.n_params()} parametre"


def test_causality_no_future_leak():
    # t <= k çıktıları, t > k girdilerinden etkilenemez.
    cfg = a2_config()
    torch.manual_seed(0)
    core = PredictiveCore(cfg)
    T, k = 12, 5
    obs = torch.randn(1, T, obs_dim(cfg))
    acts = torch.zeros(1, T, N_ACTIONS)
    acts[..., 0] = 1.0
    out1, _ = core(obs, acts)
    obs2 = obs.clone()
    obs2[:, k + 1:, :] = torch.randn_like(obs2[:, k + 1:, :])  # geleceği boz
    out2, _ = core(obs2, acts)
    assert torch.equal(out1[:, :k + 1], out2[:, :k + 1]), "gelecek sızıntısı!"
    assert not torch.equal(out1[:, k + 1:], out2[:, k + 1:])


def test_homeostasis_accounting_and_death():
    cfg = a2_config()
    h = Homeostasis(cfg)
    h.apply_turn(STAY, 0.0)
    assert h.energy == cfg.max_energy - cfg.base_metabolism
    h.apply_turn(UP, 0.0)
    assert abs(h.energy - (cfg.max_energy - 2 * cfg.base_metabolism
                           - cfg.move_energy_cost)) < 1e-9
    h.apply_turn(INTERACT, +15.0)  # hasat; tavan max_energy
    assert h.energy == cfg.max_energy
    h.energy = 1.0
    h.apply_turn(UP, 0.0)
    assert not h.alive


def test_mpc_returns_valid_action_deterministically():
    cfg = a2_config()
    torch.manual_seed(0)
    core = PredictiveCore(cfg)
    a1 = MPCPlanner(cfg, np.random.default_rng(9)).plan(
        core, None, torch.zeros(obs_dim(cfg)))
    a2 = MPCPlanner(cfg, np.random.default_rng(9)).plan(
        core, None, torch.zeros(obs_dim(cfg)))
    assert a1 == a2
    assert 0 <= a1 < N_ACTIONS


def test_mpc_prefers_energy_conserving_action_with_oracle_model():
    # Modelin enerji dinamiğini öğrendiği durumda MPC'nin hedefi doğru
    # okuduğunu doğrula: enerji tahminini elle yükselten "kukla" çekirdek.
    cfg = a2_config()

    class Oracle:
        def __call__(self, obs, act, h):
            # STAY (indeks 0) enerjiyi korur, diğerleri düşürür.
            pred = obs.clone()
            pred[..., -1] = obs[..., -1] - 0.013 + 0.01 * act[..., 0]
            return pred, h

    obs = torch.zeros(obs_dim(cfg))
    obs[-1] = 0.5
    action = MPCPlanner(cfg, np.random.default_rng(3)).plan(Oracle(), None, obs)
    assert action == STAY


def test_mpc_step4_sampler_eliminates_first_action_dilution():
    # K-109: sabit-eylem adayları + elit iyileştirme açıkken, oracle
    # altında STAY seçimi HER rng seed'inde garantidir (hep-STAY adayı
    # aday kümesinde). Kapalıyken seyreltme bazı seed'lerde hareket seçer.
    class Oracle:
        def __call__(self, obs, act, h):
            pred = obs.clone()
            pred[..., -1] = obs[..., -1] - 0.013 + 0.01 * act[..., 0]
            return pred, h

    base = dict(obs_radius=4, memory_dim=128, learning_rate=5e-4)
    cfg4 = a2_config(mpc_constant_candidates=True, mpc_cem_iters=2)
    obs = torch.zeros(obs_dim(a2_config()))
    obs[-1] = 0.5
    picks = [MPCPlanner(cfg4, np.random.default_rng(s)).plan(Oracle(), None, obs)
             for s in range(20)]
    assert all(p == STAY for p in picks), f"adım-4 örnekleyici sızdırdı: {picks}"


def test_mpc_defaults_bitcompatible_with_pre_step4():
    # Varsayılan config (iters=1, sabit adaylar kapalı) eski tek-atış
    # davranışıyla aynı rng tüketimine sahip: aynı seed → aynı eylem.
    cfg = a2_config()
    torch.manual_seed(0)
    core = PredictiveCore(cfg)
    obs = torch.zeros(obs_dim(cfg))
    a1 = MPCPlanner(cfg, np.random.default_rng(9)).plan(core, None, obs)
    rng = np.random.default_rng(9)
    seqs = rng.integers(0, N_ACTIONS, size=(cfg.mpc_candidates, cfg.mpc_horizon))
    planner = MPCPlanner(cfg, np.random.default_rng(0))
    scores = planner._score(core, None, obs, seqs)
    assert a1 == int(seqs[int(np.argmax(scores)), 0])
