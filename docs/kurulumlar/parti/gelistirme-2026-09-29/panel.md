# Karar paneli — gelistirme-2026-09-29

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| jcode | CLI | 1 | MIT | koşmadı: kurulu | ZATEN VAR | eşdeğer: codex p 0.75 | |
| graphify | CLI | 2 | Apache-2.0 (README rozeti; depoda ayrıca LICENSE-MIT dosyası var, bir web sonucu MIT diyor. Çift lisans olabilir, doğrulanmadı) | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | |
| headroom | CLI | 1 | Apache-2.0 | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | |
| ponytail | CLI | 1 | MIT | koşmadı: kurulu | ZATEN VAR | kurulu: ponytail | |
| superpowers | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: superpowers · alt tür çakışması (kurulu > ürün) | |
| claude-mem | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: claude-mem | |
| impeccable | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: impeccable · alt tür çakışması (kurulu > ürün) | |
| task-observer | skill | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: anthropic-skills:task-observer · alt tür çakışması (kurulu > servis) | |
| claude-code | CLI | 1 | bilinmiyor | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | |
| rtk | CLI | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | |
| graphify-gelistirme | CLI | 2 | — | — | ÖĞREN | Not al. Büyük bir repoda deneme yapılırsa token tasarrufu ve doğruluk ölçülür. Bu videolarda ölçüm yok. (kanıt: oHKt0FUbR58 0:24: karede 'Any input. One graph. Complete recall.' sayfası, altyazıda 'called Graphify'. klDiYMzW0o0 0:00: aynı çalışma şekli anlatılıyor.) | |
| headroom-gelistirme | CLI | 1 | — | — | ÖĞREN | Not al; yalnızca 'sıkıştırma katmanı' tanımı var. Yöntemi ve güvenliği repodan doğrulanana kadar kurma. (kanıt: klDiYMzW0o0 0:00: altyazıda birinci araç olarak sıkıştırma katmanı diye anlatılıyor.) | |
| rtk-gelistirme | CLI | 1 | — | — | UYARLA | Uyarla: Bash çıktısı için PreToolUse/PostToolUse hook'unda çıktı kırpma ekle veya rtk'yi dene. Önce bir repoda token ölçümü yap; bilgi kaybı riskini kontrol et. (kanıt: g89FJiNAlEs 0:50: diyagramda 'rtk git status' hook akışı ~300 token, doğrudan 'git status' ~600 token.) | |

