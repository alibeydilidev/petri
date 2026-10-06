"""S2.6 testleri: oracle politikası + PER (K-110)."""

import dataclasses

import numpy as np

from agent.config import a2_config
from training.loop import OnlineAgent, run_episode
from training.oracle import OraclePolicy
from training.per import PERBuffer
from world.config import WorldConfig
from world.grid import DOWN, INTERACT, RIGHT, UP, World


def test_oracle_walks_to_visible_resource_and_harvests():
    cfg = a2_config()
    pol = OraclePolicy(cfg.obs_radius)
    obs = np.zeros((4, 9, 9), dtype=np.float32)
    obs[0, 4, 7] = 1.0                      # 3 doğuda kaynak
    assert pol.act_grid(obs) == RIGHT
    obs2 = np.zeros((4, 9, 9), dtype=np.float32)
    obs2[0, 4, 4] = 1.0                     # üstünde
    assert pol.act_grid(obs2) == INTERACT
    obs3 = np.zeros((4, 9, 9), dtype=np.float32)
    obs3[0, 1, 4] = 1.0                     # 3 kuzeyde
    assert pol.act_grid(obs3) == UP


def test_oracle_avoids_visible_hazard_step():
    pol = OraclePolicy(4)
    obs = np.zeros((4, 9, 9), dtype=np.float32)
    obs[0, 4, 7] = 1.0                      # doğuda kaynak
    obs[2, 4, 5] = 1.0                      # ama bir doğu tehlikeli
    a = pol.act_grid(obs)
    assert a != RIGHT or obs[2, 4, 5] == 0  # alternatife sapmalı
    assert a in (UP, DOWN)


def test_oracle_scan_is_deterministic_and_covers():
    # Ekonomiyi test dışına al (m≈0): amaç determinizm + tarama kapsaması.
    cfg = a2_config(base_metabolism=0.01, move_energy_cost=0.01,
                    interact_energy_cost=0.01)
    r1 = run_episode(OraclePolicy(cfg.obs_radius), world_seed=7, cfg=cfg,
                     max_turns=600, spawn_seed=1)
    r2 = run_episode(OraclePolicy(cfg.obs_radius), world_seed=7, cfg=cfg,
                     max_turns=600, spawn_seed=1)
    assert r1 == r2
    assert r1["harvest_count"] >= 1, "oracle 600 turda tek kaynak bulamadı"


def test_per_priority_biases_sampling():
    buf = PERBuffer(10, alpha=1.0, rng=np.random.default_rng(0))
    buf.stratify_prob = 0.0
    hi = np.array([True] * 6)
    buf.push("A", priority=100.0, actions_present=hi)
    buf.push("B", priority=0.001, actions_present=hi)
    idx, items = buf.sample(200)
    assert items.count("A") > 180


def test_per_stratified_sampling_reaches_minority_action():
    buf = PERBuffer(50, alpha=1.0, rng=np.random.default_rng(0))
    buf.stratify_prob = 1.0  # hep tabakalı
    only0 = np.zeros(6, dtype=bool); only0[0] = True
    only5 = np.zeros(6, dtype=bool); only5[5] = True
    for _ in range(49):
        buf.push("çoğunluk", priority=1.0, actions_present=only0)
    buf.push("azınlık", priority=1.0, actions_present=only5)
    _, items = buf.sample(120)
    frac = items.count("azınlık") / 120
    assert frac > 0.08, f"tabakalama azınlığa ulaşmıyor: {frac:.2f}"


def test_per_training_deterministic_and_active(tmp_path):
    def train(per: bool):
        cfg = a2_config(per_enabled=per)
        agent = OnlineAgent(cfg, torch_seed=3, np_seed=4)
        for ep in range(2):
            run_episode(agent, world_seed=300 + ep, cfg=cfg, max_turns=120)
        return agent.core.weight_hash()

    h1, h2 = train(True), train(True)
    assert h1 == h2, "PER'li eğitim bit-eş değil"
    assert h1 != train(False), "PER hiçbir şey değiştirmiyor (bağlı değil mi?)"


