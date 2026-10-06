"""S2.10 — K-113 (evrişimli decoder) zinciri: kayma → nakit → tam eval.

Tek-ajan mühendisliğinin SON sprinti. Ön-kayıt FINDINGS S2.10:
çatal A (zincir tamam → PL-13), B (kayma>1, nakit/eval çökük →
planlayıcı; K-112 karşı-olgusal yeniden ölçüm), C (kayma ≤1 → DP-05
Ali'ye; yeni müdahale önerisi YOK — vade doldu).

Kullanım: python3 -m training.eval_s210 --stage full
"""

import argparse
import json
import pathlib

import numpy as np
from scipy.stats import wilcoxon

from training.cash_test import cash_test
from training.eval_s27 import (CURRICULUM_V2, HARVEST_THRESHOLD,
                               S27_OVERRIDES, WCFG,
                               measure_calibration_incontext)
from training.eval_s28 import S28_PLANNER, train_nest_agent
from training.eval_s29 import S29_DATA
from training.loop import run_episode
from training.shift_test import shift_test
from world.config import config_hash

S210_OVERRIDES = {**S27_OVERRIDES, **S28_PLANNER, **S29_DATA,
                  "decoder_type": "conv"}  # K-113


def stage_full(seeds: int = 5, eval_episodes: int = 12, cap: int = 1500) -> None:
    results = []
    for s in range(seeds):
        agent, info = train_nest_agent(s, S210_OVERRIDES)
        cfg = agent.cfg
        sh = shift_test(agent, WCFG, seed_base=s)
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
        stay_l = [r["lifetime"] for r in st_rows]
        hc = [r["harvest_count"] for r in tr_rows]
        try:
            p = float(wilcoxon(tr_l, stay_l, alternative="greater").pvalue)
        except ValueError:
            p = 1.0
        results.append({
            "seed": s, **info, "counters": agent.stats,
            "shift": {k: sh[k] for k in ("correct_mass", "old_mass", "ratio")},
            "cash": cash, "calibration": calib,
            "median_harvest": float(np.median(hc)), "harvest_counts": hc,
            "median_lifetime": float(np.median(tr_l)),
            "median_stay": float(np.median(stay_l)),
            "wilcoxon_p_vs_stay": p,
        })
        print(f"[s210 seed {s}] kayma {sh['ratio']:.2f} "
              f"({sh['correct_mass']:.3f}/{sh['old_mass']:.3f}) | nakit "
              f"d1={cash['1']:.0%} d2={cash['2']:.0%} d3={cash['3']:.0%} | "
              f"eval hasat {results[-1]['median_harvest']:.1f} | yaşam "
              f"{results[-1]['median_lifetime']:.0f} vs "
              f"{results[-1]['median_stay']:.0f} p={p:.4f} | kalib "
              f"{calib:+.3f} | {info['per_turn_ms']} ms/tur", flush=True)

    shift_med = float(np.median([r["shift"]["ratio"] for r in results]))
    shift_pass = shift_med > 1.0
    pooled = {d: float(np.mean([r["cash"][d] for r in results]))
              for d in ("1", "2", "3")}
    cash_pass = pooled["1"] >= 0.70 and pooled["2"] >= 0.70
    med_of_med = float(np.median([r["median_lifetime"] for r in results]))
    ok_harvest = all(r["median_harvest"] >= HARVEST_THRESHOLD for r in results)
    ok_life = all(r["wilcoxon_p_vs_stay"] < 0.05 for r in results)
    ok_collapse = all(r["median_lifetime"] >= 0.5 * med_of_med
                      for r in results)
    eval_pass = ok_harvest and ok_life and ok_collapse
    if shift_pass and cash_pass and eval_pass:
        fork = "A"
    elif shift_pass:
        fork = "B-PLANLAYICI (K-112 karşı-olgusal yeniden ölçüm)"
    else:
        fork = "C-DP05 (vade doldu)"
    summary = {"overrides": S210_OVERRIDES, "curriculum_v2": CURRICULUM_V2,
               "world_config_hash": config_hash(WCFG),
               "shift_ratio_median": shift_med, "shift_pass": shift_pass,
               "cash_pooled": pooled, "cash_pass": cash_pass,
               "done_harvest": ok_harvest, "done_life_vs_stay": ok_life,
               "done_no_collapse": ok_collapse, "eval_pass": eval_pass,
               "fork": fork, "results": results}
    with open("runs/s210_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nS2.10: kayma {shift_med:.2f} {'✓' if shift_pass else '✗'} | "
          f"nakit d1={pooled['1']:.0%} d2={pooled['2']:.0%} "
          f"{'✓' if cash_pass else '✗'} | eval {'✓' if eval_pass else '✗'} "
          f"| ÇATAL: {fork}")


# ---------------------------------------------------- K-112 karşı-olgusal

import torch

from agent.homeostasis import Homeostasis
from training.eval_s28 import load_agent
from training.loop import encode_obs
from world.grid import INTERACT, N_ACTIONS, STAY, World
from training.oracle import OraclePolicy


