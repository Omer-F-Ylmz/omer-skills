"""Kurallar.md (Obsidian, tek kaynak) -> .kos/kopru/on-soz.md kartı; ilgili(metin) -> göreve uyan 2-3 kuralın tam metni."""
import pathlib
import re
import sys

KAYNAK = pathlib.Path(r"C:\Users\pc\Desktop\Obsidian\10-kararlar\Kurallar.md")
HEDEF = pathlib.Path(__file__).resolve().parent.parent / ".kos" / "kopru" / "on-soz.md"


def oku(yol=KAYNAK):
    """[(baslik, kart, anahtarlar, govde)]"""
    kurallar = []
    for blok in re.split(r"^## ", yol.read_text(encoding="utf-8"), flags=re.M)[1:]:
        baslik, _, kalan = blok.partition("\n")
        kart = re.search(r"^kart: (.*)$", kalan, re.M)
        anahtar = re.search(r"^anahtar: (.*)$", kalan, re.M)
        govde = re.sub(r"^(kart|anahtar): .*\n", "", kalan, flags=re.M).strip()
        kurallar.append((baslik.strip(), kart.group(1) if kart else "", (anahtar.group(1) if anahtar else "").split(), govde))
    return kurallar


def kart(kurallar):
    govde = " · ".join(f"{b.split()[0]} {k}" for b, k, _, _ in kurallar)
    return f"KURAL KARTI (tek kaynak Obsidian 10-kararlar/Kurallar.md#<id>; ayrıntı: dosya ya da `beyin ara`; ilgili kurallar tam metin aşağıda): {govde}\n"


def ilgili(metin, n=3, kurallar=None):
    """Görev metnine anahtar sözcük örtüşmesiyle en çok uyan n kuralın tam metni (yerel, Claude jetonu 0); eşleşme yoksa ''."""
    kurallar = kurallar or oku()
    dusuk = metin.lower()
    puan = sorted(((sum(1 for a in an if a in dusuk), i) for i, (_, _, an, _) in enumerate(kurallar)), reverse=True)
    sec = [kurallar[i] for p, i in puan[:n] if p > 0]
    return "".join(f"[{b}] {g}\n" for b, _, _, g in sec) + _icgoru(metin)


def _icgoru(metin):
    """BEYIN-DUSUN-1: göreve uyan kanıtlı ≤2 içgörü, kural bloğuyla aynı önekte; uyan yoksa '' (0 jeton)."""
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import beyin_dusun
        s = beyin_dusun.satirlar(metin)
        return f"İçgörü:\n{s}\n" if s else ""
    except Exception:
        return ""


def uret():
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import beyin_dusun
        icgoru = beyin_dusun.kart_metin()  # BEYIN-DUSUN-1: kural kartının yanında bugünün kanıtlı içgörüleri (yoksa '')
    except Exception:
        icgoru = ""
    HEDEF.write_text(kart(oku()) + icgoru, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ilgili":
        print(ilgili(" ".join(sys.argv[2:])))
    else:
        uret()
        print(HEDEF.stat().st_size, "bayt")
