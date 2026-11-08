"""Docker Desktop'u kapatır ve WSL VM'ini (VmmemWSL) durdurur → RAM geri gelir. STRIX gibi Docker gerektiren iş bitince çağrılır.
Açmak için: tools/docker_ac.py. .wslconfig memory tavanı 2GB."""
import subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
w = Path.home() / ".wslconfig"
t = w.read_text(encoding="utf-8") if w.exists() else ""
if "memory=3GB" in t:
    w.write_text(t.replace("memory=3GB", "memory=2GB"), encoding="utf-8")
    print(".wslconfig memory=2GB")
for ad in ["Docker Desktop.exe", "com.docker.backend.exe", "com.docker.build.exe"]:
    subprocess.run(["taskkill", "/IM", ad, "/F"], capture_output=True)
time.sleep(3)
subprocess.run(["wsl", "--shutdown"], capture_output=True, timeout=60)
time.sleep(5)
o = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Process vmmem* -ErrorAction SilentlyContinue | ForEach-Object { \"$($_.Name) $([int]($_.WorkingSet64/1MB)) MB\" }"], capture_output=True, text=True, errors="replace").stdout.strip()
print("kalan vmmem:", o or "yok")
