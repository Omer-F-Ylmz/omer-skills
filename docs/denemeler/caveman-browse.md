# Deneme: caveman-browse

video ? · 15 · bu dalgada koşulmaz (14b)

## Hipotez
büyük tablolu sayfada playwright snapshot / pixeljury'ye göre ≥%50 daha az girdi token, doğru öğe bulma düşmez.

## Metrik
sayfa başına girdi token ve doğru öğe/değer bulma; playwright-cli snapshot ve pixeljury ekran testine karşı A/B.

## Bütçe
3 sayfa (büyük tablo · form · landing) × 3 kol ≤9 claude -p, ≤$2.

## Geri alma
npm rm -g @caveman-ai/cli; playwright/pixeljury ayarı değişmez.

## Başarı eşiği
büyük tabloda girdi token −%50 ve doğruluk ≥ playwright; formda kayıp ≤ playwright.

