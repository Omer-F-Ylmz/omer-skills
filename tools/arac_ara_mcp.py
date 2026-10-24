"""BEYIN-ARAC-KART-1: arac_ara MCP sunucusu (stdio, satır-ayraçlı JSON-RPC, bağımlılıksız). CC · Desktop · Hermes aynı kapıyı kullanır.
  python tools/arac_ara_mcp.py [--kok DİZİN --kart DOSYA --db DOSYA]   (bayraklar yalnız test için; varsayılan: omer-skills yolları)
Araçlar: arac_ara(sorgu, n, bolum, tam) · arac_sec(gorev, tur)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arac_ara  # noqa: E402

ARACLAR = [
    {"name": "arac_ara", "description": "Kurulu skill/ajan/MCP/CLI/betik kartlarında ara: ilk kartlar + yalnız ilgili bölüm. tam=<ad> verilirse o aracın tam kaynak metni.",
     "inputSchema": {"type": "object", "properties": {"sorgu": {"type": "string"}, "n": {"type": "integer", "default": 12}, "bolum": {"type": "integer", "default": 3},
                                                       "tam": {"type": "string", "description": "tam metni istenen araç adı"}}}},
    {"name": "arac_sec", "description": "Görev metni için önerilen tam araç kümesi (kart sırası + geçmişte birlikte başarılı eşler + iş türü tarifi).",
     "inputSchema": {"type": "object", "properties": {"gorev": {"type": "string"}, "tur": {"type": "string"}}, "required": ["gorev"]}},
]


def cagir(ad, a, c):
    if ad == "arac_ara":
        if a.get("tam"):
            return arac_ara.tam(a["tam"], c) or "kart yok: " + a["tam"]
        return arac_ara.metin(arac_ara.ara(a.get("sorgu", ""), c, int(a.get("n", 12)), int(a.get("bolum", 3))))
    if ad == "arac_sec":
        r = arac_ara.sec(a.get("gorev", ""), c, a.get("tur"))
        return " · ".join(r["kume"]) + "\n" + "\n".join(f"{k}: {v}" for k, v in r["kartlar"].items())
    raise KeyError(ad)


def isle(m, c):
    i, y = m.get("id"), m.get("method")
    if y == "initialize":
        return {"jsonrpc": "2.0", "id": i, "result": {"protocolVersion": (m.get("params") or {}).get("protocolVersion", "2024-11-05"),
                                                        "capabilities": {"tools": {}}, "serverInfo": {"name": "arac-ara", "version": "1.0"}}}
    if y == "tools/list":
        return {"jsonrpc": "2.0", "id": i, "result": {"tools": ARACLAR}}
    if y == "tools/call":
        p = m.get("params") or {}
        try:
            return {"jsonrpc": "2.0", "id": i, "result": {"content": [{"type": "text", "text": cagir(p.get("name"), p.get("arguments") or {}, c)}]}}
        except Exception as e:  # istemciye hata olarak dön, süreç ölmesin
            return {"jsonrpc": "2.0", "id": i, "result": {"isError": True, "content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}]}}
    if i is not None:  # bildirim değilse bilinmeyen yöntem
        return {"jsonrpc": "2.0", "id": i, "error": {"code": -32601, "message": f"yöntem yok: {y}"}}
    return None


if __name__ == "__main__":
    a = sys.argv[1:]
    c = {}
    for bayrak, anahtar in (("--kok", "kok"), ("--kart", "kart"), ("--db", "db")):
        if bayrak in a:
            c[anahtar] = Path(a[a.index(bayrak) + 1])
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    for satir in sys.stdin:
        if satir.strip():
            try:
                r = isle(json.loads(satir), c or None)
            except ValueError:
                r = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "JSON ayrıştırılamadı"}}
            if r:
                print(json.dumps(r, ensure_ascii=False), flush=True)
