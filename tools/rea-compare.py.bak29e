import json, subprocess, os, sys, threading
W = r"C:\Projeler\omer-skills\tools\rea-mcp-compact.mjs"
NODE = r"C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
env = {k: v for k, v in os.environ.items() if not k.startswith("REA_MCP")}
p = subprocess.Popen([NODE, W], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, creationflags=0x08000000)
_t = threading.Timer(60, p.kill); _t.daemon = True; _t.start()
def gonder(m): p.stdin.write((json.dumps(m) + "\n").encode()); p.stdin.flush()
def al(i):
    while True:
        s = p.stdout.readline()
        if not s: return None
        m = json.loads(s)
        if m.get("id") == i: return m
gonder({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}); al(1)
gonder({"jsonrpc":"2.0","method":"notifications/initialized"})
c = json.load(open(r"C:/Projeler/omer-skills/.kos/kopru/ara/rea5b-caps.json"))
d = [json.loads(x["result"]["content"][0]["text"]) for x in c]
modes = {"c": lambda: {"before": {"inspection": d[0]["normalized_result"]}, "after": {"inspection": d[1]["normalized_result"]}},
         "d": lambda: {"before": {"inspection": d[0]}, "after": {"inspection": d[1]}},
         "a": lambda: {"before": d[0], "after": d[1]},
         "b": lambda: {"before": d[0]["normalized_result"], "after": d[1]["normalized_result"]}}
args = modes[sys.argv[1]]()
gonder({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"compare_web_captures","arguments":args}})
r = al(2)
t = r["result"]["content"][0]["text"]
print("isError", r["result"].get("isError"), len(t))
print(json.dumps(t[:int(sys.argv[2])]))
p.kill()
