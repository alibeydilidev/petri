"""S3-E analiz aracı: runs/s3e/<kol>_s<seed>/breath.json → ön-kayıtlı
çıtalar (FINDINGS S3-E ÖN-KAYIT). Ölçüm aleti; ajana gitmez.

Karşılıklı bilgi I(ipucu; sembol): 4×16 tablo, log2. Miller-Madow
yanlılık düzeltmesi ve 200 permütasyonlu şans dağılımı (satır/sütun
marjinalleri sabit) raporlanır — n küçükken ham I şişer (M-13:
anlamlılık ≠ etki).

Kullanım: python3 -m training.analyze_s3e [--dir runs/s3e] [--out runs/s3e/summary.json]
"""

import argparse
import json
import pathlib

import numpy as np


def mutual_info_bits(table: np.ndarray) -> float:
    t = table.astype(float)
    n = t.sum()
    if n == 0:
        return 0.0
    p = t / n
    pr, pc = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        term = p * np.log2(p / (pr @ pc))
    return float(np.nansum(term))


def mi_report(table: np.ndarray, n_perm: int = 200, seed: int = 0) -> dict:
    t = np.asarray(table, dtype=np.int64)
    n = int(t.sum())
    raw = mutual_info_bits(t)
    rows_nz = int((t.sum(1) > 0).sum())
    cols_nz = int((t.sum(0) > 0).sum())
    mm = (rows_nz - 1) * (cols_nz - 1) / (2 * n * np.log(2)) if n else 0.0
    # permütasyon: marjinaller sabit, bağımlılık kırılır
    rng = np.random.default_rng(seed)
    perms = []
    if n:
        row_lab = np.repeat(np.arange(t.shape[0]), t.sum(1))
        col_lab = np.repeat(np.arange(t.shape[1]), t.sum(0))
        for _ in range(n_perm):
            rng.shuffle(col_lab)
            tt = np.zeros_like(t)
            np.add.at(tt, (row_lab, col_lab), 1)
            perms.append(mutual_info_bits(tt))
    perms = np.array(perms) if perms else np.zeros(1)
    return {"n": n, "mi_raw_bits": round(raw, 4),
            "mi_miller_madow_bits": round(max(raw - mm, 0.0), 4),
            "perm_mean_bits": round(float(perms.mean()), 4),
            "perm_p95_bits": round(float(np.percentile(perms, 95)), 4),
            "p_value_perm": round(float((perms >= raw).mean()), 3),
            "row_counts": t.sum(1).tolist()}


