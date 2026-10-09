# Comment “DI” to get the carousel system and how to implement this for your socia
## Künye
Comment “DI” to get the carousel system and how to implement this for your socia · piyush.glitch · süre: 0:00 · ? · https://www.instagram.com/p/Dbi13BDlDDQ/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-28 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (6)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 52589 tk · claude-haiku-5-5: claude-haiku-5-5 · 33379 tk
## Özet
Instagram carousel gönderisi (6 slayt): piyush.glitch, promptbase.shop üzerindeki 100+ carousel referansını gezmeyi, content.py içinde slayt promptlarını yazmayı, generate.py ile gpt-image-2 üzerinden 6 slaytı paralel üretmeyi anlatıyor. Son slaytta 'DI' yorumuyla tam sistem ve PDF'ler teklif ediliyor.
## Bölümler
- 0:00 Kapak: Carousel System (01/06)
- 0:00 Adım 01: promptbase.shop'u gez (02/06)
- 0:00 Adım 02: content.py'de slaytları yaz (03/06)
- 0:00 Adım 03: generate.py çalıştır (04/06)
- 0:00 GPT Image 2 görselleri üretir (05/06)
- 0:00 Yorum 'DI' çağrısı (06/06)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | CLI | yok | Carousel tasarım stilinin referansı ve marka teması; slaytlarda logo olarak geçiyor. | 0:00 | Tüm slaytların sol üstünde Claude logosu; sitede 'Claude AI' satırı. (karede: kanıttan) Tüm slaytların sol üstünde Claude logosu; sitede 'Claude AI' satırı. |
| PromptBase | yok | plugin | yok | 100+ carousel promptunun gezildiği prompt pazaryeri sitesi. | 0:00 | Slayt 2'de 'browse promptbase.shop' ve site ekran görüntüsü. (karede: kanıttan) Slayt 2'de 'browse promptbase.shop' ve site ekran görüntüsü. |
| gpt-image-2 | yok | teknik | yok | generate.py'nin slaytları ürettiği görsel model. | 0:00 | Terminal çıktısında turuncu 'gpt-image-2' etiketi; slayt 5 'GPT Image 2 builds the visuals'. (karede: kanıttan) Terminal çıktısında turuncu 'gpt-image-2' etiketi; slayt 5 'GPT Image 2 builds the visuals'. |
| GPT Image | yok | teknik | yok | Promptbase sitesinde üst marquee satırı kategorisi. | 0:00 | Site görüntüsünde 'GPT Image' başlıklı satır. (karede: kanıttan) Site görüntüsünde 'GPT Image' başlıklı satır. |
| content.py | yok | iş akışı | yok | Tüm carousel brief'ini ve slayt başına promptları tutan Python dosyası. | 0:00 | Slayt 3'te editörde content.py kodu görünüyor. (karede: kanıttan) Slayt 3'te editörde content.py kodu görünüyor. |
| generate.py | yok | CLI | yok | API ile 6 slaytı paralel üretip caption.txt yazan betik. | 0:00 | Slayt 4'te 'python3 generate.py --workers 6' terminal çıktısı. (karede: kanıttan) Slayt 4'te 'python3 generate.py --workers 6' terminal çıktısı. |
| Python | yok | CLI | yok | content.py ve generate.py'yi çalıştıran dil (python3). | 0:00 | Terminalde 'python3 generate.py' komutu. (karede: kanıttan) Terminalde 'python3 generate.py' komutu. |
| Canva | yok | ipucu | yok | 'Zero Canva' mesajında anılan tasarım aracı; kullanılmıyor, karşılaştırma. | 0:00 | Slayt 5 altında 'One prompt. 6 slides. Zero Canva.' (karede: kanıttan) Slayt 5 altında 'One prompt. 6 slides. Zero Canva.' |
| 6 slaytlık carousel üretimi (GPT Image 2) | yok | prompt | yok | @piyush.glitch Claude stilinde 6 slaytlık carousel oluştur: krem editoryal arka plan, kalın siyah başlıklar, yalnız mercan vurgu, temiz minimal teknoloji hissi, tutarlı tipografi, sağ üstte slayt sayacı; çıktı 6 slayt (01–06). | 0:00 | kaynak: kare |
| content.py içinde slayt başına prompt yapısı | yok | prompt | yok | BASE stil kilidi: Claude/Promptbase carousel referanslarına uy; krem arka plan, Claude logosu, turuncu vurgular, kalın sans başlıklar, temiz teknoloji-infografik estetiği. Her slayt için ayrı prompt (kapak, adımlar, CTA, bonus). | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| İki satırlı kayan şerit (marquee) | Promptbase ana sayfasında GPT Image üstte, Claude AI altta iki marquee satırı; sağda ok düğmeleri. (karede: Slayt 2: 'GPT Image' ve 'Claude AI' satırları, 'View all' bağlantıları, sağda yuvarlak ok düğmeleri.) | 0:00 | kare |
| Kahraman bölümü (hero section) | 'Real Carousel Prompts. Real Results.' başlığı, istatistik sayaçları, 'Browse Prompts' düğmesi. (karede: Slayt 2: site ekran görüntüsü, siyah 'Browse Prompts' düğmesi, sağda 10,000+ Creators / 200,000+ Prompts Sold.) | 0:00 | kare |
| Gezinme çubuğu (navbar) | PromptBase logosu, Marketplace/Sell/Explore menüleri, Login ve Sign up düğmeleri. (karede: Slayt 2: üstte menü çubuğu, sağda siyah 'Sign up' düğmesi.) | 0:00 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| python3 generate.py --workers 6 | 6 işçiyle API üzerinden 6 slaytı paralel üretir, PNG'ler ve caption.txt yazar. (karede: Slayt 4: kutuda ve terminalde '$ python3 generate.py --workers 6'.) | 0:00 | kare |
| /prompt | Sohbet arayüzünde carousel üretim promptunu başlatan slash komutu olarak gösteriliyor. (karede: Slayt 5: siyah kutuda '>_ /prompt'.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Promptbase ana sayfasında şu an 100+ carousel yayında. | 0:00 | sayısal |
| Gezmek ücretsiz; Pro sürüm PDF'leri ve generate sistemini açıyor. | 0:00 | özellik |
| generate.py 6 slaytı paralel üretir, mevcut dosyaları atlar, tekrar çalıştırmak güvenlidir. | 0:00 | özellik |
| Tek prompt, 6 slayt, Canva gerekmez. | 0:00 | karşılaştırma |
| Sitede 10,000+ yaratıcı ve 200,000+ satılmış prompt var. | 0:00 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 (slayt 1) | Claude logosu ve @PIYUSH.GLITCH | Claude | Tüm slaytlarda Claude logosu |
| kare 0:00 (slayt 1) | Promptbase | PromptBase | 'steal my carousels from promptbase' |
| kare 0:00 (slayt 1) | Örnek kapaklar (iPhone 17 Pro Max, Cloud Agents, GGSfield Games Cloud MCP vb.) | aday değil: konu dışı | Yalnız örnek carousel kapak görselleri |
| kare 0:00 (slayt 2) | promptbase.shop sitesi | PromptBase | Tarayıcı çubuğunda promptbase.shop |
| kare 0:00 (slayt 2) | GPT Image satırı | GPT Image | Sitede 'GPT Image' marquee satırı |
| kare 0:00 (slayt 2) | Claude AI satırı | Claude | Sitede 'Claude AI' marquee satırı |
| kare 0:00 (slayt 2) | Pro planı, PDF'ler | PromptBase | 'Pro unlocks PDFs + the generate system' |
| kare 0:00 (slayt 3) | content.py | content.py | Editörde content.py |
| kare 0:00 (slayt 3) | BASE stil bloğu | aday değil: başka adayın parçası (content.py) | content.py içindeki BASE değişkeni |
| kare 0:00 (slayt 3) | caption.txt | aday değil: başka adayın parçası (generate.py) | generate.py'nin yazdığı çıktı dosyası |
| kare 0:00 (slayt 4) | generate.py | generate.py | python3 generate.py --workers 6 |
| kare 0:00 (slayt 4) | python3 | Python | Terminal komutu |
| kare 0:00 (slayt 4) | --workers 6 parametresi | aday değil: başka adayın parçası (generate.py) | generate.py bayrağı |
| kare 0:00 (slayt 4) | gpt-image-2 etiketi | gpt-image-2 | Terminalde turuncu etiket |
| kare 0:00 (slayt 5) | GPT Image 2 | gpt-image-2 | 'GPT Image 2 builds the visuals' |
| kare 0:00 (slayt 5) | /prompt komutu | aday değil: genel kavram | Kutuda '>_ /prompt' başlığı |
| kare 0:00 (slayt 5) | Canva | Canva | 'Zero Canva' ifadesi |
| kare 0:00 (slayt 5) | @zero.canon_ | aday değil: konu dışı | Alt köşede hesap adı |
| açıklama | 'DI' yorum çağrısı | aday değil: sponsor/reklam | Comment “DI” to get the carousel system |
| kare 0:00 (slayt 6) | Get the full library düğmesi, promptbase.shop | PromptBase | '100+ carousels · generate scripts · promptbase.shop' |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- Slayt 1 (0:00): Başlık 'steal my carousels from promptbase', 'The Carousel System', örnek kapaklar, '100+ live. pick one. generate yours.'
- Slayt 2 (0:00): 'browse promptbase.shop', iki marquee satırı, PromptBase site ekran görüntüsü, Pro PDF ve generate sistemini açar.
- Slayt 3 (0:00): content.py kodu: BASE STYLE LOCK, COVER, slides listesi; 'One prompt per slide → batch generate'.
- Slayt 4 (0:00): 'python3 generate.py --workers 6', OK 01–06.png, OK caption.txt, 'Done: 6 ok, 0 fail', gpt-image-2.
- Slayt 5 (0:00): 'GPT Image 2 builds the visuals', /prompt kutusu, 'One prompt. 6 slides. Zero Canva.', @zero.canon_.
- Slayt 6 (0:00): 'comment DI', 'Get the full Carousel System + every PDF', 'GET THE FULL LIBRARY', 'Create smarter.'
## Belirsizlikler
- Video değil görsel gönderi; süre 0:00 ve tüm zamanlar 0:00 yazıldı.
- Yorumlar girişsiz alınamadı; 'DI' ile gelen içerik/bağlantı doğrulanamadı.
- Slayt 1'deki 'iPhone 17 Pro Max', 'Cloud Agents', 'GGSfield Games Cloud MCP' örnek kapak görselleri; araç olarak kullanılmıyor.
- Slayt 5'te @zero.canon_ hesabı anılıyor; rolü belirsiz.
- generate.py'nin hangi API'yi çağırdığı yazılmamış; yalnız gpt-image-2 etiketi var.
- Sunucudaki ana yapay zekâ olarak Claude'un gerçekten kullanıldığı net değil, marka teması olabilir.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| promptbase.shop | 0:00 | ekran | evet |
| https://www.instagram.com/p/Dbi13BDlDDQ/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — promptbase.shop'ta 100+ carousel kapağını gezip referans seç — araçlar: PromptBase
- 2. adım — Seçilen referansı tersine mühendislikle analiz et, stil kilidini (BASE) belirle — araçlar: PromptBase, Claude
- 3. adım — content.py içinde BASE stil bloğunu ve kapak promptunu yaz — araçlar: content.py, Python
- 4. adım — Slayt 2–6 için ayrı promptları slides listesine ekle — araçlar: content.py
- 5. adım — generate.py'yi python3 generate.py --workers 6 ile çalıştır — araçlar: generate.py, Python, gpt-image-2
- 6. adım — Çıktıyı kontrol et: 01–06.png ve caption.txt, 'Done: 6 ok, 0 fail' — araçlar: generate.py
- 7. adım — Gerekirse yeniden çalıştır (mevcut dosyalar atlanır) — araçlar: generate.py
- 8. adım — PNG'leri ve caption.txt ile carousel olarak paylaş — araçlar: gpt-image-2
## Promptlar
- 6 slaytlık carousel üretimi (GPT Image 2) — @piyush.glitch Claude stilinde 6 slaytlık carousel oluştur: krem editoryal arka plan, kalın siyah başlıklar, yalnız mercan vurgu, temiz minimal teknoloji hissi, tutarlı tipografi, sağ üstte slayt sayacı; çıktı 6 slayt (01–06).
- content.py içinde slayt başına prompt yapısı — BASE stil kilidi: Claude/Promptbase carousel referanslarına uy; krem arka plan, Claude logosu, turuncu vurgular, kalın sans başlıklar, temiz teknoloji-infografik estetiği. Her slayt için ayrı prompt (kapak, adımlar, CTA, bonus).
