# K-104 DOSYASI — ARŞİV (veriyle reddedildi, 2026-07-08)

> **ŞERH (S2.8 talimatı):** Bu dosya "veriyle reddedildi" olarak
> arşivlenmiştir: teşhis, merakın çözeceği katmanın (deneyim üretimi)
> çözülmüş, darboğazın planlayıcı nakde çevirmesi (PL-17) olduğunu
> gösterdi. **Yeniden açılma koşulu (S2.8 çatal-5, ön-kayıtlı):**
> nakit testi (mesafe≤2'de ≥%70) GEÇER ve standart eval hasadı yine 0
> kalırsa → kalan boşluk keşif/arama davranışıdır (görünür kaynak
> yokken ne yapmalı) ve bu dosya O veriyle yeniden açılır — merak
> lehine ilk gerçek kanıt o olur.

# (orijinal metin aşağıda korunmuştur)
# K-104 DOSYASI — Merak Terimi Kararı (Ali'ye)

> S2.7 Çatal B gereği açıldı (2026-07-08). Soru: MPC hedefine merak
> (tahmin-hatası arayışı) terimi eklensin mi? KERNEL_BUDGET K-104 şu an
> bilinçli boş. Karar Ali'nin; bu dosya veriyi ve seçenekleri toplar.

## Kanıt zinciri (kronolojik)
1. **PL-16 (S2.6):** müfredatsız eğitimde 45K turda 10 hasat olayı —
   deneyim üretimi darboğazı.
2. **calibN (S2.7, düzeltilmiş cihaz):** N* = 50 — model, PER
   tamponunda canlı tutulan 50 deneyimden olumsallığı öğreniyor
   (bağlam-içi tahmini sıçrama gerçeğin %62-84'ü). Öğrenme UCUZ.
3. **Yuva müfredatı (S2.7):** deneyim 10 → 25-57/seed (~4-6×). Seed 1
   ve 3: deneyim ≥ N* VE kalibrasyon ≥ eşik — İKİ kriter de sağlandı.
4. **AMA eval hasadı 5/5 seed'de 0.0.** Ve bağımsız davranışsal test
   (calibN N=2000 ajanı, kalibrasyon 0.36): kaynak 2 hücre yandayken
   10 denemede 2 hasat. **Bilgi var; nakde çevirme yok.**

## Teşhis ayrışması — merak neyi çözer, neyi çözmez
Başarısızlık iki alt-probleme ayrışıyor:
- **(i) Deneyim üretimi** (B1): merak terimi BUNU hedefler (yeniliğe
  yönelim → kaynak karşılaşması artar). Ama yuva müfredatı bunu zaten
  kısmen çözdü ve calibN gösterdi ki 50 deneyim yetiyor — yani (i)
  artık birincil darboğaz DEĞİL.
- **(ii) Nakde çevirme** (B2): kalibre model + MPC, gördüğü kaynağa
  gidip hasat planını seçemiyor. Muhtemel mekanizma: rollout'ta
  egosantrik grid-kayma halüsinasyonunun bileşik hatası (yaklaşma
  adımları boyunca kaynağın tahmini konumu bozuluyor) + aday
  dizilerinde doğru öneklerin seyrekliği (2 hücre için P(önek)≈%0.5).
  **Merak terimi (ii)'yi ÇÖZMEZ** — keşfi artırır, planın icrasını değil.

## Seçenekler
| # | Müdahale | Hedeflediği | Kernel maliyeti | Not |
|---|----------|-------------|-----------------|-----|
| A | Merak: J = ort-enerji + β·tahmin-hatası | (i) | ~6 bit + β | Anayasa md.2 harfiyle savunulabilir ("içsel sinyal: tahmin hatası"); ama (i) çözüldü sayılır → beklenen etki DÜŞÜK |
| B | Planlayıcı iyileştirme: CEM iter 2→4, mutasyon ayarı, aday-önek uzatma | (ii) | ~2 bit (K-109 revizyonu) | Ölçülen darboğazı hedefler; içerik vermez; EN UCUZ |
| C | Rollout yerine gerçek-dünya-modeli değerlendirmesi vb. mimari değişiklik | (ii) | büyük | S1 mimari kararlarını yeniden açar — önerilmez |
| D | Hiçbiri; bu haliyle S3 | — | 0 | B-kaynağı koordinasyon basıncı, tekil hasat bile çözülmemişken büyük risk |

## Tavsiyem
Önce **B** (bir koşum, ~25 dk): darboğaz ölçülü olarak planlayıcıda;
merak, teşhisin işaret etmediği probleme çare. B başarısız olursa A'yı
B2-kanıtı zayıflamış olarak yeniden değerlendiririz (o zaman (i)+(ii)
etkileşimi tartışılır). Karar senin.

## Ham veri
`runs/s27_calibN.json`, `runs/s27_nest_results.json`,
`runs/s27_visibleA_oracle.json`; teşhis çıktıları FINDINGS S2.7.
