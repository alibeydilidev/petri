"""S1 bitti-tanımı deneyi: A2 (MPC + online öğrenme) vs rastgele politika.

Protokol (seed başına):
  1. Eğitim fazı: taze A2, ardışık epizotlarla toplam >= train_turns tur
     yaşar (ağırlıklar epizotlar arası taşınır — PL-06).
  2. Değerlendirme fazı: eval_episodes taze dünyada (eğitimde GÖRÜLMEMİŞ
     world seed'leri) yaşam süresi ölçülür; online öğrenme açık kalır
     (ajanın tanımı bu).
  3. Rastgele politika AYNI eval dünyalarında koşar.
İstatistik: seed başına tek yönlü Mann-Whitney U (A2 > rastgele) +
Cliff's delta; ayrıca 5 seed'in tümünde tutarlılık şartı (Beş Kapı
KAPI 1 disiplini S1'e de uygulanır).

Kullanım:
  python3 -m training.eval_s1 --out runs/s1_results.json
"""

import argparse
import json
import pathlib
import time

import numpy as np
from scipy.stats import mannwhitneyu

from agent.config import a2_config
from training.loop import OnlineAgent, run_episode
from training.snapshot import SnapshotRecorder


def cliffs_delta(a, b) -> float:
    a, b = np.asarray(a), np.asarray(b)
    gt = (a[:, None] > b[None, :]).sum()
    lt = (a[:, None] < b[None, :]).sum()
    return float((gt - lt) / (len(a) * len(b)))


def run_seed(seed: int, train_turns: int, eval_episodes: int, cap: int,
             snapshot_dir: str | None) -> dict:
    cfg = a2_config()
    agent = OnlineAgent(cfg, torch_seed=1000 + seed, np_seed=2000 + seed)

    # --- eğitim fazı ---
    t0 = time.perf_counter()
    total, ep, train_lifetimes = 0, 0, []
    while total < train_turns:
        r = run_episode(agent, world_seed=seed * 10_000 + ep, cfg=cfg, max_turns=cap)
        train_lifetimes.append(r["lifetime"])
        total += r["lifetime"]
        ep += 1
    train_time = time.perf_counter() - t0

    # --- değerlendirme fazı (taze dünyalar; son epizotta snapshot) ---
    a2_life, a2_harvest = [], []
    for j in range(eval_episodes):
        snap = None
        if snapshot_dir is not None and j == eval_episodes - 1:
            snap = SnapshotRecorder(stride=1)
        r = run_episode(agent, world_seed=seed * 10_000 + 5000 + j, cfg=cfg,
                        max_turns=cap, snapshot=snap)
        a2_life.append(r["lifetime"])
        a2_harvest.append(r["harvested"])
        if snap is not None:
            p = pathlib.Path(snapshot_dir) / f"s1_seed{seed}_eval{j}.npz"
            snap.save(str(p), agent, {"world_seed": seed * 10_000 + 5000 + j})

    # --- rastgele politika, aynı eval dünyaları ---
    rnd_life, rnd_harvest = [], []
    rng = np.random.default_rng(3000 + seed)
    for j in range(eval_episodes):
        r = run_episode("random", world_seed=seed * 10_000 + 5000 + j, cfg=cfg,
                        max_turns=cap, random_rng=rng)
        rnd_life.append(r["lifetime"])
        rnd_harvest.append(r["harvested"])

    stat = mannwhitneyu(a2_life, rnd_life, alternative="greater")
    return {
        "seed": seed,
        "train_episodes": ep,
        "train_turns": total,
        "train_time_s": round(train_time, 1),
        "per_turn_ms": round(1000 * train_time / total, 3),
        "train_lifetimes_last5": train_lifetimes[-5:],
        "a2_lifetimes": a2_life,
        "random_lifetimes": rnd_life,
        "a2_harvested_mean": round(float(np.mean(a2_harvest)), 1),
        "random_harvested_mean": round(float(np.mean(rnd_harvest)), 1),
        "a2_median": float(np.median(a2_life)),
        "random_median": float(np.median(rnd_life)),
        "mwu_p": float(stat.pvalue),
        "cliffs_delta": round(cliffs_delta(a2_life, rnd_life), 3),
        "final_weight_hash": agent.core.weight_hash(),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--train-turns", type=int, default=40_000)
    ap.add_argument("--eval-episodes", type=int, default=12)
    ap.add_argument("--cap", type=int, default=1500)
    ap.add_argument("--out", default="runs/s1_results.json")
    ap.add_argument("--snapshot-dir", default="runs/snapshots")
    a = ap.parse_args()

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.snapshot_dir).mkdir(parents=True, exist_ok=True)

    results = []
    for s in range(a.seeds):
        r = run_seed(s, a.train_turns, a.eval_episodes, a.cap, a.snapshot_dir)
        results.append(r)
        print(f"[seed {s}] A2 medyan {r['a2_median']:.0f} vs rastgele "
              f"{r['random_median']:.0f} tur | p={r['mwu_p']:.2e} | "
              f"δ={r['cliffs_delta']} | {r['per_turn_ms']} ms/tur", flush=True)

    all_sig = all(r["mwu_p"] < 0.05 for r in results)
    all_dir = all(r["a2_median"] > r["random_median"] for r in results)
    summary = {
        "all_seeds_significant_p05": all_sig,
        "all_seeds_direction_consistent": all_dir,
        "median_per_turn_ms": float(np.median([r["per_turn_ms"] for r in results])),
        "config": vars(a),
        "results": results,
    }
    with open(a.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nsonuç: {a.out} | tüm seed'ler p<0.05: {all_sig} | "
          f"yön tutarlı: {all_dir}")


if __name__ == "__main__":
    main()
