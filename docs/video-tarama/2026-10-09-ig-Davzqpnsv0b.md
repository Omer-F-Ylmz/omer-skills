# 👇 Reponun linkini hemen almak için yorumlara "TMUX" yazın!
## Künye
👇 Reponun linkini hemen almak için yorumlara "TMUX" yazın! · arifata.kosker · süre: 0:40 · ? · https://www.instagram.com/reel/Davzqpnsv0b/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-26 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 32099 tk · claude-haiku-5-5: claude-haiku-5-5 · 32659 tk
## Özet
Kısa videoda yapay zekâ kodlama ajanlarının (Grok Build, Open Code, Claude Code) dizüstü bilgisayarda doğrudan çalıştırılmak yerine tmux oturumu içinde çalıştırılması öneriliyor. Terminal dört bölmeye ayrılıyor: kod yazan Grok, hata ayıklayan Open Code, testler ve sunucu günlükleri. Bilgisayar kapansa ya da internet kesilse bile süreçlerin ve bağlamın kaybolmadığı anlatılıyor. Video tmux GitHub reposunu gösteriyor ve yorumlara 'TMUX' yazılmasını istiyor.
## Bölümler
- 0:00 Giriş: ajanları dizüstünde çalıştırmayı bırakın
- 0:09 Çözüm: tmux'ı kurmak ve çalıştırmak
- 0:21 Ekranı dört bölmeye bölme
- 0:30 Bilgisayarı kapat, bir saat sonra devam et
- 0:37 tmux GitHub reposu ve yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| tmux | yok | CLI | https://github.com/tmux/tmux | Terminal çoklayıcı; oturumlar bağlantı kopsa da arka planda çalışmaya devam eder, ekran bölmelere ayrılır. | 0:09 | Altyazı 'tek yapmanız gereken terminal açmak ve tmux'ı kurmak' yazıyor. (karede: kanıttan) Altyazı 'tek yapmanız gereken terminal açmak ve tmux'ı kurmak' yazıyor. |
| Grok Build | yok | CLI | yok | Birinci bölmede kod yazan yapay zekâ kodlama ajanı. | 0:03 | Konuşmada 'Grogg Build', ekranda 'grok build' geçiyor. |
| opencode | yok | CLI | yok | İkinci bölmede hata ayıklayan yapay zekâ kodlama ajanı. | 0:04 | Ekranda 'opencode' yazıyor, konuşmada 'Open Code' deniyor. |
| Claude Code | yok | CLI | yok | Dizüstünde doğrudan çalıştırılmaması önerilen ajanlardan biri. | 0:00 | Konuşmada 'Cloud Code' geçiyor; 0:07 karesinde Claude arayüzü var. |
| npm | yok | CLI | yok | Node paket yöneticisi; tmux penceresinde web projesini 'npm run start' ile başlatmak için kullanılıyor. | 0:15 | npm run start (karede: kanıttan) npm run start |
| psql | yok | CLI | yok | PostgreSQL istemcisi; tmux bölmesinde sürüm çıktısı ve veritabanı istemi görünüyor. | 0:21 | psql (15.8 (Debian 15.8-0+deb12u1)) (karede: kanıttan) psql (15.8 (Debian 15.8-0+deb12u1)) |
| Poster konseptleri üretme (Claude arayüzü örneği) | yok | prompt | yok | Sanatsal bir yengeç siluetini çizmesi ve tek betikte üç farklı poster konsepti üretmesi isteniyor. | 0:05 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| tmux new-session -d -s dev_env -n horsetinder | dev_env adlı oturumu arka planda başlatır, ilk pencereye horsetinder adını verir. (karede: OCR metni 0:15: 'tmux new-session -d -s dev_env -n horsetinder'; bu an için görsel gönderilmedi.) | 0:15 | kare |
| new-window -n web_server | web_server adlı yeni tmux penceresi açar. (karede: OCR metni 0:15: 'new-window -n web_server'; bu an için görsel gönderilmedi.) | 0:15 | kare |
| send-keys "cd /path/to/web/project && npm run start" C-m | Pencereye proje dizinine girip npm run start çalıştıran tuşları gönderir. (karede: OCR metni 0:15: 'send-keys "cd /path/to/web/project && npm run start" C-m'; bu an için görsel gönderilmedi.) | 0:15 | kare |
| tmux | tmux oturumunu başlatır (videoda 'tmux'ı çalıştırmak' olarak anlatılıyor, komut ekranda yazılmıyor). | 0:13 | altyazı |
| tmux new-window -n web_server | 'web_server' adlı yeni bir tmux penceresi açar. | 0:15 | kare |
| ./server.Js | Sunucu betiğini çalıştırır (dosya adı OCR'da 'server.Js' okunuyor). | 0:21 | kare |
| psql | PostgreSQL istemcisini açar; ekranda sürüm çıktısı ve 'template1=>' istemi görünüyor, çalıştırma komutu tam görünmüyor. | 0:21 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bilgisayar kapatılıp wifi kesilse ve bir saat sonra dönülse bile ajanlar çalışmaya devam eder, süreçler çökmez, bağlam kaybolmaz. | 0:30 | özellik |
| Her yapay zekâ kullanıcısının öğrenmesi gereken tek araç tmux'tır. | 0:00 | öneri |
| Terminal dört bölmeye ayrılabilir: kod yazan ajan, hata ayıklayan ajan, testler, sunucu günlükleri. | 0:21 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | yapay zekâ ajanları (genel) | aday değil: genel kavram | 'her yapay zekâ kullanıcısı' ifadesi genel. |
| konuşma 0:03 | Grok Build | Grok Build | Ekranda 'grok build', konuşmada 'Grogg Build'. |
| konuşma 0:04 | Open Code | opencode | Ekranda 'opencode' yazıyor. |
| konuşma 0:00 | Cloud Code / Claude Code | Claude Code | Konuşmada anılıyor; 0:07 karesinde Claude arayüzü var. |
| kare 0:07 | Claude sohbet arayüzü | Claude Code | 'Reply to Claude...' alanı görünüyor. |
| kare 0:05 | reportlab (Python PDF kütüphanesi) | aday değil: konu dışı | Ekrandaki poster kodunda import satırları var; anlatılmıyor. |
| konuşma 0:09 | tmux | tmux | Ana konu; 0:37 karesinde GitHub deposu. |
| kare 0:15 | npm run start | aday değil: başka adayın parçası (tmux) | tmux send-keys örneğinin içindeki komut. |
| kare 0:37 | GitHub tmux/tmux sayfası | tmux | Repo sayfası ekranda. |
| konuşma 0:21 | test ve sunucu günlükleri bölmeleri | aday değil: başka adayın parçası (tmux) | tmux bölme düzeninin parçası. |
| açıklama | Instagram reel sayfası | aday değil: konu dışı | Videonun kendi künye bağlantısı. |
| yorum | yorumlar | aday değil: konu dışı | Girişsiz alınamadı. |
## Kareden okunanlar
- 0:07: Claude sohbet arayüzü: 'Perfect! I've generated 3 completely different poster concepts', Concept 1: Underwater Realm, Concept 2: Nautilus Portal, 'Reply to Claude...'; altyazı 'çalıştırmayı bırakın'.
- 0:10: Koyu terminal paneli (TERMINAL, PORTS sekmeleri) içinde ofis iş (chore) yönetim uygulaması soruları; altyazı 'tek yapmanız gereken terminal açmak ve tmux'ı kurmak'.
- 0:37: GitHub tmux/tmux deposu: Public, master, 12 Branches, 43 Tags, Issues 21, Pull requests 4, Agents, Discussions; son commit 'nicm Regress for more hooks.'; altyazı 'ancak tmux ile iş çalışmaya devam ediyor'.
## Belirsizlikler
- Konuşmada 'TMAX' geçiyor; ekran ve açıklama tmux olduğunu gösteriyor, altyazı hatası sayıldı.
- Yorumlar girişsiz alınamadı; repo linki doğrulanamadı.
- GitHub deposunun URL'si adres çubuğundan okunmadı; repo_url sayfa başlığından (tmux/tmux) türetildi.
- Grok Build ve opencode ekranda çalışırken gösterilmedi; yalnız adları anıldı.
- 0:10 karesindeki ofis iş uygulaması sorusunu hangi aracın sorduğu belli değil.
- Açıklamadaki Grok, ngrok ve Inter sözlük eşleşmeleri; videoda ngrok veya Inter kullanılmıyor.
- Konuşmada 'Cloud Code' geçiyor; Claude Code olarak yorumlandı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/Davzqpnsv0b/ | açıklama | açıklama | hayır |
| https://github.com/tmux/tmux | 0:37 | ekran | evet |
## İş akışı
- 1. adım — Terminali açıp tmux'ı kurma — araçlar: Terminal, tmux
- 2. adım — tmux'ı çalıştırıp tmux oturumuna girme — araçlar: tmux
- 3. adım — dev_env adında yeni oturum oluşturma ve ilk pencereyi horsetinder olarak adlandırma — araçlar: tmux
- 4. adım — web_server adında yeni pencere açma — araçlar: tmux
- 5. adım — Web sunucu penceresine 'npm run start' komutunu gönderip çalıştırma — araçlar: tmux, npm
- 6. adım — Sunucu betiğini çalıştırma — araçlar: tmux, server.js betiği
- 7. adım — Veritabanı istemcisini açma — araçlar: tmux, psql
- 8. adım — Pencere listesi ve durum çubuğunu kontrol etme — araçlar: tmux
- 9. adım — Terminali 4 bölmeye ayırma (kod, hata ayıklama, testler, sunucu günlükleri) — araçlar: tmux (bölme)
- 10. adım — Bölmelerde ajanları çalıştırma: Grok Build kod yazar, Open Code hata ayıklar — araçlar: Grok Build, Open Code
- 11. adım — Sistem izleme ekranıyla süreç ve yük durumunu kontrol etme — araçlar: Sistem izleme aracı (adı görünmüyor)
- 12. adım — Bilgisayarı kapatıp bağlantıyı kesme, bir saat sonra dönüp oturumu sürdürme — araçlar: tmux
- 13. adım — tmux GitHub deposunu gösterme — araçlar: GitHub, tmux
- 14. adım — Yorumlara TMUX yazılarak repo linki isteme — araçlar: Instagram yorumları
## Promptlar
- Poster konseptleri üretme (Claude arayüzü örneği) — Sanatsal bir yengeç siluetini çizmesi ve tek betikte üç farklı poster konsepti üretmesi isteniyor.
ikinci göz KAPALI: --ikinci-goz yok
