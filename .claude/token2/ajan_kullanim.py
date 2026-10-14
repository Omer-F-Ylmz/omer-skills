"""K2: transkriptlerde Agent/Task subagent_type kullanım sayısı (14 gün) — ajan profili için tut listesi."""
import json, time, collections
from pathlib import Path
sinir = time.time() - 14 * 86400
say = collections.Counter(); oturum = collections.Counter(); dosya = 0
for f in (Path.home() / ".claude/projects").glob("*/*.jsonl"):
    if f.stat().st_mtime < sinir: continue
    dosya += 1; gor = set()
    for l in f.open(encoding="utf-8", errors="ignore"):
        if '"subagent_type"' not in l: continue
        try: d = json.loads(l)
        except Exception: continue
        for c in (d.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in ("Agent", "Task"):
                t = (c.get("input") or {}).get("subagent_type", "?"); say[t] += 1; gor.add(t)
    for t in gor: oturum[t] += 1
print("dosya", dosya, "toplam_cagri", sum(say.values()), "farkli", len(say))
for t, n in say.most_common(40): print(n, oturum[t], t)
