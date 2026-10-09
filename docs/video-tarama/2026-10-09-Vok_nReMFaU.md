# The Engineering System for AI Agents.
## Künye
The Engineering System for AI Agents. · JavaScript Mastery · süre: 23:33 · en-orig · https://youtu.be/Vok_nReMFaU · şema 2
motor: parti 2026-10-09-uzun-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 174426 tk · claude-haiku-5-5: claude-haiku-5-5 · 143055 tk
## Özet
JavaScript Mastery, yapay zekâ ajanlarıyla geliştirmede 'çürüme' sorununu (her özellik sonrakini zorlaştırır) anlatıyor ve çözüm olarak açık kaynak JSM Skills iş akışını gösteriyor: /scope (planlama), /architect (tasarım kararları), /develop (karar uydurmadan inşa), /audit (AGENTS.md ve CLAUDE.md bağlam dosyaları; eski PHP ve NestJS kodunda da), /sync, /check verify, /test, /check review (farklı modelle inceleme), /document ve /debug (kök neden odaklı). Gösterim Claude Code içinde (Opus 5 1M) bir ekip issue tracker'ı (Next.js 16, Prisma, Better Auth, Tailwind v4, shadcn/ui, Vitest, Playwright) ve NestJS + Drizzle bir auth sunucusu üzerinde yapılır. Kurulum npx skills ile; sonda Agentic Engineering kursu (22 Eylül) tanıtılır.
## Bölümler
- 0:00 Yapay zekâ çürümesi sorunu
- 1:49 Kapsamla planlama
- 4:40 Mimari ve geliştirme
- 9:02 Proje bağlamını yönetme
- 11:28 Eski kodda çalışma
- 14:28 Doğrulama ve kalite
- 17:25 Disiplinli hata ayıklama
- 20:25 Ajan mühendisliği zihniyeti
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Skill'lerin çalıştığı ana ajan ortamı (VS Code içinde) | 3:12 | Claude Code paneli ve giriş kutusu görünüyor (karede: VS Code içinde 'Claude Code' paneli, 'Learn Claude Code' kutusu, Opus 5 (1M) High seçili) |
| Opus 5 (1M) | yok | teknik | yok | Sunucunun içinde çalıştığı ana model; kodu yazan model | 3:12 | Giriş kutusunda model adı yazıyor (karede: Giriş çubuğunda 'Opus 5 (1M) High' yazıyor) |
| JSM Skills | yok | skill | https://github.com/jsmastery-pro/skills | Plandan yayına skill seti: scope, architect, develop, audit, sync, check, test, document, debug | 20:20 | GitHub deposu 'Engineering Workflow Skills' (karede: GitHub jsmastery-pro/skills sayfası, README 'Engineering Workflow Skills', 1.0k yıldız) |
| /scope | yok | skill | yok | Fikri röportajla sıralı plana çevirir, teknolojiye dokunmaz | 3:12 | /scope A team issue tracker komutu çalıştırılıyor (karede: Sohbette '/scope A team issue tracker: create issues…' ve AskUserQuestion sekmeleri) |
| /architect | yok | skill | yok | Yığın ve mimari kararlarını seçenekler ve gerekçelerle spec'e yazar | 6:12 | /architect stack & architecture çalışıyor (karede: Sohbette '/architect stack & architecture', Framework/Database/Auth soru sekmeleri) |
| /develop | yok | skill | yok | Spec'ten inşa eder; kaynağı olmayan değerde durur | 7:12 | /develop stack & architecture ve /develop tooling (karede: '/develop stack & architecture' sohbeti, 'Scaffold is green' mesajı) |
| /audit | yok | skill | yok | Projeyi okuyup AGENTS.md ve CLAUDE.md yazar | 8:16 | /audit çalışıyor, AGENTS.md ve CLAUDE.md üretiliyor (karede: '/audit complete · whole-repo' özeti: 4 AGENTS.md ve CLAUDE.md) |
| /sync | yok | skill | yok | Bağlam dosyalarını repo'nun güncel haline göre eşitler | 10:02 | sync skill will reconcile those files against what the repo actually shows |
| /check verify | yok | skill | yok | Gerçek uygulamayı sürüp plan ölçütlerine karşı doğrular | 15:29 | /check verify stack & architecture komutu (karede: Sohbette '/check verify stack & architecture', next 16.3.4 ve tailwindcss 4.3.3 çıktısı) |
| /test | yok | skill | yok | Kıdemli mühendis seviyesinde test paketi yazar | 15:40 | /test stack & architecture ve 19 test yazıldı (karede: '/test stack & architecture', Testing Library sorusu) |
| /check review | yok | skill | yok | Kodu yazandan farklı modelle inceleme yapar | 15:50 | Author model sorusu: opus yazdı, sonnet inceler (karede: '/check review', 'Which model wrote this code?' seçenekleri opus, sonnet, fable) |
| /document | yok | skill | yok | PR açıklaması ve değişiklik kaydını diff'ten yazar | 16:14 | /document pr komutu (karede: '/document pr' sohbeti, git rev-parse ve gh pr view komutları) |
| /debug | yok | skill | yok | Hatayı yeniden üretip tek kuramla kök nedeni bulur | 17:24 | Girişte /debug design system & ui foundation (karede: Giriş kutusunda '/debug design system & ui foundation') |
| AGENTS.md | yok | teknik | yok | Ajan bağlam dosyası (yığın, komutlar, kurallar) | 9:02 | Every agentic setup runs on a context file, an agent's MD |
| CLAUDE.md | yok | teknik | yok | Claude için bağlam dosyası | 9:02 | a claude MD, or whatever your tool calls it |
| Skills CLI | yok | CLI | yok | npx skills ile skill kurulumu | 20:28 | README 'Uses npx skills' (karede: README Install bölümü: npx skills@latest add jsmastery-pro/skills -a claude-code) |
| jsm-skills | yok | CLI | yok | Tüm skill'leri ekleyen CLI | 20:54 | npx jsm-skills add --all (OCR) (karede: Kurs sayfasında OCR'de 'npx jsm-skills add --all' (karede net doğrulanamadı)) |
| Next.js | yok | teknik | yok | Issue tracker için seçilen tam yığın framework | 6:16 | Next.js 16 (recommended) seçili (karede: Framework sekmesinde 'Next.js 16 (recommended)' seçili) |
| Better Auth | yok | teknik | yok | Önerilen kimlik doğrulama kütüphanesi | 6:18 | Auth sekmesinde Better Auth (recommended) (karede: Auth sekmesinde 'Better Auth, hosted by you (recommended)') |
| Tailwind CSS | yok | teknik | yok | Stil sistemi, v4 @theme tokenları | 6:36 | Tailwind v4 @theme ve prefers-color-scheme (karede: Spec 0003'te 'Tailwind v4's @theme' ve globals.css) |
| shadcn/ui | yok | teknik | yok | Kopyalanan bileşen seti ve skill | 6:36 | Implementation skills: shadcn (shadcn/ui) (karede: 'Implementation skills: shadcn (shadcn/ui, .claude/skills/shadcn/)') |
| tailwind-4-docs | yok | skill | yok | Tailwind 4 dokümantasyon skill'i | 6:36 | lombiq/tailwind-agent-skills (karede: Spec'te 'tailwind-4-docs (lombiq/tailwind-agent-skills, .claude/skills/tailwind-4-docs/)') |
| web-design-guidelines | yok | skill | yok | Tasarım rehberi skill'i | 6:36 | antfu/skills · kanıt: kare (karede: 'web-design-guidelines (antfu/skills, .claude/skills/web-design-guidelines/)') |
| next-dev-loop | yok | skill | yok | Next.js geliştirme döngüsü skill'i | 6:36 | vercel/next.js · kanıt: kare (karede: 'next-dev-loop (vercel/next.js, .claude/skills/next-dev-loop/)') |
| playwright-cli | yok | CLI | yok | Tarayıcı otomasyon skill'i | 6:36 | microsoft/playwright-cli (karede: 'playwright-cli (microsoft/playwright-cli, .claude/skills/playwright-cli/)') |
| Playwright | yok | teknik | yok | Uçtan uca tarayıcı testleri | 15:46 | 7 tarayıcı akışı pnpm test:e2e ile geçti (karede: '7 browser flows passed via pnpm test:e2e' ve e2e/scaffold.spec.ts) |
| Vitest | yok | teknik | yok | Birim test çalıştırıcı | 15:46 | 12 unit passed via pnpm test (karede: '12 unit passed via pnpm test') |
| Geist | yok | teknik | yok | Font ailesi (Geist ve Geist_Mono), next/font/google ile | 6:40 | layout.tsx'te Geist ve Geist_Mono yükleniyor (karede: 'Load Geist and Geist_Mono in src/app/layout.tsx' ve --font-geist-sans) |
| Prisma | yok | teknik | yok | Issue tracker veritabanı ORM'i | 6:46 | prisma/schema.prisma ve IssueStatus enum (karede: 'The IssueStatus enum in prisma/schema.prisma (spec 0002)') |
| Zod | yok | teknik | yok | Env ve form doğrulama şeması | 6:58 | VERCEL_ENV Zod şemasına eklendi (karede: 'VERCEL_ENV: added to the Zod schema in src/lib/env.ts') |
| Lucide | yok | teknik | yok | İkon kütüphanesi (empty-state) | 6:44 | empty-state'te muted lucide icon (karede: 'empty-state: a centred block holding a muted lucide icon') |
| Radix UI | yok | teknik | yok | shadcn bileşenlerinin temeli | 6:36 | Radix tabanlı bileşenler (karede: 'data-state keyframe animations that the Radix based components use') |
| Sonner | yok | teknik | yok | Toast bileşeni | 6:44 | Sonner iç kalıbı; bileşen envanterinde sonner (karede: 'same pattern Sonner uses internally' ve envanterde 'sonner') |
| Vercel | yok | teknik | yok | Dağıtım hedefi | 5:52 | Vercel deploys from one repo (karede: 'there is no git repository here yet, and Vercel deploys from one') |
| Husky | yok | teknik | yok | Git hook yöneticisi (seçilen) | 7:54 | Husky plus lint-staged (recommended) (karede: 'Husky plus lint-staged (recommended)'; .husky/pre-commit) |
| lint-staged | yok | teknik | yok | Staged dosyalarda Prettier ve ESLint | 8:12 | lint-staged.config.mjs (karede: Tabloda 'lint-staged.config.mjs: ESLint fix plus Prettier on staged files') |
| Prettier | yok | teknik | yok | Kod biçimlendirici, Tailwind sınıf sıralayıcılı | 8:12 | prettier.config.mjs (karede: 'Prettier on near defaults… Tailwind class sorter') |
| ESLint | yok | teknik | yok | Lint aracı | 8:12 | eslint-config-prettier/flat eklendi (karede: 'eslint-config-prettier/flat added last') |
| GitHub Actions | yok | teknik | yok | CI iş akışı | 8:12 | .github/workflows/ci.yml · kanıt: kare (karede: Tabloda '.github/workflows/ci.yml') |
| pnpm | yok | CLI | yok | Paket yöneticisi | 8:12 | pnpm lint, format:check, typecheck, build (karede: 'pnpm lint, pnpm format:check, pnpm typecheck, pnpm build') |
| NestJS | yok | teknik | yok | Eski/mevcut auth sunucusu yığını | 12:20 | /audit NestJS 11 projesini okuyor (karede: README çıktısında nestjs.com bağlantısı ve 'NestJS 11, Drizzle ORM') |
| Drizzle ORM | yok | teknik | yok | NestJS projesinin veritabanı katmanı | 12:32 | Drizzle skill ve MCP önerileri (karede: 'Drizzle ORM' ve drizzle-docs / drizzle-mcp satırları) |
| Neon | yok | MCP | https://github.com/neondatabase/mcp-server-neon | Neon Postgres skill'i ve MCP sunucusu önerisi | 12:32 | @neondatabase/mcp-server-neon, neon-postgres (karede: '@neondatabase/mcp-server-neon' ve 'neondatabase/agent-skills@neon-postgres') |
| drizzle-docs | yok | MCP | https://github.com/Michael-Obele/drizzle-docs | Drizzle dokümantasyonunda anlamsal arama MCP'si (önerildi) | 12:32 | Michael-Obele/drizzle-docs (karede: 'drizzle-docs — semantic search over Drizzle documentation') |
| drizzle-mcp | yok | MCP | https://github.com/defrex/drizzle-mcp | Drizzle işlemleri ve drizzle-kit MCP'si (önerildi) | 12:32 | github.com/defrex/drizzle-mcp (karede: 'drizzle-mcp — Drizzle ORM database operations and drizzle-kit CLI integration') |
| nestjs-best-practices | yok | skill | yok | Kurulan NestJS skill'i | 12:52 | 4 kurulu skill listesinde (karede: 'Installed skills: nestjs-best-practices, drizzle, javascript-typescript-jest, typescript-advanced-types') |
| drizzle | yok | skill | yok | Kurulan Drizzle skill'i | 12:52 | Kurulu skill listesi (karede: Aynı kurulu skill listesi) |
| javascript-typescript-jest | yok | skill | yok | Kurulan Jest skill'i | 12:52 | Kurulu skill listesi (karede: Aynı kurulu skill listesi) |
| typescript-advanced-types | yok | skill | yok | Kurulan TypeScript skill'i | 12:52 | Kurulu skill listesi (karede: Aynı kurulu skill listesi) |
| Claude Sonnet 5 | yok | teknik | yok | /check review'da inceleme modeli | 17:24 | reviewed by Claude Sonnet 5 over 79 files (karede: 'reviewed by Claude Sonnet 5 over 79 files') |
| Argon2 | yok | teknik | yok | NestJS auth sunucusunda parola özetleme | 12:24 | Yığın listesinde argon2 (karede: 'Resend, argon2, class-validator, Jest') |
| Resend | yok | teknik | yok | NestJS projesinde e-posta servisi | 12:24 | Resend skill önerisi (karede: 'Resend email: resend/resend-skills@resend') |
| Claude Opus 5 | yok | teknik | yok | Claude Code oturumlarında kullanılan ana model (1M bağlam, High düşünme). | 3:12 | Opus 5 (1M) High (karede: Model seçici: 'Opus 5 (1M) High') |
| Claude Fable | yok | teknik | yok | İnceleme için seçilebilen model seçeneği ('fable'). | 15:50 | fable · Review will run on fable (karede: Model seçim penceresi: 'opus', 'sonnet', 'fable' seçenekleri) |
| GitHub Copilot | yok | plugin | yok | Eski demo klibinde VS Code içinde kullanılan yapay zekâ asistanı. | 0:02 | GitHub Copilot (karede: Sohbet panelinde 'GitHub Copilot' ve '@workspace Create a new service...' mesajı) |
| Gemini CLI | yok | CLI | yok | Agent Skills'in çalıştığı istemciler listesinde yer alıyor. | 20:28 | Gemini CLI (karede: 'Works on any Agent Skills client' listesinde 'Gemini CLI' (OCR)) |
| Cursor | yok | teknik | yok | Agent Skills'in çalıştığı istemciler listesinde; yorumda da geçiyor. | 20:28 | Cursor (karede: 'Works on any Agent Skills client' listesinde 'Cursor' (OCR)) |
| VS Code | yok | teknik | yok | Videodaki kodlama editörü; skill'ler editör içinde çalışıyor. | 0:02 | runner-service.ts (karede: VS Code benzeri editörde runner-service.ts dosyası ve sağda sohbet paneli) |
| Git | yok | CLI | yok | Depo durumu, commit ve geçmiş kontrolü için kullanılıyor. | 9:40 | List project files and git history (karede: Bash komutu 'List project files and git history' (OCR, 9:38 karesine yakın)) |
| npm | yok | CLI | yok | create-next-app sürümünü sorgulamak için npm view komutu kullanılıyor. | 7:42 | npm view create-next-app version (karede: OCR: 'npm view create-next-app version' komutu (7:12 karesine yakın)) |
| Lefthook | yok | teknik | yok | Go tabanlı git hook yöneticisi; seçenek olarak sunuldu, seçilmedi. | 7:54 | One Go binary, faster, runs jobs in parallel · kanıt: kare (karede: Hook runner seçenekleri listesinde 'Lefthook') |
| Testing Library | yok | teknik | yok | Bileşen testleri için kütüphane; eklenip eklenmeyeceği kullanıcıya soruldu. | 15:40 | Add Testing Library for component tests now? (karede: Test sorusu: 'Add Testing Library for component tests now?' ve 'No, not yet (recommended)') |
| class-validator | yok | teknik | yok | Eski kod tabanında DTO doğrulama kütüphanesi. | 12:24 | argon2, class-validator (karede: Agent Skills sorusunun stack listesinde 'class-validator') |
| Docker | yok | teknik | yok | Yerel Postgres için gerekliydi; makinede çalışmıyordu, veritabanı testleri koşulamadı. | 17:56 | docker: not available (karede: OCR: 'docker: not available' (ekli kare dışı, 17:56)) |
| Remix | yok | teknik | yok | Çatı seçeneği (Remix v3); seçilmedi. | 6:16 | Remix v3 (karede: Framework seçenekleri: 'Remix v3') |
| SvelteKit | yok | teknik | yok | Çatı seçeneği (SvelteKit 2); seçilmedi. Scope örneğinde SQLite ve Fly.io ile birlikte gösterildi. | 6:16 | SvelteKit 2 (karede: Framework seçenekleri: 'SvelteKit 2'; ayrıca 4:12 karesinde 'SvelteKit' örneği) |
| TanStack Start | yok | teknik | yok | Çatı seçeneği; seçilmedi. | 6:16 | TanStack Start (karede: Framework seçenekleri: 'TanStack Start') |
| Auth.js | yok | teknik | yok | NextAuth'un yeni adı; kimlik seçeneği olarak sunuldu, seçilmedi. | 6:18 | Auth.js v6 (formerly NextAuth) (karede: Kimlik seçenekleri: 'Auth.js v6 (formerly NextAuth)') |
| Clerk | yok | teknik | yok | Barındırılan kimlik servisi; seçenek olarak geçti, seçilmedi. | 6:18 | hosted provider such as Clerk or WorkOS · kanıt: kare (karede: Kimlik seçeneği metni: 'such as Clerk or WorkOS') |
| WorkOS | yok | teknik | yok | Barındırılan kimlik ve organizasyon servisi; seçenek olarak geçti, seçilmedi. | 6:18 | hosted provider such as Clerk or WorkOS (karede: Kimlik seçeneği metni: 'such as Clerk or WorkOS') |
| Fly.io | yok | teknik | yok | Barındırma; scope örneğinde SvelteKit ve SQLite ile birlikte geçiyor. | 4:12 | HOSTING Fly.io · kanıt: kare (karede: Karşılaştırma diyagramında 'HOSTING Fly.io') |
| SQLite | yok | teknik | yok | Veritabanı; scope örneğinde geçiyor. | 4:12 | DATABASE SQLite · kanıt: kare (karede: Karşılaştırma diyagramında 'DATABASE SQLite') |
| PostgreSQL | yok | teknik | yok | İlişkisel veritabanı; mimari varsayılanı olarak anılıyor. | 4:08 | PostgreSQL (karede: OCR: 'PostgreSQL' ekran metni (ekli kare dışı, 4:08)) |
| react-beautiful-dnd | yok | teknik | yok | Sürükle-bırak kütüphanesi; landscape kontrolünde kullanımdan kalkmış olarak işaretlendi. | 6:12 | react-beautiful-dnd is deprecated (karede: Landscape kontrolü metni: 'react-beautiful-dnd is deprecated') |
| dnd-kit | yok | teknik | https://www.npmjs.com/package/dnd-kit | Sürükle-bırak alternatifi olarak incelendi; npm paketi. | 6:12 | npmjs.com/package/dnd-kit (karede: Web Fetch satırında 'https://www.npmjs.com/package/dnd-kit' (OCR)) |
| React | yok | teknik | yok | UI kütüphanesi (React 19); proje yığınında. | 15:40 | Next.js 16, React 19 (karede: OCR: 'Stack detected: pnpm, Next.js 16, React 19, TypeScript' (ekli kare dışı, 15:40)) |
| shadcn skill | yok | skill | yok | shadcn/ui için agent skill (.claude/skills/shadcn/). | 6:36 | shadcn (shadcn/ui, .claude/skills/shadcn/) · kanıt: kare (karede: Spec 'Implementation skills' satırı: 'shadcn (shadcn/ui, .claude/skills/shadcn/)') |
| /scope ile issue tracker planı | yok | prompt | yok | Takım için issue tracker: issue oluştur, ata, durum ve öncelik belirle, yorum yap, panoda sürükle, filtre ve arama içeren panel; yalnızca plan aşaması, teknoloji seçimi yok. | 3:12 | kaynak: kare |
| /architect stack & architecture | yok | prompt | yok | Yığın ve mimariyi (framework, veritabanı, veri erişimi, auth) seçenek ve gerekçelerle kararlaştır. | 5:48 | kaynak: kare |
| Planlanmamış tek seferlik istem örneği (çürüme anlatımı) | yok | prompt | yok | Runner için yeni bir servis oluştur, ID ile aramaya izin ver. | 0:02 | kaynak: kare |
## Açıklama bağlantıları
- https://jsm.dev/ai — Agentic Engineering kursu yönlendirme bağlantısı · aday: hayır · Kendi kurs tanıtımı; izleyicinin kullanacağı araç değil · sınıf: diğer
- https://discord.com/invite/n6EdbFJ — Topluluk Discord daveti · aday: hayır · Sosyal topluluk bağlantısı, videoda araç olarak kullanılmıyor · sınıf: diğer
- https://twitter.com/jsmasterypro — Kanal Twitter hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://instagram.com/javascriptmastery — Kanal Instagram hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://linkedin.com/company/javascriptmastery — Kanal LinkedIn sayfası · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://jsmastery.com/skills — JSM Skills deposuna giden sayfa · aday: evet (JSM Skills) · Videoda anlatılan ve kullanılan skill setinin kendisi · sınıf: diğer
- https://jsmastery.com/workflow-guides — İş akışı rehberleri sayfası · aday: hayır · Rehber/doküman sayfası; videoda ayrıca kullanılmıyor, sayfa içeriği doğrulanamadı · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Açık/koyu tema (prefers-color-scheme) | Tema işletim sisteminin ayarından otomatik seçiliyor; koyu set @media ile tanımlanıyor. Tercih saklanmaz. (karede: Spec metni: 'prefers-color-scheme: dark' ve @theme ile koyu set tanımı) | 6:40 | kare |
| Odak halkası (focus ring) | Her odaklanabilir öğenin görünür bir halkası olur; outline:none değiştirilmeden kullanılmaz. (karede: Anahtar kurallar: 'Every focusable element has a visible ring') | 6:58 | kare |
| Duyuru bölgesi (aria-live region) | Uygulamada tek bir canlı bölge bulunur; ekran okuyucuya duyurular bu bölgeden okunur. (karede: Anahtar kurallar: 'There is exactly one live region in the whole app') | 6:58 | kare |
| Hareket azaltma (prefers-reduced-motion) | Kullanıcı hareket azaltmayı seçtiğinde CSS geçişleri ve Radix animasyonları kapatılır. (karede: Spec metni: 'Under prefers-reduced-motion: reduce both CSS transitions') | 6:36 | kare |
| Renk tokenları (design tokens) | Tüm renkler rol tabanlı tokenlar üzerinden gelir; bileşen içinde ham renk yazılmaz. (karede: Spec metni: 'Define role named design tokens in Tailwind v4's @theme') | 6:36 | kare |
| Yazı tipi (Geist, Geist Mono) | Gövde ve kod yazı tipleri Geist ve Geist Mono olarak yüklenir. (karede: Spec metni: 'Load Geist and Geist_Mono in src/app/layout.tsx') | 6:40 | kare |
| Durum simgesi (status glyph) | Issue durumunu şekil ve renkle gösterir; örneğin 'Circle outline, three quarters filled' (İnceleniyor). (karede: Spec tablosu: 'Circle outline, three quarters filled', 'Three bars, the two shortest filled') | 6:42 | kare |
| Öncelik simgesi (priority glyph) | Issue önceliğini üç çubuk şekliyle gösterir (NONE, LOW, MEDIUM, HIGH, URGENT). (karede: Spec tablosu: 'Three bars, the two shortest filled' ve 'Three faint bars, none filled') | 6:42 | kare |
| Issue kartı (issue card) | Kart oluşturulma zamanını '2 days ago' gibi gösterir ve proje anahtarını taşır. (karede: Değer kaynağı tablosu: 'issue-card renders' ve 'TeamProfile.keyPrefix joined to Issue.number') | 6:46 | kare |
| Boş durum (empty state) | Ortalanmış blok; soluk bir Lucide ikonu, tek satır başlık ve isteğe bağlı açıklama içerir. (karede: OCR: 'empty-state : a centred block holding a muted lucide icon' (ekli kare dışı, 6:44)) | 6:44 | kare |
| Yükleme göstergesi (loading state) | Her ekranda bir yükleme durumu gösterilir; spec'te tek bir kural olarak tanımlı. | 3:52 | altyazı |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx skills@latest add jsmastery-pro/skills -a claude-code | JSM skill'lerini Claude Code için .claude/skills altına kurar (karede: README Install: 'npx skills@latest add jsmastery-pro/skills -a claude-code') | 20:28 | kare |
| npx skills@latest add jsmastery-pro/skills | Skill'leri genel .agents/skills klasörüne kurar (Codex vb.) (karede: README Install ikinci komut satırı) | 20:28 | kare |
| npx skills experimental_install | skills-lock.json'dan gitignore'lanmış skill'leri geri yükler (karede: 'A fresh clone restores them with npx skills experimental_install') | 8:16 | kare |
| npx jsm-skills add --all | Tüm skill'leri ekler (OCR okuması) (karede: OCR'de '$ npx jsm-skills add --all'; görsel doğrulanamadı) | 20:54 | kare |
| pnpm test | Vitest birim testlerini çalıştırır (karede: '12 unit passed via pnpm test') | 15:46 | kare |
| pnpm test:e2e | Playwright uçtan uca testlerini çalıştırır (karede: '7 browser flows passed via pnpm test:e2e') | 15:46 | kare |
| pnpm lint && pnpm format:check && pnpm typecheck && pnpm build | Lint, biçim, tip denetimi ve derleme kapılarını çalıştırır (karede: 'Verify steps, all run and passing: pnpm lint, pnpm format:check, pnpm typecheck, pnpm build') | 8:12 | kare |
| /scope, /architect, /develop, /audit, /sync, /check verify, /test, /check review, /document pr, /debug, /clear, /compact | Claude Code sohbetinde skill ve oturum komutları (karede: Sohbet girişlerinde bu slash komutları ve 'Run /clear between units') | 3:12 | kare |
| npx -y create-next-app@latest --help | create-next-app seçeneklerini gösterir. (karede: Terminal satırı 'npx -y create-next-app@latest --help' (OCR, 7:12 karesine yakın)) | 7:42 | kare |
| npm view create-next-app version | create-next-app'in son sürümünü npm'den sorgular. (karede: Terminal satırı 'npm view create-next-app version' (OCR)) | 7:42 | kare |
| git version | Yüklü git sürümünü gösterir (2.51.0). (karede: OCR: 'git version 2.51.0' (ekli kare dışı)) | 7:40 | kare |
| pnpm build | Next.js uygulamasını derler; build exit kodu kontrol edilir. (karede: Doğrulama çıktısı; 'pnpm build' komutu (OCR)) | 14:56 | kare |
| pnpm typecheck / pnpm lint / pnpm format:check | TypeScript tip denetimi, ESLint ve Prettier biçim kontrolü; hepsi çıkış kodu ile doğrulanır. (karede: Doğrulama çıktısında pnpm komutları (OCR)) | 14:56 | kare |
| pnpm test / pnpm test:e2e | Birim (Vitest) ve tarayıcı (Playwright) testlerini çalıştırır; 12 birim ve 7 tarayıcı akışı geçti. (karede: Test çıktısı 'pnpm test' ve 'pnpm test:e2e --reporter=line' (OCR, ekli kare dışı)) | 15:46 | kare |
| prisma migrate deploy | Veritabanı migrasyonlarını uygular; pnpm test öncesi çalıştırılması önerilir. (karede: Rapor metni 'prisma migrate deploy before pnpm test' (OCR, ekli kare dışı)) | 18:40 | kare |
| pnpm exec vitest run src/lib/db/mutations.test.ts -t "serialises two drags" | Tek bir Vitest testini adıyla çalıştırır. (karede: Terminal satırı (OCR, ekli kare dışı)) | 17:48 | kare |
| /scope A team issue tracker: create issues, assign them, set status and priority... | Sohbet içinde scope skill'ini başlatır; ürün fikrini plana dönüştürür. (karede: Claude Code sohbetinde '/scope A team issue tracker: create issue...' komutu) | 3:18 | kare |
| /clear | Oturum bağlamını temizler; her skill arasında önerilir. (karede: Scope plan çıktısında 'Next: /clear, then /architect stack & architecture') | 5:48 | kare |
| /architect stack & architecture | Architect skill'ini stack ve mimari kapsamla çalıştırır. (karede: Sohbette '/architect stack & architecture' komutu) | 5:54 | kare |
| /develop stack & architecture | Develop skill'i ile spec 0001'e göre iskelet kurar. (karede: Sohbette '/develop stack & architecture' komutu) | 7:10 | kare |
| /develop tooling | Araç setini (format, lint, typecheck, commit kancası) kurar. (karede: Sohbette '/develop tooling' komutu) | 7:54 | kare |
| /audit | Mevcut kod tabanını okuyup bağlam dosyalarını üretir. (karede: Sohbette '/audit' komutu ve 'Actualizing...' durumu) | 9:38 | kare |
| /check verify stack & architecture | Uygulamayı çalıştırıp kontrol eder (build, typecheck, lint, format). (karede: Sohbette '/check verify stack & architecture' komutu) | 14:56 | kare |
| /test stack & architecture | Test skill'i ile test paketini yazar ve çalıştırır. (karede: Sohbette '/test stack & architecture' komutu) | 15:40 | kare |
| /check review | Farklı bir modelle kod incelemesi yapar. (karede: Sohbette '/check review' komutu) | 15:50 | kare |
| /document pr | PR açıklaması ve değişiklik kaydını üretir. (karede: Sohbette '/document pr' komutu) | 16:04 | kare |
| /debug system & ui foundation | Hatanın kök nedenini bulur, düzeltir ve regresyon testi yazar. (karede: Girdi kutusunda '/debug system & ui foundation') | 17:24 | kare |
| /sync | Bağlam dosyalarını repo'nun güncel durumuyla eşitler. | 10:02 | altyazı |
| /model | Oturumun modelini değiştirir; kod incelemesi için başka bir model seçilebilir. (karede: İnceleme sonucu metni: 'switch your model with /model' (OCR)) | 17:24 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Plan satırını değiştirmek bedavadır; kod tabanına yayılmış kararı değiştirmek yeniden yazımdır. | 2:50 | öneri |
| scope veritabanı, framework ve kütüphanelere bilerek dokunmaz; yığın ayrı karardır. | 3:50 | özellik |
| architect her değer için kaynağı adlandırır; kaynağı olmayan değer verilmemiş karardır. | 6:43 | özellik |
| develop kaynağı olmayan değerde inşayı reddeder; geçersen varsayım dosyada işaretlenir. | 7:43 | özellik |
| audit mevcut elle yazılmış içeriği ezmez, yalnız boşlukları doldurur ve çelişkileri işaretler. | 10:02 | özellik |
| Skill 15 yıllık PHP kod tabanında da çalışır; JavaScript gerekmez. | 12:30 | özellik |
| Kod incelemesi, kodu yazandan farklı modelle yapılır; çünkü kendi işini inceleyen model kör noktalarını taşır. | 16:30 | özellik |
| Kurs sessiz lansmanda 2 haftada 3.000'den fazla ders kaydetti; 22 Eylül'de herkese açılıyor. | 22:26 | sayısal |
| Skill'ler tamamen açık kaynak, ücretsiz ve tek komutla kurulur. | 20:25 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Ajan çürümesi anlatımı | aday değil: genel kavram | Every feature you add makes the next one harder to build |
| kare 3:12 | Claude Code, Opus 5 (1M) | Claude Code | Panel ve model seçici |
| kare 3:12 | /scope skill | /scope | /scope A team issue tracker |
| konuşma 4:40 | architect skill | /architect | I built the architect skill before any code |
| konuşma 6:43 | develop skill | /develop | develop skill does something you don't expect |
| konuşma 9:02 | Bağlam dosyaları | AGENTS.md | an agent's MD, a claude MD |
| konuşma 10:02 | audit ve sync skill | /audit | sync skill will reconcile those files |
| konuşma 12:30 | 15 yıllık PHP kod tabanı | aday değil: genel kavram | pointed at a 15-year-old PHP codebase |
| kare 6:12 | better-auth sayfası | Better Auth | Web Fetch better-auth |
| kare 6:12 | dnd-kit sayfası | aday değil: başka adayın parçası (/architect) | Web Fetch dnd-kit; sürükle bırak kütüphane kontrolü |
| kare 6:12 | react-beautiful-dnd kullanımdan kalkmış | aday değil: başka adayın parçası (/architect) | Landscape check sonucu |
| kare 6:36 | shadcn, tailwind-4-docs, web-design-guidelines, next-dev-loop, playwright-cli skill'leri | shadcn/ui | Implementation skills satırı |
| kare 6:40 | Geist fontu | Geist | Geist ve Geist_Mono |
| kare 6:44 | Lucide ve Sonner | Lucide | muted lucide icon; Sonner |
| kare 7:54 | Lefthook seçeneği | aday değil: başka adayın parçası (/develop) | Husky'ye alternatif olarak sunuldu, seçilmedi |
| kare 7:54 | Husky ve lint-staged | Husky | Husky plus lint-staged (recommended) |
| kare 8:12 | Prettier, ESLint, GitHub Actions | Prettier | Tooling tablosu |
| kare 12:20 | NestJS README | NestJS | nestjs.com bağlantısı |
| kare 12:32 | Neon MCP, drizzle-docs, drizzle-mcp | Neon | Öneri listesi |
| kare 12:52 | 4 kurulu skill | nestjs-best-practices | Installed skills satırı |
| kare 12:24 | Resend, argon2 | Resend | NestJS yığını listesi |
| kare 15:46 | Vitest ve Playwright testleri | Playwright | 12 unit ve 7 browser flow |
| kare 17:24 | Claude Sonnet 5 incelemesi | Claude Sonnet 5 | reviewed by Claude Sonnet 5 |
| kare 20:28 | npx skills README | Skills CLI | Uses npx skills |
| kare 20:28 | Gemini CLI, Cursor, Codex uyumluluk listesi | aday değil: genel kavram | Yalnızca desteklenen istemci listesi, kullanılmadı |
| kare 20:56 | Kurs sayfası (Linear, Vercel, Adidas logoları) | aday değil: sponsor/reklam | Kurs tanıtım sayfası logoları |
| konuşma 22:26 | Agentic Engineering kursu | aday değil: sponsor/reklam | opens to everyone on September 22nd |
| açıklama | Discord, Twitter, Instagram, LinkedIn, jsm.dev/ai | aday değil: konu dışı | Açıklama bağlantıları |
| açıklama | jsmastery.com/skills | JSM Skills | Skill deposu sayfası |
| yorum | SpecKit, Notegpt, Codex, Cursor, Astro, fallow | aday değil: konu dışı | İzleyici yorumlarında anıldı, videoda gösterilmedi |
| linkli sayfa | Tailwind docs, gitignore, nestjs.com sponsor logoları | aday değil: başka adayın parçası (Tailwind CSS) | Bağlantılı sayfalar; sponsor listeleri konu dışı |
## Kareden okunanlar
- 3:12: Claude Code paneli, Opus 5 (1M) High, 'Learn Claude Code' kontrol listesi
- 3:30: /scope sorusu: MVP, Tenancy, Money, Purpose sekmeleri; 'Board plus issues' önerilen
- 4:00: Approach sekmesi: Tracer Bullet (önerilen), Skateboard, Journey, Facade
- 6:12: Web Fetch dnd-kit, better-auth, vitest, tailwindcss; react-beautiful-dnd kullanımdan kalkmış
- 6:16: Framework seçenekleri: Next.js 16 (önerilen), Remix v3, SvelteKit 2, TanStack Start
- 6:40: Font bağlama: Geist ve Geist_Mono, globals.css'te @theme inline takma adları
- 8:16: CI hiç çalışmadı; kurulu skill'ler gitignore, skills-lock.json commit'li
- 12:32: Neon MCP, drizzle-docs, drizzle-mcp önerileri ve Neon skill'i
- 15:50: Author model sorusu: opus, sonnet, fable
- 20:28: README: npx skills@latest add jsmastery-pro/skills; Claude Code, Cursor, Codex, Gemini CLI uyumlu
- 20:56: Kurs sayfası: 'The Ultimate AI Engineering Course', 120 developers already inside
## Belirsizlikler
- Video yalnızca issue tracker (Next.js) ve NestJS auth sunucusunu gösteriyor; konuşmadaki 15 yıllık PHP kod tabanı ekranda görünmüyor.
- Sözlük eşleşmeleri (Three.js, Matter.js, Meshy, Notion, taste-skill, TestSprite, claude-mem, context7 vb.) ses tanıma hatası; videoda geçmiyor, aday yapılmadı.
- 'fable' model seçeneği yalnızca author model menüsünde görünüyor; kullanılmadı.
- Kare listesindeki Linear, Gemini, OpenAI, Vue, Docker, Svelte, Redis ve benzerleri menü, kurs sayfası ya da listede geçiyor; araç olarak kullanılmadı.
- Review ekranında 'Review will run on opus' ve 'sonnet' ifadeleri çelişkili; sonuçta Claude Sonnet 5 incelemesi görünüyor.
- npx jsm-skills add --all yalnız OCR'den; karede doğrulanamadı.
- Yorumlardaki Notegpt, fallow, SpecKit, Astro, Cursor, Codex gibi adlar videoda gösterilmedi.
- Site/landing içeriği kurulan uygulama değil, tasarım spec'i olarak görünür; site_ui boş bırakıldı.
## Atlanan segment oranı
0/26 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://jsm.dev/ai | açıklama | açıklama | hayır |
| https://discord.com/invite/n6EdbFJ | açıklama | açıklama | hayır |
| https://twitter.com/jsmasterypro | açıklama | açıklama | hayır |
| https://instagram.com/javascriptmastery | açıklama | açıklama | hayır |
| https://linkedin.com/company/javascriptmastery | açıklama | açıklama | hayır |
| https://jsmastery.com/skills | açıklama | açıklama | evet |
| https://jsmastery.com/workflow-guides | açıklama | açıklama | hayır |
| https://github.com/neondatabase/mcp-server-neon | 12:32 | ekran | evet |
| https://github.com/Michael-Obele/drizzle-docs | 12:32 | ekran | evet |
| github.com/defrex/drizzle-mcp | 12:32 | ekran | evet |
| https://www.npmjs.com/package/better-auth | 6:12 | ekran | evet |
| https://www.npmjs.com/package/vitest | 6:12 | ekran | evet |
| https://tailwindcss.com/docs | 6:12 | ekran | evet |
| https://www.npmjs.com/package/dnd-kit | 6:12 | ekran | evet |
| http://nestjs.com/ | 12:20 | ekran | evet |
| http://localhost:3000/ | 15:04 | ekran | hayır |
| university-library-murex.vercel.app | 21:36 | ekran | hayır |
| jsmastery.com | 20:16 | ekran | hayır |
| https://github.com/jsmastery-pro/skills | 20:16 | ekran | evet |
| https://help.github.com/articles/ignoring-files/ | 8:02 | ekran | hayır |
| https://nestjs.com/img/logo-small.svg | 12:20 | ekran | hayır |
| localhost:3000/_next/webpack-hmr | 15:28 | ekran | hayır |
| db.prisma.io | 18:04 | ekran | hayır |
## İş akışı
- 1. adım — /scope ile fikri röportajla planlamak: MVP, kiracılık, amaç, yetenekler, yaklaşım (Tracer Bullet) seçimi — araçlar: Claude Code, /scope, Opus 5 (1M)
- 2. adım — Scope çıktısını docs/scope/scope.md olarak yazmak (14 özellik, 9 ertelenmiş) — araçlar: /scope
- 3. adım — /architect ile yığın kararı: framework, veritabanı, veri erişimi, auth, git ve ortam; kütüphane kontrolü için web fetch — araçlar: /architect, Next.js, Better Auth, Vitest, Tailwind CSS
- 4. adım — Tasarım sistemi spec'ini (0003) yazmak: tokenlar, Geist fontu, durum glifleri — araçlar: /architect, Tailwind CSS, shadcn/ui, Geist
- 5. adım — /develop ile iskeleti kurmak, doğrulama adımlarını verify.md'ye kaydetmek — araçlar: /develop, pnpm
- 6. adım — /develop tooling: Prettier, ESLint, Husky, lint-staged ve CI kurmak — araçlar: /develop, Prettier, ESLint, Husky, lint-staged, GitHub Actions
- 7. adım — /audit ile mevcut projeyi okuyup AGENTS.md ve CLAUDE.md üretmek — araçlar: /audit
- 8. adım — Eski/mevcut NestJS projesinde /audit çalıştırıp skill ve MCP aramak, 4 skill kurmak — araçlar: /audit, NestJS, Drizzle ORM, Neon, Skills CLI
- 9. adım — Mevcut koda göre /scope ile sonraki dilimi planlamak — araçlar: /scope
- 10. adım — /check verify ile gerçek uygulamayı sürüp doğrulamak — araçlar: /check verify, pnpm
- 11. adım — /test ile 19 test yazıp çalıştırmak — araçlar: /test, Vitest, Playwright
- 12. adım — /check review ile farklı modelde inceleme, bulguları sıralamak — araçlar: /check review, Claude Sonnet 5
- 13. adım — /document pr ile PR açıklaması yazmak — araçlar: /document, git
- 14. adım — /debug ile bulguları kök nedene göre düzeltmek (CI, yetki kodları, kilit) — araçlar: /debug, Prisma, pnpm
- 15. adım — Skill'leri npx skills ile kurmak ve kursu tanıtmak — araçlar: Skills CLI, JSM Skills
## Promptlar
- /scope ile issue tracker planı — Takım için issue tracker: issue oluştur, ata, durum ve öncelik belirle, yorum yap, panoda sürükle, filtre ve arama içeren panel; yalnızca plan aşaması, teknoloji seçimi yok.
- /architect stack & architecture — Yığın ve mimariyi (framework, veritabanı, veri erişimi, auth) seçenek ve gerekçelerle kararlaştır.
- Planlanmamış tek seferlik istem örneği (çürüme anlatımı) — Runner için yeni bir servis oluştur, ID ile aramaya izin ver.
ikinci göz KAPALI: --ikinci-goz yok
