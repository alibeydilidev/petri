"""S2.8 — PL-17 hedefli: rollout çürüme eğrisi → K-111/K-112 → nakit testi
→ (geçerse) tam stage-2 eval → ön-kayıtlı çatal.

Kullanım:
  python3 -m training.eval_s28 --stage decay
  python3 -m training.eval_s28 --stage full [--score-horizon K]
"""

import argparse
import dataclasses
import json
import pathlib
import time

import numpy as np
import torch
from scipy.stats import wilcoxon

from agent.config import a2_config
from training.cash_test import cash_test
from training.eval_s27 import (CURRICULUM_V2, HARVEST_THRESHOLD,
                               S27_OVERRIDES, WCFG, _p_nest,
                               measure_calibration_incontext)
from training.loop import OnlineAgent, encode_obs, run_episode
from world.config import config_hash
from world.grid import N_ACTIONS, World

S28_PLANNER = dict(mpc_cem_iters=4, mpc_candidates=64,
                   mpc_macro_candidates=True)  # K-111


def train_nest_agent(seed: int, overrides: dict, train_turns: int = 45_000,
                     cap: int = 1500,
                     save_path: str | None = None) -> tuple[OnlineAgent, dict]:
    cfg = a2_config(**overrides)
    agent = OnlineAgent(cfg, torch_seed=1000 + seed, np_seed=2000 + seed)
    nest_rng = np.random.default_rng(900_000 + seed)
    t0 = time.perf_counter()
    total, ep, harvests = 0, 0, 0
    while total < train_turns:
        nested = nest_rng.random() < _p_nest(total)
        r = run_episode(agent, world_seed=seed * 10_000 + ep, cfg=cfg,
                        max_turns=cap, world_cfg=WCFG,
                        nest_rng=nest_rng if nested else None)
        total += r["lifetime"]
        harvests += r["harvest_count"]
        ep += 1
    info = {"train_turns": total, "train_episodes": ep,
            "train_harvest_events": harvests,
            "per_turn_ms": round(1000 * (time.perf_counter() - t0) / total, 3)}
    if save_path is not None:
        import dataclasses
        torch.save({"state_dict": agent.core.state_dict(),
                    "cfg": dataclasses.asdict(cfg),
                    "weight_hash": agent.core.weight_hash(),
                    "info": info}, save_path)
    return agent, info


def load_agent(path: str, cfg_overrides: dict | None = None) -> OnlineAgent:
    """Kaydedilmiş ağırlıklarla ajan kur (eval amaçlı; planner cfg'si
    override edilebilir — K-112 uygulaması gibi salt-planlama değişimleri
    ağırlıkları etkilemez)."""
    ckpt = torch.load(path, weights_only=False)
    cfg_dict = {**ckpt["cfg"], **(cfg_overrides or {})}
    agent = OnlineAgent(a2_config(**cfg_dict), torch_seed=0, np_seed=0)
    agent.core.load_state_dict(ckpt["state_dict"])
    assert agent.core.weight_hash() == ckpt["weight_hash"], \
        "yükleme bit-eş değil"
    return agent


# ---------------------------------------------------------------- stage decay

