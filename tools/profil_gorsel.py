"""PROFIL-GORSEL-1: iki marka icin profil/afis/kapak seti (PIL + numpy, yerel, ucretsiz).
Kullanim: python tools/profil_gorsel.py <onizleme|uret> [marka] [yon]"""
import math, sys, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

OUT = r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-oto\marka"
FD = "C:/Windows/Fonts/"
MS = 1600  # isaret tuvali

PAL = {
    "free-ai-drop": dict(ink=(8, 10, 28), ink2=(30, 16, 84), glow=(104, 64, 255), lime=(200, 255, 46),
                         lime2=(70, 255, 168), white=(244, 247, 255), hot=(255, 79, 123)),
    "curiosity-well": dict(ink=(7, 11, 36), ink2=(12, 70, 86), glow=(255, 181, 71), amber=(255, 181, 71),
                           amber2=(255, 233, 160), cream=(255, 243, 214), teal=(20, 110, 124), deep=(3, 5, 18)),
}


def font(name, size, var=None):
    f = ImageFont.truetype(FD + name, size)
    if var:
        try:
            f.set_variation_by_name(var)
        except Exception:
            pass
    return f


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(size, c1, c2, mask):
    w, h = size
    t = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(c1)[None, None, :] * (1 - t) + np.array(c2)[None, None, :] * t) * np.ones((h, w, 1))
    im = Image.fromarray(arr.astype("uint8"), "RGB").convert("RGBA")
    im.putalpha(mask)
    return im


# ---------------------------------------------------------------- arka plan
def background(brand, w, h, seed=7, focus=(0.5, 0.5)):
    rng = np.random.default_rng(seed)
    p = PAL[brand]
    yy, xx = np.mgrid[0:h, 0:w].astype("float32")
    d = (xx / w * 0.4 + yy / h * 0.6)[..., None]
    arr = np.array(p["ink"])[None, None, :] * (1 - d) + np.array(p["ink2"])[None, None, :] * d
    fx, fy = focus[0] * w, focus[1] * h
    r = np.sqrt((xx - fx) ** 2 + (yy - fy) ** 2) / (0.62 * max(w, h))
    g = np.exp(-(r ** 2) * 2.2)[..., None]
    arr = arr + g * np.array(p["glow"])[None, None, :] * (0.42 if brand == "free-ai-drop" else 0.30)
    im = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB").convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    if brand == "free-ai-drop":  # dusen cizgiler + soluk izgara
        col = p["lime"]
        for _ in range(int(w * h / 26000)):
            x = rng.uniform(0, w); y = rng.uniform(-0.1, 1) * h; L = rng.uniform(0.04, 0.22) * h
            a = int(rng.uniform(28, 120)); wd = max(2, int(w / 540 * rng.uniform(0.8, 2.2)))
            for k in range(8):
                dr.line([(x, y + L * k / 8), (x, y + L * (k + 1) / 8)], fill=col + (int(a * (k + 1) / 8),), width=wd)
            dr.ellipse([x - wd, y + L - wd, x + wd, y + L + wd], fill=col + (min(255, a + 60),))
        gs = int(w / 18)
        for gx in range(0, w, gs):
            dr.line([(gx, 0), (gx, h)], fill=p["white"] + (10,), width=1)
        for gy in range(0, h, gs):
            dr.line([(0, gy), (w, gy)], fill=p["white"] + (10,), width=1)
    else:  # kuyu halkalari + toz
        for k in range(1, 15):
            rr = k * 0.075 * max(w, h)
            dr.ellipse([fx - rr, fy - rr * 0.62, fx + rr, fy + rr * 0.62],
                       outline=p["amber"] + (int(70 / (1 + k * 0.35)),), width=max(2, int(w / 700)))
        for _ in range(int(w * h / 9000)):
            x = rng.uniform(0, w); y = rng.uniform(0, h); s = rng.uniform(1, 3.4) * w / 1080
            dr.ellipse([x - s, y - s, x + s, y + s], fill=p["amber2"] + (int(rng.uniform(40, 190)),))
    lay = lay.filter(ImageFilter.GaussianBlur(max(1, w / 1500)))
    im = Image.alpha_composite(im, lay)
    noise = rng.normal(0, 4.5, (h, w, 1))
    a = np.array(im).astype("float32"); a[..., :3] += noise
    # vinyet
    v = 1 - 0.38 * np.clip(r - 0.35, 0, 1)[..., None]
    a[..., :3] *= v
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"), "RGBA")


