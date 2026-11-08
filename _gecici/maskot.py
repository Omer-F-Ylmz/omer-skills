import os, math
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
O = r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-onizleme\maskot-adaylari"
INK = "#2b2236"
def face(e, c, ex, ey, gap, my, body):
    L, R = ex - gap, ex + gap
    def eye(x, y, r=17, dx=0, dy=0):
        return f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*1.15}" fill="{INK}"/><circle cx="{x+dx-5}" cy="{y+dy-7}" r="{r*0.38}" fill="#fff"/><circle cx="{x+dx+5}" cy="{y+dy+6}" r="{r*0.18}" fill="#fff"/>'
    brow = lambda x1,y1,x2,y2: f'<path d="M{x1} {y1} Q{(x1+x2)/2} {min(y1,y2)-8} {x2} {y2}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    cheeks = f'<ellipse cx="{L-22}" cy="{my-6}" rx="16" ry="10" fill="{c["cheek"]}" opacity=".75"/><ellipse cx="{R+22}" cy="{my-6}" rx="16" ry="10" fill="{c["cheek"]}" opacity=".75"/>'
    if e == "curious":
        s = eye(L,ey,16,4,-4)+eye(R,ey,19,4,-4)+brow(L-14,ey-34,L+14,ey-40)+brow(R-14,ey-46,R+14,ey-54)
        s += f'<ellipse cx="{ex+8}" cy="{my+4}" rx="9" ry="11" fill="{INK}"/><ellipse cx="{ex+8}" cy="{my+8}" rx="5" ry="5" fill="#e8708a"/>'
        return cheeks + s
    if e == "surprised":
        s = eye(L,ey,23)+eye(R,ey,23)+brow(L-16,ey-44,L+16,ey-50)+brow(R-16,ey-50,R+16,ey-44)
        s += f'<ellipse cx="{ex}" cy="{my+8}" rx="16" ry="22" fill="{INK}"/><ellipse cx="{ex}" cy="{my+19}" rx="10" ry="8" fill="#e8708a"/>'
        for sx, sy in [(L-50, ey-50), (R+50, ey-40)]:
            s += f'<path d="M{sx} {sy-14} L{sx+4} {sy-4} L{sx+14} {sy} L{sx+4} {sy+4} L{sx} {sy+14} L{sx-4} {sy+4} L{sx-14} {sy} L{sx-4} {sy-4}Z" fill="#ffd166"/>'
        return cheeks + s
    if e == "skeptical":
        s = eye(L,ey,16,-3,2)+eye(R,ey,16,-3,2)
        for x in (L, R):
            s += f'<path d="M{x-21} {ey-22} L{x+21} {ey-22} L{x+21} {ey-2} L{x-21} {ey-2}Z" fill="{body}"/><path d="M{x-20} {ey-3} L{x+20} {ey-3}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        s += brow(L-16,ey-32,L+16,ey-22)+brow(R-16,ey-48,R+16,ey-46)
        s += f'<path d="M{ex-18} {my+6} Q{ex-6} {my-2} {ex+4} {my+6} T{ex+22} {my+2}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        return cheeks + s
    if e == "happy":
        s = eye(L,ey)+eye(R,ey)
        s += f'<path d="M{ex-20} {my-2} Q{ex} {my+24} {ex+20} {my-2}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        return cheeks + s
    if e == "laughing":
        s = ''.join(f'<path d="M{x-17} {ey+4} Q{x} {ey-18} {x+17} {ey+4}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>' for x in (L,R))
        s += f'<path d="M{ex-26} {my-6} Q{ex} {my+2} {ex+26} {my-6} Q{ex+24} {my+34} {ex} {my+34} Q{ex-24} {my+34} {ex-26} {my-6}Z" fill="{INK}"/><path d="M{ex-14} {my+26} Q{ex} {my+14} {ex+14} {my+26} Q{ex} {my+36} {ex-14} {my+26}Z" fill="#e8708a"/>'
        s += f'<path d="M{L-24} {ey+10} q-6 14 0 20 q6 -6 0 -20Z" fill="#8fd3ff"/><path d="M{R+24} {ey+10} q-6 14 0 20 q6 -6 0 -20Z" fill="#8fd3ff"/>'
        return cheeks + s
