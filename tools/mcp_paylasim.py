r"""Paylaşımlı MCP (TOKEN-7c/7a): durumsuz stdio MCP'leri tek mcp-proxy sürecinde 127.0.0.1'de koşar,
CC oturumları bunlara http URL'siyle bağlanır (oturum başı süreç yerine tek kopya).

Kullanım:
  python tools/mcp_paylasim.py yapilandir <kaynak.json> <cikti.json>   # proxy named-server config (env değerleri yalnız dosyaya)
  python tools/mcp_paylasim.py karsilastir <kaynak.json> <port> [ad..]  # stdio tools/list == http tools/list ?
Env DEĞERİ hiçbir modda basılmaz.
"""
import json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(__file__))

PORT = 47800
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


if __name__ == "__main__":
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
