import json
import os
import shutil
import subprocess
from pathlib import Path

out = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\tani.txt")
s = []
r = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, errors="replace")
for l in r.stdout.splitlines():
    if any(k in l.lower() for k in ("winget", "appinstaller", "msiexec", "llama", "pythonw", "consent")):
        s.append(l)
s.append("which llama-server: %s" % shutil.which("llama-server"))
la = Path(os.environ["LOCALAPPDATA"])
s.append("links: %s" % list((la / "Microsoft" / "WinGet" / "Links").glob("llama*")))
s.append("pkgs: %s" % [p.name for p in (la / "Microsoft" / "WinGet" / "Packages").glob("*lama*")])
s.append("free GB: %.0f" % (shutil.disk_usage("C:\\").free / 2**30))
out.write_text("\n".join(s), encoding="utf-8")
