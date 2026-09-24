---
iddia: Headroom ön-işlem p95'inin ~%95'i Kompress ONNX çıkarımı; --disable-kompress hızlandırmaz, girdiyi +%33 artırır.
kaynak: headroom perf --hours 72 --format json, proxy.log Kompress slow satırları, docs/denemeler/headroom-hiz-sonuc.md (8 claude -p)
guven: orta
dogrulama: docs/olcumler/headroom-gelistir.md
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: token, headroom, rtk, olcum
---
Headroom ön-işlem p95'inin ~%95'i Kompress ONNX çıkarımı; --disable-kompress hızlandırmaz, girdiyi +%33 artırır.
- compression_first_stage p95 2032 ms / maks 30.2 s; inference p95 5.9 s.
- 24 çekirdek: worker ve concurrency varsayılanları darboğaz değil.
- 30 s uçları 67–94k tokluk ardışık patlamalarda.
