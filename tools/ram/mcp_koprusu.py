"""stdio → paylaşım havuzu (127.0.0.1:47800) köprüsü: Desktop her MCP'yi iki kez başlatır; paylaşımlı sunucular için
komut bu betik olur, gerçek sunucu havuzda tek kopya kalır. python -I -S mcp_koprusu.py <ad> [port]
shortcut: istek başına iş parçacığı, yeniden bağlanma yok; havuz düşerse hata JSON-RPC yanıtı döner, bekçi havuzu kaldırır."""
import json
import sys
import threading
import urllib.request

sys.stdin.reconfigure(encoding="utf-8", errors="replace")  # 0911 20:05: -I ile PYTHONIOENCODING yok sayilir; Windows'ta stdin cp1254 cozuluyor, Turkce yollar bozuluyordu
sys.stdout.reconfigure(encoding="utf-8")
ad = sys.argv[1]
URL = f"http://127.0.0.1:{sys.argv[2] if len(sys.argv) > 2 else 47800}/servers/{ad}/mcp"
oturum = None
kilit = threading.Lock()


def yaz(m):
    with kilit:
        sys.stdout.write(json.dumps(m) + "\n")
        sys.stdout.flush()


def gonder(m):
    global oturum
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if oturum:
        h["mcp-session-id"] = oturum
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL, json.dumps(m).encode(), h), timeout=600)
        oturum = r.headers.get("mcp-session-id") or oturum
        metin = r.read().decode("utf-8", "replace")
        if "event-stream" in (r.headers.get("content-type") or ""):
            for s in metin.splitlines():
                if s.startswith("data:") and s[5:].strip():
                    yaz(json.loads(s[5:]))
        elif metin.strip():
            yaz(json.loads(metin))
    except Exception as e:
        if "id" in m:
            yaz({"jsonrpc": "2.0", "id": m["id"], "error": {"code": -32000, "message": f"havuz: {e}"}})


for satir in sys.stdin:
    if satir.strip():
        m = json.loads(satir)
        if "method" in m and m["method"] == "initialize":
            gonder(m)  # oturum kimliği ilk yanıttan gelmeli; sonrakiler paralel
        else:
            threading.Thread(target=gonder, args=(m,), daemon=True).start()
