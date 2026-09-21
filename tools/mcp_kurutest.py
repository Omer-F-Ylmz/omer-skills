r"""K3 kuru test: her stdio MCP tanimini bagimsiz calistir, initialize + tools/list al.

Kullanim: python tools/mcp_kurutest.py [--desktop-env] [--cwd YOL] [--spawner node] [sunucu-adi ...]
Cikti: her sunucu icin ARAC SAYISI ya da gerekcelendirilmis hata.

--cwd YOL: sureci o calisma dizininde baslatir. Desktop'in cwd'si kullanici
dizini degil; cwd'ye goreli yazan sunucular (puppeteer-mcp-server gunluk dosyasini
<cwd>\logs altina acar) yalnizca bu bayrakla ayristirilabilir.
--spawner node: cmd wrapper yerine node.exe'yi dogrudan calistirir (shell=False),
boylece "suclu cwd mi, cmd katmani mi" sorusu ayrilir.

--desktop-env: sureci Claude Desktop gibi baslatir. Desktop yerel MCP sunucularini
tam kullanici ortamiyla degil, MCP SDK'nin beyaz listesiyle baslatir; kanit
app.asar ofset 3899305 (DEFAULT_INHERITED_ENV_VARS, Claude 2.2553.1.0). Bu modda
%VAR% genisletmesi de YAPILMAZ -- cmd.exe ayni kisitli ortamla basladigi icin
genisletemez. K11_ERR=<dizin> verilirse her sunucunun stderr'i oraya yazilir.
"""
import json, os, subprocess, sys, threading, queue, time

TIMEOUT = 90

# app.asar ofset 3899305 -- MCP SDK DEFAULT_INHERITED_ENV_VARS (win32)
DESKTOP_ENV = ["APPDATA", "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA", "PATH",
               "PROCESSOR_ARCHITECTURE", "SYSTEMDRIVE", "SYSTEMROOT", "TEMP",
               "USERNAME", "USERPROFILE", "PROGRAMFILES"]

def dene(ad, komut, argv, env_ek, temizle=(), taban=None, hata_bufer=None, cwd=None):
    t0 = time.time()
    env = dict(taban) if taban is not None else os.environ.copy()
    for k in temizle:
        env.pop(k, None)
    env.update(env_ek or {})
    try:
        p = subprocess.Popen([komut] + argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env, text=True, encoding="utf-8",
                             errors="replace", bufsize=1, cwd=cwd)
    except Exception as e:
        return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "BASLAMADI", "hata": f"{type(e).__name__}: {e}", "arac": 0}

    q = queue.Queue()
    threading.Thread(target=lambda: [q.put(l) for l in p.stdout], daemon=True).start()
    hata_bufer = [] if hata_bufer is None else hata_bufer
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
            kod = p.poll()          # kendi mi cikti (kod var) yoksa asili mi kaldi (None)
            p.kill()
            return {"sure": round(time.time()-t0,1), "ad": ad, "durum": "INIT-YOK", "arac": 0,
                    "cikis": kod,
                    "hata": ("".join(hata_bufer)[-400:] or f"yanit yok / surec dustu (cikis={kod})").strip()}
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


# --spawner node icin: sunucu adi -> global paketin giris dosyasi
NPM_PREFIX = (r"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages"
              r"\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64")
NODE_GIRIS = {
    "puppeteer":    [r"node_modules\puppeteer-mcp-server\dist\index.js"],
    "brave-search": [r"node_modules\@brave\brave-search-mcp-server\dist\index.js"],
    "stitch":       [r"node_modules\@_davideast\stitch-mcp\bin\stitch-mcp.js", "proxy"],
}


def ayikla(argv):
    """--cwd YOL ve --spawner DEGER'i cikarir, kalan argumanlari dondurur."""
    kalan, deger = [], {}
    i = 0
    while i < len(argv):
        if argv[i] in ("--cwd", "--spawner") and i + 1 < len(argv):
            deger[argv[i][2:]] = argv[i+1]; i += 2
        else:
            kalan.append(argv[i]); i += 1
    return kalan, deger.get("cwd"), deger.get("spawner")



def cwd_coz(deger):
    """--cwd ciplak ad kabul eder: System32 -> %SystemRoot%\\System32 (Desktop'in cwd'si)."""
    if not deger:
        return None
    if os.path.isabs(deger) or os.path.dirname(deger):
        return deger
    return os.path.join(os.environ["SystemRoot"], deger)


def spawner_uygula(ad, komut, cagri, spawner):
    """--spawner node: haritadaki sunucu node.exe ile, haritada olmayan config komutuyla kosar."""
    if spawner != "node" or ad not in NODE_GIRIS:
        return komut, cagri
    cagri = [os.path.join(NPM_PREFIX, y) if y.startswith("node_modules") else y
             for y in NODE_GIRIS[ad]]
    return os.path.join(NPM_PREFIX, "node.exe"), cagri

if __name__ == "__main__":
    argv, cwd, spawner = ayikla(sys.argv[1:])
    cwd = cwd_coz(cwd)
    bayraklar = [a for a in argv if a.startswith("--")]
    hedef = [a for a in argv if not a.startswith("--")]
    desktop = "--desktop-env" in bayraklar
    taban = {k: os.environ[k] for k in DESKTOP_ENV if k in os.environ} if desktop else None
    hata_dizin = os.environ.get("K11_ERR")
    if hata_dizin:
        os.makedirs(hata_dizin, exist_ok=True)
    if desktop:
        print(f"[--desktop-env] taban {len(taban)} degisken, %VAR% genisletmesi KAPALI", flush=True)
    if cwd:
        print(f"[--cwd] {cwd}", flush=True)
    if spawner:
        print(f"[--spawner] {spawner}", flush=True)
    print(flush=True)
    sunucular = yukle()
    secim = {k: v for k, v in sunucular.items()
             if v.get("type", "stdio") == "stdio" and (not hedef or k in hedef)}
    sonuc = []
    for ad, tanim in sorted(secim.items()):
        gen = (lambda x: x) if desktop else os.path.expandvars
        env_ek = {k: gen(v) for k, v in (tanim.get("env") or {}).items()}
        komut, cagri = tanim["command"], [gen(a) for a in tanim.get("args", [])]
        komut, cagri = spawner_uygula(ad, komut, cagri, spawner)
        buf = []
        r = dene(ad, komut, cagri, env_ek, taban=taban, hata_bufer=buf, cwd=cwd)
        if hata_dizin:
            with open(os.path.join(hata_dizin, ad + ".stderr.txt"), "w",
                      encoding="utf-8", errors="replace") as fh:
                fh.write("".join(buf))
        sonuc.append(r)
        print(f"{r['durum']:<11} {ad:<26} arac={r['arac']:<4} {r['sure']:>6}s {r.get('sunucu','')}", flush=True)
        if r.get("hata"):
            print(f"            > {r['hata'][:300]}", flush=True)
    print("\n=== OZET ===")
    for r in sonuc:
        print(f"{r['ad']:<26} {r['durum']:<11} arac={r['arac']:<4} {r['sure']:>6}s")
    json.dump(sonuc, open(os.environ.get("K11_OUT", "kurutest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
