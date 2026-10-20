"""Yetim süreç temizliği: python yetim.py liste | durdur [--kuru] [--yas DK]
Yetim = python/node/conhost/uv/cmd süreci; ata zinciri ölü bir ebeveynde bitiyor ve zincirde canlı claude/Desktop/powershell/explorer
da korunan bir komut satırı (Headroom, OmniRoute, claude-mem...) yok. durdur yalnız yaşı >= --yas dk (varsayılan 15) olanları /PID ile
(ağaçsız) kapatır; her turu yetim.log'a yazar. Pencere açmaz."""
import ctypes, json, os, subprocess, sys, time

HEDEF = {"python.exe", "pythonw.exe", "node.exe", "conhost.exe", "uv.exe", "uvx.exe", "cmd.exe"}
# zincirde bu adlardan biri canlıysa süreç bir oturuma/runner'a bağlıdır
BAGLI_AD = ("claude", "powershell", "pwsh", "explorer", "video.exe")
# komut satırı (süreç ya da zincirindeki herhangi biri) bunlardan birini içeriyorsa dokunulmaz
KORUNAN = ("headroom", "omniroute", "worker-service", "bun-runner", "37777", "20190", "ucretsiz_havuz", "ajan_sira",
           "video764", "cc-kopru", "obsidian", "chrome", "mem_bekci", "mem-bekci", "yetim.py", "ram_bekci", "arka.py",
           "mcp_paylasim", "mcp-proxy", "_kos.py")  # mcp-proxy havuzu bilerek ortak: altındaki MCP sunucuları yetim değil
KOK = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(KOK, "yetim.log")
PS = ("Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,WorkingSetSize,"
      "@{n='T';e={if($_.CreationDate){[DateTimeOffset]::new($_.CreationDate).ToUnixTimeSeconds()}else{0}}},"
      "@{n='Cmd';e={($_.CommandLine+'') -replace '\\s+',' '}} | ConvertTo-Json -Compress")


class MEM(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in ("t", "a", "tp", "ap", "tv", "av", "ae")]


def ram():
    m = MEM()
    m.dwLength = ctypes.sizeof(MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def anlik():
    out = subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True, encoding="utf-8",
                         errors="replace", creationflags=0x08000000).stdout
    return {x["ProcessId"]: x for x in json.loads(out)}


def yetimler(p, simdi=None, benim=None):
    """[(süreç, yaş_sn, neden)] — saf işlev: p = {pid: {ProcessId, ParentProcessId, Name, WorkingSetSize, T, Cmd}}."""
    simdi = simdi or time.time()
    benim = benim or set()
    sonuc = []
    # korunan bir sürecin kardeşi olan conhost da korunur (video koşusunun konsolu)
    kardes = {x["ParentProcessId"] for x in p.values() if any(s in (x.get("Cmd") or "").lower() for s in KORUNAN)}
    for pid, x in p.items():
        if (x["Name"] or "").lower() not in HEDEF or pid in benim:
            continue
        yol, g, k = [], set(), pid
        while k in p and k not in g:
            g.add(k); yol.append(p[k]); k = p[k]["ParentProcessId"]
        if k in p or (x["Name"].lower() == "conhost.exe" and x["ParentProcessId"] in kardes):
            continue
        ust = yol[1:]
        if any((y["Name"] or "").lower().startswith(BAGLI_AD) for y in ust):
            continue
        if any(s in (y.get("Cmd") or "").lower() for y in yol for s in KORUNAN):
            continue
        yas = simdi - x["T"] if x.get("T") else 0
        sonuc.append((x, yas, f"ebeveyn {k} ölü" if len(yol) == 1 else f"zincir {k}'da ölü, oturum yok"))
    return sonuc


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("liste", "durdur"):
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    min_yas = int(a[a.index("--yas") + 1]) * 60 if "--yas" in a else 900
    benim, k = set(), os.getpid()
    p = anlik()
    while k in p and k not in benim:  # kendi ata zincirimize dokunma
        benim.add(k); k = p[k]["ParentProcessId"]
    y = yetimler(p, benim=benim)
    mb = sum(x["WorkingSetSize"] or 0 for x, _, _ in y) // 2**20
    if a[0] == "liste":
        for x, yas, neden in sorted(y, key=lambda t: -(t[0]["WorkingSetSize"] or 0)):
            print(f"{x['ProcessId']} · {x['Name']} · {(x['WorkingSetSize'] or 0) // 2**20} MB · {int(yas // 60)} dk · {x['Cmd'][:70]} · {neden}")
        print(f"yetim {len(y)} süreç · {mb} MB · RAM %{ram()}")
        return
    secili = [(x, yas) for x, yas, _ in y if yas >= min_yas]
    smb = sum(x["WorkingSetSize"] or 0 for x, _ in secili) // 2**20
    once = ram()
    if "--kuru" in a:
        print(f"kuru: {len(secili)}/{len(y)} yetim durdurulurdu · {smb} MB · RAM %{once}")
        return
    ok = sum(subprocess.run(["taskkill", "/PID", str(x["ProcessId"]), "/F"], capture_output=True, creationflags=0x08000000).returncode == 0
             for x, _ in secili)
    if secili:
        time.sleep(2)
    satir = f"{time.strftime('%Y-%m-%d %H:%M:%S')} durdurulan {ok}/{len(secili)} · ~{smb} MB · RAM %{once}->%{ram()}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(satir + "\n")
    print(satir)


if __name__ == "__main__":
    main()
