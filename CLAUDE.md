# PETRI — Session Anayasası

> Kaynak: `PETRI_TALIMAT.md` (Bölüm 10 gereği türetildi). Çelişki halinde
> kaynak doküman kazanır. Bu dosya her oturumun başında okunur.

## Proje tek cümlede
Bilinç üretmiyoruz; bilincin öncüllerinin (öz-model, yüksek mertebe
modelleme, birleşimsel iletişim) hangi ekolojik basınç altında
**kendiliğinden** belirdiğini yakalayan bir tuzak kuruyoruz.

## İhlal edilemez ilkeler (özet)
1. **Çekirdek minimalizmi:** Ajana verilen her ön-bilgi bit cinsinden
   `KERNEL_BUDGET.md`'ye gerekçesiyle loglanır. Gerekçesiz prior yasak.
2. **Fizik hakemdir:** Ödül şekillendirme YASAK. Tek içsel sinyal:
   tahmin hatası + homeostaz.
3. **Dil verilmez, basınç verilir.** Kanal: sadece genişlik + enerji maliyeti.
4. **Duygu verilmez.** Duygu-benzeri durumlar problarla aranır, gömülmez.
5. **Davranış yalan söyler:** İddia yalnızca iç temsil problarıyla desteklenir.
   "Sanki anlıyormuş gibi davrandı" cümlesi rapora giremez.
6. **LLM deneyin İÇİNDE yer alamaz** — yalnızca gözlemci/log analisti.
7. **Negatif sonuç sonuçtur** — her sprint sonunda `FINDINGS.md`'ye yazılır.

## Bulgu disiplini
Pozitif bulgu iddiası, `FINDINGS.md`'deki **Beş Kapı** kontrol listesinden
geçmeden rapora giremez. Şablon oradadır; boş kapı = iddia yok.

## Sprint disiplini
- Durum: **S0-S2.10 ✓/✗ yayı kapandı; S2.10-ek ✓ (PL-13 iki-katmanlı
  verdikt, PL-15 kapandı-aday düştü); S3 AÇIK (economy v3, kanal açık,
  nüfus + DP-01b fiili, ölüm gerçek). İlk nefes koşumu: drift-baskın
  çöküş — rapor FINDINGS'te.**
- S2.10-ek özeti: üretici katmanda öz-hareket ↑ → hasat doğdu (Ali
  öngörüsü o katmanda desteklendi, n=1); disp probu yükselmedi
  (tek-adım kayma ≠ kümülatif entegrasyon); öz-enerji adayı
  varyans-eşleşmiş kontrolle DÜŞTÜ (genel girdi-iyileştirmesi).
- S3 açık soruları: ekoloji öğrenme birikimi yapamıyor (ömür medyanı
  56 tur = "her tur hareket" tavanı; seçilimsiz mutasyon σ=0.01 mirası
  65. nesilde gürültüye gömüyor). Çerçeve kararları Ali'de (PL-22).
- **DÜZELTME (2026-07-27, PL-23):** "sinyal maliyet baskısıyla sönüyor"
  iddiası ÇÜRÜTÜLDÜ — vitals enstrüman artefaktıydı (sayaçlar ölümde
  resetleniyordu). Gerçek sinyal oranı 0.55 ve YÜKSELİYOR; kullanım
  yetkinlik eridikçe ARTIYOR, yani şu an iletişim değil planlayıcı
  yetkinsizliği ölçülüyor. Enstrüman onarıldı (Ledger + M-23 testleri).
- **PL-24 KAPALI:** B oracle'ı yazıldı (`training/b_oracle.py`); eşik
  yine 135, B=180 gerekçesi ayakta, KAPI 5 kapandı.
