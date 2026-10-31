"""LISTE-CIKAR-1 EK 2: ana-liste.tsv kalemleri için özellik düzeyi satırlar + yapılış tarzı (videodan, Haiku). Kaldığı yerden sürer.
Kullanım: python -I tools/liste_ozellik.py [--en-az-video N] [--en-cok M] [--isci K]   (kalemler video sayısına göre büyükten küçüğe)"""
import csv
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(K / "tools"))
import liste_cikar as LC  # noqa: E402
import ucretsiz_havuz as H  # noqa: E402

LISTE = K / "docs/video-tarama/ana-liste.tsv"
OZ = K / "docs/video-tarama/ana-liste-ozellik.tsv"
YAP = K / "docs/video-tarama/yapilis"
YAP.mkdir(exist_ok=True)
csv.field_size_limit(10**7)
ISTEM = """Asagida arac/site/kutuphane kalemleri ve her biri icin videolardan alinti metin var. Yalniz alintida GECEN bilgiye dayan; tahmin/uydurma yok, bilgi yoksa bos birak.
Her kalem icin JSON: {"ad":"","ozellikler":["madde"],"nasil":"videoda nasil yapildi/kullanildi: adimlar, komut, ayar, prompt, is akisi","bizde":"bizdeki karsiligi ve FARKI (BIZDE alanina bak)","al":"alinacak iyi ozellik","at":"atilacak/kotu yan"}
CIKTI: yalniz JSON dizisi.

"""


def guvenli(ad):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", ad)[:80] or "kalem"


def baglam(ad, vids, dos):
    parca, ad_l = [], ad.lower().split("/")[-1]
    for v in vids[:3]:
        if v not in dos:
            continue
        d = LC.oku(dos[v])
        m = d.get("meta") or {}
        tr = " ".join(x.get("t", "") for x in d.get("transkript") or [])
        ek = " | ".join(dict.fromkeys(x.get("t", "") for x in d.get("ekran") or []))
        kare = d.get("kare_aciklama") or ""
        kare = kare if isinstance(kare, str) else json.dumps(kare, ensure_ascii=False)
        tum = f"{m.get('aciklama') or ''}\n{tr}\n{ek}\n{kare}"
        pen = []
        for mt in re.finditer(re.escape(ad_l), tum.lower()):
            pen.append(tum[max(0, mt.start() - 350):mt.end() + 450])
            if len(pen) == 2:
                break
        parca.append(f"[{v}] {m.get('baslik')}: " + (" ... ".join(pen) if pen else tum[:500]))
    return "\n".join(parca)[:2600]


def main():
    a = sys.argv[1:]
    g = lambda k, v: int(a[a.index(k) + 1]) if k in a else v
    en_az, en_cok, isci = g("--en-az-video", 3), g("--en-cok", 10**9), g("--isci", 8)
    rows = list(csv.DictReader(open(LISTE, encoding="utf-8", newline=""), delimiter="\t"))
    rows = [r for r in rows if len(r["kaynak_video_idleri"].split(",")) >= en_az]
    rows.sort(key=lambda r: -len(r["kaynak_video_idleri"].split(",")))
    bekle = [r for r in rows if not (YAP / (guvenli(r["kalem"]) + ".md")).exists()][:en_cok]
    dos = LC.dosyalar()
    partiler = [bekle[i:i + 5] for i in range(0, len(bekle), 5)]
    kilit, say = threading.Lock(), [0]
    yeni = not OZ.exists()

    def is_(p):
        istem = ISTEM + "\n\n".join(f"### {r['kalem']} (tur {r['tur']}, durum {r['durum']})\nBIZDE: {r['bizde_nerede'] or 'yok'}\n{baglam(r['kalem'], r['kaynak_video_idleri'].split(','), dos)}" for r in p)
        try:
            met = re.sub(r"^```\w*|```$", "", H._haiku(istem).strip(), flags=re.M).strip()
            arr = json.loads(met[met.index("["):met.rindex("]") + 1])
        except Exception as e:
            print("hata", p[0]["kalem"], str(e)[:80], flush=True)
            return
        by = {x.get("ad"): x for x in arr if isinstance(x, dict)}
        with kilit:
            with open(OZ, "a", encoding="utf-8", newline="") as f:
                w = csv.writer(f, delimiter="\t", lineterminator="\n")
                for r in p:
                    x = by.get(r["kalem"])
                    if not x:
                        continue
                    var = "var" if r["bizde_nerede"] else "yok"
                    for oz in x.get("ozellikler") or []:
                        w.writerow([r["kalem"], str(oz).replace("\n", " "), var, r["bizde_nerede"][:200]])
                    md = (f"# {r['kalem']}\n\n- tür: {r['tur']} · durum: {r['durum']} · videolar: {r['kaynak_video_idleri']}\n- bizde: {r['bizde_nerede'] or 'yok'}\n\n"
                          f"## Özellikler\n" + "\n".join(f"- {o}" for o in x.get("ozellikler") or []) +
                          f"\n\n## Videoda yapılış\n{x.get('nasil') or '-'}\n\n## Bizdeki karşılık ve fark\n{x.get('bizde') or '-'}\n\n## Al\n{x.get('al') or '-'}\n\n## At\n{x.get('at') or '-'}\n")
                    (YAP / (guvenli(r["kalem"]) + ".md")).write_text(md, encoding="utf-8")
                    say[0] += 1
            if say[0] % 50 < 5:
                print("kalem", say[0], flush=True)

    if yeni:
        with open(OZ, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter="\t", lineterminator="\n").writerow(["kalem", "ozellik", "bizde_var_mi", "nerede"])
    with ThreadPoolExecutor(isci) as ex:
        list(ex.map(is_, partiler))
    print("bitti", say[0], "/", len(bekle))


main()
