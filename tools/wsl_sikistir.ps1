$ErrorActionPreference = 'Continue'
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}
$log = 'C:\Projeler\omer-skills\tools\wsl_sikistir.log'
function Yaz($m) { "$(Get-Date -Format 'HH:mm:ss') $m" | Tee-Object -FilePath $log -Append }
$diskler = @(Get-ChildItem "$env:LOCALAPPDATA\wsl\*\ext4.vhdx") + @(Get-Item "$env:LOCALAPPDATA\Docker\wsl\disk\docker_data.vhdx" -ErrorAction SilentlyContinue)
Yaz "C bos once: $([math]::Round((Get-PSDrive C).Free/1GB,1)) GB"
if (Get-Process 'Docker Desktop' -ErrorAction SilentlyContinue) { Yaz 'Docker Desktop acik, kapatilip tekrar deneyin'; exit }
wsl --shutdown
Start-Sleep 8
wsl --manage Ubuntu --set-sparse false --allow-unsafe | Out-Null
foreach ($d in $diskler) {
    $f = $d.FullName
    $tmp = "$env:TEMP\wsl_sikistir.txt"
    "select vdisk file=`"$f`"`r`nattach vdisk readonly`r`ncompact vdisk`r`ndetach vdisk`r`nexit" | Set-Content -Encoding ASCII $tmp
    Yaz "sikistiriliyor: $f"
    diskpart /s $tmp | Out-Null
    Yaz "bitti: $([math]::Round((Get-Item $f).Length/1GB,1)) GB"
}
wsl --manage Ubuntu --set-sparse true --allow-unsafe | Out-Null
Yaz "C bos sonra: $([math]::Round((Get-PSDrive C).Free/1GB,1)) GB"
Yaz 'TAMAM'
Start-Sleep 5
