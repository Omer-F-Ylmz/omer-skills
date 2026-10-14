"""TOKEN-4 A6: köprü (ajan profili) tur başı sabit bağlamın kalem kalem GERÇEK token'ı.
Tek `claude -p` kayıt vekilinden geçer (onek_kayit ile aynı zincir → Headroom 6767); ilk /v1/messages gövdesi + başlıkları
yalnız bellekte tutulur, sonra her kalem için count_tokens(tam) − count_tokens(kalemsiz) farkı alınır. Başlık diske yazılmaz.
  python a6.py [gövde.json | ek_ayar_json] [-- claude ek argümanları]   (gövde verilirse claude -p koşmaz, başlık yoksa yalnız karakter dökümü)"""
import copy, http.client, json, os, re, subprocess, sys, threading, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / ".claude" / "token3"))
import onek_kayit as ok

EK_ARG = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
import cc_profil

CIKTI = KOK / "docs" / "kutuphane" / "olcum" / f"token-4-a6{'-deny' if sys.argv[1:] and sys.argv[1].startswith('{') else '-tools' if EK_ARG else ''}.tsv"
yakala = {}


class V(ok.V):
    def _ilet(self):
        if self.path.startswith("/v1/messages") and "count_tokens" not in self.path:
            n = int(self.headers.get("content-length") or 0)
            g = self.rfile.read(n)
            if len(g) > len(yakala.get("govde", b"")):  # en büyük = ana opus isteği
                    yakala["govde"], yakala["baslik"] = g, {k: v for k, v in self.headers.items()
                                                      if k.lower() not in ("host", "connection", "content-length")}
            self.rfile = __import__("io").BytesIO(g)
        super()._ilet()

    do_POST = do_GET = _ilet


def say(baslik, b):
    g = json.dumps({k: b[k] for k in ("model", "system", "tools", "messages") if k in b}).encode()
    c = http.client.HTTPConnection(*ok.UST, timeout=120)
    c.request("POST", "/v1/messages/count_tokens?beta=true", body=g, headers={**baslik, "content-length": str(len(g))})
    r = c.getresponse()
    v = r.read()
    if r.status != 200:
        raise RuntimeError(f"count_tokens {r.status}: {v[:200]!r}")
    return json.loads(v)["input_tokens"]


def kalemler(b):
    """(ad, kalemsiz gövde, karakter) — her kalem tek başına çıkarılır."""
    for i, t in enumerate(b["tools"]):
        y = copy.deepcopy(b); del y["tools"][i]
        yield f"araç:{t['name']}", y, len(json.dumps(t, ensure_ascii=False))
    for i, s in enumerate(b["system"]):
        y = copy.deepcopy(b); y["system"][i]["text"] = "."
        yield f"sistem[{i}]:{s['text'][:40]!r}", y, len(s["text"])
    for mi, m in enumerate(b["messages"]):
        if not isinstance(m["content"], list):
            continue
        for ci, c in enumerate(m["content"]):
            t = c.get("text", "")
            # kanca bloğu tek metin: alt parçalara böl
            sinir = [0] + [x.start() for x in re.finditer(
                r"SessionStart[^\n]{0,40}hook|<context_window_protection>|<EXTREMELY_IMPORTANT>|# \[[^\]]+\] recent context|"
                r"# Work state|Codebase map|Contents of [^\n]*", t) if x.start() > 0] + [len(t)]
            for a, z in zip(sinir, sinir[1:]):
                y = copy.deepcopy(b)
                y["messages"][mi]["content"][ci]["text"] = (t[:a] + t[z:]) or "."
                yield f"mesaj[{mi}.{ci}]:{t[a:a+50]!r}", y, z - a


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ek = json.loads(sys.argv[1]) if sys.argv[1:] and sys.argv[1].startswith("{") else None
    if sys.argv[1:] and sys.argv[1] != "--" and not ek:
        yakala["govde"] = Path(sys.argv[1]).read_bytes()
    else:
        ok.etiket = "a6"; ok.DIZ.mkdir(parents=True, exist_ok=True)
        s = ok.http.server.ThreadingHTTPServer(("127.0.0.1", 0), V)
        threading.Thread(target=s.serve_forever, daemon=True).start()
        ayar = {**(ek or {}), "env": {"ANTHROPIC_BASE_URL": f"http://127.0.0.1:{s.server_port}"}}
        a, e = cc_profil.kur("ajan", ek_ayar=ayar, gecici=ok.DIZ.parent / "profil")
        argv = [r"C:\Users\pc\.local\bin\claude.exe", "-p", "--output-format", "json", "--model", "opus",
                "--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *a, *EK_ARG]
        t = time.time()
        p = subprocess.run(argv, input="Yalnız 'tamam' yaz, araç kullanma.".encode(), capture_output=True, cwd=str(KOK),
                           env={**os.environ, **e}, creationflags=0x08000000, timeout=300)
        u = json.loads(p.stdout)["usage"]
        print(f"claude -p {time.time()-t:.0f} sn · g {u.get('input_tokens')} cw {u.get('cache_creation_input_tokens')} "
              f"cr {u.get('cache_read_input_tokens')}")
    b = json.loads(yakala["govde"])
    tam = say(yakala["baslik"], b) if "baslik" in yakala else None
    satir = [("TOPLAM", tam, len(yakala["govde"]))]
    for ad, y, kar in kalemler(b):
        satir.append((ad, tam - say(yakala["baslik"], y) if tam else None, kar))
    with open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        f.write("kalem\ttoken\tkarakter\n")
        for ad, tk, kar in sorted(satir, key=lambda x: -(x[1] or x[2])):
            f.write(f"{ad}\t{tk}\t{kar}\n")
    print("yazıldı", CIKTI, "· toplam token", tam, "· kalem", len(satir) - 1)
