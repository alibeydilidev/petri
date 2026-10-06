"""PETRI replay viewer — ayrı süreçte çalışan izleyici.

Sıfır bağımlılık: ANSI/terminal render (PL-03). matplotlib kuruluysa
`play --backend mpl` de kullanılabilir.

Kullanım:
    python3 -m replay.viewer record out.npz --turns 2000 [--seed 42] [--stride 1]
    python3 -m replay.viewer play out.npz [--fps 20] [--start 0] [--no-color]
    python3 -m replay.viewer frame out.npz --at 150
    python3 -m replay.viewer info out.npz
"""

import argparse
import sys
import time

import numpy as np

from replay import recorder as rec
from world.config import WorldConfig
from world.grid import N_ACTIONS, World

# Semboller: . boş, a kaynak A, B kaynak B, ! tehlike bölgesi, 0-9 varlık.
_CLR = {"a": "\x1b[32m", "B": "\x1b[1;33m", "!": "\x1b[31m", "e": "\x1b[1;36m",
        "reset": "\x1b[0m"}


def record(path: str, turns: int, seed: int, stride: int, n_entities: int) -> None:
    """Seed'li rastgele politika ile koşum kaydeder (S0: ajan yok)."""
    world = World(WorldConfig(), n_entities=n_entities, seed=seed)
    policy_rng = np.random.default_rng(seed + 1)  # dünya RNG'sinden ayrı, kayıtlı
    r = rec.Recorder(world)
    for t in range(1, turns + 1):
        world.step(policy_rng.integers(0, N_ACTIONS, size=n_entities))
        if t % stride == 0:
            r.capture()
    r.save(path)
    print(f"kayıt: {path} | {turns} tur (stride {stride}) | seed {seed} | "
          f"final hash {world.state_hash()[:16]}…")


def _render_frame(data: dict, idx: int, color: bool) -> str:
    g = data["meta"]["grid_size"]
    rad = data["meta"]["hazard_radius"]
    canvas = np.full((g, g), ".", dtype="<U1")
    for hy, hx in data["hazard"][idx]:
        if hy < 0:
            continue
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                canvas[(hy + dy) % g][(hx + dx) % g] = "!"
    for y, x in data["res_a"][idx]:
        canvas[y][x] = "a"
    for y, x in data["res_b"][idx]:
        canvas[y][x] = "B"
    for i, (y, x) in enumerate(data["entity"][idx]):
        canvas[y][x] = str(i % 10)
    lines = []
    for row in canvas:
        if color:
            out = []
            for ch in row:
                if ch == ".":
                    out.append(ch)
                elif ch.isdigit():
                    out.append(f"{_CLR['e']}{ch}{_CLR['reset']}")
                else:
                    out.append(f"{_CLR[ch]}{ch}{_CLR['reset']}")
            lines.append("".join(out))
        else:
            lines.append("".join(row))
    head = (f"tur {int(data['turns'][idx])}  "
            f"[kare {idx + 1}/{len(data['turns'])}]  "
            f"a:{len(data['res_a'][idx])} B:{len(data['res_b'][idx])} "
            f"tehlike:{int((data['hazard'][idx][:, 0] >= 0).sum())}")
    return head + "\n" + "\n".join(lines)


def play(path: str, fps: float, start: int, color: bool) -> None:
    data = rec.load(path)
    n = len(data["turns"])
    try:
        for idx in range(start, n):
            frame = _render_frame(data, idx, color)
            sys.stdout.write("\x1b[2J\x1b[H" + frame + "\n")
            sys.stdout.flush()
            time.sleep(1.0 / fps)
    except KeyboardInterrupt:
        pass


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="replay.viewer")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("record")
    pr.add_argument("path")
    pr.add_argument("--turns", type=int, default=2000)
    pr.add_argument("--seed", type=int, default=WorldConfig().seed)
    pr.add_argument("--stride", type=int, default=1)
    pr.add_argument("--entities", type=int, default=5)

    pp = sub.add_parser("play")
    pp.add_argument("path")
    pp.add_argument("--fps", type=float, default=20.0)
    pp.add_argument("--start", type=int, default=0)
    pp.add_argument("--no-color", action="store_true")

    pf = sub.add_parser("frame")
    pf.add_argument("path")
    pf.add_argument("--at", type=int, default=0, help="kare indeksi")
    pf.add_argument("--no-color", action="store_true")

    pi = sub.add_parser("info")
    pi.add_argument("path")

    a = p.parse_args(argv)
    if a.cmd == "record":
        record(a.path, a.turns, a.seed, a.stride, a.entities)
    elif a.cmd == "play":
        play(a.path, a.fps, a.start, color=not a.no_color)
    elif a.cmd == "frame":
        data = rec.load(a.path)
        print(_render_frame(data, a.at, color=not a.no_color))
    elif a.cmd == "info":
        data = rec.load(a.path)
        m = data["meta"]
        print(f"kare: {len(data['turns'])} | son tur: {int(data['turns'][-1])} | "
              f"seed: {m['seed']} | varlık: {m['n_entities']} | "
              f"grid: {m['grid_size']} | final hash: {m['final_state_hash']}")


if __name__ == "__main__":
    main()
