"""PROFIL-GORSEL-1 tur3: roast-room kazananları (A düşen çip+kıvılcım, B kuyu içinden bakış). PIL, yerel.
Kullanim: python tools/profil_gorsel_v2.py   -> <marka>/v2/ altına yazar"""
import math, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
import profil_gorsel as P
from profil_gorsel import MS, PAL, BR, OUT, _canvas, _glow, vgrad, lerp, font, fit_text, spaced, background, circle_crop, astroid, sticker


def mark_a5():
    p = PAL["free-ai-drop"]; S = MS
    cx, cy = S * 0.5, S * 0.60
    lay, d = _canvas()
    # çip gövdesi
    B = S * 0.27
    for i in range(5):  # pimler
        o = -B * 0.62 + i * B * 0.31
        for sx in (-1, 1):
            d.rounded_rectangle([cx + sx * B * 1.0 - (S * 0.05 if sx < 0 else 0) + (0 if sx < 0 else 0), cy + o - S * 0.014,
                                 cx + sx * B * 1.0 + (0 if sx < 0 else S * 0.05), cy + o + S * 0.014], radius=6, fill=p["white"] + (255,))
        d.rounded_rectangle([cx + o - S * 0.014, cy - B * 1.0 - S * 0.05, cx + o + S * 0.014, cy - B * 1.0], radius=6, fill=p["white"] + (255,))
        d.rounded_rectangle([cx + o - S * 0.014, cy + B * 1.0, cx + o + S * 0.014, cy + B * 1.0 + S * 0.05], radius=6, fill=p["white"] + (255,))
    bm = Image.new("L", (S, S), 0); ImageDraw.Draw(bm).rounded_rectangle([cx - B, cy - B, cx + B, cy + B], radius=int(S * 0.06), fill=255)
    lay.alpha_composite(vgrad((S, S), p["lime"], p["lime2"], bm))
    d = ImageDraw.Draw(lay)
    # hediye kurdelesi (çip üstünde çapraz değil, düz çift bant) + AI çekirdeği
    d.rectangle([cx - S * 0.035, cy - B, cx + S * 0.035, cy + B], fill=p["white"] + (255,))
    d.rectangle([cx - B, cy - S * 0.035, cx + B, cy + S * 0.035], fill=p["white"] + (255,))
    d.rounded_rectangle([cx - S * 0.10, cy - S * 0.10, cx + S * 0.10, cy + S * 0.10], radius=int(S * 0.03), fill=p["ink"] + (255,))
    spark = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(spark).polygon(astroid(cx, cy, S * 0.085, 60, 3), fill=p["lime"] + (255,))
    lay = Image.alpha_composite(lay, _glow(spark, p["lime"], S * 0.012, 1.4))
    lay = sticker(lay, p["ink"], S * 0.012)
    tr = Image.new("RGBA", (S, S), (0, 0, 0, 0)); td = ImageDraw.Draw(tr)
    for k in range(60):
        t = k / 60; y0 = cy - B - S * 0.04 - t * S * 0.46; w = S * 0.40 * (1 - t) ** 0.9 + 6
        td.rectangle([cx - w / 2, y0, cx + w / 2, y0 + S * 0.009], fill=lerp(p["white"], p["glow"], t ** 0.6) + (int(255 * (1 - t) ** 1.1),))
    tr = _glow(tr.filter(ImageFilter.GaussianBlur(S * 0.003)), p["glow"], S * 0.03, 1.3)
    rng = np.random.default_rng(5); td = ImageDraw.Draw(tr)
    for _ in range(12):
        x = cx + rng.uniform(-0.17, 0.17) * S; y = cy - B - S * rng.uniform(0.08, 0.46); r = S * rng.uniform(0.008, 0.018)
        td.polygon(astroid(x, y, r * 2.4, 40), fill=p["white"] + (255,))
    lay = Image.alpha_composite(tr, lay)
    lay = lay.rotate(24, resample=Image.BICUBIC, center=(cx, cy))
    return lay


