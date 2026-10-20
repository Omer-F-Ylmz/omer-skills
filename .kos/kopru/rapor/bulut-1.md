BULUT-1: yerel ollama zincirlerden çıktı; 10 dk boyunca llama-server yok (3 ölçüm 0).
1. Çağıranlar: tools/mem_fix_omni.py:13 (mem-yedek), tools/yonlendir.py:24 (T1), tools/ucuz_alt.py:32-34 (gpt-oss:20b-cloud, RAM≥%80'de atlanır; yerel değil), tools/video/video/ucuz.py:5 (gpt-oss:120b-cloud varsayılan), cli.py:1571 whisper.cpp. server.log: qwen3.5:4b 64k ctx, claude-mem/mem-yedek kaynaklı.
2. mem-yedek yeniden kuruldu: nemotron-3.5-lightning:free → gemma-4-31b:free → nemotron-3-super:free → Groq son. yonlendir T1: Gemini → nemotron :free → Groq → Haiku. Testler 7+4 yeşil.
3. Halka sağlığı: Groq 200 · GitHub Models (gh, openai/gpt-4.1-mini) 200 · Gemini 429 (günlük kota, 3.5-flash-lite) · OmniRoute gemini bağlantısı 401 (anahtar geçersiz) · nemotron-super :free zaman aşımı. Halka başına dakika tavanı eklenmedi (OmniRoute'ta ayar yok).
4. Whisper: Groq zaten birincil (cli.py:1590); yerel whisper.cpp artık RAM ≥%70 ise atlanıyor.
5. mem_bekci.py: her turda yüklü ollama modelini boşaltır, çağıranı ram-olay.log'a yazar. OLLAMA_KEEP_ALIVE=0 (kullanıcı ortamı) ayarlandı.
6. Kanıt: (b) geçersiz Gemini → 400 → Groq gpt-oss-120b yanıtladı; mem-yedek 200 (groq/gpt-oss-20b); (c) 3×0; (d) gözlem 29445→29446.
Ömer: Cerebras / Mistral / Ollama Cloud hesapları açılmadı, anahtarlar yok, yapılandırma hazırlanmadı (resmi koşullar doğrulanmadı). Hesap açınca anahtarı CEREBRAS_API_KEY / MISTRAL_API_KEY / OLLAMA_API_KEY'e koy. Gemini anahtarını AI Studio'dan yenile, OmniRoute'taki gemini bağlantısını güncelle. GitHub Models OmniRoute'a bağlanmadı.
SIRA: bulut-1 KAPANDI (GitHub Models/Gemini OmniRoute bağlantısı açık)
