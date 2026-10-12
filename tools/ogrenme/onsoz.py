"""Ders yuvası — ajan önsözü. KALİTE-3-d14 godmode önsöz betiği yazılmadığı için uyumlu kendi yuvamız (devir/kalite-3-d14-ogrenme.md):
ajan .md'de frontmatter'dan hemen sonra işaretli blok; tek kaynak ONSOZ, idempotent, satır sonu korunur.
  python onsoz.py enjekte <ajan.md>... [--kuru] [--geri]
  python onsoz.py istem --ajan AD --gorev "..."   → dersler + istem (claude -p için; ders yoksa istem aynen)"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ders  # noqa: E402

BAS, BIT = "<!-- ders-yuvasi:basla -->", "<!-- ders-yuvasi:bitir -->"
DERS_PY = "C:/Projeler/omer-skills/tools/ogrenme/ders.py"
ONSOZ = f"""{BAS}
## Ders bankası
- Başta: `python {DERS_PY} getir --ajan {{ad}} --gorev "<görevin tek satırı>"`; çıkan dersleri (≤3) uygula, göreve uymuyorsa yok say.
- Sonda: kullandığın her ders için `ders.py geri --id <id> --sonuc basari|basarisizlik`; görev öğretici olduysa ≤3 genellenebilir ders: `ders.py ekle --ajan {{ad}} --sonuc basari|basarisizlik --kaynak <görev> --baslik .. --kosul .. --icerik ..` (sır/anahtar/kişisel veri yazma).
{BIT}"""


def enjekte(yol, kuru=False, geri=False):
    """→ değişti mi. Frontmatter'sız dosya atlanır."""
    yol = Path(yol)
    metin = yol.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in metin else "\n"
    if geri:
        if BAS not in metin:
            return False
        bas, bit = metin.index(BAS), metin.index(BIT) + len(BIT) + len(nl)
        yeni = metin[:bas] + metin[bit:]
    else:
        if BAS in metin or not metin.startswith("---"):
            return False
        son = metin.find(f"{nl}---{nl}", 3)
        if son < 0:
            return False
        son += len(nl) * 2 + 3
        yeni = metin[:son] + ONSOZ.format(ad=yol.stem).replace("\n", nl) + nl + metin[son:]
    if not kuru:
        yol.write_bytes(yeni.encode("utf-8"))
    return True


def istem(ajan, gorev):
    """claude -p yolu: ilgili dersleri istemin önüne koyar → (istem, ders id'leri)."""
    blok, ids = ders.getir(ajan, gorev)
    return (f"{blok}\n\n{gorev}" if blok else gorev), ids


def main(argv=None):
    ap = argparse.ArgumentParser()
    alt = ap.add_subparsers(dest="komut", required=True)
    e = alt.add_parser("enjekte")
    e.add_argument("dosyalar", nargs="+")
    e.add_argument("--kuru", action="store_true")
    e.add_argument("--geri", action="store_true")
    i = alt.add_parser("istem")
    i.add_argument("--ajan", required=True)
    i.add_argument("--gorev", required=True)
    a = ap.parse_args(argv)
    if a.komut == "istem":
        print(istem(a.ajan, a.gorev)[0])
        return
    for d in a.dosyalar:
        print(("değişir" if a.kuru else "değişti") if enjekte(d, a.kuru, a.geri) else "aynı", d)


if __name__ == "__main__":
    main()
