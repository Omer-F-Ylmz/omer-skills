"""TOKEN-8 f2b iş 2 çağrısız tarama: 7 günlük transcript'lerde (a) Agent subagent_type kullanımı,
(b) agent_listing_delta ekleri (ilk + oturum içi delta) sayı/boyut, (c) ilk istek girdisine oranı."""
import json, sys, time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
SINIR = time.time() - 7 * 86400
kul, ilk_kr, delta_kr, delta_n, ilk_n = Counter(), [], [], 0, 0
uzun = []  # (delta_n, ilk_kr, toplam delta_kr, dosya)
for f in (Path.home() / ".claude/projects").glob("**/*.jsonl"):
    if f.stat().st_mtime < SINIR:
        continue
    dn = dk = ik = 0
    try:
        satirlar = f.read_text(encoding="utf8", errors="replace").splitlines()
    except OSError:
        continue
    for s in satirlar:
        if '"agent_listing_delta"' not in s and '"subagent_type"' not in s:
            continue
        try:
            a = json.loads(s)
        except ValueError:
            continue
        at = a.get("attachment") or {}
        if at.get("type") == "agent_listing_delta":
            k = len("\n".join(at.get("addedLines") or []))
            if at.get("isInitial"):
                ik += k; ilk_n += 1; ilk_kr.append(k)
            else:
                dn += 1; dk += k; delta_kr.append(k)
        for c in (a.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in ("Agent", "Task"):
                kul[(c.get("input") or {}).get("subagent_type", "general-purpose")] += 1
    delta_n += dn
    if dn:
        uzun.append((dn, ik, dk, f.name))
print("ilk_liste n", ilk_n, "ort_kr", sum(ilk_kr) // max(1, len(ilk_kr)), "max_kr", max(ilk_kr or [0]))
print("oturum_ici_delta n", delta_n, "toplam_kr", sum(delta_kr), "dosya", len(uzun))
for u in sorted(uzun, reverse=True)[:5]:
    print("  delta", u)
print("ajan_kullanim toplam", sum(kul.values()), "farkli", len(kul))
for k, v in kul.most_common(40):
    print(f"  {v:4d} {k}")
