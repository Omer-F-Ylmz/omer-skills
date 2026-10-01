r"""RAM-1 bakim: dogrudan baslatilan MCP sunucusunun sabit surumunu degistirir.

  python tools/mcp_guncelle.py <ad> <surum>   surumu dogrula -> once-envanter -> kur -> kurulu surum = hedef mi
                                              -> sonra-envanter -> karsilastir (fark ya da surum uyusmazligi: exit 1)
  python tools/mcp_guncelle.py geri-al        RAM-1 oncesine don (.bak-ram1 yedekleri)

Kurulum yerleri: npm -> C:\AI\mcp\<ad>\ (package-lock'lu, --ignore-scripts), uv -> `uv tool install`
(~/.local/bin/<exe>), dotnet -> `dotnet tool --tool-path C:\AI\mcp\<ad>`. Config'deki yol surumden
bagimsiz; guncellemede config degismez.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_envanter as envanter  # noqa: E402
from mcp_kurutest import DESKTOP_CFG  # noqa: E402

KOK = r"C:\AI\mcp"
LAUNCH = os.path.join(envanter.REPO, "tools", "mcp-launch")
KURULUM = {  # ad: (tur, paket)
    "mcp-sequential-thinking": ("npm", "@modelcontextprotocol/server-sequential-thinking"),
    "mcp-memory": ("npm", "@modelcontextprotocol/server-memory"),
    "mcp-filesystem": ("npm", "@modelcontextprotocol/server-filesystem"),
    "stitch": ("npm", "@_davideast/stitch-mcp"),
    "brave-search": ("npm", "@brave/brave-search-mcp-server"),
    "playwright": ("npm", "@playwright/mcp"),
    "mcp-fetch": ("uv", "mcp-server-fetch"),
    "mcp-git": ("uv", "mcp-server-git"),
    "mcp-time": ("uv", "mcp-server-time"),
    "code-review": ("uv", "code-review-mcp"),
    "binlog": ("dotnet", "Microsoft.AITools.BinlogMcp"),
}
SURUM = re.compile(r"\d+(\.\d+)*([-+][0-9A-Za-z.-]+)?")


def surum_dogrula(s):
    if not SURUM.fullmatch(s or ""):
        raise ValueError(f"sabit surum gerekli (latest, ^, ~, >= olmaz): {s!r}")


def surum_kontrol(kurulu, hedef):
    return None if kurulu == hedef else f"kurulu surum {kurulu} != hedef {hedef}"


def paket_dizini(ad):
    return os.path.join(KOK, ad, "node_modules", *KURULUM[ad][1].split("/"))


def giris(ad):
    """npm paketinin bin giris dosyasi (mutlak yol)."""
    d = paket_dizini(ad)
    b = json.load(open(os.path.join(d, "package.json"), encoding="utf-8"))["bin"]
    return os.path.normpath(os.path.join(d, b if isinstance(b, str) else next(iter(b.values()))))


def kur(ad, surum):
    tur, paket = KURULUM[ad]
    hedef = os.path.join(KOK, ad)
    if tur == "npm":
        os.makedirs(hedef, exist_ok=True)
        komut = [shutil.which("npm"), "install", "--ignore-scripts", "--save-exact", f"{paket}@{surum}"]
    elif tur == "uv":
        komut = ["uv", "tool", "install", "--force", f"{paket}=={surum}"]
    else:
        var = os.path.isdir(hedef)
        komut = (["dotnet", "tool", "update" if var else "install", paket, "--version", surum, "--tool-path", hedef]
                 + (["--allow-downgrade"] if var else []) + (["--prerelease"] if "-" in surum else []))
    r = subprocess.run(komut, cwd=hedef if tur == "npm" else None, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit(f"{ad}: kurulum basarisiz: {(r.stderr or r.stdout).strip()[-300:]}")


def kurulu_surum(ad):
    tur, paket = KURULUM[ad]
    if tur == "npm":
        return json.load(open(os.path.join(paket_dizini(ad), "package.json"), encoding="utf-8"))["version"]
    if tur == "uv":
        liste = subprocess.run(["uv", "tool", "list"], capture_output=True, text=True).stdout
        m = re.search(rf"^{re.escape(paket)} v(\S+)", liste, re.M)
    else:
        liste = subprocess.run(["dotnet", "tool", "list", "--tool-path", os.path.join(KOK, ad)],
                               capture_output=True, text=True).stdout
        m = re.search(rf"^{re.escape(paket)}\s+(\S+)", liste, re.M | re.I)
    return m.group(1) if m else None


def cc_yaz(ad, tanim):
    """~/.claude.json elle duzenlenmez: CLI ile kaldir + ekle."""
    subprocess.run(["claude", "mcp", "remove", ad, "-s", "user"], capture_output=True)
    r = subprocess.run(["claude", "mcp", "add-json", ad, json.dumps(tanim), "-s", "user"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit(f"{ad}: add-json basarisiz: {r.stderr.strip()[-200:]}")


def geri_al():
    yedek = json.load(open(envanter.CC_CFG + ".bak-ram1", encoding="utf-8"))["mcpServers"]
    simdi = json.load(open(envanter.CC_CFG, encoding="utf-8"))["mcpServers"]
    for ad, tanim in yedek.items():
        if simdi.get(ad) != tanim:
            cc_yaz(ad, tanim)
    shutil.copy2(DESKTOP_CFG + ".bak-ram1", DESKTOP_CFG)
    bak = os.path.join(KOK, "mcp-launch.bak-ram1")
    for f in os.listdir(bak):
        shutil.copy2(os.path.join(bak, f), os.path.join(LAUNCH, f))
    print("geri alindi: ~/.claude.json sunuculari, Desktop config, tools/mcp-launch")


def guncelle(ad, surum):
    once = envanter.al([ad])
    kur(ad, surum)
    hata = surum_kontrol(kurulu_surum(ad), surum)
    if hata:
        print(f"{ad}: {hata}")
        return 1
    fark = envanter.karsilastir(once, envanter.al([ad]))
    print("\n".join(fark) or f"{ad} {surum}: arac seti birebir ayni")
    return 1 if fark else 0


NODE_RE = re.compile(r'[A-Za-z]:\\[^"\s]*?\\node-v\d+\.\d+\.\d+-win-x64\\node\.exe', re.I)


def node_degistir(s, yeni):
    return NODE_RE.sub(lambda _: yeni, s)


def node_tanim(tanim, yeni):
    """Yalniz surum klasorlu node.exe yolu degisir; diger arguman ve env'e dokunulmaz."""
    t = dict(tanim)
    if "command" in t:
        t["command"] = node_degistir(t["command"], yeni)
    if "args" in t:
        t["args"] = [node_degistir(x, yeni) for x in t["args"]]
    return t