EXPR = ["curious", "surprised", "skeptical", "happy", "laughing"]
def body_pufo(c):
    tufts = ''.join(f'<path d="M{x} 118 Q{x+dx} 80 {x+dx*2} {y}" stroke="{c["main"]}" stroke-width="18" stroke-linecap="round" fill="none"/>' for x,dx,y in [(185,-8,86),(200,0,76),(215,9,86)])
    return (f'<ellipse cx="150" cy="168" rx="26" ry="26" fill="{c["dark"]}"/><ellipse cx="250" cy="168" rx="26" ry="26" fill="{c["dark"]}"/>'
            f'<ellipse cx="162" cy="352" rx="26" ry="16" fill="{c["dark"]}"/><ellipse cx="238" cy="352" rx="26" ry="16" fill="{c["dark"]}"/>'
            f'{tufts}<ellipse cx="200" cy="245" rx="135" ry="112" fill="{c["main"]}"/><ellipse cx="200" cy="300" rx="80" ry="45" fill="{c["belly"]}" opacity=".7"/>'), (200, 225, 52, 292)
def body_lumi(c):
    cl = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["main"]}"/>' for x,y,r in [(125,250,66),(275,250,66),(200,190,82),(200,265,88),(150,205,60),(250,205,60)])
    return (f'<path d="M200 118 Q205 78 222 62" stroke="{c["dark"]}" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="224" cy="58" r="14" fill="#fff3a3"/><circle cx="224" cy="58" r="22" fill="#fff3a3" opacity=".35"/>'
            f'<ellipse cx="160" cy="345" rx="24" ry="14" fill="{c["dark"]}"/><ellipse cx="240" cy="345" rx="24" ry="14" fill="{c["dark"]}"/>'
            f'<ellipse cx="82" cy="262" rx="20" ry="26" fill="{c["dark"]}"/><ellipse cx="318" cy="262" rx="20" ry="26" fill="{c["dark"]}"/>{cl}'
            f'<ellipse cx="200" cy="305" rx="70" ry="34" fill="{c["belly"]}" opacity=".7"/>'), (200, 225, 54, 292)
def body_sprout(c):
    return (f'<path d="M200 102 Q150 40 118 66 Q132 112 200 104Z" fill="#7fd6a0"/><path d="M200 104 Q250 36 284 62 Q268 110 200 104Z" fill="#5cc486"/><path d="M200 106 L200 82" stroke="#3c9c68" stroke-width="5"/>'
            f'<ellipse cx="112" cy="260" rx="22" ry="30" fill="{c["dark"]}" transform="rotate(14 112 260)"/><ellipse cx="288" cy="260" rx="22" ry="30" fill="{c["dark"]}" transform="rotate(-14 288 260)"/>'
            f'<ellipse cx="165" cy="368" rx="24" ry="13" fill="{c["dark"]}"/><ellipse cx="235" cy="368" rx="24" ry="13" fill="{c["dark"]}"/>'
            f'<ellipse cx="200" cy="240" rx="108" ry="135" fill="{c["main"]}"/><ellipse cx="200" cy="315" rx="62" ry="42" fill="{c["belly"]}" opacity=".7"/>'), (200, 215, 46, 280)
CAND = {
 "A-pufo": (body_pufo, dict(main="#ffb48a", dark="#f08c62", belly="#ffe2cf", cheek="#ff7f8f")),
 "B-lumi": (body_lumi, dict(main="#7fd8d0", dark="#4fb3ac", belly="#d4f6f1", cheek="#ff9aa8")),
 "C-sprout": (body_sprout, dict(main="#c4a8ff", dark="#9a7be0", belly="#eadfff", cheek="#ff8fb0")),
}
def svg(name, e):
    fn, c = CAND[name]
    b, (ex, ey, gap, my) = fn(c)
    tilt = ' transform="rotate(-5 200 250)"' if e == "curious" else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400"><defs>'
            f'<filter id="f" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".07" numOctaves="3" seed="4"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter></defs>'
            f'<g{tilt}><g filter="url(#f)">{b}</g>{face(e, c, ex, ey, gap, my, c["main"])}</g></svg>')
os.makedirs(O, exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 400, "height": 400})
    for n in CAND:
        d = os.path.join(O, n); os.makedirs(d, exist_ok=True)
        for e in EXPR:
            open(os.path.join(d, e + ".svg"), "w", encoding="utf-8").write(svg(n, e))
            pg.set_content(f'<body style="margin:0;background:transparent">{svg(n, e)}</body>')
            pg.screenshot(path=os.path.join(d, e + ".png"), omit_background=True)
    br.close()
f = ImageFont.truetype("arial.ttf", 22)
for n in CAND:
    sh = Image.new("RGB", (5 * 300, 340), "#fff7ec"); dr = ImageDraw.Draw(sh)
    for i, e in enumerate(EXPR):
        im = Image.open(os.path.join(O, n, e + ".png")).convert("RGBA").resize((300, 300))
        sh.paste(im, (i * 300, 10), im); dr.text((i * 300 + 110, 312), e, fill="#2b2236", font=f)
    sh.save(os.path.join(O, n + "-ifade-tablosu.png"))
print("ok")
