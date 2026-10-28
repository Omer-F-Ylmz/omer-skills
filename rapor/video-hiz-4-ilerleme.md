# VIDEO-HIZ-4 ilerleme (28 Eki 19:3x–)
- Bulgu 1: video_derin.py'de zaman günlüğü (derin-zaman.tsv) + DL_SEM(8)/CPU_SEM(4) + OCR da GPU_KILIT'te (ASR ile sıralı, nefes) eklendi.
- Bulgu 2 (12 shorts, es6): taban 140–150 video/sa; GPU baştan %64 dolu (başka işler), ASR GPU adımı medyan 11 sn/short (çekişme), OCR 7–12 sn/link.
- Bulgu 3: altyazı yolu shorts'ta referansa 0,60–0,95 → yalnız >900 sn videoda (VD_ALT_MIN).
- Bulgu 4: batched ASR shorts'ta 0,85–0,97, sıralı 1,00 → batched yalnız >120 sn ses (VD_TOPLU_MIN).
- Bulgu 5: 3/11 örnek çok-ses-izli (YouTube dublaj) video; referans izi rastgele (wa=en kötü iz) → benzerlik anlamsız (EKd, F2u, F86); indir artık -S lang,+abr ile en iyi-dil izi.
- Bulgu 6: kare açıklama Gemini kotası dolu, yerel kapalı → 0 çıktı; ücretsiz görsel havuz (havuz_aciklama, ≤3 istek/link) eklendi.
