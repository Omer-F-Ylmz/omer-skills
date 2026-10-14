"""ENVANTER-KULLAN-1: aynı kare üstünde Tesseract tur / RapidOCR / qwen3.5:4b (ollama yerel VLM) — süre + çıktı."""
import base64, json, subprocess, sys, time, urllib.request
from pathlib import Path

KARE = Path(sys.argv[1])
OUT = Path(__file__).with_name("deneme_gorsel.txt")
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = r"C:\Projeler\.tmp-video\tessdata"
VENV_PY = r"C:\Projeler\omer-skills\tools\video\.venv\Scripts\python.exe"
sonuc = [f"kare: {KARE}"]


def olc(ad, f):
    t = time.time()
    try:
        s = f()
    except Exception as e:
        s = f"HATA {type(e).__name__}: {e}"[:300]
    sonuc.append(f"## {ad} ({time.time() - t:.1f}s)\n{s.strip()[:1200]}")


olc("tesseract tur+eng", lambda: subprocess.run([TESS, str(KARE), "-", "--tessdata-dir", TESSDATA, "-l", "tur+eng"],
                                                 capture_output=True, text=True, encoding="utf-8", errors="replace").stdout)
olc("rapidocr (venv, onnx)", lambda: subprocess.run(
    [VENV_PY, "-c", "import sys;from rapidocr import RapidOCR;r=RapidOCR()(sys.argv[1]);print('\\n'.join(r.txts or []))", str(KARE)],
    capture_output=True, text=True, encoding="utf-8", errors="replace").stdout)


def vlm():
    govde = {"model": "qwen3.5:4b", "stream": False, "think": False, "keep_alive": "0",
             "messages": [{"role": "user", "content": "List every software tool, product or website name visible in this image, one per line. Nothing else.",
                           "images": [base64.b64encode(KARE.read_bytes()).decode()]}]}
    r = urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/chat", json.dumps(govde).encode(),
                                                      {"Content-Type": "application/json"}), timeout=300)
    d = json.loads(r.read())
    return d["message"]["content"] + f"\n[eval_count={d.get('eval_count')} load={d.get('load_duration', 0) / 1e9:.1f}s]"


olc("ollama qwen3.5:4b (yerel VLM, keep_alive=0)", vlm)
OUT.write_text("\n".join(sonuc) + "\n", encoding="utf-8")
print(OUT)
