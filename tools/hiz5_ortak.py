"""VIDEO-HIZ-5: iki koşuyu ref2'ye göre ORTAK videolarda (her ikisinde recall>0,5: referans kusuru elenir) kelime-recall + benzerlik ile karşılaştırır. Kullanım: hiz5_ortak.py <taban> <aday>"""
import difflib, json, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import video_hiz4_olc as o

D = KOK / ".kos/kopru/ogren/hiz4"


def olc(ad):
    r = {}
    for p in (D / ad).glob("*.json"):
        q = D / "ref2" / p.name
        if p.name.startswith("_") or not q.exists():
            continue
        ke, ky = o.kel(json.loads(q.read_text(encoding="utf-8"))), o.kel(json.loads(p.read_text(encoding="utf-8")))
        ce, cy = Counter(ke), Counter(ky)
        r[p.stem] = (sum((ce & cy).values()) / max(1, sum(ce.values())), difflib.SequenceMatcher(None, ke, ky, autojunk=False).ratio() if ke or ky else 1.0)
    return r


b, g = olc(sys.argv[1]), olc(sys.argv[2])
k = [x for x in g if x in b and b[x][0] > 0.5 and g[x][0] > 0.5]
n = len(k)
print(f"ortak N={n}  {sys.argv[1]}: recall {sum(b[x][0] for x in k)/n:.3f} benz {sum(b[x][1] for x in k)/n:.3f} | {sys.argv[2]}: recall {sum(g[x][0] for x in k)/n:.3f} benz {sum(g[x][1] for x in k)/n:.3f} | recall oranı {sum(g[x][0] for x in k)/sum(b[x][0] for x in k):.3f} | aday recall>=0.95: {sum(g[x][0]>=.95 for x in k)}/{n}, taban {sum(b[x][0]>=.95 for x in k)}/{n}")
