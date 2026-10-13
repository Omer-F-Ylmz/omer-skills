# Most people are running one AI agent… while others are running entire teams.
## Künye
Most people are running one AI agent… while others are running entire teams. · duncanrogoff · süre: 0:54 · ? · https://www.instagram.com/reel/DXxQS0AO1Km/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-12-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 18319 tk · claude-haiku-5-5: claude-haiku-5-5 · 50210 tk
## Özet
Kısa reel, Claude Code'u 60'tan fazla ajanlı bir sisteme dönüştüren açık kaynak Ruflo (eski adıyla Claude Flow) çerçevesini tanıtıyor. Kraliçe (yönetici) ajanlar takımları yönetir, taktik ajanlar araştırma, kodlama, test ve inceleme yapar. Ortak bellek sayesinde sistem her çalıştırmada gelişir. Görev karmaşıklığına göre ucuz ya da güçlü modele otomatik yönlendirme yapılır; konuşmacı token kullanımında %50'ye varan tasarruf iddia ediyor. Ekranda GitHub README'si, kurulum komutları, paralel ajanların çalıştığı terminal ve token monitörü görünüyor. Açıklamada tanıtımın sonunda 'flow' yorumuyla kurulum rehberi vaat ediliyor.
## Bölümler
- 0:00 Ruflo'ya giriş: GitHub'da bir numara, ücretsiz
- 0:09 Kraliçe ve taktik ajan hiyerarşisi, ortak bellek
- 0:29 Paralel ajanlarla uygulama geliştirme örneği
- 0:37 Otomatik model yönlendirme ve token tasarrufu
- 0:47 Açık kaynak, GitHub'da #1 ve kurulum rehberi çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Ruflo | yok | CLI | https://github.com/ruvnet/ruflo | Claude Code'u çok ajanlı sürü sistemine çeviren orkestrasyon çerçevesi | 0:00 | It's called Ruflo. ... spins up 60 plus AI agents that all work together |
| Claude Code | yok | CLI | yok | Ruflo'nun üzerinde çalıştığı ana yapay zekâ kodlama aracı | 0:05 | IMPORTANT: Claude Code must be installed first (karede: kanıttan) IMPORTANT: Claude Code must be installed first |
| Claude Flow | yok | CLI | yok | Ruflo'nun eski adı; init komutu bu paketle gösteriliyor | 0:11 | $ npx claude-flow@v3alpha init (karede: kanıttan) $ npx claude-flow@v3alpha init |
| RuVector | yok | teknik | yok | PostgreSQL tabanlı vektör zekâ ve arama katmanı | 0:13 | RuVector: 77+ SQL functions, ~61μs search (karede: kanıttan) RuVector: 77+ SQL functions, ~61μs search |
| MCP | yok | MCP | yok | Ruflo'nun Claude Code'a sunduğu 170+ araçlık entegrasyon | 0:12 | Loaded 170+ MCP tools for Claude Code integration (karede: kanıttan) Loaded 170+ MCP tools for Claude Code integration |
| flow-nexus | yok | MCP | yok | Bulut sürü dağıtımı MCP sunucusu | 0:18 | flow-nexus - Cloud swarm deployment (karede: kanıttan) flow-nexus - Cloud swarm deployment |
| SoNA | yok | teknik | yok | Kendi kendine öğrenme sistemi | 0:12 | Initialized SoNA self-learning system (karede: kanıttan) Initialized SoNA self-learning system |
| MoE routing | yok | teknik | yok | Uzman karışımı ile görev yönlendirme (8 uzman) | 0:13 | Initializing MoE routing (8 experts). (karede: kanıttan) Initializing MoE routing (8 experts). |
| AIDefence | yok | teknik | yok | Tehdit algılama güvenlik katmanı | 0:18 | AIDefence security layer active (<10ms threat detection) (karede: kanıttan) AIDefence security layer active (<10ms threat detection) |
| Node.js | yok | teknik | yok | Ruflo için gerekli çalışma ortamı (20+) | 0:05 | Node.js 20+ (required) (karede: kanıttan) Node.js 20+ (required) |
| npm | yok | CLI | yok | Claude Code ve Ruflo kurulum paket yöneticisi | 0:05 | npm install -g @anthropic-ai/claude-code (karede: kanıttan) npm install -g @anthropic-ai/claude-code |
| Sonnet 4.6 | yok | teknik | yok | Alt ajanın kullandığı model | 0:17 | Agent(Implement Task 10: SRT subtitles) Sonnet 4.6 (karede: kanıttan) Agent(Implement Task 10: SRT subtitles) Sonnet 4.6 |
| Opus 4.7 | yok | teknik | yok | Karmaşık görevler için güçlü model örneği | 0:39 | Opus 4.7 (karede: kanıttan) Opus 4.7 |
| GPT-5.4 | yok | teknik | yok | Yönlendirmede gösterilen model | 0:39 | GPT-5.4 (karede: kanıttan) GPT-5.4 |
| Gemini 3.1 Pro | yok | teknik | yok | Yönlendirmede gösterilen model | 0:39 | Gemini 3.1 Pro (karede: kanıttan) Gemini 3.1 Pro |
| Llama 3.1 | yok | teknik | yok | Yönlendirmede gösterilen model | 0:37 | Llama 3.1 (karede: kanıttan) Llama 3.1 |
| Claude Token Monitor | yok | CLI | yok | Token tüketimini izleyen terminal aracı | 0:40 | CLAUDETOKEN MONITOR ... 156.4 tokens/min (karede: kanıttan) CLAUDETOKEN MONITOR ... 156.4 tokens/min |
| Groq | yok | teknik | yok | Örnek projede LLM analiz servisi | 0:14 | Task 8: Groq LLM analysis (karede: kanıttan) Task 8: Groq LLM analysis |
| FastAPI | yok | teknik | yok | Örnek projedeki arka uç çerçevesi | 0:14 | from fastapi inport APIRouter, Depends, File, Form (karede: kanıttan) from fastapi inport APIRouter, Depends, File, Form |
| Next.js | yok | teknik | yok | Örnek e-ticaret projesinin çerçevesi | 0:30 | Next.js 16 App Router. IMPoRTANT: params is a Promise (karede: kanıttan) Next.js 16 App Router. IMPoRTANT: params is a Promise |
| shadcn/ui | yok | teknik | yok | Frontend bileşen kütüphanesi | 0:30 | Frontend UI - Layout, theme, components (shadcn/ui) (karede: kanıttan) Frontend UI - Layout, theme, components (shadcn/ui) |
| Prisma | yok | teknik | yok | Örnek projede veritabanı ORM'i | 0:30 | import prisma from '@/lib/db' (karede: kanıttan) import prisma from '@/lib/db' |
| NextAuth.js | yok | teknik | yok | Örnek projede kimlik doğrulama | 0:29 | Authentication with NextAuth.js (email + Google OAuth) (karede: kanıttan) Authentication with NextAuth.js (email + Google OAuth) |
| Stripe | yok | teknik | yok | Örnek projede ödeme/checkout | 0:29 | Cart + Stripe checkout (running) (karede: kanıttan) Cart + Stripe checkout (running) |
| Docker | yok | teknik | yok | Örnek projede dağıtım ve ortam yapılandırması | 0:30 | Devops - Docker, env config (karede: kanıttan) Devops - Docker, env config |
| GitHub | yok | teknik | yok | Ruflo deposunun README, commit ve sürüm sayfaları; videoda sıralama iddiasının kaynağı olarak gösterilir | 0:49 | #1 on Github (karede: kanıttan) #1 on Github |
| PostgreSQL | yok | teknik | yok | RuVector MCP'sinin vektör veritabanı altyapısı | 0:18 | ruvector - PostgresQL vector intelligence (karede: kanıttan) ruvector - PostgresQL vector intelligence |
| FFmpeg | yok | teknik | yok | Ajan görevi listesinde geçen video işleme servisi (Task 9) | 0:14 | Task 9: FFmpeg service · kanıt: kare (karede: Task 9: FFmpeg service) |
| TypeScript | yok | teknik | yok | Hedef projenin dili (src/lib/*.ts dosyaları) | 0:30 | TypeScript (ekran sözlük eşleşmesi, 0:30) (karede: kanıttan) TypeScript (ekran sözlük eşleşmesi, 0:30) |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh / bash | Ruflo'yu tek satırlık betikle kurar (karede: Get Started Fast bölümünde One-Line Install komutu) | 0:04 | kare |
| curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh / bash -s -- --full | MCP ve tanılamalı tam kurulum yapar (karede: 'Or full setup with MCP + diagnostics' yorumunun altındaki komut) | 0:04 | kare |
| npx ruflo@latest init --wizard | Ruflo'yu npx ile sihirbaz modunda başlatır (karede: 'Or via npx' yorumunun altındaki komut) | 0:04 | kare |
| npm install -g @anthropic-ai/claude-code | Önkoşul olarak Claude Code'u global kurar (karede: '1. Install Claude Code globally' altındaki komut) | 0:05 | kare |
| claude --dangerously-skip-permissions | Claude Code'u izin istemlerini atlayarak başlatır (karede: Önkoşul bölümünde izinleri atlama komutu) | 0:05 | kare |
| npx claude-flow@v3alpha init | Claude Flow v3 alpha projesini başlatır | 0:11 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ruflo GitHub'da bir numara ve tamamen ücretsiz | 0:00 | sayısal |
| 60'tan fazla ajan birlikte çalışır ve her çalıştırmada gelişir | 0:00 | özellik |
| Görev karmaşıklığına göre otomatik model yönlendirme yapar | 0:29 | özellik |
| Token kullanımını %50'ye kadar azaltır, Claude kullanımını %250 uzatır | 0:40 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Ruflo | Ruflo | It's called Ruflo. |
| konuşma 0:00 | GitHub | aday değil: genel kavram | ranked number one on GitHub |
| kare 0:05 | Claude Code | Claude Code | Claude Code must be installed first |
| kare 0:11 | Claude Flow | Claude Flow | npx claude-flow@v3alpha init |
| kare 0:13 | RuVector | RuVector | RuVector: 77+ SQL functions |
| kare 0:12 | MCP araçları | MCP | Loaded 170+ MCP tools |
| kare 0:18 | flow-nexus | flow-nexus | flow-nexus - Cloud swarm deployment |
| kare 0:12 | SoNA | SoNA | Initialized SoNA self-learning system |
| kare 0:13 | MoE routing | MoE routing | Initializing MoE routing (8 experts). |
| kare 0:18 | AIDefence | AIDefence | AIDefence security layer active |
| kare 0:13 | Raft, BFT, Gossip, CRDT protokolleri | aday değil: başka adayın parçası (Ruflo) | 5 consensus protocols ready (Raft, BFT, Gossip, CRDT) |
| kare 0:05 | Node.js | Node.js | Node.js 20+ (required) |
| kare 0:05 | npm | npm | npm install -g @anthropic-ai/claude-code |
| kare 0:05 | pnpm ve bun | aday değil: başka adayın parçası (npm) | npm 9+ / pnpm / bun package manager |
| kare 0:05 | Anthropic, OpenAI, Google, Cohere, Ollama sağlayıcıları | aday değil: başka adayın parçası (Ruflo) | 5 providers (Anthropic, OpenAI, Google, Cohere, Ollama) |
| kare 0:17 | Sonnet 4.6 | Sonnet 4.6 | Agent(Implement Task 10: SRT subtitles) Sonnet 4.6 |
| kare 0:39 | Opus 4.7 | Opus 4.7 | Opus 4.7 |
| kare 0:39 | GPT-5.4 | GPT-5.4 | GPT-5.4 |
| kare 0:39 | Gemini 3.1 Pro | Gemini 3.1 Pro | Gemini 3.1 Pro |
| kare 0:37 | Llama 3.1 | Llama 3.1 | Llama 3.1 |
| kare 0:40 | Claude Token Monitor | Claude Token Monitor | CLAUDETOKEN MONITOR |
| kare 0:14 | Groq | Groq | Task 8: Groq LLM analysis |
| kare 0:14 | FastAPI | FastAPI | from fastapi inport APIRouter |
| kare 0:14 | Python | aday değil: genel kavram | Terminal sekmesinde Python etiketi |
| kare 0:30 | Next.js | Next.js | Next.js 16 App Router |
| kare 0:30 | shadcn/ui | shadcn/ui | components (shadcn/ui) |
| kare 0:30 | Prisma | Prisma | import prisma from '@/lib/db' |
| kare 0:29 | NextAuth.js | NextAuth.js | Authentication with NextAuth.js |
| kare 0:29 | Stripe | Stripe | Cart + Stripe checkout |
| kare 0:30 | Docker | Docker | Devops - Docker, env config |
| açıklama | Instagram reel bağlantısı | aday değil: konu dışı | Videonun kendi sayfası |
| açıklama | Yorum/DM ile kurulum rehberi çağrısı | aday değil: konu dışı | Comment 'flow' or DM 'flow' |
## Kareden okunanlar
- 0:04: Ruflo README: Getting into the Flow, Get Started Fast, curl install.sh ve npx ruflo@latest init --wizard
- 0:05: README ön koşullar: Node.js 20+, npm 9+, Claude Code kurulumu, claude --dangerously-skip-permissions, LLM sağlayıcı tablosu
- 0:14: VS Code terminali: 6 paralel ajan tablosu (Project CRUD router, Audio DSP, Groq analizi), FastAPI kodu; konuşmacı kamerada
## Belirsizlikler
- Kareler yalnızca 0:04, 0:05 ve 0:14 anlarına ait; diğer anlar OCR'a dayanıyor.
- Konuşmada 'cloud code' ifadesi Claude Code anlamında yorumlandı.
- %50 token tasarrufu ve %250 kullanım uzatma iddiaları doğrulanmadı.
- OCR'da 'Ruflow' ve 'RuFlo' yazımları geçiyor; kanonik ad Ruflo alındı.
- Yorumlar girişsiz alınamadı.
- Sözlük eşleşmeleri (Codex, CapCut, Hermes Agent, agent-sdk-dev) videoda gösterilmiyor, aday yapılmadı.
- Fransızca terminal çıktısı ve model listesinin (0:37-0:39) tam bağlamı belirsiz.
- Kurulum rehberi yorum/DM ile veriliyor, içeriği görülemedi.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | 0:04 | ekran | evet |
| https://www.instagram.com/reel/DXxQS0AO1Km/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Ruflo'nun GitHub README ve sürüm sayfasını inceleme — araçlar: GitHub, Ruflo
- 2. adım — Node.js ön koşulunu ve Claude Code'u npm ile global kurma — araçlar: Node.js, npm, Claude Code
- 3. adım — Ruflo tek satır kurulum scriptini çalıştırma — araçlar: curl, Ruflo
- 4. adım — Ruflo sihirbazını başlatma (init --wizard) — araçlar: npx, Ruflo
- 5. adım — Claude Code'u izin istemeden başlatma (--dangerously-skip-permissions) — araçlar: Claude Code
- 6. adım — Proje içinde claude-flow init ile kurulum ve MCP sunucu yapılandırması — araçlar: npx, Ruflo, MCP
- 7. adım — Görevleri ajan takımına dağıtma (Task 3, 4, 6, 8, 9, 10) — araçlar: Ruflo, Claude Sonnet 4.6, Groq, FFmpeg
- 8. adım — Ajanların arka planda çalışmasını ve görev durumlarını terminalde izleme — araçlar: Claude Code
- 9. adım — Beklenen başarısız testleri doğrulama (404, rotalar henüz yok) — araçlar: Ruflo
- 10. adım — Token kullanımını ve limit sıfırlanmasını izleme — araçlar: Claude Token Monitor
- 11. adım — Hedef projede Next.js iskeleti, Prisma şeması ve NextAuth.js kimlik doğrulaması — araçlar: Next.js, Prisma, NextAuth.js, TypeScript
- 12. adım — Sepet ve Stripe ödeme entegrasyonunu kurma — araçlar: Stripe
- 13. adım — Ön yüz bileşenleri ve temayı kurma — araçlar: shadcn/ui
- 14. adım — Docker ve ortam değişkenleri ile dağıtım yapılandırması — araçlar: Docker
- 15. adım — Ruflo sürüm ve değişiklik kayıtlarını (CHANGELOG, README) GitHub'da inceleme — araçlar: GitHub, Git
## Promptlar
- yok
