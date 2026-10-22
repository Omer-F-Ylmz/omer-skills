"""Altın referansa (.kos/kopru/wer-altin/<id>.altin.txt) karşı yerel Whisper WER ölçümü.

Kullanım: venv-ocr\\Scripts\\python.exe tools/wer_altin_olc.py [--model large-v3,large-v3-turbo] [--ikinci 0.5,0.7]
  --ikinci: large-v3 + Groq ikinci geçiş; avg_logprob < eşik olan segmentler Groq'a gider (eşik başına bir satır)
Çıktı: .kos/kopru/wer-altin/olcum.json (yalnız özet yazdırılır)
"""
import argparse
import io
import json
import subprocess
import sys
import time
import wave
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
import wer_altin as wa  # noqa: E402

ALTIN, TMP = wa.ALTIN, wa.TMP


def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    d = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        yeni = [i]
        for j, hw in enumerate(h, 1):
            yeni.append(min(d[j] + 1, yeni[j - 1] + 1, d[j - 1] + (rw != hw)))
        d = yeni
    return d[-1] / max(len(r), 1)


def kes(wav, bas, son):
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        w.setpos(int(bas * sr))
        kare = w.readframes(int((son - bas) * sr))
    tampon = io.BytesIO()
    with wave.open(tampon, "wb") as o:
        o.setnchannels(1)
        o.setsampwidth(2)
        o.setframerate(sr)
        o.writeframes(kare)
    return tampon.getvalue()


def groq_parca(veri):
    g, ct = wa.multipart({"model": "whisper-large-v3", "temperature": "0", "language": "tr"}, veri, "file")
    r = wa.urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", g,
                                  {"Authorization": "Bearer " + wa.os.environ["GROQ_API_KEY"], "Content-Type": ct, **wa.UA})
    for bekle in (5, 15, 30, 60, 0):  # Groq ücretsiz dakika sınırı: 429'da bekle
        try:
            return json.load(wa.urllib.request.urlopen(r, timeout=120))["text"]
        except wa.urllib.error.HTTPError as e:
            if e.code != 429 or not bekle:
                raise
            time.sleep(bekle)


GROQ_ONB = ALTIN / "groq-seg.json"


def groq_onbellekli(k, bas, son):
    """Segment başına Groq metni diske yazılır; kesilen koşu kaldığı yerden sürer."""
    onb = json.loads(GROQ_ONB.read_text(encoding="utf-8")) if GROQ_ONB.exists() else {}
    anahtar = f"{k}:{bas:.2f}-{son:.2f}"
    if anahtar not in onb:
        onb[anahtar] = groq_parca(kes(TMP / f"{k}_0.wav", bas, son))
        GROQ_ONB.write_text(json.dumps(onb, ensure_ascii=False), encoding="utf-8")
        print(len(onb), "groq seg", flush=True)
    return onb[anahtar]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="large-v3-turbo,large-v3")
    ap.add_argument("--ikinci", default="")
    a = ap.parse_args()
    import video_derin as vd  # CUDA DLL PATH'i süreçte kurulur
    from faster_whisper import WhisperModel

    kodlar = sorted(p.name.split(".")[0] for p in ALTIN.glob("*.altin.txt"))
    refler = {k: (ALTIN / f"{k}.altin.txt").read_text(encoding="utf-8") for k in kodlar}
    sonuc = {"groq_tek": round(sum(wer(refler[k], wa.norm((ALTIN / f"{k}.groq.txt").read_text(encoding="utf-8"))) * len(refler[k].split()) for k in kodlar) / sum(len(r.split()) for r in refler.values()), 4)}
    toplam_sn = sum(wave.open(str(TMP / f"{k}_0.wav")).getnframes() / 16000 for k in kodlar)
    for ad in a.model.split(","):
        model = WhisperModel(ad, device="cuda", compute_type=vd.WHISPER["cuda"][1])
        onbellek = ALTIN / f"seg-{ad}.json"
        if onbellek.exists():  # ASR bir kez koşar; ikinci geçiş denemeleri bunu kullanır
            segler, sure = json.loads(onbellek.read_text(encoding="utf-8")).values()
        else:
            segler, sure = {}, 0.0
            for k in kodlar:
                t0 = time.time()
                seg, _ = model.transcribe(str(TMP / f"{k}_0.wav"), language="tr", vad_filter=True)
                segler[k] = [(s.start, s.end, s.text, s.avg_logprob) for s in seg]
                sure += time.time() - t0
            onbellek.write_text(json.dumps({"segler": segler, "sure": sure}), encoding="utf-8")
        varyantlar = {ad: None}
        if ad == "large-v3":
            varyantlar.update({f"{ad}+groq<{e}": float(e) for e in a.ikinci.split(",") if e})
        for ad_v, esik in varyantlar.items():
            hata = kelime = 0
            for k in kodlar:
                metin, n2 = [], 0
                for bas, son, t, lp in segler[k]:
                    if esik is not None and lp < esik and son - bas > 0.5:
                        t, n2 = groq_onbellekli(k, bas, son), n2 + 1
                    metin.append(t)
                n = len(refler[k].split())
                hata += wer(refler[k], wa.norm(" ".join(metin))) * n
                kelime += n
            sonuc[ad_v] = {"wer": round(hata / kelime, 4), "asr_sn": round(sure, 1), "ses_sn": round(toplam_sn), "hiz_x": round(toplam_sn / sure, 1)}
        del model
    (ALTIN / "olcum.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(sonuc, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
