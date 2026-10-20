"""Bekçi: belgelerde bugünden ileri tarih olamaz (2026-10-20 tarih kayması vakası)."""
import datetime
import pathlib
import re

DOCS = ["FINDINGS.md", "OPEN_LOOPS.md", "README.md", "CLAUDE.md",
        "METODOLOJI.md", "KERNEL_BUDGET.md"]
ROOT = pathlib.Path(__file__).resolve().parent.parent
AYLAR = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6,
         "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}


def test_no_future_dates_in_docs():
    today = datetime.date.today()
    bad = []
    for name in DOCS:
        text = (ROOT / name).read_text()
        for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", text):
            try:
                d = datetime.date(*map(int, m.groups()))
            except ValueError:
                continue
            if d > today:
                bad.append(f"{name}: {m.group(0)}")
        for m in re.finditer(r"\b(\d{1,2})(?:-\d{1,2})? (" + "|".join(AYLAR) + r")\b", text):
            day, month = int(m.group(1)), AYLAR[m.group(2)]
            try:
                d = datetime.date(today.year, month, day)
            except ValueError:
                continue
            if d > today and (d - today).days < 60:
                bad.append(f"{name}: {m.group(0)}")
    assert not bad, "gelecek tarihli kayıt: " + ", ".join(bad[:10])
