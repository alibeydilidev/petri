"""PL-37 / CH0 — varlık-kodlu kanal oracle'ı (saf Monte Carlo; ölçüm aleti, 0 bit).

Kimliksiz küresel kanalda göndericiler "bitim 1 ise konuşurum" kuralıyla
(varlık kodu) yayın yaparsa, Bayes-optimal bir alıcı K=4 kutbu ne kadar
çözer? Her ajan olay başına rastgele bir bit indeksi b∈{0,1} ve o bitin
değerini görür (S3-C `event_visibility_split`). Alıcı yalnız diğerlerinin
KAÇININ konuştuğunu duyar (kimlik/sembol yok).

Kullanım: python -m training.channel_oracle --events 200000
"""

import argparse
import itertools
import json

import numpy as np

K, N = 4, 5


def bit(p, b):
    return (p >> b) & 1


def decode_presence(own_b, own_v, k_heard, ps1, ps0, n_others=N - 1):
    """Bayes-optimal kutup: P(p) ∝ 1[bit_own(p)=own_v] · P(k | p)."""
    best, bestp = None, -1.0
    for p in range(K):
        if bit(p, own_b) != own_v:
            continue
        # diğer ajan: indeks tekdüze → P(konuşur|p) = ort_b [ps1 if bit_b(p) else ps0]
        q = 0.5 * sum(ps1 if bit(p, b) else ps0 for b in (0, 1))
        from math import comb
        lik = comb(n_others, k_heard) * q ** k_heard * (1 - q) ** (n_others - k_heard)
        if lik > bestp + 1e-15:
            best, bestp = p, lik
    return best


def run(arm, events, rng, ps1=1.0, ps0=0.0):
    hits = prot = 0
    total = 0
    for _ in range(events):
        p = int(rng.integers(0, K))
        idx = rng.integers(0, 2, size=N)
        vals = np.array([bit(p, b) for b in idx])
        if arm == "told":
            # her ajan diğer en az bir ajanın farklı indeksini duyarsa tam bilir
            choices = []
            for i in range(N):
                others_idx = set(int(idx[j]) for j in range(N) if j != i)
                known = {int(idx[i])} | others_idx
                if known == {0, 1}:
                    choices.append(p)
                else:
                    cands = [q for q in range(K) if bit(q, idx[i]) == vals[i]]
                    choices.append(int(rng.choice(cands)))
        else:
            speaks = np.zeros(N, dtype=bool)
            if arm.startswith("presence"):
                pr = np.where(vals == 1, ps1, ps0)
                speaks = rng.random(N) < pr
            choices = []
            for i in range(N):
                if arm == "own":
                    cands = [q for q in range(K) if bit(q, idx[i]) == vals[i]]
                    choices.append(int(rng.choice(cands)))
                else:
                    k = int(speaks.sum() - speaks[i])
                    choices.append(decode_presence(int(idx[i]), int(vals[i]), k, ps1, ps0))
        choices = np.array(choices)
        correct = choices == p
        hits += int(correct.sum())
        prot += int((correct & (correct.sum() >= 2)).sum())
        total += N
    return {"arm": arm, "hit": round(hits / total, 4), "protected_N2": round(prot / total, 4)}


def info_presence(ps1, ps0):
    """I(kutup; k | kendi (b,v)) — alıcıya kanalın kattığı bilgi (bit)."""
    from math import comb, log2
    tot = 0.0
    for b, v in itertools.product((0, 1), (0, 1)):
        cands = [p for p in range(K) if bit(p, b) == v]
        joint = {}
        for p in cands:
            q = 0.5 * sum(ps1 if bit(p, bb) else ps0 for bb in (0, 1))
            for k in range(N):
                joint[(p, k)] = (1 / len(cands)) * comb(N - 1, k) * q ** k * (1 - q) ** (N - 1 - k)
        pk = {k: sum(joint[(p, k)] for p in cands) for k in range(N)}
        mi = sum(pr * log2(pr / ((1 / len(cands)) * pk[k])) for (p, k), pr in joint.items() if pr > 0)
        tot += 0.25 * mi
    return round(tot, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", type=int, default=200_000)
    ap.add_argument("--out", default="runs/ch0_channel_oracle.json")
    a = ap.parse_args()
    rng = np.random.default_rng(37)
    res = [run("own", a.events, rng), run("presence", a.events, rng, 1.0, 0.0),
           run("presence_obs", a.events, rng, 0.55, 0.22), run("told", a.events, rng)]
    res[1]["info_bits"] = info_presence(1.0, 0.0)
    res[2]["info_bits"] = info_presence(0.55, 0.22)
    for r in res:
        print(r)
    json.dump(res, open(a.out, "w"), indent=2)


if __name__ == "__main__":
    main()
