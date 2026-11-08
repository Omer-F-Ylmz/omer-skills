import glob, os
d = os.path.expandvars(r"%LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe\LocalState\DiagOutputDir")
fs = sorted(glob.glob(d + r"\WinGet-*.log"), key=os.path.getmtime, reverse=True)[:4]
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\winget_log_bak.log", "w", encoding="utf-8")
for f in fs:
    t = open(f, encoding="utf-8", errors="ignore").read().splitlines()
    print("=====", os.path.basename(f), len(t), "satir", file=out)
    for l in t[:3] + t[-25:]: print(l[:220], file=out)
out.close()
