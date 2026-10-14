"""TOKEN-3 K10: ardışık N kısa `claude -p` (ajan profili) isteğini yerel kayıt vekilinden geçirip (→ Headroom 6769, zincir aynı)
gövdeleri .claude/token3/istek/ altına yazar. Global ayara dokunmaz: taban URL yalnız çocuğun --settings env'inde.
  python onek_kayit.py <etiket> [N=2] [ek_ayar_json]"""
import http.client, http.server, json, os, subprocess, sys, threading, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
import cc_profil

DIZ = Path(__file__).parent / "istek"
UST = ("127.0.0.1", 6769)
sayac = [0]


class V(http.server.BaseHTTPRequestHandler):
    def _ilet(self):
        n = int(self.headers.get("content-length") or 0)
        govde = self.rfile.read(n) if n else None
        if govde and self.path.startswith("/v1/messages") and "count_tokens" not in self.path:
            sayac[0] += 1
            (DIZ / f"{etiket}-{sayac[0]:02d}.json").write_bytes(govde)
        c = http.client.HTTPConnection(*UST, timeout=600)
        h = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection")}
        c.request(self.command, self.path, body=govde, headers=h)
        r = c.getresponse()
        self.send_response(r.status)
        for k, v in r.getheaders():
            if k.lower() not in ("transfer-encoding", "content-length", "connection"):
                self.send_header(k, v)
        self.send_header("connection", "close")
        self.end_headers()
        while b := r.read1(65536):
            self.wfile.write(b)
            self.wfile.flush()
        self.close_connection = True

    do_POST = do_GET = _ilet

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    etiket, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2
    ek = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    DIZ.mkdir(parents=True, exist_ok=True)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), V)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    ayar = {**ek, "env": {**ek.get("env", {}), "ANTHROPIC_BASE_URL": f"http://127.0.0.1:{s.server_port}"}}
    # gecici ayrı: canlı ajan_sira'nın cc_profil/ajan-ayar.json'unu ezmesin
    a, e = cc_profil.kur("ajan", ek_ayar=ayar, gecici=Path(__file__).parent / "profil")
    argv = [r"C:\Users\pc\.local\bin\claude.exe", "-p", "--output-format", "json", "--model", "opus",
            "--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *a]
    for i in range(n):
        t = time.time()
        p = subprocess.run(argv, input="Yalnız 'tamam' yaz, araç kullanma.".encode(), capture_output=True, cwd=str(KOK),
                           env={**os.environ, **e}, creationflags=0x08000000, timeout=300)
        try:
            u = json.loads(p.stdout)["usage"]
            print(f"koşu {i+1}: {time.time()-t:.0f} sn · g {u.get('input_tokens')} cw {u.get('cache_creation_input_tokens')} "
                  f"cr {u.get('cache_read_input_tokens')} ç {u.get('output_tokens')}")
        except Exception as x:
            print(f"koşu {i+1}: rc {p.returncode} çıktı okunamadı {x!r} {p.stdout[:200]!r} {p.stderr[:200]!r}")
    print("istek dosyası:", sayac[0])
