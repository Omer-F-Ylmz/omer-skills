# Yetim MCP sunucuları (FIX-6 K2) — KOŞULMAZ

## Teşhis (2026-09-24 14:05)
- 169 MCP ilişkili süreç: 46 canlı CC'ye, 90 canlı Desktop'a bağlı, **33 yetim** (ata zinciri ölü ebeveynde kopuyor).
- 33 yetimin tamamı `mcp-filesystem` + `mcp-git` ağacı: 12:40'ta 22, 13:04-13:05'te 11 (iki Desktop yeniden başlatması).
- Yetim kökleri 6 `node gecit.mjs` süreci (ebeveyni ölü): 12:40'ta 4, 13:04'te 2. Altında npx/cmd → server-filesystem ve uvx → uv → mcp-server-git → python.
- CC'nin başlattığı npx/uvx sunucularında yetim **0**: npx/uvx ara kabuğu tek başına yetim üretmiyor.

## Kök neden
`gecit.mjs` stdin EOF'u dinlemiyordu. Desktop kapanınca geçidin stdin'i kapanıyor ama geçit
alt sunucunun stdin'ini açık tutuyordu; alt sunucu EOF görmediği için kapanmıyor, geçit de
yalnız alt sunucu kapanınca çıkıyordu. Windows ebeveyn ölünce torunları öldürmez; libuv'un
kill-on-close job nesnesi yalnız doğrudan çocuğu kapsar (cmd/npx/uvx arasındaki torunlar dışarıda).
Aynı kusur 22 Eyl'deki 48 sızmış gecit.mjs'in de nedeni.

## Kalıcı çözüm (uygulandı, 13a9d52)
Geçit stdin kapanınca alt sunucuya EOF iletir, 5 sn içinde kapanmazsa ağacı `taskkill /T /F` ile kapatır.
Test: `FIX-6 · stdin kapaninca gecit alt sunucusuyla birlikte kapanir`. Desktop yeniden başlatılınca
yeni geçitler bu kodla açılır. 21c'deki "npx → doğrudan node" önerisi yetimleşme için gerekmiyor:
CC tarafında npx/uvx ile başlatılan sunucularda yetim yok.

## Mevcut yetimleri temizleme (KOŞULMAZ, kullanıcı onayıyla)
Yalnız ebeveyni ölü olan VE komut satırı MCP listesindeki bir ada uyan kökleri ağacıyla kapatır.
Ebeveyni yaşayan süreçlere (canlı CC/Desktop çocukları) dokunmaz. Önce `-Kuru` ile listele.

```powershell
param([switch]$Kuru)
$ad = 'gecit\.mjs|mcp-server-git|server-filesystem|server-memory|server-sequential-thinking|mcp-server-time|mcp-server-fetch|headroom.*mcp'
$hepsi = Get-CimInstance Win32_Process
$canli = @{}; $hepsi | ForEach-Object { $canli[[int]$_.ProcessId] = $_ }
$kokler = $hepsi | Where-Object {
  $_.CommandLine -match $ad -and (
    -not $canli[[int]$_.ParentProcessId] -or
    $canli[[int]$_.ParentProcessId].CreationDate -gt $_.CreationDate)   # pid yeniden kullanımı = ölü ebeveyn
}
foreach ($k in $kokler) {
  "{0} {1} {2}" -f $k.ProcessId, $k.CreationDate.ToString('MM-dd HH:mm'), $k.CommandLine
  if (-not $Kuru) { taskkill /T /F /PID $k.ProcessId | Out-Null }
}
"kok: $(@($kokler).Count)"
```

Geri alma: yok (kapatılan yetimlerin sahibi yok; Desktop yeniden başlatılınca gerekenleri yeniden açar).
Doğrulama: betik sonrası teşhis sayımı yetim 0; canlı CC ve Desktop altındaki sayılar değişmemeli.
