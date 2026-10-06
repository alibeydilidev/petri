# PETRI — Emergent Zihin Öncülleri Deneyi
### (PROMETHEUS v2 çalışma adı — Petri kabı metaforundan)

> **Tek cümlelik tanım:** Bilinç üretmeye çalışmıyoruz. Bilincin öncüllerinin
> (öz-model, yüksek mertebe modelleme, birleşimsel iletişim) hangi ekolojik
> basınç altında **kendiliğinden** belirdiğini yakalayan bir tuzak kuruyoruz.

---

## 0. ÖZET (önce özet, sonra detay)

- **Ne inşa ediyoruz:** Kıt kaynaklı, deterministik fizikli bir grid dünyada
  yaşayan 5–7 heterojen ajan. Her ajan sadece üç şeyden ibaret: tahmin
  makinesi + homeostaz (ölümlülük) + kısıtlı sinyal kanalı.
- **Ne VERMİYORUZ:** Dil, gramer, duygu uzayı, katmanlı bilinç mimarisi,
  ödül şekillendirme. Çekirdek utanç verici derecede küçük olacak ve bit
  cinsinden ölçülecek.
- **Neyi ölçüyoruz:** Davranışı değil, iç temsilleri. Üç prob: öz-model (P1),
  modellenmeyi modelleme (P2), içselleştirilmiş sinyal (P3). Artı sinyal
  protokolünde birleşimsellik metrikleri.
- **Başarı tanımı:** Pozitif VEYA negatif sonucun dürüst raporu. "Çıkmadı ve
  işte neden çıkmadı" da başarıdır. Hype yasak.

---

## 1. HİPOTEZLER

| ID | Hipotez | Test aracı | Beklenti |
|----|---------|-----------|----------|
| H1 | Ölümlü + eyleyen her tahmin makinesi, iç temsillerinde öz-model geliştirir | P1 lineer prob | Yüksek (çıkması beklenir) |
| H2 | Opaklık + koordinasyon zorunluluğu altında ajanlar birbirinin kendi hakkındaki modelini modellemeye başlar | P2 prob | Orta (uzun eğitim, zayıf sinyal) |
| H3 | Kısıtlı kanal, sinyal üretimini içselleştirmeye zorlar (Vygotsky iç konuşması) | P3 dedektör | Düşük (muhtemelen negatif — negatif raporu değerli) |
| H4 | Asimetrik bilgi + kanal kıtlığı, sinyal protokolünde birleşimsellik (proto-gramer) doğurur | Topografik benzerlik + zipf analizi | Orta |

**H0 (sıfır hipotezi, dürüstlük maddesi):** Tüm gözlenen davranışlar reaktif
hesaplamayla açıklanabilir. Her pozitif bulgu önce H0'a karşı savunulmak
zorundadır. PROMETHEUS v1 disclaimer geleneği devam eder.

---

## 2. ANAYASA (ihlal edilemez ilkeler)

1. **Çekirdek minimalizmi:** Ajana verilen her ön-bilgi bit cinsinden
   sayılır ve `KERNEL_BUDGET.md` dosyasında gerekçesiyle loglanır.
   Gerekçesiz hiçbir prior eklenemez. Hedef metrik:
   `çekirdek biti / final yetkinlik` oranını minimize etmek.
2. **Fizik hakemdir:** Doğruluğun tek kaynağı dünya simülasyonudur. Ajanlara
   dışarıdan ödül şekillendirme (reward shaping) YASAK. Tek içsel sinyal:
   tahmin hatası + homeostaz durumu.
3. **Dil verilmez, basınç verilir:** Sinyal kanalının anlamı, kelime dağarcığı,
   protokolü tanımlanmaz. Sadece kanal genişliği ve enerji maliyeti tanımlanır.
4. **Duygu verilmez:** 8D duygu uzayı yok. "Korku" gibi durumlar çıkacaksa
   tahmin ufku + homeostaz etkileşiminden kendiliğinden çıkmalı; problarla
   aranır, mimariye gömülmez.
5. **Davranış yalan söyler:** Başarı iddiası yalnızca iç temsil problarıyla
   desteklenirse geçerlidir. "Ajan sanki anlıyormuş gibi davrandı" cümlesi
   rapora giremez.
6. **LLM deneyin İÇİNDE yer alamaz:** LLM yalnızca gözlemci/analistdir
   (log analizi, protokol birleşimsellik incelemesi). Ajan mimarisine,
   dünyaya veya sinyal üretimine LLM giremez.
