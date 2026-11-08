import subprocess as s, time, os, glob, shutil, sys
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
K = r"C:\Projeler\omer-skills"
B = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "borsa-botu")
LOG = open(K + r"\.kos\kopru\log\kontrol_acilis.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(*a, file=LOG)
def ps(c, t=90): return s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=t).stdout.strip()
def kuyruk(f, n):
    try:
        with open(f, encoding="utf-8", errors="ignore") as h: return h.read().splitlines()[-n:]
    except Exception as e: return [f"YOK {e}"]
p(time.strftime("%H:%M:%S"), "acilis", ps("(Get-CimInstance Win32_OperatingSystem).LastBootUpTime"))
p("RAM %", ps("$o=Get-CimInstance Win32_OperatingSystem; [int](100-($o.FreePhysicalMemory/$o.TotalVisibleMemorySize*100))"), "| bos GB", round(shutil.disk_usage("C:/").free / 1e9, 1))
p("== python", s.run(["python", "--version"], capture_output=True, text=True, errors="ignore").stdout.strip())
p("== kur-hepsi"); [p(l) for l in kuyruk(K + r"\rapor\kur-hepsi-sonuc.tsv", 4)]
p("== ilgili surecler")
p(ps("Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'kur_hepsi|kurulum_|egit|borsa|arka_ajan|yonetici_gorev|gece_kuyruk|winget|claude.exe -p' } | % { '{0}|{1}|{2}dk|{3}' -f $_.ProcessId,$_.Name,[int]((Get-Date)-$_.CreationDate).TotalMinutes,(($_.CommandLine -replace '\\s+',' ') -replace '^(.{0,200}).*','$1') }"))
p("== borsa egit.log"); [p(l[:170]) for l in kuyruk(B + r"\kayit\egit.log", 4)]
p("== borsa kayit dosyalari")
for f in sorted(glob.glob(B + r"\kayit\*"), key=os.path.getmtime, reverse=True)[:10]:
    p(" ", os.path.basename(f), time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(f))), os.path.getsize(f))
p("== baslangic gorevleri")
p(ps("Get-ScheduledTask | ? { $_.TaskName -match 'omer|borsa|egit|arka|yonetici|kos' } | % { $_.TaskName + ' ' + $_.State }"))
p(ps("Get-ChildItem \"$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\" | % { $_.Name }"))
p("== liste-eksik-2"); [p(l[:200]) for l in kuyruk(K + r"\.kos\kopru\arka\liste-eksik-2.log", 6)]
p("BITTI")
