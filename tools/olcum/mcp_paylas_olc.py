"""MCP-HAFIF-2 hedef 2 ölçümü (claude -p yok): N oturumun her biri kendi stdio MCP kopyasını açar (önce) ↔ tek mcp-proxy
(kurulu uv aracı, stdio→streamable HTTP) N oturuma aynı sunucuyu verir (sonra). Durumsuz iki sunucu (time, fetch); kalite
eşitliği = iki kolda tools/list aynı. Yalnız kendi başlattığı süreç ağaçlarını PID ile kapatır.
  python tools/olcum/mcp_paylas_olc.py [N=5] [cikti.tsv]"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kosucu  # noqa: E402
from mcp_hafif_kabul import anlik, torunlar  # noqa: E402

SUNUCU = {"time": "mcp-server-time", "fetch": "mcp-server-fetch"}
PORT = 8797
INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "olc", "version": "1"}}}
BILDIR = {"jsonrpc": "2.0", "method": "notifications/initialized"}
LISTE = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}


def basla(args):
    return subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            creationflags=kosucu.PENCERESIZ)


def stdio_araclar(p):
    for m in (INIT, BILDIR, LISTE):
        p.stdin.write((json.dumps(m) + "\n").encode())
        p.stdin.flush()
        if "id" in m:
            y = json.loads(p.stdout.readline())
    return sorted(a["name"] for a in y["result"]["tools"])


def http(url, m, oturum=None):
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if oturum:
        h["Mcp-Session-Id"] = oturum
    with urllib.request.urlopen(urllib.request.Request(url, json.dumps(m).encode(), h), timeout=60) as r:
        g = r.read().decode()
        sid = r.headers.get("Mcp-Session-Id") or oturum
    v = [s[5:] for s in g.splitlines() if s.startswith("data:")] or [g]
    return (json.loads(v[-1]) if "id" in m else None), sid


def http_araclar(ad):
    url = f"http://127.0.0.1:{PORT}/servers/{ad}/mcp"
    _, sid = http(url, INIT)
    http(url, BILDIR, sid)
    y, _ = http(url, LISTE, sid)
    return sorted(a["name"] for a in y["result"]["tools"])


def ram(pidler):
    d = anlik()
    hepsi = {q for p in pidler for q in [p, *torunlar(d, p)] if q in d}
    return len(hepsi), sum(d[q][2] for q in hepsi) / 2**20


def kapat(pidler):
    for p in pidler:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p)], capture_output=True, creationflags=kosucu.PENCERESIZ)


def once(n):
    pler = [basla([k]) for _ in range(n) for k in SUNUCU.values()]
    try:
        araclar = {ad: stdio_araclar(p) for p, ad in zip(pler, list(SUNUCU) * n)}
        time.sleep(3)
        return araclar, ram([p.pid for p in pler])
    finally:
        kapat([p.pid for p in pler])


def sonra(n):
    px = basla(["mcp-proxy", "--port", str(PORT), "--transport", "streamablehttp",
                *[x for ad, k in SUNUCU.items() for x in ("--named-server", ad, k)]])
    try:
        for _ in range(60):
            try:
                araclar = {ad: http_araclar(ad) for ad in SUNUCU}
                break
            except OSError:
                time.sleep(1)
        for _ in range(n - 1):  # N oturum: her biri kendi HTTP oturumunu açar (açık bırakılır)
            assert {ad: http_araclar(ad) for ad in SUNUCU} == araclar
        time.sleep(3)
        return araclar, ram([px.pid])
    finally:
        kapat([px.pid])


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    a1, (s1, m1) = once(n)
    a2, (s2, m2) = sonra(n)
    satir = f"{n}\t{s1}\t{m1:.0f}\t{s2}\t{m2:.0f}\t{a1 == a2}\n"
    print("n\tonce_surec\tonce_mb\tsonra_surec\tsonra_mb\taraclar_ayni\n" + satir, end="")
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text("n\tonce_surec\tonce_mb\tsonra_surec\tsonra_mb\taraclar_ayni\n" + satir, encoding="utf-8")
