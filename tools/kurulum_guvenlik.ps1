# kurulum_guvenlik.ps1  —  Omer calistirir. Once:  -Deneme
# Kendi site/uygulama/binary'lerini sertlestirme ve inceleme seti. Tum indirmeler resmi kaynaktan,
# surum sabit, SHA256 GitHub release digest'iyle eslenir; eslesmezse dosya silinir, ATLANIR.
# Zaten kurulu olan atlanir. AFL++ ve aircrack-ng Omer 6 Kas karariyla HARIC.
# -Derle : ProxSpace icinde Proxmark3 istemcisini derler (uzun surer; ayri bayrak).
param([switch]$Deneme, [switch]$Derle)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$log = Join-Path $PSScriptRoot '..\rapor\kurulum-guvenlik-sonuc.tsv'
"kalem`tyontem`tdurum`tnot" | Out-File -FilePath $log -Encoding utf8
function Kayit($k,$y,$d,$n){ "$k`t$y`t$d`t$n" | Out-File -FilePath $log -Append -Encoding utf8; Write-Host "$k  $d  $n" }
function Exe($ad){ (Get-Command "$ad.exe" -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source }

$kok = Join-Path $env:USERPROFILE ('Desktop\Claude ile yap' + [char]0x0131 + 'lanlar\araclar\guvenlik')
$ind = Join-Path $kok '_indir'
$klon = 'C:\Projeler\_araclar\v'
if(-not $Deneme){ New-Item -ItemType Directory -Force -Path $ind | Out-Null }

function PathEkle($dir){
  $p = [Environment]::GetEnvironmentVariable('Path','User')
  if(($p -split ';') -notcontains $dir){ [Environment]::SetEnvironmentVariable('Path', ($p.TrimEnd(';') + ';' + $dir), 'User') }
  if(($env:Path -split ';') -notcontains $dir){ $env:Path = $env:Path + ';' + $dir }
}

function Indir($ad,$url,$sha,$boyut){
  $dosya = Join-Path $ind ($url.Split('/')[-1])
  if(Test-Path $dosya){
    if($sha -and ((Get-FileHash $dosya -Algorithm SHA256).Hash -ieq $sha)){ return $dosya }
    Remove-Item $dosya -Force
  }
  Invoke-WebRequest -Uri $url -OutFile $dosya -UseBasicParsing
  if(-not (Test-Path $dosya)){ Kayit $ad indir HATA "indirilemedi $url"; return $null }
  if($boyut -and ((Get-Item $dosya).Length -ne $boyut)){ Kayit $ad indir HATA "boyut uyusmadi"; Remove-Item $dosya -Force; return $null }
  if($sha){
    $h = (Get-FileHash $dosya -Algorithm SHA256).Hash
    if($h -ine $sha){ Kayit $ad indir HATA "SHA256 uyusmadi ($h)"; Remove-Item $dosya -Force; return $null }
  }
  return $dosya
}

# --- 1) GitHub release: surum sabit + SHA256 ---
$rel = @(
  @{ ad='jadx';   url='https://github.com/skylot/jadx/releases/download/v1.5.6/jadx-gui-1.5.6-win.zip';
     sha='6e070b197d4e40275d10f6559a1661bdd2e2bb325e9ef4181c7ac1286b274d99'; boyut=72668086; hedef='jadx-1.5.6'; tip='zip'; bin='' ; kontrol='jadx-gui-1.5.6.exe' },
  @{ ad='jadx-cli'; url='https://github.com/skylot/jadx/releases/download/v1.5.6/jadx-1.5.6.zip';
     sha='545ea2be9c242511bc145755cf4bda2485ade42966e096f8b4d3da2a230e8974'; boyut=72646741; hedef='jadx-cli-1.5.6'; tip='zip'; bin='bin'; kontrol='bin\jadx.bat' },
  @{ ad='apktool'; url='https://github.com/iBotPeaches/Apktool/releases/download/v3.0.3/apktool_3.0.3.jar';
     sha='dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423'; boyut=15478013; hedef='apktool-3.0.3'; tip='jar'; bin=''; kontrol='apktool.bat' },
  @{ ad='yara';   url='https://github.com/VirusTotal/yara/releases/download/v4.6.0/yara-4.6.0-2443-win64.zip';
     sha='5e7124f173ed442458429ac0f79a4db2c024cc183c595737d477a7575d81e6dc'; boyut=2238893; hedef='yara-4.6.0'; tip='zip'; bin=''; kontrol='yara64.exe' },
  @{ ad='ghidra'; url='https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.2_build/ghidra_12.2_PUBLIC_20261016.zip';
     sha='2c2cd776db3c1f6a097ba418922378ac3649cadd5e844a6f5f088ae628a7be67'; boyut=569712708; hedef='ghidra-12.2'; tip='zip'; bin=''; kontrol='ghidra_12.2_PUBLIC\ghidraRun.bat' }
)
foreach($r in $rel){
  $h = Join-Path $kok $r.hedef
  if(Test-Path (Join-Path $h $r.kontrol)){ Kayit $r.ad gh-release ZATEN $h; continue }
  if($Deneme){ Kayit $r.ad gh-release DENEME ("$($r.url) -> $h ($([math]::Round($r.boyut/1MB)) MB, SHA256 sabit)"); continue }
  $f = Indir $r.ad $r.url $r.sha $r.boyut
  if(-not $f){ continue }
  New-Item -ItemType Directory -Force -Path $h | Out-Null
  if($r.tip -eq 'zip'){ Expand-Archive -Path $f -DestinationPath $h -Force }
  else {
    Copy-Item $f (Join-Path $h 'apktool.jar') -Force
    "@echo off`r`njava -jar `"%~dp0apktool.jar`" %*" | Out-File -FilePath (Join-Path $h 'apktool.bat') -Encoding ascii
  }
  if(-not (Test-Path (Join-Path $h $r.kontrol))){
    $alt = Get-ChildItem $h -Directory | Select-Object -First 1
    if($alt -and (Test-Path (Join-Path $alt.FullName $r.kontrol))){ $h = $alt.FullName }
  }
  if(Test-Path (Join-Path $h $r.kontrol)){
    if($r.ad -ne 'ghidra'){ PathEkle (Join-Path $h $r.bin).TrimEnd('\') }
    Kayit $r.ad gh-release KURULDU $h
  } else { Kayit $r.ad gh-release HATA "acildi ama $($r.kontrol) yok" }
}

# ghidra masaustu kisayolu yerine PATH'e kucuk baslatici
$gr = Get-ChildItem (Join-Path $kok 'ghidra-12.2') -Recurse -Filter ghidraRun.bat -ErrorAction SilentlyContinue | Select-Object -First 1
if($gr -and -not $Deneme){
  $bat = Join-Path $kok 'bin'; New-Item -ItemType Directory -Force -Path $bat | Out-Null
  "@echo off`r`ncall `"$($gr.FullName)`" %*" | Out-File -FilePath (Join-Path $bat 'ghidra.bat') -Encoding ascii
  PathEkle $bat
}

# --- 2) pip (wheel'i olanlar) ---
$py = Exe python
foreach($k in @('frida-tools','yara-python')){
  if($Deneme){ Kayit $k pip DENEME "python -m pip install --user $k"; continue }
  if(-not $py){ Kayit $k pip HATA 'python yok'; continue }
  & $py -m pip install --user --upgrade $k 2>&1 | Out-Null
  if($LASTEXITCODE -eq 0){ Kayit $k pip KURULDU $k } else { Kayit $k pip HATA "exit $LASTEXITCODE" }
}

# --- 3) binwalk v3 (Rust; PyPI'deki 2.1.0 yalniz sdist, Python 3.12'de calismaz) ---
$cargo = Exe cargo
if(-not $cargo){ $c2 = Join-Path $env:USERPROFILE '.cargo\bin\cargo.exe'; if(Test-Path $c2){ $cargo = $c2 } }
if($Deneme){ Kayit binwalk cargo DENEME ("cargo +stable-x86_64-pc-windows-msvc install binwalk" + $(if($cargo){''}else{' (once winget Rustlang.Rustup)'})) }
elseif(Exe binwalk){ Kayit binwalk cargo ZATEN (Exe binwalk) }
else {
  if(-not $cargo){
    $w = Exe winget
    & $w install --id Rustlang.Rustup -e --silent --accept-source-agreements --accept-package-agreements 2>&1 | Out-Null
    $c2 = Join-Path $env:USERPROFILE '.cargo\bin\cargo.exe'; if(Test-Path $c2){ $cargo = $c2; PathEkle (Split-Path $c2) }
  }
  if(-not $cargo){ Kayit binwalk cargo HATA 'rustup kurulamadi' }
  else {
    # varsayilan zincir gnu; binwalk'un C bagimliliklari icin makinedeki VS 2022 MSVC zinciri kullanilir (varsayilan degismez)
    $rustup = Join-Path (Split-Path $cargo) 'rustup.exe'
    $zincir = 'stable-x86_64-pc-windows-msvc'
    if(Test-Path $rustup){ & $rustup toolchain install $zincir --profile minimal 2>&1 | Out-Null }
    & $cargo "+$zincir" install binwalk 2>&1 | Out-File -FilePath (Join-Path $ind 'binwalk-cargo.log') -Encoding utf8
    if($LASTEXITCODE -eq 0){ Kayit binwalk cargo KURULDU "cargo +$zincir install binwalk" } else { Kayit binwalk cargo HATA "exit $LASTEXITCODE, ayrinti: _indir\binwalk-cargo.log" }
  }
}

# --- 4) nmap (winget; Npcap ayri ve ucretsiz surumu sessiz kurulmaz) ---
if(Exe nmap){ Kayit nmap winget ZATEN (Exe nmap) }
elseif($Deneme){ Kayit nmap winget DENEME 'winget install Insecure.Nmap (winget en yeni 7.80; Npcap kurulum penceresi acilir)' }
else {
  $w = Exe winget
  & $w install --id Insecure.Nmap -e --accept-source-agreements --accept-package-agreements 2>&1 | Out-Null
  if($LASTEXITCODE -eq 0){ Kayit nmap winget KURULDU 'Insecure.Nmap' } else { Kayit nmap winget HATA "exit $LASTEXITCODE" }
}

# --- 5) Metasploit: mevcut klon + Ruby 3.4 bundle ---
$msf = Join-Path $klon 'rapid7__metasploit-framework'
$bundle = Exe bundle; if(-not $bundle){ $b2 = Get-Command bundle.bat -ErrorAction SilentlyContinue; if($b2){ $bundle = $b2.Source } }
if(-not (Test-Path (Join-Path $msf 'msfconsole'))){ Kayit metasploit bundle HATA "klon yok: $msf" }
elseif($Deneme){ Kayit metasploit bundle DENEME "bundle install ($msf, development/test/coverage haric)" }
elseif(-not $bundle){ Kayit metasploit bundle HATA 'bundle yok' }
else {
  Push-Location $msf
  & $bundle config set --local without 'development test coverage' 2>&1 | Out-Null
  & $bundle install 2>&1 | Out-File -FilePath (Join-Path $ind 'msf-bundle.log') -Encoding utf8
  $ok = ($LASTEXITCODE -eq 0)
  Pop-Location
  if($ok){
    $bat = Join-Path $kok 'bin'; New-Item -ItemType Directory -Force -Path $bat | Out-Null
    "@echo off`r`ncd /d `"$msf`"`r`nbundle exec ruby msfconsole %*" | Out-File -FilePath (Join-Path $bat 'msfconsole.bat') -Encoding ascii
    PathEkle $bat
    Kayit metasploit bundle KURULDU "$msf (msfconsole.bat)"
  } else { Kayit metasploit bundle HATA "bundle install basarisiz, ayrinti: _indir\msf-bundle.log" }
}

# --- 6) Proxmark3: ProxSpace v3.11 (release digest yok -> boyut sabit, hash kayda yazilir) ---
$ps = Join-Path $kok 'ProxSpace'
if(Test-Path (Join-Path $ps 'runme64.bat')){ Kayit proxspace gh-release ZATEN $ps }
elseif($Deneme){ Kayit proxspace gh-release DENEME 'ProxSpace v3.11 .7z (747 MB) indir + ac; -Derle ile pm3 istemcisi derlenir' }
else {
  $f = Indir proxspace 'https://github.com/Gator96100/ProxSpace/releases/download/v3.11/ProxSpace.7z' $null 783412388
  if($f){
    $h = (Get-FileHash $f -Algorithm SHA256).Hash
    $z = Exe 7z; if(-not $z -and (Test-Path 'C:\Program Files\7-Zip\7z.exe')){ $z = 'C:\Program Files\7-Zip\7z.exe' }
    if($z){ & $z x $f "-o$kok" -y 2>&1 | Out-Null } else { & tar.exe -xf $f -C $kok 2>&1 | Out-Null }
    if(Test-Path (Join-Path $ps 'runme64.bat')){ Kayit proxspace gh-release KURULDU "$ps sha256=$h" } else { Kayit proxspace gh-release HATA "acilamadi sha256=$h" }
  }
}
if($Derle -and -not $Deneme -and (Test-Path (Join-Path $ps 'runme64.bat'))){
  $pm3 = Join-Path $ps 'pm3\proxmark3'
  if(-not (Test-Path $pm3)){ & git clone --depth 1 https://github.com/RfidResearchGroup/proxmark3.git $pm3 2>&1 | Out-Null }
  Push-Location $ps
  & cmd /c "runme64.bat -c `"cd pm3/proxmark3 && make clean && make -j client`"" 2>&1 | Out-File -FilePath (Join-Path $ind 'pm3-derle.log') -Encoding utf8
  Pop-Location
  if(Test-Path (Join-Path $pm3 'client\proxmark3.exe')){ Kayit proxmark3 derle KURULDU $pm3 } else { Kayit proxmark3 derle HATA 'derleme basarisiz, _indir\pm3-derle.log' }
}

# --- 7) Haric (Omer 6 Kas) ---
Kayit aflplusplus haric ATLA 'Omer 6 Kas: almiyoruz'
Kayit aircrack-ng haric ATLA 'Omer 6 Kas: almiyoruz'

$say = Import-Csv $log -Delimiter "`t" | Group-Object durum | ForEach-Object { "$($_.Name)=$($_.Count)" }
Write-Host ("OZET: " + ($say -join ' ')) 
Write-Host "Yeni PATH icin terminali kapatip ac."
