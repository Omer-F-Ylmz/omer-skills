"""ANİMASYON-1: html tarifini tek komutta kopyala + AYAR'ı değiştir + ölç (ajan turu: 1).
    python uyarla.py <tarif.html> <hedef.html> '<ayar json>'
AYAR json'u tarifin AYAR bloğuyla derin birleşir (sözlükler birleşir, liste/değer yerine geçer); <title> = metin.baslik.
Çıktı: olc.py'nin tek satır JSON'u (kareler <hedef>-kare/).
"""
import html
import json
import re
import sys
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
BLOK = re.compile(r"(const AYAR = )(\{.*?\n\});", re.S)


def oku(metin):
    return json.loads(BLOK.search(metin).group(2))


def birlestir(taban, ek):
    for k, v in ek.items():
        taban[k] = birlestir(taban[k], v) if isinstance(v, dict) and isinstance(taban.get(k), dict) else v
    return taban


def uyarla(tarif, hedef, ek):
    metin = (DIZIN / "tarifler" / tarif).read_text(encoding="utf-8")
    ayar = birlestir(oku(metin), ek)
    blok = json.dumps(ayar, ensure_ascii=False, indent=2).replace("</", "<\\/")
    metin = BLOK.sub(lambda m: m.group(1) + blok + ";", metin, count=1)
    baslik = html.escape(ayar.get("metin", {}).get("baslik", ""))
    if baslik:
        metin = re.sub(r"<title>.*?</title>", lambda m: f"<title>{baslik}</title>", metin, count=1)
    Path(hedef).write_text(metin, encoding="utf-8")
    return ayar


if __name__ == "__main__":
    tarif, hedef = sys.argv[1], sys.argv[2]
    uyarla(tarif, hedef, json.loads(sys.argv[3]) if len(sys.argv) > 3 else {})
    sys.path.insert(0, str(DIZIN))
    import olc
    print(json.dumps(olc.olc(hedef, Path(hedef).with_suffix("").as_posix() + "-kare"), ensure_ascii=False))
