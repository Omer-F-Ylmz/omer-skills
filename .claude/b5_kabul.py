"""BLENDER-5 f3 KABUL özeti: blender-faz5-b5.tsv + b5-yargi.json → yol başına ortalamalar ve kapı kararları."""
import csv, json, statistics as st
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "docs" / "kutuphane" / "olcum"
rows = list(csv.DictReader((D / "blender-faz5-b5.tsv").open(encoding="utf-8"), delimiter="\t"))
by = defaultdict(list)
for r in rows:
    by[r["yol"]].append(r)
ort = lambda y, k: st.mean(float(r[k]) for r in by[y]) if by[y] else float("nan")
for y in by:
    print(y, "n", len(by[y]), "jeton", round(ort(y, "toplam")), "süre", round(ort(y, "sure_sn"), 1),
          "tur", round(ort(y, "tur"), 2), "kontrol", sorted({r["kalite"] for r in by[y]}), "hata", [r["hata"] for r in by[y] if r["hata"] != "-"])

yp = D / "blender-faz5-b5-yargi.json"
puan, eslik = defaultdict(list), defaultdict(list)
for anahtar, v in (json.loads(yp.read_text(encoding="utf-8")) if yp.is_file() else {}).items():
    if not isinstance(v["puan"], dict):
        print("yargı ayrıştırılamadı:", anahtar)
        continue
    toplamlar = {v["esle"][h].rsplit("-", 1)[0]: sum(p.values()) / len(p) for h, p in v["puan"].items() if h in v["esle"]}
    hedef = eslik if "tek5K" in anahtar else puan
    for y, p in toplamlar.items():
        hedef[y].append(p)
po = lambda d, y: st.mean(d[y]) if d[y] else float("nan")
print("yargı ana", {y: (round(po(puan, y), 2), len(puan[y])) for y in puan})
print("yargı eşli", {y: (round(po(eslik, y), 2), len(eslik[y])) for y in eslik})

kapi = {
    "jeton tek5 ≤ 0.55×tek": ort("tek5", "toplam") <= 0.55 * ort("tek", "toplam"),
    "süre tek5 ≤ tek4": ort("tek5", "sure_sn") <= ort("tek4", "sure_sn"),
    "yargı tek5 > tek": po(puan, "tek5") > po(puan, "tek"),
    "yargı tek5 ≥ tek4": po(puan, "tek5") >= po(puan, "tek4"),
    "eşli tek5K ≥ tek": po(eslik, "tek5K") >= po(eslik, "tek"),
    "kontrol her satır 1.0": all(float(r["kalite"]) == 1.0 for r in rows),
}
print("oran jeton tek5/tek", round(ort("tek5", "toplam") / ort("tek", "toplam"), 3))
for k, v in kapi.items():
    print("KAPI", "OK " if v else "YOK", k)
