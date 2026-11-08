"""VIDEO-HIZ-5 TUR 2 (2): ikinci ücretsiz bulut ASR adayı (Mistral Voxtral) — ref2'ye göre recall ölçümü.
Kullanım: hiz5_bulut_asr.py mistral <model> [azami_video]   (ses: .kos/kopru/hiz5/ses/<kod>.wav, hiz5_gemini_asr.py indir üretir)
Çıktı: ogren/hiz4/h5_<saglayici>_<model>/<kod>.json (hiz4 biçimi); recall: hiz5_asr_recall.py h5_<saglayici>_<model>"""
import base64, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
H4 = KOK / ".kos/kopru/ogren/hiz4"
SES = KOK / ".kos/kopru/hiz5/ses"
URL = {"mistral": "https://api.mistral.ai/v1/audio/transcriptions", "openrouter": "https://openrouter.ai/api/v1/chat/completions"}
KEY = {"mistral": "MISTRAL_API_KEY", "openrouter": "OPENROUTER_API_KEY"}
sag, model = sys.argv[1], sys.argv[2]
azami = int(sys.argv[3]) if len(sys.argv) > 3 else 99
cikti = H4 / f"h5_{sag}_{model.replace('/', '-').replace(':', '-')}"
cikti.mkdir(exist_ok=True)
key = os.environ[KEY[sag]]
n = 0
for w in sorted(SES.glob("*.wav")):
    k = w.stem
    if not (H4 / "ref2" / f"{k}.json").exists() or (cikti / f"{k}.json").exists():
        continue
    if n >= azami:
        break
    if sag == "openrouter":  # sohbet API'si, ses input_audio olarak
        govde = json.dumps({"model": model, "max_tokens": 1500, "temperature": 0, "messages": [{"role": "user", "content": [
            {"type": "text", "text": "Transcribe the speech in this audio verbatim, in its original language. Output only the transcript text."},
            {"type": "input_audio", "input_audio": {"data": base64.b64encode(w.read_bytes()).decode(), "format": "wav"}}]}]}).encode()
        req = urllib.request.Request(URL[sag], govde, {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "curl/8.5.0"})
    else:
        sinir = "b" + str(time.time_ns())
        alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
        govde = (alan("model", model) + alan("temperature", "0")
                 + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
                 + w.read_bytes() + f"\r\n--{sinir}--\r\n".encode())
        req = urllib.request.Request(URL[sag], govde, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        print(k, "HATA", e.code, e.read().decode("utf-8", "replace")[:300], dict(e.headers.items()).get("retry-after"), flush=True)
        if e.code == 429:
            break
        continue
    metin = (r["choices"][0]["message"]["content"] if sag == "openrouter" else r.get("text") or "").strip()
    (cikti / f"{k}.json").write_text(json.dumps({"kod": k, "dil": r.get("language") or "", "transkript": [{"b": 0.0, "s": round(w.stat().st_size / 32000, 1), "t": metin}]}, ensure_ascii=False), encoding="utf-8")
    n += 1
    print(k, f"{time.time() - t0:.1f}sn", len(metin.split()), "kelime", flush=True)
    time.sleep(0.3)
