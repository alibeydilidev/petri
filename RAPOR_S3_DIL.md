# PETRI S3 dil kolu: bütüncül kapanış raporu

**Hüküm: H4 negatif.** Bu anayasa altında, 5 ölümlü öngörücü ajanlık bir
ekolojide, 4 bitlik maliyetli ve kimliksiz bir kanaldan anlam taşıyan bir
iletişim kendiliğinden doğmadı. Yaklaşık 320 koşum, 600 bin tura kadar
süren ekolojiler ve ajana kalıcı olarak verilen 0 yeni bit ile.

Kapanış: 2026-10-21 (Ali kararı, PL-40 (a)). Kaynak tablolar ve
ön-kayıtlar: [`FINDINGS.md`](FINDINGS.md). Dersler:
[`METODOLOJI.md`](METODOLOJI.md). Bit defteri:
[`KERNEL_BUDGET.md`](KERNEL_BUDGET.md).

---

## 1. Özet

Bilincin öncüllerinden biri olan birleşimsel iletişimin (H4) hangi basınç
altında kendiliğinden belirdiğini yakalamak için bir "alarm çağrısı"
tuzağı kurduk. Küresel bir tehlike gelmeden önce her ajan güvenli
kutbun 2 bitlik kodundan yalnız 1 bitini görür. Bilgi tek bir ajanda
tamamlanmaz; kanal onu tamamlamanın tek yoludur. Bir fizibilite hesabı
(oracle) görevin geçerli bir tuzak olduğunu doğruladı: mükemmel bir
konvansiyon olsaydı kanal olay değerinin %71'ini kurtarırdı.

Öğrenen ajanlarla bu tuzakta dil doğmadı. Bunu ilk gün söyleyebilirdik.
Asıl iş, olumsuzluğun **neden** olduğunu kanıtlamaktı. Sırayla şu
açıklamaları eledik:

1. Ajanlar öğrenemiyor mu? Hayır. Tek ajan da nüfus da kendi ipucunu
   öğreniyor ve kendi-ipucu tavanına ulaşıyor.
2. Kanal kullanılamayacak kadar mı pahalı ya da gürültülü? Hayır.
   Mekanik engeller (miras gürültüsü, tampon sıfırlamasından doğan sahte
   prim, açılış şoku) bulunup kaldırıldı. Kanal nötr ve doğru fiyatlı
   hâle geldi.
3. Kanalda alıcıya ulaşabilecek bilgi yok mu? Var. Optimal bir alıcı,
   ekolojideki gerçek göndericilerden bile kendi-ipucu tavanını aşabilirdi.
4. Ajan başkasını dinlemeyi öğrenebilir mi? Evet. Okulda, net konuşan
   komşularla bir ajan dinlemeyi öğrendi ve tavanı ilk kez aştı.

Geriye kalan açıklama sayısal bir tavuk-yumurta: dinleyici öğrenmesi
için göndericinin yaklaşık **0.18 bit** net olması gerekiyor. Ekoloji
göndericileri **0.05 ile 0.10 bit** arasında kilitli kalıyor. Dinleyen
olmadığı için netleşmenin göndericiye faydası yok. Bu "sessiz denge"
uzun zaman (500 bin tur), grup seçilimi, uyarı süresi kalibrasyonu ve
dışarıdan eğitilmiş dinleyicilerle tohumlama karşısında kararlı kaldı.

## 2. Soru ve tuzak

**Hipotez H4:** Asimetrik bilgi ve kanal kıtlığı, proto-gramer doğurur.
Daha alçakgönüllü ön koşulu: sembol ile dünya arasında, alıcının
eyleminde kullanılan bir olumsallık kurulur.

**Anayasa (değişmedi):** Ödül şekillendirme yok; tek içsel sinyal tahmin
hatası ve homeostaz. Dil, konvansiyon ve duygu verilmez. Kanalın yalnız
genişliği (16 sembol) ve enerji maliyeti tanımlı. Ajana giren her ön
bilgi bit cinsinden deftere yazılır.

