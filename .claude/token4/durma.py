"""TOKEN-4 A2: durma adımlarının (cw=0, önbelleksiz girdi ≥3k) kırılımı."""
import json, sys
from collections import Counter
from datetime import date
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
GUN = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
k = Counter(); g = Counter(); ard = Counter(); cr0 = Counter(); ornek = []
for j in (Path.home() / ".claude/projects").rglob("*.jsonl"):
    if date.fromtimestamp(j.stat().st_mtime).isoformat() < GUN: continue
    gor, onceki = set(), None
    for s in j.open(encoding="utf-8", errors="replace"):
        try: o = json.loads(s)
        except ValueError: continue
        m = o.get("message")
        if o.get("type") != "assistant" or not isinstance(m, dict) or not isinstance(m.get("usage"), dict) or m.get("id") in gor: continue
        if not str(o.get("timestamp", "")).startswith(GUN): continue
        gor.add(m.get("id")); u = m["usage"]
        d = not u.get("cache_creation_input_tokens") and (u.get("input_tokens") or 0) >= 3000
        anah = (j.parent.name[:28], "alt" if "subagents" in str(j) or o.get("isSidechain") else "ana", m.get("model", "")[:18], o.get("entrypoint", ""))
        k[(anah, d)] += 1
        if d:
            g[anah] += u["input_tokens"]; ard[onceki] += 1; cr0["cr=0" if not u.get("cache_read_input_tokens") else "cr>0"] += 1
            if len(ornek) < 4 and u.get("cache_read_input_tokens"): ornek.append((j.name[:12], u))
        onceki = d
print("durma sonrası önceki adım durma mı:", dict(ard), "|", dict(cr0))
for a, v in g.most_common(12):
    print(v, k[(a, True)], "/", k[(a, True)] + k[(a, False)], a)
for o in ornek: print(o)
