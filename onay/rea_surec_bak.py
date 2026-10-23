"""Calisan REA sureclerinin komut satiri (yalniz 'rea' gecen node surecleri; dosya adlari) + baslama saati."""
import subprocess
ps = ("Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object { $_.CommandLine -match 'rea' } | "
      "ForEach-Object { $k = (($_.CommandLine -split ' ') | ForEach-Object { Split-Path $_.Trim([char]34) -Leaf }) -join ' '; '{0} | {1} | {2}' -f $_.ProcessId, $_.CreationDate.ToString('HH:mm:ss'), $k }")
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=0x08000000)
print(r.stdout.strip()[:1500] or "rea sureci yok", r.stderr.strip()[:300])
