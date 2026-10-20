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

## S3-P — SONUÇLAR: **susma verisi primi yarılıyor ama kırmıyor; 0-bit merdiven bitti** (2026-10-19, öğle)

Veri: `runs/s3p/`, `runs/s3p/summary.json`, prob `runs/s3p/signal_curse_probe_p.json`.

| kol | eps_quiet | frac | isabet 80-100K | kendi-ipucu son 20K | sinyal son 20K | prob: prim (ort. skor farkı) | argmax→sinyalli @%4 pay | MI |
|---|---|---|---|---|---|---|---|---|
| N-A | 0 | 1.0 | 0.23-0.24 | 0.47 | 0.77 | ≈0 (N-A soyunda prim yoktu) | 0.04 | 0.0004 |
| O-05 | 0 | 0.05 | 0.22-0.25 | 0.44-0.50 | 0.44-0.54 | **+0.5 … +0.9** | 0.88-0.96 | ≤0.0002 |
| **P-A** | 0.5 | 0.05 | 0.23 / 0.25 / 0.25 | 0.47-0.51 | **0.28-0.37** | +0.36 … +0.61 | 0.21-0.75 | ≤0.0001 |
| **P-B** | 0.5 | 1.0 | 0.22 / 0.25 / 0.24 | 0.45-0.50 | 0.59-0.63 | +0.1 … +0.46 | 0.04-0.51 | 0.0005 |
| N-K (kapalı) | — | — | **0.28** | 0.55 | 0 | — | — | — |

