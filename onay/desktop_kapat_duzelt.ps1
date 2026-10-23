$ErrorActionPreference = "Continue"
$py = "python"
$kok = "C:\Projeler\omer-skills"
Write-Host "1/4 Claude Desktop kapatiliyor (Claude Code CLI'ya dokunulmaz)..."
$desk = Get-Process -Name claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -notlike "*\.local\bin\*" }
$exe = ($desk | Select-Object -First 1).Path
$desk | ForEach-Object { $_.CloseMainWindow() | Out-Null }
for ($i = 0; $i -lt 20; $i++) {
  Start-Sleep -Milliseconds 500
  $kalan = Get-Process -Name claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -notlike "*\.local\bin\*" }
  if (-not $kalan) { break }
}
$kalan = Get-Process -Name claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -notlike "*\.local\bin\*" }
if ($kalan) { $kalan | Stop-Process -Force; Start-Sleep -Seconds 2 }
Write-Host "2/4 Ayar duzeltiliyor (rea compact + code-mode + hostinger)..."
& $py -I "$kok\onay\rea_fix_6.py"
& $py -I "$kok\onay\config_fark.py" --esitle
Write-Host "3/4 Dogrulama:"
& $py -I "$kok\onay\rea_fix_6.py" --kuru
Write-Host "4/4 Claude Desktop aciliyor..."
if ($exe -and (Test-Path $exe)) { Start-Process $exe } else { Write-Host "Claude Desktop'u elle ac." }
Start-Sleep -Seconds 3
