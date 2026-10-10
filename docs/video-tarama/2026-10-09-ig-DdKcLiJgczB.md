# Send files from one device to many in real time, no size limit — FileSync is a f
## Künye
Send files from one device to many in real time, no size limit — FileSync is a f · gittrend.io · süre: 0:32 · ? · https://www.instagram.com/reel/DdKcLiJgczB/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-36 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 18449 tk · claude-haiku-5-5: claude-haiku-5-5 · 84794 tk
## Özet
Kısa reel, açık kaynak FileSync projesini tanıtıyor. FileSync, WebRTC ile tarayıcılar arasında doğrudan, boyut sınırı ve hesap olmadan, bir cihazdan birçok cihaza dosya gönderen ve kendi sunucunda Docker ile barındırılan bir WeTransfer alternatifi. Video GitHub README sayfasını kaydırarak özellikleri, HTTP ve HTTPS (Caddy) kurulum seçeneklerini, gizli anahtar üretimini, gerekli portları ve port özelleştirmeyi gösteriyor.
## Bölümler
- 0:00 FileSync tanıtımı ve özellikler
- 0:09 Kendi sunucuda barındırma ve içindekiler
- 0:12 Kullanım adımları (oda bağlantısı, dosya bırakma)
- 0:15 Gereksinimler ve gizli anahtar üretimi
- 0:20 Seçenek A: HTTP kurulumu
- 0:21 Seçenek B: HTTPS kurulumu (Caddy)
- 0:26 Gerekli portlar
- 0:30 Port özelleştirme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| FileSync | yok | CLI | https://github.com/polius/FileSync | Dosyaları bir cihazdan çok cihaza, tarayıcılar arasında doğrudan ve boyut sınırı olmadan gönderen, kendi sunucuna kurulan açık kaynak araç. | 0:00 | FileSync lets you share large files peer-to-peer with no size limit |
| WebRTC | yok | teknik | yok | Dosyaların tarayıcılar arasında şifreli ve doğrudan aktarılmasını sağlayan teknoloji. | 0:00 | README: files travel directly between browsers over encrypted WebRTC (karede: kanıttan) README: files travel directly between browsers over encrypted WebRTC |
| Docker | yok | CLI | yok | FileSync tek bir Docker imajı olarak çalıştırılıyor. | 0:00 | run one Docker command and share your room URL |
| Docker Compose | yok | CLI | yok | docker compose up -d ile FileSync'i HTTP veya HTTPS yapılandırmasıyla başlatır. | 0:20 | Ekran metni: docker compose up -d (karede: kanıttan) Ekran metni: docker compose up -d |
| Caddy | yok | teknik | yok | HTTPS seçeneğinde ters vekil sunucu olarak Let's Encrypt sertifikasını otomatik alır ve yeniler. | 0:21 | Caddy obtains and renews a Let's Encrypt certificate automatically (karede: kanıttan) Caddy obtains and renews a Let's Encrypt certificate automatically |
| Let's Encrypt | yok | teknik | yok | Caddy'nin HTTPS için otomatik aldığı ücretsiz sertifika servisi. | 0:21 | Caddy obtains and renews a Let's Encrypt certificate automatically (karede: kanıttan) Caddy obtains and renews a Let's Encrypt certificate automatically |
| STUN/TURN | yok | teknik | yok | NAT/güvenlik duvarı arkasında doğrudan bağlantı kurulamadığında röle yedeği sağlar. | 0:07 | automatic STUN/TURN relay fallback for restrictive NATs and firewalls (karede: kanıttan) automatic STUN/TURN relay fallback for restrictive NATs and firewalls |
| Python 3 | yok | CLI | yok | Yalnızca gizli anahtarı üretmek için kullanılan gereksinim. | 0:15 | Python 3 (only to generate the secret key below) (karede: kanıttan) Python 3 (only to generate the secret key below) |
| GitHub | yok | teknik | https://github.com/polius/FileSync | FileSync deposu ve README sayfası GitHub'da gösteriliyor. | 0:00 | Tarayıcı sekmesi: GitHub - polius/FileSync (karede: kanıttan) Tarayıcı sekmesi: GitHub - polius/FileSync |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| QR kodlu oda bağlantısı paneli (QR code room share) | Uygulama arayüzünde oda bağlantısı ve QR kodu gösteriliyor, kullanıcılar bağlanana kadar bekleme mesajı çıkıyor. (karede: FileSync arayüzünde QR kod, 'Waiting users to join...' yazısı ve filesync.app oda bağlantısı kutusu) | 0:00 | kare |
| Eylem düğmeleri (Send Files / Add password buttons) | Mavi 'Send Files' ve yeşil 'Add password' düğmeleri. (karede: QR kodun altında 'Send Files' ve 'Add password' düğmeleri) | 0:07 | kare |
| Kullanıcı ve dosya listesi (Users / Files list) | 'Users (1)' altında 'Red Heron (You)', 'Change name' bağlantısı; 'Files (0)', 'Download all' ve 'No files transferred' boş durumu. (karede: Users (1) ve Files (0) bölümleri, Download all düğmesi, No files transferred) | 0:09 | kare |
| Koyu tema (Dark theme) | Uygulama ve GitHub sayfası koyu temada. (karede: Koyu arka planlı FileSync arayüzü ve README) | 0:00 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| python3 -c "import secrets, base64; print(base64.b64encode(secrets.tc... | Gizli anahtar üretir (TURN kimlik bilgilerini imzalar); komut ekranda kesik görünüyor. (karede: Gönderilen karelerde yok; 0:16 ekran metni (OCR) okundu) | 0:16 | kare |
| docker compose up -d | FileSync'i HTTP kurulumuyla arka planda başlatır. (karede: Gönderilen karelerde yok; 0:20 ekran metni (OCR) okundu) | 0:20 | kare |
| docker compose -f docker-compose-ssl.yml up -d | FileSync'i Caddy ile HTTPS kurulumunda başlatır. (karede: Gönderilen karelerde yok; 0:24 ekran metni (OCR) okundu) | 0:24 | kare |
| docker compose down | HTTP kurulumunu durdurur. (karede: Gönderilen karelerde yok; 0:25 ekran metni (OCR) okundu) | 0:25 | kare |
| docker compose -f docker-compose-ssl.yml down | HTTPS kurulumunu durdurur. (karede: Gönderilen karelerde yok; 0:25 ekran metni (OCR) okundu) | 0:25 | kare |
| python3 -c "import secrets, base64; print(base64.b64encode(secrets.tc..." (kesik okundu) | Rastgele bir gizli anahtar (secret key) üretip base64 olarak yazdırır; TURN kimlik bilgilerini imzalamak için kullanılır. (karede: Kurulum bölümünde 'Generate one with:' altındaki python3 -c satırı (OCR, komut kesik)) | 0:16 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Dosyalar tarayıcılar arasında doğrudan akıyor; sunucu verileri görmüyor. | 0:00 | özellik |
| Boyut sınırı ve hesap gerekmiyor; alıcılar yalnızca bağlantıyı açıyor. | 0:00 | özellik |
| Docker pulls rozeti 25k, sürüm v4.0.0 görünüyor. | 0:00 | sayısal |
| Bağlantıların yaklaşık %5-10'u doğrudan kurulamayıp TURN röle kullanıyor. | 0:29 | sayısal |
| Ücretsiz, kendi sunucuda barındırılan WeTransfer alternatifi. | açıklama | karşılaştırma |
| HTTP ile 500 MB üstü büyük aktarımlar güvenilir değil; HTTPS öneriliyor. | 0:17 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | FileSync | FileSync | FileSync lets you share large files peer-to-peer |
| konuşma 0:00 | peer-to-peer aktarım | WebRTC | files travel directly between browsers |
| konuşma 0:00 | Docker komutu | Docker | run one Docker command |
| kare 0:00 | GitHub sayfası | GitHub | Sekme: GitHub - polius/FileSync |
| kare 0:00 | WebRTC | WebRTC | over encrypted WebRTC |
| kare 0:00 | MIT lisansı | aday değil: genel kavram | License MIT rozeti |
| kare 0:07 | STUN/TURN | STUN/TURN | automatic STUN/TURN relay fallback |
| ekran 0:08 | Table of contents | aday değil: konu dışı | README içindekiler listesi |
| ekran 0:10 | Claude Code (sözlük eşleşmesi) | aday değil: konu dışı | Videoda kullanım yok; bulanık OCR |
| ekran 0:15 | Python 3 | Python 3 | Python 3 (only to generate the secret key) |
| ekran 0:20 | docker compose up -d | Docker Compose | Ekran metni: docker compose up -d |
| ekran 0:21 | Caddy | Caddy | Caddy obtains and renews a Let's Encrypt certificate |
| ekran 0:21 | Let's Encrypt | Let's Encrypt | Let's Encrypt certificate automatically |
| ekran 0:31 | Nginx, Traefik | aday değil: konu dışı | Yalnızca alternatif vekil örneği olarak yazılı |
| açıklama | WeTransfer | aday değil: konu dışı | free, self-hosted alternative to WeTransfer |
| açıklama | gittrend.io | aday değil: konu dışı | More like this → gittrend.io |
| açıklama | Hashtag'ler (#OpenSource, #SelfHosted, #Privacy vb.) | aday değil: genel kavram | Açıklamadaki etiketler |
| konuşma 0:00 | OpenAI, Browser Use (sözlük eşleşmesi) | aday değil: konu dışı | Bulanık ses eşleşmesi; videoda anlatılmıyor |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:00: GitHub polius/FileSync README; 'Send files from one device to many, in real time'; rozetler release v4.0.0, docker pulls 25k, MIT; altyazı 'FILESYNC LETS YOU'.
- 0:07: Aynı README; uygulama önizlemesi (QR, Send Files, Add password, Red Heron (You)); özellik listesi; altyazı 'TRAVEL DIRECTLY BETWEEN'.
- 0:09: Özellikler listesi ve Table of contents (Self-hosting, Option A HTTP, Option B HTTPS); altyazı 'SO THE SERVER'.
## Belirsizlikler
- Yorumlar girişsiz alınamadı; yorumlardaki bağlantılar bilinmiyor.
- Gönderilen 3 kare yalnızca 0:00-0:09; kurulum komutları OCR metninden alındı, gönderilen karelerde doğrulanamadı.
- Python gizli anahtar komutu ekranda kesik; tam hali okunamadı.
- Nginx ve Traefik 0:31'de yalnızca README metninde örnek olarak geçiyor, gösterilip kullanılmadı.
- Sözlük eşleşmeleri (OpenAI, Browser Use, Claude Code, Inter, Go) bulanık OCR/ses hatası gibi; videoda gerçek kullanım doğrulanmadı.
- Videonun çalıştığı ana yapay zekâ aracı belli değil; sunucu/model bilgisi yok.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/polius/FileSync#readme | 0:00 | ekran | evet |
| https://github.com/polius/filesync | açıklama | açıklama | evet |
| https://filesync.app/kxi-skhl-kqy | 0:00 | ekran | hayır |
| filesync.example.com | 0:22 | ekran | hayır |
| https://yourdomain.com | 0:24 | ekran | hayır |
| http://localhost:8080 | 0:31 | ekran | hayır |
| gittrend.io | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — FileSync GitHub README sayfasını açıp özellikleri tanıtma — araçlar: GitHub, FileSync
- 2. adım — Gizlilik, boyut sınırsızlığı ve bire-çok gönderim özelliklerini gösterme — araçlar: FileSync, WebRTC
- 3. adım — Kendi sunucuda barındırma bölümüne ve içindekiler listesine geçme — araçlar: GitHub
- 4. adım — Kullanım adımlarını gösterme: oda bağlantısı/QR paylaşma, dosyaları bırakma, isteğe bağlı parola — araçlar: FileSync
- 5. adım — Gereksinimleri gösterme — araçlar: Docker Compose, Python 3
- 6. adım — Python ile gizli anahtar üretme komutunu gösterme — araçlar: Python 3
- 7. adım — HTTP seçeneğinde gizli anahtarı yerleştirme ve docker compose up -d ile başlatma — araçlar: Docker Compose
- 8. adım — HTTPS seçeneğinde compose ve Caddyfile indirme, anahtarı ve alan adını ayarlama — araçlar: Caddy, Docker Compose, Let's Encrypt
- 9. adım — HTTPS kurulumunu docker-compose-ssl.yml ile başlatma — araçlar: Docker Compose, Caddy
- 10. adım — Durdurma komutlarını gösterme — araçlar: Docker Compose
- 11. adım — Gerekli portları ve TURN röle aralığını açıklama — araçlar: STUN/TURN
- 12. adım — HTTP/HTTPS portlarını özelleştirmeyi gösterme — araçlar: Docker Compose, Caddy
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
