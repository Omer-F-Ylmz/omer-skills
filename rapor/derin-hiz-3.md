# DERIN-HIZ-3 — TUR BITTI (kapı GEÇMEDİ, toplu koşu YOK: Ömer 16:35 emri)

Ölçüm: 2x-aQy730Ew (550 sn), RTX 4070 Ti, GPU başka işlerle paylaşımlı (süreler şişik). tools/asr_hiz3.py. Benzerlik = eski json'a; sıralı yolun kendisi 0,978–0,984.
| yol | süre | VRAM | kelime | benzerlik |
|---|---|---|---|---|
| sıralı fp16 beam5 (taban) | 85–168 sn | ~6 GB | 1549→1570 | 0,978–0,984 |
| sıralı int8_float16 | 141 sn | ~4,1 GB | →1523 | 0,971 |
| batch8 fp16 (varsayılan VAD) | 12 sn | – | →1377 | 0,934 |
| batch8 fp16 timestamps+VAD pad/sessizlik ayarı | 34 sn | ~6 GB | →1494 | 0,972 (sıralıya 0,960) |
| batch8 int8_float16 | 33 sn | ~4,8 GB | →1478 | 0,965 |
- Batched hep %3–5 kelime kaybeder; VAD/chunk ayarı kaybı kapatmadı → ≥0,98 yok. Altyazı-önce, Groq aynı-VAD, bulut havuzu, boru hattı kuyrukları ölçülmedi (tur bütçesi bitti).
- YT takılması: indirme değil (hls 8 sn); a.wav sonrası ASR'de duruyor, tek başına aynı wav bitiyor → `--es 2` + GPU çekişmesi şüphesi, kanıtlanmadı.
- Sonraki tur: (1) YouTube altyazı-önce ölçümü, (2) Groq'a VAD segmentli gönderim, (3) YT'yi `--es 1` + faulthandler ile izle.
