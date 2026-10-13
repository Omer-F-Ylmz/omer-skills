"""stdio MCP açılış ölçümü: initialize ve tools/list yanıt süresi + hazır anda süreç ağacı RAM'i (WorkingSet toplamı).
Ağaç sonunda PID ile /T kapatılır (uvx/cmd zincirinde torun kalmasın). Pencere açmaz.
  python tools/olcum/mcp_acilis.py <etiket> <n> -- <komut> [arg...]   → her koşu bir JSON satırı (stdout)"""
import json
import subprocess
import sys
import threading
import time

GIZLI = 0x08000000


def agac(kok):
    """kok pid'in alt ağacı: (süreç sayısı, WorkingSet MB toplamı)."""
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "Get-CimInstance Win32_Process | % { \"$($_.ProcessId) $($_.ParentProcessId) $($_.WorkingSetSize)\" }"],
                       capture_output=True, text=True, creationflags=GIZLI)
    cocuk, ws = {}, {}
    for s in r.stdout.split("\n"):
        p = s.split()
        if len(p) == 3:
            pid, ebeveyn, w = map(int, p)
            cocuk.setdefault(ebeveyn, []).append(pid)
            ws[pid] = w
    yigin, gorulen = [kok], set()
    while yigin:
        pid = yigin.pop()
        if pid in gorulen or pid not in ws:
            continue
        gorulen.add(pid)
        yigin += cocuk.get(pid, [])
    return len(gorulen), round(sum(ws[p] for p in gorulen) / 2**20)


def kos(komut, sinir=300):
    t0 = time.time()
    p = subprocess.Popen(komut, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, encoding="utf-8", errors="replace", bufsize=1, creationflags=GIZLI)
    yanit = {}
    olay = threading.Event()

    def oku():
        for satir in p.stdout:
            try:
                m = json.loads(satir)
            except ValueError:
                continue
            if isinstance(m, dict) and m.get("id") in (1, 2):
                yanit[m["id"]] = (round(time.time() - t0, 1), m)
                olay.set()
    threading.Thread(target=oku, daemon=True).start()

    def bekle(i):
        while i not in yanit and time.time() - t0 < sinir and p.poll() is None:
            olay.wait(0.5); olay.clear()
        return yanit.get(i)
    try:
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "mcp-acilis", "version": "1"}}}) + "\n")
        p.stdin.flush()
        ini = bekle(1)
        if ini is None:
            return {"durum": "INIT-YOK", "sure": round(time.time() - t0, 1)}
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n")
        p.stdin.flush()
        tl = bekle(2)
        if tl is None:
            return {"durum": "TOOLS-YOK", "init": ini[0]}
        time.sleep(3)  # hazır sonrası ilk yerleşme
        n, mb = agac(p.pid)
        return {"durum": "OK", "init": ini[0], "tools": tl[0], "surec": n, "ram_mb": mb,
                "araclar": sorted(a["name"] for a in tl[1].get("result", {}).get("tools", []))}
    finally:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, creationflags=GIZLI)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ayrac = sys.argv.index("--")
    etiket, n, komut = sys.argv[1], int(sys.argv[2]), sys.argv[ayrac + 1:]
    for i in range(n):
        print(json.dumps({"etiket": etiket, "kosu": i + 1, **kos(komut)}, ensure_ascii=False), flush=True)
