"""TOKEN-8 f2b iş 4 keşif (çağrısız): 7 günlük ana transcript'lerde kanca ekleri — tür/kanca adı başına sayı, kr, istek başına."""
import json, sys, time
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf8")
S = time.time() - 7 * 86400
n, kr, istek = Counter(), Counter(), 0
for f in (Path.home() / ".claude/projects").glob("*/*.jsonl"):
    if f.stat().st_mtime < S: continue
    for s in f.read_text(encoding="utf8", errors="replace").splitlines():
        if '"type":"assistant"' in s: istek += 1
        if '"hook_' not in s: continue
        try: at = json.loads(s).get("attachment") or {}
        except ValueError: continue
        t = at.get("type", "")
        if not t.startswith("hook_"): continue
        k = f'{t}|{at.get("hookEvent","")}|{str(at.get("hookName",""))[:40]}'
        n[k] += 1; kr[k] += len(str(at.get("content") or at.get("additionalContext") or at.get("stdout") or ""))
print("asistan_istek", istek)
for k, v in kr.most_common(15): print(f"{v:>10} kr {n[k]:>6} adet {v//max(istek,1):>5} kr/istek  {k}")
