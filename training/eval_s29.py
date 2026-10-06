"""S2.9 — PL-17 / öz-hareket hedefli: PER-uzamsal (K-110rev) + ε hareket
yanlılığı; zincir: kayma testi → nakit testi → tam eval → çatal A/B/C.

Ön-kayıtlar FINDINGS S2.9'da (çıtalar: kayma oranı > 1; nakit d≤2 ≥ %70;
eval S2.7 bitti-tanımı).

Kullanım:
  python3 -m training.eval_s29 --stage full
"""

import argparse
import dataclasses
import json
import pathlib

import numpy as np
from scipy.stats import wilcoxon

from training.cash_test import cash_test
from training.eval_s27 import (CURRICULUM_V2, HARVEST_THRESHOLD,
                               S27_OVERRIDES, WCFG,
                               measure_calibration_incontext)
from training.eval_s28 import S28_PLANNER, train_nest_agent
from training.loop import run_episode
from training.shift_test import shift_test
from world.config import config_hash

S29_DATA = dict(per_spatial_weight=4.0, eps_move_bias=0.5)  # K-110rev


def stage_full(seeds: int = 5, eval_episodes: int = 12, cap: int = 1500) -> None:
    overrides = {**S27_OVERRIDES, **S28_PLANNER, **S29_DATA}
    results = []
    for s in range(seeds):
        agent, info = train_nest_agent(s, overrides)
        cfg = agent.cfg
        st = agent.stats
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
            "seed": s, **info, "counters": st,
            "move_shift_per_10k": round(1e4 * st["move_shift"]
                                        / st["transitions"], 1),
            "shift": {k: sh[k] for k in ("correct_mass", "old_mass", "ratio")},
            "cash": cash, "calibration": calib,
            "median_harvest": float(np.median(hc)), "harvest_counts": hc,
            "median_lifetime": float(np.median(tr_l)),
            "median_stay": float(np.median(stay_l)),
            "wilcoxon_p_vs_stay": p,
        })
        print(f"[s29 seed {s}] kayma oranı {sh['ratio']:.2f} "
              f"({sh['correct_mass']:.3f}/{sh['old_mass']:.3f}) | "
              f"hareket+kayma {results[-1]['move_shift_per_10k']}/10K | "
              f"nakit d1={cash['1']:.0%} d2={cash['2']:.0%} | eval hasat "
              f"{results[-1]['median_harvest']:.1f} | yaşam "
              f"{results[-1]['median_lifetime']:.0f} vs "
              f"{results[-1]['median_stay']:.0f} p={p:.4f} | "
              f"{info['per_turn_ms']} ms/tur", flush=True)

    shift_ratio_med = float(np.median([r["shift"]["ratio"] for r in results]))
    shift_pass = shift_ratio_med > 1.0
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
    elif shift_pass and cash_pass:
        fork = "B-KESIF (K-104 yeniden acilir)"
    else:
        fork = "C-VERI-YETMEDI" if not shift_pass else "C-KAYMA-VAR-NAKIT-YOK"

    summary = {
        "data_overrides": S29_DATA, "planner": S28_PLANNER,
        "curriculum_v2": CURRICULUM_V2,
        "world_config_hash": config_hash(WCFG),
        "shift_ratio_median": shift_ratio_med, "shift_pass": shift_pass,
        "cash_pooled": pooled, "cash_pass": cash_pass,
        "done_harvest": ok_harvest, "done_life_vs_stay": ok_life,
        "done_no_collapse": ok_collapse, "eval_pass": eval_pass,
        "fork": fork, "results": results,
    }
    with open("runs/s29_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nS2.9: kayma medyan oran {shift_ratio_med:.2f} (çıta >1) "
          f"{'✓' if shift_pass else '✗'} | nakit d1={pooled['1']:.0%} "
          f"d2={pooled['2']:.0%} {'✓' if cash_pass else '✗'} | "
          f"eval {'✓' if eval_pass else '✗'} | ÇATAL: {fork}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=("full",))
    a = ap.parse_args()
    pathlib.Path("runs").mkdir(exist_ok=True)
    stage_full()


if __name__ == "__main__":
    main()
