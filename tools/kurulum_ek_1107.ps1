# kurulum_ek_1107.ps1  —  kur_hepsi.ps1 cagirir (adim 6e). Once: -Deneme
# Kapsam (Omer 7 Kas 18:20): coz-5 DOGRULANDI ama gh/npm/pip disi kalemler + 2 GB ustu EVET'ler (MegaTTS3, CUDA).
# DaVinci Resolve winget'te yok; resmi sitede kayit formu var -> Omer tarayicidan indirir (betik yalniz yoklar).
param([switch]$Deneme)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$log = Join-Path $PSScriptRoot '..\rapor\kurulum-ek-1107-sonuc.tsv'
"kalem`tyontem`tdurum`tnot" | Out-File -FilePath $log -Encoding utf8
function Kayit($k,$y,$d,$n){ "$k`t$y`t$d`t$n" | Out-File -FilePath $log -Append -Encoding utf8; Write-Host "$k  $d  $n" }
function Exe($ad){ (Get-Command "$ad.exe","$ad.cmd" -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source }
$kok = Join-Path $env:USERPROFILE ('Desktop\Claude ile yap' + [char]0x0131 + 'lanlar\araclar')

# --- 1) winget: SQLite (sqlite3 CLI) ---
if(Exe sqlite3){ Kayit sqlite winget ZATEN (Exe sqlite3) }
elseif($Deneme){ Kayit sqlite winget DENEME 'winget install SQLite.SQLite' }
else {
  & winget.exe install --id SQLite.SQLite -e --silent --accept-source-agreements --accept-package-agreements 2>&1 | Out-Null
  if($LASTEXITCODE -eq 0){ Kayit sqlite winget KURULDU 'SQLite.SQLite' } else { Kayit sqlite winget HATA "exit $LASTEXITCODE" }
}

# --- 2) VS Code eklentileri ---
$code = Exe code
$liste = if($code){ (& $code --list-extensions 2>$null) -join "`n" } else { '' }
foreach($id in @('GitHub.copilot','GitHub.copilot-chat')){
  if(-not $code){ Kayit $id vscode HATA 'code yok'; continue }
  if($liste -match ('(?im)^' + [regex]::Escape($id) + '$')){ Kayit $id vscode ZATEN $id; continue }
  # 8 Kas: Copilot Chat VS Code'a yerlesik (0.71.0); pazar yerindeki eski surum 'cannot be downgraded' ile exit 1 veriyordu
  $vk = Split-Path (Split-Path $code)
  $yer = Get-ChildItem @((Join-Path $vk 'resources\app\extensions'), (Join-Path $vk '*\resources\app\extensions')) -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'copilot' }
  if($yer){ Kayit $id vscode ZATEN ("yerlesik: " + (($yer | ForEach-Object Name) -join ',')); continue }
  if($Deneme){ Kayit $id vscode DENEME "code --install-extension $id"; continue }
  & $code --install-extension $id --force 2>&1 | Out-Null
  if($LASTEXITCODE -eq 0){ Kayit $id vscode KURULDU $id } else { Kayit $id vscode HATA "exit $LASTEXITCODE" }
}

# --- 3) Blender eklentisi F2 (extensions.blender.org) ---
$bl = Get-ChildItem 'C:\Program Files\Blender Foundation\*\blender.exe' -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1
if(-not $bl){ Kayit f2 blender HATA 'blender.exe yok' }
elseif($Deneme){ Kayit f2 blender DENEME "$($bl.FullName) --command extension install f2 --sync --enable" }
else {
  & $bl.FullName --online-mode --command extension install f2 --sync --enable 2>&1 | Out-File -FilePath (Join-Path $env:TEMP 'blender-f2.log') -Encoding utf8
  if($LASTEXITCODE -eq 0){ Kayit f2 blender KURULDU 'f2 (enable)' } else { Kayit f2 blender HATA "exit $LASTEXITCODE, ayrinti: $env:TEMP\blender-f2.log" }
}