- **PL-25 SONUÇLANDI — ÇATAL C:** B koordinasyonu mevcut kalibrasyonda
  keşfedilebilir DEĞİL. Kanal yardım etmiyor, ZARAR veriyor
  (`signal` 0.0 vs kanalsız `vision` 0.652 açılış/1000 çift-turu);
  mükemmel konvansiyon hediye edildiğinde bile. Yoğunluk/menzil/
  senkron penceresi süpürmelerinin hiçbiri tavanı (43/1000, 48/48)
  yakalamıyor → doz sorunu değil, görev-kanal uyumsuzluğu: yönsüz
  4 bit "nerede" taşıyamaz.
- **S3-C AÇILDI — Ali kararı (A):** görev uzamsal olmaktan çıkarıldı.
  `world/events.py` (PL-05 kapandı): küresel olay, güvenli olan TEK
  eylem = kutup; kutup log2(K)=2 bitlik kod ve her ajan olay başına
  YALNIZ 1 bit gözler (`event_visibility_split`) → bilgi tek ajanda
  tamamlanmaz. `event_duration=1` tasarım kilidi: acıdan öğrenme
  kaçışı kapalı. Ekolojik emsal: alarm çağrısı.
- **Fizibilite ÇATAL A (ön-kayıtlı üç çıta da geçti, n=5/menzil 32):**
  değer 1.96 ✓, gereklilik 0.241 ✓ (+ `own_infer`=`own` birebir),
  yeterlilik 0.709 ✓. Olaylar ömrü yarıya indiriyor (210→115); kendi
  ipucu değerin %24'ünü, mükemmel konvansiyonlu yayın %71'ini kurtarıyor.
  **Görev geçerli bir dil tuzağı.** Veri: `runs/s3c_event_oracle.json`.
- **PL-27 KAPALI (Ali: seçenek c) — 0 prior biti.** Öncü ayrı kanal
  açılmadan tehlike kanalına yazılır; algı ajan-merkezli ve ÖZEL
  ((0,0)=pencere, (0,1)=bit indeksi, (1,0)=bit değeri; anlamları
  söylenmez). Ajan öncüyü gerçek tehlikeden kendisi ayıracak.
  Kayıpsızlık + özel-algı testli.
- **PL-28 KAPALI (Ali): `signal_range` 8 → 32 = KÜRESEL.** Sembolün
  taşıyabildiği tek şey KİMLİĞİ. İtiraz testi: küresel menzil S3-B'nin
  ÇATAL C'sini değiştirmiyor (kanalsız `vision` hâlâ önde).
- **PL-22 KARAR (Ali, 2026-10-18): (c) 5× seed-3 klon taban + (b) yuva
  dönemi; seçilim (a) sonra.** S3-D nüfus oracle'ı (`training/pop_oracle.py`,
  FINDINGS S3-D): kapasite ✓, klon taban ✓ (118 tur), **kanal klonu
  boğuyor** (açılınca 78; dondurulmuş klon %77 sinyal yayıyor) → 52
  turluk ömrün birincil kaynağı kanal maliyeti. Yuva (600, f=0.5) →
  408 tur, hasat korunur; f≤0.25 yuva-sonu uçurumu (PL-29).
- **S3 KAPANIŞ (2026-10-19, FINDINGS "S3 KAPANIŞ RAPORU"):** 15 koşum
  (S3-E…K). σ=0.002 ile ekoloji kararlı; model öncüyü görüyor; tek ajan
  kendi ipucunu öğreniyor (0.86); kanal-kapalı ekoloji öğreniyor (0.31↑);
  kanal açıkken öğrenemiyor; kanal 0 bilgi taşıyor (MI ≤0.0005 bit).
  **H4 NEGATİF (bu koşullarda), H3 ön koşul negatif, H2 test edilmedi,
  H1 karışık.** Yeni prior: 0 bit. Teşhis: göndericiye dönen fayda yok
  (PL-33). Ali: tüm kararlar Claude'da (18 Ekim), defterli.
