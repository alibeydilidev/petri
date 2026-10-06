"""S2 veri üretimi: PL-10 müfredatlı eğitim + checkpoint snapshot'ları.

Müfredat (ekolojik iskele, ajan prior'ı DEĞİL — KERNEL_BUDGET S1 notu):
A-kaynağı yoğunluğu aşamalı kıtlaştırılır (48 → 24 → 12) ki hasat
deneyimi veriye girsin; DEĞERLENDİRME her zaman standart kıtlıkta (12).

Checkpoint'lerde ajanın ÖĞRENMESİZ KOPYASI (eval_clone) taze dünyalarda
koşar ve temsiller dondurulur. Eğitim gidişatı checkpoint'lerden
etkilenmez — bit-eş kanıt: tests/test_s2_gen.py::test_checkpoints_zero_touch.

Kullanım:
  python3 -m training.gen_s2_data --out runs/s2_snapshots
"""

import argparse
import dataclasses
import json
import pathlib
import time

import numpy as np

from agent.config import a2_config
from training.loop import OnlineAgent, run_episode
from training.snapshot import SnapshotRecorder
from world.config import WorldConfig

# (resource_a_count, faz uzunluğu tur)
DEFAULT_PHASES = [(48, 15_000), (24, 15_000), (12, 15_000)]
DEFAULT_CKPTS = [0, 5_000, 15_000, 25_000, 35_000, 45_000]


def phase_cfg(total_turns: int, phases) -> WorldConfig:
    t = 0
    for count, dur in phases:
        t += dur
        if total_turns < t:
            return dataclasses.replace(WorldConfig(), resource_a_count=count)
    return dataclasses.replace(WorldConfig(), resource_a_count=phases[-1][0])


def run_checkpoint_evals(agent: OnlineAgent, seed: int, ckpt_turns: int,
                         eval_episodes: int, cap: int, out_dir: str,
                         spawn_randomize: bool = False,
                         eval_world_overrides: dict | None = None) -> list[dict]:
    """Öğrenmesiz klonla, sabit eval dünyasında, dondurulmuş temsil toplar."""
    cfg = agent.cfg
    wcfg = dataclasses.replace(WorldConfig(), **(eval_world_overrides or {}))
    rows = []
    for j in range(eval_episodes):
        clone = agent.eval_clone(eval_seed=80_000 + seed * 100 + j)
        world_seed = 90_000 + seed * 1000 + ckpt_turns // 100 + j * 7
        spawn_seed = (70_000 + seed * 1000 + ckpt_turns // 100 + j * 7
                      if spawn_randomize else None)  # PL-11
        snap = SnapshotRecorder(stride=1)
        r = run_episode(clone, world_seed=world_seed, cfg=cfg, max_turns=cap,
                        world_cfg=wcfg, snapshot=snap, learn=False,
                        spawn_seed=spawn_seed)
        p = pathlib.Path(out_dir) / f"s2_seed{seed}_ck{ckpt_turns}_ep{j}.npz"
        snap.save(str(p), clone, {
            "seed": seed, "ckpt_turns": ckpt_turns, "world_seed": world_seed,
            "eval_episode": j, "lifetime": r["lifetime"],
            "harvested": r["harvested"],
        })
        rows.append({"ep": j, "lifetime": r["lifetime"],
                     "harvested": r["harvested"]})
    return rows


def run_curriculum(seed: int, phases, ckpts, eval_episodes: int, cap: int,
                   out_dir: str | None, cfg_overrides: dict | None = None,
                   spawn_randomize: bool = False,
                   eval_world_overrides: dict | None = None,
                   nest_schedule: list | None = None) -> OnlineAgent:
    """Bir seed'in müfredatlı eğitimi; out_dir=None → snapshot üretme
    (zero-touch testinin karşılaştırma kolu).

    nest_schedule (S2.7 curriculum_v2): [(p_nest, tur), ...] — eğitim
    epizotlarında p olasılıkla kaynak-yakını doğum. Eval'e uygulanmaz."""
    cfg = a2_config(**(cfg_overrides or {}))
    nest_rng = (np.random.default_rng(900_000 + seed)
                if nest_schedule else None)

    def p_nest(total_turns: int) -> float:
        t = 0
        for p, dur in nest_schedule:
            t += dur
            if total_turns < t:
                return p
        return nest_schedule[-1][0]
    agent = OnlineAgent(cfg, torch_seed=1000 + seed, np_seed=2000 + seed)
    pending = sorted(ckpts)
    total, ep, train_harvests = 0, 0, 0
    log = []

    while pending or total < sum(d for _, d in phases):
        while pending and total >= pending[0]:
            ck = pending.pop(0)
            if out_dir is not None:
                rows = run_checkpoint_evals(agent, seed, ck, eval_episodes,
                                            cap, out_dir, spawn_randomize,
                                            eval_world_overrides)
                log.append({"ckpt": ck, "evals": rows})
        if total >= sum(d for _, d in phases):
            break
        wcfg = phase_cfg(total, phases)
        nested = (nest_rng is not None
                  and nest_rng.random() < p_nest(total))
        r = run_episode(agent, world_seed=seed * 10_000 + ep, cfg=cfg,
                        max_turns=cap, world_cfg=wcfg,
                        nest_rng=nest_rng if nested else None)
        total += r["lifetime"]
        train_harvests += r["harvest_count"]
        ep += 1

    if out_dir is not None:
        meta = {"seed": seed, "phases": phases, "ckpts": ckpts,
                "nest_schedule": nest_schedule,        # curriculum_v2 damgası
                "train_harvest_events": train_harvests,
                "train_episodes": ep, "train_turns": total,
                "final_weight_hash": agent.core.weight_hash(),
                "checkpoint_log": log}
        with open(pathlib.Path(out_dir) / f"s2_seed{seed}_meta.json", "w") as f:
            json.dump(meta, f, indent=2)
    return agent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--eval-episodes", type=int, default=6)
    ap.add_argument("--cap", type=int, default=1500)
    ap.add_argument("--out", default="runs/s2_snapshots")
    ap.add_argument("--spawn-randomize", action="store_true")  # PL-11
    ap.add_argument("--cfg-override", default=None,
                    help='JSON, örn. \'{"energy_loss_weight": 1.0}\'')
    ap.add_argument("--eval-world-override", default=None,
                    help='JSON, örn. \'{"resource_a_count": 24}\'')
    ap.add_argument("--phases", default=None,
                    help='JSON [[kaynak, tur], ...]; yoksa varsayılan müfredat')
    a = ap.parse_args()
    overrides = json.loads(a.cfg_override) if a.cfg_override else None
    ewo = json.loads(a.eval_world_override) if a.eval_world_override else None
    phases = ([tuple(p) for p in json.loads(a.phases)] if a.phases
              else DEFAULT_PHASES)
    pathlib.Path(a.out).mkdir(parents=True, exist_ok=True)
    for s in range(a.seeds):
        t0 = time.perf_counter()
        agent = run_curriculum(s, phases, DEFAULT_CKPTS,
                               a.eval_episodes, a.cap, a.out,
                               cfg_overrides=overrides,
                               spawn_randomize=a.spawn_randomize,
                               eval_world_overrides=ewo)
        print(f"[seed {s}] bitti: {time.perf_counter() - t0:.0f} sn | "
              f"whash {agent.core.weight_hash()[:12]}", flush=True)


if __name__ == "__main__":
    main()
