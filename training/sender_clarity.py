"""PL-38: gönderici netliği zaman çizgisi — vitals'tan pencere başına
P(sinyal|değer) ve I(değer; sinyal var/yok) (değer 0/1 eşit olası varsayımı).
Kullanım: python -m training.sender_clarity runs/pl38/LA_s3001 [...]"""
import json
import sys

import numpy as np


def _h(p):
    p = np.clip(p, 1e-12, 1); return -(p * np.log2(p)).sum()


def clarity(rows, pending):
    s0, s1 = rows[0] + rows[2], rows[1] + rows[3]; n = pending / 2
    if n <= 0:
        return None
    P = np.array([[s0, n - s0], [s1, n - s1]]) / (2 * n)
    return {"p0": s0 / n, "p1": s1 / n, "mi": float(_h(P.sum(1)) + _h(P.sum(0)) - _h(P.ravel()))}


def windows(path, every=None):
    v = [x for x in json.load(open(f"{path}/breath.json"))["vitals"] if "cue_rows" in x]
    out, prev = [], None
    for x in v:
        if prev is not None:
            r = np.array(x["cue_rows"]) - np.array(prev["cue_rows"])
            c = clarity(r, x["pending_turns"] - prev["pending_turns"])
            hits = x["event_hits"] - prev["event_hits"]; et = x["event_turns"] - prev["event_turns"]
            out.append({"turn": x["turn"], **{k: round(val, 4) for k, val in c.items()},
                        "hit": round(hits / et, 4) if et else None,
                        "own": x.get("own_cue_rate_window")})
        prev = x
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p)
        for w in windows(p):
            print("  ", w)
