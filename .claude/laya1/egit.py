"""LAYA-1 ince ayar (venv python'u ile): veri.jsonl'in eğitim yarısı (test=False, Opus etiketi) → laya.train.finetune.
Kollar: bas (freeze_encoder, yalnız karar başı) · tam (kodlayıcı da, düşük lr). Çıktı: .claude/laya1/ck-<kol>/"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "olcum"))
from huggingface_hub import snapshot_download
from laya.train import TrainConfig, finetune

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
for kol, cfg in (("bas", TrainConfig(epochs=12, freeze_encoder=True, micro_batch=4, grad_accum=2, max_len=2048, calib_frac=0.2)),
                 ("tam", TrainConfig(epochs=6, encoder_lr=1e-5, micro_batch=2, grad_accum=4, max_len=2048, calib_frac=0.2,
                                     gradient_checkpointing=True))):
    son = sys.argv[1] if len(sys.argv) > 1 else ""  # d2: ck-<kol>2, d1 checkpoint'lerinin üstüne yazmaz
    print(kol, json.dumps(finetune(str(D / "egitim.jsonl"), taban, str(D / f"ck-{kol}{son}"), cfg), default=str)[:600], flush=True)
print("EGIT BITTI", flush=True)
