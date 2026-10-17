"""S3-D / PL-22 — NÜFUS fizibilite oracle'ı (M-21: rejim transferi
ÖLÇÜLÜR, varsayılmaz).

Ali kararı (2026-10-18): ekoloji çerçevesi önce (c) 5× seed-3 klon
taban + (b) yuva dönemi; seçilim (a) sonra, ayrı değişken. Öğrenen-
ajan ekolojisi koşulmadan ÖNCE bu modül üç soruya cevap verir:

  A `capacity` — dünya 5 YETKİN ajanı taşıyor mu? (M-02: önce dünyayı
                 yargıla.) Scripted A-oracle × n∈{1,5}.
  B `clone`    — tek-ajan yetkinliği (seed-3) 5-ajan rejimine taşınıyor
                 mu? Merdiven (M-06, tek değişken):
                   L0 clone1_mute  (1 klon, kanal yok)   = cihaz doğrulaması
                   L1 clone5_mute  (+4 rakip)
                   L2 clone5_open  (+kanal, ortak planlama)
                   L3 clone5_learn (+online öğrenme)
  C `nest`     — yuva dönemi (nest_turns, nest_factor) ömrü ve hasadı
                 nasıl değiştiriyor? Kollar: random5, fresh5, clone5_learn.

Bu modül AJAN DEĞİLDİR, ölçüm aletidir → KERNEL_BUDGET'a bit yazmaz
(training/oracle.py, training/b_oracle.py emsali). Klon kolları gerçek
seed-3 ağırlıklarını ÖLÇÜM NESNESİ olarak kullanır; hediye yok.

HALEF YOK: ölen ölü kalır (STAY, sessiz; entity kanalında hayalet —
b_oracle ile aynı beyanlı sınır). Ekoloji değil, oracle.

Çıtalar ve sonuç matrisi FINDINGS "S3-D — ÖN-KAYIT" bölümünde,
koşumdan önce yazıldı (M-08).

Kullanım:
  python3 -m training.pop_oracle --stage capacity --out runs/s3d_capacity.json
  python3 -m training.pop_oracle --stage clone    --out runs/s3d_clone.json
  python3 -m training.pop_oracle --stage nest     --out runs/s3d_nest.json
"""

import argparse
import dataclasses
import json
import pathlib
import time

import numpy as np
import torch

from agent.channel import NO_SIGNAL, N_SYMBOLS, own_signal_onehot, received_vector
from agent.config import AgentConfig
from agent.homeostasis import Homeostasis
from population.lifecycle import transplant_seed3
from population.roster import agent_cfg
from training.ecology import SEED3, WCFG, MutePlanner, SocialPlanner
from training.loop import OnlineAgent, encode_obs
from training.oracle import OraclePolicy
from world.config import config_hash
from world.grid import N_ACTIONS, STAY, World

MAX_TURNS = 3000
SEED_BASE = 9100

# Yuva ızgarası (ön-kayıtlı): (nest_turns, nest_factor)
NEST_GRID = [(0, 1.0), (600, 0.5), (600, 0.25), (600, 0.1), (2000, 0.1)]


# ----------------------------------------------------------------- kollar
# kol → (politika türü, n ajan, kanal, öğrenme)
ARMS = {
    "oracle1":      ("scripted", 1, False, False),
    "oracle5":      ("scripted", 5, False, False),
    "random5":      ("random",   5, False, False),
    "fresh5":       ("fresh",    5, True,  False),
    "clone1_mute":  ("clone",    1, False, False),
    "clone5_mute":  ("clone",    5, False, False),
    "clone5_open":  ("clone",    5, True,  False),
    "clone5_learn": ("clone",    5, True,  True),
}


def _agent_cfg(nest: tuple[int, float]) -> AgentConfig:
    """Roster A2 config'i (ekolojiyle aynı yığın) + yuva parametreleri."""
    return dataclasses.replace(agent_cfg("A2"), nest_turns=nest[0],
                               nest_factor=nest[1])


