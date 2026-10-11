# The EASY way to build a beautiful website with Claude Code (full workflow)
## Künye
The EASY way to build a beautiful website with Claude Code (full workflow) · Create a Pro Website · süre: 26:00 · en-orig · https://youtu.be/fDTwHIKltpc · şema 2
motor: parti 2026-10-11-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (48)
kareler: girdi ≤40000 jeton için 60→48
claude-sonnet-5-5: claude-sonnet-5-5 · 75910 tk · claude-haiku-5-5: claude-haiku-5-5 · 291276 tk
## Özet
Josh, Claude Code masaüstü uygulamasıyla sıfırdan Summit Ridge Landscaping adlı kurgusal bir peyzaj firması için tek HTML dosyalı profesyonel bir site kurar. Önce Claude Pro hesabı ve medya varlıkları hazırlanır (görseller ve hero videosu Higgsfield ile üretilmiş). Proje klasörü açılır, iki skill kurulur: Anthropic'in frontend-design skill'i ve UI UX Pro Max. İlham için Awwwards ve Dribbble taranır, referans ekran görüntüsü ve /ui-ux-pro-max ile tek bir prompt verilir; Claude soru sorar, logoyu ve renkleri klasörden okuyup siteyi üretir. Sonrasında hero kesilmesi düzeltilir, scroll ile oynayan video eklenir, seçme aracıyla bir bölüm sadeleştirilir. Son olarak Hostinger'da hosting ve ücretsiz alan adı alınıp dosyalar archive.zip olarak yüklenir ve site yayına çıkar.
## Bölümler
- 0:00 Giriş
- 1:09 Adım 1: Başlamak için gerekenler
- 2:58 Adım 2: Projeyi kurma
- 5:02 Adım 3: Skill'leri ekleme
- 7:34 Adım 4: Web sitesini oluşturma
- 9:45 Site kurma promptu
- 16:35 Düzenlemeler
- 19:55 Adım 5: Siteyi yayınlama
- 23:34 Ücretsiz özel alan adı
- 24:07 Site dosyalarını kopyalama
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Masaüstü uygulamasındaki Code sekmesinde siteyi üreten, dosyaları okuyup yazan ana kodlama aracı. | 2:58 | if you click on code, this is where we can actually get started building |
| Claude Pro | yok | ipucu | yok | Claude Code'a erişim için gereken, yaklaşık 17 $/ay'lık ücretli plan. | 1:12 | Fiyat tablosunda Pro planı 'Includes Claude Code' içeriyor. · kanıt: kare (karede: Fiyat tablosunda Pro planı 'Includes Claude Code' içeriyor.) |
| Claude Desktop | yok | CLI | yok | Chat, Cowork ve Code sekmelerini barındıran masaüstü uygulaması. | 2:58 | we have the chat tab, we have the co-work tab, and we have the Cloud code tab |
| Claude Design | yok | CLI | yok | Pro plana dahil olduğu söylenen tasarım aracı (yalnız anıldı). | 1:09 | You also get access to Cloud Design and Cloud Co-work |
| Claude Cowork | yok | CLI | yok | Pro plana dahil olduğu söylenen Cowork sekmesi (yalnız anıldı, kullanılmadı). | 1:09 | You also get access to Cloud Design and Cloud Co-work |
| Opus 4.8 | yok | teknik | yok | Code oturumunda model seçicide görünen, siteyi üreten ana yapay zekâ modeli (Medium). | 3:52 | Ekran metni 3:54: 'Opus4.8 Medium'. (karede: kanıttan) Ekran metni 3:54: 'Opus4.8 Medium'. |
| Higgsfield | yok | CLI | yok | Sitedeki görselleri ve hero videosunu üreten yapay zekâ görsel/video platformu. | 2:08 | Higgsfield logosu ve platform ana sayfası gösteriliyor. (karede: kanıttan) Higgsfield logosu ve platform ana sayfası gösteriliyor. |
| frontend-design | yok | skill | https://github.com/anthropics/skills/tree/main/skills/frontend-design | Anthropic'in skill'i; jenerik yapay zekâ görünümü yerine daha yaratıcı font ve yerleşim seçtirir. | 5:02 | first skill is called front-end design, and this is actually built by Anthropic |
| UI UX Pro Max | yok | skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | Renk paleti, font eşleşmesi, UI stili ve yığın bilgisi veren tasarım zekâsı skill'i; /ui-ux-pro-max ile çağrılır. | 6:02 | second skill here is called UI UX ProMax skill |
| uipro-cli | yok | CLI | yok | UI UX Pro Max'in npm paketi; uipro init --ai claude ile skill kurar. Claude yerel kurulum yaptı. | 7:06 | Ekran metni: 'Ran Install uipro-cli globally via npm'; 6:16 karesinde 'uipro init --ai claude'. (karede: kanıttan) Ekran metni: 'Ran Install uipro-cli globally via npm'; 6:16 karesinde 'uipro init --ai claude'. |
| npm | yok | CLI | yok | Paket yöneticisi; plugin'i global kurmak için promptta özellikle istendi, prefix ~/.npm-global'a ayarlandı. | 6:02 | install this plugin globally again using NPM |
| Node.js | yok | CLI | yok | Claude, node 24 ile CLI'ı doğrudan çalıştırdı ve statik sunucu için serve kullandı. | 7:06 | Ekran metni: 'I have node 24 but no bun'. (karede: kanıttan) Ekran metni: 'I have node 24 but no bun'. |
| esbuild | yok | CLI | yok | Claude'un CLI kaynağını paketlemek için kullandığı bundler. | 7:18 | Ekran metni: 'I'll bundle it with esbuild'. (karede: kanıttan) Ekran metni: 'I'll bundle it with esbuild'. |
| Git | yok | CLI | yok | Skill depolarını sparse checkout ve git clone ile çekmek için kullanıldı. | 7:00 | Ekran metni: 'git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git uiux-check'. (karede: kanıttan) Ekran metni: 'git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git uiux-check'. |
| Awwwards | yok | iş akışı | yok | Ödüllü web sitelerinden ilham alma kütüphanesi; canlı bağlantılar açılıp incelendi. | 7:34 | huge library of award-winning websites that you can get inspiration from |
| Dribbble | yok | iş akışı | yok | 'landscaping' aranıp referans tasarım ekran görüntüsü alınan ilham sitesi. | 8:34 | I'm going to type in landscape to see if I can find any inspiration |
| Playfair Display | yok | teknik | yok | Claude'un seçtiği başlık serif fontu (logoyla uyumlu). | 13:50 | Ekran metni: 'Playfair Display + Inter (elegant/premium...)'. (karede: kanıttan) Ekran metni: 'Playfair Display + Inter (elegant/premium...)'. |
| Inter | yok | teknik | yok | Playfair Display ile eşleştirilen gövde fontu. | 13:50 | Ekran metni: 'Playfair Display + Inter'. (karede: kanıttan) Ekran metni: 'Playfair Display + Inter'. |
| Tailwind CSS | yok | teknik | yok | Tek index.html dosyasında kullanılan stil çerçevesi (Claude'un özetinde). | 12:32 | Ekran metni: 'One self-contained index.html with Tailwind'. (karede: kanıttan) Ekran metni: 'One self-contained index.html with Tailwind'. |
| Claude Preview | yok | CLI | yok | Claude Code içindeki canlı önizleme paneli; Claude bununla eval ve ekran görüntüsü aldı. | 17:20 | Ekran metni: 'Using Claude Preview: preview eval' ve 'preview screenshot'. (karede: kanıttan) Ekran metni: 'Using Claude Preview: preview eval' ve 'preview screenshot'. |
| Önizlemede seçme ve çizim aracı | yok | ipucu | yok | Önizlemede bölüm seçip veya çizip nota ekleyerek Claude'a düzenleme yaptırma. | 18:36 | if we click the pencil, we can actually draw · kanıt: yok |
| Auto modu | yok | ipucu | yok | Her adımda izin sormadan çalışan mod; varsayılan accept edits. | 10:45 | I've gone ahead and set mine to auto mode |
| Sesle giriş | yok | ipucu | yok | Prompt kutusundaki mikrofonla yazmadan konuşarak prompt verme. | 9:45 | I can actually talk directly into the prompt box · kanıt: yok |
| Hostinger | yok | iş akışı | yok | Hosting ve ücretsiz alan adı alınan, site dosyalarının taşındığı servis. | 19:55 | my favorite platform for doing that is called Hostinger |
| Python | yok | teknik | yok | UI UX Pro Max'in veri arama ve tasarım sistemi script'lerinin çalıştığı dil; python3 kurulu olmalı. | 9:38 | Python required: this skill's scripts use python3 (karede: Claude metni: 'Python required: this skill's scripts use python3'.) |
| Bun | yok | teknik | yok | CLI'nin TypeScript paketini derlemek için gereken çalışma zamanı; kurulu değildi, Claude derlemeyi atlayıp node ile denedi. | 7:12 | The CLI uses a TS bin built with bun (karede: Claude metni: 'The CLI uses a TS bin built with bun'.) |
| Claude Opus | yok | teknik | yok | Claude Code oturumunda çalışan model (Opus 4.8, Medium düşünme seviyesi). | 3:52 | Opus4.8 Medium (karede: Oturum model seçicisinde 'Opus 4.8 Medium' yazıyor.) |
| frontend-design skill'ini global kurma | yok | prompt | yok | Frontend-design skill'in GitHub bağlantısını verip bunu global olarak kurmasını ister. | 5:02 | kaynak: altyazı |
| UI UX Pro Max'i npm ile global kurma | yok | prompt | yok | UI UX Pro Max bağlantısını verip plugin'i npm ile global kurmasını ister; temiz kurulum amaçlı. | 6:02 | kaynak: altyazı |
| İlk siteyi referans görsel ve UI UX Pro Max ile oluşturma | yok | prompt | yok | Austin, Texas'taki Summit Ridge Landscaping için site; referans görseli ilham alsın ama kendi marka, renk ve logolar kullanılsın; belirli bölümler olsun; gereken soruları sorsun. | 9:45 | kaynak: altyazı |
| Hero düzeltmesi ve scroll ile video | yok | prompt | yok | Hero alttan kesiliyor; tüm öğeler ilk ekrana sığsın. Hero görselini, kaydırmayla tetiklenen ve oynayan video dosyasıyla değiştir. | 16:35 | kaynak: altyazı |
| Bölüm sadeleştirme | yok | prompt | yok | Seçilen bölümdeki üç görseli sadeleştir; kırpmadan tek yatay ekip fotoğrafı göster. | 18:36 | kaynak: altyazı |
## Açıklama bağlantıları
- https://createaprowebsite.com/hosting150 — Hostinger ortak markalı indirimli hosting sayfası · aday: evet (Hostinger) · Videoda kullanılan Hostinger'a giden, açıklamadaki yönlendirme kodlu bağlantı; izleyicinin kullanabileceği servis. · sınıf: affiliate
- https://github.com/anthropics/skills/tree/main/skills/frontend-design — frontend-design skill deposu · aday: evet (frontend-design) · Videoda kurulan ve kullanılan skill'in kaynağı. · sınıf: diğer
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — UI UX Pro Max skill deposu · aday: evet (UI UX Pro Max) · Videoda kurulan ve /ui ile çağrılan skill'in kaynağı. · sınıf: diğer
- https://www.udemy.com/course/how-to-create-a-wordpress-website-with-elementor-2021/ — Yazarın WordPress kursu · aday: hayır · Kanal sahibinin kurs tanıtımı; videoda kullanılan araç değil. · sınıf: diğer
- https://youtu.be/88zWBJ8L4y8?si=oCAum_XJZxA_cBl3 — Başka YouTube videosu · aday: hayır · Önerilen diğer video; araç değil. · sınıf: diğer
- https://www.youtube.com/watch?v=Cm0Tnm97mC4 — Başka YouTube videosu · aday: hayır · Önerilen diğer video; araç değil. · sınıf: diğer
- https://www.youtube.com/watch?v=iIC4k0P6Wf8 — Başka YouTube videosu · aday: hayır · Önerilen diğer video; araç değil. · sınıf: diğer
- https://www.youtube.com/watch?v=0_3A0uAkBZ0 — Başka YouTube videosu · aday: hayır · Önerilen diğer video; araç değil. · sınıf: diğer
- https://createaprowebsite.com — Kanal sahibinin sitesi · aday: hayır · Kanalın kendi tanıtım sitesi; araç değil. · sınıf: diğer
- https://www.instagram.com/createaprowebsite/ — Instagram hesabı · aday: hayır · Sosyal medya bağlantısı. · sınıf: diğer
- https://www.facebook.com/createaprowebsite/ — Facebook sayfası · aday: hayır · Sosyal medya bağlantısı. · sınıf: diğer
- http://youtube.com/createaprowebsite?sub_confirmation=1 — Kanal abonelik bağlantısı · aday: hayır · Kanala abone olma bağlantısı; araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Sabit üst gezinme çubuğu: logo, menü bağlantıları, telefon numarası ve 'Get Free Quote' butonu (sticky navigation bar) | Üstte logo, bölümlere giden menü, arama telefonu ve koyu yeşil teklif butonu bulunur; bağlantılar bölümlere kaydırır. (karede: Üstte krem çubuk: logo, Home/Services/About/Our Process/Portfolio/Blog/Contact, (512) 555-0148 ve koyu yeşil 'Get Free Quote' butonu.) | 0:00 | kare |
| Tam ekran hero bölümü: serif başlık, italik altın vurgu, iki CTA butonu (hero section, call to action) | 'Texas Landscapes, Crafted to Last' başlığı, altın 'Get Your Free Estimate' ve çerçeveli 'View Our Work' butonları. (karede: Bahçe fotoğrafı üstünde 'Texas Landscapes, Crafted to Last', altın ve çerçeveli iki buton.) | 0:00 | kare |
| Hero altında yarı saydam istatistik şeridi (stats bar, glassmorphism) | 15+ yıl, 1.200+ proje, %98 memnuniyet, 5.0 Google puanı sayıları hero'nun altında. (karede: Hero altında yarı saydam şerit: 15+ Years in Austin, 1,200+ Projects Completed, 98% Client Satisfaction, 5.0 Google Rated.) | 0:02 | kare |
| Güven çubuğu: sertifika ve ortak rozetleri (trust bar) | Hero'nun altında 'Trusted across Central Texas' ile Austin Chamber, TNLA Certified, BBB, EPA WaterSense, Houzz Pro rozetleri. (karede: Krem alanda 'Trusted across Central Texas · Licensed & Insured' ve beş rozet.) | 0:02 | kare |
| Hizmet kartları ızgarası, hover'da görsel yakınlaştırma (card grid, hover zoom) | Altı hizmet kartı (Landscape Design, Hardscaping & Patios, Outdoor Living vb.) üzerine gelince görsel zoom yapar. (karede: 3x2 kart ızgarası; her kartta fotoğraf, altın ikon, başlık ve kısa açıklama.) | 0:04 | kare |
| Portfolyo bölümü: asimetrik görsel ızgarası (bento / masonry grid) | 'Recent Transformations' başlığı altında bir büyük, dört küçük proje görseli. (karede: 'Recent Transformations' başlığı; solda büyük havuz fotoğrafı, sağda dört küçük görsel.) | 15:10 | kare |
| Önce/Sonra sürükleme çubuklu karşılaştırma (before/after image slider) | Önceki ve sonraki bahçe fotoğrafları sürüklenen çubukla karşılaştırılır; '11 günde tamamlandı' hikâyesi eşlik eder. | 15:10 | altyazı |
| Kaydırmayla oynayan hero videosu (scroll-scrubbed video, scroll-driven playback) | Sayfa aşağı kaydırılırken arka plandaki video ileri, yukarı kaydırılırken geri sarılır. | 17:36 | altyazı |
| Hero'nun ilk ekrana sığdırılması (above the fold düzeni) | Hero öğeleri ve kartlar ilk ekranda görünecek şekilde yeniden düzenlendi. | 17:36 | altyazı |
| Kaydırınca beliren animasyonlar, mobil menü, azaltılmış hareket desteği (reveal-on-scroll, hamburger menu, prefers-reduced-motion) | Claude özetinde: tam duyarlı, mobil menü, scroll'da beliren öğeler, klavye erişimi. (karede: Ekran metni: 'fully responsive (mobile menu, reveal-on-scroll animations, prefers-reduced-motion respected, keyboard-accessible)'.) | 13:48 | kare |
| Bölümlere giden çapa menüsü (anchor navigation, smooth scroll) | Üstteki menü bağlantıları ve teklif butonu ilgili bölüme götürür. | 14:49 | altyazı |
| 4 adımlı süreç bölümü ve yorumlar bölümü (process steps, testimonials) | 'Our Process' dört adım gösterir; ayrıca müşteri yorumları, yer tutucu blog ve teklif formu bölümleri var. | 11:46 | altyazı |
| Ekibin yatay tek görselle gösterilmesi (full-width image, uncropped) | Üç görsellik kolaj yerine kırpılmamış tek yatay ekip fotoğrafı konuldu. (karede: Ekran metni: 'I'll replace the three-image collage with just the crew photo shown full-width and uncropped.') | 19:26 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| install this skill globally: https://github.com/anthropics/skills/tree/main/skills/frontend-design | Claude'a frontend-design skill'ini ~/.claude/skills/ altına global kurdurur. | 5:02 | altyazı |
| install this plugin globally using npm: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | Claude'a UI UX Pro Max'i npm yoluyla global kurdurur. | 6:02 | altyazı |
| ls -la ~/.claude/skills/ | Global skill dizininin var olup olmadığını kontrol eder (Claude çalıştırdı). (karede: Ekran metni: 'ls -la ~/.claude/skills/ 2>/dev/null && echo "---EXISTS---"'; which git.) | 6:02 | kare |
| cd /tmp && rm -rf uiux-check && git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git uiux-check | UI UX Pro Max deposunu geçici dizine klonlayıp paketleme yöntemini inceler. (karede: İzin kutusunda komut metni görünür: 'cd /tmp && rm -rf uiux-check && git clone --depth 1 ...'.) | 7:00 | kare |
| uipro init --ai claude | UI UX Pro Max skill'ini Claude için başlatır/kurar (README'de gösterilir). (karede: README ekran görüntüsünde '$ uipro init --ai claude' komut satırı.) | 6:16 | kare |
| uipro init --ai claude --global | Skill'i ~/.claude/skills/ altına global kurar; yalnız repodaki yeni CLI sürümünde var (Claude çalıştırdı). (karede: Ekran metni: 'init --ai claude --global 2>&1 / tail -40'.) | 7:06 | kare |
| npm install -g uipro-cli | uipro-cli'ı global kurmaya çalışır; /usr/local/lib yazılamadığı için başarısız oldu, sonra kullanıcı prefix'i ile kuruldu. (karede: Ekran metni: 'Ran Install uipro-cli globally via npm'; npm prefix ~/.npm-global.) | 7:18 | kare |
| /ui-ux-pro-max | Sohbet kutusunda '/ui' yazıp seçilen slash komutu; UI UX Pro Max skill'ini bu prompt için çağırır. | 9:06 | altyazı |
| ls -la ~/.claude/skills/ 2>/dev/null && echo '--EXISTS--' // echo '--NO SKILLS DIR--'; which git | Global skills klasörünün varlığını ve git'in kurulu olup olmadığını kontrol eder (Claude çalıştırdı). (karede: Claude Code izin penceresi: 'Allow Claude to run Check global skills dir and git?' ve komut satırı.) | 6:02 | kare |
| npm prefix → ~/.npm-global | npm global kurulum klasörünü kullanıcıya yazılabilir yola taşır; sudo gerekmez. Tam komut ekranda okunamadı. (karede: Claude metni: 'npm prefix ⇒ ~/.npm-global (user-writable, no sudo needed)'.) | 9:22 | kare |
| python3 --version | Python 3'ün kurulu olup olmadığını kontrol eder (skill script'leri için). (karede: Claude metni: 'You have it if python3 --version works'.) | 9:38 | kare |
| source ~/.bash_profile | PATH değişikliğini açık olan diğer terminallere uygular. (karede: Claude metni: 'For other open terminals, run source ~/.bash_profile'.) | 9:32 | kare |
| /ui | Sohbette UI UX Pro Max skill'ini seçer (slash komutu). (karede: Komut kutusunda '/ui' yazılı; açılır listede ui-ux-pro-max ilk sırada.) | 9:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ücretsiz plan Claude Code içermez; Pro plan yaklaşık 17 $/ay ve Code, Design, Cowork dahildir. | 1:09 | sayısal |
| Skill'ler kurulmazsa jenerik, sıkıcı yapay zekâ siteleri çıkar; frontend-design daha yaratıcı font ve yerleşim seçtirir. | 5:02 | özellik |
| UI UX Pro Max'in README'sinde 57 UI stili, 95 renk paleti, 56 font eşleşmesi görünür. | 6:16 | sayısal |
| Tek prompttan çıkan ilk taslak, sıfırdan yapmaktan çok daha hızlı; yaklaşık 10-15 dakika sürdü. | 15:50 | karşılaştırma |
| Prompt'a 'bana soru sor' eklemek Claude'un eksik bilgiyi tamamlamasını sağlar. | 9:45 | öneri |
| Premium plan 2,69 $/ay, Business 3,59 $/ay'dan başlar; Business 50 siteye kadar destekler, ödeme/arka uç için önerilir. | 20:56 | sayısal |
| 12 aylık paket, kuponla yaklaşık 160 $ yerine 43 $; ücretsiz alan adı ve iki posta kutusu içerir. | 21:57 | sayısal |
| ZIP yalnız klasörün içeriğinden oluşturulmalı, klasörün kendisinden değil. | 24:07 | öneri |
| Localhost bağlantısı yalnız yerel cihazda çalışır; başkası açamaz. | 19:55 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | fast and easy way to build a beautiful looking website |
| kare 1:12 | Claude Pro planı | Claude Pro | Fiyat tablosu Pro 17 $ |
| kare 1:12 | Claude Cowork / Claude Design | Claude Cowork | Pro listesinde 'Includes Claude Cowork', 'Includes Claude Design' |
| kare 1:12 | Slack/Google bağlayıcıları, Microsoft 365, Outlook | aday değil: konu dışı | Yalnız fiyat tablosu maddeleri |
| konuşma 1:09 | Claude Design | Claude Design | Cloud Design and Cloud Co-work |
| konuşma 2:09 | Higgsfield | Higgsfield | generated all of this media here for the website I'm going to be building |
| kare 2:10 | Higgsfield menüsündeki modeller (Nano Banana, Seedance, Kling, Sora, Veo, FLUX.2, Grok vb.) | aday değil: başka adayın parçası (Higgsfield) | Higgsfield Image/Video menülerinde listeli |
| kare 2:12 | Higgsfield MCP ve Claude Fable 5 | aday değil: başka adayın parçası (Higgsfield) | Ekran metni 'Available on Higgsfield and in Claude via Higgsfield MCP' |
| konuşma 2:58 | Claude Desktop | Claude Desktop | downloaded and installed the Cloud desktop application |
| kare 3:52 | Opus 4.8 Medium | Opus 4.8 | Ekran metni 'Opus4.8 Medium' |
| kare 2:52 | Sonnet 4.6 Low | aday değil: konu dışı | Chat sekmesinde model seçici; kullanılmadı |
| konuşma 3:59 | Trust workspace | aday değil: başka adayın parçası (Claude Code) | Claude Code çalışma alanı güven iletişim kutusu |
| konuşma 4:59 | Skills kavramı | aday değil: genel kavram | skills are basically just pre-written instructions |
| konuşma 5:02 | frontend-design | frontend-design | first skill is called front-end design |
| kare 5:08 | anthropics/skills deposundaki diğer skill'ler (canvas-design, claude-api, skill-creator vb.) | aday değil: konu dışı | GitHub dosya ağacında listeli, kullanılmadı |
| konuşma 6:02 | UI UX Pro Max | UI UX Pro Max | second skill here is called UI UX ProMax skill |
| kare 6:10 | Antigravity, Codex, Cursor, Windsurf, Tailwind CSS | aday değil: başka adayın parçası (UI UX Pro Max) | README dosya ağacı/rozetlerinde, UI UX Pro Max'in desteklediği platformlar |
| kare 6:18 | NextLevelBuilder.io, GoClaw.sh, ClaudeKit.cc, TOSE.sh | aday değil: başka adayın parçası (UI UX Pro Max) | README'de 'Other projects' |
| kare 7:06 | uipro-cli | uipro-cli | Ran Install uipro-cli globally via npm |
| konuşma 6:02 | npm | npm | install this plugin globally again using NPM |
| kare 7:06 | Node.js 24; Bun yok | Node.js | I have node 24 but no bun |
| kare 7:18 | esbuild | esbuild | I'll bundle it with esbuild |
| kare 7:00 | git clone | Git | git clone --depth 1 ... uiux-check |
| kare 7:12 | Python | aday değil: başka adayın parçası (UI UX Pro Max) | Skill betikleri python3 gerektirir |
| konuşma 7:34 | Awwwards | Awwwards | awards.com ... library of award-winning websites |
| kare 7:58 | Locomotive, Immersive Garden, Resn, .monks, Active Theory, Hello Monday, AQuest, Adoratorio | aday değil: başka adayın parçası (Awwwards) | Awwwards Directory'de gezilen ajanslar |
| kare 7:50 | Fauna Robotics sitesi | aday değil: başka adayın parçası (Awwwards) | Site of the Day |
| konuşma 7:34 | Dribbble | Dribbble | dribbble.com ... search bar |
| kare 8:54 | Mobbin reklamı | aday değil: sponsor/reklam | Dribbble sonuçlarında reklam kartı |
| kare 8:28 | Dribbble WELCOME20 indirim afişi | aday değil: sponsor/reklam | Alt banner |
| konuşma 9:45 | Sesle yazma (mikrofon) | Sesle giriş | I can actually talk directly into the prompt box |
| konuşma 10:45 | Auto / accept edits modu | Auto modu | set mine to auto mode |
| konuşma 11:46 | Sorulara cevap (React/Next.js seçeneği, tek HTML) | aday değil: genel kavram | single HTML file seçildi |
| kare 12:32 | Tailwind ile tek index.html | Tailwind CSS | One self-contained index.html with Tailwind |
| kare 12:32 | Netlify, GitHub Pages | aday değil: konu dışı | Yalnız Claude'un barındırma önerisinde |
| kare 13:50 | Playfair Display + Inter | Playfair Display | its excellent typography pick: Playfair Display + Inter |
| kare 13:50 | Inter | Inter | Playfair Display + Inter |
| kare 17:20 | Claude Preview | Claude Preview | Using Claude Preview: preview eval |
| konuşma 17:36 | localhost bağlantısı | aday değil: genel kavram | this localhost link |
| konuşma 18:36 | Kalem ve seç aracı | Önizlemede seçme ve çizim aracı | if we click the pencil, we can actually draw |
| konuşma 19:55 | Hostinger | Hostinger | my favorite platform ... is called Hostinger |
| açıklama | createaprowebsite.com/hosting150 | Hostinger | Açıklamadaki yönlendirme kodlu bağlantı |
| kare 20:28 | 1-Click OpenClaw, Node.js web apps, WordPress, Hostinger Reach | aday değil: başka adayın parçası (Hostinger) | Hostinger plan sayfasındaki özellikler |
| kare 23:12 | Hostinger Kodee onboarding | aday değil: başka adayın parçası (Hostinger) | hPanel URL'sinde kodee-onboarding |
| konuşma 24:07 | archive.zip sıkıştırma | aday değil: genel kavram | right-click and hit compress |
| açıklama | Udemy WordPress kursu | aday değil: konu dışı | Kanal sahibinin kursu |
| açıklama | Diğer YouTube videoları, Instagram, Facebook, kanal bağlantısı | aday değil: konu dışı | Tanıtım bağlantıları |
| açıklama | Anthropic, GitHub | aday değil: başka adayın parçası (frontend-design) | Skill'in yayımlandığı kurum ve barındırma platformu |
| yorum | Divi, Trent Calloway'in içeriği | aday değil: konu dışı | İzleyici yorumlarında geçer |
| linkli sayfa createaprowebsite.com | YouTube video bağlantıları | aday değil: konu dışı | Kanal sahibinin site sayfasında |
| linkli sayfa awwwards.com | preymaker.com, abatable.com, santalarch.com ve benzeri site listeleri | aday değil: başka adayın parçası (Awwwards) | Awwwards sayfasındaki galeri bağlantıları |
| linkli sayfa NextLevelBuilder.io | claudekit.cc, uupm.cc, goclaw.sh, tose.sh, 200lab.io | aday değil: başka adayın parçası (UI UX Pro Max) | Geliştiricinin diğer projeleri |
| sözlük eşleşmesi | Three.js, Stitch, Nuxt, Hermes Agent, context7, claude-mem, Browser Use | aday değil: konu dışı | Bulanık sözlük eşleşmesi; videoda anlatılmadı |
## Kareden okunanlar
- 0:00: Summit Ridge sitesi: 'Texas Landscapes, Crafted to Last', iki CTA butonu, telefon (512) 555-0148, 15+/1.200+/98%/5.0 istatistikleri.
- 1:12: Claude fiyat sayfası: Free 0 $, Pro 17 $ (yıllık indirimli, aylık 20 $), Max 100 $'dan; Pro 'Includes Claude Code', Cowork, Design.
- 2:08: Higgsfield logosu ve ana sayfa menüsü (Supercomputer, MCP & CLI, Cinema Studio vb.).
- 2:10: Higgsfield Image menüsü: Create Image, Canvas, Soul 2.0, Nano Banana Pro, Seedream, FLUX.2 vb.
- 5:08: GitHub anthropics/skills, skills/frontend-design klasörü: LICENSE.txt ve SKILL.md.
- 6:16: nextlevelbuilder/ui-ux-pro-max-skill README'si: v2.5.0, MIT, '$ uipro init --ai claude', 57 UI stili, 95 palet, 56 font eşleşmesi.
- 7:50: Awwwards ana sayfa: 'FAUNA ROBOTICS' Site of the Day.
- 8:00: Awwwards 'Active Theory' profil sayfası.
- 8:44: Dribbble 'landscaping' arama sonuçları: yeşil tonlu peyzaj web tasarımları.
- 9:32: Slash menüsü: ui-ux-pro-max, frontend-design, run-skill-generator, setup-cowork, team-onboarding, btw.
- 24:38: Migration completed: Archive.zip yüklendi, summitridgeatx.com, Platform Other.
## Belirsizlikler
- Altyazıda 'Cloud/CloudCode' yazan yerler Claude/Claude Code olarak yorumlandı.
- 'awards.com' altyazı hatası; ekranda awwwards.com görünüyor.
- Higgsfield menüsündeki modeller (Nano Banana, Seedance, Kling, Sora, Veo, FLUX.2, Grok Imagine, MiniMax vb.) yalnız menüde görünür; hangisiyle görsel/video üretildiği söylenmedi, aday yapılmadı.
- 'Claude Fable 5' ve 'Sonnet 4.6 Low' yalnız OCR/menüde; Sonnet kullanılmadı, aday yapılmadı.
- Netlify ve GitHub Pages yalnız Claude'un önerisinde geçer; kullanılmadı.
- Sözlükteki Three.js, Stitch, Nuxt, Hermes Agent, context7, claude-mem, Browser Use vb. eşleşmeleri bulanık; videoda anlatılmadı.
- Hostinger indirim kodu açıkça söylenmedi; açıklamada affiliate uyarısı var, 'sponsor' ifadesi yok. Kuponun adı altyazıda 'Creator Pro website' olarak bozuk.
- Sabit yorumdaki '10% off' ile videodaki 43 $ fiyatın ilişkisi belirsiz.
- OCR bozuk metinler (ör. 'sumitr1iametx.com') yazım hatası; alan adı summitridgeatx.com.
- Kare listesi 59 zaman damgası içeriyor, ekli görsel 48; kare zamanları yaklaşık eşleştirildi. OCR'dan gelen kanıtlar 'kare' olarak etiketlendi.
- Sitedeki blog bağlantıları yer tutucu; form arka ucu yok (Claude özetinde belirtildi).
## Atlanan segment oranı
0/31 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://createaprowebsite.com/hosting150 | açıklama | açıklama | evet |
| https://github.com/anthropics/skills/tree/main/skills/frontend-design | 5:08 | ekran | evet |
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | 6:12 | ekran | evet |
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git | 7:00 | ekran | hayır |
| https://www.udemy.com/course/how-to-create-a-wordpress-website-with-elementor-2021/ | açıklama | açıklama | hayır |
| https://youtu.be/88zWBJ8L4y8?si=oCAum_XJZxA_cBl3 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=Cm0Tnm97mC4 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=iIC4k0P6Wf8 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=0_3A0uAkBZ0 | açıklama | açıklama | hayır |
| https://createaprowebsite.com | açıklama | açıklama | hayır |
| https://www.instagram.com/createaprowebsite/ | açıklama | açıklama | hayır |
| https://www.facebook.com/createaprowebsite/ | açıklama | açıklama | hayır |
| http://youtube.com/createaprowebsite?sub_confirmation=1 | açıklama | açıklama | hayır |
| cloud.com | 1:01 | ses | evet |
| awwwards.com | 7:50 | ekran | evet |
| awwwards.com/directory/ | 7:56 | ekran | hayır |
| awwwards.com/active_theory/ | 8:02 | ekran | hayır |
| activetheory.net | 8:00 | ekran | hayır |
| dribbble.com | 7:34 | ses | evet |
| dribbble.com/search/landscaping | 8:44 | ekran | hayır |
| dribbble.com/shots/26673502-Landscaping-Lawn-Care-Business-Website-Design | 9:06 | ekran | hayır |
| createaprowebsite.com/hosting150 | 19:55 | ses | evet |
| hostinger.com/recommended/createaprowebsite-hp?utm_medium=affiliate&utm_source=aff108612&utm_campaign=519#pricing | 20:40 | ekran | evet |
| cart.hostinger.com/pay/094de70d-982d-4a3c-9b4c-a40ffdad7a8d | 21:40 | ekran | evet |
| auth.hostinger.com/register | 22:46 | ekran | evet |
| hpanel.hostinger.com/migrations-onboarding/.../upload-backups | 24:00 | ekran | evet |
| summitridgeatx.com | 0:50 | ekran | hayır |
| https://createaprowebsite.com/hosting150 (sabit yorum) | açıklama | yorum | evet |
| NextLevelBuilder.io | 6:18 | ekran | hayır |
| claudekit.cc | 6:18 | ekran | hayır |
| GoClaw.sh | 6:18 | ekran | hayır |
| TOSE.sh | 6:18 | ekran | hayır |
| awards.com | 7:34 | ses | evet |
| refokus.com | 7:56 | ekran | hayır |
| immersive-g.com | 7:58 | ekran | hayır |
| monks.com | 7:58 | ekran | hayır |
| hellomonday.com | 8:00 | ekran | hayır |
| adoratorio.com | 8:00 | ekran | hayır |
| activetheory.net/work | 8:10 | ekran | hayır |
| ATX.com | 19:55 | ses | hayır |
| Landscaping.com | 19:55 | ses | hayır |
| www.createaprowebsite.com/hosting150 | 20:24 | ekran | hayır |
| hostinger.com/recommended/createaprowebsite-hp (utm parametreleri kısaltıldı) | 20:40 | ekran | evet |
| www.yourwebsite.com | 20:56 | ses | hayır |
| cart.hostinger.com/pay/<sipariş> | 21:40 | ekran | evet |
| hostinger.com | 21:40 | ekran | evet |
| auth.hostinger.com/register (yönlendirme parametreleri kısaltıldı) | 22:46 | ekran | evet |
| cart.hostinger.com/pay/<sipariş>/checkout | 22:56 | ekran | evet |
| gmail.com | 22:56 | ekran | hayır |
| cart.hostinger.com/pay/<sipariş>/success | 23:08 | ekran | evet |
| hpanel.hostinger.com/onboarding-V2/<hesap>/kodee-onboarding | 23:12 | ekran | evet |
| hpanel.hostinger.com/migrations-onboarding/<alan>/method-select | 23:22 | ekran | evet |
| hpanel.hostinger.com/migrations-onboarding/<alan>/select-domain | 23:28 | ekran | evet |
| hpanel.hostinger.com/add-domain/... (kayıt sayfası, kısaltıldı) | 23:50 | ekran | evet |
| hpanel.hostinger.com/migrations-onboarding/summitridgeatx.com/<hesap>/upload-backups | 24:00 | ekran | evet |
| hpanel.hostinger.com/migrations-onboarding/summitridgeatx.com/<hesap>/summary-v2 | 25:08 | ekran | evet |
| hpanel.hostinger.com/migrations-onboarding/summitridgeatx.com/<hesap>/setup | 25:16 | ekran | evet |
## İş akışı
- 1. adım — Claude Pro planına geçilir, masaüstü uygulaması kurulur ve Higgsfield ile görsel ve hero videosu üretilir. — araçlar: Claude Pro, Claude Desktop, Higgsfield
- 2. adım — Masaüstünde proje klasörü açılıp Media klasörü (logo, görseller, video) içine konur. — araçlar: Finder
- 3. adım — Code sekmesinde yeni oturum başlatılır, klasör açılıp çalışma alanına güvenilir. — araçlar: Claude Code
- 4. adım — frontend-design skill'i bağlantıyla global kurulur. — araçlar: Claude Code, frontend-design, Git
- 5. adım — UI UX Pro Max npm yoluyla kurulur; izinler verilir, npm prefix ve esbuild/Node ile sorunlar aşılır. — araçlar: Claude Code, UI UX Pro Max, uipro-cli, npm, Node.js, esbuild
- 6. adım — Uygulama yeniden başlatılarak skill'lerin yüklenmesi sağlanır. — araçlar: Claude Desktop
- 7. adım — İlham için siteler gezilir, Dribbble'da 'landscaping' aranır ve seçilen tasarımın ekran görüntüsü alınır. — araçlar: Awwwards, Dribbble
- 8. adım — Görsel yapıştırılır, /ui-ux-pro-max çağrılır ve sesle/yazıyla ana prompt verilir (auto modu). — araçlar: Claude Code, UI UX Pro Max
- 9. adım — Claude'un sorularına (marka, bölümler, tek HTML, hizmetler) cevap verilir. — araçlar: Claude Code
- 10. adım — Claude logoyu ve renkleri okur, tasarım sistemi üretir, Playfair Display + Inter ile index.html'i kurar. — araçlar: Claude Code, Opus 4.8, Playfair Display, Inter, Tailwind CSS
- 11. adım — Önizlemede site incelenir; hero kesilmesi ve yer tutucular fark edilir. — araçlar: Claude Preview
- 12. adım — Hero düzeltme ve scroll ile oynayan video promptu verilir, önizleme yenilenip test edilir. — araçlar: Claude Code, Claude Preview
- 13. adım — Localhost bağlantısıyla site tarayıcıda test edilir. — araçlar: Claude Code
- 14. adım — Seçme aracıyla bölüm işaretlenip üç görsel tek ekip fotoğrafına indirilir. — araçlar: Claude Preview, Claude Code
- 15. adım — Hostinger'da plan ve 12 ay seçilir, hesap açılıp ödeme yapılır. — araçlar: Hostinger
- 16. adım — 'Migrate existing site' ve yedek yükleme seçilir, ücretsiz alan adı summitridgeatx.com alınır. — araçlar: Hostinger
- 17. adım — Proje klasörünün içeriği archive.zip yapılıp Hostinger'a yüklenir, geçiş tamamlanıp site canlıda açılır. — araçlar: Hostinger, Finder
## Promptlar
- frontend-design skill'ini global kurma — Frontend-design skill'in GitHub bağlantısını verip bunu global olarak kurmasını ister.
- UI UX Pro Max'i npm ile global kurma — UI UX Pro Max bağlantısını verip plugin'i npm ile global kurmasını ister; temiz kurulum amaçlı.
- İlk siteyi referans görsel ve UI UX Pro Max ile oluşturma — Austin, Texas'taki Summit Ridge Landscaping için site; referans görseli ilham alsın ama kendi marka, renk ve logolar kullanılsın; belirli bölümler olsun; gereken soruları sorsun.
- Hero düzeltmesi ve scroll ile video — Hero alttan kesiliyor; tüm öğeler ilk ekrana sığsın. Hero görselini, kaydırmayla tetiklenen ve oynayan video dosyasıyla değiştir.
- Bölüm sadeleştirme — Seçilen bölümdeki üç görseli sadeleştir; kırpmadan tek yatay ekip fotoğrafı göster.
ikinci göz KAPALI: --ikinci-goz yok
