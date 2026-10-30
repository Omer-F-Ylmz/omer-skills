---
name: ucretsiz-web-ai
description: "Girişsiz/ücretsiz web AI araçları (ToolFK + gömülü HF Space'ler): görsel→video (Wan 2.2), upscaler, prompt'lu görsel düzenleme (arka plan sil, nesne sil, 2D→3D, thumbnail). Yerel hat yetmediğinde sosyal-oto/ai-influencer için video/görsel kaynağı. Qwen Chat videosu girişsiz ÇALIŞMAZ."
---

# ucretsiz-web-ai (QWEN-TOOLFK-1, 30 Eki 2026, ölçülü)

Sürücü: Playwright headless Chrome (`python -X utf8`; `-I` PYTHONIOENCODING'i yok sayar). Pencere açılmaz; varsayılan tarayıcı yok.

| İş | Yol | Ölçüm (tilki 512px) |
|---|---|---|
| Görsel→video | `scripts/wan_i2v.py` → zerogpu-aoti/wan2-2-fp8da-aoti-faster.hf.space (ToolFK hf-wan-image-to-video) | 45 sn, 640×640, 16fps, 3,6 sn, filigran yok, karakter tutarlı, el sallama gerçekleşti |
| Upscaler | `scripts/ui_hf.py https://ovi054-image-upscaler-pro.hf.space/ girdi.jpg etiket` | 20 sn, 512→2048 px |
| Arka plan sil / nesne sil / 2D→3D / thumbnail | `scripts/toolfk_gen.py <slug> "Generate Image" "<prompt>" 200 girdi.jpg` (slug: ai-background-remover, ai-object-remover, ai-2d-to-3d-image-converter, ai-youtube-thumbnail-maker) | bg-remover: 45 sn, 1024², beyaz zemin, temiz |
| Ücretsiz Qwen API | Model Studio/OpenRouter `:free` Qwen — ölçülmedi (hesap/anahtar gerekir) | — |

## Çalışmayanlar / sınırlar
- chat.qwen.ai "Video Oluştur": prompt gönderince giriş penceresi çıkar, 120 sn'de video yok → reeldeki "giriş yok" iddiası YANLIŞ/doğrulanmadı. Giriş gerekir (Ömer yapar).
- ToolFK `online-img-to-video`, `online-text-to-video`: anında üretmiyor ("Video generation failed", e-postayla manuel kuyruk, misafir günlük sınır). Kullanma; Wan Space kullan.
- Görsel düzenleyici ailesi: paylaşılan günlük kota 5000 (gece 00:00 sunucu), sayfada herkesin prompt'ları + IP ülkesi akışı görünüyor → yüklenen görsel/prompt kamuya açık sayılır.
- HF Space ZeroGPU: anonim kota dolarsa hata verir; tekrar dene/bekle. gradio_client "Unknown protocol: ws" veriyor → UI sürücüsü kullan.
- Ölçülemedi: ToolFK OCR/PaddleOCR (çıktı alınamadı; yerel RapidOCR/Unlimited-OCR kullan), TTS (tarayıcı içi Piper/sistem sesi; yerel Kokoro/Chatterbox daha iyi), compress (istemci tarafı).

## YASAK
AI Clothes Remover/undress, skin/skinny gibi gerçek kişi bedenini değiştiren filtreler: KULLANMA. Watermark Remover ve Remove People yalnız kendi içeriğimizde. Gerçek kişi fotoğrafı yüklenmez; kişisel veri yok (site Çin merkezli, KVKK). Yalnız maskot/üretilmiş görsel yükle. Ticari kullanım koşulları ölçülmedi: yayından önce ilgili Space/ToolFK şartı okunmalı.

## Bağlantı
sosyal-oto-1 / ai-influencer-1: tilki maskot kareleri → Wan i2v ile 3,6 sn klip (ücretsiz kaynak), upscaler ile 2048px. Yerel ComfyUI/Wan varsa önce o.
