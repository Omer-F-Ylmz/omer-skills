"""SKILL-MODE-3: canlı katalog (docs/katalog/yetenek.jsonl) → yetenek-tam.jsonl eşitle (yalnız ekler, silmez); bm25.pkl yeniden, vek.npy yalnız yeni satırlar.
python esitle.py"""
import json, sys
from pathlib import Path
import numpy as np
import her_sey_ara as h

D = Path(__file__).resolve().parent
CANLI = D.parents[2] / "docs" / "katalog" / "yetenek.jsonl"
anahtar = lambda o: f"{o['ad']}|{o.get('imza', '')}"

tam = h.yukle(h.KAT)
var = {anahtar(o) for o in tam}
yeni = [o for o in h.yukle(CANLI) if anahtar(o) not in var]
print("yeni", len(yeni), flush=True)
if yeni:
    v = np.load(D / "vek.npy")
    assert len(v) <= len(tam), (len(v), len(tam))
    with h.KAT.open("a", encoding="utf-8") as f:
        f.write("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in yeni))
    yeni = tam[len(v):] + yeni  # dizin eşitlemeden sonra eklenen satırlar da vektörlenir
    from fastembed import TextEmbedding
    e = np.array(list(TextEmbedding(h.MODEL, threads=4).embed([h.belge_metin(o) for o in yeni], batch_size=64)), dtype="float32")
    e /= np.linalg.norm(e, axis=1, keepdims=True) + 1e-9
    np.save(D / "vek.npy", np.vstack([v, e]))
    h.dizin_bm25()
print("tam", len(h.yukle(h.KAT)), "vek", np.load(D / "vek.npy").shape, flush=True)
