# VİDEO-YENİ-1 — H3 (kral) vs Pika H3 Flex (01 Kas 2026)
Sabit: aynı İngilizce prompt, seed 42, 768x448, 97 kare, 24 fps, aynı VAE (fp16) + tiled decode, RAM tavanı %95.
| | H3 + turbo 4 adım | Pika H3 Flex 6 adım |
|---|---|---|
| Süre | 205 sn | 195 sn |
| Tepe RAM / VRAM | %92,6 / 7,2 GB | %86,6 / 6,6 GB |
| Ses (ortalama / tepe) | -44,6 / -20,6 dB (neredeyse sessiz) | -16,9 / -0,5 dB (dolu, tepe kırpılmaya yakın) |
| Prompt uyumu | 7 — yürüyor, kamera yanında, başını çevirip gülüyor | 5 — kavşakta duruyor, yürüme/izleme belirsiz; baş çevirme + gülme var |
| Yüz/el | 6 — tutarlı, biraz yumuşak | 7 — doğal, keskin |
| Işık/yansıma | 6 | 8 — sinematik renk, ıslak zemin yansımaları güçlü |
| Keskinlik | 5 | 7 |
| Tabela yazıları | uydurma | uydurma |
Sert puan (50–55 ölçeği): H3 ~50, Pika ~53. Kareler 4'er kare (0/32/64/96) kendim açıp baktım; ses yalnız ölçüldü, dinlenmedi.
KARAR (Ömer, 07:10, videoları izleyip): KRAL H3 KALIR — H3'ün sesi/dublajı iyi, Pika'nın sesi çok kötü. Pika'nın iki LoRA'sı silme adayı (3,64 GB).
Eski öneri (geçersiz): Pika H3 Flex yeni kral (aynı H3 tabanı üstüne LoRA; daha hızlı, daha az RAM, daha iyi görüntü). Zayıf yanı: prompt'taki "yürürken kamera yanında" hareketini tam yapmadı.
Silme adayları (Ömer onayı): pika_h3_flex_fl2va_comfy_bf16 (Pika'nın kendi dönüşümü, kopya, 1,82 GB); kral değişirse minimax_h3_fl2v_turbo_4step LoRA (1,82 GB).
Çıktılar: Desktop\Claude ile yapılanlar\video-karsilastirma\ pika.mp4, h3_vs_pika.mp4, h3_tam_kareler.png, pika_tam_kareler.png.
