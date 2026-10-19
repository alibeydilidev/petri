# METODOLOJI — Nasıl Aramayı Öğrendik

> Yaşayan dosya. Her sprint kapanışında güncellenir. `FINDINGS.md`
> "ne bulduk"tur; bu dosya "nasıl aramayı öğrendik"tir. Her sprint
> raporunun son bölümü "Yeni ders var mı?" sorusuna cevap verir:
> varsa buraya M-xx olarak eklenir, yoksa rapora "yok" yazılır.
> Tasarım kararı bu derslerden biriyle çelişiyorsa: DUR, Ali'ye sor
> (CLAUDE.md kuralı).

## Dersler

- **M-01 — Cetvel önce, çıta sonra** *(S2.5→S2.6)*: Hedef koymadan önce
  fizibilite oracle'ı koşulur. Ulaşılabilirliği kanıtlanmamış
  bitti-tanımı geçersizdir. (S2.5 hedefi baştan imkânsızdı; S2.6'da
  oracle bunu iki saatte gösterdi.)
- **M-02 — Ajanı yargılamadan önce dünyayı yargıla** *(S2.6)*:
  "Öğrenemiyor" teşhisinden önce "öğrenilecek şey gerçekten optimal mi"
  sorusu. (Üç sprint'lik tasarrufçuluk ajanın hatası değil, dünyanın
  gerçek optimumuydu — hasat net zarardı.)
- **M-03 — Karıştırılmış negatif ≠ negatif** *(S2)*: Ayırt etme gücü
  olmayan koşulda ölçülen negatif "confounded" etiketi alır, düz negatif
  değil. (Öz-konum: hareketsiz ajanda yol entegrasyonu ölçülemez.)
- **M-04 — Girdi yankısı tuzağı** *(S2)*: Gözlemde zaten duran değişkenin
  hidden state'ten "okunması" temsil kanıtı değildir; rastgele-ağırlıklı
  ikiz kontrolü zorunludur. (İkiz GRU'nun enerji R²'si 0.96–0.98 çıktı —
  kontrolsüz koşsak sahte pozitif manşet atacaktık.)
- **M-05 — Karşı-olgusal çürüme** *(S1-v1, S2.5-adım4; PL-12)*: Kapalı
  döngü on-policy öğrenmede model, az yapılan eylemin sonucunu kalibre
  edemez; ajan neye yakınsarsa modelin karşı tarafı çürür ve döngü
  kararsızdır. Panzehir: olay-öncelikli tekrar (PER), eylem-dengeleme
  değil — nadirlik eylem uzayında değil durum uzayındaysa
  eylem-dengeleme kurtarmaz.
- **M-06 — Tek değişken merdiveni** *(S2.5)*: Müdahaleler sıralı denenir,
  hepsi birden değil — "hangisi çözdü" bilgisi çözümün kendisi kadar
  değerli. Başarısız merdiven de mekanizmayı katman katman soyar.
  (S2.5'in 4 adımı hasat vermedi ama PL-12'yi teşhis etti.)
- **M-07 — Pozitif kontrol olmadan negatif yorumlanamaz** *(S2→S5)*:
  P1 aynı zamanda prob aparatının kalibrasyon testidir; P1 altyapısı
  doğrulanmadan P2/P3 negatifi "çıkmadı" mı "ölçemedik" mi
  ayrıştırılamaz.
