import os, glob, time, json
kok = os.path.expanduser(r"~\.claude\projects")
fs = sorted(glob.glob(os.path.join(kok, "*", "*.jsonl")), key=os.path.getmtime)[-4:]
for f in fs:
    print(time.strftime("%d %H:%M:%S", time.localtime(os.path.getmtime(f))), os.path.getsize(f), f[-90:])
f = fs[-1]
satir = open(f, encoding="utf-8", errors="replace").read().splitlines()
print("satir", len(satir))
for l in satir[-6:]:
    try:
        d = json.loads(l)
        m = d.get("message", {})
        c = m.get("content")
        if isinstance(c, list):
            c = " | ".join(str(x.get("text") or x.get("name") or x.get("content") or "")[:300] for x in c)
        print(d.get("type"), str(c)[:400])
    except Exception as e:
        print("?", l[:200])
