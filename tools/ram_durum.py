import psutil, collections
m = psutil.virtual_memory()
print("RAM", m.percent, "%", round(m.used / 2**30, 1), "/", round(m.total / 2**30, 1), "GB")
print("CPU", psutil.cpu_percent(1), "%")
susp = 0
c = collections.Counter()
for p in psutil.process_iter(["name", "status", "memory_info"]):
    try:
        if p.info["status"] == psutil.STATUS_STOPPED:
            susp += 1
        if p.info["memory_info"]:
            c[p.info["name"]] += p.info["memory_info"].rss
    except Exception:
        pass
print("duraklatilmis surec", susp)
for n, b in c.most_common(10):
    print(n, round(b / 2**30, 2), "GB")
