"""omer-site için vite preview başlat (pencere yok, open yok), strix'i kısa kipte koş, preview'i kendi pid'iyle kapat."""
import subprocess, sys, time
from pathlib import Path

SITE = Path("C:/Users/pc/Desktop/Claude ile yapılanlar/omer-site")
CNW = 0x08000000  # CREATE_NO_WINDOW

p = subprocess.Popen(["npx.cmd", "vite", "preview", "--port", "4173", "--host", "127.0.0.1"], cwd=SITE,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CNW)
try:
    time.sleep(6)
    r = subprocess.run(["strix", "-n", "-m", "quick", "--max-budget", "0.5", "-t", "http://127.0.0.1:4173"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, creationflags=CNW)
    print("strix çıkış", r.returncode)
    print(((r.stdout or "") + (r.stderr or ""))[-1500:])
finally:
    subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, creationflags=CNW)
    print("preview kapandı pid", p.pid)
