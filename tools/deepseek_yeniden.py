import subprocess
import sys
import time
from pathlib import Path

ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*deepseek_kur_arka.py*' -or "
      "($_.Name -eq 'curl.exe' -and $_.CommandLine -like '*DeepSeek-V4.1*') } | "
      "ForEach-Object { Stop-Process -Id $_.ProcessId -Force; $_.ProcessId }")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace")
print("kapatilan", r.stdout.split())
time.sleep(3)
betik = Path(__file__).with_name("deepseek_kur_arka.py")
pythonw = Path(sys.executable).with_name("pythonw.exe")
p = subprocess.Popen(
    [str(pythonw if pythonw.exists() else sys.executable), str(betik)],
    creationflags=0x00000008 | 0x00000200 | 0x08000000,
    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True,
)
print("PID", p.pid)