def mark_b5():
    """kuyunun dibinden yukarı bakış: tuğla halkalar → altın açıklık, içinde yıldız."""
    p = PAL["curiosity-well"]; S = MS; c = S / 2
    im, d = _canvas()
    R0 = S * 0.47
    d.ellipse([c - R0 - S * 0.02, c - R0 - S * 0.02, c + R0 + S * 0.02, c + R0 + S * 0.02], fill=p["amber"] + (255,))
    N = 7
    for i in range(N):
        t = i / N; r_out = R0 * (1 - t) ** 1.55; r_in = R0 * (1 - (i + 1) / N) ** 1.55
        base = lerp((6, 22, 40), (30, 150, 160), t ** 1.1)
        for j in range(16):
            u = j / 16; r = r_out - (r_out - r_in) * u
            col = lerp(lerp(base, (2, 8, 20), 0.55), lerp(base, (255, 200, 110), 0.30 * t + 0.1), u)
            d.ellipse([c - r, c - r, c + r, c + r], fill=col + (255,))
    # tuğla çentikleri: her halkada radyal çizgiler
    for i in range(N - 1):
        r_out = R0 * (1 - i / N) ** 1.55; r_in = R0 * (1 - (i + 1) / N) ** 1.55
        n = 14 + 4 * i
        for k in range(n):
            a = 2 * math.pi * (k + (0.5 if i % 2 else 0)) / n
            d.line([(c + r_in * math.cos(a), c + r_in * math.sin(a)), (c + r_out * math.cos(a), c + r_out * math.sin(a))],
                   fill=(3, 10, 24, 150), width=max(3, int(S * 0.004)))
        d.ellipse([c - r_out, c - r_out, c + r_out, c + r_out], outline=(3, 10, 24, 200), width=int(S * 0.006))
    # açıklık: sıcak altın ışık
    ro = S * 0.115
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([c - ro * 1.8, c - ro * 1.8, c + ro * 1.8, c + ro * 1.8], fill=p["amber"] + (110,))
    g = g.filter(ImageFilter.GaussianBlur(S * 0.03)); im = Image.alpha_composite(im, g)
    d = ImageDraw.Draw(im)
    d.ellipse([c - ro, c - ro, c + ro, c + ro], fill=p["amber2"] + (255,))
    st = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(st).polygon(astroid(c, c, S * 0.085, 60, 3), fill=(255, 255, 255, 255))
    im = Image.alpha_composite(im, _glow(st, p["amber"], S * 0.015, 1.6))
    # dış halka: kuyu ağzı kenarı
    d = ImageDraw.Draw(im)
    d.ellipse([c - R0, c - R0, c + R0, c + R0], outline=p["amber2"] + (255,), width=int(S * 0.014))
    return im


MARKS2 = {"free-ai-drop": mark_a5, "curiosity-well": mark_b5}
SCALE = {"free-ai-drop": 0.74, "curiosity-well": 0.76}


