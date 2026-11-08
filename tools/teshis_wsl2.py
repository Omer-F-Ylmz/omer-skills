import subprocess as s, time
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\teshis_wsl2.log", "w", encoding="utf-8", buffering=1)
def r(a, t=40):
    try:
        p = s.run(a, capture_output=True, timeout=t)
        o = (p.stdout + p.stderr)
        x = o.decode("utf-16-le", "ignore") if o[1:2] == b"\x00" else o.decode("utf-8", "ignore")
        print(">", " ".join(a), "| exit", p.returncode, "\n", x.replace("\x00", "").strip()[:1200], file=LOG)
    except Exception as e:
        print(">", " ".join(a), "| HATA", e, file=LOG)
print(time.strftime("%H:%M:%S"), file=LOG)
r(["wsl", "-l", "-v"], 20)
r(["wsl", "-d", "Ubuntu", "-e", "echo", "WSL_OK"], 40)
r(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | ? { $_.Name -match 'winget|powershell|npcap|nmap|msiexec|cargo|kur_hepsi' } | % { '{0}|{1}|{2}' -f $_.ProcessId,$_.ParentProcessId,$_.CommandLine }"], 30)
print("BITTI", time.strftime("%H:%M:%S"), file=LOG)
