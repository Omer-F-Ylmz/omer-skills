# VIDEO-PARTI-YT1 4: gece kosturucu. Partileri sirayla baslatir/surdurur; asla `parti kapat`, commit ya da push yapmaz.
# Ayrik baslatma (-Baslat ayni seyi yapar ve PID basar):
#   Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','<yol>\parti-gece.ps1'
# Cikti: <Kok>\.kos\gece-<gun>.log (ekleme) ve <Kok>\.kos\ozet-<gun>.md.
# Butce sayaci: kosturucunun kendi partilerinin defter.jsonl satirlari, parti.py _defter ile ayni kural
#   (satir "cagri" alani, yoksa 1; adim ikinci_goz*/tavan*/omniroute_baslat*/paket_yenilendi* sayilmaz).
#   Durum dosyasinda cagri sayaci yok (durum.json yalniz tavani tutar), defter gercek claude -p sayisidir.
# Acik (kapandi olmayan) parti sonraki baslat'ta videolarini atlatir: istenen, kosturucu kapatmaz.
param(
    [int]$Paralel = 4,
    [int]$EnFazla = 25,
    [int]$Tavan = 200,
    [string]$Video = '',
    [string]$Kok = '',
    [string]$RamOku = '',   # bos: bos RAM (MB) Win32_OperatingSystem'den; dolu: son cikti satiri MB donen komut (test)
    [int]$Bekle = 60,
    [switch]$Baslat
)
$ErrorActionPreference = 'Continue'
$repo = Split-Path (Split-Path $PSScriptRoot)
if ($Baslat) {
    $a = '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Paralel', $Paralel, '-EnFazla', $EnFazla, '-Tavan', $Tavan, '-Bekle', $Bekle
    foreach ($p in 'Video', 'Kok', 'RamOku') { if (Get-Variable $p -ValueOnly) { $a += "-$p", (Get-Variable $p -ValueOnly) } }
    $p = Start-Process powershell -WindowStyle Hidden -PassThru -ArgumentList $a
    "PID $($p.Id)"
    return
}
[Console]::OutputEncoding = [Text.Encoding]::UTF8
if (-not $Kok) { $Kok = if ($env:VIDEO_UYGULA_KOK) { $env:VIDEO_UYGULA_KOK } else { $repo } }
if (-not $Video) { $Video = Join-Path $repo 'tools\video\.venv\Scripts\video.exe' }
$env:VIDEO_UYGULA_KOK = $Kok   # parti.py ayni kokten okur
$kos = Join-Path $Kok '.kos'
New-Item -ItemType Directory -Force $kos | Out-Null
$gun = Get-Date -Format 'yyyy-MM-dd'
$logYol = Join-Path $kos "gece-$gun.log"
$sw = [Diagnostics.Stopwatch]::StartNew()
$partiler = @()
$asama = @{}       # asama adi -> @(sn, adet)
$ardisik403 = 0
$ardisikHata = 0
$neden = 'bitti'

function Log($m) { Add-Content -Path $logYol -Encoding UTF8 -Value ("{0} {1}" -f (Get-Date -Format 's'), $m) }

