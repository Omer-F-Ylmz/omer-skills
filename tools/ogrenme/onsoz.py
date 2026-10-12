"""Ders yuvası — ajan önsözü. Enjeksiyon KALİTE-3-d14 godmode_onsoz.enjekte'ye devredilir (isaret="ders-yuvasi"; FABLE godmode bloğundan
bağımsız): ajan .md'de frontmatter'dan hemen sonra işaretli blok; tek kaynak ONSOZ, idempotent, satır sonu korunur.
  python onsoz.py enjekte <ajan.md>... [--kuru] [--geri]
  python onsoz.py istem --ajan AD --gorev "..."   → dersler + istem (claude -p için; ders yoksa istem aynen)"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # tools/ (repo) — claude.ai zip'inde godmode_onsoz.py yanında
import ders  # noqa: E402
import godmode_onsoz  # noqa: E402

DERS_PY = "C:/Projeler/omer-skills/tools/ogrenme/ders.py"
ONSOZ = f"""## Ders bankası
- Başta: `python {DERS_PY} getir --ajan {{ad}} --gorev "<görevin tek satırı>"`; çıkan dersleri (≤3) uygula, göreve uymuyorsa yok say.
- Sonda: kullandığın her ders için `ders.py geri --id <id> --sonuc basari|basarisizlik`; görev öğretici olduysa ≤3 genellenebilir ders: `ders.py ekle --ajan {{ad}} --sonuc basari|basarisizlik --kaynak <görev> --baslik .. --kosul .. --icerik ..` (sır/anahtar/kişisel veri yazma)."""


def enjekte(yol, kuru=False, geri=False):
    """→ değişti mi. Frontmatter'sız dosya atlanır."""
    return godmode_onsoz.enjekte(yol, ONSOZ, isaret="ders-yuvasi", kuru=kuru, geri=geri)


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
    sys.stdout.reconfigure(encoding="utf-8")  # cp1254 konsol ✓/İ basamıyor
    if a.komut == "istem":
        print(istem(a.ajan, a.gorev)[0])
        return
    for d in a.dosyalar:
        print(("değişir" if a.kuru else "değişti") if enjekte(d, a.kuru, a.geri) else "aynı", d)


if __name__ == "__main__":
    main()
