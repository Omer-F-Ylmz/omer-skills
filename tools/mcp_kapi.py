"""ERİŞİM-TAM-1 araç kapısı: tek stdio MCP ("kapi"), arkasında kurulu tüm MCP sunucuları. İstemciye yalnız iki araç görünür (ara, cagir);
şemalar istek anında `ara` ile gelir → araç adı listesi + sunucu yönergeleri giriş jetonuna girmez.
  python mcp_kapi.py                   stdio sunucu (MCP istemcisi başlatır; env KAPI_HARIC=ad,ad dışarıda bırakılır)
  python mcp_kapi.py katalog [ad...]   araç kataloğunu .kos/kopru/kapi-katalog.json'a yazar (tanım: mcp_profil.tanimlar)
  python mcp_kapi.py ara <sorgu>       katalogda arama (sınama)
OAuth isteyen http sunucular (401) kapıdan geçmez; doğrudan MCP olarak kalır (mcp_profil.DOGRUDAN)."""
import json, os, queue, re, shutil, subprocess, sys, threading, time, urllib.error, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "tools")]
import mcp_profil  # noqa: E402

KAT = KOK / ".kos" / "kopru" / "kapi-katalog.json"
SURE = int(os.environ.get("KAPI_SURE", "60"))
INIT = {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "kapi", "version": "1"}}


def gen(v):  # ${VAR} → ortam (değer asla yazdırılmaz)
    return re.sub(r"\$\{(\w+)\}", lambda m: os.environ.get(m[1], ""), v) if isinstance(v, str) else v


