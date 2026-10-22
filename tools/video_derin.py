"""VIDEO-YENIDEN-1: yerel derin tarama, Claude jetonu 0.
yt-dlp -> ffmpeg (0,5 sn kare) -> faster-whisper (kelime zamanli) -> RapidOCR -> Gemini kare aciklamasi -> JSON.
Kullanim: python tools/video_derin.py <url|kod> [...]   |  --liste <dosya> [--en N]
Cikti: docs/video-tarama/derin/<kod>.json ; ilerleme: .kos/kopru/derin-ilerleme.txt (kaldigi yerden)."""
import base64, json, os, re, shutil, site, subprocess, sys, tempfile, threading, time, urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil

KOK = Path(__file__).resolve().parents[1]
CIKTI = Path(os.environ["VD_CIKTI"]) if os.environ.get("VD_CIKTI") else KOK / "docs/video-tarama/derin"  # VD_CIKTI: profil/WER koşuları gerçek çıktıya yazmaz
ILERLEME = KOK / ".kos/kopru/derin-ilerleme.txt"
PROFIL = KOK / ".kos/kopru/derin-profil.tsv"  # video başı adım süreleri (sn)
ATLA_DOSYA = KOK / ".kos/kopru/video-atla.txt"  # kalıcı atlama listesi: yeniden deneme yok
NW = 0x08000000
# cuBLAS/cuDNN pip wheel'leri (nvidia-*-cu12) DLL'lerini nvidia/*/bin altına koyar. ctranslate2 LoadLibrary'yi
# arama bayraksız çağırdığı için add_dll_directory yetmez: yalnız bu süreçin PATH'ine eklenir (sistem PATH'i değişmez).
for sp in site.getsitepackages():
    for bin_dir in Path(sp, "nvidia").glob("*/bin"):
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(bin_dir))
        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]
# onnxruntime-gpu 1.31 CUDA provider'ı cublasLt64_13.dll ister; bulamazsa sessizce CPU'ya düşer (OCR ~26x yavaş).
# DLL torch (CUDA 13) wheel'inde bulunur: yalnız bu süreçin PATH'ine eklenir. Kalıcı PATH önerisi: rapor/cuda-kur-3-devam2.md
CUDA13_ADAYLAR = [os.environ.get("VD_CUDA13_DIR", ""), r"C:\AI\ComfyUI\.venv\Lib\site-packages\torch\lib"]
for ad in CUDA13_ADAYLAR:
    if ad and Path(ad, "cublasLt64_13.dll").exists():
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(ad)
        os.environ["PATH"] = ad + os.pathsep + os.environ["PATH"]
        break
URL_RE = re.compile(r"(?:https?://|www\.)[^\s\"'<>]+|\b[\w.-]+\.(?:com|io|ai|dev|app|org|net|co|xyz)(?:/[^\s]*)?\b|\b[\w-]+/[\w.-]+\b(?=.*github)", re.I)
KOMUT_RE = re.compile(r"^(?:\$\s*)?(?:npm|npx|pnpm|pip|pipx|uv|git|brew|winget|docker|curl|claude|python|node)\s+.+", re.I | re.M)
_ocr = None


def kos(*a, timeout=600):
    return subprocess.run(list(map(str, a)), capture_output=True, text=True, timeout=timeout, creationflags=NW)


def kod_of(u):
    m = re.search(r"(?:reel|p|tv|shorts)/([\w-]+)|[?&]v=([\w-]+)|youtu\.be/([\w-]+)", u)
    return next((g for g in m.groups() if g), re.sub(r"\W+", "_", u)[-24:]) if m else re.sub(r"\W+", "_", u)[-24:]


def indir(url, d):
    r = kos("yt-dlp", "-f", "wv[height>=360]+wa/w[height>=360]/best", "--no-playlist", "-o", d / "v.%(ext)s", url, "--write-info-json", timeout=300)
    v = next((p for p in d.glob("v.*") if p.suffix not in (".json",)), None)
    return v, r.stderr[-200:]


