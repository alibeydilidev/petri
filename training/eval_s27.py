"""S2.7 — kalibrasyon-N + yuva müfredatı + önceden kayıtlı çatal.

İş 2 (calibN): sentetik hasat-penceresi enjeksiyonu SADECE teşhis içindir;
yuva koşumunda sentetik veri YOKTUR. N* kuralı FINDINGS'te önceden kayıtlı:
N* = medyan tahmini INTERACT−STAY ayrımının >= 0.22 olduğu en küçük N.

İş 3 (nest): p_nest tavlaması 0.7→0.3→0.1 (15K'lık üç faz), eval standart
spawn/v2/müfredatsız. Run meta'sına curriculum_v2 parametreleri (M-10).

Kullanım:
  python3 -m training.eval_s27 --stage calibN
  python3 -m training.eval_s27 --stage nest
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
from agent.homeostasis import Homeostasis
from training.loop import OnlineAgent, encode_obs, run_episode
from training.oracle import OraclePolicy
from world.config import WorldConfig, config_hash
from world.grid import INTERACT, N_ACTIONS, STAY, World

S27_OVERRIDES = dict(base_metabolism=0.6, mpc_horizon=10,
                     mpc_constant_candidates=True, mpc_cem_iters=2,
                     per_enabled=True)
WCFG = dataclasses.replace(WorldConfig(), resource_a_count=24)
CURRICULUM_V2 = {"p_nest_schedule": [[0.7, 15_000], [0.3, 15_000],
                                     [0.1, 15_000]],
                 "nest_chebyshev": 2}
TRUE_SEPARATION = 0.44   # e=50: interact (50+45-1.6)/100 - stay (50-0.6)/100
N_STAR_THRESHOLD = 0.22  # ön-kayıtlı: gerçeğin %50'si
HARVEST_THRESHOLD = 3.0  # iş-1 revizyonu: max(3, görünür-A 1.0 x 0.4)


def _onehot(a: int) -> torch.Tensor:
    v = torch.zeros(N_ACTIONS)
    v[a] = 1.0
    return v


def make_harvest_window(cfg, rng: np.random.Generator, W: int = 8):
    """Gerçek fizikle sentetik hasat penceresi: ajan kaynağın <=2
    yakınına konur, görünür-A oracle'ı yaklaşıp hasat eder."""
    while True:
        world = World(WCFG, n_entities=1,
                      seed=int(rng.integers(0, 2**31 - 1)))
        k = int(rng.integers(0, WCFG.resource_a_count))
        off = rng.integers(-2, 3, size=2)
        world.entity_pos[0] = (world.res_a[k] + off) % WCFG.grid_size
        homeo = Homeostasis(cfg)
        homeo.energy = float(rng.uniform(30, 80))
        pol = OraclePolicy(cfg.obs_radius, scan=False)
        obs_l, act_l, tgt_l = [], [], []
        e_for_obs, harvests = homeo.energy, 0
        for _ in range(W):
            grid = world.observe(0, cfg.obs_radius)
            obs_l.append(encode_obs(grid, e_for_obs, cfg))
            a = pol.act_grid(grid)
            deltas = world.step(np.array([a]))
            homeo.apply_turn(a, float(deltas[0]))
            harvests += int(deltas[0] > 0)
            act_l.append(_onehot(a))
            tgt_l.append(encode_obs(world.observe(0, cfg.obs_radius),
                                    max(homeo.energy, 0.0), cfg))
            e_for_obs = max(homeo.energy, 0.0)
        if harvests >= 1:
            item = (torch.stack(obs_l).unsqueeze(0),
                    torch.stack(act_l).unsqueeze(0),
                    torch.stack(tgt_l).unsqueeze(0), None)
            mask = np.zeros(N_ACTIONS, dtype=bool)
            mask[torch.stack(act_l).argmax(dim=-1).unique().numpy()] = True
            return item, mask