**Tuzak (S3-C, alarm çağrısı):** 64×64 torus dünya, 5 ajan. Her 10 turda
bir küresel olay gelir. Güvenli tek eylem K=4 kutuptan biridir. Olaydan
birkaç tur önce her ajan, özel algısında kutup kodunun rastgele bir
bitini görür. Kanal küreseldir ve gönderen kimliği taşımaz. Ölüm
gerçektir. Halefler ölen ajanın ağırlıklarını küçük bir mutasyonla
devralır.

**Tuzağın fizibilitesi (koşumdan önce):** değer oranı 1.96, kanal
gereklilik 0.241, kanal yeterlilik 0.709. Üç ön-kayıtlı çıta da geçti.

## 3. Yöntem disiplini

- **Ön-kayıt (M-08):** her koşumdan önce soru, çıta ve öngörü
  `FINDINGS.md`'ye yazılıp commit edildi. Git commit zamanı yetkili zaman
  damgasıdır. 18-20 Ekim kayıtlarındaki bir günlük tarih kayması git'e
  göre düzeltildi. Ön-kayıt sırası tek bir istisna dışında git ile
  kanıtlanıyor: CH0 kanal hesabı sonucuyla aynı commit'te. CH0 öğrenme
  içermeyen bir Monte Carlo hesabı olduğu için "açıklayıcı hesap" olarak
  etiketlendi.
- **Önce oracle (M-21, M-22, M-27):** ekolojiyi yargılamadan önce aynı
  görevin tek ajan tavanı ve optimal alıcı tavanı ölçüldü.
- **Öngörü karneleri:** her bulgu bölümünde tutan ve tutmayan tahminler
  birlikte durur.
- **Beş Kapı:** hiçbir pozitif gözlem kapılardan geçmedi. Aşağıdaki
  pozitifler "aday gözlem" ya da "mekanizma" etiketlidir.
- **Bit defteri:** iki aday satır açıldı ve ikisi de geri alındı (K-115
  model topluluğu, K-116 kültürel tohum). Dil kolunun kalıcı bit maliyeti
  sıfırdır.

## 4. Yolculuk

| Aşama | Soru | Sonuç |
|---|---|---|
| S3-D | Nüfus yaşayabilir mi? | Klon kadro ve yuva dönemi ömrü uzattı. Eğitimsiz kanal klonu boğuyor. |
| S3-E…K | Öğrenen ekolojide dil doğar mı? | Mutasyon gürültüsü düşünce (σ=0.002) ekoloji kararlı. Ajanlar ipucunu öğreniyor. Kanal 0 bilgi taşıyor ve öğrenmeyi yavaşlatıyor. |
| S3-L…P | Kanal neden yavaşlatıyor? | Yavaşlatan taraf gönderme. Planlayıcı kendi sinyaline sahte bir enerji primi öğreniyor. Paylaşılan kayıp eklemek yetmedi. |
| Program B | Önce yetkinlik, sonra kanal? | Yetkin ajan sinyali fiyatlamayı öğrendi. Açılış şoku isabeti düşürdü, 600 bin turda dil yok. |
| Program A | Sahte primin kaynağı ne? | Halefte deneyim tamponunun sıfırlanması. Tampon mirasıyla prim silindi, kanal nötr oldu. Model topluluğu işe yaramadı (K-115 geri). |
| Program C | Göndericiye doğrudan fayda verirsek? | "Birlikte açılan sığınak": 3 kişilik sığınak bireysel öğrenmeyi bozdu, 2 kişilik sığınak basınç üretmedi. Kanal nötr, fiyatlı, kullanılmıyor. |
| Program A′/A″ | Grup seçilimi kırar mı? | Ada modeli (açık kanalda 6, kontrolde 3 ada; ada başına 360 bin tur) sembol anlamı doğurmadı. Ajanlar ipucuna bağlı bir konuşma kararı geliştirdi (0.10 bit). Bunun yaklaşık %75'i reflekse benziyor. Dinleyen yok. |
| PL-37 | Kanal tavan mı? Dinleyici öğrenebilir mi? | Kanal tavan değil. Okulda ajan dinlemeyi öğrendi (isabet 0.42'den 0.62'ye). Dinleyici öğrenmesi için gönderici netliği eşiği yaklaşık 0.18 bit. |
| PL-38 | Zaman ya da uyarı süresi göndericiyi eşiğe taşır mı? | Hayır. 500 bin turda ve 6 ile 8 turluk uyarıda gönderici netliği 0.05 ile 0.10 bit arasında kaldı. |
| PL-39 | Dinleme bir kez kurulursa yaşar mı? | Hayır. Okulda dinlemeyi öğrenmiş kurucular yaklaşık 20 bin turda kendi ipuçlarına döndü. Göndericisiz dinleme yaşamıyor. |

