# Scout is a free tool that finds verified emails from social media bios — no paid
## Künye
Scout is a free tool that finds verified emails from social media bios — no paid · gittrend.io · süre: 0:32 · ? · https://www.instagram.com/reel/DbJtLyLAJ2D/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-26 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 31124 tk · claude-haiku-5-5: claude-haiku-5-5 · 41801 tk
## Özet
Kısa Instagram reel'i: Scout adlı açık kaynak (MIT) Python CLI aracını tanıtıyor. Araç Instagram, TikTok, LinkedIn, GitHub, YouTube, Twitch, Pinterest ve Linktree profillerinden e-posta, telefon ve bağlantı çekiyor. E-postaları ücretli API olmadan SMTP ile doğrulayıp 0-100 puanlıyor ve CSV'ye aktarıyor. Hunter.io'ya ücretsiz alternatif olarak sunuluyor. Video GitHub README sayfasını kaydırarak gösteriyor.
## Bölümler
- 0:00 Scout tanıtımı ve GitHub README
- 0:12 Desteklenen platformlar ve özellikler
- 0:18 LinkedIn ve proxy kurulumu
- 0:24 Zenginleştirme adımları ve sınırlamalar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Scout | yok | CLI | https://github.com/kiryano/Scout | Sosyal medya biyografilerinden e-posta, telefon ve bağlantı çekip SMTP ile doğrulayan, CSV'ye aktaran ücretsiz Python CLI aracı. | 0:00 | README başlığı Scout; 'Lead generation tool for appointment setters' açıklaması. (karede: GitHub kiryano/Scout README sayfası, Scout başlığı, Install ve Usage kod blokları, ASCII Scout logosu.) |
| Hunter.io | yok | CLI | yok | Ücretli e-posta bulma servisi; Scout'un ücretsiz alternatifi olarak anılıyor, README'de isteğe bağlı destek var. | 0:00 | It's a free alternative to tools like Hunter.io. |
| SMTP verification | yok | teknik | yok | Her e-posta adayı posta sunucusuna SMTP ile sorularak doğrulanıyor. | 0:13 | Email enrichment with SMTP verification (no paid API needed) (karede: Features listesinde 'Email enrichment with SMTP verification (no paid API needed)' maddesi.) |
| DNS MX lookup | yok | teknik | yok | Şirket alan adı DNS MX sorgusuyla bulunuyor. | 0:26 | 4. Finds the company domain via DNS MX lookup (karede: kanıttan) 4. Finds the company domain via DNS MX lookup |
| Python | yok | teknik | yok | Scout Python ile yazılmış; Python 3.10+ gerekiyor. | 0:00 | python 3.10+ rozeti ve pip install komutu (karede: README başında 'python 3.10+' rozeti ve pip install -r requirements.txt satırı.) |
| LinkedIn li_at cookie | yok | teknik | yok | LinkedIn kazıması için tarayıcıdan alınan oturum çerezi .env'e eklenir. | 0:18 | Copy the value of li_at; LINKEDIN_COOKIE=... · kanıt: kare (karede: LinkedIn Setup adımları ve LINKEDIN_COOKIE=your_li_at_cookie_value kod bloğu.) |
| Proxy rotation | yok | teknik | yok | SCOUT_PROXY, SCOUT_PROXY_FILE ve SCOUT_FREE_PROXY ile proxy ayarı. | 0:24 | Proxy Setup bölümü (karede: Proxy Setup kod bloğunda SCOUT_PROXY, SCOUT_PROXY_FILE=proxies.txt, SCOUT_FREE_PROXY=true.) |
| git | yok | CLI | yok | Scout deposunu yerel makineye klonlamak için kullanılır | 0:00 | git clone https://github.com/kiryano/Scout.git (karede: Install bölümünde 'git clone https://github.com/kiryano/Scout.git' komutu yazılı) |
| pip | yok | CLI | yok | Python bağımlılıklarını requirements.txt dosyasından kurar | 0:00 | pip install -r requirements.txt (karede: Install bloğunda 'pip install -r requirements.txt' satırı yazılı) |
| Chrome | yok | teknik | yok | LinkedIn'e giriş yapmak ve çerez değerini almak için kullanılan tarayıcı | 0:18 | 1. Log into LinkedIn in Chrome (karede: LinkedIn Setup bölümünün 1. adımı: 'Log into LinkedIn in Chrome') |
| DevTools | yok | teknik | yok | Chrome geliştirici araçlarında linkedin.com çerezlerinden li_at değerini bulmak için kullanılır (F12) | 0:18 | Open DevTools (F12) > Application > Cookies > linkedin.com (karede: LinkedIn Setup 2. adımı: 'Open DevTools (F12) > Application > Cookies > linkedin.com') |
## Açıklama bağlantıları
- gittrend.io — Açıklamadaki 'More like this' bağlantısı · aday: hayır · Kanalın kendi sitesi; Scout'un parçası ya da kullanılabilir bir araç değil · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/kiryano/Scout.git | Scout deposunu klonlar. (karede: Install bloğunun ilk satırı.) | 0:00 | kare |
| cd Scout | Proje klasörüne girer. (karede: Install bloğunda cd Scout.) | 0:00 | kare |
| pip install -r requirements.txt | Python bağımlılıklarını kurar. (karede: Install bloğunda pip install satırı.) | 0:00 | kare |
| cp .env.example .env | Ortam dosyası şablonunu kopyalar. (karede: Install bloğunun son satırı.) | 0:00 | kare |
| python scout.py | Etkileşimli CLI'yi başlatır. (karede: Usage bloğunun ilk satırı.) | 0:00 | kare |
| python scout.py --verbose | Hata ayıklama günlüğünü açar. (karede: Usage bloğunda '# enable debug logging' yorumuyla.) | 0:00 | kare |
| python scout.py --version | Sürümü gösterir. | 0:14 | kare |
| python scout.py --help | Yardımı gösterir. (karede: Usage bloğunun son satırı.) | 0:00 | kare |
| LINKEDIN_COOKIE=your_li_at_cookie_value | .env dosyasına LinkedIn li_at çerez değerini koyar (kullanıcının kendi değeri girilir) (karede: LinkedIn Setup 4. adımındaki .env kod bloğunda yazılı) | 0:24 | kare |
| SCOUT_PROXY=http://<kullanıcı>:<şifre>@<host>:<port> | Tek proxy tanımlar (şablon; gerçek kimlik bilgisi yazılmadı) (karede: Proxy Setup bloğunda '# Single proxy' altında SCOUT_PROXY satırı) | 0:24 | kare |
| SCOUT_PROXY_FILE=proxies.txt | Satır başına bir proxy içeren dosyadan döndürmeli proxy listesi okur (karede: Proxy Setup bloğunda '# Rotating proxies from file' altında SCOUT_PROXY_FILE satırı) | 0:24 | kare |
| SCOUT_FREE_PROXY=true | Yapılandırma gerektirmeyen ücretsiz anonim proxy kullanımını açar (karede: Proxy Setup bloğunda '# Free anonymous proxies' altında SCOUT_FREE_PROXY satırı) | 0:24 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Scout ücretli API gerektirmeden doğrulanmış e-posta buluyor. | 0:00 | özellik |
| Instagram, TikTok, LinkedIn ve beş platform daha kazınıyor (toplam 8). | 0:00 | sayısal |
| Hunter.io gibi araçlara ücretsiz alternatif. | 0:00 | karşılaştırma |
| E-posta güven skoru 0-100 arası verilir. | 0:14 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Scout | Scout | Scout is a free tool that finds verified emails |
| konuşma 0:00 | Hunter.io | Hunter.io | free alternative to tools like Hunter.io |
| konuşma 0:00 | Instagram, TikTok, LinkedIn platformları | aday değil: başka adayın parçası (Scout) | scrapes profiles from Instagram, TikTok, LinkedIn |
| kare 0:00 | GitHub | aday değil: başka adayın parçası (Scout) | GitHub kiryano/Scout sayfası |
| kare 0:00 | Python | Python | python 3.10+ rozeti |
| kare 0:00 | git clone, pip install, cp .env.example | aday değil: başka adayın parçası (Scout) | Install bloğu |
| kare 0:00 | Discord rozeti | aday değil: başka adayın parçası (Scout) | Discord widget disabled |
| kare 0:00 | MIT lisansı | aday değil: genel kavram | MIT license |
| kare 0:13 | SMTP verification | SMTP verification | Email enrichment with SMTP verification |
| kare 0:26 | DNS MX lookup | DNS MX lookup | Finds the company domain via DNS MX lookup |
| kare 0:18 | LinkedIn li_at cookie | LinkedIn li_at cookie | Copy the value of li_at |
| kare 0:24 | Proxy ayarları | Proxy rotation | SCOUT_PROXY_FILE=proxies.txt |
| kare 0:18 | Chrome DevTools | aday değil: başka adayın parçası (LinkedIn li_at cookie) | Open DevTools (F12) > Application > Cookies |
| kare 0:14 | Lead scoring ve CSV export | aday değil: başka adayın parçası (Scout) | Lead scoring (0-100); CSV export |
| açıklama | gittrend.io | aday değil: sponsor/reklam | More like this → gittrend.io |
| açıklama | Hashtagler | aday değil: konu dışı | #leadgeneration #opensource #python |
| kare 0:10 | Descript/TypeScript/Inter OCR eşleşmeleri | aday değil: konu dışı | OCR gürültüsü |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: GitHub kiryano/Scout README: Install, Usage komutları, 'SCOUT IS A FREE TOOL' altyazısı.
- 0:18: Supported Platforms tablosu ve Features listesi; LinkedIn Setup başlangıcı.
- 0:24: Features, LinkedIn Setup ve Proxy Setup kod blokları.
## Belirsizlikler
- Yorumlar girişsiz alınamadı; repo bağlantısı yorumda verilmiş olabilir.
- Alt yazı dili belirtilmemiş.
- OCR'daki Descript, TypeScript, Inter eşleşmeleri gürültü; videoda kullanılmıyor.
- Hunter.io isteğe bağlı destek olarak README'de geçiyor, kullanılmıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/kiryano/Scout#readme | 0:00 | ekran | evet |
| https://github.com/kiryano/Scout.git | 0:00 | ekran | evet |
| Hunter.io | 0:00 | ses | evet |
| gittrend.io | açıklama | açıklama | hayır |
| company.com | 0:14 | ekran | hayır |
| linkedin.com | 0:18 | ekran | evet |
## İş akışı
- 1. adım — Scout README sayfasını tarayıcıda açıp aracı tanıtma — araçlar: GitHub, Scout
- 2. adım — Depoyu klonlayıp bağımlılıkları kurma ve .env hazırlama — araçlar: git, pip, Python
- 3. adım — Desteklenen 8 platformu ve kazınan alanları gösterme — araçlar: Scout
- 4. adım — Özellik listesini (SMTP, skor, CSV, proxy) gösterme — araçlar: Scout, SMTP verification
- 5. adım — LinkedIn li_at çerezini alıp .env'e ekleme — araçlar: LinkedIn li_at cookie, Chrome
- 6. adım — İsteğe bağlı proxy ayarlama — araçlar: Proxy rotation
- 7. adım — Zenginleştirme adımlarını ve e-posta doğrulamayı anlatma — araçlar: DNS MX lookup, SMTP verification
- 8. adım — Sınırlamaları gösterme — araçlar: Scout
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
