# Claude Code Works Better With Loops, Not Prompts
## Künye
Claude Code Works Better With Loops, Not Prompts · Eric Tech · süre: 11:28 · en-orig · https://youtu.be/D7TIvqtSZQE · şema 2
motor: parti 2026-10-10-short-14 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 54596 tk · claude-haiku-5-5: claude-haiku-5-5 · 108883 tk
## Özet
Eric Tech, "loop engineering" kavramını anlatıyor: kullanıcı ajana tek seferlik prompt vermek yerine orkestratör → yürütücü → gözden geçirici döngüsü tasarlıyor ve hedef karşılanana kadar yinelemesini sağlıyor. Altı yapı taşı (tetikleyici, worktree, skill, bağlayıcı, bellek, alt ajanlar) GitHub Issues'ın bellek/durum katmanı olarak kullanıldığı gerçek bir proje panosu üzerinden gösteriliyor. Sonunda tüm bu pratikleri paketleyen taşınabilir Loop Maker skill'i tanıtılıyor: 7 soruluk sihirbaz, ayrı doğrulayıcı, durum dosyası ve insan kapısı ile döngü iskeleti üretiyor.
## Bölümler
- 0:00 Giriş
- 1:42 Döngüler nasıl çalışır
- 4:06 Neden birden çok ajan
- 4:50 Tetikleyici
- 5:03 Worktree
- 5:21 Skill'ler
- 5:34 Bağlayıcılar
- 7:08 Bellek
- 7:47 Alt ajanlar
- 8:07 Özet
- 10:06 Loop Maker skill'i
- 11:04 Kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Döngülerin içinde çalıştığı ana kodlama ajanı; Boris Cherny'nin tweet'inde ve terminal karesinde görünüyor. | 0:06 | Tweet: 'Claude Code creator, Boris Cherny' ve terminalde 'Claude Code Opus 4.7'. (karede: kanıttan) Tweet: 'Claude Code creator, Boris Cherny' ve terminalde 'Claude Code Opus 4.7'. |
| Opus 4.7 | yok | teknik | yok | Terminal karesinde Claude Code'un kullandığı model olarak görünüyor. | 0:42 | Terminal penceresinde 'Opus 4.7 · ~/acme' yazıyor. (karede: kanıttan) Terminal penceresinde 'Opus 4.7 · ~/acme' yazıyor. |
| Loop Maker | yok | skill | yok | 7 soruluk sihirbazla doğrulayıcılı, durum dosyalı, insan kapılı döngü iskeleti üreten taşınabilir skill. | 10:06 | Konuşmacı Loop Maker adlı taşınabilir agent skill'ini paketlediğini anlatıyor. |
| GitHub Issues | yok | iş akışı | yok | Her görev bir issue; her iterasyon log olarak ekleniyor, bellek/durum katmanı. | 9:08 | Durum için GitHub issues'a bağlandığını, her görevin bir issue olduğunu söylüyor. |
| GitHub | yok | MCP | yok | Bağlayıcı olarak commit, issue ve PR yönetimi için kullanılıyor. | 5:34 | GitHub'a bağlanıp değişiklikleri commit ettiğini ve issue'ları ittiğini söylüyor. |
| GitHub Projects | yok | iş akışı | yok | magnetgate proje panosu; Ready, Building, QA, Review, Done, Blocked sütunları. | 4:48 | Kanban panosunda Done 11, Blocked 2, Ready, Building, QA sütunları görünüyor. · kanıt: kare (karede: Kanban panosunda Done 11, Blocked 2, Ready, Building, QA sütunları görünüyor.) |
| Sentry | yok | MCP | yok | Logları incelemek için bağlayıcı olarak kullanılıyor. | 5:34 | Logları görmek için 'Century' (Sentry) bağlantısından söz ediyor; yazım otomatik altyazı hatası olabilir. · kanıt: yok |
| Slack | yok | MCP | yok | Bağlayıcı örneği olarak sayılıyor. | 5:34 | Bağlayıcı örnekleri arasında Slack, Jira, Supabase, Stripe sayılıyor. |
| Jira | yok | MCP | yok | Bağlayıcı örneği olarak sayılıyor. | 5:34 | Slack, Jira, Supabase, Stripe örnekleri sayılıyor. |
| Supabase | yok | MCP | yok | Bağlayıcı örneği; magnetgate görevlerinde şema ve provisioning için geçiyor. | 5:34 | Supabase bağlayıcı örnekleri arasında anılıyor; panoda 'Task 2: Supabase schema + seed SQL'. |
| Stripe | yok | MCP | yok | Bağlayıcı örneği olarak sayılıyor. | 5:34 | Slack, Jira, Supabase, Stripe örnekleri sayılıyor. |
| Git worktree | yok | teknik | yok | Her ajanın ayrı ortamda çalışması için; kod çakışmasını önler. | 5:03 | Her ajanın kendi work tree'sinde çalıştığını, çakışma olmadığını söylüyor. · kanıt: yok |
| Alt ajanlar | yok | teknik | yok | Her iterasyonda taze bağlam penceresiyle yeni alt ajan başlatılıyor; paralel çalışabilir. | 7:47 | Alt ajanlarla birden çok ajanın paralel, ayrı worktree'lerde çalışabildiğini anlatıyor. · kanıt: yok |
| Excalidraw | yok | CLI | yok | Döngü diyagramı ve '6 Steps to Perfect Loop' slaytı için kullanılan beyaz tahta aracı. | 0:46 | Excalidraw arayüzünde Trigger/Generator/Validator diyagramı ve 'Excalidraw+' düğmesi. (karede: kanıttan) Excalidraw arayüzünde Trigger/Generator/Validator diyagramı ve 'Excalidraw+' düğmesi. |
| Next.js | yok | teknik | yok | magnetgate issue'sundaki iskelet uygulamanın çatısı. | 5:48 | Issue'da 'Create the Next.js app' ve npx create-next-app komutu görünüyor. (karede: kanıttan) Issue'da 'Create the Next.js app' ve npx create-next-app komutu görünüyor. |
| Tailwind CSS | yok | teknik | yok | Issue'daki scaffold komutunda --tailwind seçeneği. | 5:58 | create-next-app komutunda --tailwind bayrağı ve tailwind.config.ts dosyası. (karede: kanıttan) create-next-app komutunda --tailwind bayrağı ve tailwind.config.ts dosyası. |
| Vitest | yok | teknik | yok | Birim testleri; QA raporunda vitest 10/10 PASS. | 6:16 | QA yorumunda 'vitest 10/10 PASS, npm run build exit 0'. (karede: kanıttan) QA yorumunda 'vitest 10/10 PASS, npm run build exit 0'. |
| Playwright | yok | teknik | yok | E2E test aracı; test:e2e betiği. | 5:52 | package.json betiklerinde 'test:e2e': 'playwright test'. (karede: kanıttan) package.json betiklerinde 'test:e2e': 'playwright test'. |
| TypeScript | yok | teknik | yok | Scaffold'da --typescript seçeneği. | 5:58 | create-next-app komutunda --typescript ve tsconfig.json. (karede: kanıttan) create-next-app komutunda --typescript ve tsconfig.json. |
| npm | yok | CLI | yok | Bağımlılık kurulumu ve test/build betikleri. | 5:58 | npm install ve npm run build komutları issue'da görünüyor. (karede: kanıttan) npm install ve npm run build komutları issue'da görünüyor. |
| Resend | yok | teknik | yok | Görev 6'da e-posta gönderici ve bağımlılık olarak geçiyor. | 6:06 | Listede 'Task 6: Resend email sender (Skool CTA included)'. (karede: kanıttan) Listede 'Task 6: Resend email sender (Skool CTA included)'. |
| Cloudflare Turnstile | yok | teknik | yok | Görev 5'te sunucu tarafı doğrulama. | 6:06 | Listede 'Task 5: Turnstile server verification #5'. · kanıt: kare (karede: Listede 'Task 5: Turnstile server verification #5'.) |
| Vercel | yok | teknik | yok | Görev 11'de dağıtım adımı olarak geçiyor. | 4:48 | Blocked sütununda 'Task 11 [HUMAN-assisted]: Vercel deploy + free.erictech.ca'. (karede: kanıttan) Blocked sütununda 'Task 11 [HUMAN-assisted]: Vercel deploy + free.erictech.ca'. |
| superpowers | yok | plugin | yok | Issue'daki plan/spec yollarında docs/superpowers klasörü. | 9:44 | Plan kaynağı: docs/superpowers/plans/2026-06-11-magnetgate-implementation.md. (karede: kanıttan) Plan kaynağı: docs/superpowers/plans/2026-06-11-magnetgate-implementation.md. |
| super-board | yok | iş akışı | yok | Build → QA → Review sürecini issue yorumlarına yazan pano hattı. | 6:16 | Yorumlarda 'super-board · QA pass · v2' ve 'Review approved · Merged'. (karede: kanıttan) Yorumlarda 'super-board · QA pass · v2' ve 'Review approved · Merged'. |
| Agentic OS | yok | iş akışı | yok | Eric'in kendi çoklu ajan sistemi; her ajan kendi worktree'sinde. | 5:03 | Agentic OS'inde ajanların ayrı worktree'lerde paralel çalıştığını söylüyor. |
| Claude Haiku | yok | teknik | yok | Yorumda işçi ajanlar için ucuz model önerisi. | açıklama | Sahip yorumu: yürütme için Haiku, gözden geçirme için Sonnet. |
| Claude Sonnet | yok | teknik | yok | Yorumda gözden geçirme ajanı için önerilen model. | açıklama | Sahip yorumu: Haiku yürütme, Sonnet gözden geçirme. |
| Ponytail | yok | skill | yok | Yorumda token harcamasını azaltmak için önerilen araç. | açıklama | Sahip yorumu: Ponytail iterasyon başına token harcamasını azaltıyor. |
| Century | yok | MCP | yok | Logları incelemek için ajanın bağlandığı konektör. Altyazıda 'Century' geçiyor; ekranda görünmüyor, Sentry olabilir. | 5:34 | connect it to Century to look at the logs |
| create-next-app | yok | CLI | yok | Next.js projesini TypeScript, Tailwind ve App Router bayraklarıyla kuran komut. | 5:58 | npx create-next-app@latest . -typescript --tailwind --app ... (karede: kanıttan) npx create-next-app@latest . -typescript --tailwind --app ... |
| Loop Maker skill'inin döngü kurmadan önce kullanıcıya soracağı soruları tanıtmak | yok | prompt | yok | Loop Maker'ın sorduğu 7 soru: hedef (ne zaman 'şimdilik tamam'), tetikleyici, keşif (iş nasıl bulunur), eylem (hangi araçlar), doğrulama (kim, neye göre kontrol eder), durum (yapılan/kalan nerede tutulur), insan kapısı (geri alınamayan eylemler). | 0:52 | kaynak: kare |
| Magnetgate Task 1 (repo iskeleti) için ajana verilen görev tanımı | yok | prompt | yok | Task 1 issue'su: repo kökünde Next.js uygulaması kur (App Router, TypeScript, Tailwind, @/* alias), package.json betiklerini ekle, vitest ve Playwright kur, .env.example ve .gitignore hazırla; npm run build çıkış kodu 0 olsun. | 5:48 | kaynak: kare |
| Task 1 için orkestratör talimatını belirtmek | yok | prompt | yok | Orkestratör notu: repo zaten .claude/ ve docs/ dosyalarını içeriyor (super-board boru hattı); bunlara dokunma, görev metninin geri kalanı aynen geçerli. | 6:02 | kaynak: kare |
| Magnetgate Task 2 (Supabase şema ve seed) için görev tanımı | yok | prompt | yok | Task 2 issue'su: supabase/schema.sql ve supabase/seed.sql oluştur; magnets ve leads tablolarında RLS'i aç, anon ve authenticated yetkilerini kaldır; seed kaydı idempotent olsun (on conflict do nothing). | 9:40 | kaynak: kare |
## Açıklama bağlantıları
- https://www.skool.com/erictech/about — Eric'in ücretli Skool topluluğu · aday: hayır · Ücretli topluluk, erişim için üyelik gerekiyor. · sınıf: diğer · erişilemez: ücretli topluluk
- https://free.erictech.ca/loopmaker?src=yt-loop-engineering — Loop Maker skill'i sayfası · aday: evet (Loop Maker) · İzleyicinin kullanabileceği skill; videoda anlatılıyor. · sınıf: affiliate
- https://youtu.be/nX_bGyIOFM4 — Önceki Eric Tech videosu · aday: hayır · Başka video, araç değil. · sınıf: diğer
- https://youtu.be/UvVVATGIm7k — Ponytail videosu · aday: hayır · Video bağlantısı; Ponytail adaylarda ayrıca yer alıyor. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*" | Repo kökünde Next.js (App Router, TS, Tailwind) uygulaması oluşturur. (karede: Issue gövdesinde Step 1 altında npx create-next-app komutu; satır sağda kesik.) | 5:58 | kare |
| npm install @supabase/supabase-js resend disposable-email-domains canvas-confetti server-only | Çalışma zamanı bağımlılıklarını kurar. (karede: Issue'da npm install satırı.) | 9:08 | kare |
| npm install -D vitest @types/canvas-confetti @playwright/test | Test ve tip geliştirme bağımlılıklarını kurar. (karede: Issue'da npm install -D vitest satırı görünüyor.) | 5:48 | kare |
| git clone … ~/.claude/skills/loop-maker | Loop Maker skill'ini Claude Code skill klasörüne klonlar (URL kesik). (karede: README tablosunda Install satırı: git clone … ~/.claude/skills/loop-maker.) | 10:06 | kare |
| npm test | Birim testlerini çalıştırır (QA test komutu). (karede: QA yorumunda 'Test command: npm test'.) | 6:16 | kare |
| npm run build | Üretim derlemesi; exit 0 bekleniyor. (karede: QA sonucunda 'npm run build exit 0'.) | 6:16 | kare |
| npx create-next-app@latest . -typescript --tailwind --app --no-src-dir --import-alias "@/*" --us… (satır kesik) | Repo kökünde TypeScript, Tailwind ve App Router ile Next.js uygulaması oluşturur (karede: Task 1 issue'sunda kod bloğu içinde 'npx create-next-app@latest .' satırı; sonu kesik.) | 5:58 | kare |
| "test": "vitest run" | package.json içinde testleri tek seferde çalıştıran betik tanımı (karede: package.json scripts bloğu: "test": "vitest run".) | 5:52 | kare |
| "test:watch": "vitest" | Testleri izleme modunda çalıştıran betik tanımı (karede: package.json scripts bloğunda "test:watch": "vitest" satırı.) | 5:52 | kare |
| "test:e2e": "playwright test" | Playwright uçtan uca testlerini çalıştıran betik tanımı (karede: package.json scripts bloğunda "test:e2e": "playwright test" satırı.) | 5:52 | kare |
| npm run dev | Geliştirme sunucusunu başlatır; yönlendirme curl ile doğrulanıyor (307/308) (karede: Acceptance criteria: 'verified with npm run dev + curl: 307/308 with Location header'.) | 6:02 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Boris Cherny artık Claude'u prompt etmediğini, döngülerin Claude'u prompt ettiğini söylüyor. | 0:06 | özellik |
| Peter Steinberger: kodlama ajanlarını prompt etmeyin, ajanları prompt eden döngüler tasarlayın. | 0:06 | öneri |
| Aynı ajanın hem işi yapıp hem değerlendirmesi öğrencinin kendi sınavını okumasına benzer; doğruluk düşer. | 4:06 | karşılaştırma |
| Loop Maker 7 soru sorar, boşlukları yoklar, döngü şeklini onaylatır ve iskeleti üretir. | 10:06 | özellik |
| Örnek issue'da QA 7/7 kabul kriterini doğruladı, vitest 10/10 geçti. | 6:16 | sayısal |
| Token maliyeti için işçi ajanlarda Haiku, gözden geçirmede Sonnet önerisi. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:06 | Boris Cherny / Claude Code tweet'i | Claude Code | Tweet 'Claude Code creator, Boris Cherny'. |
| kare 0:18 | Peter Steinberger tweet'i | aday değil: konu dışı | Kişi alıntısı, araç değil. |
| kare 0:42 | Addy Osmani paylaşımı | aday değil: konu dışı | Referans gönderi. |
| kare 0:22 | YouTube sayfası, vidIQ, NotebookLM | aday değil: konu dışı | Önceki video ve YouTube araçları arka planda. |
| kare 0:34 | Omnisend sponsor satırı | aday değil: sponsor/reklam | Başka videonun açıklamasındaki sponsor. |
| kare 0:46 | Excalidraw diyagramı | Excalidraw | Diyagram Excalidraw'da çiziliyor. |
| kare 0:48 | Cloudbot logosu | aday değil: konu dışı | Diyagramın köşe logosu. |
| kare 0:50 | Loop Maker README ve install.sh | Loop Maker | README'de loop-maker açıklaması. |
| kare 0:58 | Skool topluluk sayfası | aday değil: sponsor/reklam | Kanalın kendi topluluk tanıtımı. |
| kare 1:02 | n8n WhatsApp AI Agent iş akışı | aday değil: konu dışı | Topluluk tanıtımındaki örnek iş akışı. |
| kare 1:34 | Google AI Overview 'loop engineering' | aday değil: genel kavram | Arama sonucu tanımı. |
| konuşma 4:50 | Tetikleyici | Loop Maker | Altı yapı taşından biri. |
| konuşma 5:03 | Worktree | Git worktree | Ayrı ortam anlatımı. |
| konuşma 5:21 | Skill'ler | aday değil: genel kavram | Ajan harness'i olarak anlatılıyor. |
| konuşma 5:34 | Bağlayıcılar | aday değil: genel kavram | MCP olarak tanımlanıyor. |
| konuşma 5:34 | Slack, Jira, Supabase, Stripe, Sentry, GitHub | Slack | Bağlayıcı örnekleri; ayrı adaylarda da listeli. |
| konuşma 7:08 | Bellek | GitHub Issues | Bellek GitHub issue'larında tutuluyor. |
| konuşma 7:47 | Alt ajanlar | Alt ajanlar | Paralel alt ajan anlatımı. |
| kare 4:48 | magnetgate GitHub Projects panosu | GitHub Projects | Kanban sütunları gösteriliyor. |
| kare 5:48 | Task 1 issue: Next.js, Tailwind, Vitest, Playwright, npm | Next.js | Issue'daki scaffold adımları. |
| kare 6:06 | Resend, Turnstile görevleri | Resend | Görev listesinde anılıyor. |
| kare 6:16 | super-board QA/Review yorumları | super-board | Yorumlarda super-board etiketi. |
| kare 9:44 | docs/superpowers yolları | superpowers | Plan ve spec yolları. |
| kare 10:06 | Wizard UX, loop_progress.py | Loop Maker | README'de Python yardımcı betiği. |
| kare 10:30 | Skool Live Q&A gönderisi | aday değil: sponsor/reklam | Topluluk duyurusu. |
| açıklama | bookzero.ai | aday değil: sponsor/reklam | Eric'in kendi ürünü tanıtılıyor. |
| açıklama | free.erictech.ca/loopmaker | Loop Maker | Skill sayfası. |
| açıklama | skool.com/erictech/about | aday değil: sponsor/reklam | Topluluk bağlantısı. |
| yorum | Ponytail | Ponytail | Token azaltma önerisi. |
| yorum | Haiku, Sonnet, Opus | Claude Haiku | Model katmanı önerisi. |
| linkli sayfa | Omnisend sayfası | aday değil: sponsor/reklam | Sponsor sayfası. |
## Kareden okunanlar
- 0:06: Boris Cherny tweet'i: 'I don't prompt Claude anymore. I have loops prompting Claude…'
- 0:18: @steipete tweet'i, 7 Haziran 2026, 8.3M görüntülenme.
- 0:42: Addy Osmani 'Loop Engineering' paylaşımı, 8 Haziran.
- 0:46: Excalidraw diyagramı: Trigger, Worktree, Skill, Connector, Generator, Validator, State, Human Review, Complete.
- 4:36: Excalidraw slaytı '6 Steps to Perfect Loop', 1. Trigger yazılıyor.
- 9:40: Task 2: Supabase schema + seed SQL issue'su, kabul kriterleri.
- 10:06: Loop Maker README: 7 soru, wizard UX, 'Q3/7 43%' ilerleme çubuğu, LOOP BLUEPRINT kutusu.
## Belirsizlikler
- Kare zamanları ve sırası listeyle birebir eşleştirilemedi; zamanlar altyazı/OCR'dan tahmin edildi.
- 'Century' büyük olasılıkla Sentry (otomatik altyazı hatası).
- Ponytail ve Haiku/Sonnet yalnız yorumda geçiyor, videoda gösterilmiyor; adaylık zayıf.
- Loop Maker bağlantısı src parametreli; affiliate sayıldı ama açıkça ücretli ortaklık belirtilmemiş.
- Omnisend sponsor bağlantısı başka videonun açıklamasında (kare 0:34), bu videoda sponsor değil.
- Sözlük eşleşmelerindeki çoğu terim (Make, Stitch vb.) bulanık eşleşme, videoda kullanılmıyor.
- İlk karedeki Hermes Agent ve OpenClaw yalnız README'de 'works in' olarak geçiyor, kullanılmıyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/17 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| x.com/steipete | 0:06 | ekran | hayır |
| https://your.omnisend.com/eric-tech | 0:34 | ekran | hayır |
| install.sh | 0:50 | ekran | hayır |
| skool.com/erictech | 0:58 | ekran | hayır |
| github.com/EricTechPro/eric-tech-free-lead-magnet/issues/2 | 9:40 | ekran | hayır |
| https://www.skool.com/erictech/about | açıklama | açıklama | hayır |
| https://free.erictech.ca/loopmaker?src=yt-loop-engineering | açıklama | açıklama | evet |
| https://youtu.be/nX_bGyIOFM4 | açıklama | açıklama | hayır |
| https://youtu.be/UvVVATGIm7k | açıklama | yorum | hayır |
| https://www.youtube.com/@EricWTech | açıklama | açıklama | hayır |
| https://github.com/EricTechPro | açıklama | açıklama | hayır |
| https://erictech.ca | açıklama | açıklama | hayır |
| https://api-docs.omnisend.com | açıklama | açıklama | hayır |
| bookzero.ai | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Döngü kavramını ve orkestratör → yürütücü → denetleyici mimarisini diyagramla anlatma — araçlar: Excalidraw
- 2. adım — Tetikleyici seçeneklerini (slash skill, zamanlama, olay) açıklama — araçlar: Claude Code
- 3. adım — Her ajana ayrı çalışma alanı (worktree) ve branch verme — araçlar: Git
- 4. adım — Skill ve konektörleri (GitHub, Century) tanımlama — araçlar: Claude Code, GitHub, Century
- 5. adım — Hafıza için GitHub Issues'ta görev ve iterasyon loglarını gösterme — araçlar: GitHub Issues, GitHub
- 6. adım — Agentic OS'ta build → QA → review → merge akışını issue üzerinden izleme — araçlar: Agentic OS, GitHub
- 7. adım — magnetgate GitHub Projects panosunda Ready, Building, QA, Review, Done kolonlarını gösterme — araçlar: GitHub
- 8. adım — Task 1 issue'sunu açıp adımları ve kabul kriterlerini inceleme — araçlar: GitHub
- 9. adım — Repo iskeleti kurulumu: create-next-app ile Next.js ve npm ile bağımlılıklar — araçlar: create-next-app, Next.js, Tailwind CSS, npm, Vitest, Playwright
- 10. adım — package.json betiklerini (test, test:watch, test:e2e) ekleme — araçlar: npm, Vitest, Playwright
- 11. adım — Doğrulama: npm run build ve npm test sonuçlarını kontrol etme — araçlar: npm, Vitest
- 12. adım — Task 2 için Supabase şema ve seed SQL'ini issue'da gösterme — araçlar: Supabase
- 13. adım — Blocked görevleri (Turnstile, Resend, Vercel) insan kararına bırakma — araçlar: GitHub, Turnstile, Resend, Vercel
- 14. adım — Loop Maker skill'inin 7 sorusunu, doğrulayıcı ve insan kapısı yapısını tanıtma — araçlar: loop-maker
- 15. adım — Loop Maker'ı ~/.claude/skills/loop-maker dizinine git clone ile kurma — araçlar: Git, loop-maker
## Promptlar
- Loop Maker skill'inin döngü kurmadan önce kullanıcıya soracağı soruları tanıtmak — Loop Maker'ın sorduğu 7 soru: hedef (ne zaman 'şimdilik tamam'), tetikleyici, keşif (iş nasıl bulunur), eylem (hangi araçlar), doğrulama (kim, neye göre kontrol eder), durum (yapılan/kalan nerede tutulur), insan kapısı (geri alınamayan eylemler).
- Magnetgate Task 1 (repo iskeleti) için ajana verilen görev tanımı — Task 1 issue'su: repo kökünde Next.js uygulaması kur (App Router, TypeScript, Tailwind, @/* alias), package.json betiklerini ekle, vitest ve Playwright kur, .env.example ve .gitignore hazırla; npm run build çıkış kodu 0 olsun.
- Task 1 için orkestratör talimatını belirtmek — Orkestratör notu: repo zaten .claude/ ve docs/ dosyalarını içeriyor (super-board boru hattı); bunlara dokunma, görev metninin geri kalanı aynen geçerli.
- Magnetgate Task 2 (Supabase şema ve seed) için görev tanımı — Task 2 issue'su: supabase/schema.sql ve supabase/seed.sql oluştur; magnets ve leads tablolarında RLS'i aç, anon ve authenticated yetkilerini kaldır; seed kaydı idempotent olsun (on conflict do nothing).
