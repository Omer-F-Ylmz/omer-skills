# YONETICI-KUR (8 Kas): tek UAC onayiyla winget onarimi + yonetici isteyen kalemler. Silme yok.
# Calistirma: Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File C:\Projeler\omer-skills\tools\yonetici_kur.ps1'
$ErrorActionPreference = 'Continue'
$log = 'C:\Projeler\omer-skills\rapor\yonetici-kur-sonuc.tsv'
"kalem`tdurum`tnot" | Out-File $log -Encoding utf8
function Kayit($k,$d,$n){ "$k`t$d`t$n" | Out-File $log -Append -Encoding utf8; Write-Host "$k  $d  $n" }
function Zamanli($ad, [string[]]$arg, $dk){
  $p = Start-Process winget.exe -ArgumentList $arg -PassThru -NoNewWindow
  if(-not $p.WaitForExit($dk*60000)){ $p.Kill(); Kayit $ad 'ZAMAN-ASIMI' "$dk dk"; return -999 }
  return $p.ExitCode
}
$e = Zamanli 'winget-source-reset' @('source','reset','--force','--disable-interactivity') 5;  Kayit 'winget-source-reset' $(if($e -eq 0){'TAMAM'}else{'HATA'}) "exit $e"
$e = Zamanli 'winget-source-update' @('source','update','--disable-interactivity') 10;     Kayit 'winget-source-update' $(if($e -eq 0){'TAMAM'}else{'HATA'}) "exit $e"
$t0 = Get-Date; $e = Zamanli 'winget-show-test' @('show','--id','Helm.Helm','-e','--source','winget','--accept-source-agreements','--disable-interactivity') 3
Kayit 'winget-show-test' $(if($e -eq 0){'TAMAM'}else{'HATA'}) ("exit $e, " + [int]((Get-Date)-$t0).TotalSeconds + " sn")
foreach($id in @('Microsoft.VCRedist.2015+.x64','PostgreSQL.PostgreSQL.17','Nvidia.CUDA')){
  $e = Zamanli $id @('install','--id',$id,'-e','--source','winget','--silent','--accept-package-agreements','--accept-source-agreements','--disable-interactivity') 40
  Kayit $id $(if($e -eq 0){'KURULDU'}else{'HATA'}) "exit $e"
}
Write-Host "Bitti. Sonuc: $log  (pencereyi kapatabilirsin)"
