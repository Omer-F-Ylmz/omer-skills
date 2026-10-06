# DERINLIK-KAPANIS-4 kabul partisi (Omer calistirir; ASCII-only).
# powershell -ExecutionPolicy Bypass -File C:\Projeler\omer-skills\docs\video-tarama\kabul-partisi.ps1
# Parti iki adimda: baslat --cagri-tavan 0 (paket kurulur, model cagrisi 0, rc 3) -> yontem kontrolu -> devam --yeniden-tara --cagri-ek 12.
# $ tavani = tahmin x 1.6 yukari yuvarlanir: short $0.0083 -> $0.02 | uzun $0.0148 + $0.0424 -> $0.10.
$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$env:PYTHONUTF8 = '1'
$kos = 'C:\Projeler\omer-skills\.kos'
$tdir = 'C:\Projeler\omer-skills\docs\video-tarama'
$kabul = 'C:\Projeler\.video-cache\kabul'
$partiler = @()

function Rapor {
    foreach ($p in $partiler) {
        $d = Get-Content -Raw -Encoding UTF8 "$kos\$p\durum.json" | ConvertFrom-Json
        Write-Host "== $p ($($d.durum))"
        foreach ($v in $d.videolar.PSObject.Properties) { Write-Host "  $($v.Name) tarama: $($v.Value.tarama.durum) $($v.Value.tarama.hata)" }
        if (Test-Path "$kos\$p\defter.jsonl") {
            Get-Content -Encoding UTF8 "$kos\$p\defter.jsonl" | Where-Object { $_ } | ForEach-Object { $_ | ConvertFrom-Json } |
                Where-Object { $_.adim -eq 'tarama' } | ForEach-Object {
                    Write-Host "  $($_.videolar -join ',') | $($_.model) | cagri $($_.cagri) | usd $($_.usd) | sure $($_.sure) | geri_donus $($_.geri_donus)" }
        }
    }
}
function Dur($m) { Write-Host "DUR: $m"; Rapor; exit 1 }

$video = (Get-Command video -ErrorAction SilentlyContinue).Source
if (-not $video) { $video = "$(uv tool dir)\video-cli\Scripts\video.exe" }
if (-not (Test-Path $video)) { Dur "video CLI yok" }

# 1 OmniRoute saglik
$omni = if ($env:OMNIROUTE_URL) { $env:OMNIROUTE_URL } else { 'http://localhost:20128' }
try { $kod = (Invoke-WebRequest -UseBasicParsing -TimeoutSec 15 -Uri "$omni/api/v1/models" -Headers @{ Authorization = "Bearer $env:OMNIROUTE_KEY" }).StatusCode }
catch { $kod = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 0 } }
if ($kod -ne 200) { Dur "OmniRoute'u baslat (ilk acilis > 60 s) - HTTP $kod" }

# 2 OMNIROUTE_KEY (yalniz var/yok)
$anahtar = [bool]$env:OMNIROUTE_KEY
Write-Host "OMNIROUTE_KEY var: $anahtar"
if (-not $anahtar) { Dur "OMNIROUTE_KEY yok (yonlendirme yazilmaz, parti eski yolda kosar)" }

New-Item -ItemType Directory -Force "$kabul\yedek" | Out-Null
Set-Content -Encoding ASCII "$kabul\kuyruk-short.md" '| Ov-B6K1EsaI | 0.95 | kabul short | DERINLIK-KAPANIS-4 | bekliyor |'
Set-Content -Encoding ASCII "$kabul\kuyruk-uzun.md" @('| vhY7OGIh1v0 | 14.2 | kabul uzun | DERINLIK-KAPANIS-4 | bekliyor |',
                                                     '| b2QkhmQ0sT0 | 20.5 | kabul uzun (b2Q) | DERINLIK-KAPANIS-4 | bekliyor |')

function Parti($tur, $kuyruk, $usd, $idler, $yedek) {
    & $video parti baslat $kuyruk "--$tur" --cagri-tavan 0 --usd-tavan $usd --ikinci-goz yok | Tee-Object -Variable out
    $m = [regex]::Match(($out -join "`n"), '(?m)^parti: (\S+) ')
    if (-not $m.Success) { Dur "$tur parti acilmadi (rc $LASTEXITCODE)" }
    $p = $m.Groups[1].Value
    $script:partiler += $p
    $d = Get-Content -Raw -Encoding UTF8 "$kos\$p\durum.json" | ConvertFrom-Json
    foreach ($i in $idler) { if (-not $d.videolar.$i) { Dur "$p : $i partide yok (acik partide mi?)" } }
    if ($d.yonlendirme.tarama.yontem -ne 'V10') { Dur "$p yonlendirme.tarama.yontem '$($d.yonlendirme.tarama.yontem)' (V10 degil)" }
    # yeniden-tara {tarih}-{id}.md raporunu ezer (parti.py:335-338): varsa once yedek
    foreach ($i in $yedek) { Get-ChildItem "$tdir\*-$i.md" -ErrorAction SilentlyContinue | Copy-Item -Destination "$kabul\yedek\" -PassThru | ForEach-Object { Write-Host "yedek: $($_.FullName)" } }
    & $video parti devam $p --yeniden-tara --cagri-ek 12 --ikinci-goz yok
    if ($LASTEXITCODE -ne 0) { Dur "$p devam rc $LASTEXITCODE (tavan/form_red asagida)" }
}

# 3 short parti
Parti 'short' "$kabul\kuyruk-short.md" '0.02' @('Ov-B6K1EsaI') @()
# 4 uzun parti
Parti 'uzun' "$kabul\kuyruk-uzun.md" '0.10' @('vhY7OGIh1v0', 'b2QkhmQ0sT0') @('b2QkhmQ0sT0')
# 5 rapor
Rapor