def kareler(v, d, tavan=240):
    k = d / "k"
    k.mkdir(exist_ok=True)
    # sahne değişimi: fps=2'ye göre OCR kare sayısı ~10× düşer; hiç sahne değişimi yoksa (tek kare) sabit 1 kare/sn
    kos("ffmpeg", "-y", "-i", v, "-vf", "select=eq(n\\,0)+gt(scene\\,0.3),scale=640:-1", "-fps_mode", "vfr", "-q:v", "4", k / "%04d.jpg")
    if len(list(k.glob("*.jpg"))) < 2:
        shutil.rmtree(k)
        k.mkdir()
        kos("ffmpeg", "-y", "-i", v, "-vf", "fps=1,scale=640:-1", "-q:v", "4", k / "%04d.jpg")
    ks = sorted(k.glob("*.jpg"))
    if len(ks) > tavan:  # tavani asarsa esit aralikla ornekle
        adim = len(ks) / tavan
        ks = [ks[int(i * adim)] for i in range(tavan)]
    return ks


WHISPER = {"cuda": ("large-v3", "float16"), "cpu": ("small", "int8")}
_whisper = {}
ASR_KILIT = threading.Lock()  # tek GPU: döküm sırayla; kare/OCR işçileri bu sırada paralel sürer
KILIT = threading.Lock()  # ilerleme dosyası ve konsol satırları


GROQ_ASR = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_DIL = {"turkish": "tr", "english": "en", "german": "de", "spanish": "es", "french": "fr", "russian": "ru", "arabic": "ar",
            "italian": "it", "portuguese": "pt", "hindi": "hi", "japanese": "ja", "korean": "ko", "chinese": "zh"}
GROQ_KILIT = threading.Lock()
groq_durum = {"sonraki": 0.0, "kapali": 0.0}  # ücretsiz kota: 20 istek/dk; 429'da 90 sn kapanır, GPU'ya döner


