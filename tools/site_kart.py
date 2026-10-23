"""KAYNAK-SİTE-1 adım 3-4: kapalı siteler için arşiv denemesi, açık siteler için kaynak kartı, site-tam.tsv'yi tamamla, kapı sayımı."""
import csv, json, re, urllib.request, concurrent.futures as cf
from pathlib import Path

R = Path(__file__).resolve().parent.parent
RP = R / ".kos/kopru/rapor"
KART = R / "kartlar/site"
KART.mkdir(parents=True, exist_ok=True)
tam = list(csv.DictReader(open(RP / "site-tam.tsv", encoding="utf-8"), delimiter="\t"))
prob = {r["ad"]: r for r in csv.DictReader(open(RP / "site-prob.tsv", encoding="utf-8"), delimiter="\t")}
UYGUN = {"ilham galerisi": "site/UI ilhamı", "component/animasyon kütüphanesi": "site + animasyon", "3D/model": "3D/Blender",
         "ikon/font/görsel": "görsel varlık", "şablon": "site şablonu", "araç/üretici": "araç hattı", "eğitim/nasıl yapılır": "eğitim",
         "belirsiz": "belirsiz"}


def arsiv(h):
    try:
        with urllib.request.urlopen("https://archive.org/wayback/available?url=" + h, timeout=10) as r:
            c = json.load(r).get("archived_snapshots", {}).get("closest")
            return c["url"] if c and c.get("available") else ""
    except Exception:
        return "?"


kapali = [r["ad"] for r in tam if not prob[r["ad"]]["durum"].startswith("a")]
with cf.ThreadPoolExecutor(20) as ex:
    arc = dict(zip(kapali, ex.map(arsiv, kapali)))

sayim = {"kart": 0, "kapali-kanitli": 0, "yedek": 0}
for r in tam:
    p = prob[r["ad"]]
    acik = p["durum"].startswith("a")
    guven = "yüksek" if ("liste" in r["kaynak"] or "bağlantı" in r["kaynak"] or "," in r["videolar"]) else "düşük"
    if acik:
        r["erisim"] = "giriş gerekebilir" if p["giris"] else "açık"
        r["ucretsiz"] = "ücretsiz/açık kaynak ipucu" if p["ucretsiz"] else "belirsiz (fiyat sayfası bakılmadı)"
        body = f"""# {r['ad']}
- URL: {r['url']} · durum: açık · güven: {guven} · erişim: {r['erisim']}
- Başlık: {p['baslik']}
- Ne sunuyor: {p['aciklama'] or '(meta açıklama yok)'}
- Tür: {r['tur']} · ücretsiz: {r['ucretsiz']}
- Videolar: {r['videolar']} — videoda: {r['baglam'] or '-'}
- Repo/paket: {p['repo'] or '-'} · {p['npm'] or '-'}
- Nasıl alınır: {('git clone https://github.com/' + p['repo'].split(';')[0]) if p['repo'] else r['url']}
- Uyduğu yer: {UYGUN.get(r['tur'], 'belirsiz')} (tasarim-katalog / departman-frontend / animasyon-atolyesi)
- Not: HTTP yoklama (başlık+meta+bağlantı taraması); Chrome ile görsel inceleme yapılmadı, lisans metni okunmadı.
"""
        (KART / (r["ad"] + ".md")).write_text(body, encoding="utf-8")
        sayim["kart"] += 1
    else:
        a = arc.get(r["ad"], "")
        r["erisim"] = "kapalı"
        r["ucretsiz"] = "-"
        yaz = f"https:// ve http:// denendi: {p['durum']} ({p['giris'] or p['baslik']}); arşiv: {a or 'anlık görüntü yok'}"
        (KART / (r["ad"] + ".md")).write_text(f"# {r['ad']}\n- KAPALI/ULAŞILAMIYOR · güven: {guven}\n- Kanıt: {yaz}\n- Videolar: {r['videolar']} — {r['baglam']}\n", encoding="utf-8")
        sayim["kapali-kanitli"] += 1
        if a and a != "?":
            sayim["yedek"] += 1

cols = list(tam[0].keys())
with open(RP / "site-tam.tsv", "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, cols, delimiter="\t")
    w.writeheader()
    w.writerows(tam)
repo = sorted({(r["ad"], p["repo"], p["npm"]) for r in tam for p in [prob[r["ad"]]] if p["repo"] or p["npm"]})
with open(RP / "site-repo.tsv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["site", "repo", "npm"])
    w.writerows(repo)
tur = {}
for r in tam:
    tur[r["tur"]] = tur.get(r["tur"], 0) + 1
print(len(tam), sayim, "repo/paket:", len(repo), tur)
print("ucretsiz ipucu:", sum(1 for r in tam if r["ucretsiz"].startswith("ücretsiz")))
