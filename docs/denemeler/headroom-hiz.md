# Deneme: headroom-hiz

22 K4: `headroom perf --hours 72` ön-işlem p95 2135 ms'nin ~%95'i `compression_first_stage` (p95 2032 ms, maks 30.2 s); okuma/kopya/kuyruk ihmal edilir. Günlükte 348 "Kompress slow compress backend=onnx" satırı: inference p50 1.65 s, p95 5.9 s, maks 14.2 s. 24 çekirdek → `--compression-max-workers` varsayılanı 24, `--anthropic-pre-upstream-concurrency` 8; iş parçacığı sıkışması değil, ONNX çıkarımı. Ayar adayı: `--disable-kompress` (yapısal sıkıştırma kalır, yalnız ML metin sıkıştırması kapanır).

## Hipotez
Kompress kapalı ikinci örnek, 4 okuma görevinde süreyi kısaltır; girdi token ve kalite bugünkü Headroom'dan kötüleşmez.

## Metrik
süre sn · girdi token · sıcak $ · başarı · Jev kalite.

## Bütçe
`video dene headroom-hiz --gorevler okuma --tavan 8 --istek-tavan 20`: temel kol headroom-okuma koşusundan (.kos önbelleği, aynı hash), yeni kol 4 görev × 2 koşu = 8 claude -p.

## Proxy
`headroom.exe proxy --port 8794 --no-http2 --no-telemetry --disable-kompress` (runtime venv, v0.37, arka planda). Ana örnek değişmez. Bitince durdurulur, 8794 boş mu bakılır.

## Başarı eşiği
girdi token −%0 (Headroom'a göre) ve kalite kapısı (18).

## Görevler
- 1-basarisiz-test
- 2-json-alan
- 3-hatali-diff
- 4-log-zincir

## Kollar
- headroom-mevcut: temel · env ANTHROPIC_BASE_URL=http://127.0.0.1:6767
- headroom-hiz: env ANTHROPIC_BASE_URL=http://127.0.0.1:8794
