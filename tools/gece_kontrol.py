import psutil, os, json, time
K = r"C:\Projeler\omer-skills"
LOG = os.path.join(K, r".kos\kopru\log\cc_gorev-kapanis-gece-0811_0450.jsonl")
cc = [p.pid for p in psutil.process_iter(["pid", "cmdline"]) if p.info["cmdline"] and "ca17c5a5" in " ".join(p.info["cmdline"])]
print("CC canli", cc, "| RAM", psutil.virtual_memory().percent, "%")
if os.path.exists(LOG):
    print("log degisim", time.strftime("%H:%M", time.localtime(os.path.getmtime(LOG))), os.path.getsize(LOG))
    son = None
    for l in open(LOG, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(l)
        except Exception:
            continue
        if d.get("type") == "result":
            son = d
    if son:
        print("SONUC", son.get("subtype"), "turn", son.get("num_turns"), str(son.get("result"))[:600])
f = os.path.join(K, r"rapor\gece-0811-ilerleme.md")
print("ILERLEME:", open(f, encoding="utf-8", errors="replace").read()[-1500:] if os.path.exists(f) else "YOK")
g = os.path.join(K, r".kos\kopru\log\gece_kuyruk.log")
print("KUYRUK:", "".join(open(g, encoding="utf-8", errors="replace").readlines()[-4:]))
