"""LINK-27 kurulum 2. parti: ajan katalogu yenile, agent-floor yerel klondan derle + global kur."""
import os, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"C:\Projeler\omer-skills")
L = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")


def kos(ad, kmt, cwd=None, t=900):
    try:
        r = subprocess.run(kmt, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd, timeout=t, env=ENV)
        print(f"[{ad}] rc={r.returncode} {(r.stdout + r.stderr).strip()[-400:]}")
        return r.returncode
    except Exception as e:
        print(f"[{ad}] HATA {e}")
        return -1


kos("ajan-katalog", [sys.executable, str(R / "tools/ajan_katalog.py")], cwd=str(R))
af = str(L / "develop212__agent-floor")
if kos("agent-floor-ci", ["npm.cmd", "ci"], cwd=af, t=1200) == 0 and kos("agent-floor-build", ["npm.cmd", "run", "build"], cwd=af) == 0:
    kos("agent-floor-test", ["npm.cmd", "test"], cwd=af)
    kos("agent-floor-g", ["npm.cmd", "i", "-g", "."], cwd=af)
    kos("agent-floor-ver", ["agent-floor.cmd", "--help"], cwd=af, t=60)
print("BITIS")
