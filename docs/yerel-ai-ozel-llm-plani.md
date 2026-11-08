# Yerel-AI: kendi verimizle ozel LLM (8 GB VRAM) - kisa plan
Kaynak: IG p/De7OUe0I6jB (@raycfu). Yalniz yerel-ai alani; sosyal/marka hattina baglanmaz.
1. Model: Qwen2.5-1.5B veya SmolLM2-1.7B (Apache-2.0), 4-bit ~1 GB. 7B de QLoRA ile 8 GB'a sigar (kisa dizi, batch 1, gradient checkpointing); 27B sigmaz.
2. Veri: 300-1000 elle onayli temiz ornek (JSONL, talimat/yanit); kalite>miktar; kisisel/musteri verisi ve sirlar disarida.
3. Egitim: transformers + peft + trl + bitsandbytes (nf4), LoraConfig r=16, target all-linear; VRAM<=%80 (~9.8 GB tavan), RAM<=%89; 1.5B icin dakikalar.
4. Servis: LoRA birlestir -> GGUF (llama.cpp convert) -> Ollama Modelfile; yerel, API ucreti yok.
5. Olcum: ayri 50 ornekli degerlendirme seti, taban modele karsi kor karsilastirma; kazanc yoksa dur.
Durum: plan; kurulum/egitim bu dalgada yapilmadi (video iddialari - $2, 11 dk - dogrulanmadi).
