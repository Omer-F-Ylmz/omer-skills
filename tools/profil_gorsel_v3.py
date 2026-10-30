"""PROFIL-GORSEL-1 tur4: imza öğeler ücretsiz bulut (Cloudflare flux-1-schnell) adaylarından; PIL montaj.
Kullanim: python tools/profil_gorsel_v3.py  -> <marka>/v3/ altına yazar (adaylar v3/aday/, üretici profil_bulut.py)"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from profil_gorsel import MS, PAL, BR, OUT, font, fit_text, spaced, background, circle_crop, lerp

PICK = {"free-ai-drop": "free-ai-drop-03-cf.png", "curiosity-well": "curiosity-well-06-cf.png"}


def cand(brand):
    return Image.open(os.path.join(OUT, brand, "v3", "aday", PICK[brand])).convert("RGB")


def mark_fad():
    p = PAL["free-ai-drop"]; im = cand("free-ai-drop"); a = np.array(im).astype("float32")
    bg = np.median(np.concatenate([a[:24, :24].reshape(-1, 3), a[-24:, :24].reshape(-1, 3), a[:24, -24:].reshape(-1, 3), a[-24:, -24:].reshape(-1, 3)]), 0)
    al = np.clip((np.sqrt(((a - bg) ** 2).sum(-1)) - 70) / 40, 0, 1) * (a.max(-1) > 150)
    rgba = np.dstack([a, al * 255]).astype("uint8"); m = Image.fromarray(rgba, "RGBA")
    bb = m.getchannel("A").point(lambda v: 255 if v > 128 else 0).getbbox(); m = m.crop(bb)
    H = int(MS * 0.72); W = int(m.width * H / m.height); m = m.resize((W, H), Image.LANCZOS)
    lay = Image.new("RGBA", (MS, MS), (0, 0, 0, 0)); ox, oy = (MS - W) // 2, (MS - H) // 2 + int(MS * 0.02)
    lay.alpha_composite(m, (ox, oy))
    # ışık kaynağı: yıldızın çevresinde sıcak parlama
    row = np.array(m.getchannel("A"))[: int(H * 0.2)] > 128; ys, xs = np.nonzero(row)
    sx, sy = ox + int(xs.mean()), oy + int(ys.mean())
    yy, xx = np.mgrid[0:MS, 0:MS].astype("float32"); r = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / (MS * 0.16)
    g = np.exp(-(r ** 2) * 3.0)
    glow = np.zeros((MS, MS, 4), "float32"); glow[..., :3] = p["lime"]; glow[..., 3] = g * 150
    halo = np.array(lay.getchannel("A").filter(ImageFilter.GaussianBlur(MS * 0.03))).astype("float32")
    hl = np.zeros((MS, MS, 4), "float32"); hl[..., :3] = p["lime2"]; hl[..., 3] = halo * 0.45
    out = Image.alpha_composite(Image.fromarray(hl.astype("uint8"), "RGBA"), Image.fromarray(glow.astype("uint8"), "RGBA"))
    return Image.alpha_composite(out, lay)


def mark_cw():
    p = PAL["curiosity-well"]; im = cand("curiosity-well")
    s = min(im.size); c = (im.width // 2, int(im.height * 0.48)); R = int(s * 0.47)
    sq = im.crop((c[0] - R, c[1] - R, c[0] + R, c[1] + R)).resize((MS, MS), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (MS * 2, MS * 2), 0); ImageDraw.Draw(m).ellipse([0, 0, MS * 2 - 1, MS * 2 - 1], fill=255)
    sq.putalpha(m.resize((MS, MS), Image.LANCZOS))
    lay = Image.new("RGBA", (MS, MS), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); w = int(MS * 0.028)
    d.ellipse([w // 2, w // 2, MS - w // 2, MS - w // 2], outline=p["amber2"] + (255,), width=w)
    return Image.alpha_composite(sq, lay)


MARKS3 = {"free-ai-drop": mark_fad, "curiosity-well": mark_cw}
SCALE = {"free-ai-drop": 0.96, "curiosity-well": 0.92}


def profile(brand, mk):
    S = 1080; bg = background(brand, S, S, focus=(0.5, 0.45)).convert("RGBA")
    k = SCALE[brand]; m = mk.resize((int(S * k),) * 2, Image.LANCZOS)
    bg.alpha_composite(m, ((S - m.width) // 2, (S - m.height) // 2)); return bg


def plate(im, box, color, alpha, blur):
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle(box, radius=60, fill=color + (alpha,))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(blur)))


def banner(brand, mk):
    W, H = 2560, 1440; b = BR[brand]; p = PAL[brand]
    im = background(brand, W, H, seed=11, focus=(0.30, 0.5))
    sx0, sy0, sw, sh = 507, 508, 1546, 423          # güvenli alan
    D = 760
    cx = sx0 + 20 + D // 2
    m = mk.resize((D, D), Image.LANCZOS)
    im.alpha_composite(m, (cx - D // 2, H // 2 - D // 2))
    tx = cx + D // 2 + 60; tw = sx0 + sw - tx
    lines = ["CURIOSITY", "WELL"] if brand == "curiosity-well" else ["FREE AI DROP"]
    # başlık arkasına yumuşak koyu levha (yağan çizgiler/halkalar yazıdan geçmesin)
    plate(im, [tx - 40, sy0 - 20, sx0 + sw + 100, sy0 + sh + 20], p["ink"], 150, 70)
    d = ImageDraw.Draw(im)
    fs = [fit_text(d, ln, b["fname"], b["var"], tw, 170, b["track"]) for ln in lines]
    f = min((x[0] for x in fs), key=lambda x: x.size)
    f2, _ = fit_text(d, b["slogan"], b["sfname"], b["svar"], tw, 54, 1)
    block = int(f.size * 1.05) * len(lines) + 20 + 20 + int(f2.size * 1.2)
    y = H // 2 - block // 2 - int(f.size * 0.1)
    for ln in lines:
        spaced(im, (tx, y), ln, f, b["c1"] + (255,), b["track"]); y += int(f.size * 1.05)
    y += 8; d.rectangle([tx, y, tx + 120, y + 7], fill=b["c2"] + (255,))
    spaced(im, (tx, y + 26), b["slogan"], f2, b["sl"] + (255,), 1)
    return im.convert("RGB")


def inter(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def shorts(brand, mk, ornek=True, log=None):
    W, H = 1080, 1920; b = BR[brand]; p = PAL[brand]
    im = background(brand, W, H, seed=21, focus=(0.5, 0.38)); boxes = {}
    d = ImageDraw.Draw(im)
    lines = (["THIS FREE AI", "TOOL REPLACES", "A $20 APP"] if brand == "free-ai-drop" else ["WHY DID THE", "ANCIENT WELL", "NEVER RUN DRY?"])
    if not ornek:
        lines = ["YOUR TITLE", "GOES HERE", "(3 LINES MAX)"]
    fname = "impact.ttf" if brand == "free-ai-drop" else "georgiab.ttf"
    ft, _ = fit_text(d, max(lines, key=len), fname, None, 780, 112, 2)
    top = 300; head_h = 200; ly = top + head_h + 30; lh = int(ft.size * 1.16)
    bot = ly + lh * len(lines) + 40                      # kart içeriğe göre boy alır
    plate(im, [60, top, 1020 - 90, bot], (0, 0, 0), 150, 1)
    ImageDraw.Draw(im).rounded_rectangle([60, top, 930, bot], radius=44, outline=b["c2"] + (200,), width=4)
    im.alpha_composite(mk.resize((150, 150), Image.LANCZOS), (96, top + 36)); boxes["logo"] = (96, top + 36, 246, top + 186)
    f1 = font(b["fname"], 40, b["var"]); f2 = font(b["sfname"], 30, b["svar"])
    tag = ("DAY 01" if brand == "free-ai-drop" else "EPISODE 01")
    spaced(im, (270, top + 66), b["name"], f1, b["c1"] + (255,), 5); boxes["ad"] = (270, top + 66, 270 + int(d.textlength(b["name"], font=f1)) + 5 * len(b["name"]), top + 66 + 46)
    spaced(im, (272, top + 122), tag, f2, b["c2"] + (255,), 4); boxes["etiket"] = (272, top + 122, 272 + int(d.textlength(tag, font=f2)) + 16, top + 122 + 36)
    for i, ln in enumerate(lines):
        spaced(im, (96, ly), ln, ft, (b["c2"] if i == 2 else b["c1"]) + (255,), 2)
        boxes[f"satir{i}"] = (96, ly, 96 + int(d.textlength(ln, font=ft)) + 2 * len(ln), ly + ft.size); ly += lh
    # alt yarı: konu görseli yer tutucu + marka çapası (güvenli alan: y<=1536, sağ 120px boş)
    ph = (60, bot + 50, 930, 1390)
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    ld.rounded_rectangle(ph, radius=36, fill=(255, 255, 255, 18))
    for x in range(ph[0] + 20, ph[2] - 20, 44):
        ld.line([(x, ph[1]), (x + 22, ph[1])], fill=b["c2"] + (200,), width=4); ld.line([(x, ph[3]), (x + 22, ph[3])], fill=b["c2"] + (200,), width=4)
    for y in range(ph[1] + 20, ph[3] - 20, 44):
        ld.line([(ph[0], y), (ph[0], y + 22)], fill=b["c2"] + (200,), width=4); ld.line([(ph[2], y), (ph[2], y + 22)], fill=b["c2"] + (200,), width=4)
    im.alpha_composite(L); boxes["yer"] = ph
    MK = min(380, ph[3] - ph[1] - 140); big = mk.resize((MK, MK), Image.LANCZOS)
    cap = "TOPIC IMAGE / B-ROLL"; fc = font(b["sfname"], 34, b["svar"]); cw = int(d.textlength(cap, font=fc))
    cx = (ph[0] + ph[2]) // 2; cy = (ph[1] + ph[3]) // 2
    spaced(im, (cx - cw // 2, cy - 17), cap, fc, b["c1"] + (170,), 1)
    boxes["yer-yazi"] = (cx - cw // 2, cy - 17, cx + cw // 2, cy + 23)
    anch = ("NEW EVERY DAY" if brand == "free-ai-drop" else "NEW EVERY WEEK"); fa = font(b["fname"], 44, b["var"])
    im.alpha_composite(mk.resize((120, 120), Image.LANCZOS), (60, 1405)); boxes["cipa-isaret"] = (60, 1405, 180, 1525)
    spaced(im, (210, 1432), anch, fa, b["c1"] + (255,), 3); boxes["cipa-yazi"] = (210, 1432, 210 + int(d.textlength(anch, font=fa)) + 3 * len(anch), 1432 + 54)
    # çakışma testi: konu görseli kutusu içindeki öğeler hariç tüm çiftler kesişmemeli
    ic = {"yer-isaret", "yer-yazi"}; bad = []
    ks = list(boxes)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, c2 = ks[i], ks[j]
            if (a == "yer" and c2 in ic) or (c2 == "yer" and a in ic) or (a in ic and c2 in ic):
                continue
            if inter(boxes[a], boxes[c2]):
                bad.append((a, c2))
    if log is not None:
        log[f"{brand}-{'ornek' if ornek else 'bos'}"] = {"kesisim": bad, "kart_alt": bot, "yer_yuk": ph[3] - ph[1], "mac_alt_sinir_ok": max(v[3] for v in boxes.values()) <= 1536}
    return im.convert("RGB")


def main():
    log = {}
    for br, fn in MARKS3.items():
        base = os.path.join(OUT, br, "v3"); os.makedirs(base, exist_ok=True)
        mk = fn(); mk.save(os.path.join(base, "isaret-1600.png"))
        pf = profile(br, mk); pf.convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
        banner(br, mk).save(os.path.join(base, "kanal-afisi-2560x1440.png"))
        shorts(br, mk, True, log).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
        shorts(br, mk, False, log).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
        sh = Image.new("RGB", (560, 400), (235, 235, 235))
        sh.paste(circle_crop(pf, 360), (10, 20)); sh.paste(circle_crop(pf, 110), (390, 20)); sh.paste(circle_crop(pf, 48), (390, 160))
        sh.save(os.path.join(base, "_kucuk-boyut.png")); print(br, "ok")
    open(os.path.join(OUT, "cakisma-testi-v3.json"), "w", encoding="utf-8").write(json.dumps(log, indent=1))
    print(json.dumps(log))


if __name__ == "__main__":
    main()
