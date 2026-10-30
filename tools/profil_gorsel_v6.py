"""PROFIL-GORSEL-1 tur7 (v6): v5 üstüne afiş düzeltmesi: blok güvenli yükseklik 423 içinde, yazı bölgesi yıldızsız. -> <marka>/v6/"""
import json, os
from PIL import Image, ImageDraw, ImageFilter
from profil_gorsel import BR, OUT, fit_text, spaced, circle_crop
from profil_gorsel_v4 import circ
import profil_gorsel_v5 as v5


def banner(brand, mk):
    W, H = 2560, 1440; b = BR[brand]
    im = v5.bg5(brand, W, H, seed=11); d = ImageDraw.Draw(im)
    D = 400; gap = 56; safe = 1546
    line = "CURIOSITY WELL" if brand == "curiosity-well" else "FREE AI DROP"
    f, tw = fit_text(d, line, b["fname"], b["var"], safe - D - gap - 20, 230, b["track"])
    f2, sw = fit_text(d, b["slogan"], b["sfname"], b["svar"], tw, 78, 1)
    bw = D + gap + int(tw); x0 = (W - bw) // 2; tx = x0 + D + gap
    if brand == "curiosity-well":                      # yazı bölgesinde yıldız yok (yumuşak maske)
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle([tx - 30, H // 2 - 170, tx + int(tw) + 30, H // 2 + 170], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(40)); im.paste(Image.new("RGBA", (W, H), v5.CW_BG + (255,)), (0, 0), m)
        d = ImageDraw.Draw(im)
    im.alpha_composite(mk.resize((D, D), Image.LANCZOS), (x0, H // 2 - D // 2))
    total = int(f.size) + 8 + 7 + 26 + int(f2.size * 1.2); y = H // 2 - total // 2 - int(f.size * 0.12)
    spaced(im, (tx, y), line, f, b["c1"] + (255,), b["track"]); y += int(f.size) + 8
    d.rectangle([tx, y, tx + 120, y + 7], fill=b["c2"] + (255,))
    spaced(im, (tx, y + 26), b["slogan"], f2, b["sl"] + (255,), 1)
    return im.convert("RGB"), {"blok": (x0, H // 2 - D // 2, x0 + bw, H // 2 + D // 2), "blok_yukseklik": D, "guvenli": (safe, 423)}


def main():
    log = {}
    for br, fn in v5.MARKS.items():
        base = os.path.join(OUT, br, "v6"); os.makedirs(base, exist_ok=True)
        mk = fn(); mk.save(os.path.join(base, "isaret-1600.png")); mkc = circ(mk) if br == "curiosity-well" else mk
        pf = v5.profile5(br, mk); pf.convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
        bn, info = banner(br, mkc); bn.save(os.path.join(base, "kanal-afisi-2560x1440.png")); log[br + "-afis"] = info
        v5.shorts(br, mkc, True, log).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
        v5.shorts(br, mkc, False, log).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
        sh = Image.new("RGB", (560, 400), (235, 235, 235))
        sh.paste(circle_crop(pf, 360), (10, 20)); sh.paste(circle_crop(pf, 110), (390, 20)); sh.paste(circle_crop(pf, 48), (390, 160))
        sh.save(os.path.join(base, "_kucuk-boyut.png"))
    open(os.path.join(OUT, "cakisma-testi-v6.json"), "w", encoding="utf-8").write(json.dumps(log, indent=1)); print(json.dumps(log["curiosity-well-afis"]))


if __name__ == "__main__":
    main()
