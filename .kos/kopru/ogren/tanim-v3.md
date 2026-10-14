# ÖĞREN-0b kategori tanımı v3 (ana + ikincil)

Her araca TAM OLARAK bir ANA kategori ver (aracın asıl işi: kullanıcı onu neyi yapmak için çağırır?). İkinci bir alan da belirgin ise İKİNCİL kategori ver, yoksa "". Kategori adları aşağıdakiyle birebir.

Genel kurallar
- "Claude", "agent", "skill", "MCP" sözcüğü geçiyor diye ajan-orkestrasyon seçme; aracın konusuna bak.
- Bir servisin MCP'si/plugin'i/skill'i o servisin alanına gider: Supabase/Postgres → veri-db, Vercel/Azure/AWS/Sentry/Convex → backend-dotnet, Figma → frontend-tasarım, Notion/Google Docs → belge, Firecrawl/Exa → araştırma.
- Açıklama boşsa ad + yer (dizin/plugin adı) + ilk satırlardan karar ver; hâlâ anlaşılamıyorsa diğer.
- Model ya da ajan rol adı (ör. "Frontend Developer", "SEO Specialist") rolün alanına gider.

token — LLM jeton/maliyet/bağlam tasarrufu: sıkıştırma, önbellek, bağlam penceresi yönetimi, bağlamı küçülten özet/compact, jeton/maliyet ölçümü, model yönlendirme (router/proxy), bağlam tasarrufu için hafıza.
  Sınır: claude-mem/context-mode/headroom/rtk burada (amaç bağlamı küçültmek). Genel "proje hafızası/not defteri" bağlam tasarrufu amaçlı değilse ajan-orkestrasyon. Bulut maliyeti (AWS fatura) backend-dotnet.
frontend-tasarım — UI/UX, web arayüzü, CSS/Tailwind, React/Vue/Svelte, animasyon, tipografi, tasarım sistemi, erişilebilirlik (a11y), web sitesi/landing page kurma, mobil uygulama arayüzü.
  Sınır: erişilebilirlik borcu takibi burada (a11y), test-qa değil. Three.js sahnesi 3d. Figma burada. Sunum slaytı belge.
video-medya — video, ses, müzik, TTS/ses sentezi, görsel/resim üretme-düzenleme, ffmpeg, transkripsiyon, OCR görüntü işleme modelleri.
  Sınır: kısa video İÇERİK STRATEJİSİ (hook, izleyici tutma, yayın takvimi) pazarlama. OCR ile belge çıkarma (PDF metni) belge. tessdata (OCR dil verisi) burada.
3d — Blender, three.js/WebGL 3B sahne, 3B model, mesh, shader, CAD.
  Sınır: oyun motoru (Unity/Godot) oyun-mod. 2B görsel üretimi video-medya.
test-qa — test yazma/koşma, QA, kod inceleme (code review), lint/format, uygulama kodunun doğrulanması, hata ayıklama (debug), TDD, e2e/Playwright testleri.
  Sınır: dağıtım öncesi altyapı doğrulama (azure-validate) backend-dotnet. Skill/plugin doğrulayıcı ajan-orkestrasyon. Güvenlik taraması güvenlik. Tasarım kalıbı önerisi backend-dotnet.
güvenlik — güvenlik açığı, pentest, gizli anahtar taraması, saldırı/savunma, tehlikeli komut engelleme, prompt injection savunması, kimlik doğrulama sertleştirme, tehdit modeli.
  Sınır: genel "dikkatli ol" hook'u değil, açıkça güvenlik amaçlı olan. Ağ güvenlik duvarı yapılandırması backend-dotnet ile çiftse ana güvenlik yalnız amaç saldırı/savunma ise.
backend-dotnet — GENEL YAZILIM MÜHENDİSLİĞİ ve altyapı: backend, API sunucusu, .NET/C#, Python/Go/Rust/Java/Node uygulama kodu, mimari ve tasarım kalıpları, refactor, paketleme/installer, deploy, CI/CD, git/GitHub iş akışı, devops, Docker/K8s, bulut (Azure/AWS/GCP), ağ/sunucu yönetimi, homelab, geliştirme modu/IDE geçişleri, eski sistem göçü.
  Sınır: "architect / yaklaşım seç / özellik tasarla" burada (frontend-tasarım değil, UI'a özgü değilse). Python installer (Nuitka) burada. Ağ mühendisliği (Huawei/H3C yönlendirme) burada. Veritabanı şeması veri-db. Mobil uygulama arayüzü frontend-tasarım.
veri-db — veritabanı, SQL, veri analizi, ETL, tablo/CSV/Excel verisi analizi, veri görselleştirme (grafik/dashboard), makine öğrenmesi (model eğitimi, ML deney izleme, hiperparametre), vektör DB.
  Sınır: ML burada, bilim değil. Excel/Word belge OLUŞTURMA belge; Excel veri ANALİZİ veri-db.
ajan-orkestrasyon — AI ajanları ve Claude Code'un kendisi: subagent tanımı, çoklu ajan, iş akışı/workflow otomasyonu, hook/telemetri/plugin/skill yazma-doğrulama-yönetme, CLAUDE.md/AGENTS.md talimat dosyaları, prompt mühendisliği, LLM/Claude API SDK entegrasyonu (messages-api-sdk), plugin'in kendi özellik/yardım/kurulum komutları (whats-new, setup), kullanıcı duygu/niyet okuma gibi ajan davranışı.
  Sınır: agents-md (talimat dosyası yazar) burada, belge değil. Plugin "yeni özellikler" komutu burada, belge değil. Genel yazılım geliştirme modu backend-dotnet.
belge — doküman, PDF/Word/PowerPoint/Excel dosyası oluşturma-düzenleme, rapor, makale/blog yazımı, sunum, not alma (Obsidian vb.), teknik dokümantasyon (README/API doc), çeviri, yazım üslubu.
  Sınır: AGENTS.md/CLAUDE.md ajan-orkestrasyon. Akademik makale okuma/yazma bilim ile çiftse konu bilimse ana bilim.
araştırma — web arama, scraping/crawl, tarayıcı otomasyonu, bilgi toplama, derin araştırma, rakip/pazar BİLGİSİ toplama, haber/RSS, YouTube/Reddit/X okuma.
  Sınır: tarayıcıyla TEST etmek test-qa. Rakip analizinden strateji çıkarmak pazarlama.
oyun-mod — oyun, oyun modu, Minecraft, Unity, Godot, Roblox, oyun tasarımı, oyun varlıkları.
  Sınır: oyun için 3B model üretimi 3d ile çift; ana oyun-mod yalnız amaç oyunsa.
pazarlama — pazarlama, satış, SEO, reklam, sosyal medya ve kısa video içerik stratejisi, marka, e-posta kampanyası, iş/girişim stratejisi, ürün yönetimi (PM, roadmap), fiyatlandırma, müşteri desteği, hukuk/finans iş araçları.
  Sınır: SEO teknik site sağlığı da burada. Finansal piyasa veri analizi veri-db.
bilim — akademik bilim: fizik, matematik, biyoloji, kimya, tıp, astronomi, akademik makale/literatür, bilimsel hesaplama.
  Sınır: ML/veri bilimi veri-db.
diğer — hiçbirine uymayan: genel geliştirici CLI'ları/paket yöneticileri (uv, npm, node, winget) kendi başına, kişisel gelişim/üretkenlik, sohbet tonu/kişilik, işi anlaşılamayan kurulum betikleri.
  Sınır: kullanıcı duygu durumu algılama (frustration-detection) ajan davranışıysa ajan-orkestrasyon; yalnız kişisel koçluksa diğer.
