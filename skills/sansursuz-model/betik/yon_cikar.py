"""Ret yonu cikarimi. Son istem tokeni, katman katman, projected + birim.
  python yon_cikar.py --model <hf> --kotu istem/kotu.jsonl --iyi istem/iyi.jsonl --cikti yon.npz --rank 1
"""
import argparse, json
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

p = argparse.ArgumentParser()
p.add_argument("--model", required=True); p.add_argument("--kotu", required=True)
p.add_argument("--iyi", required=True); p.add_argument("--cikti", required=True)
p.add_argument("--rank", type=int, default=1); p.add_argument("--ek", default="")
p.add_argument("--batch", type=int, default=4)
a = p.parse_args()

tok = AutoTokenizer.from_pretrained(a.model)
tok.padding_side = "left"
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
mdl = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map="auto")
mdl.eval()


def oku(yol):
    return [json.loads(x)["istem"] for x in open(yol, encoding="utf-8") if x.strip()]


@torch.no_grad()
def ort_hidden(istemler):
    toplam, say = None, 0
    for i in range(0, len(istemler), a.batch):
        par = istemler[i:i + a.batch]
        metin = [tok.apply_chat_template([{"role": "user", "content": s}],
                                         add_generation_prompt=True, tokenize=False) for s in par]
        b = tok(metin, return_tensors="pt", padding=True, truncation=True, max_length=2048).to(mdl.device)
        h = mdl(**b, output_hidden_states=True).hidden_states
        son = b["attention_mask"].sum(1) - 1
        for j in range(len(par)):
            v = torch.stack([x[j, son[j]] for x in h]).float().cpu().numpy()
            toplam = v if toplam is None else toplam + v
            say += 1
    return toplam / say


kotu, iyi = ort_hidden(oku(a.kotu)), ort_hidden(oku(a.iyi))
if a.ek:
    ek = []
    for x in open(a.ek, encoding="utf-8"):
        if x.strip():
            d = json.loads(x)
            if d.get("sinif") in ("hard", "soft", "yarim"):
                ek.append(d.get("istem") or d.get("cevap", ""))
    if ek:
        kotu = (kotu * 2 + ort_hidden(ek)) / 3

L = kotu.shape[0]
fark = kotu - iyi
mu_i = iyi / np.maximum(np.linalg.norm(iyi, axis=1, keepdims=True), 1e-9)
fark = fark - (fark * mu_i).sum(1, keepdims=True) * mu_i
std = 0.5 * (kotu.std(0) + iyi.std(0)) + 1e-9
skor = np.linalg.norm(fark, axis=1) / np.linalg.norm(std, axis=1)
alt, ust = int(0.15 * L), int(0.85 * L)
sec = int(np.argmax(np.where((np.arange(L) >= alt) & (np.arange(L) <= ust), skor, -1)))
dirs = fark / np.maximum(np.linalg.norm(fark, axis=1, keepdims=True), 1e-9)

if a.rank == 1:
    U = dirs[sec][None, :]
else:
    U, _, _ = np.linalg.svd(fark[alt:ust], full_matrices=False)
    U = U[:a.rank]
    for k in range(1, len(U)):
        U[k] -= U[:k].T @ U[k] @ U[:k]
        U[k] /= np.linalg.norm(U[k]) + 1e-9

ben = np.abs(dirs @ dirs[sec])
np.savez(a.cikti, dirs=U.astype(np.float32), katman=sec, skor=skor.astype(np.float32),
         benzerlik_ort=float(ben.mean()), benzerlik_min=float(ben.min()), L=L)
print(json.dumps({"katman": sec, "L": L, "rank": a.rank,
                  "benzerlik_ort": round(float(ben.mean()), 4),
                  "benzerlik_min": round(float(ben.min()), 4)}, ensure_ascii=False))
print("UYARI: benzerlik_ort < 0,9 ise --rank 3 dene." if ben.mean() < 0.9 else "Yon tutarli.")
