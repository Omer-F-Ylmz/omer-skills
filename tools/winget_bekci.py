import subprocess as s, time, sys
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\winget_bekci.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "a", encoding="utf-8", buffering=1)
def ps(c): return s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=90).stdout.strip()
KOD = r"""
$all = Get-CimInstance Win32_Process
$all | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match ' install ' } | % {
  $dk=[int]((Get-Date)-$_.CreationDate).TotalMinutes; $id=$_.ProcessId
  $c = @($all | ? { $_.ParentProcessId -eq $id })
  $kur = @($all | ? { $_.Name -match 'msiexec|setup|install' -and ((Get-Date)-$_.CreationDate).TotalMinutes -lt ($dk+1) })
  if ($dk -ge 12 -and $c.Count -eq 0 -and $kur.Count -eq 0) { Stop-Process -Id $id -Force; 'KAPATILDI ' + $id + ' ' + $dk + 'dk ' + ($_.CommandLine -replace '.*--id\s+(\S+).*','$1') }
}
if (Get-Process -Id 42104 -ErrorAction SilentlyContinue) { 'KUR_HEPSI_CALISIYOR' } else { 'KUR_HEPSI_BITTI' }
"""
print(time.strftime("%H:%M:%S"), "bekci basladi", file=LOG)
while True:
    o = ps(KOD)
    for l in o.splitlines():
        if l.startswith("KAPATILDI"): print(time.strftime("%H:%M:%S"), l, file=LOG)
    if "KUR_HEPSI_BITTI" in o:
        print(time.strftime("%H:%M:%S"), "kur_hepsi bitti, bekci cikiyor", file=LOG); break
    time.sleep(60)