7. **Negatif sonuç sonuçtur:** Her sprint sonunda bulgular, çıkmayan şeyler
   dahil `FINDINGS.md`'ye yazılır.

---

## 3. NON-GOALS (bilinçli dışarıda bırakılanlar)

- Bilinç ürettiğini iddia etmek (felsefi iddia yok, ampirik prob var)
- Türkçe veya herhangi bir insan dili öğretmek
- Genel amaçlı yetenek / benchmark performansı
- Minecraft veya zengin 3D dünya (v1 hatası: fazla zengin, fazla affedici)
- İnsan geri bildirimi, RLHF, herhangi bir insan-döngüde mekanizma

---

## 4. MİMARİ

### 4.1 Dünya: `petri/world/`

Deterministik, ayrık zamanlı grid dünya. Petri kabı, oyun değil.

| Özellik | Spesifikasyon | Gerekçe |
|---------|--------------|---------|
| Grid | 64×64, toroidal (kenarlar sarılır) | Köşe-kaçış stratejilerini engeller |
| Fizik | Deterministik, tur bazlı | Hakem rüşvet yemez |
| Kaynak tipi A | Tek ajanla toplanabilir, azdır, **yer değiştirir** | Temel kıtlık + keşif basıncı |
| Kaynak tipi B | **Yalnızca 2+ ajanın eşzamanlı, koordineli eylemiyle** açılır, A'dan 4–6× verimli | İletişimi hayatta kalma organına çevirir |
| Tehlike bölgeleri | Periyodik beliren, enerji emen alanlar | Kaçınma öğrenimi + uyarı sinyali basıncı |
| Olay enjeksiyonu | Kaynak kayması / tehlike doğuşu; her ajana olayın **farklı parçası** görünür | Asimetrik bilgi → referans ihtiyacı |
| Gözlem | Ajan-merkezli, kısıtlı menzil (ajana göre değişir, bkz. 4.3) | Opaklık üretir |

```python
# petri/world/config.py
from dataclasses import dataclass

@dataclass(frozen=True)
class WorldConfig:
    grid_size: int = 64
    toroidal: bool = True
    resource_a_count: int = 12          # tek-ajan kaynağı
    resource_a_energy: float = 15.0
    resource_a_drift_every: int = 200   # tur; kaynak yer değiştirme periyodu
    resource_b_count: int = 3           # koordinasyon kaynağı
    resource_b_energy: float = 75.0     # ~5x verim
    resource_b_min_agents: int = 2      # eşzamanlı ajan şartı
    resource_b_sync_window: int = 2     # eşzamanlılık toleransı (tur)
    hazard_spawn_every: int = 500
    hazard_drain_per_turn: float = 5.0
    event_visibility_split: bool = True # her ajana olayın farklı parçası
    seed: int = 42                      # tam tekrarlanabilirlik
```

### 4.2 Ajan: `petri/agent/`

Üç organ. Fazlası yok. Her organ ayrı modül, ayrı test.

**Organ 1 — Tahmin çekirdeği (`predictive_core.py`):**
Küçük bir recurrent world-model. Girdi: yerel gözlem + kendi son eylemi +
alınan sinyaller. Çıktı: sonraki gözlemin tahmini. Öğrenme sinyali: tahmin
hatası (self-supervised). GRU tabanlı başla (BiLSTM değil — nedensellik oku
tek yönlü olmalı, gelecek sızıntısı yasak). Boyut küçük tutulur: hedef
< 500K parametre/ajan. Amaç kapasite gösterisi değil, basınç deneyi.

**Organ 2 — Homeostaz (`homeostasis.py`):**
Tek skaler: enerji. Her tur sabit gider + eylem maliyeti + sinyal maliyeti.
Sıfırlanırsa ajan ölür. Ölüm gerçek: o ajanın ağırlıkları o epizotta biter.
(Süreklilik sorusu → Karar Noktası DP-01, bölüm 8.)

**Organ 3 — Kanal (`channel.py`):**
Tur başına maksimum **4 bit** sinyal (16 sembol). Sinyal göndermek enerji
yakar. Yayın (broadcast) menzillidir: yalnız yakın ajanlar duyar.
Semboller anlamsız doğar — anlam, kullanım basıncından çıkmak zorunda.

```python
# petri/agent/config.py
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentConfig:
    obs_radius: int            # heterojen — ajana göre 3..6
    memory_dim: int            # heterojen — GRU hidden, 64..256
    learning_rate: float       # heterojen — 1e-4 .. 1e-3
    channel_bits: int = 4      # SABİT: kıtlık anayasal
    signal_energy_cost: float = 0.5
    move_energy_cost: float = 1.0
    base_metabolism: float = 0.3
    max_energy: float = 100.0
```

