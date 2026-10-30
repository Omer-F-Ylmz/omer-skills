"""PROFIL-GORSEL-1 tur6 (v5): Desktop yönü. FAD: 'D' içinde indirme oku oyuğu, düz mor zemin; CW: simetrik ışın + kuyu ağzı çemberi, saf lacivert.
Kullanim: python tools/profil_gorsel_v5.py -> <marka>/v5/"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from profil_gorsel import MS, PAL, BR, OUT, font, fit_text, spaced, circle_crop
from profil_gorsel_v3 import inter
from profil_gorsel_v4 import circ

SS = 2
FAD_BG = (30, 12, 82)
CW_BG = (6, 10, 40)


def bg5(brand, w, h, seed=5, focus=(0.5, 0.5)):
    rng = np.random.default_rng(seed)
    p = PAL[brand]
    if brand == "free-ai-drop":
        arr = np.ones((h, w, 3), "float32") * np.array(FAD_BG, "float32")
        xx = np.arange(w, dtype="float32")[None, :]
        fx = focus[0] * w; sw = w * 0.05
        beam = np.exp(-((xx - fx) / sw) ** 2)[..., None] * np.linspace(1, 0.15, h, dtype="float32")[:, None, None]  # tek ince ışık: üstten düşen
        arr = arr + beam * np.array(p["glow"], "float32") * 0.16
        im = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB").convert("RGBA")
    else:
        im = Image.new("RGBA", (w, h), CW_BG + (255,))
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        for _ in range(int(w * h / 30000)):              # yıldızlar v4'e göre ~%70 az
            x = rng.uniform(0, w); y = rng.uniform(0, h); s = rng.uniform(1, 2.6) * w / 1080
            dr.ellipse([x - s, y - s, x + s, y + s], fill=p["amber2"] + (int(rng.uniform(70, 200)),))
        im = Image.alpha_composite(im, lay.filter(ImageFilter.GaussianBlur(max(0.6, w / 2200))))
    a = np.array(im).astype("float32"); a[..., :3] += rng.normal(0, 2.0, (h, w, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"), "RGBA")


def mark_fad():
    p = PAL["free-ai-drop"]; S = MS * SS; u = S / 1600
    m = Image.new("L", (S, S), 0); d = ImageDraw.Draw(m)
    x0, top, bot, sx = 300, 140, 1120, 330; R = (bot - top) // 2; cy = (top + bot) // 2
    d.rectangle([x0 * u, top * u, (x0 + sx) * u, bot * u], fill=255)
    d.pieslice([(x0 + sx - R) * u, top * u, (x0 + sx + R) * u, bot * u], -90, 90, fill=255)
    ax = 700; tip = cy + 340; ht = 260; hw = 230      # oyuk: pikselden düşen indirme oku
    d.polygon([((ax - hw) * u, (tip - ht) * u), ((ax + hw) * u, (tip - ht) * u), (ax * u, tip * u)], fill=0)
    d.rectangle([(ax - 85) * u, (tip - ht - 260) * u, (ax + 85) * u, (tip - ht + 2) * u], fill=0)
    body = np.array(m.resize((MS, MS), Image.LANCZOS)).astype("float32")
    arr = np.zeros((MS, MS, 4), "float32"); arr[..., :3] = np.array(p["lime"], "float32"); arr[..., 3] = body
    out = Image.fromarray(arr.astype("uint8"), "RGBA")
    bb = out.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox(); c = out.crop(bb)
    k = 1100 / c.height; c = c.resize((int(c.width * k), 1100), Image.LANCZOS)
    fin = Image.new("RGBA", (MS, MS), (0, 0, 0, 0)); fin.alpha_composite(c, ((MS - c.width) // 2, (MS - c.height) // 2))
    halo = fin.getchannel("A").filter(ImageFilter.GaussianBlur(MS * 0.02))
    hl = Image.new("RGBA", (MS, MS), p["lime2"] + (0,)); hl.putalpha(halo.point(lambda v: int(v * 0.18)))
    return Image.alpha_composite(hl, fin)


def mark_cw():
    p = PAL["curiosity-well"]; S = MS * SS; u = S / 1600; cx = cy = S / 2
    im = Image.new("RGB", (S, S), CW_BG); d = ImageDraw.Draw(im)
    N = 24; w = math.pi / N                              # tüm ışınlar aynı: eşit açı, eşit uzunluk, %50 doluluk
    for i in range(N):
        a0 = 2 * math.pi * i / N - w / 2
        pts = [(cx + 400 * u * math.cos(a0 + w * t / 6), cy + 400 * u * math.sin(a0 + w * t / 6)) for t in range(7)]
        pts += [(cx + 1300 * u * math.cos(a0 + w * t / 6), cy + 1300 * u * math.sin(a0 + w * t / 6)) for t in range(6, -1, -1)]
        d.polygon(pts, fill=p["amber"])
    d.ellipse([cx - 350 * u, cy - 350 * u, cx + 350 * u, cy + 350 * u], fill=CW_BG)                  # kuyu ağzı: tek çember
    d.ellipse([cx - 350 * u, cy - 350 * u, cx + 350 * u, cy + 350 * u], outline=p["amber2"], width=int(34 * u))
    hr = 82 * u; hy = cy - 70 * u                       # anahtar deliği kuyunun içinde, ışık rengi
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=p["amber2"])
    d.polygon([(cx - 44 * u, hy + 40 * u), (cx + 44 * u, hy + 40 * u), (cx + 82 * u, cy + 200 * u), (cx - 82 * u, cy + 200 * u)], fill=p["amber2"])
    return im.resize((MS, MS), Image.LANCZOS).convert("RGBA")


MARKS = {"free-ai-drop": mark_fad, "curiosity-well": mark_cw}


def profile5(brand, mk):
    S = 1080; bg = bg5(brand, S, S, focus=(0.5, 0.45))
    m = mk.resize((S, S), Image.LANCZOS); bg.alpha_composite(m, (0, 0)); return bg


def banner(brand, mk):
    W, H = 2560, 1440; b = BR[brand]
    im = bg5(brand, W, H, seed=11, focus=(0.5, 0.5)); d = ImageDraw.Draw(im)
    D = 560 if brand == "free-ai-drop" else 440; gap = 60; safe = 1546
    line = "CURIOSITY WELL" if brand == "curiosity-well" else "FREE AI DROP"
    f, tw = fit_text(d, line, b["fname"], b["var"], safe - D - gap - 20, 230, b["track"])
    f2, sw = fit_text(d, b["slogan"], b["sfname"], b["svar"], tw, 78, 1)
    bw = D + gap + int(tw); x0 = (W - bw) // 2; tx = x0 + D + gap
    im.alpha_composite(mk.resize((D, D), Image.LANCZOS), (x0, H // 2 - D // 2))
    total = int(f.size * 1.0) + 8 + 7 + 26 + int(f2.size * 1.2); y = H // 2 - total // 2 - int(f.size * 0.12)
    spaced(im, (tx, y), line, f, b["c1"] + (255,), b["track"]); y += int(f.size * 1.0) + 8
    d.rectangle([tx, y, tx + 120, y + 7], fill=b["c2"] + (255,))
    spaced(im, (tx, y + 26), b["slogan"], f2, b["sl"] + (255,), 1)
    return im.convert("RGB"), {"blok": (x0, H // 2 - D // 2, x0 + bw, H // 2 + D // 2), "guvenli_x": ((W - safe) // 2, (W + safe) // 2)}


def shorts(brand, mk, ornek=True, log=None):
    W, H = 1080, 1920; b = BR[brand]
    im = bg5(brand, W, H, seed=21, focus=(0.5, 0.38)); boxes = {}; d = ImageDraw.Draw(im)
    lines = (["THIS FREE AI", "TOOL REPLACES", "A $20 APP"] if brand == "free-ai-drop" else ["WHY DID THE", "ANCIENT WELL", "NEVER RUN DRY?"])
    if not ornek:
        lines = ["YOUR TITLE", "GOES HERE", "(3 LINES MAX)"]
    fname = "impact.ttf" if brand == "free-ai-drop" else "georgiab.ttf"
    ft, _ = fit_text(d, max(lines, key=len), fname, None, 780, 112, 2)
    top = 260; lh = int(ft.size * 1.16); ly = top + 210; bot = ly + lh * len(lines) + 40
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle([60, top, 1020, bot], radius=44, fill=(0, 0, 0, 150), outline=b["c2"] + (210,), width=4)
    im.alpha_composite(L)
    f1 = font(b["fname"], 48, b["var"]); f2 = font(b["sfname"], 40, b["svar"]); tag = "DAY 01" if brand == "free-ai-drop" else "EPISODE 01"
    n1 = int(d.textlength(b["name"], font=f1)) + 5 * len(b["name"]); n2 = int(d.textlength(tag, font=f2)) + 4 * len(tag)
    LG = 130; rw = LG + 28 + max(n1, n2); rx = (W - rw) // 2        # başlık satırı: logo + ad/etiket, kartta ortalı
    im.alpha_composite(mk.resize((LG, LG), Image.LANCZOS), (rx, top + 32)); boxes["logo"] = (rx, top + 32, rx + LG, top + 32 + LG)
    tx = rx + LG + 28
    spaced(im, (tx, top + 40), b["name"], f1, b["c1"] + (255,), 5); boxes["ad"] = (tx, top + 50, tx + n1, top + 96)
    spaced(im, (tx, top + 108), tag, f2, b["c2"] + (255,), 4); boxes["etiket"] = (tx, top + 104, tx + n2, top + 144)
    for i, ln in enumerate(lines):
        lw = int(sum(d.textlength(c, font=ft) + 2 for c in ln)) - 2; lx = (W - lw) // 2
        spaced(im, (lx, ly), ln, ft, (b["c2"] if i == 2 else b["c1"]) + (255,), 2)
        boxes[f"satir{i}"] = (lx, ly, lx + lw, ly + ft.size); ly += lh
    ph = (60, bot + 50, 1020, 1550)                        # b-roll alanı: alt 1/3, kart ile aynı 60/60 marj
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle(ph, radius=36, fill=(255, 255, 255, 22), outline=b["c2"] + (90,), width=3)
    im.alpha_composite(L); boxes["yer"] = ph
    fb = font(b["sfname"], 36, b["svar"]); bt = "B-ROLL / VIDEO AREA"; bw_ = int(d.textlength(bt, font=fb))
    spaced(im, ((W - bw_) // 2, (ph[1] + ph[3]) // 2 - 20), bt, fb, (255, 255, 255, 70), 0)
    anch = "NEW EVERY DAY" if brand == "free-ai-drop" else "NEW EVERY WEEK"; fa = font(b["fname"], 48, b["var"]); aw = int(d.textlength(anch, font=fa)) + 3 * len(anch)
    ay = 1585; spaced(im, ((W - aw) // 2, ay), anch, fa, b["c1"] + (255,), 3); boxes["cipa-yazi"] = ((W - aw) // 2, ay, (W + aw) // 2, ay + 58)
    boxes_chk = {k: v for k, v in boxes.items() if k != "yer"}
    bad = [(a, c) for i, a in enumerate(boxes) for c in list(boxes)[i + 1:] if inter(boxes[a], boxes[c])]
    if log is not None:
        log[f"{brand}-{'ornek' if ornek else 'bos'}"] = {"kesisim": bad, "kart_marj_sol_sag": (60, W - 1020), "en_alt_y": max(v[3] for v in boxes_chk.values()), "alt_250_guvenli_ust_sinir": H - 250,
                                                          "brol_yukseklik": ph[3] - ph[1], "satir_merkez_sapma": [abs((boxes[f"satir{i}"][0] + boxes[f"satir{i}"][2]) // 2 - W // 2) for i in range(3)]}
    return im.convert("RGB")


def main():
    log = {}
    for br, fn in MARKS.items():
        base = os.path.join(OUT, br, "v5"); os.makedirs(base, exist_ok=True)
        mk = fn(); mk.save(os.path.join(base, "isaret-1600.png")); mkc = circ(mk) if br == "curiosity-well" else mk
        pf = profile5(br, mk); pf.convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
        bn, info = banner(br, mkc); bn.save(os.path.join(base, "kanal-afisi-2560x1440.png")); log[br + "-afis"] = info
        shorts(br, mkc, True, log).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
        shorts(br, mkc, False, log).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
        sh = Image.new("RGB", (560, 400), (235, 235, 235))
        sh.paste(circle_crop(pf, 360), (10, 20)); sh.paste(circle_crop(pf, 110), (390, 20)); sh.paste(circle_crop(pf, 48), (390, 160))
        sh.save(os.path.join(base, "_kucuk-boyut.png")); print(br, "ok")
    open(os.path.join(OUT, "cakisma-testi-v5.json"), "w", encoding="utf-8").write(json.dumps(log, indent=1)); print(json.dumps(log))


if __name__ == "__main__":
    main()
