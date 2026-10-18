"""S3-C: asimetrik olay fiziği (world/events.py, PL-05 açıldı).

Ali kararı (A) gereği görev uzamsal olmaktan çıkarıldı: olay KÜRESEL,
tek belirsizlik hangi EYLEMİN güvenli olduğu (kutup). Buradaki testler
fiziği ve — projenin değişmez kuralı — KAPALIYKEN BİT-EŞ KORUNUMU
sabitler.
"""

import dataclasses

import numpy as np

from world.config import WorldConfig
from world.events import EventSystem
from world.grid import INTERACT, RIGHT, STAY, World


def _cfg(**kw):
    return dataclasses.replace(WorldConfig(), **kw)


def test_disabled_by_default_is_bit_identical():
    """Varsayılan KAPALI: durum, hash ve dinamik S0'la bit-eş
    (K-109/K-110/K-113 geleneği)."""
    assert WorldConfig().event_every == 0
    w1 = World(WorldConfig(), n_entities=3, seed=7)
    w2 = World(WorldConfig(), n_entities=3, seed=7)
    for _ in range(200):
        w1.step(np.array([STAY, RIGHT, INTERACT]))
        w2.step(np.array([STAY, RIGHT, INTERACT]))
    assert w1.state_hash() == w2.state_hash()
    assert "events" not in w1.state_dict(), \
        "olaylar kapalıyken state_dict'e sızmamalı (eski hash'ler bozulur)"


def test_event_drains_only_unsafe_actors_and_is_global():
    """Olay küreseldir: ceza KONUMA bakmaz, yalnız EYLEME bakar.
    (Uzamsal olmayan koordinasyon görevinin tanımı budur.)"""
    cfg = _cfg(event_every=10, event_lead=2, event_duration=1,
               event_penalty=25.0, hazard_spawn_every=10**9,
               resource_a_count=0, resource_b_count=0)
    w = World(cfg, n_entities=2, seed=3)
    w.entity_pos[0] = (0, 0)
    w.entity_pos[1] = (32, 32)          # taban tabana zıt köşeler
    while not w.events.active(w.turn + 1):
        w.step(np.array([STAY, STAY]))
        assert w.turn < 100, "olay hiç aktifleşmedi"
    safe = w.events.safe_action()
    unsafe = (safe + 1) % 6
    d = w.step(np.array([safe, unsafe]))
    assert d[0] == 0.0, f"güvenli eylem cezalandırıldı: {d[0]}"
    assert d[1] == -cfg.event_penalty, f"güvensiz eylem: {d[1]}"


def test_cue_split_leaves_information_incomplete_alone():
    """event_visibility_split'in ÖZÜ: tek ajanın ipucu kutbu
    belirlemeye YETMEZ (K=4 → 2 aday kalır), ama iki farklı bit
    birlikte kutbu TEK'e indirir. Kanalın gerekliliği buradan gelir."""
    cfg = _cfg(event_every=6, event_lead=2, event_duration=1,
               event_polarities=4, hazard_spawn_every=10**9)
    w = World(cfg, n_entities=6, seed=17)
    while w.events.polarity < 0:
        w.step(np.zeros(6, dtype=int))
        assert w.turn < 50
    for i in range(6):
        cands = w.events.candidates(i)
        assert len(cands) == 2, f"ajan {i}: tek ipucu 2 aday bırakmalı"
        assert w.events.polarity in cands

    bits = {w.events.cue_for(i)[0] for i in range(6)}
    assert bits == {0, 1}, "ipucu dağılımı iki biti de kapsamalı"
    # İki farklı biti gözleyen iki ajanın kesişimi TEK kutup.
    i0 = next(i for i in range(6) if w.events.cue_for(i)[0] == 0)
    i1 = next(i for i in range(6) if w.events.cue_for(i)[0] == 1)
    joint = set(w.events.candidates(i0)) & set(w.events.candidates(i1))
    assert joint == {w.events.polarity}, \
        "iki bit birleşince kutup tek kalmalı — yoksa iletişim işe yaramaz"


