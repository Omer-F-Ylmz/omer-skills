import argparse, io, json, math, os, shutil, subprocess, sys, unicodedata, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont

API = "https://cbsapi.tkgm.gov.tr/megsiswebapi.v3.1/api"
IL_LISTE = "https://parselsorgu.tkgm.gov.tr/app/modules/administrativeQuery/data/ilListe.json"
TILE = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Accept": "application/json"}


def get(url, raw=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        b = r.read()
    return b if raw else json.loads(b.decode("utf-8"))


def norm(s):
    s = (s or "").replace("İ", "i").replace("I", "ı").lower()
    s = s.translate(str.maketrans("çğıöşü", "cgiosu"))
    return "".join(c for c in unicodedata.normalize("NFKD", s) if c.isalnum())


def pick(features, name, what):
    n = norm(name)
    rows = [(f.get("properties") or {}) for f in features.get("features", [])]
    exact = [p for p in rows if norm(p.get("text")) == n]
    part = [p for p in rows if n in norm(p.get("text"))]
    hit = exact or part
    if not hit:
        sys.exit(f"{what} bulunamadı: {name}. Seçenekler: " + ", ".join(sorted(p.get('text', '') for p in rows))[:600])
    return hit[0]["id"]


def parsel_feature(a):
    if a.geojson:
        d = json.load(open(a.geojson, encoding="utf-8"))
        return d["features"][0] if d.get("type") == "FeatureCollection" else d
    if a.latlng:
        lat, lng = a.latlng.split(",")
        return get(f"{API}/parsel/{lat.strip()}/{lng.strip()}/")
    mah = a.mahalle_kodu
    if not mah:
        il = pick(get(IL_LISTE), a.il, "İl")
        ilce = pick(get(f"{API}/idariYapi/ilceListe/{il}"), a.ilce, "İlçe")
        mah = pick(get(f"{API}/idariYapi/mahalleListe/{ilce}"), a.mahalle, "Mahalle")
    d = get(f"{API}/parsel/{mah}/{a.ada}/{a.parsel}")
    if d.get("Message"):
        sys.exit("TKGM: " + d["Message"])
    return d


def ring_of(feat):
    g = feat["geometry"]
    return g["coordinates"][0] if g["type"] == "Polygon" else g["coordinates"][0][0]


def ll2px(lat, lng, z):
    s = math.sin(math.radians(lat))
    n = 256 * 2 ** z
    return (lng + 180) / 360 * n, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n


def mosaic(ring, z, pad_px):
    pts = [ll2px(lat, lng, z) for lng, lat in ring]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    half = max(max(xs) - min(xs), max(ys) - min(ys)) / 2 + pad_px
    x0, y0, x1, y1 = cx - half, cy - half, cx + half, cy + half
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    img = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    total = (tx1 - tx0 + 1) * (ty1 - ty0 + 1)
    k = 0
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            k += 1
            try:
                t = Image.open(io.BytesIO(get(TILE.format(z=z, x=tx, y=ty), raw=True))).convert("RGB")
                img.paste(t, ((tx - tx0) * 256, (ty - ty0) * 256))
            except Exception:
                pass
            print(f"\ruydu karo {k}/{total}", end="", file=sys.stderr)
    print(file=sys.stderr)
    off = (tx0 * 256, ty0 * 256)
    local = [(x - off[0], y - off[1]) for x, y in pts]
    return img, local, (cx - off[0], cy - off[1]), half


def draw_parcel(img, poly, center, half):
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon(poly, fill=(255, 214, 0, 55))
    w = max(4, int(half / 60))
    d.line(poly + [poly[0]], fill=(255, 214, 0, 255), width=w, joint="curve")
    r = half * 0.62
    for i in range(0, 360, 12):
        a0, a1 = math.radians(i), math.radians(i + 6)
        d.arc([center[0] - r, center[1] - r, center[0] + r, center[1] + r], i, i + 6, fill=(255, 214, 0, 200), width=max(2, w // 2))
    return img


def font(sz):
    for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def ease(t):
    return t * t * (3 - 2 * t)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--il"); p.add_argument("--ilce"); p.add_argument("--mahalle")
    p.add_argument("--mahalle-kodu"); p.add_argument("--ada"); p.add_argument("--parsel")
    p.add_argument("--latlng"); p.add_argument("--geojson")
    p.add_argument("--zoom", type=int, default=18)
    p.add_argument("--sure", type=float, default=8.0)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--dikey", action="store_true")
    p.add_argument("--aci", type=float, default=90.0)
    p.add_argument("--baslik", default="")
    p.add_argument("--cikti", default="parsel.mp4")
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg yok")
    feat = parsel_feature(a)
    props = feat.get("properties") or {}
    ring = ring_of(feat)
    W, H = (1080, 1920) if a.dikey else (1920, 1080)
    big, poly, c, half = mosaic(ring, a.zoom, pad_px=900)
    big = draw_parcel(big, poly, c, half)
    json.dump(feat, open(os.path.splitext(a.cikti)[0] + ".geojson", "w", encoding="utf-8"), ensure_ascii=False)
    n = int(a.sure * a.fps)
    diag = math.hypot(W, H)
    f_big, f_small = font(int(W * 0.045)), font(int(W * 0.022))
    title = a.baslik or f"{props.get('mahalleAd', a.mahalle or '')} · Ada {props.get('adaNo', a.ada)} Parsel {props.get('parselNo', a.parsel)}"
    alan = props.get("alan")
    sub = f"{alan} m²" if alan else ""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.cikti]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    view_far, view_near = half * 2.6, half * 1.25
    for i in range(n):
        t = ease(i / max(1, n - 1))
        view = view_far + (view_near - view_far) * t
        side = view * diag / min(W, H)
        box = (int(c[0] - side / 2), int(c[1] - side / 2), int(c[0] + side / 2), int(c[1] + side / 2))
        crop = big.crop(box).rotate(a.aci * t, resample=Image.BICUBIC)
        k = min(W, H) / view
        crop = crop.resize((int(crop.width * k), int(crop.height * k)), Image.BILINEAR)
        l, u = (crop.width - W) // 2, (crop.height - H) // 2
        fr = crop.crop((l, u, l + W, u + H))
        d = ImageDraw.Draw(fr, "RGBA")
        d.rectangle([0, H - int(H * 0.16), W, H], fill=(0, 0, 0, 120))
        d.text((int(W * 0.05), H - int(H * 0.135)), title, font=f_big, fill="white")
        if sub:
            d.text((int(W * 0.05), H - int(H * 0.07)), sub, font=f_small, fill=(255, 214, 0))
        d.text((W - int(W * 0.25), H - int(H * 0.035)), "© Esri, TKGM", font=f_small, fill=(255, 255, 255, 180))
        ff.stdin.write(fr.tobytes())
        print(f"\rkare {i + 1}/{n}", end="", file=sys.stderr)
    ff.stdin.close(); ff.wait()
    print(f"\n{a.cikti}", file=sys.stderr)


if __name__ == "__main__":
    main()
