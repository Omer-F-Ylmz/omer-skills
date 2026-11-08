"""LINK-27 kurulum 1. parti (temiz repolar): agency-agents -> ~/.claude/agents-katalog (ajan-getir), rederive -> CC plugin, agent-floor -> npm -g, ScrapeGraph -> kendi venv'i."""
import json, shutil, subprocess, sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"C:\Projeler\omer-skills")
L = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27")
EV = Path.home() / ".claude"
CLAUDE = str(Path.home() / ".local/bin/claude.exe")


def kos(ad, kmt, cwd=None, t=900):
    try:
        r = subprocess.run(kmt, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd, timeout=t)
        print(f"[{ad}] rc={r.returncode} {(r.stdout + r.stderr).strip()[-400:]}")
        return r.returncode
    except Exception as e:
        print(f"[{ad}] HATA {e}")
        return -1


aa = L / "msitarzewski__agency-agents"
hedef = EV / "agents-katalog"
hedef.mkdir(exist_ok=True)
divs = [d["id"] if isinstance(d, dict) and "id" in d else d for d in []]
atla = {"examples", "scripts", "integrations", ".github", ".git"}
n = m = 0
for f in aa.rglob("*.md"):
    rel = f.relative_to(aa)
    if len(rel.parts) < 2 or rel.parts[0] in atla or f.name.upper().startswith(("README", "CONTRIBUTING")):
        continue
    if not re.match(r"---\r?\n.*?\bname:", f.read_text(encoding="utf-8", errors="replace")[:600], re.S):
        continue
    ad = "agency-" + "-".join(p.lower() for p in rel.with_suffix("").parts)
    d = hedef / f"{ad}.md"
    if d.exists():
        m += 1
        continue
    shutil.copy2(f, d)
    n += 1
print(f"[agency-agents] {n} ajan kopyalandı, {m} zaten vardı -> {hedef}")
kos("ajan-katalog", [sys.executable, "-E", str(R / "tools/ajan_katalog.py")], cwd=str(R))

rd = L / "EricJujianZou__rederive"
kos("rederive-mp", [CLAUDE, "plugin", "marketplace", "add", str(rd)])
kos("rederive-kur", [CLAUDE, "plugin", "install", "rederive@rederive"])

kos("agent-floor", ["npm.cmd", "i", "-g", "agent-floor"])

sg = L / "ScrapeGraphAI__Scrapegraph-ai"
uv = shutil.which("uv")
if uv:
    kos("scrapegraph-venv", [uv, "venv", str(sg / ".venv"), "--python", "3.12"], cwd=str(sg))
    kos("scrapegraph-kur", [uv, "pip", "install", "--python", str(sg / ".venv/Scripts/python.exe"), "scrapegraphai"], cwd=str(sg), t=1500)
else:
    print("[scrapegraph] uv yok")
print("BITIS")