def test_event_duration_one_blocks_learning_from_pain():
    """Tasarım kilidi 1: olay tek tur sürer → 'cezayı ye, sonra düzelt'
    stratejisi imkânsız. Uzun olayda deneyim iletişimin yerini alırdı."""
    assert WorldConfig().event_duration == 1
    cfg = _cfg(event_every=9, event_lead=2, event_duration=1,
               hazard_spawn_every=10**9)
    w = World(cfg, n_entities=1, seed=4)
    active_runs = []
    run = 0
    for _ in range(90):
        w.step(np.array([STAY]))
        if w.events.active(w.turn):
            run += 1
        elif run:
            active_runs.append(run)
            run = 0
    assert active_runs and set(active_runs) == {1}, \
        f"olay birden fazla tur aktif kaldı: {active_runs}"


def test_precursor_appears_before_event_and_clears_after():
    cfg = _cfg(event_every=20, event_lead=5, event_duration=2,
               hazard_spawn_every=10**9)
    w = World(cfg, n_entities=1, seed=11)
    seen_pending = False
    for _ in range(60):
        w.step(np.array([STAY]))
        if w.events.pending(w.turn):
            seen_pending = True
            assert w.events.precursor.shape == (1, 2)
            assert w.events.polarity >= 0
            assert not w.events.active(w.turn)
    assert seen_pending, "uyarı penceresi hiç gözlenmedi"


def test_polarity_is_unpredictable_but_deterministic():
    """Kutup dünya rng'sinden çekilir: aynı seed → aynı dizi (anayasa),
    ama dizi sabit değil (deneyimden öğrenilemez olması şart)."""
    def polarities(seed):
        cfg = _cfg(event_every=12, event_lead=2, event_duration=2,
                   hazard_spawn_every=10**9)
        w = World(cfg, n_entities=1, seed=seed)
        out, last = [], None
        for _ in range(400):
            w.step(np.array([STAY]))
            if w.events.polarity >= 0 and w.events.polarity != last:
                out.append(w.events.polarity)
            last = w.events.polarity if w.events.polarity >= 0 else None
        return out

    a, b = polarities(5), polarities(5)
    assert a == b and len(a) >= 8, "aynı seed bit-eş olmalı"
    assert len(set(a)) >= 3, f"kutup çeşitlenmiyor — öğrenilebilir olurdu: {a}"


def test_percept_encodes_cue_losslessly_in_hazard_channel():
    """PL-27(c): öncü YENİ KANAL AÇMADAN tehlike kanalına yazılır.
    Enstrüman denetimi: gözlemden çözülen ipucu, olayın gerçek
    ipucuyla BİREBİR aynı olmalı — kodlama kayıpsızsa ajan için
    öğrenilebilir bir sinyal vardır; değilse tuzak baştan bozuktur."""
    cfg = _cfg(event_every=15, event_lead=6, event_duration=1,
               event_polarities=4, hazard_spawn_every=10**9,
               resource_a_count=0, resource_b_count=0)
    w = World(cfg, n_entities=5, seed=29)
    r = 4
    checked = 0
    for _ in range(120):
        w.step(np.zeros(5, dtype=int))
        if not w.events.pending(w.turn):
            continue
        for i in range(5):
            obs = w.observe(i, r)
            lit = [(int(y) - r, int(x) - r)
                   for y, x in np.argwhere(obs[2] > 0.5)]
            assert w.events.decode_percept(lit) == w.events.cue_for(i), \
                f"ajan {i}: algı ipucuyla eşleşmiyor"
            checked += 1
    assert checked > 20, f"yeterli uyarı penceresi gözlenmedi ({checked})"


