# VIDEO-HIZ-5 (ara kayıt, 29 Eki)
Set: 40 shorts (kisa.txt), ref2 = orijinal ses izi large-v3 beam5; ölçüm tools/video_hiz4_olc.py + hiz4_karsi2.py + hiz5_asr_recall.py. Taban (TUR 3/4, es 3): 343–368/sa, GPU tepe %100.
| deney | video/sa | GPU tepe | VRAM | RAM | link/komut | OCR sabit | ASR kelime-recall (34 ortak video) |
|---|---|---|---|---|---|---|---|
| taban es3 (tur4es3o12) | 343 | 100 | 60 | 86 | 37/37 | 37/37 | 0,947 |
| G: Groq whisper-large-v3 (ASR bulutta), es3 | 658 | 21 | 15 | 82 | 38/38 | 38/38 | 0,949 (taban/Groq = 1,002) |
- Not: ref2'ye göre 4 videoda recall 0,0 (çok ses izli/farklı iz) hem tabanda hem Groq'ta aynı → referans kusuru, karşılaştırmadan çıkarıldı. SequenceMatcher benzerliği Groq 0,840 / taban 0,936 (sıra/segment farkı; kelime recall eşit).
| T: Groq whisper-large-v3-turbo, es3 | 744 | 30 | 15 | 83 | 37/37 | 37/37 | 0,930 (oran 0,980) |
| K: Groq v3+turbo, bütçe 585 sn/model (saatlik 6500'ün 40-video eşdeğeri), yerel GPU yedek, es3 | 490 | **96** | 53 | **92** | 38/38 | 38/38 | 0,937 (oran 0,990) · 24 Groq / 15 yerel |
- K dağılımı: yerel yedek GPU large-v3 batched; GPU tepe %96 ve RAM tepe %92 (başlangıç RAM %80 — Ömer süreçleri; TUR 3'te %75 idi) → kapı (GPU ≤%80, RAM ≤%89) GEÇMEDİ.
- Kod: video_derin.py → Groq model listesi + saatlik ses-sn bütçesi (VD_GROQ_MODELLER, VD_GROQ_SAAT), VD_SAHNE, VD_ASR_AYGIT/VD_ASR_IPLIK; CPU ASR GPU_KILIT tutmaz. Varsayılanlar henüz değişmedi (VD_GROQ=0).
| C: K ile aynı, yerel yedek CPU large-v3 int8 (VD_ASR_AYGIT=cpu) | 98 | 79 | 25 | 90 | 38/38 | 38/38 | (yerel hat video başı 50–330 sn; ölçüm 1432 sn) |
| K3: K + GPU nefes 0,6 + OCR kare azaltma (VD_TEKIL=5, VD_SAHNE=0.4), es2 | 396 | **100** | 54 | 84 (başlangıç %74) | 38/38 | 34/38 ≥0,98, ort 0,966 (ham 0,808) | 0,937 (oran 0,990) |

# VIDEO-HIZ-5 — TUR BITTI (kapı GEÇMEDİ; izleme/kurulum başlamadı; push yok)
Kapı: 400–500/sa + recall ≥%95 + link/komut %100 + GPU tepe ≤%80 (+ RAM ≤%89).
- (1) ASR'yi GPU kilidinden ayırma: Groq bulut ASR (large-v3 / turbo, ücretsiz) → 658 / 744 video/sa, GPU tepe %21 / %30, RAM ≤%83, link/komut %100, ASR kelime-recall tabana oranla 1,002 / 0,980. TEK başına kapıyı (hız+GPU+recall) geçer AMA yalnız kota dolana dek: videolar ort 49,7 sn ses; model başına 7200 ses-sn/sa varsayımıyla (belgelenmiş ücretsiz kota; 429 yakalaması kodda, kota gerçek hâlde ölçülmedi) iki model ≈ 290 video/sa sürdürülebilir. Kalan ~%40 yerel ASR'ye düşer.
- Yerel yedek GPU (large-v3 batched): 490/sa ama GPU tepe %96, RAM %92 (başlangıç %80) → kapı geçmez. GPU nefes 0,6 + OCR azaltma + es2 (K3): 396/sa, GPU tepe hâlâ %100 → geçmez. Yerel yedek CPU large-v3 int8: GPU %79 ama 98/sa, RAM %90 → kullanılamaz.
- (2) yazı ön sınıflandırıcı: YAPILMADI (OCR GPU'da tek başına %21–30; Groq hattında darboğaz değil). Kare azaltma (VD_TEKIL 2→5, VD_SAHNE 0.3→0.4) OCR ham recall'ı 0,948 → 0,808, sabit 1,000 → 0,966 düşürdü (kabul sınırında, 4/38 video <0,98) → varsayılan yapılmadı.
- (3) sahne eşiği: yukarıda (K3 ile birlikte ölçüldü, ayrı ölçülmedi). (4) altyazı: YouTube shorts'ta referansa 0,60–0,95 (TUR 4 bulgusu), değişmedi. (5) toplu OCR: denenmedi (40 tur bütçesi).
- Varsayılanlar DEĞİŞMEDİ (VD_GROQ=0, es 3, VD_TEKIL=2, VD_SAHNE=0.3): kapıyı geçen birleşim yok, geri alma gerekmiyor. Yeni kod yalnız env bayrağı: VD_GROQ_MODELLER, VD_GROQ_SAAT (model başına saatlik ses-sn bütçesi; dolunca sıradaki model sonra yerel), VD_SAHNE, VD_ASR_AYGIT/VD_ASR_IPLIK, CPU ASR GPU_KILIT tutmaz.
- Referans kusuru: ref2'de 4 video (2YPak3uh7Ws, hLZ_yRgKq3M, LofyMQts7hY, 9ciMSvQkQDg) tabanda da recall ~0 (çok ses izi) → ortak karşılaştırmada (tools/hiz5_ortak.py) elendi.
- Sonraki deneme önerisi (kapıyı geçmek için yeni kaynak lazım): ücretsiz ikinci/üçüncü bulut ASR sağlayıcı (kota biter bitmez sıradaki), ya da GPU'yu %80 altında tutan sert zamanlayıcı (nvidia-smi geri beslemeli, ORAN yerine) — ikisi de ölçülmedi.
- Kaynaklar: video-hiz-4.md (TUR 1–4), tools/video_hiz4_olc.py, hiz4_karsi2.py, derin-zaman.tsv; Groq ücretsiz kota değerleri belgeden (canlı doğrulanmadı). Roast Room/envanter_tara kullanılmadı (tur bütçesi).
