"""Saf işlevler: VTT temizliği, chapter'a hizalı segmentleme, altyazı dili seçimi, URL/id çıkarımı, JPEG boyutu, aHash."""
import html
import re
import struct

ZAMAN = re.compile(r"(?:(\d+):)?(\d+):(\d+)[.,](\d+)\s+-->")
ETIKET = re.compile(r"<[^>]*>")
URL = re.compile(r"https?://[^\s<>\"'()\[\]]+")
ID = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([\w-]{11})(?![\w-])|^([\w-]{11})$")


def sn(s):
    """"12:30" · "1:02:03" · "750" → saniye."""
    t = 0.0
    for x in s.strip().split(":"):
        t = t * 60 + float(x)
    return t


def ss(t):
    t = int(t)
    return f"{t // 3600}:{t // 60 % 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def vtt_ayristir(metin):
    """[(sn, satır)]: etiket ve boş satır atılır; YouTube'un kayan satır tekrarı (önceki satırın yeniden yazılması) ayıklanır.
    Satır, ilk göründüğü cue'nun başlangıç zamanını taşır."""
    out, bas, son = [], None, None
    for satir in metin.splitlines():
        z = ZAMAN.search(satir)
        if z:
            h, dk, s, ms = z.groups()
            bas = int(h or 0) * 3600 + int(dk) * 60 + int(s) + int(ms) / 10 ** len(ms)
            continue
        if bas is None:
            continue
        t = " ".join(html.unescape(ETIKET.sub("", satir)).split())
        if t and t != son:
            out.append((round(bas, 3), t))
            son = t
    return out


def segmentle(satirlar, chapters=None, sure=None, hedef=60):
    """~hedef sn'lik segmentler {i, bas, son, metin}; hiçbir segment chapter sınırını aşmaz."""
    son_t = sure or (satirlar[-1][0] + 1 if satirlar else 0)
    bolum = [(float(c["start_time"]), float(c.get("end_time") or son_t)) for c in chapters or []] or [(0.0, son_t)]
    seg = []
    for cb, cs in bolum:
        cur = None
        for t, x in satirlar:
            if not cb <= t < cs:
                continue
            if cur is None or t - cur["bas"] >= hedef:
                if cur:
                    cur["son"] = t
                cur = {"bas": cb if cur is None and t - cb < hedef else t, "son": cs, "metin": []}
                seg.append(cur)
            cur["metin"].append(x)
    for i, s in enumerate(seg):
        s["i"], s["metin"] = i, " ".join(s["metin"])
    return [{"i": s["i"], "bas": s["bas"], "son": s["son"], "metin": s["metin"]} for s in seg]


def dil_sec(meta, dil=None):
    """Öncelik: elle dil → elle en → otomatik dil → otomatik en (dil varsayılan tr). Önce tam anahtar, sonra `dil-` öneki."""
    diller = list(dict.fromkeys([dil or "tr", "en"]))
    for tur, anahtar in (("elle", "subtitles"), ("oto", "automatic_captions")):
        mevcut = list(meta.get(anahtar) or {})
        for d in diller:
            k = next((k for k in mevcut if k == d), None) or next((k for k in mevcut if k.startswith(d + "-") and k != d + "-orig"), None)
            if k:
                return k, tur
    return None


def urller(aciklama):
    return list(dict.fromkeys(u.rstrip(".,;:!?") for u in URL.findall(aciklama or "")))


def vid(s):
    g = ID.search(s.strip())
    return (g[1] or g[2]) if g else None


def jpeg_boyut(veri):
    """SOF işaretinden (genişlik, yükseklik)."""
    i = 2
    while i + 9 < len(veri):
        if veri[i] != 0xFF:
            i += 1
            continue
        isaret, uzunluk = veri[i + 1], struct.unpack(">H", veri[i + 2:i + 4])[0]
        if isaret in (0xC0, 0xC1, 0xC2):
            y, g = struct.unpack(">HH", veri[i + 5:i + 9])
            return g, y
        i += 2 + uzunluk
    return 0, 0


def ahash(ham):
    """8×8 gri ham bayttan ortalama-hash (int)."""
    ort = sum(ham) / max(len(ham), 1)
    return sum(1 << n for n, b in enumerate(ham) if b > ort)
