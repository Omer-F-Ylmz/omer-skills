"""VİDEO-PLATFORM-1: herkese açık Instagram gönderisi → <önbellek>/ig-<kod>/ (meta.json + medya).
Tek uç embed/captioned; Cookie başlığı yok, oturum yok, tarayıcı çerezi okunmaz. İmzalı medya adresi hiçbir yere yazılmaz."""
import json
import random
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

BASLIK = {  # DEVAM-1 basamak a: tam Chrome başlık seti (çıplak UA'ya Instagram hata sayfası veriyor)
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}
ARA = (10, 20)  # ayar: embed istekleri arası rastgele sn
ENGEL_BEKLE, ENGEL_UST = 120, 3  # ayar: 429/giriş → bekle, 1 tekrar; art arda N engel → IG durur
_KILIT, _SON, _ENGEL = threading.Lock(), [None], [0]
uyku, saat = time.sleep, time.monotonic  # testte sahte


class IgHata(Exception):
    pass


def gizle(url):
    return f"{urllib.parse.urlsplit(url).hostname} (imzalı adres gizlendi)"


def _al(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=BASLIK), timeout=30) as r:
            return r.status, r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""


def _indir(url, yol):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": BASLIK["User-Agent"]}), timeout=120) as r:
            yol.write_bytes(r.read())
    except (urllib.error.URLError, OSError) as e:  # mesajda adres yok: yalnız alan adı + kod
        raise IgHata(f"ig indirme: {gizle(url)} {getattr(e, 'code', '') or type(e).__name__}") from None


def sayfa(kod):
    """Embed sayfası; istekler arası ARA sn; 429/giriş yönlendirmesi → ENGEL_BEKLE sn, 1 tekrar, yine engel → IgHata('ig: engellendi')."""
    url = f"https://www.instagram.com/p/{kod}/embed/captioned/"
    with _KILIT:
        if _ENGEL[0] >= ENGEL_UST:
            raise IgHata(f"ig: parti durdu (art arda {ENGEL_UST} engel)")
        for i in (0, 1):
            if i:
                uyku(ENGEL_BEKLE)
            elif _SON[0] is not None and (b := _SON[0] + random.uniform(*ARA) - saat()) > 0:
                uyku(b)
            durum, son, html = _al(url)
            _SON[0] = saat()
            if durum != 429 and "/accounts/login" not in son:
                break
        else:
            _ENGEL[0] += 1
            raise IgHata("ig: engellendi")
        _ENGEL[0] = 0
    if durum != 200:
        raise IgHata(f"ig: HTTP {durum}")
    return html


def ayristir(html):
    """Gömülü contextJSON (JSON içinde JSON dizesi) → {tur, hesap, aciklama, sure, ogeler[{video, gorsel}]}; kaçışları json çözer."""
    i = html.find('"contextJSON":')
    sm = None
    if i >= 0:
        sm = (json.loads(json.JSONDecoder().raw_decode(html, i + 14)[0]).get("gql_data") or {}).get("shortcode_media")
    if not sm:
        raise IgHata("ig: embed verisi yok")
    yan = (sm.get("edge_sidecar_to_children") or {}).get("edges")
    ac = (sm.get("edge_media_to_caption") or {}).get("edges") or []
    return {"tur": "reel" if sm.get("is_video") and not yan else "post", "hesap": (sm.get("owner") or {}).get("username") or "?",
            "aciklama": ac[0]["node"].get("text") or "" if ac else "", "sure": sm.get("video_duration"),
            "ogeler": [{"video": o.get("video_url") if o.get("is_video") else None, "gorsel": o.get("display_url")}
                       for o in ([e["node"] for e in yan] if yan else [sm])]}


def getir(d):
    """ig-<kod> klasörü: sayfa → ayrıştır → medya hemen indir (imzalı adres süreli) → meta.json (adres yazılmaz)."""
    kod = d.name[3:]
    p = ayristir(sayfa(kod))
    video, gorseller, goz_not = False, [], None
    if p["tur"] == "reel":
        if p["ogeler"][0]["video"]:
            _indir(p["ogeler"][0]["video"], d / "goz-video.mp4")
            video = True
        else:
            goz_not = "göz: yok (embed video vermedi)"
    else:  # ponytail: karışık sidecar'da video öğesinin yalnız kapağı OCR'lanır; video işlemek gerekirse ayrı adım
        for i, o in enumerate(p["ogeler"], 1):
            if o["gorsel"]:
                _indir(o["gorsel"], d / f"gorsel-{i}.jpg")
                gorseller.append(f"gorsel-{i}.jpg")
    ilk = next((s.strip() for s in p["aciklama"].splitlines() if s.strip()), "")
    meta = {"id": d.name, "title": (ilk[:80] or f"instagram {p['tur']}").replace("·", "-"), "language": None, "channel": p["hesap"].replace("·", "-"),
            "duration": p["sure"] or 0, "chapters": [], "description": p["aciklama"], "subtitles": {}, "automatic_captions": {},
            "platform": "instagram", "ig_tur": "reel" if p["tur"] == "reel" else "görsel gönderi",
            "url": f"https://www.instagram.com/{'reel' if p['tur'] == 'reel' else 'p'}/{kod}/", "video": video, "gorseller": gorseller, "goz_not": goz_not}
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta
