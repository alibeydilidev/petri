"""S3 açılış testleri: sinyal fiziği, kanal kodlaması, transplant, ekoloji."""

import pathlib

import numpy as np
import pytest
import torch

from agent.channel import NO_SIGNAL, own_signal_onehot, received_vector
from agent.config import a2_config
from training.loop import OnlineAgent, encode_obs
from world.config import WorldConfig
from world.grid import World


def test_world_signal_delivery_range_and_self_exclusion():
    world = World(WorldConfig(), n_entities=3, seed=5)
    world.entity_pos[0] = (10, 10)
    world.entity_pos[1] = (10, 14)   # Chebyshev 4 → menzil 8 içinde
    world.entity_pos[2] = (40, 40)   # uzak
    world.step(np.zeros(3, dtype=int), signals=np.array([7, 3, -1]))
    h0 = world.heard(0, 8)
    assert h0 == [(1, 3)], h0        # kendi 7'sini duymaz, uzak 2'yi duymaz
    assert world.heard(2, 8) == []
    v = received_vector(h0)
    assert v[3] == 1.0 and v.sum() == 1.0
    assert own_signal_onehot(NO_SIGNAL)[0] == 1.0
    assert own_signal_onehot(5)[6] == 1.0


def test_signals_not_in_state_hash():
    w1 = World(WorldConfig(), n_entities=2, seed=5)
    w2 = World(WorldConfig(), n_entities=2, seed=5)
    w1.step(np.zeros(2, dtype=int), signals=np.array([7, 3]))
    w2.step(np.zeros(2, dtype=int))
    assert w1.state_hash() == w2.state_hash(), \
        "sinyaller dünya durumunu değiştirmemeli (geçici enformasyon)"


def test_channel_open_dims_and_budget():
    from agent.predictive_core import PredictiveCore, act_dim, obs_dim
    for r, m in [(6, 64), (3, 256), (4, 128), (5, 96), (3, 192)]:
        cfg = a2_config(obs_radius=r, memory_dim=m, channel_open=True,
                        decoder_type="conv")
        core = PredictiveCore(cfg)
        assert core.n_params() < 500_000, f"({r},{m}): {core.n_params()}"
        assert obs_dim(cfg) == 4 * (2*r+1)**2 + 16 + 1
        assert act_dim(cfg) == 6 + 17
    v = encode_obs(np.zeros((4, 9, 9), dtype=np.float32), 50.0,
                   a2_config(channel_open=True),
                   signals_vec=received_vector([(1, 3)]))
    assert v.shape[0] == 4*81 + 16 + 1
    assert v[-1] == 0.5 and v[4*81 + 3] == 1.0  # enerji son, sinyal yerinde


@pytest.mark.skipif(not pathlib.Path("runs/s210_weights/seed3.pt").exists(),
                    reason="seed3.pt yok")
def test_transplant_neutral_extension_equivalence():
    # Sinyalsiz girdide transplant, eski modele SAYISAL ÖZDEŞ olmalı
    # (yeni sütun/satırlar sıfır-başlatma; mutasyon uygulanmadan).
    from population.lifecycle import transplant_seed3
    from training.eval_s28 import load_agent
    from training.eval_s210 import S210_OVERRIDES
    old = load_agent("runs/s210_weights/seed3.pt")
    cfg_new = a2_config(**{**S210_OVERRIDES, "channel_open": True})
    new = transplant_seed3("runs/s210_weights/seed3.pt", cfg_new,
                           torch_seed=1, np_seed=2)
    grid = np.random.default_rng(0).random((4, 9, 9)).astype(np.float32)
    obs_old = encode_obs(grid, 50.0, old.cfg)
    obs_new = encode_obs(grid, 50.0, cfg_new)          # sinyal=0
    act_old = torch.zeros(6); act_old[2] = 1.0
    act_new = torch.cat([act_old,
                         torch.from_numpy(own_signal_onehot(NO_SIGNAL))])
    with torch.no_grad():
        p_old, _ = old.core(obs_old.view(1,1,-1), act_old.view(1,1,-1))
        p_new, _ = new.core(obs_new.view(1,1,-1), act_new.view(1,1,-1))
    # grid bölümü + enerji özdeş (yeni model ayrıca 16 sinyal tahmini üretir)
    assert torch.allclose(p_old[..., :324], p_new[..., :324], atol=1e-5)
    assert torch.allclose(p_old[..., -1], p_new[..., -1], atol=1e-5)


