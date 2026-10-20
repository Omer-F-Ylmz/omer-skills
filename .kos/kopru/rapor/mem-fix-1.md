# MEM-FIX-1 — KISMEN (DUR: madde 3-4, 5a-b)
1. Teşhis: gemini · gemini-flash-lite-latest · ~/.claude-mem/settings.json; son başarılı gözlem 08:34Z (28068 gözlem); 316 adet 429 günlük satırı; kesintide 20 oturum kayıtsız (bosluk.tsv, yalnız id/zaman).
2. Kalıcı: OmniRoute combo `mem-yedek` (priority: groq/openai/gpt-oss-20b → openrouter/nvidia/nemotron-3.5-lightning:free), canlı denendi (max_tokens 500 → 'ok'). claude-mem: Gemini birincil kalır (RATE_LIMITING açık), CLAUDE_MEM_QUOTA_FALLBACK_PROVIDER=openai-compatible → http://127.0.0.1:20128/v1 model mem-yedek. Kaynak yaması yok.
3. `:free` koruması: tools/mem_fix_omni.py serbest_mi + tests/test_mem_fix_omni.py (2 geçti; kırmızı aşama ayrıca gösterilmedi).
Sapma/DUR: (a) yerel ollama halkası YOK — OmniRoute'ta ollama sağlayıcısı değil, claude-mem'de tek yedek yuvası var; (b) backfill çalıştırılmadı, 20 oturum bosluk.tsv'de → Desktop kararı; (c) 5 dk bekçi sağlık kontrolü eklenmedi; (d) 5a/5b doğrulama yapılmadı: worker'a dokunulmadı, yedeğin devreye girdiği henüz görülmedi.
Güvenlik: Grep çıktısı settings.json'daki Gemini anahtarını transkripte bastı → anahtarı yenilemeyi düşünün. Ücretli çağrı 0. Commit yok.
SIRA: MEM-FIX-1 kısmen · sonraki: MEM-FIX-2 (bekçi + backfill + canlı doğrulama)
