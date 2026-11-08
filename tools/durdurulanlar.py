import psutil, sys, collections
devam = len(sys.argv) > 1 and sys.argv[1] == "devam"
HARIC = {"shellexperiencehost.exe", ""}
m = psutil.virtual_memory()
print("RAM", m.percent, "%")
gruplar = collections.Counter()
hedef = []
for p in psutil.process_iter(["pid", "name", "status", "cmdline"]):
    try:
        if p.info["status"] != psutil.STATUS_STOPPED:
            continue
        if (p.info["name"] or "").lower() in HARIC:
            continue
        hedef.append(p)
    except Exception:
        pass
print("hedef", len(hedef))
if devam:
    ok = 0
    for p in hedef:
        try:
            p.resume()
            ok += 1
        except Exception as e:
            print("hata", p.pid, e)
    print("devam ettirilen", ok)
    import time
    time.sleep(5)
    kalan = sum(1 for p in psutil.process_iter(["status", "name"]) if p.info["status"] == psutil.STATUS_STOPPED and (p.info["name"] or "").lower() not in HARIC)
    print("hala durgun", kalan)
    print("RAM", psutil.virtual_memory().percent, "%", "CPU", psutil.cpu_percent(1), "%")
