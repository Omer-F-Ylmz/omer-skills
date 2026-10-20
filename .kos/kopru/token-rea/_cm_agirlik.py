"""mem2 bm25 ağırlık taraması (yalnız B kolu, eğitim tohumu). Kullanım: python -I -S _cm_agirlik.py <tohum> [n]"""
import os
import random
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mem2

tohum, n = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 60
rnd = random.Random(tohum)
c = sqlite3.connect("file:" + mem2.DB + "?mode=ro", uri=True)
satir = c.execute("SELECT id,title,narrative FROM observations WHERE project='omer-skills' AND length(narrative)>300 AND id<(SELECT max(id) FROM observations)-5").fetchall()
soz = lambda s: list(dict.fromkeys(w for w in re.findall(r"[^\W\d_]{5,}", (s or "").lower())))
Q = []
for i, b, a in rnd.sample(satir, n):
    wb, wa = soz(b), [w for w in soz(a) if w not in soz(b)]
    if len(wb) >= 3:
        Q.append((i, "b", " ".join(rnd.sample(wb, 3))))
    if len(wa) >= 4:
        Q.append((i, "a", " ".join(rnd.sample(wa, 4))))
for ag in [(8, 3, 1, 1, 2, 3), (1, 1, 1, 1, 1, 1), (3, 2, 3, 1, 2, 2), (4, 2, 4, 1, 2, 2), (2, 1, 4, 1, 3, 2), (5, 2, 5, 0, 3, 3)]:
    h = {"b": [0, 0], "a": [0, 0]}
    for i, t, q in Q:
        h[t][1] += 1
        h[t][0] += i in [r[0] for r in mem2.ara(q, 5, None, ag)]
    print(ag, {t: round(v[0] / v[1], 3) for t, v in h.items()}, round((h["a"][0] + h["b"][0]) / (h["a"][1] + h["b"][1]), 3))
