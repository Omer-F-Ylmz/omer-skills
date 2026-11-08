"""BUL-KUR-2: HIZMET sinifi kalemler icin site + ucretsiz katman. Cikti tmp/bk2/hizmet.tsv (kalem, site, ucretsiz, hesap)"""
import csv, json, re, sys, os, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ucretsiz_havuz as H
csv.field_size_limit(10**7)
R = Path(__file__).resolve().parents[1]
def oku(p, enc="utf-8"): return list(csv.DictReader(open(R / p, encoding=enc, errors="replace"), delimiter="\t"))
ana = {x["kalem"]: x for x in oku("docs/video-tarama/ana-liste.tsv", "utf-8-sig")}
sin = {}
for f in ("kurulum-ad.tsv", "kurulum-url.tsv"):
    for r in oku("docs/video-tarama/" + f): sin[r["kalem"]] = r["sinif"]
kalem = sorted(k for k, s in sin.items() if s == "HIZMET" and ana.get(k, {}).get("durum") in ("KURULMADI-SIRADA", "BULUNAMADI-KESIN", "BULUNDU-ADAY", "BULUNAMADI-ARANIYOR"))
CIK = R / "tmp/bk2/hizmet.tsv"
bit = {r["kalem"] for r in oku("tmp/bk2/hizmet.tsv")} if CIK.exists() else set()
kalan = [k for k in kalem if k not in bit]
print("hizmet", len(kalem), "kalan", len(kalan), flush=True)
ISTEM = """Asagidaki kalemler web hizmeti/SaaS/API adlari. Her biri icin: resmi site alan adi (bilmiyorsan bos), ucretsiz katman/deneme var mi: EVET | HAYIR | BILINMIYOR (UYDURMA, emin degilsen BILINMIYOR), hesap/anahtar gerekir mi: HESAP | ANAHTAR | YOK.
YALNIZ JSON dizi: [{"i":0,"site":"ornek.com","ucretsiz":"EVET","hesap":"HESAP"}, ...] her i bir kez.
Kalemler:
"""
KIL = threading.Lock()
def isle(parti):
    istem = ISTEM + "\n".join(f"{i}: {k}" for i, k in enumerate(parti))
    for tur in ("kolay", "orta", "orta"):
        m, mdl, _ = H.cagir(tur, istem, max_tokens=4000, zaman=120, etiket="bk2-hizmet", haiku_tavan=60)
        try:
            j = json.loads(re.search(r"\[.*\]", m, re.S).group(0))
            if {x.get("i") for x in j if isinstance(x, dict)} == set(range(len(parti))):
                return [(parti[x["i"]], str(x.get("site", ""))[:60], x.get("ucretsiz", "BILINMIYOR"), x.get("hesap", "")) for x in j]
        except Exception: pass
    return []
yeni = not CIK.exists()
f = open(CIK, "a", encoding="utf-8", newline=""); w = csv.writer(f, delimiter="\t")
if yeni: w.writerow(["kalem", "site", "ucretsiz", "hesap"])
P = [kalan[i:i + 50] for i in range(0, len(kalan), 50)]
with ThreadPoolExecutor(4) as ex:
    for s in ex.map(isle, P):
        with KIL: w.writerows(s); f.flush()
print("BITTI", flush=True)
