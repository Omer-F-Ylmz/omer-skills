"""video_intro.py - ffmpeg ile tek sahnelik başlık intro'su (Python stdlib + ffmpeg; npm/Remotion yok).

Kullanım:
    python video_intro.py --baslik "Omer Skills" --alt "Animasyon Atölyesi" --cikti intro.mp4
    python video_intro.py --baslik "Rapor: 2026" --sure 5 --en 1920 --boy 1080 --renk1 "#111827" --renk2 "#7c3aed" --vurgu "#22d3ee"

Nasıl uyarlanır:
    - Zamanlama: ZAMAN sözlüğündeki başlangıç/süre değerlerini değiştir (her öğe kendi ease-out'unu kullanır).
    - Yerleşim/boyut: filtre() içindeki h*... katsayıları ve punto oranları; renkler argümanla gelir.
    - Yeni öğe: filtre listesine bir drawtext/drawbox daha ekle, alpha/x/y için kolay() ifadesini kullan.

Ne zaman Remotion/hyperframes'e geç:
    Çok sahneli kurgu, veriye bağlı (grafik, sayaç, liste) ya da React bileşeni/tasarım sistemi
    yeniden kullanan işler; bu tarif tek sahne + birkaç metin katmanı için en ucuz yoldur.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ZAMAN = {"baslik": (0.2, 0.9), "cizgi": (0.6, 0.8), "alt": (1.1, 0.8)}  # (başlangıç sn, süre sn)


def esc(deger):
    """Filtre seçenek değeri için iki seviyeli ffmpeg kaçışı (seçenek + filtergraph)."""
    for k in "\\':":
        deger = deger.replace(k, "\\" + k)
    for k in "\\'[],;":
        deger = deger.replace(k, "\\" + k)
    return deger


def kolay(ad):
    """ease-out cubic: 1-(1-p)^3, p = [0,1]'e kırpılmış ilerleme."""
    t0, d = ZAMAN[ad]
    return f"(1-pow(1-clip((t-{t0})/{d},0,1),3))"


def varsayilan_font():
    for yol in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(yol):
            return yol
    return None  # ffmpeg/fontconfig varsayılanı


def filtre(a):
    font = f":fontfile={esc(a.font)}" if a.font else ""
    eb, ec, ea = kolay("baslik"), kolay("cizgi"), kolay("alt")
    cw = int(a.en * 0.22)
    return ",".join([
        f"gradients=s={a.en}x{a.boy}:r={a.fps}:d={a.sure}:c0={esc(a.renk1)}:c1={esc(a.renk2)}"
        f":x0=0:y0=0:x1={a.en}:y1={a.boy}:nb_colors=2:speed=0.01",
        # başlık: yukarı kayarak + saydamlıktan belirir
        f"drawtext=text={esc(a.baslik)}:expansion=none{font}:fontsize={int(a.boy * 0.1)}:fontcolor=white"
        f":x='(w-tw)/2':y='h*0.44-th+{int(a.boy * 0.06)}*(1-{eb})':alpha='{eb}'"
        f":shadowcolor=black@0.35:shadowx=0:shadowy=4",
        # vurgu çizgisi: soldan büyür (drawbox w=0 tam genişlik demek, o yüzden enable + max)
        f"drawbox=x={(a.en - cw) // 2}:y='ih*0.50':w='max(2,{cw}*{ec})':h={max(4, a.boy // 120)}"
        f":color={esc(a.vurgu)}:t=fill:enable='gte(t,{ZAMAN['cizgi'][0]})'",
        # alt başlık: gecikmeli belirir
        f"drawtext=text={esc(a.alt)}:expansion=none{font}:fontsize={int(a.boy * 0.042)}:fontcolor=white@0.85"
        f":x='(w-tw)/2':y='h*0.55+{int(a.boy * 0.025)}*(1-{ea})':alpha='{ea}'",
        f"fade=t=out:st={a.sure - 0.5}:d=0.5",
        "format=yuv420p",
    ])


def main():
    p = argparse.ArgumentParser(description="ffmpeg başlık intro'su")
    p.add_argument("--baslik", required=True)
    p.add_argument("--alt", default="")
    p.add_argument("--cikti", required=True)
    p.add_argument("--sure", type=float, default=4)
    p.add_argument("--en", type=int, default=1280)
    p.add_argument("--boy", type=int, default=720)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--renk1", default="#0f172a")
    p.add_argument("--renk2", default="#4338ca")
    p.add_argument("--vurgu", default="#f59e0b")
    p.add_argument("--font", default=varsayilan_font())
    a = p.parse_args()

    Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
    komut = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", filtre(a),
             "-t", str(a.sure), "-c:v", "libx264", "-crf", "20", "-preset", "medium",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.cikti]
    r = subprocess.run(komut, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       creationflags=0x08000000 if os.name == "nt" else 0)
    if r.returncode:
        sys.exit(f"ffmpeg hata ({r.returncode}):\n{r.stderr[-2000:]}")
    print(a.cikti)


if __name__ == "__main__":
    main()
