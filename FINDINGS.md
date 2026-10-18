# FINDINGS — Sprint Sonu Bulgular (negatifler dahil)

> Anayasa md. 7: Negatif sonuç sonuçtur. Her sprint sonunda bulgular,
> çıkmayan şeyler dahil buraya yazılır. Rapor dili iddiasız,
> ölçüm-merkezli. Her pozitif bulgu önce H0'a ("hepsi reaktif hesaplama")
> karşı savunulur.

---

## BEŞ KAPI — Pozitif Bulgu Kontrol Listesi (ZORUNLU ŞABLON)

**Kural:** Pozitif bulgu iddiası bu beş kapıdan geçmeden rapora giremez.
Her pozitif bulgu girişi aşağıdaki şablonu doldurur. Tek bir kapı boşsa
veya "GEÇMEDİ" ise bulgu "İDDİA" değil "ADAY GÖZLEM" olarak etiketlenir
ve öyle kalır.

### Şablon (kopyala-doldur)

```markdown
## BULGU-Sxx-nn: <tek cümlelik, iddiasız başlık>
- Hipotez: H_  | Prob: P_ | Tarih: ____ | Commit: ____
- Statü: ADAY GÖZLEM → (beş kapı geçilirse) İDDİA

### KAPI 1 — Ablasyon gerçekten düştü mü?
Gönderilmeyen sembol geri beslemesi kesildi, planlama performansı düştü —
kaç seed'de? Tek seed'de düşüş gürültüdür.
- [ ] En az 5 seed'de koşuldu. Seed listesi: ____
- [ ] Düşüş HEPSİNDE tutarlı. Seed-bazlı sonuç tablosu: ____
- [ ] Etki büyüklüğü raporlandı (ör. Cohen's d / % düşüş + CI): ____
- [ ] TERS ABLASYON: geri beslemeye rastgele sembol enjekte edildi.
      Sonuç: ____
      Performans aynı kalıyorsa bu "iç konuşma" DEĞİL, ekstra rekürran
      kapasitedir — ajan sembollerle değil o kabloyla düşünüyordur.
      Sembollerin İÇERİĞİ fark yaratmak zorunda.
- KAPI 1 SONUÇ: GEÇTİ / GEÇMEDİ — gerekçe: ____

### KAPI 2 — Prob sızıntısı var mı?
- [ ] P3 (ve ilgili prob) dedektör gradyanının ajan eğitimine HİÇBİR
      yoldan değmediği doğrulandı. Doğrulama yöntemi: ____
- [ ] Snapshot pipeline'ında dondurma gerçekten dondurma: tüm prob
      girdileri detach/no_grad altında, satır satır kontrol edildi.
      Kontrol eden + commit: ____
- [ ] Kanıt: prob eğitimi öncesi/sonrası ajan ağırlık hash'leri bit-eş.
      Hash'ler: ____
- Not: Tek bir unutulmuş detach() bütün bulguyu enjekte edilmiş yapar.
- KAPI 2 SONUÇ: GEÇTİ / GEÇMEDİ — gerekçe: ____

### KAPI 3 — Zaman çizgisi doğru mu? (Vygotsky sıralaması)
İç sinyal kullanımı, sosyal sinyal yetkinliğinden SONRA mı doğdu?
Tez sıralamaya bağlı: önce dışa konuşma, sonra içe göçme.
- [ ] Sosyal sinyal yetkinliğinin doğum turu ölçüldü: tur ____
- [ ] İç sinyal kullanımının doğum turu ölçüldü: tur ____
- [ ] Sıralama: sosyal → iç (arada anlamlı gecikme). Gecikme: ____ tur
- Eşzamanlı doğdularsa ya da iç kullanım önce geldiyse: gözlenen şey
  içselleştirilmiş iletişim DEĞİL, baştan beri var olan bir hesaplama
  yoludur — ilginç ama başka bir bulgudur; öyle raporlanır.
- KAPI 3 SONUÇ: GEÇTİ / GEÇMEDİ — gerekçe: ____

### KAPI 4 — KERNEL_BUDGET temiz mi?
İlgili bağlantı/yol mimaride açık bırakıldı ama teşvik edilmedi — emin miyiz?
- [ ] Loss fonksiyonu satır satır tarandı: o yolu kayıran terim yok. ____
- [ ] Başlatma ağırlıkları tarandı: o yola asimetrik avantaj yok. ____
- [ ] Öğrenme oranı zamanlaması tarandı: o yolu kayıran schedule yok. ____
- [ ] KERNEL_BUDGET.md güncel; bulgede rol alan her yapısal seçim ya
      defterde ya da "prior değil" gerekçesiyle kayıtlı. ____
- KAPI 4 SONUÇ: GEÇTİ / GEÇMEDİ — gerekçe: ____

### KAPI 5 — Bit-eş tekrar
- [ ] Aynı seed, SIFIRDAN koşum (temiz süreç, temiz durum).
- [ ] Aynı turda aynı bulgu yeniden üretildi. Tur: ____ | Metrik: ____
- [ ] Koşum hash'leri bit-eş (S0 determinizm altyapısı: `World.state_hash()`).
      Hash: ____
- KAPI 5 SONUÇ: GEÇTİ / GEÇMEDİ — gerekçe: ____

### KARAR
Beş kapı sonucu: __/5 GEÇTİ → Statü: İDDİA / ADAY GÖZLEM
H0 savunması (bulgu neden salt reaktif hesaplamayla açıklanamıyor): ____
```

---

# Sprint girişleri

## S0 — Dünya fiziği + determinizm + replay (2026-07-08)

S0 bir hipotez sprinti değil, altyapı sprintidir; bulgu girişi yok.
Bitti-tanımı ölçümleri:

- **Bit-eş determinizm:** Aynı seed ile iki bağımsız koşum, 3.000 tur
  boyunca her 250 turda `state_hash()` (SHA-256; RNG durumu dahil tüm
  dünya durumu) karşılaştırıldı → tümü eş. Snapshot al/geri yükle/devam
  koşumu da kesintisiz koşumla bit-eş. (bkz. `tests/test_determinism.py`)
  Ayrıca süreçler-arası doğrulama: iki AYRI işletim sistemi sürecinde
  10.000 turluk kayıt, aynı final hash: `23679df497437ed0…fac9f87d`.
- **Hız:** 10.000 tur, 5 varlık, rastgele eylemler: **0.275 sn**
  (~36.400 tur/sn) — < 60 sn şartı ~218× marjla sağlandı.
  (Ölçüm: `tests/test_perf.py`, Apple Silicon, Python 3.13.2, numpy 2.4.2.)
- **Negatif/eksikler (dürüstlük):** Tehlike geometrisi/ömrü ve hasat
  semantiği dokümanda tanımsızdı; varsayımlar PL-01/PL-02'de, Ali onayı
  bekliyor. `world/events.py` bilinçli olarak S3–S4'e ertelendi (PL-05).

---

## S1 — Tek ajan (A2), kanal KAPALI: çekirdek + homeostaz + MPC (2026-07-08)

Altyapı sprinti; hipotez iddiası yok. Beş Kapı burada bulguya değil,
sürece uygulandı (≥5 seed + etki büyüklüğü + bit-eş altyapı).

### (a) Hayatta kalma üstünlüğü — SAĞLANDI (v2 koşumu)
Protokol: seed başına ~40K tur eğitim (ağırlıklar epizotlar arası taşınır,
PL-06), sonra 12 taze dünyada eval; rastgele politika AYNI dünyalarda.
Tek yönlü Mann-Whitney U + Cliff's δ. Veri: `runs/s1_results.json`.

| seed | A2 medyan | rastgele medyan | p | Cliff's δ |
|------|-----------|------------------|-----|-----------|
| 0 | 130 | 88 | 1.7e-4 | 0.868 |
| 1 | 128 | 91 | 1.8e-5 | 1.0 |
| 2 | 129 | 91 | 1.7e-5 | 1.0 |
| 3 | 166 | 88 | 1.8e-5 | 1.0 |
| 4 | 163 | 88 | 1.8e-5 | 1.0 |

5/5 seed'de aynı yönde, anlamlı, büyük etki. Hiçbir epizot 1500 tur
tavanına çarpmadı (sansür yok).

**Dürüstlük notları:**
1. **v1 koşumu BAŞARISIZDI** (`runs/s1_results_v1_failed.json`): 2/5
   seed'de A2 rastgeleden KÖTÜydü (δ=-1.0). Neden: MPC argmax'ı kendi
   eğitim verisini yanlılaştırdı (STAY hiç denenmedi → tasarruf
   öğrenilemedi) + kırpılmamış rollout geri beslemesi sayısal kaçıyordu.
   Düzeltmeler (ε=0.1 keşif, [0,1] kırpma, J=ufuk ortalaması) K-108 ve
   K-103 revizyonu olarak KERNEL_BUDGET'a işlendi. Deney değil mimari
   düzeltildi; v1 ham verisi silinmedi.
2. **Üstünlüğün kaynağı hasat DEĞİL, enerji tasarrufu.** Eval'de A2
   hasat ortalaması 0-3.8 enerji/epizot (çoğunlukla 0). Ajan "A-kaynağıyla
   hayatta kalmayı" değil, "ucuz eylem seçmeyi" öğrendi. Yaşam süresi
   (128-166) saf-tasarruf üst sınırının (~260, ε maliyetli) altında —
   öğrenme kısmi. A-hasadı davranışı S1'de ÇIKMADI; bu, kaynak
   karşılaşma seyrekliğiyle (12/4096 hücre, menzil 4) tutarlı. S2/S3'te
   kıtlık basıncı ayarı gerekebilir (PL-10).
3. PL-09: enerji tahmin hedefinde λ=10 ile kayrılıyor — S2'de P1
   yorumlanırken bu enjeksiyon hesaba katılmak zorunda.

### (b) Snapshot/temsil dondurma pipeline'ı — ÇALIŞIYOR
`training/snapshot.py`: hidden state + enerji + konum + eylem + tur +
dünya hash'i, anında detach + numpy kopyası. Sızıntısızlık KANITI:
kayıt açık ve kapalı eğitim bit-eş ağırlık hash'i üretiyor
(`tests/test_training.py::test_recording_does_not_touch_training`).
5 seed'in son eval epizotları `runs/snapshots/` altında (P1 girdisi,
analiz S2'nin işi — probes/ klasörüne kod yazılmadı).

### (c) 5-ajanlı performans projeksiyonu
Ölçüm: 1.071 ms/tur/ajan (MPC C=32×D=5 + TBPTT-8 öğrenme + dünya;
tek thread, Apple Silicon). Dünya adımı ~0.015 ms (ihmal edilebilir).
- 5 ajan seri (naif): ~5.4 ms/tur → 100K tur ≈ **9 dk**; 1M tur (S5) ≈ **90 dk**.
- 5 ajan paralel süreç (çekirdek başına 1 ajan, determinizm korunur):
  ~1.1-1.5 ms/tur → 1M tur ≈ **20-25 dk**.
- Heterojen hidden boyutları tek batch'e engel; süreç-paralelliği önerilir.
S5'in ≥1M tur şartı mevcut donanımda RAHAT karşılanır. Risk: S3'te kanal
+ 5 ajan gözlem maliyeti gözlem yarıçapına bağlı (~%10-30 artış beklenir).

### S1 determinizm
Aynı seed üçlüsüyle eğitim bit-eş ağırlık üretir
(`test_training_bit_identical_repeat`); torch tek thread'e sabitlendi.

---

## S2 — P1 öz-model probu, tek ajan (2026-07-08)

**H1 verisi. Manşet: öz-modelin ANA kanıtı (yol entegrasyonu) tek ajanda
ÇIKMADI. Negatif sonuç sonuçtur; H1 tek-ajan koşulunda desteklenmedi.**

Protokol: 5 seed × PL-10 müfredatlı eğitim (A-kaynağı 48→24→12, 45K tur)
× 6 checkpoint × 6 öğrenmesiz eval epizodu (standart kıtlık), dondurulmuş
temsiller (`runs/s2_snapshots/`, 180 epizot). Prob: lineer ridge, epizot
başına dışarıda-bırak CV; kontroller: (a) 3 rastgele-ağırlıklı ikiz GRU
(deterministik dünya replay'i ile AYNI gözlem/eylem akışında — replay
sadakati pozisyon bit-eş + enerji 1e-6 assert'li), (b) etiket karıştırma,
(c) checkpoint eğrisi. Veri: `runs/s2_p1_results.json`.
Zero-touch kanıtı: checkpoint'li ve checkpoint'siz eğitim bit-eş ağırlık
(`tests/test_s2_gen.py::test_checkpoints_zero_touch`).

### Hedef 1 — öz-konum / yol entegrasyonu (ANA kanıt): **NEGATİF**
- Eğitilmiş temsilde displacement R² çoğunlukla NEGATİF (epizotlar-arası
  genelleme yok); seed/checkpoint boyunca düzensiz.
- Eğitilmiş−ikiz farkı tutarsız: final ckpt Δ ∈ {−0.20, −0.08, −0.02,
  +0.03, +0.45}, hiçbir seed'de p<0.05 (Wilcoxon, n=6 epizot).
- Eğri (kontrol c) 2/5 seed'de düşüyor → "kazanılmış" etiketi de yok.
- MLP ikinci görüş (lineer negatif olduğu için zorunluydu): o da tutarsız
  (3/5 seed'de eğitilmiş < ikiz). İki sonuç birlikte: **sinyal yok.**
- Mekanik not: davranış aşırı kalıplaşmış (aynı ckpt'te yaşam süreleri
  neredeyse özdeş, örn. [79,79,79,83,79,79]) → displacement varyansı
  düşük, prob tahminleri kararsız. Tek başına açıklama değil ama probun
  istatistik gücünü düşürüyor (PL-11).

### Hedef 2 — öz-enerji (PL-09 şerhli, YAN kanıt): **ADAY GÖZLEM**
- Eğitilmiş R² 0.983–0.997; ikiz de 0.96–0.98 → sinyalin BÜYÜK kısmı
  girdi yankısı (enerji gözlemin içinde) + rezervuar etkisi; yapısal.
- Eğitilmiş > ikiz farkı: 5/5 seed'de anlamlı (p≤0.031) ama etki MİNİK
  (ΔR² +0.011…+0.042). Eğri 4/5 seed'de yükseliyor (seed 4: düz/negatif).
- Karar: Ali'nin S2 şartı "anlamlılık + etki + yükselen eğri" ÜÇÜNÜ
  istiyor; eğri 4/5 → şart eksik → **ADAY GÖZLEM**, İDDİA değil.
  Üstüne PL-09: enerji λ=10 ile eğitime enjekte — bu farkın "öz-model"
  değil "kayrılmış hedefin artığı" olması baş hipotez olmalı (H0 önce).

### Hedef 3 — sonraki-tur öz-enerji deltası: **NEGATİF**
R² ≈ 0 (en iyi +0.03), hiçbir seed'de anlamlı fark yok. İleriye dönük
enerji-değişim sinyali lineer okunur değil.

### Yan bulgu — müfredat hasadı ÜRETEMEDİ
180 standart-kıtlık eval epizodunda toplam 3 tekil hasat (hepsi 15.0,
tesadüfi görünümlü). Yoğun fazda (48 kaynak) öğrenilen şeyin kıt faza
transferi yok. PL-10 yeniden açıldı.

### Sprint kuralı gereği not (doküman §7)
Öz-model tek ajanda çıkmadı; S3'e geçilir. Sosyal basınç altında (S5/P2
yolunda) çıkarsa H2 güçlenir — bu karşılaştırma için S2'nin negatif
taban çizgisi artık elimizde ve bit-eş yeniden üretilebilir.

---

## S2.5 — Tek hedef: güvenilir A-hasadı (2026-07-08)

**Manşet: BİTTİ-TANIMI SAĞLANAMADI. Dört izole müdahale de (merdiven
protokolü) standart kıtlıkta hasat üretemedi (medyan 0). Ama başarısızlığın
mekanizması üç enstrümanlı teşhisle zincir halinde belgelendi — bu S3+
tasarımı için S2.5'in asıl çıktısıdır.**

### Merdiven sonuçları (5 seed, eval: 12 taze dünya + seed'li spawn,
taban çizgisi: saf-tasarruf/ε=0 "stay" politikası, eşleştirilmiş Wilcoxon)

| adım | müdahale (birikimli) | medyan hasat | medyan yaşam | stay tavanı | ms/tur |
|------|----------------------|--------------|--------------|-------------|--------|
| 1 | ufuk 5→10 | 0 | 118–150 | 334 (m=0.3) | 1.72–1.81 |
| 2 | + metabolizma 0.3→1.0 (kalibrasyon: tavan 100 < S2 medyan 130) | 0 | 57–69 | 100 | 1.66–1.77 |
| 3 | + yumuşak müfredat 48→36→24→18→12 (60K), C=48 | 0 | 57–75 | 100 | 2.65–3.22 |
| 4 | planlayıcı örneklemesi: sabit-eylem adayları + elit iyileştirme (K-109; teşhis-güdümlü ek adım) | 0 | 50–91 | 100 | 2.91–4.83 |

Hiçbir adımda hiçbir seed stay taban çizgisini geçemedi (tüm p=1.0).
Veriler: `runs/s25_step{1..4}.json`.

### Mekanizma zinciri (enstrümanlı teşhisler)
1. **5K tur:** modelin eylem-koşullu enerji tahmini TERS işaretli
   (STAY−UP: model −0.026, gerçek +0.055) — erken dönemde on-policy
   verinin ~%87'si hareket; MSE'nin ucuz çözümü eylemi yok saymak.
2. **45K tur (adım-2 verisiyle):** koşullama DÜZELİYOR (+0.084, gerçek
   +0.055) — model biliyor. Ama epizot-içi sonda: MPC yalnız %55 STAY
   seçiyor; rastgele aday dizilerinde İLK-EYLEM SEYRELTMESİ + ε=0.1,
   ajanı ~%45 gereksiz harekete kilitliyor → 69 turda ölüm (tavan 100).
3. **Adım 4 (seyreltme giderildi):** seed 4 kuramsal tavana oturdu
   (medyan 91 ≈ ε-maliyetli tavan 92) ama seed 0-1 ~51'e ÇÖKTÜ:
   STAY-ağır hale gelen eğitim verisi dengesizliği ters çevirdi —
   model bu kez hareketin maliyetini kalibre edemiyor.

