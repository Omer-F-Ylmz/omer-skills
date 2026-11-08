import os, time, psutil
f = r"C:\Projeler\omer-skills\tmp\bulunan-0811.tsv"
if os.path.exists(f):
    n = sum(1 for _ in open(f, encoding="utf-8", errors="replace"))
    print("bulunan satir", n, "degisim", time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(f))))
c = []
for p in psutil.process_iter(["pid", "cmdline"]):
    try:
        s = " ".join(p.info["cmdline"] or [])
        if "sira3_0811" in s or "claude.exe" in s.lower() and " -p" in s:
            c.append((p.pid, s[:120]))
    except Exception:
        pass
print("surecler", c)
print("RAM", psutil.virtual_memory().percent)
