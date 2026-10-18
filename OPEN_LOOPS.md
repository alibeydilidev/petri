# OPEN_LOOPS — Açık İşler ve Karar Noktaları

## Karar noktaları (kaynak dokümandan)

- **DP-01 — Süreklilik sorusu (AÇIK, S5'te karar):** Ölen ajanın yerine
  gelen yeni ajan (a) sıfırdan mı başlar, (b) ölenin ağırlıklarından
  mutasyonlu tortu mu devralır? Öneri: S5'e kadar (a); sonra A/B testi.
- **DP-02 — Kanal genişliği ablasyonu (AÇIK):** 4 bit anayasal; 2/4/8 bit
  ablasyonu H4 kontrol deneyi olarak S4 sonunda düşünülebilir.
- **DP-03 — Nüfus ölçeği (AÇIK):** B-kaynağı açılma oranı 100K turda < %5
  kalırsa 5 → 7 ajan.

## PL — açık işler / bekleyen onaylar

- **PL-01 — Tehlike geometrisi ve ömrü (S0 varsayımı, Ali onayı bekliyor):**
  Kaynak doküman tehlike bölgesinin şeklini ve süresini tanımlamıyor.
  S0'da varsayılan: kare bölge, Chebyshev yarıçapı 2 (5×5 hücre), ömür 250
  tur (`hazard_radius`, `hazard_duration` — `world/config.py`). Config
  parametresi olarak açık; değiştirmek testleri bozmaz.
- **PL-02 — Hasat semantiği (S0 varsayımı, Ali onayı bekliyor):**
  (a) Toplanan A kaynağı anında rastgele yeni hücreye taşınır (sayı sabit 12
  kalır — "azdır, yer değiştirir" ile uyumlu en basit yorum).
  (b) B açıldığında 75 enerji, senkron penceredeki katılımcılara **eşit
  bölünür** (2 katılımcı × 37.5 = kişi başı 2.5×A, toplam 5×A — dokümandaki
  "4–6× verimli" aralığında) ve B yeni hücreye taşınır.
  Alternatif yorum (herkese tam 75) isteniyorsa tek satır değişiklik.
- **PL-03 — Viewer arka ucu:** Ortamda matplotlib/pygame yok. Replay viewer
  sıfır bağımlılıkla ANSI/terminal tabanlı yazıldı; matplotlib kuruluysa
  `--backend mpl` ile kullanılabilir (opsiyonel). Zengin görselleştirme
  istenirse bağımlılık kurulumu Ali kararı.
- **PL-04 — Python sürümü:** Doküman 3.12 diyor, makinede 3.13.2 var.
  S0 kodu her ikisiyle uyumlu; sabitlemek gerekirse Ali kararı.
- **PL-06 — S1 "yetiştirme kabı" modu (Ali onayı bekliyor):** DP-01/"ölüm
  gerçek" kuralı S1 eğitiminde askıya alındı: ağırlıklar epizotlar arası
  taşınır. Gerekçe: S1 makine dairesi testidir (çekirdek+homeostaz+MPC
  çalışıyor mu); tek yaşam içi öğrenmeyle rastgeleyi geçmek ayrı ve daha
  sert bir iddia. Ekoloji deneyi (S3+) "ölüm gerçek" ile koşacak.
  Alternatif istenirse: eval'i "tek yaşam içi öğrenme" varyantıyla tekrar.
- **PL-07 — INTERACT enerji maliyeti (varsayım):** Dokümanda tanımsız;
  hareketle eş (1.0) alındı (`interact_energy_cost`). Bedava olursa ajan
  her tur bedavaya "hasat yoklaması" yapabilir; maliyet koordinasyon
  basıncını koruyor.
- **PL-08 — Sinyal girdisi S3'te eklenecek:** predictive_core girdisi şu an
  gözlem+eylem. S3'te kanal açılınca girdi boyutu değişecek → S3 ajanları
  taze başlar (DP-01a ile tutarlı); S1 ağırlıkları S3'e taşınmaz.
- **PL-09 — P1 λ=10 konfound'u (KAPALI, S2.6):** λ=1 ablasyonu koşuldu:
  öz-enerji ΔR² değişmedi (0.028 → 0.026, 5/5 seed anlamlı kaldı).
  Minik avantaj loss kayırmasından gelmiyor. Kalan itiraz PL-15'te.
- **PL-15 — Öz-enerji kontrolleri (KISMEN KAPALI, S2.6):** Enerji-körü
  eş-eğitimli kontrol KOŞULDU ve keskin çıktı: girdisiz temsil yok
  (kör kol R²≈0, 5/5), zaman-korelat alternatifi çürüdü, etki
  interosepsiyon yoluna özgü. KALAN tek itiraz ("eğitilmiş GRU tüm
  girdilerini genel olarak daha iyi temsil eder") hareketsiz rejimde
  TEST EDİLEMEZ (varyans-eşleşmiş kontrol özelliği yok — M-03).
  Terfi kapısı PL-16 mobiliteye kilitli. Etiket: ADAY GÖZLEM.
- **PL-10 — A-hasadı S1'de çıkmadı → S2'de müfredatla ele alındı (KISMEN
  KAPALI):** Ali'nin S2 talimatıyla kaynak-yoğunluğu müfredatı uygulandı:
  eğitimde A-kaynağı 48 → 24 → 12 (15'er bin tur) aşamalı kıtlaştırma;
  DEĞERLENDİRME her zaman standart kıtlıkta (12). Müfredat ekolojik
  iskeledir, ajan prior'ı değildir (loss/mimari/başlatmaya dokunmaz);
  KERNEL_BUDGET'a bit yazılmadı, dünya-tarafı not düşüldü.
  **S2 sonucu: müfredat hasadı ÜRETEMEDİ** → S2.5'te dört müdahaleli
  merdiven denendi (ufuk, metabolizma, müfredat, planlayıcı örneklemesi)
  — HİÇBİRİ hasat üretmedi. Kök neden PL-12'ye taşındı; PL-10 artık
  PL-12'nin türevi.
- **PL-12 — Kapalı-döngü karşı-olgusal kalibrasyon kararsızlığı (S2.5 kök
  bulgusu, S3 tasarım girdisi):** On-policy self-supervised world-model +
  MPC, az yapılan eylemlerin sonuç modelini kalibre edemiyor; davranış
  hangi kutba yakınsarsa model o kutbun dışında bozuluyor (S1-v1 ve
  S2.5-adım-4 aynı kararsızlığın iki yüzü). Çözüm adayları (hepsi
  KERNEL_BUDGET'a bit yazdırır, karar Ali'de): (a) ε'u artırmak (0.1→0.25) —
  en ucuz, en az prior; (b) eylem-dengeli replay tamponu (öğrenme mekaniği,
  içerik vermez); (c) model topluluğu/belirsizlik cezası; (d) hiçbir şey
  yapmayıp S3'e geçmek — nüfus dinamiği dünyayı ajan-dışı perturbe ederek
  doğal karşı-olgusal veri üretebilir (en "ekolojik" çözüm, deneyin ruhuna
  en uygun). Not: B-kaynağı koordinasyonu (S3'ün kalbi) hasat planlaması
  gerektirir — PL-12 çözülmeden S3'ün sinyal basıncı hiç doğmayabilir.
- **PL-14 — DÜNYA EKONOMİSİ KALİBRASYONU (KAPALI, 2026-07-08 Ali kararı):**
  economy_version=2: resource_a_energy 15→45 (`world/config.py`, M-10
  damgalı; v1 tanımı `economy_v1()` olarak korundu — eski kayıtların
  replay'i v1 ile). Stage-2 koşulu: m=0.6, 24 kaynak, oracle medyanı 8.5.
  Orijinal analiz aşağıda: Oracle fizibilite ızgarası +
  A-enerji süpürmesi (`runs/s26_oracle.json`, `runs/s26_a_energy_sweep.json`)
  gösterdi ki mevcut anayasal değerlerle (A=15 enerji) HASAT HER KOŞULDA
  NET ZARAR: yetkin scripted hasatçı bile tüm ızgarada saf-tasarruftan
  kısa yaşıyor. "Medyan hasat ≥3" + "stay'den uzun yaşam" birlikte
  sağlanamaz → S2.5'in başarısızlığının bir katmanı da buymuş (öğrenme
  sorunlarının üstünde). Oracle-doğrulanmış geçerli koşullar (hepsi
  A-enerjisi artışı istiyor): m=1.0/24kaynak/A=45 (ince marj: 108 vs 100),
  m=0.6/24/A=45 (sağlam: 197 vs 167, hasat 8.5), m=0.3/24/A=60
  (bol: 534 vs 334, hasat 22.5). Önerim: m=0.6/24/A=45 — basınç sürer,
  marj istatistiksel güce yeter. Not: A-enerjisi anayasal spec'te 15;
  değişiklik Ali onayı gerektirir, KERNEL_BUDGET'a değil (dünya-tarafı)
  WorldConfig + bu satıra işlenir.
- **PL-13 — Ali'nin öngörüsü (KISMEN SONUÇLANDI, S2.10-ek, n=1):**
  Üretici katmanda DESTEKLENDİ (kayma yetisi ↑ → hasat doğdu, sıralama
  net); korelasyonel katmanda DESTEKLENMEDİ (disp probu yükselmedi).
  Tek-adım öz-hareket ≠ kümülatif yol entegrasyonu ayrımı kayda geçti.
  Çoğaltma (≥5 seed) açık iş; azami etiket ADAY GÖZLEM (ön-kayıt).
- **PL-15 — (KAPALI, S2.10-ek): itiraz AYAKTA, öz-enerji adayı DÜŞTÜ.**
  Varyans-eşleşmiş kontrol (görünür-A) mobil ajanda koşuldu:
  Δ(görünür-A)=+0.062 ≥ Δ(enerji)=+0.033 → genel girdi-iyileştirmesi.
  Öz-model kanıtı olarak sınıflandırma kaldırıldı (M-13 merdiveni
  çalıştı).
- **PL-23 — S3 vitals enstrüman kusuru (KAPALI, 2026-07-27):** Sayaçlar
  ölümde resetlenen `Citizen` nesnesinde yaşıyordu; `signal_rate`
  resetlenen payı kümülatif paydaya bölüyordu → "sinyaller söndü"
  artefaktı (gerçek oran 0.55 ve yükseliyor). Onarım: `Ledger` kümülatif
  defteri + pencere oranları + `World.b_openings_total` + M-23
  bilinen-pozitif testleri; test eski cihazda DÜŞTÜĞÜ doğrulandı.
  Ayrıca halef doğum yeri `succ_rng` → `World.respawn_entity()`
  (anayasa: dünya rastgeleliği tek generator'dan). Çürütme FINDINGS S3
  ENSTRÜMAN ŞERHİ'nde; orijinal metin M-12 gereği korundu.
- **PL-24 — economy v3 (B=180) (KAPALI, 2026-07-27):** Eksik oracle
  yazıldı (`training/b_oracle.py`, ajan değil ölçüm aleti — 0 bit).
  48 epizot × tavan 3000: eşik yine **135**; çapraz kontrol v1'in
  1500-tur tavanındaki 62 açılışına karşı 129 ≈ 2×62 → neredeyse
  birebir yeniden üretim. `resource_b_energy=180` gerekçesi AYAKTA,
  KAPI 5 kapandı, sansür oranı (39/48) beyanlı.
  Veri: `runs/s3_b_oracle_v2.json`.
- **PL-25 — B keşfedilebilirliği (SONUÇLANDI: ÇATAL C, 2026-07-27):**
  Ön-kayıtlı çıtaların İKİSİ de düştü. Mevcut config'de `signal`
  0.0 açılış/1000 çift-turu vs kanalsız `vision` 0.652 → **kanal
  ZARAR veriyor**; güçlü çıta (6.2) ~66× altında. M-21 kontrolü
  (n=5): mutlak sayılar 5× arttı (`vision` 4/48 → 20/48) ama sıralama
  değişmedi ve güçlü çıta yine aşılmadı (en iyi 2.227).
  Mekanizma: kanal yön/kimlik taşımıyor (PL-21b/c) → menzil büyütmek
  duyma oranını artırırken yerelleştirmeyi aynı oranda bozuyor (net
  fayda 0) + enerji maliyeti pencereyi kısaltıyor (146→116→90).
  Yoğunluk, menzil ve senkron penceresi süpürmelerinin HİÇBİRİ tavanla
  (43/1000, 48/48) aradaki farkı kapatmıyor → doz sorunu değil.
  Veri: `runs/s3_b_discover.json`, `runs/s3_b_calib.json`.
  **AÇIK KALAN ÇERÇEVE KARARI (Ali):** (A) görevi değiştir —
  koordinasyonun zor kısmı uzamsal olmasın (yönsüz 4 bit "nerede"
  taşıyamaz, "ne/ne zaman" taşıyabilir); (B) kanal konum/yön taşısın
  (ağır anayasal değişiklik, deneyin sorusunu zayıflatır).
  Tavsiye: (A). PL-22 bu karardan SONRA anlamlı.
- **PL-24-eski — economy v3 (B=180) yeniden üretilemez (kapandı; özgün metin):**
  `runs/s3_b_oracle.json`'ı üreten kod repoda yok; `training/oracle.py`
  yalnız A kanalına bakar ve "Tanrı-gözü YOK" der — FINDINGS'in
  "Tanrı-gözlü koordinasyon oracle'ı" tanımıyla çelişir. KAPI 5 açık.
  Ayrıca B≥135 satırlarının hepsi 1500-tur tavanında (sansürlü) →
  "keskin eşik 135" okuması bu sansürle sınırlı. Yapılacak: oracle'ı
  yaz + commit et, B süpürmesini yeniden üret; sayı değişirse
  `world/config.py` M-10 damgasıyla güncellenir.
- **PL-25 — B koordinasyonunun KEŞFEDİLEBİLİRLİĞİ hiç ölçülmedi (AÇIK;
  M-22):** Şans-keşfi olasılığı 20K turda 0.002 → gözlenen "B-açılış 0"
  sıfır güçlü ölçüm, ajan hakkında negatif değil. S3'ün merkezi basıncı
  şu an FİİLEN YOK. Yapılacak: keşfedilebilirlik oracle'ı (kanallı
  scripted koordinatör B'yi ne kadar sürede buluyor) → B yoğunluğu /
  senkron penceresi / menzil kalibrasyonu. PL-22 çerçeve kararından
  ÖNCE gelmeli: yoksa hangi seçenek seçilirse seçilsin basınç doğmaz.
- **PL-27 — (KAPALI, Ali kararı (c), 2026-07-27):** Öncü, ayrı kanal
  AÇILMADAN tehlike kanalına yazılır; algı ajan-merkezli ve ÖZEL
  (spec'in "her ajana olayın farklı parçası" maddesi). Kodlama:
  (0,0)=pencere açık, (0,1)=bit indeksi, (1,0)=bit değeri. **0 bit**
  KERNEL_BUDGET'a. Kayıpsızlık ve özel-algı testle sabitlendi
  (`tests/test_events.py`). Ajan öncüyü gerçek tehlikeden kendisi
  ayırmak zorunda (öncü yalıtık + enerji çekmez; tehlike 5×5 + çeker).
- **PL-28 — (KAPALI, Ali kararı 2026-07-27):** `signal_range` 8 → 32
  = küresel (64-toruste azami Chebyshev 32). Sembolün taşıdığı tek şey
  KİMLİĞİ. PL-21'in "yakın ajanlar duyar" gerekçesi geri alındı ve
  bunun S3-B sonucunu değiştirmediği itiraz testiyle gösterildi
  (küresel menzilde bile kanalsız `vision` 20/48 önde → ÇATAL C sağlam).
- **PL-27-eski — İpucu bölünmesinin GÖZLEM KODLAMASI (kapandı; özgün metin):**
  Fizik hazır ve fizibilite ÇATAL A verdi; ama ajanın ipucu bitini
  NASIL algılayacağı henüz kararsız. Oracle ipucunu doğrudan okuyor
  (ölçüm aleti; ajana gitmiyor). Seçenekler ve bit maliyetleri:
  (a) yeni gözlem kanalı "öncü" + bit değeri hücre yoğunluğunda
      (~1-2 bit; K-101'in kanal-ayrımı emsali),
  (b) iki ayrı kanal (bit=0 / bit=1) — kategorik ayrımı hediye eder,
      daha pahalı (~2-3 bit),
  (c) mevcut tehlike kanalını yeniden kullanmak — 0 yeni bit ama
      olay/tehlike ayrımını ajana bırakır (en cimri, en zor).
  Tavsiye: (c) sonra (a); her biri M-19 doğum günü kapısından geçmeli.
  Not: kanal açıldığında obs_dim değişir → S3-C ajanları taze başlar.
- **PL-28 — Sinyal menzili küresel olsun mu? (AÇIK, Ali kararı):**
  S3-C kalibrasyonu çıtanın YALNIZ menzil 32'de aşıldığını gösterdi
  (64-toruste Chebyshev 32 = küresel). Küresel kanal, sembolün
  taşıyabildiği tek şeyin KİMLİĞİ olması demektir (uzam/yön/mesafe/
  gönderen hepsi düşer) — dil tuzağının en temiz hâli. Ama PL-21'in
  "yakın ajanlar duyar" gerekçesini geri alır. Ara değerler yetmiyor
  (menzil 24 → yeterlilik 0.468, çıta 0.50). Alternatif: menzili 24'te
  tutup `event_penalty` veya `event_every` ile basıncı artırmak —
  o da ayrı bir kalibrasyon koşumu ister (M-01).
- **PL-05 — events.py (KAPALI, 2026-07-27):** S3–S4'e ertelenen
  asimetrik olay enjeksiyonu S3-C'de yazıldı (`world/events.py`),
  fiziği testli, varsayılan KAPALI (bit-eş korunum:
  `test_disabled_by_default_is_bit_identical`).
- **PL-26 — Kaynak doküman repoda yok (KAPALI, 2026-10-18):**
  `PETRI_TALIMAT.md` repoda mevcut (commit ce97904, 2026-10-06; ilk
  oturum açılışında doğrulandı). Anayasal hakem erişilebilir. Özgün
  kayıt: CLAUDE.md "çelişki halinde kaynak doküman kazanır" diyordu ama
  dosya dizinde yoktu; spec'e dayanan yorumlar (4.2 kanal, 4.3 roster,
  4-6× B bandı) ikincil kaynaktan okunuyordu.
- **PL-22 — Ekoloji nefes alamadı (S3 ilk nefes, ÇERÇEVE KARARI Ali'de):**
  5-ajan/ölüm-gerçek/seçilimsiz-mutasyon rejiminde medyan ömür 53-66 tur
  (öğrenme ufkunun ~750× altında); kanal maliyet baskısıyla söndü;
  seed-3 mirası eridi. Seçenekler FINDINGS S3 (a seçilim / b yuva-dönemi
  / c 5×klon taban); tavsiye (c)+(b) sonra (a), her biri M-21 gereği
  yeni nüfus-oracle'ı ister. PL-06 gerilimi ("ölüm gerçek" vs "yetiştirme
  kabı") ekolojik ölçekte fiilen patladı.
  **GÜNCELLEME (2026-07-27, PL-23 denetimi):**
  (i) *"kanal maliyet baskısıyla söndü"* ÇÜRÜTÜLDÜ — enstrüman
  artefaktıydı; gerçek sinyal oranı 0.55 ve YÜKSELİYOR (FINDINGS S3
  ENSTRÜMAN ŞERHİ). Sinyal kullanımı yetkinlik eridikçe ARTIYOR.
  (ii) Sürüklenme nicelendi: seed-3 ağırlık RMS'i 0.0804, mutasyon
  σ=0.01 → gürültü=sinyal **65. nesilde**; koşum 250-356 nesle gitti,
  yani miras t≈3900'de bitmiş, kalan %80 saf rastgele yürüyüş.
  DP-01b anlamlı olacaksa σ≈0.002 (kritik nesil ~1600) ya da
  seçilim (a) şart — bu, a/b/c seçiminin nicel girdisi.
  (iii) Ömür medyanı 56 tur = "her tur hareket" tavanı (62.5): ajanlar
  tasarruf ETMİYOR, sürekli hareket ediyor (S2'nin tasarruf-ağır
  patolojisinin TERSİ).
  **Sıra şerhi:** PL-25 (B keşfedilebilirliği) bu karardan ÖNCE
  kapanmalı; aksi halde a/b/c'nin hiçbiri B basıncını doğuramaz.
  **Taban veri v2 TAMAMLANDI** (`runs/s3_breath_v2/breath.json`, 20K
  tur / 100K ajan-turu): 1714 ölüm, medyan ömür 52, A-hasat 79,
  B-açılış 0, sinyal oranı 0.681 plato; sembol entropisi 3.9897/4 bit
  (yapı yok; sosyal katman için ön-kayıtlı gürültü tabanı 0.0103 bit).
  Ayrıntı FINDINGS "S3 TABAN ÇİZGİSİ v2".
  **KARAR (Ali, 2026-10-18):** önce (c) 5× seed-3 klon taban + (b) yuva
  dönemi; seçilim (a) sonra ayrı değişken (M-06). Başlangıç: M-21 gereği
  nüfus fizibilite oracle'ı (öğrenen ajan koşumundan ÖNCE).
  **ORACLE SONUCU (2026-10-18, FINDINGS S3-D):** kapasite ✓; klon taban
  ✓ (5 klon kanal-kapalı 118 tur); ASIL KIRILMA KANAL: kanal açılınca
  78 tur (dondurulmuş klon turların %77'sinde sinyal yayıp maliyet
  ödüyor) → ekolojideki 52'nin birincil kaynağı drift değil kanal
  maliyeti (bu kaydın (ii) "drift" teşhisi ikincil kaynağa düşer).
  Yuva: (600, 0.5) → 408 tur, hasat korunur; f≤0.25 yuva-sonu uçurumu.
  **KARAR (Ali, 2026-10-18 gece):** yuva (600, 0.5) + kanal açık
  onaylandı; oto karar + push yetkisi. **S3-E SONUCU:** ekoloji 138 tur
  (çıta 300 ✗), dil doğmadı (MI 0.001 bit), kanal net zarar (61 vs 83).
  Drift baskın → PL-31 σ merdiveni (S3-F) koşuluyor.
- **PL-32 — Kanal neden öğrenmeyi yavaşlatıyor? (AÇIK, S3-L koşuluyor):**
  S3-K: kanal açıkken kendi-ipucu öğrenmesi 100K'da başlamıyor (0.24
  düz) — kapalıyken 0.31 ↑. Üç aday mekanizma: planlayıcı aday
  seyrelmesi (6×17 uzay), girdi gürültüsü (16+17 boyut), sinyal
  maliyeti. Ayırıcı: `--channel hear` (duy, konuşma) / `--channel speak`
  (konuş, duyma). 0 bit.
- **PL-33 — Tuzağın eksik dişlisi: göndericiye dönen fayda (AÇIK,
  anayasal tasarım, Ali/Claude):** sinyalin bireysel beklenen değeri
  ≤ 0 (küresel olay, kişisel ceza, kimliksiz kanal, akrabalık yok) →
  hiçbir öğrenen sistem sinyal seçmez. Seçenekler: (a) soy düzeyinde
  seçilim ("paylaşan soy çoğalır": halef, en çok hayatta kalan SOYDAN
  değil, hayatta kalma + ortak isabet puanı yüksek soydan — ödül değil
  demografi, ama tasarım kararı), (b) olay cezasının kısmen paylaşılması
  (görev değişir), (c) tekrarlanan eş / yerel kanal (PL-28'i geri alır).
  M-28 ders adayı (FINDINGS S3 kapanış).
  **KARAR (Claude, 2026-10-19 sabah): (b) `event_share=0.5`** — fizik
  değişikliği, 0 bit, s=0 bit-eş testli; (a) nüfus-düzeyi ödül
  şekillendirmeye kaydığı için reddedildi; (c) PL-28'i geri alır.
  Oracle (M-01) + ekoloji S3-N koşuluyor; beyan: görev "sürü alarmı".
- **PL-30 — (KAPALI, S3-E…K koşuldu):** olay görevi klon+yuva
  ekolojisiyle 15 koşum; hükümler FINDINGS S3 KAPANIŞ.
- **PL-22 — (KAPALI, 2026-10-19):** çerçeve (c)+(b)+σ=0.002 ekoloji
  kararlı (266 tur, olaysız); seçilim (a) 20K'da etkisiz (S3-H);
  soy-düzeyi seçilim PL-33'e devredildi.
- **PL-31 — Halef mutasyonu σ (DP-01b dozu) (AÇIK, S3-F koşuluyor):**
  S3-E: σ=0.01 ile klon yetkinliği ~65. nesilde eriyor (ömür 185→138,
  hasat 7.4→2.8/1K); kanal/olay kolları bunun üstüne biniyor. S3-F
  σ ∈ {0, 0.002} merdiveni (FINDINGS S3-F ön-kayıt). σ=0 "ölüm gerçek"
  kuralının ağırlık ayağını fiilen kaldırır (PL-06 gerilimi) — anayasal
  soru olarak Ali'ye işaretli; oto-karar yetkisiyle koşuluyor, karar
  sonuçla birlikte sunulacak.
  **SONUÇ (S3-F):** σ=0 → 260 tur kararlı, σ=0.002 → 266 kararlı,
  σ=0.01 → 138 eriyen. **KARAR (oto-yetki):** ekoloji varsayılanı
  σ=0.002 (S3-G'den itibaren). Anayasal şerh Ali'ye: "ölüm gerçek"
  bedene/yaşantıya, yapıya değil.
- **PL-29 — Ölüm ucuz / yuva çiftçiliği riski (AÇIK, S3-D kaydı):**
  Ekolojide ölen slot 100 enerjiyle ve (b) ile yuva korumasıyla yeniden
  doğar. Oracle f≤0.25'te klonların yuva biter bitmez öldüğünü gösterdi
  (15/15). Ekolojide bu, "yuvada yaşa, öl, yuvaya dön" döngüsü üretebilir
  (M-25 kaçış yolu; ölçülmedi, halefsiz oracle göremez). İzleme: ölüm
  sayısı / nesil hızı / yuva-içi ölüm payı. Olası kapatıcılar (Ali):
  halef doğum enerjisi < 100; yuva yalnız kurucu nesle; seçilim (a).
- **PL-30 — S3-C olay görevi + klon/yuva ekolojisi (SIRADAKİ, Ali
  onayı bekliyor):** `training/ecology.py` için (c) 5×A2 transplant
  kurucu kadro + (b) nest parametreleri + `event_every>0`. Öncesinde
  ecology.py `apply_turn(signal_cost=)` yoluna geçmeli (yuva sinyali
  kapsasın; f=1'de bit-eş değil, kayan nokta sırası değişir — determinizm
  testi yeniden koşulur, eski breath kayıtları etkilenmez). Ön-kayıt
  (M-08) yazılmadan koşulmaz.
- **PL-20 — Kısmi miras gerilimi (S3 açılışı, kayıt):** "seed-3 tabanı +
  roster heterojenliği" tam bağdaşmıyor: farklı obs_radius/memory_dim
  mimarileri ağırlık devralamaz. Uygulanan: A2 slotu transplant+mutasyon,
  diğer 4 slot taze. Alternatif (5×A2 klonu, roster'ı ertele) istenirse
  tek satır. Karar Ali'ye görünür olsun diye kayıt.
- **PL-21 — Sinyal fiziği varsayımları (S3, Ali onayı bekliyor):**
  (a) menzil=8 Chebyshev; (b) gönderen kimliği alıcıya VERİLMEZ;
  (c) kendi sinyalini duymaz (efferensle bilir); (d) sinyaller dünya
  durumu/hash dışı (geçici enformasyon). Hepsi config/kodda tek noktadan
  değişir.
- **PL-19 — Tek-ajan mühendisliği kapanış durumu (S2.10, bilgi amaçlı):**
  Kayma katmanı çözüldü (K-113 + M-19 kapısı); nakit d1 ✓ / d2 ✗;
  seed 3 tam eval'de eşik-üstü hasat verdi (tarihte ilk). Kalan iki
  açık fenomen (müdahale önerisi YOK — vade doldu; kayıt): (i) hasat
  sıçraması büyüklüğünün eksik tahmini (%25-75), (ii) seed varyansı
  (seed 0 enerji kalibrasyonu kurulamıyor). Ağırlıklar
  `runs/s210_weights/`. S3 kararı ve çerçeve Ali'de.
- **PL-18 — M-18 sınır sorusu (KAPALI, Ali kararı 2026-07-08):**
  Salt-yerellik izinli, M-19 doğum günü kapısıyla; uygulandı (K-113),
  kapıdan geçti. Orijinal soru metni:
  Salt yerellik prior'ı (eylem-koşulsuz evrişimli decoder) M-18
  kapsamında mı? Eylem-koşullu kayma-eşdeğişimlilik açıkça yasak
  (cevabı yazar); salt yerellik kaymayı yazmaz ama öğrenilebilir kılar.
  S2.9 Çatal C'nin tek çıkış yolu bu sınırın yorumundan geçiyor
  (alternatif: doz artırımı — doz-cevap eğrisi tek noktalı, umut zayıf;
  veya öz-hareket negatifini kabul edip S3'e geçmek).
- **PL-17 — Nakde çevirme darboğazı (S2.8'de mekanizma ÖLÇÜLDÜ; S2.9
  Çatal C: veri/dikkat-yönlü çözüm K-110rev dozunda YETMEDİ):** Aday-önek seyrekliği hipotezi K-111 ile test edildi ve
  ELENDİ (makrolar + CEM-4 → nakit d1=%25, çıta %70). Ölçülen gerçek
  mekanizma: model hareket altında egosantrik grid kaymasını
  öğrenmemiş (kayma sadakati: merkez 0.08, eski konum 0.71) →
  rollout'ta kaynağa yaklaşılamıyor → hasat planı hiç kârlı
  görünmüyor. PL-12/M-05'in uzamsal enkarnasyonu: tasarruf-ağır veri
  → grid-kalıcılık modeli → kapalı döngü. Seçenekler (FINDINGS S2.8):
  (a) hareket-zengin veri (ε artışı / PER grid-değişim tabakalaması —
  ucuz, tavsiye edilen), (b) kayma-eşdeğişimli decoder (güçlü uzamsal
  prior, KERNEL_BUDGET tartışması şart), tek tek (M-06). K-104 ön-kayıt
  gereği KAPALI (nakit geçmedi → keşif çatalına ulaşılamadı).
- **PL-16 — Keşif tuzağı (GÜNCELLENDİ, S2.7):** Yuva müfredatı deneyimi
  10 → 25-57'ye çıkardı (N*=50 sınırında) ve calibN N*=50 gösterdi —
  deneyim üretimi artık birincil darboğaz değil; bayrak PL-17'ye devretti.
  Orijinal S2.6 metni: v2 ekonomide hasat kârlı (oracle
  kanıtlı) ve tasarruf stabil öğreniliyor (PER, çöküş yok) ama
  görme→yaklaşma→etkileşim zinciri ε-keşifle tamamlanmıyor: 45K turda
  10 hasat olayı → model olumsallığı öğrenemiyor → MPC hasat planı
  kuramıyor. Seçenekler: (a) merak terimi (K-104'ün bilinçli boşluğunu
  bozar — anayasal karar), (b) dünya-tarafı doğum/yuva müfredatı
  (kaynak-yakını spawn; sıfır ajan-biti, emsalli), (c) bu haliyle S3.
  Tavsiye: (b). PL-10 ve PL-12'nin kalan yarısı buraya devrolur.
- **PL-13 — Ali'nin öngörüsü askıda (kayıt):** "Öz-konum temsili hasat
  yetkinliğiyle birlikte yükselir (temsil ihtiyacın gölgesidir)" —
  hasatçı ajan üretilemediği için test edilemedi; yara almadı. Hasat
  çıktığı gün S2-tekrar protokolü hazır (`runs/s2r_*` + probe).
- **PL-11 — Davranış kalıplaşması prob gücünü düşürüyor (S2 gözlemi):**
  Ajan politikası neredeyse deterministik (tek keşif kaynağı ε=0.1) →
  eval epizotları birbirine çok benziyor → displacement gibi hedeflerde
  varyans düşük, prob CV'si kararsız. S3'te nüfus/etkileşim doğal
  çeşitlilik getirebilir; gelmezse eval protokolüne çeşitlendirilmiş
  başlangıç eklemek değerlendirilmeli (dünya-tarafı, prior değil).
- **PL-05 — events.py S0 dışı bırakıldı:** Asimetrik olay enjeksiyonu
  (`world/events.py`) gözlem/ajan kavramına bağımlı olduğundan S3–S4
  kapsamına ertelendi. S0 fiziği (drift, tehlike doğumu) grid.py içinde.
