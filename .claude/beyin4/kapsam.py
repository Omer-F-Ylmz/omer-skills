"""İlk `beyin ara` çıktısı cevabı içeriyor mu (model yok): python .claude/beyin4/kapsam.py 2014 2015"""
import json
import subprocess
import sys
from pathlib import Path

import kayip

D = Path(__file__).parent
for t in map(int, sys.argv[1:]):
    qs = [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    ok, kar, yok = 0, 0, []
    for q in qs:
        out = subprocess.run([sys.executable, "tools/beyin.py", "ara", q["soru"]], capture_output=True, text=True,
                             encoding="utf-8", cwd=kayip.KOK).stdout.lower().replace("\\", "/")
        kar += len(out)
        if all(kayip.cevap_var(p, out) for p in kayip.parcalar(q)):
            ok += 1
        else:
            yok.append(q["id"])
    print(t, f"{ok}/{len(qs)} ilk-arama kapsam; ort {kar // len(qs)} karakter; yok {yok}")
