import json, subprocess, os, sys, threading, time
W = r"C:\Projeler\omer-skills\tools\rea-mcp-compact.mjs"
NODE = r"C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
env = {k: v for k, v in os.environ.items() if not k.startswith("REA_MCP")}
p = subprocess.Popen([NODE, W], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, creationflags=0x08000000)
threading.Timer(int(sys.argv[2]) if len(sys.argv) > 2 else 150, p.kill).start()
def gonder(m): p.stdin.write((json.dumps(m) + "\n").encode()); p.stdin.flush()
def al(i):
    while True:
        s = p.stdout.readline()
        if not s: return None
        m = json.loads(s)
        if m.get("id") == i: return m
t0 = time.time()
gonder({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}); al(1)
gonder({"jsonrpc":"2.0","method":"notifications/initialized"})
print("init", round(time.time()-t0, 1))
gonder({"jsonrpc":"2.0","id":2,"method":"tools/list"})
r = al(2)
for t in r["result"]["tools"]:
    if t["name"] in ("inspect_web_page", "compare_web_captures"):
        print(t["name"], json.dumps(t.get("inputSchema"))[:900])
print("tools", len(r["result"]["tools"]), round(time.time()-t0, 1))
url = sys.argv[1]
import urllib.request, tempfile
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9333
ch = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={port}", "--user-data-dir=" + tempfile.mkdtemp(), "--no-first-run", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
tid = None
for _ in range(40):
    try:
        L = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2))
        pg = [x for x in L if x.get("type") == "page"]
        if pg: tid = pg[0]["id"]; break
    except Exception: pass
    time.sleep(0.5)
print("target", tid, round(time.time()-t0, 1))
caps = []
try:
    for i in (3, 4):
        gonder({"jsonrpc":"2.0","id":i,"method":"tools/call","params":{"name":"inspect_web_page","arguments":{"cdp_endpoint":f"http://127.0.0.1:{port}","target_id":tid,"allowed_origins":[url.rstrip("/")],"observation_ms":1500}}})
        r = al(i)
        s = json.dumps(r)
        print("inspect", i, len(s), round(time.time()-t0, 1), s[:300])
        caps.append(r)
        if i == 3: time.sleep(int(sys.argv[3]) if len(sys.argv) > 3 else 5)
    json.dump(caps, open(r"C:/Projeler/omer-skills/.kos/kopru/ara/rea5b-caps.json", "w"))
finally:
    ch.kill(); p.kill()
