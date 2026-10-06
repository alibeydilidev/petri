"""Asimetrik olay enjeksiyonu (PL-05'te ertelenmişti; S3-C'de açıldı).

**Neden bu tasarım (PL-25 ÇATAL C'nin sonucu):** ölçüldü ki yönsüz,
kimliksiz 4-bitlik kanal UZAMSAL bir randevu görevine hiçbir şey
katmıyor — mükemmel konvansiyon hediye edilse bile (FINDINGS S3-B).
Kanal "nerede" taşıyamaz; "ne" taşıyabilir. Ali kararı (A): görevi,
koordinasyonun zor kısmı uzamsal OLMAYACAK şekilde değiştir.

**Ekolojik emsal:** alarm çağrısı. Vervet maymununda sembol "yırtıcı
nerede" değil "hangi kaçış eylemi" der — kategorik, uzamsal değil.

**Fizik (ödül DEĞİL — yalnız enerji ve homeostaz):**
  - `event_every` turda bir olay zamanlanır, `event_lead` tur sonra
    `event_duration` tur boyunca aktif olur.
  - Olayın bir KUTBU var: p ∈ {0..K-1}, K=`event_polarities`.
    O turda GÜVENLİ tek eylem `p`'dir; başka her eylem
    `event_penalty` enerji yakar.
  - Olay KÜRESELDİR: ceza konuma bakmaz. Kaçacak "yer" yoktur,
    yalnız yapılacak DOĞRU EYLEM vardır.

**İki tasarım kilidi — kanalın GEREKLİ olması için:**

1. **Olay, acıdan öğrenmeye vakit bırakmaz.** `event_duration=1`
   varsayılan. Uzun olayda ajan ilk turda cezalanıp kalan turlarda
   düzeltir; o zaman deneyim iletişimin yerini alır ve tuzak boşa
   düşer. (Bu, tasarım sırasında yakalandı: 3 turluk olayda
   kendi-kendine-çıkarım değerin ~%67'sini kurtarıyordu.)

2. **Bilgi TEK ajanda tamamlanmaz** (`event_visibility_split`,
   spec 3.x'in "her ajana olayın farklı parçası" maddesi). Kutup
   `cue_bits = log2(K)` bitlik bir koddur; her ajan olay başına
   YALNIZ BİR biti gözler (hangi biti gözleyeceği her olayda dünya
   rng'sinden çekilir — sabit rol değil). Kendi biti ajanı K'dan
   K/2 adaya indirir; kalanı ancak BAŞKASININ bitinden gelir.
   Yani kanal "yardımcı" değil, bilginin tek yoludur.

Semboller yine ANLAMSIZ doğar: hangi sembolün hangi biti taşıdığı
ajanların keşfetmesi gereken şeydir. Bu modül hiçbir konvansiyon
dayatmaz; yalnız konvansiyonun KARŞILIĞI OLAN dünyayı kurar.

Öncü hücrenin gözlem kodlaması S3-C'nin ayrı kararıdır (PL-27);
fizibilite oracle'ı ipuçlarını doğrudan okur — M-01: cetvel önce,
gözlem kodlaması sonra.

Determinizm: tüm rastgelelik World'ün tek generator'ından akar.
Varsayılan KAPALI (`event_every=0`) → state_dict/state_hash bit-eş.
"""

import numpy as np

N_CUE_BITS = 2          # K=4 için; cue_bits = log2(event_polarities)


