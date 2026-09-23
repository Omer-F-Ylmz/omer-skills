# Deneme sonucu: caveman-learn

2026-09-24 · `video koru --agsiz -- caveman learn [--all]` · claude -p 0 · $0 · parmak izi eşit (89 ad)

## Salt-okur mu
Evet (statik tarama, ad düzeyi): JS'teki `learn` yalnız `caveman-proxy learn scan|report` çağırır; `learn-tui.js`'te ağ/dosya yazma yok. `caveman-proxy.exe` dizgilerinde ağ hedefi yalnız sağlayıcı adresleri (api.anthropic.com vb.), caveman bulut adresi yok. Okur: `~/.claude` transkriptleri, `~/.claude.json`, `~/.codex`. Yazar: yalnız `~/.caveman/{caveman.db, ccr.db}` + `~/.caveman/reports/caveman-learn.html`. `learn implement` dosya düzenler (her düzenlemede sorar), koşulmadı. Koşu API anahtarsız + ölü BASE_URL ile.

## İlk 5 kalem (1364 oturum, 30 gün, tahmini)
| # | kalem | tahmini kayıp | bizde kapsanıyor mu |
|---|---|---|---|
| 1 | ajan yapılandırması her tura ~2421 token (yük taşıyan) | ~4.3M token/gün | kısmen: departman müdürleri + description token bütçesi (`video departman`); CLAUDE.md sadeliği elle |
| 2 | 60 skill her tura ~1262 token, kullanım yok | ~2.3M token/gün | hayır: kullanım sayacı yok; omer-kurallar:22 kaldırmayı yasaklar → uyarlama: docs/uyarlamalar/skill-kullanim-sayaci.md |
| 3 | ~38.8k token'lık blok 16 oturumda yeniden kuruluyor | ~21k token/gün | kısmen: dalga.md ≤30 satır + /clear; tarif yapıştırmaları kalıcı özete inmiyor |
| 4 | ~38.7k token'lık blok 16 oturumda | ~21k token/gün | kısmen (3 ile aynı) |
| 5 | ~38.8k token'lık blok 9 oturumda | ~12k token/gün | kısmen (3 ile aynı) |

İlk tur istemi ~59k (sağlayıcı sayımı, medyan).

## Karar
RED(eşik): kapsanmayan tek kalem (2) oturum girdisinin ~%2.1'i (1262/59k; eşik %5). Fikir UYARLA'ya gider, araç kurulu kalır.
