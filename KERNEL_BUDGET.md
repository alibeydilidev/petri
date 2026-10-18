# KERNEL_BUDGET — Ajana Verilen Ön-Bilginin Bit Muhasebesi

> Anayasa md. 1: Ajana verilen her ön-bilgi bit cinsinden sayılır ve
> burada gerekçesiyle loglanır. Gerekçesiz hiçbir prior eklenemez.
> Hedef metrik: `çekirdek biti / final yetkinlik` oranını minimize etmek.

## Sayım kuralları
1. **Ne sayılır:** Ajanın öğrenmeden bildiği her şey — mimariye gömülü
   yapısal varsayımlar, gözlem kodlamasında dünya hakkında sızdırılan
   yapı, loss/başlatma/zamanlama yoluyla kayrılan yollar.
2. **Ne sayılmaz:** Dünyanın kendi parametreleri (grid boyutu, kaynak
   sayısı, tehlike periyodu), ajana gözlem yoluyla *öğrenilebilir* olarak
   sunulduğu sürece prior değildir — fizik hakemdir, ortamdır. Ancak bu
   parametrelerin herhangi biri ajana **açıkça kodlanırsa** (örn. gözlem
   vektörüne "toroidal=1" biti gömülürse) o anda buraya satır açılır.
3. **Bit hesabı:** Ayrık seçimler için log2(alternatif sayısı); sürekli
   hiperparametreler için makul ızgara üzerinden log2; belirsizse üst
   sınır yazılır ve gerekçelendirilir.
4. Her satır bir PR/commit'e ve gerekçeye bağlanır. Silinen prior satırı
   silinmez, "GERİ ALINDI" işaretlenir (muhasebe izi kalır).

## Defter

