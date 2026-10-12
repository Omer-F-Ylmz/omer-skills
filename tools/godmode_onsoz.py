"""GODMODE önsöz enjeksiyonu: tek kaynak metni ajan .md'lerine frontmatter'dan hemen sonra işaretli blok olarak koyar.
İşaret `<!-- {isaret}:basla -->`…`<!-- {isaret}:bitir -->`; isaret="ders-yuvasi" RUFLO-1 onsoz.py bloğuyla birebir aynıdır.
Kaynak değişince yeniden çalıştır: eski blok sökülüp yenisi konur (idempotent; içerik aynıysa dosya değişmez).
  python tools/godmode_onsoz.py <kaynak.md> <ajan.md>... [--isaret godmode] [--kuru] [--geri]"""
import argparse
from pathlib import Path


def enjekte(yol, icerik, isaret="godmode", kuru=False, geri=False):
    """→ değişti mi. Frontmatter'sız dosya atlanır."""
    yol = Path(yol)
    metin = yol.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in metin else "\n"
    bas, bit = f"<!-- {isaret}:basla -->", f"<!-- {isaret}:bitir -->"
    yeni = metin
    if bas in yeni:
        i, j = yeni.index(bas), yeni.index(bit) + len(bit) + len(nl)
        yeni = yeni[:i] + yeni[j:]
    if not geri:
        if not yeni.startswith("---"):
            return False
        son = yeni.find(f"{nl}---{nl}", 3)
        if son < 0:
            return False
        son += len(nl) * 2 + 3
        blok = f"{bas}\n{icerik.strip()}\n{bit}\n".replace("\n", nl).replace("{ad}", yol.stem)
        yeni = yeni[:son] + blok + yeni[son:]
    if yeni == metin:
        return False
    if not kuru:
        yol.write_bytes(yeni.encode("utf-8"))
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("kaynak")
    ap.add_argument("ajanlar", nargs="+")
    ap.add_argument("--isaret", default="godmode")
    ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--geri", action="store_true")
    a = ap.parse_args(argv)
    icerik = Path(a.kaynak).read_text(encoding="utf-8")
    n = sum(enjekte(y, icerik, a.isaret, a.kuru, a.geri) for y in a.ajanlar)
    print(f"{'kuru: ' if a.kuru else ''}{n}/{len(a.ajanlar)} dosya {'söküldü' if a.geri else 'güncellendi'}")


if __name__ == "__main__":
    main()
