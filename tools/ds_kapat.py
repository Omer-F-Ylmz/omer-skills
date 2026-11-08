import subprocess
from pathlib import Path

ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*ds_test.py*' -or $_.Name -eq 'llama-server.exe' -or "
      "($_.Name -eq 'claude.exe' -and $_.CommandLine -like '*ds-ayar.json*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; $_.Name };"
      "$c=Get-CimInstance Win32_ComputerSystem; $o=Get-CimInstance Win32_OperatingSystem;"
      "'RAM toplam GB ' + [math]::Round($c.TotalPhysicalMemory/1GB) + ' bos GB ' + [math]::Round($o.FreePhysicalMemory/1MB,1);"
      "(Get-CimInstance Win32_DiskDrive | Select-Object -First 3 | ForEach-Object { $_.Model + ' ' + [math]::Round($_.Size/1GB) }) -join ' | '")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", timeout=55)
Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\ds_kapat.txt").write_text(r.stdout + r.stderr, encoding="utf-8")
