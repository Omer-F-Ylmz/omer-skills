"""K3 kuru test: her stdio MCP tanimini bagimsiz calistir, initialize + tools/list al.

Kullanim: python tools/mcp_kurutest.py [sunucu-adi ...]
Cikti: her sunucu icin ARAC SAYISI ya da gerekcelendirilmis hata.
"""
import json, os, subprocess, sys, threading, queue, time

TIMEOUT = 90

def dene(ad, komut, argv, env_ek, temizle=()):
    t0 = time.time()
    env = os.environ.copy()
    for k in temizle:
        env.pop(k, None)
    env.update(env_ek or {})
    try:
        p = subprocess.Popen([komut] + argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env, text=True, encoding="utf-8",
                             errors="replace", bufsize=1)
    except Exception as e:
        return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "BASLAMADI", "hata": f"{type(e).__name__}: {e}", "arac": 0}

    q = queue.Queue()
    threading.Thread(target=lambda: [q.put(l) for l in p.stdout], daemon=True).start()
    hata_bufer = []
    threading.Thread(target=lambda: [hata_bufer.append(l) for l in p.stderr], daemon=True).start()

    def gonder(obj):
        p.stdin.write(json.dumps(obj) + "\n"); p.stdin.flush()

    def bekle(idno, son):
        while time.time() < son:
            try:
                satir = q.get(timeout=0.5)
            except queue.Empty:
                if p.poll() is not None:
                    return None
                continue
            satir = satir.strip()
            if not satir or not satir.startswith("{"):
                continue
            try:
                m = json.loads(satir)
            except Exception:
                continue
            if m.get("id") == idno:
                return m
        return None

    son = time.time() + TIMEOUT
    try:
        gonder({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "k11-kurutest", "version": "1.0"}}})
        ini = bekle(1, son)
        if ini is None:
            p.kill()
            return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "INIT-YOK", "arac": 0,
                    "hata": ("".join(hata_bufer)[-400:] or "yanit yok / surec dustu").strip()}
        if "error" in ini:
            p.kill()
            return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "INIT-HATA", "arac": 0, "hata": json.dumps(ini["error"])[:400]}

        gonder({"jsonrpc": "2.0", "method": "notifications/initialized"})
        gonder({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tl = bekle(2, son)
        p.kill()
        if tl is None:
            return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "TOOLS-YOK", "arac": 0,
                    "hata": ("".join(hata_bufer)[-400:] or "tools/list yanitsiz").strip()}
        if "error" in tl:
            return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "TOOLS-HATA", "arac": 0, "hata": json.dumps(tl["error"])[:400]}
        araclar = tl.get("result", {}).get("tools", [])
        srv = ini.get("result", {}).get("serverInfo", {})
        return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "OK", "arac": len(araclar),
                "sunucu": f"{srv.get('name','?')} {srv.get('version','')}".strip(),
                "ornek": [a.get("name") for a in araclar[:3]]}
    except Exception as e:
        try: p.kill()
        except Exception: pass
        return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "ISTISNA", "arac": 0, "hata": f"{type(e).__name__}: {e}"}


def yukle():
    cfg = json.load(open(os.path.expanduser(os.environ.get("K11_CFG", "~/.claude.json")), encoding="utf-8"))
    return cfg.get("mcpServers", {})


if __name__ == "__main__":
    hedef = sys.argv[1:]
    sunucular = yukle()
    secim = {k: v for k, v in sunucular.items()
             if v.get("type", "stdio") == "stdio" and (not hedef or k in hedef)}
    sonuc = []
    for ad, tanim in sorted(secim.items()):
        env_ek = {k: os.path.expandvars(v) for k, v in (tanim.get("env") or {}).items()}
        argv = [os.path.expandvars(a) for a in tanim.get("args", [])]
        r = dene(ad, tanim["command"], argv, env_ek)
        sonuc.append(r)
        print(f"{r['durum']:<11} {ad:<26} arac={r['arac']:<4} {r['sure']:>6}s {r.get('sunucu','')}", flush=True)
        if r.get("hata"):
            print(f"            > {r['hata'][:300]}", flush=True)
    print("\n=== OZET ===")
    for r in sonuc:
        print(f"{r['ad']:<26} {r['durum']:<11} arac={r['arac']:<4} {r['sure']:>6}s")
    json.dump(sonuc, open(os.environ.get("K11_OUT", "kurutest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
