# Bilinen hatalar

| belirti | çözüm |
|---|---|
| torch CPU'ya düştü | `uv pip install torch --index-url .../cu128` |
| HF snapshot asılıyor | `allow_patterns` ile parça parça, `HF_HUB_ENABLE_HF_TRANSFER=1` |
| GGUF `header cok buyuk` | deneme boylarını 128'e çıkar |
| 4B indirilemedi | arka planda bırak, ölçümü 0.8B'de yap |
| tüm cevaplar "boş" | düşünen model: `--reasoning-budget 0`, `content` yoksa `reasoning_content` oku |
| `n_gpu_layers already set, abort` | model VRAM'e sığmıyor, CPU'da çalışır: `--n-cpu-moe` kullan |
| GGUF'ta ret geri geldi | üst kuant, yoksa B4'e dön |
| 12 GB OOM | bnb-4bit + `--lora`, ya da bulut |
| vekil 502 | llama-server ölü, yeniden başlat |
| katman yolu kırık (Qwen) | `model.language_model.layers` üzerinden soyutla |
