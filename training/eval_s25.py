"""S2.5 merdiven değerlendiricisi: tek ajanda güvenilir A-hasadı.

Müdahaleler TEK TEK eklenir (Ali: hangisinin çözdüğü bilinmek isteniyor):
  adım 1: mpc_horizon 5→10
  adım 2: + base_metabolism kalibrasyonu (saf-tasarruf tavanı < medyan yaşam)
  adım 3: + uzun/yumuşak müfredat (48→36→24→18→12)

Bitti-tanımı (standart kıtlık, 12 kaynak, ≥5 seed):
  (i)  epizot başına medyan hasat sayısı ≥ 3
  (ii) yaşam süresi, SAF-TASARRUF taban çizgisine (her tur STAY, ε=0)
       karşı anlamlı uzuyor — aynı dünya + aynı spawn, eşleştirilmiş
       Wilcoxon (rastgele politika artık taban çizgisi DEĞİL).

Eval, PL-11 gereği seed'li spawn randomizasyonu ile koşar.

Kullanım:
  python3 -m training.eval_s25 --step 1 --out runs/s25_step1.json
"""

import argparse
import json
import pathlib
import time

import numpy as np
from scipy.stats import wilcoxon

from agent.config import a2_config
from training.gen_s2_data import DEFAULT_PHASES, phase_cfg
from training.loop import OnlineAgent, run_episode

SOFT_PHASES = [(48, 20_000), (36, 10_000), (24, 10_000), (18, 10_000),
               (12, 10_000)]

STEPS = {
    1: {"overrides": {"mpc_horizon": 10}, "phases": DEFAULT_PHASES},
    # Kalibrasyon (KERNEL_BUDGET S2 müfredat şerhi): saf-tasarruf tavanı
    # = max_energy / base_metabolism = 100 / 1.0 = 100 tur < 130
    # (S2'de gözlenen medyan-yaşam alt sınırı). Hasatsız medyana ulaşmak
    # matematiksel olarak imkansız.
    2: {"overrides": {"mpc_horizon": 10, "base_metabolism": 1.0},
        "phases": DEFAULT_PHASES},
    3: {"overrides": {"mpc_horizon": 10, "base_metabolism": 1.0,
                      "mpc_candidates": 48},
        "phases": SOFT_PHASES},
    # Adım 4 (teşhis-güdümlü, K-109): epizot-içi sonda gösterdi ki model
    # STAY'i doğru tercih ediyor ama rastgele aday dizilerinde ilk-eylem
    # seyreltmesi MPC'yi ~%45 gereksiz harekete zorluyor. Düzeltme planlayıcı
    # örneklemesinde: sabit-eylem adayları + elit iyileştirme. Taban = adım 2
    # (adım 3'ün müfredat/aday değişiklikleri katkısız çıktı, dahil edilmedi).
    4: {"overrides": {"mpc_horizon": 10, "base_metabolism": 1.0,
                      "mpc_constant_candidates": True, "mpc_cem_iters": 2},
        "phases": DEFAULT_PHASES},
}


def run_seed(seed: int, overrides: dict, phases, eval_episodes: int,
             cap: int) -> dict:
    cfg = a2_config(**overrides)
    agent = OnlineAgent(cfg, torch_seed=1000 + seed, np_seed=2000 + seed)

    total_target = sum(d for _, d in phases)
    t0 = time.perf_counter()
    total, ep = 0, 0
    while total < total_target:
        wcfg = phase_cfg(total, phases)
        r = run_episode(agent, world_seed=seed * 10_000 + ep, cfg=cfg,
                        max_turns=cap, world_cfg=wcfg)
        total += r["lifetime"]
        ep += 1
    train_time = time.perf_counter() - t0

    rows = []
    for j in range(eval_episodes):
        ws = 95_000 + seed * 1000 + j * 7
        sp = 70_000 + seed * 1000 + j * 7  # PL-11: seed'li spawn
        clone = agent.eval_clone(eval_seed=80_000 + seed * 100 + j)
        tr = run_episode(clone, world_seed=ws, cfg=cfg, max_turns=cap,
                         learn=False, spawn_seed=sp)
        st = run_episode("stay", world_seed=ws, cfg=cfg, max_turns=cap,
                         spawn_seed=sp)
        rows.append({"world_seed": ws, "trained": tr, "stay": st})

    tr_life = [r["trained"]["lifetime"] for r in rows]
    st_life = [r["stay"]["lifetime"] for r in rows]
    hc = [r["trained"]["harvest_count"] for r in rows]
    try:
        p = float(wilcoxon(tr_life, st_life, alternative="greater").pvalue)
    except ValueError:  # tüm farklar sıfır
        p = 1.0
    return {
        "seed": seed, "train_episodes": ep, "train_turns": total,
        "per_turn_ms": round(1000 * train_time / total, 3),
        "median_harvest_count": float(np.median(hc)),
        "harvest_counts": hc,
        "trained_lifetimes": tr_life, "stay_lifetimes": st_life,
        "median_trained": float(np.median(tr_life)),
        "median_stay": float(np.median(st_life)),
        "wilcoxon_p_vs_stay": p,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", type=int, required=True, choices=(1, 2, 3, 4))
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--eval-episodes", type=int, default=12)
    ap.add_argument("--cap", type=int, default=1500)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or f"runs/s25_step{a.step}.json"
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)

    spec = STEPS[a.step]
    results = []
    for s in range(a.seeds):
        r = run_seed(s, spec["overrides"], spec["phases"],
                     a.eval_episodes, a.cap)
        results.append(r)
        print(f"[adım {a.step} seed {s}] medyan hasat {r['median_harvest_count']:.1f} | "
              f"yaşam {r['median_trained']:.0f} vs stay {r['median_stay']:.0f} | "
              f"p={r['wilcoxon_p_vs_stay']:.4f} | {r['per_turn_ms']} ms/tur",
              flush=True)

    ok_harvest = all(r["median_harvest_count"] >= 3 for r in results)
    ok_life = all(r["wilcoxon_p_vs_stay"] < 0.05 for r in results)
    summary = {"step": a.step, "overrides": spec["overrides"],
               "phases": spec["phases"],
               "done_harvest_ge3_all_seeds": ok_harvest,
               "done_life_vs_stay_all_seeds": ok_life,
               "passed": ok_harvest and ok_life,
               "results": results}
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nadım {a.step}: hasat≥3 {ok_harvest} | stay'e karşı p<0.05 "
          f"{ok_life} | GEÇTİ: {ok_harvest and ok_life} → {out}")


if __name__ == "__main__":
    main()
