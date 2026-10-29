"""Altının yalnız gömme ve yalnız BM25 sırası (dosya düzeyinde); sorgu gömmesi önbelleğe yazılır."""
import json, sys, time
from pathlib import Path
import numpy as np
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ertele_katalog as ek
d = ek._dizin()
yollar = json.loads((ek.EV / "ertele-gomme.json").read_text(encoding="utf-8"))
M = np.load(ek.GOMME).astype(np.float32)
onb = Path(__file__).with_name("sorgu-gomme.json")
c = json.loads(onb.read_text(encoding="utf-8")) if onb.exists() else {}
for f in ["tmp/ertele9/tarif.jsonl", "tmp/ertele7/tarif.jsonl", "tmp/ertele7/tarif2.jsonl"]:
    gs, bs = [], []
    for s in (KOK / f).read_text(encoding="utf-8").splitlines():
        t = json.loads(s)
        if t["tarif"] not in c: c[t["tarif"]] = ek._gom([t["tarif"]])[0]
        q = np.asarray(c[t["tarif"]], np.float32); sk = M @ (q / np.linalg.norm(q))
        h = yollar.index(d[t["ad"]]["yol"]); gs.append(int((sk > sk[h]).sum()) + 1)
        t0 = time.time(); bm = ek._bm25(t["tarif"], d); dt = time.time() - t0
        bmy = {}
        for a, p in bm.items(): bmy[d[a]["yol"]] = max(p, bmy.get(d[a]["yol"], 0))
        bs.append(sum(p > bmy.get(yollar[h], 0) for p in bmy.values()) + 1)
    print(f, "gömme sıra:", sorted(gs), "\n  bm25 sıra:", sorted(bs), f"bm25 {dt:.1f}s")
onb.write_text(json.dumps(c), encoding="utf-8")
