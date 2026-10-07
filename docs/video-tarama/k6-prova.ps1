# K6 prova: tek takip kanalinin kuyrugundan siradaki -Adet video -> partiler (short <=8, uzun <=3, ardisik) -> tek ozet.
# Tavan: toplam 40 cagri / $0.40 (kalan butce parti tavani olur; bitince sonraki parti baslamaz). Commit yapmaz.
param([switch]$OmniKapat, [switch]$Listele, [int]$Adet = 5, [string]$Kanal)
$ErrorActionPreference = "Stop"
$kok = (Resolve-Path "$PSScriptRoot\..\..").Path
$video = "$(uv tool dir)\video-cli\Scripts\video.exe"
$utf8 = New-Object Text.UTF8Encoding($false)
$OutputEncoding = $utf8; [Console]::OutputEncoding = $utf8
$CAGRI_MAX = 40; $USD_MAX = 0.40
function Oku($y) { [IO.File]::ReadAllText($y, $utf8) | ConvertFrom-Json }

# 1) kanal + video secimi
$kanallar = Oku "$kok\docs\video-tarama\kanallar.json"
$islenen = @{}
foreach ($s in [IO.File]::ReadAllLines("$kok\docs\video-tarama\kayit.jsonl", $utf8)) { if ($s.Trim()) { $islenen[($s | ConvertFrom-Json).id] = 1 } }
$secim = $null
foreach ($a in $kanallar.PSObject.Properties.Value) {
    if ($a.karar -ne "takip") { continue }
    if ($Kanal -and $Kanal -ne $a.channel_id -and $Kanal -ne $a.kanal) { continue }
    $y = "$kok\.kos\kanal\$($a.channel_id).json"
    if (-not (Test-Path $y)) { continue }
    $bek = @((Oku $y).videolar.PSObject.Properties | Where-Object { -not $islenen.ContainsKey($_.Name) } | Select-Object -First $Adet)
    if ($bek.Count -gt 0) { $secim = @{ kanal = $a; v = $bek }; break }
}
if (-not $secim) { Write-Host "k6: kuyrugu dolu takip kanali yok"; exit 1 }
$videolar = foreach ($p in $secim.v) {
    $sure = $p.Value.sure
    $dk = if ($sure) { [math]::Round($sure / 60, 1) } elseif ($p.Value.tur -eq "short") { 1 } else { 10 }
    [pscustomobject]@{ id = $p.Name; baslik = [string]$p.Value.baslik; dk = $dk; tur = $(if ($dk -lt 2) { "short" } else { "uzun" }) }
}
# repo siniflandirmasi (tarama.kuyruk_parti): dk < 2 short; parti short <=8, uzun <=3
$partiler = @()
foreach ($t in @(@("short", 8), @("uzun", 3))) {
    $l = @($videolar | Where-Object { $_.tur -eq $t[0] })
    for ($i = 0; $i -lt $l.Count; $i += $t[1]) { $partiler += , @{ tur = $t[0]; v = @($l[$i..([math]::Min($i + $t[1], $l.Count) - 1)]) } }
}
Write-Host "kanal: $($secim.kanal.kanal) ($($secim.kanal.channel_id))"
foreach ($v in $videolar) { Write-Host ("  {0} | {1} | {2} dk | {3}" -f $v.id, $v.baslik, $v.dk, $v.tur) }
$n = 0; foreach ($p in $partiler) { $n++; Write-Host ("parti {0}: {1} - {2}" -f $n, $p.tur, (($p.v | ForEach-Object { $_.id }) -join ", ")) }
if ($Listele) { exit 0 }

# 2) OmniRoute yalniz 20128'i dinleyen omniroute.mjs sureci
if ($OmniKapat) {
    $c = Get-NetTCPConnection -LocalPort 20128 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c) {
        $pr = Get-CimInstance Win32_Process -Filter "ProcessId=$($c.OwningProcess)"
        if ($pr.CommandLine -match 'omniroute\.mjs') { Stop-Process -Id $c.OwningProcess -Force; Write-Host "omniroute durduruldu (pid $($c.OwningProcess))" }
    }
}

