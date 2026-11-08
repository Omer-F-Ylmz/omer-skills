import subprocess as s, time, sys, os
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\hizlandir2.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def ps(c, t=90):
    return s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=t).stdout.strip()
p("== buyukler")
p("\n" + ps("Get-CimInstance Win32_Process | ? { $_.WorkingSetSize -gt 180MB } | Sort-Object WorkingSetSize -Descending | % { '{0,6}MB {1} ebeveyn={2} {3}dk {4}' -f [int]($_.WorkingSetSize/1MB),$_.ProcessId,$_.ParentProcessId,[int]((Get-Date)-$_.CreationDate).TotalMinutes,(($_.CommandLine -replace '\\s+',' ') -replace '^(.{0,230}).*','$1') }"))
p("== svchost 28536 hizmetleri")
p(ps("Get-CimInstance Win32_Service | ? { $_.ProcessId -eq 28536 } | % { $_.Name + ' / ' + $_.DisplayName }"))
p("== node gruplari (ebeveyne gore)")
p("\n" + ps("Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Group-Object ParentProcessId | Sort-Object Count -Descending | Select-Object -First 8 | % { $pp=[int]$_.Name; $par=(Get-CimInstance Win32_Process -Filter \"ProcessId=$pp\" -ErrorAction SilentlyContinue); '{0} adet {1}MB ebeveyn={2} {3}' -f $_.Count,[int](($_.Group|Measure-Object WorkingSetSize -Sum).Sum/1MB),$pp,(($par.CommandLine -replace '\\s+',' ') -replace '^(.{0,160}).*','$1') }"))
p("== METASPLOIT: gem dizini sikistirmasini kaldir + bundle install")
g = os.path.expanduser(r"~\.local\share\gem")
r = s.run(["compact", "/u", "/s:" + g, "/i", "/q"], capture_output=True, timeout=900)
p("compact /u exit", r.returncode, (r.stdout + r.stderr).decode("cp857", "ignore").strip()[-300:])
r = s.run(["compact", "/u", "/exe", "/s:" + g, "/i", "/q"], capture_output=True, timeout=900)
p("compact /u /exe exit", r.returncode, (r.stdout + r.stderr).decode("cp857", "ignore").strip()[-300:])
msf = r"C:\Projeler\_araclar\v\rapid7__metasploit-framework"
bl = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "guvenlik", "_indir", "msf-bundle2.log")
with open(bl, "w", encoding="utf-8") as f:
    r = s.run("bundle install", cwd=msf, shell=True, stdout=f, stderr=s.STDOUT, timeout=3000)
p("bundle install exit", r.returncode, "log:", bl)
p("RAM %", ps("$o=Get-CimInstance Win32_OperatingSystem; [int](100-($o.FreePhysicalMemory/$o.TotalVisibleMemorySize*100))"))
p("BITTI")
