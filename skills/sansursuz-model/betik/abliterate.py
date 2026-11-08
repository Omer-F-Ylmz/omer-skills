"""Yazici matrislerde ortogonallestirme. Rank-1..k, rampa cekirdek, norm koruma, MoE.
  python abliterate.py --model <hf> --yon yon.npz --cikti <dizin> --max-agirlik 1.2 --norm-koru
"""
import argparse, json, os, re, shutil
import numpy as np
import torch
from safetensors import safe_open
from safetensors.torch import save_file

BILESEN = (r"(?:^|\.)(?:o_proj|out_proj|down_proj|down_exps|w2|output_linear)$",)

p = argparse.ArgumentParser()
p.add_argument("--model", required=True); p.add_argument("--yon", required=True)
p.add_argument("--cikti", required=True)
p.add_argument("--max-agirlik", type=float, default=1.2)
p.add_argument("--min-agirlik", type=float, default=0.3)
p.add_argument("--tepe", type=float, default=0.85); p.add_argument("--mesafe", type=float, default=12)
p.add_argument("--ilk-katman", type=int, default=4); p.add_argument("--son-oran", type=float, default=0.9)
p.add_argument("--norm-koru", action="store_true"); p.add_argument("--lora", action="store_true")
a = p.parse_args()

y = np.load(a.yon)
U = torch.tensor(y["dirs"], dtype=torch.float32)
L = int(y["L"])
son = int(L * a.son_oran)
tepe = int(L * a.tepe)


def agirlik(katman):
    if katman < a.ilk_katman or katman > son:
        return 0.0
    d = abs(katman - tepe)
    if d >= a.mesafe:
        return 0.0
    return a.max_agirlik + (d / a.mesafe) * (a.min_agirlik - a.max_agirlik)


def uygula(W, r, w):
    if W.ndim == 3:
        for e in range(W.shape[0]):
            W[e] = uygula(W[e], r, w)
        return W
    if W.shape[0] != r.shape[0]:
        return W
    Wd = W.float()
    for rk in r:
        Wd = Wd - w * torch.outer(rk, rk @ Wd)
    if a.norm_koru:
        Wd *= (W.float().norm(dim=1) / Wd.norm(dim=1).clamp_min(1e-9))[:, None]
    return Wd.to(W.dtype)


shutil.copytree(a.model, a.cikti, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.safetensors", "*.bin"))
kayit, n = {}, 0
for f in [x for x in os.listdir(a.model) if x.endswith(".safetensors")]:
    with safe_open(os.path.join(a.model, f), "pt") as s:
        for k in s.keys():
            W = s.get_tensor(k)
            m = re.search(r"layers\.(\d+)\.", k)
            if not m or not any(re.search(b, k) for b in BILESEN):
                kayit[k] = W; continue
            w = agirlik(int(m.group(1)))
            if w == 0:
                kayit[k] = W; continue
            W2 = uygula(W.clone(), U, w)
            if a.lora:
                d = (W2.float() - W.float())
                u, sv, vh = torch.linalg.svd_lowrank(d, q=min(4, min(d.shape)))
                kayit[k + ".lora_A"] = (u * sv).to(torch.float16).contiguous()
                kayit[k + ".lora_B"] = vh.T.contiguous().to(torch.float16)
            else:
                kayit[k] = W2
            n += 1
    print(f, flush=True)
save_file(kayit, os.path.join(a.cikti, "model.safetensors"), metadata={"format": "pt"})
json.dump({"yon": os.path.abspath(a.yon), "degisen": n, "max": a.max_agirlik, "min": a.min_agirlik,
           "tepe": tepe, "mesafe": a.mesafe, "ilk": a.ilk_katman, "son": son, "norm_koru": a.norm_koru},
          open(os.path.join(a.cikti, "abliteration.json"), "w"), indent=1)
print(json.dumps({"degisen_tensor": n, "cikti": a.cikti}))
