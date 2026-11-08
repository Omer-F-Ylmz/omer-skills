import subprocess
from pathlib import Path

ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*motor_kur.py*' -or "
      "($_.Name -like 'Unity Hub*' -and $_.CommandLine -like '*headless*') -or $_.Name -like 'UnityDownload*' } | "
      "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; \"$($_.ProcessId) $($_.Name)\" }")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace")
import glob, shutil
s = "kapatilan: %s | editor klasoru: %s | bos GB %.0f" % (
    r.stdout.strip().replace("\n", ", ") or "yok", glob.glob(r"C:\Program Files\Unity\Hub\Editor\*"), shutil.disk_usage("C:\\").free / 2**30)
Path(r"C:\Projeler\omer-skills\.kos\kopru\log\motor_durdur.out.txt").write_text(s, encoding="utf-8")