## form_red
- yok
## Eksik alanlar
- yok
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- jcode: hedef_tur: hook tarif: JCode'un tamamı üretilemez, ama bağlam tasarrufu fikirleri Claude Code hook'u olarak yapılabilir. PostToolUse hook'u yaz. Grep/Read çıktısını oturumdaki görülmüş satır/dosya karma listesiyle karşılaştır ve tekrar eden içeriği 'daha önce görüldü' özetiyle kısalt. Ayrıca grep sonuçlarına dosya başına sembol/yapı özeti ekleyen küçük bir CLI (ctags veya tree-sitter tabanlı) yaz. Oturum hafızası için yerel bir gömme dizini kullanan bir MCP sunucusu düşünülebilir. Swarm modu kapsam dışı.
- graphify: hedef_tur: CLI tarif: Graphify zaten kurulabilir bir CLI+skill olduğundan kopyalamak yerine doğrudan kullanmak daha mantıklı. Hafif bir sürüm için: Python CLI yaz, tree-sitter ile dosyalardan sembol, import ve call kenarlarını çıkar, networkx ile graph.json üret, query/path/explain alt komutları ekle. Ardından bir SKILL.md ile Claude'a 'önce graph.json'ı sorgula' talimatı ver ve isteğe bağlı bir PreToolUse hook'u ile ilk ham Read'i grafiğe yönlendir.
- headroom: hedef_tur: hook tarif: Tam proxy yerine hafif bir Claude Code PostToolUse hook'u: Bash/Read çıktısı eşiği (örn. >8k token) aşarsa (1) JSON'u alan/dizi örnekleyerek özetle, (2) log'ları tekrarlayan satırları grupla ama ERROR/FATAL/stack trace satırlarını aynen koru, (3) tam çıktıyı yerel bir dosyaya (.cache/ccr/<hash>.txt) yaz ve özetin sonuna 'tam çıktı: <yol>' referansı ekle; modele bu dosyayı Read ile geri çağırma imkanı ver. İstenirse ek olarak `retrieve`/`stats` için küçük bir MCP sunucusu. Kompress benzeri ML modeli gerektirmez; kural tabanlı başla, ölçüm için önce/sonra token sayısını logla.
- ponytail: hedef_tur: skill tarif: Bir SKILL.md yaz. Ajana kod yazmadan önce 7 basamaklı merdiveni (gerekli mi, kod tabanında var mı, stdlib, native özellik, mevcut bağımlılık, tek satır, minimum) uygulamasını söyle. Önce ilgili kodu okumayı ve doğrulama, hata yönetimi, güvenlik ve erişilebilirliği asla kesmemeyi şart koş. Önce/sonra örnekleri ekle. Etkiyi kendi ortamımızda 5-10 görevle git diff satırı ve token ölçerek sına. Kopyalamak yerine MIT lisansına atıf vererek sıfırdan yazmak daha temiz.
## Kural önerileri (T0)
- yok
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- yok
## Site/UI teknikleri
- npm sayfası: 'npm i framer-motion' seçili; github.com/motiondivision/motion; 7648 Dependents, 1,381 Versions; 41,411,060 haftalık indirme; sürüm 12.38.0; MIT. · M9qgd_KJkWc · 0:21 (kare) → docs/departmanlar/frontend.md
- Landing page (marka renkleri, animasyon) · 86HM0RUWhCk · 7:13 (kare) → docs/departmanlar/frontend.md
- Referans site klonu ve markaya uyarlama · 86HM0RUWhCk · 13:46 (altyazı) → docs/departmanlar/frontend.md
- Hero animasyonlu arka plan (21st.dev) · 86HM0RUWhCk · 19:17 (altyazı) → docs/departmanlar/frontend.md
- Parlayan CTA butonu · 86HM0RUWhCk · 25:18 (altyazı) → docs/departmanlar/frontend.md
- VS Code Welcome ekranı; son projeler arasında 'Website Building YT'; 'Get started with Claude Code' kartı. · 86HM0RUWhCk · 0:30 (kare) → docs/departmanlar/frontend.md
- Uzantılar panelinde 'Claude Code for VS Code' (Anthropic) kurulu; sağda Claude Code paneli, 'Bypass permissions' yazıyor. · 86HM0RUWhCk · 1:27 (kare) → docs/departmanlar/frontend.md
- Diyagram: CLAUDE.md (Project Instructions) sistem istemi olarak enjekte edilir; 'CLAUDE.md loads before EVERY message'. · 86HM0RUWhCk · 2:25 (kare) → docs/departmanlar/frontend.md
- CLAUDE.md: 'Always Do First – Invoke the frontend-design skill'; Reference Images, Local Server (node serve.mjs, localhost:3000). · 86HM0RUWhCk · 3:17 (kare) → docs/departmanlar/frontend.md
- Skills diyagramı: Claude bir skill'in yardım edip edemeyeceğini kontrol eder; Yol A uzman skill, Yol B genel bilgi. · 86HM0RUWhCk · 4:10 (kare) → docs/departmanlar/frontend.md
- Claude Code girişinde landing page istemi; brand_assets içinde 'AIS Brand Guidelines-1.png' ve 'AIS PNG.png'. · 86HM0RUWhCk · 6:12 (kare) → docs/departmanlar/frontend.md
- Üretilen AIS landing page: 'Build the Future with AI Automation', JOIN NOW butonu, 5,000+ Members. · 86HM0RUWhCk · 7:13 (kare) → docs/departmanlar/frontend.md
- Beş adımlı şema: 0 CLAUDE.md, 1 Frontend Design Skill, 2 Screenshot Loop, 3 ve 4 henüz boş. · 86HM0RUWhCk · 8:31 (kare) → docs/departmanlar/frontend.md
- CLAUDE.md ile projede brand_assets, node_modules, temporary screenshots, index.html, package.json, screenshot.mjs, serve.mjs. · 86HM0RUWhCk · 9:23 (kare) → docs/departmanlar/frontend.md
- Düşük / Orta / Yüksek (seçili) / Çok yüksek; model: "GPT 5.6 Sol" · yp7gg8cG5wc · 3:35 Zeka seviyesi dropdown (kare) → docs/departmanlar/frontend.md
- "1. zanwei/design-dna" (Stars: 1,604, Maintained: Yes), "2. ibelick/ui-skills" (Stars: 7,826), "3. 14islands/r3f-scroll-rig" · yp7gg8cG5wc · 6:41 Repo listesi (kare) → docs/departmanlar/frontend.md
- "ibelick/ui-skills", Production Status: "Research", Priority: "Medium" · yp7gg8cG5wc · 19:10 Content Pipeline tablosu satırı (kare) → docs/departmanlar/frontend.md
- "ai/size-limit", Category: "Frontend performance workflow", Video Potential: "Medium" · yp7gg8cG5wc · 21:14 Repo inceleme kartı (kare) → docs/departmanlar/frontend.md
- "barvin/number-flow", Review Status dropdown: New / Review / Test / Video Candidate / Rejected, Video Potential: "High" · yp7gg8cG5wc · 22:15 Repo inceleme kartı (kare) → docs/departmanlar/frontend.md
- Scroll'a bağlı kademeli metin belirme (reveal, fade+translateY) · JfmAm3sxCSc · GSAP (omer-kutuphaneler/web-sahne-desenleri kontrol edilmedi) → docs/departmanlar/frontend.md
- Yumuşak (inertial) kaydırma · JfmAm3sxCSc · tahmin: Lenis (omer-kutuphaneler/scroll-craft kontrol edilmedi) → docs/departmanlar/frontend.md
- 3D sarmal görsel galeri sahnesi · JfmAm3sxCSc · Three.js (omer-kutuphaneler/web-sahne-desenleri kontrol edilmedi) → docs/departmanlar/frontend.md
- Hover'da görsele parallax/geri kayma · JfmAm3sxCSc · tahmin: CSS/JS transform + mousemove veya GSAP (yok) → docs/departmanlar/frontend.md
- Büyük serif italik başlık tipografisi + kontrast renk paneli · JfmAm3sxCSc · tahmin: özel/serif display font (ad ekranda görünmüyor) (yok) → docs/departmanlar/frontend.md
- Kademeli (staggered) satır/blok belirmesi (scroll top 80% eşiği) · JfmAm3sxCSc · tahmin: GSAP ScrollTrigger (yok) → docs/departmanlar/frontend.md
- "new-video / Create premium studio landing page with spiral gallery" · JfmAm3sxCSc · 6:37 Dosya sekmesi (kare) → docs/departmanlar/frontend.md
- CONFIG, scene/camera/renderer setup, createCurvedTileGeometry, buildSpiral · JfmAm3sxCSc · 6:37 script.js (kare) → docs/departmanlar/frontend.md
- spinVelocity callback, "existing lenisRaf loop" · JfmAm3sxCSc · 6:37 shaders.js (kare) → docs/departmanlar/frontend.md
- Hero title 138.24px (was 187.2px); 23 .reveal-text elements; mid-scroll opacity 0.07 / translateY(44.66px); canvas 1440x900, is-ready; "No console errors"; "Dev server still running on http://localhost:5174/" · JfmAm3sxCSc · 6:37 Doğrulama metrikleri (kare) → docs/departmanlar/frontend.md
- "Opus 4.7 1M Extra high" · JfmAm3sxCSc · 6:37 Sağ altta model etiketi (kare) → docs/departmanlar/frontend.md
- "Unlock your AI design superpowers", "copy prompt" özelliği, "Powered by DESIGN ROCKET" · JfmAm3sxCSc · 9:42 motionsites.ai anasayfası (kare) → docs/departmanlar/frontend.md
- 3D dairesel (ring) galeri kart dizilimi, transform-style:preserve-3d · NyNScAc2u_o · tahmin: vanilla CSS 3D transform + GSAP (yok) → docs/departmanlar/frontend.md
- Scroll'a bağlı saat yönü/ters yönü dönüş · NyNScAc2u_o · tahmin: GSAP (yok) → docs/departmanlar/frontend.md
- Hover'da kart yumuşak kayma/uzaklaşma geçişi · NyNScAc2u_o · tahmin: GSAP (yok) → docs/departmanlar/frontend.md
- Mouse Y eksenine bağlı galeri parallax hareketi · NyNScAc2u_o · tahmin: GSAP + JS mousemove (yok) → docs/departmanlar/frontend.md
- Dönerek açılan yükleme ekranı (loader→intro akışı) · NyNScAc2u_o · tahmin: GSAP timeline (yok) → docs/departmanlar/frontend.md
- Masaüstü/mobil için tek kod tabanında ayrı davranış (breakpoint) · NyNScAc2u_o · tahmin: CSS media query / JS breakpoint (yok) → docs/departmanlar/frontend.md
- Merkezde sabit başlık, hover'da kart odaklı bilgi değişimi · NyNScAc2u_o · tahmin: vanilla JS DOM güncelleme (yok) → docs/departmanlar/frontend.md
- merkez başlık "We are STUDIO.", adres localhost:5179 · NyNScAc2u_o · 0:30 STUDIO galeri ekranı (kare) → docs/departmanlar/frontend.md
- CLOU, Site of the Day - Jun 21 2022, puan 7.62/10, Unseen Studio · NyNScAc2u_o · 1:34 Awwwards sayfası (kare) → docs/departmanlar/frontend.md
- DESIGN TOKENS (font Helvetica Neue/apple-system), CORE GEOMETRY (.gallery position:fixed, transform-origin orbit), EXACT CONSTANTS: PERSPECTIVE 1600, ITEM_COUNT 136, TURNS 1, ROT_Y 86, RING_SCALE 0.88, PARALLAX 4, MOBILE breakpoint max-width:768px · NyNScAc2u_o · 6:14 Prompt/design-spec dosyası (kare) → docs/departmanlar/frontend.md
- proje "Interactive circular project gallery", working directory /Users/yildizdilske/Desktop/clou-deneme, model "Opus 4.8", durum "Needs input" · NyNScAc2u_o · 7:14 Claude arayüzü (kare) → docs/departmanlar/frontend.md
- localhost:5179, "We are STUDIO." · NyNScAc2u_o · 7:56 STUDIO galeri ekranı tekrar (kare) → docs/departmanlar/frontend.md
- Estetik yön seçimi (brütalist/maksimalist/retro-fütüristik/lüks/organik) sonra uygulama · Gg35_iQWx7g · tahmin: frontend-design skill (anthropics/skills), kütüphane belirtilmemiş (yok) → docs/departmanlar/frontend.md
- Tipografi, renk (CSS variables), motion tasarımı, mekansal kompozisyon temel tasarım sütunları olarak vurgulanıyor · Gg35_iQWx7g · tahmin: frontend-design skill, HTML/CSS/JS/React/Vue çıktısı (ekranda yazılı) (yok) → docs/departmanlar/frontend.md
- "npx skills add https://github.com/anthropics/skills --skill frontend-design"; INSTALLS 721.0K; GITHUB STARS 165.1K; REPOSITORY anthropics/skills; FIRST SEEN Jan 19 2026 · Gg35_iQWx7g · 2:54 skills.sh/anthropics/skills/frontend-design (kare) → docs/departmanlar/frontend.md
- Hy3 (tencent), Step 3.7 Flash (stepfun), DeepSeek V4 Pro, MiniMax M3, Nemotron 3 Ultra (nvidia), GLM 5.2 (z-ai), Nemotron 3 Super (nvidia), Claude Sonnet 5 (anthropic, 559B tokens), Kimi K3 (moonshotai), Claude Opus 4.8 (anthropic, 391B tokens), MiMo-V2.5-Pro / MiMo-V2.5 (xiaomi) · Gg35_iQWx7g · 9:08 openrouter.ai/apps/hermes-agent model/token sıralaması (kare) → docs/departmanlar/frontend.md
- Prompt'tan tam site (React component'ler) üretimi · jGJ09wdTGDI · tahmin: Claude Design (yok) → docs/departmanlar/frontend.md
- Component bazlı dosya mimarisi (Nav.jsx, ProductCard.jsx, Primitives.jsx...) · jGJ09wdTGDI · tahmin: React (yok) → docs/departmanlar/frontend.md
- Tasarım token sistemi (spacing, corner radii, elevation, renk paleti) · jGJ09wdTGDI · tahmin: design tokens deseni (yok) → docs/departmanlar/frontend.md
- İkonografi kütüphanesi · jGJ09wdTGDI · Lucide 1.25 (yok) → docs/departmanlar/frontend.md
- Tipografi: display + UI + mono font üçlüsü (Cormorant Garamond + Inter + JetBrains Mono) · jGJ09wdTGDI · tahmin: web font servisi (yok) → docs/departmanlar/frontend.md
- Renk paleti tokenlaştırma (obsidian/emerald/champagne-gold) · jGJ09wdTGDI · tahmin: Claude Design (colors_and_type.css) (yok) → docs/departmanlar/frontend.md
- Responsive breakpoint testi (mobile/tablet/desktop) · jGJ09wdTGDI · tahmin: Chrome DevTools cihaz araç çubuğu (yok) → docs/departmanlar/frontend.md
- CSS Grid ile yerleşim · jGJ09wdTGDI · tahmin: CSS Grid (yok) → docs/departmanlar/frontend.md
- "Limited 40/yr", "Boutique only" · jGJ09wdTGDI · 4:48 CLAUDE marka etiketleri (kare) → docs/departmanlar/frontend.md
- HomeHero.jsx, HomeApp.jsx, BrandStory.jsx, FeaturedSection.jsx, NewsletterFooter.jsx, CartDrawer.jsx, Nav.jsx, ProductCard.jsx, Primitives.jsx, PressBar.jsx; sohbette "colors_and_type.css" ve token açıklaması (obsidian arka plan, emerald, champagne-gold, Cormorant Garamond + Inter + JetBrains Mono) · jGJ09wdTGDI · 7:18 Design Files paneli (kare) → docs/departmanlar/frontend.md
- Spacing, Corner radii, Elevation system, Spacing scale, Badges & tags, Buttons, Form inputs, Iconography - Lucide 1.25, Product card; sohbette "chat upstream error ... invalid_request_error ... 0 tokens" hata mesajı (görsel düzenleme isteğinde) · jGJ09wdTGDI · 9:23 Design System paneli (kare) → docs/departmanlar/frontend.md
- "iPad Mini 768x1024" cihaz simülasyonu, CSS grid-template-columns kodu · jGJ09wdTGDI · 11:24 DevTools (kare) → docs/departmanlar/frontend.md
- sohbet + görev paneli iki sütun yerleşimi (GOAT arayüzü, sol chat/sağ gelen kutusu-görevler) · XemheY_aM1g · tahmin: özel React uygulaması (GOAT), ekranda ad görünmüyor (yok) → docs/departmanlar/frontend.md
- liste + detay iki panelli grid (MiniMax'ten üretilen örnek arayüz önizlemesi) · XemheY_aM1g · tahmin: MiniMax'in ürettiği HTML/CSS, araç adı ekranda/açıklamada geçmiyor (yok) → docs/departmanlar/frontend.md
- tek CTA'lı kısa e-posta şablon düzeni (komut satırı ≤7 kelime, gövde 3-7 cümle) · XemheY_aM1g · tahmin: düz markdown şablon, framework yok (yok) → docs/departmanlar/frontend.md
- APP ACCELERATOR, BUSINESS, GOATSTARTER klasörleri · XemheY_aM1g · 3:42 VS Code karşılama ekranı, Recent (kare) → docs/departmanlar/frontend.md
- "Sosyal medya stratejisi / Carousel tasarla / Müşteri (lead) bul / Outreach kampanyası" görev listesi, Plan: Paid · XemheY_aM1g · 6:43 GOAT paneli (kare) → docs/departmanlar/frontend.md
- kategori listesi (Demo&Trial, Onboarding&Welcome, Satış&Closing, Partnership, İçerik&Newsletter, Event&Webinar, Feedback&Survey, İş Operasyon, Yatırımcı/PR, GOAT Tarzında), Toplam 100 şablon · XemheY_aM1g · 8:37 terminal çıktısı (kare) → docs/departmanlar/frontend.md
- Scroll'a bağlı video scrub animasyonu · 4cE9t4rE0-0 · tahmin: GSAP (ScrollTrigger) (yok) → docs/departmanlar/frontend.md
- Yumuşak/anchor kaydırma ile navbar geçişi · 4cE9t4rE0-0 · tahmin: GSAP ScrollToPlugin (yok) → docs/departmanlar/frontend.md
- Renk/tipografi sistemi (deep navy/ivory, Cormorant Garamond + Inter) · 4cE9t4rE0-0 · tahmin: Google Fonts (Cormorant Garamond, Inter) (yok) → docs/departmanlar/frontend.md
- Sabit navbar renk geçişi (transparent → ivory) · 4cE9t4rE0-0 · GSAP (yok) → docs/departmanlar/frontend.md
- Minimal footer + geniş whitespace grid · 4cE9t4rE0-0 · tahmin: CSS (grid/flex) (yok) → docs/departmanlar/frontend.md
- "Stripe Integrated Website", "LinkedIn Outreach Agent", "Multi-Agent Code Review", "Build a Mobile App" · 4cE9t4rE0-0 · 2:46 şablon kartları (kare) → docs/departmanlar/frontend.md
- "Luxury Yacht Cinematic Shot", "Luxury Yacht Scroll Hero", "Premium Perfume Landing..." · 4cE9t4rE0-0 · 4:35 sohbet listesi (kare) → docs/departmanlar/frontend.md
- "ONE ScrollTrigger... targetProgress = self.progress... gsap.ticker does the scrub" · 4cE9t4rE0-0 · 7:22 kod (kare) → docs/departmanlar/frontend.md
- 2,089" · 4cE9t4rE0-0 · 9:41 "Generated with Kling AI v3 (auto-routed for medium quality)"; "Credits Used (kare) → docs/departmanlar/frontend.md
- 2,836" · 4cE9t4rE0-0 · 11:38 deployed url "yacth-demo-website.abacusai.app" (ekranda böyle yazıyor); "Cormorant Garamond + Inter fonts, GSAP scroll reveals"; "Credits Used (kare) → docs/departmanlar/frontend.md
- e-posta contact.yildzdikme@gmail.com, Team "YildzDikme", Credits Total 20,000(20K), Used 7,201(7.2K), Remaining 12,897(12.9K); sol menüde "MCP Server Configuration" · 4cE9t4rE0-0 · 12:53 profil (kare) → docs/departmanlar/frontend.md
- kaydırmaya bağlı sahne geçişi (pencereden içeri girme, plan/metin belirme) · b-LZ_Y9wor8 · tahmin: GSAP ScrollTrigger (yok) → docs/departmanlar/frontend.md
- yumuşak (inertia) kaydırma · b-LZ_Y9wor8 · Lenis (yok) → docs/departmanlar/frontend.md
- 3D obje (jet modeli, blueprint girişli) · b-LZ_Y9wor8 · tahmin: WebGL/Three.js (yok) → docs/departmanlar/frontend.md
- sürüklenince fizik tepkili slider (kağıt sallanması) · b-LZ_Y9wor8 · tahmin: GSAP Draggable/Inertia (yok) → docs/departmanlar/frontend.md
- tipografi ile odak (iki kelimenin sırayla belirmesi) · b-LZ_Y9wor8 · tahmin: GSAP timeline (yok) → docs/departmanlar/frontend.md
- noktalı 3D dünya küresi (footer) · b-LZ_Y9wor8 · tahmin: cobe/globe.gl (ekranda/açıklamada ad geçmiyor) (yok) → docs/departmanlar/frontend.md
- varlıklar hazır olana kadar loading screen · b-LZ_Y9wor8 · tahmin: özel React loading state (yok) → docs/departmanlar/frontend.md
- "Yıldız Dikme — Creative Dev", "Jesko Jets", "Awwwards Nominees"; jeskojets.com'da "Gulfstream 650ER" uçak sayfası · b-LZ_Y9wor8 · 1:22 tarayıcı sekmeleri (kare) → docs/departmanlar/frontend.md
- Kaydırmaya bağlı 3D kamera animasyonu (scroll-tied camera pose) · iYwCzKy6W40 · tahmin: GSAP ScrollTrigger + R3F (web-sahne-desenleri) → docs/departmanlar/frontend.md
- Yükleme ekranında kameranın yavaşça açılışı (giriş animasyonu) · iYwCzKy6W40 · tahmin: React Three Fiber + GSAP timeline (web-sahne-desenleri) → docs/departmanlar/frontend.md
- 3D ürün modeli entegrasyonu (Sketchfab GLB indirme) · iYwCzKy6W40 · tahmin: three.js GLTFLoader (web-sahne-desenleri (GLB derleme notları)) → docs/departmanlar/frontend.md
- Responsive/mobil sahne testi · iYwCzKy6W40 · tahmin: R3F responsive canvas + DevTools cihaz modu (omer-kutuphaneler) → docs/departmanlar/frontend.md
- Performans denetimi (Lighthouse) · iYwCzKy6W40 · Chrome DevTools Lighthouse (yok) → docs/departmanlar/frontend.md
- WEBGI Camera Landing Page, Canon EOS 5D Mark IV, Three.js — JavaScript 3D Library, LUMEN Pro — Interactive 3D · iYwCzKy6W40 · 0:30 LUMEN sitesi, "Always shoot like a Pro" başlığı, URL 3d-camera-landing-page.netlify.app; sekmeler (kare) → docs/departmanlar/frontend.md
- "Canon EOS 5D Mark IV", Download 3D Model butonu, 25.3k triangles / 14.7k vertices · iYwCzKy6W40 · 2:33 Sketchfab model sayfası (kare) → docs/departmanlar/frontend.md
- WEBGI Camera Landing Page) · iYwCzKy6W40 · 10:41 camera-webgi.vercel.app (ilham alınan referans site; sekme adı (kare) → docs/departmanlar/frontend.md
- Performance 92, Accessibility 96, Best Practices 100, SEO 100; Dimensions: iPhone 14 Pro Max, DPR: No throttling · iYwCzKy6W40 · 12:45 Chrome DevTools Lighthouse sonucu (kare) → docs/departmanlar/frontend.md
- Kaydırınca eski haline dönen portal/kapı geçişi (glow çerçeveli telefon siluetinde manzara) · fCc97Rv-60w · tahmin: GSAP ScrollTrigger (yok) → docs/departmanlar/frontend.md
- Kaydırmaya bağlı 3D kredi kartı (yansıma, çip, eğim) · fCc97Rv-60w · tahmin: CSS 3D transform / Three.js (yok) → docs/departmanlar/frontend.md
- Kaydırmaya bağlı para birimi kaydırıcısı (slider kaydırınca hareket ediyor) · fCc97Rv-60w · tahmin: GSAP ScrollTrigger (yok) → docs/departmanlar/frontend.md
- Kaydırmaya bağlı ülke/isim listesi değişimi · fCc97Rv-60w · tahmin: GSAP ScrollTrigger (yok) → docs/departmanlar/frontend.md
- Bölüm bazlı snap kaydırma (Fable 5 versiyonu) · fCc97Rv-60w · tahmin: CSS scroll-snap (yok) → docs/departmanlar/frontend.md
- Çapraz (diagonal) tipografi, görsel yerine yazıyla anlatım · fCc97Rv-60w · tahmin: CSS transform rotate (yok) → docs/departmanlar/frontend.md
- Sürekli görünen ince kenar çizgisi (border) tüm bölümler boyunca devam eden görsel motif · fCc97Rv-60w · tahmin: yok (belirtilmedi) (yok) → docs/departmanlar/frontend.md
- kaydırmaya bağlı video scrub + sahne geçişi · 39IlNR-P3-Q · tahmin: scroll-craft (ekranda "scrollcraft.css" adı geçiyor, k00686) (bilgi/scroll-a-bağlı-video-scrub.md) → docs/departmanlar/frontend.md
- kaydırmaya bağlı kademeli metin belirme/kaybolma · 39IlNR-P3-Q · tahmin: scroll-craft (bilgi/scroll-a-bagli-kademeli-metin-belirme-reveal-fade-translatey.md) → docs/departmanlar/frontend.md
- sayfa içi konum göstergesi (scroll navigasyonu) · 39IlNR-P3-Q · tahmin: scroll-craft/custom (web-sahne-desenleri) → docs/departmanlar/frontend.md
- tutarlı tema/yoğunluk kararı (klasik vs. animasyonlu) · 39IlNR-P3-Q · taste-skill (yok) → docs/departmanlar/frontend.md
- footer'da mouse hover ışık efekti · 39IlNR-P3-Q · tahmin: custom CSS/JS (yok) → docs/departmanlar/frontend.md
- mobil görünüm devtools ile responsive test · 39IlNR-P3-Q · tahmin: Chrome DevTools (bilgi/responsive-mobil-sahne-testi.md) → docs/departmanlar/frontend.md
- Claude merkezde, dört skill — "Design DNA / Visual Analysis", "Frontend Design / Art Direction", "Taste / Design Character", "Scrollcraft / Scroll Experience" · 39IlNR-P3-Q · 0:26 (k00026) Skill diyagramı (kare) → docs/departmanlar/frontend.md
- zanwei/design-dna, nateherkai/scroll-craft, Leonxlnx/taste-skill, anthropics/skills — dört repo linki teyit · 39IlNR-P3-Q · 3:27 (k00207) Tarayıcı sekmeleri (kare) → docs/departmanlar/frontend.md
- "Ran page script", "Edited index.html +9", "Edited styles.css +20", "Edited site.js +29", "read sheet.png"; model seçici "Fable 5 · High" · 39IlNR-P3-Q · 11:26 (k00686) Claude Code ajan günlüğü (kare) → docs/departmanlar/frontend.md
- "Aurea, a journal of myth"; localhost:4500 üzerinde çalışıyor · 39IlNR-P3-Q · 12:29 (k00749) Site adı (kare) → docs/departmanlar/frontend.md
- iPhone 14 Pro Max, 430x932, HTML'de `sc-css`, `sc-scrub`, `data-scrub`, `sc-act--pinned` sınıfları — scroll-craft'ın CSS/attribute konvansiyonu · 39IlNR-P3-Q · 14:11 (k00851) Chrome DevTools (kare) → docs/departmanlar/frontend.md
- Koyu hero kartı, yeşil parlama çerçeve, düğüm-ağ (graph) görseli · oHKt0FUbR58 · 0:24 (kare) → docs/departmanlar/frontend.md
- Premium tasarım referanslarıyla ön yüz üretimi (impeccable skill) · lipJRiztOgM · 0:30 (altyazı) → docs/departmanlar/frontend.md
- Koyu tema dashboard, kart ızgarası, çubuk grafikler · 6cEQEba0i2A · 0:16 (kare) → docs/departmanlar/frontend.md
- Koyu tema infografik sayfası, üç istatistik kartı ve alıntı bloğu · 6cEQEba0i2A · 0:53 (kare) → docs/departmanlar/frontend.md
- İki sütunlu karşılaştırma kartları (yeşil/kırmızı vurgu) · 6cEQEba0i2A · 1:44 (kare) → docs/departmanlar/frontend.md
## Anatomi bekliyor
- 4cE9t4rE0-0
- b-LZ_Y9wor8
- iYwCzKy6W40
- fCc97Rv-60w
## Geliştirme önerileri
- jcode · video: Rust ile sıfırdan yazılmış açık kaynaklı kodlama ajanı harness'ı; otomatik hafıza, paralel oturum ve alt ajan iddiası. · bizde: Bizde 'codex' skill'i var: OpenAI Codex CLI sarmalayıcısı. jcode ile aynı türde değil; jcode ayrı bir harness. · fark: Kanıt yalnız 'Rust ile yeniden yazıldı' ifadesi. Hafıza ve paralel oturum iddiaları doğrulanmadı; jcode'un codex ile ilişkisi bilinmiyor. · yok: Kanıt zayıf olduğundan değişiklik önerilmiyor. İstenirse jcode reposu ayrıca incelenebilir. · kanıt: Video enFgYQvI1dM 0:30: karede 'rebuilt it from scratch in rust' yazısı. Hafıza iddiası için ayrıntı yok.
- graphify · video: Kod tabanını bir kez okuyup bilgi grafiği çıkarır; sonraki oturumlarda Claude dosyaları yeniden okumak yerine grafikte gezinir. · bizde: Bizde kayıt yok. Kod tabanı için bilgi grafiği aracı görünmüyor. · fark: Bizde her oturumda dosyaların yeniden okunması muhtemel; grafik bu maliyeti azaltabilir. Etkisi ölçülmedi. · ÖĞREN: Not al. Büyük bir repoda deneme yapılırsa token tasarrufu ve doğruluk ölçülür. Bu videolarda ölçüm yok. · kanıt: oHKt0FUbR58 0:24: karede 'Any input. One graph. Complete recall.' sayfası, altyazıda 'called Graphify'. klDiYMzW0o0 0:00: aynı çalışma şekli anlatılıyor.
- headroom · video: Kullanıcı ile model arasına girip gereksiz içeriği Claude'a ulaşmadan sıkıştırır. · bizde: Bizde kayıt yok. Bağlam sıkıştırma için claude-mem var ama o hafıza katmanı, headroom ise girdi sıkıştırma katmanı. · fark: Girdi tarafında sıkıştıran ara katman bizde görünmüyor. Nasıl çalıştığı ve kayıp riski videoda anlatılmıyor. · ÖĞREN: Not al; yalnızca 'sıkıştırma katmanı' tanımı var. Yöntemi ve güvenliği repodan doğrulanana kadar kurma. · kanıt: klDiYMzW0o0 0:00: altyazıda birinci araç olarak sıkıştırma katmanı diye anlatılıyor.
- ponytail · video: Dördüncü araç; işlevi açıklanmıyor, yalnız token sorununa karşı araçlardan biri olarak anılıyor. · bizde: Bizde ponytail plugin'i kurulu: en basit, kısa çözümü zorlar (YAGNI, stdlib öncelikli). · fark: Videoda işlevi anlatılmıyor; karşılaştıracak bir yan yok. · yok: Yok. · kanıt: klDiYMzW0o0 0:00: altyazıda yalnız 'Sonuncusu Ponytail' deniyor.
- superpowers · video: Claude'u yavaşlatıp planlatır ve işe başlamadan kendi işini kontrol ettirir. · bizde: Bizde superpowers plugin'i kurulu (TDD, hata ayıklama, iş birliği desenleri). · fark: Videodaki kullanım (planlama ve öz kontrol) bizdeki plugin'in kapsamında. Bizde olmayan bir yan görünmüyor. · yok: Yok. · kanıt: lipJRiztOgM 0:00: altyazıda ikinci skill olarak anlatılıyor; yeni bir özellik iddiası yok.
- claude-mem · video: Oturumlar arası hafıza sağlar; proje ve dosyalar yeniden anlatılmaz. · bizde: Bizde claude-mem plugin'i kurulu (oturumlar arası bağlam saklama). · fark: Aynı araç, aynı işlev; videoda ek bir yan yok. · yok: Yok. · kanıt: lipJRiztOgM 0:22: karede claude-mem yıldız geçmişi grafiği; altyazı 'remembers'.
- impeccable · video: Ön yüz için premium referanslardan tasarım zevki katar; 'slop' görünümü azaltır. · bizde: Bizde impeccable plugin'i kurulu (23 komut, anti-pattern tespiti). · fark: Aynı araç; videoda bizde olmayan bir özellik yok. · yok: Yok. · kanıt: lipJRiztOgM 0:30: altyazıda dördüncü skill olarak anlatılıyor; ek ayrıntı yok.
- task-observer · video: Çalışma tarzını izleyip diğer skill'leri arka planda iyileştirir. · bizde: Bizde anthropic-skills:task-observer skill'i var; çok adımlı işlerde skill iyileştirme fırsatlarını izler. · fark: Aynı araç, aynı amaç; bizde olmayan bir yan görünmüyor. · yok: Yok. · kanıt: lipJRiztOgM 0:30: altyazıda beşinci skill olarak anlatılıyor; ek ayrıntı yok.
- claude-code · video: Terminale komut kopyalanarak kurulan, web sitesi üretiminde kullanılan kodlama aracı. · bizde: Bizde ayrı kayıt yok; ama zaten Claude Code ortamında çalışıyoruz. · fark: Videoda yalnız kurulum anlatılıyor; geliştirilecek bir yan yok. · yok: Yok. · kanıt: M9qgd_KJkWc 0:00: 'install Cloud Code ... copy the command into your terminal'. Yeni bir yetenek iddiası yok.
- rtk · video: Ajan ile CLI arasında duran proxy/hook; Bash çıktısını kırpıp modele daha az token gönderir. Videoda %60-90 tasarruf iddiası var. · bizde: Bizde kayıt yok. Bash çıktısı ham haliyle modele gidiyor gibi görünüyor. · fark: Hook ile komut çıktısını kısaltmak bizde olmayan somut bir yöntem. Diyagramda git status için yaklaşık 300 token, doğrudan ise 600 token. Bu iddia kaynakta ölçülmüş değil. · UYARLA: Uyarla: Bash çıktısı için PreToolUse/PostToolUse hook'unda çıktı kırpma ekle veya rtk'yi dene. Önce bir repoda token ölçümü yap; bilgi kaybı riskini kontrol et. · kanıt: g89FJiNAlEs 0:50: diyagramda 'rtk git status' hook akışı ~300 token, doğrudan 'git status' ~600 token.
## Defter
1 çağrı · $0.0534 · 8913 jeton
