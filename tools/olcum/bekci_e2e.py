"""MCP-HAFIF-2: bekçi yeniden asılmayı gerçek zamanda yakalıyor mu (mock'suz süre, gerçek port, gerçek taskkill).
Sahte proxy: /status'u 30 sn sunar, sonra portu kapatıp canlı kalır (12 Eki 18:42 asılma biçimi); ikinci başlatma hemen çıkar.
Beklenen: ~30 sn + 20 yoklama (≈5-6 dk) sonra 1. sahte öldürülür, bekçi 2. kez başlatır. python tools/olcum/bekci_e2e.py [port]"""
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mcp_paylasim as mp  # noqa: E402

SAHTE = """import http.server, sys, threading, time
from pathlib import Path
s = Path(sys.argv[2]); n = int(s.read_text()) + 1 if s.exists() else 1; s.write_text(str(n))
if n > 1: sys.exit()
h = http.server.HTTPServer(("127.0.0.1", int(sys.argv[1])), http.server.BaseHTTPRequestHandler)
h.RequestHandlerClass.do_GET = lambda r: (r.send_response(200), r.end_headers())
threading.Thread(target=h.serve_forever, daemon=True).start()
time.sleep(30); h.shutdown(); h.server_close()
time.sleep(3600)
"""

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 47899
    d = Path(tempfile.mkdtemp(prefix="bekci-e2e-"))
    (d / "sahte.py").write_text(SAHTE, encoding="utf-8")
    gercek = subprocess.Popen
    mp.subprocess.Popen = lambda a, **k: gercek(
        [sys.executable, str(d / "sahte.py"), str(port), str(d / "sayac")], **k) if a[0] == str(mp.PROXY) else gercek(a, **k)
    t = time.time()
    mp.bekci(str(d / "sunucular.json"), port, turlar=2)
    sure, n = round(time.time() - t), int((d / "sayac").read_text())
    print(f"sure_sn={sure} baslatma={n} asili_olduruldu={'EVET' if n == 2 and sure >= 300 else 'HAYIR'}", flush=True)
    sys.exit(0 if n == 2 and sure >= 300 else 1)
