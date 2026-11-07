# KUR-HEPSI-1: Omer'in TEK komutu.  .\tools\kur_hepsi.ps1 -Deneme   (kurulumsuz, ne yapacagini yazar)
#                                    .\tools\kur_hepsi.ps1           (gercek kurulum)
# PowerShell 5.1. Yonetici gerekmeyen kisim once; winget/sistem (-Sistem) adimi en sonda.
# Bir adim hata verse de digerleri surer. Her adim rapor\kur-hepsi-sonuc.tsv'ye yazilir. Anahtar/ortam degeri yazdirilmaz. Silme yok.
param([switch]$Deneme, [int]$DiskAltGB = 60, [int]$SikistirBeklemeDk = 30)
$ErrorActionPreference = 'Continue'
$kok = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $kok
$sonuc = Join-Path $kok 'rapor\kur-hepsi-sonuc.tsv'
if (-not (Test-Path $sonuc)) { "adim`tdurum`tsure_sn`tbosGB`tnot" | Set-Content $sonuc -Encoding utf8 }
$py = (Get-Command python.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$ps = (Get-Command powershell.exe -CommandType Application | Select-Object -First 1).Source
$script:dur = $false

function BosGB { [math]::Round((Get-PSDrive C).Free / 1GB, 1) }
function Kayit($adim, $durum, $sn, $not) {
    $b = BosGB
    "$adim`t$durum`t$sn`t$b`t$not" | Add-Content $sonuc -Encoding utf8
    Write-Host ("{0,-6} {1,-9} {2,5}s bos={3}GB  {4}" -f $adim, $durum, $sn, $b, $not)
}

# Adim 8: her adim arasinda bos alan kontrolu. < DiskAltGB ise sikistirmayi bekle, yine dusukse dur.
function DiskKapi($once) {
    if ($script:dur) { return }
    if ((BosGB) -ge $DiskAltGB) { return }
    if ($Deneme) { Kayit "disk" "DENEME" 0 "bos < $DiskAltGB GB olsaydi sikistirma beklenirdi ($once oncesi)"; return }
    Kayit "disk" "BEKLE" 0 "bos < $DiskAltGB GB, sikistirma bekleniyor ($once oncesi)"
    $bitis = (Get-Date).AddMinutes($SikistirBeklemeDk)
    while ((BosGB) -lt $DiskAltGB -and (Get-Date) -lt $bitis) { Start-Sleep -Seconds 60 }
    if ((BosGB) -lt $DiskAltGB) { $script:dur = $true; Kayit "disk" "DUR" 0 "$SikistirBeklemeDk dk sonra bos hala < $DiskAltGB GB; kalan adimlar atlandi" }
}

function Adim($ad, $aciklama, [scriptblock]$is, [scriptblock]$deneme) {
    DiskKapi $ad
    if ($script:dur) { Kayit $ad "ATLANDI" 0 "disk dolu (DUR)"; return }
    $t0 = Get-Date
    try {
        $global:LASTEXITCODE = 0
        if ($Deneme) {
            if ($deneme) { & $deneme } else { Write-Host "  [deneme] $aciklama" }
            $durum = if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) { "DENEME" } else { "HATA" }
            Kayit $ad $durum ([int]((Get-Date) - $t0).TotalSeconds) $aciklama
        } else {
            & $is
            $durum = if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) { "TAMAM" } else { "HATA" }
            Kayit $ad $durum ([int]((Get-Date) - $t0).TotalSeconds) ("$aciklama (exit $LASTEXITCODE)")
        }
    } catch { Kayit $ad "HATA" ([int]((Get-Date) - $t0).TotalSeconds) ("$aciklama : " + $_.Exception.Message) }
}

function Dosya($yol) { Join-Path $kok $yol }

# [0] Sikistirma: mevcut gunluk gorev (kodu .kos\kopru\sikistir_tum.py: compact /exe:lzx, tek ornek korumali) arka planda baslat, oncelik dusur
Adim "0" "schtasks /run omer-sikistir-gunluk (arka plan, BelowNormal)" {
    schtasks.exe /run /tn omer-sikistir-gunluk | Out-Null
    Start-Sleep -Seconds 8
    Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'sikistir_tum\.py' -or $_.Name -eq 'compact.exe' } | ForEach-Object {
        try { (Get-Process -Id $_.ProcessId -ErrorAction Stop).PriorityClass = 'BelowNormal' } catch {} }
    $global:LASTEXITCODE = 0
} { Write-Host "  [deneme] gorev: $((schtasks.exe /query /tn omer-sikistir-gunluk /fo list | Select-String 'Status|Next Run') -join ' | ')"; $global:LASTEXITCODE = 0 }

# [1] kurulum_omer2.ps1 (sistem/winget haric: yonetici gerekmez)
Adim "1" "tools\kurulum_omer2.ps1" { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_omer2.ps1') } { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_omer2.ps1') -Deneme | Select-Object -Last 3 }

