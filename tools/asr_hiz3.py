"""DERIN-HIZ-3: ASR yolları kelime benzerliği + süre. Kullanım: asr_hiz3.py <kod> <wav> <yol: seq|bat8|bat16>"""
import difflib, json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import video_derin as vd  # DLL yolları ve ASR ayarları


def kel(t):
    return re.sub(r"[^\w\s]", "", t.lower()).split()


kod, wav, yol = sys.argv[1:4]
eski = json.loads((vd.KOK / "docs/video-tarama/derin" / f"{kod}.json").read_text(encoding="utf-8"))
from faster_whisper import BatchedInferencePipeline, WhisperModel
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
t0 = time.time()
if yol == "seq":
    seg, _ = m.transcribe(wav, word_timestamps=True, vad_filter=True, beam_size=5)
else:
    seg, _ = BatchedInferencePipeline(m).transcribe(wav, word_timestamps=True, vad_filter=True, beam_size=5, batch_size=int(yol.split("_")[0][3:]), without_timestamps=("nt" not in yol), **({"chunk_length":int(yol.split("c")[-1])} if "c" in yol.split("_")[-1] else {}))
metin = " ".join(s.text.strip() for s in seg)
sn = time.time() - t0
a, b = kel(" ".join(s["t"] for s in eski["transkript"])), kel(metin)
print(f"{kod} {yol} sure={sn:.1f}s kelime {len(a)}->{len(b)} benzerlik={difflib.SequenceMatcher(None, a, b, autojunk=False).ratio():.4f}")
