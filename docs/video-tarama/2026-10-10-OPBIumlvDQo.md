# Viral Shorts Otomasyonu | Sıfır Kodla Otomatik Video Üretimi (FFmpeg + yt-dlp + n8n)
## Künye
Viral Shorts Otomasyonu | Sıfır Kodla Otomatik Video Üretimi (FFmpeg + yt-dlp + n8n) · Ömer Göçmen | Yapay Zeka & Otomasyon · süre: 20:28 · tr-orig · https://youtu.be/OPBIumlvDQo · şema 2
motor: parti 2026-10-10-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (54)
kareler: girdi ≤40000 jeton için 60→54
claude-sonnet-5-5: claude-sonnet-5-5 · 84607 tk · claude-haiku-5-5: claude-haiku-5-5 · 110329 tk
## Özet
Ömer Göçmen, n8n içinde yt-dlp ve FFmpeg kullanarak viral 'üstte popüler video, altta oyun/rahatlatıcı video' formatında Shorts'u otomatik üretip YouTube'a yükleyen bir akış kuruyor. Önce özel Dockerfile ile n8n imajına ffmpeg, curl, python3 ve yt-dlp ekleniyor (docker build/run). Akış Google Sheets'ten günün satırını alıyor, Crypto ile benzersiz ID üretiyor, iki videoyu indirip kırpıp alt alta birleştiriyor, yt-dlp ile Türkçe SRT indirip FFmpeg ile videoya yakıyor, SRT'yi Gemini'li AI Agent ile başlık/etikete çeviriyor ve YouTube node'u ile yüklüyor. Akış ve Docker dosyaları GitHub Gist'te ücretsiz paylaşılıyor.
## Bölümler
- 0:00 Giriş ve video planı
- 1:01 Viral Shorts formatı ve örnek çıktı
- 2:16 Sistemin mantığı: FFmpeg ve yt-dlp
- 3:50 Gist sayfası ve Dockerfile'ı indirme
- 5:03 Docker Desktop ile image build ve container çalıştırma
- 7:06 Workflow'un genel mantığı ve Google Sheets listesi
- 8:40 Google Sheets node'u, Limit ve Google kimlik bilgisi
- 11:13 Crypto ID ve yt-dlp ile video indirme
- 13:10 FFmpeg ile kırpma ve birleştirme
- 14:18 Altyazı indirme ve videoya gömme
- 15:19 SRT'yi metne çevirme ve AI Agent ile başlık/etiket
- 18:20 YouTube'a yükleme ve final
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n | yok | teknik | yok | Otomasyon platformu; tüm akış burada kuruluyor, Docker'da yerelde çalışıyor. | 0:00 | Nat platformunu çok özledim (n8n'in bozuk yazımı) |
| FFmpeg | yok | CLI | yok | Videoları kırpma, alt alta birleştirme ve altyazı gömme. | 2:02 | videoları oluşturmak için FFM PG kullanıyorum |
| yt-dlp | yok | CLI | https://github.com/yt-dlp/yt-dlp | YouTube videolarını MP4 ve Türkçe altyazı olarak indirme. | 2:02 | YouTube'un DLP'sini kullanıyorum |
| Docker Desktop | yok | teknik | yok | Image build ve n8n container'ını çalıştırma; terminal paneli kullanılıyor. | 4:03 | Docker Desktop'a geçiyoruz |
| Dockerfile | yok | teknik | yok | n8nio/n8n imajına ffmpeg, curl, python3 ve yt-dlp ekleyen özel imaj tarifi. | 3:50 | FROM n8nio/n8n:latest, apk add ffmpeg curl python3 (karede: kanıttan) FROM n8nio/n8n:latest, apk add ffmpeg curl python3 |
| GitHub Gist | yok | teknik | yok | Komutlar, Dockerfile ve workflow.json'un paylaşıldığı sayfa. | 3:50 | GitHub Gist sayfası: n8n with ffmpeg (karede: kanıttan) GitHub Gist sayfası: n8n with ffmpeg |
| Google Sheets | yok | teknik | yok | Ayın günlerine göre üst/alt video linklerini tutan tablo; akışın veri kaynağı. | 7:06 | Bir tane Google Sheets'im var |
| Google OAuth2 (Client ID/Secret) | yok | teknik | yok | Sheets ve YouTube node'larına bağlanmak için kimlik bilgisi oluşturma. | 9:08 | Google client ID ve secret almanız gerekiyor · kanıt: yok |
| Limit | yok | teknik | yok | n8n Limit node'u; Sheets'ten gelen iki satırdan yalnız ilkini bırakır. | 10:11 | bir tane limit tanımlıyoruz ve bir tane item getirip |
| Crypto | yok | teknik | yok | n8n Crypto node'u; dosya adları için benzersiz UUID üretir. | 11:13 | kripto diye bir tane nod var |
| Execute Command | yok | teknik | yok | yt-dlp ve ffmpeg komutlarını n8n içinde çalıştıran node. | 11:40 | Execute Command2 node'u, yt-dlp komutu (karede: kanıttan) Execute Command2 node'u, yt-dlp komutu |
| Read/Write Files from Disk | yok | teknik | yok | İndirilen/üretilen videoları ve SRT'yi diskten okur; kontrol ve yükleme için. | 12:14 | read file from disk nodu kullandım |
| Code | yok | teknik | yok | JavaScript node'u; SRT/VTT içeriğini temiz metne çevirir. | 15:40 | Code node: Buffer.from(binaryData, 'base64'), filter satırları (karede: kanıttan) Code node: Buffer.from(binaryData, 'base64'), filter satırları |
| AI Agent | yok | teknik | yok | Transkriptten başlık ve etiket üreten n8n yapay zekâ ajanı. | 16:19 | bu altyazıları yapay zekaya veriyorum |
| Google Gemini Chat Model | yok | teknik | yok | AI Agent'ın içinde çalışan ana model. | 15:56 | Google Gemini Chat alt node'u AI Agent'a bağlı · kanıt: kare (karede: Google Gemini Chat alt node'u AI Agent'a bağlı) |
| Structured Output Parser | yok | teknik | yok | Ajan çıktısını title ve tags JSON biçimine zorlar. | 16:19 | bir adet structured output parser kullanıyorum |
| YouTube | yok | teknik | yok | n8n YouTube node'u (upload video) ile final video kanala yükleniyor; kaynak videolar da buradan. | 18:20 | YouTube paylaşma kısmına geldik |
| SRT | yok | teknik | yok | yt-dlp'nin indirdiği altyazı dosya biçimi; FFmpeg subtitles filtresiyle gömülüyor. | 14:18 | bir tane SRT dosyası indiriyor |
| Gill Sans MT | yok | teknik | yok | Gömülü altyazıda kullanılan font ailesi. | 14:28 | force_style Fontname=Gill Sans MT,Fontsize=12 (karede: kanıttan) force_style Fontname=Gill Sans MT,Fontsize=12 |
| Medya Oynatıcı | yok | teknik | yok | Üretilen örnek videoyu oynatmak için kullanılan Windows uygulaması. | 1:42 | Medya Oynatıcı penceresinde dikey blur'lu video · kanıt: kare (karede: Medya Oynatıcı penceresinde dikey blur'lu video) |
| libx264 | yok | teknik | yok | H.264 video kodlayıcı; FFmpeg birleştirme komutunda -c:v libx264 -crf 18 -preset veryfast ile kullanılıyor. | 13:14 | -c:v libx264 -crf 18 -preset veryfast komutu (karede: FFmpeg komutunda '-c:v libx264 -crf 18 -preset veryfast' parametreleri okunuyor.) |
| Transkriptten YouTube başlığı ve etiketi üretmek | yok | prompt | yok | AI Agent'a SRT'den temizlenmiş transkript verilir; videoya uygun bir başlık (title) ve virgülle ayrılmış etiketler (tags) üretmesi, boş alanları videoya göre doldurması istenir. Çıktı structured output parser ile title/tags JSON'una zorlanır. | 16:14 | kaynak: kare |
## Açıklama bağlantıları
- https://gist.github.com/omergocmen/efb10f602dfe55e56ac641e63295dfd2 — Docker komutları, Dockerfile ve workflow.json içeren GitHub Gist · aday: evet (GitHub Gist) · Videoda gösterilip kullanılan GitHub Gist servisi; dosyalar buradan indiriliyor. · sınıf: diğer
- https://youtu.be/e1DzQAh4Xw0 — Kanal sahibinin başka videosu · aday: hayır · Diğer videolar listesi; içeriği doğrulanamadı, araç bağlantısı değil. · sınıf: diğer
- https://youtu.be/BjqaV253lNI — Kanal sahibinin başka videosu · aday: hayır · Diğer videolar listesi; araç bağlantısı değil. · sınıf: diğer
- https://youtu.be/gmYYHjlOJTI — Kanal sahibinin başka videosu · aday: hayır · Diğer videolar listesi; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=wlyl_yv7nSk&lc=Ugz7N1NOe3aQdwU6rwJ4AaABAg&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu (yorum parametreli) · aday: hayır · Diğer video referansı; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=uKoi9uQLdCs&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Diğer video referansı; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=gXhVFwzN4_4&t=2s&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Diğer video referansı; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=bXBS2Hzr-vU&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Diğer video referansı; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=7tInlFRcTEQ&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu (yorumda Docker/self-host için anılıyor) · aday: hayır · Diğer video referansı; araç bağlantısı değil. · sınıf: diğer
- https://www.linkedin.com/in/%C3%B6mer-g%C3%B6%C3%A7men-43a353227 — Yazarın LinkedIn profili · aday: hayır · Sosyal medya profili; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://www.tiktok.com/@omerrgcmn — Yazarın TikTok profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
- https://www.instagram.com/omerrgcmn — Yazarın Instagram profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
- https://youtu.be/7tInlFRcTEQ?si=9NRn9KgaFuoGc1M_ — Kanal sahibinin başka videosu (paylaşım parametreli, yorumda da geçiyor) · aday: hayır · Diğer video referansı; si parametresi izleme amaçlı paylaşım kodu, affiliate değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| cd n8n-custom | Docker terminalinde Dockerfile'ın bulunduğu klasöre geçer. (karede: Terminalde PS C:\Users\omer_> cd n8n yazısı, sonra n8n-custom klasör yolu) | 6:11 | kare |
| docker build -t n8n-custom:latest . | Dockerfile'dan n8n-custom:latest imajını oluşturur. (karede: Gist'teki satır: image build: docker build -t n8n-custom:latest; terminalde naming to docker.io/library/n8n-custom:latest) | 6:23 | kare |
| docker run -d --name n8n-custom -p 5678:5678 -v n8n_data:/home/node/.n8n -v [yol] -v /var/run/docker.sock:/var/run/docker.sock -e N8N_SECURE_COOKIE=false n8n-custom | n8n container'ını arka planda 5678 portunda başlatır; veri ve dosya klasörlerini bağlar. (karede: Terminalde docker run -d --name n8n-custom -p 5678:5678 -v n8n_data:... -e N8N_SECURE_COOKIE=false komutu; ardından 'container name already in use' hatası) | 6:24 | kare |
| RUN apk update && apk add --no-cache ffmpeg curl python3 | Dockerfile içinde imaja ffmpeg, curl ve python3 kurar. (karede: Gist'te dockerfile bölümünde apk add --no-cache ffmpeg curl python3 satırı) | 3:54 | kare |
| RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && chmod +x /usr/local/bin/yt-dlp | Dockerfile içinde yt-dlp ikilisini indirip çalıştırılabilir yapar (pip'siz). (karede: Dockerfile satırları: # yt-dlp binary kur, RUN curl -L .../yt-dlp, chmod +x /usr/local/bin/yt-dlp) | 4:13 | kare |
| yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o "{{ $json.data }}top.mp4" {{ $json.top }} | Üst videoyu en iyi video+ses ile MP4 olarak indirir (Execute Command2). (karede: Execute Command2 komut alanında yt-dlp -f bestvideo+bestaudio ... top.mp4) | 11:40 | kare |
| yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o "{{ $('Crypto').item.json.data }}bot.mp4" {{ $('Limit').item.json.bot }} | Alt (oyun) videosunu bot.mp4 olarak indirir (Execute Command3). (karede: Execute Command3 komutunda Crypto ve Limit ifadeleri, bot.mp4) | 12:14 | kare |
| ffmpeg -i {{ ID }}top.mp4 -i {{ ID }}bot.mp4 -filter_complex "[0:v]crop=iw:ih*0.5:0:ih*0.25[top]; ... [top][bot]vstack=inputs=2[out]" -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac -b:a 128k {{ ID }}vert.mp4 | İki videoyu kırpıp alt alta birleştirir, vert.mp4 üretir. (karede: Expression ekranında ffmpeg -i top.mp4 -i bot.mp4 -filter_complex crop..., vstack, -c:v libx264 -crf 18 -preset veryfast, vert.mp4) | 13:14 | kare |
| yt-dlp --write-auto-sub --convert-subs=srt --sub-lang tr --skip-download -o "{{ ID }}srt" {{ $('Limit').item.json.top }} | Üst videonun Türkçe otomatik altyazısını SRT olarak indirir, videoyu indirmez. (karede: Komut alanında yt-dlp --write-auto-sub --convert-subs=srt --sub-lang tr --skip-download -o) | 14:04 | kare |
| ffmpeg -i {{ ID }}vert.mp4 -vf "subtitles={{ ID }}srt.tr.srt:force_style='Fontname=Gill Sans MT,Fontsize=12,borderstyle=3,outline=3,OutlineColour=&H80000000,PrimaryColour=&H0000d7ff,Alignment=10'" -c:a copy {{ ID }}output.mp4 | SRT altyazıyı stil vererek videoya gömer, output.mp4 üretir. (karede: Expression penceresinde ffmpeg -i vert.mp4 -vf subtitles=...force_style Fontname=Gill Sans MT, Fontsize=12, borderstyle=3, Alignment=10, -c:a copy output.mp4) | 14:28 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Sistem tamamen ücretsiz araçlarla çalışıyor; workflow'lar ücretsiz paylaşılıyor. | 3:02 | özellik |
| Kurulum yaklaşık 2 dakikada yapılabilir. | 3:02 | sayısal |
| Sheets'te 31 link var; ayın gününe göre ilgili satır seçiliyor (today.day + 1). | 9:08 | sayısal |
| İki video %25 oranında kırpılıp alt alta birleştiriliyor. | 13:17 | sayısal |
| Yapay zekâ SRT dosyalarını doğrudan okuyamaz, metne çevirmek gerekir. | 15:19 | özellik |
| Üstte popüler, altta oyun videosu olan format çok izlenme ve beğeni alıyor. | 1:01 | özellik |
| Videoların lisansına dikkat edilmeli. | 18:20 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | n8n | n8n | Nat platformunu çok özledim |
| konuşma 0:00 | MCP'ler (önceki videolar) | aday değil: konu dışı | Uzun zamandır MCP'ler hakkında video çekiyordum |
| konuşma 1:01 | Bolt New short'u | aday değil: konu dışı | Bolt New için attığım videonun shortunu |
| konuşma 2:02 | FFmpeg | FFmpeg | videoları oluşturmak için FFM PG kullanıyorum |
| konuşma 2:02 | yt-dlp | yt-dlp | YouTube'un DLP'sini kullanıyorum |
| konuşma 3:50 | GitHub Gist | GitHub Gist | kitap sayfası hazırladım (Gist) |
| kare 3:50 | Dockerfile | Dockerfile | FROM n8nio/n8n:latest |
| kare 3:54 | python3 / curl / apk | aday değil: başka adayın parçası (Dockerfile) | apk add --no-cache ffmpeg curl python3 |
| kare 3:56 | workflow.json | aday değil: başka adayın parçası (GitHub Gist) | gist raw workflow.json |
| konuşma 4:03 | Docker Desktop | Docker Desktop | Docker Desktop'a geçiyoruz |
| kare 4:42 | n8nio/n8n imajı | aday değil: başka adayın parçası (Dockerfile) | docker.n8n.io/n8nio/n8n |
| kare 5:06 | .cursor, .windsurf, .lmstudio klasörleri | aday değil: konu dışı | Dosya listesinde klasör adları |
| kare 5:55 | PowerRename, WinMerge, Copilot'a Sor | aday değil: konu dışı | Sağ tık menüsü girdileri |
| kare 5:30 | Dosya Gezgini | aday değil: genel kavram | n8n-custom klasörü açık |
| kare 6:11 | PowerShell terminali | aday değil: başka adayın parçası (Docker Desktop) | PS C:\Users\omer_> cd n8n |
| kare 6:26 | docker scout quickview | aday değil: konu dışı | View a summary of image vulnerabilities |
| kare 6:52 | OBS 31.0.3 | aday değil: konu dışı | OBS 31.0.3 - Profil: isimsiz |
| kare 6:52 | Google Chrome | aday değil: genel kavram | n8n with ffmpeg - Google Chrome |
| konuşma 7:06 | Google Sheets | Google Sheets | Bir tane Google Sheets'im var |
| konuşma 9:08 | Google OAuth2 Client ID/Secret | Google OAuth2 (Client ID/Secret) | Google client ID ve secret almanız gerekiyor |
| konuşma 10:11 | Limit node'u | Limit | bir tane limit tanımlıyoruz |
| konuşma 11:13 | Crypto node'u | Crypto | kripto diye bir tane nod var |
| konuşma 11:13 | UUID | aday değil: başka adayın parçası (Crypto) | benzersiz bir tane ID oluşturuyor |
| kare 11:40 | Execute Command node'u | Execute Command | Execute Command2 yt-dlp komutu |
| konuşma 12:14 | Read/Write Files from Disk | Read/Write Files from Disk | read file from disk nodu kullandım |
| kare 13:10 | crop / vstack / libx264 / aac | aday değil: başka adayın parçası (FFmpeg) | -c:v libx264 -crf 18 -preset veryfast |
| kare 14:28 | Gill Sans MT | Gill Sans MT | Fontname=Gill Sans MT,Fontsize=12 |
| konuşma 14:18 | SRT | SRT | bir tane SRT dosyası indiriyor |
| kare 15:40 | Code node (JavaScript) | Code | Buffer.from(binaryData, 'base64') |
| konuşma 16:19 | AI Agent | AI Agent | bu altyazıları yapay zekaya veriyorum |
| kare 15:56 | Google Gemini Chat Model | Google Gemini Chat Model | Google Gemini Chat alt node'u |
| konuşma 16:19 | Structured Output Parser | Structured Output Parser | bir adet structured output parser kullanıyorum |
| konuşma 17:19 | TikTok / Instagram paylaşımı | aday değil: konu dışı | YouTube, TikTok, Instagram ya da diğer platformlar |
| konuşma 18:20 | YouTube node'u (upload video) | YouTube | resource kısmını video, operation upload |
| kare 1:42 | Medya Oynatıcı | Medya Oynatıcı | Medya Oynatıcı penceresinde video |
| kare 4:24 | Google Translate açılır penceresi | aday değil: konu dışı | İngilizce/Türkçe çeviri kutusu Gist sayfasında |
| açıklama | Hashtag'ler (#ai, #automation, #n8n, #ffmpeg vb.) | aday değil: genel kavram | #ai #automation #n8n #nocode #ffmpeg |
| açıklama | LinkedIn, TikTok, Instagram profilleri | aday değil: konu dışı | Sosyal medya bağlantıları |
| açıklama | Diğer YouTube videoları (8 bağlantı) | aday değil: konu dışı | İzleyebileceğiniz diğer videolar |
| açıklama | GitHub Gist bağlantısı | GitHub Gist | gist.github.com/omergocmen/efb10f60... |
| linkli sayfa | docs.docker.com sandboxes kit-examples | aday değil: konu dışı | Bağlantılı sayfa listesinde docs.docker.com |
| linkli sayfa | GitHub giriş/kayıt/profil sayfaları | aday değil: konu dışı | gist.github.com/login, join, github.com/Om |
| yorum | Telegram, OpenAI, Gemini API anahtarları | aday değil: konu dışı | openai, gemini, telegram botu hep hata alıyorum |
| yorum | Railway, AWS, npx ile n8n | aday değil: konu dışı | railway sunucusuna kurmam lazımmış; npx komutuyla çalıştırıyorum |
| yorum | Google Lens düğmesi | aday değil: konu dışı | Google lens butonu çıkıyor |
## Kareden okunanlar
- 0:00: n8n tuvali: youtube-shorts-generator akışı; Google Sheets, Limit, Crypto, Execute Command, Read/Write Files, Code, AI Agent (Gemini + Structured Output), YouTube node'ları; çıktı: title 'Kızın Profilini Çözme Rehberi: Emoji Dedektifliği'.
- 0:58: YouTube Shorts: üstte konuşan adam, altta Minecraft parkuru; altyazı 'Hacı ben bu kıza yazacağım da şimdi garip garip birçok emoji numara var'.
- 1:42: Medya Oynatıcı'da dikey, blur'lu kenarlı Bolt New short'u; altyazı 'seçiyorsunuz... api keyinizi girip kullanabiliyorsunuz'.
- 3:50: GitHub Gist 'n8n with ffmpeg': commands, dockerfile (FROM n8nio/n8n:latest, USER root, apk add ffmpeg curl python3, yt-dlp curl) ve workflow.json bölümleri.
- 4:22: gist.githubusercontent.com raw workflow.json: name youtube-shorts-generator, executeCommand node'u yt-dlp komutuyla.
- 4:32: Raw dockerfile sayfası ve Farklı Kaydet iletişim kutusu; dosya adı dockerfile.txt.
- 4:42: Docker Desktop Images: docker.n8n.io/n8nio/n8n 1.86.1 (1.23 GB) ve n8n-custom latest (1.6 GB); altta Terminal.
- 5:30: Dosya Gezgini: n8n-custom klasöründe dockerfile ve dockerfile.txt; sağ tık menüsü ile Yeniden adlandır.
- 6:16: Docker terminalinde build çıktısı: CACHED RUN curl ... yt-dlp, naming to docker.io/library/n8n-custom:latest.
- 6:36: Containers: n8n-custom çalışıyor, port 5678:5678, CPU %802.
- 7:28: youtube-short-links Google Sheet'i: 'top' ve 'bot' sütunlarında 31 satır YouTube linki.
- 9:10: Google Sheets OAuth2 kimlik bilgisi penceresi: OAuth Redirect URL, Client ID/Secret alanları (değerler okunmadı).
- 11:40: Execute Command2: yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o ...top.mp4 komutu.
- 13:14: ffmpeg birleştirme ifadesi: filter_complex ile crop, vstack, libx264 -crf 18 -preset veryfast, vert.mp4.
- 14:28: Altyazı komutu: subtitles=...srt.tr.srt:force_style Fontname=Gill Sans MT, Fontsize=12, borderstyle=3, Alignment=10, output.mp4.
- 15:40: Code node: Buffer.from(binaryData,'base64').toString('utf-8'), boş satır ve WEBVTT filtresi.
## Belirsizlikler
- Kare listesi 60 zaman damgası gösteriyor ama 54 görsel var; kare zamanları görsellerle yaklaşık eşleştirildi.
- Altyazı otomatik: 'Nat/Nathon' n8n, 'FFM PG' FFmpeg, 'DLP' yt-dlp, 'Aykut Elmas' (muhtemelen 'aynı kırpma/video') gibi bozuk yazımlar var.
- Konuşma 'Bolt New' short'undan söz ediyor ama o short'u üreten yapay zekâ aracının adı verilmiyor; aday yazılmadı.
- Dosya Gezgini sağ tık menüsünde Notepad++, PowerRename, WinMerge, Copilot görünüyor; kullanılmadığı için aday yapılmadı.
- Dosya Gezgini'nde .cursor, .windsurf, .lmstudio klasörleri görünüyor; videoda kullanılmıyor.
- OBS 31.0.3 ve Logi Capture görev değiştirici listesinde göründü; muhtemelen kayıt aracı, videonun konusu değil.
- Sözlük eşleşmeleri (Claude, Cursor, Figma, Ollama, Veo, Canva vb.) çoğunlukla OCR gürültüsü; doğrulanmadı.
- Sheets'teki çok sayıda short URL'si OCR'de tekrarlı ve bozuk; yalnız ayrı olanlardan örnek liste verildi.
- Execute Command ve ffmpeg komutlarında {{ ID }} yer tutucusu Crypto'nun ürettiği UUID'dir; tam ifade ekranda kısmen okunuyor.
- Yorumdaki --rm ipucu videoda gösterilmedi.
## Atlanan segment oranı
0/21 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| gist.github.com/omergocmen/efb10f602dfe55e56ac641e63295dfd2 | 3:50 | ekran | evet |
| https://gist.github.com/omergocmen/efb10f602dfe55e56ac641e63295dfd2 | açıklama | açıklama | evet |
| https://youtu.be/e1DzQAh4Xw0 | açıklama | açıklama | hayır |
| https://youtu.be/BjqaV253lNI | açıklama | açıklama | hayır |
| https://youtu.be/gmYYHjlOJTI | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=wlyl_yv7nSk&lc=Ugz7N1NOe3aQdwU6rwJ4AaABAg&ab_channel=%C3%96merG%C3%B6%C3%A7men | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=uKoi9uQLdCs&ab_channel=%C3%96merG%C3%B6%C3%A7men | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=gXhVFwzN4_4&t=2s&ab_channel=%C3%96merG%C3%B6%C3%A7men | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=bXBS2Hzr-vU&ab_channel=%C3%96merG%C3%B6%C3%A7men | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=7tInlFRcTEQ&ab_channel=%C3%96merG%C3%B6%C3%A7men | açıklama | açıklama | hayır |
| https://youtu.be/7tInlFRcTEQ?si=9NRn9KgaFuoGc1M_ | açıklama | yorum | hayır |
| https://www.linkedin.com/in/%C3%B6mer-g%C3%B6%C3%A7men-43a353227 | açıklama | açıklama | hayır |
| https://www.tiktok.com/@omerrgcmn | açıklama | açıklama | hayır |
| https://www.instagram.com/omerrgcmn | açıklama | açıklama | hayır |
| youtube.com/shorts/eQKZsCL_4DQ | 0:58 | ekran | hayır |
| https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp | 3:50 | ekran | evet |
| gist.githubusercontent.com/omergocmen/efb10f602dfe55e56ac641e63295dfd2/raw/26dedcbad3429c4f534949c20eae36e1665c0bd9/workflow.json | 4:22 | ekran | hayır |
| gist.githubusercontent.com/omergocmen/efb10f602dfe55e56ac641e63295dfd2/raw/26dedcbad3429c4f534949c20eae36e1665c0bd9/dockerfile | 4:30 | ekran | hayır |
| docker.n8n.io/n8nio/n8n | 4:42 | ekran | evet |
| docker.io/library/n8n-custom:latest | 6:16 | ekran | hayır |
| https://docs.docker.com/ai/sandboxes/customize/kit-examples | açıklama | açıklama | hayır |
| http://localhost:5678 | 6:38 | ekran | hayır |
| http://localhost:5678/rest/oauth2-credential/callback | 9:10 | ekran | hayır |
| docs.google.com/spreadsheets/d/1MjtmEVHBa6vuxakm3fJBVNjFC-fBWqmC3J_tBqfqc7A/edit?gid=0#gid=0 | 7:28 | ekran | evet |
| https://www.youtube.com/watch?v=RQ3tfdCMjN4&list=PLdxE72LIkFodEb4jBP8ewH1-qfUcneR7Z&index=4 | 7:28 | ekran | hayır |
| https://www.youtube.com/watch?v=ftc2fWSh3uc | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/9ciMSvQkQDg | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/LofyMQts7hY | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/C1c5owEUOHQ | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/WpCt5Xs18_o | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/wBGh_IcXt90 | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/WbDASw5leHk | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/NLMZpxtl_3U | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/Mg5ax4IKKA8 | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/2bFszFztkWY | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/DGY1ps4366Y | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/HFjWL-Gqlk8 | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/5urFgJ0V1J0 | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/SKh_zOnpYGg | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/pgVfeLCPDQM | 7:28 | ekran | hayır |
| https://gist.githubusercontent.com/omergocmen/efb10f602dfe55e56ac641e63295dfd2/raw/26dedcbad3429c4f534949c20eae36e1665c0bd9/commands | 4:22 | ekran | evet |
| https://www.youtube.com/shorts | 12:00 | ekran | hayır |
| https://www.youtube.com/shorts/2YPak3uh7Ws | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/4AAhElgk5FY | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/BGXx5sqEbvU | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/K_F11iSMzHQ | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/NF6v0louK5g | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/Nag_TKPDw_E | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/O7NbLaNqVu8 | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/OOHICRhAYfc | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/moHFdzJa_0c | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/rsXCL9ykDFg | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/yJuPErtkh3o | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/zcoUIECwS_s | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/zxK-VYr8NrY | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/21wCTCf7z-4 | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/ChXQbu7B3rM | 7:28 | ekran | hayır |
| https://www.youtube.com/shorts/iavZeas5N4s | 7:44 | ekran | hayır |
| https://www.youtube.com/shorts/h6rXtXsSyDA | 7:44 | ekran | hayır |
| https://www.youtube.com/shorts/4YMGBMXLpxY | 7:48 | ekran | hayır |
## İş akışı
- 1. adım — Gist sayfasından Dockerfile'ı ham halde indirip dockerfile.txt'yi uzantısız Dockerfile olarak yeniden adlandırma — araçlar: GitHub Gist, Dosya Gezgini
- 2. adım — Docker terminalinde n8n-custom klasörüne geçip özel imajı build etme — araçlar: Docker Desktop, Dockerfile
- 3. adım — n8n container'ını docker run ile 5678 portunda başlatıp localhost'tan açma — araçlar: Docker Desktop, n8n
- 4. adım — Workflow'u Gist'ten içe aktarma — araçlar: n8n, GitHub Gist
- 5. adım — Google Sheets'ten ayın gününe göre satırları çekme (today.day + 1) ve Google OAuth kimlik bilgisini bağlama — araçlar: Google Sheets, Google OAuth2 (Client ID/Secret), n8n
- 6. adım — Limit ile yalnız ilk satırı bırakma — araçlar: Limit
- 7. adım — Crypto ile benzersiz ID (UUID) üretme — araçlar: Crypto
- 8. adım — Üst videoyu indirme — araçlar: Execute Command, yt-dlp
- 9. adım — Alt (oyun) videosunu indirme — araçlar: Execute Command, yt-dlp
- 10. adım — İndirilen videoyu diskten okuyup kontrol etme — araçlar: Read/Write Files from Disk
- 11. adım — İki videoyu kırpıp alt alta birleştirme (vert.mp4) ve sonucu kontrol etme — araçlar: Execute Command, FFmpeg, Read/Write Files from Disk
- 12. adım — Üst videonun Türkçe SRT altyazısını indirme — araçlar: Execute Command, yt-dlp, SRT
- 13. adım — Altyazıyı stil vererek videoya gömme (output.mp4) — araçlar: Execute Command, FFmpeg, Gill Sans MT
- 14. adım — SRT'yi okuyup Code ile temiz metne çevirme — araçlar: Read/Write Files from Disk, Code
- 15. adım — Gemini'li AI Agent ile başlık ve etiket üretme — araçlar: AI Agent, Google Gemini Chat Model, Structured Output Parser
- 16. adım — Final videoyu okuyup YouTube'a yükleme (title, tags, açıklama, Türkçe dil) — araçlar: Read/Write Files from Disk, YouTube, Google OAuth2 (Client ID/Secret)
## Promptlar
- Transkriptten YouTube başlığı ve etiketi üretmek — AI Agent'a SRT'den temizlenmiş transkript verilir; videoya uygun bir başlık (title) ve virgülle ayrılmış etiketler (tags) üretmesi, boş alanları videoya göre doldurması istenir. Çıktı structured output parser ile title/tags JSON'una zorlanır.
ikinci göz KAPALI: --ikinci-goz yok
