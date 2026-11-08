import os, subprocess as s, time
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\teshis_wsl.log", "w", encoding="utf-8", buffering=1)
v = os.path.join(os.environ["LOCALAPPDATA"], "wsl", "{4da2ed96-528b-473b-85a2-7eb381f250d8}", "ext4.vhdx")
def r(a, enc=None, t=40):
    try:
        p = s.run(a, capture_output=True, timeout=t)
        o = p.stdout + p.stderr
        try: x = o.decode(enc) if enc else o.decode("utf-8")
        except Exception: x = o.decode("cp857", "ignore")
        print(">", " ".join(a), "| exit", p.returncode, file=LOG); print(x.replace("\x00", "").strip()[:1500], file=LOG)
    except Exception as e:
        print(">", " ".join(a), "| HATA", e, file=LOG)
print(time.strftime("%H:%M:%S"), file=LOG)
r(["fsutil", "reparsepoint", "query", v])
r(["fsutil", "sparse", "queryflag", v])
w = os.path.join(os.environ["USERPROFILE"], ".wslconfig")
print(".wslconfig:", open(w, encoding="utf-8", errors="ignore").read() if os.path.exists(w) else "YOK", file=LOG)
r(["wmic", "process", "where", "name='winget.exe' or name='powershell.exe' or name='WindowsPackageManagerServer.exe' or name='AppInstallerCLI.exe'", "get", "ProcessId,ParentProcessId,CreationDate,CommandLine", "/format:list"])
r(["wsl", "-d", "Ubuntu", "-e", "echo", "WSL_OK"], "utf-16-le", 90)
print("BITTI", time.strftime("%H:%M:%S"), file=LOG)
