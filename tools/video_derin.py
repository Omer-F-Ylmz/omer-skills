"""VIDEO-YENIDEN-1: yerel derin tarama, Claude jetonu 0.
yt-dlp -> ffmpeg (0,5 sn kare) -> faster-whisper (kelime zamanli) -> RapidOCR -> Gemini kare aciklamasi -> JSON.
Kullanim: python tools/video_derin.py <url|kod> [...]   |  --liste <dosya> [--en N]
Cikti: docs/video-tarama/derin/<kod>.json ; ilerleme: .kos/kopru/derin-ilerleme.txt (kaldigi yerden)."""
import base64, contextlib, json, os, queue, re, shutil, site, subprocess, sys, tempfile, threading, time, urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vram_bekci  # VRAM-BEKCI: GPU işi başlatma kapısı
import ekran_duzelt

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
KOMUT_RE = re.compile(r"^(?:\$\s*)?(?:npm|npx|pnpm|pip|pipx|uv|git|brew|winget|docker|curl|python|node|claude(?=\s+(?:-|mcp|plugin|code|doctor|update|config|install|agents|login|\/)))\s+.+", re.I | re.M)
_ocr = None


def kos(*a, timeout=600):
    return subprocess.run(list(map(str, a)), capture_output=True, text=True, timeout=timeout, creationflags=NW)


ZAMAN = KOK / ".kos/kopru/derin-zaman.tsv"  # VIDEO-HIZ-4: aşama başı zaman günlüğü (kod, aşama, başlangıç epoch, süre sn, iş parçacığı)
ZAMAN_KILIT = threading.Lock()
ASAMA_AKTIF = {}  # takılma teşhisi: iş parçacığı → (kod, aşama, başlangıç); ASAMA_TAKILI bunu tarar


class zam:
    def __init__(self, kod, asama):
        self.kod, self.asama = kod, asama

    def __enter__(self):
        self.t = time.time()
        ASAMA_AKTIF[threading.get_ident()] = (self.kod, self.asama, self.t)
        return self

    def __exit__(self, *e):
        ASAMA_AKTIF.pop(threading.get_ident(), None)
        with ZAMAN_KILIT, ZAMAN.open("a", encoding="utf-8") as f:
            f.write(f"{self.kod}\t{self.asama}\t{self.t:.1f}\t{time.time() - self.t:.2f}\t{threading.get_ident()}\n")


def gpu_olc():
    """(kullanım %, VRAM %, VRAM GB boş) — 0,5 sn önbellekli tek nvidia-smi çağrısı."""
    if time.time() - gpu_olc.t < 0.5:
        return gpu_olc.v
    try:
        u, k, t = (float(x) for x in kos("nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits", timeout=10).stdout.strip().splitlines()[0].split(","))
        gpu_olc.v = (u, 100 * k / t, (t - k) / 1024)
    except Exception:
        pass
    gpu_olc.t = time.time()
    return gpu_olc.v


gpu_olc.t, gpu_olc.v = 0.0, (0.0, 0.0, 99.0)
GPU_KILIT = threading.Lock()  # ASR toplu adımı ve OCR kareleri TEK GPU sırası: aynı anda tek çekirdek akışı
GPU_ORAN = float(os.environ.get("VD_GPU_ORAN", "0.33"))  # bekçiler (gpu_sinir ≥%78) hiç devreye girmesin: her GPU patlamasından sonra patlama×ORAN boşta kal (~%75 görev oranı)
DL_SEM = threading.BoundedSemaphore(int(os.environ.get("VD_DL", "8")))
CPU_SEM = threading.BoundedSemaphore(int(os.environ.get("VD_CPU", "4")))  # ffmpeg kare/ses çıkarma
GPU_TAVAN = float(os.environ.get("VD_GPU_TAVAN", "70"))  # ölçülen kullanım bunu aşarsa ek bekleme
GPU_BASLAT = float(os.environ.get("VD_GPU_BASLAT", "101"))  # <100 ise yeni GPU patlaması ölçülen kullanım ≤ bu olana dek (en çok 3 sn) bekler


def bosta_mi():
    """HIZ-8 (a): Ömer'in klavye/fare girdisi VD_BOSTA_DK dakikadır yok → GPU tavanı yok (kural 1 Kas). VD_BOSTA_DK=0 kapatır. 30 sn önbellek."""
    if bosta_mi.t + 30 > time.time():
        return bosta_mi.v
    dk = float(os.environ.get("VD_BOSTA_DK", "10"))
    try:
        import ctypes

        class LII(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

        li = LII(ctypes.sizeof(LII), 0)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li))
        bosta_mi.v = dk > 0 and (ctypes.windll.kernel32.GetTickCount() - li.dwTime) / 60000 >= dk
    except Exception:
        bosta_mi.v = False
    bosta_mi.t = time.time()
    return bosta_mi.v


bosta_mi.t, bosta_mi.v = 0.0, False


def gpu_nefes(patlama):
    """GPU_KILIT tutulurken çağrılır: kilidi bırakmadan uyur, böylece boşluğu başka işçi doldurmaz."""
    if bosta_mi():
        return
    u = gpu_olc()[0]
    time.sleep(patlama * GPU_ORAN + (0.25 if u >= GPU_TAVAN else 0))
    son = time.time() + 3  # VIDEO-HIZ-5 TUR 2: sert zamanlayıcı — ölçülen kullanım BASLAT'ın altına inene dek sonraki patlama başlamaz (nvidia-smi geri beslemeli)
    while GPU_BASLAT < 100 and gpu_olc()[0] > GPU_BASLAT and time.time() < son:
        time.sleep(0.2)


