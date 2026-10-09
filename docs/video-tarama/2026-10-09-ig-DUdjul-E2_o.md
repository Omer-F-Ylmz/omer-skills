# Comment “UNLIMITED” 👇 to get the direct GitHub link in your DMs
## Künye
Comment “UNLIMITED” 👇 to get the direct GitHub link in your DMs · piyush.glitch · süre: 0:28 · ? · https://www.instagram.com/reel/DUdjul-E2_o/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-25 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 16932 tk · claude-haiku-5-5: claude-haiku-5-5 · 114720 tk
## Özet
Kısa reel: Lightricks'in açık kaynaklı LTX-2 video üretim modelinin kendi bilgisayarında yerel çalıştığı, Veo 3 ve Kling gibi ücretli araçlara gerek bırakmadığı anlatılıyor. Ekranda LTX Studio arayüzü, GitHub README (hızlı kurulum, gerekli modeller, ipuçları, prompt rehberi) ve ComfyUI entegrasyonu gösteriliyor. Repo bağlantısı için yorum yapma çağrısı var.
## Bölümler
- 0:00 Giriş: ücretsiz, yerel açık kaynak video üretimi
- 0:10 LTX-2 / LTX Studio arayüzü
- 0:12 GitHub deposu ve README
- 0:15 Hızlı kurulum ve gerekli modeller
- 0:17 Performans ipuçları ve prompt rehberi
- 0:18 ComfyUI entegrasyonu ve paketler
- 0:22 Model listesi (Veo ile karşılaştırma)
- 0:26 Kapanış: filigran yok, bulut bağımlılığı yok
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| LTX-2 | yok | teknik | https://github.com/Lightricks/LTx-2.git | Lightricks'in açık kaynaklı DiT tabanlı ses-video üretim modeli; yerelde çalışır. | 0:14 | README: LTX-2 ilk DiT tabanlı ses-video temel modeli (karede: README sayfasında LTX-2 tanıtım metni ve model dosyaları listesi) |
| LTX Studio | yok | iş akışı | yok | LTX-2 tanıtım arayüzü; projeler, storyboard, video/görsel üretimi, API playground. | 0:10 | Ekranda Ltx-2 başlığı, Create Storyboard, Generate Videos, Test in API playground (karede: Ltx-2 başlığı, All Projects, Create Storyboard, Generate Videos, Generate Images, Edit on a Timeline) |
| ComfyUI | yok | iş akışı | https://github.com/Lightricks/ComfyUI-LTXVideo/ | LTX-2'yi kullanmak için ComfyUI entegrasyonu. | 0:18 | OCR: To use our model with ComfyUI, please follow the instructions |
| Veo 3.1 | yok | teknik | yok | Rakip ücretli video modeli; ekranda model listesinde ve Image to Video'da görünür. | 0:22 | OCR: Veo 3.1, Veo 3.1 Fast, Veo 2 model listesi |
| Kling | yok | teknik | yok | Konuşmada anılan ücretli video üretim aracı. | 0:00 | no longer need to pay for VO3, Kling |
| Gemma 3 | yok | teknik | yok | LTX-2 için metin kodlayıcı (Gemma Text Encoder). | 0:16 | README: Gemma Text Encoder, Gemma 3 (karede: Gemma Text Encoder (download all assets from the repository) altında Gemma 3) |
| uv | yok | CLI | yok | Python bağımlılık/ortam yöneticisi; uv sync ile kurulum. | 0:15 | OCR: uv sync --frozen |
| Git | yok | CLI | yok | Depoyu klonlamak için git clone. | 0:15 | OCR: git clone https://github.com/Lightricks/LTx-2.git |
| GitHub | yok | iş akışı | yok | Deponun barındığı platform. | 0:12 | OCR: repo sayfası, 17 Commits, README.md |
| DistilledPipeline | yok | teknik | yok | 8 sigma ile en hızlı çıkarım hattı. | 0:17 | README: Use DistilledPipeline - Fastest inference with only 8 predefined sigmas (karede: Use DistilledPipeline maddesi, 8 steps stage 1, 4 steps stage 2) |
| FP8 transformer | yok | teknik | yok | Daha düşük bellek kullanımı için FP8 modu. | 0:17 | README: Enable FP8 transformer, lower memory footprint (karede: Enable FP8 transformer maddesi, --enable-fp8 (CLI)) |
| Gradient estimation | yok | teknik | yok | Çıkarım adımlarını 40'tan 20-30'a düşürür. | 0:17 | README: Use gradient estimation - Reduce inference steps from 40 to 20-30 (karede: Use gradient estimation maddesi) |
| LoRA | yok | teknik | yok | Distilled, Camera-Control, IC-LoRA (Canny, Depth, Detailer, Pose) ağırlıkları. | 0:16 | README LoRAs listesi (karede: LoRAs altında LTX-2-19b-IC-LoRA-Canny-Control, Depth-Control, Detailer, Camera-Control-Dolly-In) |
| Spatial Upscaler | yok | teknik | yok | İki aşamalı hat için gerekli uzamsal büyütücü model. | 0:16 | ltx-2-spatial-upscaler-x2-1.0.safetensors (karede: Spatial Upscaler başlığı ve ltx-2-spatial-upscaler-x2-1.0.safetensors) |
| Temporal Upscaler | yok | teknik | yok | Gelecek hatlar için zamansal büyütücü model. | 0:16 | ltx-2-temporal-upscaler-x2-1.0.safetensors (karede: Temporal Upscaler başlığı ve ltx-2-temporal-upscaler-x2-1.0.safetensors) |
| Automatic Prompt Enhancement | yok | teknik | yok | enhance_prompt parametresiyle otomatik prompt iyileştirme. | 0:18 | OCR: pipelines support automatic prompt enhancement via enhance_prompt |
| Python | yok | teknik | yok | fp8transformer=True gibi Python kullanımı. | 0:17 | README: (CLI) or fp8transformer=True (Python) (karede: Enable FP8 transformer maddesinde (Python) ifadesi) |
| xFormers | yok | teknik | yok | Dikkat (attention) hesaplamasını hızlandıran ve bellek kullanımını azaltan kütüphane; README'de optimizasyon olarak öneriliyor. | 0:17 | Install attention optimizations - Use xFormers · kanıt: kare (karede: README satırı: 'Install attention optimizations - Use xFormers (or sdpa - extra xformers) or Flash Attention 2 for Hopper GPUs'.) |
| Flash Attention 2 | yok | teknik | yok | Hopper GPU'lar için dikkat hesaplaması optimizasyonu kütüphanesi; README'de xFormers ile birlikte anılıyor. | 0:17 | or Flash Attention 2 for Hopper GPUs · kanıt: kare (karede: Aynı README satırında 'or Flash Attention 2 for Hopper GPUs' ifadesi.) |
| Veo 2 | yok | teknik | yok | LTX arayüzünün 'OTHER MODELS' listesinde görünen eski Veo sürümü. | 0:22 | OTHER MODELS · Veo 2 (karede: kanıttan) OTHER MODELS · Veo 2 |
| LTX-2 için etkili prompt yazma rehberi | yok | prompt | yok | LTX-2 prompt rehberi: tek akıcı paragrafta, 200 kelime içinde, ana eylemle başla; karakterleri, hareketleri, arka planı, kamera açılarını, ışığı ve renkleri kronolojik ve net anlat; ani değişiklikleri not et. | 0:17 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/Lightricks/LTx-2.git | LTX-2 deposunu klonlar (karede: Quick Start altında # Clone the repository ve git clone satırı) | 0:15 | kare |
| uv sync --frozen | Bağımlılıkları kilit dosyasına göre kurar (karede: # Set up the environment altında uv sync --frozen) | 0:15 | kare |
| source .venv/bin/activate | Sanal ortamı etkinleştirir (karede: source .venv/bin/activate satırı) | 0:15 | kare |
| --enable-fp8 | FP8 transformer'ı etkinleştirir ve bellek kullanımını düşürür (CLI bayrağı). (karede: README satırı: 'Enable FP8 transformer - Enables lower memory footprint: --enable-fp8 (CLI)'.) | 0:17 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| LTX-2 tamamen açık kaynak ve kendi bilgisayarda yerel çalışıyor. | 0:00 | özellik |
| Veo 3 ve Kling gibi ücretli araçlara artık ihtiyaç yok. | 0:00 | karşılaştırma |
| Filigran yok, bulut bağımlılığı yok. | 0:26 | özellik |
| Düşük donanımlı bilgisayarlarda da çalışır, pahalı GPU gerekmez. | açıklama | özellik |
| Gradient estimation çıkarım adımlarını 40'tan 20-30'a düşürür. | 0:17 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Lightrix/Lightricks | LTX-2 | fully open source video generation model |
| kare 0:10 | LTX Studio arayüzü | LTX Studio | Create Storyboard, Generate Videos |
| konuşma 0:00 | VO3 / Veo 3 | Veo 3.1 | no longer need to pay for VO3 |
| konuşma 0:00 | Kling | Kling | VO3, Kling or any other paid |
| kare 0:00 | Veo 3.1 Image to Video | Veo 3.1 | OCR: GVeo 3.1 Image to Video |
| kare 0:12 | GitHub repo sayfası | GitHub | 17 Commits, README.md |
| kare 0:15 | git clone | Git | git clone https://github.com/Lightricks/LTx-2.git |
| kare 0:15 | uv sync --frozen | uv | Set up the environment |
| kare 0:16 | Gemma Text Encoder | Gemma 3 | Gemma 3 |
| kare 0:16 | Spatial Upscaler | Spatial Upscaler | ltx-2-spatial-upscaler-x2-1.0 |
| kare 0:16 | Temporal Upscaler | Temporal Upscaler | ltx-2-temporal-upscaler-x2-1.0 |
| kare 0:16 | LoRA'lar | LoRA | LTX-2-19b-IC-LoRA-Canny-Control |
| kare 0:17 | DistilledPipeline | DistilledPipeline | only 8 predefined sigmas |
| kare 0:17 | FP8 transformer | FP8 transformer | --enable-fp8 (CLI) |
| kare 0:17 | gradient estimation | Gradient estimation | 40 to 20-30 steps |
| kare 0:17 | Prompting for LTX-2 | LTX-2 | prompt rehberi bölümü |
| altyazı 0:18 | enhance_prompt | Automatic Prompt Enhancement | automatic prompt enhancement via enhance_prompt |
| ekran 0:18 | ComfyUI-LTXVideo | ComfyUI | github.com/Lightricks/ComfyUI-LTXVideo/ |
| ekran 0:17 | Python (fp8transformer=True) | Python | (Python) |
| açıklama | @ltx.studio | LTX Studio | @ltx.studio |
| açıklama | Gemini hashtag | aday değil: konu dışı | #gemini #contentcreator #foryou |
| açıklama | UNLIMITED yorum çağrısı | aday değil: sponsor/reklam | Comment UNLIMITED to get the link |
| ekran 0:22 | LTX-2 Ultra / Legacy modeller | LTX-2 | LTX LEGACY MODELS listesi |
| ekran 0:22 | Veo 2 / Veo 3.1 Fast | Veo 3.1 | OTHER MODELS listesi |
## Kareden okunanlar
- 0:10: Ltx-2 başlığı, Test in API playground, All Projects, Create Storyboard, Generate Videos, proje kartları (Translucent prism, Supremo, Moebius Trailer, The Chain Shortfilm, 88 Lip Balm Advert); altta konuşmacı.
- 0:16: README model listesi: Spatial/Temporal Upscaler, Distilled LoRA, Gemma Text Encoder, LoRAs; altyazı 'generation forever'.
- 0:17: README: DistilledPipeline, FP8 transformer, gradient estimation, skip memory cleanup, single-stage pipeline, Prompting for LTX-2; altyazı 'This means you no longer'.
## Belirsizlikler
- Dil alanı belirsiz; konuşma İngilizce.
- Konuşmada 'Lightrix' deniyor, açıklamada Light Tricks/@ltx.studio; Lightricks kastediliyor.
- 'Düşük donanımda çalışır' iddiası yalnız açıklamada; videoda donanım gereksinimi gösterilmiyor.
- Sözlükteki Claude, Descript, Three.js, LightRAG eşleşmeleri doğrulanmadı; videoyla ilgisiz.
- Yorumlar girişsiz alınamadı.
- Veo 2 / Veo 3.1 Fast gibi öğeler yalnız model menüsünde görünüyor, kullanılmıyor.
- Açıklamadaki #gemini etiketi videoyla ilgisiz görünüyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/DUdjul-E2_o/ | açıklama | açıklama | hayır |
| https://github.com/Lightricks/LTx-2.git | 0:15 | ekran | evet |
| github.com/Lightricks/ComfyUI-LTXVideo/ | 0:18 | ekran | evet |
| https://ltx.video/blog/how-to-prompt-for-ltx-2 | 0:17 | ekran | hayır |
## İş akışı
- 1. adım — Ücretli alternatiflerle (Veo 3, Kling) karşılaştırarak LTX-2'nin ücretsiz ve yerel olduğunu anlat — araçlar: LTX-2, Veo 3.1, Kling
- 2. adım — LTX Studio arayüzünü, proje menülerini ve model seçicisini göster — araçlar: LTX Studio
- 3. adım — GitHub'da LTx-2 deposunu ve README'yi aç — araçlar: GitHub
- 4. adım — Gerekli model dosyalarını (.safetensors), upscaler'ları ve LoRA'ları README'den listele — araçlar: GitHub, LTX-2
- 5. adım — Gemma 3 metin kodlayıcısının gerekli olduğunu belirt — araçlar: Gemma 3
- 6. adım — git clone ile depoyu yerel bilgisayara klonla — araçlar: Git
- 7. adım — Sanal ortamı etkinleştir ve uv sync --frozen ile bağımlılıkları kur — araçlar: uv
- 8. adım — Pipeline seçeneklerini göster: DistilledPipeline, gradient estimation, tek aşamalı pipeline — araçlar: LTX-2
- 9. adım — Bellek ve hız optimizasyonlarını göster: FP8 transformer, xFormers veya Flash Attention 2 — araçlar: xFormers, Flash Attention 2
- 10. adım — ComfyUI entegrasyonu için ComfyUI-LTXVideo deposunu göster — araçlar: ComfyUI, ComfyUI-LTXVideo
- 11. adım — README'deki prompt yazma kurallarını göster — araçlar: LTX-2
- 12. adım — Yorum/DM ile repo linki dağıtımını duyur (UNLIMITED) — araçlar: Instagram
## Promptlar
- LTX-2 için etkili prompt yazma rehberi — LTX-2 prompt rehberi: tek akıcı paragrafta, 200 kelime içinde, ana eylemle başla; karakterleri, hareketleri, arka planı, kamera açılarını, ışığı ve renkleri kronolojik ve net anlat; ani değişiklikleri not et.