@torch.no_grad()
def measure_calibration(agent, cfg, probe_rng, n_states: int = 10):
    """Kaynak-üstü durumda INTERACT−STAY tahmini enerji ayrımı (medyan).
    Bağlam: aynı gözlemle 4 STAY adımı (statik yaklaşıklık, beyanlı)."""
    seps = []
    for _ in range(n_states):
        world = World(WCFG, n_entities=1,
                      seed=int(probe_rng.integers(0, 2**31 - 1)))
        k = int(probe_rng.integers(0, WCFG.resource_a_count))
        world.entity_pos[0] = world.res_a[k].copy()
        obs = encode_obs(world.observe(0, cfg.obs_radius), 50.0, cfg)
        h = None
        for _ in range(4):
            _, h = agent.core(obs.view(1, 1, -1),
                              _onehot(STAY).view(1, 1, -1), h)
        p_i, _ = agent.core(obs.view(1, 1, -1),
                            _onehot(INTERACT).view(1, 1, -1), h)
        p_s, _ = agent.core(obs.view(1, 1, -1),
                            _onehot(STAY).view(1, 1, -1), h)
        seps.append(float(p_i[0, 0, -1] - p_s[0, 0, -1]))
    return float(np.median(seps)), seps


@torch.no_grad()
def measure_calibration_incontext(agent, cfg, rng, n_windows: int = 20):
    """DÜZELTİLMİŞ cihaz (ön-kayıt v2, yuva koşumundan önce): taze sentetik
    pencerede hasat adımındaki TAHMİNİ enerji sıçraması. İlk cihaz
    (statik-STAY sondası) bağlam-dışı ölçüyordu — GRU olumsallığı
    yaklaşma-bağlamında tutuyor; kanıt FINDINGS S2.7 girişinde."""
    jumps = []
    for _ in range(n_windows):
        (obs, acts, tgts, _), _ = make_harvest_window(cfg, rng)
        pred, _ = agent.core(obs, acts)
        e_t = tgts[0, :, -1].numpy()
        e_p = pred[0, :, -1].numpy()
        k = int(np.argmax(np.diff(e_t)))
        jumps.append(float(e_p[k + 1] - e_p[k]))
    return float(np.median(jumps)), jumps


TRUE_INCONTEXT_JUMP = 0.434
N_STAR_THRESHOLD_V2 = 0.217  # ön-kayıt v2: bağlam-içi gerçek sıçramanın %50'si


def stage_calibN(train_turns: int = 15_000, seeds: int = 3) -> None:
    results = []
    for N in (50, 200, 500, 2000):
        for s in range(seeds):
            cfg = a2_config(**S27_OVERRIDES)
            agent = OnlineAgent(cfg, torch_seed=1000 + s, np_seed=2000 + s)
            inj_rng = np.random.default_rng(7_000_000 + 100 * s + N)
            for _ in range(N):
                item, mask = make_harvest_window(cfg, inj_rng)
                agent.per.push(item, priority=1.0, actions_present=mask)
            total, ep = 0, 0
            while total < train_turns:
                r = run_episode(agent, world_seed=s * 10_000 + ep, cfg=cfg,
                                max_turns=1500, world_cfg=WCFG)
                total += r["lifetime"]
                ep += 1
            med, seps = measure_calibration(
                agent, cfg, np.random.default_rng(8_000_000 + s))
            med_ic, _ = measure_calibration_incontext(
                agent, cfg, np.random.default_rng(8_100_000 + s))
            results.append({"N": N, "seed": s, "median_separation": med,
                            "median_incontext_jump": med_ic,
                            "separations": [round(x, 4) for x in seps]})
            print(f"[calibN N={N} seed {s}] statik {med:+.4f} | "
                  f"bağlam-içi {med_ic:+.4f} (eşik v2 {N_STAR_THRESHOLD_V2})",
                  flush=True)
    n_star = None
    for N in (50, 200, 500, 2000):
        meds = [r["median_incontext_jump"] for r in results if r["N"] == N]
        if np.median(meds) >= N_STAR_THRESHOLD_V2:
            n_star = N
            break
    out = {"true_separation": TRUE_SEPARATION,
           "true_incontext_jump": TRUE_INCONTEXT_JUMP,
           "n_star_rule_v1_INVALID": f"statik ayrım >= {N_STAR_THRESHOLD} "
                                     "(cihaz kusurlu — FINDINGS S2.7)",
           "n_star_rule_v2": f"bağlam-içi sıçrama medyanı >= "
                             f"{N_STAR_THRESHOLD_V2} olan en küçük N",
           "n_star": n_star, "train_turns": train_turns,
           "results": results}
    with open("runs/s27_calibN.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nN* = {n_star}")


