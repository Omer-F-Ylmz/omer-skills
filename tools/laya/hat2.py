"""LAYA-2 hattı (arka planda tek iş): kurul bitişini bekle → kurul↔Opus uyumu → havuz etiketlerini veri.jsonl'e kat → tam ince ayar → test puanı + rapor.
  python .kos/kopru/arka.py .claude/laya2/hat2.log tools/laya/hat2.py        çıktı: .claude/laya2/rapor-d2.txt (kapı kararı raporu okuyup verilir)
Test = laya-1 bölmesi (Opus etiketli, eğitime girmez); havuz öğeleri test=False, kaynak 'havuz' (rapor yalnız jev1/video'yu sayar).
Eski checkpoint'e dokunulmaz: yeni ck-tam2 ayrı dizin, geçmezse eskisi (laya1 ck-tam3k) kalır = geri alma."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
D1, D = KOK / ".claude/laya1", KOK / ".claude/laya2"
PY = "C:/Projeler/.laya-venv/Scripts/python.exe"
sys.path.insert(0, str(KOK / "tools/laya"))
env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
env.update(HF_HUB_OFFLINE="1", PYTHONIOENCODING="utf-8")


def kos(*a):
    print(">>", *a, flush=True)
    r = subprocess.run(list(a), cwd=D, env=env, stdout=sys.stdout, stderr=subprocess.STDOUT, creationflags=0x08000000)
    if r.returncode:
        sys.exit(f"rc {r.returncode}: {a}")


while "KURUL BITTI" not in (D / "kurul.log").read_text(encoding="utf-8", errors="replace"):
    time.sleep(60)
kos(sys.executable, str(KOK / "tools/laya/uyum.py"))
import uyum  # noqa: E402

w = json.loads((D / "uyum.json").read_text(encoding="utf-8"))
opus = {json.loads(x)["id"] for x in open(D / "opus.jsonl", encoding="utf-8")}
girdi = {k["id"]: k["state"] for k in map(json.loads, open(D / "kurul-girdi.jsonl", encoding="utf-8"))}
shutil.copy(D1 / "veri.jsonl", D / "veri.jsonl")
n = 0
with open(D / "veri.jsonl", "a", encoding="utf-8") as f:
    for r in map(json.loads, open(D / "kurul.jsonl", encoding="utf-8")):
        if r["id"] in opus or r["id"] not in girdi:
            continue
        et = min(5, max(0, round(uyum.kurul_puan(r["puan"], w))))
        f.write(json.dumps({"id": r["id"], "kaynak": "havuz", "soru": "SORU", "state": girdi[r["id"]], "opus": et * 2, "jev": 0,
                            "test": False}, ensure_ascii=False) + "\n")
        n += 1
print("havuz etiketli", n, flush=True)
for ad in ("egit.py", "olc.py"):
    shutil.copy(D1 / ad, D / ad)
e = (D / "egit.py").read_text(encoding="utf-8").replace("epochs=6, encoder_lr", "epochs=3, encoder_lr")  # ~2k öğe: 3 dönem
(D / "egit.py").write_text(e, encoding="utf-8")
kos(PY, "egit.py", "2", "1", "tam")
kos(sys.executable, "olc.py", "puanla", "laya-tam2", str(D / "ck-tam2"))
with open(D / "rapor-d2.txt", "w", encoding="utf-8") as f:
    subprocess.run([sys.executable, "olc.py", "rapor", "laya-tam2"], cwd=D, env=env, stdout=f, stderr=subprocess.STDOUT, creationflags=0x08000000)
print("HAT2 BITTI", flush=True)
