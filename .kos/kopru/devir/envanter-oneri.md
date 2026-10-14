# ENVANTER-KULLAN-1 öneri blokları (Desktop devirlere aktarır; kaynak docs/kullan-haritasi.md)

## VİDEO-3 / VİDEO-KISA-TOKEN-2 / 180 link
- STT zaten Gemini'siz (whisper.cpp CUDA + --prompt, cli.py:1634). Dokunma.
- Kare metni: RapidOCR (tools/video/.venv) birincil; Tesseract tur yedek değil (gürültülü).
- Gemini 429 PerDay olunca görsel kolu: ollama yerel `qwen3.5:4b` (/api/chat, images, think:false, ~6 s sıcak). Yalnız OCR'ın boş döndüğü karelere.
- Metin çıkarımı yedek: openrouter nemotron-3-super :free ya da ollama `gpt-oss:20b-cloud` — önce onaylı 1 çağrılık deneme.
- Groq OmniRoute üstünden kırık (canlı katalog 400, ucretsiz-groq 502) — kota planına Groq'u yazma.

## SİTE-OKULU-2 yargıç
- `pixeljury review <url> --provider ollama --model qwen3.5:4b --json` yerel kör yargıç; Gemini + nemotron-omni :free ile medyan.

## TELVE görsel kabul
- PixelJury ollama kolu + kontak.py + Blender 5.2.1 `-b` (tam yol `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`).
- Doku/arka plan: ComfyUI `C:\AI\ComfyUI` z_image_turbo / flux-2-klein-4b, RealESRGAN_x4plus; dekupaj `C:\AI\rembg`. fps ölçümü sırasında GPU'yu kullanma.

## TOKEN-4
- Ölçüm: `rtk gain` (82.2% tasarruf), `headroom savings` (bugün 26.9%), `claude-usage`. qmd dizini 120 KB — kullanılmıyor; ya dizinle ya devreden çıkar.

## GRAPHIFY
- graphify paketi 0.9.88, ~/.agents skill'i 0.9.57 → `graphify install --platform agents` (onay betiği --kuru ile önerilir).

## Bakım (onay gerek)
- skill-ui kırık (node modül), lms kırık (LM Studio kurulumu yok; diskte Qwen3.8-27B VLM gguf boşta), whisper-cli/tesseract/blender PATH'te yok (köprü allowlist adları çözülmez).
