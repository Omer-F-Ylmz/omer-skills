"""clodfarm'ı durdurur, Docker'ı kapatır, WSL belleğini Windows'a geri verir."""
import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CLI = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
CF = r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27\matank001__clodfarm"
subprocess.run([CLI, "compose", "stop"], cwd=CF, timeout=120)
subprocess.run(["taskkill", "/IM", "Docker Desktop.exe", "/F"], capture_output=True)
subprocess.run(["wsl.exe", "--shutdown"], timeout=60)
print("clodfarm durdu, WSL kapandı")
