# 6 Kas: sayfalama dosyasini otomatikten sabit 44 GB'a ceker (61 GB -> 44 GB, ~+17 GB). Yonetici + yeniden baslatma gerekir.
# Neden 44: olculen commit 67,5 GB; limit = 32 GB RAM + sayfa. 44 -> limit 76 GB (%12 pay). Daha kucugu = bellek yetersiz cokmesi.
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""; exit }
$log = 'C:\Projeler\omer-skills\tools\sayfa_dosyasi.log'
$cs = Get-CimInstance Win32_ComputerSystem
Set-CimInstance -InputObject $cs -Property @{AutomaticManagedPagefile = $false}
$pf = Get-CimInstance Win32_PageFileSetting -Filter "Name='C:\\pagefile.sys'"
if (-not $pf) { $pf = New-CimInstance -ClassName Win32_PageFileSetting -Property @{Name='C:\pagefile.sys'} }
Set-CimInstance -InputObject $pf -Property @{InitialSize = 45056; MaximumSize = 45056}
"$(Get-Date) ayarlandi: $((Get-CimInstance Win32_PageFileSetting | Out-String).Trim())" | Tee-Object -FilePath $log -Append
Write-Host 'TAMAM - etkinlesmesi icin bilgisayari yeniden baslatin (ajanlar durur).'; Start-Sleep 8