- **M-08 — Öngörüler önceden kayda girer** *(S2.5; PL-13)*: Sonuç
  gelmeden yazılmış tahmin bağlayıcıdır; sonuçtan sonra yazılan yorum
  kendine yontar. Sonuç matrisi (hangi kombinasyon ne anlama gelir)
  deney koşulmadan yorumlanır. (Öz-konum/hasat korelasyon öngörüsü
  PL-13'te askıda ve kayıtta.)
- **M-09 — Sıfır-bit müdahaleler de deftere girer** *(S2–S2.6)*: Ekonomi
  kalibrasyonu, müfredat, bellek mimarisi ajan-priori olmasa da
  deneycinin kararıdır; itirazcı hakem bitleri değil kararları sayar.
  (A=45 kalibrasyonu, K-110 PER, curriculum şerhi.)
- **M-10 — Dünya sürümlenir** *(S2.6)*: Değer sistemini değiştiren her
  config değişikliği `economy_version` + config hash ile damgalanır;
  eski bulgular hangi dünyada doğduğunu üstünde taşır. ("S2 negatifi
  hangi ekonomideydi" sorusunun cevabı dosyada yazmalı, hafızada değil.
  Uygulama: v1 = A-enerji 15; v2 = A-enerji 45, 2026-07-08.)
- **M-11 — Belirsizlik geri alınabilir karara çevrilir** *(S0)*:
  Tanımsız parametre için durup sormak yerine config parametresi +
  OPEN_LOOPS kaydı; karar sonradan tek satırla değişebilir olmalı.
  (PL-01/02 refleksi.)
- **M-12 — Başarısız koşumlar kayıtta kalır** *(S1)*: v1 hataları ve
  ham verileri silinmez, `runs/` altında yaşar — hayatta kalan
  önyargısının panzehiri arşivdir. (`s1_results_v1_failed.json`
  geleneği.)
- **M-13 — İddia merdiveni** *(S2–S2.6; PL-09→PL-15)*: ADAY GÖZLEM →
  İDDİA terfisi ancak ardışık itiraz testlerinden (spawn
  randomizasyonu, ablasyon, eş-eğitimli kontrol...) sağ çıkmakla olur;
  Beş Kapı'dan tek kapı eksikse etiket düşük kalır. (Öz-enerji
  gözleminin PL-09→PL-15 yolculuğu.)
- **M-14 — Deneyim taban-oranı müdahaleden önce sayılır** *(S2.6
  stage-2)*: "Model X'i öğrenemiyor" teşhisi, X deneyiminin veride kaç
  kez geçtiği ölçülmeden eksiktir; öğrenme müdahalesi (PER, müfredat,
  keşif) bu sayıya göre seçilir. (PER'den önce hasat olayını
  saysaydık — 45K turda 10 — tamponun tekrarlatacak şey bulamayacağı
  baştan görülürdü; bir koşum tasarruf edilirdi.)
