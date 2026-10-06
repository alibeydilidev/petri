import dataclasses
import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class WorldConfig:
    grid_size: int = 64
    toroidal: bool = True
    resource_a_count: int = 12          # tek-ajan kaynağı
    # M-10 / PL-14: ekonomi v2 (2026-07-08, Ali kararı). v1'de 15.0 idi;
    # oracle fizibilitesi hasadın v1'de HER koşulda net zarar olduğunu
    # gösterdi (runs/s26_a_energy_sweep.json). Eski bulgular v1 damgalı.
    resource_a_energy: float = 45.0
    resource_a_drift_every: int = 200   # tur; kaynak yer değiştirme periyodu
    resource_b_count: int = 3           # koordinasyon kaynağı
    # M-10 / S3 kalibrasyonu (economy v3): v1'de 75 (=5xA15); v2'de A=45
    # olunca 75 bozuldu (kişi başı 37.5 < A). Oracle süpürmesi
    # (runs/s3_b_oracle.json): sürdürülebilirlik eşiği 135; anayasal
    # 4-6x bandı korunarak 180 (=4xA) seçildi.
    resource_b_energy: float = 180.0
    resource_b_min_agents: int = 2      # eşzamanlı ajan şartı
    resource_b_sync_window: int = 2     # eşzamanlılık toleransı (tur)
    hazard_spawn_every: int = 500
    hazard_drain_per_turn: float = 5.0
    hazard_radius: int = 2              # PL-01: Chebyshev yarıçap (5x5 bölge)
    hazard_duration: int = 250          # PL-01: tehlike ömrü (tur)
    event_visibility_split: bool = True # her ajana olayın farklı parçası
    seed: int = 42                      # tam tekrarlanabilirlik
    economy_version: int = 3            # M-10: değer sistemi sürümü
    # PL-28 (Ali kararı 2026-07-27): KÜRESEL. 64-toruste azami Chebyshev
    # mesafe 32'dir → 32 = herkes duyar. S3-C kalibrasyonu çıtanın yalnız
    # burada aşıldığını gösterdi (menzil 24 → yeterlilik 0.468 < 0.50).
    # Sonucu: sembolün taşıyabildiği TEK şey KİMLİĞİ (16'dan hangisi);
    # uzam, yön, mesafe, gönderen hepsi düşer — dil tuzağının en temiz
    # hâli. PL-21'in "yakın ajanlar duyar" gerekçesi geri alındı.
    signal_range: int = 32              # S3-C: küresel yayın (PL-28)
    # --- S3-C: asimetrik olay (world/events.py; PL-05 açıldı, PL-27) ---
    # Ali kararı (A): koordinasyonun zor kısmı UZAMSAL olmasın — yönsüz
    # 4 bit "nerede" taşıyamaz, "ne/ne zaman" taşıyabilir (FINDINGS S3-B).
    # Varsayılan 0 = KAPALI → state_dict/state_hash bit-eş korunur.
    event_every: int = 0                # 0=kapalı; >0: zamanlama periyodu
    event_lead: int = 8                 # öncü ile olay arası (uyarı penceresi)
    # SÜRE 1: olay, "acıyı çek ve düzelt" stratejisine vakit BIRAKMAMALI.
    # Uzun olayda deneyim iletişimin yerine geçer ve tuzak boşa düşer
    # (tasarım sırasında ölçüldü: 3 turluk olayda kendi-çıkarım değerin
    # ~%67'sini kurtarıyordu). Bkz. world/events.py "iki tasarım kilidi".
    event_duration: int = 1             # olayın süresi (tur)
    event_penalty: float = 25.0         # güvensiz eylemin tur başı bedeli
    # Kutup sayısı = güvenli eylem alternatifleri. log2(K) bit → her ajan
    # olay başına YALNIZ 1 bit gözler (event_visibility_split) → bilgi
    # tek ajanda tamamlanmaz, kanal gereklidir.
    event_polarities: int = 4


def config_hash(cfg) -> str:
    """Config damgası (M-10): bulgular hangi dünyada doğduğunu taşır."""
    blob = json.dumps(dataclasses.asdict(cfg), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


# v1 ekonomisi (S0–S2.6 iş-1 arası tüm koşumlar): eski kayıtların
# replay'i için açık tanım — varsayılanlara güvenme (M-10).
def economy_v1() -> WorldConfig:
    return dataclasses.replace(WorldConfig(), resource_a_energy=15.0,
                               resource_b_energy=75.0, economy_version=1)


# v2 ekonomisi (S2.6 stage-2 – S2.10 arası): A=45, B hâlâ 75 (bozuk prim).
def economy_v2() -> WorldConfig:
    return dataclasses.replace(WorldConfig(), resource_b_energy=75.0,
                               economy_version=2)
