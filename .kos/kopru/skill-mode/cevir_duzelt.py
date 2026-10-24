"""sorgu-cevir.json'daki hizası kaymış çevirileri (q ile EN yeniden yazım kosinüsü <0.5) 8'lik paketle yeniden çevirir; kosinüs doğrulamalı, en çok 4 tur."""
import json, sys
import numpy as np
import sorgu_cevir as sc
import her_sey_ara as h
sys.stdout.reconfigure(encoding="utf-8")
sc.PAKET = 8
a = h.Arayici(yogun=True)
ob = json.loads(sc.CIK.read_text(encoding="utf-8"))
def emb(l):
    v = np.array(list(a.m.embed(l)), dtype="float32"); return v / np.linalg.norm(v, axis=1, keepdims=True)
def kotu(qs):
    c = (emb(qs) * emb([ob[q].split("|")[0] for q in qs])).sum(1)
    return [q for q, x in zip(qs, c) if x < 0.5]
bad = kotu(list(ob))
print("başlangıç kötü", len(bad), flush=True)
for tur in range(4):
    if not bad: break
    for q in bad: ob.pop(q, None)
    ob = sc.cevir(bad, ob)
    bad = kotu([q for q in bad if q in ob]) + [q for q in bad if q not in ob]
    sc.CIK.write_text(json.dumps(ob, ensure_ascii=False, indent=0), encoding="utf-8")
    print("tur", tur, "kötü", len(bad), "kayıt", len(ob), flush=True)
