"""Docker Desktop'u açar ve motor hazır olana dek bekler (≤3 dk). İş bitince tools/docker_kapat.py."""
import subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
cli = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
subprocess.Popen([r"C:\Program Files\Docker\Docker\Docker Desktop.exe"], creationflags=0x00000008 | 0x00000200)
for _ in range(12):
    time.sleep(15)
    p = subprocess.run([cli, "version", "--format", "{{.Server.Version}}"], capture_output=True, text=True, errors="replace", timeout=30)
    if p.returncode == 0:
        print("docker hazır", p.stdout.strip()); break
else:
    print("docker açılmadı")
