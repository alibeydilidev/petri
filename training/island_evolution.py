"""Program A′ — ada modeli ile evrimsel önyükleme (0 bit; nüfus kuralı).

Neden ada: bireysel seçilim (en uzun yaşayan çoğalır) bilgilendiren
göndericiyi değil, dinleyip bedel ödemeyen bedavacıyı ödüllendirir.
Alarm çağrıları doğada akrabalık / grup düzeyinde seçilimle evrilir.
Burada G ada (her biri 5 ajanlı bağımsız ekoloji) dönem dönem koşulur;
her dönem sonunda adalar olay isabetine göre sıralanır, en kötü Q ada
en iyi Q adanın mutasyonlu kopyasıyla değiştirilir. Bir adada bir
uzlaşı tesadüfen doğarsa o ada kazanır ve yayılır. Ajana bit gitmez
(fitness ajanın girdisine/kaybına girmez; yalnız hangi ağırlıkların
sonraki döneme taşındığını belirler). Deneyci kararı (M-09).

Her dönem: her ada `training.ecology` alt süreci (E tur, kendi
ağırlıklarından kurucu, her dönem yeni dünya seed'i). PER tamponu
dosyaya yazılmadığı için her dönem sıfırdan dolar (beyan; E=10K'da
tampon ~1K turda dolar).

Durum `<out>/state.json`'da; yeniden başlatılabilir (biten dönem atlanır).

Kullanım:
  python -m training.island_evolution --arm open --islands 6 --epochs 30 \\
      --seeds-from runs/c4/C4A_s3001/final_weights.pt,... --out runs/ev/open
"""

import argparse
import json
import pathlib
import subprocess
import sys

import numpy as np
import torch

from training.analyze_s3e import mi_report

PY = sys.executable
BASE_ARGS = ["--nest", "600", "0.5", "--sigma", "0.002", "--events",
             "--event-every", "10", "--event-lead", "4", "--event-share", "0.0",
             "--min-safe", "2"]


def mutate_weights(src: str, dst: str, sigma: float, seed: int) -> None:
    """Tüm 5 çekirdeğe N(0, σ) ekler (kopya adası). numpy rng, deterministik."""
    ck = torch.load(src, weights_only=False)
    rng = np.random.default_rng(seed)
    for slot in sorted(ck):
        sd = ck[slot]["state_dict"]
        for k in sorted(sd):
            t = sd[k]
            if t.is_floating_point():
                sd[k] = t + torch.from_numpy(
                    rng.normal(0.0, sigma, size=tuple(t.shape)).astype("float32"))
        ck[slot].pop("ensemble_state_dict", None)
    torch.save(ck, dst)


def island_fitness(run_dir: pathlib.Path) -> dict:
    j = json.load(open(run_dir / "breath.json"))
    L = j["ledger"]
    et = max(L["event_turns"], 1)
    cs = np.array(j["cue_symbol_cumulative"])
    mi = mi_report(cs, n_perm=50)["mi_miller_madow_bits"] if cs.sum() else 0.0
    return {"hit": L["event_hits"] / et,
            "protected": L.get("event_protected", 0) / et,
            "own_cue": L.get("event_own_consistent", 0) / et,
            "signal_rate": L["signals_sent"] / max(L["agent_turns"], 1),
            "mi_bits": float(mi),
            "harvest_per_1k": 1000 * L["harvests_a"] / max(L["agent_turns"], 1)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["open", "mute"], required=True)
    ap.add_argument("--islands", type=int, default=6)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--epoch-turns", type=int, default=10_000)
    ap.add_argument("--replace", type=int, default=2)
    ap.add_argument("--copy-sigma", type=float, default=0.005)
    ap.add_argument("--seeds-from", required=True,
                    help="virgülle ayrılmış final_weights.pt yolları (adalara döngüyle)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed-base", type=int, default=50_000)
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    state_p = out / "state.json"
    srcs = a.seeds_from.split(",")
    if state_p.exists():
        state = json.load(open(state_p))
    else:
        state = {"arm": a.arm, "islands": a.islands, "epoch_turns": a.epoch_turns,
                 "replace": a.replace, "copy_sigma": a.copy_sigma,
                 "current": [srcs[i % len(srcs)] for i in range(a.islands)],
                 "lineage": [f"src{i % len(srcs)}" for i in range(a.islands)],
                 "epochs": []}
    for k in range(len(state["epochs"]), a.epochs):
        procs, dirs = [], []
        for i in range(a.islands):
            d = out / f"e{k:03d}_i{i}"
            dirs.append(d)
            if (d / "breath.json").exists() and (d / "final_weights.pt").exists():
                procs.append(None); continue
            cmd = [PY, "-m", "training.ecology", "--turns", str(a.epoch_turns),
                   "--out", str(d), "--world-seed", str(a.seed_base + 1000 * k + i),
                   "--founding", f"weights:{state['current'][i]}",
                   "--channel", a.arm, "--log-every", str(a.epoch_turns)] + BASE_ARGS
            log = open(out / f"e{k:03d}_i{i}.log", "w")
            procs.append(subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT))
        for p in procs:
            if p is not None and p.wait() != 0:
                raise SystemExit(f"ada koşumu düştü (dönem {k})")
        fit = [island_fitness(d) for d in dirs]
        order = sorted(range(a.islands), key=lambda i: (-fit[i]["hit"], i))
        top, bottom = order[:a.replace], order[-a.replace:]
        nxt = [str(dirs[i] / "final_weights.pt") for i in range(a.islands)]
        lineage = list(state["lineage"])
        for r, (b, t) in enumerate(zip(bottom, top)):
            dst = out / f"e{k:03d}_copy_{t}_to_{b}.pt"
            mutate_weights(nxt[t], str(dst), a.copy_sigma, seed=a.seed_base + 97 * k + r)
            nxt[b] = str(dst)
            lineage[b] = lineage[t] + f">{k}"
        ep = {"epoch": k, "fitness": fit, "order": order, "replaced": list(zip(bottom, top)),
              "lineage_after": lineage,
              "mean_hit": float(np.mean([f["hit"] for f in fit])),
              "max_hit": float(max(f["hit"] for f in fit)),
              "max_mi": float(max(f["mi_bits"] for f in fit))}
        state["epochs"].append(ep); state["current"] = nxt; state["lineage"] = lineage
        json.dump(state, open(state_p, "w"), indent=2)
        print(f"[{a.arm} dönem {k:>2}] isabet ort {ep['mean_hit']:.3f} maks {ep['max_hit']:.3f} "
              f"| MI maks {ep['max_mi']:.4f} | sinyal "
              f"{np.mean([f['signal_rate'] for f in fit]):.3f} | soylar {sorted(set(l.split('>')[0] for l in lineage))}",
              flush=True)


if __name__ == "__main__":
    main()
