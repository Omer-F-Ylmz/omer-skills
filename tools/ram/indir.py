"""ram-opt-2 dalindaki tools/ram/indir.txt'te listelenen dosyalari C:\\Projeler\\omer-skills altina indirir (dosya araci yokken)."""
import sys, urllib.request
from pathlib import Path
REF = sys.argv[1] if len(sys.argv) > 1 else "ram-opt-2"
TABAN = f"https://raw.githubusercontent.com/Omer-F-Ylmz/omer-skills/{REF}/"
KOK = Path(r"C:\Projeler\omer-skills")
liste = urllib.request.urlopen(TABAN + "tools/ram/indir.txt", timeout=30).read().decode().split()
for y in liste:
    veri = urllib.request.urlopen(TABAN + y, timeout=30).read()
    h = KOK / y
    h.parent.mkdir(parents=True, exist_ok=True)
    h.write_bytes(veri)
    print("indirildi", y, len(veri))
