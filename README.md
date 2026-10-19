# PETRI — Emergent Zihin Öncülleri Deneyi

> **Bilinç üretmiyoruz.** Bilincin öncüllerinin (öz-model, yüksek mertebe
> modelleme, birleşimsel iletişim) hangi ekolojik basınç altında
> **kendiliğinden** belirdiğini yakalayan bir tuzak kuruyoruz.

Kıt kaynaklı, deterministik fizikli bir grid dünyada yaşayan 5 heterojen ajan.
Her ajan yalnızca üç şeyden oluşur: **tahmin makinesi + homeostaz (ölümlülük)
+ kısıtlı sinyal kanalı.** Dil, duygu ve ödül şekillendirme verilmez. Davranış
değil, iç temsiller ölçülür. Negatif sonuç da sonuçtur.

**Durum (2026-10-19):** S3 kapandı (FINDINGS "S3 KAPANIŞ RAPORU"). Dil
tuzağı öğrenen ajanlarla 15 koşumda sınandı: ajanlar kendi ipuçlarını
öğreniyor, **kanal hiçbir bilgi taşımıyor ve öğrenmeyi yavaşlatıyor**
→ H4 bu koşullarda **negatif**, mekanizmasıyla: sinyalin göndericiye
faydası yoktu (fiziğe eklendi, yetmedi) ve planlayıcı kendi sinyaline
sahte bir enerji primi öğreniyor (kapalı-döngü karıştırma); 0-bitlik
çareler primi yarıya indirdi, silemedi. Program B (kademeli kanal,
600K tur): yetkin ajan sinyali fiyatlamayı öğrenebiliyor ama kanal
kalıcı net yük, kullanılmıyor (93 koşum). Ekoloji kararlı (σ=0.002),
ajanlar kendi ipuçlarını öğreniyor. Yeni prior 0 bit. Sonraki program
kararı PL-34 (Ali): evrimsel önyükleme / öğrenme mekaniği / yeniden
tasarım.

---

## Bu çalışma nasıl yürütüldü (açık beyan)

Hipotezler, anayasa ve mimari plan **Ali Beydili**'ye aittir. Kodun büyük
bölümü, tüm koşumlar, ön-kayıtlar, analizler ve bulgu metinleri, Ali'nin
verdiği karar yetkisiyle **Claude (Anthropic)** tarafından otonom olarak
yürütülmüş ve yazılmıştır; Ali karar noktalarında yön vermiştir (bkz.
`OPEN_LOOPS.md` "KARAR" satırları). Bu bilinçli bir seçimdir: deneyin
iddiası "ajana hiçbir şey vermeden" ise, deneyi yürüten elin de şeffaf
olması gerekir. Her koşum **koşumdan önce** yazılmış ön-kayıt ve çıtalarla
(`FINDINGS.md`, "ÖN-KAYIT" başlıkları) gelir; git geçmişi zaman
damgalıdır. Öngörü karneleri (tutmayanlar dahil) bulgu bölümlerinin
içindedir. Yanılgılar silinmez, şerh düşülür (M-12).

## Nereden başlanır (okuyucu rehberi)

1. **5 dakika:** bu README'nin "Şu an nerede duruyoruz" ve "Bulgu tablosu"
   bölümleri.
2. **30 dakika:** `FINDINGS.md` sonundaki **"S3 NİHAİ HÜKÜM"** ve
   **"S3 KAPANIŞ RAPORU"**; sonra `METODOLOJI.md` (29 ders: nasıl
   kendimizi kandırmadık).
3. **Doğrulamak isteyen:** `KERNEL_BUDGET.md` (ajana giden her bit),
   `tests/` (determinizm + bilinen-pozitif enstrüman testleri),
   `runs/*/breath.json` (ham sayılar; her tablo buradan türetilir).
4. **Tekrar koşmak isteyen:** aşağıda "Çalıştırma". Tüm koşumlar
   deterministiktir (dünya seed'i + ajan seed'i → bit-eş).

Lisans: kod MIT (`LICENSE`), doküman ve veri CC BY 4.0
(`LICENSE-DOCS-DATA.md`).

