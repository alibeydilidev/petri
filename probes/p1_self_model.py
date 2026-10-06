"""P1 — Öz-model dedektörü. YALNIZ dondurulmuş temsil okur.

Bu modül ajan eğitimine hiçbir yoldan dokunamaz: girdisi diskteki .npz
snapshot'ları (numpy), çıktısı JSON. Ajan süreciyle paylaşılan tek şey
mimari TANIMI (ikiz kontrol için PredictiveCore sınıfı) ve gözlem
kodlayıcıdır (replay için) — ikisi de salt-okunur kullanım.

Hedefler (ayrı problar):
  disp     — öz-konum: epizot başından kümülatif yer değiştirme
             (yol entegrasyonu; ANA kanıt — gözlemde yok, loss'ta yok)
  energy   — öz-enerji (PL-09 şerhli: λ=10 ile eğitime enjekte, YAN kanıt)
  denergy  — sonraki-tur öz-enerji deltası

Kontroller:
  (a) rastgele-ağırlıklı ikiz GRU (3 ikiz ortalaması): AYNI gözlem/eylem
      akışı deterministik dünya replay'i ile yeniden üretilir (S0
      determinizmi tam bu iş içindi; pozisyon+enerji bit-eş assert edilir)
  (b) etiket karıştırma: şans tabanı
  (c) checkpoint eğrisi: yapısal mı kazanılmış mı

Prob sınıfı: lineer ridge (LOEO çapraz doğrulama, iç-CV ile λ);
lineer negatifse küçük MLP ile tekrar, İKİSİ birlikte raporlanır.
"""

import argparse
import glob
import json
import pathlib
import re
from collections import defaultdict

import numpy as np
import torch
from scipy.stats import spearmanr, wilcoxon

from agent.config import a2_config
from agent.homeostasis import Homeostasis
from agent.predictive_core import PredictiveCore
from training.loop import encode_obs
from training.snapshot import load as load_snap
from world.config import WorldConfig
from world.grid import N_ACTIONS, World

LAMBDAS = (1.0, 10.0, 100.0, 1000.0)
TWIN_SEEDS = (7001, 7002, 7003)


# --------------------------------------------------------------- replay/twin

def snap_cfg(snap: dict):
    """Snapshot'ın kaydedildiği ajan konfigürasyonu (meta'dan; eski
    S2 kayıtları için A2 varsayılanına düşer)."""
    from agent.config import AgentConfig
    meta = snap["meta"]
    if "agent_config" in meta:
        return AgentConfig(**meta["agent_config"])
    return a2_config()


