# Deneme: caveman-proxy

video ? · 15 · bu dalgada koşulmaz (14b)

## Hipotez
caveman proxy girdi tokenını Headroom'dan belirgin fazla azaltır, doğruluk düşmez (yazar: −%33.2 18/18; Headroom −%6.7 15/18); README: Headroom caveman'ın önünde çalışabilir.

## Metrik
girdi token (provider-reported) ve doğruluk (bilinen-doğru cevap); 4 kol aynı görev seti: doğrudan · Headroom · caveman · Headroom+caveman.

## Bütçe
3 görev × 4 kol (doğrudan · Headroom · caveman · Headroom+caveman) ≤12 claude -p, ≤$3, Jev ≤12; kurulum T2 onayı + hemen `caveman telemetry off`; BSL-1.1 lisans notu (kendi kullanım serbest).

## Geri alma
`caveman disable claude` + npm rm -g @caveman-ai/cli; Headroom ayarı değişmez.

## Başarı eşiği
caveman ya da Headroom+caveman girdi tokenı Headroom'a göre ≥%15 daha az ve doğruluk ≥ Headroom.

