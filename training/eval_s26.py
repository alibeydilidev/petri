"""S2.6 — sıralı üç iş: fizibilite oracle'ı → PER eğitimi → revize bitti-tanımı.

İş 1 (stage1): oracle ızgarası. Metabolizma {0.3, 0.6, 1.0} × kaynak
{12, 24}; oracle'ın medyan hasat ≥ 3 sağladığı EN SIKI koşul standart-eval
koşulu olarak sabitlenir. Sıkılık sıralaması (beyan): önce metabolizma
(yüksek = sıkı), sonra kaynak (az = sıkı). Hiçbiri sağlamazsa DUR.

İş 2/3 (stage2): PER'li (K-110) eğitim, oracle koşulunda; revize bitti-tanımı:
  (i)   ≥5 seed'de medyan hasat ≥ max(3, oracle_medyanı×0.4)
  (ii)  saf-tasarruf (stay) taban çizgisine karşı anlamlı yaşam uzaması
  (iii) çöküş yok: hiçbir seed'in medyan yaşamı, seed-medyanlarının
        medyanının %50'sinin altına düşmez (adım-4 patolojisi kontrolü)

Kullanım:
  python3 -m training.eval_s26 --stage 1
  python3 -m training.eval_s26 --stage 2 --metabolism M --resources N --oracle-median H
"""

import argparse
import dataclasses
import json
import pathlib
import time

import numpy as np
from scipy.stats import wilcoxon

from agent.config import a2_config
from training.loop import OnlineAgent, run_episode
from training.oracle import OraclePolicy
from world.config import WorldConfig

GRID_METAB = (1.0, 0.6, 0.3)     # sıkıdan gevşeğe
GRID_RES = (12, 24)              # azdan çoğa (az = sıkı)
EVAL_EPISODES = 12
CAP = 1500


def eval_condition(policy_name: str, metabolism: float, resources: int,
                   agent: OnlineAgent | None = None, seed_base: int = 0) -> list[dict]:
    cfg = a2_config(base_metabolism=metabolism)
    wcfg = dataclasses.replace(WorldConfig(), resource_a_count=resources)
    rows = []
    for j in range(EVAL_EPISODES):
        ws = 95_000 + seed_base * 1000 + j * 7
        sp = 70_000 + seed_base * 1000 + j * 7
        if policy_name == "oracle":
            pol = OraclePolicy(cfg.obs_radius)
        elif policy_name == "stay":
            pol = "stay"
        else:
            pol = agent.eval_clone(eval_seed=80_000 + seed_base * 100 + j)
        r = run_episode(pol, world_seed=ws, cfg=agent.cfg if agent else cfg,
                        max_turns=CAP, world_cfg=wcfg,
                        learn=False if agent else True, spawn_seed=sp)
        rows.append(r)
    return rows


def stage1() -> None:
    report = []
    for m in GRID_METAB:
        for res in GRID_RES:
            rows = eval_condition("oracle", m, res)
            hc = [r["harvest_count"] for r in rows]
            lf = [r["lifetime"] for r in rows]
            report.append({
                "metabolism": m, "resources": res,
                "median_harvest": float(np.median(hc)),
                "median_lifetime": float(np.median(lf)),
                "harvest_counts": hc, "lifetimes": lf,
                "capped": sum(r["capped"] for r in rows),
            })
            print(f"[oracle m={m} kaynak={res}] medyan hasat "
                  f"{np.median(hc):.1f} | medyan yaşam {np.median(lf):.0f} | "
                  f"tavana çarpan {report[-1]['capped']}/12", flush=True)

    # En sıkı geçerli koşul: metabolizma desc, kaynak asc sırasında ilk geçen.
    chosen = None
    for m in GRID_METAB:
        for res in GRID_RES:
            e = next(x for x in report
                     if x["metabolism"] == m and x["resources"] == res)
            if e["median_harvest"] >= 3:
                chosen = e
                break
        if chosen:
            break
    out = {"grid": report, "chosen": chosen}
    pathlib.Path("runs").mkdir(exist_ok=True)
    with open("runs/s26_oracle.json", "w") as f:
        json.dump(out, f, indent=2)
    if chosen:
        print(f"\nSEÇİLEN standart-eval koşulu: m={chosen['metabolism']} "
              f"kaynak={chosen['resources']} (oracle medyan hasat "
              f"{chosen['median_harvest']:.1f})")
    else:
        print("\nHİÇBİR koşul oracle medyan hasat >= 3 sağlamadı — DUR, "
              "dünya kalibrasyonu Ali'ye.")


