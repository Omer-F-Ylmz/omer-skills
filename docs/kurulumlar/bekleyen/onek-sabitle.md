# ONAY onek-sabitle (21a K1) — KOŞULMAZ, Ömer onaylar

Amaç: 17.565. token'daki önek kaymasının sebebini istek gövdesiyle kesinleştirmek (docs/olcumler/onek-kaymasi.md). Ücretli: 2 × claude -p (≈$0.62), en fazla 2.

```powershell
# 0) 8787 caveman'da (bekleyen/caveman-otobaslat.md) — Headroom'u boş porta aç
$port = 8791
Start-Process headroom -ArgumentList "proxy","--port",$port,"--log-messages" -WindowStyle Hidden
Start-Sleep 5
# 1) yalnız bu iki çağrı için yönlendir (global ayar değişmez)
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:$port"
1..2 | % { claude -p "ok de" --model sonnet --output-format json --max-budget-usd 1 < $null }
Remove-Item Env:ANTHROPIC_BASE_URL
# 2) iki isteğin sistem bloklarını karşılaştır
headroom inspect -p $port --last 2 --full --format json | Out-File "$env:TEMP\onek-21a.json" -Encoding utf8
# 3) proxy'yi kapat
Get-NetTCPConnection -LocalPort $port -State Listen | % { Stop-Process -Id $_.OwningProcess }
```
Beklenen: iki isteğin sistem metinleri yalnız Environment satırındaki scratchpad yolunda (oturum kimliği) ayrışır. Geri alma gerekmiyor; kalıcı hiçbir şey değişmiyor.
