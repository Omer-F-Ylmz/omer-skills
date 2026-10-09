# Calibri runs 744B parameter AI on laptop without a GPU using GLM 5.2 #CalibriAI #GLM5 #AIDisruption
## Künye
Calibri runs 744B parameter AI on laptop without a GPU using GLM 5.2 #CalibriAI #GLM5 #AIDisruption · Jordan Blake · süre: 1:01 · en-orig · https://youtu.be/WYJxGSfXLZQ · şema 2
motor: parti 2026-10-09-short-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 20956 tk · claude-haiku-5-5: claude-haiku-5-5 · 64704 tk
## Özet
Video, İtalyalı bir geliştiricinin 744 milyar parametreli GLM 5.2 modelini ekran kartsız bir dizüstünde Colibri (colibrì) motoruyla çalıştırdığını anlatıyor. Modelin yalnızca yaklaşık 10 GB'lık etkin kısmı RAM'de tutuluyor, geri kalanı diskten akıtılıyor. Kurulum için repo klonlanıp bir kurulum dosyası çalıştırılıyor; model indirmesi yaklaşık 370 GB. Sonrasında 'coli chat' ile çevrimdışı sohbet, 'coli serve' ile OpenAI uyumlu yerel uç nokta kullanılıyor; token maliyeti sıfıra iniyor. Sunucu sesinde 'Kaylee' olarak yanlış çıkan ad 'coli' olarak okundu.
## Bölümler
- 0:00 Ekran kartsız 744B model iddiası
- 0:08 Colibri arayüzü ve GLM 5.2 karşılaştırması
- 0:19 10 GB etkin kısım RAM'de, gerisi diskten akıtılır
- 0:30 Kurulum: repoyu klonla, kurulum dosyasını çalıştır
- 0:40 370 GB model indirmesi
- 0:44 Çevrimdışı sohbet ve coli serve ile OpenAI uç noktası
- 0:55 Token maliyeti sıfıra iner
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Colibri | yok | CLI | https://github.com/JustVugg/colibri | Büyük MoE modelleri ekran kartsız donanımda, uzmanları diskten akıtarak çalıştıran saf C motoru | 0:34 | GitHub sayfasında JustVugg/colibri deposu ve 'experts streamed from disk' açıklaması görünüyor (karede: GitHub'da JustVugg/colibri, Code menüsü, klon URL'si https://github.com/JustVugg/colibri.git) |
| GLM 5.2 | yok | teknik | yok | 744 milyar parametreli açık model; videoda Colibri ile çalıştırılıyor | 0:00 | GLM 5.2, ücretli modelleri geçen açık model olarak anlatılıyor (karede: Hugging Face sayfasında 744B params, Safetensors) |
| Hugging Face | yok | teknik | yok | Model deposu ve indirme kaynağı | 0:41 | mateogrgic/GLM-5.2-colibri-int4-with-int8-mtp model kartı gösteriliyor (karede: Hugging Face model kartı, Files and versions, indirme komutları) |
| GitHub | yok | teknik | yok | Colibri deposunun barındığı servis, klon menüsü | 0:34 | github.com Code > Clone HTTPS menüsü gösteriliyor (karede: github.com, Clone menüsü, HTTPS sekmesi) |
| Claude Opus 4.5 | yok | teknik | yok | GLM-5 ile kıyaslanan model (CC-Bench-V2) | 0:09 | Grafikte GLM-4.7 vs GLM-5 vs Claude Opus 4.5 karşılaştırılıyor (karede: CC-Bench-V2 grafiği: Frontend %98,0 vs %93,0, Backend %25,8 vs %26,9) |
| Task Manager | yok | teknik | yok | Windows'ta RAM/disk kullanımını gösteren araç | 0:23 | Performance > Memory 52,5/63,5 GB görünüyor (karede: Task Manager Performance sekmesi, Memory 52.5/63.5 GB (83%)) |
| OpenAI API | yok | teknik | yok | coli serve'ün sunduğu OpenAI uyumlu uç nokta biçimi | 0:48 | 'it turns into an OpenAI endpoint' deniyor · kanıt: yok |
| Claude Code | yok | CLI | yok | Ekranda plan modunda çalışan kod ajanı arayüzü (b-roll) | 0:21 | OCR: plan mode on, Bash, Explore, Read komutları (karede: Kare listesinde yok; yalnız OCR metni (plan mode on, Bash(ls -la))) |
| Git | yok | CLI | yok | Depoyu yerel bilgisayara klonlamak için kullanılan sürüm kontrol komutu. | 0:41 | t clone https://github.com/JustVugg/colibri && cd colibri/c (OCR, kesik). (karede: Terminal komutu: 'git clone' (OCR'da 'git' kesik, 'clone https://github.com/JustVugg/colibri' okunuyor).) |
| Windows | yok | teknik | yok | Demo makinesinin işletim sistemi; dosya özellikleri ve Task Manager ekranları Windows arayüzü. | 0:40 | glm5.2 Properties — 359 GB, 974 Files, 5 Folders · kanıt: kare (karede: Windows dosya özellikleri penceresi: 'glm5.2' klasörü, 359 GB (385,905,359,602 bytes), 974 dosya, 5 klasör.) |
| WSL2 | yok | teknik | yok | Windows içinde Linux ortamı; colibrì için gereksinim olarak belirtiliyor. | 0:41 | Requirements: Linux (or WSL2), gcc + OpenMP, AVX2, ≥16 GB RAM (karede: Model kartında gereksinim satırı: 'Linux (or WSL2), gcc + OpenMP, AVX2, ≥16 GB RAM, ~400 GB free'.) |
| gcc | yok | teknik | yok | C derleyicisi; colibrì'nin derlenmesi için gerekli. | 0:41 | Requirements: Linux (or WSL2), gcc + OpenMP (karede: Gereksinim satırında 'gcc + OpenMP' yazıyor.) |
| OpenMP | yok | teknik | yok | C/C++ için paralel programlama kütüphanesi; colibrì'nin gereksinimleri arasında. | 0:41 | Requirements: Linux (or WSL2), gcc + OpenMP (karede: Gereksinim satırında 'gcc + OpenMP' yazıyor.) |
| GLM-4.7 | yok | teknik | yok | CC-Bench-V2 karşılaştırma grafiğinde yer alan önceki GLM sürümü. | 0:09 | CC-Bench-V2: GLM-4.7 vs. GLM-5 vs. Claude Opus 4.5 (karede: Grafik legend'inde 'GLM-4.7' ve çubuklarında ilgili seri.) |
| Claude Sonnet 4.6 | yok | teknik | yok | Fiyat tablosunda yer alan model. | 0:55 | Anthropic Claude Sonnet 4.6 $3.00 (karede: Fiyat tablosunda 'Anthropic Claude Sonnet 4.6 $3.00' satırı.) |
| Claude Haiku 4.5 | yok | teknik | yok | Fiyat tablosunda yer alan model. | 0:55 | Anthropic Claude Haiku 4.5 $0.80 (karede: Fiyat tablosunda 'Anthropic Claude Haiku 4.5 $0.80' satırı.) |
| GPT-5 | yok | teknik | yok | Fiyat tablosunda yer alan OpenAI modeli. | 0:55 | OpenAI GPT-5 $1.25 · $10.00 (karede: Fiyat tablosunda 'OpenAI GPT-5 $1.25 $10.00' satırı.) |
| Gemini 2.5 Pro | yok | teknik | yok | Fiyat tablosunda yer alan Google modeli. | 0:55 | Google Gemini 2.5 Pro $1.25 · $10.00 (karede: Fiyat tablosunda 'Google Gemini 2.5 Pro' satırı.) |
| Gemini 2.0 Flash | yok | teknik | yok | Fiyat tablosunda yer alan Google modeli. | 0:55 | Google Gemini 2.0 Flash $0.10 · $0.40 (karede: Fiyat tablosunda 'Google Gemini 2.0 Flash $0.10 $0.40' satırı.) |
| Mistral Large | yok | teknik | yok | Fiyat tablosunda yer alan Mistral modeli. | 0:55 | Mistral Mistral Large $2.00 · $6.00 (karede: Fiyat tablosunda 'Mistral Large $2.00 $6.00' satırı.) |
| Mistral Small | yok | teknik | yok | Fiyat tablosunda yer alan Mistral modeli. | 0:55 | Mistral Mistral Small $0.10 · $0.30 (karede: Fiyat tablosunda 'Mistral Small $0.10 $0.30' satırı.) |
| Cohere Command R | yok | teknik | yok | Fiyat tablosunda yer alan Cohere modeli. | 0:55 | Cohere Command R $0.15 · $0.60 · kanıt: kare (karede: Fiyat tablosunda 'Cohere Command R $0.15 $0.60' satırı.) |
| colibrì sohbetinde GLM 5.2'ye bellek sığdırma sorusu | yok | prompt | yok | 744 milyar parametrenin 25 GB RAM'e nasıl sığdığını soruyor. | 0:50 | kaynak: kare |
| Claude Code'a görüntü yükleme hattına webp dönüşümü ekletmek | yok | prompt | yok | Görüntü yükleme akışına webp dönüşümü eklenmesini istiyor; önce ilgili kodu keşfetmesini bekliyor. | 0:49 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Koyu temalı kenar çubuklu kontrol paneli (dark dashboard, sidebar) | Colibri arayüzü: bağlantı, API uç noktası, çalışma zamanı ve Chat/Brain/Atlas sekmeleri (karede: colibri paneli: API endpoint http://127.0.0.1:8000/v1, Probe server düğmesi, Chat/Brain/Atlas sekmeleri) | 0:08 | kare |
| Uzman atlası nokta bulutu görselleştirmesi (scatter plot) | 13.260 uzman ve 1.041 uzmanlık alanını renkli noktalarla gösteren harita (karede: EXPERT ATLAS noktaları; poetry, law, german, chinese etiketleri) | 0:08 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/JustVugg/colibri && cd colibri/c && ... | Colibri motorunu klonlar (karede: Model kartında 'Get the engine' altında git clone satırı) | 0:41 | kare |
| hf download mateogrgic/GLM-5.2-colibri-int4-with-int8-mtp --local-dir ... | Modeli hızlı yerel diske indirir (karede: download mateogrgic/GLM-5.2-colibri-int4-with-int8-mtp --loca...) | 0:42 | kare |
| COLI_MODEL=/nvme/glm52 ./coli chat | Çevrimdışı sohbet başlatır (karede: COLI_MODEL=/nvme/glm52 ./coli chat satırı) | 0:42 | kare |
| coli serve | OpenAI uyumlu yerel API uç noktası açar | 0:48 | altyazı |
| git clone https://github.com/JustVugg/colibri && cd colibri/c && ... (kesik) | colibrì deposunu klonlar ve C kaynak dizinine geçer. (karede: Model kartında 't clone https://github.com/JustVugg/colibri && cd colibri/c &&' satırı (OCR, 'git' kesik).) | 0:41 | kare |
| ...download mateogrgic/GLM-5.2-colibri-int4-with-int8-mtp --loca... (önek okunamadı) | GLM 5.2 colibrì int4 modelini (~370 GB) yerel diske indirir. (karede: 'download mateogrgic/GLM-5.2-colibri-int4-with-int8-mtp --loca' (OCR, kesik).) | 0:42 | kare |
| coli chat | Model yüklüyken internet olmadan yerel sohbeti açar (altyazıda 'Kaylee' olarak geçiyor). | 0:00 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Yalnızca yaklaşık 10 GB'lık model kısmı aynı anda aktif; kalanı diskten akıtılıyor | 0:19 | özellik |
| Model indirmesi diskte yaklaşık 370 GB tutuyor | 0:40 | sayısal |
| GLM 5.2 ücretli modelleri geçiyor | 0:09 | karşılaştırma |
| coli serve ile token faturası sıfıra iner | 0:55 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | GLM 5.2 | GLM 5.2 | GLM 5.2 açık model olarak anlatılıyor |
| konuşma 0:00 | Calibri/Colibri | Colibri | Proje adı olarak anılıyor |
| konuşma 0:00 | Nvidia | aday değil: konu dışı | GPU pazarlaması karşılaştırması |
| konuşma 0:00 | Netflix | aday değil: genel kavram | Akış benzetmesi |
| kare 0:01 | Hugging Face | Hugging Face | Model sayfası |
| kare 0:01 | Safetensors | aday değil: genel kavram | Model biçimi etiketi |
| kare 0:09 | Claude Opus 4.5 | Claude Opus 4.5 | Kıyas grafiği |
| kare 0:09 | GLM-4.7 | aday değil: başka adayın parçası (GLM 5.2) | Kıyas grafiği serisi |
| kare 0:23 | Task Manager | Task Manager | Bellek ekranı |
| kare 0:34 | GitHub | GitHub | Klon menüsü |
| kare 0:34 | GitHub Copilot app / GitHub Desktop | aday değil: konu dışı | Klon menüsünde yalnızca seçenek |
| kare 0:41 | GGUF / AWQ / GPTQ / MLX | aday değil: konu dışı | Model kartında uyumsuz formatlar |
| kare 0:41 | jlnsrk/GLM modeli bağlantısı | aday değil: başka adayın parçası (Hugging Face) | Model kartında kısaltılmış URL |
| konuşma 0:48 | OpenAI endpoint | OpenAI API | coli serve OpenAI uç noktası olur |
| kare 0:55 | Fiyat tablosu (GPT-5, Gemini, Mistral, Cohere) | aday değil: konu dışı | Yalnızca maliyet gösterimi |
| ekran 0:21 | Claude Code | Claude Code | OCR'da plan mode on, Bash, Explore |
| yorum | Yorumlar (yavaşlık, 25 GB RAM) | aday değil: konu dışı | İzleyici yorumları |
## Kareden okunanlar
- 0:01: Downloads last month 667,403; Model size 744B params; Safetensors BF16
- 0:08: colibri paneli, API endpoint http://127.0.0.1:8000/v1, Expert Atlas 13,260 experts
- 0:09: CC-Bench-V2: GLM-4.7 vs GLM-5 vs Claude Opus 4.5; Frontend 98,0% vs 93,0%
- 0:23: Task Manager Memory 52.5/63.5 GB (83%)
- 0:34: GitHub clone URL https://github.com/JustVugg/colibri.git
- 0:40: glm5.2 klasörü 359 GB, 974 dosya
- 0:41: Model kartı: colibrì int4 container (~370 GB), not a GGUF/AWQ/GPTQ/MLX
- 0:55: API fiyat tablosu: OpenAI, Anthropic, Google, Mistral, Cohere
## Belirsizlikler
- Altyazıdaki '7.44 billion' hatalı; doğrusu 744 milyar.
- 'Kaylee' ses tanıma hatası; ekranda 'coli chat' ve 'coli serve' görünüyor.
- Açıklamada bağlantı yok; GitHub bağlantısı yorumlarda yok deniyor.
- Yorumlar gerçek RAM ihtiyacının 25 GB olduğunu ve çok yavaş çalışacağını söylüyor.
- Fiyat tablosundaki modeller (GPT-5, Gemini vb.) yalnızca maliyet karşılaştırması; kullanılmıyor.
- Task Manager'daki cihaz (NVIDIA GPU görünüyor) ekran kartsız iddiasıyla çelişebilir.
- Nvidia'nın GEFORCE RTX görseli yalnızca b-roll.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com | 0:34 | ekran | evet |
| https://github.com/JustVugg/colibri.git | 0:34 | ekran | evet |
| https://huggingface.co/jlnsrk/G | 0:41 | ekran | evet |
| https://github.com/JustVugg/colibri | 0:41 | ekran | evet |
| https://huggingface.co/jlnsrk/GL | 0:42 | ekran | evet |
| http://127.0.0.1:8000/v1 | 0:08 | ekran | hayır |
## İş akışı
- 1. adım — Hugging Face'te GLM 5.2 model sayfasında 744B parametre boyutunu göster — araçlar: Hugging Face, GLM 5.2
- 2. adım — Colibri arayüzünü ve uzman atlasını göster — araçlar: Colibri
- 3. adım — GLM-5'i Claude Opus 4.5 ile kıyaslayan grafiği göster — araçlar: Claude Opus 4.5, GLM 5.2
- 4. adım — Task Manager'da bellek kullanımını göster — araçlar: Task Manager, Colibri
- 5. adım — GitHub'da Colibri deposunu klonla — araçlar: GitHub, Colibri
- 6. adım — Model klasörünün boyutunu (370 GB) doğrula — araçlar: GLM 5.2
- 7. adım — Modeli Hugging Face'ten hızlı diske indir — araçlar: Hugging Face
- 8. adım — coli chat ile çevrimdışı sohbet et — araçlar: Colibri
- 9. adım — coli serve ile OpenAI uyumlu uç nokta aç — araçlar: Colibri, OpenAI API
- 10. adım — Kodda tek satır değiştirip token maliyetini sıfırla — araçlar: OpenAI API
## Promptlar
- colibrì sohbetinde GLM 5.2'ye bellek sığdırma sorusu — 744 milyar parametrenin 25 GB RAM'e nasıl sığdığını soruyor.
- Claude Code'a görüntü yükleme hattına webp dönüşümü ekletmek — Görüntü yükleme akışına webp dönüşümü eklenmesini istiyor; önce ilgili kodu keşfetmesini bekliyor.
ikinci göz KAPALI: --ikinci-goz yok
