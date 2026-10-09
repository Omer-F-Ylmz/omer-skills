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
    [string]$Kuyruk = '',   # bos: parti.py varsayilan kuyrugu (docs/video-tarama/kuyruk.md)
    [string]$RamOku = '',   # bos: bos RAM (MB) Win32_OperatingSystem'den; dolu: son cikti satiri MB donen komut (test)
    [int]$Bekle = 60,
    [int]$CokmeBekle = 30,   # GECE-4b: cokme (negatif cikis, 0xC0000005 vb.) sonrasi ayni partiye devam oncesi bekleme
    [switch]$Baslat
)
$ErrorActionPreference = 'Continue'
$repo = Split-Path (Split-Path $PSScriptRoot)
if ($Baslat) {
    $a = '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Paralel', $Paralel, '-EnFazla', $EnFazla, '-Tavan', $Tavan, '-Bekle', $Bekle, '-CokmeBekle', $CokmeBekle
    foreach ($p in 'Video', 'Kok', 'Kuyruk', 'RamOku') { if (Get-Variable $p -ValueOnly) { $a += "-$p", (Get-Variable $p -ValueOnly) } }
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
$adEk = if ($Kuyruk) { '-' + [IO.Path]::GetFileNameWithoutExtension($Kuyruk) } else { '' }   # KILIT-1: iki kosucu ayni gun ayri log/ozet
$logYol = Join-Path $kos "gece-$gun$adEk.log"
$ardisikLimit = 0
$limitSifir = ''
$limitNeden = "kullan$([char]0x131)m limiti"   # betik ASCII; PS 5.1 BOM'suz UTF-8'i ANSI okur
$sw = [Diagnostics.Stopwatch]::StartNew()
$partiler = @()
$asama = @{}       # asama adi -> @(sn, adet)
$ardisik403 = 0
$ardisikHata = 0
$neden = 'bitti'
$ic = [Globalization.CultureInfo]::InvariantCulture

function Log($m) { Add-Content -Path $logYol -Encoding UTF8 -Value ("{0} {1}" -f (Get-Date -Format 's'), $m) }

function Ram {
    if ($RamOku) { [double](@(& $RamOku)[-1]) }
    else { (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1024 }
}

function Cagir([string[]]$a) {   # cocuk cikti (stdout+stderr) loga; satirlari dondurur, kod $script:kod
    Log "> video $($a -join ' ')"
    $s = @(& $Video @a 2>&1 | ForEach-Object { "$_" })
    $script:kod = $LASTEXITCODE
    $lim = @($s | Where-Object { $_ -match 'usage limit|rate.?limit|\b429\b' })   # KILIT-1: claude -p kullanim limiti, art arda 3 cagri -> DUR
    if ($lim) { $script:ardisikLimit++ } else { $script:ardisikLimit = 0 }
    foreach ($l in $lim) { if ($l -match '(?i)\breset\w*\b.*') { $script:limitSifir = $Matches[0] } }
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

function Harcanan($p) {   # parti.py _defter: ikinci_goz/tavan/omniroute_baslat/paket_yenilendi satirlari cagri degil; @(cagri, usd)
    $n = 0; $u = 0.0
    foreach ($r in Defter $p) {
        if ("$($r.adim)" -match '^(ikinci_goz|tavan|omniroute_baslat|paket_yenilendi)') { continue }
        $n += if ($null -ne $r.cagri) { [int]$r.cagri } else { 1 }
        if ($null -ne $r.usd) { $u += [double]$r.usd }
    }
    @($n, $u)
}

function YeniParti($once) {   # GECE-4b: cokunce "parti:" satiri stdout tamponunda kaybolur; bu kosucunun kuyruguna ait yeni parti klasoru
    $k = [IO.Path]::GetFileName($(if ($Kuyruk) { $Kuyruk } else { 'kuyruk.md' }))
    Get-ChildItem $kos -Directory | Where-Object { $_.Name -notin $once -and [IO.Path]::GetFileName("$((Durum $_.Name).kuyruk)") -eq $k } |
        Sort-Object CreationTime | Select-Object -Last 1 -ExpandProperty Name
}

function Kullanilan { $n = 0; foreach ($p in $partiler) { $n += (Harcanan $p)[0] }; $n }

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

    $u = ($EnFazla * 0.15).ToString($ic)   # olculen ~0.11 $/video; cli varsayilani 1.0 gecede 13 videoda durdurdu
    $a = @('parti', 'baslat') + @($Kuyruk | Where-Object { $_ }) + @('--en-fazla', $EnFazla, '--paralel', $Paralel, '--cagri-tavan', $tavanParti, '--usd-tavan', $u)
    if ($EnFazla * 0.15 -gt 2.0) { $a += '--usd-tavan-max', $u }   # cli usd_max varsayilani 2.0 bu tavanin altinda kalmasin
    $once = @(Get-ChildItem $kos -Directory | ForEach-Object Name)
    $cikti = Cagir $a
    if ($ardisikLimit -ge 3) { $neden = $limitNeden; break }
    # parti sonucu durum.json'dan: tavanda baslat 3 doner ama parti kurulmustur
    $m = $cikti | Where-Object { $_ -match '^parti: \S+ . \w+ . \d+ video' } | Select-Object -First 1
    $cokme = 0
    if ($m) { $pid_ = ($m -split ' ')[1] }
    elseif ($kod -lt 0 -and ($pid_ = YeniParti $once)) {   # cokme: negatif cikis (0xC0000005, 0xC0000409 ...)
        $cokme = 1
        Log "COKME: baslat (cikis $kod), $CokmeBekle sn sonra parti devam $pid_"
        Start-Sleep -Seconds $CokmeBekle
    }
    else {
        $neden = if ($kod -in 1, 3) { 'kuyruk bos' } else { "baslat hata (cikis $kod)" }   # 1: bekleyen yok - 3: hepsi baska acik partide
        break
    }
    $partiler += $pid_
    if ($ardisik403 -ge 3) { $neden = '403'; break }

    $devam = 0
    while (($d = Durum $pid_).durum -notin 'tamam', 'iptal', 'hata', 'kapandi') {
        if (++$devam -gt 5) { $neden = "parti $pid_ ilerlemiyor"; break }
        $a = 'parti', 'devam', $pid_
        if ($d.durum -eq 'tavan') {   # ayni partide devam: kalan video basina 2 cagri, gecelik tavan icinde
            $kalan = @($d.videolar.PSObject.Properties | Where-Object { $_.Value.tarama.durum -in 'bekliyor', 'hata', 'tavan', 'yeniden' }).Count
            $ek = [math]::Min(2 * $kalan, $Tavan - (Kullanilan))
            if ($ek -le 0) { $neden = 'tavan'; break }
            $h = Harcanan $pid_
            $ort = if ($h[0] -gt 0) { $h[1] / $h[0] * 1.5 } else { 0.15 }   # defter ortalamasi; sabit 0.075 uzun videoda (~0.16) yetmedi
            $a += '--cagri-ek', [math]::Max(0, $h[0] + $ek - [int]$d.tavan.cagri),
                '--usd-ek', ([math]::Max(0.0, $h[1] + $ek * $ort - [double]$d.tavan.usd)).ToString('0.0000', $ic)
        }
        Cagir $a | Out-Null
        if ($kod -lt 0) {   # ayni partiye en fazla 3 cokme donusu
            if (++$cokme -gt 3) { $neden = "cokme (cikis $kod, parti $pid_ 3 donuste de coktu)"; break }
            Log "COKME: devam (cikis $kod), $CokmeBekle sn sonra parti devam $pid_"
            Start-Sleep -Seconds $CokmeBekle
        }
        if ($ardisik403 -ge 3) { $neden = '403'; break }
        if ($ardisikLimit -ge 3) { $neden = $limitNeden; break }
    }
    if ($neden -ne 'bitti') { break }

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
$sayi = @{ islenen = 0; tamam = 0; tamam_eksik = 0; tavan = 0; hata = 0 }
$tok = 0; $usd = 0.0; $usdVar = $false
foreach ($p in $partiler) {
    foreach ($v in (Durum $p).videolar.PSObject.Properties) {
        $sayi.islenen++
        switch ($v.Value.tarama.durum) { 'tamam' { $sayi.tamam++ } 'tamam_eksik' { $sayi.tamam_eksik++ } 'tavan' { $sayi.tavan++ } 'bekliyor' { } default { $sayi.hata++ } }
    }
    foreach ($r in Defter $p) {
        $tok += [long]$r.girdi + [long]$r.onb_okuma + [long]$r.onb_yazma + [long]$r.cikti
        if ($null -ne $r.usd) { $usd += [double]$r.usd; $usdVar = $true }
    }
}
$sn =[math]::Round($sw.Elapsed.TotalSeconds)
$ort = if ($sayi.islenen) { [math]::Round($sn / $sayi.islenen, 1).ToString($ic) } else { '-' }
$o = @("# Gece ozeti $gun", '', "- durma nedeni: $neden", "- partiler: $($partiler -join ', ')",
    "- islenen: $($sayi.islenen)", "- tamam: $($sayi.tamam)", "- tamam_eksik: $($sayi.tamam_eksik)", "- tavan: $($sayi.tavan)", "- hata: $($sayi.hata)",
    "- token: $tok", "- claude -p cagri: $(Kullanilan)",
    $(if ($usdVar) { "- usd esdegeri: $($usd.ToString('0.0000', $ic))" } else { '- usd esdegeri: defterde yok' }),
    "- toplam sure: $sn sn", "- video basina ortalama: $ort sn")
if ($neden -eq $limitNeden) { $o += "- sifirlanma: $(if ($limitSifir) { $limitSifir } else { 'ciktida yok' })" }
$o += '', '## Asama sureleri'
foreach ($k in $asama.Keys | Sort-Object) {
    $t = $asama[$k][0]; $c = $asama[$k][1]
    $o += "- ${k}: toplam $($t.ToString('0.#', $ic)) sn, ortalama $(([math]::Round($t / $c, 1)).ToString($ic)) sn ($c adet)"
}
Set-Content -Path (Join-Path $kos "ozet-$gun$adEk.md") -Encoding UTF8 -Value $o
exit 0
