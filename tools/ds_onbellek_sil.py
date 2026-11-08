import os
import shutil
from pathlib import Path

h = Path.home()
la = Path(os.environ.get("LOCALAPPDATA", h / "AppData/Local"))
kokler = [h / ".cache", la / "llama.cpp", la / "huggingface", la / "Temp", h / "AppData/Roaming/huggingface",
          la / "Microsoft/WinGet/Packages", la / "Microsoft/WinGet/Cache"]
anahtar = ("abiray", "deepseek-v4.1", "deepseek_v4.1", "deepseek-v4-1", "ggml.llamacpp")
bulunan = []
for k in kokler:
    if not k.exists():
        continue
    for kok, dizinler, dosyalar in os.walk(k):
        for ad in list(dizinler) + dosyalar:
            if any(a in ad.lower() for a in anahtar):
                p = Path(kok) / ad
                bulunan.append(p)
                if ad in dizinler:
                    dizinler.remove(ad)
        if kok.count(os.sep) - str(k).count(os.sep) > 6:
            dizinler[:] = []


def boyut(p):
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


s = []
once = shutil.disk_usage("C:\\").free / 2**30
for p in bulunan:
    try:
        b = boyut(p) / 2**30
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        s.append("SILINDI %.2f GB %s" % (b, p))
    except Exception as e:
        s.append("HATA %s %r" % (p, e))
sonra = shutil.disk_usage("C:\\").free / 2**30
s.append("bos once %.1f sonra %.1f GB (bulunan %d)" % (once, sonra, len(bulunan)))
Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\onbellek_sil.txt").write_text("\n".join(s), encoding="utf-8")
