import subprocess as s, time
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\winget_takili.log", "w", encoding="utf-8", buffering=1)
def ps(c): return s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=60).stdout.strip()
kod = r"""
$all = Get-CimInstance Win32_Process
function Cocuk($id,$d){ $all | ? { $_.ParentProcessId -eq $id } | % { ('  '*$d) + $_.ProcessId + ' ' + $_.Name + ' ' + [int]((Get-Date)-$_.CreationDate).TotalMinutes + 'dk'; Cocuk $_.ProcessId ($d+1) } }
$all | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match ' install ' } | % {
  $dk=[int]((Get-Date)-$_.CreationDate).TotalMinutes
  'WINGET ' + $_.ProcessId + ' ' + $dk + 'dk ' + ($_.CommandLine -replace '.*--id\s+(\S+).*','$1')
  $c = @(Cocuk $_.ProcessId 1); $c
  $kurucu = $all | ? { $_.Name -match 'msiexec|setup|install|podman' -and ((Get-Date)-$_.CreationDate).TotalMinutes -lt ($dk+1) }
  $kurucu | % { '  ADAY-KURUCU ' + $_.ProcessId + ' ' + $_.Name + ' ebeveyn=' + $_.ParentProcessId }
  if ($dk -gt 15 -and $c.Count -eq 0 -and -not $kurucu) { Stop-Process -Id $_.ProcessId -Force; '  KAPATILDI (UAC bekliyordu, cocuk sureci yok)' }
}
$all | ? { $_.Name -eq 'consent.exe' } | % { 'UAC PENCERESI ACIK consent.exe ' + $_.ProcessId }
"""
print(time.strftime("%H:%M:%S"), "\n" + ps(kod), file=LOG)
print("BITTI", file=LOG)