| ID | Sprint | Prior | Bit | Gerekçe | Durum |
|----|--------|-------|-----|---------|-------|
| K-000 | S0 | — (ajan kodu yok; hiçbir prior verilmedi) | 0 | S0 yalnız dünya fiziği + testler + replay. Ajan mevcut değil. | AÇIK DEĞİL |
| K-101 | S1 | **Gözlem kodlaması:** ajan-merkezli (2r+1)² pencere; A/B/tehlike/diğer-varlık 4 AYRI kanala önceden ayrıştırılmış; kendi bedeni gözlemde YOK; enerji ham skaler olarak gözlemde (interosepsiyon) | ~13 | Kanal ayrımı: nesne türlerini ayırt etme işi ajandan alınıyor — 4 türü tek düzlemden ayırmak yerine veriliyor ≈ log2(türlü atama alternatifleri) ~8 bit (üst sınır kabulü). Ajan-merkezlilik ~2, toroidal pencere sarması ~1, enerji normalizasyonu (1/100) ~1, enerjinin son boyut olduğu yapı ~1. İnterosepsiyon anayasa md.2 ile izinli ("homeostaz durumu içsel sinyal"). Kodlama: `world/grid.py::observe` + `training/loop.py::encode_obs` | AKTİF |
| K-102 | S1 | **Eylem uzayı:** 6 ayrık eylem var (kardinalite bilgisi). Eylemlerin ANLAMI verilmiyor — one-hot indeksin ne yaptığını model deneyimden öğrenir | ~3 | log2(6)≈2.6; MPC'nin aynı 6'lıdan örneklemesi yapısal. Semantik (hangi indeks kuzey, hangisi hasat) SIFIR bit — `agent/mpc.py` model tahminlerinden başka hiçbir eylem bilgisi kullanmaz | AKTİF |
| K-102a | S2.10 denetimi | **EFFERENCE COPY (S1'den beri verili, deftere GEÇ yazıldı — denetim bulgusu):** ajanın kendi son eylemi girdi olarak veriliyor. "Ne yaptığını bilmek" verilmiş bir öz-sinyaldir; alternatifler (eylem girdisi yok / gecikmeli / gürültülü) hiç değerlendirilmemişti | ~3 | Öz-hareket merdiveninin BASAMAK 1'i: VERİLDİ ve YETMEDİ (S2.9: efference copy eldeyken bile kayma modeli oluşmadı — ★ ara sonucu keskinleştirir: girdi eksikliği değil, temsil oluşumu engelli). Geç kayıt M-09 ihlaliydi; denetimle kapatıldı | AKTİF (denetimle) |
| K-103 | S1 | **Homeostatik hedef fonksiyonu:** MPC amaç ölçütü J = ufuk boyunca ORTALAMA tahmini kendi enerjisi; argmax'ın ilk eylemi uygulanır. (İlk sürüm ufuk-sonu değeriydi; tek-adım gürültüsüne dayanıksız çıktı, ortalamaya geçildi — revizyon da tasarım seçimidir, sayıldı) | ~6 | "Enerji iyidir" yönü + "ufuk sonu değeri" tercihi (alternatifler: min-enerji, toplam, iskonto, hayatta-kalma olasılığı… ≈ 2⁶ makul tasarım noktası içinden seçim). Ödül şekillendirme DEĞİL: J dışsal ödül değil, ajanın kendi tahmin makinesinin homeostaz değişkeni üzerindeki çıktısı (anayasa md.2'nin izin verdiği iki sinyalin bileşimi) | AKTİF |
| K-104 | S1 | **Merak terimi: YOK** | 0 | Bilinçli olarak eklenmedi. Keşif, erken dönemde kötü modelin argmax'ının rastgele adaylar üzerinde ~rastgele davranmasından geliyor. İleride eklenirse satır açılır | AKTİF (boş) |
| K-105 | S1 | **MPC hiperparametreleri:** ufuk D=5, aday C=32 (config'de). **S2.5 revizyonu (Ali talimatı):** D=10 (spec'in orijinal 8-12 bandına dönüş); C gerekirse 48 | ~4 | Planlama derinliği/genişliği örtük bir "ne kadar ileriyi düşün" prior'ı. Izgara kabulü: D∈{1..16} (4 bit üstü sınır). Davranışı şekillendirir, içerik vermez. D revizyonu bit toplamını değiştirmez (aynı ızgara içi seçim) | AKTİF |
| K-106 | S1 | **Loss ağırlığı:** enerji boyutunun tahmin loss'undaki ağırlığı λ=10 (325 boyutun 1'i) | ~3 | İnterosepsiyon yolunu KAYIRAN bir seçim — Beş Kapı/KAPI 4'ün tam arayacağı türden. Bu yüzden burada beyan: gerekçe, enerjinin 1/325 boyut olarak grid MSE'sinde boğulması; λ=10 ~ boyut oranının %3'ü. **S2 P1 yorumunda dikkate alınmak ZORUNDA** (bkz. FINDINGS S1 uyarısı) | AKTİF |
| K-107 | S1 | **TBPTT penceresi W=8 + Adam + roster lr** | ~3 | Öğrenme mekaniği hiperparametreleri; yol kayırma içermez (tüm boyutlara aynı optimizasyon). lr roster'dan (heterojenlik tasarımı, doküman 4.3) | AKTİF |
| K-108 | S1 | **ε-greedy keşif, ε=0.1 (eval'de de açık)** + rollout geri beslemesinin gözlem aralığına ([0,1]) kırpılması | ~4 | İlk koşumda 2/5 seed'de MPC argmax'ı kendi eğitim verisini yanlılaştırdı (STAY hiç denenmedi → enerji tasarrufu öğrenilemedi → rastgeleden KÖTÜ). ε içerik vermez, veri çeşitliliği verir. Kırpma: "gözlemler [0,1]'de yaşar" bilgisi ~1 bit yapısal prior | AKTİF |
| K-109 | S2.5 | **Planlayıcı aday örneklemesi (adım 4):** 6 sabit-eylem dizisi aday kümesine katılır + 1 tur elit-iyileştirme (elit 8, mutasyon 0.3) | ~4 | Teşhis-güdümlü: epizot-içi sonda, modelin STAY'i 69/69 turda doğru tercih ettiğini ama rastgele aday dizilerinde İLK-EYLEM SEYRELTMESİNİN MPC'yi ~%45 gereksiz harekete zorladığını gösterdi. Düzeltme içerik VERMEZ (6 eyleme simetrik, standart MPC/CEM pratiği); planlama mekaniğidir. Varsayılanlar eski davranışı bit-eş korur (test: `test_mpc_defaults_bitcompatible_with_pre_step4`) | AKTİF |
| K-114 | S3 | **Kanal I/O yapısı:** alınan sinyaller gözleme 16-boyut doygun-toplam one-hot (GÖNDEREN KİMLİĞİ VERİLMEZ — opaklık korunur); kendi sinyali efferens one-hot(17) olarak çekirdek girdisine (K-102a simetrisi); kendi sinyalini duymaz | ~4 | Spec 4.2'nin kodlama kararları: kimliksizlik ~1 bit (alternatif: kimlikli), doygunluk ~1, efferens ~1, kendi-sesini-duymama ~1. İçerik/anlam SIFIR — semboller anlamsız doğar, kanal yalnız boru | AKTİF (S3) |
| K-113 | S2.10 | **Eylem-koşulsuz evrişimli decoder** (yerellik + ağırlık paylaşımı; 8→16→4 kanal, 3×3). Eylem bilgisi decoder'a GİRMEZ — kayma bilgisi hidden'dan gelmek zorunda. M-19 doğum günü testi: init'te kayma oranı 0.0 → GEÇTİ (`runs/s210_m19_birthday.json`) | **içerik: 0 / yapı: ~8** | ÇİFT SÜTUN (Ali talimatı): İÇERİK biti 0 — dünya hakkında hiçbir olgu yazılmıyor (kayma yönü, kaynak semantiği vs. yok). YAPI biti ~8 — "gözlem uzamsal ve yereldir, istatistik konumlar arası paylaşılır" (mimari ızgarasında log2 üst sınır). PL-18 kararıyla izinli; varsayılan "dense" bit-eş (`test_k113_default_dense_bitcompatible`) | AKTİF (S2.10) |
| K-110rev | S2.9 | **Uzamsal PER + ε hareket yanlılığı:** örnekleme ağırlığı × (1 + 4·grid-değişim); ε ateşlenince p=0.5 ile yalnız 4 hareket eyleminden çekiliş (hareket payı ε içinde 0.67→0.83) | ~3 | PL-17 ölçülen mekanizmasına (öz-hareket geçişi kıtlığı → grid-kalıcılık modeli) veri-yönlü cevap. İçerik vermez: hangi yönün/neyin iyi olduğunu söylemez; DEĞİŞİMİN öğrenme için değerli olduğunu söyler (~2 bit) + hareket lehine hafif keşif kayması (~1 bit). Varsayılanlar kapalı, bit-eş test: `test_k110rev_defaults_bitcompatible` | AKTİF (S2.9) |
| K-111 | S2.8 | **Planlayıcı aday havuzu rev2:** CEM iter 2→4, aday 32→64, yön×süre makro önekleri (4 yöne simetrik; kuyruk rastgele — "sonra ne yapılır" bilgisi VERİLMEZ, CEM bulur) | ~3 | PL-17 nakde çevirme darboğazına: doğru yaklaşma öneklerinin rastgele havuzdaki seyrekliği ölçülmüştü (P≈%0.5). Makrolar içerik taşımaz (tüm yönlere eşit); planlama mekaniği. Varsayılan KAPALI, bit-eş korunum testli | AKTİF |
| K-112 | S2.8 | **Skorlama ufku kırpma mekanizması** (`mpc_score_horizon`; H_eff ölçümüne bağlı) | ~1 | Ön-kayıtlı kural: H_eff < 10 ise kırp. ÖLÇÜM (runs/s28_decay.json): H_eff=10 (3/3 seed) → **kırpma UYGULANMADI** (None). Mekanizma config'de hazır; satır, ölçümün yapıldığının ve sonucun kaydı. Şerh: H_eff on-policy davranış dağılımında ölçüldü; karşı-olgusal dizilerde çürüme daha hızlı olabilir | ÖLÇÜLDÜ, PASİF |
| K-110 | S2.6 | **Öncelikli deneyim tekrarı:** pencere tamponu (2000), kayıp^0.6 orantılı örnekleme, hafif eylem tabakalaması (p=0.3: rastgele eylem seç, onu içeren pencereden örnekle), tur-tekrar batch 4. IS/β ağırlığı bilinçli YOK (sapma beyanlı). Varsayılan KAPALI (bit-eş korunum) | ~5 | PL-12'ye cevap: az yapılan eylemlerin karşı-olgusal kalibrasyonunu tampon canlı tutar. İçerik vermez: hangi eylemin iyi olduğunu söylemez, hangi DENEYİMİN tekrar görüleceğini seçer. Tabakalama tek tartışmalı bileşen — "her eylem türü veri olarak eşit değerli" örtük varsayımı, ~2 bit'i bundan. Durum: KOD-HAZIR + testli; koşum dünya kalibrasyonu (PL-14) kararını bekliyor | HAZIR |

**Toplam: ~32 bit** (üst sınır kabulleriyle; yöntem: her ayrık tasarım
seçimi için log2(makul alternatif ızgarası), belirsizse yukarı yuvarla).

## S0 notu — dünya-tarafı seçimler (prior DEĞİL, ileride prior olmasın diye kayıt)
Aşağıdakiler dünyanın fiziğidir; ajan bunları gözlem yoluyla keşfetmek
zorunda kalacak. S1+'da gözlem kodlaması tasarlanırken bunların hiçbiri
ajana açıkça verilmemeli; verilecekse buraya bit satırı açılmalı:
- Grid'in toroidal olduğu bilgisi (verilirse ~1 bit + kodlama yapısı)
- Kaynak A/B ayrımının varlığı ve B'nin koordinasyon şartı
- Tehlike bölgelerinin periyodikliği (500 tur) ve süresi
- Kaynak A'nın drift periyodu (200 tur)
- Eylem uzayının anlamı (hareket yönleri / etkileşim) — S1'de eylem
  kodlaması kaçınılmaz olarak birkaç bit prior taşıyacak; o gün sayılacak.

## S2.6 notu — ekonomi v2 (dünya-tarafı, prior DEĞİL; M-09/M-10 gereği kayıt)
resource_a_energy 15→45 (economy_version=2, Ali kararı 2026-07-08).
Gerekçe: oracle fizibilitesi v1'de hasadın her koşulda net zarar olduğunu
gösterdi — bitti-tanımı matematiksel olarak sağlanamazdı. Bu bir deneyci
kararıdır ve bulguların yorumunda beyan edilir: v2 bulgular "hasadın
ekonomik olduğu dünya" koşuluna aittir. Ajan-prior'ı değildir (ajana
kod/loss/mimari yoluyla hiçbir şey gitmiyor; dünya değişti).

