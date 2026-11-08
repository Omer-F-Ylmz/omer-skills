param([string]$User = 'thuglord\pc')
$ErrorActionPreference = 'Continue'
$log = 'C:\Projeler\omer-skills\.kos\kopru\rapor\yonetici-1.log'
function L($m) { ("{0} {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) | Out-File -FilePath $log -Append -Encoding utf8 }
L 'basladi'
# a) Docker
try {
    Set-Service com.docker.service -StartupType Automatic; L 'docker startup=Automatic'
    Start-Service com.docker.service; L 'docker service started'
} catch { L "docker hata: $_" }
try {
    if (-not (Get-LocalGroupMember -Group 'docker-users' -Member $User -ErrorAction SilentlyContinue)) {
        Add-LocalGroupMember -Group 'docker-users' -Member $User; L "docker-users eklendi: $User"
    } else { L "docker-users zaten uye: $User" }
} catch { L "docker-users hata: $_" }
# b) SQL Server: durdur + Manual (kaldirma yok)
foreach ($s in (Get-Service 'MSSQL*','SQLAgent*','SQLBrowser','SQLTELEMETRY*','SQLWriter' -ErrorAction SilentlyContinue)) {
    try {
        if ($s.Status -eq 'Running') { Stop-Service $s.Name -Force }
        if ($s.StartType -ne 'Disabled') { Set-Service $s.Name -StartupType Manual }
        L "sql $($s.Name): durdu, Manual"
    } catch { L "sql $($s.Name) hata: $_" }
}
# c) BSOD dokumleri
$desk = [Environment]::GetFolderPath('Desktop', 'None')
$prof = (Get-CimInstance Win32_UserProfile | ? { $_.LocalPath -like '*\pc' } | select -First 1).LocalPath
$base = Get-ChildItem (Join-Path $prof 'Desktop') -Directory | ? { $_.Name -like 'Claude ile yap*' } | select -First 1
$dst = Join-Path $base.FullName 'bsod'
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item 'C:\Windows\Minidump\*.dmp' $dst -Force -ErrorAction Continue
Get-ChildItem 'C:\Windows\LiveKernelReports' -Recurse -Filter *.dmp -ErrorAction SilentlyContinue | sort LastWriteTime -Desc | select -First 3 | % { Copy-Item $_.FullName (Join-Path $dst ($_.Directory.Name + '_' + $_.Name)) -Force }
$m = Get-Item 'C:\Windows\MEMORY.DMP' -ErrorAction SilentlyContinue
if ($m) { if ($m.Length -gt 5GB) { L "MEMORY.DMP >5GB ($($m.Length)), kopyalanmadi: C:\Windows\MEMORY.DMP" } else { Copy-Item $m.FullName $dst -Force; L 'MEMORY.DMP kopyalandi' } }
icacls $dst /grant "${User}:(OI)(CI)R" /T | Out-Null
L "bsod kopyalandi: $dst"
L 'bitti'
