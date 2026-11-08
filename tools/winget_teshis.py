import subprocess as s, time, sys
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\winget_teshis.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def r(a, t):
    t0 = time.time()
    try:
        p = s.run(a, capture_output=True, timeout=t)
        o = (p.stdout + p.stderr).decode("utf-8", "ignore")
        print(time.strftime("%H:%M:%S"), f"{time.time()-t0:.0f}sn", " ".join(a), "| exit", p.returncode, "|", o.strip()[-700:], file=LOG)
    except Exception as e:
        print(time.strftime("%H:%M:%S"), f"{time.time()-t0:.0f}sn", " ".join(a), "| ZAMAN ASIMI/HATA", e, file=LOG)
r(["winget", "--version"], 30)
r(["winget", "source", "list"], 60)
r(["winget", "show", "--id", "Helm.Helm", "-e", "--source", "winget", "--accept-source-agreements"], 120)
r(["winget", "show", "--id", "Helm.Helm", "-e", "--accept-source-agreements"], 120)
r(["winget", "install", "--id", "Helm.Helm", "-e", "--source", "winget", "--scope", "user", "--silent", "--accept-package-agreements", "--accept-source-agreements", "--disable-interactivity"], 300)
print("BITTI", file=LOG)
