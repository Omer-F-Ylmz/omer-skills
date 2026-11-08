"""clodfarm'ı az RAM'le açar: .wslconfig (2GB, dropcache, sparse), Docker, imaj çek, compose up. Kapatma: tools/clodfarm_kapat.py."""
import subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
CLI = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
CF = r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27\matank001__clodfarm"
wsl = Path.home() / ".wslconfig"
wsl.write_text("[wsl2]\nmemory=2GB\nprocessors=4\nswap=2GB\n\n[experimental]\nautoMemoryReclaim=dropcache\nsparseVhd=true\n", encoding="utf-8")
print("wslconfig yazıldı")


def kos(ad, k, t=1200):
    r = subprocess.run(k, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=CF, timeout=t)
    print(f"[{ad}] rc={r.returncode} {(r.stdout + r.stderr).strip()[-300:]}")
    return r.returncode


if subprocess.run([CLI, "version", "--format", "{{.Server.Version}}"], capture_output=True, timeout=30).returncode != 0:
    subprocess.run(["wsl.exe", "--shutdown"], timeout=60)
    subprocess.Popen([r"C:\Program Files\Docker\Docker\Docker Desktop.exe"], creationflags=0x00000008 | 0x00000200)
    for _ in range(16):
        time.sleep(15)
        if subprocess.run([CLI, "version"], capture_output=True, timeout=30).returncode == 0:
            break
print("docker hazır" if subprocess.run([CLI, "version"], capture_output=True, timeout=30).returncode == 0 else "docker AÇILMADI")
if kos("pull", [CLI, "compose", "pull"]) != 0:
    kos("build", [CLI, "compose", "build"], t=2400)
kos("up", [CLI, "compose", "up", "-d"])
time.sleep(20)
kos("durum", [CLI, "stats", "--no-stream", "--format", "{{.Name}} {{.MemUsage}} {{.CPUPerc}}"])
print("BITIS")
