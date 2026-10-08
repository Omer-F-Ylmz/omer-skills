"""VİDEO-GÖZ-1a K4: rapor.md'yi altın JSON'a karşı puanlar (salt okur, LLM yok)."""
import re
from pathlib import Path

from . import anlamsal
from .tarama import bolum, tablolar

ALAN_YOK = ()  # 1b-2a: urller · is_akisi · promptlar artık rapor şemasında; alan_yok anahtarı boş liste olarak kalır


def norm(s):
    return re.sub(r"[\W_]+", "", s.casefold().replace("ı", "i"))  # 1b-1: RapidOCR ı'yı i okur → iki taraf katlanır


def lev(a, b):
    on = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        su = [i]
        for j, y in enumerate(b, 1):
            su.append(min(on[j] + 1, su[j - 1] + 1, on[j - 1] + (x != y)))
        on = su
    return on[-1]


def eslesir(rapor_ad, altin_ad, alias):
    r = norm(rapor_ad)
    return any(r == a or (len(a) > 5 and lev(r, a) <= 1) for a in map(norm, [altin_ad, *alias]))


def url_norm(u):
    u = re.sub(r"^https?://(www\.)?", "", u.strip().casefold())
    return re.split(r"[?#]", u)[0].rstrip("/")


def _ilk_sutun(metin, bas, sutun):
    return [r[0] for h, rows in tablolar(bolum(metin, bas)) if h and h[0].casefold() == sutun for r in rows if r]


def _rapor_linkler(metin):
    out = {}
    for s in bolum(metin, "Açıklama bağlantıları").splitlines():
        m = re.search(r"https?://\S+", s)
        if s.lstrip().startswith("-") and m:
            c = re.search(r"sınıf: (\w+)", s)  # 1b-2a: yalnız açık sınıf alanı; "sponsor değil" gibi alt dizeler sayılmaz
            out[url_norm(m[0])] = {"aday": "aday: evet" in s, "sponsor": bool(c) and c[1] == "sponsor"}
    return out


def puan(metin, altin):
    rapor_adlar = _ilk_sutun(metin, "Adaylar", "ad")
    tur, kacan, yazim, isabetli, bel = {}, [], [0, 0], set(), [0, 0]
    for a in altin.get("adaylar", []):
        bulunan = [r for r in rapor_adlar if eslesir(r, a["ad"], a.get("alias", []))]
        if a.get("belirsiz"):  # paydaya girmez; bulunursa ayrı sayılır
            bel[1] += 1; bel[0] += bool(bulunan); isabetli.update(bulunan); continue
        t = tur.setdefault(a["tur"], [0, 0]); t[1] += 1
        if not bulunan:
            kacan.append((a["ad"], a["tur"])); continue
        t[0] += 1; isabetli.update(bulunan)
        yazim[1] += 1; yazim[0] += any(norm(r) == norm(a["ad"]) for r in bulunan)
    yak = sum(v[0] for v in tur.values()), sum(v[1] for v in tur.values())

    rl, link = _rapor_linkler(metin), {}
    for k in ("aciklama", "yorum"):
        y, s = [0, 0], [0, 0]
        for l in (x for x in altin.get("linkler", []) if x.get("kaynak", "aciklama") == k):
            y[1] += 1
            r = rl.get(url_norm(l["url"]))
            if r:
                y[0] += 1; s[1] += 1
                s[0] += r["aday"] == bool(l.get("aday")) and r["sponsor"] == (l.get("sinif") == "sponsor")
        link[k] = {"yakalama": tuple(y), "sinif": tuple(s)}

    sem = {k: (len(g), len(anlamsal.esle(g, r, anlamsal.ESIK[k]))) for k, (g, r) in anlamsal.alanlar(metin, altin).items()}  # 1b-2a DEVAM-1: anlamsal

    rk = [norm(x) for x in _ilk_sutun(metin, "Kurulum/komutlar", "komut")]
    km = altin.get("komutlar", [])
    km_y = sum(any(norm(k["komut"]) in r for r in rk) for k in km)

    ogr = (sem["ogrenimler"][1], sem["ogrenimler"][0]) if "ogrenimler" in altin else None

    uu = [url_norm(r[0]) for _, rows in tablolar(bolum(metin, "URL'ler")) for r in rows if r]
    u_ur = altin.get("urller", [])
    u_iy = [u for u in u_ur if not DEGERSIZ.search(url_norm(u["url"]))]
    yeni = {"urller": (sum(url_norm(u["url"]) in uu for u in u_ur), len(u_ur)), "urller_iy": (sum(url_norm(u["url"]) in uu for u in u_iy), len(u_iy)),
            "is_akisi": sem["is_akisi"][::-1], "promptlar": sem["promptlar"][::-1]}
    return {"yakalama": yak, "isabet": (len(isabetli), len(rapor_adlar)), "ad_yazim": tuple(yazim),
            "belirsiz": tuple(bel), "ogrenimler": ogr,
            "tur": {k: tuple(v) for k, v in tur.items()}, "link_aciklama": link["aciklama"], "link_yorum": link["yorum"],
            "site_ui": sem["site_ui"][::-1], "komutlar": (km_y, len(km)), "kacan": kacan, "alan_yok": list(ALAN_YOK), **yeni}