- **S3-L…P (19 Ekim):** yavaşlatan taraf gönderme; paylaşılan kayıp
  (event_share 0.5) faydayı fiziğe ekledi ama yetmedi; planlayıcı kendi
  sinyaline SAHTE prim öğreniyor (M-05); bütçe/ε susma yarıya indirdi,
  silemedi. **0-bit merdiven bitti. Nihai: H4 negatif, mekanizmalı.**
  M-26/27/28 işlendi. Yeni prior 0 bit.
- **Program B (S3-Q/R, 19-20 Ekim):** kapalı 300K → isabet 0.36, kendi-
  ipucu 0.75; kanal açılınca yetkin ajan sinyali fiyatlamayı öğrendi
  (prim tersine, ilk kez) ama açılış şoku −0.08 ve 300K'da geri gelmedi;
  dil yok. **S3 NİHAİ: H4 negatif, mekanizması tam; kanal kalıcı yük.**
  M-29 işlendi. 93 koşum, 0 bit.
- **Program A + C (20 Ekim):** sahte sinyal priminin kaynağı = halefte
  PER sıfırlaması (ömür 40 → tampon boş); `inherit_per` varsayılan
  (PL-35): prim silindi, açık=kapalı. Topluluk ✗ (K-115 geri). Sığınak
  tuzağı: N=3 kredi atamasını bozdu, N=2 + yetkin kadro + tampon →
  kanal nötr ve fiyatlı, isabet 0.45 (tavan), MI 0.004 platosu, kanal
  KULLANILMIYOR (600K). M-30/M-31. Toplam 113 koşum, 0 bit.
- **Program A′/A″ (20-21 Ekim):** ada modeli grup seçilimi (6+3 ada, 360K
  tur/ada) sembol anlamı doğurmadı. Post-hoc: konuşma KARARI ipucu
  değerini taşıyor (0.10 bit), A″ ablasyonunda ~%75 refleks; dinleyen yok.
  Toplam ~150 koşum, 0 bit.
- **PL-37 (21 Ekim):** kanal tavan değil (CH0); okulda dinleyici öğrenebiliyor
  (RS: 0.62, tavan 0.50 aşıldı — ilk); eşik ≈0.18 bit gönderici netliği
  (RS-dose); ekoloji 0.08 bit.
- **PL-38 (21 Ekim):** uzun ekoloji 500K ve lead 6/8: gönderici netliği
  0.05-0.10 bitte kilitli; dinleyici yok. Sessiz denge.
- **SIRADAKİ ADIM (PL-39, Ali kararı):** kültürel tohumlama ile "konuşan+
  dinleyen" dengenin kararlılığı (köken değil); KERNEL ~1 bit beyanı.
- Enstrüman rafı + ağırlık kayıtları: runs/. `probes/` sosyal katman
  KAPALI.

## Teknik kurallar
- Python 3.13 (dokümanda 3.12 — bkz. OPEN_LOOPS PL-04), NumPy vektörize dünya.
- Determinizm anayasal: dünyadaki TÜM rastgelelik `World` içindeki tek
  `numpy.random.Generator`'dan (PCG64, seed `WorldConfig.seed`) akar.
  `random`, `time`, global `np.random` kullanımı dünya kodunda yasak.
- Her fizik değişikliğinde determinizm testleri yeniden koşulur:
  `python3 -m pytest tests/ -q`
- Replay kaydı `.npz` formatında; izleme ayrı süreçte:
  `python3 -m replay.viewer record out.npz --turns 2000`
  `python3 -m replay.viewer play out.npz --fps 20`

## Metodoloji
Tasarım kararlarında `METODOLOJI.md` derslerine aykırılık varsa durup
Ali'ye sor. Her sprint raporu "Yeni ders var mı?" ile kapanır.

## Belirsizlik protokolü
Belirsizlikte Ali'ye sor, varsayma. Bloklanmamak için geçici varsayım
gerekiyorsa: varsayımı `OPEN_LOOPS.md`'ye PL-xx olarak yaz, kodda config
parametresi olarak açık bırak, raporda beyan et.
