import json, sys
from pathlib import Path
import numpy as np
KOK = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(KOK / "tools"))
import ertele_katalog as ek
d = ek._dizin(); yollar = json.loads((ek.EV / "ertele-gomme.json").read_text(encoding="utf-8"))
M = np.load(ek.GOMME).astype(np.float32); c = json.loads(Path(__file__).with_name("hyde.json").read_text(encoding="utf-8"))
for s in (KOK / "tmp/ertele9/tarif.jsonl").read_text(encoding="utf-8").splitlines():
    t = json.loads(s); q = np.asarray(c[t["tarif"]]["v"], np.float32); sk = M @ q
    h = yollar.index(d[t["ad"]]["yol"]); r = int((sk > sk[h]).sum()) + 1
    if r > 20:
        print(r, t["ad"], "|", d[t["ad"]]["acik"][:90], "| T:", t["tarif"][:90], "| 1.:", yollar[int(sk.argmax())][-60:])
