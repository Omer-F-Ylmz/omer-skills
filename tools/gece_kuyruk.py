import subprocess as s, time, sys, os
K = r"C:\Projeler\omer-skills"
LOGP = K + r"\.kos\kopru\log\gece_kuyruk.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], cwd=K, creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
if sys.argv[1] != "calis":
    print("kullanim: gece_kuyruk.py [calis]  (arguman yoksa arka planda baslatir)"); sys.exit(2)
LOG = open(LOGP, "a", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def ps(c, t=90): return s.run(["powershell", "-NoProfile", "-Command", c], capture_output=True, text=True, errors="ignore", timeout=t).stdout.strip()
# 1) winget bekcisi: eskiyi kapat, yenisi: tasinabilirle kurulanlar hemen, digerleri 5 dk cocuksuz bekleyince kapatilir
ps("Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'winget_bekci.py' } | % { Stop-Process -Id $_.ProcessId -Force }")
BEKCI = r"""
$hazir = 'Helm.Helm|zig.zig|Hashicorp.Terraform|JetBrains.Kotlin.Compiler|Google.DartSDK|Insecure.Nmap|skylot.jadx'
$all = Get-CimInstance Win32_Process
$all | ? { $_.Name -eq 'winget.exe' -and $_.CommandLine -match ' (install|show) ' } | % {
  $dk=((Get-Date)-$_.CreationDate).TotalMinutes; $id=$_.ProcessId
  $c = @($all | ? { $_.ParentProcessId -eq $id })
  $kur = @($all | ? { $_.Name -match 'msiexec|setup|install' -and ((Get-Date)-$_.CreationDate).TotalMinutes -lt ($dk+1) })
  $tasinabilir = $_.CommandLine -match $hazir
  if ($tasinabilir -or ($dk -ge 5 -and $c.Count -eq 0 -and $kur.Count -eq 0)) { Stop-Process -Id $id -Force; 'KAPATILDI ' + $id + ' ' + [int]$dk + 'dk ' + $(if($tasinabilir){'(tasinabilir kuruldu) '}else{''}) + ($_.CommandLine -replace '.*--id\s+(\S+).*','$1') }
}
"""
def bekci_tur():
    for l in ps(BEKCI).splitlines():
        if l.startswith("KAPATILDI"): p("BEKCI", l)
def kos(ad, argv, tavan_sn):
    p("BASLA", ad)
    lg = open(K + rf"\.kos\kopru\log\gece_{ad}.log", "w", encoding="utf-8")
    pr = s.Popen(argv, cwd=K, stdout=lg, stderr=s.STDOUT, creationflags=0x08000000)
    t0 = time.time()
    while pr.poll() is None and time.time() - t0 < tavan_sn:
        bekci_tur(); time.sleep(60)
    if pr.poll() is None: pr.kill(); p("ZAMAN ASIMI", ad)
    p("BITTI", ad, "exit", pr.returncode, f"{(time.time()-t0)/60:.0f}dk")
KH = "Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'kur_hepsi\.ps1' -and $_.Name -eq 'powershell.exe' } | % { $_.ProcessId }"
def kh_var(): return bool(ps(KH))
p("== gece kuyrugu basladi; kur_hepsi bitene kadar bekleniyor (ayni kurulum_d2 dosyalarina iki is yazmasin)")
while kh_var():
    bekci_tur(); time.sleep(60)
p("kur_hepsi bitti, kuyruk basliyor")
psx = r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe"
kos("kur_tur2", [psx, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", K + r"\tools\kurulum_tur2.ps1"], 4 * 3600)
kos("coz6", [sys.executable, "-I", K + r"\tools\kurulum_d2.py", "--faz", "kur", "--coz", K + r"\docs\video-tarama\kurulum-coz-6.tsv", "--sinif", "SKILL,CLI,PAKET"], 4 * 3600)
# kur_hepsi bitene kadar bekci
p("== kuyruk bitti")
