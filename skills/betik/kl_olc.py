"""Iki model arasinda zararsiz istemlerde KL (kapasite kaybi sinyali). Kucuk modelde kos.
  python kl_olc.py --a <orijinal> --b <duzenlenmis> --n 50
Hedef: KL <= 0,01 (sert) ; 0,2'ye kadar ikinci kapi. 4-bit yukleme kabul, iki model ayni sekilde.
"""
import argparse, json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

p = argparse.ArgumentParser()
p.add_argument("--a", required=True); p.add_argument("--b", required=True)
p.add_argument("--n", type=int, default=50)
a = p.parse_args()

tok = AutoTokenizer.from_pretrained(a.a)
ist = [json.loads(x)["istem"] for x in open("istem/iyi.jsonl", encoding="utf-8") if x.strip()][:a.n]
modeller = []
for yol in (a.a, a.b):
    m = AutoModelForCausalLM.from_pretrained(yol, torch_dtype=torch.float16, device_map="auto")
    m.eval(); modeller.append(m)

kl, ppl_o, ppl_y = [], [], []
for s in ist:
    ids = tok(s, return_tensors="pt", truncation=True, max_length=512).to(modeller[0].device)
    with torch.no_grad():
        lo = modeller[0](**ids).logits[0, :-1].float()
        ly = modeller[1](**ids).logits[0, :-1].float()
    y = ids["input_ids"][0, 1:]
    lp_o, lp_y = torch.log_softmax(lo, -1), torch.log_softmax(ly, -1)
    kl.append(float((lp_o.exp() * (lp_o - lp_y)).sum(-1).mean()))
    ppl_o.append(float(-lp_o[range(len(y)), y].mean())); ppl_y.append(float(-lp_y[range(len(y)), y].mean()))
ort = sum(kl) / len(kl)
print(json.dumps({"n": len(kl), "kl_ort": round(ort, 5), "kl_max": round(max(kl), 5),
                  "ppl_orijinal": round(sum(ppl_o) / len(ppl_o), 3),
                  "ppl_duzenlenmis": round(sum(ppl_y) / len(ppl_y), 3)}, ensure_ascii=False))
print("KAPI KL:", "GECTI" if ort <= 0.01 else ("IKINCI KAPI" if ort <= 0.2 else "KALDI"))
