"""S3-D: yuva dönemi muhasebesi + nüfus oracle'ı duman/determinizm."""

import pathlib

import numpy as np
import pytest

from agent.config import a2_config
from agent.homeostasis import Homeostasis
from world.grid import STAY, UP


def test_nest_defaults_bit_identical():
    """T=0/f=1 varsayılanı eski muhasebeyle bit-eş (K-109 geleneği)."""
    cfg = a2_config(base_metabolism=0.6)
    h = Homeostasis(cfg)
    e = 100.0
    for a, d in [(UP, 0.0), (STAY, 45.0), (UP, -5.0), (UP, 0.0)]:
        h.apply_turn(a, d)
        e = min(e + d - (0.6 + (1.0 if a == UP else 0.0)), 100.0)
        assert h.energy == e
    assert not h.in_nest and h.age == 4


def test_nest_discount_applies_only_to_own_costs_then_expires():
    cfg = a2_config(base_metabolism=0.6, nest_turns=2, nest_factor=0.25)
    h = Homeostasis(cfg)
    h.apply_turn(UP, 0.0, signal_cost=0.5)     # yuva: (0.6+1+0.5)*0.25
    assert abs(h.energy - (100 - 2.1 * 0.25)) < 1e-9
    h.apply_turn(UP, -5.0)                     # dünya deltası indirimsiz
    assert abs(h.energy - (100 - 2.1 * 0.25 - 5.0 - 1.6 * 0.25)) < 1e-9
    assert not h.in_nest
    h.apply_turn(UP, 0.0)                      # yuva bitti: tam maliyet
    assert abs(h.energy - (100 - 2.1 * 0.25 - 5.0 - 1.6 * 0.25 - 1.6)) < 1e-9


def test_nest_analytic_bound_for_mover():
    """Ön-kayıt analitik sınırı: her tur hareket eden, hasatsız ajan
    yuvada 100/(f*1.6) tur yaşar (f=0.25 → 250)."""
    cfg = a2_config(base_metabolism=0.6, nest_turns=10_000, nest_factor=0.25)
    h = Homeostasis(cfg)
    t = 0
    while h.alive:
        h.apply_turn(UP, 0.0)
        t += 1
    assert t == 250


def test_pop_oracle_scripted_and_random_smoke_deterministic():
    from training.pop_oracle import run_arm
    a = run_arm("oracle5", seed=9100, max_turns=80)
    b = run_arm("oracle5", seed=9100, max_turns=80)
    a.pop("seconds"); b.pop("seconds")
    assert a == b, "oracle kolu bit-eş değil"
    assert a["agent_turns"] == 5 * 80 or sum(a["censored"]) < 5
    r = run_arm("random5", seed=9100, nest=(600, 0.1), max_turns=80)
    assert all(r["censored"])            # yuvada 80 turda kimse ölmez


@pytest.mark.skipif(not pathlib.Path("runs/s210_weights/seed3.pt").exists(),
                    reason="seed3.pt yok")
def test_pop_oracle_clone_arms_smoke_deterministic():
    from training.pop_oracle import run_arm
    for arm in ("clone1_mute", "clone5_open", "clone5_learn"):
        a = run_arm(arm, seed=9100, max_turns=12)
        b = run_arm(arm, seed=9100, max_turns=12)
        a.pop("seconds"); b.pop("seconds")
        assert a == b, f"{arm} bit-eş değil"
    # mute kolu hiç sinyal göndermez; open kolu ε dalında gönderebilir
    m = run_arm("clone5_mute", seed=9100, max_turns=12)
    assert sum(m["signals"]) == 0
