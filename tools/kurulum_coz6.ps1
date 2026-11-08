param([switch]$Deneme,[switch]$Sistem)
# BUL-KUR-2 (uretici: tools/kurulum_gurultu_uret.py). Omer kosar. -Deneme kurulum yapmaz, ne yapacagini yazar.
# -Sistem: winget (calisma zamani/derleyici/uygulama) satirlari yalniz bu bayrakla kosar (Node/Python surumunu degistirebilir).
# Mevcut olan ZATEN atlanir. Anahtar/ortam degeri yazdirilmaz. Silme yok.
$ErrorActionPreference="Continue"
$sonuc="$PSScriptRoot/../rapor/kurulum-coz6-sonuc.tsv"
if(-not (Test-Path $sonuc)){"kalem`tyontem`tdurum`tnot" | Set-Content $sonuc -Encoding utf8}
$sk="$env:USERPROFILE\.claude\skills"; $klonkok="$env:USERPROFILE\Downloads\kurulum-coz6\klon"; $indir="$env:USERPROFILE\Downloads\kurulum-coz6"
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

# --- DeBERTa-v3-large | OMER-SOR | mit | 2.97 GiB
# OMER-SOR (2.97 GiB): hf download microsoft/deberta-v3-large
# --- Flux Schnell | OMER-SOR | apache-2.0 | 53.87 GiB
# OMER-SOR (53.87 GiB): hf download black-forest-labs/FLUX.1-schnell
# --- HunyuanVideo-gguf | OMER-SOR | other | 123.79 GiB
# OMER-SOR (123.79 GiB): hf download city96/HunyuanVideo-gguf
# --- Lyra 2.0 | OMER-SOR | ? | 91.59 GiB
# OMER-SOR (91.59 GiB): hf download nvidia/Lyra-2.0
# --- ModernBERT | OMER-SOR | apache-2.0 | 2.92 GiB
# OMER-SOR (2.92 GiB): hf download answerdotai/ModernBERT-base
# --- NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 | OMER-SOR | other | 20.10 GiB
# OMER-SOR (20.10 GiB): hf download nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
# --- Wan2.1 | OMER-SOR | apache-2.0 | 453.95 GiB
# OMER-SOR (453.95 GiB): hf download Comfy-Org/Wan-2.1
# --- WiLoR | OMER-SOR | cc-by-nc-4.0 | 2.48 GiB
# OMER-SOR (2.48 GiB): hf download rolpotamias/WiLoR
# --- nemotron-3-nano-omni-30b-a3b-reasoning | OMER-SOR | other | 61.52 GiB
# OMER-SOR (61.52 GiB): hf download nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16
# --- nemotron-3-ultra-550b-a55b | OMER-SOR | other | 1044.09 GiB
# OMER-SOR (1044.09 GiB): hf download nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16
# --- nemotron-3.5-lightning-30b-a3b | OMER-SOR | other | 61.32 GiB
# OMER-SOR (61.32 GiB): hf download nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
# --- nemotron-parse-2 | OMER-SOR | openmdw-1.1 | 3.38 GiB
# OMER-SOR (3.38 GiB): hf download nvidia/NVIDIA-Nemotron-Parse-2.0
# --- qwen3.8 | OMER-SOR | apache-2.0 | 51.77 GiB
# OMER-SOR (51.77 GiB): hf download Qwen/Qwen3.8-27B
# --- CogVideoX-1.5 | OMER-SOR | other | 28.92 GiB
# OMER-SOR (28.92 GiB): hf download zai-org/CogVideoX1.5-5B
# --- FireredASR | OMER-SOR | apache-2.0 | 4.41 GiB
# OMER-SOR (4.41 GiB): hf download FireRedTeam/FireRedASR2-AED
# --- Fluid-1 Mini | OMER-SOR | other | 4.24 GiB
# OMER-SOR (4.24 GiB): hf download altic-dev/fluid-1-mini
# --- Fluid-1 Pico | HF | ? | 0.61 GiB
# hf download altic-dev/Fluid-1-Pico-0.8B-MLX-6bit  (kucuk: Omer hf CLI ile indirir)
# --- mmBERT-base | HF | mit | 1.16 GiB
# hf download jhu-clsp/mmBERT-base  (kucuk: Omer hf CLI ile indirir)
# --- GitHub Copilot Chat | VSCODE
Kur5Vscode 'GitHub Copilot Chat' 'GitHub Copilot Chat'
# --- sqlite | WINGET | winget:SQLite.SQLite SQLite'ın kendisi; diğerleri Node istem
Kur5Winget 'sqlite' 'SQLite.SQLite'
# --- Texel Density Checker | BLENDER
# blender uzantisi: Blender icinde Edit>Preferences>Get Extensions: Texel Density Checker
# --- P-H3-Image | OMER-SOR | other | 92.99 GiB
# OMER-SOR (92.99 GiB): hf download PrunaAI/P-H3-Image
# --- SkinTokens | HF | mit | 1.51 GiB
# hf download VAST-AI/SkinTokens  (kucuk: Omer hf CLI ile indirir)
