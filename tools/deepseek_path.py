import subprocess
import time
from pathlib import Path

klasor = str(Path.home() / ".local" / "llama.cpp")
out = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\tani.txt")
ps = (
    "$p=[Environment]::GetEnvironmentVariable('Path','User');"
    "if(($p -split ';') -notcontains '%s'){[Environment]::SetEnvironmentVariable('Path',($p.TrimEnd(';')+';%s'),'User');'EKLENDI'}else{'ZATEN'}"
    % (klasor, klasor)
)
r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace")
s = ["PATH: " + (r.stdout + r.stderr).strip()]
model = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\model")
a = {p.name: p.stat().st_size for p in model.glob("*.gguf")}
time.sleep(30)
b = {p.name: p.stat().st_size for p in model.glob("*.gguf")}
for k in b:
    s.append("%s %.1f GB  hiz %.1f MB/s" % (k, b[k] / 2**30, (b[k] - a.get(k, 0)) / 30 / 2**20))
out.write_text("\n".join(s), encoding="utf-8")