@torch.no_grad()
def rollout_decay(agent, cfg, n_episodes: int = 4, kmax: int = 10,
                  anchor_stride: int = 10, seed_base: int = 0) -> dict:
    """Açık-döngü k-adım hata eğrisi, kalıcılık tabanına karşı."""
    err_e = {k: [] for k in range(1, kmax + 1)}
    err_g = {k: [] for k in range(1, kmax + 1)}
    per_e = {k: [] for k in range(1, kmax + 1)}
    per_g = {k: [] for k in range(1, kmax + 1)}

    for j in range(n_episodes):
        ws = 95_000 + seed_base * 1000 + j * 7
        sp = 70_000 + seed_base * 1000 + j * 7
        clone = agent.eval_clone(eval_seed=80_000 + seed_base * 100 + j)
        # Epizodu kaydet: obs dizisi, eylemler, her turdaki hidden.
        from agent.homeostasis import Homeostasis
        world = World(WCFG, n_entities=1, seed=ws)
        world.entity_pos[0] = np.random.default_rng(sp).integers(
            0, WCFG.grid_size, size=2)
        homeo = Homeostasis(cfg)
        obs_seq, act_seq, h_seq = [], [], []
        obs = encode_obs(world.observe(0, cfg.obs_radius), homeo.energy, cfg)
        for t in range(400):
            a = clone.act(obs)
            d = world.step(np.array([a]))
            homeo.apply_turn(a, float(d[0]))
            obs_seq.append(obs)
            act_seq.append(a)
            h_seq.append(None if clone.h is None else clone.h.clone())
            clone.observe_step(obs, a)
            obs = encode_obs(world.observe(0, cfg.obs_radius),
                             max(homeo.energy, 0.0), cfg)
            if not homeo.alive:
                break
        obs_seq.append(obs)  # son gözlem
        n = len(act_seq)

        for t0 in range(0, n - kmax, anchor_stride):
            h = h_seq[t0]  # (obs_t0, act_t0) TÜKETİLMEDEN önceki hidden
            o = obs_seq[t0].view(1, 1, -1)
            for k in range(1, kmax + 1):
                a_oh = torch.zeros(1, 1, N_ACTIONS)
                a_oh[0, 0, act_seq[t0 + k - 1]] = 1.0
                pred, h = agent.core(o, a_oh, h)
                o = pred.clamp(0.0, 1.0)          # MPC ile aynı geri besleme
                true = obs_seq[t0 + k]
                err_e[k].append(abs(float(pred[0, 0, -1]) - float(true[-1])))
                err_g[k].append(float(((pred[0, 0, :-1] - true[:-1]) ** 2).mean()))
                base = obs_seq[t0]
                per_e[k].append(abs(float(base[-1]) - float(true[-1])))
                per_g[k].append(float(((base[:-1] - true[:-1]) ** 2).mean()))

    curve = {k: {"model_e": float(np.median(err_e[k])),
                 "persist_e": float(np.median(per_e[k])),
                 "model_grid": float(np.median(err_g[k])),
                 "persist_grid": float(np.median(per_g[k]))}
             for k in range(1, kmax + 1)}
    h_eff = 0
    for k in range(1, kmax + 1):
        if curve[k]["model_e"] < curve[k]["persist_e"]:
            h_eff = k
        else:
            break
    return {"curve": curve, "h_eff_energy": h_eff}


def stage_decay(seeds: int = 3) -> None:
    out = {"per_seed": {}}
    for s in range(seeds):
        agent, info = train_nest_agent(s, S27_OVERRIDES)
        r = rollout_decay(agent, agent.cfg, seed_base=s)
        out["per_seed"][s] = {**info, **r}
        row = "  ".join(f"k={k}:{v['model_e']:.4f}/{v['persist_e']:.4f}"
                        for k, v in list(r["curve"].items())[:5])
        print(f"[decay seed {s}] H_eff={r['h_eff_energy']} | {row} …",
              flush=True)
    h_effs = [v["h_eff_energy"] for v in out["per_seed"].values()]
    out["h_eff_median"] = int(np.median(h_effs))
    with open("runs/s28_decay.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nH_eff medyan = {out['h_eff_median']} → K-112 kırpma "
          f"{'GEREKSİZ (>=10)' if out['h_eff_median'] >= 10 else out['h_eff_median']}")


# ---------------------------------------------------------------- stage full

