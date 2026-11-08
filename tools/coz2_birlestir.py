"""coz2-cikti/p*.tsv -> kurulum-coz-2.tsv (kurulum-coz.tsv bicimi: kalem,sinif,sonuc,kaynak,puan,yol) + kurulum-coz-2-gerekce.tsv. Tekrar calistirilabilir."""
import csv
from pathlib import Path
from collections import Counter
K = Path(__file__).resolve().parents[1] / "docs/video-tarama"
rows = {}
for f in sorted((K / "coz2-cikti").glob("p*.tsv")):
    for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="\t"):
        if r.get("kalem"): rows[r["kalem"]] = r
with open(K / "kurulum-coz-2.tsv", "w", encoding="utf-8", newline="") as a, open(K / "kurulum-coz-2-gerekce.tsv", "w", encoding="utf-8", newline="") as b:
    wa, wb = csv.writer(a, delimiter="\t"), csv.writer(b, delimiter="\t")
    wa.writerow(["kalem", "sinif", "sonuc", "kaynak", "puan", "yol"]); wb.writerow(["kalem", "sonuc", "gerekce"])
    for r in rows.values():
        wa.writerow([r["kalem"], r["sinif"], r["sonuc"], r["kaynak"], r["puan"], r["yol"]]); wb.writerow([r["kalem"], r["sonuc"], r["gerekce"]])
print(len(rows), Counter(r["sonuc"] for r in rows.values()), "ARAMA-LIMITI/repo bulunamadi YOK:", sum(1 for r in rows.values() if r["sonuc"] == "YOK" and ("LIMIT" in r["gerekce"].upper() or "bulunamadi" in r["gerekce"].lower())))