def analyze_run(path: pathlib.Path) -> dict:
    j = json.load(open(path))
    L = j["ledger"]
    lifes = np.array(L["lifespans"], dtype=float)
    at = max(L["agent_turns"], 1)
    et, eh = L["event_turns"], L["event_hits"]
    eth, ehh = L["event_turns_heard"], L["event_hits_heard"]
    out = {"arm": j["arm"], "seed": j["world_seed"], "deaths": j["deaths"],
           "median_lifespan": float(np.median(lifes)) if lifes.size else None,
           "mean_lifespan": round(float(lifes.mean()), 1) if lifes.size else None,
           "a_harvest_per_1k": round(1000 * L["harvests_a"] / at, 2),
           "signal_rate": round(L["signals_sent"] / at, 4),
           "pending_signal_rate": (round(L["pending_signals"]
                                         / L["pending_turns"], 4)
                                   if L["pending_turns"] else None),
           "event_hit_rate": round(eh / et, 4) if et else None,
           "hit_rate_heard": round(ehh / eth, 4) if eth else None,
           "hit_rate_not_heard": (round((eh - ehh) / (et - eth), 4)
                                  if et - eth else None),
           "heard_share_of_events": round(eth / et, 4) if et else None,
           "own_cue_consistent_rate": (round(L.get("event_own_consistent", 0)
                                             / et, 4) if et else None),
           "event_stay_share": (round(L.get("event_stay", 0) / et, 4)
                                if et else None),
           "deaths_in_nest": L["deaths_in_nest"],
           "deaths_nest_tail": L["deaths_nest_tail"],
           "b_openings": L["b_openings"],
           "symbol_entropy_bits": None}
    h = np.array(j["symbol_hist_cumulative"], dtype=float)
    if h.sum():
        p = h / h.sum()
        out["symbol_entropy_bits"] = round(float(-(p[p > 0]
                                                   * np.log2(p[p > 0])).sum()), 4)
    cs = np.array(j["cue_symbol_cumulative"])
    out["mi_cue_symbol"] = mi_report(cs) if cs.sum() else None
    # ipucu BİT DEĞERİ (0/1) × sembol: 2×16 — "hangi bit" değil "ne değer"
    val_tab = np.vstack([cs[0] + cs[2], cs[1] + cs[3]])
    out["mi_cuevalue_symbol"] = mi_report(val_tab, seed=1) if cs.sum() else None
    # zaman çizgisi: pencere oranları
    out["timeline"] = [{"turn": v["turn"], "hit": v["event_hit_rate_window"],
                        "sig": v["signal_rate_window"],
                        "life": v["median_lifespan"], "deaths": v["deaths"]}
                       for v in j["vitals"] if v["turn"] % 5000 == 0]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="runs/s3e")
    ap.add_argument("--out", default="runs/s3e/summary.json")
    a = ap.parse_args()
    runs = sorted(pathlib.Path(a.dir).glob("*_s*/breath.json"))
    rows = [analyze_run(p) for p in runs]
    by_arm: dict[str, list] = {}
    for r, p in zip(rows, runs):
        by_arm.setdefault(p.parent.name.split("_")[0], []).append(r)
    summary = {}
    for arm, rs in by_arm.items():
        def med(key):
            v = [r[key] for r in rs if r.get(key) is not None]
            return round(float(np.median(v)), 4) if v else None
        summary[arm] = {
            "n_runs": len(rs),
            "median_lifespan": med("median_lifespan"),
            "event_hit_rate": med("event_hit_rate"),
            "hit_rate_heard": med("hit_rate_heard"),
            "hit_rate_not_heard": med("hit_rate_not_heard"),
            "signal_rate": med("signal_rate"),
            "pending_signal_rate": med("pending_signal_rate"),
            "a_harvest_per_1k": med("a_harvest_per_1k"),
            "own_cue_consistent_rate": med("own_cue_consistent_rate"),
            "event_stay_share": med("event_stay_share"),
            "mi_cue_symbol_mm_bits": [r["mi_cue_symbol"]["mi_miller_madow_bits"]
                                      for r in rs if r["mi_cue_symbol"]],
            "mi_cue_symbol_p": [r["mi_cue_symbol"]["p_value_perm"]
                                for r in rs if r["mi_cue_symbol"]],
            "deaths": [r["deaths"] for r in rs],
            "deaths_in_nest": [r["deaths_in_nest"] for r in rs],
            "deaths_nest_tail": [r["deaths_nest_tail"] for r in rs],
        }
        print(f"[{arm}] n={len(rs)} | medyan ömür {summary[arm]['median_lifespan']} "
              f"| isabet {summary[arm]['event_hit_rate']} (duydu "
              f"{summary[arm]['hit_rate_heard']} / duymadı "
              f"{summary[arm]['hit_rate_not_heard']}) | sinyal "
              f"{summary[arm]['signal_rate']} | I(ipucu;sembol) MM "
              f"{summary[arm]['mi_cue_symbol_mm_bits']} p "
              f"{summary[arm]['mi_cue_symbol_p']} | ölüm {summary[arm]['deaths']} "
              f"yuva-içi {summary[arm]['deaths_in_nest']} "
              f"yuva-sonu {summary[arm]['deaths_nest_tail']}")
    with open(a.out, "w") as f:
        json.dump({"runs": rows, "summary": summary}, f, indent=2)
    print(f"yazıldı: {a.out}")


if __name__ == "__main__":
    main()
