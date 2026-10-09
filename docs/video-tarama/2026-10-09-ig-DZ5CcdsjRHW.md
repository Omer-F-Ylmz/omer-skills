# GLM-5.2 just dropped open source. 744B parameters, 1M context window, and it goe
## Künye
GLM-5.2 just dropped open source. 744B parameters, 1M context window, and it goe · fullstackparody · süre: 0:00 · ? · https://www.instagram.com/p/DZ5CcdsjRHW/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-30 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 36363 tk · claude-haiku-5-5: claude-haiku-5-5 · 69231 tk
## Özet
Instagram kaydırmalı görsel gönderi (süre yok, 10 görsel): Z.ai'nin açık kaynak GLM-5.2 modelini (744B parametre, 1M bağlam, MIT lisansı) llama.cpp ile yerelde çalıştırma rehberi. Donanım gereksinimleri, llama.cpp derleme, Unsloth 2-bit GGUF indirme, llama-cli ile çalıştırma, llama-server ile OpenAI uyumlu API ve düşünme modları ipucu anlatılıyor. Karşılaştırma değerleri gönderideki görsellerden; bağımsız doğrulanmadı.
## Bölümler
- 0:00 Kapak: GLM-5.2 yerelde çalışır
- 0:00 GLM-5.2 tanıtımı ve benchmark grafiği
- 0:00 Donanım ve nicemleme bellek tablosu
- 0:00 Adım 1: llama.cpp derleme
- 0:00 Adım 2: Model ağırlıklarını indirme
- 0:00 Adım 3: llama-cli ile çalıştırma
- 0:00 Adım 4: llama-server ile OpenAI uyumlu API
- 0:00 Sonuç: terminal çıktısı örneği
- 0:00 Pro ipucu: düşünme modları
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| GLM-5.2 | yok | teknik | yok | Z.ai'nin açık kaynak, MoE mimarili 744B parametreli, 1M bağlamlı modeli; yerelde çalıştırılan ana model | 0:00 | Kapak ve Z.ai sayfasında GLM-5.2 744B Parameters, MIT License yazıyor (karede: Kapakta 'GLM-5.2' büyük başlık; ikinci karede Z.ai model sayfası, 744B Parameters, 1M Context Window, MIT License etiketleri) |
| llama.cpp | yok | CLI | https://github.com/ggml-org/llama.cpp | Modeli yerelde çalıştıran çıkarım motoru; kaynaktan derlenir | 0:00 | git clone https://github.com/ggml-org/llama.cpp ve cmake komutları (karede: Adım 1 terminalinde git clone ve cmake komutları) |
| llama-cli | yok | CLI | yok | llama.cpp'nin etkileşimli sohbet aracı | 0:00 | ./llama.cpp/build/bin/llama-cli --model ... --temp 1.0 (karede: Adım 3 terminalinde llama-cli komutu) |
| llama-server | yok | CLI | yok | OpenAI uyumlu yerel API sunucusu (port 8080) | 0:00 | llama-server --port 8080; localhost:8080/v1/ (karede: Adım 4 terminalinde llama-server komutu) |
| Hugging Face CLI | yok | CLI | yok | Model ağırlıklarını indirmek için hf download | 0:00 | pip install huggingface_hub; hf download unsloth/GLM-5.2-GGUF (karede: Adım 2 terminalinde pip install huggingface_hub ve hf download) |
| Unsloth | yok | teknik | yok | 2-bit dinamik quant (UD-IQ2_M GGUF) sağlayıcısı | 0:00 | Metinde 2-bit dynamic quant from Unsloth; repo unsloth/GLM-5.2-GGUF (karede: Adım 2 metni ve unsloth/GLM-5.2-GGUF) |
| GGUF | yok | teknik | yok | Model ağırlık dosya biçimi | 0:00 | GLM-5.2-UD-IQ2_M-00001-of-00006.gguf (karede: Adım 3 ve 4 terminalinde .gguf dosya adı) |
| CMake | yok | CLI | yok | llama.cpp derleme aracı | 0:00 | cmake llama.cpp -B llama.cpp/build (karede: Adım 1 terminalinde cmake komutları) |
| CUDA | yok | teknik | yok | NVIDIA GPU için derleme bayrağı (-DGGML_CUDA=ON) | 0:00 | -DGGML_CUDA=ON; Mac için OFF (karede: Adım 1 terminalinde -DGGML_CUDA=ON) |
| Apple Metal | yok | teknik | yok | Mac'te varsayılan GPU hızlandırma | 0:00 | Metal support is on by default for Macs; çıktıda Metal = 1 (karede: Adım 1 metni ve sonuç terminalinde Metal = 1) |
| pip | yok | CLI | yok | Python paket yöneticisi, huggingface_hub kurar | 0:00 | $ pip install huggingface_hub (karede: Adım 2 terminalinde pip install) |
| Claude Code | yok | CLI | yok | Yerel GLM-5.2 API'sine bağlanabilecek araç olarak anılıyor | 0:00 | plug GLM-5.2 into Claude Code, Cursor, Continue (karede: Adım 4 metninde vurgulu 'plug GLM-5.2 into Claude Code, Cursor,') |
| Cursor | yok | CLI | yok | Yerel OpenAI uyumlu API'ye bağlanabilecek editör | 0:00 | Adım 4 metninde Cursor anılıyor (karede: Adım 4 metni) |
| Continue | yok | plugin | yok | Yerel API'ye bağlanabilecek geliştirici eklentisi | 0:00 | Adım 4 metninde Continue anılıyor (karede: Adım 4 metni) |
| Claude Opus 4.8 | yok | teknik | yok | Benchmark karşılaştırma modeli | 0:00 | Grafik göstergesinde Claude Opus 4.8 (karede: Grafik göstergesi: GLM-5.2, Claude Opus 4.8, GPT-5.5, Gemini 2.5 Pro, Llama 4 Maverick) |
| GPT-5.5 | yok | teknik | yok | Benchmark karşılaştırma modeli | 0:00 | Kapakta BEATS GPT-5.5; grafik göstergesi (karede: Kapak başlığı ve grafik göstergesi) |
| Gemini 2.5 Pro | yok | teknik | yok | Benchmark karşılaştırma modeli | 0:00 | Grafik göstergesinde Gemini 2.5 Pro (karede: Grafik göstergesi) |
| Llama 4 Maverick | yok | teknik | yok | Benchmark karşılaştırma modeli | 0:00 | Grafik göstergesinde Llama 4 Maverick (karede: Grafik göstergesi) |
| Z.ai | yok | teknik | yok | GLM-5.2 model sayfası ve önerilen ayarların kaynağı | 0:00 | Z.ai model sayfası; recommended settings from Z.ai (karede: Z.ai site başlığı, Model sekmesi, GLM-5.2 sayfası) |
| Mixture-of-Experts | yok | teknik | yok | GLM-5.2 mimarisi | 0:00 | Etiket Mixture-of-Experts; kapakta MoE kodu (karede: Z.ai sayfasında Mixture-of-Experts etiketi) |
| Düşünme modları (--reasoning) | yok | ipucu | yok | --reasoning on/off ve reasoning_effort max ile düşünme kontrolü | 0:00 | llama-cli --reasoning on/off; --chat-template-kwargs reasoning_effort max · kanıt: kare (karede: Pro tip terminalinde üç komut) |
| git | yok | CLI | yok | llama.cpp deposunu yerel makineye klonlamak için kullanılan sürüm kontrol aracı. | 0:00 | $ git clone https://github.com/ggml-org/llama.cpp (karede: Terminal: git clone komutu ilk satırda.) |
| Yerel GLM-5.2 demo sorusu: LRU cache | yok | prompt | yok | Python'da LRU önbelleğini en verimli nasıl uygularım diye soruluyor; model OrderedDict ile O(1) get/put örneği veriyor. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/ggml-org/llama.cpp | llama.cpp deposunu klonlar (karede: Adım 1 terminali) | 0:00 | kare |
| cmake llama.cpp -B llama.cpp/build -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON | CUDA'lı derleme yapılandırması (Mac'te CUDA=OFF) (karede: Adım 1 terminali) | 0:00 | kare |
| cmake --build llama.cpp/build --config Release -j | Release derlemesini paralel yapar (karede: Adım 1 terminali) | 0:00 | kare |
| pip install huggingface_hub | Hugging Face CLI'yi kurar (karede: Adım 2 terminali) | 0:00 | kare |
| hf download unsloth/GLM-5.2-GGUF --local-dir GLM-5.2-GGUF --include "*UD-IQ2_M*" | 2-bit UD-IQ2_M GGUF dosyalarını indirir (karede: Adım 2 terminali) | 0:00 | kare |
| ./llama.cpp/build/bin/llama-cli --model GLM-5.2-GGUF/UD-IQ2_M/GLM-5.2-UD-IQ2_M-00001-of-00006.gguf --temp 1.0 --top-p 0.95 --min-p 0.01 | Modeli yerelde sohbet için çalıştırır (karede: Adım 3 terminali) | 0:00 | kare |
| ./llama.cpp/build/bin/llama-server --model GLM-5.2-GGUF/UD-IQ2_M/GLM-5.2-UD-IQ2_M-00001-of-00006.gguf --port 8080 | localhost:8080/v1/ üzerinde OpenAI uyumlu API açar (karede: Adım 4 terminali) | 0:00 | kare |
| llama-cli --reasoning on | Düşünmeyi açar (varsayılan high) (karede: Pro tip terminali) | 0:00 | kare |
| llama-cli --reasoning off | Hızlı sorgular için düşünmeyi kapatır (karede: Pro tip terminali) | 0:00 | kare |
| llama-cli --chat-template-kwargs '{"reasoning_effort": "max"}' | Zor problemler için maksimum düşünme (karede: Pro tip terminali) | 0:00 | kare |
| # Mac users: set -DGGML_CUDA=OFF | Mac kullanıcılarına CUDA'yı kapatma notu (yorum satırı); komut değil, not. (karede: Slayt 4 Terminal: yeşil/gri yorum satırı 'Mac users: set -DGGML_CUDA=OFF'.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| GLM-5.2 744B parametreli, 1M bağlamlı, MIT lisanslı | 0:00 | özellik |
| Kodlama benchmarklarında Claude Opus ve GPT-5.5 ile başa baş; grafikte LiveCodeBench v5 80.3, SWE-bench 71.4 | 0:00 | karşılaştırma |
| 2-bit sürüm yaklaşık 245GB bellek ister; 1-bit 223GB, 4-bit 475GB, 8-bit 810GB | 0:00 | sayısal |
| 1.51TB model 239GB'a sıkışır, %82 doğruluk korunur | 0:00 | sayısal |
| Önerilen ayarlar temperature 1.0, top-p 0.95 | 0:00 | öneri |
| llama-server ile OpenAI uyumlu yerel API; rate limit yok | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | GLM-5.2 | GLM-5.2 | Kapak başlığı |
| kare 0:00 | Zhipu AI | aday değil: genel kavram | Logo ve ZHIPU AI yazısı (model üreticisi) |
| kare 0:00 | Z.ai | Z.ai | Model sayfası |
| kare 0:00 | GPT-5.5 | GPT-5.5 | Kapak ve grafik |
| kare 0:00 | Claude Opus 4.8 | Claude Opus 4.8 | Grafik göstergesi |
| kare 0:00 | Gemini 2.5 Pro | Gemini 2.5 Pro | Grafik göstergesi |
| kare 0:00 | Llama 4 Maverick | Llama 4 Maverick | Grafik göstergesi |
| kare 0:00 | Mixture-of-Experts | Mixture-of-Experts | Z.ai etiketi |
| kare 0:00 | MIT lisansı | aday değil: genel kavram | Lisans etiketi |
| kare 0:00 | Benchmark adları (LiveCodeBench, SWE-bench, AIME, GPQA, MATH-500, HLE) | aday değil: genel kavram | Grafik eksen etiketleri |
| kare 0:00 | Mac Studio, RTX 3090 | aday değil: genel kavram | Donanım örnekleri; kullanılmıyor |
| kare 0:00 | Nicemleme (1/2/4/8-bit) | aday değil: genel kavram | Bellek tablosu |
| kare 0:00 | llama.cpp | llama.cpp | Adım 1 |
| kare 0:00 | CMake | CMake | Adım 1 komutları |
| kare 0:00 | CUDA | CUDA | -DGGML_CUDA=ON |
| kare 0:00 | Apple Metal | Apple Metal | Adım 1 metni |
| kare 0:00 | pip | pip | Adım 2 |
| kare 0:00 | huggingface_hub / hf | Hugging Face CLI | Adım 2 |
| kare 0:00 | Unsloth | Unsloth | Adım 2 |
| kare 0:00 | GGUF | GGUF | Dosya adı |
| kare 0:00 | llama-cli | llama-cli | Adım 3 |
| kare 0:00 | llama-server | llama-server | Adım 4 |
| kare 0:00 | OpenAI API uyumluluğu | aday değil: genel kavram | Protokol/arayüz tarifi |
| kare 0:00 | Claude Code | Claude Code | Adım 4 |
| kare 0:00 | Cursor | Cursor | Adım 4 |
| kare 0:00 | Continue | Continue | Adım 4 |
| kare 0:00 | OrderedDict LRU cache kodu | aday değil: konu dışı | Demo çıktısı örneği |
| kare 0:00 | --reasoning bayrakları | Düşünme modları (--reasoning) | Pro tip |
| kare 0:00 | @fullstackparody | aday değil: konu dışı | Hesap filigranı |
| kare 0:00 | PyTorch kodu (attention, MoE) | aday değil: konu dışı | Kapak arka plan süsü |
| açıklama | GPT-5, Llama sözlük eşleşmeleri | aday değil: genel kavram | Sözlük eşleşmesi; ilgili modeller GPT-5.5 ve Llama 4 Maverick olarak ele alındı |
| açıklama | Instagram gönderi bağlantısı | aday değil: konu dışı | Gönderinin kendi URL'si |
## Kareden okunanlar
- 1 (kapak): GLM-5.2, ZHIPU AI, @fullstackparody, 'THIS CHINESE AI BEATS GPT-5.5 AND YOU CAN RUN IT ON YOUR OWN MACHINE', SWIPE TO SET IT UP
- 2: Z.ai GLM-5.2 sayfası; grafik: LiveCodeBench v5 80.3, SWE-bench Verified 71.4, AIME 2025 93.6, GPQA 83.2, MATH-500 96.2, HLE 21.6
- 3: Nicemleme tablosu 1-bit 223GB, 2-bit 245GB, 4-bit 475GB, 8-bit 810GB; 256GB Mac Studio, 4x RTX 3090 + 192GB RAM
- 4: Adım 1: git clone ve cmake komutları
- 5: Adım 2: pip install huggingface_hub, hf download unsloth/GLM-5.2-GGUF
- 6: Adım 3: llama-cli --temp 1.0 --top-p 0.95 --min-p 0.01
- 7: Adım 4: llama-server --port 8080
- 8: llama-cli çıktısı: LRU cache yanıtı, 4.02 tokens/s, CPU RAM 38.67 GB, KV cache 234562.34 MB
## Belirsizlikler
- Görsel gönderi; süre yok, tüm zamanlar 0:00 olarak verildi.
- Gönderinin 9. (pro tip) ve 10. görselleri için ekli kare yalnızca 8 tane; 9. görsel yalnız OCR'dan okundu, 10. görsel 8. görselin tekrarı gibi.
- Kapakta devlet başkanı benzeri bir kişi görseli var; parodi hesabı, model/araç ile ilgisi yok.
- GLM-5.2, GPT-5.5, Claude Opus 4.8 ve benchmark değerleri doğrulanmadı; parodi hesap olduğundan iddialar güvenilir olmayabilir.
- Çıktıdaki 4.02 tokens/s ile 228.82 tok/s değerleri tutarsız görünüyor; OCR'da prompt eval ve load time satırları bozuk.
- Komutlarda Mac için CUDA=OFF notu var, Metal bayrağı gösterilmedi.
- Yorumlar girişsiz alınamadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DZ5CcdsjRHW/ | açıklama | açıklama | hayır |
| https://github.com/ggml-org/llama.cpp | 0:00 | ekran | evet |
| localhost:8080/v1/ | 0:00 | ekran | hayır |
| z.ai | 0:00 | ekran | hayır |
## İş akışı
- 1. adım — GLM-5.2'yi Z.ai sayfası ve benchmark grafiğiyle tanıtma — araçlar: GLM-5.2, Z.ai
- 2. adım — Donanım gereksinimini nicemleme tablosuyla gösterme — araçlar: GLM-5.2
- 3. adım — llama.cpp deposunu klonlama — araçlar: llama.cpp
- 4. adım — llama.cpp'yi CUDA ya da Metal ile yapılandırıp derleme — araçlar: CMake, CUDA, Apple Metal
- 5. adım — Hugging Face CLI kurma — araçlar: pip, Hugging Face CLI
- 6. adım — 2-bit Unsloth GGUF ağırlıklarını indirme — araçlar: Hugging Face CLI, Unsloth, GGUF
- 7. adım — Modeli llama-cli ile önerilen örnekleme ayarlarıyla çalıştırma — araçlar: llama-cli, GLM-5.2
- 8. adım — llama-cli çıktısında LRU cache sorusunu ve zamanlamaları kontrol etme — araçlar: llama-cli
- 9. adım — llama-server ile OpenAI uyumlu API başlatma — araçlar: llama-server
- 10. adım — Yerel API'yi Claude Code, Cursor, Continue'a bağlama — araçlar: Claude Code, Cursor, Continue
- 11. adım — Düşünme modunu bayraklarla ayarlama — araçlar: llama-cli, Düşünme modları (--reasoning)
## Promptlar
- Yerel GLM-5.2 demo sorusu: LRU cache — Python'da LRU önbelleğini en verimli nasıl uygularım diye soruluyor; model OrderedDict ile O(1) get/put örneği veriyor.
ikinci göz KAPALI: --ikinci-goz yok
