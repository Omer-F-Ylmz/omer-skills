# “STRIX” yazarak bu ücretsiz ve açık kaynaklı aracı edinin ve vibe kodlu uygulama
## Künye
“STRIX” yazarak bu ücretsiz ve açık kaynaklı aracı edinin ve vibe kodlu uygulama · arifata.kosker · süre: 0:46 · ? · https://www.instagram.com/reel/DbpsEzyMzR9/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-29 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 42238 tk · claude-haiku-5-5: claude-haiku-5-5 · 30220 tk
## Özet
Kısa reel, vibe kodlu uygulamalara hacker gibi saldırıp güvenlik açıklarını bulan ücretsiz, açık kaynaklı yapay zekâ sızma testi aracı Strix'i tanıtıyor. Strix uzman AI ajanlarından oluşan bir ekip görevlendiriyor, uygulamayı canlı çalıştırıyor, hedefli saldırılar yapıyor, çalışan kanıt ve düzeltme önerisi sunuyor. Kendi model anahtarınızla (Claude, GPT, Gemini, yerel model) çalışıyor. Yoruma STRIX yazanlara link vaat ediliyor.
## Bölümler
- 0:00 Strix tanıtımı: hacker gibi saldıran AI aracı
- 0:14 Tarama listesi yerine uzman AI ajan ekibi
- 0:26 Çalışan kanıt ve zafiyet raporu
- 0:35 Yayından önce tam güvenlik testi ve yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Strix | yok | CLI | https://github.com/usestrix/strix | Gerçek hacker gibi davranan uzman AI ajanlarıyla uygulamayı canlı test eden açık kaynaklı sızma testi aracı | 0:26 | Ekranda strix --target komutu ve github.com/usestrix/strix; zafiyet raporu 0:26 karesinde (karede: 0:26 karesinde terminalde 'VULNERABILITY CONFIRMED' ve 'Vulnerability Report' (Negative Quantity Acceptance, Severity HIGH, CVSS 7.1) çıktısı) |
| Claude | yok | teknik | yok | Strix'e bağlanabilecek model seçeneği | açıklama | Açıklamada Claude, GPT, Gemini veya yerel model entegre edilebilir deniyor |
| GPT | yok | teknik | yok | Strix'e bağlanabilecek model seçeneği | açıklama | Açıklamada model seçeneği olarak geçiyor |
| Gemini | yok | teknik | yok | Strix'e bağlanabilecek model seçeneği | açıklama | Açıklamada model seçeneği olarak geçiyor |
| GitHub | yok | teknik | yok | Strix deposunun barındığı ve yıldız sayısının gösterildiği servis | 0:09 | Konuşmada gitapta 45 bin yıldız; ekranda github.com/usestrix/strix |
| Vercel | yok | teknik | yok | Taranan örnek uygulamanın barındığı adres (my-startup.vercel.app) | 0:02 | Tarayıcı çubuğunda my-startup.vercel.app görünüyor (karede: 0:02 karesinde 'SCANNING' etiketi, '0 ZAFİYET' sayacı, my-startup.vercel.app adres çubuklu 'Welcome to my startup' sayfası ve kırmızı tarama çizgisi) |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Tarama çizgisi animasyonu (scanline animation) | Kırmızı ışık çizgisi ekranda yukarıdan aşağıya taranarak tarama hissi veriyor. (karede: Koyu arka plan üzerinde 'Welcome to my startup' başlığının üstünde kırmızı yatay bir tarama çizgisi.) | 0:02 | kare |
| Sayaç güncellemesi (counter update) | Bulunan zafiyet sayısı canlı olarak artıyor. (karede: Sağ üstte '0 ZAFİYET' sayacı; 0:03 karesinde '1 ZAFİYET' olarak değişiyor.) | 0:02 | kare |
| Tarayıcı çerçevesi (browser chrome) | Demo uygulama bir tarayıcı penceresi içinde gösteriliyor. (karede: Sayfa üstünde üç nokta ve 'my-startup.vercel.app' yazılı adres çubuğu içeren pencere başlığı.) | 0:02 | kare |
| Yükleme iskeleti (skeleton loading) | İçerik yüklenmeden önce gri blok yer tutucular gösteriliyor. (karede: Başlığın altında gri, yuvarlatılmış çubuklardan oluşan yer tutucu satırlar.) | 0:02 | kare |
| Önem derecesi rozeti (severity badge) | Zafiyet önem derecesi kırmızı etiketle gösteriliyor. (karede: Satırın yanında kırmızı nokta ve 'CRITICAL' etiketi; kırmızı bir vurgu bloğu.) | 0:03 | kare |
| Terminal arayüzü (terminal UI) | Strix'in terminal çıktısı ve rapor metni koyu temalı bir pencerede gösteriliyor. (karede: Siyah zemin üzerinde yeşil ve beyaz monospace metinli, kenarlıklı çıktı penceresi.) | 0:26 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| strix --target https://your-app.com | Canlı bir uygulama URL'sine karşı Strix taraması başlatır (karede: Verilen 3 karede görünmüyor; yalnızca OCR metninde (0:25) okundu) | 0:25 | kare |
| strix --target ./app-directory | Yerel kod dizinini tarar (karede: Verilen 3 karede görünmüyor; yalnızca OCR metninde (0:36-0:37) okundu) | 0:37 | kare |
| strix --target https://github.com/org/repo | GitHub deposunu hedef alarak tarar (karede: Verilen 3 karede görünmüyor; yalnızca OCR metninde (0:38) okundu) | 0:38 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Strix GitHub'da 45 bin yıldızı geçti (açıklamada on binlerce) | 0:09 | sayısal |
| Tarama listesi vermek yerine gerçek hacker gibi davranan uzman AI ajan ekibi görevlendiriyor | 0:14 | özellik |
| Her bulgunun gerçek olduğuna dair çalışan kanıt ve düzeltme önerisi sunuyor | 0:26 | özellik |
| Araç ücretsiz; yalnızca kullanılan modelin maliyeti ödenir | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Strix | Strix | Adı Strix, açık kaynaklı AI penetrasyon aracı |
| kare 0:02 | my-startup.vercel.app örnek sayfa | Vercel | Adres çubuğunda vercel.app |
| konuşma 0:09 | GitHub | GitHub | 45 bin yıldız, github.com/usestrix/strix |
| açıklama | Claude | Claude | Model seçeneği olarak sayılıyor |
| açıklama | GPT | GPT | Model seçeneği olarak sayılıyor |
| açıklama | Gemini | Gemini | Model seçeneği olarak sayılıyor |
| açıklama | Yerel model | aday değil: genel kavram | Belirli bir model adı verilmiyor |
| kare 0:26 | CVSS skoru ve vektörü | aday değil: başka adayın parçası (Strix) | Strix raporunun içinde |
| kare 0:26 | Sepet API negatif adet açığı | aday değil: başka adayın parçası (Strix) | Strix'in bulduğu örnek zafiyet |
| yorum | STRIX yorum çağrısı | aday değil: konu dışı | Link isteme çağrısı |
| ekran 0:24 | strix --target https://your-app.com | Strix | OCR'da komut satırı |
| ekran 0:24 | strix view | Strix | OCR'da komut |
## Kareden okunanlar
- 0:02: SCANNING, 0 ZAFİYET, my-startup.vercel.app, Welcome to my startup, altyazı 'uygulamanıza bir hacker'
- 0:03: SCANNING, 1 ZAFİYET, CRITICAL etiketi, altyazı 'gibi saldıran ve gerçek'
- 0:26: Order created successfully, VULNERABILITY CONFIRMED, Order ID 12, Total Price $-149.9, Severity HIGH, CVSS Score 7.1, Endpoint /api/v1/cart/add, Method POST
## Belirsizlikler
- Yorumlar girişsiz alınamadı; STRIX yorumuyla gönderilen link bilinmiyor.
- Altyazıda 45 bin yıldız, açıklamada 'on binlerce' deniyor.
- Sözlük eşleşmelerindeki Descript, Slack ve Codex videoda gösterilmiyor; OCR/ses gürültüsü olabilir.
- Terminal komutları (strix --target ...) yalnızca OCR'dan okundu, karelerde doğrulanmadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| my-startup.vercel.app | 0:02 | ekran | hayır |
| github.com/usestrix/strix | 0:09 | ekran | evet |
| https://your-app.com | 0:24 | ekran | hayır |
| https://github.com/org/repo | 0:38 | ekran | hayır |
## İş akışı
- 1. adım — Örnek uygulama (my-startup.vercel.app) hedef olarak gösterilir ve tarama başlar — araçlar: Strix, Vercel
- 2. adım — Tarama sırasında ilk kritik zafiyet işaretlenir — araçlar: Strix
- 3. adım — Strix'in GitHub deposu ve yıldız sayısı gösterilir — araçlar: GitHub, Strix
- 4. adım — Uzman AI ajanları (browser, recon) görevlendirilir — araçlar: Strix
- 5. adım — Strix hedef URL, dizin veya repo ile komut satırından çalıştırılır — araçlar: Strix, GitHub
- 6. adım — Hedefli saldırı yapılır ve zafiyet çalışan kanıtla doğrulanır — araçlar: Strix
- 7. adım — Zafiyet raporu ve önerilen düzeltmeler incelenir — araçlar: Strix
- 8. adım — Kendi model anahtarıyla Claude, GPT, Gemini veya yerel model bağlanır — araçlar: Claude, GPT, Gemini
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