def replay_twins(snap: dict, cfg=None, twin_seeds=TWIN_SEEDS):
    """Kayıtlı eylemleri deterministik dünyada yeniden koşar; ikiz GRU'ların
    hidden dizilerini üretir. Sadakat: pozisyon bit-eş, enerji ~1e-9.

    Dönüş: (h_twins: {seed: (n, H)}, start_pos: (2,))
    """
    meta = snap["meta"]
    if cfg is None:
        cfg = snap_cfg(snap)
    # M-10: dünya, kaydın damgasından kurulur; damgasız eski kayıtlar
    # v1 ekonomisinde doğdu — varsayılana (v2) DÜŞME.
    if meta.get("world_config"):
        wcfg = WorldConfig(**meta["world_config"])
    else:
        from world.config import economy_v1
        wcfg = economy_v1()
    world = World(wcfg, n_entities=1, seed=meta["world_seed"])
    if meta.get("start_pos") is not None:  # spawn randomizasyonu (PL-11)
        world.entity_pos[0] = np.array(meta["start_pos"], dtype=np.int64)
    homeo = Homeostasis(cfg)
    start_pos = world.entity_pos[0].copy()

    twins = {}
    for ts in twin_seeds:
        torch.manual_seed(ts)
        twins[ts] = PredictiveCore(cfg)
    h = {ts: None for ts in twin_seeds}
    outs = {ts: [] for ts in twin_seeds}

    actions = snap["action"]
    n = len(actions)
    e_for_obs = homeo.energy
    with torch.no_grad():
        for i in range(n):
            obs_vec = encode_obs(world.observe(0, cfg.obs_radius), e_for_obs, cfg)
            act_oh = torch.zeros(N_ACTIONS)
            act_oh[int(actions[i])] = 1.0
            for ts in twin_seeds:
                _, h[ts] = twins[ts](obs_vec.view(1, 1, -1),
                                     act_oh.view(1, 1, -1), h[ts])
                outs[ts].append(h[ts].numpy().reshape(-1).copy())
            deltas = world.step(np.array([int(actions[i])]))
            homeo.apply_turn(int(actions[i]), float(deltas[0]))
            # Sadakat kapısı: replay kayıtla bit-eş olmak ZORUNDA.
            if not np.array_equal(world.entity_pos[0], snap["pos"][i]):
                raise RuntimeError(f"replay sadakati bozuk: tur {i} pozisyon")
            if abs(homeo.energy - snap["energy"][i]) > 1e-6:
                raise RuntimeError(f"replay sadakati bozuk: tur {i} enerji")
            e_for_obs = max(homeo.energy, 0.0)
    return {ts: np.stack(outs[ts]) for ts in twin_seeds}, start_pos


# --------------------------------------------------------------- targets

