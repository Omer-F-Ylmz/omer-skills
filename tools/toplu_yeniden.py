import subprocess
import sys
import time
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*video-toplu-1*' -and $_.CommandLine -notlike '*toplu_yeniden*' } | "
      "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; $_.ProcessId }")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace")
time.sleep(3)
with open(kok / ".kos/kopru/arka/video-toplu-1.log", "a", encoding="utf-8") as f:
    f.write("YENIDEN %s kapatilan %s (GROQ_API_KEY ortama alindi)\n" % (time.strftime("%H:%M:%S"), r.stdout.split()))
r2 = subprocess.run([sys.executable, str(kok / "tools/arka_baslat.py"), str(kok / "tools/toplu_gozetmen.py"),
                     str(kok / ".kos/kopru/arka/video-toplu-1.log"), "python", "tools/video_derin.py", "--es", "3",
                     "--liste", ".kos/kopru/arka/video-toplu-1-kuyruk.txt"], capture_output=True, text=True)
print(r.stdout.split(), r2.stdout)
