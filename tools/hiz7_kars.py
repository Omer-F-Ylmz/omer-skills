"""VIDEO-HIZ-7: yerel large-v3 tabanına karşı Groq çıktıları (opus24/opus32/flac): kelime benzerliği.
Taban: hiz7/<id>/taban.json (üretim yolu) yoksa yerel_seq.json. Kullanım: hiz7_kars.py"""
import difflib
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parents[1] / ".kos/kopru/ogren/hiz7"


def kel(p):
    j = json.loads(p.read_text(encoding="utf-8"))
    s = j.get("transkript") or j.get("segments")
    return re.sub(r"[^\w\s]", "", " ".join(x.get("t") or x.get("text") for x in s).lower()).split()


toplam = {}
for d in sorted(p for p in D.iterdir() if p.is_dir()):
    tp = next((d / f for f in ("taban.json", "yerel_seq.json") if (d / f).exists()), None)
    if not tp:
        continue
    kt, cik = kel(tp), []
    for a in ("opus24", "opus32", "flac"):
        p = d / f"groq_{a}.json"
        if not p.exists():
            cik.append("-")
            continue
        s = difflib.SequenceMatcher(None, kt, kel(p), autojunk=False).ratio()
        toplam.setdefault(a, []).append(s)
        cik.append(f"{s:.3f}")
    print(d.name, tp.name, *cik, sep="\t")
for a, v in toplam.items():
    print("ORT", a, len(v), round(sum(v) / len(v), 3), "min", round(min(v), 3))
