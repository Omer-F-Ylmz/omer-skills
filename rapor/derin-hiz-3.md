# DERIN-HIZ-3 — TUR BITTI (kapı GEÇMEDİ, toplu koşu başlatılmadı)

- Batched large-v3 beam5 (tools/asr_hiz3.py, 2x-aQy730Ew 550 sn): sıralı 85 sn → batch8 12 sn, ama kelime 1549→1377, benzerlik 0,934 (sıralı yol 0,978). Zaman damgalı (without_timestamps=False) batch8: 29 sn, 0,972. İkisi de <0,98.
- Taban: sıralı large-v3 beam5 yeniden koşusu 5 IG linkte eskiyle 1,000 (deterministik); YT 2x-aQy730Ew tek başına 0,978 (eski json başka sürümle üretilmiş olabilir).
- YouTube takılması: indirme değil (yt-dlp hls 8 sn'de indi). Boru hattında 5 YT linki a.wav üretildikten sonra ASR'de duruyor (kare klasörü yok); tek başına aynı wav 85 sn'de bitti → eş zamanlı --es 2 + ASR_KILIT/GPU çekişmesi şüpheli, kök neden KANITLANMADI. Zaman aşımı/yeniden deneme eklenmedi.
- Groq'u VAD segmentleriyle besleme ölçülmedi (20 istek/dk kotası uzun videoda uygulanamaz görünüyor).
- 5 IG linki sıralı yolda koştu (h3seq); karşılaştırma YT'ler bitmediği için 5 link üzerinden. RAM %90,6 idi.
- Sonraki adım: --es 1 ile YT'yi koş, takılma yerini py-spy/faulthandler ile bul; batched yol kapıyı geçmediği için hız kazancı için kaliteden ödün gerekir (Ömer kararı).