def test_visible_a_oracle_stays_when_nothing_visible():
    from world.grid import STAY
    pol = OraclePolicy(4, scan=False)
    obs = np.zeros((4, 9, 9), dtype=np.float32)
    assert pol.act_grid(obs) == STAY
    obs[0, 4, 6] = 1.0  # görünür kaynak → yaklaşır
    assert pol.act_grid(obs) != STAY


def test_make_harvest_window_contains_harvest():
    from agent.config import a2_config as _cfg
    from training.eval_s27 import make_harvest_window
    cfg = _cfg(base_metabolism=0.6)
    rng = np.random.default_rng(5)
    item, mask = make_harvest_window(cfg, rng)
    obs, acts, tgts, h0 = item
    assert obs.shape[:2] == (1, 8) and acts.shape == (1, 8, 6)
    # pencere içinde enerji sıçraması var mı (hedef enerji boyutu artıyor)
    e = tgts[0, :, -1].numpy()
    assert (np.diff(e) > 0.2).any(), "pencerede hasat sıçraması yok"
    assert mask.any()


def test_nest_spawn_deterministic():
    from agent.config import a2_config as _cfg
    cfg = _cfg()
    r1 = run_episode("stay", world_seed=3, cfg=cfg, max_turns=50,
                     nest_rng=np.random.default_rng(9))
    r2 = run_episode("stay", world_seed=3, cfg=cfg, max_turns=50,
                     nest_rng=np.random.default_rng(9))
    assert r1 == r2


def test_k111_k112_defaults_bitcompatible():
    # K-109 geleneği: yeni bayraklar kapalıyken eski davranış bit-eş.
    import torch
    from agent.mpc import MPCPlanner
    from agent.predictive_core import PredictiveCore, obs_dim
    cfg = a2_config()  # macro=False, score_horizon=None
    torch.manual_seed(0)
    core = PredictiveCore(cfg)
    obs = torch.randn(obs_dim(cfg))
    a_new = MPCPlanner(cfg, np.random.default_rng(9)).plan(core, None, obs)
    # referans: tek atış, tam ufuk skorlaması (eski yol)
    rng = np.random.default_rng(9)
    seqs = rng.integers(0, 6, size=(cfg.mpc_candidates, cfg.mpc_horizon))
    planner = MPCPlanner(cfg, np.random.default_rng(0))
    scores = planner._score(core, None, obs, seqs)
    assert a_new == int(seqs[int(np.argmax(scores)), 0])


def test_k111_macro_candidates_present():
    import torch
    from agent.mpc import MPCPlanner
    from world.grid import UP
    cfg = a2_config(mpc_constant_candidates=True, mpc_macro_candidates=True,
                    mpc_candidates=64, mpc_cem_iters=1)
    planner = MPCPlanner(cfg, np.random.default_rng(3))
    # plan() içindeki aday inşasını taklit etmek yerine oracle ile UP-2
    # önekli makro adayın kazanabildiğini doğrula: kuzeyde 2 hücrede "iyi"
    class Oracle:  # kuzeye gidildikçe enerji artar
        def __call__(self, obs, act, h):
            pred = obs.clone()
            pred[..., -1] = obs[..., -1] + 0.05 * act[..., UP] - 0.01
            return pred, h
    from agent.predictive_core import obs_dim
    obs = torch.zeros(obs_dim(cfg)); obs[-1] = 0.5
    assert planner.plan(Oracle(), None, obs) == UP


def test_k112_score_horizon_clips():
    import torch
    from agent.mpc import MPCPlanner
    from agent.predictive_core import PredictiveCore, obs_dim
    cfg_full = a2_config()
    cfg_clip = a2_config(mpc_score_horizon=3)
    torch.manual_seed(1)
    core = PredictiveCore(cfg_full)
    obs = torch.randn(obs_dim(cfg_full))
    seqs = np.random.default_rng(5).integers(0, 6, size=(8, 10))
    s_full = MPCPlanner(cfg_full, np.random.default_rng(0))._score(
        core, None, obs, seqs)
    s_clip = MPCPlanner(cfg_clip, np.random.default_rng(0))._score(
        core, None, obs, seqs)
    assert not np.allclose(s_full, s_clip), "kırpma skorları değiştirmedi"


