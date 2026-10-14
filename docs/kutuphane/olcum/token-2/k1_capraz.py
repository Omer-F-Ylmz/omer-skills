"""TOKEN-2 K1: önbellek durması × Headroom proxy dönüşümleri çapraz tablosu.
Durma = cache_write 0 VE önbelleksiz girdi ≥3000 (token_olc --durma ile aynı tanım)."""
import ast, json, collections as C
from pathlib import Path

H = Path.home() / ".headroom"

def oku(f):
    for l in open(H / f, encoding="utf-8", errors="replace"):
        try:
            yield json.loads(l)
        except Exception:
            pass

def lst(s):
    try:
        return ast.literal_eval(s) if isinstance(s, str) else (s or [])
    except Exception:
        return []

def oran(c):
    return f"{c['d']}/{c['n']} (%{100*c['d']/(c['n'] or 1):.1f})"

# 1) h2a_kayit: mesaj karması önce/sonra
t = C.defaultdict(lambda: {"n": 0, "d": 0})
tr = C.defaultdict(lambda: {"n": 0, "d": 0})
for r in oku("h2a_kayit.jsonl"):
    try:
        cw, un = int(r.get("cache_write_tokens", 0)), int(r.get("uncached_input_tokens", 0))
    except ValueError:
        continue
    d = cw == 0 and un >= 3000
    a, b = lst(r.get("request_messages")), lst(r.get("compressed_messages"))
    deg = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    son = bool(deg) and deg[-1] == len(a) - 1
    sys_deg = any(a[i][0] == "system" for i in deg) if deg else False
    if len(a) != len(b):
        k = "uzunluk_farkli"
    elif not deg:
        k = "degismedi"
    elif son:
        k = "son_mesaj_degisti"
    elif sys_deg and len(deg) == 1:
        k = "yalniz_system_degisti"
    else:
        k = "ara_mesaj_degisti"
    for key in (k, "TUM", f"model={r.get('model')}"):
        t[key]["n"] += 1; t[key]["d"] += d
    for x in lst(r.get("transforms_applied")):
        x = x.split(":")[0] + ":" + x.split(":")[1] if x.count(":") else x
        tr[x]["n"] += 1; tr[x]["d"] += d
print("== h2a_kayit (mesaj karması önce/sonra) ==")
for k, c in sorted(t.items(), key=lambda kv: -kv[1]["n"]):
    print(f"{k:28s} {oran(c)}")
print("-- dönüşüm (ilk 12) --")
for k, c in sorted(tr.items(), key=lambda kv: -kv[1]["n"])[:12]:
    print(f"{k[:40]:40s} {oran(c)}")

# 2) savings_events v2: cache sözlüğü + saved
s = C.defaultdict(lambda: {"n": 0, "d": 0})
for r in oku("savings_events.jsonl"):
    c = r.get("cache")
    if not c:
        continue
    try:
        c = ast.literal_eval(c) if isinstance(c, str) else c
        cw = int(c.get("cw5", 0)) + int(c.get("cw1", 0) or c.get("cw1h", 0) or 0)
        un = int(c.get("un", 0)); sv = int(r.get("saved", 0)); st = int(r.get("saved_tool_schema", 0) or 0)
    except Exception:
        continue
    d = cw == 0 and un >= 3000
    for key in ("TUM", "saved>0" if sv else "saved=0", "tool_schema>0" if st else "tool_schema=0",
                f"deferred>0" if int(r.get("deferred", 0) or 0) else "deferred=0", f"model={r.get('model')}",
                f"gun={r.get('ts','')[:10]}"):
        s[key]["n"] += 1; s[key]["d"] += d
print("== savings_events v2 (proxy cache) ==")
for k, c in sorted(s.items()):
    if not k.startswith("gun=") or c["n"] > 200:
        print(f"{k:28s} {oran(c)}")
