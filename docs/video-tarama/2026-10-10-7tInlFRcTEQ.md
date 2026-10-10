# n8n’i Kendi Bilgisayarında Ücretsiz Çalıştır ve Deneme Süresi Kısıtlamasından Kurtul (Self-host n8n)
## Künye
n8n’i Kendi Bilgisayarında Ücretsiz Çalıştır ve Deneme Süresi Kısıtlamasından Kurtul (Self-host n8n) · Ömer Göçmen | Yapay Zeka & Otomasyon · süre: 25:35 · tr-orig · https://youtu.be/7tInlFRcTEQ · şema 2
motor: parti 2026-10-10-short-14 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (44)
kareler: girdi ≤40000 jeton için 60→44
claude-sonnet-5-5: claude-sonnet-5-5 · 72839 tk · claude-haiku-5-5: claude-haiku-5-5 · 236580 tk
## Özet
Ömer Göçmen, n8n bulut sürümünün deneme süresi bittiğinde n8n'i Windows bilgisayarda ücretsiz self-host etmenin iki yolunu gösteriyor: Docker Desktop (volume oluşturma + docker run) ve Node.js ile npm/npx. Gemini Chat Model ile AI Agent iş akışı kurup test ediyor. Ardından konteyner yönetimi (durdurma, silme, yeniden oluşturma), Görev Zamanlayıcı ile otomatik başlatma ve her şeyin kaldırılması (Docker Desktop, .n8n klasörü, Node.js) anlatılıyor.
## Bölümler
- 0:00 Giriş ve deneme süresi sorunu
- 1:43 n8n dokümantasyonu ve Self-host sayfası
- 3:08 Docker nedir, Docker kurulum komutları
- 4:08 Docker Desktop indirme ve kurma
- 7:06 Docker Desktop arayüzü: konteyner, image, volume
- 8:12 Volume ve konteyner komutlarını çalıştırma
- 10:46 n8n hesap kurulumu ve lisans anahtarı
- 12:00 Gemini credential ve AI Agent testi
- 13:56 Konteyner yönetimi: durdur, sil, yeniden oluştur
- 15:36 Docker'ı tamamen kaldırma
- 16:26 npm yöntemi: Node.js kurulumu
- 18:28 npx n8n ile çalıştırma
- 22:12 Görev Zamanlayıcı ile otomatik başlatma
- 23:28 Verilerin yeri ve npm kurulumunu kaldırma
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n | yok | iş akışı | https://github.com/n8n-io/n8n | İş akışı otomasyon platformu; self-host ediliyor | 0:00 | n8n.io ana sayfası ve localhost:5678 arayüzü gösteriliyor (karede: kanıttan) n8n.io ana sayfası ve localhost:5678 arayüzü gösteriliyor |
| Docker Desktop | yok | CLI | yok | n8n'i konteyner olarak çalıştırmak için kuruldu | 4:08 | Docker Desktop 4.38.0 kurulum penceresi (karede: kanıttan) Docker Desktop 4.38.0 kurulum penceresi |
| Docker | yok | teknik | yok | Konteynerleştirme; volume ve run komutları | 8:16 | docker volume create n8n_data terminalde (karede: kanıttan) docker volume create n8n_data terminalde |
| Docker volume | yok | teknik | yok | n8n verilerini kalıcı saklayan n8n_data volume | 8:36 | Volumes sekmesinde n8n_data görünüyor (karede: kanıttan) Volumes sekmesinde n8n_data görünüyor |
| Node.js | yok | CLI | yok | npm yöntemi için gereken çalışma ortamı (v22 LTS) | 16:48 | Download Node.js (LTS) v22.14.0 sayfası (karede: kanıttan) Download Node.js (LTS) v22.14.0 sayfası |
| npm | yok | CLI | yok | n8n'i global kurmak için paket yöneticisi | 18:16 | npm install -g n8n komutu dokümanda (karede: kanıttan) npm install -g n8n komutu dokümanda |
| npx | yok | CLI | yok | n8n'i kurmadan çalıştırma (npx n8n) | 18:28 | Komut istemi başlığı 'npx n8n' (karede: kanıttan) Komut istemi başlığı 'npx n8n' |
| Windows Görev Zamanlayıcı | yok | teknik | yok | Bilgisayar açılırken n8n komutunu otomatik çalıştırma | 22:12 | Görev oluştur, tetikleyici bilgisayar başlatılırken, eylem program başlat · kanıt: yok |
| Google Gemini Chat Model | yok | plugin | yok | AI Agent'a bağlanan sohbet modeli düğümü | 12:00 | Google Gemini Chat Model düğümü ayar paneli (karede: kanıttan) Google Gemini Chat Model düğümü ayar paneli |
| Gemini 2.0 Flash | yok | teknik | yok | Testte seçilen model | 13:04 | models/gemini-2.0-flash listede seçiliyor (karede: kanıttan) models/gemini-2.0-flash listede seçiliyor |
| Google AI Studio | yok | iş akışı | yok | Gemini API anahtarı oluşturma servisi | 12:32 | Get API key sayfası aistudio.google.com · kanıt: kare (karede: Get API key sayfası aistudio.google.com) |
| AI Agent | yok | plugin | yok | n8n AI Agent düğümü (Tools Agent) | 12:00 | AI Agent paneli, Agent: Tools Agent, prompt 'test' · kanıt: kare (karede: AI Agent paneli, Agent: Tools Agent, prompt 'test') |
| Windows PowerShell | yok | CLI | yok | Docker terminali ve komutların çalıştığı kabuk | 8:12 | Docker Desktop terminalinde Windows PowerShell (karede: kanıttan) Docker Desktop terminalinde Windows PowerShell |
| Komut İstemi (cmd) | yok | CLI | yok | npx n8n komutunu çalıştırmak için | 18:36 | cmd yazacağım ve sağ tıklayarak paste edeceğim · kanıt: yok |
| Google Chrome | yok | ipucu | yok | Tarayıcı olarak kullanılıyor | 1:34 | Chrome sekmeleri ve adres çubuğu · kanıt: kare (karede: Chrome sekmeleri ve adres çubuğu) |
| SQLite | yok | teknik | yok | n8n varsayılan veritabanı (dokümanda) | 3:08 | Ekran metni: n8n uses SQLite to save credentials |
| PostgreSQL | yok | teknik | yok | Docker'da alternatif veritabanı; örnek olarak anlatıldı | 7:06 | postgre sql'e mi ihtiyacınız var ... ayağa kaldırabiliyorsunuz |
| Gemini API | yok | teknik | yok | Google'ın Gemini modellerine API anahtarıyla erişim servisi; n8n'deki Google Gemini Chat Model düğümü bunu kullanıyor. | 12:20 | Google Gemini(PaLM) Api account (karede: n8n'de 'Google Gemini(PaLM) Api account' penceresi; Host alanı generativelanguage.googleapis.com.) |
| Gemini credential ve AI Agent bağlantısını test etme | yok | prompt | yok | AI Agent düğümüne basit bir test mesajı ('test') gönderilerek Gemini bağlantısının çalıştığı doğrulanıyor. | 13:56 | kaynak: kare |
## Açıklama bağlantıları
- https://blog.tekhnelogos.com/docker-nedir-ve-ne-icin-kullanilir — Docker nedir yazısı (blog) · aday: hayır · Referans blog yazısı; izleyicinin kullanacağı araç değil · sınıf: diğer
- https://www.youtube.com/watch?v=1nzxcq61Ffw — Kanalın diğer videosu · aday: hayır · Referans video bağlantısı · sınıf: diğer
- https://www.youtube.com/watch?v=wlyl_yv7nSk&lc=Ugz7N1NOe3aQdwU6rwJ4AaABAg&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanalın diğer videosu · aday: hayır · Referans video bağlantısı · sınıf: diğer
- https://www.youtube.com/watch?v=uKoi9uQLdCs&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanalın diğer videosu · aday: hayır · Referans video bağlantısı · sınıf: diğer
- https://www.youtube.com/watch?v=gXhVFwzN4_4&t=2s&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanalın diğer videosu · aday: hayır · Referans video bağlantısı · sınıf: diğer
- https://www.youtube.com/watch?v=bXBS2Hzr-vU&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanalın diğer videosu · aday: hayır · Referans video bağlantısı · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| docker volume create n8n_data | n8n verileri için kalıcı volume oluşturur (karede: PS C:\Users\omer_> docker volume create n8n_data) | 8:16 | kare |
| docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n | n8n konteynerini 5678 portunda başlatır, volume bağlar (karede: docker run komutu terminalde, n8n_data:/home/node/.n8n) | 8:54 | kare |
| npx n8n | n8n'i kurmadan çalıştırır (karede: [yol]>npx n8n ve pencere başlığı 'npx n8n') | 18:28 | kare |
| npm install n8n -g | n8n'i global kurar (dokümanda gösterildi) (karede: Dokümanda npm install n8n -g) | 19:16 | kare |
| n8n start | Global kurulu n8n'i başlatır (karede: Dokümanda n8n start) | 19:10 | kare |
| npm update -g n8n | n8n'i son sürüme günceller (dokümanda) (karede: To update your n8n instance... npm update -g n8n) | 19:36 | kare |
| npm install -g n8n@next | next sürümünü kurar (dokümanda) (karede: npm install -g n8n@next) | 16:28 | kare |
| -e N8N_DEFAULT_BINARY_DATA_MODE=filesystem | Yorumda önerilen docker run ortam değişkeni | açıklama | açıklama |
| npm install -g n8n | n8n'i npm ile global olarak kurar. | 19:16 | altyazı |
| curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=[gizlendi]" | Gemini API'yi komut satırından test etmek için örnek istek; videoda gösterildi, çalıştırılmadı. Anahtar yerine yer tutucu yazıldı. (karede: Google AI Studio'da 'Quickly test the Gemini API' bölümünde curl komutu görünüyor.) | 12:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Self-host edilen n8n sınırsız kullanılabilir; 15 günlük deneme limiti yoktur. | 10:46 | özellik |
| Volume silinmediği sürece konteyner silinse bile workflow'lar korunur. | 15:16 | özellik |
| npm yöntemi Docker'a göre daha basit ve indirmesi hızlıdır. | 16:26 | karşılaştırma |
| npm kurulumunda komut satırı kapanırsa n8n erişilemez olur; Görev Zamanlayıcı ile otomatikleştirilebilir. | 22:12 | öneri |
| Docker Desktop indirmesi yaklaşık 524 MB, Node.js yaklaşık 29,5 MB. | 4:08 | sayısal |
| Gemini'de günlük yaklaşık 1600 istek hakkı olduğunu hatırladığını söylüyor (emin değil). | 13:14 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:00 | n8n.io ana sayfası | n8n | n8n.io sayfası ve Sign in |
| ekran 0:20 | omerapp.app.n8n.cloud bulut hesabı, 2 days left | n8n | 2 days left in your n8n trial |
| ekran 1:34 | n8n.tekhnelogos.com | aday değil: konu dışı | Arama önerisi |
| ekran 1:34 | ChatGPT kısayolu | aday değil: konu dışı | Tarayıcı yeni sekme kısayolu |
| ekran 1:43 | Google arama | Google Chrome | google.com/search?q=n8n |
| ekran 1:46 | Discord menüsü | aday değil: konu dışı | Community menüsünde listeleniyor |
| ekran 2:04 | n8n Docs Hosting sayfası | n8n | Self-hosting n8n |
| ekran 2:19 | Asana, Slack, GitHub, Jira, Langchain | aday değil: konu dışı | Docs alt popüler entegrasyon listesi |
| konuşma 2:30 | Docker anlatımı | Docker | Konteyner aracı anlatılıyor |
| ekran 3:08 | SQLite ve PostgreSQL dokümanı | SQLite | n8n uses SQLite to save credentials |
| konuşma 7:06 | PostgreSQL örneği | PostgreSQL | postgre sql'e mi ihtiyacınız var |
| konuşma 7:06 | Yapay zekâ modeli konteyner örneği | aday değil: genel kavram | Docker image varsa model de çalışır |
| ekran 4:08 | WSL, Hyper-V | aday değil: konu dışı | Docker kurulum sayfası gereksinimleri |
| kare 4:28 | Docker Desktop 4.38.0 installer | Docker Desktop | Installing Docker Desktop 4.38.0 |
| kare 6:20 | Google hesap seçimi ile Docker girişi | Docker Desktop | docker.com uygulamasına devam etmek için |
| kare 8:16 | PowerShell terminali | Windows PowerShell | PS C:\Users\omer_> |
| ekran 9:40 | N8N_RUNNERS_ENABLED / task runners uyarısı | aday değil: başka adayın parçası (n8n) | Running n8n without task runners is deprecated |
| kare 11:16 | Lisans anahtarı formu | aday değil: başka adayın parçası (n8n) | Get paid features for free (forever) |
| kare 11:34 | Trigger manually, Telegram/Notion/Airtable menüsü | aday değil: başka adayın parçası (n8n) | n8n trigger menüsü |
| kare 11:40 | AI Agent ve OpenAI düğüm listesi | AI Agent | AI Nodes listesi |
| kare 12:00 | Google Gemini Chat Model | Google Gemini Chat Model | Düğüm paneli |
| kare 12:20 | Google Gemini(PaLM) Api account credential | Google Gemini Chat Model | Host generativelanguage.googleapis.com |
| kare 12:32 | Google AI Studio API keys | Google AI Studio | aistudio.google.com Get API key |
| kare 13:04 | models/gemini-2.0-flash | Gemini 2.0 Flash | Model listesi |
| kare 14:14 | Konteyner pause/start/delete | Docker Desktop | Containers ekranı |
| konuşma 16:26 | npm yöntemi | npm | Install globally with npm |
| kare 16:48 | Node.js indirme | Node.js | Download Node.js (LTS) |
| kare 17:56 | node-gyp, Chocolatey, Python/VS Build Tools | aday değil: konu dışı | Kurulum sihirbazı isteğe bağlı araç ekranı |
| kare 18:36 | npx n8n | npx | Komut istemi - npx n8n |
| ekran 19:42 | n8n --tunnel / cloudflared | aday değil: konu dışı | Dokümanda geçiyor, anlatılmadı |
| kare 22:12 | Görev Zamanlayıcı | Windows Görev Zamanlayıcı | Görev oluştur penceresi |
| konuşma 24:26 | pm2, Forever | aday değil: konu dışı | Alternatif olarak sözlü anıldı, gösterilmedi |
| kare 15:38 | Program kaldır listesi (Anaconda, Cursor, Git, Python vb.) | aday değil: konu dışı | Yüklü programlar listesi |
| kare 23:22 | .ollama, .ipython, Claude, Bolt klasörleri | aday değil: konu dışı | Kullanıcı klasöründeki listede |
| açıklama | Docker/NPM yöntemi | Docker | Açıklama metni |
| açıklama | blog.tekhnelogos.com Docker yazısı | aday değil: konu dışı | Referans blog |
| açıklama | Diğer 5 YouTube videosu | aday değil: konu dışı | İzleyebileceğiniz diğer videolar |
| yorum | ngrok, Telegram, LM Studio, WhatsApp, ffmpeg | aday değil: konu dışı | İzleyici soruları |
| yorum | --rm ve N8N_DEFAULT_BINARY_DATA_MODE=filesystem önerisi | Docker | Sahip yanıtları |
| bağlantılı sayfalar | n8n/Docker/Node.js dokümantasyon sayfaları | aday değil: konu dışı | Referans sayfalar |
## Kareden okunanlar
- 8:16 terminal: PS C:\Users\omer_> docker volume create n8n_data; çıktı n8n_data
- 9:40 konteyner: n8n konteyneri Running, port 5678:5678, Version: 1.81.4, Editor is now accessible via http://localhost:5678
- 13:56 AI Agent: Prompt 'test', çıktı 'Okay! How can I help you today?', Workflow executed successfully
- 4:28 Docker kurulum: Docker Desktop 4.38.0; mevcut 4.34.3 sürümü değiştirme uyarısı
## Belirsizlikler
- Ekran metni ve altyazıda 'nan/naton' n8n anlamına geliyor; sözlükteki Composio, Hostinger, Ollama, Claude Code, Bolt, Llama vb. eşleşmeleri videoda kullanılmıyor (yalnız liste/arka plan).
- Sürüm numaraları (n8n 1.81.4 / npm 0.126.1) OCR'da bozuk; kesin değil.
- Gemini günlük 1600 istek bilgisi konuşmacının hafızasından, doğrulanmadı.
- Görev Zamanlayıcıya girilen komutun tam metni videoda net görünmüyor.
- Kare listesindeki 1:34 ve 1:43 gibi bazı kareler arama geçmişi; Make, Discord, Notion, OpenAI vb. yalnız menü/listede göründü, kullanılmadı.
- Yorumlardaki ngrok, Telegram, LM Studio önerileri videoda gösterilmedi.
## Atlanan segment oranı
0/26 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://n8n.io | 0:00 | ekran | hayır |
| https://docs.n8n.io/hosting/ | 1:56 | ekran | hayır |
| https://docs.n8n.io/hosting/installation/docker/ | 2:18 | ekran | hayır |
| https://docs.n8n.io/hosting/installation/npm/ | 2:16 | ekran | hayır |
| http://localhost:5678 | 3:08 | ekran | hayır |
| https://docs.docker.com/get-docker/ | 3:34 | ekran | hayır |
| https://desktop.docker.com/win/main/amd64/Docker Desktop Installer.exe | 4:10 | ekran | evet |
| https://nodejs.org/en/ | 16:42 | ekran | evet |
| https://aistudio.google.com/app/apikey | 12:26 | ekran | evet |
| https://generativelanguage.googleapis.com | 12:20 | ekran | hayır |
| https://blog.tekhnelogos.com/docker-nedir-ve-ne-icin-kullanilir | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=1nzxcq61Ffw | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=wlyl_yv7nSk | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=uKoi9uQLdCs | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=gXhVFwzN4_4 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=bXBS2Hzr-vU | açıklama | açıklama | hayır |
| omerapp.app.n8n.cloud | 0:20 | ekran | hayır |
| https://app.docker.com | 6:32 | ekran | hayır |
| https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=[gizlendi] | 12:36 | ekran | evet |
## İş akışı
- 1. adım — n8n bulut hesabına girilip kalan deneme süresi gösterildi — araçlar: n8n, Google Chrome
- 2. adım — n8n dokümantasyonunda Self-host sayfası bulundu — araçlar: n8n, Google Chrome
- 3. adım — Docker kurulum sayfası ve gereksinimler incelendi — araçlar: Docker
- 4. adım — Docker Desktop for Windows indirilip kuruldu — araçlar: Docker Desktop
- 5. adım — Docker Desktop açılıp Google hesabıyla giriş yapıldı — araçlar: Docker Desktop
- 6. adım — Terminalde n8n_data volume'ü oluşturuldu — araçlar: Docker Desktop, Docker volume, Windows PowerShell
- 7. adım — docker run ile n8n konteyneri başlatıldı — araçlar: Docker, Windows PowerShell
- 8. adım — localhost:5678'de n8n sahibi hesabı ve lisans anahtarı formu dolduruldu — araçlar: n8n
- 9. adım — Manual trigger ve AI Agent düğümü eklendi — araçlar: n8n, AI Agent
- 10. adım — Google AI Studio'dan Gemini API anahtarı alınıp credential oluşturuldu — araçlar: Google AI Studio, Google Gemini Chat Model
- 11. adım — Gemini 2.0 Flash seçilip iş akışı test edildi — araçlar: Gemini 2.0 Flash, AI Agent
- 12. adım — Konteyner durdurma, silme ve yeniden oluşturma denendi; veriler korundu — araçlar: Docker Desktop, Docker volume
- 13. adım — Docker konteyner, image, volume silindi ve Docker Desktop kaldırıldı — araçlar: Docker Desktop
- 14. adım — Node.js kuruldu, npx n8n çalıştırıldı, Gemini credential tekrar test edildi — araçlar: Node.js, npx, Komut İstemi (cmd), Google Gemini Chat Model
- 15. adım — Görev Zamanlayıcı ile otomatik başlatma görevi oluşturuldu — araçlar: Windows Görev Zamanlayıcı
- 16. adım — Görev, .n8n klasörü ve Node.js kaldırıldı — araçlar: Windows Görev Zamanlayıcı, Node.js
## Promptlar
- Gemini credential ve AI Agent bağlantısını test etme — AI Agent düğümüne basit bir test mesajı ('test') gönderilerek Gemini bağlantısının çalıştığı doğrulanıyor.
ikinci göz KAPALI: --ikinci-goz yok
