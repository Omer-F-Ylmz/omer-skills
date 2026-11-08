# Bilinen hatalar (bu oturumda gerçekten oldu)

| belirti | neden | çözüm |
|---|---|---|
| `uv tool install heretic-llm` sonrası torch CPU | PyPI wheel CPU | `uv pip install torch --index-url .../cu128` (torch.log) |
| HF snapshot 11 dosyada 26 dk asılıyor | büyük shard, 7 MB/s | `allow_patterns` ile shard shard, `HF_HUB_ENABLE_HF_TRANSFER=1` |
| `header cok buyuk` / struct.error | GGUF başlığı 16 MB'ı aşıyor | `header()` deneme boylarını 128'e çıkar; ya da yerel dosyayı oku |
| 4B ikilisi indirilemedi | 60 tur bütçesi + hız | `ss3_indir.py`'yi arka planda bırak, ölçümü 0.8B'de yap, 4B'yi sonra |
| 35B uzman ölçümü yarım | Q8_0 38 GB, seçili desen az | desen listesine `ffn_down_exps` ekle, `ThreadPoolExecutor` 4 → 2 |
| `model.model.layers` yolu kırık (Qwen) | özel uygulama | katman yolunu `model.language_model.layers` üzerinden soyutla |
| GGUF'ta ret geri geldi | kuant gürültüsü | bir üst kuant, yoksa 4'e dön (güç zayıf) |
| 12 GB'da OOM | model sığmıyor | bnb-4bit + `--lora`, sonra birleştir; ya da bulut |
| vekil 8081'de 502 | llama-server ölü | sunucuyu yeniden başlat, `/health` bekle, sonra istek |
| düşünen modelde ret ölçülmüyor | cevap `thinking` içinde bitiyor | `max_tokens` 2000, düşünme bloğunu at, iki konumda ölç |
