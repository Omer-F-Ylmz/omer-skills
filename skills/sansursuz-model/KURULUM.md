# Kurulum

1. Paket metnini `C:\Users\pc\Desktop\UNCLLM\sansursuz-v3.md` olarak kaydet (UTF-8).
2. Kurulum komutunu PowerShell'de çalıştır — dosyaları `.claude\skills` ve depoya açar, zip üretir.
3. Claude Code'u kapat-aç. claude.ai'de eski skill'i sil, `sansursuz-v3.zip` yükle.
4. `sablon/tercih-blogu.md` içeriğini Ayarlar > Profil > Claude'a talimatlar alanına yapıştır.
5. Kapı D: `istem/kural-testleri.jsonl` 30 istem, hard ret 0 olana kadar kural ekle.

Bağımlılıklar (yalnız Mod B): Python 3.12, uv, torch cu128, transformers, safetensors, numpy, accelerate, bitsandbytes, llama.cpp b12063+.
