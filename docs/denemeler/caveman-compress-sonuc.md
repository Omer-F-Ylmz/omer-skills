# Deneme sonucu: caveman-compress

2026-09-24 · claude -p 0 · Jev istek 0 · kaynak C:/Users/pc/Desktop/smart/Divisima.Solution/CLAUDE.md (yalnız kopya: docs/denemeler/.kos/caveman-compress/)

## Ölçüm
- Komut: `video koru -- caveman compress < kopya > CLAUDE.out` (1.3.4'te compress yalnız stdin→stdout; dosya argümanı okunmaz, `## Komut {kopya}` biçimi uygulanamaz)
- caveman raporu: content_type text · token 10981 → 10981 · ratio 0
- Çıktı gövdesi girdiyle bayt bayt aynı (+ tek satır JSON metrik) → 94/94 kural korunur, Jev'e sorulmadı
- Hedef sha önce/sonra: c6a4d386…2ce13 = c6a4d386…2ce13; parmak izi eşit (89 ad)

## Neden
Engine düz yazı/markdown için kayıplı sıkıştırma seçmez (15 sıkıştırıcı JSON · log · kod · diff · arama · HTML · tablo · yapılandırma · şema · TOON · tekrar · terminal çıktısı); küçülmeyen sonuç özgün bayta döner.

## Karar
RED(token): −%0 (eşik %30) · korunmayan kural 0
