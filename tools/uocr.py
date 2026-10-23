"""Baidu Unlimited-OCR sarmalayıcı: python tools/uocr.py [--cok] [--dpi 200] [--cikti dosya.md] girdi...
Görsel → her biri ayrı infer (varsayılan), --cok → tüm görseller tek infer_multi; PDF → infer_multi. Çıktı Markdown (stdout ya da --cikti).
Model çağrıda yüklenir, bitince GPU bırakılır (servis yok). Ortam: C:\\AI\\unlimited-ocr\\.venv (kurulum: docs/kurulumlar/unlimited-ocr.md).
Süre + tepe VRAM stderr'e `uocr: {...}` olarak yazılır."""
import argparse, json, os, subprocess, sys, tempfile, time

KOK = r"C:\AI\unlimited-ocr"
VENV_PY = os.path.join(KOK, ".venv", "Scripts", "python.exe")
MODEL = os.path.join(KOK, "model")


def pdf_gorsel(pdf, dpi, dizin):
    import fitz
    yollar = []
    for i, s in enumerate(fitz.open(pdf)):
        y = os.path.join(dizin, f"{os.path.basename(pdf)}_{i:04d}.png")
        s.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72)).save(y)
        yollar.append(y)
    return yollar


def calis(a):
    import torch
    from transformers import AutoModel, AutoTokenizer
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    m = AutoModel.from_pretrained(MODEL, trust_remote_code=True, use_safetensors=True, torch_dtype=torch.bfloat16).eval().cuda()
    yukle = time.time() - t0
    torch.cuda.reset_peak_memory_stats()
    parcalar = []
    t1 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        def oku(cikti):
            return open(os.path.join(cikti, "result.md"), encoding="utf-8").read()

        def tek(yol):
            c = tempfile.mkdtemp(dir=tmp)
            m.infer(tok, prompt="<image>document parsing.", image_file=yol, output_path=c, base_size=1024, image_size=640,
                    crop_mode=True, max_length=32768, no_repeat_ngram_size=35, ngram_window=128, save_results=True)
            return oku(c)

        def cok(yollar):
            c = tempfile.mkdtemp(dir=tmp)
            m.infer_multi(tok, prompt="<image>Multi page parsing.", image_files=yollar, output_path=c, image_size=1024,
                          max_length=32768, no_repeat_ngram_size=35, ngram_window=1024, save_results=True)
            return oku(c)

        gorseller = []
        for g in a.girdi:
            if g.lower().endswith(".pdf"):
                parcalar.append(cok(pdf_gorsel(g, a.dpi, tmp)))
            else:
                gorseller.append(g)
        if gorseller and a.cok:
            parcalar.append(cok(gorseller))
        else:
            for g in gorseller:
                parcalar.append(f"## {os.path.basename(g)}\n\n" + tek(g))
    ist = {"yukle_s": round(yukle, 1), "infer_s": round(time.time() - t1, 1), "tepe_vram_mb": round(torch.cuda.max_memory_allocated() / 2**20)}
    print("uocr: " + json.dumps(ist), file=sys.stderr)
    return "\n\n".join(parcalar)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("girdi", nargs="+")
    ap.add_argument("--cok", action="store_true")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--cikti")
    a = ap.parse_args()
    if os.path.normcase(sys.executable) != os.path.normcase(VENV_PY):
        r = subprocess.run([VENV_PY, os.path.abspath(__file__), *sys.argv[1:]], stdout=sys.stdout, stderr=sys.stderr, creationflags=0x08000000)
        sys.exit(r.returncode)
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    ayri = sys.stdout
    sys.stdout = sys.stderr  # model infer metin basar; yalnız sonuç stdout'a gider
    md = calis(a)
    sys.stdout = ayri
    if a.cikti:
        open(a.cikti, "w", encoding="utf-8").write(md)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(md)


if __name__ == "__main__":
    main()
