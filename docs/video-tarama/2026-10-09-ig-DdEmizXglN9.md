# Yorumlara YEREL yaz ✅, cihazında hangi modelin çalışacağını bulduğun rehberi DM’
## Künye
Yorumlara YEREL yaz ✅, cihazında hangi modelin çalışacağını bulduğun rehberi DM’ · benburhankocabiyik · süre: 0:00 · ? · https://www.instagram.com/p/DdEmizXglN9/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-31 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 29665 tk · claude-haiku-5-5: claude-haiku-5-5 · 42987 tk
## Özet
Görsel (karusel) gönderi: Cihazında hangi yerel yapay zekâ modelinin rahat çalışacağını bulmanın üç yolu anlatılıyor. Yol 1: donanım ekran görüntüsünü ChatGPT/Claude'a yükleyip prompt ile sormak. Yol 2: uv kurup uvx whichllm@latest ile sistemi taratmak, whichllm run ile model indirip sohbet etmek. Yol 3: terminalsiz LM Studio ile model aramak. Uyarı: büyük model teknik olarak çalışsa da çok yavaş olabilir. Yorumlara YEREL yazana rehber DM'den gönderilecek.
## Bölümler
- 0:00 Giriş: Hangi modeller cihazında çalışır?
- 0:00 Yerelde yapay zekâ çalıştırmak ne demek?
- 0:00 Yol 1: Ekran görüntüsü + prompt ile ChatGPT/Claude'a sor
- 0:00 Yol 2: WhichLLM (terminal, uv kurulumu, uvx whichllm@latest, whichllm run)
- 0:00 Yol 3: LM Studio
- 0:00 Akılda tutulacak: çalışıyor ≠ kullanılabilir
- 0:00 Yoruma YEREL yaz, DM ile rehber
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| WhichLLM | yok | CLI | yok | CPU, GPU ve belleği tarayıp donanıma uygun yerel modelleri önerir; model adı, bellek ihtiyacı, tahmini hız gösterir | 0:00 | WhichLLM, işlemcinizi, ekran kartınızı ve belleğinizi otomatik olarak analiz eder (karede: Yol 2 başlığı ve WhichLLM açıklaması; ayrıca uvx whichllm@latest komutu ve 'Yaz sadece: whichllm run' kareleri) |
| uv | yok | CLI | yok | Astral'ın Python paket/araç yöneticisi; uvx ile whichllm çalıştırmak için kurulur | 0:00 | Şimdi, uv adında küçük bir araç kuracağız (karede: 'Şimdi, uv adında küçük bir araç kuracağız' ve Windows/Mac kurulum komut kutuları) |
| LM Studio | yok | CLI | yok | Terminalsiz masaüstü uygulaması; uygun yerel model arar, indirir, uygulama içinde sohbet ettirir | 0:00 | LM Studio'yu kullan. LM Studio'yu indir. (karede: Yol 3 listesi: 'LM Studio'yu kullan', indir, uygun modeli ara, sohbet et) |
| ChatGPT | yok | iş akışı | yok | Donanım ekran görüntüsü yüklenip hangi modellerin çalışacağı soruluyor | 0:00 | ChatGPT veya Claude'a yükle ve şu prompt'u ekle (karede: Yol 1 kare: 'ChatGPT veya Claude'a yükle' ve koyu sohbet arayüzü çizimi, 'Bugün aklında ne var?') |
| Claude | yok | iş akışı | yok | ChatGPT alternatifi olarak ekran görüntüsünden donanım okutup model önerisi alma | 0:00 | ChatGPT veya Claude'a yükle (karede: Yol 1 kare metni ve 2. karede 'ChatGPT veya Claude kullanırken') |
| Terminal | yok | CLI | yok | Windows/Mac terminalinde komutlar yapıştırılarak WhichLLM çalıştırılır | 0:00 | Terminal'i açın. Karşınıza siyah bir ekran çıkacak. (karede: Yol 2 kare: Terminal'i açın adımı ve siyah terminal kapısı çizimi) |
| PowerShell | yok | CLI | yok | Windows'ta uv kurulum komutunu çalıştırır | 0:00 | powershell -ExecutionPolicy ByPass -c · kanıt: kare (karede: Windows kutusunda powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 / iex") |
| curl | yok | CLI | yok | Mac'te uv kurulum betiğini indirir | 0:00 | curl -LsSf https://astral.sh/uv/install.sh / sh (karede: Mac kutusunda curl -LsSf https://astral.sh/uv/install.sh / sh) |
| uvx | yok | CLI | yok | uv ile araçları kurmadan çalıştıran komut; whichllm@latest çalıştırır | 0:00 | uvx whichllm@latest (karede: Kutuda 'uvx whichllm@latest' ve Enter tuşu) |
| Kuantizasyon | yok | teknik | yok | Prompt'ta dizüstü için en iyi sürüm/kuantizasyon isteniyor | 0:00 | Dizüstüm için en iyi sürüm/kuantizasyon (karede: Yol 1 kare, prompt maddeleri arasında 'Dizüstüm için en iyi sürüm/kuantizasyon') |
| Donanım ekran görüntüsünden yerel çalışabilecek modelleri belirletme | yok | prompt | yok | Yerel olarak bu dizüstünde çalışabilecek yapay zekâ modellerini çalıştırmak istiyorum. Ekran görüntüsünden donanım özelliklerimi oku. Model adı, dizüstüm için en iyi sürüm/kuantizasyon, performans beklentisi (hızlı/idare eder/yavaş) ver. Yalnızca yerelde çalıştırabileceğim modelleri öner. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 / iex" | Windows'ta uv'yi kurar (karede: 5. kare Windows kutusu) | 0:00 | kare |
| curl -LsSf https://astral.sh/uv/install.sh / sh | Mac'te uv'yi kurar (karede: 5. kare Mac kutusu) | 0:00 | kare |
| uvx whichllm@latest | WhichLLM'i son sürümle çalıştırıp donanımı tarar, uygun modelleri listeler (karede: 6. kare komut kutusu ve Enter tuşu) | 0:00 | kare |
| whichllm run | Uygun modeli seçip indirir ve yerelde sohbet başlatır (karede: 7. kare: 'Yaz sadece: whichllm run') | 0:00 | kare |
| powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.psl / iex" | Windows'ta uv kurulum betiğini indirip PowerShell üzerinden çalıştırır (script adı ekranda 'install.psl' olarak okunuyor). (karede: Kare 5: Windows kutusunda bu komut yazılı.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Büyük model teknik olarak çalışabilir ama acı verici derecede yavaş olabilir; çalışıyor demek kullanılabilir demek değil | açıklama | öneri |
| WhichLLM işlemci, ekran kartı ve belleği otomatik analiz edip uygun modelleri önerir | 0:00 | özellik |
| Yerel çalıştırmada internet gerekmez, dosyalar cihazda kalır, mesaj başına ücret ödenmez | 0:00 | özellik |
| whichllm run uygun modeli seçip indirir ve yerelde sohbet başlatır | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 · 0:00 | Hangi yapay zekâ modelleri cihazda çalışır başlığı | aday değil: genel kavram | Hangi Yapay Zeka Modellerini Cihazında Çalıştırabilirsin? |
| kare 2 · 0:00 | Yerel yapay zekâ kavramı | aday değil: genel kavram | Yapay zekâyı yerelde çalıştırmak ise şunu ifade eder |
| kare 2 · 0:00 | ChatGPT | ChatGPT | Genelde, ChatGPT veya Claude kullanırken |
| kare 2 · 0:00 | Claude | Claude | Genelde, ChatGPT veya Claude kullanırken |
| kare 3 · 0:00 | Windows Ayarlar / Mac Bu Mac hakkında | aday değil: genel kavram | Windows'ta: Ayarlar → Bu bilgisayar hakkında |
| kare 3 · 0:00 | Kuantizasyon | Kuantizasyon | en iyi sürüm/kuantizasyon |
| kare 3 · 0:00 | Ekran görüntüsü yükleme + prompt | ChatGPT | ChatGPT veya Claude'a yükle ve şu prompt'u ekle |
| kare 4 · 0:00 | WhichLLM | WhichLLM | WhichLLM, işlemcinizi, ekran kartınızı ve belleğinizi analiz eder |
| kare 4 · 0:00 | Terminal | Terminal | Terminal'i açın. |
| kare 5 · 0:00 | uv | uv | Şimdi, uv adında küçük bir araç kuracağız |
| kare 5 · 0:00 | PowerShell komutu | PowerShell | powershell -ExecutionPolicy ByPass -c |
| kare 5 · 0:00 | curl komutu | curl | curl -LsSf https://astral.sh/uv/install.sh / sh |
| kare 5 · 0:00 | astral.sh URL'leri | uv | https://astral.sh/uv/install.ps1 ve install.sh |
| kare 6 · 0:00 | uvx whichllm@latest | uvx | uvx whichllm@latest |
| kare 7 · 0:00 | whichllm run | WhichLLM | Yaz sadece: whichllm run |
| kare 8 · 0:00 | LM Studio | LM Studio | LM Studio'yu kullan. |
| OCR görsel 9 · 0:00 | Hız uyarısı | aday değil: genel kavram | büyük bir modeli teknik olarak çalıştırabilir ama acı verici derecede yavaş |
| OCR görsel 10 · 0:00 | YEREL yorum çağrısı | aday değil: konu dışı | Yoruma YEREL yaz, bağlantıları ve promptu göndereyim |
| açıklama | Terminal tek komutla tarama | WhichLLM | terminale tek komutla sistemini taratmak |
| açıklama | Masaüstü uygulamasından arama | LM Studio | hiç terminale dokunmadan masaüstü uygulamasından aramak |
| sözlük: Git | 'Git' sözlük eşleşmesi | aday değil: konu dışı | açıklamada 'Hangi yoldan gidersen git' fiili |
## Kareden okunanlar
- 1: Başlık: Hangi Yapay Zeka Modellerini Cihazında Çalıştırabilirsin? İşte nasıl öğrenebileceğin; laptop içinde AI kutuları çizimi
- 2: Yerelde yapay zekâ çalıştırmak ne demek; bulut/ChatGPT-Claude ile yerel karşılaştırma
- 3: Yol 1: Windows Ayarlar → Bu bilgisayar hakkında, Mac Apple logosu → Bu Mac hakkında; ekran görüntüsü ve prompt
- 4: Yol 2: WhichLLM; Terminal'i açma (Windows/Mac)
- 5: uv kurulumu: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 / iex"; Mac: curl -LsSf https://astral.sh/uv/install.sh / sh
- 6: uvx whichllm@latest; çıktı: model adı, bellek ihtiyacı, tahmini hız, uygunluk
- 7: Yaz sadece: whichllm run
- 8: Yol 3: LM Studio'yu indir, uygun modeli ara, indir ve sohbet et
- 9 ve 10: Kare listesinde 8 kare var; OCR 9. ve 10. görselleri (Akılda Tutulacak Tek Şey, YEREL yorumu) içeriyor ama ekli görsel bulunmuyor, metin yalnız OCR'dan
## Belirsizlikler
- Süre 0:00 görsel gönderi; tüm zamanlar 0:00 olarak verildi.
- OCR 10 görsel, ekli kare 8; 9. ve 10. görsel metni yalnız OCR'dan, kare olarak doğrulanamadı.
- Yorumlar girişsiz alınamadı; yorumlardaki bağlantılar bilinmiyor.
- Rehberdeki 'tüm bağlantılar' DM'de; LM Studio ve WhichLLM resmi URL'leri gönderide yok.
- Sözlükteki 'Git' eşleşmesi açıklamada geçmiyor ('Git' fiili), araç değil.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://astral.sh/uv/install.ps1 | 0:00 | ekran | evet |
| https://astral.sh/uv/install.sh | 0:00 | ekran | evet |
| https://www.instagram.com/p/DdEmizXglN9/ | açıklama | açıklama | hayır |
| https://astral.sh/uv/install.psl | 0:00 | ekran | evet |
## İş akışı
- 1. adım — Cihazın teknik özelliklerini öğren (Windows: Ayarlar → Bu bilgisayar hakkında; Mac: Apple logosu → Bu Mac hakkında) — araçlar: Windows Ayarlar, macOS Apple menüsü
- 2. adım — Teknik özellik sayfasının ekran görüntüsünü al — araçlar: Ekran görüntüsü aracı
- 3. adım — Ekran görüntüsünü ChatGPT ya da Claude'a yükle ve donanıma uygun yerel model önerisi isteyen prompt'u ekle — araçlar: ChatGPT, Claude
- 4. adım — Yanıtı kontrol et: model adı, sürüm/kuantizasyon, performans ve hız bilgilerini değerlendir — araçlar: ChatGPT, Claude
- 5. adım — Terminali aç (Windows tuşu veya Command + Space ile arayıp Terminal'i başlat) — araçlar: Terminal
- 6. adım — Windows'ta uv kurulum komutunu PowerShell'de çalıştır — araçlar: PowerShell, uv
- 7. adım — Mac'te uv kurulum komutunu curl ile çalıştır — araçlar: curl, uv
- 8. adım — uv kurulumunu doğrula (uv kurulu değilse bu adım atlanabilir) — araçlar: uv
- 9. adım — uvx whichllm@latest komutuyla WhichLLM'i çalıştır; donanım taraması yapılır — araçlar: uv, WhichLLM
- 10. adım — WhichLLM çıktısında model adı, bellek ihtiyacı, tahmini hız ve donanım uygunluğunu kontrol et — araçlar: WhichLLM
- 11. adım — whichllm run komutunu yaz; uygun modeli seç, indir ve yerel ortamda sohbeti başlat — araçlar: WhichLLM
- 12. adım — Terminal kullanmak istemeyenler için alternatif: LM Studio'yu indir ve kur — araçlar: LM Studio
- 13. adım — LM Studio'yu aç, uygun bir modeli ara, indir ve uygulama içinde sohbet et — araçlar: LM Studio
## Promptlar
- Donanım ekran görüntüsünden yerel çalışabilecek modelleri belirletme — Yerel olarak bu dizüstünde çalışabilecek yapay zekâ modellerini çalıştırmak istiyorum. Ekran görüntüsünden donanım özelliklerimi oku. Model adı, dizüstüm için en iyi sürüm/kuantizasyon, performans beklentisi (hızlı/idare eder/yavaş) ver. Yalnızca yerelde çalıştırabileceğim modelleri öner.
ikinci göz KAPALI: --ikinci-goz yok
