"""TR ASR WER ölçümü: altyazı (.tr.vtt) referans, video_derin ile aynı Whisper modeli/aygıtı.

Kullanım: venv-ocr\\Scripts\\python.exe tools/wer_olc.py [--n 5]
Çıktı: .kos/kopru/rapor/wer-tr.json (yalnız özet döner)
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
RAW = KOK / "docs/video-tarama/raw"
TMP = KOK / ".kos/kopru/wer-tmp"
CIKTI = KOK / ".kos/kopru/rapor/wer-tr.json"


def sec(vtt):
    satirlar, onceki = [], None
    for s in vtt.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = re.sub(r"<[^>]+>", "", s).strip()
        if not s or s == "WEBVTT" or "-->" in s or s.isdigit() or s == onceki:
            continue  # otomatik altyazıdaki yinelenen satırları at
        satirlar.append(s)
        onceki = s
    return norm(" ".join(satirlar))


def norm(m):
    m = re.sub(r"[^\w\s]", " ", m.lower())
    return re.sub(r"\s+", " ", m).strip()


def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    d = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        yeni = [i]
        for j, hw in enumerate(h, 1):
            yeni.append(min(d[j] + 1, yeni[j - 1] + 1, d[j - 1] + (rw != hw)))
        d = yeni
    return d[-1] / max(len(r), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    a = ap.parse_args()
    sys.path.insert(0, str(KOK / "tools"))
    import video_derin as vd  # import ile CUDA13 DLL PATH'i süreçte kurulur (pipeline ile aynı)
    from faster_whisper import WhisperModel

    adaylar = [v for v in sorted(RAW.glob("*.tr.vtt")) if not (RAW / v.name.replace(".tr.vtt", ".tr-orig.vtt")).exists()][: a.n]
    TMP.mkdir(parents=True, exist_ok=True)
    model_adi, tip = vd.WHISPER["cuda"]
    model = WhisperModel(model_adi, device="cuda", compute_type=tip)
    sonuc = []
    for v in adaylar:
        kod = v.name.replace(".tr.vtt", "")
        wav = TMP / f"{kod}.wav"
        if not wav.exists():
            subprocess.run(["yt-dlp", "-x", "--audio-format", "wav", "--postprocessor-args", "ffmpeg:-ac 1 -ar 16000",
                            "-o", str(TMP / f"{kod}.%(ext)s"), f"https://www.youtube.com/watch?v={kod}"], check=False, capture_output=True)
        if not wav.exists():
            sonuc.append({"id": kod, "hata": "ses indirilemedi"})
            continue
        seg, _ = model.transcribe(str(wav), language="tr", vad_filter=True)
        hyp = norm(" ".join(s.text for s in seg))
        ref = sec(v)
        sonuc.append({"id": kod, "ref_kelime": len(ref.split()), "wer": round(wer(ref, hyp), 4)})
        print(f"{kod} ref={len(ref.split())} wer={sonuc[-1]['wer']}", flush=True)
    olculen = [s["wer"] for s in sonuc if "wer" in s]
    ozet = {"n": len(olculen), "ort_wer": round(sum(olculen) / len(olculen), 4) if olculen else None, "videolar": sonuc}
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"n": ozet["n"], "ort_wer": ozet["ort_wer"]}))


if __name__ == "__main__":
    sys.exit(main())
