# kurulum_duzelt_1107.ps1 — kur_hepsi 1. ve 2. adimlarda HATA veren 7 kalemin kok neden duzeltmesi. Once: -Deneme
# FilaCheck+Rector (composer yok) · EasySpider (.7z) · Ocis (yalniz Linux -> WSL) · geo-crawlers (eski klon) · Spacedrive (baglanti koptu) · DataviewJS (Obsidian eklentisi)
param([switch]$Deneme)
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$log = Join-Path $PSScriptRoot '..\rapor\kurulum-duzelt-1107-sonuc.tsv'
"kalem`tyontem`tdurum`tnot" | Out-File -FilePath $log -Encoding utf8
function Kayit($k,$y,$d,$n){ "$k`t$y`t$d`t$n" | Out-File -FilePath $log -Append -Encoding utf8; Write-Host "$k  $d  $n" }
function Exe($ad){ (Get-Command "$ad.exe","$ad.bat","$ad.cmd" -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source }
function Indir($url,$dst,$sha){
  New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
  if((Test-Path $dst) -and $sha -and ((Get-FileHash $dst -Algorithm SHA256).Hash -ieq $sha)){ return $true }
  for($i=1; $i -le 3; $i++){
    try { Invoke-WebRequest -Uri $url -OutFile $dst -UseBasicParsing; break } catch { Start-Sleep -Seconds (10*$i) }
  }
  if(-not (Test-Path $dst)){ return $false }
  if($sha -and ((Get-FileHash $dst -Algorithm SHA256).Hash -ine $sha)){ Remove-Item $dst -Force; return $false }
  return $true
}
$arac = Join-Path $env:USERPROFILE ('Desktop\Claude ile yap' + [char]0x0131 + 'lanlar\araclar')
$lbin = Join-Path $env:USERPROFILE '.local\bin'

# --- 1) Composer + FilaCheck + Rector ---
$php = Exe php
if(-not $php){ Kayit composer phar HATA 'php yok' }
elseif($Deneme){ Kayit composer phar DENEME "getcomposer.org latest-stable composer.phar (+.sha256) -> $lbin; php.ini openssl/curl/zip/mbstring; composer global require laraveldaily/filacheck rector/rector" }
else {
  $pdir = Split-Path $php; $ini = Join-Path $pdir 'php.ini'
  if(-not (Test-Path $ini) -and (Test-Path (Join-Path $pdir 'php.ini-production'))){ Copy-Item (Join-Path $pdir 'php.ini-production') $ini }
  if(Test-Path $ini){
    $t = Get-Content $ini -Raw
    $t = $t -replace '(?m)^;\s*extension_dir\s*=\s*"ext"', 'extension_dir = "ext"'
    foreach($e in 'openssl','curl','zip','mbstring','fileinfo'){ $t = $t -replace "(?m)^;\s*extension=$e\s*$", "extension=$e" }
    Set-Content $ini $t -Encoding ascii
  }
  $shaTxt = try { (Invoke-WebRequest 'https://getcomposer.org/download/latest-stable/composer.phar.sha256' -UseBasicParsing).Content.Trim().Split(' ')[0] } catch { '' }
  $phar = Join-Path $lbin 'composer.phar'
  if($shaTxt -and (Indir 'https://getcomposer.org/download/latest-stable/composer.phar' $phar $shaTxt)){
    "@echo off`r`n`"$php`" `"%~dp0composer.phar`" %*" | Out-File (Join-Path $lbin 'composer.bat') -Encoding ascii
    Kayit composer phar KURULDU "$phar sha256 dogru"
    foreach($p in 'laraveldaily/filacheck','rector/rector'){
      & (Join-Path $lbin 'composer.bat') global require $p --no-interaction 2>&1 | Out-File (Join-Path $env:TEMP 'composer-kur.log') -Append -Encoding utf8
      if($LASTEXITCODE -eq 0){ Kayit $p composer KURULDU $p } else { Kayit $p composer HATA "exit $LASTEXITCODE, $env:TEMP\composer-kur.log" }
    }
    $cbin = Join-Path $env:APPDATA 'Composer\vendor\bin'
    $up = [Environment]::GetEnvironmentVariable('Path','User'); if(($up -split ';') -notcontains $cbin){ [Environment]::SetEnvironmentVariable('Path', $up.TrimEnd(';') + ';' + $cbin, 'User') }
  } else { Kayit composer phar HATA 'indirme ya da SHA256 basarisiz' }
}

# --- 2) EasySpider Windows .7z (SHA256 GitHub digest) ---
$es = Join-Path $arac 'EasySpider'
$z = 'C:\Program Files\7-Zip\7z.exe'
function EsVar { (Test-Path -LiteralPath $es) -and [bool](Get-ChildItem -LiteralPath $es -Recurse -Filter 'EasySpider*.exe' -ErrorAction SilentlyContinue | Select-Object -First 1) }
if(EsVar){ Kayit EasySpider 7z ZATEN $es }
elseif($Deneme){ Kayit EasySpider 7z DENEME "v0.6.5 Windows_x64.7z (361 MB) -> $es" }
else {
  $f = Join-Path $es '_indir\EasySpider_0.6.5_Windows_x64.7z'
  if(Indir 'https://github.com/NaiboWang/EasySpider/releases/download/v0.6.5/EasySpider_0.6.5_Windows_x64.7z' $f '5b60c019d53ddc442b2f1eba1fa2c7ffb13be41f0556501407927eae87013fa4'){
    & $z x $f "-o$es" -y 2>&1 | Out-Null
    if(EsVar){ Kayit EasySpider 7z KURULDU $es } else { Kayit EasySpider 7z HATA 'acildi ama EasySpider*.exe yok' }
  } else { Kayit EasySpider 7z HATA 'indirme/SHA256' }
}

# --- 2b) WSL saglik + lightpanda (kur_hepsi 4. adimda ext4.vhdx 0x80071127; betik yanlislikla 'Kuruldu' demisti) ---
if($Deneme){ Kayit wsl saglik DENEME 'wsl --shutdown; wsl -e true; sonra tools\kurulum_lightpanda.ps1' }
else {
  & wsl.exe --shutdown 2>&1 | Out-Null; Start-Sleep -Seconds 8
  $t = (& wsl.exe -e sh -c 'echo wsl-ok' 2>&1) -join ' '
  if($t -match 'wsl-ok'){
    Kayit wsl saglik KURULDU 'WSL acildi'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'kurulum_lightpanda.ps1') 2>&1 | Out-File (Join-Path $env:TEMP 'lightpanda-kur.log') -Encoding utf8
    if($LASTEXITCODE -eq 0){ Kayit lightpanda wsl KURULDU '~/.local/bin/lightpanda' } else { Kayit lightpanda wsl HATA "exit $LASTEXITCODE, $env:TEMP\lightpanda-kur.log" }
  } else { Kayit wsl saglik HATA "WSL acilmadi: $t" }
}