@torch.no_grad()
def counterfactual_decay(agent, seed_base: int = 0, trials: int = 10,
                         kmax: int = 10) -> dict:
    """K-112'nin M-17-uyumlu yeniden ölçümü: çürüme, planlayıcının
    DEĞERLENDİRDİĞİ dağılımda — yaklaşma+INTERACT dizilerinde — ölçülür.
    Taban: kalıcılık. H_eff kuralı S2.8 ön-kaydıyla aynı."""
    cfg = agent.cfg
    rng = np.random.default_rng(660_000 + seed_base)
    err_e = {k: [] for k in range(1, kmax + 1)}
    per_e = {k: [] for k in range(1, kmax + 1)}
    for d in (1, 2, 3):
        for _ in range(trials):
            world = World(WCFG, n_entities=1,
                          seed=int(rng.integers(0, 2**31 - 1)))
            kres = int(rng.integers(0, WCFG.resource_a_count))
            off = np.array([0, -d]) if rng.random() < 0.5 else np.array([-d, 0])
            world.entity_pos[0] = (world.res_a[kres] + off) % WCFG.grid_size
            homeo = Homeostasis(cfg)
            homeo.energy = 50.0
            pol = OraclePolicy(cfg.obs_radius, scan=False)
            # Gerçek devam: oracle yaklaş+hasat (+STAY dolgu), dünya GERÇEK.
            obs0 = encode_obs(world.observe(0, cfg.obs_radius),
                              homeo.energy, cfg)
            true_e, acts = [], []
            e_for_obs = homeo.energy
            for _ in range(kmax):
                grid = world.observe(0, cfg.obs_radius)
                a = pol.act_grid(grid)
                deltas = world.step(np.array([a]))
                homeo.apply_turn(a, float(deltas[0]))
                acts.append(a)
                true_e.append(max(homeo.energy, 0.0) / 100.0)
                e_for_obs = max(homeo.energy, 0.0)
            # Model: aynı eylemlerle açık-döngü rollout (h bağlamsız —
            # nakit testindeki soğuk başlangıçla uyumlu; 4 STAY bağlam).
            h = None
            stay_oh = torch.zeros(1, 1, N_ACTIONS)
            stay_oh[0, 0, STAY] = 1.0
            o = obs0.view(1, 1, -1)
            for _ in range(4):
                _, h = agent.core(o, stay_oh, h)
            for k in range(1, kmax + 1):
                a_oh = torch.zeros(1, 1, N_ACTIONS)
                a_oh[0, 0, acts[k - 1]] = 1.0
                pred, h = agent.core(o, a_oh, h)
                o = pred.clamp(0.0, 1.0)
                err_e[k].append(abs(float(pred[0, 0, -1]) - true_e[k - 1]))
                per_e[k].append(abs(float(obs0[-1]) - true_e[k - 1]))
    curve = {k: {"model_e": float(np.median(err_e[k])),
                 "persist_e": float(np.median(per_e[k]))}
             for k in range(1, kmax + 1)}
    h_eff = 0
    for k in range(1, kmax + 1):
        if curve[k]["model_e"] < curve[k]["persist_e"]:
            h_eff = k
        else:
            break
    return {"curve": curve, "h_eff_cf": h_eff}


def stage_decay_cf(seeds=(1, 2, 3)) -> None:
    pathlib.Path("runs/s210_weights").mkdir(parents=True, exist_ok=True)
    out = {"per_seed": {}}
    for s in seeds:
        path = f"runs/s210_weights/seed{s}.pt"
        agent, info = train_nest_agent(s, S210_OVERRIDES, save_path=path)
        r = counterfactual_decay(agent, seed_base=s)
        out["per_seed"][s] = {**info, **r}
        row = " ".join(f"k{k}:{v['model_e']:.4f}/{v['persist_e']:.4f}"
                       for k, v in list(r["curve"].items())[:6])
        print(f"[decay-cf seed {s}] H_eff_cf={r['h_eff_cf']} | {row} …",
              flush=True)
    out["h_eff_cf_median"] = int(np.median(
        [v["h_eff_cf"] for v in out["per_seed"].values()]))
    with open("runs/s210_decay_cf.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nH_eff_cf medyan = {out['h_eff_cf_median']}")


def stage_apply(k_star: int, seeds=(1, 2, 3)) -> None:
    """K-112 kırpmasını KAYDEDİLMİŞ ağırlıklar üzerinde uygula: salt
    planlama değişimi, ağırlık aynı — hızlı planlayıcı-katmanı testi."""
    rows = []
    for s in seeds:
        agent = load_agent(f"runs/s210_weights/seed{s}.pt",
                           cfg_overrides={"mpc_score_horizon": k_star})
        cash = cash_test(agent, WCFG, seed_base=s)
        rows.append({"seed": s, "cash": cash})
        print(f"[apply k*={k_star} seed {s}] nakit d1={cash['1']:.0%} "
              f"d2={cash['2']:.0%} d3={cash['3']:.0%}", flush=True)
    pooled = {d: float(np.mean([r["cash"][d] for r in rows]))
              for d in ("1", "2", "3")}
    with open("runs/s210_apply.json", "w") as f:
        json.dump({"k_star": k_star, "pooled": pooled, "rows": rows}, f,
                  indent=2)
    print(f"\nhavuz: d1={pooled['1']:.0%} d2={pooled['2']:.0%} "
          f"(çıta %70) → {'GEÇTİ' if pooled['1'] >= .7 and pooled['2'] >= .7 else 'GEÇEMEDİ'}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=("full", "decay-cf", "apply"))
    ap.add_argument("--k-star", type=int, default=None)
    a = ap.parse_args()
    pathlib.Path("runs").mkdir(exist_ok=True)
    if a.stage == "full":
        stage_full()
    elif a.stage == "decay-cf":
        stage_decay_cf()
    else:
        stage_apply(a.k_star)


if __name__ == "__main__":
    main()
