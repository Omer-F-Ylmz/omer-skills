import subprocess as s, time, sys, os
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\hizlandir.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def ps(c, t=60):
    return s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=t).stdout.strip()
p("== RAM en buyuk 20 (MB)")
p("\n" + ps("Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 20 | % { '{0,6} {1,-22} {2}' -f [int]($_.WorkingSet64/1MB),$_.ProcessName,$_.Id }"))
p("== ada gore toplam (MB)")
p("\n" + ps("Get-Process | Group-Object ProcessName | % { [pscustomobject]@{n=$_.Name;c=$_.Count;mb=[int](($_.Group|Measure-Object WorkingSet64 -Sum).Sum/1MB)} } | Sort-Object mb -Descending | Select-Object -First 12 | % { '{0,6} x{1,-3} {2}' -f $_.mb,$_.c,$_.n }"))
p("== takili winget search")
p(ps("Get-CimInstance Win32_Process | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match ' search ' } | % { $pp=$_.ProcessId; $b=(Get-Date)-$_.CreationDate; '{0} {1}dk {2}' -f $pp,[int]$b.TotalMinutes,$_.CommandLine }"))
p(ps("Get-CimInstance Win32_Process | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match ' search ' -and ((Get-Date)-$_.CreationDate).TotalMinutes -gt 30 } | % { Stop-Process -Id $_.ProcessId -Force; 'kapatildi ' + $_.ProcessId }"))
p("== mukerrer claude-mem / chroma / mcp-proxy")
p("\n" + ps("Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'claude-mem-mcp|mcp-server.cjs|chroma-mcp|mcp-proxy' } | % { '{0} ebeveyn={1} {2}dk {3}MB {4}' -f $_.ProcessId,$_.ParentProcessId,[int]((Get-Date)-$_.CreationDate).TotalMinutes,[int]($_.WorkingSetSize/1MB),($_.CommandLine -replace '.*\\\\','') }"))
p("== RAM %", ps("$o=Get-CimInstance Win32_OperatingSystem; [int](100-($o.FreePhysicalMemory/$o.TotalVisibleMemorySize*100))"))
p("BITTI")