## S3 notu — economy v3 + açılış kararları (dünya-tarafı; M-09/M-10)
- **economy_version=3:** resource_b_energy 75→180. Gerekçe: v2'de A=45
  olunca B primi bozulmuştu (kişi başı 37.5 < A). İki-ajanlı oracle
  süpürmesi (runs/s3_b_oracle.json): sürdürülebilirlik eşiği B=135;
  anayasal 4-6× bandı korunarak 180 (=4×A) seçildi. En-sıkı-geçen (135)
  ile band çelişkisi Ali raporunda beyanlı.
- **signal_range=8** (PL-21): yayın menzili spec'te tanımsızdı; obs
  yarıçaplarının (3-6) üstünde, grid'in (64) çok altında seçildi —
  "yakın ajanlar duyar" basıncı. Config'de, tek satırla değişir.
- **5-ajan hafifletmesi:** mpc_cem_iters 4→2 (tur maliyeti; roster
  COMMON'da beyanlı). Başka hafifletme yok.
- **DP-01 fiili karar (Ali talimatı):** kurucu A2 = seed-3 transplant
  (sıfır-nötr genişletme, testli) + mutasyon σ=0.01; diğer slotlar
  mimari uyumsuzluğundan taze (KISMİ miras — dürüst kayıt). Ölümde
  halef = ölenin ağırlıkları + mutasyon (seçenek b, "çekirdek+miras").
  A/B karşılaştırması (seçenek a) yapılmadı — fiili karar, deneysel
  sonuç değil; S5'te veriyle sınanabilir.

## S3-C notu — asimetrik olay görevi (dünya-tarafı; M-09/M-10)
Ali kararı (A) uyarınca görev uzamsal olmaktan çıkarıldı (PL-25'in
ÇATAL C'si: yönsüz 4 bit "nerede" taşıyamıyor). Uygulama spec'ten
sapma değil, `event_visibility_split` + PL-05'te ertelenmiş
`world/events.py`'nin açılmasıdır. **Ajana giden bit: 0 — ve PL-27 kararından
SONRA da 0.** Ali seçenek (c)'yi seçti: öncü, AYRI KANAL AÇILMADAN
mevcut tehlike kanalına (obs kanal 2) yazılır. Yeni gözlem boyutu yok,
kategorik ayrım verilmedi, loss/mimari/başlatma değişmedi → defterde
satır açılmaz. Ajan-merkezli ÖZEL algı: (0,0)=uyarı penceresi açık,
(0,1)=bit indeksi, (1,0)=bit değeri; hangi hücrenin ne demek olduğu
SÖYLENMEZ. Öncüyü gerçek tehlikeden ayırmak da ajanın işi (öncü
yalıtık hücre + enerji çekmez; tehlike 5×5 blok + çeker).
Kayıpsızlık ve algının özel olduğu testli (`tests/test_events.py`).
**PL-28 (Ali):** `signal_range` 8 → 32 = küresel. Dünya-tarafı; ajana
bit gitmez ama deneyci kararıdır: sembolün taşıyabildiği tek şey
artık KİMLİĞİDİR (uzam/yön/mesafe/gönderen düştü).
Dünya-tarafı parametreler (`WorldConfig`): `event_every=0` (varsayılan
KAPALI, bit-eş), `event_lead=8`, `event_duration=1`, `event_penalty=25`,
`event_polarities=4`.
- **`event_duration=1` bir tasarım kilididir, keyfi değil** (M-25):
  daha uzun olay "acıyı çek sonra düzelt" kaçışına izin verir ve
  kanalı gereksiz kılar (ölçüldü: 3 turda değerin ~%67'si kurtuluyordu).
- **İpucu bölünmesi bir YORUMDUR:** kutup log2(K)=2 bitlik kod, her
  ajan olay başına 1 bit gözler. Spec metni elde olmadığı için
  (PL-26) bu somutlaştırma PL-27'de kayıtlı.
- **Oracle hediyeleri (ölçüm aleti, ajana gitmez):** `told` kolu
  sembol→bit konvansiyonunu hazır alır; tüm kollar olayın NE ZAMAN
  aktif olduğunu bilir (M-06: tek değişken HANGİ eylem). Bu kollar
  öğrenilmiş bir dilin TAVANINI ölçer, tipik başarımını değil.

## S3-D notu — PL-22 çerçevesi: klon taban + yuva dönemi (ajan-tarafı 0 bit; M-09)
Ali kararı (2026-10-18): önce (c) 5× seed-3 klon taban + (b) yuva
dönemi; seçilim (a) sonra, ayrı değişken. Deftere BİT satırı açılmaz,
ama üç deneyci kararı M-09 gereği kayda geçer:
- **Yuva dönemi (b):** `AgentConfig.nest_turns` / `nest_factor`
  (`agent/homeostasis.py`). Yaş < T iken ajanın KENDİ maliyetleri
  (metabolizma + eylem + sinyal) f ile çarpılır; dünyadan gelen delta
  (hasat/tehlike) değişmez. Gözlem, loss, mimari, başlatma değişmez →
  içerik 0 bit. Ama ekonomi kararıdır: "genç ajan ucuz yaşar" bir
  gelişim koruması emsalidir (ekolojik: yavru bakımı). Varsayılan
  T=0/f=1 bit-eş (`tests/test_pop_oracle.py::test_nest_defaults_bit_identical`).
  Analitik sınır beyanlı: f>0 iken hasatsız ajan 100/(f·1.6) tur yaşar;
  yuva sıfırdan öğrenme penceresi (~45K tur) AÇAMAZ.
- **Klon taban (c):** kurucu kadronun 5 slotu da seed-3 transplantı
  (A2 mimarisi); roster heterojenliği (doküman 4.3) ERTELENDİ (PL-20
  alternatifi fiilen seçildi). Bu, ekolojiye öğrenilmiş bir başlangıç
  noktası vermektir — ajan-içi prior değil, nüfus-tarihi kararıdır;
  bit sayılmaz, ama "sıfırdan ekoloji" iddiası artık yapılamaz (beyan).
- **Nüfus oracle'ı** (`training/pop_oracle.py`): ölçüm aleti, ajan
  değil; klon kolları gerçek seed-3 ağırlıklarını ÖLÇÜM NESNESİ olarak
  koşar (hediye yok). `MutePlanner` eylem-only planlama yalnız oracle
  içindir (kanal farkını izole eder, M-06). Ölü beden hayalet olarak
  görünür (halefsiz oracle sınırı, b_oracle emsali).

## S3-E…K notu — gece koşumları (ajan-tarafı 0 bit; M-09 deneyci kararları, 2026-10-18/19)
Ali yetki devriyle Claude'un verdiği kararlar; hiçbiri ajana bit yazmaz,
hepsi dünya/nüfus parametresidir ve FINDINGS ön-kayıtlarında beyanlıdır:
- **σ=0.002** halef mutasyonu (PL-31; DP-01b dozu). Drift öğrenmeyi
  siliyordu (M-26). "Ölüm gerçek" bedene/yaşantıya, yapıya değil.
- **Yuva (600, 0.5)** her nesilde (PL-29 riski kayıtlı).
- **Olay zamanlaması** `event_every` 30→10, `event_lead` 8→4/2, ceza
  25/10/8: dünya-tarafı kalibrasyon, ajana söylenmez.
- **Seçilim `max_age`** (S3-H): nüfus kuralı; 20K'da etkisiz.
- **Olay okulu** (S3-J): tek-ajan tavan ölçümü, yetiştirme kabı rejimi
  (PL-06 emsali); ekoloji iddiası değil.
- **K-106 revizyonu (λ 10→30) DENENDİ ve GERİ ÇEKİLDİ** (okulda fark
  yok) → defter değişmedi.
- **Anayasal basamak (PL-27 a: ayrı öncü kanalı) ATILMADI**: okul,
  mevcut kodlamanın öğrenilebilir olduğunu gösterdi.
Gözlemci enstrümanları (`analyze_s3e.py`, `precursor_probe.py`,
`event_school.py`) ajana gitmez.
- **S3-N `event_share=0.5` (PL-33):** olay kaybının yarısı nüfusça
  paylaşılır (fizik; sürü savunması). Ajana bit yazmaz; gözlem/loss/
  mimari değişmez. Ama görev semantiğini değiştiren deneyci kararıdır
  (M-09): "alarm çağrısı" → "sürü alarmı". Varsayılan 0 bit-eş
  (`tests/test_events.py::test_event_share_default_bit_identical_and_math`).
- **S3-O `mpc_signal_candidate_frac` (PL-32):** ortak planlamada sinyal
  taşıyabilen rastgele aday satırı payı (1.0 bit-eş → 0.25/0.05).
  İçerik vermez; arama bütçesinin eylem/sinyal paylaşımı (K-109/K-111
  soyu). Üst sınır ~1 bit (ızgara {1, .25, .05}); kalıcı olursa K-115
  satırı açılır. Test: `test_s3o_signal_frac_default_bit_identical_and_quieter`.
  **Sonuç (S3-O): kalıcı yapılmadı** (prim baskın); varsayılan 1.0 kaldı.
- **S3-P `eps_signal_quiet_prob` (K-108 revizyon adayı):** ε dalında
  sinyal/sessizlik dengesi (karşı-olgusal susma verisi, M-05). İçerik
  vermez; üst sınır ~1 bit. **Sonuç: kalıcı yapılmadı** (primi yarıladı,
  silmedi); varsayılan 0 (bit-eş) kaldı.
  Test: `test_s3p_eps_quiet_default_bit_identical`.
- **Nihai (19 Ekim öğle):** S3-D…P boyunca deftere KALICI bit satırı
  açılmadı. Açık olan tek kalıcı dünya değişikliği `event_share=0.5`
  (fizik; görev adı "sürü alarmı").

## S3-B notu — koordinasyon oracle'ı (ajan-tarafı 0 bit; M-09 gereği kayıt)
`training/b_oracle.py` ajana HİÇBİR ŞEY vermez (ajan kodu değil, ölçüm
aletidir — `training/oracle.py` emsali) → deftere bit satırı açılmaz.
Ancak M-09 gereği DENEYCİ KARARLARI kayda geçer:
- **SYM_B konvansiyonu HEDİYE:** `signal`/`beacon` seviyeleri hangi
  sembolün "burada B var" demek olduğunu hazır alır. Bu tam olarak
  ajanın keşfetmesi gereken şeydir (H3/H4). Bilinçli: bu kollar
  **mükemmel paylaşılan konvansiyon altındaki TAVANI** ölçer. Bulgu
  (kanal yardım etmiyor, zarar veriyor) bu tavan altında okunmalıdır —
  yani öğrenilmiş bir dil için ÜST SINIR sonucudur.
- **Tanrı-gözü kapsamı:** `god` kolu B ve A konumlarını + diğer
  ajanların konumlarını bilir (randevu minimax). Salt tavan ölçümü.
- **Politika repertuvarı** (greedy-görüş, yayın, çapalı fener, görsel
  takip) tüketici değildir; sınır FINDINGS S3-B "Sınırlar"da beyanlı.
- **Tarama fazı kaydırması:** iki koordinatör aynı lawnmower fazında
  bağıl hızsız kalıp hiç karşılaşmıyordu (enstrüman kusuru); faz
  ajan indeksine göre kaydırıldı ve tüm merdiven yeniden koşuldu.

## S2.7 notu — curriculum_v2: yuva müfredatı (dünya-tarafı; M-09 gereği kayıt)
Eğitim epizotlarının p_nest olasılıkla ajanın doğum yeri rastgele bir
A-kaynağının Chebyshev ≤2 komşuluğuna alınır; tavlama 0.7→0.3→0.1
(15K'lık üç faz). Eval HER ZAMAN standart spawn/müfredatsız. Ajana bit
gitmiyor (loss/mimari/gözlem değişmedi; dünyadaki doğum dağılımı
değişti) ama bu bir deneyci kararıdır: PL-16 keşif tuzağına ekolojik
iskele. Ayrıca S2.7 calibN teşhisinde SENTETİK hasat penceresi PER
tamponuna enjekte edildi — YALNIZ teşhis koşumlarında; yuva/ana ajanda
sentetik veri yok (beyan). Parametreler run meta'sında (`curriculum_v2`).

## S2 notu — müfredat (dünya-tarafı, prior DEĞİL)
S2 veri üretiminde A-kaynağı yoğunluğu müfredatı (48→24→12) kullanıldı
(PL-10). Bu, ajanın İÇİNE giden bilgi değil, ortamın zamanlamasıdır:
loss'a, mimariye, başlatmaya, gözlem kodlamasına dokunmaz. Bit
sayılmadı. Ancak beyan: müfredat, hangi deneyimin veriye gireceğini
şekillendirir — S2+ bulguları "müfredatlı eğitim" koşulu altında okunmalı.
