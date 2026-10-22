"""VIDEO-YENIDEN-1: yerel derin tarama, Claude jetonu 0.
yt-dlp -> ffmpeg (0,5 sn kare) -> faster-whisper (kelime zamanli) -> RapidOCR -> Gemini kare aciklamasi -> JSON.
Kullanim: python tools/video_derin.py <url|kod> [...]   |  --liste <dosya> [--en N]
Cikti: docs/video-tarama/derin/<kod>.json ; ilerleme: .kos/kopru/derin-ilerleme.txt (kaldigi yerden)."""
import base64, json, os, re, shutil, site, subprocess, sys, tempfile, time, urllib.request
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
CIKTI = KOK / "docs/video-tarama/derin"
ILERLEME = KOK / ".kos/kopru/derin-ilerleme.txt"
ATLA_DOSYA = KOK / ".kos/kopru/video-atla.txt"  # kalıcı atlama listesi: yeniden deneme yok
NW = 0x08000000
# cuBLAS/cuDNN pip wheel'leri (nvidia-*-cu12) DLL'lerini nvidia/*/bin altına koyar. ctranslate2 LoadLibrary'yi
# arama bayraksız çağırdığı için add_dll_directory yetmez: yalnız bu süreçin PATH'ine eklenir (sistem PATH'i değişmez).
for sp in site.getsitepackages():
    for bin_dir in Path(sp, "nvidia").glob("*/bin"):
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(bin_dir))
        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]
URL_RE = re.compile(r"(?:https?://|www\.)[^\s\"'<>]+|\b[\w.-]+\.(?:com|io|ai|dev|app|org|net|co|xyz)(?:/[^\s]*)?\b|\b[\w-]+/[\w.-]+\b(?=.*github)", re.I)
KOMUT_RE = re.compile(r"^(?:\$\s*)?(?:npm|npx|pnpm|pip|pipx|uv|git|brew|winget|docker|curl|claude|python|node)\s+.+", re.I | re.M)
_ocr = None


def kos(*a, timeout=600):
    return subprocess.run(list(map(str, a)), capture_output=True, text=True, timeout=timeout, creationflags=NW)


def kod_of(u):
    m = re.search(r"(?:reel|p|tv|shorts)/([\w-]+)|[?&]v=([\w-]+)|youtu\.be/([\w-]+)", u)
    return next((g for g in m.groups() if g), re.sub(r"\W+", "_", u)[-24:]) if m else re.sub(r"\W+", "_", u)[-24:]


def indir(url, d):
    r = kos("yt-dlp", "-f", "worst[height>=360]/worst/best", "--no-playlist", "-o", d / "v.%(ext)s", url, "--write-info-json", timeout=300)
    v = next((p for p in d.glob("v.*") if p.suffix not in (".json",)), None)
    return v, r.stderr[-200:]


def kareler(v, d, tavan=240):
    (d / "k").mkdir(exist_ok=True)
    kos("ffmpeg", "-y", "-i", v, "-vf", "fps=2,scale=640:-1", "-q:v", "4", d / "k/%04d.jpg")
    ks = sorted((d / "k").glob("*.jpg"))
    if len(ks) > tavan:  # tavani asarsa esit aralikla ornekle
        adim = len(ks) / tavan
        ks = [ks[int(i * adim)] for i in range(tavan)]
    return ks


WHISPER = {"cuda": ("large-v3-turbo", "float16"), "cpu": ("small", "int8")}
_whisper = {}


def asr(v, d):
    from faster_whisper import WhisperModel
    kos("ffmpeg", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", d / "a.wav")
    if not (d / "a.wav").exists():
        return "", []
    for aygit, (model, tip) in WHISPER.items():  # GPU başarısızsa CPU'ya düşer, hat durmaz
        try:
            if aygit not in _whisper:
                _whisper[aygit] = WhisperModel(model, device=aygit, compute_type=tip)
            seg, info = _whisper[aygit].transcribe(str(d / "a.wav"), word_timestamps=True, vad_filter=True)
            out = [{"b": round(s.start, 1), "s": round(s.end, 1), "t": s.text.strip()} for s in seg]  # üretici tüketilmeden hata yakalanmaz
            print(f"device={aygit} model={model}", flush=True)
            return info.language, out
        except Exception as e:
            _whisper.pop(aygit, None)
            print(f"device={aygit} basarisiz: {str(e)[:150]}", flush=True)
    return "", []


def ocr(ks):
    global _ocr
    from rapidocr_onnxruntime import RapidOCR
    _ocr = _ocr or RapidOCR()
    gorulen, out = set(), []
    for i, k in enumerate(ks):
        try:
            res, _ = _ocr(str(k))
        except Exception:
            continue
        for _, t, c in res or []:
            t = t.strip()
            if len(t) > 2 and float(c) > 0.6 and t.lower() not in gorulen:
                gorulen.add(t.lower())
                out.append({"k": k.name, "t": t})
    return out


KARE_PROMPT = "Bu video karelerinde ne gosteriliyor? Arac/site/teknik adlarini, adim adim ne yapildigini 6 maddede Turkce yaz."


def yerel_aciklama(ks, n=4, model="gemma4:e4b"):  # Gemini kotası/anahtarı yoksa yerel Ollama görsel model
    if not ks:
        return None
    sec = [ks[int(i * len(ks) / n)] for i in range(n)]
    istek = {"model": model, "stream": False, "think": False, "options": {"num_ctx": 8192},
             "messages": [{"role": "user", "content": KARE_PROMPT, "images": [base64.b64encode(k.read_bytes()).decode() for k in sec]}]}
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/chat", json.dumps(istek).encode(), {"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=300))["message"]["content"]
    except Exception:
        return None


