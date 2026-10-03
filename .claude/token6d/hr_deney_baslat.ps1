# TOKEN-6d: Headroom Desktop'u yalniz bu surecin ortaminda, HEADROOM_DISABLE_FEATURES'tan
# proxy_output_shaper suzulmus olarak baslatir. User env'e dokunmaz, deger yazdirmaz.
# Kullanim (yeni bir PowerShell penceresinden, Desktop tepsiden Quit edildikten sonra):
#   powershell -ExecutionPolicy Bypass -File C:\Projeler\omer-skills\.claude\token6d\hr_deney_baslat.ps1
$ErrorActionPreference = 'Stop'
$exe = Join-Path $env:LOCALAPPDATA 'Headroom\headroom-desktop.exe'
if (-not (Test-Path $exe)) { throw "headroom-desktop.exe bulunamadi: $exe" }
if (Get-Process headroom-desktop -ErrorAction SilentlyContinue) { throw 'Desktop calisiyor: once tepsiden Quit et.' }
if (Get-CimInstance Win32_Process -Filter "Name='headroom.exe'" | Where-Object { $_.CommandLine -match ' proxy ' }) {
    throw 'Eski proxy sureci hala calisiyor: Desktop kapanisini bekle, sonra yeniden kos.'
}
$ham = [Environment]::GetEnvironmentVariable('HEADROOM_DISABLE_FEATURES', 'User')
$adlar = @("$ham" -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
$kalan = @($adlar | Where-Object { $_.ToLower().Replace('-', '_') -ne 'proxy_output_shaper' })
"shaper listedeydi: $($adlar.Count -ne $kalan.Count) | kalan ad sayisi: $($kalan.Count)"
if ($kalan.Count) { $env:HEADROOM_DISABLE_FEATURES = $kalan -join ',' }
else { Remove-Item Env:HEADROOM_DISABLE_FEATURES -ErrorAction SilentlyContinue }
Start-Process -FilePath $exe
'Desktop deney ortamiyla baslatildi.'