- **M-29 — Yeni eylem boyutu kademeli açılır, aksi hâlde eğitilmemiş
  sütun sahte prim üretir** *(S3-Q2, 2026-10-19)*: Bir ajanın hiç
  kullanmadığı eylem boyutu (sinyal) açıldığında, o boyutun modeldeki
  sütunları eğitimsizdir ve karşılaştırma dışı kaldıkları için argmax'a
  sahte bir prim olarak görünür (Q1→Q2: +1…+3 skor, ilk 2K turda sinyal
  oranı 0.97, yetkinlik −0.08 ve 300K'da geri gelmedi). Kural: yeni
  boyut ya baştan ε ile beslenir ya da açılış öncesi karşı-olgusal
  veriyle ısıtılır; "açılış şoku" ayrı bir ölçüm kalemidir. M-05 ve
  M-28'in geçiş-anı yüzü.
- **M-28 — Tuzağın geri dönüş yolunu kur, ama önce giriş ücretini
  ölç** *(S3-N…P, 2026-10-19)*: Bir davranışın (sinyal) kendiliğinden
  belirmesi için iki hesap gerekir: göndericiye dönen BEKLENEN DEĞER
  (M-25'in gelir tarafı) ve davranışı DENEMENİN öğrenme maliyeti (enerji
  + kapalı-döngü karıştırması). İkincisi birincisinden büyükse fayda
  hiç keşfedilmez; fiziğe fayda eklemek (paylaşılan kayıp) yetmez.
  Argmax planlayıcı + on-policy tek model, nadir eylemlere sahte prim
  öğrenir (M-05'in sinyal yüzü); bunu yalnız veri dengesiyle silmek
  mümkün olmadı. Kural: kanal basıncı tasarlanırken "ilk sinyalin
  bedeli" ve "ilk faydanın gecikmesi" birlikte, oracle ile ölçülür.
- **M-27 — Ekolojiyi yargılamadan önce tek-ajan tavanını ölç** *(S3-J,
  2026-10-19)*: "Nüfus X'i öğrenemiyor" teşhisi, aynı görevi TEK ajanın
  sınırsız deneyimle öğrenip öğrenemediği ölçülmeden eksiktir. Tavan
  şans düzeyindeyse sorun mimari/öğrenme sinyalidir (anayasal adım
  gerekebilir); tavan yüksekse sorun ekolojik parametredir (deneyim
  sayısı, ölüm, gürültü) ve anayasaya dokunulmaz. (S3-G/H/I üç basamak
  — doz, seçilim, zamanlama — bu ölçüm olmadan harcandı; 25 dakikalık
  "olay okulu" ayırdı: tek ajan kendi ipucunu 6/6 öğrendi, λ
  revizyonu gereksizdi.) M-01/M-02/M-21'in nüfus-öncesi özel hâli.
- **M-26 — Sürüklenme cihaz hatası gibi davranır** *(S3-E/F,
  2026-10-18)*: Seçilimsiz halef mutasyonu, öğrenmeyle kazanılan her
  şeyi nesil ölçeğinde siler ve bunu "ekoloji öğrenemiyor" gibi
  gösterir. Nüfus deneyinde σ, ağırlık RMS'ine göre ÖNCE kalibre edilir
  (kritik nesil ≈ (RMS/σ)²; σ=0.01, RMS 0.08 → 65. nesil), sonra
  öğrenme yargılanır. (S3 ilk nefes → S3-F arası üç koşum yanlış
  katmana yazıldı; σ=0.002'de aynı ekoloji 138 → 266 tur ve kararlı.)
- **M-25 — Tuzak kurmadan önce kaçış yollarını say** *(S3-C,
  2026-07-27)*: Bir yetinin (X) baskı altında kendiliğinden belirip
  belirmeyeceğini ölçecek aparatı kurmadan ÖNCE, ödüle giden alternatif
  yollar sayılır; herhangi biri X'ten ucuzsa tuzak X'i değil
  alternatifi ölçer. (Olay görevinin ilk taslağında 3 turluk olay
  "acıyı çek sonra düzelt" kaçışına izin veriyordu ve değerin ~%67'sini
  kurtarıyordu → kanal gereksiz kalırdı; kilit `event_duration=1`
  tasarım anında, koşum yapılmadan kondu. Simetrik uyarı B görevinden:
  kaçış yolu olmaması yetmez, ödülün kendisi de ULAŞILABİLİR olmalı.)
  M-01'in ("cetvel önce, çıta sonra") hedef değil TASARIM tarafına
  uygulanmış hâli; M-22 ile birlikte okunur.
- **M-24 — Payda tedaviden etkileniyorsa oran yanıltır** *(S3-B,
  2026-07-27)*: `açılış/1000 çift-turu` metriği, sinyal maliyeti
  koordinasyon penceresini kısalttığı için `beacon` kolunu en iyi
  gösterdi (11.5 > çıta 6.2); güvenilir ölçü olan EPİZOT PAYI'nda aynı
  kol en kötülerdendi (1/12). Kural: tedavi paydayı da değiştiriyorsa
  oran değil olay payı (ya da her ikisi birlikte) raporlanır. M-20'nin
  ("taban çizgisi de cihazın parçasıdır") payda kardeşi.
- **M-23 — Sonda kadar SAYAÇ da cihazdır** *(S3 denetimi, 2026-07-27)*:
  M-15 ölçü aletleri için vardı ama MUHASEBE enstrümanına uygulanmadı;
  S3 vitals sayaçları ölümde resetlenen nesnede yaşıyordu ve "sinyaller
  söndü" manşeti bu artefakttan doğdu (gerçek oran 0.55 ve YÜKSELİYORDU).
  Kural: türetilmiş/defter-tutan her metrik de bilinen-pozitifte
  doğrulanır; kümülatif alanın azalmadığı testle sabitlenir; ve testin
  ESKİ hatada düştüğü gösterilmeden test geçerli sayılmaz.
  Genel biçim: rejim değişince (M-21) enstrüman disiplini sıfırdan
  uygulanır — M-21'in ölçüm-tarafı ikizi.
- **M-22 — Fizibilite iki sorudur** *(S3 denetimi, 2026-07-27)*: "Ödül
  değer mi" (sürdürülebilirlik) ile "bulunabilir mi" (keşfedilebilirlik)
  ayrı ölçülür; M-01 birincisini kurumsallaştırdı, ikincisi ayrı bir
  oracle ister. (B kaynağı sürdürülebilir ilan edildi ama şans-keşfi
  olasılığı 20K turda 0.002'ydi — "B-açılış 0" bulgu değil, sıfır güçlü
  ölçümdü. Proje bu dersi A için zaten ödemişti: PL-16 keşif tuzağı.)
- **M-21 — Rejim transferi ölçülür, varsayılmaz** *(S3 ilk nefes)*: Bir
  rejimde (tek-ajan) kazanılan çözüm, komşu rejime (çok-ajan ekoloji)
  otomatik taşınmaz; taşınabilirliği bir hipotezdir ve ölçülür. Her yeni
  rejim kendi fizibilite oracle'ını (M-01) ve kalibrasyonunu ister.
  (seed-3 yetkinliği 5-ajan ekolojide 58 turda söndü: ömür<<öğrenme-ufku,
  seçilimsiz yenilenme, maliyet-altında-sönen kanal.)
- **M-20 — Taban çizgisi de cihazın parçasıdır** *(S2.10)*: Karşılaştırma
  tabanı ölçülen yetinin zorluğunda seçilmezse kapı boşuna açılır.
  (Kalıcılık tabanı hasat sıçramasında ~0.40 hata yapar; model
  sıçramanın %30'unu tahmin edip "tabanı yendi" sayıldı — H_eff kuralı
  olay adımlarında vekaleten sağlandı. Olay-bilinçli taban veya
  mutlak-hata eşiği gerekirdi.)
- **M-19 — Doğum günü testi** *(S2.10/K-113 kapısı)*: Yapıya eklenen
  her prior, ölçülen yetiyi INIT ağırlıklarında üretmediği gösterilerek
  aklanır; init'te üretiyorsa prior geri çekilir (yeti "kazanılmış"
  değil "verilmiş" olur, M-18'e düşer). Her yapısal prior eklemesinin
  zorunlu ön-kapısıdır.
- **M-18 — Bazı priorlar bağımlı değişkendir** *(PL-17, kayma-eşdeğişimli
  decoder reddi)*: Bazı priorlar pahalı oldukları için değil, ölçmek
  istediğin bağımlı değişkenin ta kendisi oldukları için yasaktır.
  (b)-tipi çözümler sınav cevabını kağıda yazar. (Öz-hareket/uzam
  modelinin KENDİLİĞİNDEN doğup doğmayacağı H1/P1'in sorusu; kayma
  eşdeğişimliğini mimariye gömmek soruyu cevaplamaz, iptal eder.)
- **M-17 — Cihaz, kullanım dağılımında koşar** *(S2.8)*: Bir modelin
  iyiliği hangi dağılımda kullanılacaksa orada ölçülür; on-policy
  metrik, karşı-olgusal kullanım (planlayıcı rollout'u) için geçerlilik
  taşımaz. (H_eff on-policy 10 çıktı; planlayıcının değerlendirdiği
  yaklaşma dizilerinde model grid-kalıcılık tuzağındaydı — kayma
  sadakati 0.08. Nakit testinin çökmesi boşluğu gösterdi.)
- **M-16 — Davranış sükût da eder** *(S2.7/B2, seed 1&3)*: Davranışsal
  negatif, bilgi negatifi değildir; bilgi ve kullanım ayrı katmanlar,
  ayrı enstrümanlarla ölçülür. (Model olumsallığı bağlam-içi biliyordu;
  eval davranışı sıfırdı. Tek enstrümanla "öğrenemedi" denseydi teşhis
  yanlış katmana yazılırdı.)
- **M-15 — Sonda da bir cihazdır** *(S2.7)*: Ölçü aleti,
  bilinen-pozitif üzerinde doğrulanmadan ön-kayıt kriteri yapılmaz.
  (Statik-STAY kalibrasyon sondası, bağlam-içi kalibre olduğu sonradan
  kanıtlanan modele "kalibre değil" dedi; ilk calibN süpürmesi bozuk
  cihazla koştu. Bilinen-pozitif testi — cihazı enjeksiyon
  pencerelerinin kendisinde çalıştırmak — kusuru bir koşum önce
  yakalardı. Düzeltme yuva koşumundan ÖNCE yeniden ön-kaydedildi;
  iki metrik de raporda.)
