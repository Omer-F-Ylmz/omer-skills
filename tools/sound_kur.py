import subprocess
import sys
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
log = kok / ".kos" / "kopru" / "log" / "sound_kur.out.txt"
vk = Path.home() / ".local" / "vcpkg"


def kos(komut, **kw):
    r = subprocess.run(komut, capture_output=True, text=True, errors="replace", **kw)
    with open(log, "a", encoding="utf-8") as f:
        f.write("$ %s\nexit %s\n%s\n" % (" ".join(komut), r.returncode, (r.stdout + r.stderr)[-3000:]))
    return r.returncode


log.write_text("", encoding="utf-8")
if not (vk / "vcpkg.exe").exists():
    if not (vk / ".git").exists():
        kos(["git", "clone", "--depth", "1", "https://github.com/microsoft/vcpkg.git", str(vk)])
    kos(["cmd", "/c", str(vk / "bootstrap-vcpkg.bat"), "-disableMetrics"], cwd=str(vk))
kos([str(vk / "vcpkg.exe"), "install", "portaudio:x64-windows"], cwd=str(vk))
kos([sys.executable, str(kok / "tools" / "kurulum_d2_hata5.py"), "--bolum", "sound"], cwd=str(kok))
with open(log, "a", encoding="utf-8") as f:
    f.write("BITTI\n")
