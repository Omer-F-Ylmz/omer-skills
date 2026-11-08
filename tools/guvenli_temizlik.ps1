# GUVENLI TEMIZLIK — Omer'in kendisi calistirir (Claude'un silme izni engellendi). Yalniz yeniden uretilebilen onbellek/gecici dosyalar.
$once = [math]::Round((Get-PSDrive C).Free/1GB,1); "Once bos: $once GB"
# 1) Go derleme onbellegi (~24 GB) - go her derlemede yeniden uretir
if (Get-Command go -ErrorAction SilentlyContinue) { go clean -cache; "go build cache temizlendi" }
# 2) uv onbelleginde hicbir ortamin kullanmadigi paketler (~ondalik GB-onlarca GB)
if (Get-Command uv -ErrorAction SilentlyContinue) { uv cache prune; "uv cache prune bitti" }
# 3) 24 saatten eski gecici dosya/klasorler (video indirme artiklari, kurulum kalintilari ~15 GB); son 24 saattekilere dokunmaz
$sinir = (Get-Date).AddHours(-24)
Get-ChildItem $env:TEMP -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt $sinir } | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
"Temp (24 saatten eski) temizlendi"
$sonra = [math]::Round((Get-PSDrive C).Free/1GB,1); "Sonra bos: $sonra GB  (kazanc $([math]::Round($sonra-$once,1)) GB)"
Read-Host "Bitti, Enter'a bas"