function Ram {
    if ($RamOku) { [double](@(& $RamOku)[-1]) }
    else { (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1024 }
}

function Cagir([string[]]$a) {   # cocuk cikti (stdout+stderr) loga; satirlari dondurur, kod $script:kod
    Log "> video $($a -join ' ')"
    $s = @(& $Video @a 2>&1 | ForEach-Object { "$_" })
    $script:kod = $LASTEXITCODE
    foreach ($l in $s) {
        Log "  $l"
        if ($l -match '\[a.ama\] (\S+) (\S+) bitti (\S+) ([\d.,]+)') {
            $k = $Matches[2]; $v = [double]($Matches[4] -replace ',', '.')
            if (-not $asama[$k]) { $asama[$k] = @(0.0, 0) }
            $asama[$k] = @(($asama[$k][0] + $v), ($asama[$k][1] + 1))
        }
        if ($l -match 'youtu\.be/') { if ($l -match 'indirme 403') { $script:ardisik403++ } else { $script:ardisik403 = 0 } }
    }
    $s
}

function Durum($pid_) {
    $y = Join-Path $kos "$pid_\durum.json"
    if (Test-Path $y) { Get-Content $y -Raw -Encoding UTF8 | ConvertFrom-Json }
}

function Defter($pid_) {
    $y = Join-Path $kos "$pid_\defter.jsonl"
    if (Test-Path $y) { Get-Content $y -Encoding UTF8 | Where-Object { $_.Trim() } | ForEach-Object { $_ | ConvertFrom-Json } }
}

function Kullanilan {   # parti.py _defter: ikinci_goz/tavan/omniroute_baslat/paket_yenilendi satirlari cagri degil
    $n = 0
    foreach ($p in $partiler) {
        foreach ($r in Defter $p) {
            if ("$($r.adim)" -match '^(ikinci_goz|tavan|omniroute_baslat|paket_yenilendi)') { continue }
            $n += if ($null -ne $r.cagri) { [int]$r.cagri } else { 1 }
        }
    }
    $n
}

Log "BASLA paralel=$Paralel enfazla=$EnFazla tavan=$Tavan kok=$Kok"
while ($true) {
    # RAM kapisi
    $dusuk = 0
    while (($ram = Ram) -lt 2048) {
        $dusuk++
        Log "RAM dusuk: $([int]$ram) MB ($dusuk/10)"
        if ($dusuk -ge 10) { break }
        Start-Sleep -Seconds $Bekle
    }
    if ($dusuk -ge 10) { $neden = 'RAM'; break }
    # butce kapisi: video basina <=2 claude -p
    $tavanParti = 2 * $EnFazla
    if ((Kullanilan) + $tavanParti -gt $Tavan) { $neden = 'tavan'; break }

    $cikti = Cagir 'parti', 'baslat', '--en-fazla', $EnFazla, '--paralel', $Paralel, '--cagri-tavan', $tavanParti
    if ($kod -in 1, 3) { $neden = 'kuyruk bos'; break }   # 1: bekleyen yok - 3: hepsi baska acik partide
    if ($kod -ne 0) { $neden = "baslat hata (cikis $kod)"; break }
    $m = $cikti | Where-Object { $_ -match '^parti: \S+ ' } | Select-Object -First 1
    if (-not $m) { $neden = 'parti kimligi okunamadi'; break }
    $pid_ = ($m -split ' ')[1]
    $partiler += $pid_
    if ($ardisik403 -ge 3) { $neden = '403'; break }

    $devam = 0
    while ((Durum $pid_).durum -notin 'tamam', 'tavan', 'iptal', 'hata', 'kapandi') {
        if (++$devam -gt 5) { $neden = "parti $pid_ ilerlemiyor"; break }
        Cagir 'parti', 'devam', $pid_ | Out-Null
        if ($ardisik403 -ge 3) { $neden = '403'; break }
    }
    if ($neden -ne 'bitti') { break }
    if ((Durum $pid_).durum -eq 'tavan') { $neden = 'parti tavani'; break }

    # tarama hatasi: videolar sirayla, ardisik 3 hata
    foreach ($v in (Durum $pid_).videolar.PSObject.Properties) {
        if ($v.Value.tarama.durum -eq 'hata') { $ardisikHata++ } else { $ardisikHata = 0 }
        if ($ardisikHata -ge 3) { break }
    }
    if ($ardisikHata -ge 3) { $neden = 'tarama hatasi (3 ardisik)'; break }
}
if ($neden -eq '403' -or $partiler.Count -gt 0 -and $ardisik403 -ge 3) { $neden = '403' }
Log "DUR: $neden"

# ozet
$sayi = @{ islenen = 0; tamam = 0; tamam_eksik = 0; hata = 0 }
$tok = 0; $usd = 0.0; $usdVar = $false
foreach ($p in $partiler) {
    foreach ($v in (Durum $p).videolar.PSObject.Properties) {
        $sayi.islenen++
        switch ($v.Value.tarama.durum) { 'tamam' { $sayi.tamam++ } 'tamam_eksik' { $sayi.tamam_eksik++ } 'bekliyor' { } default { $sayi.hata++ } }
    }
    foreach ($r in Defter $p) {
        $tok += [long]$r.girdi + [long]$r.onb_okuma + [long]$r.onb_yazma + [long]$r.cikti
        if ($null -ne $r.usd) { $usd += [double]$r.usd; $usdVar = $true }
    }
}
$ic = [Globalization.CultureInfo]::InvariantCulture
$sn = [math]::Round($sw.Elapsed.TotalSeconds)
$ort = if ($sayi.islenen) { [math]::Round($sn / $sayi.islenen, 1).ToString($ic) } else { '-' }
$o = @("# Gece ozeti $gun", '', "- durma nedeni: $neden", "- partiler: $($partiler -join ', ')",
    "- islenen: $($sayi.islenen)", "- tamam: $($sayi.tamam)", "- tamam_eksik: $($sayi.tamam_eksik)", "- hata: $($sayi.hata)",
    "- token: $tok", "- claude -p cagri: $(Kullanilan)",
    $(if ($usdVar) { "- usd esdegeri: $($usd.ToString('0.0000', $ic))" } else { '- usd esdegeri: defterde yok' }),
    "- toplam sure: $sn sn", "- video basina ortalama: $ort sn", '', '## Asama sureleri')
foreach ($k in $asama.Keys | Sort-Object) {
    $t = $asama[$k][0]; $c = $asama[$k][1]
    $o += "- ${k}: toplam $($t.ToString('0.#', $ic)) sn, ortalama $(([math]::Round($t / $c, 1)).ToString($ic)) sn ($c adet)"
}
Set-Content -Path (Join-Path $kos "ozet-$gun.md") -Encoding UTF8 -Value $o
exit 0
