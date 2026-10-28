"""DERIN-HIZ-3: YouTube altyazı-önce. VTT ayrıştırma (oto altyazı kayan-pencere tekrarı atılır) + doğrulama; bozuksa None -> ASR."""
import re, subprocess, tempfile
from pathlib import Path

NW = 0x08000000
ZAMAN = re.compile(r"(\d+):(\d\d):(\d\d)\.(\d+) --> (\d+):(\d\d):(\d\d)\.(\d+)")


def vtt_segment(p):
    """Cue başına yalnız yeni satırlar; son 6 yazılan satırda geçen tekrar atılır. [{b,s,t}]"""
    seg, son = [], []
    cue, b, s = [], None, None
    def bosalt():
        for l in cue:
            if l and l not in son:
                seg.append({"b": round(b, 1), "s": round(s, 1), "t": l}); son.append(l)
        del son[:-6]
    for ham in p.read_text(encoding="utf-8", errors="replace").splitlines() + [""]:
        m = ZAMAN.search(ham)
        if m:
            if cue and b is not None: bosalt()
            g = list(map(int, m.groups()[:3] + m.groups()[4:7]))
            b = g[0] * 3600 + g[1] * 60 + g[2] + int(m.group(4)) / 1000
            s = g[3] * 3600 + g[4] * 60 + g[5] + int(m.group(8)) / 1000
            cue = []
        elif b is not None and ham.strip() and not ham.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            cue.append(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", ham)).strip())
    return seg


def gecerli(seg, sure):
    """Kaba sağlık: kelime/sn 0,8–4,5 ve kapsama ≥%70 (bozuk ayrıştırma/kısmi altyazı ASR'ye düşer)."""
    if not seg or not sure:
        return False
    n = sum(len(x["t"].split()) for x in seg)
    return 0.8 <= n / sure <= 4.5 and seg[-1]["s"] >= 0.7 * sure


def getir(kod, sure, dil):
    """(dil, segmentler) ya da None. Yalnız videonun kendi dili (çeviri izi yok: dil uyuşmazlığı benzerliği 0,01 yapıyordu). yt-dlp zaman aşımı 60 sn, 1 yeniden deneme."""
    if not dil:
        return None
    with tempfile.TemporaryDirectory(prefix="alt_") as d:
        d = Path(d)
        for _ in range(2):
            try:
                subprocess.run(["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", f"{dil}.*,{dil}", "--sub-format", "vtt", "-o", str(d / "a.%(ext)s"), f"https://www.youtube.com/watch?v={kod}"],
                               capture_output=True, text=True, timeout=60, creationflags=NW)
                break
            except subprocess.TimeoutExpired:
                continue
        fs = sorted(d.glob("a.*.vtt"), key=lambda f: (".orig" in f.name, f.name))
        for f in fs:
            seg = vtt_segment(f)
            if gecerli(seg, sure):
                return f.name.split(".")[1].split("-")[0], seg
    return None