def test_diagnostic_counter_outside_state_hash():
    """b_openings_total teşhis sayacıdır: dinamiğe ve state_hash'e
    girmemeli (last_signals emsali)."""
    w = World(WorldConfig(), n_entities=2, seed=5)
    before = w.state_hash()
    w.b_openings_total += 7
    assert w.state_hash() == before


def test_respawn_uses_world_rng():
    """Anayasa: dünyadaki TÜM rastgelelik World'ün tek generator'ından.
    Halef doğum yeri (a) aynı seed'de tekrarlanabilir olmalı, (b) dünya
    rng'sini İLERLETMELİ — dışarıdan çekilseydi ikisi de sağlanmazdı."""
    w1, w2 = (World(WorldConfig(), n_entities=3, seed=9) for _ in range(2))
    before = w1.state_hash()
    w1.respawn_entity(1)
    w2.respawn_entity(1)
    assert w1.state_hash() == w2.state_hash()          # (a) deterministik
    assert w1.state_hash() != before                   # (b) rng ilerledi
    assert (w1.entity_pos[1] == w2.entity_pos[1]).all()


@pytest.mark.skipif(not pathlib.Path("runs/s210_weights/seed3.pt").exists(),
                    reason="seed3.pt yok")
def test_vitals_counters_are_cumulative(tmp_path):
    """M-23 — SAYAÇ DA BİR CİHAZDIR (bilinen-pozitif doğrulaması).

    S3 ilk nefes koşumunda vitals sayaçları ölümde resetlenen Citizen
    nesnesinde yaşıyordu; rapor edilen 'A-hasat' ve 'sinyal oranı'
    ZAMANLA DÜŞÜYORDU ve bu 'sinyaller söndü' diye okundu. Kümülatif bir
    sayaç tanım gereği azalamaz — kural burada sabitlenir.

    Bilinen-pozitif şartı: cihaz kusurun gerçekleştiği rejimde (ölümlü,
    sayaç taşıyan sakinler ölürken) sınanır; ölümsüz koşumda test boştur.
    """
    import json

    from training.ecology import run_ecology
    run_ecology(120, str(tmp_path / "c"), world_seed=3001, log_every=20)
    j = json.load(open(tmp_path / "c" / "breath.json"))
    v = j["vitals"]

    # (1) BİLİNEN-POZİTİF: ölüm gerçekleşmiş VE ölen sakinler sayaç taşımış.
    assert j["deaths"] > 0, "ölümsüz koşum — test boş, rejim kusuru göstermez"
    living = sum(sum(h) for h in j["final_symbol_hist"].values())
    cumulative = sum(j["symbol_hist_cumulative"])
    assert cumulative > living, (
        "ölen sakinler sayaç taşımamış — bilinen-pozitif kurulamadı "
        f"(kümülatif {cumulative} == yaşayan {living})")

    # (2) ASIL KURAL: kümülatif alanlar asla azalmaz.
    for key in ("deaths", "agent_turns", "a_harvests", "b_shares",
                "b_openings", "signals_sent"):
        seq = [r[key] for r in v]
        assert all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1)), \
            f"kümülatif sayaç '{key}' azaldı: {seq}"

    # (3) Payda ajan-turu; her tur 5 sakin yaşar (ölen anında ikame edilir).
    assert v[-1]["agent_turns"] == 5 * v[-1]["turn"]

    # (4) Sinyal oranı ε-tabanının altına DÜŞEMEZ: ε=0.1 dalında sembol
    #     u{-1..15}'ten çekilir → P(sinyal) = 16/17. Eski cihaz 0.0
    #     raporlamıştı; bu alt sınır o hatayı yakalar.
    eps_floor = 0.1 * 16 / 17
    assert v[-1]["signal_rate"] > 0.5 * eps_floor, (
        f"sinyal oranı {v[-1]['signal_rate']} ε-tabanının ({eps_floor:.3f}) "
        "yarısının altında — cihaz yine payı eksik sayıyor")


@pytest.mark.skipif(not pathlib.Path("runs/s210_weights/seed3.pt").exists(),
                    reason="seed3.pt yok")
def test_ecology_smoke_and_determinism(tmp_path):
    from training.ecology import run_ecology
    import json
    run_ecology(60, str(tmp_path / "a"), world_seed=42, log_every=30)
    run_ecology(60, str(tmp_path / "b"), world_seed=42, log_every=30)
    ja = json.load(open(tmp_path / "a" / "breath.json"))
    jb = json.load(open(tmp_path / "b" / "breath.json"))
    ja.pop("world_config_hash"); jb.pop("world_config_hash")
    for j in (ja, jb):
        for v in j["vitals"]:
            v.pop("ms_per_turn")
    assert ja == jb, "ekoloji bit-eş değil"
