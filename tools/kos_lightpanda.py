import subprocess as s, sys, time
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\kos_lightpanda.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def r(a, t):
    try:
        p = s.run(a, capture_output=True, timeout=t)
        o = p.stdout + p.stderr
        x = o.decode("utf-16-le", "ignore") if o[1:2] == b"\x00" else o.decode("utf-8", "ignore")
        print(time.strftime("%H:%M:%S"), ">", " ".join(a)[-90:], "| exit", p.returncode, "|", x.replace("\x00", "").strip()[:1500], file=LOG)
        return p.returncode
    except Exception as e:
        print(time.strftime("%H:%M:%S"), ">", " ".join(a)[-90:], "| HATA", e, file=LOG); return -1
k = r(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", r"C:\Projeler\omer-skills\tools\kurulum_lightpanda.ps1"], 300)
r(["wsl", "-e", "bash", "-lc", "ls -la ~/.local/bin/lightpanda && ~/.local/bin/lightpanda version 2>&1 | head -3"], 60)
print("SONUC", "KURULDU-KANITLI" if k == 0 else "HATA", time.strftime("%H:%M:%S"), file=LOG)
