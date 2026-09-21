<#
.SYNOPSIS
  gitleaks raporundaki konum/desene gore transkript dosyalarindaki anahtarlari maskeler.
.DESCRIPTION
  Maskeleme YALNIZ gitleaks'in buldugu esleme dizesine gore yapilir, HKCU'daki
  guncel degere gore DEGIL -- anahtar yenilenirse eslesme kaybolur, eski
  transkriptteki eski deger maskesiz kalirdi.
  Ekrana yalniz dosya adi ve eslesme sayisi basilir; degerin kendisi asla.
  Once .bak11d yedegi alinir, sonra yerinde degistirilir.
.EXAMPLE
  .\redakte-transkript.ps1 -Rapor C:\gecici\k7b-rapor.json -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [string]$Rapor
)

if (-not (Test-Path -LiteralPath $Rapor)) { throw "Rapor bulunamadi: $Rapor" }

$bulgular = Get-Content -LiteralPath $Rapor -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $bulgular) { Write-Host "Rapor bos - yapilacak is yok."; return }

$gruplar = $bulgular | Group-Object -Property File
$toplam = 0

foreach ($g in $gruplar) {
    $yol = $g.Name
    if (-not (Test-Path -LiteralPath $yol)) {
        Write-Host ("{0} : ATLANDI (dosya yok)" -f (Split-Path $yol -Leaf))
        continue
    }

    # Ayni deger birden cok kez gecebilir; benzersiz sirlari uzundan kisaya sirala
    # ki kisa bir dize uzun olanin icini parcalamasin.
    $sirlar = $g.Group | ForEach-Object { $_.Secret } | Where-Object { $_ } |
              Sort-Object -Unique | Sort-Object -Property Length -Descending

    $icerik = Get-Content -LiteralPath $yol -Raw -Encoding UTF8
    $sayac = 0
    foreach ($s in $sirlar) {
        $adet = ([regex]::Matches($icerik, [regex]::Escape($s))).Count
        if ($adet -gt 0) {
            $maske = "[REDAKTE-" + $s.Length + "-KARAKTER]"
            $icerik = $icerik.Replace($s, $maske)
            $sayac += $adet
        }
    }

    $ad = Split-Path $yol -Leaf
    if ($sayac -eq 0) {
        Write-Host ("{0} : 0 eslesme" -f $ad)
        continue
    }

    if ($PSCmdlet.ShouldProcess($ad, "$sayac eslesme maskele")) {
        Copy-Item -LiteralPath $yol -Destination ($yol + ".bak11d") -Force
        Set-Content -LiteralPath $yol -Value $icerik -Encoding UTF8 -NoNewline
        Write-Host ("{0} : {1} eslesme maskelendi (yedek .bak11d)" -f $ad, $sayac)
    }
    else {
        Write-Host ("{0} : {1} eslesme maskelenecek (kuru calisma)" -f $ad, $sayac)
    }
    $toplam += $sayac
}

Write-Host ("TOPLAM: {0} eslesme, {1} dosya" -f $toplam, @($gruplar).Count)
