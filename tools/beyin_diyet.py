"""BEYIN-1 çekirdek diyeti: görev dosyasında yalnız geçerli ★ satırları kalır, geçmiş ★ satırları
`.kos/kopru/gorev-gecmis/<ad>.md`'ye eklenir (silinmez; beyin_al onu da içe alır).

Geçerli = ilk ★ satırı + ondan sonra, ilk geçmiş satırına dek öneki "GEÇERLİ" diyenler.
Kullanım: python tools/beyin_diyet.py <gorev.md> [--cikti YOL] [--uygula]
  --cikti: diyetli metni başka dosyaya yazar (ölçüm için; görev dosyasına dokunmaz)
  --uygula: görev dosyasını yerinde kısaltır (Desktop/Ömer onayıyla)
"""
import argparse
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
GECMIS = KOK / ".kos/kopru/gorev-gecmis"


def ayir(metin, ad):
    """(diyetli_metin, gecmis_satirlari)"""
    kalan, gecmis, ilk = [], [], True
    for s in metin.split("\n"):
        if s.startswith("★") or (s.startswith("(") and ") ★" in s):
            onek = s.split(") ★", 1)[0] if s.startswith("(") else ""
            # GEÇERLİ öneki yalnız ilk geçmiş satırından önce sayılır (eski dalganın "GEÇERLİ"si bayattır)
            if ilk or ("GEÇERLİ" in onek and not gecmis):
                ilk = False
                kalan.append(s)
                son = len(kalan)
                continue
            gecmis.append(s)
            continue
        kalan.append(s)
    if gecmis:
        kalan.insert(son,f"(geçmiş ★ {len(gecmis)} satır: `python tools/beyin.py ara \"{ad} <konu>\"`"
                        f" · .kos/kopru/gorev-gecmis/{ad}.md)")
    return "\n".join(kalan), gecmis


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("gorev")
    ap.add_argument("--cikti")
    ap.add_argument("--uygula", action="store_true")
    a = ap.parse_args(argv)
    p = Path(a.gorev)
    metin = p.read_bytes().decode("utf-8")
    diyet, gecmis = ayir(metin, p.stem)
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{p.name}: {len(metin.encode())} → {len(diyet.encode())} bayt, geçmiş ★ {len(gecmis)}")
    if a.cikti:
        Path(a.cikti).write_bytes(diyet.encode("utf-8"))
    if a.uygula and gecmis:
        GECMIS.mkdir(parents=True, exist_ok=True)
        with open(GECMIS / p.name, "a", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(gecmis) + "\n")  # önce geçmiş yazılır: yarıda kesilirse satır kaybolmaz
        p.write_bytes(diyet.encode("utf-8"))


if __name__ == "__main__":
    main()