# ---------------------------------------------------------------- isaretler
def _canvas():
    im = Image.new("RGBA", (MS, MS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def _glow(im, color, rad, boost=1.0):
    g = im.filter(ImageFilter.GaussianBlur(rad))
    a = np.array(g).astype("float32"); a[..., 3] *= boost
    g = Image.fromarray(np.clip(a, 0, 255).astype("uint8"), "RGBA")
    return Image.alpha_composite(g, im)


def astroid(cx, cy, R, n=80, k=3):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        pts.append((cx + R * math.copysign(abs(math.cos(t)) ** k, math.cos(t)),
                    cy + R * math.copysign(abs(math.sin(t)) ** k, math.sin(t))))
    return pts


def mark_a1():
    p = PAL["free-ai-drop"]; S = MS
    cx, cy, r = S / 2, S * 0.60, S * 0.285
    tip = (cx, S * 0.10); d = cy - tip[1]; ang = math.acos(r / d)
    base = -math.pi / 2
    t1 = (cx + r * math.cos(base - ang), cy + r * math.sin(base - ang))
    t2 = (cx + r * math.cos(base + ang), cy + r * math.sin(base + ang))
    m = Image.new("L", (S, S), 0); md = ImageDraw.Draw(m)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    md.polygon([tip, t1, t2], fill=255)
    md.polygon(astroid(cx, cy + r * 0.12, r * 0.62), fill=0)  # kıvılcım oyuk
    lay, ld = _canvas()
    for i, (k, a) in enumerate([(1.0, 255), (1.32, 140), (1.68, 70)]):  # dalga halkaları
        ew, eh = S * 0.30 * k, S * 0.062 * k
        yc = S * 0.915
        ld.ellipse([cx - ew, yc - eh, cx + ew, yc + eh], outline=p["glow"][:3] + (a,) if i else p["lime"] + (a,), width=int(S * 0.016))
    drop = vgrad((S, S), p["lime"], p["lime2"], m)
    out = Image.alpha_composite(lay, _glow(drop, p["lime"], S * 0.03, 0.9))
    return out


def mark_a2():
    p = PAL["free-ai-drop"]; S = MS
    im, d = _canvas(); cx = S / 2
    # paraşüt
    m = Image.new("L", (S, S), 0); md = ImageDraw.Draw(m)
    md.pieslice([cx - S * 0.40, S * 0.10, cx + S * 0.40, S * 0.10 + S * 0.62], 180, 360, fill=255)
    for i, x in enumerate([-0.40, -0.133, 0.133]):  # etek tırtığı
        md.ellipse([cx + S * x, S * 0.41, cx + S * (x + 0.267), S * 0.51], fill=0)
    md.rectangle([cx - S * 0.42, S * 0.43, cx + S * 0.42, S * 0.50], fill=0)
    md.ellipse([cx - S * 0.40, S * 0.40, cx - S * 0.133, S * 0.50], fill=255)
    md.ellipse([cx - S * 0.133, S * 0.40, cx + S * 0.133, S * 0.50], fill=255)
    md.ellipse([cx + S * 0.133, S * 0.40, cx + S * 0.40, S * 0.50], fill=255)
    chute = vgrad((S, S), p["lime"], p["lime2"], m)
    for x0 in (-0.36, 0.0, 0.36):
        d.line([(cx + S * x0, S * 0.45), (cx + S * x0 * 0.45, S * 0.66)], fill=p["white"] + (255,), width=int(S * 0.014))
    d.rounded_rectangle([cx - S * 0.19, S * 0.66, cx + S * 0.19, S * 0.90], radius=int(S * 0.03), fill=p["white"] + (255,))
    d.rectangle([cx - S * 0.19, S * 0.755, cx + S * 0.19, S * 0.795], fill=p["glow"] + (255,))
    d.polygon(astroid(cx, S * 0.775, S * 0.05), fill=p["ink"] + (255,))
    return _glow(Image.alpha_composite(chute, im), p["lime"], S * 0.03, 0.8)


def mark_a3():
    p = PAL["free-ai-drop"]; S = MS
    m = Image.new("L", (S, S), 0); md = ImageDraw.Draw(m)
    x0, y0, x1, y1 = S * 0.20, S * 0.14, S * 0.80, S * 0.86
    rr = (y1 - y0) / 2
    md.rectangle([x0, y0, x1 - rr, y1], fill=255)
    md.pieslice([x1 - 2 * rr, y0, x1, y1], -90, 90, fill=255)
    t = S * 0.17  # iç boşluk
    md.rectangle([x0 + t, y0 + t, x1 - rr - 0, y1 - t], fill=0)
    md.pieslice([x1 - 2 * rr + t, y0 + t, x1 - t, y1 - t], -90, 90, fill=0)
    base = _glow(vgrad((S, S), p["lime"], p["lime2"], m), p["lime"], S * 0.03, 0.9)
    cx, cy = S * 0.50, S * 0.50
    ar = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ad = ImageDraw.Draw(ar)
    ad.polygon([(cx - S * 0.075, cy - S * 0.20), (cx + S * 0.075, cy - S * 0.20), (cx + S * 0.075, cy - S * 0.02),
                (cx + S * 0.16, cy - S * 0.02), (cx, cy + S * 0.20), (cx - S * 0.16, cy - S * 0.02),
                (cx - S * 0.075, cy - S * 0.02)], fill=p["white"] + (255,))
    return Image.alpha_composite(base, ar)


def mark_b1():
    p = PAL["curiosity-well"]; S = MS
    cx, cy = S / 2, S * 0.52
    def almond(w, h, n=120):
        pts = [(cx + w * math.cos(math.pi * i / n), cy - h * math.sin(math.pi * i / n) ** 1.15) for i in range(n + 1)]
        pts += [(cx + w * math.cos(math.pi + math.pi * i / n), cy + h * math.sin(math.pi * i / n) ** 1.15) for i in range(n + 1)]
        return pts
    im, d = _canvas()
    # ışınlar (üstte)
    for k in range(-3, 4):
        a = -math.pi / 2 + k * 0.30
        d.line([(cx + S * 0.33 * math.cos(a), cy + S * 0.33 * math.sin(a) - S * 0.12),
                (cx + S * 0.45 * math.cos(a), cy + S * 0.45 * math.sin(a) - S * 0.12)],
               fill=p["amber"] + (255,), width=int(S * 0.025))
    d.polygon(almond(S * 0.47, S * 0.27), fill=p["amber"] + (255,))
    d.polygon(almond(S * 0.405, S * 0.20), fill=p["deep"] + (255,))
    ir = S * 0.175
    m = Image.new("L", (S, S), 0); md = ImageDraw.Draw(m)
    md.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=255)
    iris = vgrad((S, S), p["amber2"], p["amber"], m)
    im = Image.alpha_composite(im, iris); d = ImageDraw.Draw(im)
    pr = S * 0.062
    d.ellipse([cx - pr, cy - S * 0.045 - pr, cx + pr, cy - S * 0.045 + pr], fill=p["deep"] + (255,))
    d.polygon([(cx - S * 0.03, cy - S * 0.03), (cx + S * 0.03, cy - S * 0.03), (cx + S * 0.062, cy + S * 0.115),
               (cx - S * 0.062, cy + S * 0.115)], fill=p["deep"] + (255,))
    return _glow(im, p["amber"], S * 0.03, 0.8)


def mark_b2():
    p = PAL["curiosity-well"]; S = MS
    cx = S / 2
    im, d = _canvas()
    n = 9
    for i in range(n):
        t = i / (n - 1)
        w = S * (0.46 - 0.40 * t ** 0.9); h = w * 0.62
        yc = S * (0.42 + 0.17 * t)
        col = lerp(p["amber"], p["deep"], min(1, t * 1.15)) if i == 0 else lerp(p["teal"], p["deep"], t ** 0.8)
        d.ellipse([cx - w, yc - h, cx + w, yc + h], fill=col + (255,))
        d.ellipse([cx - w * 0.92, yc - h * 0.92 + S * 0.012, cx + w * 0.92, yc + h * 0.92 + S * 0.012],
                  fill=lerp(p["teal"], p["deep"], t ** 0.8) + (255,))
        if i < 6:
            d.ellipse([cx - w, yc - h, cx + w, yc + h], outline=p["amber2"] + (int(230 - t * 300),), width=int(S * 0.008))
    # yıldız/ışık dibinde
    star = Image.new("RGBA", (S, S), (0, 0, 0, 0)); sd = ImageDraw.Draw(star)
    sd.polygon(astroid(cx, S * 0.60, S * 0.085, k=3), fill=p["amber2"] + (255,))
    im = Image.alpha_composite(im, _glow(star, p["amber"], S * 0.04, 2.5))
    # kenar yıldız parıltısı
    return _glow(im, p["amber"], S * 0.02, 0.5)


def mark_b3():
    p = PAL["curiosity-well"]; S = MS
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx, cy = S / 2, S / 2
    w = int(S * 0.055)
    R = S * 0.20; bx, by = S * 0.50, S * 0.27
    d.ellipse([bx - R, by - R, bx + R, by + R], outline=p["amber"] + (255,), width=int(S * 0.07))
    d.polygon(astroid(bx, by, S * 0.115), fill=p["amber2"] + (255,))  # yuvada yıldız
    d.rectangle([bx - w / 2, by + R, bx + w / 2, S * 0.88], fill=p["amber"] + (255,))
    for yy, ln in ((0.70, 0.13), (0.79, 0.09)):
        d.rectangle([bx, S * yy, bx + S * ln, S * yy + w * 0.9], fill=p["amber"] + (255,))
    d.rectangle([bx - w / 2, S * 0.86, bx + S * 0.12, S * 0.86 + w * 0.9], fill=p["amber"] + (255,))
    return _glow(lay, p["amber"], S * 0.03, 0.8)


def sticker(lay, outline, w, shadow=None, off=0):
    S = lay.width; a = lay.getchannel("A")
    dil = a.filter(ImageFilter.GaussianBlur(w)).point(lambda v: 255 if v > 8 else 0)
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", lay.size, shadow + (255,)); sh.putalpha(ImageChops.offset(dil, off, off))
        out = Image.alpha_composite(out, sh)
    ol = Image.new("RGBA", lay.size, outline + (255,)); ol.putalpha(dil)
    return Image.alpha_composite(Image.alpha_composite(out, ol), lay)


def mark_a4():
    p = PAL["free-ai-drop"]; S = MS; cx = S / 2
    lay, d = _canvas()
    apex, by = S * 0.07, S * 0.50
    dm = Image.new("L", (S, S), 0); ImageDraw.Draw(dm).pieslice([cx - S * 0.43, apex, cx + S * 0.43, apex + 2 * (by - apex)], 180, 360, fill=255)
    lay.alpha_composite(vgrad((S, S), p["lime"], p["lime2"], dm))
    for side in (-1, 1):
        tm = Image.new("L", (S, S), 0)
        ImageDraw.Draw(tm).rectangle([min(cx + side * S * 0.15, cx + side * S), 0, max(cx + side * S * 0.15, cx + side * S), by], fill=255)
        lay.alpha_composite(vgrad((S, S), p["white"], (190, 205, 255), ImageChops.multiply(dm, tm)))
    d = ImageDraw.Draw(lay)
    for x0, x1 in ((-0.41, -0.17), (0.41, 0.17), (0.0, 0.0)):
        d.line([(cx + S * x0 * 0.98, by), (cx + S * x1, S * 0.70)], fill=p["white"] + (255,), width=int(S * 0.026))
    d.rounded_rectangle([cx - S * 0.23, S * 0.68, cx + S * 0.23, S * 0.97], radius=int(S * 0.04), fill=p["white"] + (255,))
    d.rectangle([cx - S * 0.04, S * 0.69, cx + S * 0.04, S * 0.95], fill=p["lime"] + (255,))
    d.rectangle([cx - S * 0.23, S * 0.79, cx + S * 0.23, S * 0.86], fill=p["lime"] + (255,))
    d.ellipse([cx - S * 0.15, S * 0.665, cx - S * 0.005, S * 0.75], fill=p["lime"] + (255,), outline=p["ink"] + (255,), width=int(S * 0.012))
    d.ellipse([cx + S * 0.005, S * 0.665, cx + S * 0.15, S * 0.75], fill=p["lime"] + (255,), outline=p["ink"] + (255,), width=int(S * 0.012))
    d.ellipse([cx - S * 0.04, S * 0.675, cx + S * 0.04, S * 0.755], fill=p["glow"] + (255,))
    return sticker(lay, p["ink"], S * 0.010)


def mark_b4():
    p = PAL["curiosity-well"]; S = MS
    cx, cy = S / 2, S * 0.54
    def almond(w, h, n=120):
        pts = [(cx + w * math.cos(math.pi * i / n), cy - h * math.sin(math.pi * i / n) ** 1.15) for i in range(n + 1)]
        pts += [(cx + w * math.cos(math.pi + math.pi * i / n), cy + h * math.sin(math.pi * i / n) ** 1.15) for i in range(n + 1)]
        return pts
    im, d = _canvas()
    d.polygon(almond(S * 0.48, S * 0.30), fill=p["amber"] + (255,))
    d.polygon(almond(S * 0.41, S * 0.225), fill=p["deep"] + (255,))
    R = S * 0.20
    for i in range(3):  # iris = kuyu kuyusu: kayan halkalar
        t = i / 2; r = R * (1 - 0.27 * i)
        col = p["amber2"] if i == 0 else lerp(p["teal"], p["deep"], t ** 0.7)
        if i == 1:
            col = p["amber"]
        d.ellipse([cx - r, cy - r + R * 0.07 * i, cx + r, cy + r + R * 0.07 * i], fill=col + (255,))
    st = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(st).polygon(astroid(cx, cy + R * 0.38, R * 0.30), fill=p["amber2"] + (255,))
    im = Image.alpha_composite(im, _glow(st, p["amber"], S * 0.02, 1.5))
    d = ImageDraw.Draw(im)
    d.polygon(astroid(S * 0.80, S * 0.17, S * 0.085), fill=p["amber2"] + (255,))
    return _glow(im, p["amber"], S * 0.025, 0.7)


MARKS = {"free-ai-drop": {"a1-damla-kivilcim": mark_a1, "a2-hava-droplu-kasa": mark_a2, "a4-droplu-hediye-kasa": mark_a4, "a3-d-ok": mark_a3},
         "curiosity-well": {"b1-anahtar-deligi-goz": mark_b1, "b4-goz-kuyu": mark_b4, "b2-kuyu-halkalari": mark_b2, "b3-anahtar-yildiz": mark_b3}}


def profile(brand, fn, size=1080):
    bg = background(brand, size, size, focus=(0.5, 0.5)).convert("RGBA")
    mk = fn().resize((int(size * 0.74), int(size * 0.74)), Image.LANCZOS)
    bg.alpha_composite(mk, ((size - mk.width) // 2, int(size * 0.13)))
    return bg


def circle_crop(im, size):
    im = im.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size * 4, size * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (20, 20, 20, 255)); out.paste(im, (0, 0), m)
    return out


def preview(brand):
    names = list(MARKS[brand]); sizes = [360, 110, 48]
    W = 380 * len(names); sheet = Image.new("RGB", (W, 640), (235, 235, 235))
    for i, n in enumerate(names):
        pf = profile(brand, MARKS[brand][n], 1080)
        x = i * 380 + 10
        sheet.paste(circle_crop(pf, 360), (x, 10))
        sheet.paste(circle_crop(pf, 110), (x + 20, 390))
        sheet.paste(circle_crop(pf, 48), (x + 170, 420))
        ImageDraw.Draw(sheet).text((x, 520), n, fill=(0, 0, 0), font=font("segoeui.ttf", 20))
    os.makedirs(OUT, exist_ok=True)
    pth = os.path.join(OUT, f"_onizleme-{brand}.png"); sheet.save(pth); return pth


# ---------------------------------------------------------------- yazi
def fit_text(draw, text, fname, var, maxw, start, track=0):
    s = start
    while s > 20:
        f = font(fname, s, var)
        w = sum(draw.textlength(c, font=f) + track for c in text) - track
        if w <= maxw:
            return f, w
        s -= 4
    return f, w


def spaced(img, xy, text, f, fill, track=0, anchor_h=None, glow=None):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x, y = xy
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    if glow:
        g = lay.filter(ImageFilter.GaussianBlur(img.width / 160)); a = np.array(g).astype("float32")
        a[..., :3] = glow; a[..., 3] *= 0.9
        img.alpha_composite(Image.fromarray(a.astype("uint8"), "RGBA"))
    img.alpha_composite(lay)


BR = {
    "free-ai-drop": dict(name="FREE AI DROP", slogan="One free AI tool. Every single day.", fname="bahnschrift.ttf", var="Bold",
                         sfname="bahnschrift.ttf", svar="Regular", track=6, c1=(244, 247, 255), c2=(200, 255, 46), sl=(200, 255, 46)),
    "curiosity-well": dict(name="CURIOSITY WELL", slogan="Drop a question into history & science.", fname="georgiab.ttf", var=None,
                           sfname="georgia.ttf", svar=None, track=10, c1=(255, 243, 214), c2=(255, 181, 71), sl=(255, 233, 160)),
}


def banner(brand, fn):
    W, H = 2560, 1440; b = BR[brand]
    im = background(brand, W, H, seed=11, focus=(0.30, 0.5))
    # guvenli alan 1546x423: x507..2053, y508..931
    sx0, sy0 = 507, 508
    mk = fn().resize((400, 400), Image.LANCZOS)
    im.alpha_composite(mk, (sx0 + 4, sy0 + 12))
    d = ImageDraw.Draw(im)
    tx = sx0 + 440; tw = 2053 - tx - 110
    f, w = fit_text(d, b["name"], b["fname"], b["var"], tw, 180, b["track"])
    spaced(im, (tx, sy0 + 40), b["name"], f, b["c1"] + (255,), b["track"], glow=b["c2"])
    f2, w2 = fit_text(d, b["slogan"], b["sfname"], b["svar"], tw, 90, 1)
    d.rectangle([tx, sy0 + 40 + int(f.size * 1.22), tx + 120, sy0 + 40 + int(f.size * 1.22) + 8], fill=b["c2"] + (255,))
    spaced(im, (tx, sy0 + 40 + int(f.size * 1.22) + 34), b["slogan"], f2, b["sl"] + (255,), 1)
    return im.convert("RGB")


def shorts(brand, fn, ornek=True):
    W, H = 1080, 1920; b = BR[brand]; OY = 230
    im = background(brand, W, H, seed=21, focus=(0.5, 0.36))
    d = ImageDraw.Draw(im)
    # baslik alani: x60..960 (sag UI 120px bos), y300..940 ; alt 380px bos
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([60, 330 + OY, 930, 1010 + OY], radius=44, fill=(0, 0, 0, 120), outline=b["c2"] + (200,), width=4)
    im.alpha_composite(panel)
    mk = fn().resize((150, 150), Image.LANCZOS)
    im.alpha_composite(mk, (96, 360 + OY))
    f1 = font(b["fname"], 40, b["var"])
    spaced(im, (270, 392 + OY), b["name"], f1, b["c1"] + (255,), 5)
    f1b = font(b["sfname"], 30, b["svar"])
    spaced(im, (272, 446 + OY), "DAY 01" if brand == "free-ai-drop" else "EPISODE 01", f1b, b["c2"] + (255,), 4)
    if ornek:
        lines = ["THIS FREE AI", "TOOL REPLACES", "A $20 APP"] if brand == "free-ai-drop" else \
                ["WHY DID THE", "ANCIENT WELL", "NEVER RUN DRY?"]
        fn_t = "impact.ttf" if brand == "free-ai-drop" else "georgiab.ttf"
        ft, _ = fit_text(d, max(lines, key=len), fn_t, None, 800, 112, 2)
        y = 570 + OY
        for i, ln in enumerate(lines):
            spaced(im, (96, y), ln, ft, (b["c2"] if i == 2 else b["c1"]) + (255,), 2, glow=b["c2"] if i == 2 else None)
            y += int(ft.size * 1.16)
    return im.convert("RGB")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "onizleme"
    if cmd == "onizleme":
        for br in MARKS:
            print(preview(br))
    else:
        brand, pick = sys.argv[2], sys.argv[3]
        for br, mk in MARKS.items():
            if br != brand:
                continue
            for name, fn in mk.items():
                sec = name.startswith(pick)
                base = os.path.join(OUT, br) if sec else os.path.join(OUT, br, "alternatif")
                os.makedirs(base, exist_ok=True)
                profile(br, fn).convert("RGB").save(os.path.join(base, f"profil-{name}-1080.png"))
                if sec:
                    banner(br, fn).save(os.path.join(base, "kanal-afisi-2560x1440.png"))
                    shorts(br, fn).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
                    shorts(br, fn, ornek=False).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
                    profile(br, fn).convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
                    print("secili:", br, name)


if __name__ == "__main__":
    main()