def _p_nest(total: int) -> float:
    t = 0
    for p, dur in CURRICULUM_V2["p_nest_schedule"]:
        t += dur
        if total < t:
            return p
    return CURRICULUM_V2["p_nest_schedule"][-1][0]


def stage_nest(seeds: int = 5, train_turns: int = 45_000,
               eval_episodes: int = 12, cap: int = 1500) -> None:
    results = []
    for s in range(seeds):
        cfg = a2_config(**S27_OVERRIDES)
        agent = OnlineAgent(cfg, torch_seed=1000 + s, np_seed=2000 + s)
        nest_rng = np.random.default_rng(900_000 + s)
        t0 = time.perf_counter()
        total, ep, train_harvests, nest_eps = 0, 0, 0, 0
        while total < train_turns:
            nested = nest_rng.random() < _p_nest(total)
            r = run_episode(agent, world_seed=s * 10_000 + ep, cfg=cfg,
                            max_turns=cap, world_cfg=WCFG,
                            nest_rng=nest_rng if nested else None)
            total += r["lifetime"]
            train_harvests += r["harvest_count"]
            nest_eps += int(nested)
            ep += 1
        train_time = time.perf_counter() - t0

        tr_rows, st_rows = [], []
        for j in range(eval_episodes):  # standart spawn, müfredatsız
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
        calib_med, _ = measure_calibration_incontext(
            agent, cfg, np.random.default_rng(8_500_000 + s))
        results.append({
            "seed": s, "train_turns": total, "train_episodes": ep,
            "nest_episodes": nest_eps, "train_harvest_events": train_harvests,
            "per_turn_ms": round(1000 * train_time / total, 3),
            "median_harvest": float(np.median(hc)), "harvest_counts": hc,
            "median_lifetime": float(np.median(tr_l)),
            "median_stay": float(np.median(st_l)),
            "trained_lifetimes": tr_l, "stay_lifetimes": st_l,
            "wilcoxon_p_vs_stay": p,
            "final_calibration_separation": calib_med,
        })
        print(f"[nest seed {s}] eğitim hasadı {train_harvests} | eval medyan "
              f"hasat {results[-1]['median_harvest']:.1f} | yaşam "
              f"{results[-1]['median_lifetime']:.0f} vs stay "
              f"{results[-1]['median_stay']:.0f} | p={p:.4f} | "
              f"kalibrasyon {calib_med:+.3f}", flush=True)

    med_of_med = float(np.median([r["median_lifetime"] for r in results]))
    ok_harvest = all(r["median_harvest"] >= HARVEST_THRESHOLD for r in results)
    ok_life = all(r["wilcoxon_p_vs_stay"] < 0.05 for r in results)
    ok_collapse = all(r["median_lifetime"] >= 0.5 * med_of_med
                      for r in results)
    summary = {
        "curriculum_v2": CURRICULUM_V2,               # M-10 damgası
        "world": dataclasses.asdict(WCFG),
        "world_config_hash": config_hash(WCFG),
        "overrides": S27_OVERRIDES,
        "harvest_threshold": HARVEST_THRESHOLD,
        "done_harvest": ok_harvest, "done_life_vs_stay": ok_life,
        "done_no_collapse": ok_collapse,
        "passed": ok_harvest and ok_life and ok_collapse,
        "results": results,
    }
    with open("runs/s27_nest_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nS2.7 yuva: hasat {ok_harvest} | yaşam {ok_life} | "
          f"çöküş-yok {ok_collapse} | ÇATAL: {'A' if summary['passed'] else 'B'}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=("calibN", "nest"))
    a = ap.parse_args()
    pathlib.Path("runs").mkdir(exist_ok=True)
    if a.stage == "calibN":
        stage_calibN()
    else:
        stage_nest()


if __name__ == "__main__":
    main()
