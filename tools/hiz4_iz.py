"""VIDEO-HIZ-4 TUR 2: ses izi/bitrate seçimi doğrulaması + düzeltilmiş referans (ref2).
Kullanım (venv-ocr python): hiz4_iz.py ref2 <liste.txt> | deney <kod...>
ref2: yt-dlp -J ile ORİJİNAL (language_preference 10 / 'original' notu) en yüksek bitrate ses formatı bağımsız seçilir,
large-v3 beam5 sıralı + VAD ile dökülür → .kos/kopru/ogren/hiz4/ref2/<kod>.json (eski referans docs/video-tarama/derin dokunulmaz)."""
import difflib, json, re, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_derin  # noqa: F401  (cuBLAS/cuDNN DLL yolunu bu süreçe ekler)

KOK = Path(__file__).resolve().parents[1]
R2 = KOK / ".kos/kopru/ogren/hiz4/ref2"
NW = 0x08000000
_m = {}


def sh(*a, t=300):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, timeout=t, creationflags=NW, encoding="utf-8", errors="replace")


def orijinal_format(url):
    j = json.loads(sh("yt-dlp", "-J", "--no-playlist", url).stdout)
    ses = [f for f in j["formats"] if f.get("vcodec") == "none" and f.get("acodec") not in (None, "none") and f.get("protocol", "").startswith("http") and "drc" not in f["format_id"]]
    if not ses:
        return None
    orj = [f for f in ses if "original" in (f.get("format_note") or "").lower() or f.get("language_preference", 0) >= 10] or ses
    if len({f.get("language") for f in ses}) > 1 and orj is ses:  # çok dilli ama işaretsiz: ilk dil (yt-dlp varsayılanı)
        orj = [f for f in ses if f.get("language") == ses[0].get("language")]
    return max(orj, key=lambda f: f.get("abr") or 0)["format_id"], j


def indir_ses(url, fmt, d, ek=()):
    for p in d.glob("a.*"):
        p.unlink()
    sh("yt-dlp", "--no-playlist", "-f", fmt, *ek, "-o", d / "a.%(ext)s", url)
    return next(d.glob("a.*"), None)


def dok(ses, d):
    from faster_whisper import WhisperModel
    if "m" not in _m:
        _m["m"] = WhisperModel("large-v3", device="cuda", compute_type="float16")
    sh("ffmpeg", "-y", "-i", ses, "-vn", "-ac", "1", "-ar", "16000", d / "a.wav")
    sg, inf = _m["m"].transcribe(str(d / "a.wav"), beam_size=5, word_timestamps=True, vad_filter=True)
    return inf.language, [{"b": round(s.start, 1), "s": round(s.end, 1), "t": s.text.strip()} for s in sg]


def kel(seg):
    return re.sub(r"[^\w\s]", "", " ".join(s["t"] for s in seg).lower()).split()


def benz(a, b):
    ka, kb = kel(a), kel(b)
    return difflib.SequenceMatcher(None, ka, kb, autojunk=False).ratio() if ka or kb else 1.0


def kod_url(k):
    return k if k.startswith("http") else f"https://www.youtube.com/watch?v={k}"


def ref2(liste):
    R2.mkdir(parents=True, exist_ok=True)
    for u in re.findall(r"https?://\S+", Path(liste).read_text(encoding="utf-8")):
        k = re.search(r"(?:shorts/|v=|youtu\.be/)([\w-]+)", u).group(1)
        if (R2 / f"{k}.json").exists():
            continue
        with tempfile.TemporaryDirectory(prefix="r2_") as t:
            d = Path(t)
            try:
                f, _ = orijinal_format(u)
                ses = indir_ses(u, f, d)
                dil, seg = dok(ses, d)
                (R2 / f"{k}.json").write_text(json.dumps({"kod": k, "format": f, "dil": dil, "transkript": seg}, ensure_ascii=False), encoding="utf-8")
                print(k, f, dil, len(seg), flush=True)
            except Exception as e:
                print(k, "HATA", str(e)[:100], flush=True)


def deney(kodlar):
    for k in kodlar:
        u = kod_url(k)
        with tempfile.TemporaryDirectory(prefix="dn_") as t:
            d = Path(t)
            f, _ = orijinal_format(u)
            r = dok(indir_ses(u, f, d), d)[1]
            sonuc = {}
            for ad, ek in (("lang+abr", ["-S", "lang,+abr"]), ("lang", ["-S", "lang"]), ("lang,abr", ["-S", "lang,abr"])):
                s = indir_ses(u, "ba", d, ek)
                sonuc[ad] = round(benz(r, dok(s, d)[1]), 3)
            print(k, f, sonuc, flush=True)


if __name__ == "__main__":
    {"ref2": lambda: ref2(sys.argv[2]), "deney": lambda: deney(sys.argv[2:])}[sys.argv[1]]()