RAM_TAVAN = float(os.environ.get("VD_RAM_TAVAN", "96.5"))  # TUR 2: tavan %89, taban Ömer'in süreçleriyle ~%87,5 → her ağır aşama başlamadan RAM'e bakar


def ram_kapi(max_bekle=240):
    """Ağır aşama (indirme/ffmpeg/model) başlamadan RAM < RAM_TAVAN olana dek bekler; zaman aşımında devam eder (kilitlenme yok)."""
    son = time.time() + max_bekle
    while psutil.virtual_memory().percent >= RAM_TAVAN and time.time() < son:
        time.sleep(1)


RAM_KES, VRAM_KES, ES_MAX = 97.0, 95.0, 7  # KARAR-30 m8: sert kesme eşikleri, işçi üst sınırı; Ömer 02.11: VRAM kapısı %95; Ömer 03.11: RAM kesme %97
KESIK = threading.Event()


def kesme_gerekli(ram, vram):
    return ram >= RAM_KES or vram >= VRAM_KES


def es_sinirla(n):
    return max(1, min(n, ES_MAX))


def kesme_izle(dur):
    """İki ardışık örnekte (2 sn arayla) eşik aşılırsa KESIK'i kurar: kuyruktaki videolar başlamaz, çalışanlar biter."""
    ard = 0
    while not dur.wait(2):
        ard = ard + 1 if kesme_gerekli(psutil.virtual_memory().percent, gpu_olc()[1]) else 0
        if ard >= 2 and not KESIK.is_set():
            KESIK.set()
            print(f"KESILDI ram={psutil.virtual_memory().percent:.1f} vram={gpu_olc()[1]:.1f}", flush=True)


def kod_of(u):
    m = re.search(r"(?:reel|p|tv|shorts)/([\w-]+)|[?&]v=([\w-]+)|youtu\.be/([\w-]+)", u)
    return next((g for g in m.groups() if g), re.sub(r"\W+", "_", u)[-24:]) if m else re.sub(r"\W+", "_", u)[-24:]


def cerez_arg(url):  # yalnız instagram.com; yol IG_COOKIES ya da .kos/ig-cookies.txt (gitignore'da), değer asla yazılmaz
    if "instagram.com" not in url:
        return []
    p = Path(os.environ.get("IG_COOKIES") or Path(__file__).resolve().parent.parent / ".kos" / "ig-cookies.txt")
    return ["--cookies", p] if p.is_file() else []


INDIR_SEM = threading.BoundedSemaphore(int(os.environ.get("VD_INDIR_ES", "2")))  # 3 Kas: 6 eş indirmede YouTube bot-kontrolü (cookies) 48 düşüş verdi; işçi 6 kalır, indirme 2'li


def indir(url, d):
    with INDIR_SEM:
        v, e = _indir1(url, d)
        if v is None and "cookies" in e:
            time.sleep(45)
            v, e = _indir1(url, d)
    return v, e


def _indir1(url, d):
    r = kos("yt-dlp", *cerez_arg(url), "-f", "wv[height>=360][protocol^=http]+(ba[format_note*=original]/ba)/w[height>=360]/best", "-S", "lang", "--no-playlist", "-N", "4", "-o", d / "v.%(ext)s", url, "--write-info-json", timeout=300)
    v = next((p for p in d.glob("v.*") if p.suffix not in (".json",) and not re.match(r"v\.f\d", p.name)), None)  # birleştirme düştüyse v.f229.mp4 gibi yalnız-video parçası seçilmez (ASR "yok" kök nedeni)
    return v, r.stderr[-200:]


TEKIL_ESIK = int(os.environ.get("VD_TEKIL", "2"))  # dHash Hamming uzaklığı ≤ eşik → aynı kare (OCR yinelenmez); 0 = kapalı


def tekil(ks):
    """VIDEO-HIZ-4: OCR'yi kes — neredeyse aynı kareleri (dHash) ve düz/boş kareleri (gri std < 6) at; en az 1 kare kalır."""
    if TEKIL_ESIK <= 0 or len(ks) < 2:
        return ks
    import numpy as np
    from PIL import Image
    kalan, hashler = [], []
    for k in ks:
        try:
            g = np.asarray(Image.open(k).convert("L").resize((9, 8)), dtype=np.int16)
            std = float(np.asarray(Image.open(k).convert("L").resize((64, 36)), dtype=np.float32).std())
        except Exception:
            kalan.append(k); continue
        h = (g[:, 1:] > g[:, :-1]).ravel()
        if std < 6 or any(int((h != x).sum()) <= TEKIL_ESIK for x in hashler):
            continue
        hashler.append(h); kalan.append(k)
    return kalan or ks[:1]


SAHNE_ESIK = os.environ.get("VD_SAHNE", "0.3")  # VIDEO-HIZ-5: ffmpeg sahne değişimi eşiği (yükselince OCR karesi azalır)


def kareler(v, d, tavan=240):
    k = d / "k"
    k.mkdir(exist_ok=True)
    # sahne değişimi: fps=2'ye göre OCR kare sayısı ~10× düşer; hiç sahne değişimi yoksa (tek kare) sabit 1 kare/sn
    kos("ffmpeg", "-y", "-i", v, "-vf", f"select=eq(n\\,0)+gt(scene\\,{SAHNE_ESIK}),scale=640:-1", "-fps_mode", "vfr", "-q:v", "4", k / "%04d.jpg")
    if len(list(k.glob("*.jpg"))) < 2:
        shutil.rmtree(k)
        k.mkdir()
        kos("ffmpeg", "-y", "-i", v, "-vf", "fps=1,scale=640:-1", "-q:v", "4", k / "%04d.jpg")
    ks = tekil(sorted(k.glob("*.jpg")))
    if len(ks) > tavan:  # tavani asarsa esit aralikla ornekle
        adim = len(ks) / tavan
        ks = [ks[int(i * adim)] for i in range(tavan)]
    return ks


