"""Organ 3 — Kanal (S3'te AÇILDI; spec 4.2 yürürlükte).

Tur başına en çok 4 bit = 16 sembol (+ "sinyal yok"). Göndermek enerji
yakar (AgentConfig.signal_energy_cost, homeostaz uygular). Yayın
menzilli (WorldConfig.signal_range, Chebyshev; PL-21). Semboller
anlamsız doğar — bu modül anlam TAŞIMAZ: yalnız kodlama yardımcıları.

Alınan sinyaller gözleme 16-boyutlu toplam-one-hot olarak eklenir
(kim gönderdi bilgisi VERİLMEZ — gönderen kimliği opaklığın parçası;
K-114). Kendi gönderdiği sembol, eylem efferensi gibi çekirdek girdisine
one-hot(17) eklenir (K-114; K-102a simetrisi).
"""

import numpy as np

N_SYMBOLS = 16
NO_SIGNAL = -1


def received_vector(heard: list[tuple[int, int]]) -> np.ndarray:
    """[(gönderen, sembol)] → (16,) float32; aynı sembol üst üste
    binerse doygunluk 1 (kaç kişinin söylediği verilmez)."""
    v = np.zeros(N_SYMBOLS, dtype=np.float32)
    for _, sym in heard:
        v[sym] = 1.0
    return v


def own_signal_onehot(sym: int) -> np.ndarray:
    """Gönderilen sembolün efferens kopyası: (17,) — indeks 0 'yok'."""
    v = np.zeros(N_SYMBOLS + 1, dtype=np.float32)
    v[0 if sym == NO_SIGNAL else sym + 1] = 1.0
    return v
