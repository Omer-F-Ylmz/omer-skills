"""K12 salt-okur: bugünkü (HH:MM'den beri) alt ajan transkriptleri — tür, iş, adım, ağırlıklı token, dönüş boyu.
  python alt_ajan.py [HH:MM=00:00]
Ağırlık token_dagilim.py ile aynı: g + 1.25·cw + 0.1·cr + 5·ç. dönüş = son asistan metninin karakter sayısı."""
import json, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PROJ = Path.home() / ".claude" / "projects"
hh, mm = (sys.argv[1] if len(sys.argv) > 1 else "00:00").split(":")
esik = datetime.now().replace(hour=int(hh), minute=int(mm), second=0).timestamp()
satirlar, tur = [], defaultdict(lambda: [0, 0.0])
for j in PROJ.rglob("subagents/*.jsonl"):
    if j.stat().st_mtime < esik:
        continue
    meta = {}
    mj = j.with_suffix(".meta.json")
    if mj.exists():
        meta = json.loads(mj.read_text(encoding="utf-8"))
    gor, ag, ilk, son, n, model = set(), 0.0, 0.0, "", 0, "?"
    for s in j.open(encoding="utf-8", errors="replace"):
        try:
            o = json.loads(s)
        except ValueError:
            continue
        m = o.get("message") if isinstance(o, dict) else None
        if not isinstance(m, dict) or o.get("type") != "assistant":
            continue
        # dönüş ya düz metin ya da SubagentHandback aracının girdisi
        metin = "".join(b.get("text", "") if b.get("type") == "text" else json.dumps(b.get("input"), ensure_ascii=False)
                        for b in m.get("content") or [] if isinstance(b, dict) and (b.get("type") == "text" or b.get("name") == "SubagentHandback"))
        if metin:
            son = metin
        u = m.get("usage")
        if not isinstance(u, dict) or m.get("id") in gor:
            continue
        gor.add(m.get("id"))
        g, cw, cr, c = (u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
        a = g + 1.25 * cw + 0.1 * cr + 5 * c
        if not n:
            ilk = a
        n += 1
        ag += a
        model = (m.get("model") or "?").replace("claude-", "")[:12]
    if not n:
        continue
    t = meta.get("agentType", "?")
    tur[t][0] += 1
    tur[t][1] += ag
    proje = j.parts[len(PROJ.parts)][-14:]
    satirlar.append((ag, t, proje, j.parent.parent.name[:8], n, ilk, len(son), model, (meta.get("description") or "")[:48]))
T = sum(r[0] for r in satirlar)
print(f"alt ajan {len(satirlar)} · ağırlıklı {T/1e6:.2f}M · 1. adım toplamı {sum(r[5] for r in satirlar)/1e6:.2f}M")
print("tür (n, M):", " · ".join(f"{k} {n} {a/1e6:.2f}" for k, (n, a) in sorted(tur.items(), key=lambda x: -x[1][1])))
print("ag_k\ttur\tproje\tana\tadim\tilk_k\tdonus\tmodel\tis")
for r in sorted(satirlar, reverse=True):
    print(f"{r[0]/1e3:.0f}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]/1e3:.0f}\t{r[6]}\t{r[7]}\t{r[8]}")