WHISPER = {"cuda": ("large-v3", "float16"), "cpu": ("small", "int8")}
_whisper = {}
ASR_BATCH = int(os.environ.get("VD_ASR_BATCH", "2"))  # DERIN-HIZ-3: batched fp16 + VAD ayarı 0,972 / ~34 sn; 0 segmentte sıralı yola düşer (7XhX8P0ebEU). VRAM-BEKCI: 9,6 GB tavanına göre 8→4 (batch başına GB ölçülmedi)
TOPLU_MIN = int(os.environ.get("VD_TOPLU_MIN", "120"))  # sn
ASR_VAD = {"min_silence_duration_ms": 500, "speech_pad_ms": 400}
ASR_BEAM = int(os.environ.get("VD_ASR_BEAM", "5"))  # DERIN-HIZ-2: turbo+beam1 kapıyı geçmedi (0,886); yerel yedek large-v3 beam5
ASR_AYGIT = os.environ.get("VD_ASR_AYGIT", "otomatik")  # VIDEO-HIZ-5: otomatik (GPU, düşerse CPU small) | cpu (large-v3 int8, GPU boş kalır) | cuda
ASR_CPU_IPLIK = int(os.environ.get("VD_ASR_IPLIK", "12"))
ASR_KILIT = threading.Lock()  # tek GPU: döküm sırayla; kare/OCR işçileri bu sırada paralel sürer
KILIT = threading.Lock()  # ilerleme dosyası ve konsol satırları


GROQ_ASR = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_DIL = {"turkish": "tr", "english": "en", "german": "de", "spanish": "es", "french": "fr", "russian": "ru", "arabic": "ar",
            "italian": "it", "portuguese": "pt", "hindi": "hi", "japanese": "ja", "korean": "ko", "chinese": "zh"}
GROQ_KILIT = threading.Lock()
groq_durum = {}  # model → {sonraki, kapali, kayit}; ücretsiz kota: 20 istek/dk; 429'da model 600 sn kapanır, sıradaki modele/GPU'ya düşer
GROQ_MODELLER = [m for m in os.environ.get("VD_GROQ_MODELLER", "whisper-large-v3").split(",") if m]
GROQ_SAAT_SN = float(os.environ.get("VD_GROQ_SAAT", "100000"))  # model başına saatlik ses saniyesi (kota 7200)


GROQ_PARCA_SN = float(os.environ.get("VD_GROQ_PARCA", "300"))  # VIDEO-HIZ-6: 15 MB üstü ses VAD sessizliğinden bu uzunlukta parçalanır (300 sn wav ≈ 9,6 MB < Groq 25 MB sınırı)
GROQ_ES = int(os.environ.get("VD_GROQ_ES", "3"))  # VIDEO-HIZ-6: bir videonun parçaları için eşzamanlı istek; 20 istek/dk tavanını GROQ_KILIT aralığı (3,2 sn) korur
GROQ_OPUS_KBPS = os.environ.get("VD_GROQ_OPUS", "24")  # VIDEO-HIZ-7: opus bit hızı (24 kbps ≈ 3 KB/sn → 24 MB ≈ 133 dk)
GROQ_MAX = int(float(os.environ.get("VD_GROQ_MAX_MB", "24")) * 1_000_000)  # Groq ücretsiz katman dosya sınırı 25 MB
GROQ_ORTUSME = 3  # sn, parçalı yolda parça sınırı örtüşmesi
VAD_KILIT = threading.Lock()


def groq_opus(wav):
    """VIDEO-HIZ-7: 16 kHz mono wav → ogg/opus (aynı dizinde a.ogg); ffmpeg yoksa/başarısızsa None."""
    o = wav.with_suffix(".ogg")
    r = kos("ffmpeg", "-y", "-i", wav, "-c:a", "libopus", "-b:a", GROQ_OPUS_KBPS + "k", "-application", "voip", o)
    return o if r.returncode == 0 and o.exists() and o.stat().st_size else None


