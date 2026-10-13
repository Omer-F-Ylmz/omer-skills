"""LAYA-1: Laya (yerel karar modeli, HF convaiinnovations/laya, Apache-2.0) için Jev Tasiyici sözleşmesi.
  jev_yargic.yargila(states, questions, LayaTasiyici()) · jev_yargic.Onbellekli(LayaTasiyici()) — önbellek aynı.
Laya ayrı venv'de (torch cu124): sınıf her yargila çağrısında venv python'unu bu dosyanın __main__'iyle koşar,
JSON stdin → stdout. Ücret $0, jeton sayımı yerel (Jev'e gönderilmez). Soru şeması Jev ile aynı (score → 0..n-1 beklenen düzey)."""
import json
import os
import subprocess
import sys
from pathlib import Path

VENV_PY = os.environ.get("LAYA_PY", r"C:\Projeler\.laya-venv\Scripts\python.exe")
MODEL = os.environ.get("LAYA_MODEL", "multilingual")  # multilingual | english | typed-decisions | ince ayarlı dizin
MAX_LEN = int(os.environ.get("LAYA_MAX_LEN", "4096"))  # README: ~4k token'a kadar 16-18/20 doğru; üstü değişken
ALT = {"english": None, "multilingual": "multilingual", "typed-decisions": "typed-decisions"}


class LayaTasiyici:
    def __init__(self, model=MODEL, max_len=MAX_LEN, py=VENV_PY):
        self.model, self.max_len, self.py, self.kullanim = model, max_len, py, []

    def yargila(self, states, questions):
        from jev.cekirdek import JevHata
        girdi = json.dumps({"model": self.model, "max_len": self.max_len, "states": states, "questions": questions},
                           ensure_ascii=False)
        r = subprocess.run([self.py, "-I", __file__], input=girdi.encode("utf-8"), capture_output=True,
                           creationflags=0x08000000 if os.name == "nt" else 0)
        if r.returncode:
            raise JevHata(f"laya rc {r.returncode}: {r.stderr.decode('utf-8', 'replace')[-300:]}")
        out = json.loads(r.stdout)
        self.kullanim.append({"cost": 0.0, "input_tokens": out["girdi_jeton"], "istek": len(states), "sn": out["sn"]})
        return out["cevap"]


def _isci():
    import time
    import laya
    g, cikti = json.loads(sys.stdin.buffer.read().decode("utf-8")), sys.stdout.buffer
    sys.stdout = sys.stderr  # kütüphane çıktısı JSON'u bozmasın
    t0, m = time.perf_counter(), g["model"]
    agent = laya.load(m) if Path(m).is_dir() else laya.load("convaiinnovations/laya", subfolder=ALT[m])
    res = agent.predict_batch(g["states"], g["questions"], batch_size=4, max_len=g["max_len"])
    cevap = [r["answers"] for r in res]
    jeton = sum((r.get("usage") or {}).get("input_tokens", 0) for r in res)
    cikti.write(json.dumps({"cevap": cevap, "girdi_jeton": jeton, "sn": round(time.perf_counter() - t0, 2)}).encode())


if __name__ == "__main__":
    _isci()