## 5. Mekanizma: dil neden doğmadı

**Engel 1, mekanik gürültü (kaldırıldı).** Yüksek mutasyon miras alınan
öğrenmeyi siliyordu (M-26). Halef her doğumda deneyim tamponunu
sıfırlayınca planlayıcı nadir eylemlere, özellikle kendi sinyaline,
sahte bir prim öğreniyordu (M-31). Kanalın açılması yetkin ajanı bir
süre sarsıyordu (M-29). Üçü de bulundu ve kaldırıldı. Sonrasında kanal
açık ve kapalı kollar aynı isabete ulaştı.

**Engel 2, giriş ücreti (yapısal).** Sinyalin göndericiye faydası
dolaylıdır. Gönderici ancak alıcı onu kullanırsa kazanır. İlk konuşan,
alıcı öğrenene kadar bedel öder. Öğrenen bireysel bir sistemde bu
yatırımı yapan seçilmez (M-28).

**Engel 3, sayısal eşik (ölçüldü).** Okulda bir doz-cevap eğrisi çıkardık:

| Gönderici netliği (bit) | Öğrenen dinleyicinin isabeti |
|---|---|
| 0.08 (ekolojide gözlenen) | 0.43 (tavan altında) |
| 0.18 | 0.47 ile 0.50 (eşik) |
| 0.25 | 0.53 |
| 0.45 | 0.59 ile 0.60 |
| 0.83 (mükemmel) | 0.62 |

Kendi-ipucu tavanı yaklaşık 0.42 ile 0.47. Ekoloji göndericileri
eşiğin yarısında.

**Engel 4, sessiz denge (kararlı).** Gönderici netliği eşiğe tırmanmıyor.
Zaman, grup seçilimi ve uyarı kalibrasyonu onu kıpırdatmadı. Diğer
uçtan girmeyi de denedik: dinlemeyi bilen ajanlarla kurulan ekoloji,
gürültülü gerçek göndericilerle karşılaşınca dinlemeyi bıraktı. Bu
ölçekte "konuşan ve dinleyen" bir denge kurulamadı. Dolayısıyla onun
kararlı olup olmadığını da bilmiyoruz.

**Tek cümlede:** dinleyici olmadan gönderici netleşmiyor, net gönderici
olmadan dinleyici öğrenmiyor. Aradaki bariyer bu sistemde kendiliğinden
aşılmadı.

## 6. Hipotez hükümleri

| H | Hüküm | Dayanak |
|---|---|---|
| H1 öz-model | Karışık, çoğunlukla negatif | Kümülatif yol entegrasyonu yok. Tek-adım öz-hareket yerellik iskelesiyle öğreniliyor. Öz-enerji adayı düştü (S2). |
| H2 karşılıklı modelleme | Test edilmedi | Ön koşul olan iletişim doğmadı. |
| H3 içselleştirme | Ön koşul negatif | İçselleştirilecek bir sinyal kullanımı yok. |
| **H4 proto-gramer** | **Negatif (bu anayasa altında)** | Bu rapor. |
| H0 reaktif hesap | Çürütülmedi | Hiçbir pozitif bulgu Beş Kapı'dan geçmedi. |

## 7. Pozitif aday gözlemler (iddia değil)

- **Öncü algısı:** iç model tehlike öncüsünü görüyor (30/30 çekirdek).
- **Kendi-ipucu öğrenimi:** tek ajanda 6/6, ekolojide 3/3.
- **Kanal fiyatlaması:** yetkin ajan sinyalin maliyetini doğru öğrenebiliyor.
- **İpucuna bağlı konuşma kararı:** ajanlar bitleri 1 iken daha sık
  konuşuyor (0.10 bit). Ablasyonda büyük kısmı refleks.
