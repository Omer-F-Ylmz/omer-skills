# Ekran kartı olmadan yapay zeka modellerini yerel cihazda çevrimdışı çalıştırmanın yolu: Colibri!
## Künye
Ekran kartı olmadan yapay zeka modellerini yerel cihazda çevrimdışı çalıştırmanın yolu: Colibri! · Esad Kılıç · süre: 0:48 · tr-orig · https://youtu.be/qvjZnWfbW0Y · şema 2
motor: parti 2026-10-09-short-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 17303 tk · claude-haiku-5-5: claude-haiku-5-5 · 33319 tk
## Özet
48 saniyelik kısa video: İtalyan bir yazılımcının Colibri projesiyle GLM-5.2 (744B MoE) modelini ekran kartı olmadan, ~25 GB RAM'li bir laptopta çevrimdışı çalıştırdığı anlatılıyor. Colibri saf C ile yazılmış; uzmanları (experts) diskten akış (streaming) ile okuyor. Kurulum: repoyu klonla, setup.sh çalıştır, modeli indir, Colibri'ye yönlendir. Yorumlar hız (çok düşük token/sn) ve ~370-430 GB disk ihtiyacı nedeniyle abartıyı eleştiriyor.
## Bölümler
- 0:00 Giriş: GPU'suz GLM 5.2 iddiası
- 0:21 Colibri projesi ve GitHub reposu
- 0:26 Klonlama ve setup.sh ile derleme
- 0:34 Modeli indirme ve Colibri'ye yönlendirme
- 0:38 Çevrimdışı çalıştırma ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Colibri | yok | CLI | yok | Saf C ile yazılmış, MoE uzmanlarını diskten akıtarak büyük modeli CPU'da çalıştıran motor | 0:21 | Konuşmada 'Projenin adı Kolibri' geçiyor; README'de colibri başlığı görülüyor. (karede: GitHub README sayfası, colibrì logosu, 'Tiny engine, immense model. Run GLM-5.2 (744B-parameter MoE)...' metni) |
| GLM-5.2 | yok | CLI | yok | Colibri ile çalıştırılan ücretsiz 744B parametreli MoE yapay zekâ modeli | 0:08 | Kare ve konuşmada 'GLM 5.2'yi aldı' deniyor. (karede: Beyaz zeminde 'GLM-5.2' yazısı ve '24-Hour Tasks. 1M Context' alt metni) |
| GitHub | yok | iş akışı | yok | Colibri reposunun barındığı ve klonlandığı platform | 0:15 | Ekranda GITHUB yazısı ve repo sayfası görülüyor. (karede: Çoklu monitörlü kod ekranında GITHUB etiketi; sonraki karelerde repo sayfası) |
| setup.sh | yok | CLI | yok | Colibri'yi derleyen kurulum betiği | 0:27 | 'orada setup. dosyasını çalıştırıyorsun ve orada tamamen kendini derliyor' |
| llama.cpp | yok | teknik | yok | Colibri ile karşılaştırılan, mmap ile işletim sisteminin tahminine dayanan yaklaşım | 0:35 | Karşılaştırma animasyonunda 'llama.cpp already does this' balonu. (karede: 'MMAP · THE OS GUESSING' ve 'COLIBRI · THE ROUTER KNOWS' diyagramı, 'llama.cpp already does this' etiketi, EPU/ROUTER/SSD kutuları) |
| Mixture-of-Experts | yok | teknik | yok | Token başına yalnız küçük bir uzman alt kümesini etkinleştiren model mimarisi | 0:26 | README'de '744B Mixture-of-Experts model activates only ~40B parameters per token' yazıyor. (karede: README 'The idea' bölümü, MoE açıklaması) |
| LRU önbellek | yok | teknik | yok | Katman başına LRU önbellekle uzmanları diskten akıtma | 0:26 | README'de 'per-layer LRU cache' ifadesi geçiyor. · kanıt: kare (karede: README metni: 'streamed on demand, with a per-layer LRU cache') |
| int4 | yok | teknik | yok | Uzmanların 4 bit nicemleme ile saklanması | 0:26 | README'de 'int4' ve 'resident 9.9 GB' geçiyor. (karede: README başlığında 'GLM-5.2 · 744B MoE · int4 · streaming CPU') |
| MLA attention | yok | teknik | yok | README'de uygulanan özellikler arasında listelenen dikkat mekanizması | 0:26 | 'MLA attention' maddesi README'de görülüyor. · kanıt: kare (karede: 'What's implemented' listesinde 'MLA attent...' satırı) |
| C | yok | teknik | yok | Motorun yazıldığı dil; tek C dosyası, BLAS ve Python'suz | 0:26 | 'The engine is a single C file (c/glm.c, ~2,400 lines)' (karede: README'de 'The engine is a single C file' cümlesi ve Languages paneli) |
| CUDA | yok | teknik | yok | İsteğe bağlı sabitlenmiş uzmanlar için opsiyonel GPU katmanı | 0:26 | README'de 'an opt-in CUDA tier for pinned experts exists'. (karede: README satırı: 'required (an opt-in CUDA tier for pinned experts exists — see below)') |
| git | yok | CLI | yok | Repoyu yerel bilgisayara klonlamak için kullanılan sürüm kontrol komut satırı aracı. | 0:00 | Tek yapman gereken şey bu repoyu klonlıyorsun. · kanıt: yok |
| MMAP | yok | teknik | yok | İşletim sisteminin dosyayı bellek adres alanına eşlemesi (memory mapping); videoda llama.cpp yaklaşımı olarak gösteriliyor. | 0:35 | 'MMAP · THE OS GUESSING' etiketi, SSD ve tek şeritli şema. (karede: Üstte 'MMAP · THE OS GUESSING' başlığı, altta tek bir SSD çubuğu; karşılaştırma için 'COLIBRI · THE ROUTER KNOWS' şeması.) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone <Colibri reposu> | Colibri reposunu klonlar | 0:26 | altyazı |
| setup.sh | Colibri'yi kendiliğinden derler (karede: Altyazıda 'setup.sh dosyasını'; ekran metninde setup.sh) | 0:27 | kare |
| git clone <repo-adresi> | Colibri reposunu yerel bilgisayara klonlar (adres videoda gösterilmiyor). | 0:00 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| GLM-5.2 ekran kartı olmayan, yalnızca 25 GB RAM'li bir laptopta çalıştırıldı | 0:00 | sayısal |
| Colibri tamamen çevrimdışı çalışıyor ve kod herkese açık | 0:38 | özellik |
| 744B MoE model token başına yalnız ~40B parametre etkinleştiriyor | 0:26 | sayısal |
| Motor tek C dosyası, yaklaşık 2.400 satır; BLAS ve Python yok | 0:26 | sayısal |
| Yorum: model ~370-430 GB NVMe disk istiyor, sıradan laptop değil | açıklama | karşılaştırma |
| Yorum: hız çok düşük; Ryzen 9 9950X ≈0,28, M5 Max ≈1,06 token/sn | açıklama | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | NVIDIA / CEO | aday değil: konu dışı | NVIDIA'nın CEO'su dün uyuyamadı |
| konuşma 0:00 | GPU / ekran kartı | aday değil: genel kavram | Nvidia'nın GPU'larını kullanmadan |
| kare 0:08 | GLM-5.2 | GLM-5.2 | GLM-5.2 logosu |
| kare 0:15 | GitHub | GitHub | GITHUB etiketi ve repo |
| konuşma 0:21 | Colibri | Colibri | Projenin adı Kolibri |
| kare 0:23 | Unified Memory | aday değil: genel kavram | UNIFIED MEMORY etiketi |
| kare 0:26 | Mixture-of-Experts | Mixture-of-Experts | README MoE açıklaması |
| kare 0:26 | LRU cache | LRU önbellek | per-layer LRU cache |
| kare 0:26 | int4 | int4 | README başlığı int4 |
| kare 0:26 | MLA attention | MLA attention | What's implemented listesi |
| kare 0:26 | C dili | C | single C file |
| kare 0:26 | CUDA | CUDA | opt-in CUDA tier |
| kare 0:26 | Python | aday değil: konu dışı | README 'no Python at runtime' diyor, kullanılmıyor |
| kare 0:26 | BLAS | aday değil: konu dışı | 'No BLAS' olarak anılıyor, kullanılmıyor |
| kare 0:26 | Apache-2.0 license | aday değil: konu dışı | Lisans etiketi |
| konuşma 0:27 | setup.sh | setup.sh | setup.sh dosyasını çalıştırıyorsun |
| kare 0:35 | llama.cpp | llama.cpp | llama.cpp already does this |
| kare 0:35 | mmap | aday değil: genel kavram | MMAP · THE OS GUESSING |
| yorum | Cursor | aday değil: konu dışı | Sözlük eşleşmesi, videoda gösterilmiyor |
| yorum | Ollama | aday değil: konu dışı | Sözlük eşleşmesi, videoda gösterilmiyor |
| yorum | Qwen3.6 35B, OLMoE 7B | aday değil: konu dışı | Yorumda küçük modeller olarak anılıyor, videoda gösterilmiyor |
| yorum | Ryzen 9 9950X, Apple M5 Max, Ryzen AI Max+ 395 | aday değil: konu dışı | Yorumda donanım hız karşılaştırması |
## Kareden okunanlar
- 0:08: 'GLM-5.2' logosu, '24-Hour Tasks. 1M Context' alt yazısı
- 0:15: Çoklu monitörlü geliştirici sahnesi, GITHUB etiketi
- 0:23: 'REFUSES TO LOAD' damgası, 'UNIFIED MEMORY' etiketi
- 0:25: Colibri GitHub README: 'The idea', 'What's implemented', Languages paneli
- 0:26: README: single C file, 21,504 routed experts, Apache-2.0 license
- 0:32: GLM-5.2 tanıtım ekranı: 'DATA LINK : ACTIVE', '1M Context', 'Native Multi-Pla'
- 0:33: Aynı tanıtım ekranı, 'GLM-5.2' yazısı belirginleşiyor
- 0:35: 'MMAP · THE OS GUESSING' ve 'COLIBRI · THE ROUTER KNOWS' diyagramı, 'llama.cpp already does this'
## Belirsizlikler
- Repo URL'si videoda yok; yorumda paylaşılacağı söyleniyor.
- Videoda 25 GB RAM iddiası var, yorumlar disk ve hız sınırlarını eleştiriyor; hız doğrulanmadı.
- Yapay zeka CEO iddiası (Nvidia CEO'su uyuyamadı) abartılı görünüyor.
- Sözlük eşleşmeleri Cursor ve Ollama yalnız yorumda; videoda gösterilmiyor.
- Altyazıda 'CLM5.2' otomatik altyazı hatası; GLM-5.2 anlaşılıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| setup.sh | 0:27 | ekran | hayır |
## İş akışı
- yok
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
