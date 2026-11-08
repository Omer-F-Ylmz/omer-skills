"""VIDEO-HIZ-5 TUR 2 (1): Groq ASR kotasını gerçekte ölç — yanıt başlıkları ve ilk 429 anı.
Kullanım: python -I tools/hiz5_groq_kota.py <wav> <model> <azami_istek> [aralik_sn]
Her istek bir satır JSON olarak .kos/kopru/hiz5/groq_kota_<model>.jsonl dosyasına yazılır (ara kayıt)."""
import json, sys, time, pathlib, os, urllib.request, urllib.error

URL = "https://api.groq.com/openai/v1/audio/transcriptions"
wav, model, azami = pathlib.Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
aralik = float(sys.argv[4]) if len(sys.argv) > 4 else 3.2
sure = wav.stat().st_size / 32000
cikti = pathlib.Path(".kos/kopru/hiz5") / f"groq_kota_{model}.jsonl"
key = os.environ["GROQ_API_KEY"]
toplam = 0.0
for i in range(azami):
    sinir = "k" + str(time.time_ns())
    alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
    govde = (alan("model", model) + alan("response_format", "json") + alan("temperature", "0")
             + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
             + wav.read_bytes() + f"\r\n--{sinir}--\r\n".encode())
    req = urllib.request.Request(URL, govde, {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=90)
        kod, bas, ek = r.status, r.headers, ""
        toplam += sure
    except urllib.error.HTTPError as e:
        kod, bas, ek = e.code, e.headers, e.read().decode("utf-8", "replace")[:300]
    satir = {"i": i + 1, "t": round(t0, 1), "kod": kod, "kumulatif_ses_sn": round(toplam, 1), "sn": round(time.time() - t0, 1),
             "baslik": {k.lower(): v for k, v in bas.items() if k.lower().startswith(("x-ratelimit", "retry-after"))}, "ek": ek}
    with cikti.open("a", encoding="utf-8") as f:
        f.write(json.dumps(satir, ensure_ascii=False) + "\n")
    print(json.dumps(satir, ensure_ascii=False), flush=True)
    if kod == 429:
        break
    time.sleep(aralik)
