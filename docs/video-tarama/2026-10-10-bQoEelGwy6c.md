# Yapay Zeka ile İş Bul (0 Kodlama)
## Künye
Yapay Zeka ile İş Bul (0 Kodlama) · Esad Kılıç · süre: 20:10 · tr-orig · https://youtu.be/bQoEelGwy6c · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (55)
kareler: girdi ≤40000 jeton için 60→55
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 102278 tk
## Özet
Esad Kılıç, Claude Code ile kod yazmadan iş bulan bir uygulama kuruyor. Viral Danimarka odaklı AI Job Search reposunu Türkiye pazarına uyarlıyor (İş Bulucu), Zeynep Kaya adlı hayali bir adayın CV'sini ATS uyumlu hale getiriyor, LinkedIn ve Freehire'dan ilan çekip 0-100 uygunluk puanlıyor, en uygun ilanlara özel CV ve ön yazı üretiyor. Yerel Python panel arayüzü yazdırıyor, Vercel'e deploy ediyor ve TestSprite CLI ile 6 uçtan uca test çalıştırıp bir hatayı tespit ediyor. Videoda kullanılan adres ve testler gösterim amaçlı.
## Bölümler
- 0:00 Giriş: kötü CV'ler ve ATS sorunu
- 1:00 AI Job Search reposu ve Türkiye uyarlaması
- 2:01 Repo akışı: setup, scrape, apply
- 5:02 Claude Code ile kurulum
- 6:03 Setup: CV yükleme ve profil soruları
- 8:04 Yerel web arayüzü (panel)
- 9:05 Scrape ve ilan listesi
- 11:07 Rank ve apply
- 13:02 Arayüzü ürün seviyesine çıkarma
- 15:09 TestSprite ile test
- 17:09 Vercel'e alma ve test planı
- 19:10 Hataları düzeltip yeniden test
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| AI Job Search | yok | iş akışı | https://github.com/MadsLorentzen/ai-job-search | Claude Code tabanlı iş arama çerçevesi; setup, scrape, apply, interview komutlarını içerir. Video bunu Türkiye'ye uyarladı. | 1:00 | AI Job Search isimli bir repo var |
| İş Bulucu | yok | iş akışı | https://github.com/goatstarter/isbulucu.git | AI Job Search'ün Türkçe ve Türkiye pazarı uyarlaması; panel arayüzü ve ilan takip sistemi dahil. | 5:02 | Türkçe alternatifini oluşturduk |
| Claude Code | yok | CLI | yok | Terminalde çalışan Anthropic kodlama ajanı; kurulum, kod ve panel işlerini yürütür. | 5:40 | Claude Code v2.1.266 sürüm yazısı görünüyor (karede: Terminal başlığında 'Claude Code v2.1.266' yazısı) |
| Fable 5.1 | yok | teknik | yok | Claude Code oturumunda kullanılan model (high effort). | 5:40 | Fable 5.1 with high effort · Claude Team (karede: 'Fable 5.1 with high effort · Claude Team' satırı) |
| TestSprite | yok | teknik | yok | Yapay zekâ destekli uçtan uca test platformu; canlı uygulamayı gerçek kullanıcı gibi test eder. | 15:09 | test sprite ile testler gerçekleştir |
| TestSprite CLI | yok | CLI | https://github.com/TestSprite/testsprite-cli | TestSprite'ın komut satırı aracı; testleri terminalden oluşturur ve çalıştırır. | 15:34 | npm install -g @testsprite/testsprite-cli komutu (karede: Terminalde 'npm install -g @testsprite/testsprite-cli' komutu) |
| Vercel | yok | CLI | yok | Uygulamayı canlıya almak için kullanılan barındırma servisi ve deploy CLI'ı. | 17:10 | vercel deploy --prod --scope goatstarter komutu (karede: 'command: vercel deploy --prod --scope goatstarter' satırı) |
| Cloudflare | yok | teknik | yok | Lokal uygulamayı geçici tünelle dışarı açmak için denenen servis (quick tunnel); TestSprite erişemediği için vazgeçildi. | 16:09 | cloud flare muhabbeti de lokaldeki bu uygulamayı canlıya |
| ngrok | yok | teknik | yok | Tünelleme aracı; ücretsiz sürümün uyarı sayfası testleri bozduğu için kullanılmadı. | 16:44 | ücretsiz sürüm uyarı sayfası gösterip otomatik testi bozuyor (karede: Ajan mesajında 'Ngrok mevcut ama ücretsiz sürüm uyarı sayfası' metni) |
| Freehire | yok | teknik | yok | AI Job Search'ün tarama kaynaklarından biri; panelde portal olarak görünüyor. | 3:24 | freehire.me yazısı ekranda görünüyor (karede: Ekranda 'freehire.me' yazısı) |
| LinkedIn | yok | teknik | yok | İlan kaynağı; LinkedIn arama CLI'ı ile ilan çekilir. | 2:01 | LinkedIn vesaire de dahil |
| Kariyer.net | yok | teknik | yok | Türkiye iş ilanı sitesi; uyarlamada veri kaynağı olarak anıldı, eklenmesi önerildi. | 2:01 | Kariyer Netnet gibi sitelerden de veri çekecek |
| Bun | yok | teknik | yok | İş arama CLI araçları için JavaScript çalışma ortamı; kurulum gereksinimi. | 3:22 | Bun (for job search CLI tools) gereksinimi (karede: Gereksinimler listesinde 'Bun (for job search CLI tools)') |
| Python | yok | teknik | yok | Panel (tools/panel.py) ve CV/PDF araçlarının çalıştığı dil; Python 3.10+. | 8:24 | yalnızca Python standart kütüphanesi, ekstra kurulum yok (karede: Terminal raporunda 'yalnızca Python standart kütüphanesi' yazısı) |
| Playwright | yok | teknik | yok | ATS uyumlu PDF üretimi için kurulan tarayıcı otomasyon kütüphanesi (chromium). | 6:08 | pip install playwright && playwright install chromium (karede: Plan metninde 'pip install playwright && playwright install chromium') |
| GitHub | yok | teknik | https://github.com | Repo'nun klonlandığı ve İş Bulucu deposunun barındırıldığı platform. | 5:54 | https://github.com/goatstarter/isbulucu.git (karede: Terminalde İş Bulucu depo adresi) |
| Visual Studio Code | yok | teknik | yok | Claude Code'un terminalden çalıştırıldığı editör. | 5:34 | Visual Studio Code (karede: Uygulama menüsünde 'Visual Studio Code') |
| frontend-design | yok | skill | yok | Anthropic'in ön yüz tasarım yeteneği; panel arayüzünün kalitesini artırmak için kullanıldı. | 12:48 | Skill(frontend-design:frontend-design) (karede: Terminalde 'Skill(frontend-design:frontend-design)' satırı) |
| Repoyu kurup sonraki adımları planlatmak | yok | prompt | yok | Repo raporunu yapıştırıp kurulumu yapmasını ve sonraki adımları planlamasını istemek (Türkçe özet). | 6:03 | kaynak: altyazı |
| Setup'ı kullanıcı gibi çalıştırmak | yok | prompt | yok | Geliştirici modundan çıkıp setup akışını sade kullanıcı gibi başlatmasını istemek; tek CV yüklemek. | 6:03 | kaynak: altyazı |
| Yerel panel arayüzü yaptırmak | yok | prompt | yok | Scrape ve apply sonuçlarını takip etmek için yerel web arayüzü yapmasını, tasarımı ürün seviyesine çıkarmasını istemek. | 8:04 | kaynak: altyazı |
| TestSprite ile test yaptırmak | yok | prompt | yok | Uygulamayı TestSprite ile gerçek kullanıcı gibi test edip sonuçları raporlamasını istemek. | 15:09 | kaynak: altyazı |
| Canlıya alıp test etmek | yok | prompt | yok | Lokal uygulamayı Vercel'e alıp TestSprite testlerini çalıştırmasını; karar konusunda serbest bırakmak. | 16:09 | kaynak: altyazı |
| Başarısız testleri düzeltmek | yok | prompt | yok | Başarısız testlerdeki sorunları çözüp testleri yeniden göndermesini istemek. | 19:10 | kaynak: altyazı |
## Açıklama bağlantıları
- https://skool.com/doa-zero — Skool topluluğu (doa-zero) · aday: hayır · Açıklamada geçiyor; videoda kullanılan bir araç değil, topluluk bağlantısı. · sınıf: diğer · erişilemez: Giriş gerekli veya ücretli topluluk olabilir; doğrulanamadı
- https://github.com/TestSprite/testsprite-cli — TestSprite CLI resmi deposu · aday: evet (TestSprite CLI) · Videoda npm ile kurulup kullanılan CLI aracının deposu. · sınıf: diğer
- https://www.youtube.com/watch?v=wjvUIPylcy0 — Kanal videosu · aday: hayır · Referans/ilham videosu; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://www.youtube.com/watch?v=T7xJ1gaZP7I — Kanal videosu · aday: hayır · Referans videosu; kullanılan bir araç değil. · sınıf: diğer
- https://www.youtube.com/watch?v=Pj2FnVE-W3c — Kanal videosu (TestSprite önceki video) · aday: hayır · Referans videosu; araç değil. · sınıf: diğer
- https://www.instagram.com/esadcom/ — Yazarın Instagram profili · aday: hayır · Yazar sosyal medya profili; araç ya da servis değil. · sınıf: diğer
- https://x.com/esadcom_ — Yazarın X profili · aday: hayır · Yazar sosyal medya profili; araç ya da servis değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kart düzeni (card layout) | Genel Bakış sayfasında ilan, puanlanan, taslak ve başvuru sayıları istatistik kartlarıyla gösterilir. (karede: Genel Bakış: üstte istatistik kartları, altta başvuru hunisi kartı) | 17:58 | kare |
| Sekmeli gezinme (tab navigation) | Genel Bakış, İlanlar, Başvurular, Belgeler ve Etkinlik sekmeleri arasında geçiş yapılır. (karede: Üst sekme çubuğunda Genel Bakış, İlanlar, Başvurular, Belgeler, Etkinlik) | 17:58 | kare |
| Kanban panosu (kanban board) | Başvurular Taslak → Başvuruldu → Mülakat → Teklif → İşe alındı → Kapandı aşamalarında takip edilir. (karede: Panel raporu metni: 'Taslak → Başvuruldu → Mülakat → Teklif → İşe alındı → Kapandı') | 8:28 | kare |
| Açılır filtre (dropdown filter) | İlanlar sekmesinde Durum ve Uygunluk filtreleriyle liste daraltılır. (karede: İlanlar sekmesinde 'Durum: hepsi' ve 'Uygunluk: hepsi' açılır alanları) | 17:23 | kare |
| Rozet (badge) | Uygunluk seviyesi low, medium, high renkli rozetlerle gösterilir. (karede: İlan satırlarında low, medium ve high renkli rozetler) | 17:23 | kare |
| Veri tablosu (data table) | İlanlar Puan, Uygunluk, Şirket, Ünvan, Konum, Portal, Yayın, Durum sütunlarıyla listelenir. (karede: Tablo başlıkları: Puan, Uygunluk, Şirket, Ünvan, Konum, Portal, Yayın, Durum) | 17:23 | kare |
| PDF önizleme (iframe embed) | Belgeler sekmesinde CV PDF'i yan panelde önizlenir. (karede: Sağda CV PDF önizlemesi, solda belge listesi) | 17:58 | kare |
| Etkinlik akışı (activity feed) | Etkinlik sekmesinde son değişen dosyalar zaman damgasıyla listelenir. (karede: Son değişen dosyalar listesi ve tarih damgaları) | 18:12 | kare |
| Koyu tema (dark theme) | Arayüz koyu renk paletiyle tasarlanmış. (karede: Koyu arka plan ve açık metinli panel) | 17:14 | kare |
| Sorgulama ile otomatik yenileme (polling) | Arayüz 2,5 saniyede bir sunucudan durum çeker (setInterval). (karede: Kod ekranında 'poll(); setInterval(poll, 2500);') | 14:08 | kare |
| Maskot logo (mascot logo) | Başlıkta tatlı bir kuş maskotu logo olarak kullanılır. | 14:08 | altyazı |
| Klavye kısayolu (keyboard shortcut) | Kısayolla pano değiştirme beklenirken çalışmadı; test başarısız oldu. | 18:10 | altyazı |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude | Terminalde Claude Code oturumunu başlatır. (karede: Terminalde 'Claude Code v2.1.266' başlığı) | 5:40 | kare |
| /setup | Claude Code içinde profil ve CV kurulum akışını başlatır; sorular sorar. | 2:01 | altyazı |
| pip install playwright && playwright install chromium | Playwright ve Chromium tarayıcısını kurar (ATS uyumlu PDF üretimi için). (karede: Plan metninde 'pip install playwright && playwright install chromium') | 6:08 | kare |
| /scrape | Ayarlı aramalarla LinkedIn ve Freehire'dan ilan çeker ve kaydeder. | 9:05 | altyazı |
| /rank | Çekilen ilanları profile göre puanlar ve sıralar (low, medium, high). | 11:07 | altyazı |
| /apply | Seçilen ilanlar için CV, ön yazı ve başvuru dokümanı üretir; ATS kontrolü yapar. | 11:07 | altyazı |
| /interview | Mülakat hazırlığı ve mock mülakat belgesi üretir. (karede: Terminalde '/interwiew' (OCR okuması) komut önerisi) | 4:42 | kare |
| /outcome | Başvurunun durumunu (mülakat, teklif, red) kaydeder; panel yalnızca okur. (karede: Panelde 'Durum değiştirmek için terminalde /outcome <şirket>' yazısı) | 12:54 | kare |
| python3 tools/panel.py --open | Yerel takip panelini açar (localhost:8765). (karede: Panel hazır mesajı ve localhost:8765 adresi) | 8:28 | kare |
| python3 tools/panel.py --export <dizin> | Paneli statik dosyalara aktarır (durum JSON'u ve belgeler tek klasörde). (karede: Terminalde '--export <dizin>' açıklaması) | 16:54 | kare |
| npm install -g @testsprite/testsprite-cli | TestSprite CLI'ı global olarak kurar. (karede: Terminalde npm install komutu) | 15:34 | kare |
| gh repo clone TestSprite/testsprite-cli | TestSprite CLI deposunu GitHub CLI ile klonlar. (karede: Terminalde '> gh repo clone TestSprite/testsprite-cli' satırı) | 15:52 | kare |
| vercel deploy --prod --scope goatstarter | Uygulamayı Vercel'e production olarak deploy eder. (karede: 'command: vercel deploy --prod --scope goatstarter' satırı) | 17:10 | kare |
| testsprite test create-batch --plan-from-dir .testsprite/plans --run --wait --timeout 900 --output json | Plan klasöründeki 6 testi oluşturup çalıştırır ve sonuçları JSON olarak kaydeder. (karede: Terminalde 'testsprite test create-batch' komutu) | 18:46 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| AI Job Search reposu 40.000'den fazla yıldıza sahip. | 1:00 | sayısal |
| Repo Danimarka pazarı için yapılmış; Türkiye'ye uyarlamak gerekiyor. | 1:00 | özellik |
| Arama 14 sorgu, 151 ilan ve 40 ilan detayı ile yapıldı. | 9:05 | sayısal |
| Önceki futbol uygulaması TestSprite'ta 90 puan aldı. | 16:09 | sayısal |
| TestSprite'ın tamamen ücretsiz bir CLI kullanımı var. | 15:10 | özellik |
| Ücretsiz ngrok sürümü uyarı sayfası gösterip otomatik testi bozuyor. | 16:44 | karşılaştırma |
| Panel yalnızca Python standart kütüphanesi kullanır; ekstra kurulum gerektirmez. | 8:24 | özellik |
| Testlerin 6 tanesinden biri (klavye kısayolu ile pano değiştirme) başarısız. | 18:10 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma | AI Job Search reposu | AI Job Search | 1:00 'AI Job Search isimli bir repo var' |
| konuşma | Repo yıldız sayısı | AI Job Search | 1:00 '40.000den fazla yıldız' |
| konuşma | /setup komutu | AI Job Search | 2:01 'slash setup yazıyorsunuz' |
| konuşma | İlan kaynağı LinkedIn | LinkedIn | 2:01 'LinkedIn vesaire de dahil' |
| konuşma | Kariyer.net veri kaynağı | Kariyer.net | 2:01 'Kariyer Netnet gibi sitelerden de veri çekecek' |
| konuşma | ATS kavramı | aday değil: genel kavram | 4:02 'Applicant tracking system' |
| konuşma | Claude (model ailesi) | Claude Code | 0:00 'Claude' ve 5:02 'cloud kod' |
| konuşma | Danimarka portalları (Jobindex, Jobnet vb.) | aday değil: başka adayın parçası (AI Job Search) | 6:08 'Danimarka mirası... jobindex, jobnet, jobbank' |
| konuşma | Railway bulut çalıştırma önerisi | aday değil: konu dışı | 14:08 'Railway gibi sistemler kullanarak' |
| konuşma | Anthropic kaynağı (frontend-design) | aday değil: genel kavram | 12:08 'Antropin resmi yeteneklerinden' |
| konuşma | Yazarın şirketleri (ARspar, ARtonar, Maiony) | aday değil: konu dışı | 0:00 'ARspar, ARtonar ve Maiony' |
| konuşma | Instagram video tanıtımı | aday değil: konu dışı | 1:00 'Instagram'da video çektim' |
| konuşma | Test edilen önceki futbol uygulaması | aday değil: konu dışı | 16:09 'Bir futbol uygulaması yapmıştık' |
| konuşma | TestSprite platformu | TestSprite | 15:09 'benim en sevdiğim araçlardan bir tanesi test sprite' |
| konuşma | Visual Studio Code | Visual Studio Code | 5:02 'VS koda götüreceğiz' |
| kare | ChatGPT yazısı (örnek CV) | aday değil: konu dışı | 0:58 'ChatGPT..' ekran metni |
| kare | Canva (örnek CV) | aday değil: konu dışı | 1:14 'Canva, sosyal medya yönetimi' |
| kare | GitHub commit geçmişi | AI Job Search | 1:40 commit 'fix(scrape)' satırları |
| kare | Kod deposu (isbulucu.git) | İş Bulucu | 5:54 'https://github.com/goatstarter/isbulucu.git' |
| kare | Bun gereksinimi | Bun | 3:22 'Bun (for job search CLI tools)' |
| kare | Python 3.10+ gereksinimi | Python | 3:22 'Python 3.10+' |
| kare | Alternatif ajanlar (Codex, Gemini CLI, Antigravity) | aday değil: genel kavram | 2:12 'Codex, Gemini CLI, Antigravity' yazısı |
| kare | Notion sync (opsiyonel) | aday değil: konu dışı | 3:24 '/notion-sync one-way pipeline' |
| kare | freehire.me sitesi | Freehire | 3:24 'freehire.me' ekran metni |
| kare | Ko-fi bağış sayfası | aday değil: sponsor/reklam | 3:26 'ko-fi.com/madslorentzen' |
| kare | Kariyer.net ekran metni | Kariyer.net | 3:36 'kariyer.net' ekran metni |
| kare | Claude Code sürümü | Claude Code | 5:40 'Claude Code v2.1.266' |
| kare | MCP sunucu uyarısı | aday değil: genel kavram | 5:40 'MCP servers need authentication' |
| kare | Playwright kurulum komutu | Playwright | 6:08 'pip install playwright && playwright install chromium' |
| kare | LinkedIn DT Cloud ilanı | LinkedIn | 10:18 'tr.linkedin.com/jobs/view/full-stack-engineer' |
| kare | viravira.co şirketi | aday değil: konu dışı | 11:50 'viravira.co' ekran metni |
| kare | frontend-design skill | frontend-design | 12:48 'Skill(frontend-design:frontend-design)' |
| kare | CML ve Insider One şirket sayfaları | aday değil: konu dışı | 12:08 'cmlteam.com' ve 14:08 'insiderone.com' |
| kare | TestSprite web sitesi | TestSprite | 15:10 'testsprite.com' ekran metni |
| kare | amazon.com demo sitesi | aday değil: konu dışı | 15:12 'https://www.amazon.com' ekran metni |
| kare | TestSprite CLI kurulumu | TestSprite CLI | 15:34 'npm install -g @testsprite/testsprite-cli' |
| kare | Discord ve gitleaks/Prettier dosyaları (CLI repo) | aday değil: konu dışı | 15:26 'Discord', '.gitleaks.toml', '.prettierrc' ekran metni |
| kare | ngrok tünelleme aracı | ngrok | 16:32 'ngrok' ekran metni |
| konuşma | Cloudflare tünel denemesi | Cloudflare | 16:09 'cloud flare muhabbeti' |
| kare | Vercel dağıtım URL'leri | Vercel | 16:54 'vercel.app' ve 17:10 'isbulucu-panel.vercel.app' |
| kare | Vercel panel bağlantısı | Vercel | 17:08 'vercel.com/goatstarter/isbulucu-panel' |
| kare | Kod yazmadan futbol uygulaması başlığı | aday değil: konu dışı | 16:12 'Kod Yazmadan Futbol Uygulaması Yaptım' kanal videosu |
| açıklama | Skool topluluk bağlantısı | aday değil: konu dışı | açıklama 'skool.com/doa-zero' |
| yorum | Türkçe repo bağlantısı isteği | İş Bulucu | yorum 'Türkçeye çevirdiğin github reposunun linkini ekler misin?' |
| yorum | TestSprite bilgisi övgüsü | TestSprite | yorum 'testsprite bilgisini paylaşmanız çok iyi' |
## Kareden okunanlar
- 0:58: ChatGPT.. ve iCloud Drive yazıları; CV örneği ekranı.
- 1:40: github.com/MadsLorentzen/ai-job-search commit geçmişi: 'fix(scrape): make seen_jobs.json keys a pure function'.
- 3:22: 'Bun (for job search CLI tools)' ve 'Python 3.10+' gereksinimleri.
- 5:40: 'Claude Code v2.1.266' ve 'Fable 5.1 with high effort · Claude Team'.
- 6:08: Plan metni: 'pip install playwright && playwright install chromium'; Danimarka portalları (jobindex, jobnet, jobbank, jobdanmark) notu.
- 10:18: LinkedIn ilanı: 'Full Stack Engineer at DT Cloud' (tr.linkedin.com).
- 15:34: '$ npm install -g @testsprite/testsprite-cli' komutu ve TestSprite CLI README metni.
- 16:44: Ajan mesajı: 'Ngrok mevcut ama ücretsiz sürüm uyarı sayfası gösterip otomatik testi bozuyor.'
- 17:10: 'command: vercel deploy --prod --scope goatstarter' ve 'Yayın hazır: isbulucu-panel.vercel.app' metni.
- 18:46: 'testsprite test create-batch --plan-from-dir .testsprite/plans --run --wait --timeout 900 --output json' komutu.
## Belirsizlikler
- Zeynep Kaya hayali bir örnek profildir; CV ve ilanlar gerçek kişiye ait değildir.
- İlan sayısı: anlatımda 151, panel ekranında 147 ilan görünüyor; sayı tutarsız.
- İş Bulucu deposunun görünürlüğü: ekranda 'Private' rozeti görünüyor; erişim durumu netleşmedi.
- Vercel deploy adresi (isbulucu-panel.vercel.app) yalnızca video için açık bırakılmış; kapatılacağı söylenmiş, kalıcılığı doğrulanamadı.
- Video 'Cloud' olarak transkribe ediliyor; kastedilen araç Claude Code'dur.
- Bağlantılı sayfalar listesindeki çok sayıda URL (Vercel Flags dokümanları, Product Hunt, Nora/PolyDub gibi repolar, esperanza.org) videoda anlatılmadığı için iz ve adaylara alınmadı.
- CV ve ilan metinlerinde geçen teknolojiler (React, Node.js, Docker, AWS, Redis, Vue, Angular, Redux, Cypress, Tailwind vb.) yalnızca profil/ilan içeriği olarak görüldüğü için adaylara alınmadı.
- 'Kod yazmadan' başlığındaki ve kanal videolarındaki ek araçlar (iTerm, Railway, Descript, Notion vb.) net kullanılmadığı için yalnız iz'de değerlendirildi.
- Skool topluluğu (doa-zero) içeriğine erişilemedi; ücretli olup olmadığı doğrulanamadı.
- '/interview' komutu OCR'da '/interwiew' olarak okundu; yazım doğrulanmadı.
- Kurulum için repo klonlama adresi (git clone) ekranda açıkça bir komut olarak gösterilmedi; yalnızca kopyalanan adres görüldü.
- TestSprite ücretsiz hesap ve CLI kullanımı iddiası, ücret planı doğrulanmadan aktarıldı.
- Test sonuçları için kesin geçen/kalan sayısı videoda net değil; anlatım 6 testten birinin başarısız olduğunu söylüyor.
## Atlanan segment oranı
0/20 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://skool.com/doa-zero | açıklama | açıklama | hayır |
| https://github.com/TestSprite/testsprite-cli | açıklama | açıklama | evet |
| https://www.youtube.com/watch?v=wjvUIPylcy0 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=T7xJ1gaZP7I | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=Pj2FnVE-W3c | açıklama | açıklama | hayır |
| https://www.instagram.com/esadcom/ | açıklama | açıklama | hayır |
| https://x.com/esadcom_ | açıklama | açıklama | hayır |
| https://github.com/MadsLorentzen/ai-job-search | 1:40 | ekran | evet |
| https://github.com/goatstarter/isbulucu.git | 5:10 | ekran | evet |
| https://freehire.me | 3:24 | ekran | evet |
| https://ko-fi.com/madslorentzen | 3:26 | ekran | hayır |
| https://kariyer.net | 3:36 | ekran | evet |
| https://linkedin.com/in/zeynepkaya | 1:04 | ekran | hayır |
| https://linkedin.com/in/elifsahin | 1:18 | ekran | hayır |
| https://tr.linkedin.com/jobs/view/full-stack-engineer-at-dt-cloud-4462169662 | 10:18 | ekran | hayır |
| https://tr.whatjobs.com/pub_api__cpl__2056233__7091 | 10:58 | ekran | hayır |
| https://viravira.co | 11:50 | ekran | hayır |
| https://cmlteam.com/about | 12:08 | ekran | hayır |
| https://insiderone.com/news/insider-becomes-insider-one/ | 14:08 | ekran | hayır |
| https://testsprite.com | 15:10 | ekran | evet |
| https://www.amazon.com | 15:12 | ekran | hayır |
| https://github.com/TestSprite/testsprite-cli | 15:26 | ekran | evet |
| https://example.com | 16:06 | ekran | hayır |
| https://isbulucu-panel.vercel.app | 17:10 | ekran | hayır |
| https://vercel.com/goatstarter/isbulucu-panel | 17:08 | ekran | hayır |
## İş akışı
- 1. adım — Viral AI Job Search reposunu inceleme — araçlar: GitHub, AI Job Search
- 2. adım — Türkiye pazarına uyarlanmış İş Bulucu reposunu alma ve açma — araçlar: GitHub, Visual Studio Code
- 3. adım — Claude Code'u terminalde başlatma — araçlar: Claude Code, Fable 5.1
- 4. adım — Repo raporunu Claude'a verip kurulumu yaptırma — araçlar: Claude Code
- 5. adım — Setup akışını çalıştırıp örnek CV yükleme ve profil sorularını yanıtlama — araçlar: Claude Code, /setup
- 6. adım — Kurulum kontrolü: Playwright ve Chromium kurulumu — araçlar: Playwright, Python, Bun
- 7. adım — İlanları çekme (scrape) — araçlar: LinkedIn, Freehire, Kariyer.net, /scrape
- 8. adım — İlanları uygunluğa göre puanlama — araçlar: /rank
- 9. adım — İlk üç ilan için CV, ön yazı ve başvuru dokümanı üretme ve ATS kontrolü — araçlar: /apply, Playwright
- 10. adım — Yerel takip panelini yazdırma ve açma — araçlar: Python, Claude Code, frontend-design, python3 tools/panel.py
- 11. adım — Mülakat ve başvuru durumu komutlarının panelde görünmesini kontrol etme — araçlar: /interview, /outcome
- 12. adım — TestSprite CLI'ı kurma ve klonlama — araçlar: TestSprite CLI, GitHub, npm
- 13. adım — Yerel uygulamayı dışa açma denemeleri (Cloudflare, ngrok) — araçlar: Cloudflare, ngrok
- 14. adım — Uygulamayı Vercel'e deploy etme ve URL doğrulama — araçlar: Vercel
- 15. adım — TestSprite ile 6 test planı yazma ve çalıştırma — araçlar: TestSprite CLI, TestSprite
- 16. adım — Başarısız testi tespit etme ve düzeltme — araçlar: Claude Code, TestSprite
- 17. adım — Düzeltme sonrası testleri yeniden gönderme — araçlar: TestSprite CLI
## Promptlar
- Repoyu kurup sonraki adımları planlatmak — Repo raporunu yapıştırıp kurulumu yapmasını ve sonraki adımları planlamasını istemek (Türkçe özet).
- Setup'ı kullanıcı gibi çalıştırmak — Geliştirici modundan çıkıp setup akışını sade kullanıcı gibi başlatmasını istemek; tek CV yüklemek.
- Yerel panel arayüzü yaptırmak — Scrape ve apply sonuçlarını takip etmek için yerel web arayüzü yapmasını, tasarımı ürün seviyesine çıkarmasını istemek.
- TestSprite ile test yaptırmak — Uygulamayı TestSprite ile gerçek kullanıcı gibi test edip sonuçları raporlamasını istemek.
- Canlıya alıp test etmek — Lokal uygulamayı Vercel'e alıp TestSprite testlerini çalıştırmasını; karar konusunda serbest bırakmak.
- Başarısız testleri düzeltmek — Başarısız testlerdeki sorunları çözüp testleri yeniden göndermesini istemek.
ikinci göz KAPALI: --ikinci-goz yok
