$ErrorActionPreference = "Continue"
Start-Transcript -Path "C:\Projeler\omer-skills\.kos\kopru\desktop_duzelt.log" -Force | Out-Null
$kok = "C:\Projeler\omer-skills"
function DeskSurec { Get-Process -Name claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -notlike "*\.local\bin\*" } }
Write-Host "1/4 Claude Desktop kapatiliyor (Claude Code CLI ve ajanlara dokunulmaz)..."
$exe = (DeskSurec | Select-Object -First 1).Path
DeskSurec | ForEach-Object { $_.CloseMainWindow() | Out-Null }
for ($i = 0; $i -lt 20; $i++) { Start-Sleep -Milliseconds 500; if (-not (DeskSurec)) { break } }
if (DeskSurec) { DeskSurec | Stop-Process -Force; Start-Sleep -Seconds 2 }
Write-Host "2/4 Ayar duzeltiliyor (rea compact + code-mode + hostinger, komutlar tam yol)..."
python -I "$kok\onay\rea_fix_6.py" 2>&1 | Out-Host
Write-Host "3/4 Claude Desktop aciliyor (bu pencereden bagimsiz)..."
if ($exe -and (Test-Path $exe)) { Start-Process -FilePath "explorer.exe" -ArgumentList "`"$exe`"" } else { Write-Host "Claude Desktop'u elle ac." }
Write-Host "4/4 25 sn sonra Desktop'un ayari silip silmedigi kontrol ediliyor..."
Start-Sleep -Seconds 25
python -I "$kok\onay\rea_fix_6.py" --kuru 2>&1 | Out-Host
Write-Host ""
Write-Host "'degisecek: -' yaziyorsa ayar kalici. Bu pencereyi kapatabilirsin; Desktop etkilenmez."
Stop-Transcript | Out-Null
pause
