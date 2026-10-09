# OpenWA turns your WhatsApp into a free, self-hosted API gateway you can run loca
## Künye
OpenWA turns your WhatsApp into a free, self-hosted API gateway you can run loca · gittrend.io · süre: 0:31 · ? · https://www.instagram.com/reel/DZ3PUfYlK6z/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-15 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 16316 tk · claude-haiku-5-5: claude-haiku-5-5 · 44538 tk
## Özet
OpenWA, WhatsApp hesaplarını API'ye çeviren açık kaynaklı, kendi sunucunuzda çalışan bir WhatsApp API ağ geçididir. Twilio gibi ücretli sağlayıcıların alternatifi olarak tanıtılıyor. Docker ile ya da tek adımlı kurulumla başlıyor. Çoklu oturum, kontrol paneli ve webhook yönetimi sunuyor. Video GitHub README sayfasını gezdiriyor.
## Bölümler
- 0:00 OpenWA tanıtımı ve Why OpenWA tablosu
- 0:13 Çekirdek özellikler tabloları
- 0:25 Quick Start: Docker kurulumu
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OpenWA | yok | CLI | https://github.com/rmyndharis/OpenWA | Açık kaynaklı, kendi sunucuda çalışan WhatsApp API ağ geçidi | 0:00 | README başlığı 'Open Source WhatsApp API Gateway', github.com/rmyndharis/OpenWA (karede: kanıttan) README başlığı 'Open Source WhatsApp API Gateway', github.com/rmyndharis/OpenWA |
| Docker | yok | CLI | yok | OpenWA'yı docker compose ile çalıştırma yolu | 0:27 | You start it with Docker or a one-step install. |
| Twilio | yok | teknik | yok | OpenWA'nın yerine geçtiği ücretli mesajlaşma sağlayıcısı | 0:00 | replacing paid providers like Twilio |
| gittrend.io | yok | teknik | yok | Açıklamada anılan benzer içerik servisi | açıklama | More like this → gittrend.io |
| NestJS | yok | teknik | yok | OpenWA'nın arka uç çatısı (rozet) | 0:03 | Rozet 'NestJS 11.x' README'de görünüyor (karede: kanıttan) Rozet 'NestJS 11.x' README'de görünüyor |
| TypeScript | yok | teknik | yok | OpenWA'nın yazıldığı dil | 0:03 | Rozet 'TypeScript 5.x' (karede: kanıttan) Rozet 'TypeScript 5.x' |
| React | yok | teknik | yok | Kontrol paneli arayüzü | 0:00 | Modern React UI for session, webhook, and API key management (karede: kanıttan) Modern React UI for session, webhook, and API key management |
| SQLite | yok | teknik | yok | Gömülü veritabanı seçeneği | 0:03 | database engines (SQLite/PostgreSQL) (karede: kanıttan) database engines (SQLite/PostgreSQL) |
| PostgreSQL | yok | teknik | yok | Üretim düzeyi veritabanı seçeneği | 0:03 | database engines (SQLite/PostgreSQL) (karede: kanıttan) database engines (SQLite/PostgreSQL) |
| Redis | yok | teknik | yok | İsteğe bağlı önbellek katmanı | 0:24 | Redis Cache: Optional performance caching (karede: kanıttan) Redis Cache: Optional performance caching |
| S3 | yok | teknik | yok | Medya depolama seçeneği | 0:03 | storage backends (Local/S3) (karede: kanıttan) storage backends (Local/S3) |
| n8n | yok | teknik | yok | İş akışı otomasyon entegrasyonu | 0:00 | n8n Integration: Community nodes for workflow automation (karede: kanıttan) n8n Integration: Community nodes for workflow automation |
| ioBroker | yok | teknik | yok | Topluluk adaptörü örneği | 0:00 | Third-party integrations (e.g. ioBroker) (karede: kanıttan) Third-party integrations (e.g. ioBroker) |
| Swagger | yok | teknik | yok | Etkileşimli API belgeleri | 0:28 | # Swagger: http://localhost:2785/api/docs (karede: kanıttan) # Swagger: http://localhost:2785/api/docs |
| Kubernetes | yok | teknik | yok | Sağlık kontrolü probları | 0:24 | Health Checks: Kubernetes-ready probes (karede: kanıttan) Health Checks: Kubernetes-ready probes |
| Podman | yok | CLI | yok | Docker yerine kullanılabilen alternatif | 0:28 | Using Podman instead of Docker? rootless mode requires the socket (karede: kanıttan) Using Podman instead of Docker? rootless mode requires the socket |
| Git | yok | CLI | yok | Depoyu klonlama | 0:27 | git clone https://github.com/rmyndharis/OpenWA.git (karede: kanıttan) git clone https://github.com/rmyndharis/OpenWA.git |
| GitHub | yok | teknik | yok | Deponun barındığı servis | 0:00 | github.com/rmyndharis/OpenWA (karede: kanıttan) github.com/rmyndharis/OpenWA |
| systemd | yok | CLI | yok | systemctl --user ile podman.socket servisini etkinleştirir ve başlatır | 0:29 | systemctl --user enable podman.socket · kanıt: kare (karede: systemctl --user enable podman.socket) |
| Node.js | yok | teknik | yok | OpenWA'nın çalışma zamanı; rozette node 22.x | 0:00 | node 22.x rozeti (karede: README rozetlerinde 'node 22.x' yazıyor.) |
## Açıklama bağlantıları
- gittrend.io — Açıklamadaki 'More like this' bağlantısı; ilgili depoları listeleyen içerik sitesi · aday: hayır · Videoda kullanılan araç değil; ilgili içerik sitesine yönlendirme · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/rmyndharis/OpenWA.git | OpenWA deposunu yerel makineye klonlar | 0:27 | kare |
| cd OpenWA | Klonlanan klasöre girer | 0:27 | kare |
| docker compose -f docker-compose.dev.yml up -d | OpenWA'yı Docker ile arka planda başlatır | 0:27 | kare |
| systemctl --user enable podman.socket | Podman rootless için soketi etkinleştirir | 0:29 | kare |
| systemctl --user start podman.socket | Podman soketini başlatır | 0:29 | kare |
| git clone https://github.com/rmyndharis/0penWA.git | Podman bölümünde depoyu klonlar (ekranda '0penWA' yazımı OCR ile okundu) | 0:28 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| OpenWA tamamen açık kaynak ve ücretsiz, lisans ücreti ya da özellik kilidi yok | 0:12 | özellik |
| Twilio gibi ücretli sağlayıcıların yerini alıyor | 0:12 | karşılaştırma |
| Çoklu oturum ve webhook yönetimi için kontrol paneli sunuyor | 0:15 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | OpenWA | OpenWA | OpenWA turns your WhatsApp accounts into an API |
| konuşma 0:00 | Twilio | Twilio | replacing paid providers like Twilio |
| konuşma 0:00 | Docker | Docker | You start it with Docker or a one-step install. |
| açıklama | gittrend.io | gittrend.io | More like this → gittrend.io |
| açıklama | Hashtagler (#opensource #whatsapp #api vb.) | aday değil: genel kavram | #opensource #whatsapp #api #selfhosted |
| kare 0:03 | NestJS | NestJS | Rozet NestJS 11.x |
| kare 0:03 | TypeScript | TypeScript | Rozet TypeScript 5.x |
| kare 0:00 | React | React | Modern React UI |
| kare 0:03 | SQLite | SQLite | SQLite/PostgreSQL |
| kare 0:03 | PostgreSQL | PostgreSQL | SQLite/PostgreSQL |
| kare 0:24 | Redis | Redis | Redis Cache |
| kare 0:03 | S3 | S3 | Local/S3 |
| kare 0:00 | n8n | n8n | n8n Integration |
| kare 0:00 | ioBroker | ioBroker | Third-party integrations (e.g. ioBroker) |
| kare 0:28 | Swagger | Swagger | Swagger: localhost:2785/api/docs |
| kare 0:24 | Kubernetes | Kubernetes | Kubernetes-ready probes |
| kare 0:28 | Podman | Podman | Using Podman instead of Docker? |
| kare 0:27 | Git | Git | git clone komutu |
| kare 0:00 | GitHub | GitHub | github.com/rmyndharis/OpenWA |
| kare 0:04 | GitHub giriş sayfası bağlantısı | aday değil: konu dışı | https://github.com/login?return_to |
| kare 0:24 | Redis dışı özellik tabloları (Rate Limiting, CIDR Whitelisting, Audit Logging vb.) | aday değil: başka adayın parçası (OpenWA) | Advanced tablosu |
| kare 0:00 | MIT license rozeti | aday değil: genel kavram | license MIT |
| yorum | Yorumlar | aday değil: konu dışı | yorum: girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: GitHub rmyndharis/OpenWA README: rozetler version 0.4.8, MIT, NestJS 11.x, docker ready, TypeScript 5.x; 'Why OpenWA?' tablosu
- 0:03: Dosya listesi (src, test, .dockerignore, .env.example, .env.minimal) ve commit mesajları
- 0:22: Core Features, Messaging, Advanced tabloları (REST API, Multi-Session, Webhooks, Groups API, Rate Limiting, CIDR Whitelisting vb.)
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Altyazıdaki 'Comment link' çağrısıyla repo bağlantısı yorumda paylaşılıyor olabilir; görülemedi.
- 0:00 ve 0:22 dışındaki kareler görsel olarak gönderilmedi; OCR'dan okundu.
- OCR'daki 'Descript', 'Inter', 'v0', 'Go', 'Make' sözlük eşleşmeleri OCR gürültüsü, videoda kullanılmıyor.
- Kurulum komutlarının tam metni OCR'dan kısmen okundu.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/rmyndharis/OpenWA | 0:00 | ekran | hayır |
| https://github.com/login?return_to | 0:05 | ekran | hayır |
| https://github.com/rmyndharis/OpenWA.git | 0:27 | ekran | hayır |
| http://localhost:2785 | 0:27 | ekran | hayır |
| http://localhost:2785/api | 0:28 | ekran | hayır |
| http://localhost:2785/api/docs | 0:28 | ekran | hayır |
| gittrend.io | açıklama | açıklama | evet |
| https://github.com/rmyndharis/0penWA.git | 0:28 | ekran | evet |
| http://localhost:2785/ap1/docs | 0:29 | ekran | hayır |
## İş akışı
- 1. adım — GitHub'da OpenWA README sayfasını açıp 'Why OpenWA?' bölümünü gösterme — araçlar: GitHub, OpenWA
- 2. adım — Dosya listesi ve son commitleri gösterme — araçlar: GitHub
- 3. adım — Core Features, Messaging ve Advanced özellik tablolarını gezme — araçlar: GitHub, OpenWA
- 4. adım — Quick Start'ta Docker kurulumunu (git clone, docker compose) gösterme — araçlar: Git, Docker
- 5. adım — Podman notunu ve yerel geliştirme seçeneğini gösterme — araçlar: Podman
## Promptlar
- yok
