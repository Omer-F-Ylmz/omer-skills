import psutil, json, sys, time, ctypes
DOSYA = r"C:\Projeler\omer-skills\.kos\kopru\log\dinlen.json"
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\dinlen.log", "a", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
mod = sys.argv[1] if len(sys.argv) > 1 else "dur"
DUR = ["egit_surekli.py", "-m borsa egit", "gece_kuyruk.py", "kurulum_tur2", "kurulum_d2.py", "aday2_", "aday_", "sikistir_tum.py", "compact.exe", "envanter_tara"]
YAVAS = ["claude.exe -p", "arka_ajan.py"]
def kirp(q):
    try:
        h = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, q.pid)
        ctypes.windll.psapi.EmptyWorkingSet(h); ctypes.windll.kernel32.CloseHandle(h)
    except Exception: pass
if mod == "dur":
    ram0 = psutil.virtual_memory().percent
    kayit = {"durdurulan": [], "yavaslatilan": []}
    hedef = {}
    for q in psutil.process_iter(["pid", "cmdline", "name"]):
        c = " ".join(q.info["cmdline"] or []) or (q.info["name"] or "")
        if "dinlen.py" in c: continue
        if any(k in c for k in DUR):
            hedef[q.pid] = q
            for ch in q.children(recursive=True): hedef[ch.pid] = ch
    for pid, q in hedef.items():
        try: q.suspend(); kirp(q); kayit["durdurulan"].append(pid)
        except Exception as e: p("durdurulamadi", pid, e)
    for q in psutil.process_iter(["pid", "cmdline"]):
        c = " ".join(q.info["cmdline"] or [])
        if any(k in c for k in YAVAS) and q.pid not in hedef:
            try: q.nice(psutil.IDLE_PRIORITY_CLASS); kayit["yavaslatilan"].append(q.pid)
            except Exception: pass
    json.dump(kayit, open(DOSYA, "w"))
    time.sleep(3)
    p("DUR: durdurulan", len(kayit["durdurulan"]), "yavaslatilan", len(kayit["yavaslatilan"]), "| RAM %", ram0, "->", psutil.virtual_memory().percent, "| CPU %", psutil.cpu_percent(interval=2))
else:
    kayit = json.load(open(DOSYA))
    n = 0
    for pid in kayit["durdurulan"]:
        try: psutil.Process(pid).resume(); n += 1
        except Exception: pass
    for pid in kayit["yavaslatilan"]:
        try: psutil.Process(pid).nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        except Exception: pass
    p("DEVAM: surduruldu", n, "| RAM %", psutil.virtual_memory().percent)
