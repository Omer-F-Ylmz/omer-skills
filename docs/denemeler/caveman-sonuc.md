# Deneme sonucu: caveman

2026-09-23 · sonnet · 3 görev · claude -p 6 · Jev istek 6 · hook kapalı (JEV_SKILL_HOOK=0)
B kolu: A + --append-system-prompt (docs/denemeler/caveman-talimat.md)

## Kol ortalamaları
| kol | çıktı | girdi | süre sn | maliyet $ | kalite 0-3 |
|---|---|---|---|---|---|
| A | 831 | 94056 | 14.9 | 0.3178 | 2.97 |
| B | 659 | 96758 | 12.2 | 0.3424 | 2.75 |

## Görev başına (çıktı · kalite)
- 1-ozet: A 337 · 2.98 → B 284 · 2.59
- 2-fonksiyon: A 2003 · 2.94 → B 1519 · 2.92
- 3-kapanis: A 152 · 2.98 → B 173 · 2.75

## Karar
RED(ölçüm): çıktı −%20.7 (eşik %30) · kalite düşüşü 0.21 (eşik 0.3) · maliyet −%-7.7 (eşik %3)
