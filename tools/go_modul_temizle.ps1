# Go modul onbellegi (~22,6 GB) — Omer onayladi (6 Kas 02:11). Bir sonraki derlemede gerekirse yeniden indirilir.
$once = [math]::Round((Get-PSDrive C).Free/1GB,1); "Once bos: $once GB"
if (Get-Command go -ErrorAction SilentlyContinue) { go clean -modcache; "go modul onbellegi temizlendi" } else { "go bulunamadi" }
$sonra = [math]::Round((Get-PSDrive C).Free/1GB,1); "Sonra bos: $sonra GB  (kazanc $([math]::Round($sonra-$once,1)) GB)"
Read-Host "Bitti, Enter'a bas"