- **Dinleyici öğrenmesi ve eşiği:** okulda net komşularla dinleme
  öğreniliyor, doz-cevap eğrisi temiz. Bu, PETRI'de bir ajanın başka
  ajanların sinyalinden bilgi çıkarıp eyleme çevirdiği ilk ölçüm. Sanal
  komşular dünya tarafında bir ölçüm aleti olduğu için "dil" iddiası
  değildir.

## 8. Sınırlar: bu sonuç neyi söylemez

- **Ölçek:** 5 ajan, 4 bitlik kanal, tek bir mimari (GRU öngörücü ve
  model tabanlı planlayıcı). Daha büyük nüfuslar, daha uzun evrim ya da
  farklı öğreniciler denenmedi.
- **Kanal tasarımı:** kanal küreseldi ve gönderen kimliği taşımıyordu.
  Akrabalık, tekrarlanan eşler ya da yerel kanal yoktu. Doğadaki alarm
  çağrılarının bilinen dayanakları tam bunlardır.
- **İki taraflı tohum denenmedi:** dinleyici ve net gönderici birlikte
  verilseydi kurulmuş bir iletişimin yaşayıp yaşamadığı ölçülebilirdi.
  Bu, gönderici kuralını hediye etmek demek ve yaklaşık 2 bit maliyetli.
  Kapanış kararıyla açık bırakıldı.
- **"Dil imkânsızdır" denmiyor.** Söylenen şu: bu anayasa ve bu ölçekte
  sıfır bitten kendiliğinden dil doğmadı, ve bunun nedeni ölçülmüş bir
  tavuk-yumurta bariyeridir.

## 9. Açık kalan yollar (davet)

Bu repoyu alıp devam etmek isteyen biri için en umutlu yönler, tahmini
bit maliyetiyle:

| Yol | Fikir | Maliyet |
|---|---|---|
| İki taraflı tohum | Dinleyici ve net gönderici birlikte; iletişim tohumdan sonra yaşar mı? | ~2 bit, köken değil kararlılık sorusu |
| Kimlikli ya da yerel kanal | Alıcı kimin konuştuğunu bilirse "hangi bit" sorunu çözülür. | Anayasal karar (PL-28'in tersi) |
| Akrabalık ya da tekrarlanan eşler | Göndericinin faydası soy üzerinden döner. | Fizik değişikliği, ~0 bit |
| Daha büyük ve uzun evrim | Daha çok ada, milyonlarca tur | 0 bit, hesaplama maliyeti |
| Farklı öğrenici | Model-free ya da keşif terimli ajan | Mimari değişiklik, defterde |

## 10. Tekrar üretim

Tüm koşumlar deterministiktir: dünya seed'i ve ajan seed'i aynıysa sonuç
bit-eştir. Her tablo `runs/` altındaki `breath.json` ve `school.json`
dosyalarından türetilir.

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/python -m training.ecology --turns 200000 --founding school:runs/rs/rs1_s0/final_weights.pt,runs/rs/rs1_s1/final_weights.pt --nest 600 0.5 --sigma 0.002 --events --event-every 10 --event-lead 4 --event-penalty 25 --event-share 0 --min-safe 2 --channel open --world-seed 3001 --out runs/tekrar
.venv/bin/python -m training.sender_clarity runs/tekrar
```

| Program | Klasör |
|---|---|
| S3 merdiveni | `runs/s3e` … `runs/s3r` |
| Program A, A″ | `runs/a0` … `runs/a3` |
| Program C | `runs/c1` … `runs/c4` |
| Program A′ | `runs/ev` |
| PL-37 okul ve doz | `runs/rs`, `runs/ch0_channel_oracle.json` |
| PL-38 | `runs/pl38` |
| PL-39 | `runs/pl39` |

## 11. Beyan

Hipotezler, anayasa ve mimari plan Ali Beydili'ye aittir. Kodun büyük
bölümü, koşumlar, ön-kayıtlar, analizler ve bu rapor, Ali'nin verdiği
karar yetkisiyle Claude (Anthropic) tarafından yürütüldü ve yazıldı.
Ali karar noktalarında yön verdi (`OPEN_LOOPS.md` "KARAR" satırları).
Hiçbir dil modeli deneyin içinde yer almadı. Claude yalnızca deneyci
ve gözlemci rolündeydi.
