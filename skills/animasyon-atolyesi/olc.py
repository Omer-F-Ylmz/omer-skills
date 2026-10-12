"""ANİMASYON-1: animasyon çıktısını headless ölçer — pencere açmaz.
    python tools/animasyon/olc.py <dosya.html|.mp4|.webm|.glb> [--kare <klasör>]
.html → Chromium headless (swiftshader WebGL): fps (rAF, 2 sn), p95 kare süresi, hareket (iki kare farkı), konsol hatası,
        scroll sonrası kare, prefers-reduced-motion var mı, düzen özelliği animasyonu (width/height/top/left/margin) var mı.
.mp4/.webm → ffprobe en/boy/fps/süre + %10/%50/%90 kareleri, kareler arası fark (hareket), boş kare denetimi.
.glb → animasyon/kanal/mesh sayısı.
Çıktı: tek satır JSON (stdout); kareler --kare klasörüne PNG.
"""
import argparse
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

PENCERESIZ = 0x08000000 if sys.platform == "win32" else 0
DUZEN = re.compile(r"(transition|animation)[^;{}]*\b(width|height|top|left|right|bottom|margin)\b"
                   r"|gsap\.(to|from|fromTo)\([^)]*\b(width|height|top|left|margin)\s*:", re.I)


def fark(a, b):
    """İki görüntü arası ortalama piksel farkı (0–1)."""
    with Image.open(a) as x, Image.open(b) as y:
        d = ImageChops.difference(x.convert("L"), y.convert("L").resize(x.size))
        return round(ImageStat.Stat(d).mean[0] / 255, 4)


def dolu(png):
    """Kare boş (tek renk) değilse True."""
    with Image.open(png) as x:
        return ImageStat.Stat(x.convert("L")).stddev[0] > 2


def glb(yol):
    b = Path(yol).read_bytes()
    sihir, surum, _ = struct.unpack_from("<4sII", b)
    n, tur = struct.unpack_from("<I4s", b, 12)
    if (sihir, surum, tur) != (b"glTF", 2, b"JSON"):
        return {"gecerli": False}
    j = json.loads(b[20:20 + n])
    an = j.get("animations", [])
    return {"gecerli": True, "animasyon": len(an), "kanal": sum(len(a.get("channels", [])) for a in an),
            "mesh": len(j.get("meshes", [])), "kb": round(len(b) / 1024, 1)}


def video(yol, kare):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(yol)],
                       capture_output=True, text=True, creationflags=PENCERESIZ)
    j = json.loads(p.stdout or "{}")
    s, sure = (j.get("streams") or [{}])[0], float(j.get("format", {}).get("duration", 0))
    a, b = (s.get("r_frame_rate") or "0/1").split("/")
    kareler = []
    for oran in (0.1, 0.5, 0.9):
        png = kare / f"v{int(oran * 100)}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{sure * oran:.2f}", "-i", str(yol), "-frames:v", "1", str(png)],
                       creationflags=PENCERESIZ)
        if png.is_file():
            kareler.append(png)
    return {"en": s.get("width"), "boy": s.get("height"), "fps": round(int(a) / max(int(b), 1), 2), "sure_sn": round(sure, 2),
            "kb": round(Path(yol).stat().st_size / 1024, 1), "dolu": all(map(dolu, kareler)) and len(kareler) == 3,
            "hareket": fark(kareler[0], kareler[-1]) if len(kareler) == 3 else 0}


FPS_JS = """() => new Promise(r => { const t = []; let s = performance.now();
  const f = n => { t.push(n); if (n - s < 2000) requestAnimationFrame(f); else {
    const d = t.slice(1).map((x, i) => x - t[i]).sort((a, b) => a - b);
    r({fps: Math.round((t.length - 1) / ((t.at(-1) - t[0]) / 1000)), p95: Math.round(d[Math.floor(d.length * .95)] || 0)}); } };
  requestAnimationFrame(f); })"""


def sayfa(yol, kare):
    from playwright.sync_api import sync_playwright
    kaynak = Path(yol).read_text(encoding="utf-8", errors="replace")
    hata = []
    with sync_playwright() as pw:
        t = pw.chromium.launch(headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        s = t.new_page(viewport={"width": 1280, "height": 720})
        s.on("pageerror", lambda e: hata.append(str(e)[:120]))
        s.on("console", lambda m: m.type == "error" and hata.append(m.text[:120]))
        s.goto(Path(yol).resolve().as_uri(), wait_until="load")
        s.wait_for_timeout(150)
        s.screenshot(path=kare / "h0.png")
        s.wait_for_timeout(1200)
        s.screenshot(path=kare / "h1.png")
        olcu = s.evaluate(FPS_JS)
        uzun = s.evaluate("document.documentElement.scrollHeight") > 720 * 1.2
        if uzun:
            for _ in range(6):
                s.mouse.wheel(0, 400)
                s.wait_for_timeout(250)
            s.wait_for_timeout(600)
            s.screenshot(path=kare / "h2.png")
        t.close()
    return {**olcu, "hareket": fark(kare / "h0.png", kare / "h1.png"),
            "scroll_hareket": fark(kare / "h1.png", kare / "h2.png") if uzun else None, "dolu": dolu(kare / "h1.png"),
            "konsol_hata": len(hata), "hata_ornek": hata[:2], "reduced_motion": "prefers-reduced-motion" in kaynak,
            "duzen_animasyonu": bool(DUZEN.search(kaynak)), "kb": round(len(kaynak.encode()) / 1024, 1)}


def olc(yol, kare):
    yol, kare = Path(yol), Path(kare)
    kare.mkdir(parents=True, exist_ok=True)
    if not yol.is_file():
        return {"dosya": str(yol), "yok": True}
    uz = yol.suffix.lower()
    f = {".html": sayfa, ".htm": sayfa, ".mp4": video, ".webm": video, ".mov": video}.get(uz)
    return {"dosya": yol.name, **(glb(yol) if uz == ".glb" else f(yol, kare) if f else {"desteksiz": uz})}


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("dosya")
    a.add_argument("--kare", default=None)
    a = a.parse_args()
    print(json.dumps(olc(a.dosya, a.kare or Path(a.dosya).with_suffix("").as_posix() + "-kare"), ensure_ascii=False))
