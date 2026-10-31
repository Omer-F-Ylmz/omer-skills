# TUR 22: tur22 kartlarini docs/usta-kart/usta.jsonl'e birlestir (normalize ad ile dedup)
import json, re
from pathlib import Path
K = Path(r"C:\Projeler\omer-skills")
D = K / ".kos/kopru/ogren/video-izle-kur-1"
U = K / "docs/usta-kart/usta.jsonl"
n = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())
var = set()
for l in U.read_text(encoding="utf-8").splitlines():
    try: var.add(n(json.loads(l)["ad"]))
    except Exception: pass
yeni, eklendi = [], []
for f in ["usta-tur22.jsonl"]:
    for l in (D / f).read_text(encoding="utf-8").splitlines():
        l = l.strip()
        if not l: continue
        a = n(json.loads(l)["ad"])
        if a in var: continue
        var.add(a); yeni.append(l); eklendi.append(json.loads(l)["ad"])
with open(U, "a", encoding="utf-8") as fo:
    for l in yeni: fo.write(l + "\n")
print(f"EKLENEN {len(yeni)}:", " | ".join(eklendi))
print("usta.jsonl satir:", len(U.read_text(encoding='utf-8').splitlines()))
