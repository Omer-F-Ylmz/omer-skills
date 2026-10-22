# RAM-1 ölçüm — yeni açılmış boşta CC oturumu (90 sn sonra claude.exe ağacı)

| etiket | zaman | süreç | çalışma kümesi GB | özel GB | aracı adayları | mcp list sn medyan (3 koşu) | bağlı | bağlanamayan |
|---|---|---|---|---|---|---|---|---|
| once | 2026-10-01 16:06 | 83 | 2.94 | 4.03 | node×19 cmd×15 conhost×19 uv×5 uvx×4 python×12 dotnet×2 | 14.9 (15.9 / 14.1 / 14.9) | 24 | - |
| sonra | 2026-10-01 16:13 | 59 | 2.19 | 3.16 | node×14 cmd×5 conhost×19 python×12 dotnet×2 | 10.8 (11.7 / 10.4 / 10.8) | 24 | - |

## 2026-10-22 — ajan süreç ağaçları (RAM %78–83, 31.7 GB; `.kos/kopru/ram_agac.py`)

| pid | başl. | süreç | MB | en büyükler (MB) |
|---|---|---|---|---|
| 61872 (site+video profili) | 10:35 | 32 | 2008 | node×9=1223 (premiere-pro 172, chrome-devtools npx+node 302, playwright 124, rea npx+node 443, ruflo 92) · claude 408 · chrome-headless×4 204 |
| 38408 (site profili) | 10:28 | 22 | 1474 | node×6=961 (chrome-devtools 302, playwright 122, rea 443, ruflo 92) · claude 386 |
| 31012 / 36840 (boş MCP) | 10:36 / 10:42 | 5 / 7 | 454 / 410 | claude ≈ 350–420 |

Diğer büyük tüketiciler: Claude Desktop 4.2 GB (109 süreç) · mcp-proxy (22 paylaşımlı sunucu) 2.6 GB / 67 süreç · headroom python 1.75 GB · Opera 3.4 GB · Discord 1.2 GB · Defender 0.8 GB.

**Bulgu:** ajan başına maliyet MCP profilinden gelir (boş MCP ≈ 0.45 GB, site profili 1.5–2.0 GB). Stdio rea+chrome-devtools+playwright ≈ 0.9–1.1 GB/ajan.
**Denendi, geri alındı:** `rea`yı paylaşımlı proxy'ye taşıma (tools/list eşit: 207 = 207) → proxy 2.6 → 4.7 GB, 67 → 93 süreç (rea proxy'de ≈ +2 GB). Ajan başı −0.44 GB kazanç bunu ancak ≥5 eşzamanlı site ajanında karşılar → uygulanmadı.
**Yetim taraması:** ajan MCP/chrome/blender kalıntısı yok; tek aday headroom `multiprocessing.spawn` çocuğu (pid 57180, 424 MB, ata ölü, 11 sa) — Ömer onayıyla kapatılabilir (kapatılmadı).
**Kuyruk (ajan_sira.py):** `tahmin_mb` (450 + ajan başı stdio MCP + render 1500) ve `ram_izin`: başlatma sonrası tahmini RAM% eşiği aşıyorsa ağır iş bekler (log `RAM BEKLE`), hafif iş sıradan geçer; RAM eşik−10'un altındaysa tavan +3. Çalışan kuyruk yöneticisi yeniden başlatılana dek eski kodla koşar.
**Öneri (Ömer onayı):** chrome-devtools ve rea npx sarmalayıcısı (≈160 MB/ajan) ecc eklenti .mcp.json'unda; gereksiz başlangıç: Epic Games Launcher 0.7 GB, Discord 1.2 GB.

**Node heap (ram-1 son):** `baslat_argv` ajan env`ine `NODE_OPTIONS=--max-old-space-size=2048` ekler (var olan tavan korunur); test `test_node_heap_tavani`.
**Önce/sonra (model, canlı A/B yok — ücretli ajan tavanı):** 6 site-profili iş ≈ 6×1.5–2.0 = 9–12 GB (+Desktop 4.2, proxy 2.6, headroom 1.75, Opera 3.4 → %78 tabanında 31.7 GB`ta tepe ≈ %100+). Eski: sabit tavan 6 → %88 kopma. Yeni: aday başı tahmin kapısı (eşik %85) ağır işi bekletir, hafifler (≈0.45 GB) paralel; boş RAM`de tavan +3. Canlı tepe ölçümü yönetici yeniden başlatılınca yapılmalı.
