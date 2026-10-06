"""S2.10-ek — seed 3'ün bit-eş enstrümanlı yeniden-yürütmesi:
checkpoint'lerde dondurulmuş temsil + kayma skoru + hasat.

Final ağırlık hash'i kayıtlı seed3.pt'ye eşit olmak ZORUNDA (Kapı-5).
Kullanım: python3 -m training.eval_s210ek
"""

import json
import pathlib

import numpy as np
import torch

from agent.config import a2_config
from training.eval_s27 import _p_nest, WCFG
from training.eval_s210 import S210_OVERRIDES
from training.loop import OnlineAgent, run_episode
from training.shift_test import shift_test
from training.snapshot import SnapshotRecorder

CKPTS = [0, 5_000, 15_000, 25_000, 35_000, 45_000]
SEED = 3
OUT = "runs/s210ek_snapshots"


def checkpoint_eval(agent, ck: int, out_dir: str) -> dict:
    cfg = agent.cfg
    sh = shift_test(agent, WCFG, seed_base=SEED)
    rows = []
    for j in range(6):
        clone = agent.eval_clone(eval_seed=80_000 + SEED * 100 + j)
        ws = 90_000 + SEED * 1000 + ck // 100 + j * 7
        sp = 70_000 + SEED * 1000 + ck // 100 + j * 7
        snap = SnapshotRecorder(stride=1)
        r = run_episode(clone, world_seed=ws, cfg=cfg, max_turns=1500,
                        world_cfg=WCFG, snapshot=snap, learn=False,
                        spawn_seed=sp)
        snap.save(str(pathlib.Path(out_dir) /
                      f"s2_seed{SEED}_ck{ck}_ep{j}.npz"), clone,
                  {"seed": SEED, "ckpt_turns": ck, "world_seed": ws,
                   "eval_episode": j, "lifetime": r["lifetime"],
                   "harvested": r["harvested"]})
        rows.append({"lifetime": r["lifetime"],
                     "harvest_count": r["harvest_count"]})
    return {"ckpt": ck,
            "shift_ratio": sh["ratio"],
            "shift_masses": [sh["correct_mass"], sh["old_mass"]],
            "median_harvest": float(np.median([r["harvest_count"]
                                               for r in rows])),
            "median_lifetime": float(np.median([r["lifetime"]
                                                for r in rows])),
            "evals": rows}


def main() -> None:
    pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)
    saved = torch.load(f"runs/s210_weights/seed{SEED}.pt",
                       weights_only=False)
    cfg = a2_config(**S210_OVERRIDES)
    agent = OnlineAgent(cfg, torch_seed=1000 + SEED, np_seed=2000 + SEED)
    nest_rng = np.random.default_rng(900_000 + SEED)
    pending = CKPTS.copy()
    total, ep = 0, 0
    timeline = []
    while pending or total < 45_000:
        while pending and total >= pending[0]:
            ck = pending.pop(0)
            row = checkpoint_eval(agent, ck, OUT)
            timeline.append(row)
            print(f"[ck {ck:>5}] kayma kütle {row['shift_masses'][0]:.3f}/"
                  f"{row['shift_masses'][1]:.3f} | hasat "
                  f"{row['median_harvest']:.1f} | yaşam "
                  f"{row['median_lifetime']:.0f}", flush=True)
        if total >= 45_000:
            break
        nested = nest_rng.random() < _p_nest(total)
        r = run_episode(agent, world_seed=SEED * 10_000 + ep, cfg=cfg,
                        max_turns=1500, world_cfg=WCFG,
                        nest_rng=nest_rng if nested else None)
        total += r["lifetime"]
        ep += 1

    final_hash = agent.core.weight_hash()
    assert final_hash == saved["weight_hash"], \
        f"BİT-EŞ DEĞİL: {final_hash[:12]} != {saved['weight_hash'][:12]} — ek GEÇERSİZ"
    with open("runs/s210ek_timeline.json", "w") as f:
        json.dump({"seed": SEED, "bit_identical_hash": final_hash,
                   "timeline": timeline}, f, indent=2)
    print(f"\nBİT-EŞ KANIT: final hash == kayıtlı seed3.pt hash "
          f"({final_hash[:16]}…) | zaman ekseni yazıldı")


if __name__ == "__main__":
    main()
