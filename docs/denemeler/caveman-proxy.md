# Deneme: caveman-proxy

video ? · 15 · bu dalgada koşulmaz (14b)

## Hipotez
caveman proxy girdi tokenını Headroom'dan belirgin fazla azaltır, doğruluk düşmez (yazar: −%33.2 18/18; Headroom −%6.7 15/18).

## Metrik
girdi token (provider-reported) ve doğruluk (bilinen-doğru cevap); Headroom'a karşı A/B, aynı görev seti.

## Bütçe
3 görev × (doğrudan · Headroom · caveman) ≤9 claude -p, ≤$3, Jev ≤12; kurulum T2 onayı + hemen `caveman telemetry off`; BSL-1.1 lisans notu (kendi kullanım serbest).

## Geri alma
`caveman disable claude` + npm rm -g @caveman-ai/cli; Headroom ayarı değişmez.

## Başarı eşiği
girdi token Headroom'a göre ≥%15 daha az ve doğruluk ≥ Headroom.