def guncel_node():
    """WinGet Links'te node.exe yok (portable paket PATH'e surum klasoruyle girer): en yeni surum klasoru."""
    adaylar = glob.glob(os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "WinGet", "Packages",
                                     "OpenJS.NodeJS*", "node-v*-win-x64", "node.exe"))
    if not adaylar:
        raise SystemExit("WinGet Packages altinda node.exe bulunamadi")
    return max(adaylar, key=lambda p: tuple(map(int, re.search(r"node-v(\d+)\.(\d+)\.(\d+)", p).groups())))


def node_yolu():
    """Node yukselince: CC + Desktop config + tools/mcp-launch/*.cmd node.exe yolu guncele cevrilir."""
    yeni = guncel_node()
    once = envanter.al()
    n = 0
    for ad, tanim in json.load(open(envanter.CC_CFG, encoding="utf-8"))["mcpServers"].items():
        if node_tanim(tanim, yeni) != tanim:
            cc_yaz(ad, node_tanim(tanim, yeni))
            n += 1
    d = json.load(open(DESKTOP_CFG, encoding="utf-8"))
    yeni_d = dict(d, mcpServers={ad: node_tanim(t, yeni) for ad, t in d["mcpServers"].items()})
    if yeni_d != d:
        with open(DESKTOP_CFG, "w", encoding="utf-8") as f:
            json.dump(yeni_d, f, indent=2, ensure_ascii=False)
        n += 1
    for cmd in glob.glob(os.path.join(LAUNCH, "*.cmd")):
        metin = open(cmd, encoding="utf-8", newline="").read()
        if node_degistir(metin, yeni) != metin:
            with open(cmd, "w", encoding="utf-8", newline="") as f:
                f.write(node_degistir(metin, yeni))
            n += 1
    fark = envanter.karsilastir(once, envanter.al())
    print("\n".join(fark) or f"node {yeni}: {n} config degisti; arac seti birebir ayni")
    return 1 if fark else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["geri-al"]:
        geri_al()
        sys.exit(0)
    if a == ["node-yolu"]:
        sys.exit(node_yolu())
    if len(a) != 2 or a[0] not in KURULUM:
        print(__doc__)
        sys.exit(2)
    try:
        surum_dogrula(a[1])
    except ValueError as e:
        print(e)
        sys.exit(2)
    sys.exit(guncelle(*a))
