# Deneme: caveman-proxy

video ? · 15 · 20a: düzenek hazır, koşulmaz (caveman kurulumu ONAY bekler: docs/kurulumlar/bekleyen/caveman.md)

## Hipotez
caveman proxy girdi tokenını Headroom'dan belirgin fazla azaltır, doğruluk düşmez (yazar: −%33.2 18/18; Headroom −%6.7 15/18); README: Headroom caveman'ın önünde çalışabilir.

## Metrik
girdi token (provider-reported) · sıcak koşu $ (karar) · soğuk koşu $ (bilgi) · görev başarısı (beklenen) · Jev kalite; okuma görev seti (gorevler-okuma, 4 görev).

## Bütçe
`video dene caveman-proxy --gorevler okuma --tavan 32 --istek-tavan 40`: 4 görev × 4 kol × 2 koşu = 32 claude -p (tavan), Jev ≤40.

## Geri alma
`caveman disable claude` + npm rm -g @caveman-ai/cli; Headroom ayarı değişmez.

## Başarı eşiği
girdi token −%15 (Headroom'a göre) ve kalite kapısı (18).

## Kollar
- dogrudan: env ANTHROPIC_BASE_URL=https://api.anthropic.com
- headroom: temel · env ANTHROPIC_BASE_URL=http://127.0.0.1:6767
- caveman: env ANTHROPIC_BASE_URL=https://api.anthropic.com · önek caveman claude --
- headroom-caveman: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 · önek caveman claude --

## Varsayım
`caveman claude -- <claude argv>` sarmalayıcı sözdizimi aday notundan (docs/kurulumlar/adaylar/caveman.md); kurulumdan sonra `caveman --help` ile doğrulanır, farklıysa yalnız `önek` satırı değişir. Zincirde caveman'ın Headroom'a yönlenmesi ANTHROPIC_BASE_URL'yi okumasına bağlıdır; okumazsa headroom-caveman kolu doğrudan-caveman ile aynı girdi tokenını verir ve bu rapora yazılır.
