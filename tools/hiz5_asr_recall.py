"""VIDEO-HIZ-5: ASR kelime geri çağırımı (çoklu küme) + SequenceMatcher benzerliği, ref2'ye göre. Kullanım: hiz5_asr_recall.py <koşu adı> [<koşu adı>...]"""
import difflib, json, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import video_hiz4_olc as o

D = KOK / ".kos/kopru/ogren/hiz4"
for ad in sys.argv[1:]:
    rc, sm, dusuk = [], [], []
    for p in sorted((D / ad).glob("*.json")):
        r2p = D / "ref2" / p.name
        if p.name.startswith("_") or not r2p.exists():
            continue
        ke, ky = o.kel(json.loads(r2p.read_text(encoding="utf-8"))), o.kel(json.loads(p.read_text(encoding="utf-8")))
        ce, cy = Counter(ke), Counter(ky)
        rc.append(sum((ce & cy).values()) / max(1, sum(ce.values())))
        sm.append(difflib.SequenceMatcher(None, ke, ky, autojunk=False).ratio() if ke or ky else 1.0)
        if rc[-1] < 0.9:
            dusuk.append((p.stem, round(rc[-1], 2)))
    n = len(rc)
    print(f"{ad}\tN={n}\tkelime_recall_ort {sum(rc)/n:.3f}\trecall>=0.95 {sum(x>=.95 for x in rc)}/{n}\tmin {min(rc):.2f}\tbenzerlik_ort {sum(sm)/n:.3f}\tdusuk {dusuk}")