def gemini_aciklama(ks, n=4):
    key = os.environ.get("GEMINI_API_KEY")
    if not key or not ks:
        return None
    sec = [ks[int(i * len(ks) / n)] for i in range(n)]
    parts = [{"text": KARE_PROMPT}]
    parts += [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(k.read_bytes()).decode()}} for k in sec]
    for model in ("gemini-flash-latest", "gemini-flash-lite-latest", "gemini-flash-latest"):
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                                         json.dumps({"contents": [{"parts": parts}]}).encode(), {"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=60))
            return r["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            continue
    return None


def atla_kodlari():
    return set(ATLA_DOSYA.read_text(encoding="utf-8").split()) if ATLA_DOSYA.exists() else set()


def isle(url):
    kod = kod_of(url)
    hedef = CIKTI / f"{kod}.json"
    if hedef.exists():
        return kod, "var"
    if kod in atla_kodlari():
        return kod, "atla"
    d = Path(tempfile.mkdtemp(prefix="vd_"))
    try:
        v, hata = indir(url, d)
        if not v:
            if "No video formats found" in hata:  # kalıcı: format yok, yeniden deneme anlamsız
                with ATLA_DOSYA.open("a", encoding="utf-8") as f:
                    f.write(kod + "\n")
                return kod, "atla"
            return kod, "indirilemedi: " + hata.strip().splitlines()[-1][:120] if hata.strip() else "indirilemedi"
        dil, seg = asr(v, d)
        ks = kareler(v, d)
        ekran = ocr(ks)
        metin = "\n".join(e["t"] for e in ekran) + "\n" + " ".join(s["t"] for s in seg)
        linkler = sorted({m.strip(".,)") for m in URL_RE.findall(metin)})
        komutlar = sorted({m.strip() for m in KOMUT_RE.findall(metin)})
        info = {}
        ij = next(d.glob("*.info.json"), None)
        if ij:
            j = json.loads(ij.read_text(encoding="utf-8"))
            info = {"baslik": j.get("title"), "sure": j.get("duration"), "yukleyen": j.get("uploader"), "aciklama": (j.get("description") or "")[:800]}
        veri = {"kod": kod, "url": url, "dil": dil, "meta": info, "transkript": seg, "ekran": ekran,
                "linkler": linkler, "komutlar": komutlar, "kare_aciklama": gemini_aciklama(ks) or yerel_aciklama(ks), "kare_sayisi": len(ks)}
        CIKTI.mkdir(parents=True, exist_ok=True)
        hedef.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        return kod, f"ok seg={len(seg)} ocr={len(ekran)} link={len(linkler)} komut={len(komutlar)}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    a = sys.argv[1:]
    en = 10**9
    if "--en" in a:
        i = a.index("--en"); en = int(a[i + 1]); del a[i:i + 2]
    if a and a[0] == "--liste":
        urls = re.findall(r"https?://\S+", Path(a[1]).read_text(encoding="utf-8"))
        urls = [u.split("\t")[0] for u in dict.fromkeys(urls)]
    else:
        urls = a
    sayac, ozet = 0, Counter()
    for u in urls:
        if sayac >= en:
            break
        t = time.time()
        kod, durum = isle(u)
        ozet[durum.split(":")[0]] += 1
        if durum not in ("var", "atla"):
            sayac += 1
        satir = f"{kod}\t{durum}\t{time.time() - t:.0f}s"
        print(satir, flush=True)
        with ILERLEME.open("a", encoding="utf-8") as f:
            f.write(satir + "\n")
        if sayac and sayac % 50 == 0 and durum not in ("var", "atla"):  # her 50 işlemde özet
            print(f"OZET islenen={sayac} {dict(ozet)}", flush=True)


if __name__ == "__main__":
    main()
