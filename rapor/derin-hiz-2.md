# DERIN-HIZ-2 — TUR BITTI (kapı GEÇMEDİ, toplu koşu başlatılmadı)

- Değişiklik (tools/video_derin.py): ASR varsayılanı large-v3 beam5'e geri döndü; groq_asr önce denenir (VD_GROQ=1), kota/hata'da yerel devralır. yt-dlp -N 4 kaldı.
- Kapı koşusu (Groq whisper-large-v3, aynı 10 link): yalnız 5 Instagram bitti; 5 YouTube linki ~15:11'den beri ilerlemedi (takıldı).
- Kelime benzerliği (noktalama çıkarılarak, eski docs/video-tarama/derin'e karşı): 1,000 / 0,991 / 0,951 / 0,898 / 0,726 → ort 0,913 < 0,98. OCR örtüşme 1,000.
- Sebep: Groq VAD'siz ve farklı segmentleme/yanlış-duyma ("so explain" vs "to explain"); aynı model ≠ aynı çıktı.
- Sonuç: Groq-önce kalite kapısını geçmedi → VD_GROQ varsayılan 0 (kapalı), yerel large-v3 beam5 = eski kalite. Hızlanma yok.
- Karşılaştırıcıya noktalama normalizasyonu eklendi (içerik değil; eski ölçüm 0,886 da buna göre yüksek çıkardı).
- Soru (Ömer): kaliteden ödün vermeden hız yolu yok gibi; toplu 877 link için yerel large-v3 beam5 ~120 sa kabul mü, yoksa eşik %95'e mi inilsin?
