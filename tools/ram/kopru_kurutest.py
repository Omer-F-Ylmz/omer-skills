import subprocess,json,sys,time,psutil
for ad in ["brave-search","code-review","headroom","mcp-fetch","mcp-memory","mcp-sequential-thinking","mcp-time","stitch"]:
    p=subprocess.Popen([sys.executable,"-I","-S",r"C:\Projeler\omer-skills\tools\ram\mcp_koprusu.py",ad],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,creationflags=0x08000000)
    msgs=[{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}},
          {"jsonrpc":"2.0","method":"notifications/initialized"},{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}]
    p.stdin.write("".join(json.dumps(m)+"\n" for m in msgs));p.stdin.flush()
    out=[]
    t=time.time()
    while len(out)<2 and time.time()-t<20:
        l=p.stdout.readline()
        if not l: break
        out.append(json.loads(l))
    rss=psutil.Process(p.pid).memory_info().rss>>20
    n=[len(o["result"]["tools"]) if "result" in o and "tools" in o["result"] else o.get("error") for o in out if o.get("id")==2]
    print(ad,len(out),n,rss,"MB")
    p.kill()
