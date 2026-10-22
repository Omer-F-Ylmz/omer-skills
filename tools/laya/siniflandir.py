"""Laya sınıflama: veri/{ad}_{train,test}.csv (text,label) -> ince ayar + test doğruluğu. Venv python'u ile.
python siniflandir.py egit <ad> <kol:bas|tam>   -> ck/<ad>-<kol>/ ; python siniflandir.py olc <ad> [ck-adı|sifir]  -> doğruluk
ck-adı verilmezse sıfır-atış (taban)."""
import csv
import json
import sys
from pathlib import Path

import laya
from huggingface_hub import snapshot_download
from laya.train import TrainConfig, finetune

D = Path(__file__).parent
sys.path.insert(0, str(D))
from dogrula import KUME  # noqa: E402

SORU = {"model": "Which model tier is enough to do this task well?", "tur": "What kind of work is this?",
        "konu": "What is the main topic of this text?"}


def sorular(ad):
    return {"etiket": {"type": "choice", "instructions": SORU[ad], "criteria": {k: k for k in KUME[ad]}}}


def taban():
    return str(Path(snapshot_download("convaiinnovations/laya")) / "multilingual")


def satirlar(ad, t):
    return list(csv.reader(open(D / "veri" / f"{ad}_{t}.csv", encoding="utf-8")))[1:]


def olc(ad, ck=None):
    ajan = laya.load(str(D / "ck" / ck) if ck else taban())
    q, dogru, say = sorular(ad), 0, 0
    for metin, etiket in satirlar(ad, "test"):
        dogru += ajan.predict({"metin": metin[:1500]}, q)["answers"]["etiket"]["choice"] == etiket
        say += 1
    return dogru, say


def main():
    komut, ad = sys.argv[1], sys.argv[2]
    if komut == "egit":
        kol = sys.argv[3]
        cfg = {"bas": TrainConfig(epochs=12, freeze_encoder=True, micro_batch=4, grad_accum=2, max_len=512, calib_frac=0.2),
               "tam": TrainConfig(epochs=int(sys.argv[4]) if len(sys.argv) > 4 else 6, encoder_lr=1e-5, micro_batch=2, grad_accum=4, max_len=512, calib_frac=0.2,
                                  gradient_checkpointing=True)}[kol]
        with open(D / "veri" / f"{ad}_egitim.jsonl", "w", encoding="utf-8") as f:
            for metin, etiket in satirlar(ad, "train"):
                f.write(json.dumps({"state": {"metin": metin[:1500]}, "questions": sorular(ad), "expected": {"etiket": etiket}},
                                   ensure_ascii=False) + "\n")
        finetune(str(D / "veri" / f"{ad}_egitim.jsonl"), taban(), str(D / "ck" / f"{ad}-{kol}{sys.argv[4] if len(sys.argv) > 4 else ''}"), cfg)
        print("EGIT BITTI", ad, kol)
    else:
        d, n = olc(ad, sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "sifir" else None)
        print(f"OLC {ad} {sys.argv[3] if len(sys.argv) > 3 else 'sifir'} {d}/{n} = {d / n:.3f}")


if __name__ == "__main__":
    main()
