"""KALİTE-1 4a: departman-* skill'lerine araç kataloğu (katalog.md) — docs/departmanlar/<ad>.md tablosundan.
Katalog skill klasöründe durur (claude.ai zip'iyle taşınır, repo dışı cwd'de de okunur), oturuma yüklenmez; SKILL.md yalnız yolunu verir.
  python tools/departman_katalog.py   (yeniden üretir; docs değişince tekrar koş)"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SATIR = "Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez."


def katalog(md):
    """docs/departmanlar/<ad>.md → başlık + yalnız tablo satırları."""
    tablo = [s for s in md.splitlines() if s.startswith("|")]
    return "\n".join([md.splitlines()[0] + " — araç kataloğu", "", *tablo, ""])


def uret(kok=KOK):
    for sk in sorted((kok / "skills").glob("departman-*/SKILL.md")):
        ad = sk.parent.name.removeprefix("departman-")
        kaynak = kok / "docs/departmanlar" / f"{ad}.md"
        if not kaynak.exists():
            continue
        (sk.parent / "katalog.md").write_bytes(katalog(kaynak.read_text(encoding="utf-8")).encode("utf-8"))
        govde = sk.read_text(encoding="utf-8")
        if SATIR not in govde:
            sk.write_bytes(govde.replace("\n## Adımlar", f"{SATIR}\n\n## Adımlar", 1).encode("utf-8"))
        yield sk.parent.name


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(" ".join(uret()))
