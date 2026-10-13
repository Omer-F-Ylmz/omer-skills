"""İş 4 izleme (çağrısız): transcript'lerde context-mode kullanım oranı = ctx_* / (ctx_* + Bash + Read + Grep + Glob),
ve Skill çağrısı olan oturum payı. Uygula öncesi taban, sonrası aynı komut; oran düşerse onay betiği --geri.
  python ctx_oran.py <başlangıç YYYY-MM-DD> [bitiş YYYY-MM-DD]"""
import json, sys
from datetime import datetime
from pathlib import Path

bas = datetime.fromisoformat(sys.argv[1]).timestamp()
bit = datetime.fromisoformat(sys.argv[2]).timestamp() if len(sys.argv) > 2 else 1e12
ctx = veri = oturum = skill_oturum = 0
for p in (Path.home() / ".claude" / "projects").rglob("*.jsonl"):
    if "subagents" in p.parts or not bas <= p.stat().st_mtime < bit:
        continue
    adlar = []
    for s in p.open(encoding="utf-8", errors="replace"):
        if '"tool_use"' not in s:
            continue
        try:
            o = json.loads(s)
        except ValueError:
            continue
        icerik = (o.get("message") or {}).get("content")
        if o.get("type") == "assistant" and isinstance(icerik, list):
            adlar += [c.get("name", "") for c in icerik if c.get("type") == "tool_use"]
    if not adlar:
        continue
    oturum += 1
    skill_oturum += "Skill" in adlar
    ctx += sum("ctx_" in a for a in adlar)
    veri += sum(a in ("Bash", "Read", "Grep", "Glob") or "ctx_" in a for a in adlar)
print(f"oturum {oturum} · ctx {ctx}/{veri} = {ctx / max(veri, 1):.3f} · Skill'li oturum {skill_oturum}/{oturum} = {skill_oturum / max(oturum, 1):.3f}")
