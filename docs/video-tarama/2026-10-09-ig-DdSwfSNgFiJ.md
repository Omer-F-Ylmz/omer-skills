# A modern platform for visual, flexible, and extensible graph-based investigation
## Künye
A modern platform for visual, flexible, and extensible graph-based investigation · git.radar · süre: 1:14 · ? · https://www.instagram.com/reel/DdSwfSNgFiJ/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-13 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 18353 tk · claude-haiku-5-5: claude-haiku-5-5 · 51975 tk
## Özet
Kısa bir Instagram reel'i: açık kaynaklı OSINT grafik araştırma aracı Flowsint'i tanıtıyor. Web siteleri, kripto cüzdanları ve şirket kayıtları gibi verileri otomatik bir ilişki grafiğinde gösteriyor. GitHub'da 8.398 yıldızı var. Ekranda README, Docker ile kurulum komutları, ağ üzerinde dağıtım ve gizli anahtar üretme adımları görünüyor.
## Bölümler
- 0:00 Flowsint'in tanıtımı ve grafik arayüzü
- 0:26 README: kurulum talimatları (Linux/macOS, Windows)
- 0:52 Ağ/sunucu dağıtımı ve gizli anahtarlar
- 1:04 Kapanış: depoya yönlendirme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Flowsint | yok | CLI | https://github.com/reconurge/flowsint | Açık kaynaklı OSINT grafik tabanlı araştırma aracı; varlıklar arası ilişkileri görsel grafikte gösterir. | 0:00 | This tool called FlowSint does for people working in security and research. |
| Docker | yok | CLI | yok | Flowsint'i konteyner olarak çalıştırmak için kullanılıyor. | 0:36 | README'de Docker ön koşulu ve docker compose komutu görünüyor. (karede: kanıttan) README'de Docker ön koşulu ve docker compose komutu görünüyor. |
| Docker Compose | yok | CLI | yok | docker-compose.prod.yml ile hazır imajları çekip başlatır. | 0:46 | docker compose -f docker-compose.prod.yml up -d (karede: kanıttan) docker compose -f docker-compose.prod.yml up -d |
| Make | yok | CLI | yok | Linux/macOS'ta 'make prod' ile kurulum komutu. | 0:37 | make prod ekranda görünüyor. (karede: kanıttan) make prod ekranda görünüyor. |
| Git | yok | CLI | yok | Depoyu klonlamak için kullanılıyor. | 0:43 | git clone https://github.com/reconurge/flowsint.git (karede: kanıttan) git clone https://github.com/reconurge/flowsint.git |
| GitHub | yok | teknik | https://github.com/reconurge/flowsint | Flowsint deposunun barındırıldığı platform. | 0:00 | sitting at a solid 8,398 stars on GitHub right now. |
| OpenSSL | yok | CLI | yok | AUTH_SECRET için openssl rand -hex 32 ile gizli değer üretir. | 1:12 | AUTH_SECRET — signs authentication tokens. Generate one: openssl rand -hex 32 (karede: kanıttan) AUTH_SECRET — signs authentication tokens. Generate one: openssl rand -hex 32 |
| Python | yok | CLI | yok | MASTER_VAULT_KEY_V1 üretmek için python3 -c komutu. | 1:12 | python3 -c "import os, base64; print('base64:' + ... (karede: kanıttan) python3 -c "import os, base64; print('base64:' + ... |
| PostgreSQL | yok | teknik | yok | Flowsint'in veritabanı bileşeni; ağa açılmaz. | 1:12 | PostgreSQL, Redis, Neo4j and the API are bound to 127.0.0.1 (karede: kanıttan) PostgreSQL, Redis, Neo4j and the API are bound to 127.0.0.1 |
| Redis | yok | teknik | yok | Flowsint yığınının bileşeni, yalnızca 127.0.0.1'e bağlı. | 1:12 | PostgreSQL, Redis, Neo4j and the API are bound to 127.0.0.1 (karede: kanıttan) PostgreSQL, Redis, Neo4j and the API are bound to 127.0.0.1 |
| Neo4j | yok | teknik | yok | Grafik veritabanı; NEO4J_PASSWORD ile korunur. | 1:12 | NEO4J_PASSWORD — Neo4j database password. (karede: kanıttan) NEO4J_PASSWORD — Neo4j database password. |
| Caddy | yok | CLI | yok | HTTPS için önerilen ters vekil sunucu (reverse proxy). | 1:12 | Example with Caddy: reverse_proxy 127.0.0.1:5173 (karede: kanıttan) Example with Caddy: reverse_proxy 127.0.0.1:5173 |
| nginx | yok | teknik | yok | Frontend'in Host-header izin listesi flowsint-app/nginx.conf içinde. | 1:02 | allowlist in flowsint-app/nginx.conf (look for map $http_host) (karede: kanıttan) allowlist in flowsint-app/nginx.conf (look for map $http_host) |
| PowerShell | yok | CLI | yok | Windows kurulumunun çalıştığı kabuklardan biri (cmd ile birlikte). | 0:39 | No Make needed. Works in both Command Prompt (cmd) and PowerShell. (karede: kanıttan) No Make needed. Works in both Command Prompt (cmd) and PowerShell. |
| Docker Desktop | yok | CLI | yok | Windows'ta çalışır durumda olması gereken ön koşul. | 0:42 | Docker Desktop (make sure it is running before the next step) (karede: kanıttan) Docker Desktop (make sure it is running before the next step) |
| Command Prompt (cmd) | yok | CLI | yok | Windows komut satırı; Windows'ta kurulum komutları burada çalıştırılır. | 0:39 | Works in both Command Prompt (cmd) and PowerShell. (karede: Görsel gönderilmedi; OCR metni: 'Command Prompt (cmd)' ifadesi okundu.) |
## Açıklama bağlantıları
- https://github.com/reconurge/flowsint — Flowsint GitHub deposu · aday: evet (Flowsint) · İzleyicinin kurup kullanabileceği araç; videoda anlatılan Flowsint. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/reconurge/flowsint.git | Flowsint deposunu klonlar. (karede: Windows bölümünde git clone satırı görünüyor (OCR).) | 0:43 | kare |
| cd flowsint | Klasöre girer. (karede: Linux/macOS bölümünde cd flowsint görünüyor (OCR).) | 0:37 | kare |
| make prod | Linux/macOS'ta üretim kurulumunu çalıştırır. (karede: make prod satırı görünüyor (OCR).) | 0:37 | kare |
| copy .env.example .env | Windows'ta ortam dosyasını kopyalar. (karede: copy .env.example .env görünüyor (OCR).) | 0:44 | kare |
| copy .env.example flowsint-api\.env | API için ortam dosyasını kopyalar. (karede: OCR'da bu satır görünüyor.) | 0:44 | kare |
| docker compose -f docker-compose.prod.yml up -d | Hazır imajları çekip arka planda başlatır. (karede: 3. Start başlığı altında komut görünüyor (OCR).) | 0:46 | kare |
| cp .env.example .env | Sunucu dağıtımında ortam dosyasını oluşturur. (karede: Deploy on a network bölümündeki kod bloğunda görünüyor.) | 1:12 | kare |
| openssl rand -hex 32 | AUTH_SECRET için rastgele değer üretir. (karede: AUTH_SECRET maddesinde satır içi kod olarak görünüyor.) | 1:12 | kare |
| python3 -c "import os, base64; print('base64:' + base64.b64encode(os.urandom(32)).decode())" | MASTER_VAULT_KEY_V1 için base64 anahtar üretir. (karede: MASTER_VAULT_KEY_V1 maddesinde görünüyor.) | 1:12 | kare |
| copy .env.example flowsint-app\.env | Windows'ta uygulama klasörü için ortam dosyası kopyalar. (karede: Görsel gönderilmedi; OCR metni bozuk, satır kısmen okundu.) | 0:45 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Flowsint GitHub'da 8.398 yıldıza sahip. | 0:00 | sayısal |
| Kendi bilgisayarınızda kurarak bulguları tamamen özel tutabilirsiniz. | 0:52 | özellik |
| Web siteleri, kripto cüzdanları ve şirket kayıtları arasındaki bağlantıları otomatik grafikte gösterir. | 0:00 | özellik |
| Ağa yalnızca 5173 portu açılır; veritabanları 127.0.0.1'e bağlıdır. | 1:12 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Flowsint | Flowsint | This tool called FlowSint does for people working in security. |
| açıklama | github.com/reconurge/flowsint bağlantısı | Flowsint | Açıklamadaki depo bağlantısı. |
| konuşma 0:00 | GitHub | GitHub | sitting at a solid 8,398 stars on GitHub |
| açıklama | TypeScript | aday değil: genel kavram | Açıklamada dil etiketi: TypeScript. |
| açıklama | Hashtag'ler (#opensource vb.) | aday değil: genel kavram | Genel etiketler. |
| kare 0:00 | Apache-2.0 lisansı | aday değil: genel kavram | README'de lisans rozeti. |
| kare 0:00 | Discord rozeti | aday değil: konu dışı | README'de Join Server rozeti. |
| kare 0:00 | Buy Me a coffee / Ko-fi rozetleri | aday değil: konu dışı | README'de destek rozetleri. |
| kare 0:00 | ETHICS.md | aday değil: başka adayın parçası (Flowsint) | Ethics: Please read ETHICS.md. |
| ekran 0:17 | FakeSubdomainEnricher / FakeResolveEnricher | aday değil: başka adayın parçası (Flowsint) | Flowsint demo arayüzünde enricher listesi. |
| ekran 0:19 | mistery-domain.org demo alanı | aday değil: başka adayın parçası (Flowsint) | Demo grafikteki sahte alan adı. |
| ekran 0:37 | Make / make prod | Make | make prod komutu. |
| ekran 0:36 | Docker | Docker | 1. Install pre-requisites · Docker. |
| ekran 0:42 | Docker Desktop | Docker Desktop | Docker Desktop (make sure it is running). |
| ekran 0:43 | git clone | Git | git clone komutu. |
| ekran 0:46 | docker compose | Docker Compose | docker compose -f docker-compose.prod.yml up -d |
| ekran 0:39 | PowerShell / cmd | PowerShell | Works in both Command Prompt (cmd) and PowerShell. |
| ekran 0:49 | localhost:5173/register | aday değil: başka adayın parçası (Flowsint) | Flowsint yerel kayıt sayfası. |
| ekran 0:58 | openssl rand -hex 32 | OpenSSL | Anahtar üretme komutu. |
| ekran 1:00 | python3 -c base64 komutu | Python | MASTER_VAULT_KEY_V1 üretimi. |
| ekran 1:04 | PostgreSQL | PostgreSQL | PostgreSQL, Redis, Neo4j and the API are bound. |
| ekran 1:04 | Redis | Redis | Aynı cümlede. |
| ekran 1:04 | Neo4j | Neo4j | Aynı cümlede; NEO4J_PASSWORD. |
| ekran 1:02 | nginx.conf | nginx | flowsint-app/nginx.conf. |
| ekran 1:09 | Caddy | Caddy | Example with Caddy. |
| ekran 1:07 | FLOWSINT_VERSION | aday değil: başka adayın parçası (Flowsint) | FLOWSINT_VERSION=1.2.10. |
| sözlük | Linear, Next.js, Inter, Meshy | aday değil: konu dışı | Yanlış OCR/ses eşleşmeleri; videoda kullanılmıyor. |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı. |
## Kareden okunanlar
- 0:00: reconurge/flowsint GitHub sayfası: Flowsint README, lisans Apache-2.0, 'open-source OSINT graph exploration tool', demo1.mp4, altyazı 'You've just found a powerful way'.
- 1:04: Deploy on a network bölümü: git clone, cp .env.example, docker compose komutu; AUTH_SECRET, MASTER_VAULT_KEY_V1, NEO4J_PASSWORD; altyazı 'And secure while you explore'.
- 1:12: Host-header allowlist, port 5173, FLOWSINT_VERSION=1.2.10, Caddy ile HTTPS örneği; altyazı 'Go check out the Flowsint repository'.
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Sözlük eşleşmelerinden Linear, Next.js, Inter, Meshy, Go ve Discord videoda kullanılmıyor/yanlış OCR; aday yapılmadı (Discord yalnızca README rozeti).
- Altyazıda 'FlowSynth' yazımı var; doğru ad Flowsint.
- Windows ortam dosyası komutlarının bazı OCR satırları bozuk (flowsint-core, flowsint-app yolları tam okunmadı).
- Videoda gösterilen demo arayüzündeki FakeSubdomainEnricher / FakeResolveEnricher kısa göründü, ayrı araç sayılmadı.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/reconurge/flowsint | açıklama | açıklama | evet |
| github.com/reconurge/flowsint.git | 0:38 | ekran | evet |
| http://localhost:5173/register | 0:49 | ekran | hayır |
| flowsint.example.com | 1:09 | ekran | hayır |
| mistery-domain.org | 0:23 | ekran | hayır |
| http://<server-ip>:5173 | 1:04 | ekran | hayır |
| www.mistery-domain.org | 0:21 | ekran | hayır |
## İş akışı
- 1. adım — Flowsint'in ne yaptığını ve OSINT grafiğini tanıtma — araçlar: Flowsint
- 2. adım — GitHub README ve demo görüntüsünü gösterme — araçlar: GitHub
- 3. adım — Ön koşulları kurma (Docker) — araçlar: Docker, Docker Desktop
- 4. adım — Depoyu klonlama — araçlar: Git
- 5. adım — Linux/macOS'ta make prod ile kurma — araçlar: Make
- 6. adım — Windows'ta .env dosyalarını kopyalama — araçlar: PowerShell
- 7. adım — Docker Compose ile servisleri başlatma — araçlar: Docker Compose
- 8. adım — localhost:5173/register'da hesap oluşturma — araçlar: Flowsint
- 9. adım — Sunucu dağıtımı için .env düzenleme — araçlar: Git, Docker Compose
- 10. adım — Gizli anahtarları üretme — araçlar: OpenSSL, Python
- 11. adım — Host-header izin listesini ayarlama — araçlar: nginx
- 12. adım — HTTPS için ters vekil kurma — araçlar: Caddy
## Promptlar
- yok