def groq_asr(wav):
    """GPU döküm kuyruğu doluyken taşan videoyu Groq whisper-large-v3'ya (ücretsiz) gönderir; başarısızsa None."""
    key = os.environ.get("GROQ_API_KEY")
    if not key or wav.stat().st_size > 15_000_000:
        return None
    with GROQ_KILIT:
        if time.time() < groq_durum["kapali"]:
            return None
        bekle = groq_durum["sonraki"] - time.time()
        groq_durum["sonraki"] = max(time.time(), groq_durum["sonraki"]) + 3.2
    if bekle > 0:
        time.sleep(bekle)
    sinir = "vd" + str(time.time_ns())
    alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
    govde = (alan("model", "whisper-large-v3") + alan("response_format", "verbose_json") + alan("temperature", "0")
             + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
             + wav.read_bytes() + f"\r\n--{sinir}--\r\n".encode())
    try:  # Python-urllib UA'sı Cloudflare'da 1010/403 alır: açık UA şart
        req = urllib.request.Request(GROQ_ASR, govde, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
        r = json.load(urllib.request.urlopen(req, timeout=60))
        out = [{"b": round(s["start"], 1), "s": round(s["end"], 1), "t": s["text"].strip()} for s in r.get("segments", []) if s["text"].strip()]
        return GROQ_DIL.get(str(r.get("language", "")).lower(), str(r.get("language", ""))), out
    except Exception as e:
        if "429" in str(e):
            groq_durum["kapali"] = time.time() + 90
        print(f"device=groq basarisiz: {str(e)[:100]}", flush=True)
        return None


def asr(v, d):
    from faster_whisper import WhisperModel
    kos("ffmpeg", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", d / "a.wav")
    if not (d / "a.wav").exists():
        return "", []
    if ASR_KILIT.locked() and (g := groq_asr(d / "a.wav")):  # GPU kuyruğu dolu: taşan video ücretsiz Groq kanalına
        print("device=groq model=whisper-large-v3", flush=True)
        return g
    for aygit, (model, tip) in WHISPER.items():  # GPU başarısızsa CPU'ya düşer, hat durmaz
        try:
            with ASR_KILIT:
                if aygit not in _whisper:
                    _whisper[aygit] = WhisperModel(model, device=aygit, compute_type=tip)
                seg, info = _whisper[aygit].transcribe(str(d / "a.wav"), word_timestamps=True, vad_filter=True)  # toplu yol WER %1,8–4,2: kullanılmaz
                out = [{"b": round(s.start, 1), "s": round(s.end, 1), "t": s.text.strip()} for s in seg]  # üretici tüketilmeden hata yakalanmaz
            print(f"device={aygit} model={model}", flush=True)
            return info.language, out
        except Exception as e:
            _whisper.pop(aygit, None)
            print(f"device={aygit} basarisiz: {str(e)[:150]}", flush=True)
    return "", []


OCR_KILIT = threading.Lock()  # tek ORT oturumu: GPU çağrıları sıralanır (kare başı ~0,2 sn)
OCR_AYGIT = "?"


def ocr_motor():
    global _ocr, OCR_AYGIT
    from rapidocr_onnxruntime import RapidOCR
    if _ocr is None:
        try:  # CUDA sağlayıcı yüklenemezse (DLL yok) ORT sessizce CPU'ya düşer: sağlayıcı listesinden doğrula
            m = RapidOCR(det_use_cuda=True, cls_use_cuda=True, rec_use_cuda=True)
            prov = getattr(getattr(getattr(m, "text_det", None), "infer", None), "session", None)
            OCR_AYGIT = "cuda" if prov is None or "CUDAExecutionProvider" in prov.get_providers() else "cpu"
            _ocr = m if OCR_AYGIT == "cuda" else RapidOCR()
        except Exception:
            _ocr, OCR_AYGIT = RapidOCR(), "cpu"
        print(f"ocr aygit={OCR_AYGIT}", flush=True)
    return _ocr


def ocr(ks):
    gorulen, out = set(), []
    for i, k in enumerate(ks):
        try:
            with OCR_KILIT:
                res, _ = ocr_motor()(str(k))
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
    istek = {"model": model, "stream": False, "think": False, "options": {"num_ctx": 8192}, "keep_alive": "2m",
             "messages": [{"role": "user", "content": KARE_PROMPT, "images": [base64.b64encode(k.read_bytes()).decode() for k in sec]}]}
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/chat", json.dumps(istek).encode(), {"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=300))["message"]["content"]
    except Exception:
        return None


gemini_durum = {"kapali": 0.0}


