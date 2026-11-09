r"""Oyun modu: arka plandaki bizim isleri (borsa, bekciler, MCP havuzu, Headroom, bos CC, kontrol pencereleri) kapatir ve
zamanlanmis gorevlerini devre disi birakir; hicbiri kendiliginden geri gelmez. --kapat hepsini eski haline getirir.
  pythonw -I tools/ram/oyun_modu.py --ac       python -I tools/ram/oyun_modu.py --kapat      --durum      --kisayol (masaustune 2 kisayol)"""
import csv, glob, io, json, os, subprocess, sys, time
from pathlib import Path
import psutil

KOK = Path(r"C:\Projeler\omer-skills")
KAYIT = KOK / ".kos" / "oyun-modu.json"
LOG = KOK / "rapor" / "oyun-modu.log"
GW = 0x08000000
BIZIM = ("omer-skills", "borsa-botu", "headroom", ".kos", "omniroute", "claude-mem", "mcp_paylasim", "mcp-proxy")
AD = ("python.exe", "pythonw.exe", "node.exe", "bun.exe", "uv.exe", "uvx.exe", "mcp-proxy.exe", "mcp-server-git.exe", "chroma-mcp.exe",
      "headroom.exe", "headroom-desktop.exe", "cmd.exe", "conhost.exe", "powershell.exe", "claude.exe")


def log(*a):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(s + "\n")
    try:
        print(s)
    except Exception:
        pass


def borsa_kok():
    g = glob.glob(str(Path.home() / "Desktop" / "Claude ile yap*" / "borsa-botu"))
    return Path(g[0]) if g else None


def gorevler():
    r = subprocess.run(["schtasks", "/Query", "/FO", "CSV", "/V"], capture_output=True, creationflags=GW)
    out, gor = [], set()
    for x in csv.reader(io.StringIO(r.stdout.decode("cp857", "replace"))):
        if len(x) < 9 or not x[1].startswith("\\") or x[1].startswith("\\Microsoft") or x[1] in gor:
            continue
        gor.add(x[1])
        if any(k in x[8].lower() for k in BIZIM):
            out.append((x[1], x[3], x[8]))
    return out


def benim_zincir():
    z, p = set(), psutil.Process()
    while p:
        z.add(p.pid)
        try:
            p = p.parent()
        except Exception:
            break
    return z


def ac():
    v0 = psutil.virtual_memory()
    kapali = []
    for ad, durum, _ in gorevler():
        if subprocess.run(["schtasks", "/Change", "/TN", ad, "/Disable"], capture_output=True, creationflags=GW).returncode == 0:
            kapali.append(ad)
    eski = json.loads(KAYIT.read_text(encoding="utf-8")) if KAYIT.exists() else {}
    KAYIT.parent.mkdir(parents=True, exist_ok=True)
    KAYIT.write_text(json.dumps({"gorevler": sorted(set(kapali) | set(eski.get("gorevler", []))), "zaman": time.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False), encoding="utf-8")
    b = borsa_kok()
    if b:
        (b / "kayit").mkdir(exist_ok=True)
        (b / "kayit" / "DURDURULDU").write_text("oyun modu " + time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")
    ben = benim_zincir()
    for tur in range(2):
        hedef = []
        for q in psutil.process_iter(["name"]):
            try:
                n = (q.info["name"] or "").lower()
                if n not in AD or q.pid in ben:
                    continue
                c = " ".join(q.cmdline())
                if n == "claude.exe" and ("WindowsApps" in q.exe() or "--type=" in c):
                    continue
                if n in ("cmd.exe", "conhost.exe", "powershell.exe"):
                    ust = q.parent()
                    if ust and ust.pid in ben:
                        continue
                    if n != "conhost.exe" and not any(k in c.lower() for k in BIZIM + ("python", "node", "claude", "npx", "uv")):
                        continue
                hedef.append((0 if "bekci" in c.lower() or "egit_surekli" in c else 1, q.pid, n))
            except Exception:
                pass
        hedef.sort()
        ok = sum(subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, creationflags=GW).returncode == 0 for _, pid, _ in hedef)
        log(f"oyun modu AC tur {tur + 1}: kapatilan {ok}/{len(hedef)}")
        time.sleep(5)
    v1 = psutil.virtual_memory()
    log(f"gorev devre disi: {len(kapali)} | RAM %{v0.percent} -> %{v1.percent} | bos {v0.available // 2**20} -> {v1.available // 2**20} MB")


def kapat():
    eski = json.loads(KAYIT.read_text(encoding="utf-8")) if KAYIT.exists() else {}
    n = 0
    for ad in eski.get("gorevler", []):
        n += subprocess.run(["schtasks", "/Change", "/TN", ad, "/Enable"], capture_output=True, creationflags=GW).returncode == 0
    b = borsa_kok()
    if b and (b / "kayit" / "DURDURULDU").exists():
        (b / "kayit" / "DURDURULDU").rename(b / "kayit" / ("DURDURULDU.eski-" + time.strftime("%H%M%S")))
    for ad in eski.get("gorevler", []):
        subprocess.run(["schtasks", "/Run", "/TN", ad], capture_output=True, creationflags=GW)
    if KAYIT.exists():
        KAYIT.rename(KAYIT.with_name("oyun-modu.son.json"))
    log(f"oyun modu KAPAT: {n} gorev yeniden etkin ve baslatildi; borsa isareti kaldirildi. MCP araclari icin Claude Desktop'u kapatip ac.")


def durum():
    print("oyun modu:", "ACIK" if KAYIT.exists() else "kapali")
    for ad, d, komut in gorevler():
        print(f"  {d[:14]:14} {ad[:40]:40} {komut[-70:]}")
    v = psutil.virtual_memory()
    print(f"RAM %{v.percent} bos {v.available // 2**20} MB")


def kisayol():
    m = Path.home() / "Desktop"
    pyw = Path(sys.executable).with_name("pythonw.exe")
    for ad, kip in (("Oyun Modu AC", "--ac"), ("Oyun Modu KAPAT", "--kapat")):
        (m / (ad + ".cmd")).write_text(f'@echo off\r\nstart "" "{pyw}" -I "{Path(__file__)}" {kip}\r\n', encoding="cp1254")
        print("kisayol:", m / (ad + ".cmd"))


if __name__ == "__main__":
    kip = (sys.argv[1] if len(sys.argv) > 1 else "--durum").lstrip("-")
    {"ac": ac, "kapat": kapat, "durum": durum, "kisayol": kisayol}[kip]()
