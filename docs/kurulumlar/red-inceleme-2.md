# RED-İNCELE-2 (tur5b-1 RED, 77 satır)

Kaynak: docs/kurulumlar/tur5b-1-sonuc.tsv sınıfı RED; her satır örnek videosunun docs/video-tarama raporuyla eşlendi. Tam tablo: red-inceleme-2.tsv. Kurulum yapılmadı.

Sınıf sayıları: KURTAR 13 · ÖĞREN 15 · UYARLA 3 · DİKKAT 5 · GÜRÜLTÜ 41

## DİKKAT
### AI/ajan
- **Higgsfield API (aFEEwCteLe4)** (aktanilanlararastirlacaklargereklihttps/wwwyoutube.c.sk) — Satır adı "aktarılan araştırılacaklar gereken youtube..." notunun OCR kırığı. Video: Higgsfield bağlantısı işbirliği/affiliate; kullandıkça öde (demo üretim başı ~0,31 $). API anahtarını prompta yapıştırma, .env.local kullan. Satır 17-26 aynı kırık.
- **paperclipai/paperclip (erclip/v2026.831 kırığı)** (erclip/v2026.831) — 7RVf25Rg0Mc (NetworkChuck): Claude Code/Codex/Hermes'i tek "şirket" altında yöneten meta-harness. Kurulum `curl -fsSLO .../v2026.831.1/scripts/install.sh; bash install.sh` → `paperclipai onboard`; `paperclipai auth bootstrap-ceo`. curl|bash: önce scripti oku. Lisans bu turda doğrulanmadı (tur5b-1 notunda MIT, AYRI-UYGULAMA).
- **multica-ai/multica** (github.com/multica) — ig-DdO1UioAHAS: görevleri Claude Code/Codex/Cursor'a takım arkadaşı gibi atan platform; özel/belirsiz lisans → önce LICENSE oku. Skill değil. [NOASSERTION · 52k★]
- **multica-ai/multica (github.con kırığı)** (github.con/multica) — ig-DdZQ5SaDxDV: aynı repo, aynı lisans uyarısı. [NOASSERTION · 52k★]
### diğer
- **Genspark GenMail https://www.genspark.ai/genmail** (genmail.go.link) — genmail.go.link = sponsorlu e-posta ajanı (4Hvkv_I8QDE, 10:42). Kapalı ticari servis, gelen kutusuna erişim ister; gizlilik riski. Kurulacak şey yok.

