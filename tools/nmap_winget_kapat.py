import subprocess as s, time
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\nmap_winget_kapat.log", "w", encoding="utf-8", buffering=1)
def r(a, t=40):
    p = s.run(a, capture_output=True, timeout=t)
    x = (p.stdout + p.stderr).decode("cp857", "ignore")
    print(time.strftime("%H:%M:%S"), " ".join(a)[-80:], "| exit", p.returncode, "|", x.strip()[:1200], file=LOG)
q = "Get-CimInstance Win32_Process | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match 'Insecure.Nmap' } | % { $_.ProcessId }"
pids = s.run(["powershell", "-NoProfile", "-Command", q], capture_output=True, text=True, timeout=40).stdout.split()
print("nmap winget pid:", pids, file=LOG)
for p in pids:
    r(["taskkill", "/PID", p, "/T", "/F"])
time.sleep(20)
r(["powershell", "-NoProfile", "-Command", "Get-Content 'C:\\Projeler\\omer-skills\\rapor\\kur-hepsi-sonuc.tsv' -Tail 4; Get-Content 'C:\\Projeler\\omer-skills\\rapor\\kurulum-guvenlik-sonuc.tsv' -Tail 6"])
print("BITTI", file=LOG)
