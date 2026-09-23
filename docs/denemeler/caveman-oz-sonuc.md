# Deneme sonucu: caveman-oz

2026-09-23 · sonnet · 6 görev · claude -p 18 (A 2 tekrar + B 1) · Jev istek 18 · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet $4.6490 (bu koşuda yeni çağrı 18)
B kolu: A + --append-system-prompt (docs/uyarlamalar/caveman-oz-talimat.md, frontmatter hariç) · gürültü (A1-A2 kalite farkı ort.) 0.03

## Kol ortalamaları
| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | maliyet $ |
|---|---|---|---|---|---|---|
| A | 0.92 | 2.92 | 481 | 94273 | 11.0 | 0.2232 |
| B | 0.83 | 2.91 | 651 | 94543 | 13.4 | 0.3284 |

## Görev başına
| görev | A başarı | B başarı | A kalite | B kalite | A çıktı | B çıktı |
|---|---|---|---|---|---|---|
| 1-ozet | 1/0 | 1 | 2.95/2.91 | 2.95 | 223/242 | 303 |
| 2-fonksiyon | 1/1 | 0 | 2.97/2.96 | 2.95 | 1448/1687 | 2363 |
| 3-kapanis | 1/1 | 1 | 2.97/2.98 | 2.98 | 183/209 | 183 |
| 4-kod-duzeltme | 1/1 | 1 | 2.95/2.93 | 2.89 | 462/486 | 573 |
| 5-turkce-soru | 1/1 | 1 | 2.96/2.99 | 2.99 | 301/417 | 342 |
| 6-talimat-izleme | 1/1 | 1 | 2.78/2.71 | 2.70 | 41/76 | 141 |

## Karar
RED(token, kalite): çıktı −%-35.2 (eşik %20) · kalite 2.92→2.91 (bant 0.10) · başarısı düşen görev: 2 · maliyet −%-47.1 (eşik %0)
