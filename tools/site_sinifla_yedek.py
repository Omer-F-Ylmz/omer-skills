"""Icerigi alinamayan (olu/engelli/bos) siteler: ad+baglam'dan havuzla sinifla; kaynak='ad-baglam' (icerik sinifi sayilmaz, ayri raporlanir)."""
import csv, json, re, sys, os, glob, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ucretsiz_havuz as h
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIK = os.path.join(KOK, ".kos/kopru/ara/site-sinif")
TURLER = "arac/uretici|ilham galerisi|component/animasyon kutuphanesi|egitim/nasil yapilir|3D/model|ikon/font/gorsel|sablon|portfolyo/ajans|blog/haber|urun/SaaS|dizin/liste|diger"
tam = {r["ad"]: r for r in csv.DictReader(open(os.path.join(KOK, "docs/site-inceleme/site-tam.tsv"), encoding="utf-8"), delimiter="\t")}


def is_(f):
    d = json.load(open(f, encoding="utf-8"))
    if "hata" not in d or d.get("kaynak") == "ad-baglam":
        return
    r = tam[d["ad"]]
    ist = ('Sitenin icerigi alinamadi. Alan adi ve onceki bilgiden tahmin et. SADECE tek satir JSON: {"tur":"<%s>","sunar":"<<=15 kelime>","ucretsiz":"evet|kismen|hayir|belirsiz","indirilebilir":"kod/model/font/ikon/sablon/yok"}\nSite: %s | on bilgi: %s / %s'
           % (TURLER, d["url"], r["baglam"], r["tur"]))
    for _ in range(8):
        try:
            m, _k, _l = h.cagir("ozet", ist, max_tokens=300, etiket="site-yedek", dogrula=lambda t: None if re.search(r'\{.*"tur".*\}', t, re.S) else "json yok")
        except PermissionError:
            continue
        if m:
            try:
                d.update(json.loads(re.search(r"\{.*\}", m, re.S).group(0)))
                d["kaynak"] = "ad-baglam"
                json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False)
            except Exception:
                pass
            return


with cf.ThreadPoolExecutor(4) as ex:
    list(ex.map(is_, glob.glob(CIK + "/*.json")))
