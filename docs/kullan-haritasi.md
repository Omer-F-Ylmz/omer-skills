# Kullan haritası — ENVANTER-KULLAN-1 (15 Eki 2026)

Amaç: tek dış servise (Gemini günlük kota) takılmamak. Her satırın kanıtı `.kos/kopru/envanter/` altındaki çıktıdan
(probe.tsv, deneme_gorsel.txt, deneme_groq.txt, yerel_kanit.txt, kacak.json, omni_models_api.json).

## Yerel güç (dış kota yok)
- GPU: RTX 4070 Ti 12 GB — kanıt `nvidia-smi`: "NVIDIA GeForce RTX 4070 Ti, 12282 MiB, 1318 MiB, 13 %".
- whisper.cpp v1.8.0 CUDA (`ggml-cuda.dll`, cublas) + `ggml-large-v3-turbo.bin` — `C:\Projeler\.tmp-video\`. PATH'te YOK; köprü allowlist'teki `whisper-cli` adı çözülmez, `video` aracı tam yolu (cli.py:1571 WCPP) kullanıyor.
- faster-whisper-large-v3-turbo + rapidocr modelleri `.tmp-video/models/`; global python'da `faster_whisper+ ctranslate2+`.
- Tesseract `C:\Program Files\Tesseract-OCR` (PATH'te yok), `tur.traineddata` yalnız `.tmp-video/tessdata`'da.
- RapidOCR (tools/video/.venv, onnxruntime DirectML) — kanıt: k00088.png'de 18 satırın hepsi temiz ("SEREIN … THE ARC RESIDENCE"), 6.3 s.
- Ollama yerel `qwen3.5:4b` (vision+tools) — kanıt: aynı kare, sıcak 6.2 s, "Serein / Private viewing" (kısa ama doğru).
- Ollama bulut modelleri bağlı: `kimi-k2.7-code:cloud` (vision), `gpt-oss:20b/120b-cloud`, `glm-5.3-flash:cloud`, `deepseek-v4.1-flash:cloud`, `gemma4:cloud` — `ollama show` yetenekleri okundu; çağrı DENENMEDİ (dış çağrı onayı yok).
- LM Studio: diskte `Qwen3.8-27B-Q4_K_M.gguf` + `mmproj-…BF16.gguf` (VLM); `lms ls` → "daemon is not running and no valid installation" → kullanılamaz.
- ComfyUI `C:\AI\ComfyUI` (.venv): `flux-2-klein-4b`, `z_image_turbo` (bf16/fp8), `qwen_3_4b` metin kodlayıcı, `RealESRGAN_x4plus`; custom_nodes boş (Florence-2/JoyCaption YOK). `C:\AI\rembg` var.
- Blender 5.2.1 LTS — `blender.exe -b --version` (PATH'te yok, tam yol).
- Diğer: yt-dlp 2026.08.19, ffmpeg/ffprobe 9.0.1, markitdown 0.1.8, qmd 2.8.3, jq 1.8.2, java 17, pytest 9.1.1.
- Bozuk/eksik: `skill-ui` (node modül yükleyici hatası, rc=1), `summarize --version` 25 s'de zaman aşımı, `lms` (yukarıda), `magick/rg/pandoc/docker` YOK.

## OmniRoute (127.0.0.1:20128, 1777 model id)
- Bağlı sağlayıcılar: gemini, grok-cli, groq, moonshot, openrouter (`omniroute providers list` hepsi active). Combolar: cc-yedek, cc-yedek-dis, ucretsiz-ozet, ucretsiz-ozet2, ucretsiz-groq.
- Groq KIRIK: `groq/llama-3.3-70b-versatile` ve `groq/meta-llama/llama-4-scout-…` → 400 "not available in the active live catalog for provider 'groq'"; `ucretsiz-groq` combo → 502. /v1/models listede gösteriyor ama canlı katalog yok (bkz. hafıza omniroute-groq-ua).
- OpenRouter :free adayları listede: nemotron-3-nano-omni-30b (görsel), nemotron-3-super-120b, nemotron-3-ultra-550b, gemma-4-31b-it, gemma-4-26b-a4b-it. Bu oturumda denenemedi (sınıflandırıcı dış çağrıyı reddetti).
- moonshot (Kimi) ücretli olabilir — :free değil, kullanma.

## İş → engel → araç → komut → kazanç
- VİDEO-3 / VİDEO-KISA-TOKEN-2 / 180 link — engel: Gemini 3 model günlük kota (kota.py MODELLER = gemini-3.8-flash, 3.5-flash, 3.5-flash-lite).
  - STT: zaten yerel — `video` cli.py:1634 whisper.cpp GPU + `--prompt` sözlüğü; Groq whisper kolu (cli.py:1597) OmniRoute dışı doğrudan. Kazanç: STT Gemini'ye hiç bağlı değil; yapılacak yok.
  - Kare metni: RapidOCR birincil (Tesseract tur gürültülü: "tösyonamne fim"). Komut: `tools/video/.venv/Scripts/python.exe -c "from rapidocr import RapidOCR; print(RapidOCR()('<kare>').txts)"`. Kazanç: kare başı 0 jeton, ~6 s CPU.
  - OCR boş karede görsel: yerel `qwen3.5:4b` (ollama /api/chat, images, `think:false`) → 6 s sıcak, kota yok. Kazanç: Gemini görsel çağrısının yerine geçer; isim kalitesi OCR'dan zayıf → yalnız yedek.
  - Metin çıkarımı (OCR+transkript → araç adları): yerel `qwen3.5:4b` ya da ollama bulut `gpt-oss:20b-cloud` / openrouter nemotron-super :free. Önce 1 çağrılık onaylı deneme gerek.
- SİTE-OKULU-2 yargıç — engel: Gemini yargıç kotası.
  - PixelJury 0.1.5: `pixeljury review <url> --provider ollama --model qwen3.5:4b --json` (yerel, anahtarsız) ve `--provider claude-code` (yerel CLI girişi; claude -p sayılır). Kör çok yargıç = ollama qwen3.5 + nemotron-omni :free + Gemini (varsa) → medyan.
  - jev (puanlama/kalibre alt komutları var: `jev kalibre`, `jev skill-olc`).
- TELVE görsel kabul — PixelJury (yukarıdaki ollama kolu) + `.kos/kopru/kontak.py` + Blender `-b` (tam yol); arka plan/doku: ComfyUI z_image_turbo/flux-2-klein-4b (yerel, 12 GB'a sığar), büyütme RealESRGAN_x4plus, dekupaj `C:\AI\rembg`. GPU'yu fps ölçümüyle paylaşma.
- TOKEN-4 (tur başı ~60k) — ölçüm araçları hazır: `rtk gain` "Tokens saved 43.6M (82.2%)"; `headroom savings` "Today 26.9% saved 6,697,253"; `claude-usage` panosu; qmd dizini yalnız 120 KB (neredeyse boş → kullanılmıyor).
- GRAPHIFY — graphify 0.9.88 ama ~/.agents skill'i 0.9.57 ("Run graphify install --platform agents" uyarısı) → skill eski.

## Kaçak (kurulu, atlasta yok — kacak.json)
- CLI/model (33): rtk, jev, headroom, pixeljury, agent-reach, claude-usage, yt-dlp, ollama, lms, whisper-cli, tesseract, comfyui, rapidocr, faster-whisper, qwen3.5, kimi-k2.7, gemma4, nemotron, flux-2, z_image, realesrgan, rembg, groq, vercel, skill-ui, jq, pytest, nvidia-smi …
  - Öneri: video-icerik kartına rapidocr+qwen3.5 yedek kolu; site-3d / frontend kartına pixeljury(ollama)+ComfyUI+rembg; token kartına rtk/headroom/claude-usage ölçüm kolu.
- MCP (25): brave-search, claude-design, serena, codegraph, codebase-memory-mcp, mcp-memory, mcp-sequential-thinking, n8n-mcp, puppeteer, unity, godot, hfspace, arxiv, apify, airtable, clickhouse, gsc, hostinger, jev, headroom, mcp-fetch/filesystem/git/time, code-review.
- Plugin 131/194, skill 430/658, agent 452/580 atlasta kartı yok (tam liste kacak.json).

## Onay bekleyen (dış çağrı, bu oturumda reddedildi)
- 1× `openrouter/nvidia/nemotron-3-super-120b-a12b:free` metin + 1× `nemotron-3-nano-omni…:free` görsel + 1× ollama `gpt-oss:20b-cloud` — `.kos/kopru/envanter/deneme_groq.py` (model satırları değiştirilerek) ile, en fazla 3 çağrı.
