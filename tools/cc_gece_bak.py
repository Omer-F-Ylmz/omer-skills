import psutil, os, time
n = 0
for p in psutil.process_iter(["pid", "name", "cmdline", "create_time"]):
    try:
        c = " ".join(p.info["cmdline"] or [])
        if "claude" in (p.info["name"] or "").lower() and (" -p" in c or "--print" in c):
            print("  ornek", c[:200])
            n += 1
            print("CC calisiyor pid", p.pid, time.strftime("%H:%M", time.localtime(p.info["create_time"])))
    except Exception:
        pass
print("CC surec", n)
f = r"C:\Projeler\omer-skills\rapor\gece-0811-ilerleme.md"
print("ilerleme", open(f, encoding="utf-8", errors="replace").read()[-1500:] if os.path.exists(f) else "YOK")
print("RAM", psutil.virtual_memory().percent)
