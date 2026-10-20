"""RUFLO-2 d4 B: Obsidian 50-dersler (MAKARA ders satırları) → tek banka (.kos/ogrenme/dersler.jsonl). Varsayılan --kuru: yazmaz.
  python tek_banka.py          → kaç satır yeni / mevcut derse birleşir / elenir
  python tek_banka.py uygula   → ders.ekle ile yazar (sır süzgeci + Jaccard birleştirme ders.py'de); kaynak not silinmez/değişmez
Yalnız "Ders/Öğrenilen/Kök neden/Sapma" satırları somut bir eylem içerirse alınır (Risk/Maliyet satırı tek başına ders değil: 'işe yaramayan ders' kök nedeni)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ogrenme"))
import ders  # noqa: E402

KASA = Path(r"C:\Users\pc\Desktop\Obsidian\50-dersler")
ALINAN = re.compile(r"(?i)^-\s*(ders|öğrenilen|ogrenilen|kök neden|kok neden|sapma)\s*[:：]\s*(.{40,})")


def adaylar():
    for p in sorted(KASA.glob("ders-*.md")):
        for s in p.read_text(encoding="utf-8", errors="replace").splitlines():
            m = ALINAN.match(s.strip())
            if m:
                govde = re.sub(r"\s*\(×\d+.*?\)\s*$", "", m[2]).strip()
                yield p.name, m[1].lower(), govde


def birlesir(baslik, kosul):
    a = set(ders.kelimeler(baslik + " " + kosul))
    return any(x["ajan"] == "*" and a and len(a & (b := set(ders.kelimeler(x["baslik"] + " " + x["kosul"])))) / len(a | b) >= 0.8
               for x in ders.oku())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    uygula = "uygula" in sys.argv
    toplam = yeni = birlesen = sirli = 0
    for dosya, tur, govde in adaylar():
        toplam += 1
        baslik, kosul = govde[:80], f"MAKARA {tur}"
        if ders.sir_var(govde):
            sirli += 1
        elif birlesir(baslik, kosul):
            birlesen += 1
        else:
            yeni += 1
        if uygula and not ders.sir_var(govde):
            ders.ekle("*", baslik, kosul, govde, "basari" if tur.startswith(("ders", "öğren", "ogren")) else "basarisizlik", f"makara:{dosya}", "betik-cikarim")
    print(f"{'UYGULANDI' if uygula else 'KURU'}: aday {toplam} · yeni {yeni} · birleşir {birlesen} · sırlı elenen {sirli}")
