"""TUR 13 doğrulama tablosu: kurulacaklar-temiz.tsv kalemi başına kurulu mu / çalışıyor mu / usta kartı var mı.
Durum: kur-tur*.tsv + skill-kur.tsv'de kalemin SON satırı geçerli (dosya sırası tur numarası). Çıktı tablo13.tsv + özet."""
import csv, json, re, pathlib
D = pathlib.Path(__file__).parent
K = D.parents[3]
n = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())

durum = {}  # norm ad -> (durum, kanit, kaynak)
def oku(p, ad_s, durum_s, kanit_s):
    for r in csv.reader(open(p, encoding="utf-8-sig"), delimiter="\t"):
        if len(r) <= max(ad_s, durum_s) or r[ad_s] in ("kalem", "ad"):
            continue
        durum[n(r[ad_s])] = (r[durum_s], r[kanit_s][:120] if len(r) > kanit_s else "", p.name)
oku(D / "skill-kur.tsv", 0, 3, 2)
for p in sorted(D.glob("kur-tur*.tsv"), key=lambda p: (int(re.search(r"\d+", p.name).group()), p.name)):
    bas = open(p, encoding="utf-8-sig").readline().split("\t")
    if len(bas) > 2 and bas[1] == "repo":
        oku(p, 0, 2, 3)
    else:
        oku(p, 0, 1, 2)

usta = set()
for l in open(K / "docs/usta-kart/usta.jsonl", encoding="utf-8"):
    try:
        usta.add(n(json.loads(l)["ad"]))
    except Exception:
        pass

def bul(ad, birlesen, repo):
    adaylar = [n(ad), n(birlesen), n(repo.split("/")[-1]) if repo else ""]
    return [a for a in adaylar if a]

satir, say = [], {}
for r in csv.DictReader(open(D / "kurulacaklar-temiz.tsv", encoding="utf-8-sig"), delimiter="\t"):
    ks = bul(r["kalem"], r["birlesen"], r["repo"])
    d = next((durum[k] for k in ks if k in durum), None)
    if d is None and r["eslesme"] == "KURULU":
        d = ("KURULU-onceden", r["kanit"][:120], "kurulacaklar-temiz")
    d = d or ("YOK", "", "")
    kart = any(k in usta or any(k and k in u for u in usta) for k in ks)
    satir.append([r["kalem"], r["tur_sinif"], r["eslesme"], d[0], "kart" if kart else "KART-YOK", d[2], d[1]])
    say[d[0]] = say.get(d[0], 0) + 1
with open(D / "tablo13.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["kalem", "tur", "eslesme", "durum", "usta", "kaynak", "kanit"])
    w.writerows(satir)
print(len(satir), "kalem;", sorted(say.items(), key=lambda x: -x[1]))
print("kart var", sum(s[4] == "kart" for s in satir))
