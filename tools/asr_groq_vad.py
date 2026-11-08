"""DERIN-HIZ-3 yol 2: yerelle AYNI VAD segmentleri Groq whisper-large-v3'e parça parça. Kullanım: asr_groq_vad.py <kod> <wav> [maks_sn]
Segmentler faster-whisper VAD'ından (get_speech_timestamps, varsayılan parametre) çıkar, maks_sn'ye (30) kadar birleştirilir; her parça ayrı istek (3,2 sn aralık)."""
import difflib, io, json, os, re, sys, time, urllib.request, wave
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import video_derin as vd
from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps


def kel(t):
    return re.sub(r"[^\w\s]", "", t.lower()).split()


kod, wav = sys.argv[1:3]
maks = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
SR = 16000
a = decode_audio(wav, sampling_rate=SR)
ts = get_speech_timestamps(a, VadOptions())
parca, cur = [], None
for s in ts:  # örnek indeksleri; maks_sn dolana dek birleştir
    if cur and (s["end"] - cur[0]) / SR <= maks:
        cur[1] = s["end"]
    else:
        cur = [s["start"], s["end"]]
        parca.append(cur)
print(f"{len(ts)} VAD segmenti -> {len(parca)} parça", flush=True)
key = os.environ["GROQ_API_KEY"]
t0, metin, istek = time.time(), [], 0
for b, e in parca:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a[b:e] * 32767).astype("int16").tobytes())
    sinir = "vd" + str(time.time_ns())
    alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
    govde = (alan("model", "whisper-large-v3") + alan("response_format", "json") + alan("temperature", "0") + alan("language", "tr")
             + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
             + buf.getvalue() + f"\r\n--{sinir}--\r\n".encode())
    req = urllib.request.Request(vd.GROQ_ASR, govde, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
    for deneme in range(3):
        try:
            metin.append(json.load(urllib.request.urlopen(req, timeout=60))["text"].strip())
            break
        except Exception as ex:
            print("hata", str(ex)[:80], flush=True)
            time.sleep(10)
    istek += 1
    time.sleep(3.2)
sn = time.time() - t0
eski = json.loads((vd.KOK / "docs/video-tarama/derin" / f"{kod}.json").read_text(encoding="utf-8"))
x, y = kel(" ".join(s["t"] for s in eski["transkript"])), kel(" ".join(metin))
print(f"{kod} groq-vad maks={maks} istek={istek} sure={sn:.1f}s kelime {len(x)}->{len(y)} benzerlik={difflib.SequenceMatcher(None, x, y, autojunk=False).ratio():.4f}")