## ÖĞREN
### tasarım/frontend
- **Astraea (demo marka, repo değil)** (astraeatrav) — r68MhqAUvR8: site akışı = isim önerisi → marka renk/logo → bölüm planı → tek ana prompt (üretim kalitesi, duyarlı, 3B hero, mobil, erişilebilirlik, azaltılmış hareket, görseller Higgsfield) → deploy.
- **astro-auts/pilots (repo yok, gh 404)** (astro-auts/pilots) — Astraea sitesinin Crew/astronot bölümü; nav: Destinations/Fleet/Experience/Crew/Book a Trip. Bölüm-listesi promptu için ilham.
- **Figma Dev Mode → Claude Code, Astro + scroll-video** (feature/accord_) — YUWBku1cNEA: Figma Dev Mode'daki örnek prompt Claude Code'a yapıştırılıp Astro 5 sitesi kurduruluyor; Seedance ile inşaat zaman atlaması, kaydırmaya bağlı kare oynatma (sticky bölüm). 4 ayrı video tutarsız çıkınca tek 20 sn'lik videoya geçildi (tutarlılık ipucu). Higgsfield sponsorlu.
- **Chase AI: zevk kütüphanesi + Impeccable + taste-skill** (fonts.gstatic.com") — 7FU98O0JLHs: (1) Dribbble/Pinterest/X ilhamını toplayan yerel "zevk kütüphanesi" uygulaması yaptır (grup, anahtar kelime, copy brief); (2) Impeccable (`npx impeccable detect`, 46 slop deseni) + Taste Skill + 21st.dev "copy prompt"; (3) önce 5 stil, sonra 3 varyant üret, "tweaks" paneliyle ince ayar. Impeccable ve taste-* zaten kurulu.
### video/içerik
- **storytold/photocraft (ana depo storytold/artcraft)** (apollo) — eFB79TYI-Vw: "apollo" raporda yok. Video ArtCraft/PhotoCraft/LightCraft/FilmCraft (saf Rust, Adobe alternatifi masaüstü uygulamaları) deniyor; PhotoCraft'ın CLI, JSON control channel ve MCP server arayüzü var. Kurulabilir skill değil; FilmCraft en zayıfı. [Apache-2.0 · photocraft 38106★, artcraft 12601★]
- **ChatGPT master prompt + Google Flow/Nano Banana 2 + ElevenLabs + CapCut** (3d/editorial) — MIiwOtKf3SI: Tek master prompt aşama aşama ilerleyip kullanıcı yanıtını bekler; görseller Flow'da Nano Banana 2, 6 sn klipler Omni 1.1 Flash, ses ElevenLabs. CapCut: klip sonuna opacity keyframe (%0) + cubic ease, sonraki kliplere "Zoom 1" combo animasyonu, hepsi compound clip.
- **Higgsfield CLI/MCP + higgsfield-ai/skills** (digitaleconomy.stanf@d.edu) — d67-HDSvMw8: Opus 5.5 + ffmpeg + whisper ile 3 dk düz anlatımı 44 sn 9:16 Reel'e kesiyor, üst yarıya Higgsfield görsel/Seedance video koyuyor. Kurulum `npm i -g @higgsfield/cli`, `npx skills add higgsfield-ai/skills` (ücretli hesap/kredi gerekir). Ağız-ses senkronu ve kelime kesilmesi hataları adım adım düzeltiliyor; sponsorlu. [MIT · 1251★]
### AI/ajan
- **obra/superpowers + Context7 + Playwright MCP** () — EIoPt1ry6ng: Claude Code'a 3 paralel subagent (DB, API, Frontend); ana oturum orkestratör, tek doğruluk kaynağı CONTRACT.md + Store interface + bellek içi sahte uygulama. Codex ile ikinci görüş denetimi (38 dosya, 0 critical, 4 high); GPT-5.4 mini ile normal arası ~24x maliyet farkı.
- **Codex tek-prompt Next.js kalıbı (aFEEwCteLe4)** (aktanilanlararatirlacaklargereklihttps/wwwyoutube.c.sik) — Tek promptla uygulama yaptırma: "önce docs kaynaklarını oku, desteklenmeyen parametre uydurma, polling kullan, sahte yanıt yok, butona basmadan ücretli üretim başlatma, maliyeti README'de belirt". Ücretli API tarifleri için güvenlik kalıbı; bizim "sayısal tavan" kuralıyla örtüşür.
- **claude.ai artifact** (claude.i) — DO45w8HX6nA: tasarım için önce dummy veriyle artifact üret, link üzerinden revize et, beğenilince "projeye uygula" de ("Claude Design gibi"). Ek: `/rename` ile Claude Code oturumlarını adlandırma ipucu (31:12).
- **DeepSeek V4 Flash (OpenRouter: deepseek/deepseek-v4-flash)** (deepseek/deepseek-v4-flash) — DYdvJCxWd6M (Hermes Agent): ana model olarak seçildi; OpenRouter'da 105 istekte ~13 sent, 5 $ haftalarca yeter; Nous Portal ~20 $/ay sabit. Ucuz ajan modeli + haftalık 10 $ limit = maliyet stratejisi. Ek: Hermes ajanı kendi skill'ini yazıp cron ile zamanlıyor.
- **Opus 5.5 + Higgsfield MCP + Expo** (doc) — eIkTn5kgNaI: kodsuz Expo su-takibi uygulaması; rakip uygulama ekran kaydı/mağaza görselleri analiz ettirilip farklılaşma planı; Opus iOS Simulator'ü ekran görüntüsüyle kendi test ediyor; `npx eas-cli@latest init/login` ile TestFlight. ~160 Higgsfield kredisi.
- **https://github.com/gsd-build/get-shit-done (GSD)** (github.com/gsd-build) — DO45w8HX6nA: npm harness, ECC/superpowers ile çakışır. Yazar yeni modellerde (auto mod) GSD'ye gerek kalmadığını söyleyip projeden kaldırıyor: "önemli planları not alıp sil, özet dosyası çıkar". Gereksiz context-engineering katmanını bırakma deneyimi. [MIT · 64331★]
- **Hermes Kanban (~/.hermes/kanban.db SQLite)** (gkihk/kanban_setups_megathread_hermes_agent_june) — 4Hvkv_I8QDE (16:58): Hermes Kanban SQLite'ta tutuluyor; başlık reddit "kanban setups megathread" benzeri, repo değil.
### diğer
- **googleapis.com (Google Cloud API)** (googleapis.com) — DWMGfkFD5SI: Cloud Console'da Gmail/Sheets/Docs/Drive API açılıp OAuth istemcisi oluşturulur; sonra `gws auth login --services drive,docs,sheets,gmail`. Yalnız okuma için `--readonly`.

## UYARLA
### tasarım/frontend
- **https://github.com/crmsnbleyd/flexoki-emacs-theme** (crmsnbleyd/flexoki-emacs-theme) — Flexoki'nin Emacs teması; lisanssız, kapsam dışı. Palet için MIT kepano/flexoki (satır 0) yeter; kod alınmaz. [lisans yok · 34★]
- **https://github.com/DavidHDev/react-bits** (davidhdev/react-bits) — ig-DePLcw_Dbwo: kopyala-yapıştır React bileşen kitaplığı. Commons Clause: yeniden satış amaçlı kullanım yasak. Mekanizma: GSAP (kaydırma efektleri) + Lenis (smooth scroll) + React Bits bağlantılarını Claude Code'a verip `npm install gsap lenis` yaptırmak = "AI slop" sitelerden kaçınma. frontend-craft'a "hareket araçları" kaynağı olarak eklenebilir; kod kopyalanmaz. [MIT + Commons Clause · 48816★]
- **getlayers.ai/templates** (getlayers.al/templates) — ig-DeMmzkxMpFZ: "copy prompt" şablonlu sinematik 3B siteler (Three.js, Next.js). Prompt içeriği gösterilmiyor; ToS belirsiz. frontend-craft'a "3B/immersive web referans prompt yapısı" fikri olarak alınabilir; içerik kopyalanmaz. [lisans yok]

## KURTAR (KUR-aday işaretli)
- https://github.com/kepano/flexoki — MIT · 3694★ — tasarım/frontend: Obsidian Flexoki teması videoda gösterildi (4Hvkv_I8QDE, 4:32); Steph Ango'nun mürekkep tonlu renk paleti. Skill/plugin değil, palet referansı; KUR-aday değil.
- https://github.com/gowtham0992/link — MIT · 201★ — AI/ajan: "Local personal memory for LLM agents"; kökte skills/, integrations/, mcp_package/. Videoda adı doğrulanamadı (Obsidian second-brain teması). Kurulmadan önce SKILL.md/MCP ve güvenlik incelenmeli; KUR-aday değil.
- https://github.com/equationalapplications/curated-thoughts — MIT · 20★ — AI/ajan: Özel second-brain masaüstü uygulaması (Tauri 2 + React + Rust + Ollama). Skill değil, uygulama; videoda adı doğrulanamadı. KUR-aday değil.
- https://github.com/agentskills/agentskills — Apache-2.0 · 26007★ — AI/ajan: Agent Skills şartname + dokümantasyon deposu (agentskills.io); SKILL.md yok. Skill yazımında referans, KUR-aday değil.
- https://github.com/DeusData/codebase-memory-mcp — MIT · 46266★ — AI/ajan: KUR-aday (graphify ile karşılaştır). ig-DbL-SXnMKDF: tree-sitter ile kod bilgi grafı çıkaran MCP, tek statik binary; install.sh `curl | bash`. "31 repoda ~10x az token" iddiası anlatıcıya ait, kanıtsız.
- **KUR-aday** https://github.com/microsoft/markitdown (+ markitdown-mcp) — MIT · 189296★ — AI/ajan: KUR-aday. ig-DcTI5sfoLGR: PDF/Word/Excel/PowerPoint/YouTube → temiz markdown; `pip install markitdown-mcp`, tek araç convert_to_markdown(uri). "%70 token tasarrufu" iddiası kanıtsız. İpucu: "PDF'leri hep önce MarkItDown'a gönder".
- **KUR-aday** https://github.com/googleworkspace/cli (gws) — Apache-2.0 · 31285★ — AI/ajan: KUR-aday. Drive/Docs/Sheets/Gmail komut satırı; `npm install -g @googleworkspace/cli`; skill: `npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-docs` (gws-drive/gmail/sheets/shared). OAuth ile kişisel hesaba yazma yetkisi → önce `--readonly`.
- https://github.com/equationalapplications/curated-thoughts-integrations — MIT · 2★ — AI/ajan: Curated Thoughts'u Hermes/OpenClaw/Claude Code harness'larına bağlayan entegrasyonlar; videoda geçmiyor, düşük ★. KUR-aday değil, izle.
- https://github.com/euandeas/omarchy-flexoki-dark-theme — MIT · 42★ — tasarım/frontend: Omarchy (Linux WM) için Flexoki dark; kapsam dışı.
- https://github.com/docling-project/docling — MIT · 68k★ — AI/ajan: ig-DdZQ5SaDxDV: PDF/DOCX → Markdown/JSON Python kütüphanesi/CLI. Skill değil; KUR-aday değil.
- **KUR-aday** https://github.com/jasonlee-breadcrumb/motion-os — MIT · 37★ — video/içerik: KUR-aday. J4oygRI6mN0: Claude Code skill'i; Claude kodla (Remotion) hareketli grafik üretir, localhost:4323'te sahne sahne oynatıcı, "Send to Claude" ile değişiklikler tek prompta toplanır. İpucu: Seedance önce 480p taslak, sonra 1080p (kredi tasarrufu). Higgsfield sponsorlu.
- https://github.com/Yeachan-Heo/oh-my-claudecode — MIT · 40k★ — AI/ajan: ig-DdO1UioAHAS: ekip odaklı çoklu ajan plugin'i; marketplace tamamı ECC ile çakışır. KUR-aday değil.
- https://github.com/shareAI-lab/learn-claude-code — MIT · 78k★ — AI/ajan: Claude Code ajan mimarisi öğretici repo (4 skill: agent-builder, code-review, mcp-builder, pdf); mevcutlarla çakışır. KUR-aday değil, öğrenme kaynağı.

## GÜRÜLTÜ: 41 satır (OCR kırığı, OpenRouter model kimlikleri, ilgisiz bağlantılar); gerekçeler TSV'de.
