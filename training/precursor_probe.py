"""S3-G algı probu — model ÖNCÜYÜ görüyor mu? (gözlemci enstrümanı, ajana
gitmez; anayasa md.5: davranış değil iç temsil/tahmin ölçülür).

Soru: uyarı penceresinde (öncü hücreleri tehlike kanalında yanarken)
modelin OLAY turu için eyleme-koşullu enerji tahmini, öncüsüz aynı
bağlama göre değişiyor mu? Değişmiyorsa model öncüyü enerji
sıçramasına bağlamamıştır; kanal/dil sorusu sorulamaz (önce algı).

Protokol (bağlam başına):
  1. Aynı seed'li iki dünya: olay AÇIK (öncü yanar) / olay KAPALI.
     Aynı yerleşim, aynı konum. Olay durumu elle kurulur: kutup p,
     ipucu ataması, öncü 8 tur sonra başlar (lead=8).
  2. 8 tur boyunca ajan STAY, gözlem çekirdeğe işlenir (hidden ilerler).
  3. Olay turunda 6 eylem için tek adım tahmin: E_a = tahmini enerji.
  4. Δ_a = E_a(öncülü) − E_a(öncüsüz). Metrikler:
     - spread = max_a Δ_a − min_a Δ_a  (öncü eylem-koşullu iz bıraktı mı)
     - own_align: argmax_a E_a(öncülü) ∈ kendi-ipucu aday kümesi (şans 0.5)
     - safe_gap: E_safe − mean(E_unsafe) (öncülü) — doğru işaret +.
Bilinen-negatif: eğitilmemiş/olay görmemiş transplant → spread ≈ 0.
Bilinen-pozitif: sentetik — öncüsüz dünyada da aynı sayılar çıkmalı
(spread tam 0) → cihazın kendisi fark üretmiyor (M-15/M-23).

Kullanım: python3 -m training.precursor_probe --weights runs/s3g/G1_s3001/final_weights.pt
"""

import argparse
import dataclasses
import json
import pathlib

import numpy as np
import torch

from agent.channel import NO_SIGNAL, own_signal_onehot, received_vector
from agent.config import AgentConfig
from agent.predictive_core import PredictiveCore
from population.lifecycle import transplant_seed3
from population.roster import agent_cfg
from training.ecology import EVENT_KW, SEED3, WCFG
from training.loop import encode_obs
from world.grid import N_ACTIONS, STAY, World

W_EVENT = dataclasses.replace(WCFG, **EVENT_KW)


def _core_from_entry(entry: dict) -> tuple[PredictiveCore, AgentConfig]:
    cfg = AgentConfig(**entry["cfg"])
    core = PredictiveCore(cfg)
    core.load_state_dict(entry["state_dict"])
    core.eval()
    return core, cfg


def _run_context(core, cfg, seed: int, polarity: int, cue_bits: np.ndarray,
                 energy: float = 0.6, n_ent: int = 5, me: int = 0):
    """Bir bağlam: (öncülü, öncüsüz) iki dünya → eylem-koşullu enerji."""
    r = cfg.obs_radius
    out = {}
    for with_event in (True, False):
        world = World(W_EVENT if with_event else WCFG, n_entities=n_ent, seed=seed)
        if with_event:
            ev = world.events
            ev.polarity = polarity
            ev.starts_at = world.turn + EVENT_KW["event_lead"]
            ev.ends_at = ev.starts_at + 1
            ev.cue_assign = cue_bits.copy()
            ev.precursor = np.zeros((1, 2), dtype=np.int64)
        h = None
        act_vec = torch.cat([torch.eye(N_ACTIONS)[STAY],
                             torch.from_numpy(own_signal_onehot(NO_SIGNAL))])
        for _ in range(EVENT_KW["event_lead"]):
            obs = encode_obs(world.observe(me, r), energy * cfg.max_energy,
                             cfg, received_vector([]))
            with torch.no_grad():
                _, h = core(obs.view(1, 1, -1), act_vec.view(1, 1, -1), h)
            # dünya ilerlemez (STAY, dünya rng'sine dokunmadan): öncü
            # penceresi boyunca gözlem sabit — hidden'a 8 kez işlenir.
            if with_event:
                world.turn += 1   # pending(turn) için zaman akar
            else:
                world.turn += 1
        obs = encode_obs(world.observe(me, r), energy * cfg.max_energy,
                         cfg, received_vector([]))
        E = np.zeros(N_ACTIONS)
        with torch.no_grad():
            for a in range(N_ACTIONS):
                av = torch.cat([torch.eye(N_ACTIONS)[a],
                                torch.from_numpy(own_signal_onehot(NO_SIGNAL))])
                pred, _ = core(obs.view(1, 1, -1), av.view(1, 1, -1), h)
                E[a] = float(pred[0, 0, -1])
        out[with_event] = E
    return out[True], out[False]


def probe(core, cfg, n_contexts: int = 48, seed0: int = 5000) -> dict:
    rng = np.random.default_rng(seed0)
    K = EVENT_KW["event_polarities"]
    spreads, aligns, gaps, dE = [], [], [], []
    for k in range(n_contexts):
        p = int(rng.integers(0, K))
        cue = rng.integers(0, 2, size=5)
        E1, E0 = _run_context(core, cfg, seed=seed0 + k, polarity=p, cue_bits=cue)
        d = E1 - E0
        spreads.append(float(d.max() - d.min()))
        b = int(cue[0]); v = (p >> b) & 1
        cands = [q for q in range(K) if (q >> b) & 1 == v]
        aligns.append(int(np.argmax(E1)) in cands)
        unsafe = [a for a in range(N_ACTIONS) if a != p]
        gaps.append(float(E1[p] - E1[unsafe].mean()))
        dE.append(float(d.mean()))
    return {"n_contexts": n_contexts,
            "spread_mean": round(float(np.mean(spreads)), 5),
            "spread_p90": round(float(np.percentile(spreads, 90)), 5),
            "own_align_rate": round(float(np.mean(aligns)), 3),
            "safe_gap_mean": round(float(np.mean(gaps)), 5),
            "mean_dE": round(float(np.mean(dE)), 5)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", nargs="*", default=[])
    ap.add_argument("--out", default=None)
    ap.add_argument("--contexts", type=int, default=48)
    a = ap.parse_args()
    results = {}
    # Bilinen-negatif: olay görmemiş transplant (A2 config).
    base = transplant_seed3(SEED3, agent_cfg("A2"), torch_seed=1, np_seed=2)
    results["known_negative_seed3"] = probe(base.core, base.cfg, a.contexts)
    print("[negatif] seed3 transplant:", results["known_negative_seed3"])
    for wpath in a.weights:
        ck = torch.load(wpath, weights_only=False)
        for slot, entry in ck.items():
            core, cfg = _core_from_entry(entry)
            r = probe(core, cfg, a.contexts)
            r.update(id=entry["id"], gen=entry["gen"])
            results[f"{wpath}:{slot}"] = r
            print(f"[{wpath} {slot} {entry['id']}] {r}")
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        json.dump(results, open(a.out, "w"), indent=2)
        print("yazıldı:", a.out)


if __name__ == "__main__":
    main()
