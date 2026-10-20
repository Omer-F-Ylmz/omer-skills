"""Cevap anahtarı örneklemi: rastgele 4 soru için cevap + kaynak satırı (ilk parça, 260 karakter çevresi)."""
import json
import os
import random
import re
from pathlib import Path

D = Path(__file__).parent
for t in (2007, 2008):
    qs = [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    for q in random.Random(t).sample(qs, 2):
        m = re.match(r"(.+):(\d+)", q["kaynak"].split(";")[0].strip().replace("\\", "/"))
        satir = Path(os.path.expanduser(m.group(1))).read_text(encoding="utf-8", errors="replace").split("\n")[int(m.group(2)) - 1]
        print(q["id"], "S:", q["soru"][:150], "\n  C:", q["cevap"][:120], "\n  K:", satir[:260].replace("\n", " "))
