# TOKEN-6d: Headroom Desktop'u normal ortamla baslatir; HEADROOM_DISABLE_FEATURES User
# kaydindan yeniden yuklenir (yazdirilmaz).
# Kullanim (yeni bir PowerShell penceresinden, Desktop tepsiden Quit edildikten sonra):
#   powershell -ExecutionPolicy Bypass -File C:\Projeler\omer-skills\.claude\token6d\hr_deney_bitir.ps1
$ErrorActionPreference = 'Stop'
$exe = Join-Path $env:LOCALAPPDATA 'Headroom\headroom-desktop.exe'
if (-not (Test-Path $exe)) { throw "headroom-desktop.exe bulunamadi: $exe" }
if (Get-Process headroom-desktop -ErrorAction SilentlyContinue) { throw 'Desktop calisiyor: once tepsiden Quit et.' }
if (Get-CimInstance Win32_Process -Filter "Name='headroom.exe'" | Where-Object { $_.CommandLine -match ' proxy ' }) {
    throw 'Deney proxy sureci hala calisiyor: Desktop kapanisini bekle, sonra yeniden kos.'
}
$ham = [Environment]::GetEnvironmentVariable('HEADROOM_DISABLE_FEATURES', 'User')
if ($ham) { $env:HEADROOM_DISABLE_FEATURES = $ham }
else { Remove-Item Env:HEADROOM_DISABLE_FEATURES -ErrorAction SilentlyContinue }
Start-Process -FilePath $exe
'Desktop normal ortamla baslatildi.'
