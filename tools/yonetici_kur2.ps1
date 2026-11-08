# YONETICI-KUR-2 (8 Kas): winget'i ATLAR. Kurucular winget-pkgs manifestindeki URL'den indirildi ve SHA256 manifestle dogrulandi (tools\manifest_indir.py).
# Burada yalniz imza (Authenticode) bir kez daha kontrol edilir ve sessiz kurulur. Tek UAC. Silme yok.
# Calistirma: Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File C:\Projeler\omer-skills\tools\yonetici_kur2.ps1'
$ErrorActionPreference = 'Continue'
$ind = Join-Path $env:USERPROFILE ('Desktop\Claude ile yap' + [char]0x0131 + 'lanlar\araclar\_yonetici_indir')
$log = 'C:\Projeler\omer-skills\rapor\yonetici-kur-sonuc.tsv'
"kalem`tdurum`tnot" | Out-File $log -Encoding utf8
function Kayit($k,$d,$n){ "$k`t$d`t$n" | Out-File $log -Append -Encoding utf8; Write-Host "$k  $d  $n" }
$plan = Get-Content (Join-Path $ind 'plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$varsayilan = @{ 'Microsoft.VCRedist.2015+.x64' = '/install /quiet /norestart'; 'Nvidia.CUDA' = '-s' }
foreach($k in $plan){
  $imza = Get-AuthenticodeSignature $k.dosya
  if($imza.Status -ne 'Valid'){ Kayit $k.id 'ATLANDI' ("imza " + $imza.Status); continue }
  $sw = if($k.sessiz){ $k.sessiz } else { $varsayilan[$k.id] }
  Write-Host ("kuruluyor: {0} {1} ({2}) imza: {3}" -f $k.id, $k.surum, $sw, $imza.SignerCertificate.Subject)
  $p = Start-Process -FilePath $k.dosya -ArgumentList $sw -PassThru
  $null = $p.Handle
  if(-not $p.WaitForExit(60*60000)){ Kayit $k.id 'ZAMAN-ASIMI' '60 dk'; continue }
  $e = $p.ExitCode
  Kayit $k.id $(if($e -eq 0 -or $e -eq 3010 -or $e -eq 1638){'KURULDU'}else{'HATA'}) ("surum $($k.surum) exit $e" + $(if($e -eq 3010){' (yeniden baslatma ister)'}elseif($e -eq 1638){' (zaten daha yeni surum var)'}else{''}))
}
Write-Host "Bitti. Sonuc: $log  (pencereyi kapatabilirsin)"
