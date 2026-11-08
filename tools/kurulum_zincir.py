"""KURULUM-TOPLU-1 zinciri: önceki coz denemesi bitene kadar bekle, sonra tam coz, sonra indir (kaldığı yerden; yeniden başlatılabilir)."""
import os, subprocess, sys, time
T = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
LOG = r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-oto\out\kurulum_coz2.py.arka.log"
for _ in range(240):
    try:
        if "BITTI-COZ" in open(LOG, encoding="utf-8", errors="replace").read():
            break
    except OSError:
        pass
    time.sleep(15)
subprocess.run([PY, os.path.join(T, "kurulum_coz2.py"), "coz"])
subprocess.run([PY, os.path.join(T, "kurulum_coz2.py"), "indir"])
subprocess.run([PY, os.path.join(T, "kurulum_coz2.py"), "say"])
print("ZINCIR-BITTI", flush=True)
