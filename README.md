<div align="center">

# 🧫 PETRI

**Emergent zihin öncülleri deneyi**

*Bilinç üretmiyoruz. Bilincin öncüllerinin hangi ekolojik basınç altında
kendiliğinden belirdiğini yakalayan bir tuzak kuruyoruz.*

[![Kod lisansı: MIT](https://img.shields.io/badge/kod-MIT-blue.svg)](LICENSE)
[![Doküman ve veri: CC BY 4.0](https://img.shields.io/badge/dok%C3%BCman%20%2B%20veri-CC%20BY%204.0-lightgrey.svg)](LICENSE-DOCS-DATA.md)
[![Python 3.13](https://img.shields.io/badge/python-3.13-informational.svg)](requirements.txt)
[![Ön-kayıtlı](https://img.shields.io/badge/her%20ko%C5%9Fum-%C3%B6n--kay%C4%B1tl%C4%B1-success.svg)](FINDINGS.md)

[Sonuç](#-sonuç) · [Nasıl çalışır](#-nasıl-çalışır) · [Okuma rehberi](#-okuma-rehberi) · [Çalıştırma](#-çalıştırma) · [English summary](#-english-summary)

</div>

---

## 📌 Sonuç

> **H4 negatif.** Beş ölümlü, öngörücü ajanın yaşadığı bir dünyada, 4 bitlik
> maliyetli ve kimliksiz bir kanaldan anlam taşıyan bir iletişim
> **kendiliğinden doğmadı.** Yaklaşık 320 koşum, 600 bin tura kadar süren
> ekolojiler, ajana verilen **0 kalıcı yeni bit.**

Asıl katkı, olumsuzluğun **nedenini ölçmek** oldu:

| Soru | Cevap |
|---|---|
| Ajanlar görevi öğrenebiliyor mu? | ✅ Evet, kendi ipuçlarını öğrenip tavana ulaşıyorlar. |
| Kanal kullanılabilir durumda mı? | ✅ Evet, mekanik engeller kaldırıldı, kanal nötr ve doğru fiyatlı. |
| Kanalda alıcıya ulaşabilecek bilgi var mı? | ✅ Evet, optimal bir alıcı kazanç sağlardı. |
| Bir ajan başkasını dinlemeyi öğrenebilir mi? | ✅ Evet, net konuşan komşularla okulda öğreniyor. |
| Peki ekolojide neden dil yok? | ❌ Dinleyici için gönderici netliği **≈0.18 bit** olmalı. Göndericiler **0.05 ile 0.10 bitte** kilitli. Dinleyen yok, netleşmenin faydası yok. |

Bu **"sessiz denge"** uzun zamana, grup seçilimine, uyarı süresi
kalibrasyonuna ve dışarıdan eğitilmiş dinleyicilerle tohumlamaya karşı
kararlı kaldı.

📄 **Tam hikâye:** [`RAPOR_S3_DIL.md`](RAPOR_S3_DIL.md), 15 dakikalık okuma.

---

## 🧪 Nasıl çalışır

Kıt kaynaklı, deterministik fizikli 64×64 bir torus dünyada 5 ajan yaşar.
Her ajan yalnızca üç şeyden oluşur:

```
  DÜNYA (kaynak, tehlike, küresel olaylar)
    │ gözlem                         ▲ eylem
    ▼                                │
  ┌──────────────── AJAN ──────────────────┐
  │  Tahmin makinesi ──▶ Planlayıcı (MPC)  │
  │  (GRU + decoder)       ▲     │         │
  │        ▲               │     │ sinyal  │
  │        │      Homeostaz│     │ (bedeli │
  │        │    (enerji,   │     │  var)   │
  │        │     ölüm)─────┘     ▼         │
  └────────┼─────────────────────┼─────────┘
           └──── KANAL ◀─────────┘
        (16 sembol, kimliksiz, küresel)
```

**Verilmeyenler:** dil, konvansiyon, duygu, ödül. Tek içsel sinyal tahmin
hatası ve hayatta kalmaktır.

**Dil tuzağı (alarm çağrısı):** Her 10 turda bir küresel tehlike gelir.
Güvenli tek eylem 4 kutuptan biridir. Tehlikeden önce her ajan kutup
kodunun **yalnız 1 bitini** görür. Bilgi tek bir ajanda tamamlanmaz;
kanal onu tamamlamanın tek yoludur. Doğadaki emsali alarm çağrılarıdır.

### Anayasa

1. **Çekirdek minimalizmi.** Ajana giren her ön bilgi bit cinsinden
   [`KERNEL_BUDGET.md`](KERNEL_BUDGET.md)'ye gerekçesiyle yazılır.
2. **Fizik hakemdir.** Ödül şekillendirme yasak.
3. **Dil verilmez, basınç verilir.** Kanalın yalnız genişliği ve maliyeti tanımlı.
4. **Duygu verilmez.** Duyguya benzer durumlar problarla aranır.
5. **Davranış yalan söyler.** İddialar iç temsil problarıyla desteklenir.
6. **Dil modeli deneyin içinde yer alamaz.** Yalnız gözlemci olabilir.
7. **Negatif sonuç sonuçtur.**

Tam metin: [`PETRI_TALIMAT.md`](PETRI_TALIMAT.md).

---

## 🎯 Hipotezler

| | Hipotez | Hüküm |
|---|---|---|
| **H1** | Ölümlü ve eyleyen tahmin makinesi öz-model geliştirir | 🟡 Karışık. Kümülatif yol entegrasyonu yok. Tek-adım öz-hareket yerellik iskelesiyle öğreniliyor. |
| **H2** | Opaklık ve koordinasyon karşılıklı modellemeyi doğurur | ⚪ Test edilmedi. Ön koşulu olan iletişim doğmadı. |
| **H3** | Kısıtlı kanal sinyalin içselleştirilmesini zorlar | ⚪ Ön koşul negatif. İçselleştirilecek sinyal kullanımı yok. |
| **H4** | Asimetrik bilgi ve kanal kıtlığı proto-gramer doğurur | 🔴 **Negatif** (bu anayasa altında) |
| **H0** | Her şey reaktif hesaplamayla açıklanır | Çürütülmedi |

Her pozitif iddia önce H0'a karşı savunulur ve [`FINDINGS.md`](FINDINGS.md)'deki
**Beş Kapı**'dan geçer: ablasyon, prob sızıntısı, zaman çizgisi, çekirdek
bütçesi, bit-eş tekrar. Bir kapı boşsa bulgu yalnız "aday gözlem"dir.

---

## 🗺️ Yolculuk

<details>
<summary><b>S0 ile S2.10: dünya, tek ajan, öz-model probu</b> (açmak için tıkla)</summary>

| Sprint | Soru | Sonuç |
|---|---|---|
| S0 | Dünya deterministik mi? | ✅ Bit-eş tekrar, ~36 bin tur/sn |
| S1 | Ajan rastgeleden uzun yaşar mı? | ✅ 5/5 seed, ama mekanizma hasat değil enerji tasarrufu |
| S2 | İç temsilde öz-konum var mı? | 🔴 Kümülatif yer değiştirme okunamıyor |
| S2.5 ile S2.9 | Ajan neden hasat etmiyor? | Darboğaz katman katman indi: ekonomi, keşif, planlayıcı, egosantrik kayma |
| S2.10 | Yerellik iskelesi işe yarar mı? | ✅ Kayma 5/5 seed'de çözüldü, ilk hasat doğdu |
| S2.10-ek | Öz-konum hasatla birlikte mi yükselir? | Üretici katmanda evet (n=1), korelasyonel katmanda hayır |

</details>

<details>
<summary><b>S3: nüfus, açık kanal, gerçek ölüm, dil tuzağı</b> (açmak için tıkla)</summary>

| Aşama | Soru | Sonuç |
|---|---|---|
| S3-B | Kanal "nerede" bilgisi taşır mı? | 🔴 Yönsüz 4 bit taşıyamıyor, görev değiştirildi |
| S3-C | Alarm çağrısı geçerli bir tuzak mı? | ✅ Ön-kayıtlı üç fizibilite çıtası geçti |
| S3-D ile S3-K | Öğrenen ekolojide dil doğar mı? | 🔴 Ajanlar ipucunu öğreniyor, kanal 0 bilgi taşıyor |
| S3-L ile S3-P | Kanal neden öğrenmeyi yavaşlatıyor? | Planlayıcı kendi sinyaline sahte prim öğreniyor |
| Program B | Önce yetkinlik, sonra kanal? | Yetkin ajan sinyali fiyatlıyor, dil yok |
| Program A | Sahte primin kaynağı ne? | Halefte deneyim tamponu sıfırlanıyordu. Düzeldi, kanal nötr |
| Program C | Göndericiye doğrudan fayda? | "Birlikte açılan sığınak" basınç üretmedi |
| Program A′/A″ | Grup seçilimi kırar mı? | 🔴 Konuşma kararı ipucuna bağlandı (0.10 bit) ama çoğu refleks, dinleyen yok |
| PL-37 | Dinleyici öğrenebilir mi? | ✅ Okulda evet. Eşik ≈0.18 bit |
| PL-38 | Zaman göndericiyi eşiğe taşır mı? | 🔴 500 bin turda kilitli |
| PL-39 | Dinleme bir kez kurulursa yaşar mı? | 🔴 ~20 bin turda söndü |

Ayrıntı: [`RAPOR_S3_DIL.md`](RAPOR_S3_DIL.md).

</details>

---

## 📚 Okuma rehberi

| Süre | Ne okunur |
|---|---|
| ⏱️ 5 dk | Bu sayfa |
| ⏱️ 15 dk | [`RAPOR_S3_DIL.md`](RAPOR_S3_DIL.md): dil kolunun bütüncül raporu |
| ⏱️ 30 dk | [`METODOLOJI.md`](METODOLOJI.md): kendimizi kandırmamak için 31 ders |
| 🔬 Derin | [`FINDINGS.md`](FINDINGS.md): her koşumun ön-kaydı, sonucu ve öngörü karnesi |
| 🧾 Denetim | [`KERNEL_BUDGET.md`](KERNEL_BUDGET.md): ajana giden her bit · [`OPEN_LOOPS.md`](OPEN_LOOPS.md): her karar |

---

## 🚀 Çalıştırma

```bash
git clone https://github.com/alibeydilidev/petri.git && cd petri
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest tests/ -q
```

Testler yaklaşık 2 dakika sürer. Determinizm, fizik ve ölçüm aletlerini
doğrular.

**Bir ekoloji koşmak:**

```bash
.venv/bin/python -m training.ecology --turns 20000 --out runs/deneme --founding clone --nest 600 0.5 --sigma 0.002 --events --event-every 10 --event-lead 4 --min-safe 2 --channel open
```

**Gönderici netliğini ölçmek:**

```bash
.venv/bin/python -m training.sender_clarity runs/deneme
```

**Diğer araçlar:**

| Komut | Ne yapar |
|---|---|
| `training.event_school` | Tek ajanlık olay okulu (sanal komşularla dinleyici eğitimi dahil) |
| `training.island_evolution` | Ada modeli grup seçilimi |
| `training.channel_oracle` | Kanalın optimal alıcı tavanı |
| `training.analyze_s3e` | Ekoloji özeti ve karşılıklı bilgi |
| `replay.viewer` | Koşum kaydı ve izleme |

Tüm koşumlar deterministiktir: aynı dünya ve ajan seed'i bit-eş sonuç verir.
5 ajanlı ekoloji Apple Silicon'da tur başına 60 ile 80 ms sürer, 100 bin
tur yaklaşık 2 saattir.

---

## 🗂️ Repo haritası

```
world/        dünya fiziği: grid, küresel olaylar, ekonomi sürümleri
agent/        tahmin çekirdeği, homeostaz, planlayıcı, kanal
population/   kurucu kadro, yaşam döngüsü, ölüm, miras, mutasyon
training/     ekoloji koşturucu, okul, oracle'lar, ada evrimi, problar
probes/       öz-model probu
replay/       kayıt ve izleyici
tests/        determinizm, fizik ve ölçüm aleti testleri
runs/         tüm ham sonuçlar (breath.json, school.json, loglar)
```

| Doküman | İçerik |
|---|---|
| [`RAPOR_S3_DIL.md`](RAPOR_S3_DIL.md) | Dil kolunun kapanış raporu |
| [`FINDINGS.md`](FINDINGS.md) | Sprint günlüğü: ön-kayıtlar, sonuçlar, Beş Kapı şablonu |
| [`METODOLOJI.md`](METODOLOJI.md) | M-01 ile M-31 arası dersler |
| [`KERNEL_BUDGET.md`](KERNEL_BUDGET.md) | Ajana verilen her ön bilgi, bit cinsinden |
| [`OPEN_LOOPS.md`](OPEN_LOOPS.md) | Açık işler ve kararlar |
| [`PETRI_TALIMAT.md`](PETRI_TALIMAT.md) | Kaynak doküman, çelişkide bu kazanır |
| [`CLAUDE.md`](CLAUDE.md) | Yürütücü yapay zekâ için oturum anayasası |
| [`K104_DOSYA.md`](K104_DOSYA.md) | Merak terimi kararı (arşiv) |

**Veri:** her tablo `runs/` altındaki ham dosyalardan türetilir. Klasör
adları programları izler: `s3e` ile `s3r` S3 merdiveni, `a0` ile `a3`
Program A, `c1` ile `c4` Program C, `ev` ada evrimi, `rs` dinleyici okulu,
`pl38` ve `pl39` son programlar. Ağırlık dosyalarının bir kısmı repoda,
yenileri yerelde tutuldu.

---

## 💡 Öne çıkan dersler

Her sprint "Yeni ders var mı?" sorusuyla kapandı. Seçmeler:

- **M-07** Pozitif kontrol olmadan negatif yorumlanamaz.
- **M-08** Öngörüler önceden kayda girer.
- **M-15** Sonda da bir cihazdır.
- **M-23** Sayaç da bir cihazdır.
- **M-26** Sürüklenme cihaz hatası gibi davranır.
- **M-27** Ekolojiyi yargılamadan önce tek-ajan tavanını ölç.
- **M-28** Tuzağın geri dönüş yolunu kur, ama önce giriş ücretini ölç.
- **M-31** Halefiyet, öğrenme mekaniğinin her parçası için ayrı bir karardır.

---

## 🔭 Buradan devam etmek isteyenlere

Bu sonuç "dil imkânsız" demiyor. Bu anayasa ve bu ölçekte sıfır bitten
kendiliğinden dil doğmadığını ve nedenini söylüyor. Umutlu yollar:

- **İki taraflı tohum:** dinleyici ve net gönderici birlikte verilirse iletişim yaşar mı? (~2 bit)
- **Kimlikli ya da yerel kanal:** alıcı kimin konuştuğunu bilirse ne olur?
- **Akrabalık ya da tekrarlanan eşler:** göndericinin faydası soy üzerinden döner.
- **Daha büyük ölçek:** daha çok ajan, daha çok ada, milyonlarca tur.
- **Farklı öğrenici:** model-free ya da keşif terimli ajanlar.

Ayrıntı ve maliyetler raporun 9. bölümünde.

---

## 🤝 Bu çalışma nasıl yürütüldü

Hipotezler, anayasa ve mimari plan **Ali Beydili**'ye aittir. Kodun büyük
bölümü, tüm koşumlar, ön-kayıtlar, analizler ve bulgu metinleri, Ali'nin
verdiği karar yetkisiyle **Claude (Anthropic)** tarafından yürütüldü ve
yazıldı. Ali karar noktalarında yön verdi (`OPEN_LOOPS.md` "KARAR"
satırları).

Bu bilinçli bir seçimdir: deneyin iddiası "ajana hiçbir şey vermeden"
ise, deneyi yürüten elin de şeffaf olması gerekir. Her koşum, koşumdan
önce yazılmış ön-kayıt ve çıtalarla gelir. Git commit zamanı yetkili zaman
damgasıdır. Tutmayan öngörüler dahil her şey kayıttadır. Yanılgılar
silinmez, şerh düşülür.

---

## 🌐 English summary

**PETRI** is a pre-registered artificial-life experiment asking whether
precursors of consciousness (self-model, mutual modelling, compositional
communication) emerge spontaneously in mortal predictive agents. Nothing
is given to the agents: no reward shaping, no language, no emotions.
Every prior is counted in bits.

**Main result (S3, hypothesis H4): negative.** Five mortal agents with a
GRU world model and a model-based planner share a costly 16-symbol,
identity-free broadcast channel. An "alarm call" task splits a 2-bit
safe-pole code so that each agent sees only 1 bit. Across ~320 runs and
ecologies of up to 600K turns, no meaningful communication emerged, with
zero permanent bits added.

We measured why. Agents learn their own cue. The channel is neutral and
correctly priced. Information is available to an optimal receiver. A single
agent *can* learn to listen to clear senders. But listener learning
requires ≈0.18 bits of sender clarity, while ecological senders stay locked
at 0.05 to 0.10 bits. Without listeners, sharper signalling pays nothing.
This "silent equilibrium" proved stable against long runs, island-model
group selection, warning-lead calibration, and seeding with pre-trained
listeners.

Documentation is in Turkish. Start with
[`RAPOR_S3_DIL.md`](RAPOR_S3_DIL.md) (closure report) and
[`METODOLOJI.md`](METODOLOJI.md) (31 methodological lessons). Code: MIT.
Docs and data: CC BY 4.0. The experiment was designed by Ali Beydili and
executed autonomously by Claude (Anthropic) under his decision authority.

---

<div align="center">

**Atıf:** [`CITATION.cff`](CITATION.cff) · **Lisans:** kod [MIT](LICENSE), doküman ve veri [CC BY 4.0](LICENSE-DOCS-DATA.md)

*Negatif sonuç da sonuçtur.*

</div>
