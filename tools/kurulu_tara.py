"""Makinede kurulu adlari toplar (PATH, pip, uv tool, npm -g, plugin cache 2 seviye, enabledPlugins)
-> .kos/kopru/ogren/video-izle-kur-1/kurulu-tara.json  {ad: kaynak}. liste_birlestir.py okur."""
import json, os, subprocess, sys
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
OUT = K / ".kos/kopru/ogren/video-izle-kur-1/kurulu-tara.json"
H = Path.home()
EXT = {".exe", ".cmd", ".bat", ".ps1", ""}
ad = {}


def ekle(n, kaynak):
    n = (n or "").strip()
    if n:
        ad.setdefault(n, kaynak)


def kos(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, shell=isinstance(cmd, str)).stdout
    except Exception as e:
        print("dustu:", cmd, e, file=sys.stderr)
        return ""


for d in os.environ.get("PATH", "").split(os.pathsep):
    p = Path(d)
    if p.is_dir() and "windows" not in str(p).lower():
        for f in p.iterdir():
            if f.is_file() and f.suffix.lower() in EXT:
                ekle(f.stem, "PATH:" + d)
for x in json.loads(kos([sys.executable, "-m", "pip", "list", "--format=json"]) or "[]"):
    ekle(x["name"], "pip")
for line in kos("uv tool list").splitlines():
    if line and not line.startswith("-"):
        ekle(line.split()[0], "uv tool")
try:
    for n in json.loads(kos("npm ls -g --depth=0 --json") or "{}").get("dependencies", {}):
        ekle(n.split("/")[-1], "npm -g")
        ekle(n, "npm -g")
except json.JSONDecodeError:
    print("npm json okunamadi", file=sys.stderr)
cache = H / ".claude/plugins/cache"
for m in [m for m in cache.iterdir() if m.is_dir() and not m.name.startswith("temp_")] if cache.exists() else []:
    ekle(m.name, "plugins/cache")
    for p in [p for p in m.iterdir() if p.is_dir()]:
        ekle(p.name, "plugins/cache/" + m.name)
s = json.loads((H / ".claude/settings.json").read_text(encoding="utf-8"))
for k in s.get("enabledPlugins", {}):
    ekle(k.split("@")[0], "enabledPlugins")
for k in s.get("mcpServers", {}):
    ekle(k, "settings mcpServers")
cj = H / ".claude.json"
if cj.exists():
    for k in json.loads(cj.read_text(encoding="utf-8")).get("mcpServers", {}):
        ekle(k, "~/.claude.json mcpServers")
OUT.write_text(json.dumps(ad, ensure_ascii=False, indent=0), encoding="utf-8")
print(len(ad), "ad ->", OUT)
