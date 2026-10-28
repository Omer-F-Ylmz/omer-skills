"""DERIN-HIZ-3: ASR yolları kelime benzerliği + süre + VRAM. Kullanım: asr_hiz3.py <kod> <wav> <ct> <batch|0> [json-kwargs]
ct: float16|int8_float16; batch 0 = sıralı. Örn: asr_hiz3.py 2x-aQy730Ew a.wav int8_float16 8 '{"vad_parameters":{"min_silence_duration_ms":500}}'"""
import difflib, json, re, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import video_derin as vd  # DLL yolları


def kel(t):
    return re.sub(r"[^\w\s]", "", t.lower()).split()


kod, wav, ct, batch = sys.argv[1:5]
kw = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
eski = json.loads((vd.KOK / "docs/video-tarama/derin" / f"{kod}.json").read_text(encoding="utf-8"))
from faster_whisper import BatchedInferencePipeline, WhisperModel
m = WhisperModel("large-v3", device="cuda", compute_type=ct)
t0 = time.time()
if batch == "0":
    seg, _ = m.transcribe(wav, word_timestamps=True, vad_filter=True, beam_size=5, **kw)
else:
    kw.setdefault("without_timestamps", False)
    seg, _ = BatchedInferencePipeline(m).transcribe(wav, word_timestamps=True, vad_filter=True, beam_size=5, batch_size=int(batch), **kw)
metin = " ".join(s.text.strip() for s in seg)
sn = time.time() - t0
import os
if os.environ.get("ASR_OUT"):
    Path(os.environ["ASR_OUT"]).write_text(metin, encoding="utf-8")
vram = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
a, b = kel(" ".join(s["t"] for s in eski["transkript"])), kel(metin)
print(f"{kod} {ct} b={batch} {kw} sure={sn:.1f}s vram={vram} kelime {len(a)}->{len(b)} benzerlik={difflib.SequenceMatcher(None, a, b, autojunk=False).ratio():.4f}")
