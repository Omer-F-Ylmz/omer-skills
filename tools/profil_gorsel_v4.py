"""PROFIL-GORSEL-1 tur5: özgün vektör işaretler (AI raster yok); 48px kapısı + kontur >= 40px@1080.
FAD: 'D' harfinin altından düşen piksel. CW: tam kareye yayılan gravür/linocut ışın + anahtar deliği.
Kullanim: python tools/profil_gorsel_v4.py -> <marka>/v4/"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from profil_gorsel import MS, PAL, BR, OUT, font, fit_text, spaced, background, circle_crop
from profil_gorsel_v3 import profile, inter

SS = 2  # süper örnekleme (1600 -> 3200)


def mark_fad():
    p = PAL["free-ai-drop"]; S = MS * SS; u = S / 1600
    m = Image.new("L", (S, S), 0); d = ImageDraw.Draw(m)
    x0, top, bot, T = 330, 140, 1120, 200; R = (bot - top) // 2; cy = (top + bot) // 2; sx = 330
    def D(draw, a, b, c, e, f, fill):
        draw.rectangle([a * u, b * u, c * u, e * u], fill=fill); draw.pieslice([(c - f) * u, (cy - f) * u, (c + f) * u, (cy + f) * u], -90, 90, fill=fill)
    D(d, x0, top, x0 + sx, bot, R, 255)
    D(d, x0 + T, top + T, x0 + sx, bot - T, R - T, 0)
    nx0, nx1 = x0 + 330, x0 + 560                      # alt çubukta delik (piksel buradan düşer)
    body = np.array(m.resize((MS, MS), Image.LANCZOS)).astype("float32") / 255
    lime = np.array(p["lime"], "float32")
    arr = np.zeros((MS, MS, 4), "float32"); arr[..., :3] = lime; arr[..., 3] = body * 255
    lay = Image.fromarray(arr.astype("uint8"), "RGBA")
    sq = Image.new("RGBA", (S, S), (0, 0, 0, 0)); sd = ImageDraw.Draw(sq)
    cxp = x0 + T + 150; s = 150; cb = bot - T - 30     # counter içinde düşen piksel + sönen iz
    for k, a in enumerate([230, 140, 70]):
        sd.rectangle([(cxp - s // 2) * u, (cb - s - (k + 1) * 105) * u, (cxp + s // 2) * u, (cb - s - (k + 1) * 105 + 70) * u], fill=p["white"] + (a,))
    sd.rectangle([(cxp - s // 2) * u, (cb - s) * u, (cxp + s // 2) * u, cb * u], fill=p["white"] + (255,))
    sq = sq.resize((MS, MS), Image.LANCZOS)
    out = Image.new("RGBA", (MS, MS), (0, 0, 0, 0)); out.alpha_composite(lay); out.alpha_composite(sq)
    bb = out.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox(); c = out.crop(bb)
    c = c.resize((int(c.width * 0.9), int(c.height * 0.9)), Image.LANCZOS)
    fin = Image.new("RGBA", (MS, MS), (0, 0, 0, 0)); fin.alpha_composite(c, ((MS - c.width) // 2, (MS - c.height) // 2))
    halo = fin.getchannel("A").filter(ImageFilter.GaussianBlur(MS * 0.02))
    hl = Image.new("RGBA", (MS, MS), p["lime2"] + (0,)); hl.putalpha(halo.point(lambda v: int(v * 0.2)))
    return Image.alpha_composite(hl, fin)


def mark_cw():
    p = PAL["curiosity-well"]; S = MS * SS; u = S / 1600; cx, cy = S / 2, S * 0.5
    im = Image.new("RGB", (S, S), p["deep"]); d = ImageDraw.Draw(im, "RGBA")
    N = 18
    for i in range(N):                                   # linocut ışınları: dar-geniş dönüşümlü
        a0 = 2 * math.pi * i / N; w = (0.62 if i % 2 == 0 else 0.30) * 2 * math.pi / N
        R = S * (0.95 if i % 2 == 0 else 0.62)
        pts = [(cx, cy)] + [(cx + R * math.cos(a0 + w * t / 8), cy + R * math.sin(a0 + w * t / 8)) for t in range(9)]
        d.polygon(pts, fill=p["amber"] + (255 if i % 2 == 0 else 190,))
    for r, wd in [(300, 10), (430, 8), (560, 6)]:       # gravür halkaları (koyu çizgi, ışınları keser)
        d.ellipse([cx - r * u, cy - r * u, cx + r * u, cy + r * u], outline=p["deep"] + (255,), width=int(wd * u))
    d.ellipse([cx - 330 * u, cy - 330 * u, cx + 330 * u, cy + 330 * u], fill=p["deep"] + (255,))
    d.ellipse([cx - 308 * u, cy - 308 * u, cx + 308 * u, cy + 308 * u], fill=p["amber2"] + (255,))  # sıcak çekirdek
    hr = 120 * u; hy = cy - 95 * u                      # anahtar deliği: koyu şekil
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=p["deep"] + (255,))
    d.polygon([(cx - 62 * u, hy + 60 * u), (cx + 62 * u, hy + 60 * u), (cx + 110 * u, cy + 245 * u), (cx - 110 * u, cy + 245 * u)], fill=p["deep"] + (255,))
    return im.resize((MS, MS), Image.LANCZOS).convert("RGBA")


def circ(mk):
    m = Image.new("L", (MS * 2, MS * 2), 0); ImageDraw.Draw(m).ellipse([0, 0, MS * 2 - 1, MS * 2 - 1], fill=255)
    o = mk.copy(); o.putalpha(Image.composite(o.getchannel("A"), Image.new("L", (MS, MS), 0), m.resize((MS, MS), Image.LANCZOS))); return o


MARKS = {"free-ai-drop": mark_fad, "curiosity-well": mark_cw}
SCALE = {"free-ai-drop": 1.0, "curiosity-well": 1.0}


def profile4(brand, mk):
    S = 1080; bg = background(brand, S, S, focus=(0.5, 0.45)).convert("RGBA"); k = SCALE[brand]
    m = mk.resize((int(S * k),) * 2, Image.LANCZOS); bg.alpha_composite(m, ((S - m.width) // 2, (S - m.height) // 2)); return bg


def banner(brand, mk):
    W, H = 2560, 1440; b = BR[brand]; p = PAL[brand]
    im = background(brand, W, H, seed=11, focus=(0.30, 0.5))
    sx0, sy0, sw, sh = 507, 508, 1546, 423
    D = 600; cx = sx0 + 20 + D // 2
    im.alpha_composite(mk.resize((D, D), Image.LANCZOS), (cx - D // 2, H // 2 - D // 2))
    tx = cx + D // 2 + 70; tw = sx0 + sw - tx + 60
    lines = ["CURIOSITY", "WELL"] if brand == "curiosity-well" else ["FREE AI DROP"]
    sh_ = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh_).ellipse([tx - 200, H // 2 - 260, tx + tw + 200, H // 2 + 260], fill=p['ink'] + (200,)); im.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(160)))
    d = ImageDraw.Draw(im)
    fs = [fit_text(d, ln, b["fname"], b["var"], tw, 230, b["track"]) for ln in lines]
    f = min((x[0] for x in fs), key=lambda x: x.size)
    f2, _ = fit_text(d, b["slogan"], b["sfname"], b["svar"], tw, 78, 1)
    y = H // 2 - (int(f.size * 1.05) * len(lines) + 40 + int(f2.size * 1.2)) // 2 - int(f.size * 0.1)
    for ln in lines:
        spaced(im, (tx, y), ln, f, b["c1"] + (255,), b["track"]); y += int(f.size * 1.05)
    y += 8; d.rectangle([tx, y, tx + 120, y + 7], fill=b["c2"] + (255,))
    spaced(im, (tx, y + 26), b["slogan"], f2, b["sl"] + (255,), 1)
    return im.convert("RGB")


def shorts(brand, mk, ornek=True, log=None):
    W, H = 1080, 1920; b = BR[brand]; p = PAL[brand]
    im = background(brand, W, H, seed=21, focus=(0.5, 0.38)); boxes = {}; d = ImageDraw.Draw(im)
    lines = (["THIS FREE AI", "TOOL REPLACES", "A $20 APP"] if brand == "free-ai-drop" else ["WHY DID THE", "ANCIENT WELL", "NEVER RUN DRY?"])
    if not ornek:
        lines = ["YOUR TITLE", "GOES HERE", "(3 LINES MAX)"]
    fname = "impact.ttf" if brand == "free-ai-drop" else "georgiab.ttf"
    ft, _ = fit_text(d, max(lines, key=len), fname, None, 780, 112, 2)
    top = 260; ly = top + 230; lh = int(ft.size * 1.16); bot = ly + lh * len(lines) + 40
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle([60, top, 1020, bot], radius=44, fill=(0, 0, 0, 160), outline=b["c2"] + (210,), width=4)
    im.alpha_composite(L)
    im.alpha_composite(mk.resize((150, 150), Image.LANCZOS), (96, top + 36)); boxes["logo"] = (96, top + 36, 246, top + 186)
    f1 = font(b["fname"], 48, b["var"]); f2 = font(b["sfname"], 40, b["svar"]); tag = "DAY 01" if brand == "free-ai-drop" else "EPISODE 01"
    spaced(im, (270, top + 56), b["name"], f1, b["c1"] + (255,), 5); boxes["ad"] = (270, top + 66, 270 + int(d.textlength(b["name"], font=f1)) + 5 * len(b["name"]), top + 112)
    spaced(im, (272, top + 126), tag, f2, b["c2"] + (255,), 4); boxes["etiket"] = (272, top + 122, 272 + int(d.textlength(tag, font=f2)) + 16, top + 158)
    for i, ln in enumerate(lines):
        spaced(im, (96, ly), ln, ft, (b["c2"] if i == 2 else b["c1"]) + (255,), 2)
        boxes[f"satir{i}"] = (96, ly, 96 + int(d.textlength(ln, font=ft)) + 2 * len(ln), ly + ft.size); ly += lh
    ph = (60, bot + 50, 1020, 1440)                       # b-roll alanı: kart ile aynı 60/60 marj
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(L); ld.rounded_rectangle(ph, radius=36, fill=(255, 255, 255, 18))
    im.alpha_composite(L); boxes["yer"] = ph
    anch = "NEW EVERY DAY" if brand == "free-ai-drop" else "NEW EVERY WEEK"; fa = font(b["fname"], 48, b["var"]); aw = int(d.textlength(anch, font=fa)) + 3 * len(anch)
    spaced(im, ((W - aw) // 2, 1472), anch, fa, b["c1"] + (255,), 3); boxes["cipa-yazi"] = ((W - aw) // 2, 1472, (W + aw) // 2, 1472 + 58)
    bad = [(a, c) for i, a in enumerate(boxes) for c in list(boxes)[i + 1:] if inter(boxes[a], boxes[c])]
    if log is not None:
        log[f"{brand}-{'ornek' if ornek else 'bos'}"] = {"kesisim": bad, "kart_marj_sol_sag": (60, W - 1020), "alt_bosluk_px": H - max(v[3] for v in boxes.values()), "max_alt_y": max(v[3] for v in boxes.values())}
    return im.convert("RGB")


def main():
    log = {}
    for br, fn in MARKS.items():
        base = os.path.join(OUT, br, "v4"); os.makedirs(base, exist_ok=True)
        mk = fn(); mk.save(os.path.join(base, "isaret-1600.png")); mkc = circ(mk) if br == "curiosity-well" else mk
        pf = profile4(br, mk); pf.convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
        banner(br, mkc).save(os.path.join(base, "kanal-afisi-2560x1440.png"))
        shorts(br, mkc, True, log).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
        shorts(br, mkc, False, log).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
        sh = Image.new("RGB", (560, 400), (235, 235, 235))
        sh.paste(circle_crop(pf, 360), (10, 20)); sh.paste(circle_crop(pf, 110), (390, 20)); sh.paste(circle_crop(pf, 48), (390, 160))
        sh.save(os.path.join(base, "_kucuk-boyut.png")); print(br, "ok")
    open(os.path.join(OUT, "cakisma-testi-v4.json"), "w", encoding="utf-8").write(json.dumps(log, indent=1)); print(json.dumps(log))


if __name__ == "__main__":
    main()
