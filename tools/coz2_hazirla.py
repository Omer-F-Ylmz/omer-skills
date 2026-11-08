"""KURULUM-D2C adim 1: tekil son durumu BULUNAMADI-2/YANLIS-ESLESME/KURULUM-YOLU-YOK/HATA olan kalemleri partilere boler."""
import csv, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]; K = R / "docs/video-tarama"
def oku(p): return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
son = {r["kalem"]: r for r in oku(K / "kurulum-d2-sonuc.tsv")}
oz = {r["kalem"]: r for r in oku(K / "ana-liste-ozellik.tsv")}
coz = {r["kalem"]: r for r in oku(K / "kurulum-coz.tsv")}
HEDEF = {"BULUNAMADI-2", "YANLIS-ESLESME", "KURULUM-YOLU-YOK", "HATA"}
bit = set()
if (K / "kurulum-coz-2.tsv").exists(): bit = {r["kalem"] for r in oku(K / "kurulum-coz-2.tsv")}
liste = [k for k, r in son.items() if r["durum"] in HEDEF and k not in bit]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 67
print("hedef tekil:", len([k for k, r in son.items() if r["durum"] in HEDEF]), "kalan:", len(liste))
for i in range(0, len(liste), N):
    with open(K / f"coz2-girdi/p{i // N + 1:02d}.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["kalem", "sinif", "eski_durum", "eski_kaynak", "eski_not", "ozellik"])
        for k in liste[i:i + N]:
            s = son[k]; w.writerow([k, s["sinif"], s["durum"], s["kaynak"] or coz.get(k, {}).get("kaynak", ""), s["not"][:80], (oz.get(k, {}).get("ozellik", "") or "")[:220]])
