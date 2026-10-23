"""Ders kitabı alıntı denetimi ($0): `> "alıntı" (dosya.md)` her alıntı kaynak klasöründeki dosyada birebir alt dize olmalı.
python tools/okul/alinti_denetle.py <kitap.md> <kaynak-klasörü>   çıkış 0 hepsi doğru · 3 uyumsuz var"""
import re, sys
from pathlib import Path

kitap, kaynak = Path(sys.argv[1]), Path(sys.argv[2])
n = lambda s: re.sub(r"\s+", " ", s).strip().lower()
metin = {p.name: n(p.read_text(encoding="utf-8")) for p in kaynak.glob("*.md")}
bul = re.findall(r'> "(.+?)" \(([\w.\-]+\.md)\)', kitap.read_text(encoding="utf-8"))
kotu = [(a, d) for a, d in bul if d not in metin or n(a) not in metin[d]]
print(f"{len(bul)} alıntı, {len(kotu)} uyumsuz")
for a, d in kotu:
    print(f"  YOK [{d}]: {a[:90]}")
sys.exit(3 if kotu or not bul else 0)