def groq_kes(wav, sr=16000):
    """VIDEO-HIZ-6: wav'ı konuşma sessizliklerinin ortasından ≤GROQ_PARCA_SN'lik [(başlangıç, bitiş)] örnek aralıklarına böler; konuşma yoksa None."""
    import numpy as np
    from faster_whisper.audio import decode_audio
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    a = decode_audio(str(wav), sampling_rate=sr)
    with VAD_KILIT:
        ts = get_speech_timestamps(a, VadOptions())
    if not ts:
        return None, None
    tavan, parca, bas, son = int(GROQ_PARCA_SN * sr), [], 0, 0
    for s in ts:
        if son > bas and s["end"] - bas > tavan:  # bu konuşma parçayı aşar: önceki konuşma ile bunun arasındaki sessizlikte kes
            kes = (son + s["start"]) // 2
            parca.append((bas, kes))
            bas = kes
        son = s["end"]
    parca.append((bas, len(a)))
    out = []
    for b, e in parca:  # tek kesintisiz konuşma tavanı aşarsa (Groq dosya sınırı) eşit böl
        k = -(-(e - b) // (2 * tavan))
        out += [(b + i * (e - b) // k, b + (i + 1) * (e - b) // k) for i in range(k)]
    return a, out


def _groq_gonder(key, wav_bytes, sure, dil=None, ad="a.wav", tur="audio/wav"):
    """Tek istek: model/bütçe seçimi + 3,2 sn aralık + kısa 429 geri çekilmesi; (dil, segmentler) ya da None."""
    for deneme in range(3):
        with GROQ_KILIT:  # VIDEO-HIZ-5: model başına saatlik ses saniyesi bütçesi (ücretsiz kota 7200 sn/sa/model); dolunca sıradaki model, hiçbiri yoksa yerel GPU
            simdi = time.time()
            model = next((m for m in GROQ_MODELLER if simdi >= groq_durum.setdefault(m, {"sonraki": 0.0, "kapali": 0.0, "kayit": []})["kapali"]
                          and sum(s for t, s in groq_durum[m]["kayit"] if simdi - t < 3600) + sure <= GROQ_SAAT_SN), None)
            if not model:
                return None
            gd = groq_durum[model]
            gd["kayit"] = [(t, s) for t, s in gd["kayit"] if simdi - t < 3600] + [(simdi, sure)]
            bekle = gd["sonraki"] - simdi
            gd["sonraki"] = max(simdi, gd["sonraki"]) + 3.2
        if bekle > 0:
            time.sleep(bekle)
        sinir = "vd" + str(time.time_ns())
        alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
        govde = (alan("model", model) + alan("response_format", "verbose_json") + alan("temperature", "0") + (alan("language", dil) if dil else b"")
                 + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="{ad}"\r\nContent-Type: {tur}\r\n\r\n'.encode()
                 + wav_bytes + f"\r\n--{sinir}--\r\n".encode())
        try:  # Python-urllib UA'sı Cloudflare'da 1010/403 alır: açık UA şart
            req = urllib.request.Request(GROQ_ASR, govde, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
            r = json.load(urllib.request.urlopen(req, timeout=90))
            out = [{"b": round(s["start"], 1), "s": round(s["end"], 1), "t": s["text"].strip()} for s in r.get("segments", []) if s["text"].strip()]
            return GROQ_DIL.get(str(r.get("language", "")).lower(), str(r.get("language", ""))), out
        except Exception as e:
            if "429" in str(e):
                ra = float(getattr(e, "headers", None) and e.headers.get("retry-after") or 600)
                if ra <= 30 and deneme < 2:  # VIDEO-HIZ-6: dakikalık istek tavanı → kısa bekle, aynı parçayı yeniden dene; saatlik/günlük kota (uzun retry-after) → model kapanır
                    time.sleep(ra + 1)
                    continue
                groq_durum[model]["kapali"] = time.time() + max(60.0, min(ra, 3600.0))
            print(f"device=groq basarisiz: {str(e)[:100]}", flush=True)
            return None
    return None


def groq_asr(wav):
    """Önce ücretsiz Groq whisper-large-v3 (yerelle aynı model); kota/hata durumunda None, yerel large-v3 beam5 devralır.
    VIDEO-HIZ-6: 15 MB üstü (~7,8 dk) ses VAD sessizliğinden ≤GROQ_PARCA_SN parçalara bölünür, zaman damgaları birleştirilir."""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return None
    boy = wav.stat().st_size
    if boy <= 15_000_000:
        return _groq_gonder(key, wav.read_bytes(), boy / 32000)  # 16 kHz mono 16 bit
    o = groq_opus(wav)  # VIDEO-HIZ-7: 15 MB sınırı ham wav içindi; Groq sınırı dosya başına 25 MB → opus ile uzun ses TEK istekte, parçalama yok
    if o and o.stat().st_size <= GROQ_MAX:
        return _groq_gonder(key, o.read_bytes(), boy / 32000, None, "a.ogg", "audio/ogg")
    if os.environ.get("VD_GROQ_UZUN", "0") != "1":  # opus bile 24 MB üstü: parçalı yol (HIZ-6'da kalite kapısını geçmedi) → varsayılan KAPALI, yerel GPU
        return None
    import io, wave
    a, aralik = groq_kes(wav)
    if not aralik:
        return None

    def parca(i, dil=None):
        b, e = aralik[i]
        s0 = max(0, b - GROQ_ORTUSME * 16000) if i else b  # HIZ-7: ilk parça dışında 3 sn önceden başlar, sınırda kelime kesilmez
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
            w.writeframes((a[s0:e] * 32767).astype("int16").tobytes())
        r = _groq_gonder(key, buf.getvalue(), (e - s0) / 16000, dil)
        if not r:
            return None
        sg = [{**s, "b": round(s["b"] + s0 / 16000, 1), "s": round(s["s"] + s0 / 16000, 1)} for s in r[1]]
        return r[0], [s for s in sg if b / 16000 <= (s["b"] + s["s"]) / 2 < e / 16000]  # örtüşmeyi ortası kendi parçasına düşen segmentle birleştir

    ilk = parca(0)  # dil ilk parçadan bulunur, kalanlara verilir (sessiz/müzikli parçada yanlış dil tahmini olmasın)
    if not ilk:
        return None
    kod = ilk[0] if ilk[0] in GROQ_DIL.values() else None
    with ThreadPoolExecutor(GROQ_ES) as ex:
        kalan = list(ex.map(lambda i: parca(i, kod), range(1, len(aralik))))
    if any(k is None for k in kalan):
        return None
    print(f"device=groq parca={len(aralik)}", flush=True)
    return ilk[0], ilk[1] + [s for k in kalan for s in k[1]]


ALT_MIN = int(os.environ.get("VD_ALT_MIN", "900"))


def altyazi_dene(d):  # DERIN-HIZ-3: YouTube'da videonun kendi dilinde altyazı varsa ve ayrıştırma sağlıklıysa ASR atlanır
    ij = next(d.glob("*.info.json"), None)
    if not ij or os.environ.get("VD_ALTYAZI", "1") != "1":
        return None
    j = json.loads(ij.read_text(encoding="utf-8"))
    if j.get("extractor_key") != "Youtube" or (j.get("duration") or 0) <= ALT_MIN:  # VIDEO-HIZ-4: kısa videoda ASR ucuz ve altyazı referansa 0,60–0,95 (kapı ≥0,96) → yalnız uzunda
        return None
    import altyazi
    r = altyazi.getir(j["id"], j.get("duration"), (j.get("language") or "").split("-")[0])
    if r:
        print(f"device=altyazi dil={r[0]}", flush=True)
    return r


def asr(v, d):
    from faster_whisper import BatchedInferencePipeline, WhisperModel
    if r := altyazi_dene(d):
        return *r, "altyazi"
    ram_kapi()
    kos("ffmpeg", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", d / "a.wav")
    if not (d / "a.wav").exists():
        return "", [], "yok"
    if os.environ.get("VD_GROQ", "1") == "1" and (g := groq_asr(d / "a.wav")):  # VIDEO-HIZ-5 TUR 3: varsayılan AÇIK (3×40 shorts 609–664/sa, kalite eşit); geri alma: VD_GROQ=0
        print("device=groq model=whisper-large-v3", flush=True)
        return *g, "groq"
    for aygit, (model, tip) in WHISPER.items():  # GPU başarısızsa CPU'ya düşer, hat durmaz
        if ASR_AYGIT != "otomatik" and aygit != ASR_AYGIT:  # VIDEO-HIZ-5: "cpu" → GPU'ya hiç dokunmaz (large-v3 int8)
            continue
        try:
            if aygit == "cuda":  # VRAM-BEKCI: VRAM ≥%80 iken GPU işi bekler; öncelik BELOW_NORMAL
                vram_bekci.vram_bekle()
                vram_bekci.dusuk_oncelik()
            with ASR_KILIT:  # tek kalıcı ASR işçisi: model süreç başına BİR kez yüklenir
                if aygit not in _whisper:
                    if aygit == "cuda":  # VRAM ≤%70: bekçi (vram_siper %78'de kapatır) hiç tetiklenmesin
                        son = time.time() + 600
                        while gpu_olc()[1] > 55 and time.time() < son:  # model + toplu bellek ~%15 ekler
                            time.sleep(5)
                    tip_ = os.environ.get("VD_ASR_TIP") or tip
                    m = WhisperModel(os.environ.get("VD_ASR_MODEL") or ("large-v3" if aygit == "cuda" or ASR_AYGIT == "cpu" else model), device=aygit, compute_type=tip_ if aygit == "cuda" else tip, **({"cpu_threads": ASR_CPU_IPLIK} if aygit == "cpu" else {}))
                    _whisper[aygit + "_seq"] = m
                    _whisper[aygit] = BatchedInferencePipeline(m) if aygit == "cuda" and ASR_BATCH > 1 else m  # VRAM tavanı batch_size ile
                toplu = aygit == "cuda" and ASR_BATCH > 1 and (d / "a.wav").stat().st_size > TOPLU_MIN * 32000  # VIDEO-HIZ-4: kısa sesde batched 0,85–0,97 (sıralı 1,00 = referansla aynı yol); batched yalnız uzunda
                kw = {"batch_size": ASR_BATCH, "vad_parameters": ASR_VAD, "without_timestamps": False} if toplu else {}
                kw["beam_size"] = ASR_BEAM

                def dok(m_, **k_):  # üretici tüketilirken her GPU patlaması arasında nefes (kilit tutulur)
                    sg, inf = m_.transcribe(str(d / "a.wav"), word_timestamps=True, vad_filter=True, **k_)
                    o, it = [], iter(sg)
                    while True:
                        t0 = time.time()
                        with GPU_KILIT if aygit == "cuda" else contextlib.nullcontext():  # CPU ASR GPU sırasını tutmaz (OCR beklemez)
                            s = next(it, None)
                            if s is not None and aygit == "cuda":
                                gpu_nefes(time.time() - t0)
                        if s is None:
                            return inf, o
                        o.append({"b": round(s.start, 1), "s": round(s.end, 1), "t": s.text.strip()})
                with zam(d.name, "asr_gpu"):
                    info, out = dok(_whisper[aygit], **kw)
                seq_dustu = False
                if toplu and not out:  # toplu yol sessizce 0 kelime verdi: sıralı yol kesin sonuç
                    info, out = dok(_whisper[aygit + "_seq"], beam_size=ASR_BEAM); seq_dustu = True
            print(f"device={aygit} model={model}", flush=True)
            return info.language, out, "asr-batched" if toplu and out and not seq_dustu else "asr-sirali"
        except Exception as e:
            _whisper.pop(aygit, None)
            print(f"device={aygit} basarisiz: {str(e)[:150]}", flush=True)
    return "", [], "yok"


OCR_AYGIT = "?"
OCR_OTURUM = int(os.environ.get("VD_OCR_OTURUM", "3"))  # HIZ-8 (c): eşzamanlı RapidOCR oturumu (kare başı sn: 1→0,257 · 2→0,120 · 3→0,087 · 6→0,084); GPU/CPU-on-işleme çakışır
OCR_ATLA = int(os.environ.get("VD_OCR_ATLA", "1"))  # HIZ-8 (e): kare metni öncekiyle ≥%95 aynıysa sonraki bu kadar kare atlanır (0 = kapalı)
_ocr_havuz, _ocr_say, _ocr_kur = queue.Queue(), [0], threading.Lock()


def _motor_kur():
    global OCR_AYGIT
    from rapidocr_onnxruntime import RapidOCR
    try:  # CUDA sağlayıcı yüklenemezse (DLL yok) ORT sessizce CPU'ya düşer: sağlayıcı listesinden doğrula
        m = RapidOCR(det_use_cuda=True, cls_use_cuda=True, rec_use_cuda=True)
        prov = getattr(getattr(getattr(m, "text_det", None), "infer", None), "session", None)
        OCR_AYGIT = "cuda" if prov is None or "CUDAExecutionProvider" in prov.get_providers() else "cpu"
        m = m if OCR_AYGIT == "cuda" else RapidOCR()
    except Exception:
        m, OCR_AYGIT = RapidOCR(), "cpu"
    print(f"ocr aygit={OCR_AYGIT}", flush=True)
    return m


def ocr_motor():
    global _ocr
    if _ocr is None:
        _ocr = _motor_kur()
    return _ocr


def ocr_oturum():
    """Havuzdan boş oturum; yoksa sınıra dek yeni kurar (CPU'ya düşerse tek oturum), sınır doluysa boşalanı bekler. Çağıran putlamalı."""
    try:
        return _ocr_havuz.get_nowait()
    except queue.Empty:
        pass
    with _ocr_kur:
        if _ocr_say[0] < (OCR_OTURUM if OCR_AYGIT != "cpu" else 1):
            ram_kapi(60)
            _ocr_say[0] += 1
            return _motor_kur()
    return _ocr_havuz.get()


YAZI_ESIK = int(os.environ.get("VD_YAZI", "0"))  # HIZ-4 yazı ön sınıflandırıcı: yazı benzeri blok sayısı bunun altındaki kare OCR'ye girmez (0 = kapalı)


def yazi_blok(k):
    import cv2
    g = cv2.imread(str(k), cv2.IMREAD_GRAYSCALE)
    if g is None:
        return 999
    e = cv2.morphologyEx(g, cv2.MORPH_GRADIENT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    _, b = cv2.threshold(e, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1)))
    n, _, st, _ = cv2.connectedComponentsWithStats(b)
    return sum(1 for x, y, w, h, a in st[1:] if 18 <= w <= 400 and 6 <= h <= 60 and w >= 1.8 * h and a >= 0.3 * w * h)


def ocr(ks):
    gorulen, out = set(), []
    if YAZI_ESIK:
        yazili = [k for k in ks if yazi_blok(k) >= YAZI_ESIK]
        print(f"yazi_kapi {len(yazili)}/{len(ks)}", flush=True)
        ks = yazili
    onc, i = None, 0
    while i < len(ks):
        k = ks[i]
        i += 1
        m = ocr_oturum()
        try:
            t0 = time.time()
            res, _ = m(str(k), use_cls=os.environ.get("VD_OCR_CLS", "0") == "1")  # TUR 2: açı sınıflandırıcı ekran metninde gereksiz, kare başı süre düşer
            if OCR_AYGIT == "cuda":
                gpu_nefes(time.time() - t0)  # patlama sonrası nefes (bekçi %78 eşiği); Ömer başında değilse atlanır
        except Exception:
            continue
        finally:
            _ocr_havuz.put(m)
        simdi = {t.strip().lower() for _, t, c in res or [] if len(t.strip()) > 2 and float(c) > 0.6}
        if OCR_ATLA and onc is not None and ((not simdi and not onc) or (simdi and onc and len(simdi & onc) / len(simdi | onc) >= 0.95)):
            i += OCR_ATLA
        onc = simdi
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
    if (Path(__file__).resolve().parents[1] / ".kos" / "yerel-model.kapali").exists():  # HAVUZ-GENIS-2: yerel KAPALI bayrağı
        return None
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/chat", json.dumps(istek).encode(), {"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=300))["message"]["content"]
    except Exception:
        return None


gemini_durum = {"kapali": 0.0}
HAVUZ_G = [("nvidia", "meta/llama-3.2-11b-vision-instruct"), ("mistral", "ministral-8b-latest"), ("groq", "qwen/qwen3.8-27b"),
           ("openrouter", "minimax/minimax-m3.1-flash:free"), ("nvidia", "nvidia/ising-calibration-1.5-31b"), ("gemini", "gemini-3.5-flash-lite")]  # gorsel_dogrula.py 3/3 geçenler
HAVUZ_SIRA, HAVUZ_KOTA = [0], {}  # sağlayıcı → soğuma bitişi; HAVUZ_G ≤3 deneme/link


def havuz_aciklama(ks, n=3):
    """VIDEO-HIZ-4: ücretsiz görsel model havuzu, link başına en fazla 3 istek; 429/hata → sağlayıcı 10 dk soğur, sıradaki denenir."""
    if not ks:
        return None
    try:
        import havuz_envanter as E
    except Exception:
        return None
    sec = [ks[int(i * len(ks) / n)] for i in range(min(n, len(ks)))]
    icerik = [{"type": "text", "text": KARE_PROMPT}] + [{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(k.read_bytes()).decode()}} for k in sec]
    with KILIT:
        bas = HAVUZ_SIRA[0]; HAVUZ_SIRA[0] += 1
    denenen = 0
    for i in range(len(HAVUZ_G)):
        prov, model = HAVUZ_G[(bas + i) % len(HAVUZ_G)]
        if time.time() < HAVUZ_KOTA.get(prov, 0) or denenen >= 3:
            continue
        denenen += 1
        try:
            m, kod, _, _ = E._gonder(prov, model, icerik, 1200, 60)
        except Exception:
            m, kod = None, 599
        if m and len(m.strip()) > 40:
            return m
        HAVUZ_KOTA[prov] = time.time() + 600
    return None


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


ACIK_KUYRUK = KOK / ".kos/kopru/aciklama-kuyruk"  # TUR 2: ücretsiz havuz tükenince kareler burada bekler; `--doldur` sonradan açıklar


def kuyruga_al(kod, ks, n=3):
    sec = [ks[int(i * len(ks) / n)] for i in range(min(n, len(ks)))]
    q = ACIK_KUYRUK / kod
    q.mkdir(parents=True, exist_ok=True)
    for i, k in enumerate(sec):
        shutil.copy(k, q / f"{i}.jpg")


def doldur(cikti=None):
    """Kuyruktaki videoların kare açıklamasını havuzdan doldurur (JSON'daki kare_aciklama null → metin); başarılı olan kuyruktan silinir."""
    cikti = cikti or CIKTI
    n = 0
    for q in sorted(ACIK_KUYRUK.glob("*")) if ACIK_KUYRUK.exists() else []:
        j = cikti / f"{q.name}.json"
        if not j.exists():
            continue
        r = havuz_aciklama(sorted(q.glob("*.jpg")), n=3) or gemini_aciklama(sorted(q.glob("*.jpg")), n=3)
        if r:
            v = json.loads(j.read_text(encoding="utf-8")); v["kare_aciklama"] = r
            j.write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
            shutil.rmtree(q); n += 1
    print(f"DOLDUR doldurulan={n}", flush=True)


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
        ram_kapi()
        with DL_SEM, zam(kod, "indir"):  # ağ/CPU kuyruğu: GPU işçileri beklemesin diye ayrı eşzamanlılık
            v, hata = indir(url, d)
        if not v:
            if "No video formats found" in hata:  # kalıcı: format yok, yeniden deneme anlamsız
                with ATLA_DOSYA.open("a", encoding="utf-8") as f:
                    f.write(kod + "\n")
                return kod, "atla"
            return kod, "indirilemedi: " + hata.strip().splitlines()[-1][:120] if hata.strip() else "indirilemedi"
        t1 = time.time(); adim["indir"] = t1 - t0
        with zam(kod, "asr"):
            dil, seg, kaynak = asr(v, d)
        t2 = time.time(); adim["asr"] = t2 - t1
        ram_kapi()
        with CPU_SEM, zam(kod, "kare"):
            ks = kareler(v, d)
        t3 = time.time(); adim["kare"] = t3 - t2
        def acik_zamanli():  # ölçüm: açıklama süresi ayrı tutulur (ADIM satırı)
            s = time.time(); r = havuz_aciklama(ks) or gemini_aciklama(ks)
            if not r and os.environ.get("VD_YEREL", "0") == "1":  # TUR 2: yerel Ollama ikinci GPU süreci → varsayılan KAPALI, açıklama kuyruğa
                r = yerel_aciklama(ks)
            if not r:
                kuyruga_al(kod, ks)
            adim["acik_s"] = time.time() - s; return r
        with ThreadPoolExecutor(1) as px:  # kare açıklaması (Gemini/Ollama) OCR ile örtüşür; profilde "ocr" ikisini birden kapsar
            acik_f = px.submit(acik_zamanli)
            with zam(kod, "ocr"):
                ekran = ocr(ks)
            adim["ocr_s"] = time.time() - t3
            acik = acik_f.result()
        t4 = time.time(); adim["ocr"] = t4 - t3
        ekran_m = "\n".join(e["t"] for e in ekran)
        duzeltme = []  # ekranda yazılı araç adı ASR'de başka duyulduysa ekrandaki alınır (ölçü: ekran_adlari_olc.py)
        for s in seg:
            s["t"], ops = ekran_duzelt.duzelt(s["t"], ekran_m)
            duzeltme += ops
        metin = ekran_m + "\n" + " ".join(s["t"] for s in seg)
        linkler = sorted({m.strip(".,)") for m in URL_RE.findall(metin)})
        komutlar = sorted({m.strip() for m in KOMUT_RE.findall(metin)})
        info = {}
        ij = next(d.glob("*.info.json"), None)
        if ij:
            j = json.loads(ij.read_text(encoding="utf-8"))
            info = {"baslik": j.get("title"), "sure": j.get("duration"), "yukleyen": j.get("uploader"), "aciklama": (j.get("description") or "")[:800]}
        veri = {"kod": kod, "url": url, "dil": dil, "meta": info, "transkript": seg, "ekran": ekran,
                "linkler": linkler, "komutlar": komutlar, "kare_aciklama": acik, "kare_sayisi": len(ks), "duzeltme": duzeltme,
                "asr": {"kaynak": kaynak, "kelime_sn": round(sum(len(x["t"].split()) for x in seg) / info["sure"], 2) if info.get("sure") else None}}
        adim["acik"] = time.time() - t4
        with KILIT, PROFIL.open("a", encoding="utf-8") as f:
            f.write(f"{kod}\t" + "\t".join(f"{adim[x]:.1f}" for x in ("indir", "asr", "kare", "ocr", "acik")) + f"\t{len(ks)}\t{OCR_AYGIT}\n")
        CIKTI.mkdir(parents=True, exist_ok=True)
        hedef.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        print("ADIM " + kod + " " + json.dumps({k: round(v, 1) for k, v in adim.items()}), flush=True)  # ölçüm
        return kod, f"ok seg={len(seg)} ocr={len(ekran)} link={len(linkler)} komut={len(komutlar)}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def isle_post(url):
    """YENIDEN-GECIS-1: /p/ gönderisi — gallery-dl ile TÜM slaytlar, her görsele OCR, video slaytına ASR+kare OCR, açıklama."""
    kod = kod_of(url)
    hedef = CIKTI / f"{kod}.json"
    if hedef.exists():
        return kod, "var"
    if kod in atla_kodlari():
        return kod, "atla"
    d = Path(tempfile.mkdtemp(prefix="vp_"))
    try:
        r = kos("gallery-dl", *cerez_arg(url), "-D", d, "--write-metadata", url, timeout=300)
        slaytlar = sorted(p for p in d.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".mp4"))
        if not slaytlar:
            return kod, "indirilemedi: " + (r.stderr.strip().splitlines() or ["slayt yok"])[-1][:120]
        gorseller = [p for p in slaytlar if p.suffix.lower() != ".mp4"]
        seg, ks, dil = [], list(gorseller), None
        for i, v in enumerate(p for p in slaytlar if p.suffix.lower() == ".mp4"):
            dv = d / f"v{i}"; dv.mkdir()
            dil, s, _ = asr(v, dv); seg += s
            ks += kareler(v, dv, tavan=30)  # karusel video slaytı: 240 kare × 9 slayt OCR kuyruğunu saatlerce tıkıyordu
        ekran = ocr(ks)
        ekran_m = "\n".join(e["t"] for e in ekran)
        duzeltme = []
        for s in seg:
            s["t"], ops = ekran_duzelt.duzelt(s["t"], ekran_m)
            duzeltme += ops
        aciklama = ""
        for mj in d.glob("*.json"):
            try:
                j = json.loads(mj.read_text(encoding="utf-8"))
            except Exception:
                continue
            aciklama = aciklama or str(j.get("description") or j.get("caption") or "")[:800]
        metin = ekran_m + "\n" + " ".join(s["t"] for s in seg) + "\n" + aciklama
        linkler = sorted({m.strip(".,)") for m in URL_RE.findall(metin)})
        komutlar = sorted({m.strip() for m in KOMUT_RE.findall(metin)})
        veri = {"kod": kod, "url": url, "dil": dil, "meta": {"aciklama": aciklama, "slayt": len(slaytlar)}, "transkript": seg, "ekran": ekran,
                "linkler": linkler, "komutlar": komutlar, "kare_aciklama": None, "kare_sayisi": len(ks), "duzeltme": duzeltme}
        CIKTI.mkdir(parents=True, exist_ok=True)
        hedef.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        return kod, f"ok post slayt={len(slaytlar)} ocr={len(ekran)} link={len(linkler)} komut={len(komutlar)}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


