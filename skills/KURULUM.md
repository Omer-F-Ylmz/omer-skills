# Kurulum

## Claude Code / claude.ai
1. Zip'i `C:\Projeler\omer-skills\skills\` altına aç → `skills\sansursuz-model\SKILL.md` oluşur.
2. claude.ai için: zip'i Ayarlar > Yetenekler > Skill yükle ile ver (zip kökünde SKILL.md var, doğrudan kabul edilir).
3. Skill adı `sansursuz-model`; "sansürsüz model", "abliterate", "model reddediyor" gibi tetiklerle açılır.

## Bağımlılıklar
- Python 3.12, uv, torch cu128, transformers, safetensors, numpy, accelerate, bitsandbytes, datasets
- llama.cpp b12063+ (convert, quantize, server, cvector-generator)
- Modal ya da Kaggle hesabı (yalnız 12 GB VRAM'e sığmayan modeller için)

## İlk koşu
```bash
python betik/ret_olc.py --url http://127.0.0.1:8080 --set ret --n 20   # duman testi
```
20 istemde sınıflandırıcı mantıklı görünüyorsa 300'e çık.
