param([switch]$Baslat)
$ErrorActionPreference = 'Stop'
$src = 'C:\Users\pc\Apps\lightpanda\lightpanda-x86_64-linux'
$beklenen = '53eb34da09159dcf8f04865dbfe3e63e9a652062684495aa7ced5ddd7c82e8b0'

if ($Baslat) {
    wsl -e bash -lc 'LIGHTPANDA_DISABLE_TELEMETRY=true exec ~/.local/bin/lightpanda serve --host 127.0.0.1 --port 9222'
    exit $LASTEXITCODE
}

if (-not (Test-Path $src)) { throw "ikili yok: $src" }
$h = (Get-FileHash $src -Algorithm SHA256).Hash.ToLower()
if ($h -ne $beklenen) { throw "SHA256 uyusmuyor: $h" }
Write-Host "SHA256 dogru (GitHub release 1.0.3 digest)"

wsl -e bash -lc 'mkdir -p ~/.local/bin && install -m 755 /mnt/c/Users/pc/Apps/lightpanda/lightpanda-x86_64-linux ~/.local/bin/lightpanda'
if ($LASTEXITCODE -ne 0) { Write-Host "HATA: WSL'e kopyalanamadi (exit $LASTEXITCODE). WSL calisiyor mu: wsl --shutdown sonra wsl -e true"; exit 1 }
wsl -e bash -lc 'grep -q LIGHTPANDA_DISABLE_TELEMETRY ~/.profile || echo "export LIGHTPANDA_DISABLE_TELEMETRY=true" >> ~/.profile'
if ($LASTEXITCODE -ne 0) { Write-Host "HATA: ~/.profile yazilamadi (exit $LASTEXITCODE)"; exit 1 }
$v = wsl -e bash -lc '~/.local/bin/lightpanda -h 2>&1 | head -5'
if ($LASTEXITCODE -ne 0 -or -not $v) { Write-Host "HATA: lightpanda calismadi (exit $LASTEXITCODE)"; exit 1 }
$v | ForEach-Object { Write-Host $_ }
Write-Host "Kuruldu. Baslatmak: .\tools\kurulum_lightpanda.ps1 -Baslat  (CDP: ws://127.0.0.1:9222, yalniz yerel)"