RAM_AZALT, RAM_DUR = 94, 96  # Ömer 03.11 RAM eşiği %97'ye taşındı; RAM-BEKCI-3: ≥86'da işçi yarıya (çalışanlar kesilmez, yeni video sayı altına inene dek beklemez), ≥88'de yeni video yok (tavan %89)
AKTIF, AKTIF_KILIT = [0], threading.Lock()


def isci_hedef(r, es):
    return 0 if r >= RAM_DUR else max(1, es // 2) if r >= RAM_AZALT else es


def ram_bekle(es):
    """Eşzamanlı işçi sayısı RAM'e göre isci_hedef'i aşmayana dek bekler; slot alır (calis bırakır)."""
    while True:
        with AKTIF_KILIT:
            if AKTIF[0] < isci_hedef(psutil.virtual_memory().percent, es):
                AKTIF[0] += 1
                return
        time.sleep(2)  # TUR 2: 30 sn bekleme RAM düşünce işçileri boşta bırakıyordu


def calis(u, es=3):
    ram_bekle(es)
    t = time.time()
    try:
        kod, durum = isle_post(u) if re.search(r"instagram\.com/p/", u) and shutil.which("gallery-dl") else isle(u)
    except Exception as e:  # tek video hatası toplu işi durdurmaz
        kod, durum = kod_of(u), f"hata: {str(e)[:120]}"
    finally:
        with AKTIF_KILIT:
            AKTIF[0] -= 1
    satir = f"{kod}\t{durum}\t{time.time() - t:.0f}s"
    with KILIT:
        print(satir, flush=True)
        with ILERLEME.open("a", encoding="utf-8") as f:
            f.write(satir + "\n")
    return durum


GPU_PY = Path(os.environ.get("VD_OCR_PY") or KOK / ".kos/kopru/venv-ocr/Scripts/python.exe")


def main():
    # genel python'da onnxruntime CPU'dur (OCR ~19x yavaş: 0,33 → 6,5 sn/kare, OCR-HIZ-1); onnxruntime-gpu venv-ocr'de
    if GPU_PY.is_file() and Path(sys.prefix).resolve() != GPU_PY.parents[1].resolve():
        sys.exit(subprocess.call([str(GPU_PY), *sys.argv], stdout=sys.stdout, stderr=sys.stderr, creationflags=NW))  # NW tek başına çıktıyı yutar: akış açıkça verilir
    a = sys.argv[1:]
    if a and a[0] == "--doldur":
        return doldur()
    en, es = 10**9, 3
    if "--en" in a:
        i = a.index("--en"); en = int(a[i + 1]); del a[i:i + 2]
    if "--es" in a:  # eşzamanlı video işçisi; GPU döküm sırası ASR_KILIT ile tek kalır
        i = a.index("--es"); es = es_sinirla(int(a[i + 1])); del a[i:i + 2]
    if a and a[0] == "--liste":
        urls = re.findall(r"https?://\S+", Path(a[1]).read_text(encoding="utf-8"))
        urls = [u.split("\t")[0] for u in dict.fromkeys(urls)]
    else:
        urls = a
    # yapılmış ve atlanacaklar baştan elenir: --en yalnız yeni işleri sayar
    urls = [u for u in urls if not (CIKTI / f"{kod_of(u)}.json").exists() and kod_of(u) not in atla_kodlari()][:en]
    ozet, sayac = Counter(), 0
    dur = threading.Event()
    threading.Thread(target=kesme_izle, args=(dur,), daemon=True).start()
    with ThreadPoolExecutor(es) as ex:
        for durum in ex.map(lambda u: "kesildi" if KESIK.is_set() else calis(u, es), urls):
            ozet[durum.split(":")[0]] += 1
            sayac += 1
            if sayac % 50 == 0:  # her 50 işlemde özet
                print(f"OZET islenen={sayac} {dict(ozet)}", flush=True)
    dur.set()
    print(f"BITIS islenen={sayac} {dict(ozet)}", flush=True)  # gözetmen (toplu_gozetmen.py) temiz bitişi bundan anlar


if __name__ == "__main__":
    main()