class Member:
    """Bir oracle sakini. Ölüm gerçek, halef yok."""

    def __init__(self, kind: str, idx: int, n: int, cfg: AgentConfig,
                 channel: bool, learn: bool, seed: int):
        self.kind, self.idx, self.cfg = kind, idx, cfg
        self.channel, self.learn = channel, learn
        self.homeo = Homeostasis(cfg)
        self.harvests = 0
        self.signals = 0
        self.lifetime = None
        self.last_obs = None
        self.agent = None
        self.planner = None
        self.policy = None
        self.rng = np.random.default_rng(seed)
        if kind == "scripted":
            self.policy = OraclePolicy(cfg.obs_radius, WCFG.grid_size)
            # Tarama fazı kaydırması (b_oracle dersi): aynı fazdaki
            # lawnmower'lar bağıl hızsız kalır; faz indekse göre dağıtılır.
            self.policy._east = (idx * WCFG.grid_size // max(n, 1)) \
                % WCFG.grid_size
        elif kind == "fresh":
            base = OnlineAgent(cfg, torch_seed=seed, np_seed=seed + 1)
            self.agent = base.eval_clone(seed + 2)     # öğrenmesiz, taze
        elif kind == "clone":
            base = transplant_seed3(SEED3, cfg, torch_seed=seed,
                                    np_seed=seed + 1)
            self.agent = base if learn else base.eval_clone(seed + 2)
        if self.agent is not None:
            P = SocialPlanner if channel else MutePlanner
            self.planner = P(cfg, self.agent.planner.rng)

    @property
    def alive(self) -> bool:
        return self.homeo.alive

    def act(self, world: World) -> tuple[int, int]:
        if self.kind == "random":
            return int(self.rng.integers(0, N_ACTIONS)), NO_SIGNAL
        if self.kind == "scripted":
            return self.policy.act_grid(
                world.observe(self.idx, self.cfg.obs_radius)), NO_SIGNAL
        cfg = self.cfg
        rng = self.planner.rng
        if rng.random() < cfg.mpc_epsilon:          # ε (K-108), ekolojiyle aynı
            if cfg.eps_move_bias > 0 and rng.random() < cfg.eps_move_bias:
                a = int(rng.integers(1, 5))
            else:
                a = int(rng.integers(0, N_ACTIONS))
            s = int(rng.integers(-1, N_SYMBOLS)) if self.channel else NO_SIGNAL
            return a, s
        return self.planner.plan_joint(self.agent.core, self.agent.h,
                                       self.last_obs)

    def observe(self, world: World) -> torch.Tensor | None:
        if self.agent is None:
            return None
        heard = world.heard(self.idx, WCFG.signal_range) if self.channel else []
        return encode_obs(world.observe(self.idx, self.cfg.obs_radius),
                          max(self.homeo.energy, 0.0), self.cfg,
                          received_vector(heard))

    def digest(self, action: int, sig: int, nxt: torch.Tensor | None) -> None:
        """Gözlemi çekirdeğe işle (öğrenerek ya da yalnız hidden ilerleterek)."""
        if self.agent is None:
            return
        act_vec = torch.cat([torch.eye(N_ACTIONS)[action],
                             torch.from_numpy(own_signal_onehot(sig))])
        if self.learn:
            self.agent.learn_step_vec(self.last_obs, act_vec, nxt)
        else:
            self.agent.observe_step_vec(self.last_obs, act_vec)
        self.last_obs = nxt


def run_arm(arm: str, seed: int, nest: tuple[int, float] = (0, 1.0),
            max_turns: int = MAX_TURNS) -> dict:
    kind, n, channel, learn = ARMS[arm]
    cfg = _agent_cfg(nest)
    world = World(WCFG, n_entities=n, seed=seed)
    members = [Member(kind, i, n, cfg, channel, learn, seed=100_000 * (i + 1) + seed)
               for i in range(n)]
    for m in members:
        m.last_obs = m.observe(world)
    agent_turns = 0
    t0 = time.perf_counter()
    for turn in range(1, max_turns + 1):
        acts, sigs = [], []
        for m in members:
            if not m.alive:
                acts.append(STAY)
                sigs.append(NO_SIGNAL)
                continue
            a, s = m.act(world)
            acts.append(a)
            sigs.append(s)
        deltas = world.step(np.array(acts), np.array(sigs))
        for i, m in enumerate(members):
            if not m.alive:
                continue
            agent_turns += 1
            sc = cfg.signal_energy_cost if sigs[i] != NO_SIGNAL else 0.0
            m.homeo.apply_turn(acts[i], float(deltas[i]), signal_cost=sc)
            if deltas[i] > 0:
                m.harvests += 1
            if sigs[i] != NO_SIGNAL:
                m.signals += 1
            if m.alive:
                m.digest(acts[i], sigs[i], m.observe(world))
            else:
                m.lifetime = turn
        if not any(m.alive for m in members):
            break
    for m in members:
        if m.lifetime is None:
            m.lifetime = max_turns
    lifes = [m.lifetime for m in members]
    return {"arm": arm, "seed": seed, "nest": list(nest),
            "lifetimes": lifes,
            "censored": [m.alive for m in members],
            "harvests": [m.harvests for m in members],
            "signals": [m.signals for m in members],
            "agent_turns": agent_turns,
            "b_openings": world.b_openings_total,
            "seconds": round(time.perf_counter() - t0, 1)}


def summarize(rows: list[dict]) -> dict:
    lifes = np.concatenate([r["lifetimes"] for r in rows]).astype(float)
    harv = sum(sum(r["harvests"]) for r in rows)
    at = sum(r["agent_turns"] for r in rows)
    sig = sum(sum(r["signals"]) for r in rows)
    return {"n_agents_total": int(lifes.size),
            "median_lifetime": float(np.median(lifes)),
            "mean_lifetime": round(float(lifes.mean()), 1),
            "min_lifetime": int(lifes.min()),
            "max_lifetime": int(lifes.max()),
            "censored": int(sum(sum(r["censored"]) for r in rows)),
            "harvests_total": int(harv),
            "harvest_per_1k_agent_turns": round(1000 * harv / max(at, 1), 2),
            "signal_rate": round(sig / max(at, 1), 4),
            "b_openings_total": int(sum(r["b_openings"] for r in rows)),
            "seconds": round(sum(r["seconds"] for r in rows), 1)}


def sweep(arm: str, seeds: int, nest=(0, 1.0), max_turns=MAX_TURNS,
          log=print) -> dict:
    rows = []
    for e in range(seeds):
        r = run_arm(arm, SEED_BASE + e, nest, max_turns)
        rows.append(r)
        log(f"  [{arm} T={nest[0]} f={nest[1]}] seed {e}: ömür {r['lifetimes']} "
            f"| hasat {r['harvests']} | {r['seconds']} sn")
    s = summarize(rows)
    s.update(arm=arm, nest=list(nest), rows=rows)
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["capacity", "clone", "nest"],
                    required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, default=None)
    ap.add_argument("--max-turns", type=int, default=MAX_TURNS)
    a = ap.parse_args()
    seeds = a.seeds or (3 if a.stage == "nest" else 5)
    out = {"stage": a.stage, "max_turns": a.max_turns, "seeds": seeds,
           "world": dataclasses.asdict(WCFG),
           "world_config_hash": config_hash(WCFG),
           "agent_cfg": dataclasses.asdict(_agent_cfg((0, 1.0))),
           "results": []}
    if a.stage == "capacity":
        arms = [("oracle1", (0, 1.0)), ("oracle5", (0, 1.0))]
    elif a.stage == "clone":
        arms = [(x, (0, 1.0)) for x in
                ("clone1_mute", "clone5_mute", "clone5_open", "clone5_learn")]
    else:
        arms = [(x, nest) for nest in NEST_GRID
                for x in ("random5", "fresh5", "clone5_learn")]
    for arm, nest in arms:
        s = sweep(arm, seeds, nest, a.max_turns)
        out["results"].append(s)
        print(f"[{a.stage}] {arm:>12} T={nest[0]:>4} f={nest[1]:<4} | medyan ömür "
              f"{s['median_lifetime']:>6} | hasat/1K {s['harvest_per_1k_agent_turns']:>6} "
              f"| sansür {s['censored']}/{s['n_agents_total']} | "
              f"{s['seconds']} sn", flush=True)
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "w") as f:          # kısmi sonuç da yazılır
            json.dump(out, f, indent=2)
    print(f"\nyazıldı: {a.out}")


if __name__ == "__main__":
    main()
