"""komut "belirsiz" olan kartın komutunu kaynaktaki birebir satırdan doldurur (model yok; ★ 20 Eki 13:15 d3)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ogren1"))
from ozet3 import bos  # noqa: E402

# sıra: skill/ajan frontmatter adı · MCP kaydı command · MCP http url · CLI --help kullanım satırı · eklenti/paket adı
KALIP = [r"^name:[ \t]*\S.*$", r'^\s*"command"\s*:.*$', r'^\s*"url"\s*:.*$', r"^\s*usage:.*$", r'^\s*"name"\s*:.*$']


def doldur(r, m):
    """r["komut"] boşsa/belirsizse m'deki ilk eşleşen satır komut + alıntı olur; bulunmazsa dokunmaz"""
    if not bos(r["komut"]):
        return r
    for k in KALIP:
        s = re.search(k, m, re.M | re.I)
        if s:
            satir = s.group(0).strip()
            sonra = m[s.end():].strip().split("\n", 1)[0].strip()
            r["komut"] = satir
            r.setdefault("alinti", {})["komut"] = satir if len(satir) >= 12 else f"{satir}\n{sonra}"  # sert: alıntı ≥10 kr
            break
    return r
