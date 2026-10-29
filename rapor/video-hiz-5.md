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
- C: Groq + yerel yedek CPU large-v3 int8 (VD_ASR_AYGIT=cpu, GPU'ya dokunmaz): CPU hattı ~50 sn/video (tek kilit) → yerel hat ~70/sa; 40 video koşusu >10 dk (ölçüm sürüyor/tamamlandığında satır eklenecek).
- Kod: video_derin.py → Groq model listesi + saatlik ses-sn bütçesi (VD_GROQ_MODELLER, VD_GROQ_SAAT), VD_SAHNE, VD_ASR_AYGIT/VD_ASR_IPLIK; CPU ASR GPU_KILIT tutmaz. Varsayılanlar henüz değişmedi (VD_GROQ=0).
