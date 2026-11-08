import subprocess as s, time
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\defender_bak.log", "w", encoding="utf-8", buffering=1)
c = ("Get-WinEvent -LogName 'Microsoft-Windows-Windows Defender/Operational' -MaxEvents 60 -ErrorAction SilentlyContinue | "
     "? { $_.Id -in 1116,1117,1118,1119 -and $_.TimeCreated -gt (Get-Date).AddHours(-3) } | "
     "% { $m=$_.Message -replace '\\s+',' '; '{0} {1} {2}' -f $_.TimeCreated.ToString('HH:mm'),$_.Id,($m -replace '^(.{0,420}).*','$1') }")
p = s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=90)
print(p.stdout.strip()[:6000] or ("BOS " + p.stderr[:500]), file=LOG)
print("BITTI", file=LOG)
