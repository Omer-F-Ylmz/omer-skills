"""VIDEO-HIZ-7: tab = yerel large-v3 beam5 (sıralı, video_derin sıralı yolu ile aynı ayar) aynı sesten. Kullanım: hiz7_yerel.py <video_id>..."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_derin  # noqa: F401  (cuBLAS/cuDNN DLL yolunu ekler)
from faster_whisper import WhisperModel

D = Path(__file__).resolve().parents[1] / ".kos/kopru/ogren/hiz7"
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
for vid in sys.argv[1:]:
    cik = D / vid / "yerel_seq.json"
    if cik.exists():
        continue
    sg, inf = m.transcribe(str(D / vid / "a.wav"), beam_size=5, word_timestamps=True, vad_filter=True)
    seg = [{"b": round(s.start, 1), "s": round(s.end, 1), "t": s.text.strip()} for s in sg]
    cik.write_text(json.dumps({"dil": inf.language, "segments": seg}, ensure_ascii=False), encoding="utf-8")
    print(vid, inf.language, len(seg), flush=True)
