# Comment "PLUGIN" to get this Claude Code Setup plugin to optimize your setup.
## Künye
Comment "PLUGIN" to get this Claude Code Setup plugin to optimize your setup. · nick_saraev · süre: 0:33 · ? · https://www.instagram.com/reel/DaagbUMP8Tg/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-12-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 14357 tk · claude-haiku-5-5: claude-haiku-5-5 · 44396 tk
## Özet
Kısa reel: Nick Saraev, çoğu kişinin Claude Code'u yanlış kullandığını, alakasız plugin ve skill kurduğunu söylüyor. Anthropic'in resmi, ücretsiz 'Claude Code Setup' plugin'ini tanıtıyor: bir kez kurulur, tek komutla kod tabanını tarar ve projeye uygun hook, skill, subagent ve MCP sunucusu önerir. Yorumlara 'PLUGIN' yazanlara doğrudan gönderileceğini söylüyor.
## Bölümler
- 0:00 Claude Code'u yanlış kullanma sorunu
- 0:06 Token/limit hatası ve büyük hata vurgusu
- 0:09 Claude Code Setup plugin'i tanıtımı
- 0:14 claude-plugins-official GitHub deposu
- 0:20 MCP sunucusu önerisi (Supabase) örneği
- 0:23 Güvenlik/hata için review subagent örneği
- 0:30 Yorum yapma çağrısı (PLUGIN)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code Setup | yok | plugin | yok | Kod tabanını tarayıp uygun hook, skill, subagent ve MCP önerileri sunan resmi Anthropic plugin'i | 0:09 | Ekranda 'Analyze codebases and recommend tailored Claude Code automations' ve 'Claude Code Set' görünüyor; ses de adı söylüyor. (karede: kanıttan) Ekranda 'Analyze codebases and recommend tailored Claude Code automations' ve 'Claude Code Set' görünüyor; ses de adı söylüyor. |
| Claude Code | yok | CLI | yok | Anthropic'in terminal tabanlı kodlama aracı; videoda sunucunun içinde çalıştığı ana araç | 0:01 | Terminalde Claude Code arayüzü, /compact ve 'Claude Code V2.1.81' görünüyor. (karede: Terminal penceresi, 'Welcome back Lewis!' ve /compact çıktısı) |
| Claude Opus 4.6 | yok | teknik | yok | Terminal arayüzünde görünen model | 0:01 | OCR: 'Opus 4.6 - Claude Max'. · kanıt: kare (karede: Terminal başlığında model adı) |
| claude-plugins-official | yok | plugin | yok | Anthropic'in resmi plugin deposu; recommender referans dosyaları burada | 0:14 | OCR: 'anthropics / claude-plugins-official Public' ve hooks-patterns.md, mcp-servers.md. |
| Hooks | yok | teknik | yok | Claude Code otomasyon kancaları; plugin'in önerdiği türlerden | 0:09 | Konuşmada 'the best hooks' geçiyor. |
| Skills | yok | skill | yok | Claude Code skill'leri; plugin tarafından önerilir | 0:09 | Konuşmada 'the best skills' geçiyor. |
| Subagents | yok | teknik | yok | Güvenlik sorunu için review subagent önerisi | 0:23 | 'recommend a review subagent to catch it'; ekranda 'sub-agent' 0:25. |
| MCP | yok | MCP | yok | Projeye uygun MCP sunucuları önerilir | 0:09 | 'best MCP servers' söyleniyor. |
| Supabase | yok | MCP | yok | MCP ile bağlanılan veritabanı örneği | 0:20 | OCR: 'Authentication successful. Connected to supabase.' (karede: kanıttan) OCR: 'Authentication successful. Connected to supabase.' |
| Postgres | yok | MCP | yok | Açıklamada örnek MCP sunucusu | açıklama | Açıklamada 'Postgres, Vercel' geçiyor. |
| Vercel | yok | MCP | yok | Açıklamada örnek MCP sunucusu | açıklama | Açıklamada 'Postgres, Vercel' geçiyor. |
| Convex | yok | MCP | yok | Recommender'a eklenen veritabanı seçeneği | 0:15 | OCR: 'recommender: add Convex to datab...'. |
| TypeScript | yok | teknik | yok | Örnek projedeki kod dili (upload.ts, Chart.tsx) | 0:01 | OCR: 'src/middleware/upload.ts'. |
| /compact | yok | ipucu | yok | Konuşmayı sıkıştırma komutu | 0:01 | OCR: '/compact' ve 'Conversation compacted'. |
| React | yok | teknik | yok | Frontend kütüphanesi; checkout ekranındaki 'unique key prop' uyarısı React uyarı biçimine benziyor (kesin doğrulanamadı). | 0:23 | Each child in a list should have a unique "key" prop (karede: kanıttan) Each child in a list should have a unique "key" prop |
| CLAUDE.md | yok | teknik | yok | Claude Code'un proje talimat dosyası; /init komutuyla oluşturulması öneriliyor. | 0:01 | Run /init to create a CLAUDE.md file (karede: kanıttan) Run /init to create a CLAUDE.md file |
| Kod tabanı taraması | yok | prompt | yok | Kullanıcı Claude'dan tüm kod tabanını taramasını istiyor (scan my entire...). | 0:12 | kaynak: altyazı |
| Supabase MCP testi | yok | prompt | yok | Supabase'teki en son 5 veritabanı kaydını getirmesi isteniyor. | 0:20 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Checkout sayfası hata katmanı (error overlay) | Ödeme formu üzerinde 'Unhandled Runtime Error' TypeError penceresi gösteriliyor (karede: CHECKOUT sayfası, Shipping Information, Order Summary ve alt kısımda kırmızı hata kutusu) | 0:23 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /compact | Konuşma geçmişini sıkıştırır (karede: Terminalde '/compact' ve 'Conversation compacted') | 0:01 | kare |
| claude connect --plugin random | Plugin kayıt defterine (plugin registry) bağlanma komutu; OCR'da 'piugin' okunduğu için metin tam doğrulanamadı. (karede: Terminalde 'claude connect --piugin random' satırı ve 'Establishing connection to plugin registry' yazısı (OCR).) | 0:02 | kare |
| /init | Proje için CLAUDE.md dosyasını oluşturur. (karede: Terminalde 'Run /init to create a CLAUDE.md file' yazısı.) | 0:01 | kare |
| ctrl+o | Sıkıştırılmış konuşmanın tam geçmişini/özetini gösterir. (karede: Ekranda 'Conversation compacted (ctrl+o for history)' ipucu (OCR).) | 0:01 | kare |
| /effort | Model çaba (effort) seviyesini ayarlar; ekranda 'medium' seçili. (karede: Alt satırda 'medium · /effort' yazısı (OCR).) | 0:13 | kare |
| shift+tab | Düzenleme kabul modunu (accept edits) değiştirir. (karede: 'accept edits on (shift+tab to cycle)' yazısı (OCR).) | 0:13 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Anthropic resmi ve ücretsiz Claude Code Setup plugin'ini yayınladı. | 0:00 | özellik |
| Kurulum tek komutla 30 saniyeden kısa sürer. | 0:25 | sayısal |
| Plugin kod tabanını tarayıp uygun hook, skill, subagent ve MCP önerir. | 0:09 | özellik |
| Alakasız plugin ve skill kurmak kurulumu şişirir ve yavaşlatır. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Most people using Cloud Code completely wrong |
| konuşma 0:00 | Anthropic | aday değil: genel kavram | Anthropic just dropped an official free plugin |
| konuşma 0:09 | Claude Code Setup | Claude Code Setup | official free plugin called Cloud Code Setup |
| konuşma 0:09 | hooks | Hooks | the best hooks |
| konuşma 0:09 | skills | Skills | the best skills |
| konuşma 0:09 | subagents | Subagents | the best subagents |
| konuşma 0:09 | MCP servers | MCP | the best MCP servers |
| kare 0:01 | Opus 4.6 | Claude Opus 4.6 | OCR: Opus 4.6 - Claude Max |
| kare 0:01 | /compact | /compact | OCR: /compact |
| kare 0:14 | claude-plugins-official | claude-plugins-official | anthropics / claude-plugins-official Public |
| kare 0:15 | Convex | Convex | recommender: add Convex to datab... |
| kare 0:20 | Supabase | Supabase | Connected to supabase |
| açıklama | Postgres | Postgres | Postgres, Vercel |
| açıklama | Vercel | Vercel | Postgres, Vercel |
| kare 0:01 | TypeScript dosyaları | TypeScript | src/middleware/upload.ts |
| kare 0:23 | Checkout hata sayfası | aday değil: konu dışı | Unhandled Runtime Error, checkout/page.tsx |
| ekran 0:13 | lewismenelaws.com | aday değil: konu dışı | Opus 4.6 · Claude Max · hi@lewismenelaws.com's |
| açıklama | PLUGIN yorum çağrısı | aday değil: sponsor/reklam | Comment PLUGIN to get this plugin |
## Kareden okunanlar
- 0:01: Claude Code terminali, /compact, 'COMPLETELY' yazısı ve üstü çizili kırmızı çizgi
- 0:06: 'OUT OF TOKENS - UPGRADE TO CONTINUE' hata ekranı ve 'THAT'S A BIG MISTAKE' yazısı
- 0:23: CHECKOUT sayfası, runtime TypeError hatası ve 'SPOT' yazısı
## Belirsizlikler
- Dil alanı '?' ; konuşma İngilizce.
- Altyazıda 'Cloud Code' yazılmış, Claude Code kastedildiği varsayıldı.
- Kurulum komutu videoda açıkça gösterilmedi; OCR'daki 'claude connect --plugin random' kısmen okunaklı bir dekor metni.
- Yorumlar girişsiz alınamadı.
- Opus 4.8 (0:17) ve Opus 4.6 farklı ekranlarda; hangisi kullanıldığı belirsiz.
- Kareler yalnızca 3 adet; diğer zamanlar OCR'dan çıkarıldı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| lewismenelaws.com | 0:13 | ekran | hayır |
| https://www.instagram.com/reel/DaagbUMP8Tg/ | açıklama | açıklama | hayır |
| https://github.com/anthropics/claude-plugins-official | 0:14 | ekran | evet |
## İş akışı
- 1. adım — Alakasız plugin ve skill kurmanın sorunu anlatılıyor — araçlar: Claude Code
- 2. adım — Token limiti hatası örneği gösteriliyor — araçlar: Claude Code
- 3. adım — Claude Code Setup plugin'i tanıtılıyor — araçlar: Claude Code Setup
- 4. adım — Plugin resmi depodan gösteriliyor — araçlar: claude-plugins-official
- 5. adım — Kod tabanı taraması isteniyor — araçlar: Claude Code Setup, Claude Code
- 6. adım — Supabase MCP bağlantısı ve sorgu örneği gösteriliyor — araçlar: MCP, Supabase
- 7. adım — Checkout hatası için review subagent önerisi gösteriliyor — araçlar: Subagents
- 8. adım — Yorumlara PLUGIN yazma çağrısı yapılıyor — araçlar: yok
## Promptlar
- Kod tabanı taraması — Kullanıcı Claude'dan tüm kod tabanını taramasını istiyor (scan my entire...).
- Supabase MCP testi — Supabase'teki en son 5 veritabanı kaydını getirmesi isteniyor.
ikinci göz KAPALI: --ikinci-goz yok
