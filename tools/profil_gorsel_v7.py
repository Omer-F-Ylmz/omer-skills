"""PROFIL-GORSEL-1 tur8 (v7): v6 üstüne Cloudflare flux dokusu (zemin boş değil). -> <marka>/v7/
Doku adayları: <marka>/v3/aday/ (profil_bulut.py, ücretsiz cf)."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from profil_gorsel import OUT, circle_crop
from profil_gorsel_v4 import circ
import profil_gorsel_v5 as v5
import profil_gorsel_v6 as v6

AD = lambda b, n: os.path.join(OUT, b, "v3", "aday", f"{b}-{n:02d}-cf.png")
TEX = {"free-ai-drop": (AD("free-ai-drop", 2), 0.80, 0.55), "curiosity-well": (AD("curiosity-well", 1), 0.70, 0.60)}  # dosya, karışım, parlaklık
WELL = AD("curiosity-well", 0)
_orig = v5.bg5


def cover(im, w, h, focus=(0.5, 0.5)):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); return im.crop((x, y, x + w, y + h))


def bg7(brand, w, h, seed=5, focus=(0.5, 0.5)):
    base = _orig(brand, w, h, seed, focus); fp, mix, br = TEX[brand]
    t = np.array(cover(Image.open(fp).convert("RGB"), w, h, (0.5, 0.5))).astype("float32") * br
    if brand == "curiosity-well" and h > w * 1.5:            # shorts: alt yarıda kuyu ağzı
        wl = np.array(cover(Image.open(WELL).convert("RGB"), w, int(h * 0.55), (0.5, 0.8))).astype("float32")
        ramp = np.linspace(0, 1, wl.shape[0], dtype="float32")[:, None, None] ** 1.2
        t[h - wl.shape[0]:] = t[h - wl.shape[0]:] * (1 - ramp) + wl * ramp
    b = np.array(base.convert("RGB")).astype("float32")
    # kenar kararması: yazı bölgesi okunur kalsın
    yy, xx = np.mgrid[0:h, 0:w].astype("float32"); vg = 1 - 0.45 * (((xx / w - .5) ** 2 + (yy / h - .5) ** 2) * 2)[..., None]
    out = np.clip((b * (1 - mix) + t * mix) * vg, 0, 255).astype("uint8")
    return Image.fromarray(out, "RGB").convert("RGBA")


v5.bg5 = bg7


def main():
    log = {}
    for br, fn in v5.MARKS.items():
        base = os.path.join(OUT, br, "v7"); os.makedirs(base, exist_ok=True)
        mk = fn(); mk.save(os.path.join(base, "isaret-1600.png")); mkc = circ(mk) if br == "curiosity-well" else mk
        pf = v5.profile5(br, mk); pf.convert("RGB").save(os.path.join(base, "profil-1080x1080.png"))
        bn, info = v6.banner(br, mkc); bn.save(os.path.join(base, "kanal-afisi-2560x1440.png")); log[br + "-afis"] = info
        v5.shorts(br, mkc, True, log).save(os.path.join(base, "shorts-kapak-sablon-1080x1920.png"))
        v5.shorts(br, mkc, False, log).save(os.path.join(base, "shorts-kapak-bos-1080x1920.png"))
        sh = Image.new("RGB", (560, 400), (235, 235, 235))
        sh.paste(circle_crop(pf, 360), (10, 20)); sh.paste(circle_crop(pf, 110), (390, 20)); sh.paste(circle_crop(pf, 48), (390, 160))
        sh.save(os.path.join(base, "_kucuk-boyut.png"))
    open(os.path.join(OUT, "cakisma-testi-v7.json"), "w", encoding="utf-8").write(json.dumps(log, indent=1))


if __name__ == "__main__":
    main()