class Stdio:
    def __init__(s, t):
        env = {**os.environ, **{k: gen(str(v)) for k, v in (t.get("env") or {}).items()}}
        cmd = [shutil.which(t["command"]) or t["command"], *[gen(a) for a in t.get("args", [])]]
        s.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, creationflags=0x08000000)
        s.q, s.n = queue.Queue(), 0
        threading.Thread(target=s._oku, daemon=True).start()
        s.rpc("initialize", INIT)
        s._yaz({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _oku(s):
        for l in s.p.stdout:
            try:
                s.q.put(json.loads(l))
            except ValueError:
                pass
        s.q.put(None)

    def _yaz(s, o):
        s.p.stdin.write((json.dumps(o) + "\n").encode("utf-8")); s.p.stdin.flush()

    def rpc(s, m, p=None):
        s.n += 1; i = s.n
        s._yaz({"jsonrpc": "2.0", "id": i, "method": m, "params": p or {}})
        son = time.time() + SURE
        while True:
            try:
                r = s.q.get(timeout=max(0.1, son - time.time()))
            except queue.Empty:
                raise TimeoutError(m)
            if r is None:
                raise RuntimeError("sunucu kapandı")
            if "method" in r:
                if "id" in r:
                    s._yaz({"jsonrpc": "2.0", "id": r["id"], "result": {}})  # sunucu isteği (ping/roots): boş yanıt
            elif r.get("id") == i:
                if "error" in r:
                    raise RuntimeError(json.dumps(r["error"])[:300])
                return r["result"]


class Http:
    def __init__(s, t):
        s.url, s.n, s.sid = gen(t["url"]), 0, None
        s.h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream", **{k: gen(v) for k, v in (t.get("headers") or {}).items()}}
        s.rpc("initialize", INIT)
        s._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _post(s, o):
        h = dict(s.h)
        if s.sid:
            h["Mcp-Session-Id"] = s.sid
        try:
            r = urllib.request.urlopen(urllib.request.Request(s.url, json.dumps(o).encode("utf-8"), h), timeout=SURE)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code}" + (" (OAuth: doğrudan MCP kullan)" if e.code == 401 else ""))
        s.sid = r.headers.get("Mcp-Session-Id") or s.sid
        return r.headers.get("Content-Type", ""), r.read().decode("utf-8")

    def rpc(s, m, p=None):
        s.n += 1
        ct, txt = s._post({"jsonrpc": "2.0", "id": s.n, "method": m, "params": p or {}})
        msg = [json.loads(l[5:]) for l in txt.splitlines() if l.startswith("data:") and l[5:].strip()] if "event-stream" in ct else [json.loads(txt)]
        r = next((x for x in msg if x.get("id") == s.n and "method" not in x), None)
        if r is None:
            raise RuntimeError("yanıt yok")
        if "error" in r:
            raise RuntimeError(json.dumps(r["error"])[:300])
        return r["result"]


BAG, KILIT = {}, threading.Lock()


def bag(ad):
    with KILIT:
        if ad not in BAG:
            t = mcp_profil.tanimlar()[ad]
            BAG[ad] = Http(t) if t.get("type") in ("http", "sse") else Stdio(t)
        return BAG[ad]


def liste(ad):
    out, c = [], None
    while True:
        r = bag(ad).rpc("tools/list", {"cursor": c} if c else {})
        out += r["tools"]; c = r.get("nextCursor")
        if not c:
            return [{"name": x["name"], "description": x.get("description", ""), "inputSchema": x.get("inputSchema", {})} for x in out]


def katalog(adlar):
    kat = json.loads(KAT.read_text(encoding="utf-8")) if KAT.exists() else {}
    def is_(ad):
        try:
            kat[ad] = liste(ad)
        except Exception as e:
            kat[ad] = {"hata": repr(e)[:160]}
    ts = [threading.Thread(target=is_, args=(a,)) for a in (adlar or mcp_profil.tanimlar())]
    [t.start() for t in ts]; [t.join() for t in ts]
    KAT.write_text(json.dumps(kat, ensure_ascii=False), encoding="utf-8")
    return {a: (len(v) if isinstance(v, list) else v["hata"]) for a, v in kat.items()}


def kat_oku():
    return json.loads(KAT.read_text(encoding="utf-8")) if KAT.exists() else {}


def ara(sorgu="", sunucu=None, n=5):
    kat, haric = kat_oku(), set(filter(None, os.environ.get("KAPI_HARIC", "").split(",")))
    adaylar = [(s, a) for s, v in kat.items() if isinstance(v, list) and s not in haric and (not sunucu or s == sunucu) for a in v]
    if sunucu and not sorgu:
        return f"{sunucu}: " + ", ".join(a["name"] for _, a in adaylar)
    kel = [k for k in re.split(r"\W+", sorgu.lower()) if k]
    def puan(sa):
        s, a = sa
        ad, ac = (s + " " + a["name"]).lower(), a["description"].lower()
        return sum(3 * (k in ad) + (k in ac) for k in kel)
    sec = [sa for sa in sorted(adaylar, key=puan, reverse=True)[:n] if puan(sa) > 0]
    return "\n".join(f"{s}.{a['name']} — {a['description'][:200]}\nşema: {json.dumps(a['inputSchema'], ensure_ascii=False, separators=(',', ':'))[:1500]}" for s, a in sec) or "eşleşme yok"


def cagir(sunucu, arac, args=None):
    return bag(sunucu).rpc("tools/call", {"name": arac, "arguments": args or {}})


def araclar():
    return [{"name": "ara", "description": "MCP araç ara (şema döner); yalnız sunucu verilirse o sunucunun araç adları",
             "inputSchema": {"type": "object", "properties": {"sorgu": {}, "sunucu": {}}}},
            {"name": "cagir", "description": "ara ile bulunan MCP aracını çağır",
             "inputSchema": {"type": "object", "properties": {"sunucu": {}, "arac": {}, "args": {}}, "required": ["sunucu", "arac"]}}]


def sunucu():
    kilit = threading.Lock()
    def yanit(i, sonuc=None, hata=None):
        with kilit:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": i, **({"error": hata} if hata else {"result": sonuc})}, ensure_ascii=False) + "\n"); sys.stdout.flush()
    def is_(r):
        m, p, i = r.get("method"), r.get("params") or {}, r.get("id")
        try:
            if m == "initialize":
                yanit(i, {"protocolVersion": p.get("protocolVersion", INIT["protocolVersion"]), "capabilities": {"tools": {}}, "serverInfo": {"name": "kapi", "version": "1"}})
            elif m == "tools/list":
                yanit(i, {"tools": araclar()})
            elif m == "tools/call":
                a = p.get("arguments") or {}
                if p["name"] == "ara":
                    yanit(i, {"content": [{"type": "text", "text": ara(a.get("sorgu", ""), a.get("sunucu"))}]})
                else:
                    try:
                        yanit(i, cagir(a["sunucu"], a["arac"], a.get("args")))
                    except Exception as e:
                        yanit(i, {"isError": True, "content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}]})
            elif i is not None:
                yanit(i, {} if m == "ping" else None, None if m == "ping" else {"code": -32601, "message": m})
        except Exception as e:
            if i is not None:
                yanit(i, None, {"code": -32000, "message": repr(e)[:200]})
    ts = []
    for l in sys.stdin:
        try:
            ts.append(threading.Thread(target=is_, args=(json.loads(l),), daemon=True)); ts[-1].start()
        except ValueError:
            pass
    [t.join() for t in ts]  # stdin kapanınca uçuştaki istekler bitsin


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["katalog"]:
        print(json.dumps(katalog(a[1:]), ensure_ascii=False))
    elif a[:1] == ["ara"]:
        print(ara(" ".join(a[1:])))
    else:
        sunucu()
