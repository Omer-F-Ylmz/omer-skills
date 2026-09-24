---
iddia: settings.json'daki PowerShell eşleyicili `rtk hook claude` kancası etkisiz ve zararsız; her PowerShell çağrısında boş çıktı, kod 0, stderr boş, medyan ~107 ms
kaynak: FIX-6 K4 ölçümü (10 çağrı, PreToolUse PowerShell yükü)
guven: yüksek
dogrulama: echo '<PowerShell PreToolUse JSON>' | rtk hook claude  → 0 bayt; aynı yük Bash ile updatedInput döner
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: rtk, kanca, powershell, olcum
---
RTK PowerShell desteklemiyor; kanca kurulu kalır (omer-kurallar:22), hiçbir girdiyi yeniden yazmaz. Tek maliyeti süreç başlatma (92-140 ms, Bash eşleyicili rtk kancasıyla aynı mertebe). RTK PowerShell desteği gelirse kanca kendiliğinden devreye girer.
