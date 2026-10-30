"""SUNUCU-KARAKTER-1 cikti uretici: yon alternatifleri, karakter karti, 10 poz tutarlilik seti."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
import sunucu_rig as R

ROOT = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yapılanlar", "sosyal-oto", "sunucu")
BR = {
    "free-ai-drop": dict(ch="robot", name="Dropi", brand="Free AI Drop", top=(8, 10, 28), bot=(30, 16, 84), acc=(200, 255, 46), txt=(244, 247, 255),
                         font=r"C:\Windows\Fonts\bahnschrift.ttf", sw=[("#080A1C", "gece"), ("#1E1054", "mor"), ("#6840FF", "parilti"), ("#C8FF2E", "limon"), ("#46FFA8", "nane"), ("#FF4F7B", "pembe"), ("#F4F7FF", "beyaz")]),
    "curiosity-well": dict(ch="owl", name="Wick", brand="Curiosity Well", top=(7, 11, 36), bot=(12, 70, 86), acc=(255, 181, 71), txt=(255, 243, 214),
                           font=r"C:\Windows\Fonts\georgiab.ttf", sw=[("#030512", "en koyu"), ("#070B24", "lacivert"), ("#0C4656", "teal"), ("#FFB547", "amber"), ("#FFE9A0", "acik amber"), ("#FFF3D6", "krem")]),
}


def bg(b, size, seed=1):
    w, h = size
    im = Image.new("RGB", size)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(b["top"][i] * (1 - t) + b["bot"][i] * t) for i in range(3)))
    rnd = random.Random(seed)
    ov = Image.new("RGBA", size, (0, 0, 0, 0))
    o = ImageDraw.Draw(ov)
    if b["ch"] == "robot":  # yagan cizgi dokusu
        for _ in range(w // 18):
            x = rnd.randint(0, w); y = rnd.randint(-200, h); L = rnd.randint(60, 260)
            o.line([(x, y), (x, y + L)], fill=(104, 64, 255, rnd.randint(25, 70)), width=3)
    else:  # yildiz tozu + kuyu halkasi
        for _ in range(w // 5):
            x = rnd.randint(0, w); y = rnd.randint(0, h); r = rnd.choice((1, 1, 2, 3))
            o.ellipse([x - r, y - r, x + r, y + r], fill=(255, 233, 160, rnd.randint(60, 200)))
        for k in range(5):
            r = int(min(w, h) * (0.25 + k * 0.1))
            o.ellipse([w // 2 - r, int(h * 0.8) - r // 2, w // 2 + r, int(h * 0.8) + r // 2], outline=(255, 181, 71, 28), width=3)
    im.paste(ov, (0, 0), ov)
    return im


def F(b, s, bold=True):
    return ImageFont.truetype(b["font"], s)


def put(canvas, sprite, x, y, size):
    s = sprite.resize((size, size), Image.LANCZOS)
    canvas.paste(s, (x, y), s)


def label(d, xy, txt, font, fill, anchor="mm"):
    d.text(xy, txt, font=font, fill=fill, anchor=anchor)


# ---- yon alternatifleri (basit kod cizimleri)
def _kit():
    S = 2
    im = Image.new("RGBA", (1000 * S, 1000 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    E = lambda bx, f, o=None, w=0: d.ellipse([v * S for v in bx], fill=f, outline=o, width=w * S)
    P_ = lambda pts, f, o=None: d.polygon([(x * S, y * S) for x, y in pts], fill=f, outline=o)
    Rr = lambda bx, r, f, o=None, w=0: d.rounded_rectangle([v * S for v in bx], radius=r * S, fill=f, outline=o, width=w * S)
    Ln = lambda pts, f, w: d.line([(x * S, y * S) for x, y in pts], fill=f, width=w * S)
    Ar = lambda bx, a0, a1, f, w: d.arc([v * S for v in bx], a0, a1, fill=f, width=w * S)
    return im, d, S, E, P_, Rr, Ln, Ar


def alt_blob(b):  # A2 damla ruh / B2 kapusonlu fener ruhu
    im, d, S, E, P_, Rr, Ln, Ar = _kit()
    ink = (11, 8, 48, 255)
    if b["ch"] == "robot":
        L = (200, 255, 46, 255)
        d.pieslice([280 * S, 60 * S, 720 * S, 400 * S], 180, 360, fill=(255, 79, 123, 255), outline=ink, width=6 * S)
        for x in (310, 400, 500, 600, 690):
            Ln([(x, 230), (500, 400)], (70, 255, 168, 255), 4)
        P_([(500, 330), (335, 640), (665, 640)], L, ink); E([300, 480, 700, 900], L, ink, 8)
        P_([(500, 330), (335, 640), (665, 640)], L)
        E([400, 570, 470, 660], (8, 10, 28, 255)); E([530, 570, 600, 660], (8, 10, 28, 255))
        E([420, 585, 445, 612], (244, 247, 255, 255)); E([550, 585, 575, 612], (244, 247, 255, 255))
        Ar([450, 670, 550, 740], 15, 165, (8, 10, 28, 255), 9)
        E([225, 650, 345, 770], (200, 255, 46, 255), ink, 6); E([655, 650, 775, 770], (200, 255, 46, 255), ink, 6)
        Rr([360, 880, 480, 960], 30, (30, 16, 84, 255), ink, 6); Rr([520, 880, 640, 960], 30, (30, 16, 84, 255), ink, 6)
        Rr([440, 760, 560, 840], 14, (255, 79, 123, 255), ink, 5)
    else:
        Ln([(300, 760), (250, 880)], (255, 181, 71, 255), 8)
        P_([(500, 120), (220, 940), (780, 940)], (7, 11, 36, 255), (255, 181, 71, 255))
        P_([(500, 210), (330, 640), (670, 640)], (12, 70, 86, 255))
        E([360, 330, 640, 660], (3, 5, 18, 255), (255, 181, 71, 255), 6)
        E([415, 440, 485, 510], (255, 181, 71, 255)); E([515, 440, 585, 510], (255, 181, 71, 255))
        E([440, 462, 460, 482], (255, 243, 214, 255)); E([540, 462, 560, 482], (255, 243, 214, 255))
        Ar([450, 540, 550, 600], 20, 160, (255, 181, 71, 255), 7)
        E([150, 830, 350, 1000 - 30], (255, 233, 160, 90))
        E([190, 780, 310, 900], (255, 233, 160, 255), (255, 181, 71, 255), 6)
        E([225, 815, 275, 865], (255, 255, 255, 255))
        P_(R._star(500, 190, 34, 15), (255, 181, 71, 255))
    return im.resize((1000, 1000), Image.LANCZOS)


def alt_fox(b):  # A3 vizorlu tilki / B3 ay cocugu
    im, d, S, E, P_, Rr, Ln, Ar = _kit()
    ink = (11, 8, 48, 255)
    if b["ch"] == "robot":
        P_([(220, 340), (290, 110), (440, 270)], (104, 64, 255, 255), ink); P_([(780, 340), (710, 110), (560, 270)], (104, 64, 255, 255), ink)
        P_([(270, 300), (300, 180), (390, 270)], (255, 79, 123, 255)); P_([(730, 300), (700, 180), (610, 270)], (255, 79, 123, 255))
        P_([(700, 800), (930, 700), (900, 900), (760, 930)], (104, 64, 255, 255), ink)
        Rr([300, 640, 700, 930], 80, (42, 27, 122, 255), ink, 8)
        Rr([440, 700, 560, 800], 18, (200, 255, 46, 255), ink, 5)
        for x in (190, 700):
            Rr([x, 680, x + 110, 860], 50, (58, 36, 160, 255), ink, 6)
        for x in (330, 540):
            Rr([x, 900, x + 130, 975], 36, (30, 16, 84, 255), ink, 6)
        E([200, 230, 800, 690], (58, 36, 160, 255), ink, 8)
        Rr([250, 370, 750, 530], 70, (8, 10, 28, 255), (200, 255, 46, 255), 8)
        E([350, 415, 420, 490], (200, 255, 46, 255)); E([580, 415, 650, 490], (200, 255, 46, 255))
        Ln([(280, 400), (400, 395)], (244, 247, 255, 160), 5)
        P_([(465, 570), (535, 570), (500, 610)], (255, 79, 123, 255)); Ar([440, 585, 560, 650], 20, 160, (200, 255, 46, 255), 7)
    else:
        Rr([320, 680, 680, 960], 120, (12, 70, 86, 255), (2, 3, 12, 255), 8)
        Rr([240, 700, 340, 860], 45, (16, 102, 126, 255), (2, 3, 12, 255), 6); Rr([660, 700, 760, 860], 45, (16, 102, 126, 255), (2, 3, 12, 255), 6)
        E([220, 190, 780, 710], (255, 233, 160, 255), (2, 3, 12, 255), 8)
        for cx_, cy_, r_ in ((330, 320, 30), (650, 600, 36), (300, 560, 20)):
            E([cx_ - r_, cy_ - r_, cx_ + r_, cy_ + r_], (240, 205, 120, 255))
        Ar([330, 410, 450, 470], 200, 340, (3, 5, 18, 255), 9); Ar([550, 410, 670, 470], 200, 340, (3, 5, 18, 255), 9)
        Ar([430, 500, 570, 590], 20, 160, (3, 5, 18, 255), 9)
        E([300, 500, 360, 540], (255, 181, 71, 140)); E([640, 500, 700, 540], (255, 181, 71, 140))
        P_([(260, 220), (500, 40), (760, 230)], (7, 11, 36, 255), (255, 181, 71, 255))
        P_(R._star(500, 150, 38, 17), (255, 181, 71, 255))
        for x, y in ((420, 800), (580, 840), (500, 900)):
            P_(R._star(x, y, 18, 8), (255, 181, 71, 255))
    return im.resize((1000, 1000), Image.LANCZOS)

def build(key):
    b = BR[key]; out = os.path.join(ROOT, key); alt = os.path.join(out, "alternatif"); tut = os.path.join(out, "tutarlilik")
    for p in (alt, tut):
        os.makedirs(p, exist_ok=True)
    fn = R.CHARS[b["ch"]]
    # --- yon alternatifleri
    W, H = 2400, 900
    c = bg(b, (W, H)); d = ImageDraw.Draw(c)
    dirs = [("Yon 1 (SECILEN): " + ("robot" if b["ch"] == "robot" else "baykus") + " " + b["name"], fn()), ("Yon 2: " + ("damla ruh" if b["ch"] == "robot" else "fener ruhu"), alt_blob(b)), ("Yon 3: " + ("vizorlu tilki" if b["ch"] == "robot" else "ay cocugu"), alt_fox(b))]
    for i, (t, s) in enumerate(dirs):
        put(c, s, 40 + i * 790, 90, 740); label(d, (410 + i * 790, 50), t, F(b, 38), b["acc"] if i == 0 else b["txt"])
    c.save(os.path.join(out, "yon-alternatifleri.png"))
    # --- karakter karti
    W, H = 2400, 2000
    c = bg(b, (W, H), 3); d = ImageDraw.Draw(c)
    label(d, (W // 2, 70), f"{b['brand']} - AI host: {b['name']}", F(b, 64), b["acc"])
    label(d, (W // 2, 128), "AI-generated character (stylized, not a real person)", F(b, 30), b["txt"])
    for i, (yw, nm) in enumerate(((0.0, "on"), (0.5, "3/4"), (1.0, "yan"))):
        put(c, fn(yaw=yw), 80 + i * 760, 170, 700); label(d, (430 + i * 760, 880), nm, F(b, 34), b["txt"])
    for i, e in enumerate(R.EXPRS):
        put(c, fn(expr=e), 20 + i * 395, 940, 380); label(d, (210 + i * 395, 1345), {"curious": "merak", "surprise": "saskinlik", "laugh": "gulme", "eureka": "iste bu", "suspicion": "suphe", "neutral": "notr"}[e], F(b, 32), b["txt"])
    label(d, (60, 1380), "Renk paleti (renk-font-karari.md ile ayni)", F(b, 38), b["acc"], "lm")
    for i, (hx, nm) in enumerate(b["sw"]):
        x = 60 + i * 330
        d.rounded_rectangle([x, 1430, x + 290, 1580], radius=22, fill=hx, outline=b["txt"], width=3)
        label(d, (x + 145, 1620), f"{hx} {nm}", F(b, 28), b["txt"])
    notes = (["Kiyafet/donanim: hediye kasasi gogus + parasut kayislari + pembe fiyonkli anten", "Yuz: koyu ekran, limon yesil goz/agiz (sadece vurgu)", "Ses/ton: enerjik, kisa cumleler, 'drop' ani"] if b["ch"] == "robot" else
             ["Kiyafet: amber esarp + alinda amber yildiz, krem karin", "Yuz: buyuk krem goz diskleri, amber iris (isik = merak)", "Ses/ton: sakin, gizemli, hikaye anlatici"])
    for i, t in enumerate(notes):
        label(d, (60, 1700 + i * 60), "- " + t, F(b, 34), b["txt"], "lm")
    c.save(os.path.join(out, "karakter-karti.png"))
    # --- 10 poz tutarlilik seti
    sheet = bg(b, (2500, 1000), 5); sd = ImageDraw.Draw(sheet)
    for i, (yw, ex, al, ar, tl) in enumerate(R.POSES):
        sp = R.render(b["ch"], tilt=tl, yaw=yw, expr=ex, armL=al, armR=ar)
        t = bg(b, (1000, 1000), 10 + i); t.paste(sp, (0, 0), sp); t.save(os.path.join(tut, f"poz-{i + 1:02d}.png"))
        put(sheet, sp, (i % 5) * 500, (i // 5) * 500, 500)
    sheet.save(os.path.join(out, "tutarlilik-10-poz.png"))
    print("ok", key)


if __name__ == "__main__":
    for k in BR:
        build(k)
