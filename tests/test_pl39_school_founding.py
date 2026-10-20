"""PL-39: okul ağırlıklarından kuruluş (school:<pt>,<pt>)."""
import pathlib
import torch
from training.ecology import founding_population

RS = pathlib.Path(__file__).resolve().parent.parent / "runs" / "rs"


def test_school_founding_loads_alternating_weights():
    a, b = RS / "rs1_s0" / "final_weights.pt", RS / "rs1_s1" / "final_weights.pt"
    if not (a.exists() and b.exists()):
        import pytest
        pytest.skip("RS ağırlıkları yok")
    cits = founding_population(founding=f"school:{a},{b}", nest=(600, 0.5),
                               channel="open")
    assert len(cits) == 5
    sa = torch.load(a, weights_only=False)["A2"]["state_dict"]
    sb = torch.load(b, weights_only=False)["A2"]["state_dict"]
    for i, c in enumerate(cits):
        ref = sa if i % 2 == 0 else sb
        sd = c.agent.core.state_dict()
        assert all(torch.equal(sd[k], ref[k]) for k in ref)
        assert c.agent.cfg.nest_turns == 600
