"""Türkçe tarif → İngilizce skill açıklaması (ücretsiz havuz, kolay); sonra gömme sırası yeniden."""
import json, sys
from pathlib import Path
import numpy as np
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ertele_katalog as ek, ucretsiz_havuz as uh
d = ek._dizin()
yollar = json.loads((ek.EV / "ertele-gomme.json").read_text(encoding="utf-8"))
M = np.load(ek.GOMME).astype(np.float32)
onb = Path(__file__).with_name("hyde.json")
c = json.loads(onb.read_text(encoding="utf-8")) if onb.exists() else {}
I = ("Rewrite this user request as the one-line English 'description:' of a Claude Code skill that would do it, "
     "naming the domain, tool/platform and concrete actions (max 40 words). Reply with the description only.\nRequest: ")
for f in sys.argv[1:]:
    gs, bs = [], []
    for s in (KOK / f).read_text(encoding="utf-8").splitlines():
        t = json.loads(s)
        if not c.get(t["tarif"], {}).get("en"):
            m = ek._llm(I + t["tarif"])
            c[t["tarif"]] = {"en": m, "kim": "cf"}
            c[t["tarif"]]["v"] = ek._gom([t["tarif"] + " | " + c[t["tarif"]]["en"]])[0]
            onb.write_text(json.dumps(c), encoding="utf-8")
        q = np.asarray(c[t["tarif"]]["v"], np.float32); sk = M @ (q / np.linalg.norm(q))
        h = yollar.index(d[t["ad"]]["yol"]); gs.append(int((sk > sk[h]).sum()) + 1)
        bm = ek._bm25(t["tarif"] + " " + c[t["tarif"]]["en"], d); bmy = {}
        for a, p in bm.items(): bmy[d[a]["yol"]] = max(p, bmy.get(d[a]["yol"], 0))
        bs.append(sum(p > bmy.get(yollar[h], 0) for p in bmy.values()) + 1)
    print(f, "gömme+hyde:", sorted(gs), "\n  bm25+hyde:", sorted(bs))