- **P1 ✗ (sınırda):** P-A sinyal oranı 0.28-0.37 (çıta <0.30: 1/3 geçer);
  prob'da prim AYAKTA (+0.4-0.6), argmax sinyalliye payının 5-20 katı.
  Susma verisi (ε'nın yarısı) primi yarıya indiriyor, söndürmüyor:
  planlayıcı dalı (%90) veriyi hâlâ sinyal-yüklü üretiyor.
- **P2 ✗:** isabet 0.23-0.25 < 0.26; kendi-ipucu 0.47-0.51 < 0.55.
  (P-A'da 0-20K → 80-100K +0.04: öğrenme başlıyor ama N-K'nın gerisinde.)
- **P3 ✗, P4 ✗:** kanal faydası yok, MI ≈ 0, H(sembol) 3.98-4.00.
- **Öngörü karnesi:** P1 ✓ (0.7) → YANLIŞ (sınırda ✗); P2 ✓ (0.6) →
  YANLIŞ; P3/P4 ✗ → doğru.

**Hüküm (PL-32 nihai):** kanal açıkken öğrenmenin yavaşlaması,
planlayıcının kapalı döngüde kendi sinyaline öğrettiği SAHTE enerji
priminden kaynaklanır (M-05 nedensel karıştırma); prim, aday bütçesi
(S3-O) ve ε susma verisiyle (S3-P) azaltılabiliyor ama bu mimaride
(argmax planlayıcı + on-policy tek model) sıfırlanamıyor. **0 bitlik
merdiven tükendi.** Kalan çözümler öğrenme MEKANİĞİNE bit yazar:
(i) karşı-olgusal düzeltme (önem ağırlıklı / çift-sağlam enerji hedefi),
(ii) model topluluğu + belirsizlik cezası (PL-12 c), (iii) planlayıcının
eylem ve sinyali ayrı değerlendirmesi (K-103 revizyonu). Hepsi
KERNEL_BUDGET satırı açar; karar Ali ile (sabah raporu).

---

# S3 KAPANIŞ EKİ (2026-10-19, öğle) — S3-L…P sonrası nihai hüküm

**Hükümler değişmedi; mekanizma zinciri tamamlandı.**
1. Ekoloji kararlı (σ=0.002) ve ajanlar KENDİ ipuçlarını öğreniyor
   (okul 0.86; kanal-kapalı ekoloji 100K'da 0.31 isabet ↑, kendi-ipucu
   ~0.60). [S3-F/J/K/L]
2. Kanal: 24 koşumda (K/L/N/O/P) hiçbir ipucu bilgisi taşımadı
   (MI ≤ 0.0005 bit, entropi tavanda); her kolda kanal açıkken
   kendi-ipucu öğrenmesi yavaşladı. [S3-K…P]
3. Neden: (a) göndericiye dönen fayda yoktu → fiziğe eklendi (s=0.5),
   yetmedi; (b) gönderme bedeli: enerji + öğrenilmiş sahte prim
   (kapalı-döngü karıştırma) → bütçe ve ε dengesi yarıya indirdi,
   silemedi. Giriş ücreti > keşfedilmemiş fayda → kanal hiç
   fiyatlanamıyor. [S3-L/N/O/P + problar]
4. **H4: NEGATİF (bu anayasa altında, 100K tur, 0 yeni bit), mekanizmalı.
   H3: ön koşul negatif. H2: test edilmedi. H1: karışık (S2 hükmü).
   H0 ayakta.**

**Sonraki program (Ali kararı; hepsi anayasaya dokunur ya da büyük
bütçe ister):**
- **A. Öğrenme mekaniği revizyonu** (bit yazar): karşı-olgusal düzeltilmiş
  enerji hedefi ya da topluluk belirsizliği; primi kaynağında keser.
  Tahmini 2-3 gün + 100K koşumlar.
- **B. Kademeli kanal + uzun süre** (0 bit, bütçe): kanal-kapalı 300K ile
  kendi-ipucu tavanı (0.5), sonra kanal açılır (öğrenmiş ajan sinyali
  doğru fiyatlar mı?). Tahmini 1 gün hesaplama.
- **C. Tuzağı yeniden tasarla** (anayasal): kimlikli/yerel kanal,
  tekrarlı eş (PL-28 geri), ya da sinyalin alıcıdaki değerini doğrudan
  gözlemlenebilir kılan görev. Deneyin sorusunu değiştirir.
Tavsiye: **B önce** (ucuz, 0 bit; "giriş ücreti" tezini test eder),
sonra A.

**Ali adına verilen ek kararlar (19 Ekim, hepsi defterde):** event_share
0.5 (fizik), mpc_signal_candidate_frac ve eps_signal_quiet_prob
(arama/keşif mekaniği, varsayılan bit-eş, üst sınır ~1 bit her biri,
kalıcı yapılmadı). Anayasal basamak atılmadı. **Toplam yeni prior: 0.**

**Yeni ders:** M-28 işlendi (aşağıda METODOLOJI).

## S3-Q — ÖN-KAYIT: Program B, kademeli kanal (koşumdan önce, M-08) (2026-10-19, öğleden sonra)

**Karar (Ali, 19 Ekim: "B ile devam").** Tez: kanal, yetkinsiz ajana
açılınca giriş ücreti öğrenmeyi boğuyor (S3-K…P). Yetkin ajana
(kendi-ipucu tavanında) açılırsa sinyal doğru fiyatlanır mı ve
başkasının biti için kullanılır mı?

**Q1 — tavana çık (kanal kapalı, 300K, 3 seed):** klon kadro, yuva
(600, 0.5), σ=0.002, her 10 tur, lead 4, ceza 25, s=0.5, mute. Son
ağırlıklar kaydedilir.
- **Q1a:** son 20K isabet ≥ 0.40 VE kendi-ipucu ≥ 0.75 (okul 100K'da
  0.44/0.86; ekoloji ~3× yavaş → 300K).
- **Q1b (zaman çizgisi):** isabet tekdüze ↑ (her 100K dilim öncekinden
  büyük).

**Q2 — kanalı aç (100K, 3 seed, Q1 final ağırlıklarından kurucu kadro):**
kollar **Q2-A** kanal açık (ortak planlama, frac 1.0, eps_quiet 0 —
anayasal varsayılanlar) ve **Q2-K** kanal kapalı devam (kontrol: aynı
ağırlıklar, aynı dünya).
- **Q2a (doğru fiyatlama):** Q2-A sinyal oranı son 20K < 0.30 VE prob'da
  prim < +0.1 (yetkin model sinyali −0.5 enerji olarak öğreniyor).
- **Q2b (giriş ücreti kalktı mı):** Q2-A isabet ≥ Q2-K − 0.02.
- **Q2c (kanal fayda, H3/H4):** Q2-A isabet > Q2-K + 0.05 VE > 0.50
  (kendi-ipucu tavanının üstü — yalnız başkasının bitiyle mümkün).
- **Q2d (konuşan/dinleyen):** MI ≥ 0.05 bit MM p<0.05; VEYA pencere
  sinyal oranı ≥ 1.3× pencere dışı; VEYA "duydu" koşullu isabet > "duymadı"
  + 0.05 (sinyal oranı düşerse "duymadı" kümesi artık boş olmaz).

**Öngörüler (bağlayıcı):** Q1a ✓ (0.6; 300K yetmeyebilir). Q2a ✓ (0.55):
yetkin modelin enerji kafası sinyal maliyetini görür; prim yine
oluşabilir (M-05 mekanizması yetkinlikten bağımsız) — bu yüzden 0.55.
Q2b ✓ (0.6). Q2c ✗ (0.8), Q2d ✗ (0.7).

**Sonuç matrisi:** Q2a✓ Q2b✓ Q2c✗ → giriş ücreti tezi DOĞRULANDI ama
dil yine yok → kalan engel fayda zincirinin keşfi (alıcı: duyduğum
sembol ⇒ eylem) → Program A (öğrenme mekaniği) ya da seçilim; S3
nihai hüküm "negatif, mekanizmalı, iki katman çözüldü". Q2a✗ → prim
yetkinlikten bağımsız → Program A zorunlu. Q2c✓ → ADAY GÖZLEM, Beş
Kapı (Q2-K ablasyon hazır; ikiz; bit-eş tekrar; zaman çizgisi; 0 bit).

**Beyan (M-09):** Q2 kurucu kadrosu öğrenmiş ağırlıklardır (nüfus-tarihi
kararı, PL-06/klon emsali); yuva Q2'de de her nesilde. Bit: 0.
Hesap: Q1 ~7 saat (3 paralel), Q2 ~2,5 saat.

### S3-Q1 — SONUÇ: tavana yaklaşma (kanal kapalı, 300K) (2026-10-19 gece)
| seed | medyan ömür | isabet 0-100K → 100-200K → 200-300K | son 20K isabet | kendi-ipucu son 20K | STAY | hasat/1K | ölüm |
|---|---|---|---|---|---|---|---|
| 3001 | 46 | 0.243 → 0.313 → 0.342 | **0.359** | **0.724** | 0.33 | 4.8 | 31.2K |
| 3002 | 47 | 0.252 → 0.312 → 0.364 | **0.370** | **0.757** | 0.39 | 5.4 | 30.9K |
| 3003 | 46 | 0.252 → 0.315 → 0.357 | **0.354** | **0.728** | 0.40 | 5.7 | 30.9K |

- **Q1a harfen ✗** (isabet 0.35-0.37 < 0.40; kendi-ipucu 1/3 ≥ 0.75),
  **Q1b ✓** (3/3 tekdüze ↑). Ekoloji 300K'da okulun 100K'daki 0.86/0.44
  noktasının ~%85'ine geldi; eğim sürüyor (~+0.02/100K). Tavana
  (0.50) ulaşmak için ~500K+ gerekir. Ömür 42 → 46 (öğrenme ömre
  dönüyor, az). Q2 ön-kayıtta Q1a'ya koşullu değildi → başlatıldı
  (Q1 final ağırlıklarından, aynı seed'ler).
- Prob (lead-8 protokolü, Q1_s3002): hiza 0.25-0.50, güvenli-eylem
  farkı 0.003-0.011 — ekoloji lead=4 öğrendi, prob lead=8 soruyor;
  protokol uyumsuzluğu (önceki beyan), davranış ölçüsü esas.

### S3-Q2 — SONUÇ: **yetkin ajan kanalı doğru fiyatlıyor; açılış şoku yetkinliği düşürüyor; dil yok** (2026-10-19 gece, 03:45)

Veri: `runs/s3q/Q2{A,K}_s*`, `runs/s3q/summary_q2.json`, prob
`runs/s3q/signal_curse_probe_q2.json`. Kurucu kadro: Q1 final ağırlıkları.

| kol | medyan ömür | isabet 0-20K → 40-60K → 80-100K | kendi-ipucu son 20K | sinyal seyri (2K→100K) | hasat/1K | MI |
|---|---|---|---|---|---|---|
| **Q2-K** (kapalı devam) | **50** | 0.36-0.40 → 0.36-0.38 → **0.37-0.39** | **0.74-0.77** | 0 | 3.6-4.0 | — |
| **Q2-A** (açık) | 40-43 | 0.26-0.28 → 0.27-0.32 → **0.30-0.31** | 0.60-0.62 | **0.97 → 0.46 → 0.41 → 0.35 → 0.26-0.48** | 2.2-2.7 | **0.0007-0.0028** (p=0) |

- **Prob (prim):** Q1 (sessiz eğitilmiş) ağırlıklarında sinyalli satırlar
  **+0.9 … +3.4** primli (sinyal sütunları 300K boyunca hiç eğitilmedi;
  argmax→sinyal %93-100) → kanal açılınca ilk 2K turda sinyal oranı
  0.97: **açılış şoku**. 100K sonra Q2-A ağırlıklarında prim **TERSİNE
  DÖNDÜ: −0.8 … −1.9**, argmax→sinyal %0-30 (%86 payla). **İlk kez bir
  ajan kanalı doğru fiyatladı** (sinyal = enerji kaybı). Kalan sinyal
  oranı (0.26-0.52) ε (0.09) + CEM gürültüsü + hâlâ inen eğilim.
- **Q2a:** prim ✓ (tersine döndü), oran ✗ (son 20K 0.26/0.44/0.52;
  çıta <0.30 → 1/3). **Q2b ✗:** Q2-A, Q2-K'nın 0.08 altında; açılış şoku
  (sinyal spam → enerji → ölüm 42→40, hasat −35%) yetkinliği 0.37'den
  0.27'ye düşürdü, 100K'da 0.30'a toparladı (↑ sürüyor). **Q2c ✗.**
  **Q2d ✗:** MI 0.0007-0.0028 bit (tüm koşumların en yükseği, çıtanın
  20'de biri); "duydu/duymadı" tutarsız (+0.065 / −0.06 / +0.02;
  duymadı kümesi %0.1-1).
- **Öngörü karnesi:** Q1a ✓ (0.6) → harfen ✗; Q2a ✓ (0.55) → yarı (prim
  ✓, oran ✗); Q2b ✓ (0.6) → ✗ (şok öngörülmedi); Q2c/Q2d ✗ → doğru.

**Hüküm (Program B, ara):** "giriş ücreti" tezi kısmen doğrulandı:
yetkin model sinyalin bedelini öğreniyor (prim tersine), yetkinsiz
model öğrenemiyordu (S3-K…P). Ama açılış şoku (eğitilmemiş sinyal
sütunlarının sahte primi) yetkinliği geriletiyor ve fayda zinciri 100K'da
kurulmuyor. Matris "süre lazım" dalı → **S3-R**.

## S3-R — ÖN-KAYIT: Q2 devamı, 200K (koşumdan önce, M-08) (2026-10-19, 03:50)

Q2-A ve Q2-K kendi final ağırlıklarından 200K daha (toplam açık kanal
300K, toplam öğrenme 600K); dünya seed'leri +100 (yeni yerleşim; ağırlık
devam, beden/dünya yeni). Kollar **R-A** (açık) / **R-K** (kapalı).
- **R1 (toparlanma):** R-A son 20K isabet ≥ R-K − 0.03 (şok geçti,
  kanal artık doğru fiyatlı ve maliyetsiz-yakın).
- **R2 (dil, H3/H4):** R-A isabet > R-K + 0.05 VE > 0.50.
- **R3 (konuşan/dinleyen):** MI ≥ 0.05 bit MM p<0.05; VEYA "duydu"
  isabeti > "duymadı" + 0.05 3/3 seed'de; VEYA pencere sinyal oranı ≥
  1.3× pencere dışı.
- **R4 (fiyatlama):** R-A sinyal oranı son 20K < 0.25 3/3.

**Öngörüler (bağlayıcı):** R1 ✓ (0.5), R4 ✓ (0.6), R2 ✗ (0.85), R3 ✗ (0.7).
**Sonuç matrisi:** R1✓ R2✗ → Program B tamam: "kanal doğru fiyatlanabilir
ama bu anayasada kullanılmıyor" → Program A (öğrenme mekaniği) ya da
C (tuzak tasarımı) kararı Ali'ye, nihai S3 hükmü güncellenir. R2✓ →
ADAY GÖZLEM, Beş Kapı (R-K ablasyon hazır; ikiz; bit-eş; zaman çizgisi).
R1✗ → kanal açık kaldıkça yetkinlik geri gelmiyor → kalıcı maliyet
(sinyal 0.5 anayasal) → C.

## S3-R — SONUÇLAR: **toparlanma yok; Program B tamam** (2026-10-19, 07:10)

Veri: `runs/s3r/`, `runs/s3r/summary.json`, prob `runs/s3r/signal_curse_probe_r.json`.
Toplam: kanal-kapalı 300K + açık 300K (R-A) / kapalı 600K (R-K).

| kol | medyan ömür | isabet 0-50K → 100-150K → 180-200K | kendi-ipucu son 20K | sinyal son 20K | hasat/1K | MI |
|---|---|---|---|---|---|---|
| **R-K** (kapalı, 600K toplam) | **50** | 0.37-0.39 → 0.36-0.38 → **0.37-0.38** | **0.74-0.75** | 0 | 2.6-3.2 | — |
| **R-A** (açık, 300K açık) | 42-47 | 0.29-0.32 → 0.29-0.32 → **0.30-0.32** | 0.60-0.64 | 0.26-0.46 | 1.8-2.3 | 0.001-0.0027 |

- **R1 ✗:** fark −0.07 sabit (300K açık kanal boyunca kapanmadı).
  **R2 ✗, R3 ✗** (MI 0.001-0.003; "duydu/duymadı" tutarsız: −0.02/+0.04/
  −0.03), **R4 ✗** (sinyal 0.26-0.46; ε tabanı 0.09).
- Prob (R-A s3002): bir soy sinyali doğru fiyatlıyor (−1.6, argmax→
  sinyal %5), diğeri nötr (−0.05, %95 — geometri payı). Fiyatlama
  soydan soya değişken; kanal maliyeti (enerji + sinyal gürültüsü +
  planlayıcı seyrelmesi) kalıcı.
- **Kapalı kol platoda:** 600K'da isabet 0.37-0.38, kendi-ipucu 0.74
  — tavan (0.50/1.0) yerine ~0.38/0.75'te doyuyor: ölüm sıfırlaması +
  5 ajan rejiminin öğrenme tavanı okulun (0.44/0.86) altında.
- **Öngörü karnesi:** R1 ✓ (0.5) → ✗; R4 ✓ (0.6) → ✗; R2/R3 ✗ → doğru.

**PROGRAM B HÜKMÜ:** "giriş ücreti" tezi yarı doğru: yetkin ajan sinyalin
bedelini öğrenebiliyor (Q2'de prim tersine döndü; S3-K…P'de hiç
öğrenemiyordu) ama (i) açılış şoku (eğitilmemiş sinyal sütunlarının
sahte primi, sinyal 0.97) yetkinliği −0.08 düşürüyor ve 300K'da geri
gelmiyor, (ii) fayda zinciri (benim sinyalim → onun eylemi → benim
paylaşılan enerjim) hiçbir soyda keşfedilmiyor — tavuk-yumurta: alıcı
sembolü kullanmadan göndericiye fayda yok, gönderici tutarlı sembol
üretmeden alıcıya öğrenecek şey yok. Kanal bu anayasada **kalıcı net
yük**. Matris: R1✗ → kalıcı maliyet → C (ya da öğrenme mekaniği A).

---

# S3 NİHAİ HÜKÜM (2026-10-19, 07:15) — Program B sonrası

**H4 NEGATİF (bu anayasa altında; 600K tura kadar; 0 yeni bit; 93
koşum), mekanizması tamamlanmış:**
1. Ekoloji öğreniyor (σ=0.002): kendi-ipucu 0.75, isabet 0.38 (plato).
2. Kanal hiçbir koşulda bilgi taşımadı (MI ≤ 0.003 bit; 36 açık-kanal
   koşumu); entropi tavanda.
3. Kanal açık olmak her koşulda yetkinliği düşürdü (−0.04 … −0.08
   isabet, −30% hasat): maliyet + sahte prim + açılış şoku.
4. Fayda fiziğe eklendi (paylaşılan kayıp): oracle değer buldu, öğrenen
   ajan keşfetmedi (tavuk-yumurta).
**H3 ön koşul negatif. H2 test edilmedi. H1 karışık (S2). H0 ayakta.**

**Pozitif iç-temsil bulguları (etiket: aday gözlem / mekanizma):**
öncü algısı (30/30), kendi-ipucu öğrenimi (okul 6/6, ekoloji 3/3),
kanal fiyatlamasının öğrenilebilirliği (Q2, soya bağlı).

**Sonraki program (Ali kararı, PL-34 güncel):**
- **A. Öğrenme mekaniği** (bit yazar): sahte primi kaynağında kesen
  karşı-olgusal düzeltme / topluluk belirsizliği. Açılış şokunu ve
  fiyatlama değişkenliğini çözer; tavuk-yumurtayı çözmez.
- **A′. Evrimsel önyükleme (0 bit, uzun):** yetkin nüfusta (Q1
  ağırlıkları) soy-düzeyi seçilim + σ ile "ipucu görünce sembol" gibi
  tutarlı gönderici varyantlarının rastgele doğup alıcı öğrenmesiyle
  seçilmesi; tavuk-yumurtanın biyolojideki çözümü (ritüelleşme).
  ≥1M tur ölçeğinde; birkaç gün hesaplama.
- **C. Tuzağı yeniden tasarla** (anayasal): sembolün alıcıdaki değerini
  göndericiye DOĞRUDAN gözlemlenebilir kılan görev (ör. birlikte açılan
  sığınak; kimlikli/yerel kanal, tekrarlı eş). Deneyin sorusunu
  değiştirir ama tavuk-yumurtayı kırar.
**Tavsiye:** A′ (0 bit, deneyin ruhuna en yakın) → sonra C. A tek başına
dil getirmez.

---

# PROGRAM A — öğrenme mekaniği (Ali kararı, 2026-10-20 sabah)

## A0 — ÖN-KAYIT: sahte sinyal primi tek ajanda oluşuyor mu? (koşumdan önce, M-08)

Okul (tek ajan, yetiştirme kabı, her 10 tur, lead 2, ceza 25, 100K), **kanal
açık**: ajan kendi sinyalini gönderir (ortak planlama, ε 16/17), duyan
yok, maliyet 0.5. Referans: S3-J base (kanal kapalı: kendi-ipucu 0.86,
isabet 0.44). 3 seed.
- **A0a (prim):** final ağırlıkta `signal_curse_probe`: sinyalli −
  sessiz ortalama skor > +0.1 VE argmax→sinyalli > pay × 1.5 → prim tek
  ajanda da oluşuyor (öğrenme döngüsüne özgü, nüfusa değil).
- **A0b (maliyet):** kanal-açık okul kendi-ipucu son 20K < 0.80 ya da
  isabet < 0.40 → kanal tek ajanda da öğrenmeyi yavaşlatıyor.
- **Öngörü:** A0a ✓ (0.7) — M-05 mekanizması tek ajanda yeterli (planlayıcı
  seçimi → karıştırılmış veri); A0b ✓ (0.6).
- **Matris:** A0a✓ → A1/A2 okulda test edilir (ucuz, 25 dk). A0a✗ →
  prim çok-ajan etkileşiminden (duyulan sinyaller) → A1/A2 doğrudan
  ekolojide, ve "duyma gürültüsü" ayrı değişken.

## A1/A2 — planlanan basamaklar (ön-kayıt A0 sonucuyla netleşir)
- **A1 Topluluk + uyuşmazlık cezası:** K=3 çekirdek (farklı init, aynı
  veri), planlayıcı J = ortalama − β·std (β ∈ {0.5, 1.0}). İçerik
  vermez; PL-12 (c). Bit: ~2 (K) + ~1 (β) → KERNEL satırı K-115 adayı.
- **A2 Sinyal-dengeli tekrar:** PER örneklemesinde sessiz/sinyalli
  pencereler dengelenir (K-110 tabakalama uzantısı). ~1 bit.
- Çıtalar (okul): prob prim ≤ +0.1 ve argmax→sinyalli ≤ pay×1.5; kanal-
  açık kendi-ipucu ≥ 0.80 ve isabet ≥ 0.40 (kapalıyla eşit). Ekoloji:
  açık kol ≥ kapalı − 0.02 (son 20K), açılış şoku yok (ilk 2K sinyal
  < 0.5).

## A0 — SONUÇ: **tek ajanda sahte prim YOK; prim nüfusa özgü** (2026-10-20, 08:45)

Veri: `runs/a0/open_s{0,1,2}`, prob `runs/a0/signal_curse_probe_a0.json`.

| | kapalı (S3-J base) | **açık (A0)** |
|---|---|---|
| kendi-ipucu 100K | 0.83-0.87 | **0.82-0.83** |
| isabet son 20K | 0.43-0.45 | **0.41-0.43** |
| sinyal oranı | 0 | 0.26-0.28 (ε 0.09 + planlayıcı) |
| prob: sinyalli − sessiz skor | — | **−0.14 … −0.30** (doğru fiyat) |
| argmax→sinyalli (%86 pay / %4 pay) | — | 27-37% / **0%** |

- **A0a ✗:** prim yok; tek ajan sinyalin bedelini öğreniyor (sinyalli
  satırlar sistematik düşük). **A0b sınırda ✓/✗:** kendi-ipucu 0.82 ≥
  0.80, isabet 0.41-0.43 ≥ 0.40 — kanal tek ajanda yalnız küçük bir yük.
- **Öngörü karnesi:** A0a ✓ (0.7) → YANLIŞ. Mekanizma hipotezi
  düzeltildi: M-05 karıştırması tek başına primi üretmiyor; prim
  **nüfus rejiminde** doğuyor. İki aday: (a) duyulan sinyaller (16 boyut
  anlamsız girdi; S3-L speak-only ağırlıklarında prob ile ayrışır),
  (b) halef mutasyonu σ=0.002'nin eğitimsiz sinyal sütunlarında
  birikmesi (ölüm her ~40 tur → 100K'da ~2500 mutasyon/slot → sinyal
  sütunlarında rastgele yürüyüş σ≈0.1; Q1'in 300K sessiz koşumunda
  +1…+3 prim buna uyar; M-26'nın yerel biçimi).

## A1-eko — ÖN-KAYIT (koşumdan önce, M-08) (2026-10-20, 08:50)

Matris gereği (A0a ✗) A1 doğrudan ekolojide; ayrıca mutasyon hipotezi
(b) ayrı kolla. Taban: N-A (σ=0.002, açık, 100K: isabet 0.23-0.24,
sinyal 0.77, prim ≈0/soyda değişken) ve N-K (kapalı 0.28).

| kol | değişken | ayar |
|---|---|---|
| **S0** | mutasyon | açık kanal, **σ=0** (saf miras), K=1 |
| **E3** | topluluk | açık kanal, σ=0.002, **K=3, β=1.0** (K-115 aday) |
(3 seed, 100K, s=0.5, her 10 tur, lead 4; prob: `signal_curse_probe` final ağırlıklarda — speak-only probu da (a) için.)

**Çıtalar (son 20K):**
- **A1a (prim):** prob'da sinyalli − sessiz ≤ +0.1 VE argmax→sinyalli ≤
  pay×1.5 (3/3 seed).
- **A1b (giriş ücreti):** isabet ≥ N-K − 0.02 (0.26) VE kendi-ipucu > 0.55.
- **A1c (açılış şoku):** ilk 2K sinyal oranı < 0.5 (E3'te uyuşmazlık
  cezası eğitimsiz sütunları baştan cezalamalı).
- **A1d (dil):** isabet > N-K + 0.05; MI ≥ 0.05.
- **S0 yorumu:** S0 A1a ✓ ise prim mutasyon kaynaklı (b) → çare σ'yı
  sinyal sütunlarında sıfırlamak değil (içerik), topluluk ya da
  mutasyonu öğrenme hızına bağlamak; S0 A1a ✗ ise kaynak duyma (a).

**Öngörüler (bağlayıcı):** S0: A1a ✓ (0.6) — mutasyon hipotezi. E3: A1a ✓
(0.6), A1c ✓ (0.7), A1b ✓ (0.5), A1d ✗ (0.85).
**Sonuç matrisi:** E3 A1a✓ A1b✓ → K-115 AKTİF; sonra Program C tuzağı bu
mekanikle. E3 ✗ ve S0 ✓ → mekanik değil mutasyon → PL-31 revizyonu
(σ öğrenme-ağırlıklı) ya da K-115 + σ=0 birleşimi. İkisi ✗ → prim
kaynağı duyma → "duyma gürültüsü" kolu (speak-only prob) → topluluk
+ alınan-sinyal maskesi tartışması (anayasal).

### A0 eki — speak-only (S3-L) ağırlıklarında prob: **duymadan da prim var**
`runs/s3l/signal_curse_probe_speak.json`: speak_s3001/s3002 çekirdeklerinde
sinyalli − sessiz **+0.03 … +0.51**, argmax→sinyalli %83-98 (%86 pay) ve
**%14-33 (%4 pay)**. Alınan sinyal yokken de prim oluşuyor → aday (a)
"duyma gürültüsü" prim kaynağı DEĞİL; aday (b) halef mutasyonu /
nüfus dinamiği öne çıkıyor. Karar S0 kolunda (σ=0, açık).

---

# PROGRAM C — ön-tasarım: "birlikte açılan sığınak" (2026-10-20, 09:05)

**Teşhis (S3 nihai):** tavuk-yumurta — sinyalin göndericiye faydası ancak
alıcı sembolü kullanırsa doğuyor; S3-N paylaşımı bile dolaylı kaldı.
**C fikri:** faydayı DOĞRUDAN ve AYNI turda göndericiye bağla: olayda
güvenli eylem ancak aynı turda en az N ajan onu yaparsa korur
(`event_min_safe=N`). Yalnız başına doğru olmak korumaz. Benim
korunmam ortaklarımın da doğru yapmasına bağlı → onların bilmediği biti
söylemek benim hayatta kalmamdır. Kanal yine kimliksiz, küresel,
pahalı, anlamsız semboller; ajana bit yok (fizik). Ekolojik emsal: sürü
hâlinde kaçış / birlikte kaldırılan sığınak kapağı.

**Analitik (5 ajan, her biri kendi bitiyle %50 doğru, bağımsız):**
P(≥2 doğru)=0.81, P(≥3)=0.50, P(≥4)=0.19. Mükemmel iletişimle herkes
%86-100 doğru → P(≥3)≈0.97. N=3'te kanalın değeri 0.50 → 0.97 (büyük,
doğrudan). N=2 zayıf, N=4 çok sert (bedavacı 1 kişi yetiyor).

## C0 — oracle ön-kaydı (M-01, koşumdan önce)
`event_oracle --min-safe {2,3} --share {0, 0.5}`, n=5, menzil 32, 48 epizot.
- **C0a (değer):** told/own ≥ 1.3 VE told − own ≥ S3-C'dekinden büyük
  (S3-C: 193 − 142 = 51 tur) — kanalın değeri sığınakta ARTMALI.
- **C0b (basınç):** deaf ömrü 60-130 arası (yaşanabilir ama basınç var).
- **C0c (kaçış, M-25):** own kolunda isabet oranı ile korunma oranı
  ayrı raporlanır; N=3'te own korunması ≈0.5 olmalı (bedavacılık yok).
- Seçim kuralı: C0a'yı en büyük farkla geçen (N, s) çifti ekolojiye
  gider; eşitlikte s=0.5 (S3-N varsayılanı) ve N=3.

### C0 — oracle SONUCU (2026-10-20, 09:10)
| N | s | deaf | own (isabet) | told (isabet) | god | told/own | told − own |
|---|---|---|---|---|---|---|---|
| 2 | 0 | 115 | 133 (0.47) | 193 (0.86) | 224 | 1.45 | **60** |
| 2 | 0.5 | 115 | 138 (0.48) | 184 (0.87) | 206 | 1.33 | 46 |
| **3** | **0** | 115 | **128 (0.48)** | **186 (0.87)** | 214 | **1.45** | **58** |
| 3 | 0.5 | 115 | 128 (0.49) | 181 (0.87) | 193 | 1.41 | 53 |
(S3-C referans: own 142, told 193, fark 51.)

- **C0a ✓** (N=2/s=0 ve N=3/s=0: oran 1.45, fark 58-60 > 51). **C0b ✓**
  (deaf 115). Fark artışı mütevazı (+7-9 tur): oracle, "kendi ipucuyla
  bağımsız %50" ajanlar arasında zaten %50-81 tesadüfi koordinasyon
  buluyor; kanalın oracle'daki değeri C'de de S3-C'dekine yakın. C'nin
  asıl farkı değerin BÜYÜKLÜĞÜ değil, YOLU: fayda aynı turda ve doğrudan.
- **Seçim: N=3, s=0.** Ön-kayıt kuralı "en büyük fark" N=2'yi (60 vs 58)
  gösteriyordu; 2 turluk fark 48 epizotluk gürültünün içinde ve N=2'de
  kendi-ipucu ajanlar %81 oranında zaten korunuyor (koordinasyon basıncı
  zayıf), N=3'te %50 (analitik). **Sapma beyanı:** kural harfiyen
  uygulanmadı, gerekçe basınç; s=0 seçildi (paylaşım bedavacılık ekler,
  sığınak zaten ortak fayda). Veri: `runs/c0_event_oracle_ms*_sh*.json`.

## C1 — ÖN-KAYIT: sığınak ekolojisi, kanal açık vs kapalı (koşumdan önce, M-08) (2026-10-20, 09:15)

Ayar: klon kadro, yuva (600, 0.5), σ=0.002, her 10 tur, lead 4, ceza 25,
**event_min_safe=3, s=0**, K=1 (A1 sonucu gelmeden taban mekanik), 100K,
3 seed. Kollar **C-A** (açık) / **C-K** (kapalı). Yeni sayaç:
`event_protected` (doğru eylem VE sığınak açıldı).

**Analitik tabanlar (5 ajan, bağımsız):** kendi-ipucu tavanında (her
biri %50) korunma P(≥3)=0.50; şansta (%22) P(≥3)=0.09; mükemmel
iletişimde ~0.97.

**Çıtalar (son 20K, ≥2/3 seed):**
- **C1a (öğrenme):** C-K isabet ≥ 0.30, kendi-ipucu ≥ 0.60 (S3-K ile aynı
  rejimde öğrenme bozulmadı).
- **C1b (koordinasyon basıncı görünür):** C-K korunma oranı < isabet
  oranı × 0.8 (sığınak gerçekten "yalnız doğru" olanı cezalandırıyor).
- **C1c (kanal fayda, H3/H4):** C-A korunma oranı > C-K korunma + 0.05
  VE C-A isabet > C-K isabet + 0.03.
- **C1d (konuşan/dinleyen):** MI ≥ 0.05 bit (MM, p<0.05) VEYA pencere
  sinyal oranı ≥ 1.3× dışarı VEYA "duydu" isabeti > "duymadı" + 0.05.
- **C1e (fiyatlama):** C-A sinyal oranı son 20K < 0.5 ve düşüş eğilimi.

**Öngörüler (bağlayıcı):** C1a ✓ (0.7), C1b ✓ (0.8), C1c ✗ (0.7) — doğrudan
fayda var ama ajanın "sinyalim → onların eylemi → aynı turda benim
korunmam" zincirini 100K'da kurması için önce alıcının sembolü eyleme
bağlaması gerekir; tavuk-yumurta fayda yolu kısalsa da sürer. C1d ✗
(0.7). C1e ✓ (0.5).

**Sonuç matrisi:** C1c✓ → ADAY GÖZLEM (H4 yönünde, ilk kez), Beş Kapı
(C-K ablasyon hazır; ikiz; bit-eş; zaman çizgisi: hangi 10K'da doğdu;
0 bit). C1c✗ C1b✓ → tuzak kurulu, zincir kurulmuyor → A1 mekaniğiyle
C2 (topluluk) ve/veya uzun koşum (300K) ve/veya yetkin kadro (Q1
ağırlıkları + min_safe). C1b✗ → sığınak basınç üretmiyor (N kalibrasyonu).

**Beyan (M-09):** min_safe fizik değişikliğidir, görev "sürü alarmı"ndan
"ortak sığınak"a döner; S3-C/S3-K sonuçlarıyla karşılaştırma
"farklı görev" şerhiyle. Bit: 0 (KERNEL C notu).

### A1-eko S0 — SONUÇ: **mutasyon hipotezi de düştü** (2026-10-20, 11:05)
`runs/a1/S0_s*` (σ=0, açık, 100K): isabet 80-100K 0.24-0.26, kendi-ipucu
0.49-0.53, sinyal 0.78-0.88, ilk 2K sinyal 0.79-0.91 (açılış şoku var).
Prob (`signal_curse_probe_s0.json`): 4 çekirdeğin 2'sinde prim +0.27/+0.38
(argmax→sinyalli %60-68 @ %4 pay), 2'sinde nötr. **S0 A1a ✗** → prim
mutasyonsuz da oluşuyor. Duyma (speak-only probu) ve mutasyon (S0)
elendi. Okul (prim yok) ile ekoloji (prim var) arasında kalan farklar:
5 ajan/rekabet, olay cezasının ortak dünyası, ve **ömür**: okulda ~500
tur (PER tamponu 2000 pencereye kadar birikir, karşı-olgusal tekrar
çalışır), ekolojide ~40 tur (halef yeni OnlineAgent → PER ve optimizer
SIFIR; yaşam başına ~5 pencere → tekrar fiilen yok). M-05'in panzehiri
(K-110 PER) ekolojide hiç devreye girmiyor olabilir. Hipotez (c):
**prim = tekrar tamponsuz on-policy öğrenme.**

## A2′ — ÖN-KAYIT: deneyim tamponu mirası (koşumdan önce, M-08) (2026-10-20, 11:10)

`successor(..., inherit_per=True)`: halef, ölenin PER tamponunu ve
optimizer durumunu devralır (ağırlık mirası zaten vardı; bu, yaşantının
İSTATİSTİĞİNİN soy hattında sürmesi — DP-01 (b) "çekirdek+miras"ın
tampon ayağı). İçerik 0 bit (hangi deneyimin değerli olduğu söylenmez);
deneyci kararı (M-09). Kol **P-A**: σ=0.002, açık, inherit_per; taban
N-A (0.23-0.24, sinyal 0.77, prim soya bağlı) ve S0. 3 seed, 100K.
- **A2a (prim):** prob prim ≤ +0.1, argmax ≤ pay×1.5 (3/3).
- **A2b:** isabet ≥ 0.26, kendi-ipucu > 0.55; sinyal son 20K < 0.5.
- **Öngörü:** A2a ✓ (0.6), A2b ✓ (0.5).
- **Matris:** ✓ → PER mirası ekoloji varsayılanı (PL-35), topluluk gereksiz
  → C2 bu mekanikle. ✗ → kalan fark rekabet/ortak dünya → A1 topluluk
  sonucu (E3) belirleyici; o da ✗ ise prim bu mimaride çok-ajan
  rejimine özgü ve mekanik çare yok → S3 nihai hükme ek.

## C1 — SONUÇLAR: **sığınak basınç üretiyor ama bireysel öğrenmeyi bozuyor; dil yok** (2026-10-20, 12:00)

Veri: `runs/c1/`, `runs/c1/summary.json` (N=3, s=0, klon kadro, 100K).

| kol | medyan ömür | isabet 0-20K → 80-100K | korunma son 20K | kendi-ipucu son 20K | sinyal | hasat/1K | MI |
|---|---|---|---|---|---|---|---|
| **C-K** (kapalı) | 37-39 | 0.22 → **0.22-0.25** | **0.13-0.18** | 0.44-0.50 | 0 | 5.7-7.2 | — |
| **C-A** (açık) | 30 | 0.21 → **0.18-0.21** | **0.03-0.05** | 0.35-0.43 | 0.70-0.79 | 4.0-4.3 | 0.0003-0.0006 |
| S3-K K-K (referans, min_safe=0) | 42 | 0.22 → 0.31 | = isabet | ~0.60 | 0 | 5.7-6.2 | — |

- **C1b ✓:** korunma ≪ isabet (sığınak gerçekten yalnız-doğruyu
  cezalandırıyor). **C1a ✗:** kapalı kolda isabet 0.31 → 0.22-0.25'e,
  kendi-ipucu 0.60 → 0.45-0.50'ye geriledi. **C1c/d/e ✗.**
- **Mekanizma:** sığınak, kredi atamasını bozuyor: "doğru eylem" artık
  tek başına "ceza yok" demek değil (5 ajanın ≥3'ü doğru olmalı; kendi-
  ipucu rejiminde P≈0.5, şansta 0.09). Enerji kafası için eylem-koşullu
  sinyal seyreliyor → kendi-ipucu öğrenimi duruyor → iletecek bilgi
  doğmuyor. Doğrudan fayda, bireysel gradyanı öldürerek geldi. Açık kol
  ayrıca açılış şoku + maliyet (ömür 30).
- **Öngörü karnesi:** C1a ✓ (0.7) → YANLIŞ; C1b ✓ doğru; C1c/d ✗ doğru;
  C1e ✓ (0.5) → ✗.

**Yeni ders adayı (M-30 taslak): Ortak fayda, bireysel kredi atamasını
koruyarak verilmeli.** Sinyalin faydasını "aynı turda, doğrudan" kılmak
için bireysel korumayı gruba bağlayınca, ajanın kendi doğruluğunu
öğrenme sinyali silinir (korelasyon: kendi eylemi → sonuç, 0.5'e
düşer). Tuzak tasarımında "göndericiye fayda" ve "kendi eylemine kredi"
ayrı ayrı korunmalı; biri diğerini yemez. (M-28'in tasarım yüzü.)

## C2 — ÖN-KAYIT: yumuşak sığınak + yetkin kadro (koşumdan önce, M-08) (2026-10-20, 12:05)

Kredi atamasını korumak için iki değişiklik (M-06 ihlali değil:
C1'in başarısızlık nedeni iki ayağa birden bağlı, her biri beyanlı):
- **N=2** (P(≥2 doğru | kendi-ipucu %50) = 0.81; yalnız-doğru olmak çoğu
  zaman korur → bireysel gradyan büyük ölçüde geri; kanalın değeri
  oracle'da N=3 ile aynı: told/own 1.45).
- **Yetkin kurucu kadro:** Q1 final ağırlıkları (kendi-ipucu 0.75, isabet
  0.36) — ajan zaten kendi bitini okuyor; sorulan şey yalnız kanal.
Kollar **C2-A** (açık) / **C2-K** (kapalı); σ=0.002, s=0, K=1, 100K, 3 seed.
Not: A2′ (PER mirası) sonucu gelmeden mekanik varsayılan; A2′ ✓ çıkarsa
C3 onunla tekrarlanır.
- **C2a (yetkinlik korunur):** C2-K isabet son 20K ≥ 0.33, korunma ≥ 0.55.
- **C2b (kanal fayda, H3/H4):** C2-A korunma > C2-K korunma + 0.05 VE
  isabet > C2-K + 0.03.
- **C2c:** MI ≥ 0.05 ya da duydu > duymadı + 0.05 ya da pencere ≥ 1.3×.
- **C2d (açılış şoku):** C2-A isabet son 20K ≥ C2-K − 0.05 (Q2'de −0.08 idi).
- **Öngörüler:** C2a ✓ (0.7), C2d ✗ (0.6), C2b ✗ (0.75), C2c ✗ (0.7).
- **Matris:** C2b✓ → ADAY GÖZLEM, Beş Kapı. C2a✓ C2b✗ → tuzak kurulu, yetkin
  ajan bile kanalı kullanmıyor → mekanik (A2′/E3) sonucuna göre C3 ya da
  S3 nihai hüküm "C tasarımı da tavuk-yumurtayı kırmadı".

### A2′ ek ön-kayıt — kontrol kolu P-K (PK başlamadan, 13:20)
Ara okuma (94K): P-A isabet 0.37-0.49 (önceki açık kolların 2 katı; kendi-
ipucu tavanı 0.50'ye değiyor). Bu kazanç tamponun kendi-ipucu
öğrenimini hızlandırmasından mı, kanaldan mı? **P-K** (inherit_per,
kanal KAPALI, aynı seed'ler) başlatıldı.
- **A2c (kanal fayda):** P-A son 20K isabet > P-K + 0.05 VE P-A > 0.50
  (tavan üstü yalnız başkasının bitiyle).
- **A2d (tampon etkisi):** P-K > N-K (0.28) + 0.05 → PER mirası tek başına
  öğrenmeyi hızlandırıyor (mekanik kazanç, kanaldan bağımsız).
- **Öngörü:** A2d ✓ (0.8); A2c ✗ (0.7) — P-A ≈ P-K beklenir (kanal
  artık zarar vermiyor ama kazandırmıyor). P-A > P-K + 0.05 çıkarsa
  ADAY GÖZLEM, Beş Kapı derhal.

## A2′ — SONUÇ (P-A; P-K kontrolü bekleniyor): **PER mirası primi kesiyor, kanal açıkken öğrenme ilk kez bozulmuyor** (2026-10-20, 14:05)

Veri: `runs/a2/PA_s*`, `runs/a2/summary_pa.json`, prob `signal_curse_probe_pa.json`.

| kol | medyan ömür | isabet 0-20K → 40-60K → **80-100K** | kendi-ipucu son 20K | sinyal son 20K | ilk 2K sinyal | hasat/1K | MI |
|---|---|---|---|---|---|---|---|
| N-A (σ=0.002, açık, tampon sıfırlanır) | 40 | 0.21 → 0.23 → 0.23-0.24 | 0.47 | 0.77 | ~0.8 | 3.9-4.3 | 0.0004 |
| **P-A** (aynı + `inherit_per`) | **50** | 0.23-0.25 → 0.30-0.32 → **0.39 / 0.41 / 0.41** | **0.77-0.79** | **0.45-0.49** | 0.58-0.75 | **7.2-7.7** | 0.0006 |
| N-K (kapalı referans) | 43 | → 0.28 | 0.55 | 0 | — | 6.4-7.6 | — |

- **A2a ✓ (3/4 çekirdek):** prim −0.03 … −0.37 (doğru fiyat), argmax→
  sinyalli @%4 pay: 0/0/0/16%. **A2b ✓:** isabet 0.39-0.41 ≥ 0.26,
  kendi-ipucu 0.78 > 0.55, sinyal 0.45-0.49 < 0.5 (sınırda, ↓).
- **Mekanizma doğrulandı (hipotez c):** ekolojide 40 turluk ömür, her
  halefte PER'i sıfırlıyordu → karşı-olgusal tekrar yoktu → planlayıcı
  seçimi veriye yansıyor, model sahte prim öğreniyordu. Tampon soy
  hattında sürünce prim siliniyor, kanal açıkken kendi-ipucu öğrenimi
  kapalı kolları (0.28-0.31) bile aşıyor. **İlk kez açık kanal, kapalı
  kanaldan İYİ** — ama bunun kanaldan mı tampondan mı geldiği P-K
  (inherit_per + kapalı) ile ayrılacak (A2c/A2d).
- **Dil hâlâ yok:** MI 0.0006 bit, H 3.997, "duydu" isabeti < "duymadı"
  (0.31-0.33 vs 0.36-0.54; duymadı kümesi küçük). İsabet 0.41 < tavan
  0.50 → başkasının biti kullanılmıyor.
- **Öngörü karnesi:** A2a ✓ (0.6) doğru; A2b ✓ (0.5) doğru.

**Karar adayı (PL-35):** `inherit_per=True` ekoloji varsayılanı olur
(P-K sonucuyla birlikte kesinleşir). İçerik 0 bit; M-09 kaydı; "ölüm
gerçek" bedene uygulanır, yapı (ağırlık) ve yaşantı istatistiği (tampon)
soy hattında sürer (DP-01 b'nin tamamlanmış hâli).

## C2 — SONUÇLAR: **yetkin kadro + yumuşak sığınak: yetkinlik korunur, kanal yine kullanılmaz, açılış şoku sürer** (2026-10-20, 14:45)

Veri: `runs/c2/`, `runs/c2/summary.json` (N=2, s=0, Q1 kurucu, 100K).

| kol | medyan ömür | isabet 0-20K → 80-100K | korunma son 20K | kendi-ipucu | sinyal son 20K | ilk 2K sinyal | hasat/1K | MI |
|---|---|---|---|---|---|---|---|---|
| **C2-K** | 50 | 0.39-0.42 → **0.41-0.42** | **0.39-0.41** | 0.84-0.86 | 0 | 0 | 3.0-3.5 | — |
| **C2-A** | 40 | 0.26-0.29 → **0.34-0.36** | 0.31-0.34 | 0.67-0.71 | 0.50 | **0.90-0.97** | 2.3-2.9 | 0.0007-0.0025 |

- **C2a:** isabet ✓ (0.41 ≥ 0.33); korunma ✗ (0.40 < 0.55) — ama korunma
  ≈ isabet: N=2, 5 ajanda neredeyse her zaman açılıyor (P(≥2) ≈ 0.95+),
  yani N=2 basınç üretmiyor; N=3 öğrenmeyi bozuyordu (C1). İkisinin
  arası yok (tam sayı). **C2b ✗, C2c ✗** (MI 0.0007-0.0025; duydu ≤
  duymadı). **C2d ✗** (−0.06/−0.08; Q2 ile aynı açılış şoku: ilk 2K
  sinyal 0.90-0.97).
- **Okuma:** yetkin ajan (kendi-ipucu 0.85) kanalı 100K boyunca
  kullanmıyor; kanal yine açılış şoku + maliyet. C tuzağı (doğrudan
  fayda) tek başına tavuk-yumurtayı kırmadı. A2′ (PER mirası) açılış
  şokunu ve primi kesiyordu → **C3 = C2 + inherit_per.**
- **Öngörü karnesi:** C2a ✓ (0.7) yarı; C2d ✗ (0.6) doğru; C2b/C2c ✗ doğru.

## C3 — ÖN-KAYIT: C2 + PER mirası (koşumdan önce, M-08) (2026-10-20, 14:50)

C2 ayarı aynen (N=2, s=0, Q1 kurucu, σ=0.002) + `inherit_per`. Kollar
**C3-A** (açık) / **C3-K** (kapalı), 3 seed, 100K. (P-K kontrolü ayrıca
koşuyor; C3'ün kendi kapalı kolu kendi kontrolüdür.)
- **C3a (açılış şoku kalktı mı):** C3-A ilk 2K sinyal < 0.6 VE son 20K
  isabet ≥ C3-K − 0.03.
- **C3b (kanal fayda, H3/H4):** C3-A isabet > C3-K + 0.05 VE > 0.50.
- **C3c:** MI ≥ 0.05 ya da duydu > duymadı + 0.05 (3/3) ya da pencere ≥ 1.3×.
- **C3d (fiyatlama):** C3-A sinyal son 20K < 0.35.
- **Öngörüler:** C3a ✓ (0.55), C3d ✓ (0.5), C3b ✗ (0.75), C3c ✗ (0.7).
- **Matris:** C3b✓ → ADAY GÖZLEM, Beş Kapı (C3-K ablasyon, ikiz, bit-eş,
  zaman çizgisi, 0 bit). C3a✓ C3b✗ → "kanal nötr, kullanılmıyor" → son
  0-bit basamak: uzun koşum (300K) bu mekanikle; ✗ ise S3 nihai hükme
  Program A/C eki ve Ali'ye A′ (evrimsel önyükleme) önerisi.

## A1-eko E3 — SONUÇ: **topluluk + uyuşmazlık cezası primi kesmedi; K-115 GERİ ALINDI** (2026-10-20, 14:50)

`runs/a1/E3_s*` (K=3, β=1.0, σ=0.002, açık, 100K): isabet 80-100K
0.23-0.25, kendi-ipucu 0.47-0.49, sinyal son 20K 0.49-0.63, ilk 2K
0.62-0.72 (A1c ✗), hasat 3.4-3.6, ömür 40; maliyet 234 ms/tur (3×).
Prob (`signal_curse_probe_e3.json`, topluluk planlayıcısıyla): prim
**+0.29 … +0.31**, argmax→sinyalli %28-33 @ %4 pay → **A1a ✗, A1b ✗**.
- Uyuşmazlık, eğitimsiz sinyal sütunlarından doğmadı: üyeler aynı
  karıştırılmış veriyle aynı yöne öğrendi (prim kaynağı veri, model
  belirsizliği değil). A2′ (PER mirası) aynı anda primi kesti → doğru
  teşhis "tampon", yanlış teşhis "epistemik belirsizlik".
- **K-115 aday satırı GERİ ALINDI** (bit yazılmadı; kod kalır, varsayılan
  k=1 bit-eş). Öngörü karnesi: A1a ✓ (0.6) → YANLIŞ; A1c ✓ (0.7) → YANLIŞ.

### A2′ — NİHAİ (P-K kontrolü geldi, 16:05): **tampon etkisi ✓, kanal isabette nötr, hasatta maliyetli**
| kol | medyan ömür | isabet 80-100K | kendi-ipucu | hasat/1K | ölüm/100K |
|---|---|---|---|---|---|
| **P-K** (inherit_per, kapalı) | 50 | **0.39 / 0.39 / 0.39** | 0.78 | **11.1-11.8** | 8.6-8.8K |
| **P-A** (inherit_per, açık) | 50 | **0.41 / 0.41 / 0.39** | 0.77-0.79 | 7.2-7.7 | 9.8-10.0K |
| N-K / N-A (tamponsuz) | 43 / 40 | 0.28 / 0.23 | 0.55 / 0.47 | 6.4-7.6 / 3.9-4.3 | — |

- **A2d ✓:** PER mirası tek başına kapalı kolu +0.11 taşıyor (0.28 → 0.39),
  kendi-ipucu 0.55 → 0.78, hasat ×1.6, ömür 43 → 50. **Mekanik kazanç
  büyük ve kanaldan bağımsız.**
- **A2c ✗:** P-A − P-K = +0.01 (çıta +0.05), tavan 0.50 aşılmadı. Kanal
  isabette ilk kez NÖTR (önceki tüm koşumlarda −0.04 … −0.08), ama
  hasat −35%, ölüm +13%: sinyal maliyeti (0.47 × 0.5 enerji/tur) hâlâ
  ödeniyor, karşılığı yok.
- **Öngörü karnesi:** A2d ✓ (0.8) doğru; A2c ✗ (0.7) doğru.

**KARAR (PL-35, Claude — Ali yetki devri): `inherit_per=True` ekoloji
varsayılanı.** 0 bit; DP-01 (b) tamamlanır: ölüm bedene ve hidden'a,
yapı (ağırlık) ve yaşantı istatistiği (tampon, optimizer) soy hattına.
Gerekçe: M-05 panzehiri (K-110 PER) ekolojide ancak böyle çalışıyor;
sahte prim siliniyor; kapalı ve açık kol eşitleniyor.

## C3 — SONUÇLAR: **kanal ilk kez nötr ve doğru fiyatlı; tavana dayanıldı; başkasının biti hâlâ kullanılmıyor** (2026-10-20, 16:40)

Veri: `runs/c3/`, `runs/c3/summary.json`, prob `signal_curse_probe_c3.json`
(N=2, s=0, Q1 kurucu, σ=0.002, inherit_per, 100K).

| kol | medyan ömür | isabet 0-20K → 40-60K → **80-100K** | korunma | kendi-ipucu | sinyal son 20K | ilk 2K | hasat/1K | MI |
|---|---|---|---|---|---|---|---|---|
| **C3-K** | 50-52 | 0.41-0.43 → 0.44 → **0.43 / 0.45 / 0.45** | 0.42-0.44 | **0.88-0.89** | 0 | 0 | 2.0-2.5 | — |
| **C3-A** | 49-50 | 0.31-0.35 → 0.43-0.45 → **0.44 / 0.45 / 0.46** | 0.43-0.45 | **0.87-0.88** | **0.33-0.37** | 0.89-0.97 | 1.9-2.0 | **0.0022-0.0040** |

- **C3a ✓ (yarı):** son 20K açık ≥ kapalı − 0.03 ✓ (hatta +0.01); ilk 2K
  sinyal 0.89-0.97 ✗ — açılış spam'i yine var ama tampon mirasıyla
  40K içinde tamamen toparlanıyor (C2'de 100K'da toparlanmamıştı).
- **C3b ✗:** +0.01; isabet 0.46 ≤ 0.50 (kendi-ipucu tavanı: 0.88 × 0.5 +
  0.12 × 0.22 ≈ 0.47 — ajanlar tavana DAYANDI; üstü yalnız başkasının
  bitiyle). **C3c ✗:** MI 0.002-0.004 bit (programların en yükseği; S3-K
  0.0004 → A2′ 0.0006 → C2 0.001-0.0025 → C3 0.002-0.004: tekdüze ↑, ama
  çıtanın 1/10'u); "duydu" < "duymadı" (duymadı kümesi ~%0.1). **C3d
  sınırda:** 0.33 / 0.36 / 0.37 (çıta <0.35: 1/3).
- **Prob:** prim −0.6 (sinyal doğru fiyatlı), argmax→sinyalli %0-20 @%86,
  %0-2 @%4. Kalan sinyal oranı (0.35) ≈ ε 0.09 + CEM'in 16/17 sinyalli
  aday geometrisi → planlayıcı "umursamıyor": sinyal ne kazandırıyor ne
  (artık) kaybettiriyor kadar az maliyetli görünüyor (yuva maliyeti
  yarılıyor).
- **Öngörü karnesi:** C3a ✓ (0.55) doğru(yarı); C3d ✓ (0.5) sınırda;
  C3b ✗ (0.75) doğru; C3c ✗ (0.7) doğru.

**Durum (Program A + C birlikte):** üç mekanik engel kaldırıldı (drift,
tampon sıfırlama → sahte prim, açılış şoku), görev doğrudan faydalı hâle
getirildi (sığınak), ajanlar kendi-ipucu tavanında ve kanal bedava-
yakın. Yine de kimse başkasının bitini kullanmıyor; MI tekdüze ama
mikroskobik artıyor. Matris: C3a✓ C3b✗ → **son 0-bit basamak: C4 uzun
devam.**

## C4 — ÖN-KAYIT: C3 devamı, +200K (koşumdan önce, M-08) (2026-10-20, 16:45)

C3-A ve C3-K kendi final ağırlıklarından (ve tamponlarından değil:
tampon dosyaya yazılmıyor, yeni başlar — beyan) 200K daha; dünya seed
+400. Toplam: 300K kapalı (Q1) + 300K sığınak.
- **C4a (dil):** C4-A son 20K isabet > C4-K + 0.05 VE > 0.50 (3/3'te > 0.50).
- **C4b (konuşan/dinleyen):** MI ≥ 0.05 bit MM p<0.05; VEYA MI eğilimi
  C3'ün ≥ 3 katı (≥ 0.01) VE "duydu" > "duymadı" + 0.05 (2/3).
- **C4c (fiyatlama):** C4-A sinyal son 20K < 0.30.
- **Öngörüler:** C4a ✗ (0.8), C4b ✗ (0.65; MI 0.005-0.01'e tırmanabilir
  ama kullanım yok), C4c ✓ (0.55).
- **Matris:** C4a✓ → ADAY GÖZLEM, Beş Kapı derhal (C4-K ablasyon, ikiz,
  bit-eş tekrar, zaman çizgisi, 0 bit) ve Ali'ye bildirim. C4a✗ →
  Program A+C kapanışı: "kanal nötr, fiyatlı, kullanılmıyor" nihai; Ali'ye
  A′ (evrimsel önyükleme) ve tasarım alternatifleri; S3 nihai hükme ek.

## C4 — SONUÇLAR: **plato; kanal nötr, fiyatlı, kullanılmıyor** (2026-10-20, 19:45)

Veri: `runs/c4/`, `runs/c4/summary.json`, prob `signal_curse_probe_c4.json`
(C3 devamı, +200K; toplam 300K kapalı + 300K sığınak).

| kol | medyan ömür | isabet 0-50K → 100-150K → **180-200K** | kendi-ipucu | sinyal son 20K | hasat/1K | MI |
|---|---|---|---|---|---|---|
| **C4-K** | 54-55 | 0.44 → 0.44-0.46 → **0.44 / 0.45 / 0.45** | **0.89-0.90** | 0 | 1.6-2.1 | — |
| **C4-A** | 50-51 | 0.44-0.45 → 0.45 → **0.46 / 0.44 / 0.45** | 0.87 | **0.29-0.35** | 1.3-1.6 | **0.0014-0.0034** |

- **C4a ✗:** fark ≤ +0.01, 0.50 aşılmadı; iki kol 200K boyunca 0.44-0.46'da
  DÜZ (kendi-ipucu tavanı: 0.89 × 0.5 ≈ 0.45 — tam oradalar).
- **C4b ✗:** MI 0.0014-0.0034 (C3 ile aynı; artış durdu); "duydu" 0.44 <
  "duymadı" 0.60-0.63 (duymadı kümesi ~%0.5; "kimsenin konuşmadığı"
  olaylar ya da olaysız pencereler — yorumlanamaz, M-03).
- **C4c:** 0.29 / 0.31 / 0.35 → 1/3 (sınırda). Prob: prim −0.35/−0.5,
  argmax→sinyalli %27-38 @ %86 pay, %5 @ %4 pay (doğru fiyat; CEM
  geometrisi kalan sinyali açıklıyor).
- **Öngörü karnesi:** C4a ✗ (0.8) doğru; C4b ✗ (0.65) doğru; C4c ✓ (0.55)
  → sınırda.

---

# PROGRAM A + C KAPANIŞI (2026-10-20, 20:00)

**Yapılan (bugün, 20 koşum + 3 okul + 3 oracle):** A0 (okul, kanal açık),
A1-eko S0/E3, A2′ P-A/P-K, C0 oracle, C1, C2, C3, C4.

**Kazanımlar (mekanizma, hepsi 0 bit):**
1. **Sahte sinyal priminin kaynağı bulundu ve kesildi:** halef her
   ölümde PER tamponunu sıfırlıyordu (ömür ~40 → tampon ~5 pencere →
   karşı-olgusal tekrar yok). `inherit_per` ile prim silindi; kapalı kol
   0.28 → 0.39, açık kol 0.23 → 0.41, ömür +25%, hasat ×1.6. **PL-35
   KARAR: varsayılan.** Yanlış adaylar sırayla elendi: duyma gürültüsü
   (speak-only prob), mutasyon (S0), epistemik belirsizlik (E3 topluluk
   ✗, K-115 geri alındı).
2. **Açılış şoku** PER mirasıyla 40K içinde toparlanıyor (C3; C2'de
   100K'da toparlanmıyordu).
3. **Sığınak görevi:** N=3 bireysel kredi atamasını öldürdü (C1, M-30);
   N=2 basınç üretmedi ama yetkinliği korudu (C2-C4).
4. **Ajanlar tavanda:** kendi-ipucu 0.87-0.90, isabet 0.44-0.46 ≈ kendi-
   ipucu tavanı. **Kanal ilk kez nötr** (açık = kapalı), doğru fiyatlı
   (prob), planlayıcı sinyali "umursamıyor" (CEM geometrisi + yuva
   indirimi → kalan 0.3 sinyal/tur).

**Sonuç:** Mekanik engellerin tamamı kaldırıldıktan sonra da hiçbir
soy başkasının bitini kullanmıyor. I(ipucu;sembol) dört programda
0.0004 → 0.004'e çıkıp platoya oturdu (çıta 0.05). Tavuk-yumurta, A
(mekanik) ve C (doğrudan fayda) ile kırılmadı.

**Nihai hüküm güncellemesi (S3 NİHAİ HÜKÜM'e ek):** H4 NEGATİF hükmü
güçlendi: olumsuzluk artık mekanik artefaktlarla (drift, prim, şok)
açıklanamıyor; kanal kullanılabilir, fiyatlı ve nötrken bile kullanılmıyor.
Kalan açıklama tasarımsal ve teorik: **sembol-dünya olumsallığını kurmak
için ilk konuşanın, alıcının öğrenmesini beklerken bedel ödemesi
gerekir; öğrenen bireysel sistemde bu yatırımı yapan seçilmez.** (M-28)

**Yeni dersler:** M-30 (ortak fayda / kredi ataması), M-31 (halefiyet,
öğrenme mekaniğinin her parçası için ayrı karardır: ağırlık, tampon,
optimizer, hidden — "ölüm gerçek" cümlesi bunların hangisine dediğini
söylemek zorunda; tampon sıfırlaması üç programlık sahte primin
kaynağıydı). METODOLOJI'ye işlendi.

**Sonraki program (PL-36, Ali kararı):**
- **A′ Evrimsel önyükleme (0 bit, uzun):** yetkin, tamponlu nüfusta
  (C4 ağırlıkları) soy-düzeyi varyasyon + seçilim; "ipucu görünce
  sembol" varyantının rastgele doğup alıcının öğrenmesiyle çoğalması.
  Biyolojideki çözüm; ≥1M tur, günler.
- **D Tasarım: alıcı önce** (0 bit, dünya-tarafı): alıcının sembolü
  eyleme bağlamasını, gönderici olmadan öğrenilebilir kılmak — ör.
  dünyanın kendisi öncüyü bazen bir sembol olarak "yayınlasın"
  (sensory bias / ritüelleşme emsali). Dil VERMEZ (sembol-anlam
  eşlemesi yine öğrenilir) ama tavuk-yumurtanın alıcı ayağını kırar.
  Anayasal tartışma: dünya "konuşuyor" mu olur? (M-25 ile sayılmalı.)
- **E Kimlikli/yerel kanal + tekrarlı eş** (PL-28 geri): karşılıklılık
  için gerekli yapı; deneyin "en temiz kanal" iddiasını zayıflatır.
**Tavsiye:** D'nin M-25 analizi (0 bit mi?) + A′ paralel.

---

# PROGRAM A′ — evrimsel önyükleme, ada modeli (Ali kararı, 2026-10-20 akşam)

## A′ — ÖN-KAYIT (koşumdan önce, M-08)

**Gerekçe.** A+C kapanışı: tavuk-yumurta bireysel öğrenmeyle kırılmıyor.
Bireysel seçilim (S3-H max_age) bedavacıyı ödüllendirir; alarm çağrıları
doğada akrabalık/grup düzeyinde seçilimle evrilir. **Tasarım:** G ada
(her biri 5 ajanlı bağımsız ekoloji), dönem = 10K tur; dönem sonunda
adalar **olay isabetine** göre sıralanır, en kötü Q ada en iyi Q adanın
mutasyonlu (σ_kopya=0.005, tüm ağırlıklar) kopyasıyla değiştirilir.
`training/island_evolution.py`. Ajana bit gitmez: fitness ajanın
girdisine/kaybına girmez, yalnız hangi ağırlıkların taşındığını seçer
(nüfus kuralı, M-09). Her dönem yeni dünya seed'i. PER her dönem
yeniden dolar (beyan).

**Kollar:** **EV-A** kanal açık, G=6, Q=2, kurucular C4-A ağırlıkları
(3 soy × 2); **EV-K** kanal kapalı, G=3, Q=1, kurucular C4-K. Ekoloji
ayarı C4 ile aynı (sığınak N=2, s=0, σ=0.002, yuva, inherit_per,
her 10 tur, lead 4). 30 dönem (300K tur/ada).

**Neden kontrol kolu:** grup seçilimi kendi-ipucu öğrenimini de
seçebilir; tavanı (≈0.45) aşmayı yalnız kanal açıklar.

**Çıtalar:**
- **EV1 (kalıtım, fizibilite):** ilk 5 dönemde, değiştirilmeyen adalar
  için isabet(k) ile isabet(k+1) arası Spearman ort. > 0.3 — seçilim bir
  şeyi taşıyor. ✗ ise seçilim gürültüyü seçiyor → dönem uzunluğu ×3 ya
  da ada sayısı ×2 (beyanlı revizyon).
- **EV2 (dil, H4):** son 3 dönemde EV-A en iyi ada isabeti > 0.50 VE EV-A
  ortalaması > EV-K ortalaması + 0.05.
- **EV3 (konuşan):** EV-A'da herhangi bir adada MI ≥ 0.05 bit (MM) son 3
  dönemde; ya da MI maks dönemlere göre tekdüze ↑ ve ≥ 0.02.
- **EV4 (soy süpürmesi):** EV-A'da son dönemde tek kurucu soy baskın
  (grup seçilimi çalışıyor işareti; dil iddiası değil).

**Öngörüler (bağlayıcı):** EV1 ✓ (0.6). EV4 ✓ (0.7). EV3 ✗ (0.7). EV2 ✗
(0.8) — 30 dönem, 6 adalık nüfusta bir uzlaşının tesadüfen doğması için
küçük olabilir; ama MI'nin seçilimle tırmanıp tırmanmadığı (EV3'ün
eğilim kolu) asıl göstergedir.

**Sonuç matrisi:** EV2✓ → ADAY GÖZLEM (H4), Beş Kapı: EV-K ablasyon,
kazanan adanın bit-eş tekrarı, zaman çizgisi (hangi dönemde, hangi
soyda), sembol-anlam tablosu (keyfi ama paylaşılan mı: farklı adalarda
farklı sembol?), 0 bit. EV2✗ EV3 eğilim ✓ → seçilim çalışıyor ama
ölçek yetmiyor → 60-100 dönem / daha çok ada (Ali kararı). İkisi ✗ →
"grup seçilimi bu ölçekte de kırmadı"; Program A′ kapanışı.

### A′ ara sonuç — EV1 ✗ ve ön-kayıtlı revizyon (2026-10-20, 21:45)
İlk 7 dönem (10K): EV-A isabet ort 0.42-0.45, maks 0.45-0.48; EV-K 0.44-0.45;
MI maks 0.007-0.012 (gürültü düzeyi). Kalıtım (korunan adalarda dönemler
arası Spearman): −0.20, 0.20, 0.60, −0.60, 0.80, 0.20 → **ort 0.17 < 0.3
→ EV1 ✗**. Adalar arası fark (~0.02) dönem içi örnekleme hatasıyla aynı
büyüklükte; seçilim şansı seçiyor. Ön-kayıtlı revizyon uygulandı:
**dönem 10K → 30K** (hata ~√3 azalır), adaların 7. dönem ağırlıklarından
devam, 10 dönem (`runs/ev/open30`, `runs/ev/mute30`). Not: tüm adalar
kendi-ipucu tavanında; seçilimin seçebileceği kalıtsal varyasyon,
tavanı aşan bir kanal kullanımı doğana kadar fiilen yok — EV1'in
düşmesi de bunun belirtisi.

## A′ — SONUÇLAR (2026-10-21, 04:40)

Veri: `runs/ev/{open,mute}` (7×10K) + `runs/ev/{open30,mute30}` (10×30K),
`state.json` dosyaları.

| | EV-A (açık, 6 ada) | EV-K (kapalı, 3 ada) |
|---|---|---|
| isabet son 3 dönem ort | 0.431 / 0.434 / 0.438 | 0.452 / 0.448 / 0.446 |
| en iyi ada son 3 | 0.440 / 0.449 / 0.447 | 0.455 / 0.452 / 0.450 |
| kendi-ipucu son dönem | 0.85 | 0.89 |
| hasat/1K son dönem | 1.45 | 1.67 |
| sembol MI maks (17 dönem) | 0.012 → 0.006 (Spearman −0.73, AZALIYOR) | — |
| soy | tek kurucu soy (src0) süpürdü | tek soy |

- **EV1 ✓ (revizyon sonrası):** 30K dönemde Spearman ort 0.47 (10K'da 0.17 ✗).
- **EV2 ✗:** en iyi ada 0.45 < 0.50; açık kol kapalının 0.01-0.02 ALTINDA.
- **EV3 ✗:** sembol MI 0.004-0.012, eğilim azalan.
- **EV4 ✓:** açıkta tek soy baskın.
- **Öngörü karnesi:** EV1 ✓ (0.6) → revizyonla doğru; EV4 ✓ doğru; EV2/EV3 ✗ doğru.

**Hüküm (ön-kayıtlı çıtalarla):** grup seçilimi bu ölçekte (17 dönem,
360K tur/ada) tavuk-yumurtayı kırmadı; sembol kimliği hiçbir bilgi
taşımıyor; seçilim, kanalın yükünü azaltacak yönde değil, en yetkin
soyu çoğaltacak yönde çalıştı.

### POST-HOC ADAY GÖZLEM — "konuşma kararı" ipucu değerini taşıyor (ön-kayıtsız; doğrulama ön-kaydı aşağıda)

Sembol kimliği değil, **sinyal verip vermeme** ajanın kendi ipucu
DEĞERİNE bağlı. Uyarı penceresinde P(sinyal | değer) ve I(değer; sinyal
var/yok) (değer 0/1 eşit olası varsayımıyla; ipucu×sembol tablosu satır
toplamları + bekleme turu sayısı):

| koşum | P(sinyal|0) | P(sinyal|1) | I (bit) |
|---|---|---|---|
| S3-K K-A (tampon sıfırlanır) | 0.80 | 0.84 | 0.002 |
| A2′ P-A (tampon mirası) | 0.41 | 0.64 | 0.041 |
| C3-A | 0.46 | 0.65 | 0.027 |
| **C4-A (3 seed)** | **0.20-0.25** | **0.50-0.62** | **0.074-0.105** |
| EV open30 son dönem | 0.22-0.24 | 0.49-0.54 | 0.050-0.083 |

- Tampon mirasıyla (PL-35) DOĞUYOR ve süreyle büyüyor (0.002 → 0.04 →
  0.10). Bit İNDEKSİNDEN bağımsız (01 ve 11 satırları birlikte yüksek):
  taşınan şey "benim bitim 1" bilgisi.
- **Etiket: ADAY GÖZLEM, post-hoc.** (i) Ölçü ön-kayıtsız (ön-kayıt
  sembol kimliğine bakıyordu). (ii) Dinleyen yok: isabet tavanı
  aşılmadı, "duydu/duymadı" ayrımı ölçülemiyor. (iii) **H0 açık:**
  değer=1 iken gözlemde (1,0) öncü hücresi yanar; model bu ek "tehlike
  benzeri" girdiye sinyal artışıyla tepki veriyor olabilir — başkası
  için değil, refleks. Bunu ayıran test: **kimse duyamazken** (speak
  modu) asimetri sürüyor mu?

## A″ — ÖN-KAYIT: konuşma-kararı asimetrisinin doğrulaması (koşumdan önce, M-08) (2026-10-21, 04:45)

Kurucular C3-A final ağırlıkları (asimetri 1.4-1.9 iken), dünya seed
+500, C4 ayarı (sığınak N=2, s=0, inherit_per), 100K, 3 seed:
- **R-open:** kanal açık (tekrar; yeni seed'ler).
- **R-speak:** gönderir ama KİMSE DUYMAZ (alınan vektör sıfır) — dinleyici
  faydası imkânsız.
**Ölçüler:** I(değer; sinyal var/yok) son 50K, P(sinyal|değer).
- **D1 (tekrar):** R-open'da I ≥ 0.05 bit (≥2/3) — bulgu tekrarlanıyor.
- **D2 (dinleyiciye yönelik mi):** R-open I − R-speak I ≥ 0.03 bit (≥2/3).
  D2 ✗ (R-speak'te de aynı) → **refleks/girdi etkisi**; "konuşan var"
  iddiası düşer, yalnız "girdiye bağlı sinyal üretimi" kalır.
- **D3 (dinleyen):** R-open isabet > kendi-ipucu tavanı (≈ own_cue×0.5 +
  (1−own_cue)×0.22) + 0.03.
**Öngörüler (bağlayıcı):** D1 ✓ (0.75); D2 ✗ (0.65) — en sade açıklama
girdi refleksi; D3 ✗ (0.85).

## A″ — SONUÇLAR: **konuşma kararı ipucu değerini taşıyor, ama büyük ölçüde refleks** (2026-10-21, 06:00)

Veri: `runs/a3/{Ropen,Rspeak}_s*` (C3-A kurucu, yeni dünyalar, 100K).

| kol | seed | I(değer; sinyal var/yok) | P(sinyal|0) | P(sinyal|1) | isabet son 20K | kendi-ipucu tavanı | fark |
|---|---|---|---|---|---|---|---|
| Ropen | 3001 | **0.091** | 0.24 | 0.58 | 0.462 | 0.464 | −0.002 |
| Ropen | 3002 | **0.098** | 0.22 | 0.58 | 0.468 | 0.462 | +0.006 |
| Ropen | 3003 | **0.078** | 0.21 | 0.52 | 0.444 | 0.458 | −0.014 |
| Rspeak | 3001 | 0.069 | 0.24 | 0.54 | 0.437 | 0.465 | −0.028 |
| Rspeak | 3002 | 0.068 | 0.21 | 0.51 | 0.447 | 0.468 | −0.021 |
| Rspeak | 3003 | 0.069 | 0.20 | 0.49 | 0.451 | 0.464 | −0.013 |

- **D1 ✓** (3/3 ≥ 0.05): bulgu bağımsız dünyalarda tekrarlandı.
- **D2 ✗ (sınırda):** Ropen − Rspeak = +0.022 / +0.030 / +0.009 (çıta ≥0.03,
  2/3 → 1/3). Asimetrinin ~%75'i kimse duymazken de var → **girdi
  refleksi**: değer=1 iken yanan öncü hücresi sinyal üretimini artırıyor.
  Kalan ~%25 (+0.02 bit) duyma koşuluna bağlı, işaret 3/3 aynı yönde ama
  çıtanın altında.
- **D3 ✗:** isabet kendi-ipucu tavanında (fark −0.014…+0.006); dinleyen yok.
  (Not: Rspeak tavanın 0.01-0.03 altında, Ropen tavanda; fark küçük,
  ön-kayıtsız — kayıt olarak.)
- **Öngörü karnesi:** D1 ✓ (0.75) doğru; D2 ✗ (0.65) doğru; D3 ✗ doğru.

**Hüküm:** post-hoc aday gözlem **kısmen düştü**: "konuşan var" iddiası
yerine "**girdiye bağlı sinyal üretimi** (refleks), üstünde küçük ve
tutarlı ama çıta altı bir dinleyici-koşullu bileşen". Beş Kapı: tekrar ✓,
ablasyon (speak) ✗, dinleyen ✗ → İDDİA yok. Değeri: dil tuzağında
göndericinin ilk kez ipucuyla OLUMSAL bir sinyal ürettiği gözlendi;
bu, tavuk-yumurtanın "gönderici" yumurtası — dinleyici öğrenmesi için
gereken ham malzeme artık ortamda var (0.07-0.10 bit/olay/ajan).

---

# PROGRAM A′/A″ KAPANIŞI ve DURUM (2026-10-21, 06:05)

1. Grup seçilimi (ada modeli, 360K tur/ada) sembol anlamı doğurmadı.
2. Ama tampon mirası rejiminde ajanlar **ipucuna bağlı konuşma
   kararı** geliştirdi (0.10 bit) — büyük kısmı refleks; dinleyici yok.
3. **Kalan tek eksik halka: dinleyici.** Ortamda "konuşan değer=1"
   bilgisi dolaşıyor; hiçbir ajan bunu eyleme çevirmiyor (alınan sinyal
   ⇒ kutup çıkarımı). Neden: küresel kanalda 4 göndericiden hangisinin
   hangi BİT İNDEKSİNİ taşıdığı bilinmiyor; "biri konuştu" 2 bitlik
   kutbu çözmeye yetmiyor (yalnız sinyal VARLIĞI, indeks/değer ayrımı
   yok → alıcı için bilgi ≪ 0.10 bit). Bu bir **kanal-tasarım tavanı**:
   varlık-kodlu sinyal, kimliksiz küresel kanalda kutup bilgisini
   alıcıya ulaştıramıyor.
**Sonraki adım adayı (PL-37, Ali):** (i) alıcının erişebildiği bilgiyi
ölçmek (oracle: "varlık kodlu" mükemmel gönderici + optimal alıcı bu
kanalda ne kazanır? — 0 bit, 1 saat); kazanç küçükse kanal tasarımı
(kimlik ya da yerellik, PL-28 geri) anayasal karar olarak Ali'ye.

## PL-37 / CH0 — ÖN-KAYIT: varlık-kodlu kanal oracle'ı (koşumdan önce, M-08) (2026-10-21)

**Soru:** kimliksiz küresel kanalda "bitim 1 ise konuşurum" (varlık kodu)
göndericileri, OPTİMAL bir alıcıya kutbu ne kadar çözdürür? Saf Monte
Carlo (`training/channel_oracle.py`, 0 bit, ölçüm aleti): kutup K=4
tekdüze, 5 ajan, her ajan olay başına rastgele bir bit indeksi görür;
alıcı kendi (indeks, değer) + diğer 4'ten duyulan sinyal SAYISI ile
Bayes-optimal kutup seçer. Kollar: `own` (yalnız kendi bit), `presence`
(mükemmel varlık kodu P(s|1)=1, P(s|0)=0), `presence_obs` (gözlenen:
0.55 / 0.22), `told` (sembol indeks+değer taşır, mükemmel konvansiyon).
Ölçüler: isabet, sığınak (N=2) korunması, I(kutup; duyulan | kendi bit).
- **CH-a (kanal yeterli mi):** presence_obs isabet − own ≥ 0.10 → kanalda
  bilgi var, eksik olan ALICI öğrenmesi (ajan sorunu) → sıradaki adım
  alıcı tarafı. < 0.05 → **kanal tavanı** (tasarım sorunu) → kimlik/
  yerellik kararı Ali'ye.
- **Öngörü:** presence (mükemmel) own'dan +0.15-0.25; presence_obs
  +0.03-0.08 (CH-a ✗ bölgesi) (0.6).

### CH0 — SONUÇ: **kanal tavan DEĞİL; masada bilgi var, dinleyen yok** (2026-10-21)
`runs/ch0_channel_oracle.json` (100K olay):
| kol | isabet | korunma (N=2) | I(kutup; duyulan sayı | kendi bit) |
|---|---|---|---|
| own | 0.500 | 0.468 | — |
| **presence_obs** (0.55/0.22) | **0.637** | 0.620 | 0.083 bit |
| presence (1.0/0.0) | 0.969 | 0.969 | 0.829 bit |
| told | 0.969 | 0.967 | — |
- **CH-a ✓** (+0.137 ≥ 0.10). Öngörüm ("kanal tavanı", +0.03-0.08) YANLIŞ:
  konuşan SAYISI kutbun bit sayısını (popcount) verir; kendi bitle
  birleşince kutup çözülür. Bugünkü gürültülü göndericiler bile optimal
  alıcıya +0.14 isabet sunuyor; ekolojide alınan: ~0. **Eksik halka
  alıcı öğrenmesi.** (Not: alınan vektör doygun one-hot; rastgele
  sembollerde farklı sembol sayısı ≈ konuşan sayısı, çakışma nadir.)

## RS — ÖN-KAYIT: alıcı okulu (koşumdan önce, M-08)
Olay okulu (tek ajan, yetiştirme kabı, inherit yok — tek beden ölünce
ağırlık sürer), her 10 tur, lead 4, ceza 25, kanal kapalı (ajan
yayınlamaz), 100K, 2 seed. Sanal 4 komşu (dünya-tarafı ölçüm aleti):
- **RS-0:** komşu yok (taban; kendi-ipucu tavanı ~0.47).
- **RS-obs:** komşular gözlenen kuralla (P(s|1)=0.55, P(s|0)=0.22, pencere
  dışı 0.3) rastgele sembol yayınlar.
- **RS-1:** mükemmel varlık kodu (1.0/0.0, dışarı 0.3).
**Çıtalar (son 20K):** RS-1 isabet > RS-0 + 0.15 (alıcı öğrenmesi MÜMKÜN);
RS-obs > RS-0 + 0.05 (gürültülü göndericiyle de mümkün).
**Öngörü:** RS-1 ✓ (0.6), RS-obs ✗ (0.6) — sayma (kaç sembol yandı) ×
kendi bit × eylem etkileşimini öğrenmek okul ölçeğinde bile zor olabilir.
**Matris:** RS-1 ✓ RS-obs ✓ → ekolojide alıcı deneyimi yetmiyor → ekoloji
koşulunu okula yaklaştır (uzun ömür / tampon / sıklık). RS-1 ✓ RS-obs ✗ →
göndericinin netleşmesi gerek (tavuk-yumurta sürer ama sayısal). RS-1 ✗ →
mimari: sayma/birleştirme öğrenilemiyor (doygun girdi + GRU) — anayasal
tartışma (sayı kodlu alım; K-114 revizyonu).

### RS — SONUÇ: **dinleyici öğrenebiliyor — ilk kez kendi-ipucu tavanı aşıldı (okulda, mükemmel varlık kodlu komşularla)** (2026-10-21, 09:00)
`runs/rs/*/school.json` (100K, lead 4, 2 seed):
| kol | isabet 10K → 50K → 100K | son 20K | kendi-ipucu | STAY |
|---|---|---|---|---|
| RS-0 (komşu yok) | 0.25 → 0.39-0.41 → 0.42 | **0.42** | 0.82-0.84 | 0.46-0.50 |
| RS-obs (0.55/0.22) | 0.20-0.23 → 0.38-0.43 → 0.43 | **0.43** | 0.82-0.83 | 0.44 |
| **RS-1 (1.0/0.0)** | 0.26 → 0.51-0.54 → 0.62 | **0.62** | 0.74-0.77 | 0.28-0.30 |
- **RS-1 ✓** (+0.20 > +0.15; 2/2): tek ajan, rastgele sembollerle yayın
  yapan komşuların SAYISINI kendi bitiyle birleştirip kutbu çözmeyi
  ÖĞRENDİ; isabet 0.50 tavanının açık üstünde (0.62) ve hâlâ ↑. Kendi-
  ipucu tutarlılığı düştü (0.75): ajan artık kendi bitine karşı da
  hareket ediyor, çünkü duyduğu bilgiyi tercih ediyor — tam olması
  gereken davranış.
- **RS-obs ✗** (+0.01): gözlenen gürültülü göndericiyle (optimal alıcıya
  +0.14 bilgi var) öğrenme görünmüyor.
- **Öngörü karnesi:** RS-1 ✓ (0.6) doğru; RS-obs ✗ (0.6) doğru.
- **Bu, PETRI'de bir öğrenen ajanın başkalarının sinyalinden bilgi
  çıkarıp eyleme çevirdiği İLK ölçümdür.** Etiket: ADAY GÖZLEM (okul;
  sanal göndericiler dünya-tarafı ölçüm aleti, gönderici kuralı
  hediye — `told` emsali: alıcı TAVANINI ölçer). Mimari sorunu YOK
  (matrisin "RS-1 ✗" dalı kapandı: doygun girdi + GRU sayabiliyor).

**Matris hücresi: RS-1 ✓ RS-obs ✗ → tavuk-yumurta SAYISAL:** alıcı,
gönderici ne kadar netse o kadar öğreniyor; bugünkü göndericiler
(I≈0.08-0.10 bit, büyük kısmı refleks) dinleyici öğrenmesini
tetiklemek için çok gürültülü. Sıradaki soru: dinleyici öğrenmesini
tetikleyen gönderici netliği eşiği nedir (doz-cevap: P(s|1)/P(s|0) =
0.9/0.1, 0.8/0.2, 0.7/0.2)? Eşik bulunursa ekolojide "gönderici
netleşmesi" ile "dinleyici öğrenmesi" arasındaki geri besleme döngüsü
(eşik üstü → alıcı dinler → gönderici için fayda doğar → netleşir)
tasarlanabilir; eşik bugünkü 0.55/0.22'ye yakınsa uzun ekoloji yeter.

## RS-dose — ÖN-KAYIT: dinleyici öğrenmesi için gönderici netliği eşiği (koşumdan önce, M-08)
Aynı okul ayarı, sanal komşular P(s|1)/P(s|0) ∈ {0.9/0.1, 0.8/0.2,
0.7/0.2}, pencere dışı 0.3, 100K, 2 seed. Optimal alıcı tavanları
`channel_oracle` ile aynı koşulda hesaplanır (rapora eklenecek).
- **Çıta:** her doz için son 20K isabet > RS-0 (0.42) + 0.05 → o doz
  "dinleyici öğrenmesini tetikler". Eşik = çıtayı geçen en gürültülü doz.
- **Öngörü:** 0.9/0.1 ✓, 0.8/0.2 ✓, 0.7/0.2 ✗ (0.5).

### RS-dose — SONUÇ: **dinleyici öğrenmesi için gönderici netliği eşiği ≈ 0.18 bit** (2026-10-21, 10:00)
`runs/rs/dose*_s*/school.json` (100K, 2 seed; optimal tavanlar `channel_oracle`):
| gönderici P(s|1)/P(s|0) | gönderici bilgisi (bit) | optimal alıcı | öğrenen alıcı son 20K | RS-0 + 0.05 çıtası |
|---|---|---|---|---|
| 0.55 / 0.22 (ekolojide gözlenen) | 0.08 | 0.64 | 0.43 / 0.43 | ✗ |
| 0.7 / 0.2 | 0.18 | 0.71 | 0.47 / 0.50 | ✓ sınırda (1/2 harfen, 2/2 ≥ 0.47) |
| 0.8 / 0.2 | 0.25 | 0.75 | 0.53 / 0.53 | ✓ |
| 0.9 / 0.1 | 0.45 | 0.82 | 0.59 / 0.60 | ✓ |
| 1.0 / 0.0 | 0.83 | 0.97 | 0.62 / 0.62 | ✓ |
- **Temiz doz-cevap eğrisi.** Dinleyici öğrenmesi gönderici netliğiyle
  tekdüze artıyor; eşik ≈ 0.7/0.2 (≈0.18 bit). Öğrenen alıcı optimalin
  ~%40-60'ını 100K'da alıyor, hâlâ ↑. Öngörü karnesi: 0.9 ✓, 0.8 ✓
  doğru; 0.7 ✗ (0.5) → sınırda geçti.
- **Ekolojiye çeviri:** bugünkü ekoloji göndericileri 0.08 bit (A″; ~%75
  refleks) — eşiğin **yarısı**. Tavuk-yumurta artık bir sayı: gönderici
  netliği ~2× artarsa dinleyici öğrenmesi başlar; dinleyici başlarsa
  göndericiye fayda (sığınak) doğar ve netlik seçilebilir/öğrenilebilir
  hâle gelir (geri besleme döngüsü).

**PL-37 → PL-38 önerisi (Ali kararı):**
- **(a) 0 bit, uzun ekoloji:** C4 rejiminde gönderici asimetrisi
  programlar boyunca büyüdü (0.002 → 0.04 → 0.10); 500K+ tur ve/veya ada
  evrimiyle 0.18'e ulaşıp ulaşmadığını izle; ulaşırsa dinleyici
  öğrenmesinin kendiliğinden başlayıp başlamadığı ölçülür. Sabır işi.
- **(b) 0 bit, refleksi büyütmek:** asimetri büyük ölçüde öncü
  hücresine refleks. Öncü algısını güçlendirmek (ör. lead 4 → 6, öncünün
  pencere boyunca kalıcı oluşu) refleksi ve dolayısıyla gönderici
  netliğini artırabilir — dünya-tarafı kalibrasyon, M-25 analizi şart
  (refleksin "konuşma" sayılmayacağı beyanıyla).
- **(c) Sinyal maliyetini düşürmek:** anayasal (0.5 sabit); yapılmaz.
Tavsiye: (b)'nin hızlı okul+ekoloji testi, paralelde (a).