### 4.3 Nüfus heterojenliği: `petri/population/`

Monokültür = karşılıklı şeffaflık = opaklık yok = dil basıncı yok.
5 ajanlık başlangıç kadrosu:

| Ajan | obs_radius | memory_dim | lr | Karakter (analiz kolaylığı için etiket) |
|------|-----------|------------|-----|------|
| A0 | 6 | 64 | 1e-3 | Uzak görür, çabuk unutur, hızlı öğrenir |
| A1 | 3 | 256 | 1e-4 | Kör ama fil hafızalı, yavaş öğrenir |
| A2 | 4 | 128 | 5e-4 | Dengeli |
| A3 | 5 | 96 | 8e-4 | Gözcü-ağırlıklı |
| A4 | 3 | 192 | 3e-4 | Hafıza-ağırlıklı |

Etiketler ajanlara verilmez — sadece bizim analiz sözlüğümüz.

---

## 5. PROB SİSTEMİ: `petri/probes/` (deneyin asıl kendisi)

Problar eğitime **karışmaz** — dondurulmuş temsiller üzerinde, ayrı süreçte
çalışır. Prob eğitimi ajan gradyanına asla sızamaz (bilgi sızıntısı = deney
geçersiz).

### P1 — Öz-model dedektörü (`p1_self_model.py`)
Ajanın GRU hidden state'inden iki hedefi ayrıştıran lineer problar:
(a) dünyanın sonraki durumu, (b) **ajanın kendi** sonraki iç durumu
(enerji, konum). Kontrol: aynı prob, rastgele-ağırlıklı ikiz ajanda.
**Pozitif bulgu şartı:** (b) doğruluğu, kontrol grubundan istatistiksel
olarak anlamlı yüksek + zaman içinde artan trend.

### P2 — Yüksek mertebe tuzağı (`p2_higher_order.py`)
Ajan A'nın hidden state'inde "B'nin A hakkındaki tahmini"nin izini arayan
prob. Ground truth: B'nin gerçek iç tahminleri (simülasyonda ikisine de
erişimimiz var — deneyin Tanrı-gözü avantajı). Bu, "modellenmeyi modelleme"
hipotezinin (H2) doğrudan ampirik testi. En değerli, en zor prob.

### P3 — Kanal-dışı iç sinyal (`p3_inner_speech.py`)
Ajanın sinyal-üretim katmanı aktivasyonlarını, sinyal GÖNDERMEDİĞİ turlarda
izle. Soru: sinyal üretim devresi, iletim olmadan iç durum düzenlemede rol
alıyor mu? (Ablasyon testi: bu devre susturulunca planlama performansı
düşüyor mu?) Beklenti negatif — negatifse H3 raporu yazılır, deney başarılı.

### Protokol analizi (`protocol_analysis.py`)
- **Topografik benzerlik:** anlam uzayı mesafeleri ↔ sinyal uzayı mesafeleri
  korelasyonu (birleşimsellik ölçüsü).
- **Zipf analizi:** sinyal frekans dağılımı doğal dil istatistiğine yaklaşıyor mu?
- **Bağlam ayrışması:** "tehlike+kuzey" ayrı semboller mi, ezber tek sembol mü?
- LLM burada devreye girer: log analisti olarak, deney dışında.

---

## 6. TEKNİK YIĞIN VE REPO YAPISI

| Katman | Seçim | Not |
|--------|-------|-----|
| Dil | Python 3.12 | |
| ML | PyTorch | ONNX gerekmiyor, deney ortamı |
| Env | Özel yazım (PettingZoo API uyumlu) | Hazır env'ler fazla zengin |
| Hız | NumPy vektörize dünya; gerekirse Numba | 64×64×5 ajan CPU'da koşmalı |
| Deney takibi | Yerel: SQLite + Parquet loglar | Bulut telemetri yok (alışkanlık) |
| Görselleştirme | Ayrı süreç, pygame/matplotlib replay | Canlı izleme eğitimi yavaşlatmasın |