def gemini_aciklama(ks, n=4):
    key = os.environ.get("GEMINI_API_KEY")
    if not key or not ks or time.time() < gemini_durum["kapali"]:
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
        except Exception as e:
            if "429" in str(e):  # günlük kota bitti (video başı 3 boş istek ~2 sn): 30 dk yerel modele geç
                gemini_durum["kapali"] = time.time() + 1800
                return None
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
    t0 = time.time()
    adim = {}
    try:
        v, hata = indir(url, d)
        if not v:
            if "No video formats found" in hata:  # kalıcı: format yok, yeniden deneme anlamsız
                with ATLA_DOSYA.open("a", encoding="utf-8") as f:
                    f.write(kod + "\n")
                return kod, "atla"
            return kod, "indirilemedi: " + hata.strip().splitlines()[-1][:120] if hata.strip() else "indirilemedi"
        t1 = time.time(); adim["indir"] = t1 - t0
        dil, seg = asr(v, d)
        t2 = time.time(); adim["asr"] = t2 - t1
        ks = kareler(v, d)
        t3 = time.time(); adim["kare"] = t3 - t2
        def acik_zamanli():  # ölçüm: açıklama süresi ayrı tutulur (ADIM satırı)
            s = time.time(); r = gemini_aciklama(ks) or yerel_aciklama(ks); adim["acik_s"] = time.time() - s; return r
        with ThreadPoolExecutor(1) as px:  # kare açıklaması (Gemini/Ollama) OCR ile örtüşür; profilde "ocr" ikisini birden kapsar
            acik_f = px.submit(acik_zamanli)
            ekran = ocr(ks)
            adim["ocr_s"] = time.time() - t3
            acik = acik_f.result()
        t4 = time.time(); adim["ocr"] = t4 - t3
        metin = "\n".join(e["t"] for e in ekran) + "\n" + " ".join(s["t"] for s in seg)
        linkler = sorted({m.strip(".,)") for m in URL_RE.findall(metin)})
        komutlar = sorted({m.strip() for m in KOMUT_RE.findall(metin)})
        info = {}
        ij = next(d.glob("*.info.json"), None)
        if ij:
            j = json.loads(ij.read_text(encoding="utf-8"))
            info = {"baslik": j.get("title"), "sure": j.get("duration"), "yukleyen": j.get("uploader"), "aciklama": (j.get("description") or "")[:800]}
        veri = {"kod": kod, "url": url, "dil": dil, "meta": info, "transkript": seg, "ekran": ekran,
                "linkler": linkler, "komutlar": komutlar, "kare_aciklama": acik, "kare_sayisi": len(ks)}
        adim["acik"] = time.time() - t4
        with KILIT, PROFIL.open("a", encoding="utf-8") as f:
            f.write(f"{kod}\t" + "\t".join(f"{adim[x]:.1f}" for x in ("indir", "asr", "kare", "ocr", "acik")) + f"\t{len(ks)}\t{OCR_AYGIT}\n")
        CIKTI.mkdir(parents=True, exist_ok=True)
        hedef.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        print("ADIM " + kod + " " + json.dumps({k: round(v, 1) for k, v in adim.items()}), flush=True)  # ölçüm
        return kod, f"ok seg={len(seg)} ocr={len(ekran)} link={len(linkler)} komut={len(komutlar)}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


RAM_ESIK = 85  # yüzde: üstündeyken yeni video başlamaz (sınır Ömer'in RAM kuralı)


def ram_bekle():
    while psutil.virtual_memory().percent >= RAM_ESIK:
        time.sleep(30)


def calis(u):
    ram_bekle()
    t = time.time()
    try:
        kod, durum = isle(u)
    except Exception as e:  # tek video hatası toplu işi durdurmaz
        kod, durum = kod_of(u), f"hata: {str(e)[:120]}"
    satir = f"{kod}\t{durum}\t{time.time() - t:.0f}s"
    with KILIT:
        print(satir, flush=True)
        with ILERLEME.open("a", encoding="utf-8") as f:
            f.write(satir + "\n")
    return durum


def main():
    a = sys.argv[1:]
    en, es = 10**9, 3
    if "--en" in a:
        i = a.index("--en"); en = int(a[i + 1]); del a[i:i + 2]
    if "--es" in a:  # eşzamanlı video işçisi; GPU döküm sırası ASR_KILIT ile tek kalır
        i = a.index("--es"); es = int(a[i + 1]); del a[i:i + 2]
    if a and a[0] == "--liste":
        urls = re.findall(r"https?://\S+", Path(a[1]).read_text(encoding="utf-8"))
        urls = [u.split("\t")[0] for u in dict.fromkeys(urls)]
    else:
        urls = a
    # yapılmış ve atlanacaklar baştan elenir: --en yalnız yeni işleri sayar
    urls = [u for u in urls if not (CIKTI / f"{kod_of(u)}.json").exists() and kod_of(u) not in atla_kodlari()][:en]
    ozet, sayac = Counter(), 0
    with ThreadPoolExecutor(es) as ex:
        for durum in ex.map(calis, urls):
            ozet[durum.split(":")[0]] += 1
            sayac += 1
            if sayac % 50 == 0:  # her 50 işlemde özet
                print(f"OZET islenen={sayac} {dict(ozet)}", flush=True)
    print(f"BITIS islenen={sayac} {dict(ozet)}", flush=True)  # gözetmen (toplu_gozetmen.py) temiz bitişi bundan anlar


if __name__ == "__main__":
    main()