class EventSystem:
    """Olay durum makinesi. Dünyanın parçasıdır (state_dict'e girer)."""

    def __init__(self, cfg, n_entities: int = 1):
        self.cfg = cfg
        self.n_entities = n_entities
        self.reset()

    @property
    def enabled(self) -> bool:
        return self.cfg.event_every > 0

    @property
    def cue_bits(self) -> int:
        return int(np.log2(self.cfg.event_polarities))

    def reset(self) -> None:
        self.polarity = -1          # -1 = zamanlanmış olay yok
        self.starts_at = 0
        self.ends_at = 0
        self.precursor = np.zeros((0, 2), dtype=np.int64)
        # Her ajanın bu olayda GÖZLEDİĞİ bit indeksi (rol sabit değil).
        self.cue_assign = np.zeros((0,), dtype=np.int64)

    # ------------------------------------------------------------------ sorgu
    def active(self, turn: int) -> bool:
        return self.polarity >= 0 and self.starts_at <= turn < self.ends_at

    def pending(self, turn: int) -> bool:
        """Öncü belirdi, olay henüz başlamadı (uyarı penceresi)."""
        return self.polarity >= 0 and turn < self.starts_at

    def safe_action(self) -> int:
        """Bu olayda güvenli olan TEK eylem."""
        return int(self.polarity)

    def cue_for(self, entity_id: int) -> tuple[int, int] | None:
        """Ajanın gözlediği (bit_indeksi, bit_değeri). Olay
        zamanlanmamışsa None. ASİMETRİNİN KAYNAĞI: ajan yalnız bir bit
        görür → K/2 aday kalır; gerisi başkasının bitindedir."""
        if self.polarity < 0 or entity_id >= len(self.cue_assign):
            return None
        b = int(self.cue_assign[entity_id])
        return b, (int(self.polarity) >> b) & 1

    # --- PL-27 seçenek (c): öncü algısı, YENİ KANAL AÇMADAN -----------
    # Ali kararı: sıfır yeni prior biti. Öncü, mevcut TEHLİKE kanalına
    # yazılır; ajan onu gerçek tehlikeden KENDİSİ ayırmak zorundadır
    # (öncü yalıtık hücrelerdir, enerji çekmez, yalnız uyarı
    # penceresinde görünür; gerçek tehlike 5x5 blok + enerji çeker).
    #
    # Algı ÖZELDİR (ajan-merkezli): spec'in "her ajana olayın farklı
    # parçası" maddesinin doğrudan karşılığı — aynı olayın farklı
    # yüzünü herkes kendi bedeninde duyar. Konum kodlaması:
    #   (0,0) işaretli → uyarı penceresi açık   (varlık göstergesi)
    #   (0,1) işaretli → gözlenen bit İNDEKSİ 1 (yoksa 0)
    #   (1,0) işaretli → gözlenen bit DEĞERİ  1 (yoksa 0)
    # Hangi hücrenin ne demek olduğu ajana SÖYLENMEZ; öğrenilecektir.
    PERCEPT_PRESENT = (0, 0)
    PERCEPT_INDEX = (0, 1)
    PERCEPT_VALUE = (1, 0)

    def percept_cells(self, entity_id: int,
                      turn: int) -> list[tuple[int, int]]:
        """Uyarı penceresinde ajanın KENDİ gözleminde yanan ajan-merkezli
        hücreler. Olay yoksa/aktifse boş."""
        if not self.enabled or not self.pending(turn):
            return []
        cue = self.cue_for(entity_id)
        if cue is None:
            return []
        b, v = cue
        cells = [self.PERCEPT_PRESENT]
        if b:
            cells.append(self.PERCEPT_INDEX)
        if v:
            cells.append(self.PERCEPT_VALUE)
        return cells

    @classmethod
    def decode_percept(cls, cells) -> tuple[int, int] | None:
        """Kodlamanın KAYIPSIZ olduğunu doğrulamak için ters çevirici
        (test/enstrüman denetimi; ajan bunu kullanmaz — öğrenecek)."""
        s = {tuple(c) for c in cells}
        if cls.PERCEPT_PRESENT not in s:
            return None
        return (1 if cls.PERCEPT_INDEX in s else 0,
                1 if cls.PERCEPT_VALUE in s else 0)

    def candidates(self, entity_id: int) -> list[int]:
        """Ajanın kendi ipucuyla daraltabildiği kutup adayları."""
        cue = self.cue_for(entity_id)
        if cue is None:
            return list(range(self.cfg.event_polarities))
        b, v = cue
        return [p for p in range(self.cfg.event_polarities)
                if (p >> b) & 1 == v]

    # ------------------------------------------------------------------ fizik
    def apply_drain(self, turn: int, actions: np.ndarray,
                    deltas: np.ndarray) -> None:
        """Aktif olayda güvenli eylemi YAPMAYAN herkesten enerji çeker.
        Konumun rolü yok — küresel olay."""
        if not self.active(turn):
            return
        deltas[np.asarray(actions) != self.safe_action()] -= \
            self.cfg.event_penalty

    def schedule(self, turn: int, rng: np.random.Generator,
                 sample_cell) -> None:
        """Süresi dolanı kapatır; sırası geleni kutup + ipucu dağılımı
        + öncü hücresiyle birlikte kurar."""
        if not self.enabled:
            return
        if self.polarity >= 0 and turn >= self.ends_at:
            self.reset()
        if self.polarity < 0 and turn % self.cfg.event_every == 0:
            self.polarity = int(rng.integers(0, self.cfg.event_polarities))
            self.starts_at = turn + self.cfg.event_lead
            self.ends_at = self.starts_at + self.cfg.event_duration
            self.precursor = sample_cell(1)
            self.cue_assign = rng.integers(0, self.cue_bits,
                                           size=self.n_entities)

    # ------------------------------------------------------------------ durum
    def state_dict(self) -> dict:
        return {"polarity": int(self.polarity),
                "starts_at": int(self.starts_at),
                "ends_at": int(self.ends_at),
                "precursor": self.precursor.tolist(),
                "cue_assign": self.cue_assign.tolist()}

    def load_state(self, s: dict) -> None:
        self.polarity = int(s["polarity"])
        self.starts_at = int(s["starts_at"])
        self.ends_at = int(s["ends_at"])
        self.precursor = np.array(s["precursor"],
                                  dtype=np.int64).reshape(-1, 2)
        self.cue_assign = np.array(s["cue_assign"], dtype=np.int64)