# --- 3) Ocis: Windows surumu yok -> WSL'e Linux ikilisi ---
$od = 'C:\Users\pc\Apps\ocis'; $of = Join-Path $od 'ocis-8.2.3-linux-amd64'
$var = (& wsl.exe -e sh -c 'test -x ~/.local/bin/ocis && echo var' 2>$null)
if($var -match 'var'){ Kayit ocis wsl ZATEN '~/.local/bin/ocis' }
elseif($Deneme){ Kayit ocis wsl DENEME 'ocis 8.2.3 linux-amd64 (143 MB, SHA256) -> WSL ~/.local/bin/ocis' }
elseif(Indir 'https://github.com/owncloud/ocis/releases/download/v8.2.3/ocis-8.2.3-linux-amd64' $of '7a386c4e85ffe629d6ffdfb0a0ea4e60c87ac3620892b9534d0a3ec8b14fc68a'){
  & wsl.exe -e sh -c 'mkdir -p ~/.local/bin && cp /mnt/c/Users/pc/Apps/ocis/ocis-8.2.3-linux-amd64 ~/.local/bin/ocis && chmod +x ~/.local/bin/ocis' 2>&1 | Out-Null
  $v = (& wsl.exe -e sh -c '~/.local/bin/ocis version 2>&1 | head -3' 2>$null) -join ' '
  if($v){ Kayit ocis wsl KURULDU "~/.local/bin/ocis :: $v" } else { Kayit ocis wsl HATA 'kopyalandi, surum okunamadi' }
} else { Kayit ocis wsl HATA 'indirme/SHA256' }

