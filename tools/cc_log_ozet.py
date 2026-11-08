import json, sys, os, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
f = sys.argv[1]
print("degisim", time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(f))), "boyut", os.path.getsize(f))
olay = []
for l in open(f, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(l)
    except Exception:
        olay.append(("ham", l[:200])); continue
    t = d.get("type")
    if t == "system" and d.get("subtype") == "init":
        olay.append(("init", "session " + str(d.get("session_id")) + " arac " + str(len(d.get("tools") or [])) + " mcp " + str(len(d.get("mcp_servers") or []))))
    elif t == "assistant":
        for c in d["message"].get("content", []):
            if c.get("type") == "tool_use":
                olay.append(("arac", c["name"] + " " + json.dumps(c.get("input"), ensure_ascii=False)[:160]))
            elif c.get("type") == "text":
                olay.append(("metin", c["text"][:200]))
        u = d["message"].get("usage", {})
        olay.append(("ctx", u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("input_tokens", 0)))
    elif t == "result":
        olay.append(("SONUC", str(d.get("subtype")) + " " + str(d.get("result"))[:500]))
ctx = [x[1] for x in olay if x[0] == "ctx"]
print("son ctx", ctx[-1] if ctx else None, "| tur", len(ctx))
for k, v in [x for x in olay if x[0] != "ctx"][-int(sys.argv[2] if len(sys.argv) > 2 else 8):]:
    print(k, "|", v)
