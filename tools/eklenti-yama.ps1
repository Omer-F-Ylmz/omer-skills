# Plugin cache'teki hooks.json'dan YALNIZ komutu -Desen'e uyan hook girdilerini çıkarır.
#   .\tools\eklenti-yama.ps1 -Plugin context-mode -Desen 'pretooluse\.mjs'   # yedek al + çıkar
#   .\tools\eklenti-yama.ps1 -Plugin context-mode -Geri                       # yedekten döner
# Idempotent: yedek (hooks.json.bak-yama) yalnız bir kez alınır, eşleşme yoksa dosya değişmez.
# Plugin güncellenince (yeni sürüm klasörü) yeniden çalıştırılır. Önce resmi env bayrağı denenmeli.
param([Parameter(Mandatory)][string]$Plugin, [string]$Desen, [switch]$Geri)
$ErrorActionPreference = 'Stop'
$kok = Join-Path $env:USERPROFILE '.claude\plugins\cache'
$dosyalar = Get-ChildItem $kok -Directory | ForEach-Object { Join-Path $_.FullName "$Plugin\*\hooks\hooks.json" } | Where-Object { Test-Path $_ } | Get-Item
if (-not $dosyalar) { throw "hooks.json bulunamadı: $Plugin" }
$utf8 = New-Object System.Text.UTF8Encoding($false)

foreach ($d in $dosyalar) {
  $yedek = "$($d.FullName).bak-yama"
  if ($Geri) {
    if (-not (Test-Path $yedek)) { throw "Yedek yok: $yedek" }
    Copy-Item $yedek $d.FullName -Force; Write-Output "Geri alındı: $($d.FullName)"; continue
  }
  if (-not $Desen) { throw '-Desen gerekli' }
  $j = Get-Content $d.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  $cikan = 0
  foreach ($ev in @($j.hooks.PSObject.Properties)) {
    $gruplar = foreach ($g in @($ev.Value)) {
      $kalan = @($g.hooks | Where-Object { $_.command -notmatch $Desen })
      $cikan += @($g.hooks).Count - $kalan.Count
      if ($kalan.Count) { $g.hooks = $kalan; $g }
    }
    $ev.Value = @($gruplar)
  }
  if (-not $cikan) { Write-Output "Eşleşme yok (zaten yamalı olabilir): $($d.FullName)"; continue }
  if (-not (Test-Path $yedek)) { Copy-Item $d.FullName $yedek }
  [System.IO.File]::WriteAllText($d.FullName, ($j | ConvertTo-Json -Depth 100), $utf8)
  Write-Output "-$cikan hook girdisi: $($d.FullName)"
}