# --- 4) geo-crawlers: yerel klon eski -> guncelle + kopyala ---
$gk = Join-Path $arac 'ana-liste\sickn33__agentic-awesome-skills'
$hedef = Join-Path $env:USERPROFILE '.claude\skills\geo-crawlers'
if(Test-Path (Join-Path $hedef 'SKILL.md')){ Kayit geo-crawlers skill ZATEN $hedef }
elseif($Deneme){ Kayit geo-crawlers skill DENEME "git pull --ff-only ($gk) + skills\geo-crawlers -> $hedef" }
else {
  $env:GIT_TERMINAL_PROMPT = 0
  & git -C $gk pull --ff-only --depth 1 2>&1 | Out-Null
  $src = Join-Path $gk 'skills\geo-crawlers'
  if(Test-Path (Join-Path $src 'SKILL.md')){ Copy-Item $src $hedef -Recurse -Force; Kayit geo-crawlers skill KURULDU $hedef }
  else { Kayit geo-crawlers skill HATA "pull sonrasi da yok: $src" }
}

# --- 5) Spacedrive msi (baglanti kopmustu) ---
$sd = Join-Path $env:USERPROFILE 'Downloads\kurulum-gurultu\Spacedrive-windows-x86_64.msi'
if($Deneme){ Kayit Spacedrive indir DENEME "yeniden indir (3 deneme) -> $sd" }
elseif(Indir 'https://github.com/spacedriveapp/spacedrive/releases/download/v0.4.3/Spacedrive-windows-x86_64.msi' $sd $null){ Kayit Spacedrive indir KURULDU "$sd (msi'yi Omer calistirir)" }
else { Kayit Spacedrive indir HATA '3 denemede indirilemedi' }

# --- 6) DataviewJS = Obsidian 'dataview' eklentisi: kayitli her kasaya ---
$oj = Join-Path $env:APPDATA 'obsidian\obsidian.json'
if(-not (Test-Path $oj)){ Kayit dataview obsidian HATA 'obsidian.json yok' }
else {
  $kasalar = ((Get-Content $oj -Raw | ConvertFrom-Json).vaults.PSObject.Properties | ForEach-Object { $_.Value.path }) | Where-Object { Test-Path $_ }
  $rel = $null
  foreach($k in $kasalar){
    $pd = Join-Path $k '.obsidian\plugins\dataview'
    if(Test-Path (Join-Path $pd 'main.js')){ Kayit dataview obsidian ZATEN $k; continue }
    if($Deneme){ Kayit dataview obsidian DENEME "blacksmithgu/obsidian-dataview latest main.js+manifest.json+styles.css -> $pd"; continue }
    if(-not $rel){ $rel = Invoke-RestMethod 'https://api.github.com/repos/blacksmithgu/obsidian-dataview/releases/latest' -Headers @{ 'User-Agent' = 'omer-kurulum' } }
    New-Item -ItemType Directory -Force -Path $pd | Out-Null
    foreach($ad in 'main.js','manifest.json','styles.css'){
      $a = $rel.assets | Where-Object name -eq $ad
      if($a){ Invoke-WebRequest $a.browser_download_url -OutFile (Join-Path $pd $ad) -UseBasicParsing }
    }
    $cp = Join-Path $k '.obsidian\community-plugins.json'
    $l = @(); if(Test-Path $cp){ $l = @(Get-Content $cp -Raw | ConvertFrom-Json) }
    if($l -notcontains 'dataview'){ $l += 'dataview'; ConvertTo-Json @($l) | Set-Content $cp -Encoding utf8 }
    if(Test-Path (Join-Path $pd 'main.js')){ Kayit dataview obsidian KURULDU "$k ($($rel.tag_name))" } else { Kayit dataview obsidian HATA $k }
  }
  if(-not $kasalar){ Kayit dataview obsidian HATA 'kayitli kasa yok' }
}

# --- Kapsam disi (bilgi) ---
Kayit SwiftPM haric ATLA 'Omer 7 Kas 18:20: Swift gerek yok'
Kayit lightpanda-releases haric ATLA 'kur_hepsi adim 4 (WSL) ile kuruluyor; bu satir tekrar'

$say = Import-Csv $log -Delimiter "`t" | Group-Object durum | ForEach-Object { "$($_.Name)=$($_.Count)" }
Write-Host ("OZET: " + ($say -join ' '))
