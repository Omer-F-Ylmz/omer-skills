# Schedule and post short videos to TikTok, Instagram, and YouTube from your own c
## Künye
Schedule and post short videos to TikTok, Instagram, and YouTube from your own c · gittrend.io · süre: 0:33 · ? · https://www.instagram.com/reel/DbLROjmkXwp/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-25 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 40732 tk · claude-haiku-5-5: claude-haiku-5-5 · 37346 tk
## Özet
AutoSocial Studio, TikTok, Instagram ve YouTube için kısa videoları kendi bilgisayarınızdan zamanlayıp paylaşmanızı sağlayan, ücretsiz ve yerelde çalışan açık kaynaklı bir pano. Video GitHub README sayfasını gezerek özellikleri, gereksinimleri ve hızlı kurulum komutlarını gösteriyor. Hesap başına ayrı kuyruk ve tarayıcı oturumu var.
## Bölümler
- 0:00 AutoSocial tanıtımı ve README başlangıcı
- 0:08 Özellikler ve kimlere yardımcı olduğu
- 0:13 Gereksinimler ve hızlı kurulum
- 0:18 Yapılandırma ayarları (.env)
- 0:23 Güvenlik, giriş ve kuyruk düzeni
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| AutoSocial | yok | CLI | https://github.com/Katzca/AutoSocial | TikTok, Instagram ve YouTube için yerel, çok hesaplı kısa video zamanlama panosu | 0:00 | README başlığı AutoSocial Studio (karede: Sekme: GitHub - Katzca/AutoSocial; başlık AutoSocial Studio) |
| Hootsuite | yok | teknik | yok | AutoSocial'ın ücretsiz alternatifi olarak anılan barındırılan servis | 0:00 | free self-hosted alternative to Hootsuite |
| Express | yok | teknik | yok | Yerel pano için kullanılan Node sunucu çatısı | 0:00 | local Express dashboard (karede: README paragrafı: local Express dashboard, Playwright-powered upload flows) |
| Playwright | yok | teknik | yok | Yükleme akışlarını ve kalıcı giriş oturumlarını yöneten tarayıcı otomasyonu | 0:00 | Playwright-powered upload flows (karede: README paragrafı: Playwright-powered upload flows) |
| yt-dlp | yok | CLI | yok | Referans ve TikTok videolarını indiren araç | 0:14 | Optional: yt-dlp.exe in autodownload/ (karede: Requirements listesinde Optional: yt-dlp.exe in autodownload/) |
| FFmpeg | yok | CLI | yok | Videoları benzersizleştirme (uniquifier) işlemi | 0:14 | FFmpeg and ffprobe in PATH (karede: Requirements listesinde FFmpeg and ffprobe in PATH) |
| ffprobe | yok | CLI | yok | FFmpeg ile birlikte PATH'te gereken araç | 0:14 | FFmpeg and ffprobe in PATH (karede: Requirements listesinde FFmpeg and ffprobe in PATH) |
| Node.js | yok | teknik | yok | Çalışma ortamı, 18+ gerekli | 0:14 | Requirements: Node.js 18+ (karede: Requirements listesinde Node.js 18+) |
| npm | yok | CLI | yok | Bağımlılık kurulumu ve betik çalıştırma | 0:14 | npm ci, npm run doctor (karede: Quick Start bloğunda npm ci ve npm run doctor) |
| Playwright Chromium | yok | teknik | yok | Otomasyon için kurulan Chromium tarayıcısı | 0:14 | npx playwright install chromium (karede: Requirements: Playwright Chromium; Quick Start: npx playwright install chromium) |
| GitHub | yok | teknik | yok | Projenin README'sinin barındığı servis | 0:00 | Sekme başlığı GitHub - Katzca/AutoSocial (karede: Tarayıcı sekmesi GitHub - Katzca/AutoSocial, adres github.com/Katzca/AutoSocial#readme) |
| TikTok | yok | teknik | yok | Paylaşım yapılan hedef platform | 0:00 | README: TikTok, Instagram, and YouTube (karede: Dashboard Overview'da TikTok kartı ve README metni) |
| Instagram | yok | teknik | yok | Paylaşım yapılan hedef platform | 0:00 | README: TikTok, Instagram, and YouTube (karede: Dashboard Overview'da Instagram kartı) |
| YouTube | yok | teknik | yok | Paylaşım yapılan hedef platform | 0:00 | README: TikTok, Instagram, and YouTube (karede: Dashboard Overview'da YouTube kartı) |
| cron | yok | teknik | yok | Cron ifadeleriyle gönderi zamanlama | 0:14 | Schedule posts with cron expressions (karede: Features listesinde Schedule posts with cron expressions) |
| Copy-Item | yok | CLI | yok | PowerShell komutu. Örnek .env.example dosyasını .env olarak kopyalar. | 0:20 | 'Copy-Item .env.example .env' komutu (karede: Quick Start altındaki 'Create your local environment file' bölümünde 'Copy-Item .env.example .env' satırı) |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Pano genel bakış (Dashboard Overview) | README'deki ekran görüntüsünde sayaç kartları, platform kartları ve canlı sistem günlüğü görünüyor (karede: Dashboard Overview: 6, 26, 1, 0 sayaçları; TikTok, Instagram, YouTube kartları; Live System Logs) | 0:00 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm ci | Bağımlılıkları kurar (karede: Quick Start bloğunda npm ci) | 0:14 | kare |
| npx playwright install chromium | Playwright Chromium tarayıcısını kurar (karede: Quick Start bloğunda npx playwright install chromium) | 0:14 | kare |
| npm run doctor | Yerel bağımlılıkları denetler (karede: Quick Start bloğunda npm run doctor) | 0:14 | kare |
| Copy-Item .env.example .env | Yerel ortam dosyasını oluşturur (karede: Create your local environment file bloğunda Copy-Item .env.example .env) | 0:20 | kare |
| npm run dashboard | Yerel panoyu başlatır (karede: Start the dashboard bloğunda npm run dashboard) | 0:20 | kare |
| npm run login | TikTok için CLI giriş oturumunu açar (şu an yalnız TikTok'a özel) (karede: OCR ekran metni (ekli kare değil): 'The CLI login command is still TikTok-specific: npm run login') | 0:27 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ücretsiz, kendi sunucunuzda çalışan Hootsuite alternatifi | 0:00 | karşılaştırma |
| Cron, günlük saat veya anlık paylaşım modu ile zamanlama | 0:14 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | AutoSocial | AutoSocial | AutoSocial is a free self-hosted alternative |
| konuşma 0:00 | Hootsuite | Hootsuite | alternative to Hootsuite |
| kare 0:00 | Express | Express | local Express dashboard |
| kare 0:00 | Playwright | Playwright | Playwright-powered upload flows |
| kare 0:14 | yt-dlp | yt-dlp | yt-dlp.exe in autodownload/ |
| kare 0:14 | FFmpeg | FFmpeg | FFmpeg and ffprobe in PATH |
| kare 0:00 | GitHub | GitHub | GitHub - Katzca/AutoSocial sekmesi |
| kare 0:00 | TikTok | TikTok | hedef platform |
| kare 0:00 | Instagram | Instagram | hedef platform |
| kare 0:00 | YouTube | YouTube | hedef platform |
| kare 0:14 | Node.js | Node.js | Node.js 18+ |
| kare 0:14 | npm | npm | npm ci |
| kare 0:14 | Playwright Chromium | Playwright Chromium | npx playwright install chromium |
| kare 0:14 | ffprobe | ffprobe | FFmpeg and ffprobe in PATH |
| kare 0:14 | cron ifadeleri | cron | Schedule posts with cron expressions |
| kare 0:00 | MIT license | aday değil: genel kavram | README sekmesi MIT license |
| kare 0:00 | Dashboard Overview ekran görüntüsü | aday değil: başka adayın parçası (AutoSocial) | README içindeki pano görseli |
| kare 0:20 | Copy-Item | aday değil: genel kavram | PowerShell komutu |
| açıklama | gittrend.io | aday değil: konu dışı | More like this → gittrend.io |
| açıklama | Hashtagler (#opensource vb.) | aday değil: genel kavram | #opensource #socialmedia ... |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
| ekran 0:11 | Headless UI, Inter, Go, Descript, Make, OpenAI, context7 | aday değil: konu dışı | Sözlük eşleşmesi, videoda kullanılmıyor |
## Kareden okunanlar
- 0:00: README: AutoSocial Studio, yerel çok hesaplı otomasyon panosu; Dashboard Overview ekran görüntüsü
- 0:14: Features ve Requirements listesi, Quick Start: npm ci, npx playwright install chromium, npm run doctor
- 0:20: Quick Start, Copy-Item .env.example .env, npm run dashboard, Configuration ayar listesi
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Sözlükteki OpenAI, context7, Make, Descript, Headless UI, Inter gibi eşleşmeler OCR/ses gürültüsü; videoda kullanılmadı.
- Altyazıda 'comment social' çağrısı var; bu bir yönlendirme.
- 0:23 sonrası güvenlik ve kuyruk içerikleri (npm run login dahil) yalnız OCR'dan; kareyle doğrulanmadı, komut listesine alınmadı.
- Konuşma dili belirtilmemiş, altyazı İngilizce.
- Açıklamada bağlantı yok; gittrend.io yalnız künyede/açıklama metninde geçiyor, aday değil.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/Katzca/AutoSocial#readme | 0:00 | ekran | evet |
| http://127.0.0.1:3000 | 0:20 | ekran | hayır |
| gittrend.io | açıklama | açıklama | hayır |
| https://www.instagram.com/reel/DbLROjmkXwp/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — GitHub'daki AutoSocial README sayfasını açıp projeyi tanıtma — araçlar: GitHub, AutoSocial
- 2. adım — Özellikleri ve hedef kitleyi gösterme — araçlar: AutoSocial
- 3. adım — Gereksinimleri gösterme — araçlar: Node.js, npm, FFmpeg, ffprobe, yt-dlp
- 4. adım — Bağımlılıkları kurma — araçlar: npm
- 5. adım — Chromium'u yükleme — araçlar: Playwright Chromium
- 6. adım — Doctor ile yerel bağımlılıkları kontrol etme — araçlar: npm
- 7. adım — .env dosyasını oluşturma — araçlar: PowerShell
- 8. adım — Panoyu başlatıp 127.0.0.1:3000'i açma — araçlar: npm, Express
- 9. adım — Zamanlama ayarlarını (cron) inceleme — araçlar: cron
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