## İçindekiler
1. [Hipotezler](#hipotezler)
2. [Anayasa](#anayasa)
3. [Mimari](#mimari)
4. [Sprint yolculuğu: ne yapıldı, ne çıktı, neden](#sprint-yolculuğu)
5. [Şu an nerede duruyoruz](#şu-an-nerede-duruyoruz)
6. [Bulgu tablosu](#bulgu-tablosu)
7. [Repo haritası](#repo-haritası)
8. [Veriler (`runs/`)](#veriler-runs)
9. [Çalıştırma](#çalıştırma)
10. [Metodoloji dersleri](#metodoloji-dersleri)

---

## Hipotezler

| ID | Hipotez | Test aracı | Durum |
|----|---------|-----------|-------|
| H1 | Ölümlü ve eyleyen her tahmin makinesi iç temsilinde öz-model geliştirir | P1 lineer prob | Uzamsal yarı **negatif** (kümülatif yol entegrasyonu yok). Tek-adım öz-hareket iskeleyle **kazanıldı**. İnteroseptif yarı **düştü** (genel girdi iyileştirmesi). |
| H2 | Opaklık ve koordinasyon zorunluluğu, karşılıklı modellemeyi doğurur | P2 prob | Test edilmedi, sosyal katman kapalı |
| H3 | Kısıtlı kanal sinyalin içselleştirilmesini zorlar (Vygotsky) | P3 dedektör | Test edilmedi |
| H4 | Asimetrik bilgi ve kanal kıtlığı proto-gramer doğurur | Topografik benzerlik, Zipf | Test edilmedi. Tuzak S3-C'de kuruldu. |

**H0:** Gözlenen her şey reaktif hesaplamayla açıklanabilir. Her pozitif
bulgu önce H0'a karşı savunulur ve [`FINDINGS.md`](FINDINGS.md)'deki
**Beş Kapı**'dan geçmek zorundadır (ablasyon, prob sızıntısı, zaman çizgisi,
çekirdek bütçesi, bit-eş tekrar). Kapılardan biri boş kalırsa bulgu iddia
sayılmaz, **aday gözlem** olarak kalır.

## Anayasa

1. **Çekirdek minimalizmi.** Her prior bit cinsinden [`KERNEL_BUDGET.md`](KERNEL_BUDGET.md)'ye gerekçesiyle yazılır.
2. **Fizik hakemdir.** Ödül şekillendirme yasak. Tek içsel sinyal tahmin hatası ve homeostazdır.
3. **Dil verilmez, basınç verilir.** Kanalın yalnızca genişliği ve enerji maliyeti tanımlıdır.
4. **Duygu verilmez.** Duyguya benzer durumlar gömülmez, problarla aranır.
5. **Davranış yalan söyler.** İddialar yalnızca iç temsil problarıyla desteklenir.
6. **LLM deneyin içinde yer alamaz.** Yalnızca gözlemci ve log analisti olabilir.
7. **Negatif sonuç sonuçtur.**

Tam metin: [`PETRI_TALIMAT.md`](PETRI_TALIMAT.md) (kaynak doküman) ve [`CLAUDE.md`](CLAUDE.md) (oturum anayasası).

## Mimari

- **Dünya** (`world/`): 64×64 torus, NumPy vektörize. A kaynağı tek ajanla
  hasat edilir. B kaynağı iki ajanın eşzamanlı etkileşimini ister. Tehlike
  bölgeleri vardır. Küresel olaylar `world/events.py`'dedir. **Determinizm
  anayasaldır:** tüm rastgelelik tek bir `numpy.random.Generator`'dan
  (PCG64) gelir ve `World.state_hash()` ile bit-eş doğrulanır.
- **Ajan** (`agent/`): GRU tabanlı tahmin çekirdeği (`predictive_core.py`),
  homeostaz (`homeostasis.py`), MPC planlayıcı (`mpc.py`; CEM ve makro
  adaylar) ve 4 bit/16 sembollük sinyal kanalı (`channel.py`).
- **Nüfus** (`population/`): roster (heterojen kurucular), yaşam döngüsü,
  gerçek ölüm, ağırlık mirası ve mutasyonla halefiyet.
- **Eğitim ve enstrümanlar** (`training/`): online öğrenme döngüsü, PER,
  snapshot (detach ve sızıntısızlık testli), fizibilite oracle'ları
  (`oracle.py`, `b_oracle.py`, `event_oracle.py`), nakit testi, sprint
  eval script'leri.
- **Problar** (`probes/`): P1 öz-model probu. Sosyal katman **kapalı**.
- **Replay** (`replay/`): `.npz` kayıt ve ayrı süreçte izleme.

## Sprint yolculuğu

Ayrıntılar ve tüm tablolar: **[`FINDINGS.md`](FINDINGS.md)**. Aşağıda kısa
anlatı var.

### S0: Dünya, determinizm, replay ✓
3.000 turda her 250 turda bir hash karşılaştırması yapıldı, hepsi bit-eş
çıktı. İki ayrı süreçte koşulan 10.000 turluk kayıtlar aynı final hash'i
verdi. Hız yaklaşık 36.400 tur/sn.

### S1: Tek ajan, kanal kapalı ✓
5/5 seed'de ajan rastgele politikadan uzun yaşadı (p<2e-4, Cliff's δ
0.87–1.0). **Ama üstünlüğün kaynağı hasat değil, enerji tasarrufuydu.** v1
koşumu başarısızdı: MPC kendi eğitim verisini yanlılaştırıyordu. Başarısız
koşumun verisi silinmedi.

### S2: P1 öz-model probu → **NEGATİF**
Kümülatif yer değiştirme gizli durumdan okunamıyor. Eğitilmiş ağın rastgele
ikizden farkı tutarsız. Öz-enerji probu yüksek R² verdi ama ikiz de 0.96
civarındaydı. Bu yüzden **aday gözlem** olarak etiketlendi.

### S2.5 – S2.9: "Neden hasat etmiyor?" teşhis zinciri
Her katman kazıldı ve darboğaz her seferinde bir alt katmana kaydı:

| Sprint | Hipotez | Sonuç |
|---|---|---|
| S2.5 | Ufuk, metabolizma, müfredat, planlayıcı | Dört müdahalenin hepsinde hasat 0. **Kök neden:** on-policy veri ve MPC döngüsü, eylem-koşullu karşı-olgusal kalibrasyonu sürdüremiyor. |
| S2.6 | Ekonomi | Oracle gösterdi ki **hasat her koşulda net zararmış.** Ekonomi v2'ye geçildi (m=0.6, 24 kaynak, A=45). PER seed çöküşünü bitirdi. Asıl darboğaz **keşifti**: 45K turda yalnızca 10 hasat olayı. |
| S2.7 | Yuva müfredatı | Model olumsallığı 50 deneyimle öğreniyor (N*=50), ama davranış hasada dönmüyor. **Çatal B2: bilgi var, kullanım yok.** |
| S2.8 | Planlayıcı (CEM, makrolar) | Nakit testi %25/%13 ile geçemedi. **Asıl neden:** model hareket altında egosantrik kaymayı öğrenmemiş, "grid kalıcıdır" diye tahmin ediyor. |
| S2.9 | Hareketten zengin veri | Kayma oranı 0.09'dan yalnızca 0.16'ya çıktı. Sorun verinin miktarı değil, **örneklem karmaşıklığı**. |
| S2.10 | Yerellik iskelesi (evrişimli decoder, K-113; M-19 doğum günü testinden geçti) | **Kayma 5/5 seed'de çözüldü.** Nakit d1 %74 ✓, d2 %57 ✗. Seed 3 tarihte ilk kez hasat etti (medyan 4.0). |

### S2.10-ek: PL-13, Ali'nin öngörüsü (n=1, seed 3)
*"Öz-konum eğrisi hasatla birlikte yükselir."*
- **Üretici katmanda desteklendi:** kayma yetisi monoton yükseldi, hasat
  ancak bu yeti yaklaşık 0.75'i geçtikten **sonra** doğdu.
- **Korelasyonel katmanda desteklenmedi:** kümülatif yer değiştirme probu
  yükselmedi. Tek adımlık öz-hareket, kümülatif yol entegrasyonu demek değil.
- **Öz-enerji adayı düştü:** varyans-eşleşmiş kontrolde, kendilikle ilgisi
  olmayan bir girdi de en az aynı ölçüde iyileşti. Bu, genel bir girdi
  iyileştirmesi.

### S3: Nüfus, kanal açık, ölüm gerçek
- **İlk nefes koşumu (20K tur):** drift-baskın çöküş. Medyan ömür 52 tur,
  bu da "her tur hareket" tavanına denk geliyor. Öğrenme ufkuyla arada
  yaklaşık **865× açık** var. Seçilimsiz mutasyon mirası 65. nesilde
  gürültüye gömüyor.
- **Enstrüman hatası yakalandı (PL-23):** "Sinyaller söndü" iddiası
  **çürütüldü.** Sayaçlar ölümde sıfırlanıyordu. Gerçek sinyal oranı 0.68
  ve yükseliyor. Bu oran bir iletişim basıncını değil, **planlayıcı
  tutarlılığının kaybını** ölçüyor. Sembol entropisi 3.99/4.00 bit, yani
  kanal yapı taşımıyor. Sosyal katman için gürültü tabanı **0.0103 bit**
  olarak ön-kayda geçti.
- **S3-B, B koordinasyonu: ÇATAL C.** Mükemmel konvansiyon hediye
  edildiğinde bile kanal **zarar veriyor**: kanalsız `vision` 0.652 açılış
  verirken `signal` 0.0 verdi. Yönsüz 4 bit "nerede" bilgisini taşıyamıyor.
  Sorun doz değil, görev ile kanalın uyumsuzluğu.
- **S3-C, alarm çağrısı görevi: ÇATAL A ✓.** Ali kararıyla görev uzamsal
  olmaktan çıkarıldı. Küresel bir olay sırasında güvenli olan tek bir eylem
  (kutup) var. Kutup 2 bitlik bir kod, her ajan olay başına yalnızca
  **1 bit** görüyor. Ön-kayıtlı üç çıtanın üçü de geçti:

  | çıta | değer | eşik |
  |---|---|---|
  | Değer (`god`/`deaf`) | **1.96** | ≥ 1.5 |
  | Kanal gerekli | **0.241** | ≤ 0.6 |
  | Kanal yeterli | **0.709** | ≥ 0.5 |

  Kanal yardımcı bir yol değil, **bilginin tek yolu.** Menzil küresel
  (PL-28). İpucu tehlike kanalına özel algı olarak yazıldı ve çekirdeğe
  **0 bit** eklendi (PL-27).

## Şu an nerede duruyoruz

**Sıradaki adım:** S3-C'yi öğrenen ajanlarla koşmak. Bunun için önce bir
blokajın kalkması gerekiyor:

> **PL-22, ekoloji çerçeve kararı (Ali'de).** Ömür 52 turken hiçbir şey
> öğrenilemez. Seçenekler:
> - (a) seçilimli halefiyet (gerçek evrim)
> - (b) gelişim koruması veya yuva dönemi
> - (c) 5× seed-3 klon tabanı
>
> Tavsiye: önce (c) ve (b), sonra (a). Her biri nüfus için ayrı bir
> fizibilite oracle'ı ister (M-21).

Açık döngüler ve bekleyen kararlar: [`OPEN_LOOPS.md`](OPEN_LOOPS.md).

## Bulgu tablosu

| Bulgu | Etiket |
|---|---|
| Ajan rastgele politikadan uzun yaşar (S1) | Sağlam, ama mekanizma tasarruf |
| Kümülatif yol entegrasyonu (P1 disp) | **Negatif**, spawn ve λ ablasyonlarına dayanıklı |
| Tek-adım öz-hareket (kayma) yerellik iskelesiyle öğrenilir | Üretici enstrümanda 5/5 seed |
| Hasat, kayma yetisinden sonra doğar | **Aday gözlem** (n=1) |
| Öz-enerji temsili | **Düştü**, genel girdi iyileştirmesi |
| "Sinyal maliyet baskısıyla söner" | **Çürütüldü**, enstrüman artefaktı |
| B koordinasyonu keşfedilebilir mi | **Hayır** (Çatal C) |
| Alarm çağrısı görevi geçerli bir dil tuzağı mı | **Evet** (Çatal A, oracle düzeyinde) |

## Repo haritası

```
world/        dünya fiziği (grid, events, config — economy v1/v2/v3)
agent/        tahmin çekirdeği, homeostaz, MPC, kanal
population/   roster + yaşam döngüsü (ölüm, miras, mutasyon)
training/     öğrenme döngüsü (loop.py), PER, ekoloji koşturucu (ecology.py),
              oracle'lar (oracle, b_oracle, event_oracle, pop_oracle),
              olay okulu (event_school), topluluk ajanı (ensemble_agent),
              gözlemci problar (analyze_s3e, precursor_probe,
              signal_curse_probe), sprint eval script'leri
agent/ensemble.py  Program A1 model topluluğu (K-115 aday)
probes/       P1 öz-model probu (sosyal katman kapalı)
replay/       .npz kayıt + izleyici
tests/        determinizm, fizik, enstrüman (M-23 bilinen-pozitif) testleri
runs/         TÜM ham sonuçlar, snapshot'lar, ağırlıklar
              s3d (nüfus oracle) · s3e…s3r (S3 ekoloji merdiveni) · s3j
              (olay okulu) · s3q (Program B) · a0/a1 (Program A) · c1
              (Program C) — her klasörde breath.json/summary.json
FINDINGS.md       sprint sonu bulgular (negatifler dahil) + Beş Kapı şablonu
OPEN_LOOPS.md     PL-xx açık işler / bekleyen kararlar
KERNEL_BUDGET.md  ajana verilen her prior, bit cinsinden
METODOLOJI.md     M-xx dersleri
K104_DOSYA.md     merak terimi (K-104) karar dosyası
PETRI_TALIMAT.md  kaynak doküman (çelişkide bu kazanır)
CLAUDE.md         oturum anayasası
```

## Veriler (`runs/`)

| Dosya / klasör | İçerik |
|---|---|
| `s1_results.json`, `s1_results_v1_failed.json` | S1 hayatta kalma (başarılı v2 + başarısız v1) |
| `s2_*_p1_results.json`, `s2*_snapshots/` | S2 P1 probu ve varyantları (λ=1, spawn-rand, PL-15 kör/normal), dondurulmuş temsiller (.npz) |
| `s25_step{1..4}.json` | S2.5 merdiven adımları |
| `s26_*.json` | ekonomi oracle'ı, A-enerji süpürmesi, PER koşumu |
| `s27_*.json` | görünür-A oracle'ı, calibN, yuva müfredatı |
| `s28_*.json` | rollout çürüme eğrisi, CEM sonuçları |
| `s29_*.json` | taban oranlar, K-110rev sonuçları |
| `s210_*.json`, `s210_weights/` | M-19 doğum günü testi, kayma zinciri, karşı-olgusal çürüme; seed 1-3 ağırlıkları (`.pt`) |
| `s210ek_*`, `s210ek_snapshots/` | PL-13 ortak zaman ekseni (seed 3) |
| `s3_breath/`, `s3_breath_v2/` | ekoloji koşumları (v1 bozuk enstrüman, v2 düzeltilmiş) |
| `s3_b_*.json` | B koordinasyon oracle'ı, keşfedilebilirlik, kalibrasyon |
| `s3c_event_oracle.json` | S3-C alarm çağrısı oracle'ı |

## Çalıştırma

```bash
uv venv --python 3.13 .venv            # ya da: python3.13 -m venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m pytest tests/ -q   # ~90 sn; determinizm + fizik + enstrüman

# Ekoloji (S3 varsayılanları: klon kadro, yuva, σ=0.002, olay her 10 tur):
.venv/bin/python -m training.ecology --turns 20000 --out runs/deneme \
  --founding clone --nest 600 0.5 --sigma 0.002 --events \
  --event-every 10 --event-lead 4 --event-share 0.5 --channel open
# Kollar: --channel mute|hear|speak, --selection max_age, --signal-frac,
# --eps-quiet, --ensemble K BETA, --min-safe N, --founding weights:<pt>
.venv/bin/python -m training.analyze_s3e --dir runs/deneme     # özet + MI
.venv/bin/python -m training.event_school --turns 100000 --seed 0 --out runs/okul
.venv/bin/python -m training.precursor_probe --weights runs/deneme/final_weights.pt
.venv/bin/python -m replay.viewer record out.npz --turns 2000
```

Ölçümler Python 3.13, NumPy 2.4.2, Torch 2.13 (tek thread, bit-eş eğitim),
Apple Silicon üzerinde alındı. 5 ajanlı ekoloji ≈ 60-80 ms/tur; 100K tur
≈ 2 saat. `runs/` 414 MB (S2 snapshot'ları ve eski ağırlık dosyaları
dahil; yeni `final_weights.pt` dosyaları git dışıdır).

## Metodoloji dersleri

Her sprint "Yeni ders var mı?" sorusuyla kapanır. Tam liste:
[`METODOLOJI.md`](METODOLOJI.md). Öne çıkanlar:

- **M-14:** Müdahale seçmeden önce, hedef deneyimin taban oranını say.
- **M-15:** Sonda da bir cihazdır. Bilinen bir pozitifte doğrulanmadan ön-kayıt kriteri yapılmaz.
- **M-17:** Cihaz, kullanıldığı dağılımda koşmalı.
- **M-20:** Taban çizgisi de cihazın parçasıdır.
- **M-21:** Rejim transferi ölçülür, varsayılmaz.
- **M-22:** Fizibilite iki ayrı sorudur: değerli mi, ve bulunabilir mi.
- **M-23:** Sayaç da bir cihazdır.
- **M-24:** Paydası tedaviden etkilenen oran yanıltır.
- **M-25:** Tuzak kurmadan önce kaçış yollarını say.
