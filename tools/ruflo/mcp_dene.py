"""Ruflo MCP stdio tek seferlik deneme: python mcp_dene.py liste | cagri <arac> '<json>'... (cwd=.kos/ruflo/calisma)"""
import json, subprocess, sys, os
CWD = "C:/Projeler/omer-skills/.kos/ruflo/calisma"


def kos(cagrilar):
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"}]
    for i, (m, p) in enumerate(cagrilar, 2):
        msgs.append({"jsonrpc": "2.0", "id": i, "method": m, "params": p})
    pr = subprocess.Popen(["ruflo.cmd", "mcp", "start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", cwd=CWD, env={**os.environ}, creationflags=0x08000000)
    out = {}
    for m in msgs:  # her istekten sonra yanıtı bekle: stdin erken kapanırsa sunucu çağrıları düşürür
        pr.stdin.write(json.dumps(m) + "\n"); pr.stdin.flush()
        if "id" in m:
            while m["id"] not in out:
                j = json.loads(pr.stdout.readline() or "{}") if True else {}
                if not j: break
                if "id" in j: out[j["id"]] = j
    pr.stdin.close(); pr.terminate()
    r = type("R", (), {"stderr": ""})
    return out, r.stderr[-400:]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "liste":
        o, e = kos([("tools/list", {})])
        t = o.get(2, {}).get("result", {}).get("tools", [])
        print(len(t), "araç"); print(" ".join(x["name"] for x in t)); print(e)
    else:
        c = [("tools/call", {"name": sys.argv[i], "arguments": json.loads(sys.argv[i + 1])}) for i in range(2, len(sys.argv), 2)]
        o, e = kos(c)
        for k in sorted(o):
            if k > 1: print(k, json.dumps(o[k], ensure_ascii=False)[:700])
        print(e)
