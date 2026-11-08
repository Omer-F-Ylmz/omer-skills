"""LISTE-CIKAR-1 EK 2: ana-liste.tsv kalemleri için özellik düzeyi satırlar + yapılış tarzı (videodan, Haiku). Kaldığı yerden sürer.
Kullanım: python -I tools/liste_ozellik.py [--en-az-video N] [--en-cok M] [--isci K]   (kalemler video sayısına göre büyükten küçüğe)"""
import csv
import json
import re
import sys
import threading
import time
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
Kalemi genel bilginle DOLDURMA: alintida yazmayan ozellik, entegrasyon, komut, kurulum adimi yazma. Alinti yalniz adi geciriyorsa ozellikler tek madde olur: 'Alintida yalniz adi geciyor (<baglam>)'. Butun alanlar duz metin (string) olur; ozellikler string dizisi.
Alinti bu kalemi ANLATMIYORSA (adi gecmiyor ya da metin baska bir seyi anlatiyor) ozellikler TEK madde olur: 'Alintida bu kalem anlatilmiyor'; baska seyin ozelliklerini bu kaleme yazma, nasil/al/at bos kalir.
Kalem bir kanal, kisi, sirket, kavram, dosya bicimi ya da genel terimse yalniz O KALEM hakkinda soyleneni yaz (or. 'Videoyu paylasan kanal', 'Listede gecen 6. madde'); videonun ana konusu olan BASKA aracin/urunun ozelliklerini bu kaleme yazma. Her ozellik maddesinden once sor: bu cumlenin oznesi bu kalem mi? Degilse yazma.
Her kalem icin JSON: {"ad":"","ozellikler":["madde"],"nasil":"videoda nasil yapildi/kullanildi: adimlar, komut, ayar, prompt, is akisi","bizde":"bizdeki karsiligi ve FARKI (BIZDE alanina bak)","al":"alinacak iyi ozellik","at":"atilacak/kotu yan"}
CIKTI: yalniz JSON dizisi.

"""


YANLIS_YER = re.compile(r"(?i)ge[cç]miyor|anlat[iı]lm[iı]yor|anlat[iı]m[iı]? yok|bahsetmiyor|i[cç]ermiyor")


def kullanim_dolu():
    try:
        sys.path.insert(0, str(K / ".kos/kopru"))
        import ajan_sira
        return ajan_sira.kullanim_dolu()
    except Exception:
        return False


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
    parti, haiku = g("--parti", 5), "--haiku" in a
    rows = list(csv.DictReader(open(LISTE, encoding="utf-8", newline=""), delimiter="\t"))
    rows = [r for r in rows if len(r["kaynak_video_idleri"].split(",")) >= en_az]
    if "--yalniz" in a:
        ad = set(open(a[a.index("--yalniz") + 1], encoding="utf-8").read().split("\n"))
        rows = [r for r in rows if r["kalem"] in ad]
    rows.sort(key=lambda r: -len(r["kaynak_video_idleri"].split(",")), reverse="--ters" in a)
    def tamam(r):
        f = YAP / (guvenli(r["kalem"]) + ".md")
        if not f.exists():
            return False
        t = f.read_text(encoding="utf-8", errors="ignore")
        if "{'" in t or "['" in t:
            return False
        oz = t.split("## Özellikler", 1)[-1].split("\n## ", 1)[0]
        if YANLIS_YER.search(oz) and oz.count("\n- ") > 1:
            return False
        if haiku and "- kural: v3" not in t:
            return False
        return "- model: haiku" in t if haiku else True
    bekle = [r for r in rows if not tamam(r)][g("--bas", 0):][:en_cok]
    dos = LC.dosyalar()
    partiler = [bekle[i:i + parti] for i in range(0, len(bekle), parti)]
    kilit, say = threading.Lock(), [0]
    yeni = not OZ.exists()

    def is_(p):
        istem = ISTEM + "\n\n".join(f"### {r['kalem']} (tur {r['tur']}, durum {r['durum']})\nBIZDE: {r['bizde_nerede'] or 'yok'}\n{baglam(r['kalem'], r['kaynak_video_idleri'].split(','), dos)}" for r in p)
        arr, son, mdl = None, "", "?"
        for den in range(4):
            y = None
            try:
                if haiku:
                    if tamam(p[0]) and tamam(p[-1]):
                        return
                    if kullanim_dolu():
                        print("durdu: plan kullanim kapisi (5s>=85 / haftalik>=80)", flush=True)
                        return
                    y = H._haiku(istem)
                else:
                    y, mdl, _ = H.cagir("kolay", istem, max_tokens=3500, zaman=120, etiket="liste-ozellik", haiku_tavan=400)
                met = re.sub(r"^```\w*|```$", "", (y or "").strip(), flags=re.M).strip()
                arr = json.loads(met[met.index("["):met.rindex("]") + 1])
                if any(not isinstance(o, str) for x in arr if isinstance(x, dict) for o in (x.get("ozellikler") or [])):
                    arr = None
                    raise ValueError("bicim: ozellik madde degil")
                for x in arr:
                    for k in ("nasil", "bizde", "al", "at"):
                        v = x.get(k) if isinstance(x, dict) else None
                        if isinstance(v, list) and all(isinstance(i, str) for i in v):
                            x[k] = "; ".join(v)
                        elif v is not None and not isinstance(v, str):
                            arr = None
                            raise ValueError(f"bicim: {k} metin degil")
                mdl = "haiku" if haiku else mdl
                break
            except Exception as e:
                son = f"{type(e).__name__} {str(e)[:60]} | yanit={len(y or '')}"
                time.sleep(15 * (den + 1))
        if arr is None:
            print("hata", p[0]["kalem"], son, flush=True)
            return
        by = {x.get("ad"): x for x in arr if isinstance(x, dict)}
        with kilit:
            with open(OZ, "a", encoding="utf-8", newline="") as f:
                w = csv.writer(f, delimiter="\t", lineterminator="\n")
                for r in p:
                    x = by.get(r["kalem"]) or (arr[0] if len(p) == 1 and arr and isinstance(arr[0], dict) else None)
                    if not x:
                        continue
                    var = "var" if r["bizde_nerede"] else "yok"
                    for oz in x.get("ozellikler") or []:
                        w.writerow([r["kalem"], str(oz).replace("\n", " "), var, r["bizde_nerede"][:200]])
                    md = (f"# {r['kalem']}\n\n- tür: {r['tur']} · durum: {r['durum']} · videolar: {r['kaynak_video_idleri']}\n- bizde: {r['bizde_nerede'] or 'yok'}\n- model: {mdl}\n- kural: v3\n\n"
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
