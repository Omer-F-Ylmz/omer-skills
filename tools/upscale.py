"""Yerel AI upscale (Upscayl 2.15.0, AGPL-3.0; yalnız harici süreç olarak çağrılır): python tools/upscale.py <girdi> <çıktı> [model] [ölçek]
Model varsayılanı digital-art-4x (illüstrasyon/afiş); fotoğraf için high-fidelity-4x. Sonuna keskinlik (Laplacian varyansı) önce/sonra basar."""
import os, subprocess, sys

APP = r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link30eki\upscayl\app\resources"


def upscale(girdi, cikti, model="digital-art-4x", olcek=4):
    r = subprocess.run([os.path.join(APP, "bin", "upscayl-bin.exe"), "-i", girdi, "-o", cikti, "-m", os.path.join(APP, "models"),
                        "-n", model, "-s", str(olcek)], capture_output=True, text=True, errors="replace",
                       creationflags=0x08000000, env=dict(os.environ), timeout=600)
    if r.returncode or not os.path.isfile(cikti):
        sys.exit(f"upscayl rc {r.returncode}: {r.stderr[-300:]}")
    return cikti


def keskinlik(yol):
    from PIL import Image, ImageFilter, ImageStat
    g = Image.open(yol).convert("L")
    return round(ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).var[0], 1), g.size


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    upscale(a[0], a[1], *(a[2:3] or ["digital-art-4x"]), *([int(a[3])] if len(a) > 3 else []))
    print("önce", keskinlik(a[0]), "sonra", keskinlik(a[1]))
