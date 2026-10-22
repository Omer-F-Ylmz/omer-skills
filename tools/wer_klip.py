"""TR ASR WER varyant ölçümü: 5 klip (wer-tmp wav'larından kesit), ref = Groq whisper-large-v3, hyp = yerel large-v3-turbo varyantları.

Kullanım: venv-ocr\\Scripts\\python.exe tools/wer_klip.py [--sure 300]
Çıktı: .kos/kopru/rapor/wer-klip.json (varyant WER + hata sınıfı sayıları, örnekler)
"""
import argparse
import difflib
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
TMP = KOK / ".kos/kopru/wer-tmp"
CIKTI = KOK / ".kos/kopru/rapor/wer-klip.json"
KLIPLER = [("NpzqWvKR_iw", 0), ("PcoZp3Hzx58", 0), ("PcoZp3Hzx58", 1500), ("TyG4ylryRfU", 0), ("TyG4ylryRfU", 1500)]
SOZLUK = "Claude Code, Claude, Anthropic, ChatGPT, OpenAI, Gemini, Cursor, GitHub, API, MCP, n8n, Veo, Sora, Kling, Midjourney, yapay zeka, prompt."
VARYANT = {
    "taban": {},
    "large_v3": {"_model": "large-v3"},
    "large_v3_tr": {"_model": "large-v3", "language": "tr"},
    "dil_tr": {"language": "tr"},
    "dil_tr_sozluk": {"language": "tr", "initial_prompt": SOZLUK},
    "dil_tr_sozluk_vad": {"language": "tr", "initial_prompt": SOZLUK, "condition_on_previous_text": False,
                          "vad_parameters": {"threshold": 0.4, "min_silence_duration_ms": 500, "speech_pad_ms": 300}},
}


def groq_ref(wav):
    key = os.environ["GROQ_API_KEY"]
    sinir = "wk" + str(os.getpid())
    alan = lambda ad, de: f'--{sinir}\r\nContent-Disposition: form-data; name="{ad}"\r\n\r\n{de}\r\n'.encode()
    govde = (alan("model", "whisper-large-v3") + alan("temperature", "0") + alan("response_format", "verbose_json")
             + f'--{sinir}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
             + wav.read_bytes() + f"\r\n--{sinir}--\r\n".encode())
    req = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", govde,
                                 {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={sinir}", "User-Agent": "curl/8.5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    return r["language"], r["text"]


def sinif(r, h):
    if any(c.isdigit() for c in r + h):
        return "sayi"
    if len(os.path.commonprefix([r, h])) >= 4:
        return "ek"
    return "ozel_ad_diger"


def hatalar(ref, hyp):
    r, h = ref.split(), hyp.split()
    sayac, ornek = {"sayi": 0, "ek": 0, "ozel_ad_diger": 0, "eksik": 0, "fazla": 0}, {}
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, r, h, autojunk=False).get_opcodes():
        if op == "replace":
            for a, b in zip(r[i1:i2], h[j1:j2]):
                k = sinif(a, b)
                sayac[k] += 1
                ornek.setdefault(k, []).append(f"{a}>{b}")
            sayac["eksik"] += max(0, (i2 - i1) - (j2 - j1))
            sayac["fazla"] += max(0, (j2 - j1) - (i2 - i1))
        elif op == "delete":
            sayac["eksik"] += i2 - i1
        elif op == "insert":
            sayac["fazla"] += j2 - j1
    return sayac, {k: v[:12] for k, v in ornek.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sure", type=int, default=300)
    ap.add_argument("--klip", help="virgüllü id: wer-tmp/<id>_0.wav hazır tam ses (reel); verilirse KLIPLER yerine kullanılır")
    a = ap.parse_args()
    klipler = [(k, 0) for k in a.klip.split(",")] if a.klip else KLIPLER
    sys.path.insert(0, str(KOK / "tools"))
    import video_derin as vd  # CUDA13 DLL PATH'i pipeline ile aynı kurulur
    from wer_olc import norm, wer
    from faster_whisper import WhisperModel

    model_adi, tip = vd.WHISPER["cuda"]
    model = WhisperModel(model_adi, device="cuda", compute_type=tip)
    modeller, sure = {}, {}
    toplam = {v: {"hata": 0, "kelime": 0, "sinif": {}} for v in VARYANT}
    ornekler = {}
    for kod, bas in klipler:
        wav = TMP / f"{kod}_{bas}.wav"
        if not wav.exists():
            subprocess.run(["ffmpeg", "-y", "-ss", str(bas), "-t", str(a.sure), "-i", str(TMP / f"{kod}.wav"), "-ac", "1", "-ar", "16000", str(wav)],
                           check=True, capture_output=True)
        ref_yol = TMP / f"{kod}_{bas}.ref.txt"
        dil_yol = TMP / f"{kod}_{bas}.dil"
        if not ref_yol.exists():
            dil, metin = groq_ref(wav)
            ref_yol.write_text(metin, encoding="utf-8")
            dil_yol.write_text(dil, encoding="utf-8")
        if dil_yol.exists() and dil_yol.read_text().lower() != "turkish":
            print(f"{kod} atlandi dil={dil_yol.read_text()}", flush=True)
            continue
        ref = norm(ref_yol.read_text(encoding="utf-8"))
        for ad, ek in VARYANT.items():
            ek = dict(ek)
            mad = ek.pop("_model", None)
            if mad and mad not in modeller:
                modeller[mad] = WhisperModel(mad, device="cuda", compute_type=tip)
            m = modeller[mad] if mad else model
            t0 = time.time()
            seg, _ = m.transcribe(str(wav), vad_filter=True, word_timestamps=True, **ek)
            hyp = norm(" ".join(s.text for s in seg))
            sure[ad] = sure.get(ad, 0) + time.time() - t0
            n = len(ref.split())
            w = wer(ref, hyp)
            sayac, ornek = hatalar(ref, hyp)
            t = toplam[ad]
            t["hata"] += w * n
            t["kelime"] += n
            for k, v in sayac.items():
                t["sinif"][k] = t["sinif"].get(k, 0) + v
            if ad == "taban":
                for k, v in ornek.items():
                    ornekler.setdefault(k, []).extend(v[:4])
            print(f"{kod}@{bas} {ad} ref={n} wer={w:.4f}", flush=True)
    ozet = {ad: {"wer_agirlikli": round(t["hata"] / t["kelime"], 4), "kelime": t["kelime"], "sn": round(sure[ad], 1), "sinif": t["sinif"]} for ad, t in toplam.items()}
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps({"ozet": ozet, "taban_ornek": ornekler}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ozet, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