def test_cash_test_instrument_runs():
    from training.cash_test import cash_test
    from training.loop import OnlineAgent
    import dataclasses
    from world.config import WorldConfig
    cfg_over = dict(base_metabolism=0.6)
    from agent.config import a2_config as _a2
    agent = OnlineAgent(_a2(**cfg_over), torch_seed=1, np_seed=2)  # eğitimsiz
    wcfg = dataclasses.replace(WorldConfig(), resource_a_count=24)
    out = cash_test(agent, wcfg, trials=3, max_steps=5)
    assert set(out) == {"1", "2", "3"}
    assert all(0.0 <= v <= 1.0 for v in out.values())


def test_k110rev_defaults_bitcompatible():
    # spatial_weight=0 + eps_move_bias=0 → S2.6 PER davranışı bit-eş.
    from training.loop import OnlineAgent
    def train(**kw):
        cfg = a2_config(per_enabled=True, **kw)
        agent = OnlineAgent(cfg, torch_seed=3, np_seed=4)
        for ep in range(2):
            run_episode(agent, world_seed=300 + ep, cfg=cfg, max_turns=120)
        return agent
    a_def = train()
    a_def2 = train()
    assert a_def.core.weight_hash() == a_def2.core.weight_hash()
    a_sp = train(per_spatial_weight=4.0, eps_move_bias=0.5)
    assert a_def.core.weight_hash() != a_sp.core.weight_hash(), \
        "K-110rev hiçbir şey değiştirmiyor"


def test_k110rev_counters_track_movement():
    from training.loop import OnlineAgent
    cfg = a2_config()
    agent = OnlineAgent(cfg, torch_seed=3, np_seed=4)
    run_episode(agent, world_seed=7, cfg=cfg, max_turns=200)
    st = agent.stats
    assert st["transitions"] > 0
    assert 0 <= st["move_shift"] <= st["transitions"]
    assert 0 <= st["move_visible"] <= st["transitions"]


def test_shift_test_instrument_runs():
    import dataclasses
    from training.loop import OnlineAgent
    from training.shift_test import shift_test
    from world.config import WorldConfig
    agent = OnlineAgent(a2_config(), torch_seed=1, np_seed=2)  # eğitimsiz
    wcfg = dataclasses.replace(WorldConfig(), resource_a_count=24)
    out = shift_test(agent, wcfg, trials_per=2)
    assert set(out) >= {"correct_mass", "old_mass", "ratio"}
    assert len(out["per_cell"]) == 12  # 4 yön x 3 mesafe


def test_k113_conv_decoder_budget_and_causality():
    import torch
    from agent.predictive_core import PredictiveCore, obs_dim
    from world.grid import N_ACTIONS
    # bütçe: tüm roster profilleri conv ile de < 500K
    for r, m in [(6, 64), (3, 256), (4, 128), (5, 96), (3, 192)]:
        core = PredictiveCore(a2_config(obs_radius=r, memory_dim=m,
                                        decoder_type="conv"))
        assert core.n_params() < 500_000, f"conv ({r},{m}): {core.n_params()}"
    # nedensellik conv'da da korunur
    cfg = a2_config(decoder_type="conv")
    torch.manual_seed(0)
    core = PredictiveCore(cfg)
    T, k = 10, 4
    obs = torch.randn(1, T, obs_dim(cfg))
    acts = torch.zeros(1, T, N_ACTIONS); acts[..., 0] = 1.0
    o1, _ = core(obs, acts)
    obs2 = obs.clone(); obs2[:, k + 1:, :] = torch.randn_like(obs2[:, k + 1:, :])
    o2, _ = core(obs2, acts)
    assert torch.equal(o1[:, :k + 1], o2[:, :k + 1])


def test_k113_default_dense_bitcompatible():
    # decoder_type varsayılanı "dense": eski modül dizisi, aynı seed →
    # aynı init → bit-eş eğitim (K-109/K-110rev geleneği).
    from training.loop import OnlineAgent
    a1 = OnlineAgent(a2_config(), torch_seed=3, np_seed=4)
    a2_ = OnlineAgent(a2_config(decoder_type="dense"), torch_seed=3, np_seed=4)
    assert a1.core.weight_hash() == a2_.core.weight_hash()
    a3 = OnlineAgent(a2_config(decoder_type="conv"), torch_seed=3, np_seed=4)
    assert a1.core.weight_hash() != a3.core.weight_hash()
