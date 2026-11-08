import psutil, time, sys
oldur = len(sys.argv) > 1 and sys.argv[1] == "oldur"
anahtar = ["gece_kuyruk.py", "kurulum_tur2.ps1"]
bul = []
for p in psutil.process_iter(["pid", "ppid", "name", "cmdline", "create_time"]):
    try:
        c = " ".join(p.info["cmdline"] or [])
        if any(a in c for a in anahtar) and "kuyruk_cift" not in c:
            bul.append(p)
    except Exception:
        pass
for p in bul:
    c = " ".join(p.info["cmdline"] or [])
    print(p.pid, "ppid", p.info["ppid"], time.strftime("%d %H:%M:%S", time.localtime(p.info["create_time"])), p.info["name"], "|", c[-90:])
if oldur:
    sinir = time.mktime(time.strptime("2026-11-08 04:25:00", "%Y-%m-%d %H:%M:%S"))
    for p in bul:
        if p.info["create_time"] >= sinir:
            for ch in p.children(recursive=True):
                try:
                    ch.kill(); print("oldu cocuk", ch.pid, ch.name())
                except Exception as e:
                    print("hata", ch.pid, e)
            try:
                p.kill(); print("oldu", p.pid)
            except Exception as e:
                print("hata", p.pid, e)
