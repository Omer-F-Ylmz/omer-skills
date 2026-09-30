# 10 Claude Code Plugins to 10X Your Projects
## Künye
10 Claude Code Plugins to 10X Your Projects · Chase AI · süre: 17:47 · en-orig · https://youtu.be/OFyECKgWXo8
motor: parti 2026-09-30-uzun-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (5)
## Özet
Chase AI, Claude Code için gerçekten kullandığı 10 aracı sıralıyor: Supabase (MCP yerine CLI öneriyor), Anthropic'in skill-creator skill'i, GSD çerçevesi, NotebookLM-py CLI, Obsidian, Vercel CLI, Playwright CLI, GitHub CLI, Firecrawl CLI ve Excalidraw diagram skill'i. Her araç için neden, nasıl kurulur, nasıl kullanılır ve kullanım senaryosunu anlatıyor. Ana tezi: aynı iş için CLI varsa MCP yerine CLI seçilmeli. Yeni bir CLI kurulunca onu tamamlayan bir skill de eklenmeli.
## Bölümler
- 0:00 Giriş
- 0:55 Supabase
- 6:07 Skill Creator
- 7:55 GSD
- 9:19 NotebookLM
- 10:36 Obsidian
- 11:43 Vercel
- 12:36 Playwright
- 13:53 Github
- 14:39 Firecrawl
- 15:35 Excalidraw
- 17:13 Daha fazla kaynak
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Supabase MCP | yok | MCP | yok | Claude Code'dan doğal dille veritabanı ve kimlik doğrulama işlerini yönetmeyi sağlar. Sunucu yine de CLI lehine önerilmiyor. | 0:55 | Anlatıcı kurulumun tek satır olduğunu ve Claude Code MCP dokümanında bulunduğunu söylüyor. |
| Supabase CLI | yok | CLI | yok | Yerel Supabase yığınını çalıştırır, veritabanı ve auth işlerini terminalden yürütür. Claude Code için MCP'den daha uygun bulunuyor. | 3:29 | Supabase CLI dokümanı: 'supabase init' ve 'supabase start' komutları gösteriliyor. (karede: EKSİK: karede_gorulen (kare gönderildi, karede görülen boş olamaz)) |
| Supabase Claude Code plugin (skill) | yok | plugin | yok | Supabase CLI'nin Claude Code'da doğru kullanılması için marketplace'te bulunan hazır skill. | 5:01 | Supabase'in marketplace'te aranabilen bir Claude Code plugin'i olduğu söyleniyor. |
| skill-creator | yok | skill | yok | Skill oluşturur, mevcut skill'leri geliştirir, A/B testi ve eval ile performansını ölçer. | 6:07 | Anlatıcı bunu on araç arasında en güçlü olarak tanımlıyor; /plugin ile kurulur. |
| GSD (Get Shit Done) | yok | iş akışı | yok | Claude Code üzerinde spec odaklı geliştirme ve bağlam yönetimi sunan orkestrasyon katmanı. Her adımda taze bağlam ve alt ajan kullanır. | 7:55 | Videoda 'Get Done framework' olarak geçiyor; kurulum tek komut, başlatma /gsd new project. |
| NotebookLM-py CLI/skill | yok | CLI | yok | NotebookLM'i Claude Code terminalinden kullanmayı sağlar. Araştırma, video, infografik, slayt, flashcard ve podcast üretimi yapılır. | 9:19 | Resmi API olmamasına rağmen NotebookLM'deki her şeyin terminalden yapılabildiği söyleniyor. |
| Obsidian | yok | iş akışı | yok | Kişisel asistan senaryosunda markdown dosyalarını vault klasöründe tutup Claude Code'u orada açma yöntemi. CLI veya skill gerekmiyor. | 10:36 | Claude Code'a Obsidian kurallarına uymasını söylemek yeterli deniyor. |
| Vercel CLI | yok | CLI | yok | Deployment yönetimini terminalden yapar. Vercel'in sitesindeki skill ile birlikte kullanılır. | 11:43 | Vercel'in skill'i web sitesinde sunduğu ve agent loop'larla deployment durumu kontrolünde kullanılabileceği söyleniyor. |
| Playwright CLI | yok | CLI | yok | Microsoft'un açık kaynak aracıyla tarayıcı otomasyonu, form ve tasarım testi yapar. 'show' komutu ajan panosu sunar. | 12:36 | Skill kurulumu 'playwright-cli install --skills' ile yapılıyor; show komutu headless ajanları gösteriyor. |
| GitHub CLI | yok | CLI | yok | GitHub'da elle yapılan işleri terminalden yapar. Vercel CLI ile kodlamadan deploy'a kadar tek akış kurulabilir. | 13:53 | Kurulum işletim sistemine göre GitHub sayfasında anlatılıyor; skill şart değil. |
| Firecrawl CLI ve skill | yok | CLI | yok | Yapay zekâ ajanlarına uygun çıktı veren web scraping aracı. Komutları scrape, crawl, map ve search. | 14:39 | Tek satırlık kurulum skill'i de içeriyor; web search aracından üstün bulunuyor. |
| Excalidraw diagram skill | yok | skill | yok | Claude Code ile doğal dilden Excalidraw diyagramları üretir. Yaratıcısı Cole Medin. | 15:35 | Repo klonlanıp proje skill dizinine kopyalanarak kurulur. |
| Claude Code'a Supabase CLI'yi kurdurmak. | yok | prompt | yok | Hey, download and install the Supabase CLI tool. | 4:00 | kaynak: altyazı |
| Claude Code'un markdown dosyalarını Obsidian uyumlu üretmesi. | yok | prompt | yok | When we create markdown files, just follow Obsidian conventions. | 11:36 | kaynak: altyazı |
| Vercel CLI kurulumunu Claude Code'a yaptırmak. | yok | prompt | yok | Go ahead and install the Vercel CLI for me. | 11:43 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.skool.com/chase-ai — Chase AI Skool topluluk sayfası · aday: hayır · Araç değil, topluluk ve ürün tanıtımı; araç adayı içermiyor. · erişilemez: Skool topluluğu, giriş/üyelik gerektiriyor
- https://www.skool.com/chase-ai-community — Ücretsiz Chase AI topluluk sayfası · aday: hayır · Topluluk tanıtımı; araç veya repo değil. · erişilemez: Skool topluluğu, giriş gerektiriyor
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Koyu tema hero bölümü: büyük sans-serif başlık, gri alt metin, iki CTA (dolu beyaz ve çerçeveli koyu), altta renkli çizgi ızgarası gradyanı ve üçgen logo. | Vercel ana sayfası hero bölümü: 'Build and deploy on the AI Cloud.' başlığı, 'Start Deploying' ve 'Get a Demo' butonları. (karede: Siyah zeminde 'Build and deploy on the AI Cloud.' başlığı, altında Vercel açıklaması, 'Start Deploying' (beyaz) ve 'Get a Demo' butonları, altta renkli çizgili gradyan.) | 0:27 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /mcp | Claude Code'da bağlı MCP sunucularını listeler; Supabase burada 'connected' görünür. (karede: Terminalde '/mcp' yazılı, 'Manage MCP servers' altında 'supabase · connected' ve iki claude.ai sunucusu 'needs authentication'.) | 2:27 | kare |
| supabase init | Yeni yerel Supabase projesi oluşturur. (karede: Supabase CLI dokümanında '1 supabase init to create a new local project' satırı.) | 3:29 | kare |
| supabase start | Supabase servislerini yerelde başlatır. (karede: Supabase CLI dokümanında '2 supabase start to launch the Supabase services' satırı.) | 3:29 | kare |
| /plugin | Plugin pazarını açar; skill-creator aranıp kurulur. | 7:09 | altyazı |
| /skill-creator | Skill-creator skill'ini doğrudan çağırır. | 7:09 | altyazı |
| /gsd new project | GSD ile yeni proje başlatır ve planlama aşamasını açar. | 8:56 | altyazı |
| notebooklm skill install | Claude Code'a NotebookLM CLI kullanımını öğreten skill'i kurar. | 10:19 | altyazı |
| notebooklm | Tarayıcı açar; NotebookLM hesabına giriş yapılır. | 9:19 | altyazı |
| playwright-cli install --skills | Playwright CLI skill'lerini kurar. | 12:36 | altyazı |
| playwright-cli show | Tarayıcı ajanlarının ne yaptığını gösteren görsel panoyu açar. | 13:36 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Aynı iş için CLI ve MCP varsa CLI seçilmeli; MCP terminal dışında olduğu için ek yük getiriyor. | 4:00 | öneri |
| Yeni bir CLI kurulunca Claude Code'a nasıl kullanılacağını öğreten uygun bir skill de eklenmeli. | 5:01 | öneri |
| Skill-creator ile skill'li ve skill'siz A/B testi yapılabiliyor; önceden karar sezgiye dayanıyordu. | 6:07 | özellik |
| GSD her adımda taze bağlam penceresi ve alt ajan kullanarak bağlam çürümesini azaltıyor. | 7:55 | özellik |
| NotebookLM işleri bu araçla neredeyse ücretsiz olarak Claude Code'a devrediliyor. | 9:19 | özellik |
| Obsidian'ın katkısı kodlama projelerinde değil, kişisel asistan bağlamında büyük. | 10:36 | öneri |
| Firecrawl, Claude Code'un kendi web search aracından bir adım üstün. | 15:35 | karşılaştırma |
| Supabase ücretsiz katmanı cömert; açık kaynak olduğu için yerelde kendi sunucuda da çalıştırılabiliyor. | 0:55 | özellik |
## Kareden okunanlar
- 0:27: Vercel ana sayfası: 'Build and deploy on the AI Cloud.', 'Start Deploying' ve 'Get a Demo' butonları.
- 1:25: github.com/supabase/supabase README sayfası; Apache-2.0 lisansı sekmesi, Watch/Unstar/Fork düğmeleri.
- 2:27: Terminalde '/mcp' çıktısı: 3 sunucu; Project MCPs altında supabase connected, claude.ai Gmail ve Google Calendar needs authentication.
- 3:29: Supabase CLI dokümanı; 'supabase init' ve 'supabase start', macOS/Windows/Linux/npm sekmeleri.
- 5:32: Supabase GitHub README: 'Build in a weekend. Scale to millions.', Hosted Postgres Database ve Authentication and Authorization maddeleri.
## Belirsizlikler
- Kare zamanları (özellikle 0:27'deki Vercel kare) anlatımla uyuşmuyor: Vercel 11:43'te anlatılıyor, kare ise 0:27 olarak etiketli.
- Supabase MCP kurulum komutunun metni videoda okunmuyor, yalnızca 'tek satır' deniyor; yazmadım.
- GSD, altyazıda 'Get Done' geçiyor; gerçek adı büyük olasılıkla 'Get Shit Done', ama videoda doğrulanmıyor.
- Repo URL'leri ekranda okunamadığı için boş bırakıldı.
- Vercel, GitHub, Firecrawl ve NotebookLM kurulum komutlarının metni okunmuyor, yalnızca 'bu komut' deniyor.
- Altyazıda 'Superbase' yazılışı otomatik çeviri hatası; doğrusu Supabase.
## Atlanan segment oranı
0/23 (paket tam okuma, motor)
