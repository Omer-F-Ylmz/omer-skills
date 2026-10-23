"""ARAC-BUL-2 adım 2: arac-bul-2.tsv'deki 'bulundu' GitHub repolarını C:\\AI\\indirilen'e indir + gitleaks + semgrep (arac_indir_1.isle); güvenlik-ret listesindekileri atlar.
>500MB olanlar arac_indir_1.isle'de 'buyuk-ertelendi' kalır (arac_buyuk_2.py işler). Kullanım: python tools/arac_bul_2d.py"""
import csv, os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arac_indir_1 as ai  # noqa: E402

YOL = os.path.join(ai.RAPOR, "arac-bul-2.tsv")
RET = os.path.join(ai.RAPOR, "..", "guvenlik-ret.tsv")


def main():
    ret = {r["repo"].lower() for r in csv.DictReader(open(RET, encoding="utf-8"), delimiter="\t")}
    with open(YOL, encoding="utf-8") as f:
        satir = list(csv.DictReader(f, delimiter="\t"))
    tekil = {}
    for r in satir:
        if r["sinif"] == "bulundu" and r["link"].startswith("https://github.com/"):
            tekil.setdefault(r["aday"].lower(), r)
    isler = []
    for k, r in tekil.items():
        if k.replace("/", "__") in ret:
            continue
        d = ai.gh_goruntule(r["aday"])
        if d:
            isler.append({"d": d, "kaynak": "bul-2", "video": r["video"]})
    print("indirilecek", len(isler), flush=True)
    sonuc = {}
    with ThreadPoolExecutor(3) as ex:
        for s in ex.map(ai.isle, isler):
            sonuc[s[0].lower()] = s
            print(s[0], s[2], s[3], s[4], flush=True)
    for r in satir:
        s = sonuc.get(r["aday"].lower())
        if s:
            r.update(durum=s[2], boyut=s[3], tarama=s[4])
    with open(YOL, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, list(satir[0]), delimiter="\t")
        w.writeheader()
        w.writerows(satir)
    import collections
    print("DURUM", collections.Counter(r["durum"] for r in satir if r["sinif"] == "bulundu"), flush=True)


if __name__ == "__main__":
    main()
