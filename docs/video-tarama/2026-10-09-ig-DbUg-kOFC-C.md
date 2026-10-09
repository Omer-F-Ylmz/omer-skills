# AI-powered job applications that run entirely on your own machine. Fork it, fill
## Künye
AI-powered job applications that run entirely on your own machine. Fork it, fill · gittrend.io · süre: 0:46 · ? · https://www.instagram.com/reel/DbUg-kOFC-C/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-38 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 17525 tk · claude-haiku-5-5: claude-haiku-5-5 · 63294 tk
## Özet
AI Job Search, Claude Code üzerinde çalışan, kendi bilgisayarında koşan ücretsiz bir iş başvurusu çerçevesidir. İş ilanını uygunluk açısından değerlendirir, CV'yi uyarlar ve LaTeX ile ilana özel ön yazı hazırlar. İkinci bir yapay zekâ ajanı çıktıyı inceler. Mülakat hazırlığı için de özel bir çalışma paketi üretir. Videoda GitHub README'si gösteriliyor: depoyu fork'la, /setup ile profili doldur, /scrape ile ilan bul, /apply ile başvuru üret. Geliştirici aynı iş akışıyla AI mühendisi olarak işe girmiş.
## Bölümler
- 0:00 Projeye giriş ve README
- 0:08 Çalışma akışı: setup, scrape, apply
- 0:13 Gereksinimler (Claude Code, Python, Bun, LaTeX)
- 0:19 Hızlı başlangıç: fork ve kurulum
- 0:27 /apply komutu
- 0:31 /interview, /outcome, /notion-sync, /gmail-sync
- 0:39 Kimler için ve ek komutlar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| AI Job Search | yok | iş akışı | https://github.com/MadsLorentzen/ai-job-search | Claude Code üzerinde çalışan, yerel iş başvurusu çerçevesi | 0:00 | AI Job Search is a free framework that runs job applications on your own computer |
| Claude Code | yok | CLI | yok | Çerçevenin üzerinde çalıştığı ana yapay zekâ kodlama aracı | 0:00 | runs job applications on your own computer using Claude Code |
| Claude | yok | CLI | yok | İlanları değerlendiren ve başvuruyu yazan model | 0:00 | README: let Claude evaluate job postings, tailor your CV (karede: kanıttan) README: let Claude evaluate job postings, tailor your CV |
| GitHub | yok | CLI | yok | Depo barındırma ve fork | 0:00 | Tarayıcı sekmesi GitHub - MadsLorentzen (karede: kanıttan) Tarayıcı sekmesi GitHub - MadsLorentzen |
| LaTeX | yok | teknik | yok | CV ve ön yazı çıktı biçimi | 0:00 | tailors your CV and writes a cover letter specific to that role, all in latex |
| lualatex | yok | CLI | yok | CV derleyicisi | 0:14 | OCR: The CV compiles with lualatex |
| xelatex | yok | CLI | yok | Ön yazı derleyicisi (cover.cls fontspec ister) | 0:14 | OCR: cover letter compiles with xelatex |
| Bun | yok | CLI | yok | İş arama CLI araçları için çalışma ortamı | 0:14 | Prerequisites: Bun (for job search CLI tools) (karede: kanıttan) Prerequisites: Bun (for job search CLI tools) |
| Python | yok | CLI | yok | Gereksinim: Python 3.10+ | 0:13 | Prerequisites listesinde Python 3.10+ (karede: kanıttan) Prerequisites listesinde Python 3.10+ |
| TypeScript | yok | teknik | yok | CLI araçlarının dili | 0:23 | Açıklama etiketi #typescript; OCR: bun install only pulls TypeScript |
| poppler | yok | CLI | yok | pdftotext ile ATS okunabilirlik kontrolü | 0:16 | Optional: pdftotext from poppler, used by /apply's ATS check (karede: kanıttan) Optional: pdftotext from poppler, used by /apply's ATS check |
| MiKTeX | yok | CLI | yok | LaTeX dağıtımı seçeneği | 0:14 | OCR: TeX Live, MacTeX, TinyTeX, or MiKTeX |
| Notion MCP | yok | MCP | yok | /notion-sync ile hattın salt okunur görünümünü Notion'a yayınlar | 0:35 | OCR: via the official Notion MCP server (OAuth, no API keys) |
| GitHub CLI | yok | CLI | yok | gh repo fork ile depoyu fork'lar | 0:19 | OCR: gh repo fork MadsLorentzen/ai-job-search --clone · kanıt: yok |
| /setup | yok | skill | yok | Profil dosyalarını oluşturur | 0:23 | OCR: /setup offers three paths |
| /scrape | yok | skill | yok | İş portallarında ilan arar | 0:08 | Akış şemasında /scrape: Search job portals (karede: kanıttan) Akış şemasında /scrape: Search job portals |
| /apply | yok | skill | yok | Uyarlanmış CV ve ön yazı üretir | 0:08 | Akış şemasında /apply <url>: Evaluate fit (karede: kanıttan) Akış şemasında /apply <url>: Evaluate fit |
| /interview | yok | skill | yok | Mülakat hazırlık paketi | 0:31 | OCR: /interview preps you for a scheduled interview |
| /outcome | yok | skill | yok | Başvuru sonuçlarını kaydeder | 0:32 | OCR: /outcome records what happened to an application |
| /notion-sync | yok | skill | yok | Hattı Notion'a yayınlar | 0:35 | OCR: /notion-sync publishes a one-way, read-only view |
| /gmail-sync | yok | skill | yok | Gmail'den başvuru durum sinyallerini okur | 0:38 | OCR: /gmail-sync reads your ... for status signals |
| /html-report | yok | skill | yok | Satır içi SVG grafikli HTML panosu üretir | 0:41 | OCR: /html-report generates a self-contained HTML dashboard |
| /expand | yok | skill | yok | Profili GitHub, portfolyo vb. kaynaklarla zenginleştirir | 0:41 | OCR: /expand enriches ... linked in it (GitHub repos, portfolio site) |
| /upskill | yok | skill | yok | İlanlardan öncelikli beceri geliştirme listesi çıkarır | 0:40 | OCR: single posting via /upskill <URL> |
| Gemini CLI | yok | CLI | yok | README'de alternatif ajan aracı olarak anılıyor; bu videoda gösterilmiyor. | 0:13 | Using a different agent tool (Codex, Antigravity, Gemini CLI) · kanıt: kare (karede: OCR (0:13): aynı satır, 'Gemini CLI' ifadesi) |
| Antigravity | yok | teknik | yok | README'de alternatif ajan aracı olarak anılıyor; bu videoda gösterilmiyor. | 0:13 | Using a different agent tool (Codex, Antigravity, Gemini CLI) (karede: OCR (0:13): aynı satır, 'Antigravity' ifadesi) |
| AGENTS.md | yok | teknik | yok | Ajanın başlangıç noktası olan talimat dosyası; portal arama becerileri burada çalışıyor. | 0:13 | Start at AGENTS.md - the portal search skills work there out of the box (karede: OCR (0:13): 'Start at AGENTs.md' satırı) |
| TeX Live | yok | teknik | yok | LaTeX dağıtımı seçeneklerinden biri olarak listeleniyor. | 0:14 | TeX Live, MacTeX, TinyTeX, or MiKTeX (karede: OCR (0:14): 'TeX Live, MacTeX, TinyTeX, or' dağıtım seçenekleri) |
| MacTeX | yok | teknik | yok | macOS için LaTeX dağıtımı seçeneği olarak listeleniyor. | 0:14 | TeX Live, MacTeX, TinyTeX, or MiKTeX (karede: OCR (0:14): dağıtım seçenekleri listesinde 'MacTeX') |
| TinyTeX | yok | teknik | yok | Hafif LaTeX dağıtımı; minimal kurulum olarak öneriliyor. | 0:14 | TinyTeX or BasicTeX, install the extra packages (karede: Önkoşullar: 'TinyTeX' seçeneği ve minimal kurulum notu) |
| BasicTeX | yok | teknik | yok | Minimal LaTeX dağıtımı; ek paketler elle kurulmalı. | 0:15 | minimal TeX install such as TinyTeX or BasicTeX (karede: OCR (0:15): 'minimal TeX install such as TinyTeX or BasicTeX') |
| fontspec | yok | teknik | yok | XeLaTeX/LuaLaTeX için yazı tipi yönetim paketi; cover.cls bunu gerektiriyor. | 0:14 | cover.cls requires fontspec · kanıt: kare (karede: Önkoşullar: 'cover.cls requires fontspec') |
| fontawesome5 | yok | teknik | yok | LaTeX ikon yazı tipi paketi; MiKTeX'te font-expansion hatası veriyor. | 0:14 | MiKTeX installs with fontawesome5 font-expansion errors (karede: Önkoşullar: 'fontawesome5 font-expansion errors' notu) |
| pdftotext | yok | CLI | yok | /apply'ın derlenmiş CV üzerinde ATS okunabilirlik kontrolü için kullandığı metin çıkarma aracı. | 0:16 | used by /apply 's ATS parseability check on the compiled CV (karede: Önkoşullar: 'used by /apply's ATS parseability check on the compiled CV') |
| Homebrew | yok | CLI | yok | macOS paket yöneticisi; poppler'ı 'brew install poppler' ile kurmak için kullanılıyor. | 0:16 | macOS: brew install poppler · kanıt: kare (karede: Önkoşullar: 'macOS: brew install poppler') |
| apt | yok | CLI | yok | Debian/Ubuntu paket yöneticisi; poppler-utils'i kurmak için kullanılıyor. | 0:18 | Debian/Ubuntu: apt install poppler-utils (karede: Önkoşullar: 'Debian/Ubuntu: apt install poppler-utils') |
| Chocolatey | yok | CLI | yok | Windows paket yöneticisi; poppler'ı 'choco install poppler' ile kurmak için kullanılıyor. | 0:18 | Windows: choco install poppler · kanıt: kare (karede: Önkoşullar: 'Windows: choco install poppler') |
| Jobindex | yok | teknik | yok | Danimarka iş ilanı sitesi; /apply örneğinde ilan URL'si olarak ve iş portalı becerilerinde geçiyor. | 0:08 | (Jobindex, Jobnet, Akademikernes Jobbank, etc.) (karede: 'What this is' bölümü: 'built for the Danish market (Jobindex, Jobnet, Akademikernes Jobbank)') |
| SVG | yok | teknik | yok | /html-report'un dış bağımlılık olmadan grafik çizmek için kullandığı inline vektör formatı. | 0:41 | generates a self-contained HTML dashboard ... (inline SVG, no external dependencies) (karede: OCR (0:41): 'inline SVG, no external dependencies' ifadesi) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| gh repo fork MadsLorentzen/ai-job-search --clone | Depoyu fork'lar ve klonlar | 0:26 | kare |
| bun install | Bağımlılıkları kurar | 0:19 | kare |
| (cd .agents/skills/Stool/cli && bun install) | Skill CLI aracının bağımlılıklarını kurar (OCR bulanık) | 0:20 | kare |
| brew install poppler | macOS'ta pdftotext için poppler kurar (karede: Prerequisites bölümünde (macOS: brew install poppler)) | 0:16 | kare |
| apt install poppler-utils | Debian/Ubuntu'da poppler kurar | 0:18 | kare |
| choco install poppler | Windows'ta poppler kurar | 0:18 | kare |
| /setup | Profili tek komutla doldurur (karede: Akış şemasında /setup: Fill in your profile) | 0:23 | kare |
| /scrape | İş portallarında ilan arar (karede: Akış şemasında /scrape: Search job portals) | 0:08 | kare |
| /apply https://jobindex.dk/job/1234567 | URL'den uyarlanmış başvuru üretir | 0:27 | kare |
| /apply <paste the full job description here> | İlan metnini yapıştırarak başvuru üretir | 0:28 | kare |
| (cd .agents/skills/…/cli && bun install) | Skill CLI klasörüne geçip bağımlılıkları kurar (dizin adı OCR'da bozuk). (karede: OCR (0:20): '(cd .agents/skills/Stool/cli && bun install)' satırı) | 0:20 | kare |
| /interview | Planlanmış mülakat için şirket araştırması ve çalışma paketi üretir. (karede: OCR (0:31): '/interview preps you for a scheduled interview') | 0:31 | kare |
| /outcome | Başvurunun sonucunu kaydeder. (karede: OCR (0:32): '/outcome records what happened to an application') | 0:32 | kare |
| /notion-sync | Pipeline'ı Notion veritabanına salt okunur aktarır. (karede: OCR (0:35): '/notion-sync publishes a one-way, read-only view') | 0:35 | kare |
| /gmail-sync | Gmail'den başvuru durum sinyallerini okur. (karede: OCR (0:38): '/gmail-syne' (muhtemelen /gmail-sync)) | 0:38 | kare |
| /upskill <URL> | İlan için beceri açıklarını öncelikli listeler. (karede: OCR (0:40): '/upskil1 <uRL>' (muhtemelen /upskill <URL>)) | 0:40 | kare |
| /expand | Profili kaynaklardan zenginleştirir. (karede: OCR (0:41): '/expand enriche...' satırı) | 0:41 | kare |
| /html-report | Tek dosyalı HTML panosu üretir. (karede: OCR (0:41): '/html-report generates a self-contained HTML dashboard') | 0:41 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Altmış dokuz uyarlanmış başvuru, yirmi ilk mülakat ve bir imzalı sözleşme elde edildi. | 0:02 | sayısal |
| İkinci bir yapay zekâ ajanı her şeyi siz görmeden önce inceler. | 0:13 | özellik |
| Kişisel verileri üçüncü taraf servise yüklemek istemeyenler için uygundur. | 0:39 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | AI Job Search | AI Job Search | AI Job Search is a free framework |
| konuşma 0:00 | Claude Code | Claude Code | using Claude Code |
| konuşma 0:00 | LaTeX | LaTeX | all in latex |
| konuşma 0:00 | İkinci yapay zekâ ajanı (reviewer) | aday değil: başka adayın parçası (AI Job Search) | A second AI agent reviews everything |
| konuşma 0:00 | Mülakat çalışma paketi | /interview | building a custom study pack |
| konuşma 0:00 | /scrape ve /apply | /apply | run scrape ... slash apply with a URL |
| açıklama | gittrend.io | aday değil: konu dışı | More like this → gittrend.io |
| açıklama | TypeScript | TypeScript | #typescript |
| açıklama | #opensoource #github #ai #jobsearch #career #productivity | aday değil: genel kavram | hashtag listesi |
| kare 0:00 | Trendshift rozeti | aday değil: konu dışı | #1 Repository Of The Day |
| kare 0:00 | Anthropic | aday değil: konu dışı | not affiliated with Anthropic |
| kare 0:08 | Ko-fi / Buy me a coffee | aday değil: konu dışı | Buy me a coffee |
| kare 0:08 | LinkedIn | aday değil: konu dışı | full application funnel, is on LinkedIn |
| kare 0:16 | Bun | Bun | Bun (for job search CLI tools) |
| kare 0:16 | Python | Python | Python 3.10+ |
| kare 0:16 | poppler | poppler | pdftotext from poppler |
| kare 0:16 | Codex, Antigravity, Gemini CLI | aday değil: konu dışı | Using a different agent tool (Codex, Antigravity, Gemini CLI) |
| ekran 0:13 | MiKTeX, TinyTeX, TeX Live, MacTeX | MiKTeX | LaTeX distribution: TeX Live, MacTeX, TinyTeX, or MiKTeX |
| ekran 0:14 | lualatex / xelatex | lualatex | CV compiles with lualatex |
| ekran 0:19 | gh repo fork | GitHub CLI | gh repo fork MadsLorentzen/ai-job-search --clone |
| ekran 0:35 | Notion MCP server | Notion MCP | official Notion MCP server |
| ekran 0:27 | jobindex.dk | aday değil: konu dışı | /apply https://jobindex.dk/job/1234567 örnek URL |
| ekran 0:23 | /setup | /setup | /setup offers three paths |
| ekran 0:32 | /outcome | /outcome | /outcome records what happened |
| ekran 0:35 | /notion-sync | /notion-sync | /notion-sync publishes a one-way |
| ekran 0:38 | /gmail-sync | /gmail-sync | /gmail-sync reads your ... |
| ekran 0:41 | /html-report | /html-report | /html-report generates a self-contained HTML dashboard |
| ekran 0:41 | /expand | /expand | /expand enriches |
| ekran 0:40 | /upskill | /upskill | /upskill <URL> |
| ekran 0:00 | GitHub | GitHub | GitHub - MadsLorentzen |
| ekran 0:23 | bun install | Bun | bun install only pulls TypeScript |
| ekran 0:45 | CLAUDE.md | Claude Code | CLAUDE.md dosya adı |
## Kareden okunanlar
- 0:00: GitHub README: AI Job Search, #1 Repository Of The Day (Trendshift), CI passing, MIT license
- 0:08: README 'Does it actually work?' bölümü ve Buy me a coffee düğmesi
- 0:16: Akış şeması /setup, /scrape, /apply ve Prerequisites listesi (Claude Code, Python 3.10+, Bun, LaTeX, poppler)
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- OCR gürültülü; /gmail-sync, /upskill ve Stool/cli yolu kısmen tahmin.
- Sözlükteki Three.js, Descript, Make, Syne, Inter, 21st eşleşmeleri OCR hatası; videoda kullanılmıyor.
- Codex, Antigravity, Gemini CLI yalnızca alternatif ajan aracı olarak README'de anılıyor, kullanılmıyor.
- Videoda gittrend.io açıklamada geçer, araç olarak gösterilmez.
- Ko-fi ve LinkedIn bağlantıları README'de anılıyor, kullanılmıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/MadsLorentzen/ai-job-search#readme | 0:00 | ekran | evet |
| https://jobindex.dk/job/1234567 | 0:27 | ekran | evet |
| gittrend.io | açıklama | açıklama | evet |
## İş akışı
- 1. adım — Repoyu kendi hesabına fork'layıp yerel olarak klonlamak. — araçlar: GitHub CLI (gh), GitHub
- 2. adım — Önkoşulları kurmak: Python 3.10+, Bun, LaTeX dağıtımı ve isteğe bağlı poppler. — araçlar: Python, Bun, MiKTeX, TinyTeX, BasicTeX, Homebrew, apt, Chocolatey
- 3. adım — Çerçevenin CLI araçlarının bağımlılıklarını kurmak (ana dizin ve skill CLI klasörü). — araçlar: bun install, Bun, TypeScript
- 4. adım — Claude Code'u açıp /setup ile profil dosyalarını doldurmak; documents klasörünü okutmak. — araçlar: Claude Code, /setup
- 5. adım — Yapıştırılan CV ya da mülakat ile profil oluşturma seçeneklerini değerlendirmek. — araçlar: Claude Code, /setup
- 6. adım — /scrape ile iş portallarında ilan aramak ve uyum puanlı eşleşmeleri listelemek. — araçlar: /scrape, Jobindex
- 7. adım — Seçilen ilan URL'si ya da metniyle /apply çalıştırıp uyum değerlendirmesi ve CV/ön yazı üretmek. — araçlar: /apply, Claude, Jobindex
- 8. adım — CV'yi lualatex, ön yazıyı xelatex ile derlemek. — araçlar: LuaLaTeX, XeLaTeX, fontspec, LaTeX
- 9. adım — Derlenen CV üzerinde ATS okunabilirlik kontrolü yapmak. — araçlar: pdftotext, poppler
- 10. adım — İkinci bir ajanla taslağı eleştirmek ve son çıktıya revize etmek. — araçlar: AI Job Search, /apply
- 11. adım — Planlanmış bir mülakat için /interview ile hazırlık paketi oluşturmak. — araçlar: /interview, Claude Code
- 12. adım — /outcome ile başvurunun sonucunu (aşamalar, teklif, red) kaydetmek. — araçlar: /outcome
- 13. adım — /notion-sync ile pipeline'ı Notion veritabanına tek yönlü aktarmak. — araçlar: /notion-sync, Notion MCP, OAuth
- 14. adım — /gmail-sync ile Gmail'den başvuru durum sinyallerini okumak. — araçlar: /gmail-sync, Gmail
- 15. adım — /expand ile profili zenginleştirmek ve /upskill ile beceri açıklarını bulmak. — araçlar: /expand, /upskill
- 16. adım — /html-report ile durum, sektör ve huni grafiklerinden HTML panosu üretmek. — araçlar: /html-report, SVG
- 17. adım — CLI skill iskeletini aynı yapıya göre oluşturmak (komut ayrıntısı okunamadı). — araçlar: Claude Code, CLAUDE.md
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
