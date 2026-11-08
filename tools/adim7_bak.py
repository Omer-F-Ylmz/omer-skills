import subprocess as s
o = s.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'envanter_tara|katalog_yenile|kurulu_kanit|topla.py|kur_hepsi' -and $_.Name -ne 'powershell.exe' -or ($_.Name -eq 'powershell.exe' -and $_.CommandLine -match 'kur_hepsi') } | % { '{0} {1} {2}dk {3}' -f $_.ProcessId,$_.Name,[int]((Get-Date)-$_.CreationDate).TotalMinutes,(($_.CommandLine -replace '\\s+',' ') -replace '^(.{0,160}).*','$1') }"], capture_output=True, text=True, errors="ignore", timeout=60).stdout
open(r"C:\Projeler\omer-skills\.kos\kopru\log\adim7_bak.log", "w", encoding="utf-8").write(o or "YOK")
print(o or "YOK")
