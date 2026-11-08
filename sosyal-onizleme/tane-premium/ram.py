import psutil
vm=psutil.virtual_memory();print("RAM %",vm.percent,"toplam GB",round(vm.total/1e9,1),"boş GB",round(vm.available/1e9,1))
ps=[]
for p in psutil.process_iter(["pid","name","memory_info","cmdline"]):
    try:ps.append((p.info["memory_info"].rss,p.info["pid"],p.info["name"]," ".join(p.info["cmdline"] or [])[:110]))
    except Exception:pass
for r,pid,n,c in sorted(ps,reverse=True)[:12]:print(round(r/1e9,2),pid,n,c)
