# Turn Claude Code Into a Dev Team in 5 Min
## Künye
Turn Claude Code Into a Dev Team in 5 Min · Yury AI · süre: 0:54 · en-orig · https://youtu.be/pR2nuRcLqbI · şema 2
motor: parti 2026-10-09-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 50577 tk · claude-haiku-5-5: claude-haiku-5-5 · 138600 tk
## Özet
Kısa videoda Claude Code için altı eklenti tanıtılıyor: superpowers (planlama, test, kendi işini gözden geçirme), frontend-design (jenerik AI görünümünü kıran arayüz), code-review (5 paralel ajan), security review (push öncesi güvenlik taraması), claude-mem (oturumlar arası hafıza) ve Garry Tan'in gstack'i (tek eklentide sanal ekip). Açılışta Claude Code Templates sitesi görünür. Açıklamadaki bağlantılar tam liste sayfalarına gider.
## Bölümler
- 0:00 Giriş: beş dakikada altı geliştirici gibi Claude Code
- 0:05 1. superpowers
- 0:14 2. frontend-design
- 0:19 3. code-review
- 0:29 4. security review
- 0:36 5. claude-mem
- 0:43 6. gstack
- 0:51 Kapanış: PLUGINS yorumu
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code Templates | yok | CLI | yok | Claude Code için hazır ajan, komut, hook, MCP ve şablon koleksiyonu sitesi ile npm CLI aracı | 0:00 | Ekranda npm install -g claude-code-templates ve Agents (102) listesi var · kanıt: kare (karede: Koyu site, 'Install CLI Tool (Optional)' kutusu, 'npm install -g claude-code-templates', Agents (102), Commands (159), Settings (51), Hooks (29), MCPs (25), Templates (14)) |
| superpowers | yok | plugin | http://github.com/obra/superpowers | Claude'u koda atlamadan planlamaya, test yazmaya ve kendi işini gözden geçirmeye iten beceri çerçevesi | 0:05 | Claude stops jumping into code and actually plans, writes tests |
| frontend-design | yok | plugin | yok | Anthropic yapımı, jenerik AI görünümünü engelleyen arayüz skill'i | 0:14 | Kills the generic AI look and outputs real production quality UI |
| code-review | yok | plugin | yok | Beş paralel ajanla kod inceleme: CLAUDE.md uyumu, gereksiz kural, hata, git geçmişi | 0:22 | Terminalde claude /code-review ile ajanlar başlatılıyor (karede: Terminal: '$ claude /code-review', 'Spawning review agents', Agent 1 CLAUDE.md compliance, Agent 2 Redundant rule check, Agent 3 Bug detection, Agent 4 Git history context, '4 agents spawned') |
| security-guidance | yok | plugin | yok | Push öncesi kod tabanını güvenlik açıklarına karşı tarayan Anthropic eklentisi | 0:30 | OCR: Installing security-guidance v2.1.0, By Anthropic (Official) (karede: OCR ekran metninde 'anthropics/security-g', 'Installing security-guidance v2.1.0...', '8 vulnerability categories' (kare görseli gönderilmedi)) |
| claude-mem | yok | plugin | http://github.com/nicholasgasior/claude-mem | Oturumlar arası sıkıştırılmış özetlerle proje hafızası sağlar, yerel depolama | 0:36 | OCR: claude /install thedotmack/claude-mem, Local storage (no cloud) (karede: OCR ekran metninde 'Installing claude-mem v3.4.1...', 'AI-compressed session summaries', 'Auto-injects past context' (kare görseli gönderilmedi)) |
| gstack | yok | plugin | http://github.com/garrytan/gstack | Garry Tan'in 23 skill'lik eklentisi: CEO review, mühendislik yöneticisi, release manager, QA | 0:43 | /install garrytan/gstack ve /plan-ceo-review çıktısı (karede: Terminalde '/plan-ceo-review', 'CEO Agent', 'Product Review: Notification Animation Export', Market fit, Priority, Risk, Decision, Pricing) |
| Claude Code | yok | CLI | yok | Eklentilerin çalıştığı ana yapay zekâ kodlama aracı | 0:40 | Terminal karşılama ekranı Claude Code v2.1.62 (karede: Terminal: 'Claude Code v2.1.62', 'Welcome back Lead Gen Man!', 'Opus 4.6 · Claude Max') |
| Claude Opus 4.6 | yok | teknik | yok | Claude Code oturumunda görünen ana model | 0:40 | Karşılama ekranında Opus 4.6 yazıyor · kanıt: kare (karede: Terminalde 'Opus 4.6 · Claude Max' ve '/Users/manthan') |
| git | yok | CLI | yok | Code-review demosunda geçmiş, blame ve diff için kullanılan komutlar | 0:23 | OCR: git log --oneline --since=30d, git blame -L 38,50 src/lib/auth.ts (karede: OCR ekran metninde git log, git blame, git diff, git show komutları (kare görseli gönderilmedi)) |
| GitHub CLI | yok | CLI | yok | Code-review demosunda PR bilgisini çeker | 0:27 | OCR: gh pr view 127 --json body · kanıt: kare (karede: OCR ekran metninde 'gh pr view 127 --json body' (kare görseli gönderilmedi)) |
| npm | yok | CLI | yok | Node.js paket yöneticisi; claude-code-templates CLI'sini global kurmak için kullanılır | 0:00 | npm install -g claude-code-templates (karede: Sitede 'npm install -g claude-code-templates' komutu.) |
| Stripe | yok | teknik | yok | Ödeme servisi; incelenen projede Stripe webhook işleyicisi commit mesajında geçer | 0:23 | f48e3b7 feat: add Stripe webhook handler (karede: EKSİK: karede_gorulen (kare gönderildi, karede görülen boş olamaz)) |
| TypeScript | yok | teknik | yok | Kod incelemesinde kullanılan dosyalar TypeScript (.ts) dosyalarıdır (src/lib/auth.ts, utils/parse.ts) | 0:24 | src/lib/auth.ts ve utils/parse.ts dosya yolları (karede: EKSİK: karede_gorulen (kare gönderildi, karede görülen boş olamaz)) |
| Zustand | yok | teknik | yok | React için durum (state) yönetimi kütüphanesi; claude-mem hafızasında projenin kullandığı kütüphane olarak geçer | 0:39 | Project uses Zustand for state management (karede: 'Recalled context:' listesinde 'Project uses Zustand for state management' satırı.) |
| WebGL | yok | teknik | yok | Tarayıcıda 3B/GPU tabanlı grafik API'si; hafızada 'Canvas 2D engine (NOT WebGL)' kararı olarak geçer | 0:39 | Canvas 2D engine (NOT WebGL) (karede: 'Recalled context:' listesinde 'Canvas 2D engine (NOT WebGL)' satırı.) |
| WebCodecs | yok | teknik | yok | Tarayıcı video kodlama/çözme API'si; projede MP4 dışa aktarma için kullanılır, tarayıcı desteği riski not edilir | 0:39 | Export: WebCodecs + Mediabunny muxer (karede: 'Recalled context:' listesinde 'Export: WebCodecs + Mediabunny muxer' satırı; ayrıca /plan-ceo-review çıktısında 'Risk: WebCodecs browser support (~87%)'.) |
| Mediabunny | yok | teknik | yok | Dışa aktarma için kullanılan muxer kütüphanesi (WebCodecs ile birlikte) | 0:39 | Export: WebCodecs + Mediabunny muxer (karede: 'Recalled context:' listesinde 'Export: WebCodecs + Mediabunny muxer' satırı.) |
| frontend-design ile fiyatlandırma sayfası üretmek | yok | prompt | yok | Fiyatlandırma sayfası yap; stil Luxury / Refined seçilir ve frontend-design skill'i devreye girer. | 0:18 | kaynak: kare |
## Açıklama bağlantıları
- https://www.notion.so/6-Claude-Code-Plugins-33a1feb6b92480a4b8dcd76d3ccb2873?source=copy_link — Altı eklentinin tam listesini içeren Notion sayfası · aday: hayır · Liste/referans sayfası; izleyicinin kullanacağı araç bağlantısı değil. Notion yalnız barındırma. · sınıf: diğer
- https://24.online/6-claude-code-plugins/ — Altı Claude Code eklentisinin listesi ve bağlantıları · aday: hayır · Referans liste sayfası; araç değil. Eklentiler zaten kendi adaylarında. · sınıf: diğer
- http://github.com/obra/superpowers — superpowers plugin deposu · aday: evet (superpowers) · Videoda kurulan superpowers aracının deposu · sınıf: diğer
- http://github.com/nicholasgasior/claude-mem — claude-mem deposu (açıklamadaki bağlantı) · aday: evet (claude-mem) · claude-mem aracının alan adı; ancak videodaki kurulum komutu thedotmack/claude-mem kullanıyor, sahiplik çelişkili · sınıf: diğer
- http://github.com/garrytan/gstack — gstack plugin deposu · aday: evet (gstack) · Videoda kurulan gstack aracının deposu · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Adım kartları düzeni (step cards) | Üç numaralı kart: CLI kur, yığını oluştur, kodlamaya başla; kopyala düğmeli komut kutusu (karede: Kare 0:02: 1 Install CLI Tool, 2 Build Your Stack, 3 Start Coding, turuncu 'Copy' düğmesi) | 0:02 | kare |
| Sekmeli tür filtresi ve kategori çipleri (tabs, filter chips) | Agents, Commands, Settings, Hooks, MCPs, Templates sekmeleri ve kategori çipleri (karede: Kare 0:00: type: Agents (102) seçili, category: All, AI Specialists, Database vb.) | 0:00 | kare |
| Piksel/retro başlık yazısı (pixel font heading) | Başlık 'CLAUDE CODE TEMPLATES' pikselli turuncu yazı (karede: Kare 0:01: pikselli büyük başlık 'CLAUDE CODE TE…') | 0:01 | kare |
| Gradyan ışıma çizgisi animasyonu (gradient glow line) | Sayfada hareket eden mavi-mor-turuncu ışıma çizgisi ve kartlar çevresinde renkli çerçeve vurgusu (karede: Kare 0:03: kartların üstünde ve altında renkli çizgiler; kare 0:01'de kıvrımlı gradyan iz) | 0:03 | kare |
| Rozet şeridi (badges) | downloads, GitHub Star ve Open in DeepGraph rozetleri (karede: Kare 0:02: 'downloads 21k', 'Star 4.5k', 'Open in DeepGraph') | 0:02 | kare |
| Koyu tema ve kart ızgarası (dark theme, card grid) | Ajan kartları ızgarası, 'Add New Agent' kartı (karede: Kare 0:00: 'Add New Agent' ve 'Hackathon AI Strategist' kartları) | 0:00 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm install -g claude-code-templates | Claude Code Templates CLI'ını global kurar (karede: Kare 0:00: 'Install CLI Tool (Optional)' altında bu komut ve Copy düğmesi) | 0:00 | kare |
| claude /install obra/superpowers | superpowers eklentisini kurar (karede: OCR ekran metninde 'claude /install obra/superpowers' (kare görseli gönderilmedi)) | 0:10 | kare |
| /superpowers:brainstorm | superpowers beyin fırtınası komutu (karede: OCR ekran metninde '/superpowers:brainstorm') | 0:12 | kare |
| claude /install anthropics/frontend-design | frontend-design skill'ini kurar (ekranda kesik: frontend-de) (karede: OCR ekran metninde 'claude /install anthropics/frontend-de') | 0:17 | kare |
| claude /code-review | Paralel inceleme ajanlarını başlatır (karede: Kare 0:22: '$ claude /code-review', 'Starting code review...') | 0:22 | kare |
| git log --oneline --since=30d | Son 30 günün commit geçmişini listeler (karede: OCR ekran metninde bu komut) | 0:23 | kare |
| git blame -L 38,50 src/lib/auth.ts | auth.ts 38-50. satırların yazarını gösterir (karede: OCR ekran metninde bu komut) | 0:24 | kare |
| gh pr view 127 --json body | PR 127 gövdesini JSON olarak getirir (karede: OCR ekran metninde bu komut) | 0:27 | kare |
| claude /install thedotmack/claude-mem | claude-mem eklentisini kurar (karede: OCR ekran metninde bu komut) | 0:36 | kare |
| /install garrytan/gstack | gstack eklentisini kurar (karede: OCR ekran metninde bu komut ve 'installed successfully!') | 0:43 | kare |
| /plan-ceo-review | gstack CEO ürün incelemesi çalıştırır (karede: Kare 0:46: '> /plan-ceo-review' ve 'CEO Agent') | 0:46 | kare |
| git log --follow --all -- src/lib/auth.ts | Dosyanın yeniden adlandırmalar dahil tüm commit geçmişini listeler | 0:24 | kare |
| git show e91b4fa --stat | Commit'in değiştirdiği dosyaların özetini gösterir | 0:26 | kare |
| git diff 7d02e1c..e91b4fa -- auth.ts | İki commit arasında auth.ts dosyasındaki farkı gösterir (OCR düzeltildi) | 0:26 | kare |
| claude | Claude Code'u terminalde başlatır (karede: Terminalde '% cla...' komutu; altında Claude Code v2.1.62 karşılama kutusu.) | 0:40 | kare |
| claude /install garrytan/gstack | gstack plugin'ini kurar (6 skill, 24 komut ekler) | 0:43 | kare |
| /plan-eng-review | gstack mühendislik planı incelemesini çalıştırır | 0:43 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| superpowers 127.000 GitHub yıldızına sahip | 0:05 | sayısal |
| frontend-design 277.000 kurulum almış ve Anthropic yapımı | 0:14 | sayısal |
| code-review beş ajanı paralel çalıştırır | 0:22 | özellik |
| claude-mem 21.000 yıldız (ekranda 38K+ yazıyor, çelişki) | 0:37 | sayısal |
| gstack tek eklentide 23 skill içerir | 0:43 | sayısal |
| Claude Code'u beş dakikada altı geliştirici ekibine çevirmek mümkün | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | Claude Code Templates sitesi | Claude Code Templates | npm install -g claude-code-templates |
| konuşma 0:05 | superpowers | superpowers | First, superpowers. |
| konuşma 0:14 | front-end design | frontend-design | Second, front-end design. |
| konuşma 0:19 | code review | code-review | Third, code review. |
| konuşma 0:29 | security review | security-guidance | Fourth, security review. |
| konuşma 0:36 | Claude MEM | claude-mem | Fifth, Claude MEM. |
| konuşma 0:43 | gstack | gstack | Sixth, Stack. Built by Garry Tan |
| kare 0:40 | Claude Code | Claude Code | Claude Code v2.1.62 |
| kare 0:40 | Opus 4.6 | Claude Opus 4.6 | Opus 4.6 · Claude Max |
| ekran 0:23 | git komutları | git | git log --oneline --since=30d |
| ekran 0:27 | gh pr view | GitHub CLI | gh pr view 127 --json body |
| ekran 0:23 | Stripe webhook commit | aday değil: başka adayın parçası (code-review) | feat: add Stripe webhook handler commit mesajı |
| ekran 0:38 | Zustand | aday değil: başka adayın parçası (claude-mem) | Project uses Zustand for state management hatırlanan bağlam |
| ekran 0:39 | WebGL / WebCodecs / Mediabunny | aday değil: başka adayın parçası (claude-mem) | Recalled context demo maddeleri |
| ekran 0:01 | Obsidian Ops Team | aday değil: başka adayın parçası (Claude Code Templates) | Site kategori çipi |
| ekran 0:02 | Open in DeepGraph | aday değil: başka adayın parçası (Claude Code Templates) | Sitedeki rozet |
| ekran 0:26 | notifymotion.com | aday değil: başka adayın parçası (code-review) | Demo commit yazarı e-postası |
| açıklama | Notion bağlantısı | aday değil: konu dışı | notion.so liste sayfası |
| açıklama | 24.online liste sayfası | aday değil: konu dışı | 24.online/6-claude-code-plugins |
| açıklama | Instagram yorum kampanyası | aday değil: konu dışı | Comment PLUGINS on my Instagram |
| açıklama | GitHub obra/superpowers sayfası | superpowers | http://github.com/obra/superpowers |
| açıklama | GitHub claude-mem sayfası | claude-mem | http://github.com/nicholasgasior/claude-mem |
| açıklama | GitHub garrytan/gstack sayfası | gstack | http://github.com/garrytan/gstack |
| yorum | Yorumlardaki 'Plug-ins' istekleri | aday değil: konu dışı | Plug-ins! Thank you! |
## Kareden okunanlar
- 0:00: Claude Code Templates sitesi: npm install -g claude-code-templates, Agents (102), Commands (159), Settings (51), Hooks (29), MCPs (25), Templates (14)
- 0:01: Aynı site; downloads 21k, Star 4.5k, 'Open in DeepGraph' rozetleri
- 0:02: Üç adım: Install CLI Tool, Build Your Stack, Start Coding ($ claude)
- 0:03: Kategori çipleri ve adım kartları vurgulu çerçeveyle
- 0:22: $ claude /code-review; Agent 1-4 listesi; 14 changed files; History analyzed (128 commits, 5 authors)
- 0:39: Recalled context: Zustand, Dark mode first, Commit format NM-XXX, Port 8000 (3000 TiltIt), Never push without explicit permission, Canvas 2D (NOT WebGL), Spring physics, WebCodecs + Mediabunny
- 0:40: Claude Code v2.1.62, Welcome back Lead Gen Man!, Opus 4.6 · Claude Max, macOS terminal
- 0:46: /plan-ceo-review, CEO Agent, Product Review: Notification Animation Export, Pricing $29 lifetime, Risk WebCodecs ~87%
## Belirsizlikler
- Altyazıda 'five agents' deniyor, ekranda 4 ajan oluşturuldu görünüyor; sayı tutarsız.
- claude-mem için ses 21.000 yıldız diyor, ekranda 38K+ yazıyor.
- github.com/nicholasgasior/claude-mem ve ekrandaki thedotmack/claude-mem farklı sahipler gösteriyor.
- Security review'un tam eklenti adı: ekranda security-guidance, ses 'security review'.
- Ekran metinlerinin çoğu OCR; 0:00-0:03, 0:22, 0:39, 0:40, 0:46 dışındaki kareler görülmedi.
- Open in DeepGraph rozeti, Zustand, WebGL, WebCodecs, Mediabunny, Stripe, Obsidian gibi öğeler yalnız site menüsü ya da demo içeriği olarak göründü; araç olarak kullanılmadı.
- Altyazıdaki Slack/Codex/Stack vb. sözlük eşleşmeleri bulanık, gerçek anma değil.
- Videoyu sunan kişi demo ekranlarını stok/kurgu gösteriyor olabilir; sürüm numaraları doğrulanamadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.notion.so/6-Claude-Code-Plugins-33a1feb6b92480a4b8dcd76d3ccb2873?source=copy_link | açıklama | açıklama | hayır |
| https://24.online/6-claude-code-plugins/ | açıklama | açıklama | hayır |
| http://github.com/obra/superpowers | açıklama | açıklama | evet |
| http://github.com/nicholasgasior/claude-mem | açıklama | açıklama | evet |
| http://github.com/garrytan/gstack | açıklama | açıklama | evet |
| notifymotion.com | 0:26 | ekran | hayır |
## İş akışı
- 1. adım — Claude Code Templates sitesi ve npm CLI'ı tanıtılır — araçlar: Claude Code Templates
- 2. adım — superpowers kurulur — araçlar: Claude Code, superpowers
- 3. adım — superpowers ile brainstorm, plan ve test akışı gösterilir — araçlar: superpowers
- 4. adım — frontend-design kurulur — araçlar: Claude Code, frontend-design
- 5. adım — Fiyatlandırma sayfası frontend-design ile üretilir — araçlar: frontend-design
- 6. adım — code-review ile dört-beş ajan paralel başlatılır — araçlar: code-review
- 7. adım — Git geçmişi ve PR bilgisi izlenir — araçlar: git, GitHub CLI
- 8. adım — security-guidance kurulur ve riskli kod (eval, os.system) yakalanır — araçlar: security-guidance
- 9. adım — claude-mem kurulur — araçlar: claude-mem
- 10. adım — Yeni oturumda geçmiş bağlam otomatik yüklenir — araçlar: claude-mem, Claude Code
- 11. adım — gstack kurulur — araçlar: gstack
- 12. adım — /plan-ceo-review ile ürün incelemesi alınır — araçlar: gstack, Claude Code
## Promptlar
- frontend-design ile fiyatlandırma sayfası üretmek — Fiyatlandırma sayfası yap; stil Luxury / Refined seçilir ve frontend-design skill'i devreye girer.
