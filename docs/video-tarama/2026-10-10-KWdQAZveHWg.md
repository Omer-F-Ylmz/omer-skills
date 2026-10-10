# Tek Bir Prompt ile Profesyonel Video Üretmek: Claude Code & Remotion Rehberi
## Künye
Tek Bir Prompt ile Profesyonel Video Üretmek: Claude Code & Remotion Rehberi · Burhan KOCABIYIK · süre: 10:03 · tr-orig · https://youtu.be/KWdQAZveHWg · şema 2
motor: parti 2026-10-10-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 198057 tk · claude-haiku-5-5: claude-haiku-5-5 · 126420 tk
## Özet
Burhan Kocabıyık, Claude Code ve Remotion ile tek prompt ya da web sitesi linkinden animasyonlu, müzikli tanıtım videosu üretmeyi gösteriyor. VS Code'a Claude Code eklentisi kuruluyor, terminalde `npx skills add remotion-dev/skills` ile Remotion skill'i ekleniyor. Ön koşul olarak Node.js ve Git anlatılıyor. Leftflow AI için yazılan promptla Claude Code siteyi okuyor, yapılacaklar listesi çıkarıyor ve Remotion projesi kuruyor. İstanbul'un Fethi YouTube otomasyonu örneği gösteriliyor. Sonda video ajansı fırsatı, DOA topluluğu ve n8n (otomasyon) ile Claude Code (ajan) farkı anlatılıyor.
## Bölümler
- 0:00 Tek Prompt ile Yapay Zeka Videosu Üretme Giriş
- 0:43 Teknik Kurulum: Claude Code ve ReMotion Entegrasyonu
- 1:35 Remotion Nedir? Video Kodlamanın Geleceği
- 1:59 Adım 1: VS Code ve Gerekli Extensionların Kurulumu
- 3:03 Adım 2: Node.js, Git ve Remotion Skills Kurulumu
- 4:24 Uygulama: Web Sitesi Linkinden Otomatik Video Üretmek
- 5:48 Remotion Arayüzü ve Canlı Önizleme Teknikleri
- 7:07 YouTube Otomasyonu ve Tanıtım Videosu Örnekleri
- 8:25 Video Ajansı Kurmak ve Ticari Fırsatlar
- 9:37 Sonuç: n8n (Otomasyon) ve Claude Code (Ajan) Farkı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Videoyu baştan sona üreten ana yapay zekâ kodlama ajanı; VS Code eklentisi olarak kullanılıyor. | 2:36 | Eklenti sayfası 'Claude Code for VS Code', sağ panelde sohbet açık. (karede: Extension: Claude Code for VS Code sayfası, Anthropic yayıncısı, Disable/Uninstall düğmeleri.) |
| Remotion | yok | skill | https://github.com/remotion-dev/remotion | React ile kodla video üreten çerçeve; skill olarak Claude Code'a ekleniyor. | 3:44 | Remotion, React ile kod yazarak video üretmenizi sağlayan bir framework'tür. |
| remotion-best-practices | yok | skill | https://github.com/remotion-dev/skills | remotion-dev/skills deposundan kurulan Remotion en iyi uygulamalar skill'i. | 3:12 | Terminalde Skill: remotion-best-practices, kaynak remotion-dev/skills.git. (karede: VS Code terminalinde 'Skill: remotion-best-practices' ve 'Source: https://github.com/remotion-dev/skills.git'.) |
| Skills CLI | yok | CLI | yok | `npx skills add` ile skill kuran komut satırı aracı. | 3:18 | Terminalde 'npx skills add remotion-dev/skills' çalıştırılıyor. (karede: Mac terminalinde 'arspar@Mac ~ % npx skills add remotion-dev/skills'.) |
| VS Code | yok | CLI | yok | Claude Code eklentisinin ve terminalin çalıştığı kod editörü. | 1:59 | İlk aşama VS kodu indiriyoruz. |
| Node.js | yok | CLI | yok | npx/npm için ön koşul; LTS sürümü öneriliyor. | 3:03 | En son versiyonu LTS'i indirmenizi tavsiye ederim. |
| Git | yok | CLI | yok | Skill deposunu klonlamak için ikinci ön koşul. | 3:03 | İkinci bir ihtiyacınız olan şey Git'in kurulu olması lazım. |
| npm | yok | CLI | yok | Claude Code'un Remotion bağımlılıklarını kurduğu paket yöneticisi. | 8:54 | 'npm install --save-exact typescript @types/react' çalıştırılıyor. (karede: Bash 'Install TypeScript dependencies' ve npm install --save-exact komutu.) |
| create-video | yok | CLI | yok | Yeni Remotion projesi oluşturan `npx create-video@latest` aracı. | 8:00 | 'Welcome to Remotion!' çıktısı, create-video@4.0.422. (karede: İzin penceresi 'allow npx create-video@latest', terminalde 'Welcome to Remotion!'.) |
| Web Fetch | yok | teknik | yok | Claude Code'un leftflow.ai sayfasını çekmek için kullandığı araç. | 5:52 | 'Web Fetch https://leftflow.ai/' ve 'Allow fetching this url?' izni. · kanıt: kare (karede: Claude panelinde Web Fetch https://leftflow.ai/ ve izin kutusu.) |
| Web Search | yok | teknik | yok | Claude Code'un Leftflow hakkında web araması yapması. | 5:52 | 'Web Search Leftflow AI platform nedir ne yapar' satırı. · kanıt: kare (karede: Claude panelinde Web Search sorguları ve sonuç linkleri.) |
| ChatGPT | yok | prompt | yok | İngilizce prompt ChatGPT 5.2 ile hazırlanıp Claude Code'a yapıştırılmış. | 2:12 | ChatGPT 5.2'de 'Make a promo video for the Leftflow AI platform'. (karede: ChatGPT penceresi, Leftflow promo video promptu ve madde listesi.) |
| Homebrew | yok | CLI | yok | Mac'te Git kurulumu için gösterilen seçenek. | 3:36 | Git sayfasında '$ brew install git'. · kanıt: kare (karede: git-scm.com/install/mac, Homebrew başlığı altında brew install git.) |
| MacPorts | yok | CLI | yok | Mac'te Git kurulum seçeneği olarak gösterilen yöntem. | 3:36 | '$ sudo port install git'. (karede: Git macOS sayfasında MacPorts bölümü.) |
| nvm | yok | CLI | yok | Node.js indirme sayfasında gösterilen sürüm yöneticisi betiği. | 3:24 | nvm install.sh curl komutu ve 'nvm install 24'. (karede: nodejs.org/en/download sayfasında nvm ile v24 kurulum komutları.) |
| TypeScript | yok | teknik | yok | Claude Code'un Remotion projesine eklediği tür sistemi. | 8:54 | 'Install TypeScript dependencies' komutu. (karede: Bash Install TypeScript dependencies adımı.) |
| Tailwind CSS | yok | teknik | yok | create-video kurulumunda sorulan isteğe bağlı stil seçeneği. | 8:12 | 'Add TailwindCSS? No / Yes' sorusu. (karede: Terminal çıktısında 'Add TailwindCSS?' sorusu.) |
| n8n | yok | iş akışı | yok | Müşteri teslimlerinde otomasyon için tercih edilen araç. | 9:37 | Müşterileri teslim ediyorken N8'yi kullanıyorum, çünkü çok daha iyi çalışıyor. |
| Codex | yok | CLI | yok | Yorumda Claude yerine alternatif olarak anılıyor. | açıklama | Yorum: Codex, openrouter vs ile de kullanabilirsiniz. |
| OpenRouter | yok | CLI | yok | Yorumda alternatif model erişimi olarak anılıyor. | açıklama | Yorum: Codex, openrouter vs ile de kullanabilirsiniz. |
| React | yok | teknik | yok | Remotion videolarının bileşen yapısını sağlayan UI kütüphanesi; video sahneleri React bileşeni olarak yazılır. | 3:52 | Use React, a powerful frontend technology, to create (karede: remotion.dev ana sayfası: 'Use React, a powerful frontend technology, to create' metni) |
| Leftflow tanıtım videosu üretimi | yok | prompt | yok | Leftflow AI platformu için tanıtım videosu oluştur; siteden görselleri, arayüz görüntülerini ve hareketli öğeleri kullan, Leftflow logosunu koy; ne yaptığı, çözdüğü problem, süreç otomasyonu ve değer önerisi odakta olsun; modern, temiz, teknolojik. | 5:24 | kaynak: kare |
| Claude Code'u Remotion akışına yönlendirmek | yok | prompt | yok | Kullanıcı Remotion ile video yapmak istediğini söylüyor; Claude proje kurulumu için mevcut proje olup olmadığını soruyor. | 4:24 | kaynak: kare |
| Remotion kurulumunu kontrol etmek | yok | prompt | yok | Remotion şu anda yüklü mü diye sorarak kurulumu doğrulat. | 6:48 | kaynak: altyazı |
## Açıklama bağlantıları
- https://drive.google.com/drive/folders/1Zg1kjVcxKWLxVcE6xTD4D1y8zGjtvyCI?usp=sharing — Kurulum dosyalarının bulunduğu Google Drive klasörü · aday: hayır · Kaynak dosya paylaşımı; videoda kullanılan araç değil, Drive yalnız barındırma. · sınıf: diğer
- https://www.skool.com/doa — DOA ücretli topluluk sayfası · aday: hayır · Yazarın kendi topluluk reklamı; araç değil, içerik giriş gerektiriyor. · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- skool.com/doa/about — DOA topluluğunun hakkında sayfası. · aday: hayır · Yazarın topluluk tanıtım sayfası (reklam). · sınıf: diğer · erişilemez: giriş gerekli (Skool, ücretli topluluk)
- skool.com/doa-zero/about — 'Tüm kaynaklar %100 ücretsiz' başlıklı topluluk sayfası. · aday: hayır · Yazarın kaynak/topluluk tanıtım sayfası (reklam). · sınıf: diğer · erişilemez: giriş gerekli (Skool)
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx skills add remotion-dev/skills | Remotion skill'ini Claude Code için kurar. (karede: Mac terminalinde 'npx skills add remotion-dev/skills' yazılı.) | 3:18 | kare |
| curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh / bash | nvm'i kurar (Node.js sayfasındaki komut). (karede: nodejs.org/en/download sayfasında nvm kurulum komutu.) | 3:24 | kare |
| nvm install 24 | Node.js 24 sürümünü kurar. (karede: Node.js sayfasındaki kod bloğu.) | 3:24 | kare |
| brew install git | Mac'te Git'i Homebrew ile kurar. (karede: git-scm.com/install/mac sayfasında.) | 3:36 | kare |
| sudo port install git | Mac'te Git'i MacPorts ile kurar. (karede: git-scm.com/install/mac sayfasında.) | 3:36 | kare |
| npx create-video@latest | Yeni Remotion projesi oluşturur. (karede: remotion.dev ana sayfasında '$ npx create-video@latest'.) | 3:52 | kare |
| cd my-video && npm start | Remotion önizlemesini başlatır (Claude yanıtında). (karede: Claude yanıtında 'cd my-video && npm start'.) | 4:26 | kare |
| which node && node --version && which npx | Node ve npx varlığını kontrol eder (Claude çalıştırdı). (karede: Bash 'Check Node.js and npx availability'.) | 7:58 | kare |
| npm install --save-exact typescript @types/react @types/react-dom | TypeScript bağımlılıklarını kurar. (karede: Bash 'Install TypeScript dependencies'.) | 8:54 | kare |
| xcode-select --install | Xcode Command Line Tools kurar; içinde Git ikili paketi gelir. (karede: git-scm.com macOS sayfasında Xcode Command Line Tools komutu) | 3:36 | kare |
| node -v | Node.js sürümünü gösterir (beklenen: v24.13.1). (karede: '# Verify the Node.js version: node -v # Should print v24.13.1.') | 3:24 | kare |
| npm -v | npm sürümünü gösterir (beklenen: 11.8.0). (karede: 'npm -v # Should print "11.8.0".' satırı) | 3:24 | kare |
| mkdir -p /Users/<kullanıcı>/Desktop/leftflow-video | Remotion projesi için leftflow-video klasörünü oluşturur (kullanıcı adı gizlendi). (karede: Claude Code izin penceresinde 'Allow this bash command' ve mkdir -p komutu) | 7:56 | kare |
| echo "blank" / npx create-video@latest --no-open . | Remotion blank şablonunu mevcut klasöre tarayıcı açmadan kurar. (karede: Claude Code bash komutu: 'Create Remotion blank project non-interactively') | 8:00 | kare |
| npx -yes create-video@latest --blank | leftflow-video klasöründe Remotion blank projesini oluşturur. (karede: Claude Code bash komutu: 'Manually set up Remotion project') | 8:14 | kare |
| npm init -y && npm install --save-exact remotion @remotion/cli @remotion/player react ... | package.json oluşturur ve Remotion bağımlılıklarını (remotion, @remotion/cli, @remotion/player, react) kurar; liste ekranda kırpılmış. (karede: Claude Code bash komutu: 'npm init -y' ve 'npm install --save-exact remotion @remotion/cli @remotion/player react') | 8:56 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Remotion'ın video duyurusunu 14 milyon kişi izlemiş. | 1:48 | sayısal |
| Remotion çalışması için Node.js ve Git kurulu olmalı. | 3:03 | özellik |
| Claude Code ücretli; ChatGPT aboneliği gibi çalışıyor. | 5:48 | özellik |
| Tek prompttan animasyon, müzik ve görselli video üretilebiliyor. | 0:00 | özellik |
| Müşteri teslimlerinde n8n daha iyi; hızlı üretimde Claude Code tercih ediliyor. | 9:37 | karşılaştırma |
| Eskiden 1 dakikalık video için freelancer'a ciddi ödeme gerekiyordu. | 8:25 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code ile tek prompttan video | Claude Code | Tek prompt ile video oluşturulduğu söyleniyor. |
| konuşma 3:44 | Remotion | Remotion | Remotion, React ile video üreten framework. |
| kare 3:12 | remotion-best-practices skill | remotion-best-practices | Terminalde skill adı görünüyor. |
| kare 3:18 | npx skills add | Skills CLI | Komut terminalde çalıştırılıyor. |
| konuşma 1:59 | VS Code | VS Code | VS Code indirilip kuruluyor. |
| konuşma 3:03 | Node.js | Node.js | Ön koşul olarak anlatılıyor. |
| konuşma 3:03 | Git | Git | Ön koşul olarak anlatılıyor. |
| kare 3:36 | Homebrew | Homebrew | brew install git gösteriliyor. |
| kare 3:36 | MacPorts | MacPorts | sudo port install git gösteriliyor. |
| kare 3:24 | nvm | nvm | Node sayfasında nvm betiği. |
| kare 8:00 | create-video | create-video | Remotion projesi oluşturuluyor. |
| kare 8:54 | npm install | npm | Bağımlılıklar kuruluyor. |
| kare 8:54 | TypeScript | TypeScript | typescript paketi kuruluyor. |
| kare 8:12 | TailwindCSS sorusu | Tailwind CSS | Kurulumda soruluyor. |
| kare 5:52 | Web Fetch | Web Fetch | Claude siteyi çekiyor. |
| kare 5:52 | Web Search | Web Search | Claude web araması yapıyor. |
| kare 2:12 | ChatGPT 5.2 | ChatGPT | Prompt ChatGPT'de hazırlanmış. |
| konuşma 9:37 | n8n | n8n | Müşteri teslimlerinde kullanılıyor. |
| yorum | Codex | Codex | Yorumda alternatif olarak anılıyor. |
| yorum | OpenRouter | OpenRouter | Yorumda alternatif olarak anılıyor. |
| yorum | React (MoviePy sorusu) | aday değil: başka adayın parçası (Remotion) | Remotion'ın React tabanı. |
| yorum | MoviePy | aday değil: konu dışı | Yorumcu alternatif soruyor, videoda kullanılmıyor. |
| açıklama | Google Drive klasörü | aday değil: konu dışı | Dosya paylaşım bağlantısı. |
| açıklama | Skool DOA topluluğu | aday değil: sponsor/reklam | Yazarın kendi topluluk reklamı. |
| kare 1:12 | Skool classroom sayfaları | aday değil: sponsor/reklam | Topluluk tanıtımı. |
| kare 1:18 | Bolt, Lovable, Replit, Antigravity, Apify, MCP | aday değil: konu dışı | Yalnız Skool ders listesinde görünüyor. |
| kare 1:42 | X (Twitter) araması | aday değil: konu dışı | Remotion duyurusu için gezilen sayfa. |
| kare 1:44 | ElevenLabs, Vidu, Higgsfield, Flexclip, Claude Opus 4.5 | aday değil: konu dışı | Başkalarının X gönderilerinde geçiyor. |
| kare 1:38 | Kling, Seedance, Grok, Supabase | aday değil: konu dışı | X haber kutusu ve yer imlerinde. |
| kare 2:32 | Diğer Claude eklentileri | aday değil: konu dışı | Marketplace arama listesinde, kurulmuyor. |
| kare 5:46 | Framer | aday değil: konu dışı | Claude, sitenin Framer ile yapıldığını belirtiyor. |
| konuşma 7:07 | YouTube otomasyonu videosu (İstanbul'un Fethi) | Remotion | Remotion ile üretilmiş örnek çıktı. |
| konuşma 0:00 | Leftflow tanıtım videosu | Remotion | Remotion ile üretilmiş örnek çıktı. |
| kare 0:42 | Google Docs kurulum özeti | aday değil: konu dışı | Yazarın notları, araç değil. |
## Kareden okunanlar
- 0:10: Solda leftflow.ai sitesi, sağda 'Yapay Zeka ile Çözüm' başlıklı üretilmiş video; AI Chatbot, Sesli Asistan, Otomasyon düğmeleri.
- 0:42: Google Docs 'CLAUDE CODE + REMOTION KURULUM ÖZETİ': Aşama 1 VSCode, Aşama 2 'npx skills add remotion-dev/skills', Node.js ve Git ön koşulları.
- 1:42: X'te 'remotion claude code' araması; Remotion'ın Agent Skills duyurusu.
- 2:36: VS Code Extensions: 'Claude Code for VS Code', Anthropic, anthropic.claude-code.
- 3:12: Terminalde Skill: remotion-best-practices, repo klonlandı, ajan seçimi listesi.
- 3:24: nodejs.org/en/download: v24.13.1 (LTS), macOS, nvm, npm; nvm kurulum komutları.
- 3:36: git-scm.com macOS: Homebrew, MacPorts, Xcode CLT seçenekleri.
- 3:52: remotion.dev: 'Make videos programmatically.' ve '$ npx create-video@latest'.
- 5:32: Claude Code yapılacaklar listesi: içerik çekme, Remotion kurulumu, sahneler, medya, render.
- 7:56: Claude Code 'Create Remotion project for Leftflow video' bash izni.
## Belirsizlikler
- Videodaki Claude modeli ekranda belirtilmiyor; X gönderilerinde Opus 4.5, eklenti listesinde Opus 4.6 geçiyor, kullanılan sürüm belirsiz.
- X aramasında ve listelerde görünen ElevenLabs, Vidu, Higgsfield, Flexclip, Kling, Seedance gibi adlar videoda kullanılmıyor.
- Ekranda geçen Framer, Antigravity, Supabase, ngrok, Hermes Agent gibi adlar yalnız menü/liste ya da yan bilgi; kullanılmadı.
- Müzik/görsel üretiminin nasıl yapıldığı gösterilmiyor; Remotion önizleme arayüzü yalnız sözle anılıyor.
- Altyazıda 'cloud code' Claude Code anlamında, 'MPX skills' npx skills olarak okundu.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/16 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| leftflow.ai | 0:10 | ekran | hayır |
| form.leftflow.ai | 0:34 | ekran | hayır |
| https://docs.google.com/document/d/1ytl0Noe03ab6X-T_-Jy9kqQOwlT9NLJISyhqfpWiduM/edit?tab=t.0 | 0:42 | ekran | hayır |
| https://code.visualstudio.com/download | 0:42 | ekran | evet |
| https://nodejs.org/en/download | 0:42 | ekran | evet |
| https://git-scm.com/install/ | 0:42 | ekran | evet |
| skool.com/doa | 1:12 | ekran | hayır |
| skool.com/doa/about | açıklama | açıklama | hayır |
| skool.com/doa-zero/about | açıklama | açıklama | hayır |
| https://drive.google.com/drive/folders/1Zg1kjVcxKWLxVcE6xTD4D1y8zGjtvyCI?usp=sharing | açıklama | açıklama | hayır |
| skool.com/doa/classroom | 1:16 | ekran | hayır |
| https://www.skool.com/skoolers | 1:20 | ekran | hayır |
| x.com/search?q=remotion%20claude%20code&src=typed_query | 1:42 | ekran | hayır |
| x.com/Remotion/status/2013626968386765291 | 1:48 | ekran | hayır |
| gist.github.com/JonnyBurger/5b | 1:50 | ekran | hayır |
| https://code.visualstudio.com | 2:02 | ekran | evet |
| claude.com/claude-code | 2:36 | ekran | evet |
| anthropic.com | 2:36 | ekran | hayır |
| https://github.com/remotion-dev/skills.git | 3:12 | ekran | evet |
| https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | 3:24 | ekran | evet |
| git-scm.com/install/mac | 3:36 | ekran | evet |
| https://nodejs.org/dist/v24.13.1/node-v24.13.1.pkg | 3:42 | ekran | evet |
| https://www.remotion.dev | 3:48 | ekran | evet |
| https://voice.leftflow.ai/ | 5:52 | ekran | hayır |
| https://apidog.com/tr/blog/flowith-ai-inf | 6:04 | ekran | hayır |
| https://www.skool.com/doa/classroom/dc0b3c3b?md=710b834978eb4f7f9ed3698ef4b86456 | 1:18 | ekran | hayır |
| https://www.skool.com/doa/projenizi-bolt-lovable-replit-gibi-platformlardan-nasil-antigravityye-gecirebilirsiniz | 1:18 | ekran | hayır |
| https://x.com/compose/post | 1:39 | ekran | hayır |
| https://x.com/explore | 1:40 | ekran | hayır |
| https://x.com/exsiorn | 1:41 | ekran | hayır |
| https://x.com/Remotion | 1:48 | ekran | hayır |
| gist.github.com/JonnyBurger/5b... (tam okunamadı) | 1:50 | ekran | hayır |
| google.com/search?q=vs+code | 2:02 | ekran | hayır |
| visualstudio.com | 2:02 | ekran | hayır |
| https://code.visualstudio.com/downioad (OCR hatası, download) | 2:06 | ekran | evet |
| leftfiow.ai (OCR hatası, leftflow.ai) | 2:12 | ekran | hayır |
| Amazon.com | 3:32 | ekran | hayır |
| https://apidog.com/tr/blog/flowith-ai-inf... (web araması sonucu) | 6:04 | ekran | hayır |
| Lognät.com (OCR okunamadı) | 7:56 | ekran | hayır |
## İş akışı
- 1. adım — Üretilmiş Leftflow tanıtım videosunu gösterme — araçlar: Remotion, Claude Code
- 2. adım — Kurulum özet dokümanını açma — araçlar: Google Docs
- 3. adım — Remotion'ın X'teki skill duyurusunu gösterme — araçlar: Remotion
- 4. adım — VS Code'u indirme — araçlar: VS Code
- 5. adım — Extensions bölümünden Claude Code eklentisini bulup kurma — araçlar: VS Code, Claude Code
- 6. adım — Terminal açıp skill kurma komutunu çalıştırma — araçlar: VS Code, Skills CLI, remotion-best-practices
- 7. adım — Node.js LTS ve Git ön koşullarını gösterme — araçlar: Node.js, Git, nvm, Homebrew
- 8. adım — Claude Code'a Remotion ile video istediğini yazma — araçlar: Claude Code, Remotion
- 9. adım — Prompt'u hazırlayıp yapıştırma — araçlar: ChatGPT, Claude Code
- 10. adım — Siteyi okutma ve izin verme — araçlar: Web Fetch, Web Search, Claude Code
- 11. adım — Yapılacaklar listesiyle Remotion projesini oluşturma — araçlar: create-video, npm, Claude Code
- 12. adım — TypeScript ve Remotion bağımlılıklarını kurma — araçlar: npm, TypeScript
- 13. adım — Üretilen videoyu önizleyip YouTube otomasyonu örneğini gösterme — araçlar: Remotion
## Promptlar
- Leftflow tanıtım videosu üretimi — Leftflow AI platformu için tanıtım videosu oluştur; siteden görselleri, arayüz görüntülerini ve hareketli öğeleri kullan, Leftflow logosunu koy; ne yaptığı, çözdüğü problem, süreç otomasyonu ve değer önerisi odakta olsun; modern, temiz, teknolojik.
- Claude Code'u Remotion akışına yönlendirmek — Kullanıcı Remotion ile video yapmak istediğini söylüyor; Claude proje kurulumu için mevcut proje olup olmadığını soruyor.
- Remotion kurulumunu kontrol etmek — Remotion şu anda yüklü mü diye sorarak kurulumu doğrulat.
