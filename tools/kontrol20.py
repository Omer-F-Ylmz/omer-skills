import subprocess as s, time, os, glob, shutil, sys
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
K = r"C:\Projeler\omer-skills"
LOG = open(K + r"\.kos\kopru\log\kontrol20.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(*a, file=LOG)
def kuyruk(f, n):
    try:
        with open(f, encoding="utf-8", errors="ignore") as h: return h.read().splitlines()[-n:]
    except Exception as e: return [f"YOK {e}"]
p(time.strftime("%H:%M:%S"))
p("== kur-hepsi"); [p(l) for l in kuyruk(K + r"\rapor\kur-hepsi-sonuc.tsv", 5)]
for f in glob.glob(K + r"\rapor\kurulum-omer2*sonuc*") + glob.glob(K + r"\rapor\kurulum-ek*sonuc*"):
    p("==", f.replace(K, ""), time.strftime("%H:%M", time.localtime(os.path.getmtime(f)))); [p(l) for l in kuyruk(f, 6)]
p("== guvenlik"); [p(l) for l in kuyruk(K + r"\rapor\kurulum-guvenlik-sonuc.tsv", 4)]
q = ("Get-CimInstance Win32_Process | ? { $_.Name -match 'winget|bundle|ruby|7z|tar|python|powershell|claude|node' } | "
     "% { '{0}|{1}|{3}dk|ebeveyn={4}|{2}' -f $_.ProcessId,$_.Name,(($_.CommandLine -replace '\\s+',' ')),[int]((Get-Date)-$_.CreationDate).TotalMinutes,$_.ParentProcessId } ")
o = s.run(["powershell", "-NoProfile", "-Command", q], capture_output=True, text=True, errors="ignore", timeout=60).stdout
p("== surecler")
for l in o.splitlines():
    if any(k in l for k in ["winget", "bundle", "ruby", "7z", "tar.exe", "kurulum", "kur_hepsi", "liste-", "bul-kur", "kanit", "kur-tur", "usta-kat", "claude", "gorev"]):
        p(l[:260])
p("== is dosyalari")
ad = ["liste-guncel-2", "bul-kur-2", "kanit-3", "kur-tur2", "liste-eksik-2", "usta-kategori-2"]
for a in ad:
    bul = []
    for kok in [K + r"\.kos", K + r"\docs", K + r"\rapor"]:
        bul += glob.glob(kok + rf"\**\*{a}*", recursive=True)
    bul = sorted(bul, key=lambda f: os.path.getmtime(f), reverse=True)[:4]
    p(a, [(f.replace(K, ""), time.strftime("%H:%M", time.localtime(os.path.getmtime(f))), os.path.getsize(f) if os.path.isfile(f) else "DIR") for f in bul])
for f in ["gece_kuyruk.log", "gece_kur_tur2.log", "gece_coz6.log"]:
    p("==", f); [p(l) for l in kuyruk(K + r"\.kos\kopru\log\\" + f, 8)]
p("== python", s.run(["python", "--version"], capture_output=True, text=True, errors="ignore").stdout.strip(), "|", s.run(["py", "-0p"], capture_output=True, text=True, errors="ignore").stdout.strip().replace("\n", " ; "))
p("== disk/ram")
p("bos GB", round(shutil.disk_usage("C:/").free / 1e9, 1))
r = s.run(["powershell", "-NoProfile", "-Command", "$o=Get-CimInstance Win32_OperatingSystem; [int](100-($o.FreePhysicalMemory/$o.TotalVisibleMemorySize*100))"], capture_output=True, text=True, timeout=30).stdout.strip()
p("RAM %", r)
p("BITTI")
