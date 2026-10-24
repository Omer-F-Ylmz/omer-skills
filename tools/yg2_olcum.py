"""YG2 paralel ölçüm: python yg2_olcum.py <işçi> [video=5] → video/saat, RAM tepe, GPU tepe."""
import subprocess
import sys
import threading
import time
from pathlib import Path

import psutil

es, n = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "5"
kok = Path(__file__).resolve().parents[1]
cikti = kok / f"docs/video-tarama/derin-olcum-{es}-{int(time.time())}"
tepe = {"ram": 0, "gpu": 0, "dur": False}


def ornekle():
    while not tepe["dur"]:
        tepe["ram"] = max(tepe["ram"], psutil.virtual_memory().percent)
        r = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], capture_output=True, text=True, creationflags=0x08000000)
        try:
            tepe["gpu"] = max(tepe["gpu"], int(r.stdout.split()[0]))
        except Exception:
            pass
        time.sleep(2)


th = threading.Thread(target=ornekle, daemon=True)
th.start()
t = time.time()
p = subprocess.run([sys.executable, str(kok / "tools/yeniden_gecis_2.py"), "--cikti", str(cikti), "--es", es, "--en", n],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=0x08000000)
sn = time.time() - t
tepe["dur"] = True
adet = len(list(cikti.glob("*.json"))) if cikti.exists() else 0
print(f"es={es} json={adet}/{n} sure={sn:.0f}s hiz={adet / sn * 3600:.0f}/saat ram_tepe={tepe['ram']:.0f}% gpu_tepe={tepe['gpu']}% rc={p.returncode}")
print((p.stdout or "")[-400:])
