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
- **SIRADAKİ ADIM:** Ali'den yuva ayarı + kanal stratejisi onayı (PL-22
  bekleyen), sonra PL-30: S3-C olay görevini klon+yuva ekolojisiyle
  koşmak (ön-kayıt önce).
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