NEDEN = {"ekran": "ekranda-var-OCR-kaçırdı", "açıklama": "açıklamada", "aciklama": "açıklamada", "yorum": "yorumda"}


def gecer(ad, duz, pencere):
    """1b-1 M0: norm ≤4 → kelime sınırı (1-3 ardışık kelime birebir); ≥5 → alt dize ya da ≤5 kelimelik pencereyle lev ≤1."""
    n = norm(ad)
    if len(n) <= 4:
        return bool(n) and n in pencere
    return n in duz or any(abs(len(w) - len(n)) <= 1 and lev(w, n) <= 1 for w in pencere)


def _jpeg(yol):
    from . import metin as m
    p = Path(yol)
    return m.jpeg_boyut(p.read_bytes()) if p.is_file() else None


DEGERSIZ = re.compile(r"^(?:localhost|127\.0\.0\.1)\b|(?:^|\.)example\.|^chatgpt\.com/c/|^claude\.ai/chat/|^web\.telegram\.org\b")  # 1b-1S S6


def kapsam(paket, altin, boyut=_jpeg):
    """1b-1 M0: altın aday/komut/url'nin paket.md metninde geçme oranı + paket jetonu (metin krk/4 + kare ⌈w/28⌉×⌈h/28⌉). LLM yok."""
    kel = [norm(w) for w in re.findall(r"\w+", paket.casefold())]
    pencere = {"".join(kel[i:i + k]) for k in range(1, 6) for i in range(len(kel))}
    duz, ses = norm(paket), bool(re.search(r"^\[\d", bolum(paket, "Segmentler"), re.M))
    y, n, kacan = 0, 0, []
    for a in altin.get("adaylar", []):
        if any(gecer(x, duz, pencere) for x in [a["ad"], *a.get("alias", [])]):
            y += not a.get("belirsiz"); n += not a.get("belirsiz"); continue
        n += not a.get("belirsiz")
        k = a.get("kaynak", "")
        kacan.append((a["ad"], "belirsiz" if a.get("belirsiz") else ("ASR-bozdu" if ses else "ses-yok") if k == "ses" else NEDEN.get(k, "ses-yok")))
    km = altin.get("komutlar", [])
    ur = altin.get("urller", [])
    kare = [b for s in bolum(paket, "Kareler").splitlines() if (yol := s.split(" · ")[0].strip()) and (b := boyut(yol))]
    uk = [(u["url"], _url_neden(u, paket)) for u in ur if norm(url_norm(u["url"])) not in duz]
    kk = [(k["komut"], k.get("kaynak", "?")) for k in km if norm(k["komut"]) not in duz]
    iy = [u["url"] for u in ur if not DEGERSIZ.search(url_norm(u["url"]))]  # 1b-1S S6: kabul işe yarar URL'lerle
    return {"aday": (y, n), "komut": (len(km) - len(kk), len(km)), "url": (len(ur) - len(uk), len(ur)), "kacan": kacan,
            "url_ise": (len(iy) - sum(u in iy for u, _ in uk), len(iy)),
            "url_kacan": uk, "komut_kacan": kk,
            "token": {"metin": len(paket) // 4, "kare": sum(-(-w // 28) * -(-h // 28) for w, h in kare), "kare_n": len(kare)}}


def kapsam_satirlar(p):
    t = p["token"]
    return [f"kapsam: aday {p['aday'][0]}/{p['aday'][1]} · komut {p['komut'][0]}/{p['komut'][1]} · url {p['url'][0]}/{p['url'][1]} · işe yarar url {p['url_ise'][0]}/{p['url_ise'][1]}",
            f"token: metin {t['metin']} + kare {t['kare']} ({t['kare_n']} kare) = {t['metin'] + t['kare']}",
            "kaçan: " + (", ".join(f"{a} ({n})" for a, n in p["kacan"]) or "yok"),
            "url kaçan: " + (", ".join(f"{a} ({n})" for a, n in p["url_kacan"]) or "yok"),
            "komut kaçan: " + (", ".join(f"{a} ({n})" for a, n in p["komut_kacan"]) or "yok")]


def _icerir(metin, adlar):
    """1b-1R R6: kapsam ile aynı eşleşme (gecer), tek metin için."""
    kel = [norm(w) for w in re.findall(r"\w+", metin.casefold())]
    pencere = {"".join(kel[i:i + k]) for k in range(1, 6) for i in range(len(kel))}
    return any(gecer(x, norm(metin), pencere) for x in adlar)


def kacan_alt(kacan, altin, ham, gurultu, esik=0.5, pay=5):
    """1b-1R R6: 'ekranda-var-OCR-kaçırdı' kaçanına ham goz/ocr.json'dan alt neden. Ham satırda geçiyor → bütçe-attı (güven ≥ esik, gürültü
    değil) | gürültü-süzgeci | düşük-güven; geçmiyor → altın zamanı ±pay sn'de okunan kare var: OCR-okuyamadı, yok: örnekleme-boşluğu."""
    from . import metin as m
    aday, out = {a["ad"]: a for a in altin.get("adaylar", [])}, []
    for ad, neden in kacan:
        if neden != NEDEN["ekran"] or ad not in aday:
            out.append((ad, neden))
            continue
        a = aday[ad]
        sat = [(x, s) for _, r in ham for x, s, _ in r if _icerir(x, [ad, *a.get("alias", [])])]
        z = m.sn(a["zaman"]) if a.get("zaman") else None
        alt = ("bütçe-attı" if any(s >= esik and not gurultu(x) for x, s in sat) else "gürültü-süzgeci" if any(s >= esik for _, s in sat)
               else "düşük-güven" if sat else "OCR-okuyamadı" if z is not None and any(abs(t - z) <= pay for t, _ in ham)
               else "örnekleme-boşluğu")
        out.append((ad, f"{neden}/{alt}"))
    return out


KISALTICI = re.compile(r"\b(?:bit\.ly|t\.co|tinyurl\.com|goo\.gl|lnkd\.in|buff\.ly|ow\.ly|rebrand\.ly|dub\.sh|shorturl\.at|is\.gd|cutt\.ly)/", re.I)
YONLEN = re.compile(r"[?&](?:ref|aff|via|utm_\w+)=|/(?:go|out|r|redirect|aff)/", re.I)


def _url_neden(u, paket):
    """Kaçan URL nedeni: açıklamada-yok | yorumda | redirect | kısaltıcı | ekranda (altın kaynağına göre)."""
    k = u.get("kaynak", "açıklama")
    if k == "yorum":
        return "yorumda"
    if k not in ("açıklama", "aciklama"):
        return "ekranda"
    a = bolum(paket, "Açıklama bağlantıları")
    return "kısaltıcı" if KISALTICI.search(a) else "redirect" if YONLEN.search(a) else "açıklamada-yok"


def satirlar(p):
    f = lambda t: f"{t[0]}/{t[1]}"  # noqa: E731
    return [f"adaylar: yakalama {f(p['yakalama'])} · isabet {f(p['isabet'])} · ad yazım {f(p['ad_yazim'])}",
            "  tür " + " · ".join(f"{k} {f(v)}" for k, v in p["tur"].items()),
            *([f"  belirsiz bulundu {f(p['belirsiz'])}"] if p["belirsiz"][1] else []),
            *(f"linkler {k}: yakalama {f(p['link_' + k]['yakalama'])} · sınıf {f(p['link_' + k]['sinif'])}" for k in ("aciklama", "yorum")),
            f"site_ui: yakalama {f(p['site_ui'])}", f"komutlar: yakalama {f(p['komutlar'])}",
            *([f"öğrenimler: yakalama {f(p['ogrenimler'])}"] if p["ogrenimler"] else []),
            *(f"{k}: yakalama {f(p[k])}" for k in ("urller", "urller_iy", "is_akisi", "promptlar")),
            "kaçan: " + (", ".join(f"{a} ({t})" for a, t in p["kacan"]) or "yok")]
