# ONAY onek-sabitle (21b) — KOŞULMAZ, Ömer onaylar

> 21c: REDDEDİLDİ (omer-kurallar:22, kurulu araç kapatılmaz). Kök neden: istem bloğun önünde, bkz. docs/olcumler/onek-kaymasi.md "21c".

Teşhis (docs/olcumler/onek-kaymasi.md, 21b): tools + system iki oturumda aynı; önbellek 17.565'te (system sonu) duruyor. Sonraki ~58.6k token (gitStatus + SessionStart çıktısı + skill/ajan/MCP listeleri) tek blok ve her oturumda değişiyor (gitStatus, claude-mem dakika damgası, MCP bağlanma yarışı). CC'de bunu sabitleyen bir ayar yok. Kaldıraç bloğu küçültmek.

Öneri: bu repoda kullanılmayan 6 eklentiyi **yalnız bu projede** kapatmak (`.claude/settings.local.json` → `enabledPlugins: false`). Global `~/.claude/settings.json`'a dokunulmaz. Beklenen: oturum başına ~15k token daha az yeniden yazım, 78 oturum/gün ile ≈ 1.2M token/gün.
Liste Ömer'in kararı; başka eklenti eklenebilir ya da çıkarılabilir.

## Uygula (PowerShell 5.1)
```powershell
$proje = "C:\Projeler\omer-skills\.claude\settings.local.json"
$kapat = "dotnet-test","dotnet-msbuild","phoenix-prd-pipeline","phoenix-security-review","taste-skill","example-skills"
$glob = Get-Content "$HOME\.claude\settings.json" -Raw | ConvertFrom-Json
$anahtarlar = $glob.enabledPlugins.PSObject.Properties.Name | ? { $kapat -contains ($_ -split "@")[0] }
if (Test-Path $proje) { Copy-Item $proje "$proje.onek-yedek" -Force; $p = Get-Content $proje -Raw | ConvertFrom-Json } else { $p = [pscustomobject]@{} }
if (-not $p.enabledPlugins) { $p | Add-Member enabledPlugins ([pscustomobject]@{}) -Force }
$anahtarlar | % { $p.enabledPlugins | Add-Member $_ $false -Force }
$p | ConvertTo-Json -Depth 100 | Set-Content $proje -Encoding utf8
"kapatildi: $($anahtarlar -join ', ')"
```

## Geri al
```powershell
$proje = "C:\Projeler\omer-skills\.claude\settings.local.json"
if (Test-Path "$proje.onek-yedek") { Move-Item "$proje.onek-yedek" $proje -Force } else { Remove-Item $proje }
```

## Doğrulama (K3) — uygulamadan sonra, en fazla 2 × claude -p (≈$0.62)
Referans (21a, uygulama öncesi): ilk istek cache_creation 76.167 / 77.444, cache_read 17.565.
```powershell
cd C:\Projeler\omer-skills
1..2 | % { claude -p "ok de" --model sonnet --output-format json --max-budget-usd 0.5 < $null | ConvertFrom-Json | % { "creation=$($_.usage.cache_creation_input_tokens) read=$($_.usage.cache_read_input_tokens) cost=$($_.total_cost_usd)" } }
```
Beklenen: cache_creation ≈ 61k (≈ −15k), cache_read 17.565 değişmez. Düşüş < 10k ise eklentilerin skill/ajan payı tahminden küçük demektir; geri al ve raporla.
