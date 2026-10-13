"""LAYA-1 d2 hattı (ortak sıradan tek iş; torch işleri sıralı, aynı anda 1): kör Opus puan → veri → ince ayar (bas2/tam2) → puanla → rapor.
python olcum_sira.py hat.py   · çıktı rapor-d2.txt"""
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).parent
PY = "C:/Projeler/.laya-venv/Scripts/python.exe"
env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
env.update(HF_HUB_OFFLINE="1", PYTHONIOENCODING="utf-8")


def kos(*a):
    print(">>", *a, flush=True)
    r = subprocess.run(list(a), cwd=D, env=env, creationflags=0x08000000)
    if r.returncode:
        sys.exit(f"rc {r.returncode}: {a}")


adim = sys.argv[1:] or ["kor", "veri", "egit", "puanla", "rapor"]
if "kor" in adim:
    kos(sys.executable, "kor.py")
if "veri" in adim:
    kos(sys.executable, "olc.py", "veri")
if "egit" in adim:
    kos(PY, "egit.py", "2")
if "puanla" in adim:
    kos(sys.executable, "olc.py", "puanla", "laya0d2")
    for k in ("bas2", "tam2"):
        kos(sys.executable, "olc.py", "puanla", f"laya-{k}", str(D / f"ck-{k}"))
if "rapor" in adim:
    with open(D / "rapor-d2.txt", "w", encoding="utf-8") as f:
        subprocess.run([sys.executable, "olc.py", "rapor", "laya0d2", "laya-bas2", "laya-tam2"], cwd=D, env=env, stdout=f,
                       stderr=subprocess.STDOUT, creationflags=0x08000000)
    print((D / "rapor-d2.txt").read_text(encoding="utf-8"), flush=True)
print("HAT BITTI", flush=True)
