r"""RAM-1: MCP sunucu envanteri ve oturum olcumu.

  python tools/mcp_envanter.py al CIKTI.json [ad ...]     CC (~/.claude.json) + Desktop (MSIX config) stdio
                                                          sunuculari config'deki komutla baslar, initialize +
                                                          tools/list alinir, kapatilir -> {kaynak:ad: araclar}
  python tools/mcp_envanter.py karsilastir A.json B.json  birebir degilse fark satirlari + exit 1
  python tools/mcp_envanter.py graf                       mcp-memory read_graph varlik/iliski sayisi (CC + Desktop)
  python tools/mcp_envanter.py olc ETIKET                 yeni konsolda bos CC oturumu: surec agaci (adet, calisma
                                                          kumesi, ozel bellek) + `claude mcp list` x3 -> docs/ram/olcum.md

CC tam ortam + ${VAR} genisletmesiyle, Desktop DESKTOP_ENV beyaz listesi + cwd=System32 ile
baslatilir (mcp_kurutest ile ayni kosullar). Ortam degiskeni DEGERI yazilmaz; yalniz ad -> var/yok.
"""
import collections
import concurrent.futures
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_kurutest import DESKTOP_CFG, DESKTOP_ENV, dene  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CC_CFG = os.path.join(os.path.expanduser("~"), ".claude.json")
SYSTEM32 = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32")
OLCUM = os.path.join(REPO, "docs", "ram", "olcum.md")
BEKLE = 90  # sn: yeni oturumun stdio sunuculari baglanana kadar
ARACI = ("node.exe", "cmd.exe", "conhost.exe", "uv.exe", "uvx.exe", "python.exe", "dotnet.exe")
GIZLI = re.compile(r"[A-Za-z0-9_-]{32,}")


def genislet(s):
    """CC'nin ${VAR} / ${VAR:-varsayilan} genisletmesi."""
    return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}",
                  lambda m: os.environ.get(m.group(1)) or (m.group(2) or ""), s)


def sunucular():
    """{kaynak:ad: (komut, argv, env_ek, taban_env, cwd)} - yalniz stdio."""
    cc = json.load(open(CC_CFG, encoding="utf-8")).get("mcpServers", {})
    ds = json.load(open(DESKTOP_CFG, encoding="utf-8")).get("mcpServers", {})
    masa = {k: os.environ[k] for k in DESKTOP_ENV if k in os.environ}
    out = {}
    for ad, c in cc.items():
        if c.get("type", "stdio") == "stdio":
            out["cc:" + ad] = (genislet(c["command"]), [genislet(a) for a in c.get("args", [])],
                               {k: genislet(v) for k, v in (c.get("env") or {}).items()}, None, REPO)
    for ad, c in ds.items():
        if c.get("type", "stdio") == "stdio":
            out["desktop:" + ad] = (c["command"], c.get("args", []), c.get("env") or {}, masa, SYSTEM32)
    return out


def al(adlar=()):
    def tek(oge):
        k, (komut, argv, env, taban, cwd) = oge
        tanim = (komut, argv, env)
        r = dene(k, komut, argv, env, taban=taban, hata_bufer=[], cwd=cwd)
        kayit = {"env": {n: bool(v) for n, v in tanim[2].items()}} if tanim[2] else {}
        if r["durum"] == "OK":
            kayit.update(arac_sayisi=r["arac"], araclar=sorted(r["araclar"]))
        else:
            kayit["hata"] = GIZLI.sub("<***>", f'{r["durum"]}: {r.get("hata", "")}')[:300]
        return k, kayit
    sec = {k: v for k, v in sunucular().items() if not adlar or k.split(":", 1)[1] in adlar}
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        return dict(sorted(ex.map(tek, sec.items())))


def karsilastir(once, sonra):
    """Fark satirlari; bos liste = birebir ayni (sunucu, arac adlari, arac sayisi)."""
    fark = []
    for ad in sorted(once.keys() | sonra.keys()):
        o, s = once.get(ad), sonra.get(ad)
        if o is None or s is None:
            fark.append(f"{ad}: {'fazla' if o is None else 'eksik'} sunucu")
            continue
        for etiket, x in (("once", o), ("sonra", s)):
            if "hata" in x:
                fark.append(f"{ad}: {etiket} baslamadi: {x['hata']}")
        oa, sa = set(o.get("araclar", [])), set(s.get("araclar", []))
        if oa - sa:
            fark.append(f"{ad}: eksik arac {sorted(oa - sa)}")
        if sa - oa:
            fark.append(f"{ad}: fazla arac {sorted(sa - oa)}")
        if o.get("arac_sayisi") != s.get("arac_sayisi"):
            fark.append(f"{ad}: arac sayisi {o.get('arac_sayisi')} -> {s.get('arac_sayisi')}")
    return fark


