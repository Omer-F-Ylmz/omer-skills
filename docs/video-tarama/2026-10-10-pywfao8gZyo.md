# Vibe Coding Bitti: Ölçülebilir AI Uygulaması Yazmanın Yolu
## Künye
Vibe Coding Bitti: Ölçülebilir AI Uygulaması Yazmanın Yolu · Emrullah Yaprak | AI & Automation · süre: 25:11 · tr · https://youtu.be/pywfao8gZyo · şema 2
motor: parti 2026-10-10-short-15 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (54)
kareler: girdi ≤40000 jeton için 60→54
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 112737 tk
## Özet
Emrullah Yaprak, AI'dan yarım kod almamak için üç temeli (PRD, Brand kit/DESIGN.md, Plan Modu + Execution) tek akışta anlatıyor ve bunu canlı olarak QR dijital menü uygulamasında uyguluyor. Akış: prd-yaz skill'iyle PRD üretimi ve seçenekli sorular, Open Design ile DESIGN.md, CLAUDE.md'ye tasarım kuralı ekleme, Plan Modu ile görev listesi, Sonnet 4.6 ile execution, Docker'da PostgreSQL ve admin panelinde test. Sonuçta çalışan menü ve admin paneli gösteriliyor; bazı hatalar iterasyonla düzeltiliyor. Kapsam dışı ve ölçülebilir kabul kriterlerinin önemi vurgulanıyor. Canlıya alma (deploy) yalnızca bir sonraki videoya yönlendirme olarak geçiyor.
## Bölümler
- 0:00 Neden AI'dan Yarım Kod Alıyoruz? Üç Temel Nedir?
- 2:00 Temel 1: PRD Nedir, Neden Önemli ve Kabul Kriterleri
- 4:33 Temel 2: Brandkit ile Tutarlı Görsel Kimlik
- 6:23 Temel 3: Plan Modu + Execution ve Doğrulama
- 8:05 Canlı Demo: prd-yaz Skill Kurulumu ve PRD Oluşturma
- 15:08 Open Design ile Brandkit Oluşturma ve DESIGN.md
- 17:00 Plan Modu ile Kodlama ve Sonuçların İncelenmesi
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Anthropic'in terminal tabanlı kodlama ajanı; PRD, plan ve execution bu araçta çalıştırıldı. | 10:08 | Ekranda 'Claude Code v2.1.183' başlığı ve claude oturumu. (karede: Terminalde Claude Code v2.1.183 açılış ekranı, Sonnet 4.6 + Claude Max bilgisi.) |
| prd-yaz | yok | skill | https://github.com/eyaprak/skills | Fikri adım adım sorgulayıp kod tabanını tarayarak prd.md üreten skill; Matt Pocock'un write-a-prd skill'inden Türkçeye uyarlanmış. | 9:24 | SKILL.md dosyasında 'name: prd-yaz' ve description alanı; açıklamada atıf. (karede: GitHub'da prd-yaz/SKILL.md dosyası; name: prd-yaz ve uzun description metni görünüyor.) |
| Open Design | yok | teknik | yok | Açık kaynak, ücretsiz 'Claude Design alternatifi' tasarım aracı; DESIGN.md (brand kit) üretmek için kullanıldı. | 15:08 | 'Open Design aslında açık kaynaklı ve tamamen ücretsiz bir tasarım oluşturma aracı.' |
| DESIGN.md | yok | teknik | yok | Renk paleti, tipografi, bileşen ve ton kurallarını tek dosyada tutan tasarım sistemi dosyası. | 16:09 | 'Design MD dosyasını ... projenin içerisine dahil edeceğiz.' |
| CLAUDE.md | yok | teknik | yok | Claude Code'un her oturumda otomatik okuduğu proje kuralı dosyası; tasarım kuralı buraya eklendi. | 17:00 | 'Clot MD neydi? Her session'da yüklenen.' |
| Plan Modu | yok | teknik | yok | Claude Code'un salt okunur plan modu (Shift+Tab); kod yazmadan plan çıkarıp onay bekler. | 6:23 | 'Plan modumuz çok önemli ... Shift tabile açılır. Siz onaylayana kadar kod yazmaz.' |
| AskUserQuestion | yok | teknik | yok | Claude Code'un seçenekli soru aracı; prd-yaz soruları bu araçla seçim kutularında sordu. | 11:00 | Ekranda 'askuserquestion tool kullan sorular için' ve '1. Next.js + Supabase (Recommended)' seçenekleri. (karede: Claude Code'da seçenekli soru ekranı: 'Hangi teknoloji stack'i tercih edersin?' ve '1. Next.js + Supabase (Recommended)' seçeneği.) |
| Git | yok | CLI | yok | Sürüm kontrol aracı; skills reposunu klonlamak için kullanıldı. | 8:08 | git-scm.com install sayfası ve 'git clone' komutu. (karede: Tarayıcıda 'git - Install' sayfası (git-scm.com/install) açık.) |
| GitHub | yok | teknik | https://github.com/eyaprak/skills | Skills reposunun barındırıldığı platform; skill dosyaları buradan incelendi ve indirildi. | 8:10 | github.com/eyaprak/skills reposu ekranı ve yıldız verme. (karede: github.com/eyaprak/skills reposu; README'de 'Claude Code skill'lerinin toplandığı repo' yazıyor.) |
| Docker | yok | CLI | yok | Konteyner aracı; docker compose ile yerel PostgreSQL konteyneri çalıştırıldı. | 20:06 | PowerShell'de 'docker compose ps' çıktısı ve postgres:16-alpine. (karede: PowerShell'de docker compose ps çıktısı; postgres:16-alpine imajlı db servisi görünüyor.) |
| PostgreSQL | yok | teknik | yok | Uygulamanın veritabanı; Docker konteynerinde (postgres:16-alpine) çalıştırıldı. | 20:06 | Docker konteyneri 'postgres:16-alpine' olarak listeleniyor. (karede: Docker çıktısında postgres:16-alpine imajı ve db konteyneri 'Up' durumunda.) |
| Prisma | yok | teknik | yok | Şema tanımı, migration ve seed için ORM; npx prisma migrate dev ile kullanıldı. | 19:12 | 'npx prisma migrate dev && npm run seed' komutu ve Prisma şeması planı. (karede: Plan çıktısında 'npx prisma migrate dev && npm run seed' komutu yazıyor.) |
| Next.js 16 | yok | teknik | yok | App Router tabanlı React tam yığın framework'ü; PRD'de Next.js 14'ten 16'ya çekildi. | 13:26 | '> next.js 14 degil next.js 16 kullanalim.' girdisi. (karede: Claude Code girdi satırında 'next.js 14 degil next.js 16 kullanalim.' yazıyor.) |
| NextAuth.js | yok | teknik | yok | Credentials provider ile tek yönetici girişi (admin paneli kimlik doğrulaması). | 13:18 | PRD metninde 'Auth: NextAuth.js (Credentials provider)'. (karede: PRD önizlemesinde 'Auth: NextAuth.js (Credentials provider) — tek yönetici hesabı' maddesi.) |
| Tailwind CSS | yok | teknik | yok | Utility-first CSS çatısı; arayüz stili için PRD'de seçildi ve kurulumda kullanıldı. | 12:12 | 'Tailwind CSS' tech stack satırı. (karede: Claude Code önerisinde 'Tech stack: ... Tailwind CSS' yazıyor.) |
| Zod | yok | teknik | yok | Girdi doğrulama kütüphanesi; API ve yükleme girdilerinde kullanılması planlandı. | 14:10 | PRD/plan metninde 'Zod ile doğrulanır' ifadesi. (karede: PRD/plan ekranında Zod ile girdi doğrulama maddesi görünüyor.) |
| sharp | yok | teknik | yok | Yüklenen görselleri yeniden boyutlandırıp WebP'ye çeviren görüntü kütüphanesi. | 14:28 | 'Tech Stack: ... sharp (yeniden boyutlandırma/WebP dönüşümü) eklendi.' (karede: PRD güncellemesinde 'sharp (yeniden boyutlandırma/WebP dönüşümü)' satırı.) |
| qrcode | yok | teknik | yok | Sunucu tarafında menü URL'si için PNG QR kod üreten npm paketi. | 13:18 | 'QR Üretimi: qrcode npm paketi — sunucu tarafında PNG üretimi'. (karede: PRD önizlemesinde 'QR Üretimi: qrcode npm paketi' satırı.) |
| Cloudinary | yok | teknik | yok | PRD'nin ilk tech stack'inde görsel depolama olarak seçildi; sonradan yerel diske (uploads/) geçildi. | 13:18 | 'Görsel Depolama: Cloudinary (ücretsiz katman)' satırı; sonra kaldırıldı. (karede: PRD önizlemesinde 'Görsel Depolama: Cloudinary (ücretsiz katman)' yazıyor.) |
| Bricolage Grotesque | yok | teknik | yok | DESIGN.md'de başlık (display) fontu olarak tanımlanan yazı tipi. | 16:08 | DESIGN.md'de 'Başlık: Bricolage Grotesque' ve tipografi bölümü. (karede: DESIGN.md önizlemesinde 'grotesk), gövde + menü Inter' tipografi satırı.) |
| Inter | yok | teknik | yok | DESIGN.md'de gövde ve menü fontu; fiyat rakamları için tabular-nums ile kullanıldı. | 16:18 | 'Inter', -apple-system ... font-family tanımı. (karede: DESIGN.md'de font-family: 'Inter', -apple-system, BlinkMacSystemFont... satırı.) |
| Claude Opus 4.8 | yok | teknik | yok | PRD inceleme, plan ve doğrulama adımlarında kullanılan üst düzey model. | 18:34 | 'Opus 4.8 (1M context) with medium effort' model göstergesi. · kanıt: kare (karede: Claude Code alt bilgisinde 'Opus 4.8 (1M context) with medium effort · Claude Max'.) |
| Claude Sonnet 4.6 | yok | teknik | yok | Plan onaylandıktan sonra görevleri uygulayan (execution) daha ucuz model. | 20:07 | 'model sonet 4.6 ile bütün görevleri tamamlayacak.' · kanıt: yok |
| npm | yok | CLI | yok | Node paket yöneticisi; npm run dev, build ve start komutları çalıştırıldı. | 19:44 | 'npm run dev' ve 'npx tsx prisma/seed.ts' plan adımları. (karede: Plan adım listesinde 'npm run dev' ve 'npx tsx prisma/seed.ts' komutları.) |
| TypeScript | yok | teknik | yok | Proje dili; build sırasında derlendi. | 21:06 | 'Finished TypeScript in 3.5s' build çıktısı. (karede: Build çıktısında 'Finished TypeScript in 3.5s' satırı.) |
| ESLint | yok | teknik | yok | Kod kalitesi kontrolü için plan maddesinde yer alan linter. | 19:08 | Plan listesinde 'ESLint/temel script'leri ayarla' maddesi. (karede: Plan görev listesinde 'ESLint/temel script'leri ayarla' maddesi.) |
| VS Code | yok | teknik | yok | Geliştirme ortamı; PRD ve DESIGN.md önizleme, terminal ve Claude Code bu editörde kullanıldı. | 8:05 | 'VS Code'da boş bir uygulama açtım' ve Markdown önizleme. |
| PowerShell | yok | CLI | yok | Windows terminali; dev sunucusu ve Docker komutları bu kabukta çalıştırıldı. | 20:48 | 'PowerShell(Start-Process ...)' ve dev server açıklaması. (karede: Claude Code'da PowerShell aracı çağrısı: Start-Process ile npm run dev.) |
| frontend-design | yok | plugin | yok | Claude Code'un ön yüz işleri için önerdiği eklenti; ekranda ipucu olarak çıktı, videoda kurulmadı. | 19:56 | 'Tip: Working with HTML/CSS? Install the frontend-design plugin'. (karede: Claude Code ipucu satırı: '/plugin install frontend-design@claude-plugins-official'.) |
| prd-yaz skill'ini tetikleyip uygulama için PRD üretmek. | yok | prompt | yok | Bir kafe için QR dijital menü uygulaması için PRD oluştur (prd-yaz skill'i ile, soruları seçenekli sorarak sor). | 10:04 | kaynak: kare |
| Claude'un kapsam, lokasyon, teknoloji ve QR sorularını seçenek kutularıyla sormasını sağlamak. | yok | prompt | yok | Soruları seçenekli soru aracıyla (AskUserQuestion) sor. | 11:00 | kaynak: kare |
| Daha güçlü modelle PRD'yi gözden geçirtip eksikleri tamamlatmak. | yok | prompt | yok | PRD'yi incele ve eksik olan noktaları düzelt/geliştir (model Opus 4.8'e geçildikten sonra). | 12:11 | kaynak: altyazı |
| Framework sürümünü PRD'de düzeltmek. | yok | prompt | yok | Next.js 14 değil, Next.js 16 kullanalım. | 13:26 | kaynak: kare |
| Görsel depolamasını yerel diske çevirmek. | yok | prompt | yok | Görseller localde tutulsun, cloud'da değil (PRD'ye yansıtılsın). | 13:34 | kaynak: kare |
| Tutarlı görsel kimlik için tasarım kurallarını üretmek. | yok | prompt | yok | Open Design'da QR ile açılan dijital menü uygulamasının tasarım sistemini (brand kit) sıfırdan oluştur ve DESIGN.md olarak dışa aktar. | 15:08 | kaynak: altyazı |
| Tasarım kurallarını her oturumda otomatik okutmak. | yok | prompt | yok | CLAUDE.md dosyasına: tasarım kuralları DESIGN.md'dedir; tüm arayüz bileşenlerinde o renk, font ve bileşen kurallarına uy; renk veya font uydurma. | 16:50 | kaynak: kare |
| Kod yazmadan önce planı çıkarıp onaylatmak. | yok | prompt | yok | Plan modundasın; hiçbir dosyaya yazma. prd.md ve DESIGN.md'yi oku, uygulamayı kurmak için adım adım plan çıkar ve görevlere böl; her görevin neyi bitireceğini yaz; henüz kod yazma. | 17:00 | kaynak: altyazı |
| Plana test kapsamını dışarıda bırakmak. | yok | prompt | yok | Test altyapısı şimdilik kapsam dışı; herhangi bir test yazma. | 19:05 | kaynak: altyazı |
| Onaylı planı daha ucuz modelle uygulatmak. | yok | prompt | yok | Görevlere başla ve bitir (Sonnet 4.6 ile execution). | 20:07 | kaynak: altyazı |
| Çalıştırma ve kurulum adımlarını modele bırakmak. | yok | prompt | yok | Gerekli adımları sen yap, çalıştır bu uygulamayı; kurulum ve migrasyonları kendin yap. | 20:07 | kaynak: altyazı |
| Çalışma sırasındaki hataları iterasyonla düzeltmek. | yok | prompt | yok | Admin paneline giriş ve yönlendirme hatalarını gösterip düzeltmesini istemek (hata çıktısını yapıştırma). | 21:10 | kaynak: altyazı |
## Açıklama bağlantıları
- https://github.com/eyaprak/skills — prd-yaz skill'inin ve diğer Claude Code skill'lerinin bulunduğu GitHub reposu. · aday: evet (prd-yaz) · Videoda kurulan prd-yaz skill'i bu repodan klonlandı; izleyicinin kullanabileceği araç kaynağı. · sınıf: diğer
- https://youtu.be/RP7QH24Qqvs — Kanal sahibinin başka bir videosu (referans). · aday: hayır · Referans video bağlantısı; araç ya da servis değil. · sınıf: diğer
- https://youtu.be/U6U0sr2xrqw — Kanal sahibinin başka bir videosu (referans). · aday: hayır · Referans video bağlantısı; araç ya da servis değil. · sınıf: diğer
- https://code.claude.com/docs/en/goal — Claude Code /goal komutu dokümantasyonu. · aday: hayır · Dokümantasyon sayfası; /goal bu videoda kullanılmadı, 2. videoda anlatılacağı söyleniyor. · sınıf: diğer
- https://youtu.be/Hvy_yv9sgz4 — Kanal sahibinin başka bir videosu (referans). · aday: hayır · Referans video bağlantısı; araç ya da servis değil. · sınıf: diğer
- https://claude.ai/download — Claude masaüstü/Claude Code indirme sayfası. · aday: hayır · İndirme sayfası; Claude Desktop videoda kullanılmadı, Claude Code ayrı anılıyor. · sınıf: diğer
- https://n8nkursu.com — Kanal sahibinin n8n kursu sitesi. · aday: hayır · Kanal sahibinin kendi kurs tanıtımı; konu dışı. · sınıf: diğer
- https://x.com/AnthropicAI/status/2072163884430229756 — Anthropic'in Fable 5 erişimi duyurusu (tweet). · aday: hayır · Duyuru bağlantısı; videonun kurulumunda kullanılmıyor, konu dışı. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Yatay kaydırmalı kategori çipleri (chip filter) | Menüde Tümü, Sıcak Kahveler, Soğuk İçecekler, Tatlılar filtre çipleri; seçili çip dolgulu terracotta. | 21:10 | altyazı |
| Öne çıkan rozeti (badge) | 'ÖNE ÇIKAN' etiketi Espresso ve Cold Brew ürünlerinde görünüyor. | 21:10 | altyazı |
| Stokta yok durumu (opacity / disabled state) | Stokta olmayan Limonata kartı soluk gri ve 'Tükendi' etiketiyle sonda görünüyor. | 21:10 | altyazı |
| Ürün kartı listesi (card grid) | Ürünler kart şeklinde; her kartta harf avatarı, ad, açıklama ve fiyat var. | 21:10 | altyazı |
| CSS değişkenleriyle tema (CSS custom properties) | DESIGN.md renkleri (kemik beyaz zemin, terracotta vurgu) arayüzde tutarlı uygulanıyor. | 22:14 | altyazı |
| Admin giriş ekranı (login card) | Yönetici giriş kartı ve oturum yönlendirmesi; oturumsuz /admin erişimi giriş ekranına gidiyor. | 21:10 | altyazı |
| Ayarlar paneli (form) | Logo, telefon ve diğer ayar alanları admin panelinde düzenlenebiliyor. | 22:14 | altyazı |
| Ürün formu ve görsel yükleme (file upload) | Admin panelinde ürün adı, fiyat, görsel, stok, öne çıkan ve sıra alanları ile ürün ekleme/düzenleme. | 23:16 | altyazı |
| QR kod üretim ekranı (QR generator) | Admin panelinde menü URL'sine göre QR kod otomatik üretiliyor ve indirilebiliyor. | 23:16 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Yarım kod sorunu modelden çok, modele işi verme biçiminden kaynaklanır. | 0:00 | öneri |
| PRD'de kapsam dışı yazmak, modelin kendiliğinden gereksiz özellik eklemesini engeller. | 2:00 | öneri |
| Brand kit (DESIGN.md) ile her ekran tutarlı renk ve font kullanır. | 4:33 | öneri |
| Open Design açık kaynak ve ücretsizdir. | 15:08 | özellik |
| Next.js 14 yerine Next.js 16 daha iyi olduğu için tercih edildi. | 13:14 | karşılaştırma |
| Opus 4.8 Sonnet 4.6'dan çok daha iyi iş çıkarıyor ama daha pahalı. | 24:20 | karşılaştırma |
| Sonnet 4.6 ile execution'da birkaç hata çıktı ve iterasyonla düzeltildi. | 24:20 | sayısal |
| Anlatılan yöntem her model için kullanılabilir. | 24:20 | öneri |
| Admin panelinde ürün ve fiyat değişiklikleri menü sayfasına yansıyor. | 22:14 | özellik |
| Admin panelindeki QR kod menü URL'sine göre otomatik üretiliyor. | 23:16 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Yarım kod ve prompt biçimi | aday değil: genel kavram | 'Sorun modelde değil, kullanım biçiminde' — kavramsal anlatım. |
| konuşma 2:00 | PRD (ürün gereksinim belgesi) | aday değil: genel kavram | 'PRD nedir? product requirements document.' |
| konuşma 4:33 | Brand kit | aday değil: genel kavram | 'Brand kit ile tutarlı görsel kimlik' başlığı. |
| konuşma 6:23 | Plan modu + execution | Plan Modu | 'Plan modumuz çok önemli ... Shift tab ile açılır.' |
| konuşma 6:23 | Codex (bulanık 'code') | aday değil: konu dışı | Ses: 'open kod / code' bulanık; ekranda ayrı bir araç gösterilmiyor. |
| konuşma 1:03 | Open Code | aday değil: genel kavram | 'open kod ... yazmadan planla, onayla' diye anlatılıyor. |
| konuşma 3:01 | Antigravity | aday değil: genel kavram | 'antigravity olsun farklı sistemlerin' — alternatif sistem olarak anılıyor. |
| konuşma 3:01 | Skill (kavram) | aday değil: genel kavram | 'skill Claude'a bir işi öğreten küçük dosyadır.' |
| konuşma 3:01 | Skills CLI (bulanık 'skillseni') | aday değil: genel kavram | Ses transkript hatası; bağlam skill kavramı. |
| konuşma 3:01 | Geist (bulanık 'gayet') | aday değil: konu dışı | Ses transkript hatası; anlamsız kelime. |
| konuşma 4:02 | Matt Pocock'un write-a-prd skill'i | aday değil: başka adayın parçası (prd-yaz) | 'Bu PRD yaz Mat Pocock'un oluşturduğu ... Türkçeye uyarladım.' |
| konuşma 4:33 | design-dna (bulanık 'designmdya') | aday değil: genel kavram | Ses transkript hatası; DESIGN.md kastediliyor. |
| konuşma 8:05 | Tripo (bulanık) | aday değil: genel kavram | Ses transkript hatası; anlamlı bir araç adı değil. |
| konuşma 8:05 | Slack (bulanık 'stack') | aday değil: konu dışı | Ses transkript hatası; tech stack kastediliyor. |
| konuşma 8:05 | VS Code | VS Code | 'Visual Studio Codda boş bir uygulama açtım.' |
| konuşma 9:07 | skill-ui (bulanık 'skillsi') | aday değil: genel kavram | Ses transkript hatası; skill kastediliyor. |
| kare 8:08 | Git | Git | git-scm.com install sayfası. |
| kare 8:08 | Amazon.com (sekme) | aday değil: konu dışı | Tarayıcı sekmesi; videoda kullanılmıyor. |
| kare 8:08 | agent-skills (repo sekmesi) | aday değil: konu dışı | Tarayıcı sekme başlığı; repo adı. |
| kare 8:08 | Claude Code Templates (sekme) | aday değil: konu dışı | Tarayıcı sekmesi; anlatılmıyor. |
| kare 8:10 | Descript (ekran) | aday değil: konu dışı | Tarayıcı yer imi/sekme; anlatılmıyor. |
| kare 8:10 | GitHub | GitHub | github.com/eyaprak/skills reposu. |
| kare 8:20 | JavaScript | aday değil: konu dışı | README'de 'Kendi web uygulamanı (Next.js, Node, ...)' listesinde geçiyor; kullanılmadı. |
| kare 8:20 | Python | aday değil: konu dışı | README'de uygulama türü listesinde geçiyor; kullanılmadı. |
| kare 8:20 | Hostinger (VPS) | aday değil: konu dışı | README'de 'Hostinger VPS'ine kur' ifadesi; videoda kullanılmadı. |
| kare 8:20 | Metabase / Uptime Kuma / WordPress / n8n / Evolution API / Ghost (README) | aday değil: konu dışı | README'de örnek açık kaynak uygulamalar listesi; anlatılmadı. |
| kare 8:20 | Skill nedir (README tanımı) | aday değil: genel kavram | 'Claude Code'a şu işi şöyle yap diye öğreten...' |
| kare 8:31 | GitHub CLI / GitHub Desktop (seçenekler) | aday değil: konu dışı | Kurulum yöntemleri listesinde görünüyor; kullanılmadı. |
| kare 9:14 | Visual Studio Code (uyarı) | VS Code | 'Are you sure you want to move skills into .claude?' |
| kare 9:24 | prd-yaz SKILL.md | prd-yaz | name: prd-yaz ve description metni. |
| kare 9:46 | Agent Skills dizini (sekme) | aday değil: konu dışı | Tarayıcı sekmesi; anlatılmıyor. |
| kare 10:04 | Claude Code | Claude Code | 'Claude Code' sekmesi ve /prd-yaz girdisi. |
| kare 10:08 | Claude Code v2.1.183 | Claude Code | Açılış ekranında sürüm bilgisi. |
| kare 10:22 | React | aday değil: konu dışı | Soru seçeneği olarak görünüyor; seçilmedi. |
| kare 10:22 | Vue | aday değil: konu dışı | Soru seçeneği olarak görünüyor; seçilmedi. |
| kare 10:22 | Supabase | aday değil: konu dışı | Soru seçeneği (Next.js + Supabase); seçilmedi. |
| kare 10:22 | Firebase | aday değil: konu dışı | Soru seçeneği (Next.js + Firebase); seçilmedi. |
| kare 10:22 | PostgreSQL | PostgreSQL | Seçilen veritabanı; Next.js + PostgreSQL. |
| kare 10:22 | Vercel | aday değil: konu dışı | Hosting sorusunda seçenek; deploy kapsam dışı, PRD'de sonra reddedildi. |
| kare 11:00 | Node.js | aday değil: konu dışı | 'React + Node.js + PostgreSQL' seçeneği; seçilmedi. |
| kare 12:12 | Tailwind CSS | Tailwind CSS | Tech stack satırı. |
| kare 12:12 | Redis | aday değil: konu dışı | PRD önerisi/soru metninde görünüyor; kullanılmadı. |
| kare 13:18 | Ollama | aday değil: konu dışı | PRD metninde görünüyor; kullanılmadı. |
| kare 13:18 | npm | npm | qrcode npm paketi ve npm komutları. |
| kare 13:18 | Cloudinary | Cloudinary | PRD'de görsel depolama olarak yazıyor; sonradan kaldırıldı. |
| kare 13:38 | Jest | aday değil: konu dışı | PRD test çerçevesi metni; test şimdilik kapsam dışı. |
| kare 13:38 | @testing-library/react | aday değil: konu dışı | PRD test çerçevesi metni; kullanılmadı. |
| kare 13:38 | Supertest | aday değil: konu dışı | PRD test seçeneği metni; kullanılmadı. |
| konuşma 13:14 | Vitest (bulanık 'vetest') | aday değil: konu dışı | Ses transkript hatası; test kapsam dışı. |
| konuşma 13:14 | Nuxt (bulanık 'nextjs') | aday değil: genel kavram | Ses transkript hatası; Next.js kastediliyor. |
| kare 14:10 | Zod | Zod | Girdi doğrulama maddesi. |
| kare 14:52 | Claude Design | aday değil: genel kavram | Open Design'ın 'Claude Design alternatifi' olduğu söyleniyor. |
| kare 14:52 | taste-skill (kenar çubuğu proje adı) | aday değil: konu dışı | Open Design kenar çubuğunda eski proje adı. |
| kare 14:28 | sharp | sharp | Görsel dönüşüm için tech stack. |
| kare 16:26 | Telegram | aday değil: konu dışı | Ekranda görünen uygulama; anlatılmadı. |
| kare 16:50 | uv (OCR, muhtemelen 'uygula') | aday değil: konu dışı | CLAUDE.md metni içinde OCR parçası; araç değil. |
| kare 16:08 | Bricolage Grotesque | Bricolage Grotesque | DESIGN.md başlık fontu. |
| kare 16:18 | Inter | Inter | DESIGN.md gövde fontu. |
| kare 18:34 | Docker Hub / Docker Scout | aday değil: konu dışı | Docker Desktop menüsünde görünür; kullanılmadı. |
| kare 18:34 | Kubernetes | aday değil: konu dışı | Docker Desktop menüsü; kullanılmadı. |
| kare 18:34 | MCP Toolkit | aday değil: konu dışı | Docker Desktop menüsü; kullanılmadı. |
| kare 18:34 | Suno (konteyner adı) | aday değil: konu dışı | postgres-suno konteyner adı; ilgisiz. |
| kare 18:34 | Opus 4.8 | Claude Opus 4.8 | Model göstergesi. |
| kare 19:00 | Syne | aday değil: konu dışı | Ekranda görünüyor; kullanımı anlatılmıyor. |
| kare 19:08 | ESLint | ESLint | Plan görev listesinde 'ESLint/temel script'leri ayarla'. |
| kare 19:12 | Prisma | Prisma | prisma migrate dev komutu. |
| kare 19:32 | Claude Haiku 4.5 | aday değil: konu dışı | Model menüsünde görünüyor; kullanılmadı. |
| kare 19:32 | Claude Fable (disabled) | aday değil: konu dışı | Model menüsünde 'Claude Fable 5 is currently unavailable'. |
| kare 19:56 | frontend-design | frontend-design | Claude Code ipucu olarak gösterildi. |
| kare 20:06 | postgres:16-alpine | PostgreSQL | Docker imajı. |
| kare 20:42 | Bricolage Grotesque / Inter değişkenleri (html class) | Bricolage Grotesque | Next.js font değişkenleri html etiketinde. |
| kare 20:44 | n8nKursu (sekme) | aday değil: konu dışı | Kanal sahibinin kurs sitesi sekmesi. |
| kare 20:48 | PowerShell | PowerShell | Start-Process ile dev server açma. |
| kare 21:06 | TypeScript | TypeScript | Build çıktısında 'Finished TypeScript'. |
| kare 21:08 | NextAuth (jwt import) | NextAuth.js | from "next-auth/jwt" kodu. |
| kare 22:00 | Hermes Agent (dosya adı) | aday değil: konu dışı | Dosya/klasör adı; anlatılmıyor. |
| kare 22:50 | Rive | aday değil: konu dışı | Ekranda görünen ad; anlatılmıyor. |
| konuşma 22:14 | fal.ai (bulanık 'falan') | aday değil: genel kavram | Ses transkript hatası; anlamsız. |
| konuşma 17:00 | agent-sdk-dev (bulanık 'agents') | aday değil: konu dışı | Ses transkript hatası; CLAUDE.md/AGENTS.md kastediliyor. |
| açıklama | Claude Code | Claude Code | 'Claude Code (Sonnet 4.6 + Opus 4.8) ile yapıyorum.' |
| açıklama | Claude | aday değil: genel kavram | Açıklamada genel model ailesi adı. |
| açıklama | Claude Sonnet | Claude Sonnet 4.6 | Açıklamada Sonnet 4.6 kullanıldığı yazıyor. |
| açıklama | Claude Opus | Claude Opus 4.8 | Açıklamada Opus 4.8 kullanıldığı yazıyor. |
| açıklama | Claude Desktop | aday değil: konu dışı | claude.ai/download bağlantısı; videoda kullanılmadı. |
| açıklama | Cursor | aday değil: konu dışı | Açıklamada 'Cursor ... kullananlar' hedef kitle olarak geçiyor. |
| açıklama | n8n | aday değil: konu dışı | Kanal sahibinin n8n kursu bağlantısı. |
| açıklama | GitHub | GitHub | Skill repo bağlantısı. |
| açıklama | Antigravity | aday değil: genel kavram | Açıklamada 'AI kodlama araçları' genel kavramı içinde geçiyor. |
| açıklama | Fable 5 / Anthropic duyuru | aday değil: konu dışı | x.com/AnthropicAI bağlantısı; kurulumla ilgili değil. |
| yorum | Cursor, Claude vb. (yorum) | aday değil: konu dışı | Yorumda 'kullandığınız AI aracına (Cursor, Claude vb.)' geçiyor. |
| yorum | Skills Repo (sabit yorum) | GitHub | 'Skills Repo / https://github.com/eyaprak/skills'. |
| yorum | Sonnet (yorum) | Claude Sonnet 4.6 | Yorumda 'coder ajanı(sonnet)' ve 'Sonnet 4.6' geçiyor. |
| yorum | Opus 4.8 (yorum) | Claude Opus 4.8 | Yorumda 'güçlü bir modelle (özellikle Opus 4.8)'. |
| yorum | Fable 5 (yorum) | aday değil: konu dışı | Yorumlarda ne zaman açılacağı soruluyor; videoda kullanılmıyor. |
| yorum | Anthropic (yorum) | aday değil: konu dışı | Yorumda 'Anthropic'e büyük zarar' ifadesi; araç değil. |
| yorum | iTerm (yorum) | aday değil: konu dışı | Çoklu terminal yorumunda geçiyor; videoda kullanılmıyor. |
| yorum | Git (yorum) | Git | Yorumda Git geçiyor; videoda git clone kullanıldı. |
| yorum | wiki (yorum) | aday değil: genel kavram | Yorumcunun kendi iş akışında geçen genel kavram. |
| sözlük açıklama | n8n | aday değil: konu dışı | Açıklama bağlantısındaki kurs sitesi. |
| kare 0:22 | Go | aday değil: konu dışı | Giriş ekranında görünen ad; anlatılmıyor. |
| kare 0:22 | Next.js | Next.js 16 | Giriş ekranında ve PRD'de geçiyor. |
| kare 0:22 | Prisma | Prisma | Giriş ekranında ve plan görevlerinde geçiyor. |
| kare 0:22 | Docker | Docker | Giriş ekranında ve plan görevlerinde geçiyor. |
| kare 0:24 | TypeScript | TypeScript | Giriş ekranında geçiyor; build'de kullanıldı. |
| kare 14:54 | Open Design (sekme) | Open Design | Açık kaynak Claude Design alternatifi tanıtımı. |
| kare 14:52 | Web Prototype Taste Edit... (Open Design proje) | aday değil: konu dışı | Open Design proje listesi. |
| kare 19:04 | Docker Compose | Docker | docker-compose.yml planı. |
| kare 20:52 | Invoke-WebRequest (localhost:3000 kontrolü) | PowerShell | Dev server HTTP kontrolü. |
| kare 21:08 | Stop-Process (node) | PowerShell | Node süreçlerini durdurma komutu. |
| kare 21:24 | localhost:3000/admin/settings | aday değil: konu dışı | Yerel uygulama adresi; araç değil. |
| kare 23:12 | localhost:3000/admin/qr | aday değil: konu dışı | Yerel uygulama adresi; araç değil. |
| kare 14:28 | Vercel | aday değil: konu dışı | PRD'de deployment seçeneği; kalıcı disk gerektiği için dışlandı. |
| kare 14:28 | Hostinger VPS (PRD) | aday değil: konu dışı | PRD'de deployment önerisi; deploy bu PRD kapsamı dışında. |
| kare 14:28 | Neon / Supabase database-only / Railway | aday değil: konu dışı | PRD'de harici PostgreSQL seçenekleri; kullanılmadı. |
| kare 11:50 | qr-code-generator.com | aday değil: konu dışı | Soruda harici QR seçeneği olarak geçiyor; kullanılmadı. |
| kare 19:32 | Sonnet 4.6 | Claude Sonnet 4.6 | Model seçimi. |
| kare 19:12 | npm run dev / npm start | npm | Doğrulama adımları. |
| kare 19:56 | /install-github-app (ipucu) | aday değil: konu dışı | Claude Code ipucu; kurulmadı. |
| kare 20:06 | Docker Desktop | Docker | Docker Desktop arayüzünde konteyner listesi. |
| konuşma 21:10 | Yönlendirme hatası düzeltme (iterasyon) | aday değil: genel kavram | 'Burada çok fazla yönlendirme hatası alıyoruz.' |
| konuşma 24:20 | Iterasyon yöntemi | aday değil: genel kavram | 'sürekli git bu hatayı yaz çıktısını al dön'. |
| konuşma 22:14 | Admin paneli (ürün/kategori yönetimi) | aday değil: genel kavram | Demo uygulamanın kendi arayüzü; ayrı bir araç değil. |
| konuşma 23:16 | Tek tıkla deploy (sağ üst kart videosu) | aday değil: konu dışı | Deploy videosuna yönlendirme; bu videoda gösterilmedi. |
| ekran 8:20 | deploy-app skill | aday değil: konu dışı | Repoda görünür; 'deploy yap ihtiyacımız yok, silebiliriz'. |
## Kareden okunanlar
- 0:24: Terminalde '> claude --dangerously-skip-permissions' komutu ve '2. utils/api.ts → retry mantığını güncelle' satırı.
- 8:08: Tarayıcıda git-scm.com/install/ sayfası; 'Install' başlığı, 'Choose your operating system above.'
- 8:10: github.com/eyaprak/skills reposu: 'YouTube videolarımda gösterdiğim Claude Code skill'lerinin toplandığı repo.'
- 9:06: PowerShell'de 'git clone https://github.com/eyaprak/skills.git' komutu.
- 9:24: SKILL.md: name: prd-yaz ve description: 'Bir fikri, kullanıcıyla adım adım sorgulayıp ... PRD'ye dönüştürür'.
- 10:04: Girdi: '/prd-yaz Bir kafe için QR dijital menü uygulaması için PRD oluştur.'
- 10:22: Soru: 'Hangi teknoloji/framework tercih edersin? (Next.js, React, Vue, vs.)' ve 'Hosting nerede olacak?'
- 11:00: Seçenek: '1. Next.js + Supabase (Recommended)', '2. Next.js + Firebase', '3. React + Node.js + PostgreSQL'.
- 12:12: 'Tech stack: Next.js 14 (App Router) + PostgreSQL (Prisma) + Cloudinary + NextAuth.js + Tailwind CSS'.
- 13:26: Girdi: 'next.js 14 degil next.js 16 kullanalim.'
- 13:34: Girdi: '2. görseller localde tutulsun cloudda degil.'
- 14:28: PRD: 'Görsel boyutu: Maksimum yükleme 5 MB; yalnızca JPEG/PNG/WebP.'
- 14:50: Not: 'Deployment değişti: Yerel disk kalıcılık gerektirdiği için artık Vercel/serverless uygun değil.'
- 16:50: CLAUDE.md: 'Tasarım kuralları DESIGN.md dosyasındadır. Tüm arayüz bileşenlerinde bu renk, font ve bileşen kurallarına her zaman uy.'
- 18:30: Plan sorusu: 'Geliştirme ortamında PostgreSQL'i nasıl sağlayalım?' seçenekleri: Docker Compose ile yerel, Mevcut bağlantı.
- 19:04: Görev listesi: 'Görev 3 - Docker Compose ile PostgreSQL + .env', 'Görev 4 - Prisma şeması, migration ve seed'.
- 19:12: Doğrulama: 'docker compose up -d → Postgres çalışır; npx prisma migrate dev && npm run seed.'
- 19:32: Model menüsü: 'Opus 4.8 with 1M context', 'Sonnet 4.6', 'Haiku 4.5', 'Fable (disabled)'.
- 19:56: İpucu: '/plugin install frontend-design@claude-plugins-official'.
- 20:06: docker compose ps çıktısı: postgres:16-alpine konteyneri, 5432 portu.
- 20:48: PowerShell: 'Start-Process "http://localhost:3000"' ve dev server bilgisi.
- 21:06: Build çıktısı: 'Finished TypeScript in 3.5s'; 'Next.js 16'da export adı proxy olmalı, middleware değil.'
- 21:16: Açıklama: '.env dosyasında $ işaretleri Next.js tarafından değişken olarak yorumlanmış' sorunu.
- 21:30: Dev server penceresi notu: 'o pencereyi kapatmayın'.
## Belirsizlikler
- Transkriptte 'TexC 14' ve 'Next JS 16 K' gibi bozuk ifadeler var; ekrandaki PRD metni Next.js 14 → 16 değişikliğini doğruluyor.
- Ses kayıtlarında bulanık kelimeler var (Geist, Tripo, Slack, Codex, Nuxt, Vitest, agents, skill-ui, design-dna). Bunlar aday olarak alınmadı.
- Konuşmada 'Skills CLI' ve 'fal.ai' gibi bulanık anılar var; bağlamdan emin değilim.
- Canlıya alma (deploy) bu videoda gösterilmedi; yalnızca sağ üst kartta başka videoya yönlendirme var.
- Video sonunda yönetim paneli ürün ekleme ve QR oluşturma gösterildi; mobil 375px görünümü ekranda var ama hangi kareye ait olduğu kesin değil.
- Ekranda görülen varsayılan yönetici giriş bilgisi ve .env değerleri bu forma yazılmadı (gizli bilgi).
- PRD'de geçen Cloudinary, Vercel, Supabase, Firebase, Redis, Ollama, Jest, Supertest ve Vitest videoda kullanılmadı; yalnızca PRD/menü metninde görünüyor.
- Skill klasörü yolu ekranda 'C:\Users\...\claude\skills\prd-yaz' olarak görünüyor; kullanıcıya özel yol burada yazılmadı.
- Kare 21:16 ve 21:30 Claude'un kendi çıktılarında ve komutlarında; videoda sohbet içi ayrıntılar kısmen okunamıyor.
- Yorumlarda 'Opus 4.8 ile sıfır hata' ve 'Sonnet 4.6 ile hatalar' tartışması var; bu video içeriği değil, izleyici görüşü.
## Atlanan segment oranı
0/26 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- yok
## Promptlar
- prd-yaz skill'ini tetikleyip uygulama için PRD üretmek. — Bir kafe için QR dijital menü uygulaması için PRD oluştur (prd-yaz skill'i ile, soruları seçenekli sorarak sor).
- Claude'un kapsam, lokasyon, teknoloji ve QR sorularını seçenek kutularıyla sormasını sağlamak. — Soruları seçenekli soru aracıyla (AskUserQuestion) sor.
- Daha güçlü modelle PRD'yi gözden geçirtip eksikleri tamamlatmak. — PRD'yi incele ve eksik olan noktaları düzelt/geliştir (model Opus 4.8'e geçildikten sonra).
- Framework sürümünü PRD'de düzeltmek. — Next.js 14 değil, Next.js 16 kullanalım.
- Görsel depolamasını yerel diske çevirmek. — Görseller localde tutulsun, cloud'da değil (PRD'ye yansıtılsın).
- Tutarlı görsel kimlik için tasarım kurallarını üretmek. — Open Design'da QR ile açılan dijital menü uygulamasının tasarım sistemini (brand kit) sıfırdan oluştur ve DESIGN.md olarak dışa aktar.
- Tasarım kurallarını her oturumda otomatik okutmak. — CLAUDE.md dosyasına: tasarım kuralları DESIGN.md'dedir; tüm arayüz bileşenlerinde o renk, font ve bileşen kurallarına uy; renk veya font uydurma.
- Kod yazmadan önce planı çıkarıp onaylatmak. — Plan modundasın; hiçbir dosyaya yazma. prd.md ve DESIGN.md'yi oku, uygulamayı kurmak için adım adım plan çıkar ve görevlere böl; her görevin neyi bitireceğini yaz; henüz kod yazma.
- Plana test kapsamını dışarıda bırakmak. — Test altyapısı şimdilik kapsam dışı; herhangi bir test yazma.
- Onaylı planı daha ucuz modelle uygulatmak. — Görevlere başla ve bitir (Sonnet 4.6 ile execution).
- Çalıştırma ve kurulum adımlarını modele bırakmak. — Gerekli adımları sen yap, çalıştır bu uygulamayı; kurulum ve migrasyonları kendin yap.
- Çalışma sırasındaki hataları iterasyonla düzeltmek. — Admin paneline giriş ve yönlendirme hatalarını gösterip düzeltmesini istemek (hata çıktısını yapıştırma).
ikinci göz KAPALI: --ikinci-goz yok