```
petri/
├── CLAUDE.md              # bu dosyadan türetilecek session anayasası
├── KERNEL_BUDGET.md       # verilen her ön-bilginin bit muhasebesi
├── FINDINGS.md            # sprint sonu bulgular (negatifler dahil)
├── OPEN_LOOPS.md          # PL-xx numaralı açık işler
├── world/
│   ├── config.py
│   ├── grid.py            # fizik + kaynak + tehlike
│   └── events.py          # asimetrik olay enjeksiyonu
├── agent/
│   ├── config.py
│   ├── predictive_core.py # GRU world-model
│   ├── homeostasis.py
│   └── channel.py
├── population/
│   ├── roster.py          # heterojen kadro tanımı
│   └── lifecycle.py       # doğum/ölüm (DP-01'e bağlı)
├── probes/
│   ├── p1_self_model.py
│   ├── p2_higher_order.py
│   ├── p3_inner_speech.py
│   └── protocol_analysis.py
├── training/
│   ├── loop.py            # ana simülasyon döngüsü
│   └── snapshot.py        # temsil dondurma (prob girdisi)
├── replay/
│   └── viewer.py
└── tests/                 # her organ için birim test; fizik determinizm testi şart
```

---

## 7. SPRINT PLANI

| Sprint | Kapsam | Bitti tanımı |
|--------|--------|--------------|
| S0 | Dünya fiziği + determinizm testleri + replay viewer | Aynı seed → bit-eş simülasyon; 10K tur < 60 sn |
| S1 | Tek ajan: tahmin çekirdeği + homeostaz, kanal KAPALI | Ajan A-kaynağıyla hayatta kalmayı öğreniyor; P1 prob altyapısı hazır |
| S2 | P1 çalıştır: öz-model tek ajanda çıkıyor mu? | H1 için ilk veri noktası + FINDINGS girişi |
| S3 | Nüfus + kanal AÇIK + B-kaynağı (koordinasyon şartı) | Sinyal kullanımı > şans seviyesi VEYA kullanılmıyor raporu |
| S4 | Asimetrik olaylar + protokol analizi | Topografik benzerlik ölçümü; H4 verisi |
| S5 | P2 + P3 problar, uzun eğitim (≥1M tur) | H2/H3 raporu; DP-01 kararı verilmiş |

Kural: sprint atlamak yasak. S2 negatifse S3'e yine geçilir ama FINDINGS'e
"öz-model tek ajanda çıkmadı, sosyal basınçla çıkarsa H2 güçlenir" notu düşülür.

---

## 8. KARAR NOKTALARI (OPEN_LOOPS formatı)

- **DP-01 — Süreklilik sorusu (AÇIK, S5'te karar):** Ölen ajanın yerine gelen
  yeni ajan (a) sıfırdan mı başlar (saf online learning — v1 ideali),
  (b) ölenin ağırlıklarından mutasyonlu tortu mu devralır (mikro-pretrain,
  "çekirdek + miras" tezi)? **Öneri:** S5'e kadar (a) ile koş; iki koşulu
  A/B olarak karşılaştır ve ilkeyi veriyle test et. İlke tartışması veriyle
  çözülür, sezgiyle değil.
- **DP-02 — Kanal genişliği ablasyonu:** 4 bit anayasal ama 2/4/8 bit
  ablasyonu H4 için kontrol deneyi olarak S4 sonunda düşünülebilir.
- **DP-03 — Nüfus ölçeği:** 5 ajan yetmezse 7'ye çıkma kriteri: B-kaynağı
  açılma oranı 100K turda < %5 kalırsa.

---

## 9. BAŞARI KRİTERLERİ VE YAYIN

- Her hipotez için pozitif/negatif fark etmeksizin bulgu raporu.
- Tüm kod + seed + loglar tekrarlanabilir halde GitHub'a (alibeydilidev),
  PROMETHEUS v1 geleneğinde dürüst README + disclaimer ile.
- Rapor dili: iddiasız, ölçüm-merkezli. "Bilinç" kelimesi yalnızca
  "aramadığımız şey" bağlamında geçer; aradığımız şey **öncüller**dir.

---

## 10. İLK OTURUM TALİMATI (Claude Code'a)

1. Bu dosyayı oku, `CLAUDE.md` + `OPEN_LOOPS.md` + `KERNEL_BUDGET.md`
   iskeletlerini türet.
2. S0'dan başla: `world/grid.py` + determinizm testleri. Fizik, prob veya
   ajan koduna S0 bitmeden dokunma.
3. Her eklenen prior için KERNEL_BUDGET.md'ye satır aç — "grid'in toroidal
   olduğu bilgisi ajana veriliyor mu, veriliyorsa kaç bit?" seviyesinde
   titizlik.
4. Belirsizlikte Ali'ye sor, varsayma.
