import subprocess as s, time, sys
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\winget_onar.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def r(a, t):
    t0 = time.time()
    try:
        x = s.run(a, capture_output=True, timeout=t); o = (x.stdout + x.stderr).decode("utf-8", "ignore")
        p(f"{time.time()-t0:.0f}sn", " ".join(a), "| exit", x.returncode, "|", o.strip()[-500:])
    except Exception as e: p(f"{time.time()-t0:.0f}sn", " ".join(a), "| ZAMAN ASIMI", e)
p("581 dk'dir acik WindowsPackageManagerServer + takili show kapatiliyor (istek gelince kendiligindan yeniden baslar)")
r(["taskkill", "/F", "/IM", "WindowsPackageManagerServer.exe"], 30)
r(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match ' show ' } | % { Stop-Process -Id $_.ProcessId -Force; 'kapatildi ' + $_.ProcessId }"], 40)
time.sleep(3)
r(["winget", "show", "--id", "Helm.Helm", "-e", "--source", "winget", "--accept-source-agreements", "--disable-interactivity"], 180)
r(["winget", "install", "--id", "Helm.Helm", "-e", "--source", "winget", "--silent", "--accept-package-agreements", "--accept-source-agreements", "--disable-interactivity"], 400)
r(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | ? { $_.Name -eq 'winget.exe' } | % { '{0} {1}dk {2}' -f $_.ProcessId,[int]((Get-Date)-$_.CreationDate).TotalMinutes,$_.CommandLine }"], 40)
p("BITTI")
