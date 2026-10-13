"""LAYA-1 d2/d3 hattı (ortak sıradan tek iş; torch işleri sıralı, aynı anda 1): kör Opus puan → veri → ince ayar (bas<S>/tam<S>) → puanla → rapor.
python olcum_sira.py hat.py   · çıktı rapor-d<S>.txt"""
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).parent
PY = "C:/Projeler/.laya-venv/Scripts/python.exe"
env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
env.update(HF_HUB_OFFLINE="1", PYTHONIOENCODING="utf-8")
S = "3"  # dalga eki (d2 → "2"; d3 eğitimi d2'de RAM yüzünden durdu)


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
    for kol in ("bas", "tam"):  # ayrı süreç → kol başına tepe bellek; RAM %88 üstü (çıkış 88) → toplu boyutu yarıya
        for mb in (2, 1):
            print(">>", PY, "egit.py", S, mb, kol, flush=True)
            if subprocess.run([PY, "egit.py", S, str(mb), kol], cwd=D, env=env, creationflags=0x08000000).returncode != 88:
                break
if "puanla" in adim:
    kos(sys.executable, "olc.py", "puanla", f"laya0d{S}")
    for k in (f"bas{S}", f"tam{S}"):
        kos(sys.executable, "olc.py", "puanla", f"laya-{k}", str(D / f"ck-{k}"))
if "rapor" in adim:
    with open(D / f"rapor-d{S}.txt", "w", encoding="utf-8") as f:
        subprocess.run([sys.executable, "olc.py", "rapor", f"laya0d{S}", f"laya-bas{S}", f"laya-tam{S}"], cwd=D, env=env, stdout=f,
                       stderr=subprocess.STDOUT, creationflags=0x08000000)
    print((D / f"rapor-d{S}.txt").read_text(encoding="utf-8"), flush=True)
print("HAT BITTI", flush=True)
