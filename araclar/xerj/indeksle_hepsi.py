"""Alt klasör alt klasör indeksler (tam kökte os error 33 abort eder): python .kos/kopru/arka.py --bagimsiz araclar/xerj/indeks.log araclar/xerj/indeksle_hepsi.py
Her satır: önek | klasör | xerj-done/error özeti. skills/ zaten indekslendi (os-skills)."""
import os, subprocess, sys
kok = os.path.dirname(os.path.abspath(__file__))
exe = os.path.join(kok, "bin", "xerj-1.0.0-rc.98-x86_64-pc-windows-msvc", "xerj.exe")
env = dict(os.environ, XERJ_DISABLE_FEEDBACK="true")
repo = os.path.dirname(os.path.dirname(kok))
hedef = [("os-" + d, os.path.join(repo, d)) for d in ("tools", "docs", "rapor", "mcp", "templates", "tests")]
hedef.append(("claude-ile-yapilanlar", os.path.expanduser(r"~\Desktop\Claude ile yapılanlar")))
for onek, kl in hedef:
    if not os.path.isdir(kl):
        print(onek, "yok", flush=True); continue
    r = subprocess.run([exe, "autoindex", kl, "--prefix", onek, "--yes"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=0x08000000, timeout=1500)
    son = [s for s in (r.stdout + r.stderr).splitlines() if s.startswith(("xerj-done", "error"))]
    print(onek, "|", kl, "|", " ".join(son) or f"rc={r.returncode}", flush=True)
