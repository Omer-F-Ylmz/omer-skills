import glob
import shutil
import subprocess
from pathlib import Path

s = ["C bos GB: %.0f" % (shutil.disk_usage("C:\\").free / 2**30)]
for d in ("D:\\", "E:\\", "F:\\"):
    try:
        s.append("%s bos GB: %.0f / %.0f" % (d, shutil.disk_usage(d).free / 2**30, shutil.disk_usage(d).total / 2**30))
    except OSError:
        pass
desen = {
    "UnityHub": [r"C:\Program Files\Unity Hub\Unity Hub.exe"],
    "UnityEditor": [r"C:\Program Files\Unity\Hub\Editor\*\Editor\Unity.exe", r"C:\Program Files\Unity*\Editor\Unity.exe"],
    "EpicLauncher": [r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
                     r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"],
    "UnrealEditor": [r"C:\Program Files\Epic Games\UE_*\Engine\Binaries\Win64\UnrealEditor.exe", r"D:\Epic Games\UE_*\Engine\Binaries\Win64\UnrealEditor.exe"],
}
for ad, dl in desen.items():
    bul = [p for d in dl for p in glob.glob(d)]
    s.append("%s: %s" % (ad, bul or "YOK"))
r = subprocess.run(["winget", "search", "--source", "winget", "Unity Hub", "--accept-source-agreements", "--disable-interactivity"],
                   capture_output=True, text=True, errors="replace", timeout=90)
s.append("winget UnityHub: " + " | ".join(l for l in r.stdout.splitlines() if "Unity" in l)[:400])
r = subprocess.run(["winget", "search", "--source", "winget", "EpicGames.EpicGamesLauncher", "--accept-source-agreements", "--disable-interactivity"],
                   capture_output=True, text=True, errors="replace", timeout=90)
s.append("winget Epic: " + " | ".join(l for l in r.stdout.splitlines() if "Epic" in l)[:400])
Path(r"C:\Projeler\omer-skills\.kos\kopru\log\motor_bak.out.txt").write_text("\n".join(s), encoding="utf-8")
