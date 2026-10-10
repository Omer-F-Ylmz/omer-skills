# I Fully Automated My Video Editing Using Claude Code (Full Walkthrough)
## Künye
I Fully Automated My Video Editing Using Claude Code (Full Walkthrough) · Christian Peverelli · süre: 16:58 · en-orig · https://youtu.be/HzXD4GVqXwM · şema 2
motor: parti 2026-10-10-short-7 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 70657 tk · claude-haiku-5-5: claude-haiku-5-5 · 124319 tk
## Özet
Christian Peverelli, YouTube videolarını uyurken Claude Code ile kurguladığı sistemi anlatıyor. Claude Code 'koordinatör' (editör) rolünde; Parakeet transkripsiyon, HyperFrames animasyon, Chrome ile araştırma/B-roll, Tella (MCP) ekran kaydı kurgusu, Epidemic Sound (MCP) müzik/ses efekti, FFmpeg ise son kontrol ve render için kullanılıyor. Tüm stil tercihleri ~1.400 satırlık 'youtube-edit' skill dosyasında toplanıyor; zaman damgalı geri bildirim sonrası 'skill'e kaydet' döngüsüyle 36 kurala ulaşmış. Claude masaüstü uygulamasında kurulum (Code sekmesi, Local, klasör, Auto izin, model, Connectors) adım adım gösteriliyor; canlı demoda 2:46'lık ham kayıt ~16 dakikada 31 sn'lik 4K hook'a dönüyor. Maliyet: Claude Max $200/ay (video başına en fazla $24) + Tella ~$2 + Epidemic ~$1 ≈ $27/video; editör maliyeti $250–1.000+ ve teslim 3–7 gün karşısında aynı gün yayın. Skill ücretsiz toplulukta paylaşılıyor.
## Bölümler
- 0:00 Hook: uyurken kurgulanan video ve vaat
- 0:35 Editör rolü: Claude Code (koordinatör)
- 1:30 Transkripsiyoncu: Parakeet
- 2:04 Animatör: HyperFrames
- 2:50 Araştırmacı: Chrome ile B-roll
- 3:40 Ekran editörü: Tella + MCP
- 4:07 Ses tasarımcısı: Epidemic Sound
- 4:55 Bitirici: FFmpeg ve skill kavramı
- 5:55 Kurulum: Claude indirme, plan, Code sekmesi
- 6:55 Local, klasör, Auto izin ve model ayarı
- 8:02 Kurulum promptu ve Connectors (Tella, Epidemic, HyperFrames)
- 9:12 Skill kaydetme ve stil öğretme döngüsü
- 11:20 Canlı demo: ham hook'u skill ile kurgulatma
- 13:16 V1 sonucu, düzeltme notları ve skill'e öğretme
- 14:20 Tam video akışı ve 'ben yönetmenim'
- 15:00 Maliyet dökümü ve tasarruf
- 16:20 Ücretsiz skill ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Kurgu sisteminin koordinatörü; yerelde dosyalara erişir, araçları çalıştırır, çıktıyı klasöre koyar | 1:01 | Claude Code can work locally, which means that it actually uses my computer |
| Claude | yok | CLI | yok | Masaüstü uygulaması; içindeki Code sekmesinde sistem kuruldu ve çalıştırıldı | 6:04 | Claude masaüstü uygulaması 'Welcome back, Christian' ekranı, Code sekmesi (karede: Claude uygulaması: sol menüde New/Projects/Artifacts/Routines/Customize, altta Local, Claude Code, phase-0-brain, Opus 5.5) |
| Opus 5.5 | yok | teknik | yok | Claude Code oturumunda seçili ana model; sunucunun içinde çalıştığı yapay zekâ | 6:04 | Giriş kutusunun altında model seçici 'Opus 5.5 High' (karede: Sağ altta 'Opus 5.5 High' yazıyor) |
| Parakeet | yok | CLI | yok | NVIDIA'nın ücretsiz transkripsiyon aracı; zaman damgalı metin üretir | 1:01 | the tool that does that is called Parakeet. It's completely free tool |
| HyperFrames | yok | CLI | https://github.com/heygen-com/hyperframes | HeyGen'in ücretsiz aracı; HTML olarak yazılan animasyonu 4K videoya render eder | 2:04 | GitHub sayfasında 'Write HTML. Render video. Built for agents.' görülüyor (karede: github.com/heygen-com/hyperframes sayfası: HeyGen HyperFrames logosu, npm v0.8.99, Apache 2.0, node >=22) |
| Google Chrome | yok | teknik | yok | Araştırmacı rolü: Claude tarayıcıdan ekran görüntüsü/kaydırma videosu alır, satır vurgular, yakınlaştırır | 3:05 | I use Google Chrome and then Claude is able to actually use the browser |
| Tella | yok | MCP | yok | Yüz ve ekranı birlikte kaydeden araç; MCP bağlayıcısıyla kesme, zoom, düzen Claude Code'dan yapılır | 3:40 | Connectors aramasında 'tella' sonucu ve yeşil bağlı işareti (karede: Customize > Connectors'ta Tella kartı 'Edit, polish, and publish your Tella videos by chatting with Claude' ve yeşil onay) |
| Epidemic Sound | yok | MCP | yok | Müzik ve ses efekti kaynağı; Claude'a bağlanır, ses arar; tercihler öğretilir | 8:34 | Bağlayıcı kartı ve 'Epidemic Sound is connected' ipucu (karede: Connectors aramasında 'Epidemic Sound Community – Pro music and sound effects' kartı, yeşil onay, 'Epidemic Sound is connected' balonu) |
| FFmpeg | yok | CLI | yok | Bitirici: kesme, siyah kare ve ses senkronu kontrolü, render | 5:08 | Kontrol listesi: renk etiketi, bitrate, süre, senkron, siyah kare PASS (karede: Kontrol listesi: Colour tags BT.709, Video bitrate 40 Mb/s or more, Duration, Video vs audio in sync, Black frames none — hepsi PASS) |
| youtube-edit | yok | skill | yok | Kullanıcının kurgu stilini (renk, font, animasyon, ses) içeren ~1.400 satırlık, 36 kurallı skill | 5:08 | 'WeAreNoCode YouTube Editor' SKILL.md sayfası (karede: youtube-edit/SKILL.md: 'Turns a flat cut into a finished, on-brand video… Everything runs locally through HyperFrames (Chrome + FFmpeg)') |
| After Effects | yok | teknik | yok | Eski dünyada animasyon için kullanılan araç; HyperFrames'in karşısında anılıyor | 2:16 | Altyazı 'The old world: After Effects' (karede: Konuşmacının altında 'The old world: After Effects' yazısı) |
| Claude Code Local modu | yok | ipucu | yok | Oturumu Local seçerek bilgisayarın dosya ve programlarını kullandırmak | 6:55 | Local/Cloud/Remote Control/SSH menüsünde Local seçili · kanıt: kare (karede: Menü: Local (işaretli), Cloud, Remote Control, SSH) |
| Auto izin modu | yok | ipucu | yok | Her adımda onay istememesi için izin modunu Auto yapmak | 7:12 | Mod menüsünde Auto seçili · kanıt: kare (karede: Mode menüsü: Auto (işaretli), Manual, Accept edits, Plan, Bypass permissions) |
| Connectors | yok | iş akışı | yok | Customize > Connectors'tan Tella, Epidemic Sound, HyperFrames bağlama | 8:22 | Customize ekranında Connectors sekmesi ve arama (karede: Customize: Skills / Connectors / Plugins sekmeleri, Yours/Discover, arama ikonu) |
| Skill'e geri bildirim kaydetme | yok | ipucu | yok | Her düzeltmeden sonra Claude'a öğrendiklerini skill'e kaydettirmek | 10:13 | you tell it to save what it's learned to the actual skill itself · kanıt: yok |
| OpenAI dots | yok | teknik | yok | OpenAI'ın sürekli çalışan AI ajanı ürünü; videoda B-roll içeriği olarak gösteriliyor, sistemin parçası değil. | 3:24 | openai.com/index/introducing-dots sayfasında dots tanıtım metni. · kanıt: kare (karede: openai.com/index/introducing-dots sayfası; başlık 'Introducing dots', metin 'Inside OpenAI, we're getting a glimpse of what work looks like...'.) |
| Kurgu sistemini kurdurmak | yok | prompt | yok | Claude'dan Hyperframes, FFmpeg, Tella ve Epidemic Sound kullanan bir video kurgu sistemi kurmasını ve adım adım kurulumu anlatmasını ister. | 8:22 | kaynak: kare |
| Sistemi skill olarak kalıcılaştırmak | yok | prompt | yok | Araçları kurduktan sonra sistemi bilgisayarda skill olarak kaydetmesini, sonra yeni oturumda test etmeyi önerir. | 9:12 | kaynak: altyazı |
| Ham hook'u skill ile otomatik kurgulamak | yok | prompt | yok | Kullanıcı youtube editing skill'i ile ham hook'u kurgulamasını ister; 'zoom' denince zoom, ses efekti denince efekt, animasyon denince en etkileyici üç animasyonu göstermesini ister. | 12:22 | kaynak: kare |
| V1 sonrası düzeltme: gerilim müziği | yok | prompt | yok | Hook boyunca gerilim hissi veren bir müzik parçası seçip eklemesini ister. | 13:58 | kaynak: altyazı |
| Müzik ekleme düzeltmesi | yok | prompt | yok | Gerilim müzik katmanını hook'un altına eklemesini ister. | 13:36 | kaynak: kare |
| Hata düzeltme geri bildirimi | yok | prompt | yok | Zaman damgalı geri bildirim: 14. saniyede istenmeyen flaş var, çıkarılsın. | 9:36 | kaynak: kare |
| Öğrenileni skill'e kaydettirmek | yok | prompt | yok | Yapılanlardan öğrenip skill'e eklemesini ister. | 14:17 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.skool.com/wearenocode — Skool'daki ücretsiz topluluk; skill burada indirilebiliyor · aday: hayır · Topluluk/CTA sayfası; video içinde araç olarak kullanılmıyor · sınıf: diğer · erişilemez: giriş gerekli (topluluk)
- https://askbond.ai/ — Bond / Outbond AI satış aracı sayfası · aday: hayır · Videoda gösterilmiyor veya kullanılmıyor; açıklamadaki 'AI Sales' başlığına ait · sınıf: diğer
- https://heyreach.io/?via=wearenocode — HeyReach tanıtımı, yönlendirme parametreli · aday: hayır · Videoda kullanılmıyor; yalnız açıklama bağlantısı · sınıf: affiliate
- https://app.emergent.sh/?via=wearenocode — Emergent uygulama oluşturma aracı · aday: hayır · Videoda geçmiyor · sınıf: affiliate
- https://base44.pxf.io/c/4885934/2477538/25619?trafcat=hp — Base44 takip bağlantısı · aday: hayır · Videoda geçmiyor · sınıf: affiliate
- https://dripl.ink/ZkTnR — Dripl kısa bağlantısı · aday: hayır · Videoda geçmiyor; içeriği belirsiz · sınıf: diğer
- https://hostinger.com/wearenocode — Hostinger yönlendirme sayfası · aday: hayır · Videoda kullanılmıyor; reklam/yönlendirme · sınıf: affiliate
- http://hostinger.com/wearenocodeopenclaw — Hostinger OpenClaw yönlendirmesi · aday: hayır · Videoda kullanılmıyor · sınıf: affiliate
- https://bit.ly/wearenocodeyt — Kanal kısa bağlantısı (abone ol) · aday: hayır · Kanal yönlendirmesi, araç değil · sınıf: diğer
- https://www.wearenocode.com — Kanalın web sitesi · aday: hayır · Kendi tanıtım sitesi, araç değil · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Metin vurgulayıcı (highlighter) | Makale paragrafında cümlenin sarı vurgu ile işaretlenmesi (OpenAI makalesi B-roll) (karede: openai.com sayfasında 'Outside OpenAI, an early tester's dot noticed…' cümlesi sarı vurgulu) | 0:10 | kare |
| 3B yüzen tarayıcı penceresi (3D floating browser) | HyperFrames GitHub sayfası perspektifle eğik, koyu gradyan arka plan üstünde (karede: Eğik duran tarayıcı penceresi, github.com/heygen-com/hyperframes, koyu mavi-yeşil arka plan) | 0:12 | kare |
| Akan yollar haritası (flowing paths / node diagram) | Raw clip → Cuts/Sound/Animations → Finished video; parlayan turkuaz çizgiler (karede: Raw clip düğümünden Cuts, Sound, Animations'a parlayan çizgiler, sağda Finished video) | 0:14 | kare |
| Etiket baloncukları (pill tags / callouts) | Konuşmacının yanında 'Watch every clip', 'Cut the rest' gibi etiketler (karede: Yuvarlak köşeli etiketler: Watch every clip, Pick the best, Cut the rest (x işaretli), Place every zoom, Plan the graphics) | 0:56 | kare |
| Kart ızgarası ve bulanıklaştırma (card grid, blur) | 7 rol kartı ızgarası; skill dosyası kartı üstüne biniyor, gradyan arka plan (karede: 01–07 numaralı kartlar (Claude Code, Parakeet, HyperFrames, Google Chrome, Tella, Epidemic Sound, FFmpeg), üstte youtube-edit / SKILL.md çerçevesi) | 5:32 | kare |
| Kontrol listesi PASS rozetleri (checklist with status badges) | Render kalite kontrolleri tek tek işaretleniyor (karede: Colour tags, Video bitrate, Duration, Video vs audio, Black frames satırları, PASS rozetleri) | 5:20 | kare |
| Çoklu pencere perspektif kaydırma (3D carousel / parallax) | Üç tarayıcı penceresi (X, openai.com, X) yan yana, ortadaki kaydırılıyor (karede: Üç pencere: x.com/OpenAI, openai.com/index/introducing-dots, x.com/sama) | 3:20 | kare |
| Kinetik altyazı (animated captions) | Vurgulu renkli kelimelerle alt yazı: 'Edited by AI while I slept' (karede: Altta beyaz yazı, 'while I slept' turkuaz vurgulu) | 0:02 | kare |
| Eğik fiyat kartı (tilted pricing card) | tella.com/pricing sayfası eğik 3B pencerede (karede: tella.com/pricing: Pro $13, Premium $19 per user/month, Monthly/Annual anahtarı) | 15:08 | kare |
| Yığılmış kart/yığın efekti (stacked cards) | '20+ LAUNCHES' etiketli OpenAI Marketplace görseli üst üste kartlar (karede: Yığılmış ekranlar, '20+ LAUNCHES', OpenAI Marketplace sahnesi) | 16:16 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Max planı ayda $200 ve tüm işleri için kullanılıyor | 14:48 | sayısal |
| Son videonun üretimi en fazla $24 token maliyetli | 15:19 | sayısal |
| HyperFrames ve Parakeet ücretsiz | 15:19 | özellik |
| Tella yıllık planda ayda $13, video başına yaklaşık $2 | 15:19 | sayısal |
| Epidemic Sound $9.99; yıllık plan nedeniyle video başına +$1 | 15:19 | sayısal |
| Toplam video başına yaklaşık $27; iyi editör $250–1.000+ | 15:44 | karşılaştırma |
| Teslim süresi 3–7 günden aynı güne indi | 15:44 | karşılaştırma |
| Hook 2:46 ham görüntüden 31 saniyeye indi | 13:16 | sayısal |
| Skill ~1.400 satır ve 36 kural | 5:08 | sayısal |
| Parakeet'in transkripsiyon + render süreci 10–20 dakika sürer | 12:44 | sayısal |
| FFmpeg 20 yıldan fazladır var ve neredeyse her kurgu yazılımının içinde | 5:08 | özellik |
| Claude Code Opus modelinde kurulum yapıp sonra ucuz modele geçilebilir; 20$ plan yeterli | 7:10 | öneri |
| Skill yalnızca ücretsiz toplulukta paylaşılıyor | 16:19 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Edited by my Claude Code system |
| konuşma 1:01 | Claude masaüstü uygulaması | Claude | I personally use the desktop version of Claude |
| konuşma 1:01 | Parakeet | Parakeet | tool … called Parakeet |
| konuşma 1:01 | NVIDIA | aday değil: başka adayın parçası (Parakeet) | built by Nvidia |
| konuşma 2:04 | HyperFrames | HyperFrames | Hyperframes comes in, tool number three |
| konuşma 2:04 | HeyGen | aday değil: başka adayın parçası (HyperFrames) | developed by HeyGen |
| kare 2:16 | After Effects | After Effects | The old world: After Effects |
| konuşma 3:05 | Google Chrome | Google Chrome | I use Google Chrome |
| konuşma 3:40 | Tella | Tella | tool called Tella |
| konuşma 3:40 | MCP | Tella | Tella has a connector called an MCP |
| konuşma 4:07 | Epidemic Sound | Epidemic Sound | sound base called Epidemic Sound |
| konuşma 5:08 | FFmpeg | FFmpeg | This tool is called FFmpeg |
| konuşma 5:08 | skill kavramı / YouTube-Edit | youtube-edit | Mine is called YouTube-Edit |
| kare 0:10 | OpenAI dots makalesi | aday değil: konu dışı | openai.com sayfası B-roll örneği |
| kare 0:10 | Slack | aday değil: konu dışı | Makale metninde geçiyor |
| kare 0:12 | GitHub, npm, Discord rozetleri | aday değil: başka adayın parçası (HyperFrames) | HyperFrames repo sayfası rozetleri |
| kare 1:56 | Doritos ve Lays görselleri | aday değil: konu dışı | Espri amaçlı çip paketleri |
| kare 2:56 | TechCrunch makalesi | aday değil: konu dışı | B-roll örneği |
| kare 3:20 | x.com/OpenAI, x.com/sama tweetleri | aday değil: konu dışı | B-roll örneği |
| kare 3:44 | Kurgu yazılımı (laptop zaman çizelgesi) | aday değil: genel kavram | Stok görüntü, klasik kurgu |
| kare 5:20 | Kalite kontrol listesi (BT.709, bitrate) | FFmpeg | Black frames none PASS |
| konuşma 6:09 | Claude ücretli plan $20 | Claude | upgrade to the $20 plan |
| kare 6:12 | claude.com/download | Claude | Download Claude sayfası |
| kare 7:00 | Local modu | Claude Code Local modu | Local seçili menü |
| kare 7:12 | Auto izin modu | Auto izin modu | Mode menüsü Auto |
| kare 7:20 | Opus 5.5 | Opus 5.5 | Opus 5.5 High seçili |
| kare 7:20 | Fable 5.1, Sonnet 5.5, Haiku 4.5 | aday değil: konu dışı | Yalnız model menüsünde listelenmiş |
| kare 7:36 | Anthropic Sans, OpenDyslexic, JetBrains Mono | aday değil: konu dışı | Yalnız ayar menüsünde |
| kare 7:38 | Remote Control, Git worktree | aday değil: konu dışı | Yalnız ayarlarda görünüyor |
| kare 8:22 | Kurulum promptu | Connectors | Video kurgu sistemi isteği |
| kare 8:30 | Webflow, Era Context, O'Reilly, Viator, Tropic | aday değil: konu dışı | Connectors listesinde |
| kare 8:38 | Descript, Riverside, Epicure, Episto | aday değil: konu dışı | Arama sonucu listesi |
| kare 9:00 | HyperFrames by HeyGen bağlayıcısı | HyperFrames | Connectors kartı |
| konuşma 10:13 | Geri bildirimle skill'e kaydetme | Skill'e geri bildirim kaydetme | save what it's learned to the actual skill |
| konuşma 12:44 | Parakeet ile transkripsiyon | Parakeet | transcribing it using Parakeet |
| kare 12:56 | 16 minutes later önizleme | HyperFrames | auto-edit-hook-v1-4k |
| kare 13:36 | STORYBOARD.md ve PAPER-CUT.md | youtube-edit | Skill çıktı dosyaları |
| kare 14:48 | support.claude.com Max planı | Claude | Max 20x: $200 per month |
| kare 15:08 | tella.com/pricing | Tella | Pro $13 |
| kare 16:16 | OpenAI Marketplace (Adobe, ElevenLabs, Lovable, Vercel vb.) | aday değil: konu dışı | Önceki videonun B-roll'u |
| açıklama | Tella.tv, Claude, Hyperframes başlıkları | Tella | TOOLS listesi |
| açıklama | HeyReach, Emergent, Base44, Hostinger, Bond (askbond.ai) | aday değil: sponsor/reklam | Yönlendirme bağlantıları, videoda geçmiyor |
| açıklama | Skool topluluğu, dripl.ink, bit.ly, wearenocode.com | aday değil: konu dışı | Kanal/topluluk bağlantıları |
| yorum | OBS, Higgsfield, ChatGPT önerileri | aday değil: konu dışı | İzleyici soruları |
| linkli sayfa | Product Hunt, Notion, Outbond YouTube (askbond.ai sayfası) | aday değil: konu dışı | Bond sayfa bağlantıları |
| linkli sayfa | Hostinger örnek siteler (hostingersite.com) | aday değil: sponsor/reklam | Hostinger yönlendirme sayfası içeriği |
| linkli sayfa | chatgpt.com, learn.chatgpt.com, Claude docs, VS Code eklentisi, oss-scanner | aday değil: konu dışı | Linkli sayfalarda geçen bağlantılar, videoda kullanılmıyor |
## Kareden okunanlar
- 0:02: Altyazı 'Edited by AI while I slept'; yan kartlarda youtube-edit / SKILL.md, 'Cost per video', '16 LAUNCHES'
- 0:12: github.com/heygen-com/hyperframes: npm v0.8.99, downloads 1.6M/month, Apache 2.0, node >=22
- 0:56: Etiketler: Watch every clip, Pick the best, Cut the rest, Place every zoom, Plan the graphics
- 2:16: Altyazı 'The old world: After Effects'
- 2:56: techcrunch.com: 'OpenAI takes on Microsoft… ChatGPT's own office suite', Lucas Ropek
- 2:58: @OpenAI tweeti 'Introducing dots, powered by GPT-6 Astra.'
- 3:20: Üç pencere: x.com/OpenAI, openai.com/index/introducing-dots, x.com/sama
- 5:20: Kontrol listesi: BT.709, 40 Mb/s or more, Duration to the frame, in sync, Black frames none, hepsi PASS
- 5:32: 7 rol: Claude Code, Parakeet, HyperFrames, Google Chrome, Tella, Epidemic Sound, FFmpeg
- 6:04: Claude uygulaması: Christian · Max, Opus 5.5 High, Local, Claude Code, phase-0-brain, worktree
- 6:12: claude.com/download: Download Claude, macOS/Windows/Windows (arm64)/Linux
- 6:50: 'Good morning, Christian', Chat/Cowork, Opus 5.5 Medium, 'Type / for skills'
- 7:00: Menü: Local, Cloud, Remote Control, SSH
- 7:12: Mod menüsü: Auto, Manual, Accept edits, Plan, Bypass permissions
- 7:20: Model menüsü: Opus 5.5, Fable 5.1, Sonnet 5.5, Haiku 4.5, More models
- 7:34: Settings > Claude Code: Guest pass, Classify session states, Claude in Chrome kenar çubuğunda
- 7:36: Interface font: Anthropic Sans / System / OpenDyslexic; Code font örnek JetBrains Mono
- 8:22: Prompt: 'Could you please create a video editing system for me?…'
- 8:30: Connectors: Tella 'Edit, polish, and publish your Tella videos', Webflow, Era Context, O'Reilly, Viator, Tropic
- 8:38: 'Epidemic Sound is connected'; Descript, Riverside, Epicure, Episto, Webull, Alpha Vantage
- 8:58: Arama 'hyperframes' → heygen-com/hyperframes, github.com · Write HTML. Render video.
- 9:00: 'HyperFrames by HeyGen' bağlayıcı kartı, 'Build animated slides and motion graphics with HTML'
- 9:06: youtube-edit/SKILL.md: 'Turns a flat cut into a finished, on-brand video… no footage leaves the Mac'
- 11:10: Etiketler: Flash cuts, Dark blue copy (x işaretli)
- 12:22: Sohbet: 'Please use my YouTube editing skill to edit this hook…', C0806.MP4
- 12:56: '16 minutes later'; auto-edit-hook-v1-4k önizlemesi, 'Edited by AI while I slept'
- 13:36: Giriş kutusu 'add the suspense music bed under the hook'; STORYBOARD.md ve PAPER-CUT.md anılıyor
- 14:48: support.claude.com: 'Max 20x: $200 per month'
- 15:08: tella.com/pricing: Pro $13, Premium $19 per user/month, Annual 50% off
- 16:16: '20+ LAUNCHES', OpenAI Marketplace logoları (Adobe, ElevenLabs, Lovable, Vercel, Higgsfield vb.)
## Belirsizlikler
- Anthropic Sans, OpenDyslexic ve JetBrains Mono yalnızca ayarlar menüsünde görünüyor; kullanımı gösterilmiyor.
- Model menüsündeki Fable 5.1, Sonnet 5.5, Haiku 4.5 ve 'More models' yalnız listede; kullanılmıyor.
- Connectors listesindeki Webflow, Descript, Riverside, Cloudflare vb. kartlar yalnız menüde; kullanılmıyor.
- 'İnternette gezinmek için açılacak önemli ayar' (7:40) adıyla söylenmiyor; kenar çubuğundaki 'Claude in Chrome' olması muhtemel, doğrulanmadı.
- Remote Control, worktree, Cloud/SSH seçenekleri menüde görünüyor, kullanılmıyor.
- Videoda hiçbir terminal komutu veya slash komutu çalıştırılmıyor; kurulum Claude arayüzünden ve prompt ile yapılıyor.
- OpenAI dots, GPT-6 Astra, TechCrunch, the-decoder ekranları B-roll örneğidir; araç değil. İçeriklerin gerçekliği doğrulanamaz.
- Claude'un Chrome ile B-roll alması konuşmada anlatılıyor; canlı demoda araştırma adımı gösterilmiyor, önceki işten geldiği belirtiliyor.
- Tella kurgu işlevinin demoda kullanıldığı gösterilmiyor; yalnız bağlayıcı kurulumu görülüyor.
- Yorumlarda geçen araçlar (OBS, Higgsfield, ChatGPT vb.) videoda anlatılmıyor.
## Atlanan segment oranı
0/17 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.skool.com/wearenocode | açıklama | açıklama | hayır |
| https://askbond.ai/ | açıklama | açıklama | hayır |
| https://heyreach.io/?via=wearenocode | açıklama | açıklama | hayır |
| https://app.emergent.sh/?via=wearenocode | açıklama | açıklama | hayır |
| https://base44.pxf.io/c/4885934/2477538/25619?trafcat=hp | açıklama | açıklama | hayır |
| https://dripl.ink/ZkTnR | açıklama | açıklama | hayır |
| https://hostinger.com/wearenocode | açıklama | açıklama | hayır |
| http://hostinger.com/wearenocodeopenclaw | açıklama | açıklama | hayır |
| https://bit.ly/wearenocodeyt | açıklama | açıklama | hayır |
| https://www.wearenocode.com | açıklama | açıklama | hayır |
| https://www.skool.com/wearenocode | açıklama | yorum | hayır |
| openai.com | 0:10 | ekran | hayır |
| github.com/heygen-com/hyperframes | 0:12 | ekran | evet |
| techcrunch.com | 2:56 | ekran | hayır |
| openai.com/index/introducing-dots | 3:20 | ekran | hayır |
| x.com/OpenAI | 3:20 | ekran | hayır |
| claude.com/download | 6:12 | ekran | evet |
| claude.ai/code | 7:38 | ekran | evet |
| claude.ai | 7:38 | ekran | evet |
| KAIKAKU.AI | 8:38 | ekran | hayır |
| github.com | 8:58 | ekran | hayır |
| the-decoder.com | 12:06 | ekran | hayır |
| support.claude.com | 14:48 | ekran | hayır |
| tella.com/pricing | 15:08 | ekran | evet |
## İş akışı
- 1. adım — Claude masaüstü uygulamasını indirip hesap açma, 20$'lık ücretli plana geçme — araçlar: Claude, claude.com/download
- 2. adım — Code sekmesine geçip oturumu Local moda alma — araçlar: Claude Code
- 3. adım — Çalışma klasörünü seçme veya yeni klasör ekleme — araçlar: Claude Code
- 4. adım — İzin modunu Auto'ya alma ve modeli son sürüme (Opus 5.5) ayarlama — araçlar: Claude Code, Opus 5.5
- 5. adım — Ayarlarda Claude Code seçeneklerini gözden geçirme ve tarama özelliğini açma — araçlar: Claude Code
- 6. adım — Kurulum promptunu yazıp Claude'dan sistemi kurmasını isteme — araçlar: Claude Code, HyperFrames, FFmpeg, Tella, Epidemic Sound
- 7. adım — Customize > Connectors'tan Tella ve Epidemic Sound'u bağlama, gerekirse HyperFrames'i bulma — araçlar: Connectors, Tella, Epidemic Sound, HyperFrames
- 8. adım — Sistemi skill olarak kaydettirip yeni oturumda test etme — araçlar: youtube-edit, Claude Code
- 9. adım — Küçük hook klipleriyle zaman damgalı geri bildirim verip stili öğretme (ses efektleri dahil) — araçlar: youtube-edit, Epidemic Sound
- 10. adım — Ham hook'u ekleyip skill'i çağıran promptu yazma — araçlar: Claude Code, youtube-edit
- 11. adım — Claude'un klibi inceleyip Parakeet ile transkribe etmesi ve konuşma parçalarını bulması — araçlar: Parakeet, Claude Code
- 12. adım — Animasyonların HyperFrames ile üretilip render edilmesi, FFmpeg ile 4K kontrol (siyah kare, senkron, loudness) — araçlar: HyperFrames, FFmpeg, Google Chrome
- 13. adım — V1'i izleyip düzeltme notları verme (gerilim müziği ekleme) — araçlar: Claude Code, Epidemic Sound
- 14. adım — Öğrenilenleri skill'e kaydettirme — araçlar: youtube-edit
- 15. adım — Tüm ham görüntüyü (ve Tella dosya adlarını) verip gece boyunca kurgulatma — araçlar: Claude Code, Tella
- 16. adım — Maliyeti hesaplatıp karşılaştırma — araçlar: Claude, Tella, Epidemic Sound
## Promptlar
- Kurgu sistemini kurdurmak — Claude'dan Hyperframes, FFmpeg, Tella ve Epidemic Sound kullanan bir video kurgu sistemi kurmasını ve adım adım kurulumu anlatmasını ister.
- Sistemi skill olarak kalıcılaştırmak — Araçları kurduktan sonra sistemi bilgisayarda skill olarak kaydetmesini, sonra yeni oturumda test etmeyi önerir.
- Ham hook'u skill ile otomatik kurgulamak — Kullanıcı youtube editing skill'i ile ham hook'u kurgulamasını ister; 'zoom' denince zoom, ses efekti denince efekt, animasyon denince en etkileyici üç animasyonu göstermesini ister.
- V1 sonrası düzeltme: gerilim müziği — Hook boyunca gerilim hissi veren bir müzik parçası seçip eklemesini ister.
- Müzik ekleme düzeltmesi — Gerilim müzik katmanını hook'un altına eklemesini ister.
- Hata düzeltme geri bildirimi — Zaman damgalı geri bildirim: 14. saniyede istenmeyen flaş var, çıkarılsın.
- Öğrenileni skill'e kaydettirmek — Yapılanlardan öğrenip skill'e eklemesini ister.
ikinci göz KAPALI: --ikinci-goz yok