def stage2(metabolism: float, resources: int, oracle_median: float,
           seeds: int, train_turns: int) -> None:
    overrides = dict(base_metabolism=metabolism, mpc_horizon=10,
                     mpc_constant_candidates=True, mpc_cem_iters=2,
                     per_enabled=True)
    wcfg = dataclasses.replace(WorldConfig(), resource_a_count=resources)
    threshold = max(3.0, 0.4 * oracle_median)
    results = []
    for s in range(seeds):
        cfg = a2_config(**overrides)
        agent = OnlineAgent(cfg, torch_seed=1000 + s, np_seed=2000 + s)
        t0 = time.perf_counter()
        total, ep = 0, 0
        while total < train_turns:
            r = run_episode(agent, world_seed=s * 10_000 + ep, cfg=cfg,
                            max_turns=CAP, world_cfg=wcfg)
            total += r["lifetime"]
            ep += 1
        train_time = time.perf_counter() - t0

        tr = eval_condition("trained", metabolism, resources, agent=agent,
                            seed_base=s)
        st = eval_condition("stay", metabolism, resources, seed_base=s)
        tr_l = [r["lifetime"] for r in tr]
        st_l = [r["lifetime"] for r in st]
        hc = [r["harvest_count"] for r in tr]
        try:
            p = float(wilcoxon(tr_l, st_l, alternative="greater").pvalue)
        except ValueError:
            p = 1.0
        results.append({
            "seed": s, "train_turns": total, "train_episodes": ep,
            "per_turn_ms": round(1000 * train_time / total, 3),
            "median_harvest": float(np.median(hc)), "harvest_counts": hc,
            "median_lifetime": float(np.median(tr_l)),
            "trained_lifetimes": tr_l, "stay_lifetimes": st_l,
            "median_stay": float(np.median(st_l)),
            "wilcoxon_p_vs_stay": p,
        })
        print(f"[s26 seed {s}] medyan hasat {results[-1]['median_harvest']:.1f} "
              f"(eşik {threshold:.1f}) | yaşam {results[-1]['median_lifetime']:.0f} "
              f"vs stay {results[-1]['median_stay']:.0f} | p={p:.4f} | "
              f"{results[-1]['per_turn_ms']} ms/tur", flush=True)

    med_of_med = float(np.median([r["median_lifetime"] for r in results]))
    ok_harvest = all(r["median_harvest"] >= threshold for r in results)
    ok_life = all(r["wilcoxon_p_vs_stay"] < 0.05 for r in results)
    ok_collapse = all(r["median_lifetime"] >= 0.5 * med_of_med for r in results)
    from world.config import config_hash
    summary = {
        "condition": {"metabolism": metabolism, "resources": resources},
        "world": dataclasses.asdict(wcfg),            # M-10 damgası
        "world_config_hash": config_hash(wcfg),
        "oracle_median": oracle_median, "harvest_threshold": threshold,
        "done_harvest": ok_harvest, "done_life_vs_stay": ok_life,
        "done_no_collapse": ok_collapse,
        "passed": ok_harvest and ok_life and ok_collapse,
        "overrides": overrides, "results": results,
    }
    with open("runs/s26_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nS2.6: hasat {ok_harvest} | yaşam-vs-stay {ok_life} | "
          f"çöküş-yok {ok_collapse} | GEÇTİ: {summary['passed']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, required=True, choices=(1, 2))
    ap.add_argument("--metabolism", type=float)
    ap.add_argument("--resources", type=int)
    ap.add_argument("--oracle-median", type=float)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--train-turns", type=int, default=45_000)
    a = ap.parse_args()
    if a.stage == 1:
        stage1()
    else:
        stage2(a.metabolism, a.resources, a.oracle_median, a.seeds,
               a.train_turns)


if __name__ == "__main__":
    main()