def stage_full(seeds: int = 5, score_horizon: int | None = None,
               eval_episodes: int = 12, cap: int = 1500) -> None:
    overrides = {**S27_OVERRIDES, **S28_PLANNER}
    if score_horizon is not None and score_horizon < 10:
        overrides["mpc_score_horizon"] = score_horizon  # K-112
    results = []
    for s in range(seeds):
        agent, info = train_nest_agent(s, overrides)
        cfg = agent.cfg
        cash = cash_test(agent, WCFG, seed_base=s)
        calib, _ = measure_calibration_incontext(
            agent, cfg, np.random.default_rng(8_500_000 + s))

        tr_rows, st_rows = [], []
        for j in range(eval_episodes):
            ws, sp = 95_000 + s * 1000 + j * 7, 70_000 + s * 1000 + j * 7
            clone = agent.eval_clone(eval_seed=80_000 + s * 100 + j)
            tr_rows.append(run_episode(clone, world_seed=ws, cfg=cfg,
                                       max_turns=cap, world_cfg=WCFG,
                                       learn=False, spawn_seed=sp))
            st_rows.append(run_episode("stay", world_seed=ws, cfg=cfg,
                                       max_turns=cap, world_cfg=WCFG,
                                       spawn_seed=sp))
        tr_l = [r["lifetime"] for r in tr_rows]
        st_l = [r["lifetime"] for r in st_rows]
        hc = [r["harvest_count"] for r in tr_rows]
        try:
            p = float(wilcoxon(tr_l, st_l, alternative="greater").pvalue)
        except ValueError:
            p = 1.0
        results.append({
            "seed": s, **info, "cash": cash, "calibration": calib,
            "median_harvest": float(np.median(hc)), "harvest_counts": hc,
            "median_lifetime": float(np.median(tr_l)),
            "median_stay": float(np.median(st_l)),
            "trained_lifetimes": tr_l, "wilcoxon_p_vs_stay": p,
        })
        print(f"[s28 seed {s}] nakit d1={cash['1']:.0%} d2={cash['2']:.0%} "
              f"d3={cash['3']:.0%} | eval hasat {results[-1]['median_harvest']:.1f} "
              f"| yaşam {results[-1]['median_lifetime']:.0f} vs "
              f"{results[-1]['median_stay']:.0f} | p={p:.4f} | "
              f"kalib {calib:+.3f} | {info['per_turn_ms']} ms/tur", flush=True)

    pooled = {d: float(np.mean([r["cash"][d] for r in results]))
              for d in ("1", "2", "3")}
    cash_pass = pooled["1"] >= 0.70 and pooled["2"] >= 0.70
    med_of_med = float(np.median([r["median_lifetime"] for r in results]))
    ok_harvest = all(r["median_harvest"] >= HARVEST_THRESHOLD for r in results)
    ok_life = all(r["wilcoxon_p_vs_stay"] < 0.05 for r in results)
    ok_collapse = all(r["median_lifetime"] >= 0.5 * med_of_med
                      for r in results)
    if cash_pass and ok_harvest and ok_life and ok_collapse:
        fork = "A"
    elif cash_pass:
        fork = "5-KESIF"   # nakit geçti, eval hasadı yok → K-104 yeniden
    else:
        fork = "B-PLANLAYICI"
    summary = {
        "planner": S28_PLANNER, "score_horizon": score_horizon,
        "curriculum_v2": CURRICULUM_V2,
        "world_config_hash": config_hash(WCFG),
        "cash_pooled": pooled, "cash_pass": cash_pass,
        "done_harvest": ok_harvest, "done_life_vs_stay": ok_life,
        "done_no_collapse": ok_collapse, "fork": fork,
        "results": results,
    }
    with open("runs/s28_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nS2.8: nakit d1={pooled['1']:.0%} d2={pooled['2']:.0%} "
          f"(çıta %70) → {'GEÇTİ' if cash_pass else 'GEÇEMEDİ'} | "
          f"eval hasat {ok_harvest} | ÇATAL: {fork}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=("decay", "full"))
    ap.add_argument("--score-horizon", type=int, default=None)
    a = ap.parse_args()
    pathlib.Path("runs").mkdir(exist_ok=True)
    if a.stage == "decay":
        stage_decay()
    else:
        stage_full(score_horizon=a.score_horizon)


if __name__ == "__main__":
    main()
