import psutil, time
for p in psutil.process_iter(["pid", "ppid", "name", "cmdline", "create_time"]):
    try:
        c = " ".join(p.info["cmdline"] or [])
        if any(a in c for a in ["sira9b_0811", "sira9a_0811", "sira8_0811"]):
            print(p.pid, "ppid", p.info["ppid"], p.info["name"], time.strftime("%H:%M", time.localtime(p.info["create_time"])), c[-60:])
    except Exception:
        pass
