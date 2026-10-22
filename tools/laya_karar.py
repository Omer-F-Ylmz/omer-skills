"""Laya yerel karar (ince ayarlı ck): görev metni → haiku|sonnet|opus (+ olasılık). Bayrak: LAYA_YONLENDIR=1 (yonlendir.sinifla).
python tools/laya_karar.py "<görev metni>"  → JSON {model, guven} · ck yok/venv yok → çıkış 3"""
import json
import subprocess
import sys
from pathlib import Path

LAYA = Path(__file__).parent / "laya"
PY = LAYA / ".venv" / "Scripts" / "python.exe"
CK = LAYA / "ck" / "model-tam"
SORU = {"etiket": {"type": "choice", "instructions": "Which model tier is enough to do this task well?",
                   "criteria": {k: k for k in ("haiku", "sonnet", "opus")}}}


def karar(metin):
    """{model, guven} ya da None (ck/venv yok, hata)."""
    if not (PY.exists() and CK.exists()):
        return None
    r = subprocess.run([str(PY), "-I", str(Path(__file__).resolve()), "--isci"], input=metin, capture_output=True, text=True,
                       encoding="utf-8", timeout=120, creationflags=0x08000000)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def _isci():
    import laya
    c = laya.load(str(CK)).predict({"metin": sys.stdin.read()[:1500]}, SORU)["answers"]["etiket"]
    print(json.dumps({"model": c["choice"], "guven": round(c["answer_confidence"], 3)}))


if __name__ == "__main__":
    if sys.argv[1] == "--isci":
        _isci()
    else:
        k = karar(sys.argv[1])
        print(json.dumps(k) if k else "yok")
        sys.exit(0 if k else 3)
