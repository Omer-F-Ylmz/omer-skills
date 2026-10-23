import glob, os, subprocess, time
r = subprocess.run(["powershell", "-NoProfile", "-Command",
                    "Get-Process claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -notlike '*\\.local\\bin\\*' } | Select-Object -First 3 Id, StartTime, Path | Format-List"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=0x08000000)
print("DESKTOP SURECLERI:\n" + r.stdout.strip()[:800])
for p in glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\*\claude_desktop_config.json*")):
    print(time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p))), os.path.basename(p))
print("ps1:", time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(r"C:\Projeler\omer-skills\onay\desktop_kapat_duzelt.ps1"))))
print("cmd:", open(os.path.expanduser(r"~\Desktop\REA-CodeMode-Duzelt.cmd"), encoding="utf-8").read())
