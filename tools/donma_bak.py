import psutil, os, time, sys, subprocess as s
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True); print("arka planda basladi"); sys.exit(0)
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\donma_bak.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=out)
p("cekirdek mantiksal", psutil.cpu_count(), "fiziksel", psutil.cpu_count(logical=False))
p("cpu %", psutil.cpu_percent(interval=3), "| RAM %", psutil.virtual_memory().percent, "| swap %", psutil.swap_memory().percent)
a = psutil.disk_io_counters(); time.sleep(5); b = psutil.disk_io_counters()
p("disk okuma MB/s", round((b.read_bytes - a.read_bytes) / 5e6, 1), "yazma MB/s", round((b.write_bytes - a.write_bytes) / 5e6, 1))
for pid in [12800, 21468]:
    try:
        q = psutil.Process(pid); p("PID", pid, q.name(), "nice", q.nice(), " ".join(q.cmdline())[:220], "| cocuk:", len(q.children(recursive=True)))
    except Exception as e: p("PID", pid, e)
# (2)+(3) oncelik dusur: borsa egit agaci + envanter_tara + kurulum betikleri
hedef = []
for q in psutil.process_iter(["pid", "cmdline", "name"]):
    try:
        c = " ".join(q.info["cmdline"] or [])
        if ("borsa egit" in c or "-m borsa" in c or "envanter_tara" in c or "kurulum_" in c or "kur_hepsi" in c) and "donma_bak" not in c:
            hedef.append(q); hedef += q.children(recursive=True)
    except Exception: pass
n = 0
for q in {x.pid: x for x in hedef}.values():
    try:
        if q.nice() == psutil.NORMAL_PRIORITY_CLASS: q.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS); n += 1
    except Exception: pass
p("BELOW_NORMAL yapilan surec:", n)
for q in psutil.process_iter():
    try: q.cpu_percent(None)
    except Exception: pass
time.sleep(3)
ps = []
for q in psutil.process_iter(["pid", "name", "memory_info", "nice", "cmdline", "ppid"]):
    try: ps.append((round(q.cpu_percent(None)), q.info["pid"], q.info["name"], q.info["memory_info"].rss // (1 << 20), q.info["nice"], q.info["ppid"], " ".join(q.info["cmdline"] or [])[:140]))
    except Exception: pass
p("== en cok CPU"); [p(r) for r in sorted(ps, reverse=True)[:15]]
p("== en cok RAM"); [p(r) for r in sorted(ps, key=lambda r: -r[3])[:10]]
p("BITTI")
