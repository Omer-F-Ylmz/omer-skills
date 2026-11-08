# KUR-TUR2: Omer'in TEK komutu.   .\tools\kurulum_tur2.ps1 -Deneme   (kurulumsuz: kalem basina kok neden + eylem plani, yoklamalar salt-okur)
#                                  .\tools\kurulum_tur2.ps1           (gercek ikinci tur)
# PowerShell 5.1. Sirasi: siniflandir -> birim testleri -> plan -> (gercek kosuda) uygula.
# Bir adim hata verse de digerleri surer; her adim rapor\kur-tur2-adim.tsv'ye yazilir. Anahtar/ortam degeri yazdirilmaz. Silme yok.
# Eylemler: D2 (kurulum_d2 --tur2, sirali), PLUGIN (claude plugin), KOMUT (.claude/commands), APT (WSL Ubuntu), WINGET, DOGRULA, PIPEK, COZUMSUZ.
param([switch]$Deneme, [int]$DiskAltGB = 40)
$ErrorActionPreference = 'Continue'
$kok = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $kok
$env:PYTHONUTF8 = '1'
$adim = Join-Path $kok 'rapor\kur-tur2-adim.tsv'
if (-not (Test-Path $adim)) { "adim`tdurum`tsure_sn`tnot" | Set-Content $adim -Encoding utf8 }
$py = (Get-Command python.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$script:hata = 0

function Adim($ad, [scriptblock]$is) {
    $t0 = Get-Date
    $global:LASTEXITCODE = 0
    try { & $is 2>&1 | ForEach-Object { Write-Host "  $_" } } catch { Write-Host "  istisna: $($_.Exception.Message)"; $global:LASTEXITCODE = 99 }
    $kod = $global:LASTEXITCODE
    $d = if ($kod -eq 0) { 'TAMAM' } else { $script:hata++; 'HATA' }
    $sn = [int]((Get-Date) - $t0).TotalSeconds
    "$ad`t$d`t$sn`tkod=$kod" | Add-Content $adim -Encoding utf8
    Write-Host ("{0,-14} {1,-6} {2,5}s kod={3}" -f $ad, $d, $sn, $kod)
}

if (-not $py) { Write-Host 'HATA: python.exe yok'; exit 1 }
$bos = [math]::Round((Get-PSDrive C).Free / 1GB, 1)
if ($bos -lt $DiskAltGB) { Write-Host "DUR: C: bos $bos GB < $DiskAltGB GB"; exit 2 }

Adim 'siniflandir' { & $py -X utf8 tools\kurulum_tur2_siniflandir.py }
Adim 'birim-test' { & $py -m pytest tests\test_kurulum_tur2.py tests\test_kurulum_d2_bitenler.py -q }
Adim 'plan' { & $py -X utf8 tools\kurulum_tur2.py --plan }

# plan kapsami: HATA + KURULUM-YOLU-YOK + KURULDU-DOGRULANMADI kalemlerinin hepsi planda eylem almali
$sinif = @(Import-Csv tmp\tur2-siniflar.tsv -Delimiter "`t")
$plan = @(Import-Csv rapor\kur-tur2-plan.tsv -Delimiter "`t")
if ($plan.Count -ne $sinif.Count) { $script:hata++; Write-Host "HATA: plan $($plan.Count) satir, siniflandirma $($sinif.Count)" }
$plan | Group-Object eylem | Sort-Object Count -Descending | ForEach-Object { Write-Host ("  eylem {0,-9} {1}" -f $_.Name, $_.Count) }

if ($Deneme) {
    Write-Host "DENEME bitti: HATA $script:hata (kurulum yapilmadi). Plan: rapor\kur-tur2-plan.tsv"
    exit $script:hata
}
Adim 'uygula' { & $py -X utf8 tools\kurulum_tur2.py --uygula }
Write-Host "TUR2 bitti: HATA $script:hata. Sonuc: rapor\kur-tur2-sonuc.tsv"
exit $script:hata
