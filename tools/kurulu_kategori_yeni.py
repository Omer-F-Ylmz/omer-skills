"""KANIT-KATEGORI-1 is 3c: bugun kurulan KURULDU kalemleri (rapor/kurulum-omer-sonuc.tsv) bagimsiz ikinci model + Sonnet hakemle kategorize eder (D.kalem_kontrol).
Cikti docs/video-tarama/kurulu-kategori-yeni.tsv (kalem,tur,yol,kategori,ikincil,guven,yontem,gerekce,kategoride_var). --uygula: kategori.tsv'de OLMAYANLARI ekler (yedek .oncesi-yeni-1107)."""
import csv, os, sys, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[1]; K = R / "docs/video-tarama"; E = R / "docs/envanter"
os.environ.setdefault("KD_SONNET", "1"); sys.path.insert(0, str(R / "tools"))
import kategori_denetim as D  # noqa: E402
csv.field_size_limit(10**9); H = Path.home()
out = K / "kurulu-kategori-yeni.tsv"
kat = {(r["ad"].lower(), r["tur"]) for r in csv.DictReader(open(E / "kategori.tsv", encoding="utf-8"), delimiter="\t")}
def kos():
    items = []
    for r in csv.DictReader(open(R / "rapor/kurulum-omer-sonuc.tsv", encoding="utf-8-sig"), delimiter="\t"):
        if r["durum"] != "KURULDU": continue
        if r["yontem"] == "SKILL":
            for ad in [x.strip() for x in r["not"].split(",") if x.strip()]:
                items.append({"ad": ad, "tur": "skill", "yol": str(H / ".claude/skills" / ad), "ozet": ""})
        else: items.append({"ad": r["kalem"], "tur": "arac", "yol": "", "ozet": f"{r['yontem']} paketi {r['not']}"})
    seen = set(); items = [i for i in items if not ((i["ad"].lower(), i["tur"]) in seen or seen.add((i["ad"].lower(), i["tur"])))]
    print("kalem", len(items), flush=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["kalem", "tur", "yol", "kategori", "ikincil", "guven", "yontem", "gerekce", "kategoride_var"])
        for i in range(0, len(items), 30):
            g = items[i:i + 30]; res = D.kalem_kontrol(g)
            for k, (b, ik, gv, y, ger) in zip(g, res):
                w.writerow([k["ad"], k["tur"], k["yol"], b, ";".join(ik) if isinstance(ik, list) else ik, gv, y, ger, "E" if (k["ad"].lower(), k["tur"]) in kat else "H"])
            f.flush(); print(i + len(g), flush=True)
def uygula():
    src = E / "kategori.tsv"; shutil.copy2(src, str(src) + ".oncesi-yeni-1107")
    crlf = "\r\n" in open(src, encoding="utf-8", newline="").read(5000); lt = "\r\n" if crlf else "\n"
    n = 0
    with open(src, "ab") as f:
        for r in csv.DictReader(open(out, encoding="utf-8"), delimiter="\t"):
            if r["kategoride_var"] == "H":
                satir = [r["kalem"], r["tur"], r["yol"] or "yok", r["kategori"], r["ikincil"], "", r["guven"], r["yontem"], r["gerekce"]]
                f.write(("\t".join(x.replace("\t", " ").replace("\n", " ") for x in satir) + lt).encode("utf-8")); n += 1
    print("eklenen", n)
if __name__ == "__main__": uygula() if "--uygula" in sys.argv else kos()
