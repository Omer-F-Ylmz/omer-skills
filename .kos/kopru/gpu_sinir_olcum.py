"""GPU-SINIR-2 kaynakta düşürme ölçümü: large-v3 batched; fp16 b4 (ref) ↔ fp16 b2 ↔ int8_float16 b4/b2. Süre, ort/tepe util, tepe VRAM, 1-WER(ref).
Kullanım: python arka.py .kos/kopru/gpu-sinir-olcum.log .kos/kopru/gpu_sinir_olcum.py <url>"""
import subprocess, sys, tempfile, threading, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_derin  # noqa: E402
from asr_olcum import wer  # noqa: E402
from faster_whisper import BatchedInferencePipeline, WhisperModel  # noqa: E402

ornek = []
dur = threading.Event()


def izle():
    while not dur.is_set():
        r = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, creationflags=0x08000000).stdout.strip().split(",")
        ornek.append((float(r[0]), float(r[1])))
        time.sleep(1)


d = Path(tempfile.mkdtemp(prefix="gs2_"))
v, hata = video_derin.indir(sys.argv[1], d)
if not v:
    sys.exit("indirilemedi " + hata[-150:])
wav = d / "a.wav"
video_derin.kos("ffmpeg", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", wav)
ref = None
for tip, batch in [("float16", 4), ("float16", 2), ("int8_float16", 4), ("int8_float16", 2)]:
    m = WhisperModel("large-v3", device="cuda", compute_type=tip)
    b = BatchedInferencePipeline(m)
    ornek.clear(); dur.clear()
    th = threading.Thread(target=izle, daemon=True); th.start()
    t = time.time()
    seg, _ = b.transcribe(str(wav), batch_size=batch, beam_size=5, vad_filter=True,
                          vad_parameters=video_derin.ASR_VAD, without_timestamps=False)
    metin = " ".join(s.text.strip() for s in seg)
    sure = time.time() - t
    dur.set(); th.join()
    ref = ref or metin
    u = [x[0] for x in ornek] or [0]
    print(f"{tip} b{batch}\tsure={sure:.1f}s\tutil_ort={sum(u)/len(u):.0f}\tutil_tepe={max(u):.0f}\tvram_tepe={max([x[1] for x in ornek] or [0]):.0f}MB\tbenzerlik={1-wer(ref, metin):.3f}", flush=True)
    del b, m
