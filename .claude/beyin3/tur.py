"""Kapı sonrası tanı (ayar değil): yanlış/doğru soruları tür ve kaynak türüne göre say; kaynak dosya `beyin.py ara` çıktısında var mı."""
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).parent
sys.path.insert(0, str(D.parent / "beyin2"))
import kapi  # noqa: E402

kapi.CIKTI = D / "kosu"
sayac = Counter()
for t in (2007, 2008):
    qs = [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    d = {p.get("id"): p.get("d", 0) for p in kapi.satirlar(json.loads((kapi.CIKTI / f"hakem{t}-1.json").read_text(encoding="utf-8")))}
    for q in qs:
        ks = [re.sub(r":\d+$", "", k.strip()).replace("\\", "/") for k in q["kaynak"].split(";")]
        tur = ("çok" if q.get("cok") else "tek") + "/" + ("sira" if any("ajan-sira" in k or "SIRA.md" in k for k in ks) else "diğer")
        out = subprocess.run([sys.executable, "tools/beyin.py", "ara", q["soru"]], capture_output=True, text=True, encoding="utf-8",
                             cwd=D.parent.parent).stdout.lower()
        bulundu = all(Path(k).stem.lower().replace("_", "-") in out or Path(k).stem.lower() in out for k in ks)
        sayac[(tur, "doğru" if d.get(q["id"]) else "yanlış", "ilk-aramada" if bulundu else "aramada-yok")] += 1
for k, v in sorted(sayac.items()):
    print(*k, v)
