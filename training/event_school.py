"""S3-J "olay okulu" — tek ajan, öğrenilebilirlik tavanı (M-01/M-22).

Soru: TEK bir öğrenen ajan, sınırsız zaman ve bol olay deneyimiyle
KENDİ ipucunu güvenli eyleme çevirmeyi öğrenebiliyor mu? Ekoloji
(5 ajan, ölüm, rekabet, kanal) bu tavanın altında kalmak zorundadır;
tavanın kendisi şans düzeyindeyse darboğaz ekoloji değil, öğrenme
sinyali ya da mimaridir — anayasal merdiven ancak o zaman anlamlıdır.

Rejim: "yetiştirme kabı" (PL-06 emsali, S1): ölüm bedeni sıfırlar
(enerji 100, yeni konum, hidden/tampon sıfır) ama ağırlıklar sürer
(σ=0). Kanal KAPALI (MutePlanner) — kendi-ipucu sorusu kanaldan
bağımsız. Olaylar sık (every=10), lead=2, ceza 25.

Çıktı: 10K'lık pencerelerde kendi-ipucu tutarlılığı (şans 0.5), isabet
(şans ~0.2-0.25), STAY payı, ölüm sayısı; sonda ağırlıklar (prob için).

Kullanım: python3 -m training.event_school --turns 100000 --seed 0 --out runs/s3j/base_s0
"""

import argparse
import dataclasses
import json
import pathlib
import time

import numpy as np
import torch

from agent.channel import NO_SIGNAL, own_signal_onehot, received_vector
from agent.homeostasis import Homeostasis
from population.lifecycle import transplant_seed3
from population.roster import agent_cfg
from training.ecology import EVENT_KW, SEED3, WCFG, MutePlanner
from training.loop import encode_obs
from world.grid import N_ACTIONS, World


def run_school(turns: int, seed: int, out_dir: str, event_every: int = 10,
               event_lead: int = 2, event_penalty: float = 25.0,
               energy_loss_weight: float | None = None,
               learning_rate: float | None = None,
               window: int = 10_000) -> dict:
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    wcfg = dataclasses.replace(WCFG, **{**EVENT_KW, "event_every": event_every,
                                        "event_lead": event_lead,
                                        "event_penalty": event_penalty})
    cfg = agent_cfg("A2")
    over = {}
    if energy_loss_weight is not None:
        over["energy_loss_weight"] = float(energy_loss_weight)
    if learning_rate is not None:
        over["learning_rate"] = float(learning_rate)
    cfg = dataclasses.replace(cfg, **over)
    agent = transplant_seed3(SEED3, cfg, torch_seed=1000 + seed, np_seed=2000 + seed)
    planner = MutePlanner(cfg, agent.planner.rng)
    world = World(wcfg, n_entities=1, seed=7000 + seed)
    homeo = Homeostasis(cfg)
    rng = planner.rng

    def observe():
        return encode_obs(world.observe(0, cfg.obs_radius),
                          max(homeo.energy, 0.0), cfg, received_vector([]))

    obs = observe()
    W = {"event_turns": 0, "hits": 0, "own": 0, "stay": 0, "deaths": 0,
         "harvests": 0}
    rows, t0 = [], time.perf_counter()
    for turn in range(1, turns + 1):
        ev = world.events
        will_active = ev.active(world.turn + 1)
        safe = ev.safe_action() if will_active else None
        cands = ev.candidates(0) if will_active else None
        if rng.random() < cfg.mpc_epsilon:
            if cfg.eps_move_bias > 0 and rng.random() < cfg.eps_move_bias:
                a = int(rng.integers(1, 5))
            else:
                a = int(rng.integers(0, N_ACTIONS))
        else:
            a, _ = planner.plan_joint(agent.core, agent.h, obs)
        deltas = world.step(np.array([a]), np.array([NO_SIGNAL]))
        homeo.apply_turn(a, float(deltas[0]))
        if deltas[0] > 0:
            W["harvests"] += 1
        if will_active:
            W["event_turns"] += 1
            W["hits"] += int(a == safe)
            W["own"] += int(a in cands)
            W["stay"] += int(a == 0)
        nxt = observe()
        act_vec = torch.cat([torch.eye(N_ACTIONS)[a],
                             torch.from_numpy(own_signal_onehot(NO_SIGNAL))])
        agent.learn_step_vec(obs, act_vec, nxt)
        obs = nxt
        if not homeo.alive:                      # beden sıfırlanır, ağırlık sürer
            W["deaths"] += 1
            homeo = Homeostasis(cfg)
            world.respawn_entity(0)
            agent.reset_episode_state()
            obs = observe()
        if turn % window == 0:
            et = max(W["event_turns"], 1)
            row = {"turn": turn, "event_turns": W["event_turns"],
                   "hit_rate": round(W["hits"] / et, 4),
                   "own_cue_rate": round(W["own"] / et, 4),
                   "stay_share": round(W["stay"] / et, 4),
                   "deaths": W["deaths"], "harvests": W["harvests"],
                   "ms_per_turn": round(1000 * (time.perf_counter() - t0) / turn, 1)}
            rows.append(row)
            print(f"[t={turn:>7}] isabet {row['hit_rate']} | kendi-ipucu "
                  f"{row['own_cue_rate']} | STAY {row['stay_share']} | ölüm "
                  f"{row['deaths']} | hasat {row['harvests']} | "
                  f"{row['ms_per_turn']} ms/tur", flush=True)
            W = {k: 0 for k in W}
    out = {"turns": turns, "seed": seed, "world": dataclasses.asdict(wcfg),
           "overrides": over, "cfg": dataclasses.asdict(cfg), "windows": rows}
    json.dump(out, open(pathlib.Path(out_dir) / "school.json", "w"), indent=2)
    torch.save({"A2": {"id": f"school.s{seed}", "gen": 0,
                       "cfg": dataclasses.asdict(cfg),
                       "state_dict": agent.core.state_dict()}},
               pathlib.Path(out_dir) / "final_weights.pt")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--energy-loss-weight", type=float, default=None)
    ap.add_argument("--learning-rate", type=float, default=None)
    ap.add_argument("--event-every", type=int, default=10)
    ap.add_argument("--event-lead", type=int, default=2)
    ap.add_argument("--event-penalty", type=float, default=25.0)
    a = ap.parse_args()
    run_school(a.turns, a.seed, a.out, a.event_every, a.event_lead,
               a.event_penalty, a.energy_loss_weight, a.learning_rate)


if __name__ == "__main__":
    main()