def test_percept_absent_outside_warning_window():
    """Öncü yalnız uyarı penceresinde yanar: olay aktifken ve olay
    yokken tehlike kanalı temiz kalmalı (gerçek tehlike kapalı)."""
    cfg = _cfg(event_every=12, event_lead=4, event_duration=1,
               hazard_spawn_every=10**9, resource_a_count=0,
               resource_b_count=0)
    w = World(cfg, n_entities=2, seed=31)
    saw_lit = saw_clean = False
    for _ in range(60):
        w.step(np.zeros(2, dtype=int))
        lit = w.observe(0, 4)[2].sum() > 0
        if w.events.pending(w.turn):
            assert lit, "uyarı penceresinde öncü yanmalı"
            saw_lit = True
        else:
            assert not lit, "pencere dışında tehlike kanalı temiz olmalı"
            saw_clean = True
    assert saw_lit and saw_clean


def test_percept_is_private_to_each_agent():
    """Algı ajan-merkezli ve ÖZEL: aynı hücrede duran iki ajan farklı
    bit gözleyebilir (event_visibility_split'in özü)."""
    cfg = _cfg(event_every=7, event_lead=4, event_duration=1,
               event_polarities=4, hazard_spawn_every=10**9,
               resource_a_count=0, resource_b_count=0)
    w = World(cfg, n_entities=8, seed=13)
    found_diff = False
    for _ in range(80):
        w.step(np.zeros(8, dtype=int))
        if not w.events.pending(w.turn):
            continue
        w.entity_pos[:] = w.entity_pos[0]         # hepsi AYNI hücrede
        cues = [w.events.cue_for(i) for i in range(8)]
        percepts = [w.events.decode_percept(
            [(int(y) - 4, int(x) - 4)
             for y, x in np.argwhere(w.observe(i, 4)[2] > 0.5)])
            for i in range(8)]
        assert percepts == cues
        if len({c[0] for c in cues}) > 1:
            found_diff = True
    assert found_diff, "aynı konumda farklı bit gözlenmedi — algı özel değil"


def test_event_state_survives_snapshot_roundtrip():
    """Olay durumu dünyanın parçası: kaydet/yükle bit-eş sürmeli."""
    cfg = _cfg(event_every=9, event_lead=3, event_duration=3)
    w = World(cfg, n_entities=2, seed=21)
    for _ in range(15):
        w.step(np.array([STAY, RIGHT]))
    snap = w.state_dict()
    assert "events" in snap
    w2 = World(cfg, n_entities=2, seed=999)
    w2.load_state(snap)
    assert w2.state_hash() == w.state_hash()
    for _ in range(30):
        w.step(np.array([RIGHT, STAY]))
        w2.step(np.array([RIGHT, STAY]))
    assert w.state_hash() == w2.state_hash()


def test_event_system_off_is_inert():
    ev = EventSystem(WorldConfig())
    assert not ev.enabled
    d = np.zeros(2)
    ev.schedule(0, np.random.default_rng(0), lambda n: np.zeros((n, 2), int))
    ev.apply_drain(0, np.array([STAY, RIGHT]), d)
    assert not d.any() and ev.polarity == -1


def test_event_share_default_bit_identical_and_math():
    """S3-N: event_share=0 eski muhasebeyle bit-eş; s=0.5'te kayıp
    (1-s)*ıska_i + s*ortalama_ıska."""
    import dataclasses

    import numpy as np

    from world.config import WorldConfig
    from world.events import EventSystem
    base = dataclasses.replace(WorldConfig(), event_every=30, event_lead=2,
                               event_penalty=20.0)
    for share, expected in ((0.0, [0.0, -20.0, -20.0, -20.0]),
                            (0.5, [-7.5, -17.5, -17.5, -17.5])):
        cfg = dataclasses.replace(base, event_share=share)
        ev = EventSystem(cfg, 4)
        ev.polarity, ev.starts_at, ev.ends_at = 2, 5, 6
        d = np.zeros(4)
        ev.apply_drain(5, np.array([2, 0, 1, 3]), d)   # 1 isabet, 3 ıska
        assert np.allclose(d, expected), (share, d)
    # paylaşım hash'e girmez (deltas dışı) — state_dict değişmez
    assert "event_share" not in EventSystem(base, 1).state_dict()