def unwrap_displacement(pos: np.ndarray, start_pos: np.ndarray,
                        grid: int = 64) -> np.ndarray:
    """Toroidal kayıtlı pozisyonlardan kümülatif yer değiştirme (n, 2)."""
    seq = np.vstack([start_pos[None, :], pos]).astype(np.int64)
    d = np.diff(seq, axis=0)
    d = np.where(d > grid // 2, d - grid, d)
    d = np.where(d < -grid // 2, d + grid, d)
    return np.cumsum(d, axis=0).astype(np.float64)


def build_targets(snap: dict, start_pos: np.ndarray) -> dict[str, np.ndarray]:
    energy = snap["energy"].astype(np.float64) / 100.0
    disp = unwrap_displacement(snap["pos"], start_pos)
    denergy = np.diff(energy)
    return {"disp": disp, "energy": energy[:, None], "denergy": denergy[:, None]}


# --------------------------------------------------------------- ridge probe

def _ridge_fit(Xtr, ytr, lam):
    mx, sx = Xtr.mean(0), Xtr.std(0) + 1e-8
    my, sy = ytr.mean(0), ytr.std(0) + 1e-8
    Xs, ys = (Xtr - mx) / sx, (ytr - my) / sy
    d = Xs.shape[1]
    W = np.linalg.solve(Xs.T @ Xs + lam * np.eye(d), Xs.T @ ys)
    return W, (mx, sx, my, sy)

def _ridge_r2(Xte, yte, W, norms):
    mx, sx, my, sy = norms
    pred = ((Xte - mx) / sx) @ W * sy + my
    sse = ((yte - pred) ** 2).sum(0)
    sst = ((yte - yte.mean(0)) ** 2).sum(0) + 1e-12
    return float(np.mean(1.0 - sse / sst))

def probe_loeo(groups: list[tuple[np.ndarray, np.ndarray]]) -> list[float]:
    """Grup (epizot) başına dışarıda-bırak R²; iç-CV ile λ seçimi."""
    scores = []
    for k in range(len(groups)):
        train = [g for j, g in enumerate(groups) if j != k]
        best_lam, best = None, -np.inf
        for lam in LAMBDAS:
            inner = []
            for m in range(len(train)):
                itr = [g for j, g in enumerate(train) if j != m]
                Xtr = np.vstack([g[0] for g in itr]); ytr = np.vstack([g[1] for g in itr])
                W, nrm = _ridge_fit(Xtr, ytr, lam)
                inner.append(_ridge_r2(train[m][0], train[m][1], W, nrm))
            if np.mean(inner) > best:
                best, best_lam = np.mean(inner), lam
        Xtr = np.vstack([g[0] for g in train]); ytr = np.vstack([g[1] for g in train])
        W, nrm = _ridge_fit(Xtr, ytr, best_lam)
        scores.append(_ridge_r2(groups[k][0], groups[k][1], W, nrm))
    return scores


def probe_mlp(groups, seed: int = 0, hidden: int = 64, epochs: int = 300) -> list[float]:
    """Lineer negatifse ikinci görüş: küçük MLP, aynı LOEO protokolü."""
    scores = []
    for k in range(len(groups)):
        train = [g for j, g in enumerate(groups) if j != k]
        Xtr = np.vstack([g[0] for g in train]); ytr = np.vstack([g[1] for g in train])
        mx, sx = Xtr.mean(0), Xtr.std(0) + 1e-8
        my, sy = ytr.mean(0), ytr.std(0) + 1e-8
        torch.manual_seed(seed + k)
        net = torch.nn.Sequential(
            torch.nn.Linear(Xtr.shape[1], hidden), torch.nn.ReLU(),
            torch.nn.Linear(hidden, ytr.shape[1]))
        opt = torch.optim.Adam(net.parameters(), lr=1e-3)
        Xt = torch.tensor((Xtr - mx) / sx, dtype=torch.float32)
        yt = torch.tensor((ytr - my) / sy, dtype=torch.float32)
        for _ in range(epochs):
            opt.zero_grad()
            loss = torch.nn.functional.mse_loss(net(Xt), yt)
            loss.backward(); opt.step()
        with torch.no_grad():
            Xe = torch.tensor((groups[k][0] - mx) / sx, dtype=torch.float32)
            pred = net(Xe).numpy() * sy + my
        yte = groups[k][1]
        sse = ((yte - pred) ** 2).sum(0)
        sst = ((yte - yte.mean(0)) ** 2).sum(0) + 1e-12
        scores.append(float(np.mean(1.0 - sse / sst)))
    return scores


# --------------------------------------------------------------- evaluation

def episode_groups(files: list[str], cfg=None, shuffle_rng=None):
    """Dosya (epizot) başına: eğitilmiş-h, ikiz-h'ler ve hedef grupları.
    cfg=None → her dosyanın kendi meta config'i kullanılır."""
    out = {"trained": defaultdict(list), "twin": defaultdict(list),
           "shuffle": defaultdict(list)}
    for f in sorted(files):
        snap = load_snap(f)
        h_twins, start = replay_twins(snap, cfg)
        targets = build_targets(snap, start)
        h = snap["h"].astype(np.float64)
        h_twin_mean = {ts: ht.astype(np.float64) for ts, ht in h_twins.items()}
        for name, y in targets.items():
            n = len(y)
            out["trained"][name].append((h[:n], y))
            for ts in TWIN_SEEDS:
                out["twin"][(name, ts)].append((h_twin_mean[ts][:n], y))
            ys = y.copy()
            if shuffle_rng is not None:
                shuffle_rng.shuffle(ys)
            out["shuffle"][name].append((h[:n], ys))
    return out


def evaluate_seed_checkpoint(files, rng, cfg=None) -> dict:
    g = episode_groups(files, cfg, shuffle_rng=rng)
    res = {}
    for name in ("disp", "energy", "denergy"):
        trained = probe_loeo(g["trained"][name])
        twin_scores = np.mean(
            [probe_loeo(g["twin"][(name, ts)]) for ts in TWIN_SEEDS], axis=0)
        shuf = probe_loeo(g["shuffle"][name])
        res[name] = {
            "trained_r2": [round(s, 4) for s in trained],
            "twin_r2": [round(float(s), 4) for s in twin_scores],
            "shuffle_r2_mean": round(float(np.mean(shuf)), 4),
            "trained_mean": round(float(np.mean(trained)), 4),
            "twin_mean": round(float(np.mean(twin_scores)), 4),
            "delta_r2": round(float(np.mean(trained) - np.mean(twin_scores)), 4),
        }
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="runs/s2_snapshots")
    ap.add_argument("--out", default="runs/s2_p1_results.json")
    ap.add_argument("--mlp-if-negative", action="store_true", default=True)
    a = ap.parse_args()
    rng = np.random.default_rng(1234)

    by_seed_ckpt = defaultdict(list)
    for f in glob.glob(str(pathlib.Path(a.data) / "s2_seed*_ck*_ep*.npz")):
        m = re.search(r"seed(\d+)_ck(\d+)_ep", f)
        by_seed_ckpt[(int(m.group(1)), int(m.group(2)))].append(f)

    results = defaultdict(dict)
    for (seed, ck) in sorted(by_seed_ckpt):
        results[seed][ck] = evaluate_seed_checkpoint(by_seed_ckpt[(seed, ck)],
                                                     rng)
        d = results[seed][ck]["disp"]
        print(f"[seed {seed} ck {ck:>5}] disp R² eğitilmiş {d['trained_mean']:+.3f} "
              f"ikiz {d['twin_mean']:+.3f} Δ {d['delta_r2']:+.3f}", flush=True)

    # Final checkpoint istatistikleri + eğri + (gerekirse) MLP ikinci görüş.
    summary = {}
    for seed, cks in results.items():
        final_ck = max(cks)
        first_ck = min(cks)
        seed_sum = {}
        for name in ("disp", "energy", "denergy"):
            fin = cks[final_ck][name]
            tr, tw = np.array(fin["trained_r2"]), np.array(fin["twin_r2"])
            try:
                stat = wilcoxon(tr, tw, alternative="greater")
                p = float(stat.pvalue)
            except ValueError:
                p = 1.0
            curve = [cks[ck][name]["trained_mean"] for ck in sorted(cks)]
            rho = spearmanr(sorted(cks), curve).statistic if len(cks) > 2 else 0.0
            seed_sum[name] = {
                "final_delta_r2": fin["delta_r2"],
                "wilcoxon_p": round(p, 5),
                "curve_trained": curve,
                "curve_twin": [cks[ck][name]["twin_mean"] for ck in sorted(cks)],
                "curve_spearman_rho": round(float(rho), 3),
                "rising": bool(curve[-1] > curve[0]),
                "first_vs_final": [curve[0], curve[-1]],
            }
        summary[seed] = seed_sum

    # MLP ikinci görüş: lineer bulgu final ckpt'de negatifse.
    mlp_annex = {}
    for seed, cks in results.items():
        final_ck = max(cks)
        for name in ("disp", "energy", "denergy"):
            if summary[seed][name]["final_delta_r2"] <= 0 or \
               cks[final_ck][name]["trained_mean"] <= 0:
                files = by_seed_ckpt[(seed, final_ck)]
                g = episode_groups(files)
                mlp_tr = probe_mlp(g["trained"][name])
                mlp_tw = np.mean([probe_mlp(g["twin"][(name, ts)])
                                  for ts in TWIN_SEEDS], axis=0)
                mlp_annex[f"seed{seed}_{name}"] = {
                    "mlp_trained_mean": round(float(np.mean(mlp_tr)), 4),
                    "mlp_twin_mean": round(float(np.mean(mlp_tw)), 4),
                }

    out = {"per_seed_checkpoint": {str(k): v for k, v in
                                   ((s, dict(cks)) for s, cks in results.items())},
           "summary": {str(k): v for k, v in summary.items()},
           "mlp_annex": mlp_annex,
           "twin_seeds": TWIN_SEEDS, "lambdas": LAMBDAS}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nyazıldı: {a.out}")


if __name__ == "__main__":
    main()
