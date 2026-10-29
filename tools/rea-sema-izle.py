"""REA sürümü değiştiyse rea-sema-tara.py'yi koşar (günlük görev çağırır). Sonuç: .kos/kopru/rea-sema-son.txt
Kullanım: pythonw -I tools/rea-sema-izle.py [--zorla]"""
import json, os, subprocess, sys, time

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAKET = r"C:/Users/pc/AppData/Roaming/npm/node_modules/rea-agents/package.json"
SURUM = os.path.join(KOK, ".kos", "kopru", "rea-surum.txt")
SON = os.path.join(KOK, ".kos", "kopru", "rea-sema-son.txt")

yeni = json.load(open(PAKET, encoding="utf-8"))["version"]
eski = open(SURUM, encoding="utf-8").read().strip() if os.path.exists(SURUM) else ""
if yeni == eski and "--zorla" not in sys.argv:
    sys.exit(0)
r = subprocess.run([sys.executable, "-I", os.path.join(KOK, "tools", "rea-sema-tara.py"), "--profil", "sarmal"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, creationflags=0x08000000)
with open(SON, "w", encoding="utf-8") as f:
    f.write(f"{time.strftime('%Y-%m-%d %H:%M')} rea {eski or '-'} -> {yeni} cikis={r.returncode}\n{r.stdout[-1500:]}{r.stderr[-500:]}")
open(SURUM, "w", encoding="utf-8").write(yeni)
sys.exit(r.returncode)