# 3) partiler ardisik; kalan tavan her parti tavani
$kayitDosya = "$kok\docs\video-tarama\kayit.jsonl"
$kullanCagri = 0; $kullanUsd = 0.0; $sonuc = @{}; $oluOlay = @(); $rc = 0; $pidler = @()
$n = 0
foreach ($p in $partiler) {
    $n++
    $kc = $CAGRI_MAX - $kullanCagri; $ku = [math]::Round($USD_MAX - $kullanUsd, 4)
    if ($kc -le 0 -or $ku -le 0) { Write-Host "tavan doldu: parti $n baslamadi"; $oluOlay += "tavan: parti $n baslamadi"; $rc = 1; continue }
    $ky = "$kok\.kos\k6-$(Get-Date -Format yyyy-MM-dd)-$n.md"
    $satir = $p.v | ForEach-Object { "| $($_.id) | $($_.dk.ToString([Globalization.CultureInfo]::InvariantCulture)) | $((($_.baslik -replace '\|', '/'))[0..([math]::Min(39, $_.baslik.Length - 1))] -join '') | /video-uygula | bekliyor |" }
    [IO.File]::WriteAllText($ky, ("| id | dk | baslik | not | durum |`n|---|---|---|---|---|`n" + ($satir -join "`n") + "`n"), $utf8)
    $a = @("parti", "baslat", $ky, "--$($p.tur)", "--en-fazla", "$($p.v.Count)", "--kayit", $kayitDosya,
           "--cagri-tavan", "$kc", "--cagri-tavan-max", "$kc", "--usd-tavan", "$ku", "--usd-tavan-max", "$ku")
    $out = & $video @a
    $out | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE) { $rc = 1 }
    $m = [regex]::Match(($out -join "`n"), '(?m)^parti: (\S+)\s')
    if (-not $m.Success) { $oluOlay += "parti $n baslamadi (rc $LASTEXITCODE)"; $rc = 1; continue }
    $pid_ = $m.Groups[1].Value; $pidler += $pid_
    $pd = "$kok\.kos\$pid_"
    $d = Oku "$pd\durum.json"
    $df = @(); if (Test-Path "$pd\defter.jsonl") { $df = @([IO.File]::ReadAllLines("$pd\defter.jsonl", $utf8) | Where-Object { $_.Trim() } | ForEach-Object { $_ | ConvertFrom-Json }) }
    foreach ($r in $df) {
        $adim = [string]$r.adim
        if ($adim -match '^(omniroute_baslat|paket_yenilendi|tavan)') { $oluOlay += "${pid_}: $adim" }
        if ($adim -notmatch '^(ikinci_goz|tavan|omniroute_baslat|paket_yenilendi)') {
            $kullanCagri += $(if ($null -ne $r.cagri) { $r.cagri } else { 1 }); $kullanUsd += [double]$r.usd
        }
        foreach ($k in "geri_donus", "gecici", "bos_yanit") { if ($r.PSObject.Properties[$k] -and $r.$k) { $oluOlay += "${pid_}: $k $($r.$k)" } }
    }
    foreach ($v in $p.v) {
        $o = @{ durum = $d.videolar.($v.id).tarama.durum; model = ""; cagri = 0.0; usd = 0.0; sure = 0.0; g = 0.0; ok = 0.0; oy = 0.0 }
        foreach ($r in ($df | Where-Object { $_.videolar -contains $v.id })) {
            $b = @($r.videolar).Count   # paylasilan satir video sayisina bolunur
            $o.model = $r.model; $o.cagri += ($(if ($null -ne $r.cagri) { $r.cagri } else { 1 })) / $b; $o.usd += [double]$r.usd / $b; $o.sure += [double]$r.sure / $b
            $o.g += [double]$r.girdi / $b; $o.ok += [double]$r.onb_okuma / $b; $o.oy += [double]$r.onb_yazma / $b
        }
        if ($o.durum -notin "tamam", "tamam_eksik") { $rc = 1 }
        $sonuc[$v.id] = $o
    }
}

# 4) tek ozet
$ozet = @("# K6 prova ozeti $(Get-Date -Format yyyy-MM-dd)", "", "kanal: $($secim.kanal.kanal) ($($secim.kanal.channel_id)) - partiler: $($pidler -join ', ')",
          "toplam: $([math]::Round($kullanCagri, 1)) cagri / `$$([math]::Round($kullanUsd, 4)) (tavan $CAGRI_MAX / `$$USD_MAX)", "")
foreach ($v in $videolar) {
    $o = $sonuc[$v.id]; if (-not $o) { $ozet += "$($v.id) | baslamadi"; continue }
    $top = $o.g + $o.ok + $o.oy; $pay = if ($top -gt 0) { [math]::Round(100 * $o.ok / $top, 1) } else { 0 }
    $ozet += ("{0} | {1} | {2} | cagri {3} | `${4} | {5} sn | onbellekli girdi %{6}" -f $v.id, $o.durum, $o.model, [math]::Round($o.cagri, 1), [math]::Round($o.usd, 4), [math]::Round($o.sure, 1), $pay)
}
$ozet += ""; $ozet += "olagandisi olaylar: " + $(if ($oluOlay) { "" } else { "yok" })
$ozet += $oluOlay | ForEach-Object { "- $_" }
$ozet | ForEach-Object { Write-Host $_ }
[IO.File]::WriteAllText("$kok\docs\video-tarama\k6-ozet-$(Get-Date -Format yyyy-MM-dd).md", (($ozet -join "`n") + "`n"), $utf8)
exit $rc
