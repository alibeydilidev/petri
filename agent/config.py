from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    obs_radius: int            # heterojen — ajana göre 3..6
    memory_dim: int            # heterojen — GRU hidden, 64..256
    learning_rate: float       # heterojen — 1e-4 .. 1e-3
    channel_bits: int = 4      # SABİT: kıtlık anayasal (S1'de kanal KAPALI)
    signal_energy_cost: float = 0.5
    move_energy_cost: float = 1.0
    interact_energy_cost: float = 1.0   # PL-07: dokümanda tanımsız, hareketle eş
    base_metabolism: float = 0.3
    max_energy: float = 100.0
    # --- S1 MPC eylem seçici (KERNEL_BUDGET K-103/K-105) ---
    mpc_horizon: int = 5        # rollout derinliği
    mpc_candidates: int = 32    # aday eylem dizisi sayısı
    mpc_epsilon: float = 0.1    # K-108: ε-greedy keşif (veri yanlılığı kırıcı)
    # K-109 (S2.5 adım 4): aday örnekleme iyileştirmesi. Varsayılanlar eski
    # davranışı bit-eş korur (iters=1 + sabit adaylar kapalı = tek atış).
    mpc_cem_iters: int = 1          # elit-iyileştirme turu sayısı
    mpc_elites: int = 8             # elit sayısı (iyileştirme açıkken)
    mpc_constant_candidates: bool = False  # 6 sabit-eylem dizisini adaylara kat
    # K-111 (S2.8): yön×süre makro önekleri aday havuzunda garantili.
    # K-112 (S2.8): skorlama ufku kırpma (H_eff; None = kırpma yok).
    # Varsayılanlar eski davranışı bit-eş korur (K-109 geleneği).
    mpc_macro_candidates: bool = False
    mpc_score_horizon: int | None = None
    # K-110 (S2.6 iş 2): öncelikli deneyim tekrarı. Varsayılan KAPALI
    # (eski davranış bit-eş). PL-12'ye cevap: az yapılan eylemlerin
    # karşı-olgusal kalibrasyonunu tampon + tabakalama ile sürdür.
    per_enabled: bool = False
    per_buffer_size: int = 2000     # pencere (W'lik dizi) kapasitesi
    per_alpha: float = 0.6          # öncelik üssü (kayıp^alpha örnekleme)
    per_batch: int = 4              # tur başına tekrar-batch boyu
    per_stratify_prob: float = 0.3  # eylem-tabakalı örnekleme olasılığı
    # K-110rev (S2.9): uzamsal PER — grid-değişim büyüklüğü örnekleme
    # ağırlığına çarpan olarak girer (0 = kapalı, bit-eş). ε hareket
    # yanlılığı: ε ateşlendiğinde bu olasılıkla yalnız 4 hareket
    # eyleminden örnekle (0 = kapalı, bit-eş; eski tek-çekiliş korunur).
    per_spatial_weight: float = 0.0
    eps_move_bias: float = 0.0
    # PL-15 kontrol bayrağı: False → enerji gözlemden VE tahmin hedefinden
    # silinir (enerji-körü eş-eğitimli kontrol ajanı). Ana ajanda hep True.
    interoception: bool = True
    # S3 (spec 4.2): kanal. Açıkken gözleme 16-boyut alınan-sinyal
    # vektörü, çekirdek girdisine 17-boyut kendi-sinyal efferensi
    # eklenir (K-114). Varsayılan KAPALI (S0-S2.10 bit-eş).
    channel_open: bool = False
    # K-113 (S2.10, PL-18 kararı): "conv" → eylem-KOŞULSUZ evrişimli
    # decoder (yalnız yerellik + ağırlık paylaşımı; eylem bilgisi
    # decoder'a girmez, eskisi gibi hidden üzerinden akar). M-19 doğum
    # günü testi kapısından geçmek zorunda. Varsayılan "dense" bit-eş.
    decoder_type: str = "dense"
    # S3-D / PL-22 (b): YUVA DÖNEMİ. Yaş < nest_turns iken metabolizma +
    # eylem + sinyal maliyeti nest_factor ile çarpılır. Ajana bit gitmez
    # (gözlem/loss/mimari değişmez; ekonomi parametresi — M-09 kaydı
    # KERNEL_BUDGET S3-D notu). Varsayılan T=0 / f=1 bit-eş.
    nest_turns: int = 0
    nest_factor: float = 1.0
    # --- S1 öğrenme ---
    tbptt_window: int = 8       # truncated BPTT pencere uzunluğu
    energy_loss_weight: float = 10.0  # K-106: enerji boyutunun loss ağırlığı


# Roster'dan A2 / "Dengeli" profil (population/ S3'te; burada sadece değerler).
def a2_config(**overrides) -> AgentConfig:
    base = dict(obs_radius=4, memory_dim=128, learning_rate=5e-4)
    base.update(overrides)
    return AgentConfig(**base)
