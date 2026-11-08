import psutil, subprocess
ps = []
for p in psutil.process_iter(["pid", "name", "memory_info"]):
    try:
        if (p.info["name"] or "").lower() in ("svchost.exe", "vmmem", "vmmemwsl", "vmmem.exe"):
            ps.append((p.info["memory_info"].rss, p.info["pid"], p.info["name"]))
    except Exception:
        pass
ps.sort(reverse=True)
out = subprocess.run(["tasklist", "/svc", "/fo", "csv", "/nh"], capture_output=True, text=True, errors="ignore").stdout
svc = {}
for l in out.splitlines():
    parca = [x.strip('"') for x in l.split('","')]
    if len(parca) >= 3:
        try:
            svc[int(parca[1])] = parca[2]
        except Exception:
            pass
for rss, pid, ad in ps[:6]:
    print(round(rss / 2**30, 2), "GB", pid, ad, svc.get(pid, ""))
