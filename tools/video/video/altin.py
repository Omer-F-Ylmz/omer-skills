"""VİDEO-GÖZ-1a K4: rapor.md'yi altın JSON'a karşı puanlar (salt okur, LLM yok)."""
import re

from .tarama import bolum, tablolar

ALAN_YOK = ("urller", "is_akisi", "promptlar")  # rapor şemasında karşılığı yok → 0, boşluk görünür


def norm(s):
    return re.sub(r"[\W_]+", "", s.casefold())


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
            out[url_norm(m[0])] = {"aday": "aday: evet" in s, "sponsor": "sponsor" in s.casefold()}
    for _, rows in tablolar(bolum(metin, "İz")):
        for r in rows:
            for m in re.finditer(r"https?://\S+", " ".join(r)):
                if url_norm(m[0]) in out and "sponsor" in " ".join(r).casefold():
                    out[url_norm(m[0])]["sponsor"] = True
    return out


def _kelime(s):
    return set(re.findall(r"\w{4,}", s.casefold()))


def puan(metin, altin):
    rapor_adlar = _ilk_sutun(metin, "Adaylar", "ad")
    tur, kacan, yazim, isabetli = {}, [], [0, 0], set()
    for a in altin.get("adaylar", []):
        t = tur.setdefault(a["tur"], [0, 0]); t[1] += 1
        bulunan = [r for r in rapor_adlar if eslesir(r, a["ad"], a.get("alias", []))]
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

    # ponytail: site_ui kelime örtüşmesi (altın kelimelerinin ≥yarısı), anlamsal eşleşme gerekirse Jev
    rt = [_kelime(x) for x in _ilk_sutun(metin, "Site/UI", "teknik")]
    ui = altin.get("site_ui", [])
    ui_y = sum(any(2 * len(_kelime(u["teknik"]) & r) >= len(_kelime(u["teknik"])) > 0 for r in rt) for u in ui)

    rk = [norm(x) for x in _ilk_sutun(metin, "Kurulum/komutlar", "komut")]
    km = altin.get("komutlar", [])
    km_y = sum(any(norm(k["komut"]) in r for r in rk) for k in km)

    return {"yakalama": yak, "isabet": (len(isabetli), len(rapor_adlar)), "ad_yazim": tuple(yazim),
            "tur": {k: tuple(v) for k, v in tur.items()}, "link_aciklama": link["aciklama"], "link_yorum": link["yorum"],
            "site_ui": (ui_y, len(ui)), "komutlar": (km_y, len(km)), "kacan": kacan, "alan_yok": list(ALAN_YOK),
            **{k: (0, len(altin.get(k, []))) for k in ALAN_YOK}}


def satirlar(p):
    f = lambda t: f"{t[0]}/{t[1]}"  # noqa: E731
    return [f"adaylar: yakalama {f(p['yakalama'])} · isabet {f(p['isabet'])} · ad yazım {f(p['ad_yazim'])}",
            "  tür " + " · ".join(f"{k} {f(v)}" for k, v in p["tur"].items()),
            *(f"linkler {k}: yakalama {f(p['link_' + k]['yakalama'])} · sınıf {f(p['link_' + k]['sinif'])}" for k in ("aciklama", "yorum")),
            f"site_ui: yakalama {f(p['site_ui'])}", f"komutlar: yakalama {f(p['komutlar'])}",
            *(f"{k}: rapor alanı yok {f(p[k])}" for k in p["alan_yok"]),
            "kaçan: " + (", ".join(f"{a} ({t})" for a, t in p["kacan"]) or "yok")]
