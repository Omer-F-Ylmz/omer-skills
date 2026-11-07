param([switch]$Deneme,[switch]$Sistem)
# GURULTU-KUR-1 (uretici: tools/kurulum_gurultu_uret.py). Omer kosar. -Deneme kurulum yapmaz, ne yapacagini yazar.
# -Sistem: winget (calisma zamani/derleyici/uygulama) satirlari yalniz bu bayrakla kosar (Node/Python surumunu degistirebilir).
# Mevcut olan ZATEN atlanir. Anahtar/ortam degeri yazdirilmaz. Silme yok.
$ErrorActionPreference="Continue"
$sonuc="$PSScriptRoot/../rapor/kurulum-gurultu-sonuc.tsv"
if(-not (Test-Path $sonuc)){"kalem`tyontem`tdurum`tnot" | Set-Content $sonuc -Encoding utf8}
$sk="$env:USERPROFILE\.claude\skills"; $klonkok="$env:USERPROFILE\Downloads\kurulum-gurultu\klon"; $indir="$env:USERPROFILE\Downloads\kurulum-gurultu"
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
function Kur5Rel($k,$repo,$ipucu){ $ghexe=(Get-Command gh.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
  if(-not $ghexe){Kayit $k RELEASE HATA "gh.exe yok";return}
  if($Deneme){Kayit $k RELEASE DENEME "gh release $repo asset~'$ipucu' -> $indir";return}
  try{ $r=(& $ghexe api "repos/$repo/releases/latest" 2>$null | ConvertFrom-Json); $a=$r.assets | Where-Object { ($ipucu -and $_.name -like "*$ipucu*") -or (-not $ipucu -and $_.name -match '(win|x64|x86_64).*\.(zip|exe|msi)$|\.(exe|msi)$') } | Select-Object -First 1
    if(-not $a){Kayit $k RELEASE HATA "asset yok: $repo $ipucu";return}
    $dst=Join-Path $indir $a.name; if(Test-Path $dst){Kayit $k RELEASE ZATEN $dst;return}
    New-Item -ItemType Directory -Force $indir | Out-Null; Invoke-WebRequest -Uri $a.browser_download_url -OutFile $dst -UseBasicParsing
    if($dst -like '*.zip'){ Expand-Archive $dst -DestinationPath ($dst -replace '\.zip$','') -Force }
    Kayit $k RELEASE KURULDU "$($a.name) -> $dst (exe/msi'yi Omer calistirir)" }catch{Kayit $k RELEASE HATA $_.Exception.Message} }
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

# --- Cloudflare/clef | OMER-SOR | Apache-2.0 | 51.21 GiB
# OMER-SOR (51.21 GiB): hf download Cloudflare/clef
# --- Cloudflare/clef-flash | OMER-SOR | Apache-2.0 | 17.77 GiB
# OMER-SOR (17.77 GiB): hf download Cloudflare/clef-flash
# --- Tijo2000/clef-decision-demo | KLON | MIT | 50 KB
Kur5Klon 'clef-decision-demo' 'ajmontalbano/clef-decision-demo'
# --- convaiinnovations/laya | OMER-SOR | Apache-2.0 | 2.21 GiB
# OMER-SOR (2.21 GiB): hf download convaiinnovations/laya
# --- axolotl | KLON | Apache-2.0 | 70 MB
Kur5Klon 'axolotl' 'axolotl-ai-cloud/axolotl'
# --- langchain-ai | KLON | MIT | 520 MB
Kur5Klon 'langchain-ai (langgraph)' 'langchain-ai/langgraph'
# --- HKUDS | KLON | MIT | 115 MB
Kur5Klon 'HKUDS (LightRAG)' 'HKUDS/LightRAG'
# --- multica-ai/andrej-karpathy-skills | SKILL | YOK (lisanssiz) | 20 KB
Kur5Skill 'andrej-karpathy-skills' 'multica-ai/andrej-karpathy-skills' 'skills'  # lisans: none
# --- ilabai/3dcodeverse | KLON | Apache-2.0 | 45 MB
Kur5Klon '3dcodeverse' 'gaoypeng/3dcodeverse'
# --- Heroic Labs (Nakama) | KLON | Apache-2.0 | 160 MB
Kur5Klon 'Nakama' 'heroiclabs/nakama'
# --- nano-pdf | UV | MIT | kucuk
Kur5Uv 'nano-pdf' 'nano-pdf'
# --- himalaya | INDIR | Apache-2.0 | 19 MB
Kur5Indir 'himalaya' 'https://github.com/pimalaya/himalaya/releases/download/v2.2.1/himalaya.x86_64-windows.zip'
# --- skills/manim-video | ZATEN | - | -
# ZATEN: ~/.claude/skills/manim-video, affaan-m-manim-video, nousresearch-manim-video
# --- nanochat | KLON | MIT | 2.5 MB
Kur5Klon 'nanochat' 'karpathy/nanochat'
# --- storm-research/SKILL | SKILL | MIT | kucuk
Kur5Skill 'storm-research' 'openwhat007/storm-research' ''
# --- Paperclip Agents | KLON | MIT | 480 MB
Kur5Klon 'Paperclip' 'paperclipai/paperclip'
# --- Spacedrive | UYGULAMA | Apache-2.0 | 86 MB msi
# UYGULAMA (86 MB msi, Omer calistirir): Kur5Indir 'Spacedrive' 'https://github.com/spacedriveapp/spacedrive/releases/download/v0.4.3/Spacedrive-windows-x86_64.msi'
# --- Typst | WINGET | Apache-2.0 | kucuk
Kur5Winget 'Typst' 'Typst.Typst'
# --- MegaTTS3 (ses turu adayi) | OMER-SOR | Apache-2.0 | 3.98 GiB
# OMER-SOR (3.98 GiB, ses turu adayi, indirilmedi): hf download ByteDance/MegaTTS3
