param([switch]$Deneme,[switch]$Sistem)
# KURULUM-5B (uretici: tools/kurulum_omer2_uret.py). Omer kosar. -Deneme kurulum yapmaz, ne yapacagini yazar.
# -Sistem: winget (calisma zamani/derleyici/uygulama) satirlari yalniz bu bayrakla kosar (Node/Python surumunu degistirebilir).
# Mevcut olan ZATEN atlanir. Anahtar/ortam degeri yazdirilmaz. Silme yok.
$ErrorActionPreference="Continue"
$sonuc="$PSScriptRoot/../rapor/kurulum-omer2-sonuc.tsv"
if(-not (Test-Path $sonuc)){"kalem`tyontem`tdurum`tnot" | Set-Content $sonuc -Encoding utf8}
$sk="$env:USERPROFILE\.claude\skills"; $klonkok="__KLON__"; $indir="$env:USERPROFILE\Downloads\kurulum5b"
$uvexe=(Get-Command uv.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$npmexe=(Get-Command npm.cmd -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$gitexe=(Get-Command git.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
function Kayit($k,$y,$d,$n){ "$k`t$y`t$d`t$n" | Add-Content $sonuc -Encoding utf8; Write-Host "$d $y $k" }
function Kur5Cal($k,$y,$tanim,[scriptblock]$is){ if($Deneme){Kayit $k $y DENEME $tanim;return}
  try{ & $is; if($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE){Kayit $k $y KURULDU $tanim}else{Kayit $k $y HATA "exit $LASTEXITCODE"} }catch{Kayit $k $y HATA $_.Exception.Message} }
function Kur5Npm($k,$p){ if(-not $npmexe){Kayit $k NPM HATA "npm.cmd yok";return}
  if($null -eq $script:npmliste){ $script:npmliste=(& $npmexe ls -g --depth 0 --parseable 2>$null) -join "`n" }
  if($script:npmliste -match ('(^|[\\/])'+[regex]::Escape($p)+'(\r?\n|$)')){Kayit $k NPM ZATEN $p;return}
  Kur5Cal $k NPM "npm i -g $p" { & $npmexe i -g $p 2>&1 | Out-Null } }
function Kur5Uv($k,$p){ if(-not $uvexe){Kayit $k UV HATA "uv.exe yok";return}
  $a=$p -split ' '; Kur5Cal $k UV "uv tool install $p" { & $uvexe tool install @a 2>&1 | Out-Null } }
function Kur5Pip($k,$p){ Kur5Cal $k PIP "pip install --user $p" { & python.exe -m pip install --user $p 2>&1 | Out-Null } }
function Kur5Venv($k,$p,$py){ $v="$env:USERPROFILE\.venvs\$($k -replace '[^\w.-]','_')"
  if(Test-Path $v){Kayit $k VENV ZATEN $v;return}
  Kur5Cal $k VENV "uv venv $v --python $py; uv pip install $p" { & $uvexe venv $v --python $py 2>&1 | Out-Null; & $uvexe pip install --python "$v\Scripts\python.exe" $p 2>&1 | Out-Null } }
function Kur5Winget($k,$id){ if(-not $Sistem){Kayit $k WINGET ATLANDI "-Sistem yok: $id";return}
  Kur5Cal $k WINGET "winget install --id $id" { winget.exe install --id $id -e --silent --accept-package-agreements --accept-source-agreements 2>&1 | Out-Null } }
function Kur5Composer($k,$p){ Kur5Cal $k COMPOSER "composer global require $p" { composer.bat global require $p 2>&1 | Out-Null } }
function Kur5Vscode($k,$id){ Kur5Cal $k VSCODE "code --install-extension $id" { code.cmd --install-extension $id 2>&1 | Out-Null } }
function Kur5Indir($k,$url){ $ad=Split-Path $url -Leaf; $dst=Join-Path $indir $ad
  if(Test-Path $dst){Kayit $k INDIR ZATEN $dst;return}
  Kur5Cal $k INDIR "$url -> $dst (exe/msi'yi Omer calistirir)" { New-Item -ItemType Directory -Force $indir | Out-Null; Invoke-WebRequest -Uri $url -OutFile $dst -UseBasicParsing
    if($dst -like '*.zip'){ Expand-Archive $dst -DestinationPath ($dst -replace '\.zip$','') -Force } } }
function Kur5Klon($k,$repo){ $hedef=Join-Path $klonkok ($repo -replace '/','__')
  if(Test-Path $hedef){Kayit $k KLON ZATEN $hedef;return}
  Kur5Cal $k KLON "git clone --depth 1 $repo" { $env:GIT_TERMINAL_PROMPT=0; & $gitexe clone --depth 1 "https://github.com/$repo" $hedef 2>&1 | Out-Null } }
function Kur5Skill($k,$repo,$sub){ $kok=Join-Path $klonkok ($repo -replace '/','__')
  if($Deneme){Kayit $k SKILL DENEME "$repo $sub -> $sk";return}
  if(-not (Test-Path $kok)){ $env:GIT_TERMINAL_PROMPT=0; & $gitexe clone --depth 1 "https://github.com/$repo" $kok 2>&1 | Out-Null }
  $baz= if($sub){Join-Path $kok ($sub -replace '/','\')}else{$kok}
  if(-not (Test-Path $baz)){Kayit $k SKILL HATA "yol yok: $repo $sub";return}
  $say=0; Get-ChildItem $baz -Recurse -Filter SKILL.md -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '\\(node_modules|\.git)\\' } | ForEach-Object {
    $ad=Split-Path $_.DirectoryName -Leaf; $dst=Join-Path $sk $ad
    if(-not (Test-Path $dst)){ try{Copy-Item $_.DirectoryName $dst -Recurse -ErrorAction Stop; $say++}catch{Kayit $k SKILL HATA "$ad $($_.Exception.Message)"} } }
  if($say -gt 0){Kayit $k SKILL KURULDU "$repo $sub ($say skill)"}else{Kayit $k SKILL ZATEN "$repo $sub (yeni skill yok)"} }
function Kur5Ajan($k,$yol){ $ad=Split-Path $yol -Leaf; $dst="$env:USERPROFILE\.claude\agents\$ad"
  if(Test-Path $dst){Kayit $k AJAN ZATEN $ad;return}
  Kur5Cal $k AJAN "ECC $yol -> $dst" { Invoke-WebRequest -Uri "https://raw.githubusercontent.com/affaan-m/everything-claude-code/HEAD/$yol" -OutFile $dst -UseBasicParsing } }

