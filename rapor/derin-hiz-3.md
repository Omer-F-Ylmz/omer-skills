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

## TUR 2 (28 Eki 17:20) — yol 1: YouTube altyazı-önce (kapı GEÇMEDİ)
- 12 YouTube linki (.kos/kopru/ogren/h3_altyazi.py): 6'sında altyazı yok (%50); olanlar eski large-v3'e: 0,962 / 0,943 (2 insan/oto temiz) ve 4'ü 0,01–0,03 (oto altyazı kayan-pencere tekrarı, ayrıştırma düzeltilmeden kullanılamaz). Süre 4–14 sn/link (ASR 85+ sn).
- Sonuç: altyazı tek başına ≥0,98 vermiyor; en iyi ihtimalle 0,94–0,96. Karar için Ömer: altyazı yalnız insan yazımı ise mi kullanılsın?
- Ölçülmedi (bütçe/bağlam doldu): Groq aynı-VAD, `--es 1`+faulthandler, bulut havuzu, kuyruklu boru hattı, 20 linklik set, GPU boşken taban. Toplu koşu başlatılmadı.

TUR 3 (28 18:05): KAPI DOGRULANAMADI. Hat kodlandi: tools/altyazi.py (VTT ayristirma+saglik: kelime/sn, kapsama; yalniz videonun kendi dili, 60 sn zaman asimi+1 yeniden deneme) + video_derin.py varsayilan batch8 fp16 VAD(500ms/pad400), 0 segmentte sirali yola dusus.
10 linkte ilk 4: altyazi yolu 24 sn (-o8hT175bHI benzerlik 0,960 = esik), digerleri ASR 34–58 sn, hata 0. 5. link 2x-aQy730Ew batched uretecte >8 dk asili (py-spy: generate_segment_batched; GPU %100, ~29 islem GPU'yu paylasiyor) -> durduruldu, 10/10 dogrulanmadi, link/komut %100 ve >=0,96 tum linklerde kanitlanmadi.
Sonraki: GPU'yu bos birakip ayni 10 linki tekrar kos; asili ASR'ye zaman asimi (alt surec) gerekebilir. Saat/link ~30–60 sn, VRAM ~6 GB.

TUR 4 (28 Eki 18:50): KAPI GECMEDI (10 link, GPU bos, hata 0, takilma 0). ASR link basina 180 sn zaman asimli alt surec (.kos/kopru/ogren/h3_kos.py); 0_3A0uAkBZ0 batch=4'te 180 sn'de asildi, batch=1 ile 60 sn'de bitti. Saat/link 20-68 sn (ort ~40), VRAM 2,0 -> ~2,5 GB (olcum anlik).
- Benzerlik >=0,96: 5/10 (-o8h 0,960, 18c3 0,966, 5G7 0,977, 5LL 0,966, a4r 0,972). Altinda: JfmA 0,959, 2x-a 0,943, 9Iti 0,888, 0i65 0,831, 0_3A 0,591 (sirali yol, 765/875 kelime). Link/komut ortusmesi 10/10 %100 (ayri olculdu, h3_karsi.py).
- Varsayilan yapilmadi; ortusme tamam ama 5 link benzerlikte esik altinda. Sonraki: dusenlerin kaynagini (altyazi mi ASR mi) json'a yaz, 0_3A/0i65/9Iti eski ciktisinin kendi referans kalitesini kontrol et.
