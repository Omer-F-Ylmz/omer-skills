r"""Paylaşımlı MCP (TOKEN-7c/7a): durumsuz stdio MCP'leri tek mcp-proxy sürecinde 127.0.0.1'de koşar,
CC oturumları bunlara http URL'siyle bağlanır (oturum başı süreç yerine tek kopya).

Kullanım:
  python tools/mcp_paylasim.py yapilandir <kaynak.json> <cikti.json>   # proxy named-server config (env değerleri yalnız dosyaya)
  python tools/mcp_paylasim.py karsilastir <kaynak.json> <port> [ad..]  # stdio tools/list == http tools/list ?
  pythonw tools/mcp_paylasim.py bekci <sunucular.json> [port]             # proxy düşerse yeniden başlatır (pid'ler cfg dizininde)
Env DEĞERİ hiçbir modda basılmaz.
"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

PORT = 47800
PROXY = Path.home() / ".local" / "bin" / "mcp-proxy.exe"
# Durumsuz ya da tek dosya/tek hesap durumlu (paylaşımı güvenli) sunucular.
# Oturum başı kalanlar: playwright/puppeteer (tarayıcı), mcp-filesystem/mcp-git (roots/cwd),
# blender/unity/godot (yerel editör köprüsü), codebase-memory-mcp (proje indeksi), http olanlar zaten süreçsiz.
PAYLASIM = ["airtable", "apify", "arxiv", "brave-search", "clickhouse", "code-review", "context7",
            "drizzle-docs", "gsc", "headroom", "hfspace", "hostinger", "jev", "markitdown", "mcp-fetch",
            "mcp-memory", "mcp-sequential-thinking", "mcp-time", "n8n-mcp", "netlify", "stitch"]


def url(ad, port=PORT):
    return f"http://127.0.0.1:{port}/servers/{ad}/mcp"


def proxy_config(sunucular, adlar=PAYLASIM):
    """Kaynak mcpServers'tan yalnız stdio + paylaşım listesindekiler (command/args/env aynen)."""
    return {"mcpServers": {a: {k: v for k, v in sunucular[a].items() if k in ("command", "args", "env")}
                           for a in adlar if a in sunucular and sunucular[a].get("type", "stdio") == "stdio"}}


def donustur(sunucular, adlar, port=PORT):
    """Saf: verilen adları http girdisine çevirir; diğerleri ve ad kümesi aynen kalır."""
    yeni = dict(sunucular)
    for a in adlar:
        if a in yeni and yeni[a].get("type", "stdio") == "stdio":
            yeni[a] = {"type": "http", "url": url(a, port)}
    return yeni


def _post(u, govde, oturum=None):
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if oturum:
        h["mcp-session-id"] = oturum
    r = urllib.request.urlopen(urllib.request.Request(u, json.dumps(govde).encode(), h), timeout=90)
    metin = r.read().decode("utf-8", "replace")
    veri = [json.loads(s[5:]) for s in metin.splitlines() if s.startswith("data:") and s[5:].strip()]
    return r.headers.get("mcp-session-id"), (veri[-1] if veri else (json.loads(metin) if metin.strip() else None))


def araclar_http(u):
    oturum, ini = _post(u, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t7c", "version": "1"}}})
    _post(u, {"jsonrpc": "2.0", "method": "notifications/initialized"}, oturum)
    _, tl = _post(u, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, oturum)
    return sorted(t["name"] for t in tl["result"]["tools"])


def karsilastir(sunucular, port, adlar):
    from mcp_kurutest import dene
    sonuc = {}
    for a in adlar:
        t = sunucular[a]
        s = dene(a, t["command"], t.get("args", []), t.get("env"))
        sa = sorted(s.get("araclar") or [])
        try:
            ha = araclar_http(url(a, port))
        except Exception as e:
            ha, s["hata"] = [], f"http: {type(e).__name__}: {str(e)[:120]}"
        sonuc[a] = {"stdio": len(sa), "http": len(ha), "esit": bool(sa) and sa == ha,
                    "durum": s["durum"], "hata": s.get("hata", "")[:160]}
    return sonuc


def ayakta(port):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/status", timeout=3); return True
    except Exception:
        return False


def bekci(cfg, port=PORT, turlar=None):
    """Port ayaktaysa 15 sn bekler; değilse proxy'yi başlatır, bitmesini (asılıysa öldürülmesini) bekler, 5 sn bekler.
    Her başlatmadan önce port bakılır (çift başlatma yok). Pid'ler: <cfg dizini>/bekci.pid, proxy.pid."""
    dizin = Path(cfg).parent
    (dizin / "bekci.pid").write_text(str(os.getpid()))
    n = 0
    while turlar is None or n < turlar:
        n += 1
        if ayakta(port):
            time.sleep(15)
            continue
        with open(dizin / "proxy.log", "a") as log:
            p = subprocess.Popen([str(PROXY), "--host", "127.0.0.1", "--port", str(port), "--pass-environment",
                                  "--named-server-config", str(cfg)], stdout=log, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, creationflags=0x08000000)
            (dizin / "proxy.pid").write_text(str(p.pid))
            kapali = 0  # süreç canlı ama port 20 yoklama (≈5 dk; açılış ≈2 dk) kapalı = asılı (12 Eki 18:42) → ağacı öldür
            while p.poll() is None:
                time.sleep(15)
                kapali = 0 if ayakta(port) else kapali + 1
                if kapali >= 20:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True,
                                   creationflags=0x08000000)
                    p.wait()
        time.sleep(5)


if __name__ == "__main__":
    if sys.argv[1] == "bekci":  # pythonw: stdout yok, json okunmaz
        bekci(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else PORT)
        sys.exit()
    sys.stdout.reconfigure(encoding="utf-8")
    kip, kaynak = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
    sunucular = kaynak.get("mcpServers", kaynak)
    if kip == "yapilandir":
        cfg = proxy_config(sunucular)
        json.dump(cfg, open(sys.argv[3], "w", encoding="utf-8"), indent=1)
        print(f"{len(cfg['mcpServers'])} sunucu → {sys.argv[3]}")
    elif kip == "karsilastir":
        adlar = sys.argv[4:] or [a for a in PAYLASIM if a in sunucular]
        for a, r in karsilastir(sunucular, int(sys.argv[3]), adlar).items():
            print(f"{'OK ' if r['esit'] else 'FARK'} {a:<24} stdio={r['stdio']:<3} http={r['http']:<3} {r['durum']} {r['hata']}")
