# skillOverrides bloğunu ~/.claude/settings.json'a birleştirir; başka anahtara dokunmaz.
#   .\tools\overrides-uygula.ps1          # yedek al + birleştir (mevcut anahtarlar korunur)
#   .\tools\overrides-uygula.ps1 -Geri    # yedekten döner
# Windows PowerShell 5.1: ConvertTo-Json -Depth 100 şart (varsayılan 2 iç içe nesneyi keser).
param([switch]$Geri)
$ErrorActionPreference = 'Stop'
$ayar = Join-Path $env:USERPROFILE '.claude\settings.json'
$yedek = "$ayar.bak-overrides"
$kok = Split-Path $PSScriptRoot -Parent
$blok = Join-Path $kok '.kos\kurulum-2\overrides.json'
$utf8 = New-Object System.Text.UTF8Encoding($false)

if ($Geri) {
  if (-not (Test-Path $yedek)) { throw "Yedek yok: $yedek" }
  Copy-Item $yedek $ayar -Force
  Write-Output "Geri alındı: $yedek -> $ayar"; return
}

if (-not (Test-Path $blok)) { throw "Blok yok: $blok" }
Copy-Item $ayar $yedek -Force
$s = Get-Content $ayar -Raw -Encoding UTF8 | ConvertFrom-Json
$yeni = Get-Content $blok -Raw -Encoding UTF8 | ConvertFrom-Json
$mevcut = [ordered]@{}
if ($s.PSObject.Properties['skillOverrides']) {
  foreach ($p in $s.skillOverrides.PSObject.Properties) { $mevcut[$p.Name] = $p.Value }
}
$eklenen = 0
foreach ($p in $yeni.PSObject.Properties) {
  if (-not $mevcut.Contains($p.Name)) { $mevcut[$p.Name] = $p.Value; $eklenen++ }   # mevcut kullanıcı kararı ezilmez
}
if ($s.PSObject.Properties['skillOverrides']) { $s.skillOverrides = [pscustomobject]$mevcut }
else { $s | Add-Member -NotePropertyName skillOverrides -NotePropertyValue ([pscustomobject]$mevcut) }
[System.IO.File]::WriteAllText($ayar, ($s | ConvertTo-Json -Depth 100), $utf8)
Write-Output "skillOverrides: +$eklenen anahtar (toplam $($mevcut.Count)). Yedek: $yedek"
