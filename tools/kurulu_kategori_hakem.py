"""KANIT-KATEGORI-1 is 3: kurulu-kategori.tsv'deki FARK satirlarina Sonnet hakem karari (A=mevcut, B=denetim, ikisiyle sinirli degil).
Cikti docs/video-tarama/kurulu-kategori-hakem.tsv (kalem,tur,mevcut,denetim,hakem,karar KALDI|DEGIS|HAKEM-YOK,gerekce). Tekrar kosulunca biten atlanir.
--uygula: DEGIS satirlarini docs/envanter/kategori.tsv birincil'ine yazar (yedek .oncesi-kanit-1107), kategori-degisiklik.tsv'ye iz birakir.
Kullanim: KD_SONNET=1 python tools/kurulu_kategori_hakem.py [--maks N] | --uygula"""
import csv, os, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]; K = R / "docs/video-tarama"; E = R / "docs/envanter"
os.environ.setdefault("KD_SONNET", "1")
sys.path.insert(0, str(R / "tools"))
import kategori_denetim as D  # noqa: E402
csv.field_size_limit(10**9)
oku = lambda p: list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
out = K / "kurulu-kategori-hakem.tsv"
def hakem_kos():
    maks = int(sys.argv[sys.argv.index("--maks") + 1]) if "--maks" in sys.argv else 10**6
    kat = {}
    for r in oku(E / "kategori.tsv"): kat.setdefault((r["ad"].lower(), r["tur"]), r)
    fark = [r for r in oku(K / "kurulu-kategori.tsv") if r["uyum"] == "FARK"]
    biten = {(r["kalem"], r["tur"]) for r in oku(out)} if out.exists() else set()
    todo = [r for r in fark if (r["kalem"], r["tur"]) not in biten][:maks]
    print("FARK", len(fark), "yapilacak", len(todo), flush=True)
    yeni = not out.exists()
    with open(out, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        if yeni: w.writerow(["kalem", "tur", "mevcut", "denetim", "hakem", "karar", "gerekce"])
        for i in range(0, len(todo), 20):
            g = todo[i:i + 20]
            grup = []
            for r in g:
                y = kat.get((r["kalem"].lower(), r["tur"]), {}).get("yol", "")
                grup.append({"tur": r["tur"], "ad": r["kalem"], "kanit": D.kanit_uret(r["kalem"], r["tur"], y), "ilk": r["mevcut"], "ikinci": r["denetim"]})
            res, kaynak, _ = D.hakem_parti(grup, sonnet=True)
            if len(res) < len(g):  # eksik kalanlar icin tek tekrar
                kalan = [j for j in range(len(g)) if j not in res]
                r2, _, _ = D.hakem_parti([grup[j] for j in kalan], sonnet=True)
                for n, j in enumerate(kalan):
                    if n in r2: res[j] = r2[n]
            for j, r in enumerate(g):
                if j in res: h, ger = res[j]; w.writerow([r["kalem"], r["tur"], r["mevcut"], r["denetim"], h, "KALDI" if h == r["mevcut"] else "DEGIS", ger])
                else: w.writerow([r["kalem"], r["tur"], r["mevcut"], r["denetim"], "", "HAKEM-YOK", "hakem yanit vermedi"])
            f.flush(); print(i + len(g), "/", len(todo), kaynak, time.strftime("%H:%M:%S"), flush=True)
def uygula():
    import shutil
    deg = {(r["kalem"].lower(), r["tur"]): r for r in oku(out) if r["karar"] == "DEGIS"}
    src = E / "kategori.tsv"; shutil.copy2(src, str(src) + ".oncesi-kanit-1107")
    raw = open(src, encoding="utf-8", newline="").read(); crlf = "\r\n" in raw[:5000]
    rows = list(csv.reader(open(src, encoding="utf-8", newline=""), delimiter="\t")); h = rows[0]
    ia, it, ib, iy, ig = h.index("ad"), h.index("tur"), h.index("birincil"), h.index("yontem"), h.index("gerekce")
    iz = []; n = 0
    for r in rows[1:]:
        d = deg.get((r[ia].lower(), r[it]))
        if d and r[ib] != d["hakem"]:
            iz.append([r[ia], r[it], r[h.index("yol")], r[ib], d["hakem"], r[h.index("ikincil")], "hakem-kurulu-1107:" + d["gerekce"]]); r[ib] = d["hakem"]; r[iy] = "hakem-kurulu-1107"; r[ig] = d["gerekce"]; n += 1
    lt = "\r\n" if crlf else "\n"
    with open(src, "w", encoding="utf-8", newline="") as f: csv.writer(f, delimiter="\t", lineterminator=lt).writerows(rows)
    dg = E / "kategori-degisiklik.tsv"
    with open(dg, "ab") as f:
        for z in iz: f.write(("\t".join(x.replace("\t", " ").replace("\n", " ") for x in z) + lt).encode("utf-8"))
    print("uygulanan", n, "iz", len(iz))
if __name__ == "__main__":
    uygula() if "--uygula" in sys.argv else hakem_kos()
