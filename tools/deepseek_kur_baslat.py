import subprocess
import sys
from pathlib import Path

betik = Path(__file__).with_name("deepseek_kur_arka.py")
pythonw = Path(sys.executable).with_name("pythonw.exe")
exe = str(pythonw if pythonw.exists() else sys.executable)
bayrak = 0x00000008 | 0x00000200 | 0x08000000
p = subprocess.Popen(
    [exe, str(betik)],
    creationflags=bayrak,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    close_fds=True,
)
print("PID", p.pid)
