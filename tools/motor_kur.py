import glob
import re
import shutil
import subprocess
import time
from pathlib import Path

log = Path(r"C:\Projeler\omer-skills\.kos\kopru\log\motor_kur.out.txt")
HUB = Path(r"C:\Program Files\Unity Hub\Unity Hub.exe")


def yaz(m):
    with open(log, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + m + "\n")


def kos(k, t=3600):
    r = subprocess.run(k, capture_output=True, text=True, errors="replace", timeout=t)
    yaz("$ %s -> %s | %s" % (" ".join(k)[:200], r.returncode, (r.stdout + r.stderr)[-1500:].replace("\n", " / ")))
    return r


log.write_text("", encoding="utf-8")
yaz("bos GB %.0f" % (shutil.disk_usage("C:\\").free / 2**30))
yaz("mevcut UnityEditor %s" % glob.glob(r"C:\Program Files\Unity\Hub\Editor\*"))
yaz("mevcut UE %s" % glob.glob(r"C:\Program Files\Epic Games\UE_*"))
w = ["winget", "install", "-e", "--silent", "--accept-source-agreements", "--accept-package-agreements", "--disable-interactivity", "--id"]
if not HUB.exists():
    kos(w + ["Unity.UnityHub"], 1800)
if not glob.glob(r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe"):
    kos(w + ["EpicGames.EpicGamesLauncher"], 1800)
if HUB.exists():
    r = kos([str(HUB), "--", "--headless", "editors", "--releases"], 600)
    surumler = re.findall(r"(\d{4}\.\d+\.\d+f\d+)", r.stdout + r.stderr)
    yaz("hub surumler %s" % sorted(set(surumler))[-10:])
    def anahtar(v):
        return [int(x) for x in re.findall(r"\d+", v)]
    if surumler:
        en = max(set(surumler), key=anahtar)
        yaz("SECILEN %s" % en)
        kos([str(HUB), "--", "--headless", "install", "--version", en, "--architecture", "x86_64"], 7200)
        kos([str(HUB), "--", "--headless", "editors", "--installed"], 300)
else:
    yaz("HATA Unity Hub kurulamadi")
yaz("bos GB %.0f" % (shutil.disk_usage("C:\\").free / 2**30))
yaz("BITTI")