# [2] gurultu kurulumu (GURULTU-KUR-1 uretir; yoksa atla)
if (Test-Path (Dosya 'tools\kurulum_gurultu.ps1')) {
    Adim "2" "tools\kurulum_gurultu.ps1" { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_gurultu.ps1') } { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_gurultu.ps1') -Deneme | Select-Object -Last 3 }
} else { Kayit "2" "ATLANDI" 0 "tools\kurulum_gurultu.ps1 yok (GURULTU-KUR-1 henuz uretmedi)" }

# [3] 257 takili kalem (kurulum-coz-4.tsv); Deneme: yalniz kapilar, 3 kalem
Adim "3" "python tools\kurulum_d2.py --faz kur --coz docs\video-tarama\kurulum-coz-4.tsv" {
    & $py -I (Dosya 'tools\kurulum_d2.py') --faz kur --coz (Dosya 'docs\video-tarama\kurulum-coz-4.tsv') } {
    & $py -I (Dosya 'tools\kurulum_d2.py') --faz kur --sadece-kapi --n 3 --coz (Dosya 'docs\video-tarama\kurulum-coz-4.tsv') | Select-Object -Last 3 }

# [4] lightpanda (WSL'e kopyalar; SHA256 betigin icinde dogrulanir). Betikte -Deneme yok: Deneme'de yalniz ikili/hash yoklanir.
Adim "4" "tools\kurulum_lightpanda.ps1" { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_lightpanda.ps1') } {
    $src = 'C:\Users\pc\Apps\lightpanda\lightpanda-x86_64-linux'
    if (Test-Path $src) { $h = (Get-FileHash $src -Algorithm SHA256).Hash.ToLower(); Write-Host "  [deneme] ikili var, sha256=$($h.Substring(0,12))..." } else { Write-Host "  [deneme] ikili yok: $src"; $global:LASTEXITCODE = 1 } }

# [5] guvenlik seti
Adim "5" "tools\kurulum_guvenlik.ps1" { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_guvenlik.ps1') } { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_guvenlik.ps1') -Deneme | Select-Object -Last 3 }

# [6] Atomic Chat sessiz kurulum; SHA256 eslesmezse ATLA
$atomik = 'C:\Users\pc\Apps\atomic-chat\Atomic.Chat_2.3.5_x64-setup.exe'
$atomikSha = 'd446ad9ce999c0b95cb60d94b647ba0abd5668e5b2ed1841b797680715707d7f'
Adim "6" "Atomic Chat /S (SHA256 dogrulanir)" {
    if (-not (Test-Path $atomik)) { Write-Host "  kurulum dosyasi yok"; $global:LASTEXITCODE = 2; return }
    $h = (Get-FileHash $atomik -Algorithm SHA256).Hash.ToLower()
    if ($h -ne $atomikSha) { Write-Host "  SHA256 eslesmiyor, ATLANDI"; $global:LASTEXITCODE = 3; return }
    $p = Start-Process -FilePath $atomik -ArgumentList '/S' -Wait -PassThru
    $global:LASTEXITCODE = $p.ExitCode } {
    if (-not (Test-Path $atomik)) { Write-Host "  [deneme] dosya yok"; $global:LASTEXITCODE = 2; return }
    $h = (Get-FileHash $atomik -Algorithm SHA256).Hash.ToLower()
    Write-Host ("  [deneme] SHA256 " + $(if ($h -eq $atomikSha) { 'ESLESTI' } else { 'ESLESMEDI' })); if ($h -ne $atomikSha) { $global:LASTEXITCODE = 3 } }

# [6s] sistem/winget kalemleri (yonetici onayi isteyebilir) en sonda
Adim "6s" "tools\kurulum_omer2.ps1 -Sistem (winget)" { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_omer2.ps1') -Sistem } { & $ps -NoProfile -ExecutionPolicy Bypass -File (Dosya 'tools\kurulum_omer2.ps1') -Sistem -Deneme | Select-Object -Last 3 }

# [7] kurulum sonrasi: kanit + envanter + katalog + 'her seyimiz' dizinine isleme (NIHAI 36J)
Adim "7" "kurulu_kanit.py + envanter/topla.py + katalog_yenile.py + envanter_tara.py --dizin" {
    & $py -I (Dosya 'tools\kurulu_kanit.py')
    if (Test-Path (Dosya 'tools\envanter\topla.py')) { & $py -I (Dosya 'tools\envanter\topla.py') }
    & $py -I (Dosya 'tools\katalog_yenile.py')
    & $py -I (Dosya 'tools\envanter_tara.py') --dizin } { Write-Host "  [deneme] 4 betik: kurulu_kanit, topla, katalog_yenile, envanter_tara --dizin" }

$say = (Import-Csv $sonuc -Delimiter "`t" | Select-Object -Last 14 | Group-Object durum | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ' '
Write-Host "KUR-HEPSI bitti. Son kosu: $say  | sonuc: rapor\kur-hepsi-sonuc.tsv"
