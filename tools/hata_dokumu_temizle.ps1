# YONETICI gerekir: Windows hata dokumleri (LiveKernelReports ~4 GB) — yalniz eski cokme raporlari
$once = [math]::Round((Get-PSDrive C).Free/1GB,1)
Get-ChildItem 'C:\Windows\LiveKernelReports' -Recurse -File -Include *.dmp -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
$sonra = [math]::Round((Get-PSDrive C).Free/1GB,1); "Hata dokumleri: kazanc $([math]::Round($sonra-$once,1)) GB"
Read-Host "Bitti, Enter'a bas"
