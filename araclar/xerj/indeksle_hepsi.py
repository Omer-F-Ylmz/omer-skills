"""Klasör klasör indeksler (tam kökte os error 33 abort eder): python .kos/kopru/arka.py --bagimsiz araclar/xerj/indeks.log araclar/xerj/indeksle_hepsi.py
Her satır: önek | klasör | xerj-done/error özeti. TimeoutExpired yakalanır: klasör loglanır, alt klasörlere bölünüp yeniden denenir.
skills/ zaten indekslendi (os-skills). Atlanan ağır klasörler HARIC (laya 15 GB, code-mode, video, dist...)."""
import os, re, subprocess, sys
kok = os.path.dirname(os.path.abspath(__file__))
exe = os.path.join(kok, "bin", "xerj-1.0.0-rc.98-x86_64-pc-windows-msvc", "xerj.exe")
env = dict(os.environ, XERJ_DISABLE_FEEDBACK="true")
repo = os.path.dirname(os.path.dirname(kok))
HARIC = {"node_modules", "laya", "code-mode", "bin", "obj", "graphify-out", ".git", "dist", "videolar", "video", "__pycache__", "veri", "indir", ".claude"}
TAVAN = 600

def indeksle(onek, kl, bol=True):
    try:
        r = subprocess.run([exe, "autoindex", kl, "--prefix", onek, "--yes"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=0x08000000, timeout=TAVAN)
    except subprocess.TimeoutExpired:
        print(onek, "|", kl, "| ZAMAN-ASIMI", flush=True)
        if bol:
            for d in sorted(os.listdir(kl)):
                if d not in HARIC and os.path.isdir(os.path.join(kl, d)):
                    indeksle(onek + "-" + re.sub(r"\W+", "-", d), os.path.join(kl, d), False)
        return
    son = [s for s in (r.stdout + r.stderr).splitlines() if s.startswith(("xerj-done", "error"))]
    print(onek, "|", kl, "|", " ".join(son) or f"rc={r.returncode}", flush=True)

def alt(onek, kl):
    for d in sorted(os.listdir(kl)):
        if d not in HARIC and os.path.isdir(os.path.join(kl, d)):
            yield onek + "-" + re.sub(r"\W+", "-", d), os.path.join(kl, d)

hedef = []
for d in ("docs", "rapor", "mcp", "templates", "tests"):
    hedef.append(("os-" + d, os.path.join(repo, d)))
hedef += alt("os-tools", os.path.join(repo, "tools"))
masa = os.path.expanduser(r"~\Desktop\Claude ile yapılanlar")
if os.path.isdir(masa):
    hedef += alt("cy", masa)
for onek, kl in hedef:
    if sys.argv[1:] and onek not in sys.argv[1:]:
        continue  # yalniz verilen onekler (basarisizlari yeniden dene)
    if not os.path.isdir(kl):
        print(onek, "yok", flush=True); continue
    indeksle(onek, kl)
