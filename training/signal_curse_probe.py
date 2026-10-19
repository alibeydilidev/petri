"""S3-O yan probu — "kazananın laneti": ortak planlayıcı sinyalli satırları
payından ÇOK daha sık seçiyor mu, ve neden?

Ölçüm (gözlemci; ajana gitmez): örneklenmiş durumlarda 64 adayın
J skorları hesaplanır; satırlar İLK adımı sinyalli / sinyalsiz diye
ikiye ayrılır. Raporlanır: her grubun skor ORTALAMASI ve STD'si, argmax'ın
sinyalli gruba düşme oranı vs sinyalli satır payı. Ortalama sinyalli ≤
sinyalsiz iken argmax sinyalliye payından sık düşüyorsa → varyans
kaynaklı seçim (kazananın laneti): eğitilmemiş sinyal sütunları tahmine
gürültü katar, max gürültüyü ödüllendirir.

Kullanım: python3 -m training.signal_curse_probe --weights runs/s3n/NA_s3001/final_weights.pt
"""

import argparse
import dataclasses
import json

import numpy as np
import torch

from agent.channel import NO_SIGNAL, N_SYMBOLS, received_vector
from agent.config import AgentConfig
from agent.predictive_core import PredictiveCore
from population.lifecycle import transplant_seed3
from population.roster import agent_cfg
from training.ecology import EVENT_KW, SEED3, WCFG, SocialPlanner
from training.loop import encode_obs
from world.grid import N_ACTIONS, World


def _states(cfg, n: int, seed: int):
    """Rastgele yürüyüşle n durum (gözlem + hidden=None; sade)."""
    wcfg = dataclasses.replace(WCFG, **{**EVENT_KW, "event_every": 10, "event_lead": 4})
    world = World(wcfg, n_entities=5, seed=seed)
    rng = np.random.default_rng(seed)
    out = []
    for t in range(n * 7):
        world.step(rng.integers(0, N_ACTIONS, 5), rng.integers(-1, N_SYMBOLS, 5))
        if t % 7 == 6:
            heard = world.heard(0, wcfg.signal_range)
            out.append(encode_obs(world.observe(0, cfg.obs_radius),
                                  float(rng.uniform(30, 90)), cfg,
                                  received_vector(heard)))
    return out


def probe(core, cfg, n_states: int = 60, seed: int = 11, frac: float = 1.0) -> dict:
    cfg = dataclasses.replace(cfg, mpc_signal_candidate_frac=frac)
    planner = SocialPlanner(cfg, np.random.default_rng(seed))
    C, D = cfg.mpc_candidates, cfg.mpc_horizon
    pick_sig, share_sig = [], []
    mean_s, mean_q, std_s, std_q, max_s, max_q = [], [], [], [], [], []
    for obs in _states(cfg, n_states, seed):
        # plan_joint'ın ilk atış aday kümesini yeniden kur (CEM öncesi)
        rng = planner.rng
        seqs = rng.integers(0, N_ACTIONS, size=(C, D))
        sigs = rng.integers(-1, N_SYMBOLS, size=(C, D))
        if frac < 1.0:
            quiet = rng.random(C) >= frac
            sigs[quiet, :] = NO_SIGNAL
        for a in range(N_ACTIONS):
            seqs[a, :] = a
            sigs[a, :] = NO_SIGNAL
        scores = planner._score_joint(core, None, obs, seqs, sigs)
        is_sig = sigs[:, 0] != NO_SIGNAL
        if is_sig.sum() == 0 or (~is_sig).sum() == 0:
            continue
        share_sig.append(float(is_sig.mean()))
        pick_sig.append(bool(is_sig[int(np.argmax(scores))]))
        mean_s.append(float(scores[is_sig].mean())); mean_q.append(float(scores[~is_sig].mean()))
        std_s.append(float(scores[is_sig].std())); std_q.append(float(scores[~is_sig].std()))
        max_s.append(float(scores[is_sig].max())); max_q.append(float(scores[~is_sig].max()))
    r = lambda x: round(float(np.mean(x)), 4)
    return {"n_states": len(pick_sig), "frac": frac,
            "signal_row_share": r(share_sig), "argmax_signal_rate": r(pick_sig),
            "mean_score_signal": r(mean_s), "mean_score_quiet": r(mean_q),
            "std_score_signal": r(std_s), "std_score_quiet": r(std_q),
            "max_score_signal": r(max_s), "max_score_quiet": r(max_q),
            "max_sig_minus_max_quiet": round(float(np.mean(np.array(max_s) - np.array(max_q))), 4)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", nargs="*", default=[])
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    res = {}
    base = transplant_seed3(SEED3, agent_cfg("A2"), torch_seed=1, np_seed=2)
    for frac in (1.0, 0.25, 0.05):
        res[f"seed3_transplant:frac{frac}"] = probe(base.core, base.cfg, frac=frac)
        print("[seed3 transplant]", res[f"seed3_transplant:frac{frac}"])
    for w in a.weights:
        ck = torch.load(w, weights_only=False)
        for slot, e in list(ck.items())[:2]:
            cfg = AgentConfig(**e["cfg"])
            if "ensemble_state_dict" in e:      # A1: topluluk planlayıcısı
                from agent.ensemble import EnsembleCore
                core = EnsembleCore(cfg, cfg.ensemble_k, 0)
                core.load_state_dict(e["ensemble_state_dict"])
            else:
                core = PredictiveCore(cfg); core.load_state_dict(e["state_dict"])
            core.eval()
            for frac in (1.0, 0.05):
                k = f"{w}:{slot}:frac{frac}"
                res[k] = probe(core, cfg, frac=frac)
                print(f"[{w} {slot} {e['id']}]", res[k])
    if a.out:
        json.dump(res, open(a.out, "w"), indent=2)


if __name__ == "__main__":
    main()
