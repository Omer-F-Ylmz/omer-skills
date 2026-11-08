import os
import shutil
import subprocess
from pathlib import Path

home = Path.home()
vk = home / ".local" / "vcpkg"
kok = vk / "installed" / "x64-windows"
subprocess.run([str(vk / "vcpkg.exe"), "install", "portaudio:x64-windows", "fftw3:x64-windows", "libsndfile:x64-windows"],
               cwd=str(vk), capture_output=True)
if (kok / "lib" / "fftw3.lib").exists():
    for ad in ("libfftw3-3.lib", "fftw3f.lib"):
        if not (kok / "lib" / ad).exists():
            shutil.copy2(kok / "lib" / "fftw3.lib", kok / "lib" / ad)
lib = kok / "lib"
for ad in ("portaudio_x64.lib", "libportaudio.lib"):
    if (lib / "portaudio.lib").exists() and not (lib / ad).exists():
        shutil.copy2(lib / "portaudio.lib", lib / ad)
test = home / ".local" / "snd-test"
test.mkdir(parents=True, exist_ok=True)
log = Path(r"C:\Projeler\omer-skills\.kos\kopru\log\sound_tani.out.txt")
env = dict(os.environ)
env["INCLUDE"] = str(kok / "include") + os.pathsep + env.get("INCLUDE", "")
env["LIB"] = str(lib) + os.pathsep + env.get("LIB", "")
env["CL"] = '/I"%s"' % (kok / "include")
env["LINK"] = '/LIBPATH:"%s"' % lib
env["PATH"] = str(kok / "bin") + os.pathsep + env["PATH"]
r = subprocess.run(["npm.cmd", "i", "--prefix", str(test), "--no-audit", "--no-fund", "--foreground-scripts", "soundengine"],
                   capture_output=True, text=True, errors="replace", env=env, timeout=900)
o = r.stdout + r.stderr
satir = [l for l in o.splitlines() if any(k in l for k in ("error", "LNK", "C1083", "fatal", "gyp ERR! not ok", "added"))]
gyp = test / "node_modules" / "soundengine" / "binding.gyp"
import re
inc = set()
for p in (test / "node_modules" / "soundengine").rglob("*.[hc]*"):
    if "node_modules" in p.relative_to(test / "node_modules" / "soundengine").parts or "build" in p.parts:
        continue
    for m in re.findall(r'#include\s*[<"]([^>"]+)[>"]', p.read_text(encoding="utf-8", errors="ignore")):
        inc.add(m)
eksik = sorted(i for i in inc if not (kok / "include" / i).exists() and "/" not in i and not i.startswith(("napi", "node", "std", "v8", "uv")))
yukle = ""
if r.returncode == 0:
    t = subprocess.run(["node", "-e", "const s=require('soundengine');console.log('YUKLENDI',Object.keys(s).slice(0,10).join(','))"],
                       capture_output=True, text=True, errors="replace", env=env, cwd=str(test))
    yukle = t.stdout + t.stderr
log.write_text(("INCLUDE adaylari (vcpkg'de yok): %s\n" % eksik) + "exit %s\n%s\n---yukle---\n%s\n---binding.gyp---\n%s" % (
    r.returncode, "\n".join(satir[:40]), yukle, gyp.read_text(encoding="utf-8", errors="replace") if gyp.exists() else "yok"), encoding="utf-8")
