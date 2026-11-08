import subprocess as s, time, os, sys
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\teshis_wsl3.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def r(a, t):
    try:
        p = s.run(a, capture_output=True, timeout=t)
        o = p.stdout + p.stderr
        x = o.decode("utf-16-le", "ignore") if o[1:2] == b"\x00" else o.decode("utf-8", "ignore")
        print(time.strftime("%H:%M:%S"), ">", " ".join(a), "| exit", p.returncode, "|", x.replace("\x00", "").strip()[:800], file=LOG)
    except Exception as e:
        print(time.strftime("%H:%M:%S"), ">", " ".join(a), "| HATA", e, file=LOG)
r(["tasklist", "/fi", "imagename eq wsl.exe"], 15)
r(["wsl", "--shutdown"], 120)
r(["wsl", "-l", "-v"], 60)
r(["wsl", "-d", "Ubuntu", "-e", "echo", "WSL_OK"], 120)
r(["wsl", "-d", "Ubuntu", "-e", "sh", "-c", "ls -la ~/lightpanda* /usr/local/bin/lightpanda* 2>&1"], 60)
r(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | ? { $_.Name -match 'winget|nmap|npcap|consent|msiexec|setup' } | % { '{0}|{1}|{2}' -f $_.ProcessId,$_.Name,$_.CommandLine }"], 40)
print("BITTI", time.strftime("%H:%M:%S"), file=LOG)