# --- 4) CUDA Toolkit (Omer EVET, ~3 GB indirme) ---
if(Exe nvcc){ Kayit cuda winget ZATEN (Exe nvcc) }
elseif($Deneme){ Kayit cuda winget DENEME 'winget install Nvidia.CUDA (~3 GB, UAC onayi)' }
else {
  & winget.exe install --id Nvidia.CUDA -e --accept-source-agreements --accept-package-agreements 2>&1 | Out-Null
  if($LASTEXITCODE -eq 0){ Kayit cuda winget KURULDU 'Nvidia.CUDA (yeni terminalde nvcc)' } else { Kayit cuda winget HATA "exit $LASTEXITCODE" }
}

# --- 5) MegaTTS3 (Omer EVET): kod + py3.10 venv + HF agirliklari (3,98 GiB) ---
$mt = Join-Path $kok 'ses\MegaTTS3'
$uv = Exe uv
$git = Exe git
if(Test-Path (Join-Path $mt 'checkpoints\diffusion_transformer')){ Kayit megatts3 klon+hf ZATEN $mt }
elseif($Deneme){ Kayit megatts3 klon+hf DENEME "git clone bytedance/MegaTTS3 -> $mt; uv venv py3.10; requirements; hf download ByteDance/MegaTTS3 -> checkpoints (3,98 GiB)" }
elseif(-not ($uv -and $git)){ Kayit megatts3 klon+hf HATA 'uv/git yok' }
else {
  $mlog = Join-Path $env:TEMP 'megatts3-kur.log'
  New-Item -ItemType Directory -Force -Path (Split-Path $mt) | Out-Null
  if(-not (Test-Path (Join-Path $mt '.git'))){ & $git clone --depth 1 https://github.com/bytedance/MegaTTS3.git $mt 2>&1 | Out-File $mlog -Encoding utf8 }
  Push-Location $mt
  & $uv venv --python 3.10 .venv 2>&1 | Out-File $mlog -Append -Encoding utf8
  $vpy = Join-Path $mt '.venv\Scripts\python.exe'
  $req = Get-Content requirements.txt | Where-Object { $_ -notmatch '^(WeTextProcessing|pynini)' -and $_.Trim() }
  $req | Set-Content (Join-Path $env:TEMP 'megatts3-req.txt') -Encoding ascii
  & $uv pip install --python $vpy -r (Join-Path $env:TEMP 'megatts3-req.txt') 2>&1 | Out-File $mlog -Append -Encoding utf8
  $okReq = ($LASTEXITCODE -eq 0)
  & $uv pip install --python $vpy WeTextProcessing 2>&1 | Out-File $mlog -Append -Encoding utf8
  $okWtp = ($LASTEXITCODE -eq 0)
  & $uv tool run --from huggingface_hub hf download ByteDance/MegaTTS3 --local-dir (Join-Path $mt 'checkpoints') 2>&1 | Out-File $mlog -Append -Encoding utf8
  $okHf = (Test-Path (Join-Path $mt 'checkpoints\diffusion_transformer'))
  $cuda = (& $vpy -c "import torch;print(torch.cuda.is_available())" 2>$null)
  Pop-Location
  $not = "req=$okReq WeTextProcessing=$okWtp agirlik=$okHf torch.cuda=$cuda log=$mlog"
  if($okReq -and $okHf){ Kayit megatts3 klon+hf KURULDU $not } else { Kayit megatts3 klon+hf HATA $not }
}

# --- 6) DaVinci Resolve: winget paketi yok; kayit formlu resmi indirme ---
if(Test-Path 'C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'){ Kayit davinci elle ZATEN 'Resolve.exe' }
else { Kayit davinci elle OMER 'blackmagicdesign.com/products/davinciresolve -> DaVinci Resolve (ucretsiz) Windows indir, kurulumu calistir' }

$say = Import-Csv $log -Delimiter "`t" | Group-Object durum | ForEach-Object { "$($_.Name)=$($_.Count)" }
Write-Host ("OZET: " + ($say -join ' '))
if(($say -join ' ') -match 'HATA'){ exit 1 }