**Kök neden (S2.5'in asıl bulgusu):** tek içsel sinyal (tahmin hatası)
+ on-policy veri + MPC kapalı döngüsü, EYLEM-KOŞULLU KARŞI-OLGUSAL
kalibrasyonu sürdüremiyor. Ajan hangi davranışa yakınsarsa, az yaptığı
eylemlerin sonuç modeli bozuluyor; planlayıcı da o bozuk modele göre
seçiyor (S1-v1 başarısızlığının genelleşmiş hali). Hasat, bu kararsızlık
çözülmeden ulaşılabilir görünmüyor: kaynak +15 sinyalini öğrenmek şöyle
dursun, tasarruf dengesi bile seed'e göre savruluyor. (PL-12)

### S2-tekrar: P1, spawn-randomizasyonlu (PL-11 itiraz testi)
Ali'nin öngörüsü ("öz-konum eğrisi hasatla birlikte yükselir") hasat
çıkmadığı için **TEST EDİLEMEDİ** — tez yara almadı, askıda; hasatçı
ajan üretilene dek açık kalır. Bunun yerine S2 protokolü, S2 config'iyle
+ spawn randomizasyonuyla yeniden koşuldu (`runs/s2r_p1_results.json`):
- **disp: negatif SAĞLAM.** Varyans artışı sinyali kurtarmadı (Δ tutarsız,
  p hiçbirinde <0.05, eğriler düzensiz). S2 negatifi kalıplaşma artefaktı
  değil.
- **energy: ADAY GÖZLEM güçlendi ama etiket değişmedi.** Artık 5/5 seed
  anlamlı (p≤0.016) VE 5/5 yükselen eğri (S2'de 4/5'ti). Etki hâlâ minik
  (ΔR² +0.020…+0.035, ikiz taban 0.96+). Yükseltme engeli: PL-09 (λ=10
  enjeksiyonu) — çözüm yolu λ=1 ablasyon koşumu; o yapılmadan İDDİA'ya
  terfi edemez.

### Dürüstlük
- Adım 4, Ali'nin merdiveninde yoktu; teşhis-güdümlü ek adım olarak
  izole uygulandı ve K-109 ile deftere işlendi. Varsayılan config eski
  davranışı bit-eş korur (`test_mpc_defaults_bitcompatible_with_pre_step4`).
- Adım 2'nin kalibrasyon hesabı: tavan = max_energy/base_metabolism =
  100/1.0 = 100 tur < 130 (S2 medyan alt sınırı). KERNEL_BUDGET S2.5
  şerhinde.
- Tehlike-kaçınma davranışı hiç ayrıca ölçülmedi (hasat önceliklendirildi);
  S3 öncesi açık kalem.

---

## S2.6 — Fizibilite oracle'ı + PER + λ ablasyonu (2026-07-08)

**Manşet 1: Dünya ekonomisi hasadı HER koşulda net zarar yapıyor —
S2.5'in başarısızlığının altındaki katman öğrenme değil, EKONOMİYMİŞ.
Manşet 2 (λ=1 ablasyonu): öz-enerji aday gözlemi λ=10 kayırmasının
artefaktı DEĞİL — iki bağımsız itiraz testinden sağ çıktı.**

### İş 1 — Fizibilite oracle'ı → DUR koşulu (güçlü formu) tetiklendi
Scripted referans politika (aynı gözlem yarıçapı, aynı maliyetler;
görünür kaynağa aç-gözlü yürüyüş + lawnmower taraması + tehlike sapması;
`training/oracle.py` — ajan değil ölçüm aleti, KERNEL_BUDGET'a bit yazmaz).

Izgara (12 epizot/koşul, spawn randomizasyonlu; `runs/s26_oracle.json`):

| koşul | medyan hasat | oracle yaşam | stay tavanı |
|-------|--------------|--------------|-------------|
| m=1.0, 12 kaynak | 2.0 | 64 | 100 |
| m=1.0, 24 kaynak | **3.5** | 76 | 100 |
| m=0.6, 12 | 2.0 | 80 | 167 |
| m=0.6, 24 | 3.5 | 96 | 167 |
| m=0.3, 12 | 2.0 | 98 | 334 |
| m=0.3, 24 | 7.0 | 150 | 334 |

Harfe göre seçilen koşul m=1.0/24 (hasat ≥3). AMA: oracle HİÇBİR koşulda
saf-tasarrufu geçemiyor — yetkin hasatçı bile tasarrufçudan kısa yaşıyor.
Revize bitti-tanımının (i) hasat≥3 ve (ii) stay'i geç şartları mevcut
anayasal ekonomide (A=15) BİRLİKTE SAĞLANAMAZ (kaba hesap: 3 hasat için
tarama şart → hareket oranı ~%90 → yaşam ~74 < 100). Geriye dönük içgörü:
S2.5'in hedefi baştan ulaşılamazmış; ayrıca 12-kaynaklı standart dünyada
"medyan 3 hasat"ı oracle bile hiçbir metabolizmada veremiyor.
→ Stage-2 eğitimi mahkûm hedefe karşı YAKILMADI; karar Ali'ye (PL-14).
A-enerji süpürmesi (salt ölçüm, `runs/s26_a_energy_sweep.json`)
oracle-doğrulanmış geçerli pencereyi çizdi: A=45+ @ 24 kaynak
(önerilen: m=0.6/24/A=45 — hasat 8.5, yaşam 197 vs stay 167).

### İş 2 — PER (K-110): KOD-HAZIR, koşum PL-14'ü bekliyor
Tampon + kayıp-orantılı örnekleme + hafif eylem tabakalaması;
ε=0.1 ve K-109 korunur. Testli (determinizm, öncelik yanlılığı,
tabakalama, bit-eş korunum); `training/per.py`. Stage-2/3 koşusu
`training/eval_s26.py`'de hazır — kalibrasyon kararıyla tek komut.

### Paralel — λ=1 ablasyonu (PL-09): KONFOUND ÇÜRÜDÜ
S2 protokolü, tek fark energy_loss_weight 10→1
(`runs/s2_lambda1_p1_results.json`):
- Öz-enerji ΔR² (eğitilmiş−ikiz): λ=10'da ort +0.028, λ=1'de ort +0.026 —
  fark yok; 5/5 seed hâlâ p=0.016; yükselen eğri 4/5.
- Yani minik ama tutarlı öz-enerji avantajı loss kayırmasından GELMİYOR.
  PL-09 kapandı. ADAY GÖZLEM güçlendi (itiraz testleri: spawn
  randomizasyonu ✓, λ ablasyonu ✓) ama İDDİA'ya terfi ETMEDİ: etki hâlâ
  minik (ikiz tabanı 0.96+ üstüne +0.02-0.04) ve H0 alternatifi ayakta —
  "herhangi bir hedefle eğitilmiş GRU girdilerini rastgele GRU'dan iyi
  temsil eder" (genel eğitim etkisi ≠ öz-model). Ayrıştırma yolu PL-15:
  enerji-körü eş-eğitimli kontrol (enerji gözlemden/hedeften çıkarılmış
  ikiz eğitim).
- disp λ=1'de de negatif/tutarsız (seed 2'de ΔR²=+33 tekil aykırı değer —
  ikiz probunun düşük-varyans epizotta patlaması; p=0.28, sinyal değil).

### PL-13 durumu
Hasat üretilemediği için S2-tekrar OTOMATİK TETİKLENMEDİ; Ali'nin
öngörüsü askıda kalmaya devam ediyor. Kalibrasyon + PER koşumu hasat
verirse tetiklenecek (protokol hazır).

---

## S2.6 stage-2 — PER + v2 ekonomi koşumu (2026-07-08)

**Manşet: Bitti-tanımı yine sağlanamadı (hasat 0.0), AMA iki kritik
sonuçla: (1) PER seed'ler-arası çöküşü BİTİRDİ — PL-12 kararsızlığına
kısmi çözüm; (2) kök neden artık ölçülü: keşif, hasat DENEYİMİNİ
üretemiyor — 45K turda 10 olay.**

Koşul: m=0.6, 24 kaynak, A=45 (economy_version=2, config damgalı),
PER + K-109 + ufuk 10, ε=0.1. Veri: `runs/s26_results.json`.

| seed | medyan hasat (eşik 3.4) | medyan yaşam | stay | p |
|------|--------------------------|--------------|------|---|
| 0 | 0.0 | 148 | 167 | 0.99 |
| 1 | 0.0 | 148 | 167 | 1.0 |
| 2 | 0.0 | 146 | 167 | 1.0 |
| 3 | 0.0 | 148 | 167 | 1.0 |
| 4 | 0.0 | 134 | 167 | 0.99 |

- **Çöküş-yok şartı GEÇTİ:** medyanlar 134–148 (bant %50'nin çok
  üstünde); S2.5-adım-4'ün 51'e çöken patolojisi PER'le kayboldu.
  Ajan tavanın (167) ~%85-89'una tutarlı oturuyor — tasarruf artık
  stabil öğreniliyor. PL-12'nin "tasarruf kararsızlığı" yüzü kapandı.
- **Hasat şartı GEÇEMEDİ:** tüm seed'lerde 0.0 (eval).
- **Teşhis (M-05 dipnotunun doğrulaması):** stage-2 seed-0 eğitiminin
  bit-eş tekrarında toplam hasat olayı sayıldı: **45.066 turda 10**
  (10K turda 2.2). "Kaynak üstünde + INTERACT" durumu ε-rastgele
  yürüyüşle neredeyse hiç oluşmuyor; PER yalnız YAŞANMIŞ deneyimi
  tekrarlatabilir. Sorun artık ne ekonomi (oracle: hasat kârlı), ne
  model kalibrasyonu (tasarruf stabil), ne planlayıcı (K-109) — sorun
  KEŞİF: görme→yaklaşma→etkileşim zinciri kendiliğinden tamamlanmıyor.
  Ekolojik tuzak: kârlı strateji, keşfedilemeyecek kadar derin (PL-16).

### Sonraki müdahale sınıfı Ali kararı ister (kernel-anayasal)
- (a) Merak terimi (K-104 bilinçli boştu): MPC hedefine tahmin-hatası
  arayışı eklemek. Anayasa md.2'nin ("tek içsel sinyal: tahmin hatası +
  homeostaz") harfiyle uyumlu savunulabilir ama K-104'ün bilinçli
  boşluğunu bozar — Ali onayı şart.
- (b) Dünya-tarafı yuva/doğum müfredatı: eğitimde ajanın bir kısım
  epizotta kaynak yakınında doğması (sıfır ajan-biti, PL-10 müfredat
  emsali; deneyim taban-oranını organik büyütür).
- (c) S3'e bu haliyle geçmek: nüfus dinamiği durum uzayını ajan-dışı
  karıştırır (en ekolojik, en belirsiz).
- Tavsiyem: (b) önce — en ucuz, emsalli, geri alınabilir; (a) felsefi
  olarak ağır; (c) PL-12/16 çözülmeden B-kaynağı basıncını boğabilir.

### PL-15 — Enerji-körü eş-eğitimli kontrol: SONUÇ KESKİN
İki kol, aynı protokol (v2 ekonomi, PER, düz 24-kaynak, 45K tur, spawn
randomize; config-damgalı), tek fark `interoception` bayrağı.
Veri: `runs/s2_pl15_{normal,blind}_p1.json`.

| seed | NORMAL Δ(enerji) R² | p | KÖR Δ | p |
|------|---------------------|-----|-------|-----|
| 0 | +0.058 | 0.016 | −0.092 | 1.0 |
| 1 | +0.074 | 0.016 | +0.018 | 0.42 |
| 2 | +0.051 | 0.016 | −0.147 | 1.0 |
| 3 | +0.074 | 0.016 | −0.024 | 0.78 |
| 4 | +0.091 | 0.016 | −0.091 | 0.92 |

- Normal kol: eğitilmiş 0.99 vs ikiz 0.90–0.94; Δ önceki koşumlardan da
  büyük (+0.07 ort), 5/5 anlamlı, eğri 5/5 yükselen.
- Kör kol: eğitilmişte de ikizde de R² ≈ 0 — enerji girdisi olmayınca
  temsil YOK. İki çıkarım: (1) enerji dekodlanabilirliği zaman/korelat
  türevi değil (kör ajanın enerjisi de zamanla ~monoton düşüyor ama
  hidden'ından okunamıyor — eğitim "genel bir saat" üretmiyor);
  (2) etki interosepsiyon girdi yolunu işlemeye bağlı.
- **Kapatılamayan son itiraz:** "eğitilmiş GRU TÜM girdilerini genel
  olarak daha iyi temsil eder" H0'ı için varyans-eşleşmiş kontrol
  özelliği denendi (görünür-A sayısı, ad-hoc analiz) ve BAŞARISIZ:
  hareketsiz rejimde epizot-içi varyansı olan enerji dışında hiçbir
  girdi özelliği yok → LOEO R² dejenere. M-03 yine: bu ayrım mobil
  ajan gelmeden test EDİLEMEZ. Etiket **ADAY GÖZLEM** kalır; terfi
  kapısı PL-16'nın (mobilite) çözümüne kilitlendi — mobil ajan hem
  disp'i hem bu son ayrımı aynı anda test edilebilir kılar.

### Yeni ders var mı? (METODOLOJI kuralı)
VAR → M-14 eklendi: müdahale seçmeden önce hedef deneyimin taban oranı
sayılır. ("Model X'i öğrenemiyor" teşhisi, X deneyiminin veride kaç kez
geçtiği ölçülmeden eksiktir — PER'i seçmeden önce bunu saysaydık bir
koşum tasarruf ederdik.)

---

## S2.7 — ÖN-KAYIT (koşumdan önce yazıldı, M-08) (2026-07-08)

### İş 1 sonucu ve eşik revizyonu
Görünür-A oracle'ı (taramasız: görünürse yaklaş, yoksa STAY), v2
koşulunda (m=0.6, 24 kaynak, A=45): **medyan hasat 1.0**, yaşam 172 vs
stay 167 (`runs/s27_visibleA_oracle.json`). Revize eşik =
max(3, 1.0×0.4) = **3**. Gerekçe: saf fırsatçılık medyan 1 verir; ≥3
hasat öğrenilmiş hafif keşif ister; tam-oracle bunun kârlı olduğunu
gösterdi (8.5 hasat, 197 yaşam). Eşik değişmedi ama artık iki oracle
arasına ölçülü oturuyor: 1.0 (fırsatçı taban) < 3 < 8.5×0.4=3.4 üstü
değil (eski eşikten daha gevşek DEĞİL; bilinçli: keşfin VARLIĞINI test
ediyoruz, oracle-düzeyi verimini değil).

### İş 2 ön-kaydı: Kalibrasyon-N kriteri (N* seçim kuralı)
Sentetik hasat-penceresi enjeksiyonu (gerçek fizikle üretilmiş,
PER tamponuna eğitim başında; SADECE teşhis — yuva koşumunda sentetik
enjeksiyon YOK). N ∈ {50, 200, 500, 2000}, 3 seed, 15K tur eğitim.
Kalibrasyon ölçüsü: kaynak-üstü durumda modelin INTERACT−STAY tahmini
enerji ayrımı (gerçek ayrım e=50'de ≈ +0.44 normalize).
**N* kuralı (önceden kayıt): N* = medyan tahmini ayrımın ≥ 0.22
(gerçeğin %50'si) olduğu en küçük N.** Müfredat-başarı kriteri: yuva
müfredatı eğitim boyunca ≥ N* GERÇEK hasat deneyimi üretmeli.
Varsayım beyanı: kalibrasyon 15K turda ölçülür, yuva 45K koşar —
"15K'daki kalibrasyon 45K'yı öngörür" varsayımı rapora yazılır.

### İş 4 ön-kaydı: Teşhis çatalı (sonuç matrisi, koşumdan önce)
- **ÇATAL A — bitti-tanımı GEÇER** (hasat ≥3, stay'e karşı uzama,
  çöküş yok): yorum = sorun keşif tuzağıydı; merak terimi (K-104)
  GEREKMEZ; ekolojik iskele yetti. → PL-13 OTOMATİK tetiklenir
  (P1 tekrarı, S2 protokolü, üç kontrol; Ali'nin öngörüsü test edilir:
  öz-konum eğrisi hasatla birlikte yükselecek mi).
- **ÇATAL B — GEÇEMEZ:** alt-teşhisle durulur, K-104 dosyası veriyle
  Ali'ye gider:
  - B1: müfredat < N* deneyim üretti → iskele yetersiz (p_nest/tavlama
    ayarı tartışılır, merak dosyası zayıf kanıtlı açılır);
  - B2: deneyim ≥ N* VE model kalibre AMA davranış hasada dönmedi →
    planlayıcı/karar katmanı sorunu (merak dosyası güçlü kanıtlı açılır:
    bilgi var, kullanım yok);
  - B3: deneyim ≥ N* AMA model kalibre OLMADI → öğrenme/temsil sorunu
    (PER/mimari tartışması, merak dosyası ertelenir).
PL-15 etiketi bu sprintte NE OLURSA OLSUN ADAY GÖZLEM'de kalır; mobil
ajan gelmeden terfi dosyası açılmaz (Ali talimatı).

### İş 2 ARA-DÜZELTME (yuva koşumundan ÖNCE kaydedildi)
İlk calibN süpürmesi N* = None verdi (statik-STAY sondası tüm N'lerde
≈0). ÜÇ katmanlı teşhis cihaz kusuru buldu (N=2000 ajanı üzerinde):
- Bağlam-içi tahmin (taze sentetik pencerede hasat adımı): **+0.363**
  (gerçeğin %84'ü) — model olumsallığı ÖĞRENMİŞ.
- Statik-STAY sondası: −0.024 — GRU bilgiyi yaklaşma-bağlamında tutuyor;
  sonda bağlam-dışıydı. Ön-kayıtlı v1 metriği CİHAZ HATASI nedeniyle
  geçersiz (sonuç manipülasyonu değil: iki metrik de raporlanıyor).
- Davranışsal: kaynak 2 hücre yandayken 10 denemede 2 hasat — bilgi
  var, MPC nakde çevirme zayıf (rollout'ta egosantrik kayma
  halüsinasyonu + aday önek olasılığı).
**Ön-kayıt v2 (yuva koşumundan önce):** kalibrasyon metriği = bağlam-içi
tahmini sıçrama; N* = medyanı ≥ 0.217 (gerçek 0.434'ün %50'si) yapan en
küçük N. Süpürme düzeltilmiş cihazla TEKRARLANIYOR; nest yorumu buna
bağlanacak. (Metodoloji ders adayı: sonda da cihazdır, bilinen-pozitif
üzerinde doğrulanmadan ön-kayıt kriteri yapılmaz — sprint kapanışında
M-15 olarak değerlendirilecek.)

## S2.7 — SONUÇLAR (2026-07-08)

### calibN (düzeltilmiş cihaz): **N* = 50**
Bağlam-içi sıçrama medyanları: N=50 → 0.27-0.34, N=200 → 0.35-0.40,
N=500 → 0.34-0.41, N=2000 → 0.33-0.36 (`runs/s27_calibN.json`).
Eğri 50'den itibaren DÜZ: PER, az sayıda deneyimi canlı tutarak
olumsallığı öğretebiliyor. Öğrenme ucuz; darboğaz veri değil.

### Yuva müfredatı: **ÇATAL B**
| seed | eğitim hasadı (N*=50) | eval hasat | yaşam vs stay | kalibrasyon (eşik .217) |
|------|----------------------|------------|----------------|--------------------------|
| 0 | 25 ✗ | 0.0 | 145/167 | 0.178 ✗ |
| 1 | **57 ✓** | 0.0 | 148/167 | **0.281 ✓** |
| 2 | 41 ✗ | 0.0 | 144/167 | 0.224 ✓ |
| 3 | **57 ✓** | 0.0 | 142/167 | **0.257 ✓** |
| 4 | 32 ✗ | 0.0 | 148/167 | 0.213 ✗ |

Çöküş-yok ✓ (142-148 sıkı bant); hasat ✗; yaşam-vs-stay ✗.
**Alt-teşhis: ağırlıklı B2.** Seed 1 ve 3 önceden kayıtlı İKİ kriteri de
sağladı (deneyim ≥ N* + kalibre model) ama eval hasadı 0 — bilgi var,
kullanım yok. Bağımsız doğrulama: calibN N=2000 ajanı (kalibrasyon 0.36)
kaynak 2 hücre yandayken 10 denemede 2 hasat. Nakde çevirme darboğazı:
rollout'ta egosantrik kayma halüsinasyonunun bileşik hatası + doğru
aday-önek seyrekliği. Yuva ayrıca beklenenden az deneyim üretti (25-57;
öngörü yüzlerceydi): yuva FIRSAT üretiyor, deneyim üretimi yine
davranışsal dönüşüm istiyor — döngüsel bağımlılık zayıf halka.
→ Talimat gereği DURULDU; **K104_DOSYA.md** veriyle hazırlandı.
Dosyanın özü: teşhis merak terimini DESTEKLEMİYOR (merak deneyim
üretimini çözer, o çözüldü; darboğaz planlayıcı nakde çevirmesi);
tavsiye önce K-109 revizyonu (CEM derinleştirme). Karar Ali'de.

### PL-13 durumu: tetiklenmedi (Çatal B); öngörü askıda kalmaya devam.

### Yeni ders var mı?
VAR → **M-15**: Sonda da bir cihazdır — ölçü aleti, bilinen-pozitif
üzerinde doğrulanmadan ön-kayıt kriteri yapılmaz. (Statik-STAY sondası
kalibre modele "kalibre değil" dedi; bilinen-pozitif testi — enjeksiyon
pencerelerinin kendisi — cihaz kusurunu bir koşum ÖNCE yakalardı.)

---

## S2.8 — ÖN-KAYIT (koşumdan önce, M-08) (2026-07-08)

### İş 1 ön-kaydı: rollout çürüme eğrisi ve H_eff kuralı
Ölçüm: yuva-eğitimli model (S2.7 konfigürasyonu, ≥3 seed), taze eval
epizotlarında çapa noktalarından açık-döngü k-adım tahmin (k=1..10,
KAYITLI gerçek eylemlerle, MPC'deki gibi [0,1] kırpmalı geri besleme),
gerçek gözleme karşı. Metrik: enerji-boyutu mutlak hata@k (planlayıcı
J'yi enerji üzerinden skorlar) + grid MSE@k (yan rapor).
Sinyal/gürültü tabanı: kalıcılık (persistence) tahmincisi
(obs_{t+k}=obs_t, e_{t+k}=e_t). **H_eff = medyan enerji-hata@k'nın
kalıcılık hatasının ALTINDA kaldığı en büyük ardışık k.**
**K-112 kuralı (önceden seçildi): ufuk KIRPMA (iskonto değil) —
planlayıcı skorlaması J = ilk min(H_eff, D) adımın ortalama tahmini
enerjisi. H_eff ≥ 10 ise değişiklik yok.** Kırpma tercihi gerekçesi:
tek parametre, yorumu net, iskonto katsayısı ayrı bir serbest parametre
ekler (M-09 tasarrufu).

### İş 3 ön-kaydı: nakit testi başarı çıtası
Standart enstrüman `training/cash_test.py`: kaynak Chebyshev {1,2,3}
mesafede (yön rastgele, seed'li), enerji 50, 12 tur bütçe; 20 deneme ×
5 seed. **Çıta: d=1 VE d=2'de (ayrı ayrı, seed'ler üstü havuzlanmış)
hasat oranı ≥ %70.**

### İş 5 ön-kaydı: çatal
- Nakit GEÇER + stage-2 eval hasadı ≥3 → **ÇATAL A**: PL-13 otomatik,
  P1 tekrarı, Ali öngörüsü sınavda.
- Nakit GEÇER + eval hasadı yine ~0 → kalan boşluk KEŞİF/ARAMA
  davranışı (görünür kaynak yokken); K104_DOSYA.md o veriyle yeniden
  açılır — merak lehine ilk gerçek kanıt.
- Nakit GEÇEMEZ → PL-17 planlayıcı hattı derinleşir; K-104 kapalı kalır.

## S2.8 — SONUÇLAR (2026-07-08)

### İş 1 — Rollout çürüme eğrisi: H_eff = 10 (kırpma uygulanmadı)
Enerji-boyutu açık-döngü hatası k=1..10 boyunca kalıcılık tabanının
altında (3/3 seed; `runs/s28_decay.json`). Ön-kayıtlı kural gereği
K-112 kırpma PASİF. **Şerh (sonradan kritik çıktı):** ölçüm on-policy
(tasarruf-ağır) dağılımda yapıldı — aşağıya bakınız.

### İş 2-3 — K-111 + nakit testi: **GEÇEMEDİ (Çatal B-PLANLAYICI)**
CEM-4 + 64 aday + yön×süre makroları (bit-eş korunum testli).
Nakit havuzlanmış: d1=%25, d2=%13, d3=%9 (çıta %70). Eval hasadı
5/5 seed'de ~0. Tur maliyeti 7.5-12.7 ms (2-4× S2.7).
İş 4 koşulmadı (nakit ön-şartı), PL-13 tetiklenmedi, K-104 ön-kayıt
gereği KAPALI kaldı.

### Mekanizma ayrıştırması (seed 4 üzerinde, iki test)
- **Test A — kayma sadakati:** kaynak 1 doğuda; RIGHT sonrası modelin
  tahmini kaynak kütlesi: MERKEZDE 0.079, ESKİ göreli konumda 0.705
  (ideal: 1 / 0). **Model hareket altında egosantrik kaymayı
  öğrenmemiş; "grid kalıcıdır" tahmini yapıyor.**
- **Test B — koşullu sıçrama:** kaymamış hayal üzerinde INTERACT →
  tahmini sıçrama +0.048 (kalibre değer ~+0.43×merkez-kütle ile tutarlı:
  merkezde kütle yok, sıçrama yok).
- **Zincir (PL-12/M-05'in uzamsal enkarnasyonu):** tasarruf-ağır veri →
  grid-kalıcılık modeli → hayalde kaynağa YAKLAŞILAMIYOR → hasat planı
  hiç kârlı görünmüyor → davranış tasarrufta → veri tasarruf-ağır.
  calibN'in bağlam-içi kalibrasyonu bu yüzden davranışa dönmüyordu:
  enjekte pencerelerde kayma GERÇEK gözlemlerden geliyordu (öğretmen
  zorlaması); planlayıcı rollout'u kaymayı KENDİ üretmek zorunda.
- Decay cihazının H_eff=10'u bu yüzden yanılttı: on-policy (statik grid)
  dağılımda kalıcılık-tarzı tahmin mükemmel görünür; planlayıcının
  kullandığı karşı-olgusal yaklaşma dizilerinde ölçülmemişti (→ M-17).

### PL-17 güncel teşhis ve seçenekler (karar Ali'de)
Darboğaz artık planlayıcı örneklemesi DEĞİL (K-111 bunu çözdü ve
yetmedi), dünya-modelinin uzamsal geçiş dinamiği:
- (a) Hareket-zengin veri: ε artışı / hareket müfredatı / PER
  tabakalamasını "grid-değişim büyüklüğü"ne genişletmek (mekanik,
  ~1-2 bit) — veri yönlü çözüm.
- (b) Kayma-eşdeğişimli (convolutional/action-conditioned) decoder —
  uzam yapısını mimariye vermek. GÜÇLÜ prior: "dünya ötelenebilir
  uzaydır" bilgisi bit olarak pahalı ve felsefi olarak tartışmalı
  (anayasa md.1 hassasiyeti). KERNEL_BUDGET tartışması gerektirir.
- (c) İkisi birden değil (M-06).
Tavsiye: önce (a) — M-05 ailesinin bilinen çözüm sınıfı, ucuz;
(b) ancak (a) ölçülü başarısız olursa ve Ali onayıyla.

### Yeni ders var mı?
VAR → **M-17**: Cihaz, kullanım dağılımında koşar. (H_eff on-policy
ölçüldü ve 10 çıktı; planlayıcı karşı-olgusal dizilerde koşuyor ve
orada model kalıcılık-tuzağındaydı. Çürüme eğrisi, planlayıcının
DEĞERLENDİRDİĞİ dizi dağılımında ölçülmeliydi.)

---

## S2.9 — ÖN-KAYIT (koşumdan önce, M-08) (2026-07-08)

### İş 1 — taban oranlar (S2.8 config, seed 0, bit-eş tekrar)
43.784 geçişte: hareket+görünür-A **1056/10K**, hareket+kayma
**1205/10K** (`runs/s29_baseline.json`). Kayma tabanı (standart
enstrüman): doğru 0.050 / eski 0.554 = **oran 0.090** (S2.8 ad-hoc
0.11'i doğruladı). **Yorum ön-kayda geçer:** kayma geçişleri nadir
DEĞİL (~%12) — birincil sorun veri kıtlığından çok GRADYAN DİKKATİ
(kayma ~2/324 boyut, λ=10 enerji baskın). K-110rev iki koldan yüklenir:
uzamsal örnekleme ağırlığı (değişim-zengin pencere ~9-33× daha sık
tekrar) + ε hareket yanlılığı (ε-içi hareket payı 0.67→0.83).
Sanity hedefi: hareket+kayma sayacı ≥ taban (düşerse müdahale ters
tepmiş); ASIL kapı aşağıda.

### İş 2 çıtası (Ali ön-kaydı): kayma medyan oranı (5 seed) **> 1**.
### İş 4 zinciri ve çatallar (aynen):
- **A:** kayma ✓ + nakit (d1 VE d2 ≥ %70) ✓ + eval (S2.7 bitti-tanımı) ✓
  → PL-13 OTOMATİK; Ali öngörüsü sınavda.
- **B-KEŞİF:** kayma ✓ + nakit ✓ + eval hasat ~0 → K104_DOSYA.md
  arşiv şerhindeki koşul gerçekleşir, dosya O veriyle yeniden açılır
  (merak lehine ilk gerçek kanıt).
- **C:** kayma ✗ (veri/dikkat-yönlü çözüm K-110rev dozunda yetmedi) VEYA
  kayma ✓ + nakit ✗ (kayma gerekli ama yetersizmiş — yeni mekanizma
  aranır) → dur, Ali'ye; M-18 gereği (b)-tipi mimari çözüm ÖNERİLMEZ;
  öz-hareket ara sonucu güçlenmiş sayılır.

---

## S2.9 — SONUÇLAR (2026-07-08): **ÇATAL C-VERİ-YETMEDİ**

| seed | kayma oranı (çıta >1, taban 0.09) | hareket+kayma /10K | nakit d1/d2 | eval hasat |
|------|-----------------------------------|--------------------|--------------|------------|
| 0 | 0.24 | 1352 | %45/%15 | 0.0 |
| 1 | 0.29 | 1331 | %20/%10 | 0.0 |
| 2 | 0.10 | 1165 | %0/%0 | 0.0 |
| 3 | 0.16 | 1029 | %30/%5 | 0.0 |
| 4 | 0.10 | 899 | %15/%5 | 0.0 |

Kayma medyan oranı **0.16** (taban 0.09'dan ~2× iyileşme, çıtanın çok
altında); nakit d1=%22, d2=%7; eval hasadı 0. Zincir ilk kapıda düştü.
Veri: `runs/s29_results.json`. Tur maliyeti 7.4-10.0 ms.

**Doz-cevap yorumu:** K-110rev dozu (uzamsal ağırlık 4, ε-hareket 0.83)
kayma öğrenimini kıpırdattı ama düzeltemedi. Taban ölçümünün ön-kayıtlı
yorumu doğrulandı: sorun veri MİKTARI değil (kayma geçişleri ~%12),
prior'suz temsilde kayma fonksiyonunun ÖRNEKLEM KARMAŞIKLIĞI: yoğun
decoder, eylem-koşullu permütasyonu hücre hücre ezberlemek zorunda
(81 konum × 4 yön × 4 kanal; örnek başına yalnız 1-2 dolu hücre
kısıt getiriyor). Ağırlık paylaşımı (evrişim) bunu çökertir — ama o
tam M-18'in yasakladığı sınıfın sınırında (aşağıda, karar Ali'de).

### Çatal C gereği: durildi; M-18 uyarınca (b)-tipi mimari çözüm
ÖNERİLMİYOR. Ali'ye giden sınır sorusu: SALT yerellik prior'ı
(eylem-koşulsuz evrişimli decoder — "uzay yereldir" bilgisi) M-18
kapsamında mı, değil mi? Eylem-koşullu kayma-eşdeğişimlilik açıkça
kapsam İÇİ (cevabı yazar); salt yerellik ise kaymayı YAZMAZ ama
öğrenilmesini örneklem-karmaşıklığı yönünden mümkün kılar. Bu bir
anayasa yorumu (md.1) — benim kararım değil.

### Yeni ders var mı?
YOK. (Sprint, M-14/M-17/M-08 disiplinlerinin uygulamasıydı; yeni
metodolojik ders çıkmadı — kural gereği beyan.)

---

## S2.10 — ÖN-KAYIT (koşumdan önce, M-08) (2026-07-08)
Tek-ajan mühendisliğinin SON sprinti (Ali). PL-18 kararı: salt-yerellik
prior'ı (eylem-koşulsuz evrişimli decoder, K-113) M-19 kapısından
geçmek şartıyla izinli.

### İş 1 — M-19 doğum günü testi
Evrişimli-decoder ajan, INIT ağırlıklarıyla kayma testi. **Oran > 1
çıkarsa prior geri çekilir**, FINDINGS'e "evrişim M-19'dan geçemedi"
girer, DUR. Operasyonalizasyon (ölçümden önce): trials_per=20 (240
ölçüm), dense-init referans oranı da raporlanır (gürültü bağlamı);
kural conv-init oranına harfiyen uygulanır.

### İş 4 zinciri: kayma (medyan oran > 1) → nakit (d1 VE d2 ≥ %70) →
tam eval (S2.7 bitti-tanımı) → PL-13.

### İş 5 çatalları (aynen):
- **A:** zincir tamam → PL-13, P1 tekrarı. P1 pozitifse etiket ŞERHLİ:
  "yerellik-iskelesi üstünde kazanılmış öz-hareket" (iskele defterde,
  iddia dürüst).
- **B:** kayma >1 ama nakit/eval çökük → planlayıcı katmanı; K-112
  karşı-olgusal dağılımda yeniden ölçülür.
- **C:** kayma ≤1 → DP-05 çerçeve kararı Ali'ye gider; yeni müdahale
  önerisi GELMEZ (vade doldu).

## S2.10 — SONUÇLAR, ZİNCİR 1 (2026-07-08)

### M-19 doğum günü testi: GEÇTİ
Conv-init kayma oranı 0.0 (720 ölçüm; dense-init referansı da 0.0) —
prior yetiyi hediye etmiyor (`runs/s210_m19_birthday.json`).

### Zincir 1: kayma katmanı ÇÖZÜLDÜ, nakit harfe göre düştü → ÇATAL B
| seed | kayma (doğru/eski kütle) | nakit d1/d2/d3 | eval hasat | yaşam | kalib |
|------|--------------------------|-----------------|------------|-------|-------|
| 0 | 1.000/0.000 | %5/%5/%0 | 0.0 | 134 | −0.022 |
| 1 | 1.000/0.000 | %85/%50/%45 | 0.0 | 142 | +0.103 |
| 2 | 1.000/0.000 | %95/%80/%50 | 0.0 | 136 | +0.239 |
| 3 | 1.000/0.000 | %90/%90/%75 | **4.0** | 162 | +0.233 |
| 4 | 0.956/0.002 | %95/%60/%35 | 0.0 | 142 | +0.181 |

- **Kayma: 5/5 seed'de ~mükemmel** (taban 0.09'a karşı doygun oran;
  rapordaki 1e9 sıfıra-bölüm koruması artefaktı — kütleler esas).
  Yerellik iskelesi, eylem-koşulsuz decoder'a rağmen kaymayı hidden
  üzerinden ÖĞRETTİ: eylem→kayma eşlemesi kazanılmış (iskele defterde,
  K-113; iddia dili çatal-A şerhine tabi).
- **Nakit: d1=%74 ✓, d2=%57 ✗** (çıta %70/%70) → harfe göre düştü;
  S2.9'a göre d1 %22→%74. **Seed 3 tarihte ilk: eval medyan hasat 4.0
  (eşik 3 üstü)**, yaşam 162 vs 167 (p=0.68, anlamlı değil).
- Aykırı: seed 0 (kalibrasyon −0.02 — enerji olumsallığı hiç oluşmamış;
  kayma mükemmelken enerji kafası çökük; conv'un enerji başı ayrı ve
  seed'e hassas görünüyor).
- Maliyet: 36-44 ms/tur (conv × 64 aday × CEM-4 × ufuk-10).
- Ön-kayıtlı çatal: **B-PLANLAYICI → K-112 karşı-olgusal dağılımda
  yeniden ölçülüyor** (M-17-uyumlu enstrüman `counterfactual_decay`;
  ağırlıklar artık kaydediliyor — salt-planlama değişiklikleri
  yeniden-eğitimsiz test edilecek).

### Zincir 1 sonrası — K-112 karşı-olgusal yeniden ölçümü (Çatal B gereği)
`counterfactual_decay` (yaklaşma+INTERACT dizileri, M-17-uyumlu):
**H_eff_cf = 10 (3/3 seed)** → ön-kayıtlı kural gereği kırpma YİNE
endike değil (`runs/s210_decay_cf.json`). AMA cihaz notu: kalıcılık
tabanı sıçrama adımında patlıyor (~0.40) — model sıçramanın yalnız bir
kısmını tahmin ederek kapıyı geçiyor. Mutlak hata: model hasat
sıçramasının %25-75'ini kaçırıyor (seed 1: ~%70 eksik; seed 2-3: ~%25).
Kalan nakit açığının (d2=%57) muhtemel yeri burası: J farkı, eksik
tahmin edilen sıçrama + CEM gürültüsüyle seyreliyor. Vade dolduğu için
yeni müdahale önerilmiyor (Ali talimatı).

### S2.10 / tek-ajan mühendisliği KAPANIŞI
Zincir sonucu: kayma ✓✓ (çözüldü), nakit ✗ (d1 ✓ %74, d2 ✗ %57),
eval ✗ (5 seed'in 1'i eşik üstü). PL-13 tetiklenmedi. Baskın kalan
fenomen SEED VARYANSI: seed 3 neredeyse tam geçer (nakit 90/90/75,
eval hasat 4.0), seed 0 enerji kalibrasyonunu hiç kuramaz (−0.02).
Mimari "eşikte": bitti-tanımının TÜM-seed şartı bu varyansta düşüyor.
Ağırlıklar `runs/s210_weights/` (seed 1-3) — sonraki her analiz
yeniden-eğitimsiz.

### Yeni ders var mı?
VAR → **M-20**: Taban çizgisi de cihazın parçasıdır. Kolay taban
(kalıcılık, olay anlarında kördür) kapıyı otomatik açar; H_eff kuralı
sıçrama adımlarında BOŞUNA sağlandı. Taban, ölçülen yetinin zorluk
düzeyinde seçilmeli (örn. olay-bilinçli taban veya mutlak-hata eşiği).

## S2.10-ek — ÖN-KAYIT (2026-07-08)
PL-13 / P1-tekrar, YALNIZ seed 3. **n=1 → azami etiket ADAY GÖZLEM**
(Ali ön-kaydı). Üç kontrol standart (ikiz ×3, etiket karıştırma,
checkpoint eğrisi). Checkpoint verisi için seed-3 eğitiminin bit-eş
enstrümanlı yeniden-yürütmesi yapılır; final ağırlık hash'i kayıtlı
`runs/s210_weights/seed3.pt` hash'ine EŞİT olmak zorunda (Kapı-5 kanıtı;
eşit değilse tüm ek geçersiz). Çıktı: kayma + hasat + öz-konum probu
ortak zaman ekseni (checkpoint bazlı). PL-15 son-itiraz analizi
(varyans-eşleşmiş görünür-A kontrolü) aynı ağırlıklarda tekrarlanır —
mobil-ajan kilidi seed 3'te açıldı. Ali'nin PL-13 öngörüsü sınavda:
"öz-konum eğrisi hasatla birlikte yükselir."

## S2.10-ek — SONUÇLAR (n=1 seed 3; azami etiket ADAY GÖZLEM) (2026-07-08)

**Bit-eş kanıt:** yeniden-yürütme final hash'i == kayıtlı seed3.pt
(e0577e36…) — checkpoint verisi AYNI eğitimin verisi (Kapı-5).

### Ortak zaman ekseni (kayma × hasat × öz-konum probu)
| ckpt | kayma kütlesi (üretici) | eval hasat | disp R² (prob) | disp Δ(eğitilmiş−ikiz) |
|------|--------------------------|------------|----------------|--------------------------|
| 0 | 0.000 | 0.0 | +0.18 | −0.03 |
| 5K | 0.015 | 0.0 | −3.26 | −0.21 |
| 15K | 0.145 | 0.0 | −6.72 | +0.40 |
| 25K | 0.457 | 0.0 | −4.21 | +0.11 |
| 35K | 0.749 | **2.0** | −2.90 | −0.39 |
| 45K | 1.000 | **3.0** | −3.94 | +0.25 |

### PL-13 öngörü verdikti (Ali: "öz-konum eğrisi hasatla yükselir")
**İki katmanda iki farklı cevap:**
- **ÜRETİCİ okumada DESTEKLENDİ:** modelin öz-hareket yetisi (kayma
  kütlesi) monoton yükseldi ve hasat davranışı ancak ~0.75 eşiğinden
  SONRA doğdu (0,0,0,0,2,3). Sıralama tam Vygotsky-öncesi beklenen yönde:
  önce içsel model yetkinliği, sonra davranış.
- **KORELASYONEL okumada DESTEKLENMEDİ:** disp probu (hidden'dan
  kümülatif yer değiştirme) yükselmedi (eğri düzensiz-negatif, ρ=−0.31;
  final ΔR²=+0.253, p=0.047 — n=6 epizotta marjinal, mutlak R² hâlâ
  derin negatif).
- **Ayrım dersi:** TEK-ADIM öz-hareket modeli (kayma) ≠ KÜMÜLATİF yol
  entegrasyonu (displacement). İlki kazanıldı ve davranışı açtı; ikincisi
  hâlâ yok (ya da lineer okunmuyor). Öngörü, "temsil"i hangi katmanda
  tanımladığına göre doğru YA DA test-başarısız — n=1, etiket ADAY
  GÖZLEM; çoğaltma (≥5 seed) S3 sonrası aday iş.
- denergy ilk kez pozitifleşti (final R² 0.17, Δ +0.167, p=0.016) —
  hareketli ajanda sonraki-tur enerji kısmen öngörülür oldu; prob
  erken-ckpt'lerde kararsız (sabit-hedef patolojisi), ihtiyatla.

### PL-15 SON-İTİRAZ SONUÇLANDI: itiraz AYAKTA — öz-enerji adayı DÜŞTÜ
Mobil ajanda varyans-eşleşmiş kontrol nihayet koşulabilir oldu:
Δ(enerji) = **+0.033**, Δ(görünür-A sayısı) = **+0.062** — kendilikle
ilgisi olmayan girdi özelliği EN AZ AYNI ölçüde iyileşmiş. "Eğitilmiş
GRU tüm girdilerini ikizden iyi temsil eder" H0'ı doğrulandı.
**Öz-enerji gözlemi öz-model kanıtı olmaktan ÇIKARILDI** — genel
girdi-iyileştirmesinin bir örneği olarak yeniden sınıflandı. Ali'nin
iddia merdiveni (M-13) tasarlandığı gibi çalıştı: aday, dördüncü
itiraz testinde öldü. (P1/H1'in interoseptif yarısı için nihai durum:
NEGATİF-genel; üretici katmandaki kayma bulgusu bundan bağımsız ayakta.)

## S3-AÇILIŞ (2026-07-08)

### İş 1 — B-kaynağı kalibrasyonu (M-01 refleksi): economy v3
İki-ajanlı Tanrı-gözlü koordinasyon oracle'ı, v2 koşulları
(`runs/s3_b_oracle.json`):

| B enerji | kişi başı | medyan çift-yaşam | medyan açılış |
|----------|-----------|--------------------|----------------|
| 75 (v2) | 37.5 | 309 | 10 |
| 135 | 67.5 | 1500 (tavan) | 62 |
| 180 | 90 | 1500 (tavan) | 62 |
| 225-270 | 112-135 | 1500 (tavan) | 62 |

> ### ⚠ YENİDEN ÜRETİLEBİLİRLİK ŞERHİ (2026-07-27) — KAPI 5 AÇIK
>
> **`runs/s3_b_oracle.json`'ı üreten kod repoda YOK.** `res_b`'ye
> dokunan tek Python: `world/grid.py`, testler, `replay/`.
> `training/oracle.py` yalnız A kanalına (`obs[0]`) bakar, koordinasyon
> mantığı içermez ve docstring'i açıkça *"Dünya durumuna Tanrı-gözü
> erişimi YOK"* der — oysa bu bölüm onu *"İki-ajanlı Tanrı-gözlü
> koordinasyon oracle'ı"* diye tanımlıyor. Çelişki çözülmemiştir.
>
> Sonuç: `world/config.py`'ye M-10 damgasıyla yazılmış dünya-tarafı bir
> değer (`resource_b_energy=180`, economy v3) ÖKSÜZ bir sonuç dosyasına
> dayanıyor. KAPI 5 (bit-eş tekrar) ve M-12 arşiv geleneği ihlali.
> Ayrıca tablodaki 135+ satırlarının hepsi 1500-tur TAVANINDA (sansürlü
> veri) — eşiğin "keskin 135" okuması bu sansürle sınırlıdır.
> Açık iş: **PL-24**.

**Bulgu: v2'de B primi BOZUKTU** (A=45 > kişi başı 37.5) — S2.6 ekonomi
kalibrasyonu A'yı düzeltirken B'yi kırmıştı; oracle yakaladı (M-01 ne
içinmiş). Sürdürülebilirlik eşiği keskin: 135. **Seçim: B=180** —
anayasal 4-6× bandının içi (4×A); en-sıkı-geçen 135 ile band çelişkisi
beyanlı, Ali isterse tek satır. economy_version=3 damgalı; v1/v2
tanımları `economy_v1()/economy_v2()` olarak korunuyor.

### İş 2 — Nüfus + soy kütüğü: DP-01 FİİLİ KARAR
Kurucu kadro: roster (doküman 4.3) aynen; **A2 slotu seed-3
transplantı** (kanal-açık mimariye SIFIR-NÖTR genişletme — sinyalsiz
girdide eski modele sayısal özdeşlik testli:
`test_transplant_neutral_extension_equivalence`) **+ mutasyon σ=0.01**;
diğer 4 slot mimari uyumsuzluğundan taze (KISMİ miras, PL-20).
Ölümde halef = ölenin ağırlıkları + mutasyon → **DP-01 seçenek (b)
"çekirdek+miras" fiilen yürürlükte** (Ali talimatı; A/B testi yapılmadı,
S5'te veriyle sınanabilir). Soy kütüğü her koşumun `breath.json`'ında.

### İş 3 — Kanal AÇIK (spec 4.2 yürürlükte)
4 bit/16 sembol + yok; enerji maliyeti 0.5 (homeostaz); menzil 8
(PL-21); alınan sinyaller kimliksiz 16-boyut; kendi sinyali efferens
(K-114). Sinyal seçimi eylemle ORTAK MPC planlamasında — ödül yok,
şekillendirme yok; anlam çıkacaksa kullanım basıncından çıkacak.
probes/ sosyal katmanı KAPALI — önce ekoloji nefes alsın.

### İlk nefes koşumu (20K tur, 5 ajan, ölüm gerçek): **DRİFT-BASKIN ÇÖKÜŞ**

> ### ⚠ ENSTRÜMAN ŞERHİ (2026-07-27) — AŞAĞIDAKİ İKİ SAYI ÇÜRÜTÜLDÜ
>
> M-12 gereği orijinal metin OLDUĞU GİBİ korunmuştur; düzeltme burada.
>
> **Kusur:** `a_harvests`, `b_openings`, `signals_sent` sayaçları
> `Citizen` NESNESİNDE yaşıyordu ve `Citizen` ölümde DEĞİŞTİRİLİYORDU
> (`training/ecology.py`). Rapor edilen değer = o anki 5 sakinin
> YAŞAM-İÇİ sayacı; kümülatif toplam DEĞİL. `signal_rate` ise bu
> resetlenen payı KÜMÜLATİF paydaya (`5*turn`) bölüyordu → yapay
> monoton düşüş.
>
> **İlk kanıt ham veride:** `a_harvests` serisi
> `[1,0,0,0,0,1,0,0,1,1,0,...]` — kümülatif bir sayaç azalamaz.
>
> **Düzeltilmiş muhasebeyle ölçüm** (aynı seed, dinamik bit-eş; yalnız
> sayaç düzeltildi; 2000 tur):
>
> | metrik | RAPOR EDİLEN | GERÇEK |
> |---|---|---|
> | A-hasat | 0 | **17** |
> | sinyal oranı | 0.006 | **0.551** |
>
> Ve sinyal oranı DÜŞMÜYOR, YÜKSELİYOR: doğum penceresine göre
> 0.367 → 0.481 → 0.681 → 0.695.
>
> **ÇÜRÜTÜLEN CÜMLE:** *"sinyal oranı 0.003→0.0 (sinyaller söndü —
> maliyet var, fayda yok: MPC tutumlu adayları seçiyor)"* — tam tersi.
> **ÇÜRÜTÜLEN SAYI:** *"A-hasat toplam ~2"* — toplam değil, anlık.
>
> **Yerine geçen ölçüm** (1500 tur, sinyal kaynağı ayrıştırması):
> ε-keşif dalı %10.1 → oran 0.925 (= havuz geometrisi 16/17);
> MPC dalı %89.9 → oran **0.456**. MPC sinyalden kısmen kaçınıyor ama
> sistematik tutumluluk YOK. Slot bazında kurucu nesil → tüm nüfus:
> A1 0.097→0.085, A3 0.142→0.393, A4 0.150→0.328,
> **A2 (seed-3 mirası) 0.261→0.765**.
> **MEKANİZMA — H0 sınavından geçirildi (M-13).** İlk okumam
> ("kurucu nesil tutumlu, yetkinlik eridikçe sinyal artıyor")
> korelasyoneldi; H0 olarak "argmax-beraberlik kazası" sınandı
> (taze çekirdek dejenere skor üretir → argmax havuzun İLK 6 satırına,
> yani sabit-eylem/sinyalsiz satırlara düşer). Doğrudan ölçüm
> (60 durum × 3 slot × 4 mutasyon dozu, `_score_joint` üzerinde):
>
> | slot | σ=0 | σ=0.01 | σ=0.05 | **σ=0.16** |
> |---|---|---|---|---|
> | A1 sabit-eylem satırı seçimi | %100 | %100 | %100 | **%8** |
> | A1 sinyal oranı | %0 | %0 | %0 | **%90** |
> | A3 sabit-eylem satırı seçimi | %100 | %100 | %100 | **%30** |
> | A3 sinyal oranı | %0 | %0 | %0 | **%68** |
> | skor yayılımı (A1) | 0.61 | 0.68 | 2.08 | **23.3** |
>
> **H0 (beraberlik kazası) DÜŞTÜ:** skorlar init'te dejenere değil
> (yayılım 0.6–1.05). Sabit-eylem satırları σ=0'da J'yi GERÇEKTEN
> kazanıyor — tutarlı bir model STAY'in enerji koruduğunu tahmin ediyor.
> **Ayakta kalan mekanizma:** σ=0.16'da (= 250. nesildeki kümülatif
> sürüklenme, tam koşumun ulaştığı yer) skor manzarası gürültüye boğulur,
> sabit-eylem satırları kaybeder ve argmax havuzun aday geometrisine
> (16/17 sinyalli) düşer.
>
> **Düzeltme:** "kurucu nesil tutumlu" fazla genel — TAZE A2 sinyal-delisi
> (%100), taze A1/A3 tutumlu (%0); mimariye bağlı. Ekolojideki A2 gen-0
> değeri (0.261) taze değil, EĞİTİLMİŞ seed-3 transplantıdır.
>
> **Savunulabilir ifade:** sinyal yayımı, TUTARLILIĞINI kaybetmiş bir
> planlayıcının varsayılan davranışıdır. Tutumluluk model tutarlılığı
> ister; tutarlılık iki yoldan kaybolur (eğitimsiz başlangıç — mimariye
> bağlı; ve birikimli mutasyon — evrensel, ~250. nesilde). Yani sinyal
> oranı şu an bir iletişim basıncı ölçüsü DEĞİL, **planlayıcı
> tutarlılığının ters vekilidir** — sosyal katman (probes/) açılmadan
> önce kapatılması zorunlu konfound: yükselen sinyal oranı "iletişim
> doğuyor" diye okunursa doğrudan sahte pozitif olur.
>
> **AYAKTA KALAN:** ölüm sayısı (1513) ve ömür istatistiği soy
> kütüğünden geliyordu, sağlam — slot medyanları 53/53/58/58/66,
> nüfus medyanı **56 tur**. Bu, "her tur hareket" tavanına
> (100/(0.6+1.0)=62.5) oturuyor: ajanlar tasarruf etmiyor, sürekli
> hareket ediyor. Drift-baskın çöküş teşhisi AYAKTA; mekanizma daha
> keskin.
>
> **Onarım:** `Ledger` (ölümden sağ çıkan kümülatif defter) + pencere
> oranları + M-23 bilinen-pozitif testleri
> (`tests/test_s3.py::test_vitals_counters_are_cumulative`); test eski
> cihazda DÜŞTÜĞÜ doğrulandı. Ayrıca halef doğum yeri `succ_rng`'den
> `World.respawn_entity()`'ye taşındı (anayasa: dünya rastgeleliği tek
> generator'dan) → **v2 koşumu yeniden analiz değil, YENİ koşumdur**:
> `runs/s3_breath_v2/`. Ders: M-22, M-23.

`runs/s3_breath/breath.json` (bit-eş determinizm testli):
- **1513 ölüm / 20K tur**; slot medyan ömürleri 53-66 tur; 254-357
  nesil. A-hasat toplam ~2, B-açılış 0, sinyal oranı 0.003→0.0
  (**sinyaller söndü** — maliyet var, fayda yok: MPC tutumlu adayları
  seçiyor; dürüst mekanizma, sansür değil).
- **Tek zayıf miras sinyali:** A2 (seed-3 soyağacı) medyan ömrü 66 vs
  diğerleri 53-58 — küçük ama görünür devralınmış avantaj; 254 nesil
  sonunda hâlâ fark edilir olması ilginç.
- **Teşhis:** ekoloji öğrenme BİRİKTİREMİYOR. İki mekanizma:
  (1) yaşam-içi öğrenme bütçesi: yetkinlik ~45K tur sürekli öğrenme
  istiyordu (S2 yayı ölçtü); ömür ~60 tur → ~750× açık. (2) halefiyet
  SEÇİLİMSİZ mutasyon = ağırlık uzayında rastgele yürüyüş; 250+ nesil
  × σ=0.01 → birikimli gürültü σ≈0.16, miras aşınıyor (drift, evrim
  değil — seçilim basıncı YOK çünkü herkes aynı hızda ölüyor).
- Bu, PL-06 geriliminin ("ölüm gerçek" vs "yetiştirme kabı") ekolojik
  ölçekte patlaması: v1 ideali (saf online + gerçek ölüm) bu
  parametrelerde matematiksel olarak öğrenemez.
- **Çerçeve seçenekleri (karar Ali'de; hepsi anayasa-dokunuşlu):**
  (a) seçilimli halefiyet (uzun yaşayanın soyu çoğalır — evrim gerçek
  olur; DP-01'in B'sine doğal ek), (b) gelişim koruması / yuva dönemi
  (genç ajana geçici metabolizma indirimi — öğrenme penceresi açar;
  dünya-tarafı, M-01 için yeni oracle ister), (c) 5×seed-3 klon tabanı
  (roster'ı ertele, PL-20 alternatifi — ekoloji yetkin tabandan başlar,
  sosyal katman üstüne oturabilir). Tavsiye: önce (c)+(b) — yetkin taban
  + yaşanabilir pencere; seçilim (a) ayrı değişken, sonra (M-06 tek tek).
  Not: her üçü de nüfus için AYRI fizibilite oracle'ı gerektirir
  (M-21) — tek-ajan kalibrasyonu çok-ajanda geçersiz.

### S3 TABAN ÇİZGİSİ v2 — düzeltilmiş enstrümanla 20K koşum (2026-07-27)

`runs/s3_breath_v2/breath.json`. **Yeniden analiz DEĞİL, yeni koşum:**
halef doğum yeri `succ_rng` → `World.respawn_entity()` taşındığı için
yörünge v1'den farklı (PL-23). Enstrümanlar: `Ledger` kümülatif defteri
+ `world.b_openings_total`; M-23 testleriyle sabitlendi.

| | v1 (bozuk cihaz) | **v2 (düzeltilmiş)** |
|---|---|---|
| ajan-turu | — | 100.000 |
| ölüm / medyan ömür | 1513 / 56 | **1714 / 52** |
| A-hasat | "~2" (anlık) | **79** (7.9 / 10K ajan-turu) |
| B-açılış | 0 (geri-çıkarım) | **0** (dünya sayacı, kesin) |
| sinyal oranı | 0.003→0.0 "söndü" | **0.681** |

**Sinyal oranı seyri (pencere, 1000'lik dilim):** 0.429 → 0.845 (t=4K)
→ 0.74 → 0.60 → 0.71 → 0.64. Yükselip ~0.6-0.75 bandında **plato**
yapıyor. Sönme YOK; v1'in "söndü" okuması tümüyle enstrüman kusuruydu.

**Kanal yapı taşımıyor — nicel tavan (asıl bulgu).** 68.089 sinyalin
sembol dağılımı:

| ölçü | değer |
|---|---|
| chi-kare (df=15) | 928.7, **p = 2.5e-188** |
| Shannon entropisi | **3.9897 bit** (tekdüze tavan 4.0000) |
| tekdüzeden sapma | **0.0103 bit** = kanal kapasitesinin %0.26'sı |
| CV | 0.117 |

Anlamlılık ezici (n=68K her sapmayı anlamlı yapar) ama etki 4 bitin
yüzde biri kadar bile değil — **PL-15'i öldüren ayrımın aynısı**
(anlamlılık ≠ etki). Sapmanın kendisi de büyük olasılıkla ajan-içi
argmax yanlılığı (ağırlık gürültüsünün bazı sembolleri kayırması),
ajanlar-arası yapı değil.

**Bu, sosyal katman için ÖN-KAYITLI GÜRÜLTÜ TABANIDIR:** `probes/`
açıldığında herhangi bir karşılıklı-bilgi / sembol-anlam iddiası bu
0.0103 bitlik tabanı aşmak ZORUNDA. Aşmayan her sonuç, kanalın
rastgele kullanımıyla açıklanır.

**Ekolojik özet (v1 teşhisi AYAKTA, mekanizma keskinleşti):** medyan
ömür 52 tur ≈ "her tur hareket" tavanı (62.5) — ajanlar tasarruf
etmiyor; öğrenme ufku ~45K tur, ömür 52 → **~865× açık**; miras 65.
nesilde gürültüye gömülüyor (σ=0.01 vs ağırlık RMS 0.0804); A-hasat
7.9/10K ajan-turu ile birikiyor ama davranışa dönüşmüyor.
**Drift-baskın çöküş teşhisi doğrulandı; "kanal maliyet baskısıyla
söndü" alt-teşhisi ise düştü.**

## S3-B — ÖN-KAYIT (koşumdan önce, M-08) (2026-07-27)

**Amaç:** PL-24'ü (KAPI 5: economy v3 yeniden üretilemez) kapatmak ve
PL-25'i (keşfedilebilirlik hiç ölçülmedi) yanıtlamak. Enstrüman:
`training/b_oracle.py` — ajan değil ölçüm aleti, KERNEL_BUDGET'a bit
yazmaz (`training/oracle.py` emsali).

**Merdiven (M-06, tek değişken = B stratejisi):** `random` (şans tabanı)
→ `noB` (hayatta-kalma kontrolü, B kovalamaz) → `vision` (gördüğü B'ye
git+bekle, kanal YOK) → `signal` (+kanal) → `god` (Tanrı-gözü minimax
randevu = koordinasyon tavanı).

**BEYAN — L2'ye hediye:** `signal` seviyesi SYM_B konvansiyonunu
(hangi sembolün "burada B var" demek olduğunu) HAZIR alır. Bu, ajanın
KEŞFETMESİ gereken şeydir (H3/H4'ün konusu). Bilinçli: L2, **mükemmel
paylaşılan konvansiyon altındaki TAVANI** ölçer. L2 bile öğrenilebilir
hızda açılış üretemiyorsa, öğrenilmiş hiçbir dil üretemez — o zaman
eksik olan ajan değil DÜNYA KALİBRASYONUDUR.

**Kanal fiziği kısıtı (PL-21b/c, ölçümün kalbi):** sinyal YÖN ve KİMLİK
taşımaz. Duyan sinyale doğru yürüyemez; aldığı tek bilgi "Chebyshev 8
içinde biri var", yani arama uzayı 4096 → 17×17=289 hücreye daralır
(~14×). L2 bu daralmanın nakit değerini ölçer.

### Cihaz doğrulaması (koşumlardan ÖNCE yapıldı — M-15)
1. Referans `training/oracle.py` aynı ekonomide (m=0.6/24/A=45) yeniden
   koşuldu: medyan ömür **215** (S2.6 raporu 197), hasat **10.5**
   (rapor 8.5) → referans yeniden üretilebilir ✓
2. `pair_lifetime` = min(iki ömür) = koordinasyon penceresi. Referans
   dağılımdan min(X1,X2) medyanı **124** öngörülür; `noB` kontrolü
   **110** ölçtü ✓ (tek-ajan ömrüyle KARŞILAŞTIRILAMAZ — ilk okumamda
   bu hatayı yaptım, kayda geçiyor).

### DÜRÜSTLÜK ŞERHİ — merdiven ön-kayıtlı DEĞİL
Keşfedilebilirlik merdiveni cihaz geliştirilirken (politika hatası
ayıklanırken) 12 epizotluk hâliyle KOŞULDU ve `vision`/`signal`
seviyelerinde 0 açılış görüldü. Bu sayılar ön-kayıt DEĞİLDİR; öyleymiş
gibi raporlanmayacak. Kriterler aşağıda yine de yazılıyor çünkü
bağımsız büyüklüklerden türetiliyor (162 = S2.10 yetkin ajan ömrü;
2× = konvansiyonel etki eşiği), gözlenen veriden değil. **`calib`
aşaması hiç koşulmadı — o gerçek ön-kayıttır.**

### PL-24 kriteri (sürdürülebilirlik)
L3 (`god`) × B ∈ {75,135,180,225,270} × 12 epizot, tavan 3000 tur
(v1 1500'de sansürlüydü; sansür oranı raporlanacak). Kapanış: eşiğin
yeri sansürle birlikte raporlanır. **Yeniden üretilen eşik 135 DEĞİLSE**
`world/config.py`'deki B=180 gerekçesi M-10 damgasıyla revize edilir.

### PL-25 çıtaları (ön-kayıt)
- **ZAYIF — "kanalın ölçülebilir değeri var":** L2 açılış hızı ≥ 2× L1.
- **GÜÇLÜ — "basınç öğrenilebilir":** L2 hızı ≥ **6.2 açılış / 1000
  çift-turu** (= 1 olay / 162 çift-turu; 162 = S2.10'un yetkin ajan
  ömrü). Gerekçe: bir ajan hayatı içinde en az bir B deneyimi olmadan
  olumsallık öğrenilemez (S2.7 N*=50 dersi).

### Sonuç matrisi (koşumdan önce yazıldı)
- **A — güçlü ✓:** B basıncı mevcut config'de VAR; PL-22 çerçeve kararı
  basınç varsayımıyla alınabilir.
- **B — zayıf ✓, güçlü ✗:** kanal işe yarıyor ama doz yetersiz →
  `calib` aşaması B yoğunluğu/menzil için sayı üretir; PL-22'den önce
  dünya ayarı gerekir.
- **C — zayıf ✗ (L1≈L2≈0):** mükemmel konvansiyonla bile koordinasyon
  BULUNAMIYOR → öğrenilmiş hiçbir dil bulamaz. S3'ün merkezi basıncı
  YOK ilan edilir; `calib` zorunlu, PL-22 kararı basınç doğana kadar
  askıya alınır.

## S3-C — ÖN-KAYIT (koşumdan önce, M-08) (2026-07-27)

**Ali kararı: (A) — görevi değiştir.** PL-25 ölçtü ki yönsüz/kimliksiz
4 bit UZAMSAL randevuya hiçbir şey katmıyor. (A): koordinasyonun zor
kısmı uzamsal olmasın. Uygulama spec'ten SAPMA DEĞİL, spec'in ertelenmiş
yarısıdır: `event_visibility_split` ("her ajana olayın farklı parçası")
+ PL-05'te S3–S4'e ertelenen `world/events.py`.

**Ekolojik emsal:** alarm çağrısı. Vervet sembolü "yırtıcı nerede"
değil "hangi kaçış eylemi" der — kategorik, uzamsal değil.

### Fizik (ödül YOK; yalnız enerji)
Küresel olay; aktifken güvenli olan TEK eylem kutup `p ∈ {0..K-1}`,
başka her eylem `event_penalty` yakar. Konumun rolü YOK.

### İki tasarım kilidi (tasarım sırasında ölçülerek kondu)
1. **`event_duration=1`** — olay, "acıyı çek sonra düzelt"e vakit
   bırakmamalı. İlk taslakta (3 tur) kendi-kendine-çıkarım değerin
   ~%67'sini kurtarıyordu; o tasarımda kanal GEREKSİZ olurdu.
2. **İpucu bölünmesi** — kutup `log2(K)=2` bitlik bir kod; her ajan
   olay başına YALNIZ BİR biti gözler (hangisi her olayda dünya
   rng'sinden çekilir, sabit rol değil). Kendi biti K=4'ü 2 adaya
   indirir; kalanı ancak BAŞKASININ bitinden gelir. Kanal "yardımcı"
   değil, bilginin tek yoludur.

### Merdiven (M-06, tek değişken = kutup bilgisi)
`none` (olaysız çıpa) → `deaf` (bilgi yok, sabit STAY, 1/K) →
`own` (kendi biti, 1/2) → `own_infer` (+acıdan öğrenme; kilit-1 sınavı)
→ `told` (kendi biti + menzildeki ortağın biti) → `god` (tavan).

**BEYAN (M-09):** tüm kollara olayın NE ZAMAN aktif olduğu verilir
(tek değişken HANGİ eylem olsun diye). `told` ayrıca sembol→bit
konvansiyonunu HEDİYE alır (B oracle'ının SYM_B geleneği) → bu kol
öğrenilmiş bir dilin ULAŞABİLECEĞİ TAVANI ölçer, tipik başarımını değil.

### Çıtalar (koşumdan ÖNCE yazıldı)
Ölçü: medyan pencere (ilk ölüme kadar) ve olay isabet oranı.
- **(i) DEĞER:** `god` / `deaf` medyan pencere oranı **≥ 1.5**.
  Sağlanmazsa bilgi değersiz → görev yanlış kalibre, DUR.
- **(ii) KANAL GEREKLİ:** `own` tek başına değerin çoğunu almamalı —
  `(own − deaf) / (god − deaf) ≤ 0.6`. Ayrıca kilit-1 sınavı:
  `own_infer ≈ own` (fark ≤ %10) olmalı; değilse süre kilidi tutmuyor.
- **(iii) KANAL YETERLİ:** `(told − deaf) / (god − deaf) ≥ 0.5`.

### Sonuç matrisi (koşumdan önce)
- **A — üçü de ✓:** görev geçerli bir dil tuzağı; S3-C ekolojiye
  bağlanabilir (gözlem kodlaması PL-27 kararı).
- **B — (i) ✓, (iii) ✗:** bilgi değerli ama kanal ulaştıramıyor →
  menzil/nüfus kalibrasyonu (süpürme raporda); B görevinin
  ÇATAL C'sinin tekrarı olup olmadığı buradan anlaşılır.
- **C — (ii) ✗:** ajan bilgiyi zaten tek başına alıyor → kanal
  gereksiz, tuzak boş. Tasarım kilidi yetmemiş demektir; DUR ve
  kilitleri yeniden ölç (K veya süre).
- **D — (i) ✗:** DUR, ekonomi kalibrasyonu.

## S3-C — SONUÇLAR: **ÇATAL A** (2026-07-27)

`runs/s3c_event_oracle.json`, 48 epizot/kol. Birincil ölçü **kişi-başı
ömür** (M-24: "pencere = min(n ömür)" n büyüdükçe tüm farkları
sıkıştırır, değer ölçüsü olarak geçersiz — ilk okumada bu tuzağa
düştüm, düzeltildi).

### Merdiven (n=5, menzil 32)
| kol | kişi-başı ömür | olay isabeti | beklenen |
|---|---|---|---|
| `none` (olaysız çıpa) | 210 | — | ref. oracle 215 ✓ |
| `deaf` | 115 | 0.271 | 1/K=0.25 ✓ |
| `own` | 142 | 0.467 | 1/2=0.50 ✓ |
| `own_infer` | **142** | **0.467** | = `own` (kilit-1) ✓ |
| `told` | **193** | **0.856** | — |
| `god` (tavan) | 225 | 1.000 | — |

### Ön-kayıtlı çıtalar
| çıta | değer | sonuç |
|---|---|---|
| (i) DEĞER `god/deaf` ≥ 1.5 | **1.96** | ✓ GEÇTİ |
| (ii) GEREKLİ `(own−deaf)/(god−deaf)` ≤ 0.6 | **0.241** | ✓ GEÇTİ |
| (ii-b) kilit-1: `own_infer` = `own` | **birebir eşit** | ✓ GEÇTİ |
| (iii) YETERLİ `(told−deaf)/(god−deaf)` ≥ 0.5 | **0.709** | ✓ GEÇTİ |

→ **ÇATAL A: görev geçerli bir dil tuzağıdır.**

- Olaylar ömrü yarıya indiriyor (210 → 115): basınç gerçek ve güçlü.
- Kendi ipucu değerin yalnız **%24**'ünü kurtarıyor; kalan %76 ancak
  BAŞKASININ bitinden gelebilir → kanal yardımcı değil, tek yol.
- `own_infer` ile `own` BİREBİR eşit: tek turluk olay "acıyı çek,
  sonra düzelt" kaçış yolunu kapatıyor (kilit-1 ampirik olarak
  doğrulandı).
- Mükemmel konvansiyonlu yayın değerin **%71**'ini, isabet açığının
  **%80**'ini kurtarıyor.

### Menzil kalibrasyonu (n=5) — B görevinin TAM TERSİ
| menzil | kapsama | told ömür | isabet | yeterlilik |
|---|---|---|---|---|
| 8 (mevcut) | %7 | 140 | 0.534 | 0.223 |
| 12 | %15 | 142 | 0.578 | 0.241 |
| 16 | %27 | 158 | 0.647 | 0.391 |
| 20 | %41 | 158 | 0.700 | 0.391 |
| 24 | %59 | 166 | 0.741 | 0.468 |
| **32 (küresel)** | %100 | **193** | **0.856** | **0.709** ✓ |

**Bu tablo tanının kanıtıdır.** B görevinde menzil 8 → 16 HİÇBİR ŞEY
değiştirmiyordu (erişim büyüdükçe yerelleştirilebilirlik aynı hızda
bozuluyordu — yönsüz kanalın net menzil faydası yok). Burada
yerelleştirme GEREKMEDİĞİ için temiz, monoton bir doz-cevap eğrisi var.
Görev değişikliği tam da amaçlanan şeyi yaptı.

**Kalibrasyon sonucu:** çıta yalnız menzil 32'de aşılıyor; 64-toruste
Chebyshev 32 = KÜRESEL yayın. Yani bu görev, kanalın herkese ulaşmasını
istiyor. Karar Ali'de (**PL-28**): küresel kanal, sembolün taşıyabildiği
tek şeyin KİMLİĞİ (16'dan hangisi) olması demektir — uzam, yön, mesafe,
gönderen: hepsi düşer. Anlam çıkacaksa saf sembolden çıkacak. Bu, dil
tuzağının en temiz hâli; ama menzili "yakın ajanlar duyar" diye
gerekçelendiren PL-21 varsayımını geri alır.

### Sınırlar (dürüstlük)
- `told` mükemmel sembol→bit konvansiyonunu HEDİYE alır → bu kol
  öğrenilmiş bir dilin ULAŞABİLECEĞİ TAVANDIR, tipik başarımı değil.
  Öğrenen ajanın bunu keşfedip keşfedemeyeceği H3/H4'ün asıl sorusudur
  ve bu oracle onu ölçmez.
- Tüm kollara olayın NE ZAMAN aktif olduğu verildi (M-06: tek değişken
  HANGİ eylem). Zamanlamanın kendisi de öğrenilmesi gereken bir şey
  olabilir; ayrı ve daha zor bir iddia.
- İpucu bölünmesi (`event_visibility_split`) burada 2 bitlik kod olarak
  somutlandı; spec metni elde olmadığından (PL-26) bu bir yorumdur ve
  PL-27'de kayıtlıdır.
### PL-27 / PL-28 KARARLARI UYGULANDI (Ali, 2026-07-27)

**PL-28 — menzil KÜRESEL** (`signal_range` 8 → 32; 64-toruste azami
Chebyshev 32). Sembolün taşıyabildiği tek şey artık KİMLİĞİ; uzam,
yön, mesafe, gönderen hepsi düştü.

> **İtiraz testi (S3-B geriye dönük):** "küresel menzil B görevini
> kurtarır mıydı?" — HAYIR. n=5, 48 epizot: `beacon` 8/48 → 17/48,
> `signal` 6/48 → 11/48 yükseldi ama kanalsız `vision` **20/48** ile
> hâlâ önde. ÇATAL C, PL-28 değişikliğine DAYANIKLI. (Mekanizma
> öngörüsü doğrulandı: menzil 32'de "biri 32 içinde" = tüm grid =
> sıfır yerelleştirme bilgisi.)

**PL-27 — seçenek (c): sıfır yeni prior biti.** Öncü, AYRI KANAL
AÇILMADAN mevcut tehlike kanalına (obs kanal 2) yazılır. Algı
ajan-merkezli ve ÖZELdir — spec'in "her ajana olayın farklı parçası"
maddesinin doğrudan karşılığı: aynı olayın farklı yüzünü herkes kendi
bedeninde duyar. Konum kodlaması:

| ajan-merkezli hücre | anlamı |
|---|---|
| (0,0) | uyarı penceresi açık (varlık göstergesi) |
| (0,1) | gözlenen bit İNDEKSİ = 1 (yoksa 0) |
| (1,0) | gözlenen bit DEĞERİ = 1 (yoksa 0) |

Hangi hücrenin ne demek olduğu ajana SÖYLENMEZ. Ayırt etme işi de
ajanda: öncü yalıtık hücredir, enerji ÇEKMEZ ve yalnız uyarı
penceresinde yanar; gerçek tehlike 5×5 bloktur ve enerji çeker.
**KERNEL_BUDGET'a yazılan bit: 0** (yeni kanal yok, kategorik ayrım
verilmedi, loss/mimari/başlatma değişmedi).

**Kodlamanın KAYIPSIZ olduğu testle sabitlendi** (enstrüman denetimi,
M-15): 5 ajan × 120 tur boyunca her uyarı penceresinde, gözlemden
çözülen ipucu olayın gerçek ipucuyla BİREBİR eşit
(`test_percept_encodes_cue_losslessly_in_hazard_channel`). Ayrıca
algının özel olduğu doğrulandı: AYNI hücrede duran 8 ajan farklı bit
gözleyebiliyor (`test_percept_is_private_to_each_agent`). Yani ajan
için öğrenilebilir bir sinyal fiilen VARDIR; keşfedip keşfetmeyeceği
H3/H4'ün sorusu.

- Oracle ipuçlarını hâlâ doğrudan okur (ölçüm aleti); fiziksel algı
  yolu yukarıdaki testlerle kayıpsız kanıtlandığı için `told` kolunun
  sayıları algı yoluyla da aynen geçerlidir.

### Yeni ders var mı?
VAR → **M-25**: *Tuzak kurmadan önce kaçış yollarını say.* Bir yetinin
(X) baskı altında belirip belirmeyeceğini ölçecek aparatı kurmadan
önce, ödüle giden ALTERNATİF yollar sayılır; herhangi biri X'ten
ucuzsa tuzak X'i değil alternatifi ölçer. Bu sprint iki yönden de
gösterdi: B görevinde kaçış yolu yoktu ama kanal ödülü hiç açamıyordu
(ölçüm boşa gitti); olay görevinin İLK taslağında (3 turluk olay)
"acıyı çek sonra düzelt" kaçış yolu değerin ~%67'sini kurtarıyordu ve
kanal gereksiz kalacaktı — kilit-1 (`event_duration=1`) tasarım
anında, koşum yapılmadan kondu. M-01'in ("cetvel önce") hedef değil
TASARIM tarafına uygulanmış hâli.

---

## S3-B — SONUÇLAR (2026-07-27)

### PL-24 — SÜRDÜRÜLEBİLİRLİK: yeniden üretildi, **KAPI 5 KAPANDI**
L3 (`god`), 48 epizot/koşul, tavan 3000 (`runs/s3_b_oracle_v2.json`):

| B enerji | kişi başı | medyan pencere | medyan açılış | sansür |
|---|---|---|---|---|
| 75 | 37.5 | 464.5 | 17.5 | 0/48 |
| **135** | 67.5 | 3000 (tavan) | 129.0 | 39/48 |
| 180 | 90 | 3000 (tavan) | 129.0 | 39/48 |
| 225 | 112.5 | 3000 (tavan) | 129.0 | 39/48 |
| 270 | 135 | 3000 (tavan) | 129.0 | 39/48 |

**Eşik yine 135 — orijinal bulgu doğrulandı.** Çapraz kontrol: v1 1500
tur tavanında 62 açılış raporlamıştı; 3000 tavanında 129 ≈ 2×62 →
neredeyse birebir yeniden üretim. 135 üstünde tüm satırların ÖZDEŞ
olması, eşiğin üstünde açılış hızının enerjiyle değil YOL SÜRESİYLE
sınırlandığını gösterir (v1'in "düz 62" örüntüsünün açıklaması).
**`resource_b_energy=180` gerekçesi ayakta**; artık üreten kod
repoda (`training/b_oracle.py`) ve sansür oranı beyanlı.

### PL-25 — KEŞFEDİLEBİLİRLİK: **ÇATAL C** (ön-kayıtlı matris)
Mevcut config (n_b=3), 48 epizot (`runs/s3_b_discover.json`):

| seviye | pencere | açılış/1000 çift-turu | epizot payı |
|---|---|---|---|
| `random` | 69 | 0.0 | 0/48 |
| `noB` (kontrol) | 146 | 0.0 | 0/48 |
| `vision` | 128 | **0.652** | 4/48 |
| `signal` | 116 | **0.0** | 0/48 |
| `beacon` (en iyi çaba) | 90 | **0.0** | 0/48 |
| `pair` (görsel takip) | 132 | 0.0 | 0/48 |
| **`god` (tavan)** | 3000 | **43.153** | **48/48** |

- **ZAYIF çıta (L2 ≥ 2×L1): GEÇMEDİ** — hem de TERS yönde: kanal
  0.0, kanalsız görüş 0.652. **Kanal zarar veriyor.**
- **GÜÇLÜ çıta (≥6.2/1000): GEÇMEDİ** (~66× altında).
- → **ÇATAL C: S3'ün merkezi basıncı mevcut kalibrasyonda YOK.**

### M-21 kontrolü kendi enstrümanıma: 2-ajan → 5-ajan
Az önce deftere yazdığım dersi oracle'a uyguladım (çift sayısı
C(5,2)=10 → karşılaşma oranı artar). 48 epizot:

| seviye | n=2 epizot payı | **n=5 epizot payı** | n=5 açılış/1000 |
|---|---|---|---|
| `vision` | 4/48 | **20/48** | 2.227 |
| `signal` | 0/48 | 6/48 | 0.808 |
| `beacon` | 0/48 | 8/48 | 0.910 |
| `pair` | 0/48 | 0/48 | 0.0 |
| `god` | 48/48 | 48/48 | 43.1 |

**Mutlak sayılar 5× değişti (M-21 haklı — 2-ajan sonucu taşınmıyor),
nitel sonuç DEĞİŞMEDİ ve keskinleşti:** her iki rejimde de
`vision` > `signal` ≥ `beacon`. Güçlü çıta n=5'te bile aşılmıyor
(en iyi 2.227 < 6.2).

### Neden kanal zarar veriyor — mekanizma
1. **Yön ve kimlik yok (PL-21b/c).** Duyan sinyale doğru yürüyemez;
   aldığı tek bilgi "Chebyshev 8 içinde biri var" (arama uzayı
   4096 → 289, ~14×). Bu daralma yol maliyetini ödemiyor.
2. **Menzil işe yaramıyor** (`runs/s3_b_calib.json`): menzil 8 vs 16
   `vision`'da ÖZDEŞ, `signal`'de gürültü. Mekanizma: menzili
   büyütmek duyma oranını artırırken yerelleştirilebilirliği AYNI
   oranda bozar (kutu alanı menzilin karesiyle büyür) — **yönsüz bir
   kanalın net menzil faydası yoktur.**
3. **Enerji maliyeti pencereyi kısaltıyor:** `noB` 146 → `signal` 116
   → `beacon` 90 (n=5'te 378 → 217 → 186). Kanal, kazandırdığından
   fazlasını pencereden götürüyor.
4. **Senkron penceresi darboğaz değil:** 2 → 200 süpürmesi `vision`'ı
   1/48'den yalnız 3/48'e taşıdı. Sorun eşzamanlılık değil, ikisinin
   AYNI B'yi hiç bulamaması.
5. **Ham karşılaşma oranı (48 epizot, `noB`):** ajanlar birbirini
   turların **%3.37**'sinde görüyor, 48 epizodun yalnız 10'unda hiç
   karşılaşıyor; bir ajan B'yi turların **%5.16**'sında görüyor.
   Koordinasyon bu iki nadir olayın ÇAKIŞMASINI istiyor.

### Ekolojiyle bağ (v2 koşumunun yorumu)
S3 ekolojisi 20K turda (5 ajan hep canlı ≈ 20.000 pencere-turu)
**0 açılış** verdi. `vision` oracle'ının n=5 hızıyla (2.227/1000)
beklenen sayı **~45**'tir. Aradaki fark yetkinlik açığıdır: ekolojideki
ajanlar `vision` seviyesinde değil, `random` seviyesindedir (o da 0
veriyor) — v2 taban çizgisinin "ömür = her tur hareket tavanı"
bulgusuyla tutarlı.

### Sonuç — tasarım düzeyinde
Tavan (`god` 48/48, 43/1000) ile ulaşılabilir her politika (≤20/48,
≤2.2/1000) arasındaki fark bir DOZ farkı değil: tek bir dünya
parametresi (yoğunluk, menzil, senkron penceresi) kapatmıyor.
H3/H4, kanalın koordinasyon maliyetini DÜŞÜREBİLECEĞİNİ varsayar; bu
görev + bu kanal fiziğinde düşürmüyor — **mükemmel paylaşılan
konvansiyon hediye edildiğinde bile.** İki çıkış yolu var, ikisi de
Ali'nin (anayasa-dokunuşlu):
- **(A) Görevi değiştir:** koordinasyonun zor kısmı UZAMSAL olmasın.
  Yönsüz 4-bitlik bir sembol "nerede" taşıyamaz ama "ne / ne zaman"
  taşıyabilir (ör. eşzamanlı eylem seçimi, tehlike uyarısı, zamansal
  senkronizasyon). B-randevusu bu kanal için yanlış görev.
- **(B) Kanalı değiştir:** konum/yön bilgisi taşısın — ağır anayasal
  değişiklik (spec 4.2 + K-114 yeniden yazılır).
Not: (A) ucuz ve anayasaya sadık; (B) deneyin sorusunu zayıflatır.

### Sınırlar (dürüstlük)
- Politika repertuvarı scripted ve tüketici değil: greedy-görüş,
  mükemmel-konvansiyon yayın, çapalı fener, görsel takip. Öğrenen bir
  ajanın aynı duyularla bunları belirgin biçimde aşması beklenmez,
  ama kanıtlanmadı.
- Ölen ajan ikame EDİLMİYOR (oracle ≠ ekoloji); ekolojide sürekli 5
  canlı olması karşılaşma oranını bir miktar yükseltir.
- `beacon` ve `pair` kolları ön-kayıtta yoktu; post-hoc eklendi ve
  öyle etiketlendi (kanal lehine en iyi çaba + ayıraç kol).

### Yeni ders var mı?
VAR → **M-24**: *Oran metriğinin paydası tedaviden etkileniyorsa oran
yanıltır.* `açılış/1000 çift-turu`, sinyal maliyeti pencereyi
kısalttığı için `beacon`'ı en iyi gösteriyordu (11.5 > çıta 6.2) —
oysa güvenilir ölçü olan EPİZOT PAYI'nda `beacon` en kötülerdendi
(1/12). M-20'nin ("taban da cihazın parçasıdır") payda kardeşi:
tedavi paydayı değiştiriyorsa oran değil, olay payı raporlanır.

---

### B-KOORDİNASYONU ÖLÇÜLEBİLİR DEĞİL — "B-açılış 0" boş enstrümandır (2026-07-27)

Şans-keşfi olasılığı hesaplandı (3 B hücresi / 4096, 2 farklı ajan,
2 turluk senkron pencere, rastgele eylemde INTERACT payı 1/6):

```
P(ajan turda B-dokunuşu)      = 1.22e-04
P(eşzamanlı çift dokunuş/tur) = 9.93e-08
20K turda beklenen B-açılışı  = 0.002
```

**Gözlenen 0, saf şansın öngördüğü değerin ta kendisi.** Yani "B-açılış
0" ajanlar hakkında bir negatif sonuç DEĞİL; ayırt etme gücü olmayan bir
ölçüm (M-03 anlamında confounded'ın uç hali: sıfır güç).

Kök neden: oracle B'nin *koordine edilirse sürdürülebilir* olduğunu
ölçtü, *keşfedilebilir* olup olmadığını hiç ölçmedi. Proje bu ayrımı
A kaynağı için zaten öğrenmişti (PL-16: "kârlı strateji,
keşfedilemeyecek kadar derin") — ders B'ye taşınmamış. Açık iş:
**PL-25**.

### DP-01b'nin nicel durumu: miras 65. nesilde bitiyor (2026-07-27)

Aşağıdaki metin "birikimli gürültü σ≈0.16" hesabını doğru yapmış ama
AĞIRLIK ÖLÇEĞİYLE karşılaştırmamıştı; kararı belirleyen oran budur:

| | |
|---|---|
| seed-3 ağırlık RMS'i | **0.0804** (262.493 parametre) |
| mutasyon σ (nesil başına) | 0.01 |
| kümülatif sürüklenme | σ·√n |
| **gürültü = sinyal olduğu nesil** | **≈ 65** |
| koşumun ulaştığı nesil | 250–356 (gürültü/sinyal 2.0–2.4×) |

Yani miras t≈3900'de tükenmiş; koşumun kalan ~%80'i saf rastgele
yürüyüştür. DP-01b'nin bir anlamı olacaksa ya σ ≈ 0.002'ye inmeli
(kritik nesil ~1600) ya da seçilim (PL-22 seçenek a) sürüklenmeyi
dengelemeli. Bu, PL-22 çerçeve kararına nicel girdidir.

**Şerh:** *"A2 medyan ömrü 66 vs diğerleri 53-58 — küçük ama görünür
devralınmış avantaj"* iddiasının KONTROLÜ YOK (A2 taze başlatılıp aynı
seed'de koşulmadı; mimari konfoundu açık). Üstelik A2'nin tutumluluğu
zamanla eriyor (sinyal oranı kurucu nesilde 0.261 → nüfusta 0.765), yani
"avantaj" zamana bağlı. Etiket: ADAY GÖZLEM değil, **kontrolsüz gözlem**.

### Yeni ders var mı?
VAR → **M-21**: Rejim transferi ölçülür, varsayılmaz. "seed-3'ü 5 ajana
taşıdım" bir hipotezdi; ekoloji 58 turda söndü. Her yeni rejim kendi
fizibilite oracle'ını + kalibrasyonunu ister (M-01'in nüfus ölçeğine
genişlemesi).

VAR (2026-07-27 denetimi) → **M-22** (fizibilite iki sorudur: değer mi +
bulunabilir mi) ve **M-23** (sonda kadar SAYAÇ da cihazdır).

---

# ★ ARA SONUÇ (tez düzeyi) — AJANIN ÖZ-HAREKET MODELİ YOK
### Öz-hareket merdiveni (S2.10 denetim revizyonu)
- **Basamak 1 — efference copy: VERİLDİ-YETMEDİ.** Kendi son eylemi
  S1'den beri girdi (K-102a, denetimle deftere geçti). S2.9 gösterdi:
  bu girdi eldeyken bile kayma modeli oluşmuyor — yokluk girdi
  eksikliği değil.
- **Basamak 2 — yerellik iskelesi (K-113, S2.10): KAZANILDI (üretici
  enstrüman).** İçerik-sıfır yapısal iskele; M-19 kapısından geçti;
  eğitim sonrası kayma sadakati 5/5 seed'de ~mükemmel (0.956-1.000).
  ARA SONUÇ RAFİNE EDİLDİ: öz-hareket modeli "oluşamaz" değil —
  prior'suz mimaride örneklem-karmaşıklığı engeliyle oluşamıyordu;
  yerellik iskelesi (dünya hakkında sıfır içerik) verilince eylem→kayma
  eşlemesi hidden üzerinden ÖĞRENİLDİ. Korelasyonel enstrüman (P1 disp)
  sınavı PL-13'te — zincir tamamlanırsa.
### (S2.9 güçlendirmesi: doz-cevap noktası eklendi)
K-110rev müdahalesi (4× uzamsal örnekleme + hareket-yanlı keşif +
~1200 kayma-geçişi/10K) kayma sadakatini yalnız 0.09→0.16'ya taşıdı.
Yokluk pasif veri eksikliği değil: prior'suz mimaride öz-hareket
temsilinin örneklem karmaşıklığı, bu ekolojinin sunabileceği gradyan
basıncının ötesinde. "Kendiliğinden belirme" bu koşulda YAPISAL olarak
engelli görünüyor — H1'in uzamsal yarısı için güçlü negatif.

**İki bağımsız enstrümanla çaprazlanmış yapısal bulgu (2026-07-08):**

1. **Korelasyonel enstrüman (S2, P1 disp probu):** Eğitilmiş GRU hidden
   state'inden kümülatif yer değiştirme lineer VE MLP probla okunamıyor;
   eğitilmiş−ikiz farkı yok; eğri yükselmiyor. Spawn randomizasyonuna
   dayanıklı negatif (S2-tekrar).
2. **Üretici enstrüman (S2.8, kayma sadakati Test A):** Aynı modelin
   ileri tahmini, öz-hareket altında egosantrik kaymayı üretmiyor
   (doğru-yer kütlesi 0.08 vs eski-yer 0.71): model "ben hareket edersem
   dünya görünümüm kayar" bilgisini TAŞIMIYOR.

İki enstrüman farklı katmanlarda (okunabilirlik / üretim) aynı yokluğu
gösteriyor: **bu bir prob zayıflığı değil, temsilin yapısal yokluğudur.**
Mekanik açıklama zinciri belgeli: tasarruf-ağır davranış → veride
öz-hareket geçişi kıtlığı → model uzamsal öz-etkiyi öğrenmiyor →
planlama uzayda kör → davranış tasarrufta kalıyor (kapalı döngü;
PL-12/M-05 ailesi). H1'in uzamsal yarısı bu rejimde OLUŞAMAZ —
"çıkmadı"dan güçlü bir ifade: oluşum yolu davranış-veri döngüsünce
kapalı. Ali'nin PL-13 tezi ("temsil ihtiyacın gölgesidir") ile TUTARLI
ama hâlâ test edilmemiş: ihtiyaç (hareket) hiç doğmadı. S2.9 bu
döngüyü veri yönünden kırmayı deniyor; kayma-eşdeğişimli mimari çözüm
M-18 gereği YASAK (bağımlı değişkeni mimariye yazmak olur).

## S3-D — NÜFUS ORACLE'I ÖN-KAYIT (koşumdan önce, M-08) (2026-10-18)

**Bağlam.** PL-22 KARARI (Ali, 2026-10-18): ekoloji çerçevesi önce
(c) 5× seed-3 klon taban + (b) yuva dönemi; seçilim (a) sonra, ayrı
değişken (M-06). M-21 gereği öğrenen-ajan koşumundan ÖNCE nüfus
fizibilite oracle'ı: tek-ajan yetkinliğinin 5-ajan rejimine taşınıp
taşınmadığı ÖLÇÜLÜR, varsayılmaz. Araç: `training/pop_oracle.py`
(ölçüm aleti, ajan değil → KERNEL_BUDGET'a bit yazmaz; deneyci
kararları M-09 gereği aşağıda beyanlı).

**Dünya:** economy v3 (24 A, A=45, B=180, m=0.6), kanal küresel (PL-28),
olaylar KAPALI (event_every=0). Tavan 3000 tur, 5 dünya seed'i
(9100+e). **Halef YOK:** ölen ölü kalır (oracle, ekoloji değil; ölü
beden entity kanalında hayalet olarak görünür — b_oracle emsali,
beyanlı sınır).

### Aşama A — `capacity`: dünya 5 yetkin ajanı taşıyor mu? (M-02)
Scripted A-oracle (`training/oracle.py::OraclePolicy`, tarama fazı
ajan indeksine göre kaydırılmış — b_oracle dersi) × n ∈ {1, 5}.
- **Çıta A:** n=5 medyan ömür ≥ 0.75 × n=1 medyan ömür.
- Düşerse: sorun ajanda değil dünyada (24 A beş ajana yetmiyor) →
  (c)/(b) kararı askıya, önce kaynak kalibrasyonu (PL-14 emsali).

### Aşama B — `clone`: (c) transfer merdiveni (M-21)
Seed-3 transplantı (`transplant_seed3`, MUTASYONSUZ), roster A2 config'i
(ekolojiyle aynı: cem_iters=2, kanal açık). Dört kol, tek değişken:

| kol | n | kanal | öğrenme | ne ölçer |
|---|---|---|---|---|
| L0 `clone1_mute` | 1 | yok (eylem-only planlama) | yok | **cihaz doğrulaması** (M-15): S2.10 eval ömrü 162 |
| L1 `clone5_mute` | 5 | yok | yok | +4 rakip: yetkinlik rekabete dayanıyor mu |
| L2 `clone5_open` | 5 | açık (ortak planlama) | yok | +kanal: başkalarının gürültüsü bozuyor mu |
| L3 `clone5_learn` | 5 | açık | açık (ε açık) | +online öğrenme: koruyor mu, aşındırıyor mu (M-05) |

- **Cihaz kapısı:** L0 medyan ömür [110, 220] dışında ise cihaz bozuk
  (cem 2 vs 4 farkı beyanlı), merdivenin hiçbir basamağı okunmaz.
- **Çıta B1 (c tezi):** L1 medyan ömür > 100 (hareket tavanı 62.5 ve
  gözlenen 52'nin açık üstü) VE ≥ 0.75 × L0.
- **Çıta B2:** L2 ≥ 0.85 × L1 (kanal gürültüsü yetkinliği bozmuyor).
- **Öngörü (bağlayıcı):** L3 ≤ L2 (on-policy öğrenme çok-ajan dünyada
  modeli aşındırır, M-05). L3 > L2 çıkarsa olumlu sürpriz; L3 < 0.6×L2
  çıkarsa öğrenme ekolojide zararlı → "ölüm gerçek + online" rejimi
  klon tabanla bile öğrenemez, (b) yetmez, Ali'ye dön.

**Sonuç matrisi (koşumdan önce yorumlanmış):**
- A✓ B1✓ B2✓ → yetkinlik taşınıyor; ekolojideki 52 turun kaynağı taze
  slotlar + drift'tir → (c) doğru ilk adım, (b) kalibrasyonuna geç.
- A✓ B1✗ → yetkinlik rekabette çöküyor (M-21 negatifi); (c) tek başına
  yetmez; PL-22'ye yeni seçenek: önce 5×klon + 48 A ile kapasite
  artırımı (M-02), Ali kararı.
- A✓ B1✓ B2✗ → kanal gürültüsü aşındırıyor; klon tabanın kanal-körü
  başlatılıp kanalı sonradan "açması" düşünülür (PL-08 emsali).
- A✗ → dünya kalibrasyonu, yukarıda.

### Aşama C — `nest`: (b) kalibrasyonu
Yuva = yaş < `nest_turns` iken metabolizma + eylem + sinyal maliyeti ×
`nest_factor` (`agent/config.py`, `agent/homeostasis.py`; varsayılan
T=0/f=1 bit-eş). **Analitik sınır (koşumdan önce):** hasat etmeyen,
her tur hareket eden ajan yuvada 100/(f·1.6) tur yaşar: f=0.5 → 125,
f=0.25 → 250, f=0.1 → 625. Yani (b), f>0 iken SIFIRDAN öğrenme
penceresi (~45K tur, S2 yayı) AÇAMAZ; rolü klon halefinin mutasyon
şokunu yumuşatmak ve hasat zincirini kurmaya vakit vermektir. Bu
beyan edilmeden "yuva öğrenme penceresi açar" denemez.
Izgara: (T,f) ∈ {(0,1.0), (600,0.5), (600,0.25), (600,0.1), (2000,0.1)};
kollar: `random5` (yetkinsizlik tabanı, ucuz), `fresh5` (eğitimsiz
çekirdek + MPC, öğrenmesiz), `clone5_learn` (asıl kol). 3 seed.
- **Çıta C1 (cihaz):** `random5` medyan ömrü analitik sınırın ±%25'i
  içinde (yuva muhasebesi doğru çalışıyor).
- **Çıta C2 (fayda):** en az bir (T,f) noktasında `clone5_learn`
  medyan ömrü yuvasız koluna göre ≥ +%30 VE A-hasat/ajan-turu düşmüyor
  (yuva tembellik üretmiyor).
- **Öngörü:** fresh5 hiçbir noktada 520'yi (10× gözlenen) geçmez;
  geçerse (b) beklenenden güçlü.

### Kaçış yolları (M-25) ve beyanlar
- **Ölüm ucuz:** ekolojide ölen slot 100 enerjiyle yeniden doğar; yuva
  bunu güçlendirir (ölüp yuvaya dönmek, hasat etmekten ucuz olabilir).
  Oracle halefsiz olduğu için ÖLÇMEZ; ekoloji koşumuna geçmeden önce
  "doğum enerjisi" / "yuva yalnız ilk nesil" seçenekleri açık loop
  (PL-29 adayı). Tuzak kurulmadan sayıldı, kapatılmadı.
- **Hediye yok:** klon kolları gerçek seed-3 ağırlıklarını kullanır
  (ölçüm nesnesi), scripted kol A konumlarını yalnız gözlemden görür.
- **Roster ertelendi:** (c) tüm slotları A2 mimarisine indirger
  (PL-20 alternatifi). Heterojenlik sonraki değişken.
- **Zaman damgası:** bu bölüm koşumdan önce yazıldı; sonuçlar ayrı
  başlıkta.

## S3-D — NÜFUS ORACLE'I SONUÇLAR (2026-10-18)

Veri: `runs/s3d_capacity.json`, `runs/s3d_clone.json`, `runs/s3d_nest.json`,
log `runs/s3d_pop_oracle.log`. Dünya hash'i dosyalarda. Halefsiz oracle,
tavan 3000; hiçbir kol sansürlenmedi. B-açılış her yerde 0 (olay görevi
kapalı, beklenen).

### Aşama A — kapasite: **GEÇTİ**
| kol | n | medyan ömür | hasat/1K ajan-turu |
|---|---|---|---|
| oracle1 | 1 | 184 | 40.9 |
| oracle5 | 5 | **214** | 51.7 |

Çıta A (≥ 0.75×184 = 138) rahat geçti; beş scripted ajan tekinden uzun
yaşıyor (A hasatta anında yer değiştirdiği için rekabet değil, bağımsız
tarama var). **Dünya 5 yetkin ajanı taşıyor; sorun dünyada değil.**

### Aşama B — klon merdiveni: **A✓ B1✓ B2✗** hücresi
| kol | tek değişken | medyan | ortalama | hasat/1K | sinyal oranı | çıta |
|---|---|---|---|---|---|---|
| L0 clone1_mute | — | **156** | 307 | 30.0 | 0 | cihaz [110,220] ✓ |
| L1 clone5_mute | +4 rakip | **118** | 140 | 18.9 | 0 | >100 ✓, ≥117 ✓ (kıl payı) |
| L2 clone5_open | +kanal | **78** | 88 | 17.7 | **0.768** | ≥100 ✗ |
| L3 clone5_learn | +öğrenme | **83** | 103 | 15.6 | 0.502 | öngörü L3≤L2: tutmadı (≈) |

- **Cihaz geçerli:** L0 = 156, S2.10 eval ömrü 162 ile uyumlu
  (cem 2 vs 4 farkına rağmen). Not: seed-3'ün tek-ajan ömrü STAY
  tabanını (167) HİÇ aşmıyordu; "yetkinlik" marjinaldir, bu okumanın
  tavanıdır.
- **(c) tezi desteklendi, kıl payı:** rekabet yetkinliği %24 aşındırıyor
  ama klon taban hareket tavanının (62.5) ve ekolojideki 52'nin açık
  üstünde kalıyor.
- **ASIL KIRILMA KANALDA (B2 düştü):** kanal açılınca 118 → 78. Mekanizma
  çoğunlukla KENDİ sinyal maliyeti: dondurulmuş klon turların %77'sinde
  sinyal yayıyor (eğitilmemiş sinyal sütunları → argmax sinyalli
  satırlara düşüyor; S3 ENSTRÜMAN ŞERHİ'ndeki "taze A2 sinyal-delisi"
  bulgusunun transplant hâli). Tur maliyeti 1.6 → ~2.0, ömür ×0.78 →
  beklenen ~92, ölçülen 78; kalan fark alınan-sinyal gürültüsü.
  **Ekolojideki 52 turluk ömrün birincil kaynağı drift ya da taze slot
  değil, kanalın klonu boğmasıdır** (yeni teşhis; PL-22 metni buna göre
  düzeltildi).
- **Öğrenme nötr:** L3 ≈ L2. Ne koruyor ne aşındırıyor; ömür zaten
  öğrenmeye yetmiyor. M-05 öngörüsü (aşındırır) bu ufukta gözlenmedi.

### Aşama C — yuva: **ömrü uzatıyor, kendine yeterlilik kurmuyor**
| (T, f) | random5 | analitik | fresh5 | clone5_learn | hasat/1K (clone) |
|---|---|---|---|---|---|
| (0, 1.0) | 71 | 70 | 50 | 83 | 17.4 |
| (600, 0.5) | 140 | 140 | 99 | **408** | 16.7 |
| (600, 0.25) | 279 | 280 | 199 | **636** | 14.8 |
| (600, 0.1) | 611 | 600 (yuva sonu) | 495 | 677 | 12.8 |
| (2000, 0.1) | 703 | 700 | 495 | **2061** | 11.3 |

(random analitik: ortalama tur maliyeti 1.43 × f; yuva sonu sınırı.)
- **C1 cihaz ✓:** random5 analitik sınırla ±%3 içinde; yuva muhasebesi
  doğru.
- **C2 fayda:** her noktada ömür ≥ +%30 ✓. Hasat şartı: f=0.5'te −%4
  (✓), f=0.25'te −%15 (sınırda), f=0.1'de −%26/−%35 (✗, **tembellik**).
- **Öngörü tuttu:** fresh5 hiçbir noktada 520'yi geçmedi (azami 495).
- **Yuva-sonu uçurumu (M-25 kaçış yolu GERÇEKLEŞTİ):** f≤0.25'te
  klonların neredeyse tamamı yuva biter bitmez ölüyor (T=600 → 603-712;
  T=2000 → 2023-2129; 15/15 ve 14/15). 600 ya da 2000 turluk öğrenme
  penceresi hasat oranını YÜKSELTMEDİ (sabit/düşen) → pencere içinde
  öğrenilen şey tam maliyette hayatta kalmaya çevrilmiyor. f=0.5
  tek "gerçek ekoloji" noktası: ölümler yuva içine ve dışına yayılmış
  (145-613), hasat korunmuş.
- **Hiçbir kol STAY tabanını (167, tam maliyet) öğrenmeyle aşmadı.**
  Bu S2 yayının bilinen sınırıdır; yuva onu değiştirmiyor, sadece
  erteliyor.

### Karar girdisi (Ali'ye)
1. **Yuva ayarı:** tavsiye (T=600, f=0.5): +%390 ömür, hasat korunur,
   uçurum yok. f=0.25 daha uzun ama yuva-sonu uçurumu ve −%15 hasat.
2. **Kanal maliyeti klonu boğuyor** — üç seçenek: (i) kanalı yuva
   bitene kadar KAPALI tut, sonra aç (kademeli; obs_dim sabit, yalnız
   sinyal gönderimi/alımı maskelenir); (ii) kanal açık, yuva sinyal
   maliyetini de indiriyor (mevcut uygulama; f=0.5'te zaten ölçüldü:
   408); (iii) sinyal maliyetini anayasal 0.5'ten düşürmek (deneyin
   basıncını zayıflatır, tavsiye edilmez). Tavsiye: **(ii)** — kanal
   anayasal olarak açık ve pahalı kalır, yuva çocuklukta yumuşatır;
   (i) ayrı değişken olarak sonra denenebilir (M-06).
3. **Ölüm ucuz** (PL-29): ekolojide halef 100 enerji + yuvayla doğar;
   yuva-sonu uçurumu + ucuz ölüm = "yuva çiftçiliği" riski. Ekoloji
   koşumunda ölüm sayısı/nesil hızı birincil izleme metriği olmalı.

### Yeni ders var mı?
YOK (kapsıyor). Kanal bulgusu M-21'in ("transfer ölçülür") bir örneği:
genişleyen eylem uzayına taşınan yetkinlik yeni boyutta rastgele harcar.
Yuva-sonu uçurumu M-25'in tasarım anında sayılmış kaçış yoludur;
ölçüldü, kapatılmadı (PL-29).

## S3-E — ÖN-KAYIT (koşumdan önce, M-08) (2026-10-18, gece)

**Bağlam.** Ali (2026-10-18): S3-D tavsiyeleri onaylandı — yuva
(T=600, f=0.5), kanal AÇIK (yuva sinyal maliyetini de indirir); oto
karar + push yetkisi verildi, "deney bitene kadar". İlk gerçek dil
tuzağı koşumu: S3-C alarm-çağrısı görevi, klon taban + yuva
ekolojisinde, ÖĞRENEN ajanlarla (PL-30).

**Dünya:** economy v3, kanal küresel, olay kalibrasyonu S3-C oracle'ı
ile aynı (`event_every=30, lead=8, duration=1, penalty=25, K=4`).
**Kadro:** 5× seed-3 transplantı (A2 mimarisi, kurucu mutasyon yok;
halefler σ=0.01, DP-01b). **Koşum:** 20.000 tur, 3 dünya seed'i
(3001-3003), üç kol, tek değişken (M-06):

| kol | olay | kanal | soru |
|---|---|---|---|
| T (taban) | kapalı | açık | ekoloji klon+yuvayla nefes alıyor mu? |
| A (asıl) | açık | açık | sinyal kullanımı olayla ilişkileniyor mu? |
| K (kontrol) | açık | KAPALI (mute) | kanal gerçekten fark yaratıyor mu? |

**Enstrümanlar (ajana gitmez; M-23 kümülatif):** olay turu / isabet
(doğru eylem = kutup), uyarı penceresinde gönderilen sinyal oranı,
ipucu×sembol tablosu (4×16; yalnız uyarı penceresi), "pencerede duydu"
koşullu isabet, PL-29 ölüm sınıfları (yuva-içi, yuva-sonu 60 tur).

**Çıtalar:**
- **T1 (nefes):** Kol T medyan ömür ≥ 300 (S3-D oracle 408 vermişti;
  ekolojide halef mutasyonu + rekabet + öğrenme ile %25 pay). Düşerse
  öğrenen ekoloji oracle'dan daha kötü → PL-29/drift teşhisi önce.
- **A1 (sinyal-ipucu bağımlılığı):** ipucu×sembol tablosunda karşılıklı
  bilgi I(ipucu; sembol) > 0.05 bit (≥ 3 seed'in 2'sinde) — gürültü
  tabanının (0.0103 bit, S3 taban v2) ~5 katı. Not: tablo
  gönderenin KENDİ ipucuyla kurulur; anlam iddiası değil, olumsallık.
- **A2 (kanal fayda):** Kol A isabet oranı > Kol K isabet oranı +0.05
  VE Kol A'da "pencerede duydu" koşullu isabet > duymadı koşullu isabet
  +0.05. Şans 0.25, kendi-ipucu tavanı 0.50, tam bilgi 1.0.
- **A3 (ömür):** Kol A medyan ömür ≥ Kol K (kanal maliyetine rağmen
  net zarar vermiyor).

**Öngörüler (bağlayıcı):**
- T1 geçer (0.7 olasılık).
- A1 DÜŞER: 20K turda, ömür ~300-400 iken, öğrenme sinyal-ipucu
  olumsallığını kurmaz (MPC'nin sinyali eyleme çevirmesi için modelin
  "sinyal→başkasının eylemi→kendi enerjim" zincirini öğrenmesi gerekir;
  bu ufukta beklemiyorum). Beklenen I ≈ 0.01-0.03 bit.
- A2 DÜŞER: isabet her iki kolda ~0.25-0.35 (şans ile kendi-ipucu
  arası; ajan öncüyü tehlikeden ayırmayı bile öğrenmemiş olabilir).
- A3: belirsiz; kanal maliyeti yuvada yarıya indiği için ≈ eşit.

**Sonuç matrisi:**
- T1✓ A1✗ A2✗ → ekoloji yaşıyor, dil doğmadı (BEKLENEN). Sıradaki
  merdiven (M-06, her basamak ön-kayıtlı): (1) daha uzun koşum (50K),
  (2) olay sıklığı/cezası kalibrasyonu (basınç dozu; dünya-tarafı),
  (3) ipucu-tehlike ayrımı teşhisi (ajan öncüyü görüyor mu — gözlemci
  probu), (4) seçilim (a) (PL-22'nin ertelenen ayağı).
- T1✓ A1✓ A2✗ → sinyal ipucuyla ilişkili ama kimse kullanmıyor:
  "konuşan var, dinleyen yok" → aday gözlem; alıcı tarafı teşhisi.
- T1✓ A1✓ A2✓ → ADAY GÖZLEM (H3/H4 yönünde); Beş Kapı başlar:
  bit-eş tekrar, mute ablasyonu (K zaten), zaman çizgisi (hangi nesilde
  doğdu), KERNEL_BUDGET denetimi, prob sızıntısı (gözlemci sayaçları
  ajana sızmıyor — yapısal). İDDİA sabah Ali ile.
- T1✗ → önce ekoloji; A/K kolları yine okunur ama "nefessiz" şerhiyle.

**Kaçış yolları (M-25):** (i) olayda STAY=kutup 0 → "hep STAY" politikası
%25 isabet alır ve enerji korur; şans tabanı bu yüzden 0.25, STAY
yanlılığı raporlanır. (ii) Ölüm ucuz + yuva (PL-29): ölüm/nesil hızı
ve yuva-içi ölüm payı raporlanır. (iii) Sinyal ε-dalından gelir
(16/17): A1 bu yüzden ipucu-KOŞULLU dağılım ister, ham sinyal oranı
değil.

**Beyanlar (M-09):** sinyal maliyeti artık `apply_turn(signal_cost=)`
yolunda (f=1'de eski breath kayıtlarıyla bit-eş değil; yeni
determinizm testi geçti). Kurucu mutasyon yok (çeşitlilik halefiyetle).
Olay parametreleri oracle kalibrasyonundan alındı, ekolojide yeniden
kalibre edilmedi (M-21 riski beyanlı: 5 öğrenen ajan ≠ 5 scripted).

## S3-E — SONUÇLAR: **T1✗ A1✗ A2✗ A3✗ — drift yine baskın, dil doğmadı** (2026-10-18, gece)

Veri: `runs/s3e/{T,A,K}_s300{1,2,3}/breath.json`, özet
`runs/s3e/summary.json` (`training/analyze_s3e.py`). 9 koşum × 20K tur,
hepsi tamamlandı.

| kol | medyan ömür | ölüm/20K | hasat/1K | sinyal oranı | olay isabet | I(ipucu;sembol) MM | çıta |
|---|---|---|---|---|---|---|---|
| T (olay yok) | **138** (131-144) | 622-653 | 3.5-4.2 | 0.60 | — | — | T1 ≥300 **✗** |
| A (olay+kanal) | **61** (60-64) | 1401-1447 | 2.1-2.6 | 0.79 | 0.199-0.209 | 0.0006-0.0017 bit (p≤0.015) | A1 ≥0.05 **✗** |
| K (olay, kanal yok) | **83** (81-87) | 1120-1152 | 3.2-3.6 | 0 | 0.205-0.217 | — | A2: A−K = −0.002 **✗**; A3: 61<83 **✗** |

**Okuma (ön-kayıtlı matris: T1✗ hücresi — "önce ekoloji").**
- **Drift yine baskın, bu kez temiz ölçüldü.** Halefsiz oracle aynı
  kadro/yuvayla 408 tur ve 16.7 hasat/1K vermişti; halefli ekolojide
  138 tur ve 3.8/1K. Zaman çizgisi (T_s3001): t=1000 (nesil 2) ömür
  185 / hasat 7.4; t=5000 (nesil 30) 144 / 3.0; t=20000 (nesil ~130)
  138 / 2.8. Tek fark halef mutasyonu σ=0.01 → kümülatif σ≈0.11 >
  ağırlık RMS 0.08 (PL-22 (ii) hesabı tutuyor: miras ~65. nesilde
  gürültüye gömülüyor). Yuva bunu geciktiriyor ama silemiyor.
- **Herkes yuvada ölüyor** (ölümlerin %100'ü yaş ≤ 600): yuva fiilen
  ömür boyu %50 indirim. PL-29'un "yuva-sonu uçurumu" bu rejimde
  gözlenemedi (kimse yuvadan çıkamadı).
- **Kanal hiçbir şey taşımıyor.** Sembol entropisi 3.98-3.99/4 bit;
  I(ipucu;sembol) 0.001 bit — permütasyon p küçük (n≈60K sinyal her
  sapmayı anlamlı yapar) ama etki gürültü tabanının (0.0103) bile
  ALTINDA (M-13: anlamlılık ≠ etki). Pencere sinyal oranı (0.75-0.79)
  ≈ genel oran: öncü sinyal davranışını değiştirmiyor.
- **Olay isabeti şans civarı ve altı:** 0.20-0.22 her iki kolda.
  **Taban düzeltmesi (M-20):** ön-kayıttaki 0.25 şans tabanı eylem
  marjinali tekdüze varsayar; kutup ∈ {STAY,UP,DOWN,LEFT}, RIGHT ve
  INTERACT hiç güvenli değil → gerçek şans = (1 − P(RIGHT) −
  P(INTERACT))/4 < 0.25. Ölçülen 0.20 bununla tutarlı; kutup bilgisi
  kullanımına dair sıfır kanıt. Kendi-ipucu tutarlılığı sayacı
  (şans 0.5) bu koşumda yoktu; S3-F'de var.
- **Kanal net zarar:** A kolu K'dan %27 kısa yaşıyor ve %30 az hasat
  ediyor. Mekanizma S3-D ile aynı: klon %79 oranında sinyal yayıyor
  (ε 16/17 + eğitilmemiş sinyal sütunları), yuva maliyeti yarıya
  indirse de birikiyor.
- **Enstrüman notu:** küresel kanal + 0.79 sinyal oranı → HER olay
  penceresinde herkes bir şey duyuyor ("duydu/duymadı" koşullu isabet
  ayrımı boş küme: duymadı yok). Bu karşılaştırma bu rejimde ölçülemez;
  rapor "ölçülemedi" der, "fark yok" demez (M-03).

**Öngörü karnesi:** T1 geçer (0.7) → YANLIŞ; A1/A2 düşer → DOĞRU;
A3 ≈ eşit → YANLIŞ (kanal net zarar).

**Yeni ders var mı?** YOK (kapsıyor): M-21 (oracle halefsizdi, ekoloji
halefli — transfer yine varsayılmıştı; oracle tasarımında halefiyet
değişkeni eksikti, S3-D beyanında "halef yok" yazılıydı ama sonucu
ekolojiye taşıma riski küçümsendi).

## S3-F — ÖN-KAYIT: halef mutasyonu (drift) merdiveni (koşumdan önce, M-08) (2026-10-18, gece)

**Soru.** Ekolojide yetkinlik erimesinin kaynağı halef mutasyonu σ mı
(drift), yoksa halefiyetin kendisi mi (hidden/PER/optimizer sıfırlama)
ya da çok-ajanlı online öğrenme (M-05)? Tek değişken: σ.
`run_ecology(mutation_sigma=)`; σ=0 → saf miras (ölen ağırlıklar
aynen devralınır; hâlâ "ölüm gerçek": enerji, hidden, tampon sıfır).

**Kollar (3 seed, 20K tur, klon kadro + yuva (600, 0.5)):**
| kol | olay | kanal | σ |
|---|---|---|---|
| T0 | kapalı | açık | **0.0** |
| T2 | kapalı | açık | **0.002** (PL-22 hesabı: kritik nesil ~1600) |
| A0 | açık | açık | **0.0** |
(T σ=0.01 = S3-E Kol T; A σ=0.01 = S3-E Kol A — tekrar koşulmaz.)

**Çıtalar:**
- **F1 (drift tezi):** T0 medyan ömür ≥ 250 VE hasat/1K ≥ 10 (oracle
  408/16.7'nin ~%60'ı; halefiyetin kendisine %40 pay). T0 da ≤ 150'de
  kalırsa drift DEĞİL: halefiyet sıfırlaması ya da M-05 erozyonu →
  sonraki basamak "yetiştirme kabı" varyantı (PL-06 gerilimi).
- **F2 (doz):** T2, T0 ile T(0.01) arasında; T0'a yakınsa (≥ 0.8×T0)
  σ=0.002 ekoloji için kabul edilebilir doz.
- **F3 (zaman çizgisi):** T0'da ömür/hasat penceresi nesille DÜŞMEZ
  (son 5K ≥ 0.8 × ilk 5K); düşerse erozyon σ-dışı.
- **A0:** A1/A2 yeniden test (daha uzun ömürlü nüfusta): çıtalar aynı
  (MI ≥ 0.05 bit MM + p<0.05; isabet > K(0.01) +0.05 ve kendi-ipucu
  tutarlılığı > 0.5+0.05).

**Öngörüler (bağlayıcı):** F1 geçer (0.75); T2 ≈ T0 (0.7); F3 geçer;
A0'da A1/A2 yine düşer (0.85) — ömür uzasa da kanal eğitilmemiş
sütunlardan rastgele yayın yapmaya devam eder; dil için yeterli
koşul ömür değil, sinyalin modelde sonucu olması.

**Sonuç matrisi:** F1✓ → σ ekoloji parametresi olarak 0 ya da 0.002'ye
çekilir (DP-01b "mutasyonlu tortu" fiilen "saf tortu" olur; kayıt
OPEN_LOOPS PL-31, Ali'ye görünür), sonra olay görevi uzun koşum (50K)
+ seçilim (a) basamağı. F1✗ → PL-06 yetiştirme kabı (ağırlık + hidden
taşıma?) ya da ekolojide öğrenmeyi dondurma ablasyonu (M-05 sınavı).

**Beyan (M-09):** σ=0 bir deneyci kararıdır; "ölüm gerçek" kuralının
ağırlık kısmını fiilen kaldırır (yaşantı değil yapı miras alınır, PL-06
tartışması). Bit sayılmaz; anayasal soru olarak Ali'ye işaretli.

## S3-F — SONUÇLAR: **drift tezi DOĞRULANDI; σ≤0.002'de ekoloji kararlı** (2026-10-18, gece)

Veri: `runs/s3f/`, özet `runs/s3f/summary.json`.

| kol | σ | medyan ömür | zaman çizgisi (5K→20K) | hasat/1K | sinyal oranı | ölüm/20K | yuva-sonu ölüm |
|---|---|---|---|---|---|---|---|
| T (S3-E) | 0.01 | 138 | 144→138 ↓ | 3.5-4.2 | 0.60 | ~640 | 0 |
| **T0** | 0.0 | **260** | 227-255→260-262 ↑ | 7.2-8.4 | **0.35** | ~325 | 13-17 (~5%) |
| **T2** | 0.002 | **266** | 223-253→262-267 ↑ | 8.1-9.4 | 0.39 | ~330 | 7-14 |
| A (S3-E) | 0.01 | 61 | — | 2.1-2.6 | 0.79 | ~1430 | 0 |
| **A0** | 0.0 | **83** | 76-87 düz | 9.3-10.2 | 0.71 | ~1095 | 0-1 |

- **F1:** ömür ✓ (260 ≥ 250), hasat ✗ (8 < 10). Kalan açık (260 vs
  oracle 408; 8 vs 16.7) halefiyetin kendisine (hidden/PER/optimizer
  sıfırlama + erken ölümler) ait; ön-kayıtta %40 pay bırakılmıştı,
  gerçek pay ~%40-50. Drift, erimenin BİRİNCİL nedeniydi.
- **F2 ✓:** σ=0.002 ≈ σ=0 (266 vs 260). Doz kabul edilebilir.
- **F3 ✓:** σ≤0.002'de ömür nesille DÜŞMÜYOR, hafif yükseliyor →
  soy hattı boyunca öğrenme birikebiliyor (ilk kez).
- **Yan bulgu (mekanizma):** sinyal oranı 0.60-0.79'dan **0.35'e**
  indi. S3 enstrüman şerhindeki mekanizma doğrulandı: tutarlı model →
  MPC sinyalden kaçınır; drift → skor manzarası gürültü → sinyal.
  Sinyal oranı hâlâ planlayıcı tutarlılığının ters vekili.
- **A0 (olay+kanal, σ=0):** ömür 61→83 ama isabet 0.20-0.22,
  **kendi-ipucu tutarlılığı 0.42 (şans 0.5'in ALTINDA)**, STAY payı
  0.27-0.31, I(ipucu;sembol) 0.0001-0.0007 bit (p: 0.02/0.36/0.26).
  **A1 ✗, A2 ✗.** Ajan öncüyü OKUMUYOR: olay anındaki eylem kendi
  ipucundan bağımsız. Dil sorusu henüz sorulamıyor; önce algı sorusu.
- **M-14 taban oranı:** 83 turluk ömürde olay deneyimi ≈ 2.7/yaşam.
  S2.7'de tek olumsallık için N*=50 deneyim gerekmişti. Yaşam içinde
  öğrenme matematiksel olarak imkânsız; soy hattında (σ≈0 ile ağırlık
  birikir) 20K turda ~667 olay/slot var ama isabet düz kaldı → sorun
  yalnız sayı değil, olayın modelde iz bırakmaması (ceza 25 = enerji
  sıçraması; S2.10'da enerji kafası sıçramaları %25-75 eksik tahmin
  ediyordu).

**Karar (oto-yetki, PL-31):** ekoloji varsayılanı σ=0.002 (DP-01b
"mutasyonlu tortu" korunur, drift etkisiz). σ=0 değil: seçilim (a)
için varyasyon gerekli. Ali'ye anayasal şerh: "ölüm gerçek" artık
bedene/yaşantıya uygulanıyor, yapıya değil (PL-06 gerilimi çözümü).

**Öngörü karnesi:** F1 (0.75) kısmen; T2≈T0 (0.7) ✓; F3 ✓; A0'da
A1/A2 düşer (0.85) ✓.

**Yeni ders var mı?** VAR, aday → **M-26 (taslak): Sürüklenme bir
cihaz hatası gibi davranır.** Seçilimsiz mutasyon, öğrenmeyle
kazanılan her şeyi nesil ölçeğinde siler ve bunu "ekoloji öğrenemiyor"
gibi gösterir; nüfus deneyinde σ, ağırlık RMS'ine göre ÖNCE kalibre
edilir (kritik nesil = (RMS/σ)²), sonra öğrenme yargılanır. (S3 ilk
nefesten S3-F'ye üç koşum bu yüzden yanlış katmana yazıldı.)
METODOLOJI'ye S3 kapanışında işlenir.

## S3-G — ÖN-KAYIT: olay görevi, doz ve süre merdiveni (koşumdan önce, M-08) (2026-10-18, gece)

**Soru.** σ=0.002 ile kararlı ekolojide alarm görevi: öğrenme için
sorun SÜRE mi (soy hattında birikim 20K'da yetmedi), DOZ mu (ceza 25
yaşamı 83'e indirip deneyimi 2.7/yaşam'a düşürüyor), yoksa ALGI mı
(öncü modelde iz bırakmıyor)? Üç kol, tek değişken (M-06), hepsi
klon kadro + yuva (600, 0.5) + σ=0.002:

| kol | olay | kanal | ceza | tur | soru |
|---|---|---|---|---|---|
| G1 | açık | açık | 25 | **50K** | süre |
| G2 | açık | açık | **10** | 20K | doz |
| G3 | açık | **kapalı** | 25 | 20K | A2 için kontrol (σ=0.002'de K) |

(G1'in ilk 20K'sı aynı zamanda A σ=0.002 referansıdır.)

**Çıtalar:**
- **G-algı:** herhangi bir kolda kendi-ipucu tutarlılığı > 0.55
  (şans 0.5) — ajan öncüyü eyleme çeviriyor. Son 10K penceresinde.
- **G-süre:** G1 son 10K isabet > ilk 10K isabet + 0.05.
- **G-doz:** G2 ömür ≥ 150 VE olay/yaşam ≥ 5 VE isabet > 0.25.
- **A1/A2 (dil):** değişmedi (MI ≥ 0.05 bit MM, p<0.05; A−K isabet
  > +0.05).

**Öngörüler (bağlayıcı):** G-algı DÜŞER tüm kollarda (0.7): sorun algı
katmanında (öncü, tehlike kanalında tek hücre; model onu enerji
sıçramasına bağlamıyor). G-doz: ömür ≥150 geçer, isabet > 0.25 düşer.
G-süre düşer. A1/A2 düşer (0.9).

**Sonuç matrisi:** hepsi ✗ → algı teşhisi: gözlemci probu
(`final_weights.pt` üzerinde: öncülü ve öncüsüz gözlemde tahmin
edilen enerji farkı; model öncüyü "görüyor" mu?) → sonra ya olay
kodlamasını değiştirmeden ceza/öncü-süre kalibrasyonu (dünya-tarafı)
ya da PL-27 (a) seçeneği (ayrı öncü kanalı, ~1-2 bit; Ali kararı,
anayasal). G-algı ✓ ama A1 ✗ → "görüyor, söylemiyor": sinyal-sonuç
zinciri teşhisi. A1 ✓ → ADAY GÖZLEM, Beş Kapı.

## S3-G — KISMİ SONUÇLAR (G2/G3 + algı probu; G1 50K sürüyor) (2026-10-18, gece)

Veri: `runs/s3g/G2_*`, `runs/s3g/G3_*`, prob `runs/s3g/probe_g23_*.json`
(`training/precursor_probe.py`).

| kol | ceza | kanal | medyan ömür | olay/yaşam | isabet | kendi-ipucu tutarlılık | STAY payı | hasat/1K |
|---|---|---|---|---|---|---|---|---|
| G2 | 10 | açık | **134** (125-135) | 4.5 | 0.20-0.21 | 0.41-0.43 | 0.33-0.41 | 9-10 |
| G3 | 25 | kapalı | **99.5** (96-103) | 3.3 | 0.20-0.23 | 0.41-0.45 | 0.15-0.26 | 12-14 |
| A0 (S3-F) | 25 | açık | 83 | 2.7 | 0.20-0.22 | 0.42 | 0.27-0.31 | 9-10 |

- **G-doz ✗:** ceza 10 ömrü 83→134 çıkarıyor ama isabet şans altında
  kalıyor; olay/yaşam 4.5 (çıta 5'in altında, N*=50'nin çok altında).
- **G-algı (davranışsal) ✗:** kendi-ipucu tutarlılığı her kolda 0.41-0.45
  < 0.5. Olay anındaki eylem kendi ipucundan BAĞIMSIZ.
- **A2 referansı:** kanal-kapalı G3 (99.5) vs kanal-açık A0 (83):
  kanal σ=0.002'de de net zarar; A σ=0.002 (G1) ile kesin karşılaştırma
  G1 bitince.
- **A1 ✗:** G2'de I(ipucu;sembol) 0.0-0.0007 bit, p 0.09-0.64.

### Algı probu — **model öncüyü GÖRÜYOR, ama eyleme bağlamıyor** (yeni teşhis)
Protokol: aynı seed'li iki dünya (öncülü / öncüsüz), 8 tur STAY ile
hidden'a işleme, olay turunda 6 eylem için tahmini enerji. 32 bağlam ×
30 çekirdek (6 koşum × 5 slot, ~120-180. nesil). Bilinen-negatif:
olay görmemiş transplant.

| | bilinen-negatif | G2 (ceza 10) | G3 (ceza 25) |
|---|---|---|---|
| ΔE ortalama (öncülü − öncüsüz) | **+0.00004** | **−0.028 … −0.058** | **−0.038 … −0.139** |
| eylem-koşullu yayılım (spread) | 0.0035 | 0.005-0.015 | 0.007-0.041 |
| kendi-ipucu hizası (argmax ∈ aday; şans 0.5) | 0.41 | 0.0-0.53 (ort. ~0.35) | 0.0-0.66 (ort. ~0.42) |
| güvenli-eylem farkı | 0.007 | −0.004 … +0.011 | −0.001 … +0.012 |

- **Öncü algılanıyor:** öncü varken olay turu için tahmin edilen
  enerji 30/30 çekirdekte düşüyor; etki büyüklüğü gürültü tabanının
  ~1000 katı ve CEZAYLA ÖLÇEKLİ (ceza 10 → ~−0.04; ceza 25 → ~−0.10 ≈
  beklenen 0.75×ceza/100 değerinin yarısı). Model "tehlike geliyor"u
  öğrenmiş — tehlike kanalındaki yalıtık öncü hücreyi gerçek
  tehlikeden ayırıp (öncü enerji çekmez) gelecek bir sıçramaya
  bağlamış. Bu, PL-27(c)'nin "ajan öncüyü kendisi ayıracak" bahsinin
  kısmen KAZANILDIĞI anlamına gelir (iç temsil ölçümü; davranış değil).
- **Ama eyleme bağlı DEĞİL:** yayılım küçük (ceza 25'te tabanın 2-10
  katı), kendi-ipucu hizası şans civarı, güvenli-eylem farkı sıfır.
  Yani öğrenilen şey "öncü ⇒ enerji düşecek" (eylemden bağımsız beklenti),
  öğrenilmeyen şey "ipucu ⇒ hangi eylem güvenli". Planlayıcı bu
  beklentiyle hiçbir şey yapamaz çünkü her eylem eşit kötü görünüyor
  → isabet şans. Kanal sorusu bu katmanın üstünde: ajan KENDİ bitini
  bile eyleme çeviremezken başkasının bitini talep etmesi beklenemez.
- **M-14 okuması:** (ipucu durumu × eylem) = 4×6 = 24 hücre; soy başına
  ~667 olay/20K → hücre başına ~28 örnek; ceza sıçraması enerji
  kafasında zayıf (S2.10: sıçramalar %25-75 eksik). Yetersiz ama
  umutsuz değil: ya daha çok örnek (sıklık ↑, ceza ↓, aynı basınç/tur),
  ya seçilim (küçük bir eylem-koşullu avantaj soy hattında çoğalsın).

## S3-H — ÖN-KAYIT: seçilim ve deneyim sıklığı (koşumdan önce, M-08) (2026-10-18, gece)

**Taban:** G1'in ilk 20K'sı (A, σ=0.002, ceza 25, her 30 tur, seçilimsiz).
İki kol, her biri tabandan TEK değişkenle ayrılır (M-06); 3 seed, 20K.

| kol | değişken | ayar |
|---|---|---|
| H1 | **seçilim (PL-22 a)** | `selection=max_age`: ölen slotun halefi, yaşayanlar arasında en uzun süredir hayatta olanın ağırlıklarından (+σ=0.002). Ajana bit gitmez; nüfus kuralı (M-09). |
| H2 | **deneyim sıklığı (M-14)** | `event_every=10, penalty=8`: beklenen kayıp/tur 0.80 (taban 0.83 — basınç sabit), olay sayısı 3× |

**Çıtalar (son 10K penceresi):**
- **H-algı:** kendi-ipucu tutarlılığı > 0.55 (şans 0.5) herhangi bir kolda.
- **H-sel:** H1 medyan ömür ≥ taban × 1.2 VE isabet > taban + 0.03.
- **H-dose:** H2 isabet > 0.25 VE olay/yaşam ≥ 10.
- **Prob:** `final_weights.pt` üzerinde kendi-ipucu hizası > 0.6 ya da
  güvenli-eylem farkı > 0.02 (taban 0.007) — iç temsilde eylem-koşullu iz.
- **A1 (dil):** değişmedi.

**Öngörüler (bağlayıcı):** H-sel ömür ✓ (seçilim hasat yetkinliğini
çoğaltır, 0.7), isabet ✗ (0.7). H-dose: olay/yaşam ≥10 ✓, isabet ✗
(0.6) ama prob yayılımı artar (0.6). H-algı ✗ (0.65). A1 ✗ (0.9).

**Sonuç matrisi:** ikisi de ✗ → eylem-koşullu öğrenme bu mimari/
ufukta kurulamıyor; ya 50K+ seçilim+sıklık birlikte (M-06 ihlali
değil: iki geçen/geçmeyen değişkenin birleşimi ayrı ön-kayıtla), ya da
Ali'ye anayasal soru (PL-27 a: ayrı öncü kanalı; ya da olay cezasının
eylem-koşullu yapısının gözlemde görünür olması — her ikisi bit yazar).
H-algı ✓ → kanal sorusu yeniden sorulabilir hâle gelir: seçilim/sıklık
ile 50K koşum + A/K karşılaştırması.

### S3-G tamamlandı — G1 (50K, süre) sonucu
| seed | medyan ömür 20K→50K | isabet 0-10K | 10-20K | 20-35K | 35-50K | kendi-ipucu | hasat/1K |
|---|---|---|---|---|---|---|---|
| 3001 | 81→85 | 0.194 | 0.217 | 0.239 | **0.247** | 0.462 | 5.6 |
| 3002 | 79→79 | 0.191 | 0.223 | 0.240 | **0.240** | 0.456 | 6.4 |
| 3003 | 82→87 | 0.211 | 0.231 | 0.246 | **0.258** | 0.471 | 5.0 |

- **G-süre: sınırda** (son 10K − ilk 10K = +0.053 / +0.049 / +0.047;
  çıta +0.05 → 1/3 harfen geçer, 3/3 tekdüze YÜKSELİYOR). Soy hattında
  (σ=0.002) olay isabeti yavaş ama kararlı artıyor: 50K'da şans altından
  şans üstüne (0.19 → 0.25). Kendi-ipucu 0.46 (0.42'den ↑, hâlâ < 0.5).
  Öğrenme VAR, hızı ~+0.015 / 10K; kendi-ipucu tavanı 0.50'ye bu hızla
  ~150K tur. Ömür 85'te düz, hasat 50K boyunca 9 → 5/1K DÜŞÜYOR (olay
  tetikte tutma hasadı yiyor; H2'deki donma eğiliminin yavaş hâli).
- **A2 (σ=0.002):** G1@20K isabet ≈ 0.22 vs G3 (kanal kapalı) 0.21,
  ömür 81 vs 99.5 → kanal yine net zarar, isabete katkı yok. **A2 ✗.**
- **A1 ✗:** MI 0.0002-0.0004 bit.

## S3-H — SONUÇLAR: **seçilim ✗, sıklık ✗; iç modelde ilk kıpırtı (n=1 seed)** (2026-10-18, gece)

Veri: `runs/s3h/`, `runs/s3h/summary.json`, prob `runs/s3h/probe_h*.json`.

| kol | medyan ömür | olay/yaşam | isabet | kendi-ipucu tutarlılık | STAY payı | hasat/1K | sinyal |
|---|---|---|---|---|---|---|---|
| taban A0 (σ=0, S3-F) | 83 | 2.7 | 0.20-0.22 | 0.42 | 0.27-0.31 | 9-10 | 0.71 |
| H1 seçilim (max_age) | **86** (85-89) | 2.9 | 0.22 | 0.44-0.45 | 0.25-0.34 | 8-10.5 | 0.70 |
| H2 sıklık (10/ceza 8) | **85** (80-87) | 8.5 | 0.22 | 0.43 | **0.38-0.47** | **5.7-6.8** | 0.61 |

- **H-sel ✗:** ömür +4% (çıta +20%), isabet +0.01 (çıta +0.03).
  Seçilim 20K'da davranışı değiştirmedi.
- **H-dose ✗:** isabet 0.22 (çıta >0.25), olay/yaşam 8.5 (çıta ≥10).
  Yan etki: STAY payı ve hasat düşüşü — sık öncü, "enerji düşecek"
  beklentisini sürekli açık tutuyor, planlayıcı donuyor (hasat %40 ↓).
  M-25 kaçış yolu (hep STAY) sıklıkla güçleniyor.
- **H-algı (davranış) ✗:** 0.43-0.45 her yerde.
- **A1 ✗:** MI 0.0-0.0007 bit.

### Algı probu (S3-H ağırlıkları)
| | H1_s3001 (5 çekirdek) | H1_s3002 | H2_s3001/2 |
|---|---|---|---|
| ΔE ortalama | −0.06 … −0.11 | −0.13 … −0.16 | −0.08 … −0.12 |
| kendi-ipucu hizası (32 bağlam) | **0.66 / 0.69 / 0.78 / 0.75 / 0.91** | 0.34-0.63 | 0.0-0.69 |
| güvenli-eylem farkı | **0.012-0.019** (taban 0.007) | 0.004-0.008 | 0.001-0.008 |

- H1_s3001'de beş çekirdeğin HEPSİNDE iç model kendi ipucuyla hizalı
  ve güvenli eylemi ayırıyor — ama bu beş çekirdek max_age seçilimiyle
  AYNI soydan (bağımsız gözlem sayısı ~1); H1_s3002'de yok. Davranışa
  (0.44) yansımıyor: ya etki planlayıcının CEM gürültüsünde kayboluyor
  (0.015 enerji farkı, ε ve 64 adaylık havuzda), ya da hizalanma
  olay turunda değil başka adımda. **Etiket: ÖN-GÖZLEM, aday gözlem
  bile değil** (n=1 soy); 96 bağlamlı tekrar aşağıda.
- **96 bağlam tekrarı:** H1_s3001 beş çekirdek hizası 0.59 / 0.60 /
  0.80 / 0.79 / 0.95 (binom p: 0.04 … <1e-8), güvenli-eylem farkı
  0.011-0.017 (taban 0.007). H1_s3003: 0.52-0.59, güvenli-eylem farkı
  NEGATİF (−0.001 … −0.005). H1_s3002 (32 bağlam): 0.34-0.63.
  **Hüküm: 3 soydan 1'inde iç modelde eylem-koşullu ipucu izi → ADAY
  GÖZLEM (en fazla).** Davranışa yansımıyor (0.44). İkiz kontrolü (M-04)
  SONRADAN KOŞULDU (`--twins 8`, `runs/s3h/probe_twins.json`): rastgele-
  init ikizlerde hiza {0, 0.45, 0.55} (dejenere argmax), %95 üst sınır
  0.552; güvenli-eylem farkı p95 0.006; yayılım p95 0.0025. H1_s3001'in
  üç çekirdeği (0.80/0.79/0.95; fark 0.011-0.017) ikiz sınırının açık
  üstünde, ikisi (0.59/0.60) sınırda. **M-04 kapısı: GEÇTİ (bu soy
  için).** Kalan kapılar: tekrar (bağımsız seed'lerde 1/3), zaman
  çizgisi (hangi nesilde doğdu — ağırlık anlık kaydı yok), davranışa
  nakit (0.44, ✗). Etiket ADAY GÖZLEM'de kalır.

**Öngörü karnesi:** H-sel ömür ✓ tahmini → YANLIŞ (ömür artmadı);
H-sel isabet ✗ → doğru; H-dose olay/yaşam ≥10 → YANLIŞ (8.5); isabet
✗ → doğru; prob yayılımı artar → kısmen (H1'de); H-algı ✗ → doğru.

**Sonuç matrisi hücresi: ikisi de ✗.** Ön-kayıt iki yol veriyordu:
birleşik 50K ya da anayasal soru. **Karar (Ali yetki devri, 18 Ekim
gecesi: "sen ver kararı"):** anayasal adımdan ÖNCE atlanmış 0-bitlik bir
dünya-tarafı kalibrasyon var — **uyarı öncesi süre** `event_lead`.
Gerekçe: prob modelin öncüyü gördüğünü söylüyor; eksik olan 8 tur
sonrasını DOĞRU TURDA planlamak (10 turluk hayal ufkunun 8. adımı; S2.10
H_eff ölçümleri rollout güvenilirliğinin birkaç adımda eridiğini
göstermişti, M-17). lead=8 S3-C oracle kalibrasyonundan geldi, scripted
ajan için zamanlama bedava idi; öğrenen ajan için değil (M-21). Kanal
için 2 tur yeterli (sinyal aynı tur duyulur, sonraki gözlemde görülür,
olay turunda eyleme döner — zamanlama testi: lead=2'de öncü 2 gözlemde
görünür). Önce bu, sonra gerekirse PL-27(a).

## S3-I — ÖN-KAYIT: uyarı penceresi (event_lead) merdiveni (koşumdan önce, M-08) (2026-10-18, gece)

**Tek değişken:** `event_lead` ∈ {2, 4}; taban lead=8 (A0/G1). Diğer
her şey: klon + yuva (600, 0.5) + σ=0.002 + ceza 25 + her 30 tur +
kanal açık + seçilimsiz. 3 seed, 20K. **0 prior biti** (dünya-tarafı
zamanlama; KERNEL_BUDGET S3-I notu).

**Çıtalar (son 10K):**
- **I-algı:** kendi-ipucu tutarlılığı > 0.55 (ilk kez şansın üstü).
- **I-isabet:** isabet > 0.30 (şans ~0.20-0.25; kendi-ipucu tavanı 0.50).
- **I-ömür:** medyan ömür > taban (83) × 1.15.
- **A1/A2 (dil):** aynı (MI ≥ 0.05 bit; A − K isabet > +0.05 — K için
  lead=2 kanal-kapalı kolu, I-algı geçerse koşulur).
- **Prob:** kendi-ipucu hizası > 0.6 (≥2 seed), güvenli-eylem farkı > 0.02.

**Öngörüler (bağlayıcı):** lead=2'de I-algı GEÇER (0.6) — zamanlama
yükü kalkınca iç modeldeki iz davranışa dönebilir; lead=4 arada.
I-isabet lead=2'de 0.30'u geçer (0.5). A1 yine düşer (0.85): kendi
bitini kullanmak kanaldan bağımsız; kanal için lead=2 tek-tur pencere
dar, lead=4 kolu kanal sorusunun asıl adayı.

**M-25:** lead kısalması kaçış yolu açmaz (acıdan öğrenme kilidi
event_duration=1 duruyor; kendi-ipucu tavanı 0.5 değişmez).
**Sonuç matrisi:** I-algı✓ → kanal sorusu yeniden açılır: lead=4'te
A/K karşılaştırması 50K (S3-J). I-algı✗ (lead=2'de bile) → zamanlama
değil, eylem-koşullu enerji öğrenmesi engelli → anayasal merdiven:
(1) PL-27(a) ayrı öncü kanalı (~1-2 bit), (2) enerji kafasına olay
turu için ayrı çıkış (~2 bit, M-18 sınırında).

## S3-I — SONUÇLAR: **lead ✗ — zamanlama darboğaz değil** (2026-10-18, gece)

Veri: `runs/s3i/`, `runs/s3i/summary.json`, prob `runs/s3i/probe_l.json`.

| lead | medyan ömür | isabet | kendi-ipucu | STAY payı | hasat/1K | sinyal | prob yayılım | prob hiza |
|---|---|---|---|---|---|---|---|---|
| 8 (A0/G1) | 83 | 0.20-0.22 | 0.42-0.46 | 0.27-0.31 | 9-10 | 0.71 | 0.005-0.015 | ~0.4 |
| **4** | 84 (79-88) | 0.21-0.24 | 0.43-0.45 | 0.22-0.31 | 8-10 | 0.73 | 0.02-0.05 | 0.02-0.52 |
| **2** | 90 (86-90) | 0.20-0.21 | 0.41-0.42 | 0.33-0.37 | 9-11 | 0.70 | 0.02-0.05 | 0.03-0.63 |

- **I-algı ✗, I-isabet ✗, I-ömür ✗** (90 < 95). Öncü ile olay arası
  2 tura inince bile eylem kendi ipucundan bağımsız. **Öngörüm (I-algı
  lead=2'de geçer, 0.6) YANLIŞ.**
- Prob: eylem-koşullu yayılım 3× büyüdü (model olay turunda eylemler
  arasında ARTIK ayrım yapıyor) ama hiza şans, güvenli-eylem farkı ~0:
  ayrım ipucuyla İLİŞKİSİZ (muhtemelen hareket/STAY maliyet farkı).
- **Teşhis daralıyor:** bellek/zamanlama değil; "ipucu değeri ⇒ hangi
  eylem cezasız" eşlemesi enerji kafasında kurulmuyor. G1 50K'daki
  yavaş yükseliş (0.19→0.25) bunun çok yavaş kurulduğunu söylüyor.

**Sonuç matrisi hücresi: I-algı ✗ → anayasal merdiven.** Ama anayasayı
değiştirmeden önce bir ölçüm daha (M-01/M-22, karar Claude — Ali yetki
devri): **öğrenilebilirlik TAVANI**. Ekolojide 5 ajan + ölüm + kanal +
rekabet varken "öğrenemiyor" demek, tek ajanın sınırsız zamanla
öğrenip öğrenemediği bilinmeden eksiktir (M-02: önce dünyayı/aparatı
yargıla). Tavan şans düzeyindeyse sorun ekoloji değil, öğrenme sinyali
ya da mimaridir ve en ucuz anayasal adım ayrı öncü kanalı DEĞİL, K-106
(enerji loss ağırlığı) revizyonudur.

## S3-J — ÖN-KAYIT: "olay okulu", tek ajan öğrenilebilirlik tavanı (koşumdan önce, M-08) (2026-10-18, gece)

`training/event_school.py`: tek ajan, yetiştirme kabı rejimi (PL-06:
ölüm bedeni sıfırlar, ağırlık sürer, σ=0), kanal KAPALI, olay her 10
tur, lead=2, ceza 25, 100K tur (≈10K olay deneyimi — N*=50'nin 200
katı). Pencere 10K.

| kol | değişken | seed |
|---|---|---|
| J-base | roster A2 config (λ_enerji=10, lr=5e-4) | 3 |
| J-λ30 | `energy_loss_weight` 10 → 30 (K-106 revizyon adayı, ~1 bit) | 3 |

**Çıtalar (son 20K penceresi):**
- **J-öğrenir:** kendi-ipucu > 0.55 VE isabet > 0.30.
- **J-λ:** J-λ30, J-base'den ≥ +0.05 kendi-ipucu önde.
- Prob (final ağırlık): hiza > 0.6, güvenli-eylem farkı > 0.02.

**Öngörüler (bağlayıcı):** J-base yavaş öğrenir, 100K sonunda kendi-ipucu
0.50-0.60 (çıtada), 0.5 olasılık; J-λ30 daha hızlı (0.6). İkisi de ✗
kalırsa (0.3): mimari/planlayıcı engeli → PL-27(a) ya da enerji
kafası revizyonu; ikisi de anayasal, deftere yazılır.

**Sonuç matrisi:** J-base ✓ → ekoloji sorunu "zaman × gürültü"dür;
ekolojide 100K+ koşum + seçilim (S3-K). J-base ✗, J-λ30 ✓ → K-106
revizyonu (λ=30, ~1 bit; M-19 doğum günü kapısından geçer: init'te
isabet şans olmalı) → ekolojiye taşı. İkisi ✗ → anayasal merdiven
basamak 2 (öncü kanalı / enerji kafası), Ali'ye sabah raporunda açık.

**Beyan:** okul kanal-kapalıdır (kendi-ipucu sorusu); "ölüm gerçek"
askıda (S1 emsali, ekoloji iddiası değil tavan ölçümü).

## S3-J — SONUÇLAR: **TEK AJAN KENDİ İPUCUNU ÖĞRENİYOR (6/6 seed)** (2026-10-19, gece)

Veri: `runs/s3j/*/school.json`, prob `runs/s3j/probe_school.json`.

| kol | seed | kendi-ipucu 10K→100K (10K pencereleri) | isabet son 20K | STAY | ölüm/10K |
|---|---|---|---|---|---|
| base | 0 | 0.44 → 0.50 → 0.60 → 0.76 → 0.82 → 0.85 → … → **0.87** | 0.44-0.45 | 0.44 | ~185 |
| base | 1 | 0.47 → 0.51 → 0.58 → 0.70 → 0.80 → 0.84 → … → **0.87** | 0.42-0.43 | 0.46 | ~188 |
| base | 2 | 0.49 → 0.53 → 0.66 → 0.78 → 0.81 → 0.84 → … → **0.86** | 0.39-0.45 | 0.47 | ~185 |
| λ30 | 0-2 | 0.41-0.49 → … → **0.84-0.88** | 0.43-0.45 | 0.45-0.48 | ~187 |

- **J-öğrenir ✓ (6/6):** kendi-ipucu tutarlılığı şans (0.5) → 0.86; isabet
  0.23 → 0.44, kendi-ipucu tavanına (0.50) yaklaşıyor. Eşik (0.55)
  ~25-30K turda (≈2.5-3K olay deneyimi); plato ~60K.
- **J-λ ✗:** λ=30 ≈ λ=10 (fark < 0.02). Öğrenme sinyali darboğaz DEĞİL
  → **K-106 revizyonu gerekmiyor; anayasal adım atılmadı (0 bit).**
- **Prob:** güvenli-eylem farkı 0.019-0.024 (ikiz p95 0.006; çıta 0.02
  ✓), yayılım 0.04-0.07 (taban 0.0025), hiza 0.53-1.0 (prob protokolü
  lead=8 ile koşuyor, okul lead=2 — hiza ölçüsü protokol-uyumsuz, fark
  ölçüsü esas).
- **Ölüm rejimi okulda da sertti** (~53 turda bir beden sıfırlama); yine
  de öğrendi → "ölüm gerçek" ağırlık sürdükçe öğrenmeyi engellemiyor.
  **Ekolojideki tıkanıklık mimari değil: olay DENEYİMİ sayısı × (lead 8,
  her 30 tur, drift, rekabet).** G1 50K'daki yavaş yükseliş bununla
  tutarlı: 50K × (1/30) ≈ 1.7K olay/soy, okulun eşiğinin altında.
- **Öngörü karnesi:** J-base yavaş öğrenir, 100K'da 0.50-0.60 → YANLIŞ
  yönde iyimser çıktı (0.86); J-λ30 daha hızlı → YANLIŞ (eşit).

**Yeni ders var mı?** VAR → **M-27 (taslak): Ekolojiyi yargılamadan
önce tek-ajan tavanını ölç.** "Nüfus öğrenemiyor" teşhisi, aynı
görevi tek ajanın sınırsız deneyimle öğrenip öğrenemediği ölçülmeden
eksiktir; tavan şans düzeyindeyse mimari, değilse ekolojik parametre
sorunudur. (S3-G/H/I üç basamak bu ölçüm olmadan harcandı; okul 25
dakikada ayırdı. M-01/M-02/M-21'in nüfus-öncesi özel hâli.)

## S3-K — ÖN-KAYIT: DİL TUZAĞI, kurulu hâliyle (koşumdan önce, M-08) (2026-10-19, gece)

**Mantık.** Tek ajan kendi bitini öğreniyor (S3-J) → isabet tavanı 0.50.
Tavanı aşmanın TEK yolu başkasının biti = kanal. Ekoloji okulun
öğrenme koşullarına yaklaştırılır (olay sıklığı, lead), kanal açık/kapalı
karşılaştırılır. H3/H4 için ilk gerçek test.

**Ayar:** klon kadro, yuva (600, 0.5), σ=0.002, seçilimsiz, olay **her 10
tur**, **lead=4** (kanal için zaman payı: gör → yayınla → duy → eyle),
ceza 25, K=4, kanal küresel, **100K tur**, 3 seed. Kollar: **K-A** kanal
açık, **K-K** kanal kapalı (mute). Beklenen basınç: şansta 1.9 enerji/
tur kayıp → ömür kısa (~40-60), soy hattı öğrenir (okul emsali).

**Çıtalar (son 20K penceresi, ≥2/3 seed):**
- **K1 (kendi-ipucu ekolojide):** K-K kendi-ipucu > 0.70, isabet > 0.40.
  (Okul 0.86/0.44'e ulaştı; ekolojiye %20 pay.)
- **K2 (kanal fayda — H3/H4 kapısı):** K-A isabet > K-K isabet + 0.05 VE
  K-A isabet > 0.50 (kendi-ipucu TAVANININ üstü — ancak başkasının
  bitiyle mümkün).
- **K3 (sembol-ipucu olumsallığı):** I(ipucu; sembol) ≥ 0.05 bit (MM,
  perm p < 0.05) — konuşan var mı.
- **K4 (dinleyen var mı):** uyarı penceresinde sinyal duyan ajanların
  isabeti, duymayanlardan +0.05 yüksek (küresel kanal + yüksek sinyal
  oranında "duymadı" kümesi boş kalabilir — o zaman ölçülemez, M-03).
- **K5 (maliyet):** K-A ömrü ≥ 0.9 × K-K (kanal net zarar vermiyor).

**Öngörüler (bağlayıcı):** K1 ✓ (0.7). K2 ✗ (0.7): kanal hâlâ ε-gürültüsü
(16/17) + eğitilmemiş sütunlar; sinyalin modelde sonucu olması için
alıcının duyduğu sembolü kendi enerji tahminine bağlaması gerekir —
100K'da belki başlar. K3: MI 0.01-0.03 bit (çıtanın altı, tabanın üstü;
0.5). K4 ölçülemez (0.6). K5 ✗ (0.6).

**Sonuç matrisi:**
- K1✓ K2✗ K3✗ → tuzak kurulu ama dil doğmadı (BEKLENEN): H3/H4 için
  "bu koşullarda, 100K turda negatif"; S3 kapanışı bu hükümle yazılır,
  sonraki merdiven (300K+, seçilim, ε-sinyal payı) Ali'ye önerilir.
- K1✓ K3✓ K2✗ → "konuşan var, dinleyen yok" → ADAY GÖZLEM (H4 yönünde
  sembol-dünya olumsallığı); alıcı tarafı teşhisi.
- K1✓ K2✓ → ADAY GÖZLEM güçlü; Beş Kapı: K-K ablasyonu (hazır), ikiz,
  bit-eş tekrar, zaman çizgisi (pencere), KERNEL_BUDGET (0 yeni bit).
  İDDİA Ali ile.
- K1✗ → ekoloji okul koşullarında bile öğrenemiyor → rekabet/ölüm
  sıfırlaması teşhisi, S3 kapanışı "ekolojik negatif".

**M-25 kaçış yolları:** hep-STAY (%25 → şimdi ölçülüyor: STAY payı);
"öl ve yuvaya dön" (PL-29: ölüm sayısı raporlanır); sinyalin
maliyetsizleşmesi yok (0.5, yuva yarıya indirir, beyanlı).

## S3-K — SONUÇLAR: **kanal-kapalı ekoloji kendi ipucunu öğreniyor; kanal öğrenmeyi yavaşlatıyor; dil doğmadı** (2026-10-19, sabah)

Veri: `runs/s3k/{KA,KK}_s300{1,2,3}/breath.json` (100K tur), özet
`runs/s3k/summary.json`, prob `runs/s3k/probe_k.json`.

| kol | medyan ömür | isabet 0-20K → 40-60K → **80-100K** | kendi-ipucu (kümülatif) | STAY | hasat/1K | sinyal | ölüm/100K |
|---|---|---|---|---|---|---|---|
| **K-K** kanal kapalı | 42 | 0.22 → 0.26 → **0.30 / 0.31 / 0.31** | 0.51-0.54 | 0.30 | 5.7-6.2 | 0 | ~10.6K |
| **K-A** kanal açık | 40 | 0.22 → 0.24 → **0.24 / 0.24 / 0.25** | 0.47-0.48 | 0.21-0.28 | 3.6-4.5 | 0.72-0.81 | ~12.1K |

- **K1 (kendi-ipucu ekolojide): harfen ✗, yönde ✓.** Kanal-kapalı
  ekolojide isabet 3/3 seed'de tekdüze yükseliyor (0.22 → 0.31; şans
  ~0.22, tavan 0.50); kümülatif kendi-ipucu 0.53 (başlangıç 0.45 →
  son pencere tahmini ~0.6; pencere sayacı enstrümanda yoktu — eklendi).
  Çıta (0.70 / 0.40) 100K'da ulaşılmadı; okulun 0.86/0.44'üne ekoloji
  ~3× daha yavaş gidiyor (ölüm her ~42 turda hidden/PER sıfırlar, 5
  rakip, σ=0.002). **Ekoloji öğreniyor; yalnız yavaş.**
- **K2 ✗ (ters yönde):** K-A isabeti K-K'nın 0.06 ALTINDA; kanal
  açıkken kendi-ipucu öğrenmesi 100K boyunca başlamıyor (0.24 düz).
- **K3 ✗:** I(ipucu;sembol) 0.0003-0.0005 bit (p=0: n≈300K sinyal;
  etki gürültü tabanının altında), H(sembol) 3.98-3.99/4. Uyarı
  penceresinde sinyal oranı (0.72-0.82) genel oranla aynı. **Konuşan
  yok.**
- **K4 ölçülemez:** duyma payı 1.0 (M-03; "duymadı" kümesi 2-3 olay).
- **K5 ✓ harfen (40 ≥ 0.9×42), ✗ ruhen:** hasat %30 düşük, ölüm %14
  fazla; kanal net maliyet.
- **Prob (K-K soyları):** güvenli-eylem farkı 0.012-0.028 (ikiz p95
  0.006; çıta 0.02'yi 4/10 çekirdek geçiyor), hiza 0.6-0.8 çoğunlukta.
  K-A: karışık (0.38-0.73), fark 0.00-0.016. Okul deseniyle tutarlı.

**Mekanizma (kanal neden öğrenmeyi yavaşlatıyor; hipotez, ölçülmedi):**
(i) ortak planlama 64 adayı eylem×sinyal uzayına (6×17) yayıyor →
eylem araması seyreliyor (K-111'in tersi), (ii) alınan 16 + efferens
17 boyutluk anlamsız girdi, enerji tahmininin ipucu hücrelerine
odaklanmasını zorlaştırıyor (gürültü), (iii) sinyal maliyeti ömrü
kısaltıp öğrenme penceresini daraltıyor. Ayırt edici deney: "yalnız
duy" (sinyal gönderimi kapalı, alım açık) ve "yalnız konuş" kolları
(S3-L, ön-kayıt aşağıda — koşulmadı).

**Öngörü karnesi:** K1 ✓ (0.7) → harfen yanlış, yönde doğru; K2 ✗
doğru (ve ters yön sürpriz); K3 0.01-0.03 bit → gerçek 0.0003
(daha da düşük); K4 ölçülemez doğru; K5 ✗ beklenirken harfen geçti.

**Yeni ders var mı?** YOK (kapsıyor): M-27 + M-21. Kanal-açık kolun
öğrenmeyi yavaşlatması S3-D/E'de ölçülen "kanal boğuyor" bulgusunun
öğrenme-hızı yüzü.

---

# S3 KAPANIŞ RAPORU (2026-10-19)

## Hükümler (H1-H4) — kanıtla

| H | Hipotez | Hüküm | Kanıt | Etiket |
|---|---|---|---|---|
| **H1** | Ölümlü + eyleyen tahmin makinesi öz-model geliştirir | **Karışık, çoğunlukla NEGATİF** | Uzamsal yol entegrasyonu: negatif/karıştırılmış (S2, PL-13; hareketsiz rejim M-03). Tek-adım öz-hareket: yerellik iskelesiyle KAZANILDI (S2.10, K-113, M-19 geçti). İnteroseptif öz-enerji: varyans-eşleşmiş kontrolde DÜŞTÜ (S2.10-ek, PL-15). | Negatif (yol entegrasyonu), kazanılmış (öz-hareket, iskeleli), düşmüş (öz-enerji) |
| **H2** | Opaklık + koordinasyon → karşılıklı modelleme | **TEST EDİLMEDİ** | Ön koşul (iletişimin doğması) sağlanmadı; P2 probu açılmadı (M-07: P1 pozitif kontrolü yok). | Açık |
| **H3** | Kısıtlı kanal sinyali içselleştirir | **TEST EDİLEMEDİ → ön koşul NEGATİF** | İçselleştirilecek bir sinyal kullanımı doğmadı (S3-E…K). | Ön koşul negatif |
| **H4** | Asimetrik bilgi + kanal kıtlığı proto-gramer doğurur | **NEGATİF (bu koşullarda, 100K tur)** | Tuzak kuruldu ve oracle'dan geçti (S3-C). Öğrenen ekolojide: ajanlar kendi ipucunu öğreniyor (okul 0.86; ekoloji 100K'da 0.31 isabet ↑), ama kanal ipucu bilgisi TAŞIMIYOR (MI ≤ 0.0005 bit, 15 koşum), kanal açıkken öğrenme YAVAŞLIYOR, kanal net maliyet. Sembol entropisi tavanda. | Negatif, mekanizmalı |
| **H0** | Her şey reaktif hesaplama | **Çürütülmedi** | Hiçbir pozitif bulgu Beş Kapı'dan geçmedi. Tek aday gözlem: iç modelde eylem-koşullu ipucu izi (S3-H, 1/3 soy; M-04 geçti, tekrar ✗). | Ayakta |

## Ne öğrendik (mekanizma zinciri, geceden)
1. **Drift öğrenmeyi siliyordu** (σ=0.01, 65. nesil) → σ=0.002 ile
   ekoloji ilk kez kararlı (138 → 266 tur). [S3-E/F, M-26]
2. **Yuva ömrü uzatır, yeterlilik kurmaz**; f≤0.25 uçurum. [S3-D]
3. **Kanal, eğitilmemiş klonu boğar** (%77 rastgele sinyal, maliyet +
   gürültü): 118 → 78 tur. [S3-D]
4. **Model öncüyü görüyor** (ΔE cezayla ölçekli, 30/30 çekirdek) ama
   başta eyleme bağlamıyor. [S3-G prob]
5. **Tek ajan kendi ipucunu ÖĞRENİYOR** (6/6, 0.86), λ revizyonu gerekmez;
   darboğaz ekolojik: deneyim × ölüm × gürültü. [S3-J, M-27]
6. **Kanal-kapalı ekoloji de öğreniyor** (yavaş); **kanal açıkken
   öğrenemiyor**. Kanal şu hâliyle iletişim aracı değil, gürültü +
   maliyet. [S3-K]
Doz (ceza), zamanlama (lead), seçilim (20K), sıklık: tek başına hiçbiri
davranışı değiştirmedi. [S3-G/H/I]

## Neden dil doğmadı (dürüst teşhis)
Kanalın kullanılması için alıcının "duyduğum sembol ⇒ enerjim" zincirini,
göndericinin "ipucum ⇒ sembolüm ⇒ (başkasının eylemi ⇒) benim enerjim"
zincirini öğrenmesi gerekir. İkincisi DOLAYLIDIR: göndericinin sinyali
kendi enerjisini doğrudan etkilemez (küresel olay, kişisel ceza); fayda
ancak karşılıklılıkla döner. Ödül yok, akrabalık yok, tekrarlanan eş
yok (küresel kanal, kimliksiz). Bu koşullarda sinyal göndermenin
bireysel beklenen değeri ≤ 0 → MPC sinyalden kaçınır (tutarlı modelde
0.35'e düşen sinyal oranı tam bunu gösterdi). **Tuzağın eksik dişlisi:
göndericiye dönen fayda.** Alarm çağrısının ekolojik emsali akrabalık
seçilimi/karşılıklılıkla çalışır; burada ikisi de yok. Bu, anayasal
bir tasarım sorusudur (seçilim (a) soy düzeyinde bunu sağlayabilir:
paylaşan soylar daha çok çoğalır).

## Ali adına verilen kararlar (18-19 Ekim gecesi; her biri defterde)
| karar | nerede | bit |
|---|---|---|
| Yuva (600, 0.5), kanal açık | PL-22, KERNEL S3-D | 0 |
| σ=0.002 ekoloji varsayılanı | PL-31 | 0 (DP-01b dozu) |
| event_lead/every/penalty/selection parametrik, koşuldu | S3-G/H/I ön-kayıtlar | 0 (dünya-tarafı) |
| λ_enerji revizyonu YAPILMADI (okul gereksiz gösterdi) | S3-J | 0 |
| Anayasal adım (öncü kanalı) ATILMADI | S3-I/J | 0 |
**Toplam yeni prior: 0 bit.** KERNEL_BUDGET değişmedi.

## Beş Kapı durumu (pozitif iddia yok)
Tek aday gözlem (iç modelde eylem-koşullu ipucu izi): M-04 ikiz ✓,
tekrar ✗ (1/3 soy; S3-K'da K-K soylarında daha yaygın ama n=2 seed
probe), zaman çizgisi ✗ (ağırlık anlık kaydı yok), nakit ✗ (davranış
0.31/0.5), bütçe ✓ (0 bit). **İDDİA yok.**

## Sıradaki merdiven (öneri; Ali kararı)
- **S3-L (0 bit, ayırt edici):** "yalnız duy" / "yalnız konuş" kolları —
  kanalın öğrenmeyi neden yavaşlattığını ayırır (planlayıcı seyrelmesi
  mi, girdi gürültüsü mü, maliyet mi).
- **S3-M (0 bit, uzun):** K-K 300K+ → kendi-ipucu tavanına (0.5) ulaşma;
  sonra kanal AÇILIR (kademeli: PL-08 emsali) — tavandaki ajan için
  başkasının biti tek kazanç yolu.
- **S3-N (anayasal, seçilim (a) soy düzeyi):** "paylaşan soy çoğalır"
  — göndericiye dönen faydayı nüfus dinamiğiyle yaratmak; ödül değil,
  demografi. Deneyin ruhuna en yakın anayasal adım.
- Sonra H2/P2.

## Yeni ders var mı?
M-26, M-27 işlendi. Ek aday: **"Tuzağın geri dönüş yolunu kur"** —
sinyalin göndericiye beklenen değeri hesaplanmadan (M-25'in gelir
tarafı) kanal basıncı doğmaz. S3-N kararıyla birlikte M-28 olur.

## S3-L — ÖN-KAYIT: kanal neden öğrenmeyi yavaşlatıyor? (koşumdan önce, M-08) (2026-10-19, sabah)

**Soru (PL-32).** S3-K'da kanal açıkken kendi-ipucu öğrenmesi başlamadı.
Üç aday mekanizma, iki ablasyonla ayrılır (0 bit; M-06):

| kol | gönderir | duyar | planlayıcı | ayırdığı mekanizma |
|---|---|---|---|---|
| K-K (S3-K) | ✗ | ✗ | eylem-only | taban |
| K-A (S3-K) | ✓ | ✓ | ortak (6×17) | hepsi |
| **L-hear** | ✗ | ✓ | eylem-only | yalnız GİRDİ GÜRÜLTÜSÜ (16 boyut alınan sinyal; ama kimse konuşmadığı için alınan vektör pratikte sıfır → bu kol "duyma yolu açık ama boş" kontrolüdür; K-K'ya eşit çıkmalı — CİHAZ kontrolü) |
| **L-speak** | ✓ | ✗ | ortak (6×17) | planlayıcı seyrelmesi + sinyal maliyeti (girdi gürültüsü yok) |

Not: L-hear'da gönderen yoksa alınan sinyal yoktur; gerçek "girdi
gürültüsü" kolu için konuşan-ama-öğrenmeyen bir gürültü kaynağı
gerekir (sonraki basamak, gerekirse). Bu turda L-speak asıl kol.

**Ayar:** S3-K ile aynı (klon, yuva, σ=0.002, her 10 tur, lead 4, ceza
25, 100K, 3 seed).

**Çıtalar (80-100K penceresi):**
- **L1:** L-hear isabet ≈ K-K (|fark| < 0.03) — cihaz kontrolü.
- **L2:** L-speak isabet < K-K − 0.03 → yavaşlamanın kaynağı GÖNDERME
  tarafı (planlayıcı seyrelmesi ve/veya maliyet). L-speak ≈ K-K →
  kaynak ALMA tarafı (girdi gürültüsü) → gürültü-kaynağı kolu gerekir.
- **L3 (ayrıştırma):** L-speak'te sinyal oranı ve ömür; ömür ≈ K-A ise
  maliyet, planlayıcı seyrelmesini ayırmak için ileride "ortak
  planlayıcı + maliyet 0" kolu (M-06).

**Öngörüler (bağlayıcı):** L1 ✓ (0.85). L2: L-speak < K-K (0.7) —
seyrelme + maliyet birlikte.

## S3-N — ÖN-KAYIT: tuzağın eksik dişlisi — paylaşılan olay kaybı (koşumdan önce, M-08) (2026-10-19, sabah)

**Karar (PL-33; Claude, Ali yetki devri).** S3 kapanış teşhisi: sinyal
vermenin göndericiye dönen faydası yok → öğrenen sistem seçmez.
Seçenekler: (a) soy-düzeyi seçilim ("başkasının isabeti"ni uygunluğa
yazmak = nüfus düzeyinde ödül şekillendirme, reddedildi), (b) **olay
kaybının paylaşılması** (fizik; sürü savunması emsali: sürüde biri
doğru kaçarsa herkesin riski düşer), (c) yerel/tekrarlı eş (PL-28'i
geri alır). **(b) seçildi:** `WorldConfig.event_share=s`,
kayıp_i = ceza × [(1−s)·ıska_i + s·ortalama_ıska]. s=0 bit-eş (test).
Ajana bit yazmaz; görev semantiği değişir (beyan: "alarm çağrısı"
artık "sürü alarmı"). s=0.5: kendi eylemi hâlâ yarı ağırlıkta
(bedavacılık kaçışı sınırlı, M-25), diğerlerinin isabeti diğer yarıyı
belirler → sinyalin göndericiye beklenen değeri > 0 olur ANCAK
alıcılar kullanırsa.

**Basamak 1 — oracle (M-01, önce cetvel):** `training/event_oracle.py
--share 0.5`, n=5, menzil 32, 48 epizot: `deaf/own/told/god` merdiveni.
- **N1:** told kişi-başı ömrü > own × 1.15 (paylaşımda kanalın değeri
  var; s=0'da 193 vs 142 = 1.36 idi — paylaşım bunu azaltmamalı).
- **N0 (cihaz):** s=0.5'te deaf ömrü s=0'dakine yakın (±%20): paylaşım
  toplam basıncı değiştirmez, dağıtır.

**Basamak 2 — ekoloji:** S3-K ayarı (her 10 tur, lead 4, σ=0.002, klon,
yuva) + s=0.5; kollar **N-A** (kanal açık) ve **N-K** (kapalı); 3 seed,
100K.
- **N2 (kanal fayda):** N-A isabet > N-K + 0.05 (son 20K).
- **N3 (konuşan):** I(ipucu;sembol) ≥ 0.05 bit MM, p<0.05.
- **N4 (kanal öder):** N-A ömür ≥ N-K.
- **N5 (bedavacılık, M-25):** N-K isabeti K-K'dan (0.31) çok düşmemeli
  (≥ 0.26); düşerse paylaşım kendi-ipucu öğrenmesini söndürüyor.

**Öngörüler (bağlayıcı):** N1 ✓ (0.8). N2 ✗ (0.65): fayda artık var ama
alıcı "duyduğum sembol ⇒ eylem" zincirini 100K'da kurmayabilir;
gönderici için fayda ancak alıcı öğrenince doğar (tavuk-yumurta;
kırılma seçilimle ya da çok uzun koşumla). N3: MI 0.005-0.03 (0.5).
N5 ✓ (0.6).

**Sonuç matrisi:** N2✓ N3✓ → ADAY GÖZLEM (H4 yönünde), Beş Kapı +
Ali. N2✗ N3✗ N5✓ → "fayda var, zincir kurulmuyor": tavuk-yumurta →
S3-O: alıcı tarafını kıran 0-bit basamak (kanal kademeli: önce K-K
300K ile kendi-ipucu tavanı, sonra kanal aç). N5✗ → paylaşım dozunu
0.25'e çek.

### S3-N basamak 1 — oracle (s=0.5, n=5, menzil 32, 48 epizot): **N0 ✓, N1 ✓**
| kol | kişi-başı ömür (s=0.5) | s=0 (S3-C) | isabet |
|---|---|---|---|
| none | 210 | 210 | — |
| deaf | **115** | 115 | 0.271 |
| own | 142 | 142 | 0.474 |
| told | **184** | 193 | 0.862 |
| god | 210 | 225 | 1.0 |

Değer 1.83, gereklilik 0.279, yeterlilik 0.726 (s=0: 1.96 / 0.241 /
0.709). **Paylaşım basıncı korur, kanalın değerini korur** (told/own
= 1.30 ≥ 1.15). Veri: `runs/s3n_event_oracle_share05.json`. Basamak
2 (ekoloji, `runs/s3n/`) başlatıldı.

## S3-L — SONUÇLAR: **yavaşlatan taraf GÖNDERME** (2026-10-19, sabah)

Veri: `runs/s3l/`, `runs/s3l/summary.json`.

| kol | gönderir/duyar | medyan ömür | isabet 0-20K → 80-100K | kendi-ipucu son 20K | hasat/1K | sinyal |
|---|---|---|---|---|---|---|
| K-K (S3-K) | ✗/✗ | 42 | 0.22 → 0.30-0.31 | ~0.60 (tahmin) | 5.7-6.2 | 0 |
| **L-hear** | ✗/✓ | 42 | 0.22 → **0.30 / 0.31 / 0.31** | **0.60-0.63** | 5.7-6.2 | 0 |
| **L-speak** | ✓/✗ | 40 | 0.21 → **0.26 / 0.26 / 0.27** | 0.52-0.53 | 4.4-5.0 | 0.80-0.85 |
| K-A (S3-K) | ✓/✓ | 40 | 0.22 → 0.24-0.25 | ~0.48 | 3.6-4.5 | 0.72-0.81 |

- **L1 ✓ (cihaz):** L-hear, K-K ile BİT-EŞ (aynı ölüm sayıları, aynı
  ömürler): kimse konuşmayınca alınan vektör sıfır → duyma yolu açık
  olmanın tek başına maliyeti yok; determinizm doğrulaması (M-23).
- **L2 ✓:** L-speak isabeti K-K'nın 0.04-0.05 altında (çıta 0.03) →
  yavaşlamanın ana kaynağı GÖNDERME tarafı: ortak planlayıcı (6×17 aday
  uzayı, 64 adayla seyrelme) + sinyal maliyeti (ömür 42 → 40, hasat
  −20%). Duyma (K-A − L-speak ≈ −0.015) küçük ek pay: anlamsız 16
  boyutluk girdi gürültüsü.
- **Kendi-ipucu son 20K penceresi (yeni sayaç):** L-hear 0.60-0.63 —
  K1 çıtası (0.70) hâlâ aşılmadı ama şansın (0.5) açık üstünde, 3/3.
- **MI 0.0003-0.0004 bit** (speak): konuşan yine yok.

**Öngörü karnesi:** L1 ✓ (0.85) doğru; L2 ✓ (0.7) doğru.

**Mekanizma hükmü (PL-32):** kanalın öğrenmeyi yavaşlatması, ajanın
sinyal "söylemesi"nin bedelidir: her sinyal enerji yakar ve planlayıcı
aday bütçesinin ~%94'ü (16/17) sinyalli satırlara gider — eylem
araması zayıflar. Çözüm adayı (0 bit, S3-O): planlayıcı aday bütçesini
eylem ve sinyal için AYIRMAK (K-111 emsali: eylem adayları sinyalsiz
garantili + ayrı sinyal adayları) — içerik vermez, arama mekaniğidir.

## S3-N — SONUÇLAR: **paylaşılan kayıp kanalı kurtarmadı** (2026-10-19, sabah)

Veri: `runs/s3n/`, `runs/s3n/summary.json` (s=0.5, her 10 tur, lead 4, 100K).

| kol | medyan ömür | isabet 0-20K → 80-100K | kendi-ipucu son 20K | STAY | hasat/1K | sinyal | MI |
|---|---|---|---|---|---|---|---|
| **N-A** (açık) | 40 | 0.21 → **0.23 / 0.24 / 0.24** | 0.47 | 0.27-0.29 | 3.9-4.3 | 0.77-0.79 | 0.0003-0.0005 bit |
| **N-K** (kapalı) | 43 | 0.22 → **0.28 / 0.28 / 0.28** | 0.55-0.56 | 0.23-0.28 | 6.4-7.6 | 0 | — |
| K-K (s=0) | 42 | 0.22 → 0.31 | ~0.61 | 0.30 | 5.7-6.2 | 0 | — |

- **N2 ✗ (ters):** N-A, N-K'nın 0.04 altında. **N3 ✗:** MI 0.0004 bit,
  H(sembol) 3.98-3.99. **N4 ✗:** 40 < 43. **N5 ✓:** N-K 0.28 ≥ 0.26 —
  paylaşım kendi-ipucu öğrenmesini söndürmüyor ama yavaşlatıyor
  (0.31 → 0.28; bedavacılık payı %50 beklenen yönde).
- **Hüküm:** göndericiye dönen fayda FİZİKTE artık var (oracle: told
  184 vs own 142), ama öğrenen ajan ona hiç ulaşamıyor: kanal açık
  kolda kendi-ipucu öğrenmesi bile başlamıyor (0.47). S3-L ile birlikte
  mekanizma: gönderme bedeli (planlayıcı seyrelmesi + enerji) fayda
  doğmadan önce öğrenmeyi boğuyor — tavuk-yumurta.

**Öngörü karnesi:** N2 ✗ (0.65) doğru; N3 0.005-0.03 → gerçek 0.0004
(yine düşük); N5 ✓ (0.6) doğru.

**Yeni ders var mı?** Aday → **M-28: Tuzağın geri dönüş yolunu kur,
ama önce giriş ücretini ölç.** Sinyalin göndericiye beklenen değeri
(M-25'in gelir tarafı) VE sinyal denemenin öğrenme maliyeti birlikte
hesaplanır; ikincisi birincisinden büyükse fayda hiç keşfedilmez.
(S3-N: fayda fizikte vardı, giriş ücreti — planlayıcı seyrelmesi +
enerji — öğrenmeyi 0'da tuttu.) S3-O sonucuyla METODOLOJI'ye.

## S3-O — ÖN-KAYIT: giriş ücretini düşür — planlayıcı aday bütçesi (koşumdan önce, M-08) (2026-10-19, sabah)

**Tek değişken:** `mpc_signal_candidate_frac` (sinyal taşıyabilen
rastgele aday satırı payı): 1.0 (S3 geometrisi, ~%94 sinyalli) →
**0.25** ve **0.05**. Diğer her şey S3-N N-A ile aynı (s=0.5, her 10
tur, lead 4, σ=0.002, klon, yuva, kanal açık), 3 seed, 100K. İçerik
vermez (hangi sembol/eylem iyi söylenmez); arama mekaniğidir
(K-109/K-111 soyu; KERNEL S3-O notu, ~1 bit üst sınır beyanı).
Varsayılan 1.0 bit-eş (test). ε-dalı değişmez (16/17 sinyal, ~%9 tur).

**Çıtalar (son 20K):**
- **O1 (giriş ücreti düştü mü):** O-25 ve/veya O-05 isabeti ≥ N-K
  (0.28) − 0.02 — kanal açıkken kendi-ipucu öğrenmesi artık başlıyor;
  kendi-ipucu > 0.55.
- **O2 (kanal fayda, H3/H4 kapısı):** herhangi bir O kolu isabeti >
  N-K + 0.05 VE > 0.50'ye yaklaşma eğilimi (son 20K > ilk 20K + 0.10).
- **O3 (konuşan):** MI ≥ 0.05 bit MM, p<0.05; VEYA uyarı penceresinde
  sinyal oranı, pencere dışının ≥ 1.3 katı (zamanlama ipucu — sembol
  içeriği olmasa da "ne zaman" bilgisi).
- **O4:** sinyal oranı 0.77'den belirgin düşer (<0.4): ajan sinyali
  artık rastgele değil seçerek veriyor (ya da hiç vermiyor — ikisi de
  bilgilendirici; O3 ayırır).

**Öngörüler (bağlayıcı):** O1 ✓ (0.7): seyrelme kalkınca açık kol kapalı
kola yaklaşır. O4 ✓ (0.8): sinyal oranı 0.1-0.3'e iner (ε + nadir
planlı). O2 ✗ (0.7), O3 ✗ (0.6): fayda zinciri 100K'da kurulmaz;
ama ilk kez "konuşmanın bedava olmadığı ve dinlemenin mümkün olduğu"
bir rejim elde edilir → S3-P: bu rejimde 300K+ (yarın).

**Sonuç matrisi:** O1✓ O2✗ O3✗ → rejim hazır, süre lazım (S3-P uzun
koşum; Ali'ye önerilir). O1✓ O3✓ → ADAY GÖZLEM (zamanlama/sembol
olumsallığı), Beş Kapı. O1✗ → giriş ücreti planlayıcı değil enerji
(sinyal maliyeti 0.5 anayasal; dokunulmaz) → kanal sorusu bu anayasa
altında kapanır, S3 nihai hüküm negatif-mekanizmalı.

### S3-O yan probu — planlayıcı sinyali neden seçiyor? **Kazananın laneti DEĞİL; öğrenilmiş sinyal primi (M-05)**
`training/signal_curse_probe.py` (`runs/s3o/signal_curse_probe.json`):
60 durum × 64 aday; satırlar ilk adımı sinyalli/sinyalsiz diye gruplandı.

| çekirdek | frac | sinyalli pay | argmax→sinyalli | ort. skor sinyalli − sessiz | std sinyalli / sessiz |
|---|---|---|---|---|---|
| seed3 transplant (olay görmemiş) | 1.0 | 0.86 | 0.50 | +0.05 | 0.27 / 0.44 |
| seed3 transplant | 0.05 | 0.04 | **0.00** | −0.01 | 0.11 / 0.29 |
| NA_s3001 (S3-N, paylaşımlı) | 1.0 / 0.05 | 0.86 / 0.04 | 0.55-0.73 / 0.04-0.05 | ≈0 | düşük / yüksek |
| **KA_s3001 (S3-K)** | 1.0 | 0.86 | **0.98** | **+0.33 … +0.55** | 0.35 / 0.69 |
| **KA_s3001** | 0.05 | 0.04 | **0.40-0.68** | **+0.35 … +0.59** | 0.13 / 0.37 |

- **Hipotez (varyans/kazananın laneti) DÜŞTÜ:** sinyalli satırların
  skor std'si sessizlerden DÜŞÜK; max'ı kazandıran gürültü değil.
- **Gerçek mekanizma:** K-A soyunun modeli **"kendi sinyalim ⇒ daha
  yüksek enerji"** diye öğrenmiş (prim 0.3-0.6; sinyalin gerçek etkisi
  −0.5 enerji/tur). Olay görmemiş transplantta prim yok, paylaşımlı
  N-A soyunda yok, K-A'da var → öğrenilmiş ve soya bağlı. Kapalı-döngü
  karıştırması (M-05, PL-12'nin sinyal enkarnasyonu): planlayıcı
  tahmini enerjisi yüksek durumlarda sinyal seçer → veride sinyal,
  yüksek enerjiyle birlikte görünür → model nedenselliği ters öğrenir →
  planlayıcı daha çok sinyal seçer. Karşı-olgu ("sussaydım") verisi
  neredeyse YOK: planlayıcı dalı %94 sinyalli, ε dalı 16/17 sinyalli
  → ajan 1000 turda ~10 kez susuyor.
- **Sonuç:** frac'ı düşürmek (S3-O) planlayıcıdaki payı kısar ama
  öğrenilmiş prim varsa az sayıdaki sinyalli satır yine kazanır (O05'te
  sinyal oranı 0.48, ε tabanı 0.09+0.04 olmalıydı — 56K ara okuma).
  **0-bit çare adayı (S3-P): ε dalında sinyal/sessizlik DENGESİ**
  (`eps_signal_quiet_prob`, K-108 revizyonu; eps_move_bias emsali:
  içerik vermez, karşı-olgusal veri çeşitliliği verir).

## S3-P — ÖN-KAYIT: karşı-olgusal susma verisi (ε sinyal dengesi) (koşumdan önce, M-08) (2026-10-19)

**Gerekçe.** S3-O yan probu: model "kendi sinyalim ⇒ yüksek enerji"
primini kapalı döngüde öğreniyor çünkü ajan neredeyse hiç SUSMUYOR
(planlayıcı %94 sinyalli, ε dalı 16/17 sinyalli). M-05'in reçetesi:
nadir eylemin karşı-olgusal verisini üret. `eps_signal_quiet_prob=0.5`:
ε ateşlendiğinde yarı yarıya sessiz. İçerik vermez (hangi sembol iyi
söylenmez); K-108'in sinyal boyutuna simetrik uygulanması
(eps_move_bias emsali; KERNEL S3-P notu, ~1 bit üst sınır).

**Kollar (S3-O sonucuna göre frac sabitlenir; O1 düşerse frac=0.05 ile
birlikte):** P-A: kanal açık, eps_quiet=0.5 (+frac); P-K: kanal kapalı
referansı N-K (0.28) / K-K (0.31). 3 seed, 100K, s=0.5, her 10 tur, lead 4.

**Çıtalar (son 20K):**
- **P1 (prim kırıldı mı):** sinyal oranı < 0.30 VE yan prob'da argmax→
  sinyalli oranı ≤ sinyalli pay × 1.5 (prim yok).
- **P2 (giriş ücreti düştü mü):** P-A isabeti ≥ N-K − 0.02 (0.26),
  kendi-ipucu > 0.55.
- **P3 (kanal fayda, H3/H4):** P-A isabeti > N-K + 0.05.
- **P4 (konuşan):** MI ≥ 0.05 bit ya da pencere sinyal oranı ≥ 1.3×
  pencere dışı.

**Öngörüler (bağlayıcı):** P1 ✓ (0.7) — susma verisi primi söndürür,
sinyal oranı ε tabanına (~0.05-0.15) iner. P2 ✓ (0.6). P3 ✗ (0.75),
P4 ✗ (0.7): susan ajan kanalı doğru fiyatlar ama fayda zincirini
100K'da kurmaz.

**Sonuç matrisi:** P1✓ P2✓ P3✗ → "kanal artık doğru fiyatlanıyor, dil
için süre/seçilim lazım" → S3-Q uzun koşum (300K) Ali'ye önerilir; S3
nihai hükmü "negatif, mekanizmalı, rejim hazır". P1✗ → prim ε'ya
dirençli (planlayıcı dalı baskın) → planlayıcı tarafında karşı-olgu
(frac → 0: sinyal yalnız ε'dan) son 0-bit basamak. P3✓ → ADAY GÖZLEM,
Beş Kapı.

## S3-O — SONUÇLAR: **aday bütçesini kısmak yetmedi; öğrenilmiş sinyal primi baskın** (2026-10-19)

Veri: `runs/s3o/`, `runs/s3o/summary.json`, prob `runs/s3o/signal_curse_probe_o.json`.

| kol | frac | medyan ömür | isabet 80-100K | kendi-ipucu son 20K | sinyal | pencere-sinyal | hasat/1K | MI |
|---|---|---|---|---|---|---|---|---|
| N-A (frac 1.0) | 1.0 | 40 | 0.23-0.24 | 0.47 | 0.77 | 0.78 | 3.9-4.3 | 0.0004 |
| **O-25** | 0.25 | 40 | 0.23 / 0.23 / 0.24 | 0.44-0.49 | **0.65-0.70** | 0.65-0.71 | 3.7-4.0 | 0.0001 |
| **O-05** | 0.05 | 40 | 0.22 / 0.25 / 0.23 | 0.44-0.50 | **0.44-0.54** | 0.44-0.54 | 4.0-4.2 | 0.0-0.0002 |
| N-K (kapalı) | — | 43 | 0.28 | 0.55 | 0 | — | 6.4-7.6 | — |

- **O1 ✗:** isabet 0.22-0.25 < 0.26; kendi-ipucu ≤ 0.50. **O4 ✗:**
  sinyal oranı ε+pay tabanının (0.05 kolunda ~0.13) 3-4 katı. O2/O3 ✗.
- **Prob (O05 soyları):** sinyalli satırların ortalama skoru sessizlerden
  **+0.47 … +0.94** yüksek; %3.8 payla argmax→sinyalli **%88-96**.
  O25'te de prim var (%65-100). Prim, frac kısıldıkça BÜYÜMÜŞ (K-A
  +0.3-0.5 → O05 +0.5-0.9): az sinyalli satır → her sinyalin "seçilmiş
  durumda" görünme olasılığı artar → karıştırma güçlenir (M-05'in
  öngördüğü yön).
- **Öngörü karnesi:** O1 ✓ (0.7) → YANLIŞ; O4 ✓ (0.8) → YANLIŞ. İki
  öngörü de yan prob'un bulduğu primi hesaba katmıyordu (prob, ön-kayıt
  sonrası kuruldu; sıralama beyanlı).

**Hüküm (PL-32 nihai):** kanalın öğrenmeyi yavaşlatması = ajanın
kendi sinyaline öğrendiği sahte enerji primi (kapalı-döngü nedensel
karıştırma) + sinyalin gerçek maliyeti. Planlayıcı bütçesi değil,
VERİ dengesi sorunu. Son 0-bit basamak: S3-P (ε dalında susma verisi).
Kollar netleşti: **P-A** eps_quiet=0.5 + frac=0.05; **P-B** eps_quiet=0.5,
frac=1.0 (M-06 ayrımı: susma verisi tek başına yeter mi).
