import json,os,glob,urllib.request,psutil
T=r"C:\Projeler\omer-skills\sosyal-onizleme\tane-premium"
for p in psutil.process_iter(["pid","cmdline","memory_info"]):
    c=" ".join(p.info["cmdline"] or [])
    if "sinema" in c or "ComfyUI" in c or "main.py" in c:print("PROC",p.info["pid"],round(p.info["memory_info"].rss/1e9,1),"GB",c[:160])
try:
    q=json.loads(urllib.request.urlopen("http://127.0.0.1:8188/queue",timeout=5).read())
    print("QUEUE run",len(q.get("queue_running",[])),"pend",len(q.get("queue_pending",[])))
except Exception as e:print("COMFY yok",str(e)[:80])
for d in glob.glob(T+r"\assets\seq\*"):print("SEQ",os.path.basename(d),len(os.listdir(d)),os.path.exists(d+r"\done"))
for f in glob.glob(r"C:\AI\ComfyUI\output\tane\*"):print("OUT",os.path.basename(f),os.path.getsize(f))
vm=psutil.virtual_memory();print("RAM bos GB",round(vm.available/1e9,1),"yuzde",vm.percent)
