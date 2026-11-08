"""VIDEO-HIZ-5 TUR 2 (2): Gemini ses→yazı recall ölçümü, ref2'ye göre.
Kullanım: hiz5_gemini_asr.py indir | kos <model> [azami_video]
indir: ref2'deki videoların sesini .kos/kopru/hiz5/ses/<kod>.wav (16 kHz mono) olarak indirir.
kos: sesi Gemini'ye yollar, ogren/hiz4/h5_gem_<model>/<kod>.json yazar (hiz4 biçimi; recall: hiz5_asr_recall.py h5_gem_<model>)."""
import base64, json, os, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
H4 = KOK / ".kos/kopru/ogren/hiz4"
SES = KOK / ".kos/kopru/hiz5/ses"
NW = 0x08000000
SES.mkdir(parents=True, exist_ok=True)
kodlar = sorted(p.stem for p in (H4 / "ref2").glob("*.json"))

if sys.argv[1] == "indir":
    for k in kodlar:
        w = SES / f"{k}.wav"
        if w.exists():
            continue
        ham = SES / f"{k}.ham"
        subprocess.run(["yt-dlp", "-q", "-f", "bestaudio", "-o", str(ham) + ".%(ext)s", f"https://www.youtube.com/shorts/{k}"], creationflags=NW)
        g = next(SES.glob(f"{k}.ham.*"), None)
        if g:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(g), "-vn", "-ac", "1", "-ar", "16000", str(w)], creationflags=NW)
            print(k, w.exists(), flush=True)
    sys.exit()

model = sys.argv[2]
azami = int(sys.argv[3]) if len(sys.argv) > 3 else 99
cikti = H4 / f"h5_gem_{model}"
cikti.mkdir(exist_ok=True)
key = os.environ["GEMINI_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
sistem = "Transcribe the speech in this audio verbatim, in its original language. Output only the transcript text, no commentary, no timestamps."
n = 0
for k in kodlar:
    w = SES / f"{k}.wav"
    if not w.exists() or (cikti / f"{k}.json").exists():
        continue
    if n >= azami:
        break
    govde = {"contents": [{"parts": [{"text": sistem}, {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(w.read_bytes()).decode()}}]}],
             "generationConfig": {"temperature": 0}}
    req = urllib.request.Request(url, json.dumps(govde).encode(), {"x-goog-api-key": key, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=120))
        metin = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"]).strip()
    except urllib.error.HTTPError as e:
        print(k, "HATA", e.code, e.read().decode("utf-8", "replace")[:300], flush=True)
        if e.code == 429:
            break
        continue
    sure = w.stat().st_size / 32000
    (cikti / f"{k}.json").write_text(json.dumps({"kod": k, "dil": "", "transkript": [{"b": 0.0, "s": round(sure, 1), "t": metin}]}, ensure_ascii=False), encoding="utf-8")
    n += 1
    print(k, f"{time.time() - t0:.1f}sn", len(metin.split()), "kelime", flush=True)
    time.sleep(0.5)
