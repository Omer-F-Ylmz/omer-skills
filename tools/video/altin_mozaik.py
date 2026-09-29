"""MOTOR-M3a K3: altın set ham kaynağı — video başına kaynak.txt (açıklama + bağlantılar + tam altyazı + kare zamanları) ve
zaman damgalı kareler + mozaikler (short/token 3×3, site 2×2) → .kos/altin/<id>/. Motor rapor/panel/adaylarına dokunmaz.
Kullanım: uv run python altin_mozaik.py (tools/video içinde)."""
import html
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from video.metin import dil_sec

KOK = Path(__file__).resolve().parents[2] / ".kos" / "altin"
ONBELLEK = Path(r"C:\Projeler\.video-cache")
SET = {"L9c49WVG_ho": "short", "g89FJiNAlEs": "uzun", "kHtOSJRUkLs": "uzun", "86HM0RUWhCk": "site", "JfmAm3sxCSc": "site"}
EN_FAZLA = 45


def _kos(a, cwd=None):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)


def zamanlar(sure, tur):
    """aralık = max(5 short / 30 uzun, süre/45); son kare videonun son %5'i içinde (0,97·süre)."""
    son = sure * 0.97
    n = max(2, min(EN_FAZLA, int(son / (5 if tur == "short" else 30)) + 1))
    return [round(0.5 + k * (son - 0.5) / (n - 1), 1) for k in range(n)]


def _hms(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def altyazi(vtt):
    """VTT → 30 sn'lik zaman damgalı paragraflar; otomatik altyazının yuvarlanan tekrar satırları tekilleşir."""
    par, onceki = {}, ""
    for blok in vtt.split("\n\n"):
        m = re.search(r"(\d+):(\d+):(\d+)\.\d+ -->", blok)
        if not m:
            continue
        t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        for s in blok.splitlines()[1:]:
            s = html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
            if s and "-->" not in s and s != onceki:
                par.setdefault(t // 30 * 30, []).append(s)
                onceki = s
    return "\n".join(f"[{_hms(k)}] {' '.join(v)}" for k, v in sorted(par.items()))


def video(vid, tur):
    d = KOK / vid
    d.mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={vid}"
    meta = json.loads(_kos(["yt-dlp", "-J", "--skip-download", url]).stdout)
    # motorun seçimi (video/metin.py dil_sec); tr video → tr öncelikli, değilse en; indirme olmazsa motorun ham .vtt önbelleği
    secim = dil_sec(meta, "tr" if (meta.get("language") or "").startswith("tr") else "en")
    vtt = []
    if secim:
        _kos(["yt-dlp", "--skip-download", "--write-subs" if secim[1] == "elle" else "--write-auto-subs", "--sub-langs", secim[0],
              "--sleep-subtitles", "3", "--sub-format", "vtt", "-o", str(d / "altyazi.%(ext)s"), url])
        vtt = [d / f"altyazi.{secim[0]}.vtt"] if (d / f"altyazi.{secim[0]}.vtt").is_file() else []
    vtt = vtt or sorted((ONBELLEK / vid).glob("altyazi.*.vtt"))
    yok = (f"altyazı yok: seçim {secim or 'yok'}; elle {sorted(meta.get('subtitles') or {})}; "
           f"oto -orig {sorted(k for k in meta.get('automatic_captions') or {} if k.endswith('-orig'))}; önbellek {ONBELLEK / vid}")
    sure = meta["duration"]
    tz = zamanlar(sure, tur)
    aki = _kos(["yt-dlp", "-g", "-f", "bv*[height<=1080]/b", url]).stdout.split()[0]
    shutil.copy(r"C:\Windows\Fonts\arial.ttf", d / "arial.ttf")  # fontfile göreli: filtre dizgesinde ':' kaçışı yok

    def kare(i):
        y = f"kare-{i + 1:03d}.png"
        _kos(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(tz[i]), "-i", aki, "-frames:v", "1", "-vf",
              f"drawtext=fontfile=arial.ttf:text='{_hms(tz[i]).replace(':', 'm')}s':x=12:y=12:fontsize=44:fontcolor=yellow:box=1:boxcolor=black@0.75",
              y], cwd=d)
        return (d / y).is_file()
    with ThreadPoolExecutor(8) as h:
        ok = list(h.map(kare, range(len(tz))))
    g = 2 if tur == "site" else 3
    en = 1920 // g
    mz = 0
    for s in range(0, len(tz), g * g):
        grup = list(range(s, min(s + g * g, len(tz))))
        mz += 1
        _kos(["ffmpeg", "-y", "-loglevel", "error", "-start_number", str(s + 1), "-i", "kare-%03d.png", "-vf",
              f"scale={en}:-2,tile={g}x{g}:nb_frames={len(grup)}", "-frames:v", "1", f"mozaik-{mz:02d}.png"], cwd=d)
    linkler = sorted(set(re.findall(r"https?://[^\s)>\]]+", meta.get("description") or "")))
    metin = altyazi(vtt[0].read_text(encoding="utf-8")) if vtt else ""
    bolum = "\n".join(f"- {_hms(c['start_time'])} {c['title']}" for c in meta.get("chapters") or [])
    (d / "kaynak.txt").write_bytes("\n".join([
        f"# {vid} · {tur} · {meta.get('title')} · {meta.get('channel')} · süre {_hms(sure)}",
        f"kare zamanları ({len(tz)}, {g}×{g} mozaik, mozaik-NN = kare {g * g} adet sırayla): " + " ".join(_hms(t) for t in tz),
        "## Açıklama", meta.get("description") or "", "## Bağlantılar", *linkler, "## Bölümler", bolum or "(yok)",
        f"## Altyazı ({vtt[0] if vtt else 'YOK'})", metin or yok]).encode("utf-8"))
    return (f"{vid} {tur} süre {_hms(sure)} kare {sum(ok)}/{len(tz)} mozaik {mz} altyazı {vtt[0] if vtt else yok} "
            f"satır {len(metin.splitlines())} bağlantı {len(linkler)}")


if __name__ == "__main__":
    assert zamanlar(60, "short")[-1] >= 57 and zamanlar(1680, "uzun")[-1] >= 1596 and len(zamanlar(1680, "uzun")) == 45
    assert len(zamanlar(600, "uzun")) == 20 and all(b - a >= 29.9 for a, b in zip(zamanlar(600, "uzun"), zamanlar(600, "uzun")[1:]))
    for vid in sys.argv[1:] or SET:
        print(video(vid, SET[vid]), flush=True)
