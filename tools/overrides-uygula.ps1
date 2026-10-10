# skillOverrides + env bloklarını ~/.claude/settings.json'a birleştirir; başka anahtara dokunmaz.
#   .\tools\overrides-uygula.ps1          # yedek al + birleştir (mevcut anahtarlar korunur)
#   .\tools\overrides-uygula.ps1 -Geri    # yedekten döner
# Windows PowerShell 5.1: ConvertTo-Json -Depth 100 şart (varsayılan 2 iç içe nesneyi keser).
#   .\tools\overrides-uygula.ps1 -Blok overrides-ek.json   # .kos\kurulum-2\ altındaki başka blok (varsayılan overrides.json)
param([switch]$Geri, [string]$Blok = 'overrides.json')
$ErrorActionPreference = 'Stop'
$ayar = Join-Path $env:USERPROFILE '.claude\settings.json'
$yedek = "$ayar.bak-overrides"
$kok = Split-Path $PSScriptRoot -Parent
$blok = Join-Path $kok (Join-Path '.kos\kurulum-2' $Blok)
$utf8 = New-Object System.Text.UTF8Encoding($false)
# Başsız ajanı durduran/gereksiz bağlam ekleyen hook bayrakları (docs/kurulumlar/hook-karar.md)
$envEk = [ordered]@{
  ECC_GATEGUARD             = 'off'   # GateGuard fact-force ret
  OCTOPUS_AUTO_ROUTER_MODE  = 'off'   # octo istem yönlendirme/bağlam
  OCTOPUS_GITHUB_WORK_QUEUE = 'off'   # octo GitHub kuyruk izleyici
}

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

if (-not $s.PSObject.Properties['env']) { $s | Add-Member -NotePropertyName env -NotePropertyValue ([pscustomobject]@{}) }
$envEklenen = 0
foreach ($k in $envEk.Keys) {
  if (-not $s.env.PSObject.Properties[$k]) { $s.env | Add-Member -NotePropertyName $k -NotePropertyValue $envEk[$k]; $envEklenen++ }
}
[System.IO.File]::WriteAllText($ayar, ($s | ConvertTo-Json -Depth 100), $utf8)
Write-Output "skillOverrides: +$eklenen anahtar (toplam $($mevcut.Count)); env: +$envEklenen anahtar. Yedek: $yedek"
