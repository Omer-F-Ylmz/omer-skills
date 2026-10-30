"""SUNUCU-KARAKTER-1: kod ile cizilen iki AI sunucu karakteri (tam tutarlilik: ayni donanim, parametreli poz/ifade).
robot = Free AI Drop 'Dropi'; owl = Curiosity Well 'Wick'. Sprite 1000x1000 RGBA."""
import math
from PIL import Image, ImageDraw

S = 2
N = 1000 * S


def _c(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def _arm(d, sh, ang, ln, w, col, line, side):
    a = math.radians(ang)
    sx = -1 if side == "L" else 1
    ex, ey = sh[0] + sx * math.sin(a) * ln, sh[1] + math.cos(a) * ln
    for ww, cc in ((w + 14, line), (w, col)):
        d.line([(sh[0] * S, sh[1] * S), (ex * S, ey * S)], fill=cc, width=int(ww * S))
        for p in ((sh[0], sh[1]), (ex, ey)):
            d.ellipse([(p[0] - ww / 2) * S, (p[1] - ww / 2) * S, (p[0] + ww / 2) * S, (p[1] + ww / 2) * S], fill=cc)
    return ex, ey


def _rr(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle([v * S for v in box], radius=r * S, fill=fill, outline=outline, width=width * S)


def _el(d, box, fill, outline=None, width=0):
    d.ellipse([v * S for v in box], fill=fill, outline=outline, width=width * S)


def _poly(d, pts, fill, outline=None):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)


def _star(cx, cy, r, ri=None, n=5, rot=-90):
    ri = ri or r * 0.45
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def _hand(d, p, col, line, r=40):
    _el(d, [p[0] - r - 6, p[1] - r - 6, p[0] + r + 6, p[1] + r + 6], line)
    _el(d, [p[0] - r, p[1] - r, p[0] + r, p[1] + r], col)


# ---------------------------------------------------------------- ROBOT (Free AI Drop)
P = dict(night="#080A1C", deep="#1E1054", glow="#6840FF", lime="#C8FF2E", mint="#46FFA8", white="#F4F7FF", pink="#FF4F7B",
         body="#2A1B7A", head="#3A24A0", line="#0B0830")


def robot(yaw=0.0, expr="neutral", mouth=None, armL=8, armR=8, blink=False):
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ay = abs(yaw)
    cx = 500 + yaw * 20
    k = 1 - 0.35 * ay
    line = _c(P["line"])
    # legs
    for sx in (-1, 1):
        _rr(d, [cx + sx * 85 * k - 48, 860, cx + sx * 85 * k + 48, 960], 30, _c(P["deep"]), line, 7)
    # body
    _rr(d, [cx - 170 * k, 600, cx + 170 * k, 880], 90, _c(P["body"]), line, 8)
    # chest crate (hediye kasasi) + pembe fiyonk seridi
    ox = yaw * 55
    _rr(d, [cx + ox - 78 * k, 665, cx + ox + 78 * k, 800], 22, _c(P["lime"]), line, 6)
    _rr(d, [cx + ox - 12 * k, 665, cx + ox + 12 * k, 800], 4, _c(P["pink"]))
    _rr(d, [cx + ox - 78 * k, 722, cx + ox + 78 * k, 744], 4, _c(P["pink"]))
    # parasut kayislari
    for sx in (-1, 1):
        d.line([((cx + sx * 120 * k) * S, 610 * S), ((cx + sx * 70 * k) * S, 800 * S)], fill=_c(P["mint"]), width=10 * S)
    # kollar
    late = []
    for side, ang in (("L", armL), ("R", armR)):
        sx = -1 if side == "L" else 1
        if ay > 0.6 and ((yaw > 0) == (side == "L")):
            ang = min(ang, 25)
        sh = (cx + sx * 170 * k, 660)
        if ang > 100:
            late.append(lambda sh=sh, ang=ang, side=side: _hand(d, _arm(d, sh, ang, 150, 52, _c(P["head"]), line, side), _c(P["lime"]), line))
            continue
        e = _arm(d, sh, ang, 150, 52, _c(P["head"]), line, side)
        _hand(d, e, _c(P["lime"]), line)
    # kulaklar
    for sx in (-1, 1):
        sc = 1 - 0.5 * max(0, sx * yaw)
        _el(d, [cx + sx * 245 * k - 28 * sc, 360, cx + sx * 245 * k + 28 * sc, 440], _c(P["glow"]), line, 6)
    # anten + fiyonk
    d.line([(cx * S, 215 * S), (cx * S, 150 * S)], fill=line, width=14 * S)
    _el(d, [cx - 22, 120, cx + 22, 164], _c(P["lime"]), line, 6)
    for sx in (-1, 1):
        _poly(d, [(cx, 142), (cx + sx * 60, 108), (cx + sx * 60, 176)], _c(P["pink"]), line)
    # kafa
    hw = 460 * (1 - 0.12 * ay)
    _rr(d, [cx - hw / 2, 215, cx + hw / 2, 590], 110, _c(P["head"]), line, 8)
    # ekran
    sxc = cx + yaw * 105
    sw = 370 * (1 - 0.38 * ay)
    sy = 405
    _rr(d, [sxc - sw / 2, sy - 125, sxc + sw / 2, sy + 125], 70, _c(P["night"]), _c(P["glow"]), 6)
    ex = 105 * (1 - 0.4 * ay)
    L, R = _c(P["lime"]), _c(P["mint"])
    eyes = [(sxc - ex, sy - 30), (sxc + ex, sy - 30)]
    my = sy + 70
    if blink:
        expr_eyes = "blink"
    else:
        expr_eyes = expr
    for i, (x, y) in enumerate(eyes):
        w = 28 * (1 - 0.25 * ay)
        if expr_eyes == "neutral":
            _rr(d, [x - w, y - 38, x + w, y + 38], 22, L)
        elif expr_eyes == "blink":
            d.line([((x - w) * S, y * S), ((x + w) * S, y * S)], fill=L, width=10 * S)
        elif expr_eyes == "curious":
            big = 1.25 if i == 0 else 0.8
            _rr(d, [x - w * big, y - 38 * big, x + w * big, y + 38 * big], 22, L)
            if i == 1:
                d.line([((x - 35) * S, (y - 62) * S), ((x + 35) * S, (y - 82) * S)], fill=L, width=9 * S)
        elif expr_eyes == "surprise":
            _el(d, [x - 42, y - 46, x + 42, y + 46], L)
            _el(d, [x - 20, y - 24, x + 20, y + 16], _c(P["night"]))
            _el(d, [x - 12, y - 18, x, y - 6], _c(P["white"]))
        elif expr_eyes == "laugh":
            d.arc([(x - 38) * S, (y - 30) * S, (x + 38) * S, (y + 40) * S], 200, 340, fill=L, width=13 * S)
        elif expr_eyes == "eureka":
            _poly(d, _star(x, y, 50, 22), R)
        elif expr_eyes == "suspicion":
            _rr(d, [x - w * 1.2, y - 4, x + w * 1.2, y + 34], 12, L)
            d.line([((x - 45) * S, (y - 22 - (14 if i == 0 else -6)) * S), ((x + 45) * S, (y - 22 + (14 if i == 0 else -6)) * S)], fill=L, width=9 * S)
    # agiz
    mw = 70 * (1 - 0.25 * ay)
    mx = sxc + yaw * 12
    if mouth is not None and expr not in ("laugh",):
        m = max(0.0, min(1.0, mouth))
        h = 8 + 56 * m
        _rr(d, [mx - mw / 2, my - h / 2, mx + mw / 2, my + h / 2], min(28, h / 2 + 2), _c(P["pink"]) if m > 0.15 else L)
        if m > 0.15:
            _rr(d, [mx - mw / 2 + 8, my - h / 2 + 8, mx + mw / 2 - 8, my + h / 2 - 4], 14, _c(P["night"]))
    elif expr == "neutral":
        d.arc([(mx - 38) * S, (my - 22) * S, (mx + 38) * S, (my + 14) * S], 20, 160, fill=L, width=9 * S)
    elif expr == "curious":
        _el(d, [mx - 12 + 26, my - 12, mx + 12 + 26, my + 14], L)
    elif expr == "surprise":
        _el(d, [mx - 22, my - 28, mx + 22, my + 28], _c(P["pink"]), line, 5)
        _el(d, [mx - 14, my - 18, mx + 14, my + 18], _c(P["night"]))
    elif expr == "laugh":
        m = 0.9 if mouth is None else 0.5 + 0.5 * mouth
        _poly(d, [(mx - 60, my - 22), (mx + 60, my - 22), (mx + 40, my + 18 + 22 * m), (mx - 40, my + 18 + 22 * m)], _c(P["pink"]), line)
        _rr(d, [mx - 36, my - 14, mx + 36, my + 4], 5, _c(P["white"]))
    elif expr == "eureka":
        d.arc([(mx - 55) * S, (my - 40) * S, (mx + 55) * S, (my + 30) * S], 10, 170, fill=L, width=12 * S)
        for a in (-60, -20, 20, 60):
            r0, r1 = 190, 245
            a_ = math.radians(a - 90)
            d.line([((cx + r0 * math.cos(a_)) * S, (330 + r0 * math.sin(a_)) * S), ((cx + r1 * math.cos(a_)) * S, (330 + r1 * math.sin(a_)) * S)], fill=R, width=9 * S)
    elif expr == "suspicion":
        d.line([((mx - 36) * S, (my + 4) * S), ((mx + 36) * S, (my - 10) * S)], fill=L, width=9 * S)
    for f in late:
        f()
    return im.resize((1000, 1000), Image.LANCZOS)


# ---------------------------------------------------------------- BAYKUS (Curiosity Well)
Q = dict(night="#030512", navy="#070B24", teal="#0C4656", amber="#FFB547", lamber="#FFE9A0", cream="#FFF3D6", feather="#10667E", line="#02030C")


def owl(yaw=0.0, expr="neutral", mouth=None, armL=8, armR=8, blink=False):
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ay = abs(yaw)
    cx = 500 + yaw * 20
    k = 1 - 0.3 * ay
    line = _c(Q["line"])
    # ayaklar
    for sx in (-1, 1):
        for t in (-22, 0, 22):
            _el(d, [cx + sx * 80 * k + t - 14, 930, cx + sx * 80 * k + t + 14, 975], _c(Q["amber"]), line, 4)
    # govde
    _el(d, [cx - 190 * k, 540, cx + 190 * k, 950], _c(Q["teal"]), line, 8)
    _el(d, [cx - 125 * k, 600, cx + 125 * k, 930], _c(Q["cream"]))
    for r_ in range(4):
        for c_ in (-1, 0, 1):
            xx = cx + c_ * 62 * k + (31 * k if r_ % 2 else 0) * 0.5
            d.arc([(xx - 24 * k) * S, (650 + r_ * 62) * S, (xx + 24 * k) * S, (690 + r_ * 62) * S], 20, 160, fill=_c(Q["amber"]), width=6 * S)
    # esarp
    _rr(d, [cx - 150 * k, 540, cx + 150 * k, 600], 30, _c(Q["amber"]), line, 6)
    # kanatlar
    late = []
    for side, ang in (("L", armL), ("R", armR)):
        sx = -1 if side == "L" else 1
        if ay > 0.6 and ((yaw > 0) == (side == "L")):
            ang = min(ang, 25)
        sh = (cx + sx * 180 * k, 650)
        if ang > 100:
            late.append(lambda sh=sh, ang=ang, side=side: _hand(d, _arm(d, sh, ang, 150, 70, _c(Q["feather"]), line, side), _c(Q["lamber"]), line, 34))
            continue
        e = _arm(d, sh, ang, 150, 70, _c(Q["feather"]), line, side)
        _hand(d, e, _c(Q["lamber"]), line, 34)
    # kulak tuyleri
    for sx in (-1, 1):
        _poly(d, [(cx + sx * 120 * k, 250), (cx + sx * 215 * k, 130), (cx + sx * 225 * k, 280)], _c(Q["teal"]), line)
    # kafa
    _el(d, [cx - 235 * (1 - 0.1 * ay), 215, cx + 235 * (1 - 0.1 * ay), 600], _c(Q["teal"]), line, 8)
    # alin yildizi
    fx = cx + yaw * 60
    _poly(d, _star(fx, 262, 30, 13), _c(Q["amber"]), line)
    # goz diskleri
    ex = 112 * (1 - 0.35 * ay)
    ecx = cx + yaw * 70
    ey = 400
    rd = 98
    for i, sx in enumerate((-1, 1)):
        x = ecx + sx * ex
        r_ = rd * (1.1 if (expr == "surprise") else 1.0) * (1 - 0.12 * ay)
        big = 1.18 if (expr == "curious" and i == 0) else (0.88 if (expr == "curious") else 1.0)
        r_ *= big
        if expr == "laugh" or blink:
            d.arc([(x - 70) * S, (ey - 40) * S, (x + 70) * S, (ey + 50) * S], 200, 340, fill=_c(Q["cream"]), width=14 * S)
            continue
        _el(d, [x - r_, ey - r_, x + r_, ey + r_], _c(Q["cream"]), line, 6)
        px = x + yaw * 26
        py = ey + (-12 if expr == "curious" else 0) + (10 if expr == "suspicion" else 0)
        ir = r_ * (0.42 if expr == "surprise" else 0.55)
        _el(d, [px - ir, py - ir, px + ir, py + ir], _c(Q["amber"]), line, 4)
        pr = ir * (0.35 if expr == "surprise" else 0.52)
        _el(d, [px - pr, py - pr, px + pr, py + pr], _c(Q["night"]))
        _el(d, [px - pr * 0.9 + 10, py - pr * 0.9 - 4, px - pr * 0.9 + 28, py - pr * 0.9 + 14], _c(Q["white"] if "white" in Q else "#FFFFFF"))
        if expr == "eureka":
            _poly(d, _star(px, py, ir * 0.95, ir * 0.35, 4), _c(Q["lamber"]))
        if expr == "suspicion":
            _poly(d, [(x - r_ + 4, ey - r_ + 2), (x + r_ - 4, ey - r_ + 2), (x + r_ - 4, ey - r_ * 0.1), (x - r_ + 4, ey - r_ * 0.1)], _c(Q["teal"]))
            d.line([((x - r_ + 4) * S, (ey - r_ * 0.1) * S), ((x + r_ - 4) * S, (ey - r_ * 0.1) * S)], fill=line, width=5 * S)
        # kas
        if expr == "curious" and i == 1:
            d.line([((x - 60) * S, (ey - r_ - 28) * S), ((x + 60) * S, (ey - r_ - 52) * S)], fill=_c(Q["amber"]), width=10 * S)
        if expr == "suspicion":
            dy = 10 if i == 0 else -14
            d.line([((x - 60) * S, (ey - r_ * 0.3 + dy) * S), ((x + 60) * S, (ey - r_ * 0.3 - dy) * S)], fill=_c(Q["amber"]), width=10 * S)
        if expr == "surprise":
            d.arc([(x - 55) * S, (ey - r_ - 55) * S, (x + 55) * S, (ey - r_ + 10) * S], 200, 340, fill=_c(Q["amber"]), width=9 * S)
    # gaga
    bx = ecx
    m = 0.0
    if mouth is not None:
        m = max(0.0, min(1.0, mouth))
    elif expr in ("surprise", "laugh"):
        m = 0.9
    elif expr == "eureka":
        m = 0.5
    by = 470
    _poly(d, [(bx - 42, by), (bx + 42, by), (bx, by + 66 * 0.8)], _c(Q["amber"]), line)
    if m > 0.08:
        lo = 30 * m
        _poly(d, [(bx - 34, by + 22), (bx + 34, by + 22), (bx, by + 50 + lo)], _c(Q["night"]), line)
        _poly(d, [(bx - 30, by + 26 + lo * 0.4), (bx + 30, by + 26 + lo * 0.4), (bx, by + 52 + lo)], _c(Q["amber"]), line)
    if expr == "eureka":
        for a in (-60, -20, 20, 60):
            a_ = math.radians(a - 90)
            d.line([((cx + 250 * math.cos(a_)) * S, (360 + 250 * math.sin(a_)) * S), ((cx + 305 * math.cos(a_)) * S, (360 + 305 * math.sin(a_)) * S)], fill=_c(Q["lamber"]), width=9 * S)
    for f in late:
        f()
    return im.resize((1000, 1000), Image.LANCZOS)


CHARS = {"robot": robot, "owl": owl}
EXPRS = ["curious", "surprise", "laugh", "eureka", "suspicion", "neutral"]
# 10 poz: yaw, ifade, sol kol, sag kol, egim (derece)
POSES = [
    (0.0, "neutral", 8, 8, 0), (0.0, "eureka", 8, 175, 0), (0.5, "curious", 8, 120, -6), (-0.5, "laugh", 60, 60, 6),
    (0.0, "surprise", 150, 150, 0), (1.0, "neutral", 8, 8, 0), (-1.0, "suspicion", 8, 8, 0), (0.0, "laugh", 100, 100, -5),
    (0.5, "eureka", 160, 40, 5), (0.0, "suspicion", 35, 35, 4),
]


def render(ch, tilt=0, **kw):
    im = CHARS[ch](**kw)
    if tilt:
        im = im.rotate(tilt, resample=Image.BICUBIC, center=(500, 700))
    return im
