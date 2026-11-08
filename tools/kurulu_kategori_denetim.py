"""KURULUM-D2C adim E: kurulu tekil kalemlerin (kurulum-d2-sonuc.tsv KURULDU*/ZATEN) kategori.tsv satirlarini
bagimsiz ikinci model + hakemle denetler (kategori_denetim.kalem_kontrol). kategori.tsv DEGISMEZ; cikti:
docs/video-tarama/kurulu-kategori.tsv (kalem,tur,mevcut,denetim,uyum,yontem,gerekce). Parti parti, tekrar kosulunca biten atlanir.
Kullanim: python tools/kurulu_kategori_denetim.py [--maks N]"""
import csv, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]; K = R / "docs/video-tarama"
sys.path.insert(0, str(R / "tools"))
import kategori_denetim as D  # noqa: E402
oku = lambda p: list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
KUR = {"KURULDU", "KURULDU-SARMALAYICI", "KURULDU-KAYNAK", "KURULDU-KUTUPHANE", "ZATEN"}
kur = {r["kalem"].lower() for r in oku(K / "kurulum-d2-sonuc.tsv") if r["durum"] in KUR}
rows = [r for r in oku(R / "docs/envanter/kategori.tsv") if r["ad"].lower() in kur]
gor = set(); tek = []
for r in rows:  # kalem basina tek satir (ilk): 802 tekil kalem
    if r["ad"].lower() not in gor: gor.add(r["ad"].lower()); tek.append(r)
rows = tek
out = K / "kurulu-kategori.tsv"
biten = {(r["kalem"], r["tur"]) for r in oku(out)} if out.exists() else set()
todo = [r for r in rows if (r["ad"], r["tur"]) not in biten]
maks = int(sys.argv[sys.argv.index("--maks") + 1]) if "--maks" in sys.argv else len(todo)
todo = todo[:maks]
print("kurulu satir", len(rows), "yapilacak", len(todo), flush=True)
yeni = not out.exists()
with open(out, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    if yeni: w.writerow(["kalem", "tur", "mevcut", "denetim", "uyum", "yontem", "gerekce"])
    for i in range(0, len(todo), 30):
        g = todo[i:i + 30]
        res = D.kalem_kontrol([{"ad": r["ad"], "tur": r["tur"], "yol": r["yol"], "ozet": ""} for r in g])
        for r, (b, ik, gv, y, ger) in zip(g, res):
            w.writerow([r["ad"], r["tur"], r["birincil"], b, "UYUM" if b == r["birincil"] else "FARK", y, ger]);
        f.flush(); print(i + len(g), "/", len(todo), time.strftime("%H:%M:%S"), flush=True)
