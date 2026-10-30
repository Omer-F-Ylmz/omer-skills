# QWEN-TOOLFK-1 (30 Eki 2026)
1 QWEN: chat.qwen.ai girişsiz açılır, "Video Oluştur" menüde var; prompt gönderince giriş penceresi ("Video oluşturma gibi özelliklerin kilidini açmak için giriş yapın"), 120 sn video yok → "girişsiz video" iddiası DOĞRULANMADI (giriş şart; sabah Ömer). Görsel→video, filigran/lisans/kota ölçülemedi (giriş gerekir). Ücretsiz Qwen API (Model Studio/OpenRouter :free) ölçülmedi.
2 TOOLFK (222 araç; çoğu gömülü HF Space, girişsiz):
- Wan2.2 i2v (hf-wan-image-to-video): ÇALIŞTI 45 sn, 640², 16fps, 3,6 sn, filigransız, tilki tutarlı + el salladı. Sert puan ~65/100 (kısa, 640px; sosyal-oto için kullanılabilir). Kanıt wan-kontak.png, out-wan.mp4.
- Upscaler: ÇALIŞTI 20 sn, 512→2048. ~70/100. upscaler-out2.png.
- ai-background-remover (ai-img editör ailesi: object remover, 2D→3D, thumbnail aynı uç): ÇALIŞTI 45 sn, 1024², beyaz zemin, temiz ~70/100. Diğer üçü bu uçtan ölçülmedi.
- img-to-video / text-to-video (native): anında üretmedi, "Video generation failed" → e-posta manuel kuyruk; kullanma.
- OCR/PaddleOCR, TTS, compress: ölçülemedi (OCR çıktısı alınamadı; TTS/compress tarayıcı içi). Yerel RapidOCR/Kokoro/ffmpeg zaten var.
- Karşılaştırma: yerel ComfyUI/Wan (1080p+, sınırsız) kalite üstün; web hat yalnız yedek/hızlı kaynak. Higgsfield/FreeVideo/TRELLIS karşılaştırması ölçülmedi.
- Sınırlar: paylaşılan kota 5000/gün; sayfada kullanıcı prompt+IP-ülke akışı herkese açık → yalnız maskot yüklendi. ZeroGPU anonim kota dolabilir. Ticari kullanım şartı okunmadı.
3 KURULUM: skills/ucretsiz-web-ai (+scripts) → ~/.claude/skills; dist/ucretsiz-web-ai.zip (zip_denetle TEMİZ; yükleme Desktop); usta kartı, envanter.tsv, kayit.jsonl, Obsidian 40-projeler/QWEN-TOOLFK-1.md. sosyal-oto-1/ai-influencer-1 devam_notu bağlantısı skill içinde yazıldı (ayrı dosya düzenlenmedi). arac-ara indeksi yeniden üretilmedi.
YASAK: undress/skin filtreleri kullanılmadı; gerçek kişi görseli yüklenmedi; giriş/kayıt yok.
Sabah Ömer: Qwen hesabıyla video/kredi/lisans ölçümü.
Kaynak: paket.md, toolfk.com, HF Space'ler. Çıktılar: sosyal-onizleme/qwen-toolfk/
