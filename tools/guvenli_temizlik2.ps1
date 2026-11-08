# GUVENLI TEMIZLIK 2 — yalniz gelecekte de ise yaramayacak, kesin cop. Kod/arac/model kaybi yok.
$once = [math]::Round((Get-PSDrive C).Free/1GB,1); "Once bos: $once GB"
# 1) Yarida kalmis HuggingFace indirmesi (8,58 GB .incomplete, 35 saat once, bitmemis)
Get-ChildItem 'C:\AI\_indir\.cache\huggingface\download' -Recurse -Filter *.incomplete -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
"Yarim kalan indirme silindi"
# 2) Gecici klasorde 24 saatten eski olanlar (video indirme artiklari ~11 GB, .NET kurulum kalintisi 3,5 GB vb.); son 24 saattekilere dokunmaz
$sinir = (Get-Date).AddHours(-24)
Get-ChildItem $env:TEMP -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt $sinir } | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
"Temp (24 saatten eski) temizlendi"
$sonra = [math]::Round((Get-PSDrive C).Free/1GB,1); "Sonra bos: $sonra GB  (kazanc $([math]::Round($sonra-$once,1)) GB)"
Read-Host "Bitti, Enter'a bas"
