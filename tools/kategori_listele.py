"""NIHAI 0-K: bir kategorinin altindaki HER seyi (yol + nasil calistirilir) listeler.
Kullanim: python tools/kategori_listele.py <kategori|cok-yonlu> [--tur X] [--ikincil] [--guven yuksek|orta|dusuk] [--say]
  --ikincil: ikincil etiketi o kategori olanlari da kat; 'cok-yonlu' / --cok-yonlu: cok_yonlu etiketli kalemler."""
import csv, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kategori_sinifla import KATEGORILER, nasil  # noqa: E402

TSV = Path(__file__).resolve().parents[1] / "docs/envanter/kategori.tsv"
csv.field_size_limit(10**9)

def sec(kat, tur=None, ikincil=False, guven=None, cy=False):
    with open(TSV, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if cy or kat == "cok-yonlu":
                if not r["cok_yonlu"]:
                    continue
            elif r["birincil"] != kat and not (ikincil and kat in r["ikincil"].split(";")):
                continue
            if tur and r["tur"] != tur:
                continue
            if guven and r["guven"] != guven:
                continue
            yield r

def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); print("kategoriler:", ", ".join(KATEGORILER), "+ cok-yonlu"); return 0
    kat = a[0]
    if kat not in KATEGORILER + ["cok-yonlu"]:
        print(f"bilinmeyen kategori {kat!r}; gecerli: {', '.join(KATEGORILER)}, cok-yonlu", file=sys.stderr); return 2
    val = lambda f: a[a.index(f) + 1] if f in a else None
    rs = list(sec(kat, val("--tur"), "--ikincil" in a, val("--guven"), "--cok-yonlu" in a))
    if "--say" in a:
        from collections import Counter
        print(len(rs), dict(Counter(r["tur"] for r in rs))); return 0
    for r in rs:
        print(f"{r['tur']}\t{r['ad']}\t{r['yol']}\t{nasil(r['tur'], r['ad'], r['yol'])}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
