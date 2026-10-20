"""RUFLO-2 onay betiği — Desktop koşar. ReasoningBank/AgentDB-native için ruflo'nun better-sqlite3 + agentdb yerel modüllerini kurar
(npm 6 paketin install betiğini çalıştırmadı → agentdb_pattern-store 'reasoningBank-unavailable:registry-null').

  python onay/ruflo_2_native.py --kuru   # plan (varsayılan): ne çalışır, hangi dizin yedeklenir
  python onay/ruflo_2_native.py uygula   # yedek → `npm.cmd rebuild better-sqlite3 agentdb --foreground-scripts` (ruflo paket dizininde)
  python onay/ruflo_2_native.py --geri   # build/ dizinlerini yedekten döndürür (yedek yoksa söker → sql.js yedek yoluna düşer)
Yüzey: yalnız ruflo paketinin kendi node_modules'ı; prebuilt indirir (github.com), yoksa node-gyp (MSVC) ister. settings/hook'a dokunmaz.
Sonra: tools/ruflo/saglik.py ile agentdb_pattern-store DEGRADED kalktı mı bak."""
import shutil
import subprocess
import sys
from pathlib import Path

PAKET = Path("C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node_modules/ruflo")
MODULLER = ("better-sqlite3", "agentdb")
YEDEK = Path("C:/Projeler/omer-skills/.kos/ruflo/yedek-native")
KOMUT = ["npm.cmd", "rebuild", *MODULLER, "--foreground-scripts"]


def yedekle():
    for m in MODULLER:
        b = PAKET / "node_modules" / m / "build"
        if b.exists() and not (YEDEK / m).exists():
            shutil.copytree(b, YEDEK / m)


def geri():
    for m in MODULLER:
        b = PAKET / "node_modules" / m / "build"
        shutil.rmtree(b, ignore_errors=True)
        if (YEDEK / m).exists():
            shutil.copytree(YEDEK / m, b)
    print("geri alındı")


if "--geri" in sys.argv:
    geri()
elif "uygula" in sys.argv:
    yedekle()
    sys.exit(subprocess.run(KOMUT, cwd=PAKET, creationflags=0x08000000).returncode)
else:
    for m in MODULLER:
        print(m, "build var" if (PAKET / "node_modules" / m / "build").exists() else "build YOK", "| yedek ->", YEDEK / m)
    print("çalışacak:", " ".join(KOMUT), "| cwd", PAKET)
