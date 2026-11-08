"""KURULUM-D2C tur2: kurulum-coz-2 + coz3-cikti/*.tsv -> kurulum-coz-4.tsv (+ -gerekce). Eski dosyalar degismez.
MODEL sinifi DOGRULANDI -> MODEL-BEKLE (Omer karari: yerel/buyuk modeller simdilik YOK); boyut yol alanina yazilir (HF API).
Kullanim: python -I tools/coz3_birlestir.py [--boyut]   (tekrar calistirilabilir)"""
import csv, json, subprocess, sys
from pathlib import Path
from collections import Counter
K = Path(__file__).resolve().parents[1] / "docs/video-tarama"
oku = lambda p: list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
rows = {r["kalem"]: r for r in oku(K / "kurulum-coz-2.tsv")}
ger = {r["kalem"]: r["gerekce"] for r in oku(K / "kurulum-coz-2-gerekce.tsv")}
yeni = Counter()
for f in sorted((K / "coz3-cikti").glob("*.tsv")):
    for r in oku(f):
        k = r.get("kalem")
        if not k or k not in rows: continue
        if r["sonuc"] not in ("DOGRULANDI", "YOK"): r["sonuc"] = rows[k]["sonuc"]  # ADAY kalirsa eski karar korunur
        eski = rows[k]["sonuc"]
        rows[k] = {x: r.get(x, "") for x in ("kalem", "sinif", "sonuc", "kaynak", "puan", "yol")}
        ger[k] = r.get("gerekce", "")
        yeni[(eski, rows[k]["sonuc"])] += 1

def hf_gb(repo):
    try:
        o = subprocess.run(["curl", "-s", "-m", "8", f"https://huggingface.co/api/models/{repo}?blobs=true"], capture_output=True, text=True, timeout=12).stdout
        s = json.loads(o).get("siblings", [])
        return sum((x.get("size") or 0) for x in s) / 2**30
    except Exception:
        return None

model_bekle = 0
for k, r in rows.items():
    if r["sinif"] == "MODEL" and r["sonuc"] == "DOGRULANDI":
        r["sonuc"] = "MODEL-BEKLE"; model_bekle += 1
        gb = hf_gb(r["kaynak"][3:]) if "--boyut" in sys.argv and r["kaynak"].startswith("hf:") else None
        r["yol"] = (f"{gb:.1f} GB; " if gb is not None else "boyut ? ; ") + "Omer karari: yerel/buyuk model simdilik YOK"
        ger[k] = "MODEL-BEKLE (DOGRULANDI iken isaretlendi): " + ger.get(k, "")

with open(K / "kurulum-coz-4.tsv", "w", encoding="utf-8", newline="") as a, open(K / "kurulum-coz-4-gerekce.tsv", "w", encoding="utf-8", newline="") as b:
    wa, wb = csv.writer(a, delimiter="\t"), csv.writer(b, delimiter="\t")
    wa.writerow(["kalem", "sinif", "sonuc", "kaynak", "puan", "yol"]); wb.writerow(["kalem", "sonuc", "gerekce"])
    for k, r in rows.items():
        wa.writerow([r["kalem"], r["sinif"], r["sonuc"], r["kaynak"], r["puan"], r["yol"]]); wb.writerow([k, r["sonuc"], ger.get(k, "")])
print(len(rows), dict(Counter(r["sonuc"] for r in rows.values())), "gecis:", dict(yeni), "MODEL-BEKLE:", model_bekle)
print("sinif x DOGRULANDI:", dict(Counter(r["sinif"] for r in rows.values() if r["sonuc"] == "DOGRULANDI")))