def graf():
    """mcp-memory read_graph varlik/iliski sayisi; istekler tek seferde yazilir, stdin kapaninca sunucu cikar."""
    istek = "".join(json.dumps(m) + "\n" for m in (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "ram1-graf", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "read_graph", "arguments": {}}}))
    out = {}
    for k, (komut, argv, env, taban, cwd) in sunucular().items():
        if k.endswith(":mcp-memory"):
            p = subprocess.run([komut] + argv, input=istek, capture_output=True, text=True, encoding="utf-8",
                               env={**(os.environ if taban is None else taban), **env}, cwd=cwd, timeout=120)
            out[k] = {"hata": p.stderr.strip()[-200:]}
            for s in p.stdout.splitlines():
                m = json.loads(s) if s.startswith("{") else {}
                if m.get("id") == 3:
                    g = json.loads(m["result"]["content"][0]["text"])
                    out[k] = {"varlik": len(g["entities"]), "iliski": len(g["relations"])}
    return out


def agac(kok):
    """kok PID ve torunlari (Win32_Process anlik goruntusu)."""
    ps = json.loads(subprocess.run(
        ["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | Select-Object "
         "ProcessId,ParentProcessId,Name,WorkingSetSize,PrivatePageCount | ConvertTo-Json -Compress"],
        capture_output=True, text=True, encoding="utf-8").stdout)
    cocuk = collections.defaultdict(list)
    for p in ps:
        cocuk[p["ParentProcessId"]].append(p)
    out = [p for p in ps if p["ProcessId"] == kok]
    gorulen, yigin = {kok}, [kok]
    while yigin:
        for c in cocuk[yigin.pop()]:
            if c["ProcessId"] not in gorulen:
                gorulen.add(c["ProcessId"])
                out.append(c)
                yigin.append(c["ProcessId"])
    return out


def olc(etiket):
    claude = shutil.which("claude")
    p = subprocess.Popen([claude], cwd=REPO, creationflags=subprocess.CREATE_NEW_CONSOLE)
    try:
        time.sleep(BEKLE)
        t = agac(p.pid)
    finally:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
    ws = sum(int(x["WorkingSetSize"] or 0) for x in t) / 2**30
    oz = sum(int(x["PrivatePageCount"] or 0) for x in t) / 2**30
    dag = collections.Counter(x["Name"].lower() for x in t)
    araci = " ".join(f"{n[:-4]}×{dag[n]}" for n in ARACI if dag[n])
    sureler = []
    for _ in range(3):
        t0 = time.time()
        liste = subprocess.run([claude, "mcp", "list"], cwd=REPO, capture_output=True, text=True,
                               encoding="utf-8").stdout
        sureler.append(time.time() - t0)
    bagli = liste.count("Connected")
    kopuk = [s.split(":")[0] for s in liste.splitlines() if "Failed" in s or "✗" in s]
    os.makedirs(os.path.dirname(OLCUM), exist_ok=True)
    yeni = not os.path.exists(OLCUM)
    satir = (f"| {etiket} | {time.strftime('%Y-%m-%d %H:%M')} | {len(t)} | {ws:.2f} | {oz:.2f} | {araci} | "
             f"{statistics.median(sureler):.1f} ({' / '.join(f'{s:.1f}' for s in sureler)}) | {bagli} | "
             f"{', '.join(kopuk) or '-'} |\n")
    with open(OLCUM, "a", encoding="utf-8", newline="\n") as f:
        if yeni:
            f.write(f"# RAM-1 ölçüm — yeni açılmış boşta CC oturumu ({BEKLE} sn sonra claude.exe ağacı)\n\n"
                    "| etiket | zaman | süreç | çalışma kümesi GB | özel GB | aracı adayları | "
                    "mcp list sn medyan (3 koşu) | bağlı | bağlanamayan |\n|---|---|---|---|---|---|---|---|---|\n")
        f.write(satir)
    print(satir.strip())


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["al"] and len(a) >= 2:
        env = al(a[2:])
        os.makedirs(os.path.dirname(os.path.abspath(a[1])), exist_ok=True)
        with open(a[1], "w", encoding="utf-8", newline="\n") as f:
            json.dump(env, f, ensure_ascii=False, indent=1)
            f.write("\n")
        for k, v in env.items():
            print(k, v.get("arac_sayisi", v.get("hata")), v.get("env", ""))
    elif a[:1] == ["karsilastir"] and len(a) == 3:
        fark = karsilastir(*(json.load(open(x, encoding="utf-8")) for x in a[1:]))
        print("\n".join(fark) or "birebir ayni")
        sys.exit(1 if fark else 0)
    elif a == ["graf"]:
        print(json.dumps(graf(), ensure_ascii=False))
    elif a[:1] == ["olc"] and len(a) == 2:
        olc(a[1])
    else:
        print(__doc__)
        sys.exit(2)
