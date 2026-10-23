"""KAYNAK-SİTE-1 adım 1: videolardaki site adreslerini çıkar, liste.tsv ile birleştir -> site-tam.tsv."""
import csv, json, re, sys
from pathlib import Path
from collections import defaultdict

R = Path(__file__).resolve().parent.parent
DERIN = R / "docs/video-tarama/derin"
OUT = R / ".kos/kopru/rapor/site-tam.tsv"
TLD = "com|io|dev|app|ai|co|design|so|me|org|net|sh|xyz|studio|tools|gallery|style|page|site|run|cloud|fm|tv|gg|build|cc|us|tech|world|works|club|to|ly|games|art|agency|space|online|website|store|zone|wiki|vc|lab|codes"
RX = re.compile(r"(?<![\w@./-])((?:[a-z0-9][a-z0-9-]{1,40}\.)+(?:%s))(?![\w-])(?:/[^\s\"'<>)]*)?" % TLD, re.I)
SKIP = {"youtube.com", "youtu.be", "instagram.com", "github.com", "tiktok.com", "x.com", "twitter.com", "facebook.com",
        "claude.ai", "anthropic.com", "openai.com", "google.com", "gmail.com", "linkedin.com", "discord.com", "discord.gg",
        "skool.com", "t.me", "wa.me", "bit.ly", "npmjs.com", "pypi.org", "example.com", "localhost.com"}
FILEEXT = {"js", "ts", "md", "py", "json"}
TURLER = [("3D/model", r"sketchfab|polyhaven|cgtrader|turbosquid|ambientcg|spline|3d|model|mixamo|blender"),
          ("ikon/font/görsel", r"font|icon|unsplash|pexels|svg|illustr|lottie|image|photo|logo"),
          ("ilham galerisi", r"awwwards|dribbble|godly|mobbin|refero|behance|land-book|gallery|saaslandingpage|siteinspire|inspiration|deck\.|design"),
          ("component/animasyon kütüphanesi", r"21st|codrops|tympanus|aceternity|magicui|shadcn|ui\.|gsap|motion|framer|animat|component|reactbits|uiverse|codepen|transition"),
          ("şablon", r"template|theme|themeforest|webflow|framer\.|wix|squarespace"),
          ("araç/üretici", r"\.ai$|\.app$|\.tools$|generat|builder|studio|lovable|v0\.|bolt|replit|vercel|netlify|cursor"),
          ("eğitim/nasıl yapılır", r"learn|course|academy|tutorial|docs|school|okul|edu")]


def tur(d):
    for ad, rx in TURLER:
        if re.search(rx, d, re.I):
            return ad
    return "belirsiz"


def temiz(h):
    h = h.lower().rstrip(".")
    h = re.sub(r"^www\.", "", h)
    return h


def gecerli(h):
    if h in SKIP or h.split(".")[-1] in FILEEXT:
        return False
    if any(h.endswith("." + s) for s in ("youtube.com", "github.com", "instagram.com")):
        return False
    lab = h.split(".")[0]
    return len(lab) >= 3 and not lab.isdigit()


site = defaultdict(lambda: {"vid": set(), "ctx": "", "url": "", "kay": set()})


def ekle(h, url, vid, ctx):
    h = temiz(h)
    if not gecerli(h):
        return
    s = site[h]
    s["vid"].add(vid)
    s["kay"].add(ctx.split(":")[0] if ctx else "liste")
    if not s["ctx"] and ctx:
        s["ctx"] = re.sub(r"\s+", " ", ctx).strip()[:140]
    if url and (not s["url"] or len(url) < len(s["url"])):
        s["url"] = url


for f in sorted(DERIN.glob("*.json")):
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    vid = d.get("kod", f.stem)
    for l in d.get("linkler") or []:
        for m in RX.finditer(str(l)):
            ekle(m.group(1), "", vid, "bağlantı")
    for e in d.get("ekran") or []:
        t = str(e.get("t", "")) if isinstance(e, dict) else str(e)
        for m in RX.finditer(t):
            ekle(m.group(1), "", vid, "ekran: " + t)
    for seg in d.get("transkript") or []:
        t = str(seg.get("t", "")) if isinstance(seg, dict) else str(seg)
        for m in RX.finditer(t):
            ekle(m.group(1), "", vid, "konuşma: " + t)
    for m in RX.finditer(str((d.get("meta") or {}).get("aciklama", ""))):
        ekle(m.group(1), "", vid, "açıklama")

# mevcut liste (tekrar yok, birleştir)
with open(R / "docs/site-inceleme/liste.tsv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        a = temiz(r["alan"])
        if gecerli(a):
            s = site[a]
            s["vid"].add(r["video id"])
            s["kay"].add("liste")
            s["ctx"] = s["ctx"] or r["neden ilginç"]

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["ad", "url", "videolar", "baglam", "tur", "ucretsiz", "erisim", "kaynak"])
    for h in sorted(site):
        s = site[h]
        w.writerow([h, "https://" + h, ",".join(sorted(s["vid"])), s["ctx"], tur(h), "", "", "+".join(sorted(s["kay"]))])
print(len(site), "site ->", OUT)
