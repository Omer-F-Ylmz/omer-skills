import psutil, collections
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\ram_top.log", "w", encoding="utf-8")
v = psutil.virtual_memory()
print("RAM %", v.percent, "kullanilan GB", round(v.used / 2**30, 1), "/", round(v.total / 2**30, 1), file=out)
g = collections.Counter(); n = collections.Counter()
for q in psutil.process_iter(["name", "memory_info"]):
    try: g[q.info["name"]] += q.info["memory_info"].rss; n[q.info["name"]] += 1
    except Exception: pass
for k, b in g.most_common(15): print(f"{b/2**20:7.0f} MB x{n[k]:<3} {k}", file=out)
