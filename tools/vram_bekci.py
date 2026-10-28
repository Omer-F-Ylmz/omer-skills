"""VRAM bekçisi: nvidia-smi ile GPU bellek doluluğunu ölçer. ≥%80 iken .kos/kopru/vram-dolu kilidi oluşur, altında kilit kalkar.
Yeni GPU işi vram_bekle() ile kilit kalkana dek bekler. Ölçüm: mem_bekci her turda bir kez; sürekli: python vram_bekci.py dongu (30 sn)."""
import os
import subprocess
import sys
import time

KOK = r"C:\Projeler\omer-skills"
KILIT = os.path.join(KOK, ".kos", "kopru", "vram-dolu")
ESIK = 80.0


def yuzde_olc():
    r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
                       capture_output=True, text=True, timeout=20, creationflags=0x08000000)
    kullanilan, toplam = (float(x) for x in r.stdout.strip().splitlines()[0].split(","))
    return 100.0 * kullanilan / toplam


def kilit_guncelle(yuzde, kilit=KILIT):
    if yuzde >= ESIK:
        with open(kilit, "w", encoding="utf-8") as f:
            f.write("%.1f\n" % yuzde)
    elif os.path.exists(kilit):
        os.remove(kilit)


def vram_bekle(zaman_asimi=3600, kilit=KILIT):
    """VRAM doluyken GPU işini bekletir; zaman aşımında kilide rağmen devam eder (kilit bayat olabilir)."""
    son = time.time() + zaman_asimi
    while os.path.exists(kilit) and time.time() < son:
        time.sleep(30)


def dusuk_oncelik():
    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)


if __name__ == "__main__":
    if sys.argv[1:] == ["dongu"]:
        while True:
            kilit_guncelle(yuzde_olc())
            time.sleep(30)
    else:
        kilit_guncelle(yuzde_olc())
