---
type: report
status: done
tags: [model-karsilastir-1, envanter, oneri]
relatedTo: [docs/gorsel/modeller.md]
---
# MODEL-KARSILASTIR-1 (31 Eki 2026)

Makine: RTX 4070 Ti 12 GB (kural ≤%80 ≈ 9,8 GB), 34 GB RAM. SİLME YOK — yalnız öneri; silme Ömer onayıyla.
Ölçüm: `.kos/kopru/model_envanter.py` (≥100 MB model dosyası, samefile ile tekil) → `.kos/kopru/rapor/model-envanter-ham.tsv`: **53 dosya, 124,8 GB**. Taranan: C:\AI\ComfyUI\models, C:\AI\ComfyUI-T2\models, ~/.cache/huggingface, ~/.lmstudio ve ~/.ollama (var, ≥100 MB model dosyası çıkmadı), C:\Projeler\araclar (yalnız Jcode build artığı, model yok).
Kullanım kanıtı: repo `rg` (tools/, docs/, akış json). C:\AI içindeki kullanıcı iş akışları taranmadı → "kullanılmıyor" = repo'da referans yok.
Web: alt ajan araştırması (çoğu ikincil blog; sayıların kaynağı URL'li, bulunamayan "bulunamadı").

## Tablo

| Grup | Kurulu (GB) | Daha iyisi var mı | Çalışır (12 GB) | ÖNERİ |
|---|---|---|---|---|
| Video | Wan2.2 TI2V 5B fp16 9,31 + GGUF Q5 3,55 + umt5 fp8 6,27 + VAE 1,31 | LTX-2.3 22B (GGUF Q3_K_M 14,7 / Q2_K 12,4 + Gemma-3-12B enc 9,5); LTX-2.5 21B (Q4_K_M 12,2); MiniMax H3 / FreeVideo (H3 açık ağırlık 3 Ağu 2026, ~54 GB, lisans ABD/AB/UK hariç, FreeVideo "8 GB VRAM" iddiası, test edilmedi); Wan 2.5/3 açık DEĞİL (Wan 2.2'de durdu) | LTX GGUF: offload; FreeVideo: evet (iddia) | **TUT** Wan GGUF Q5 (akış wan22_5b_t2v.json kullanıyor). **SİL adayı** Wan fp16 9,31 (yalnız tmp notlarında; GGUF aynı işi yapıyor). **KUR (denemeli)** LTX-2.3 Q3_K_M ≈15 GB + enc 9,5; FreeVideo önce küçük paket ölç. |
| Görsel | flux1-schnell fp8 16,05; Z-Image bf16 11,46 / fp8 5,73 / GGUF Q4 3,59; Flux-2 klein 4B 7,22; qwen_3_4b 7,49 / fp8_mixed 5,25 / Q4 GGUF 2,33 | Z-Image-Turbo ve Flux.2 klein 4B zaten güncel (Apache-2.0); Qwen-Image 20B daha iyi yazı ama 12 GB'ta yalnız offload | evet | **TUT** Z-Image fp8 (sunucu_zimage.py), GGUF Q4 (turbo.json), klein 4B, qwen fp8_mixed, Q4 GGUF. **SİL adayı** `z_image_turbo_bf16` 11,46 (yalnız fp8_cevir.py kaynağı; fp8 türetildi, çalışma zamanında yüklenmiyor — yeniden türetme gerekirse HF'den iner); `qwen_3_4b.safetensors` 7,49 (hiçbir akış/koddan referans yok); `flux1-schnell-fp8` 16,05 (repo'da yalnız env listesi; klein 4B + Z-Image aynı işi daha hızlı/küçük yapıyor). |
| 3D | TRELLIS.2-4B bf16 ≈13 + FP8 ≈6,3 (visualbruno) + TRELLIS-image-large 0,14 + dinov3 1,13 | Hunyuan3D 2.1 (mmgp ile ~10 GB, texture dahil) alternatif; TRELLIS.2 resmi "≥24 GB", topluluk build'i offload | FP8 build: topluluk build'i, bu makinede ölçülmedi; bf16 resmi ≥24 GB | **TUT** FP8. **SİL adayı** bf16 ckpts (≈13 GB) — ancak FP8 çıktı kalitesi Ömer ölçeğinde onaylanırsa (repo'da bu iki yola referans bulunmadı; C:\AI\ComfyUI-T2 düğüm kodu bakılmadı → silmeden önce orada doğrula). |
| TTS | Dia 1.6B 6,0; OmniVoice 3,0; Chatterbox 3,0+; XTTS-v2 1,74; Kokoro 0,3 | Qwen3-TTS 0.6B/1.7B (Apache-2.0, 22 Oca 2026, 3 sn klonlama) — kurulu değil; Chatterbox Turbo/Multilingual v3 | hepsi evet | **TUT** Kokoro (CPU, Apache), Chatterbox (MIT), Dia. **KUR (denemeli)** Qwen3-TTS. **Lisans notu:** XTTS-v2 (Coqui NC) ve OmniVoice ağırlıkları (CC-BY-NC) ticari işte kullanılamaz → XTTS-v2 **SİL adayı** (Chatterbox klonlamada aynı işi MIT ile yapıyor). |
| ASR | faster-whisper large-v3 2,88; large-v3-turbo 1,51; small 0,45; small.en 0,45 | Leaderboard WER: Qwen3-ASR-1.7B 5,40; Parakeet TDT v2 6,02 (çok hızlı); Whisper large-v3 7,16; turbo 7,64 | evet | **TUT** large-v3 (kendi ölçümümüz: WER yarıya iniyor), turbo. small/small.en yalnız araclar/autoclip whisper_model_manager.py'de → **SİL adayı değil** (0,9 GB, autoclip bağımlı). **KUR (denemeli)** Parakeet v2 / Qwen3-ASR, kendi Türkçe WER setimizde ölç (leaderboard İngilizce ağırlıklı). |
| Upscaler / arka plan / OCR | kurulu model bulunmadı (≥100 MB eşiğinde) | SeedVR2 3B fp8/GGUF (~7 GB, 12 GB'a uygun); RMBG-2.0 NC lisans; OCR: PaddleOCR-VL 0.9B Apache-2.0 | evet | Gerek doğarsa KUR: SeedVR2, PaddleOCR-VL. Şimdi kurma. |
| LLM/metin kodlayıcı | Qwen3-4B 3 varyant (yukarıda); LM Studio/Ollama boş | — | — | Görsel satırına bak. |

## Geri kazanılabilir yer (yalnız öneri)
- z_image_turbo_bf16 11,46 + qwen_3_4b 7,49 + flux1-schnell-fp8 16,05 + wan fp16 9,31 = **44,3 GB** (kanıtlı: çalışma yolunda referans yok).
- Koşullu: TRELLIS.2 bf16 ≈13 GB, XTTS-v2 1,74 GB.

## Büyük kurulumlar planı
| Model | Gerçek boyut | VRAM | Yer |
|---|---|---|---|
| LTX-2.3 GGUF Q3_K_M | 14,7 GB + Gemma-3-12B enc 9,5 + VAE (boyut bulunamadı) ≈ 25 GB | offload gerekir (dosya ≈ VRAM'den büyük); Q2/Q3 kalitesi kötü (kaynak) | 44 GB silme sonrası rahat sığar |
| LTX-2.5 GGUF Q4_K_M | 12,2 GB + enc | +4–8 GB VRAM tavsiyesi → 12 GB sınırda | — |
| FreeVideo / H3 | model paketi boyutu **bulunamadı** (OpenVideo açıklamasında H3 ~54 GB, fp8/GGUF boyutu doğrulanmadı); "~77 GB" doğrulanamadı | iddia 8 GB VRAM/16 GB RAM, test yok | önce paket boyutunu repo'dan ölç, sonra karar |
| ODS | **bulunamadı** (web'de kaynak yok) | — | — |
Not: H3/FreeVideo lisansı bölge kısıtlı (ABD/AB/UK/G.Kore hariç) — ticari kullanımdan önce hukuk bakışı. LTX lisansı <10M$ ciro için ücretsiz.

## Sınırlar
- 12 GB uygunluk hükümleri TTS/ASR/OCR için parametre sayısından çıkarım, ölçüm değil; video/görsel kaynak iddialarına dayanır, makinede koşulmadı.
- LTX 2.3 çıkış tarihi bulunamadı; fp8/bf16 dosya boyutları bulunamadı.
- Silme yapılmadı.
