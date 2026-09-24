# ONAY caveman-otobaslat (21a K0) — KOŞULMAZ, Ömer onaylar

## Bulgu (2026-09-24 03:05, salt-okur)
- 127.0.0.1:8787 dinleyen: `caveman-proxy.exe` PID 41352 · `C:\Users\pc\.caveman\bin\caveman-proxy.exe` (argümansız) · başlama 2026-09-24 02:15:55 (20b-devam K1 proxy denemesi).
- Üst süreç PID 45752 artık yok → süreç yetim kalmış. `~/.caveman/run/8787.json`: mode compress · owner **wrap** · started_at 23:15:55Z. 20b-devam kapanışındaki "proxy 48340 durduruldu, 8788 boş" yalnız 8788 kolunu kapattı; 8787 örneği ayakta kaldı.
- Otomatik başlatma kaydı **yok**: Başlangıç klasörleri (kullanıcı + ortak: yalnız Cloudflare WARP), HKCU/HKLM `...\CurrentVersion\Run` + RunOnce + WOW6432Node (caveman yok; `headroom-desktop.exe --autostart` önceden var), zamanlanmış görevler (cave/headroom/8787 eşleşmesi 0), Windows servisleri (0). Yeniden başlatmada geri gelmez; "hiçbir şey kendiliğinden devreye girmez" onayı bozulmamış, ama oturum sonunda kapanmamış bir süreç var.
- Trafik etkisi: CC'nin ANTHROPIC_BASE_URL'i 8787'yi göstermiyor (boolean kontrol); Headroom masaüstü 127.0.0.1:6767'de. CC trafiği caveman'dan geçmiyor.

## Çakışma riski
8787 Headroom'un varsayılan portu: `headroom proxy` (port verilmeden) bağlanamaz; `headroom inspect`/`perf` gibi `-p` varsayılanı 8787 olan komutlar caveman'a gider ("cave_gateway_error: Proxy path is not recognized" — 21a keşfinde görüldü). Headroom'u 8787'de başlatan bir tarif/araç yanlış proxy'ye bağlanır.

## Durdurma (yedekli, KOŞULMAZ)
```powershell
$run = "$env:USERPROFILE\.caveman\run"
$yedek = "C:\Projeler\omer-skills\docs\denemeler\.kos\caveman\run-yedek-21a"
New-Item -ItemType Directory -Force $yedek | Out-Null
Copy-Item "$run\8787.json" $yedek -Force
$p = Get-Process -Id 41352 -ErrorAction SilentlyContinue
if ($p -and $p.Path -like "*\.caveman\bin\caveman-proxy.exe") { Stop-Process -Id 41352 } else { "41352 artık caveman-proxy değil; dokunulmadı" }
Get-NetTCPConnection -LocalPort 8787 -State Listen -ErrorAction SilentlyContinue   # boş dönmeli
```

## Otomatik başlatmayı kapatma
Kapatılacak kayıt yok (bulgu: 0). İleride çıkarsa aynı denetim:
```powershell
Get-ScheduledTask | ? { ($_.Actions | % Execute) -match "(?i)caveman" } | % { Export-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath | Out-File "$yedek\$($_.TaskName).xml"; Disable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath }
```

## Geri alma
```powershell
Start-Process "$env:USERPROFILE\.caveman\bin\caveman-proxy.exe" -WindowStyle Hidden   # 8787'de yeniden dinler
Get-ChildItem $yedek -Filter *.xml | % { Register-ScheduledTask -Xml (Get-Content $_.FullName -Raw) -TaskName $_.BaseName }
```
Paket (`~/.caveman`, Go ikilileri, npm CLI) kurulu kalır (omer-kurallar:22).
