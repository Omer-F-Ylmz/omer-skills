"""KATEGORI-KAPSAM adim 3 dogrulama: yer basina kapsam, 50 klasor/paket diskte, 100'luk ornek.
Kullanim: python tools/kapsam_dogrula.py [seed]   (cikti: .kos/kopru/arka/kategori-kapsam-dogrula.json + docs/envanter/kapsam-denetim-ornek3.tsv)
"""
import csv, json, os, random, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kapsam_sinifla as K

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv.field_size_limit(10**9)
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 5151
rd = lambda p: list(csv.DictReader(open(os.path.join(R, p), encoding="utf-8", newline=""), delimiter="\t"))
ek = rd("docs/envanter/kapsam-ek.tsv")
kat = rd("docs/envanter/kategori.tsv")
idx = {}
for r in kat:
    idx.setdefault(K.norm(r["ad"]), r)
yer = collections.OrderedDict()
eksik = []
for r in ek:
    y = yer.setdefault(r["kaynak_yer"], [0, 0])
    y[0] += 1
    if K.norm(r["ad"]) in idx:
        y[1] += 1
    else:
        eksik.append(r["ad"])
bos = [r["ad"] for r in kat if not (r.get("birincil") or "").strip()]
# 50 klasor/paket: diskte var mi + kategori.tsv'de var mi
rnd = random.Random(seed)
disk = [r for r in ek if r["yol"] and os.path.exists(r["yol"])]
ornek50 = rnd.sample(disk, min(50, len(disk)))
ok50 = sum(1 for r in ornek50 if K.norm(r["ad"]) in idx)
# 100'luk dogruluk ornegi (yalniz ek satirlar)
o100 = rnd.sample(ek, 100)
out = os.path.join(R, "docs/envanter/kapsam-denetim-ornek3.tsv")
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["no", "ad", "tur", "yol", "birincil", "ikincil"])
    for i, r in enumerate(o100, 1):
        k = idx.get(K.norm(r["ad"]), {})
        w.writerow([i, r["ad"], r["tur"], r["yol"], k.get("birincil", "?"), k.get("ikincil", "")])
res = {"seed": seed, "ek_satir": len(ek), "kategori_satir": len(kat), "bos_birincil": len(bos),
       "eksik": len(eksik), "eksik_ornek": eksik[:20], "disk_acik_50": len(ornek50), "kategoride_50": ok50,
       "yer": {k: {"toplam": v[0], "kategoride": v[1]} for k, v in yer.items()}}
json.dump(res, open(os.path.join(R, ".kos/kopru/arka/kategori-kapsam-dogrula.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v for k, v in res.items() if k != "yer"}, "yer_sayisi", len(yer))