def profile(brand, fn):
    S = 1080; bg = background(brand, S, S, focus=(0.5, 0.5)).convert("RGBA")
    k = SCALE[brand]; mk = fn().resize((int(S * k),) * 2, Image.LANCZOS)
    bg.alpha_composite(mk, ((S - mk.width) // 2, (S - mk.height) // 2))
    return bg


def banner(brand, fn):
    W, H = 2560, 1440; b = BR[brand]
    im = background(brand, W, H, seed=11, focus=(0.27, 0.5))
    # güvenli alan 1546x423: x507..2053, y508..931 — her şey bunun içinde, dikey ortalı
    sx0, sy0, sw, sh = 507, 508, 1546, 423
    K = int(sh * 1.3); mk = fn().resize((K, K), Image.LANCZOS); im.alpha_composite(mk, (sx0 - (K - sh) // 2, sy0 - (K - sh) // 2))
    d = ImageDraw.Draw(im)
    tx = sx0 + sh + 40; tw = sx0 + sw - tx
    f, w = fit_text(d, b["name"], b["fname"], b["var"], tw, 150, b["track"])
    f2, w2 = fit_text(d, b["slogan"], b["sfname"], b["svar"], tw, 64, 1)
    block = int(f.size * 1.0) + 44 + int(f2.size * 1.0)
    y0 = sy0 + (sh - block) // 2 - int(f.size * 0.12)
    spaced(im, (tx, y0), b["name"], f, b["c1"] + (255,), b["track"])
    ry = y0 + int(f.size * 1.30)
    d.rectangle([tx, ry, tx + 120, ry + 7], fill=b["c2"] + (255,))
    spaced(im, (tx, ry + 24), b["slogan"], f2, b["sl"] + (255,), 1)
    return im.convert("RGB")


def shorts(brand, fn, ornek=True):
    W, H = 1080, 1920; b = BR[brand]; p = PAL[brand]
    im = background(brand, W, H, seed=21, focus=(0.5, 0.40))
    d = ImageDraw.Draw(im)
    # güvenli: üst %15 (0-288) ve alt %20 (1536-1920) boş; sağ 120px boş
    top, bot = 330, 1130
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([60, top, 930, bot], radius=44, fill=(0, 0, 0, 120), outline=b["c2"] + (200,), width=4)
    im.alpha_composite(panel)
    im.alpha_composite(fn().resize((150, 150), Image.LANCZOS), (96, top + 36))
    spaced(im, (270, top + 66), b["name"], font(b["fname"], 40, b["var"]), b["c1"] + (255,), 5)
    spaced(im, (272, top + 122), "DAY 01" if brand == "free-ai-drop" else "EPISODE 01", font(b["sfname"], 30, b["svar"]), b["c2"] + (255,), 4)
    if ornek:
        lines = ["THIS FREE AI", "TOOL REPLACES", "A $20 APP"] if brand == "free-ai-drop" else ["WHY DID THE", "ANCIENT WELL", "NEVER RUN DRY?"]
        ft, _ = fit_text(d, max(lines, key=len), "impact.ttf" if brand == "free-ai-drop" else "georgiab.ttf", None, 780, 112, 2)
        y = top + 240
        for i, ln in enumerate(lines):
            spaced(im, (96, y), ln, ft, (b["c2"] if i == 2 else b["c1"]) + (255,), 2)
            y += int(ft.size * 1.16)
    # alt görsel çapa (y 1290-1490): büyük işaret + ilerleme çubuğu
    big = fn().resize((400, 400), Image.LANCZOS)
    im.alpha_composite(big, (60, 1190))
    d = ImageDraw.Draw(im)
    tx = 500
    spaced(im, (tx, 1330), "NEW EVERY DAY" if brand == "free-ai-drop" else "NEW EVERY WEEK", font(b["fname"], 40, b["var"]), b["c1"] + (255,), 3)
    d.rounded_rectangle([tx, 1400, 930, 1418], radius=9, fill=(255, 255, 255, 40))
    d.rounded_rectangle([tx, 1400, tx + 150, 1418], radius=9, fill=b["c2"] + (255,))
    return im.convert("RGB")


def main():
    for br, fn in MARKS2.items():
        base = os.path.join(OUT, br, "v2"); os.makedirs(base, exist_ok=True)
        profile(br, fn).convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
        banner(br, fn).save(os.path.join(base, "kanal-afisi-2560x1440.png"))
        shorts(br, fn).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
        shorts(br, fn, False).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
        pf = profile(br, fn); sh = Image.new("RGB", (560, 400), (235, 235, 235))
        sh.paste(circle_crop(pf, 360), (10, 20)); sh.paste(circle_crop(pf, 110), (390, 20)); sh.paste(circle_crop(pf, 48), (390, 160))
        sh.save(os.path.join(base, "_kucuk-boyut.png"))
        print(br, "ok")


if __name__ == "__main__":
    main()
