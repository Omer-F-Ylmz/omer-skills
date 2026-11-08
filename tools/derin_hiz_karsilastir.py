"""DERIN-HIZ-1 kalite kapısı: eski ve yeni derin json'larda transkript benzerliği (kelime) + ekran OCR örtüşmesi. Kullanım: derin_hiz_karsilastir.py <eski_dizin> <yeni_dizin>"""
import difflib
import json
import re
import sys
from pathlib import Path


def kelimeler(j):
    return re.sub(r"[^\w\s]", "", " ".join(s["t"] for s in j["transkript"]).lower()).split()  # noktalama içerik değil


def main(eski, yeni):
    toplam = []
    for p in sorted(Path(yeni).glob("*.json")):
        e, y = json.loads((Path(eski) / p.name).read_text(encoding="utf-8")), json.loads(p.read_text(encoding="utf-8"))
        ke, ky = kelimeler(e), kelimeler(y)
        asr = difflib.SequenceMatcher(None, ke, ky, autojunk=False).ratio() if ke or ky else 1.0
        oe, oy = {x["t"].lower() for x in e["ekran"]}, {x["t"].lower() for x in y["ekran"]}
        ocr = len(oe & oy) / max(1, len(oe | oy))
        toplam.append((asr, ocr))
        print(f"{p.stem}\tkelime {len(ke)}->{len(ky)}\tasr_benzerlik {asr:.3f}\tocr_ortusme {ocr:.3f}\tlink {len(e['linkler'])}->{len(y['linkler'])}\tkomut {len(e['komutlar'])}->{len(y['komutlar'])}")
    n = len(toplam)
    print(f"ORT asr {sum(a for a, _ in toplam) / n:.3f} ocr {sum(o for _, o in toplam) / n:.3f} n={n}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
