import subprocess, sys
from pathlib import Path
betik = Path(sys.argv[1])
cikti = Path(r"C:\Projeler\omer-skills\.kos\kopru\log") / (betik.stem + ".out.txt")
f = open(cikti, "w", encoding="utf-8")
subprocess.Popen([r"C:\Users\pc\AppData\Local\Programs\Python\Python312\python.exe", str(betik)] + sys.argv[2:],
                 stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                 creationflags=0x08000000 | 0x00000008 | 0x00000200)
print("arka:", cikti)
