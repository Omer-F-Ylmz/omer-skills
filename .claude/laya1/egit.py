"""LAYA-1 ince ayar (venv python'u ile): veri.jsonl'in eğitim yarısı (test=False, Opus etiketi) → laya.train.finetune.
Kollar: bas (freeze_encoder, yalnız karar başı) · tam (kodlayıcı da, düşük lr). Çıktı: .claude/laya1/ck-<kol><son>/
python egit.py <son> [micro_batch] [kol]  · etkin toplu 8 = micro_batch × grad_accum · RAM %88 üstü → çıkış 88 (hat.py toplu boyutu düşürür)"""
import ctypes
import json
import os
import sys
import threading
import time
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "olcum"))
from huggingface_hub import snapshot_download
from laya.train import TrainConfig, finetune


class _MS(ctypes.Structure):
    _fields_ = [("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD)] + [(n, ctypes.c_uint64) for n in
                ("tp", "ap", "tf", "af", "tv", "av", "aev")]


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("pf", wintypes.DWORD)] + [(n, ctypes.c_size_t) for n in
                ("peak_ws", "ws", "qpp", "qp", "qpnp", "qnp", "commit", "peak_commit")]


def ram_yuzde():
    m = _MS(dwLength=ctypes.sizeof(_MS))
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def tepe_gb():
    p = _PMC(cb=ctypes.sizeof(_PMC))
    ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(p), p.cb)
    return round(p.peak_ws / 2**30, 2), round(p.peak_commit / 2**30, 2)


def bekci():
    tepe = 0
    while True:
        r = ram_yuzde()
        tepe = max(tepe, r)
        if r > 88:
            print(f"RAM %{r} > 88 → çıkış 88 (tepe süreç ws/commit GB {tepe_gb()})", flush=True)
            os._exit(88)
        bekci.tepe = tepe
        time.sleep(2)


threading.Thread(target=bekci, daemon=True).start()
D = Path(__file__).parent
SEVIYE = ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik", "Çoğunlukla, küçük eksik", "Tam karşılıyor",
          "Tam ve örnek nitelikte"]  # jev_yargic.SEVIYE/SORU kopyası (venv'de jev paketi yok)
SORULAR = {"SORU": {"kalite": {"type": "score", "criteria": SEVIYE, "instructions": "`yanit`, `gorev` isteğini `kabul` ölçütüne göre ne kadar karşılıyor? Yalnız yanıtın içeriğini yargıla; biçim/uzunluk değil, doğruluk ve kabul ölçütü."}},
           "ESLES": {"kalite": {"type": "noul", "instructions": "Does the report line `satir` state the same tool, claim or item as the gold item `altin` (same thing, possibly paraphrased)?"}}}
v = [json.loads(x) for x in open(D / "veri.jsonl", encoding="utf-8")]
with open(D / "egitim.jsonl", "w", encoding="utf-8") as f:
    for k in v:
        if not k["test"]:
            e = int(k["opus"] // 2) if k["soru"] == "SORU" else bool(k["opus"])
            f.write(json.dumps({"state": k["state"], "questions": SORULAR[k["soru"]], "expected": {"kalite": e}}, ensure_ascii=False) + "\n")
taban = str(Path(snapshot_download("convaiinnovations/laya")) / "multilingual")
son = sys.argv[1] if len(sys.argv) > 1 else ""  # d2/d3: ck-<kol>2|3, d1 checkpoint'lerinin üstüne yazmaz
mb = int(sys.argv[2]) if len(sys.argv) > 2 else None
kollar = {"bas": TrainConfig(epochs=12, freeze_encoder=True, micro_batch=mb or 4, grad_accum=8 // (mb or 4), max_len=2048,
                             calib_frac=0.2),
          "tam": TrainConfig(epochs=6, encoder_lr=1e-5, micro_batch=mb or 2, grad_accum=8 // (mb or 2), max_len=2048,
                             calib_frac=0.2, gradient_checkpointing=True)}
for kol in sys.argv[3:] or kollar:
    print(kol, json.dumps(finetune(str(D / "egitim.jsonl"), taban, str(D / f"ck-{kol}{son}"), kollar[kol]), default=str)[:600], flush=True)
print(f"TEPE {sys.argv[3:]} mb={mb} süreç ws/commit GB {tepe_gb()} · sistem RAM tepe %{getattr(bekci, 'tepe', '?')}", flush=True)
print("EGIT BITTI", flush=True)
