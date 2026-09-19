# KURULUM-6 · claude.ai yükleme sırası · 19 Eyl 2026

99 zip (dist/, SkillSpector'ı geçenler) üç gruba ayrıldı; grup içinde sıra SKILL.md byte'ı küçükten büyüğe. Satır: zip · kaynak repo · ne yapar. UI dışı = çakışma taramasında ALAN DIŞI çıkan ya da UI'a dokunmayan (superpowers). Benzersiz = set içinde aynı işi yapan başka zip yok; aynı işi yapan çiftte A-kovasındaki (CC'de kullanılan) ya da ailenin CLI sürümü G1'de kalır, diğeri G2'ye iner. Kaynak: docs/kurulum-6-envanter.md, docs/kurulum-6-cakisma.md.

## G1 · önce — çakışmada kazanan taraf + UI dışı benzersiz yetenek (59)

1. omniroute-cli-models.zip · CullinanCloud/omniroute · Kullanılabilir modelleri, takma adları ve kataloğu CLI'dan sorgular.
2. omniroute-omni-proxies.zip · CullinanCloud/omniroute · Sağlayıcı isteklerine HTTP/HTTPS/SOCKS proxy kuralları ve rotasyonu tanımlar.
3. omniroute-config-codex-cli.zip · CullinanCloud/omniroute · OpenAI Codex CLI'yi OmniRoute'u OpenAI uyumlu arka uç olarak kullanacak şekilde yapılandırır.
4. omniroute-omni-webhooks.zip · CullinanCloud/omniroute · Webhook uç noktalarını ve olay aboneliklerini kaydeder, test eder, yeniden denemeleri yönetir.
5. omniroute-omni-budget.zip · CullinanCloud/omniroute · Anahtar başına ya da genel harcama limiti, token kotası ve hız sınırı tanımlar.
6. omniroute-omni-github-skills.zip · CullinanCloud/omniroute · GitHub repolarındaki SKILL.md/CLAUDE.md benzeri ajan dosyalarını arar, puanlar, tarar ve içe aktarır.
7. omniroute-cli-routing.zip · CullinanCloud/omniroute · Yönlendirme kombinasyonlarını ve yedek zincirlerini CLI'dan oluşturur ve test eder.
8. omniroute-cli-health.zip · CullinanCloud/omniroute · Sunucu sağlığını, bileşen durumunu ve devre kesici metriklerini CLI'dan canlı izler.
9. omniroute-cli-tunnel.zip · CullinanCloud/omniroute · ngrok/Cloudflare tünellerini CLI'dan başlatır, durdurur ve erişimi test eder.
10. skills-internal-comms.zip · anthropics/skills · Şirket içi iletişim metinlerini şirketin kullandığı formatlarda yazar. · claude.ai Directory'den açılır, yüklenmez (dist/_yerlesik/)
11. ponytail-ponytail-audit.zip · DietrichGebert/ponytail · Tüm repoda aşırı mühendisliği tarayıp silinecek, sadeleşecek ve stdlib ile değişecekleri sıralar.
12. ponytail-ponytail-debt.zip · DietrichGebert/ponytail · Koddaki `ponytail:` yorumlarını bir borç defterine toplar.
13. omniroute-cli-mcp.zip · CullinanCloud/omniroute · MCP sunucu durumunu, kayıtlı araçları ve denetim loglarını CLI'dan inceler.
14. omniroute-cli-a2a.zip · CullinanCloud/omniroute · OmniRoute A2A sunucusuna CLI'dan görev gönderir ve JSON-RPC 2.0 ajanlar arası protokolü test eder.
15. ponytail-ponytail-gain.zip · DietrichGebert/ponytail · ponytail'in ölçülmüş etkisini (daha az kod, maliyet, süre) skor tablosu olarak gösterir.
16. omniroute-cli-resilience.zip · CullinanCloud/omniroute · Devre kesici, bekleme, kota ve geri çekilme durumlarını CLI'dan yönetir.
17. omniroute-cli-compression.zip · CullinanCloud/omniroute · RTK filtreleri, Caveman kuralları ve katmanlı sıkıştırma modlarını CLI'dan ayarlar ve önizler.
18. omniroute-cli-batches.zip · CullinanCloud/omniroute · CLI'dan toplu çıkarım (batch) işi gönderir, izler ve sonuçları alır.
19. ponytail-ponytail-review.zip · DietrichGebert/ponytail · Diff'i yalnız aşırı mühendislik açısından inceler; gereksiz soyutlama ve bağımlılıkları bulur.
20. taste-skill-full-output-enforcement.zip · Leonxlnx/taste-skill · Kısaltma ve yer tutucu kodu yasaklayıp eksiksiz kod çıktısı zorlar, token sınırında düzgün böler.
21. omniroute-cli-keys.zip · CullinanCloud/omniroute · OmniRoute API anahtarlarını CLI'dan oluşturur, döndürür, iptal eder; OAuth akışlarını yönetir.
22. ponytail-ponytail-help.zip · DietrichGebert/ponytail · Tüm ponytail modları, skill'leri ve komutları için hızlı başvuru kartı gösterir.
23. superpowers-requesting-code-review.zip · obra/superpowers · İş bitince ya da birleştirmeden önce gereksinime göre kod incelemesi ister.
24. omniroute-cli-cost-usage.zip · CullinanCloud/omniroute · Sağlayıcı/model/tarih bazında maliyet, token kullanımı ve çağrı loglarını CLI'dan gösterir.
25. omniroute-cli-policy-audit.zip · CullinanCloud/omniroute · Denetim loglarını, erişim politikalarını ve telemetriyi CLI'dan inceler.
26. omniroute-cli-setup.zip · CullinanCloud/omniroute · İlk kurulumu, genel CLI ayarlarını, ortam değişkenlerini ve otomatik başlatmayı yapılandırır.
27. nano-banana-2-mcp-generate-image.zip · daveremy/nano-banana-2-mcp · nano-banana-2 MCP araçlarıyla iyi prompt pratiğiyle görsel üretir ve düzenler.
28. superpowers-verification-before-completion.zip · obra/superpowers · Bitti demeden önce doğrulama komutlarını çalıştırıp çıktıyı kanıt olarak ister.
29. omniroute-cli-backup-sync.zip · CullinanCloud/omniroute · OmniRoute verisini CLI'dan yedekler, buluta eşitler, zamanlar ve arşivden geri yükler.
30. strix-web-app-penetration-testing.zip · usestrix/strix · Canlı URL, staging ya da yerel sunucuya uçtan uca kara kutu sızma testi yapar.
31. strix-find-security-vulnerabilities-in-code.zip · usestrix/strix · Strix ile kaynak kodda veri akışı ve yetki modeline dayalı beyaz kutu güvenlik incelemesi yapar.
32. omniroute-cli-plugins-skills.zip · CullinanCloud/omniroute · Omni Skills, plugin'ler ve kalıcı hafızayı CLI'dan yönetir.
33. strix-application-security-testing.zip · usestrix/strix · Ürün genelinde hangi varlığa hangi Strix testinin gerektiğini seçer, çalıştırır, rapora çevirir.
34. omniroute-cli-contexts.zip · CullinanCloud/omniroute · Bağlam mühendisliği ayarlarını, RTK filtre setlerini ve konuşma oturumlarını CLI'dan yönetir.
35. strix-fix-security-vulnerabilities-with-strix.zip · usestrix/strix · Strix bulgularını önem sırasıyla yamalar ve yeniden tarayarak düzeltmeyi kanıtlar.
36. superpowers-dispatching-parallel-agents.zip · obra/superpowers · Bağımsız iki ya da daha fazla işi paylaşılan durum olmadan paralel ajanlara dağıtır.
37. superpowers-receiving-code-review.zip · obra/superpowers · Gelen inceleme geri bildirimini uygulamadan önce teknik olarak doğrular.
38. strix-owasp-top-10-testing.zip · usestrix/strix · Uygulamayı OWASP Top 10:2025 kategorilerine karşı gerçek istismar denemeleriyle test eder.
39. strix-api-security-testing.zip · usestrix/strix · Strix ajanlarıyla REST/GraphQL/gRPC API'lerini keşfedip gerçek istismarla güvenlik testi yapar.
40. ponytail-ponytail.zip · DietrichGebert/ponytail · YAGNI ile en kısa, en az kodlu çalışan çözümü zorlayan mod.
41. superpowers-using-git-worktrees.zip · obra/superpowers · Özellik işi için git worktree ile yalıtılmış çalışma alanı açar.
42. context7-find-docs.zip · upstash/context7 · Herhangi bir kütüphane, SDK, CLI ya da bulut servisi için güncel doküman ve kod örneği getirir.
43. skills-academy-guide.zip · anthropics/skills · Claude ürün kullanımı sorularında Claude Academy'den uygun kurs ve örnekleri önerir.
44. skills-slack-gif-creator.zip · anthropics/skills · Slack kısıtlarına uygun animasyonlu GIF üretir ve doğrular. · claude.ai Directory'den açılır, yüklenmez (dist/_yerlesik/)
45. agent-skills-idea-refine.zip · addyosmani/agent-skills · Ham fikri ıraksak ve yakınsak düşünmeyle net, uygulanabilir konsepte dönüştürür.
46. superpowers-writing-plans.zip · obra/superpowers · Çok adımlı iş için koda dokunmadan önce uygulama planı yazar.
47. superpowers-superpowers-tdd.zip · obra/superpowers · Uygulama kodundan önce test yazdırarak geliştirme yürütür. · 6c: ad superpowers-tdd (addyosmani TDD ile ad çakışması) → yeni yükleme
48. agent-skills-incremental-implementation.zip · addyosmani/agent-skills · Çok dosyalı değişiklikleri ince, doğrulanabilir dilimler halinde teslim eder. · 6c: referans onarıldı → Replace
49. agent-skills-documentation-and-adrs.zip · addyosmani/agent-skills · Mimari kararları ADR olarak, API/özellik değişikliklerini belge olarak kaydeder.
50. omniroute-omni-settings.zip · CullinanCloud/omniroute · Sistem prompt'u, düşünme bütçesi, IP filtresi ve giriş zorunluluğu gibi genel ayarları okur ve günceller.
51. agent-skills-using-agent-skills.zip · addyosmani/agent-skills · İşe hangi agent-skills becerisinin ya da iş akışının uyduğunu seçip çağırır. · 6c: referans onarıldı → Replace
52. agent-skills-debugging-and-error-recovery.zip · addyosmani/agent-skills · Kırılan test/build ve beklenmeyen hatalarda sistematik kök neden hata ayıklaması yürütür.
53. omniroute-omni-version-manager.zip · CullinanCloud/omniroute · Gömülü servisleri (9Router, CLIProxyAPI) kurar, başlatır, günceller ve loglarını izler.
54. agent-skills-spec-driven-development.zip · addyosmani/agent-skills · Yeni proje ya da büyük değişiklikte koddan önce spec yazdırır.
55. agent-skills-deprecation-and-migration.zip · addyosmani/agent-skills · Eski sistem/API kaldırmayı ve kullanıcıları yeni uygulamaya taşımayı yönetir.
56. agent-skills-observability-and-instrumentation.zip · addyosmani/agent-skills · Log, metrik, trace ve alarm ekleyerek üretim davranışını görünür kılar. · 6c: referans onarıldı → Replace
57. agent-skills-interview-me.zip · addyosmani/agent-skills · Tek tek soru sorarak kullanıcının gerçek niyetini yüksek güvene kadar çıkarır.
58. taste-skill-design-taste-frontend-v1.zip · Leonxlnx/taste-skill · Orijinal v1 taste kuralları: jenerik AI görünümü yasakları ve tasarım kadranlarıyla frontend yazar. · kazanan taraf (taste referansının kendisi)
59. claude-design-skills-ux-research.zip · Gustavosilveira23/claude-design-skills · Araştırma planı, kullanıcı görüşmesi ve bulgu sentezinden kanıta dayalı ürün kararı ve spec çıkarır.

## G2 · çakışması olmayan, A-kovasında olmayan skill'ler (26)

60. omniroute-omni-db-backups.zip · CullinanCloud/omniroute · Sistem yedeği alır, geri yükler ve SQLite veritabanı yaşam döngüsünü yönetir. · UI dışı ama omniroute-cli-backup-sync.zip ile aynı yetenek
61. omniroute-omni-tunnels.zip · CullinanCloud/omniroute · OmniRoute'u dışarı açmak için ngrok/Cloudflare tünelleri kurar ve yönetir. · UI dışı ama omniroute-cli-tunnel.zip ile aynı yetenek
62. ui-skills-ui-skills-root.zip · ibelick/ui-skills · UI işinden önce ui-skills CLI ile gereken en küçük UI Skills bağlamını seçer.
63. omniroute-omni-models.zip · CullinanCloud/omniroute · Yapılandırılmış tüm sağlayıcılardaki modelleri ve takma adları sorgular. · UI dışı ama omniroute-cli-models.zip ile aynı yetenek
64. omniroute-omni-context-rtk.zip · CullinanCloud/omniroute · RTK filtrelerini, bağlam mühendisliği kurallarını ve bağlam aktarımını yapılandırıp test eder. · UI dışı ama omniroute-cli-compression.zip ile aynı yetenek
65. omniroute-omni-sync-cloud.zip · CullinanCloud/omniroute · OmniRoute yapılandırmasını ve bağlantılarını bulut depoya eşitler. · UI dışı ama omniroute-cli-backup-sync.zip ile aynı yetenek
66. omniroute-omni-usage-logs.zip · CullinanCloud/omniroute · Çağrı loglarını ve kullanım analitiğini filtreler, dışa aktarır, token kullanımını toplar. · UI dışı ama omniroute-cli-cost-usage.zip ile aynı yetenek
67. context7-context7-mcp.zip · upstash/context7 · Kütüphane/framework/API sorularında Context7 MCP araçlarıyla güncel doküman getirir. · UI dışı ama context7-find-docs.zip ile aynı yetenek
68. context7-context7-cli.zip · upstash/context7 · ctx7 CLI ile kütüphane dokümanı çeker, skill yönetir, Context7 MCP'yi yapılandırır. · UI dışı ama context7-find-docs.zip ile aynı yetenek
69. skills-web-artifacts-builder.zip · anthropics/skills · React, Tailwind ve shadcn/ui ile çok bileşenli claude.ai HTML artifact'ları kurar. · claude.ai Directory'den açılır, yüklenmez (dist/_yerlesik/)
70. magic-mcp-21st-ui.zip · 21st-dev/magic-mcp · 21st.dev'den UI bileşeni, ilham ve SVG marka logosu bulur, kurar ya da üretir. · A-kovası (CC'de kurulu, çakışma karşılaştırmasına girmedi); G1/G3 ölçütüne uymadığı için G2
71. ui-skills-fixing-metadata.zip · ibelick/ui-skills · Başlık, meta açıklama, canonical, OG/Twitter kartı, favicon, JSON-LD ve robots etiketlerini denetleyip düzeltir.
72. ui-skills-fixing-accessibility.zip · ibelick/ui-skills · HTML erişilebilirlik sorunlarını (ARIA, klavye, odak, kontrast, form hataları) denetleyip düzeltir.
73. ui-skills-fixing-motion-performance.zip · ibelick/ui-skills · Layout thrashing, compositor, scroll bağlı hareket ve blur kaynaklı animasyon performans sorunlarını düzeltir.
74. ui-skills-improve-ui.zip · ibelick/ui-skills · Arayüzü kendi tasarım kanıtına göre salt okuma denetler, doğrulanmış sorunlar için uygulama planı yazar.
75. design-mastery-claude-code-design-masters.zip · HermeticOrmus/design-mastery-claude-code · Saul Bass, Vignelli, Rams, Scher gibi ustaların ilkelerini tasarım kararlarına taşır. · 6c: referans onarıldı → Replace
76. agent-skills-planning-and-task-breakdown.zip · addyosmani/agent-skills · Spec ya da net gereksinimi sıralı, uygulanabilir görevlere böler. · UI dışı ama superpowers-writing-plans.zip ile aynı yetenek · 6c: referans onarıldı → Replace
77. agent-skills-frontend-ui-engineering.zip · addyosmani/agent-skills · Üretim kalitesinde, erişilebilir ve duyarlı kullanıcı arayüzü ve bileşen geliştirir. · 6c: referans onarıldı → Replace
78. claude-design-skills-figma-craft.zip · Gustavosilveira23/claude-design-skills · Figma MCP ile Figma dosyasında ekran/frame çizerken yerleşim zanaatını uygular.
79. taste-skill-stitch-design-taste.zip · Leonxlnx/taste-skill · Google Stitch için jenerik olmayan UI standartları koyan DESIGN.md dosyaları üretir.
80. skills-canvas-design.zip · anthropics/skills · Tasarım felsefesiyle poster ve sanat gibi statik görselleri .png/.pdf olarak üretir. · claude.ai Directory'den açılır, yüklenmez (dist/_yerlesik/)
81. agent-skills-test-driven-development.zip · addyosmani/agent-skills · Kırmızı-yeşil-refactor döngüsüyle testle ilerleyen geliştirme yürütür. · UI dışı ama superpowers-superpowers-tdd.zip ile aynı yetenek · 6c: referans onarıldı → Replace
82. agent-skills-code-review-and-quality.zip · addyosmani/agent-skills · Değişikliği birleştirmeden önce çok eksenli kod incelemesi yapar. · UI dışı ama superpowers-requesting-code-review.zip ile aynı yetenek · 6c: referans onarıldı → Replace
83. agent-skills-performance-optimization.zip · addyosmani/agent-skills · Frontend, backend ve sorgu performansını ölçüp iyileştirir (Core Web Vitals dahil). · 6c: referans onarıldı → Replace
84. claude-design-skills-design-system.zip · Gustavosilveira23/claude-design-skills · shadcn/ui + Tailwind 4 + Next.js ile tasarım sistemi kurar, denetler ve belgeler. · 6c: referans onarıldı → Replace
85. taste-skill-image-to-code.zip · Leonxlnx/taste-skill · Önce tasarım görseli üretip analiz eder, sonra siteyi o görsele uyacak şekilde kodlar.

## G3 · en son — çakışmada kaybeden; yüklenir ama tarifte çağrılmaz (14)

86. skills-brand-guidelines.zip · anthropics/skills · Anthropic'in resmi marka renklerini ve tipografisini çıktılara uygular. · sebep: 2 kuralda kaybeden (kazanan frontend-craft) — frontend-craft'ın Poppins/Arial font yasağıyla çelişir; taste/frontend-craft'ın tek vurgu rengi kuralıyla çelişir; tarifte çağrılmaz · claude.ai Directory'den açılır, yüklenmez (dist/_yerlesik/)
87. ui-skills-baseline-ui.zip · ibelick/ui-skills · UI kodunda boşluk, hiyerarşi, tipografi ve küçük yerleşim sorunlarını hızlıca temizler. · sebep: 5 kuralda kaybeden (kazanan frontend-craft, taste) — taste'nin varsayılan sürekli animasyon zorunluluğuyla çelişir; frontend-craft/taste'nin zorunlu özel easing eğrisiyle çelişir; frontend-craft/taste'nin zorunlu letter-spacing kuralıyla çelişir; frontend-craft'ın düz shadow-md yasağıyla çelişir; frontend-craft'ın Tailwind varsayılan renk yasağıyla çelişir; tarifte çağrılmaz
88. taste-skill-gpt-taste.zip · Leonxlnx/taste-skill · GSAP hareketi, AIDA sayfa yapısı ve rastgele yerleşim varyansıyla landing tasarımı dayatır. · sebep: 1 kuralda kaybeden (kazanan taste) — gpt-taste ortalı hero'yu tercih ediyor; taste DESIGN_VARIANCE>4'te yasaklıyor.; tarifte çağrılmaz
89. taste-skill-minimalist-ui.zip · Leonxlnx/taste-skill · Sıcak monokrom palet, tipografik kontrast ve düz bento ızgaralı editoryal arayüzler kurar. · sebep: 1 kuralda kaybeden (kazanan frontend-craft) — Minimalist-skill Lucide'ı yasaklıyor; frontend-craft Lucide istiyor.; tarifte çağrılmaz
90. taste-skill-industrial-brutalist-ui.zip · Leonxlnx/taste-skill · İsviçre tipografisiyle askeri terminal estetiğini birleştiren brütalist arayüzler kurar. · sebep: 1 kuralda kaybeden (kazanan frontend-craft) — Brutalist-skill Inter öneriyor; FC ve taste Inter'i yasaklıyor.; tarifte çağrılmaz
91. design-mastery-claude-code-brand-systems.zip · HermeticOrmus/design-mastery-claude-code · Stratejiden uygulamaya logo, palet, font eşleşmesi ve ses rehberiyle marka kimlik sistemi kurar. · sebep: 2 kuralda kaybeden (kazanan frontend-craft) — Brand-systems Inter'i öneriyor; FC ve taste Inter'i yasaklıyor.; Brand-systems Space Grotesk öneriyor; FC Space Grotesk'i yasaklıyor.; tarifte çağrılmaz · 6c: referans onarıldı → Replace
92. taste-skill-high-end-visual-design.zip · Leonxlnx/taste-skill · Pahalı hissettiren font, boşluk, gölge, kart ve animasyon kararlarını ajans düzeyinde tanımlar. · sebep: 2 kuralda kaybeden (kazanan frontend-craft) — Soft-skill Lucide'ı yasaklıyor; frontend-craft Lucide outline zorunlu kılıyor.; Soft-skill büyük radius zorunlu tutuyor; FC aşırı yuvarlatmayı yasaklıyor.; tarifte çağrılmaz
93. design-mastery-claude-code-design-movements.zip · HermeticOrmus/design-mastery-claude-code · Bauhaus, İsviçre Stili, Art Deco, Memphis gibi akımların dilini ve etkisini anlatır. · sebep: 2 kuralda kaybeden (kazanan frontend-craft, taste) — Design-movements İsviçre stilinde Inter öneriyor; FC/taste yasaklıyor.; Design-movements çok renkli palet öneriyor; taste tek aksan istiyor.; tarifte çağrılmaz · 6c: referans onarıldı → Replace
94. taste-skill-redesign-existing-projects.zip · Leonxlnx/taste-skill · Mevcut siteyi denetleyip jenerik AI kalıplarını ayıklar, işlevi bozmadan üst seviyeye taşır. · sebep: 1 kuralda kaybeden (kazanan frontend-craft) — Redesign-skill Lucide/Feather'ı sorun sayıyor; FC Lucide'ı zorunlu tutuyor.; tarifte çağrılmaz
95. ui-skills-create-design-md.zip · ibelick/ui-skills · Mevcut repo ya da siteden tasarım dilini çıkarıp DESIGN.md yazar veya günceller. · sebep: 1 kuralda kaybeden (kazanan frontend-craft) — frontend-craft'ın zorunlu 6 başlıklı DESIGN.md şemasıyla çelişir; tarifte çağrılmaz
96. taste-skill-brandkit.zip · Leonxlnx/taste-skill · Marka rehberi panoları, logo sistemleri ve kimlik sunumları için üst düzey görsel üretir. · sebep: 1 kuralda kaybeden (kazanan taste) — Brandkit lila/mor palet öneriyor; taste "AI mor" estetiğini yasaklıyor.; tarifte çağrılmaz
97. skills-algorithmic-art.zip · anthropics/skills · p5.js ile tohumlu rastgelelik ve etkileşimli parametrelerle üretken sanat oluşturur. · sebep: 1 kuralda kaybeden (kazanan frontend-craft) — frontend-craft'ın Poppins font yasağıyla çelişir; tarifte çağrılmaz · claude.ai Directory'den açılır, yüklenmez (dist/_yerlesik/)
98. claude-design-skills-ui-designer.zip · Gustavosilveira23/claude-design-skills · Arayüz görsel tasarımı, UI sistemleri ve piksel hassas uygulama/inceleme yapar. · sebep: 2 kuralda kaybeden (kazanan frontend-craft, taste) — taste'nin tek vurgu rengi sınırıyla çelişir; frontend-craft'ın sabit bezier easing kuralıyla çelişir; tarifte çağrılmaz
99. taste-skill-imagegen-frontend-mobile.zip · Leonxlnx/taste-skill · iOS/Android için uygulama-yerli mobil ekran konsepti ve akış görselleri üretir. · sebep: 1 kuralda kaybeden (kazanan frontend-craft) — Mobil skill Lucide'dan kaçının diyor; FC Lucide outline zorunlu kılıyor.; tarifte çağrılmaz

## claude.ai yükleme notu

- Her zip tek tek: Settings → Capabilities → Skills → Upload. Menü farklı görünüyorsa docs/claude-ai-yukleme.md'deki yol geçerli (Customize → Skills → Add). Önkoşul: "Code execution and file creation" açık.
- Sıra yukarıdaki numaralardır; G3 en son yüklenir ve tariflerde çağrılmaz.
- Yüklenen her 10 zip'te bir (10, 20, … 90 ve 99. satırdan sonra) "skill kontrol": Skills listesinde son 10 skill'in adıyla göründüğünü ve açık olduğunu doğrula; yeni bir sohbette birini açıklamasındaki bir istekle tetikleyip yüklendiğini gör. Eksik ya da hata veren zip'in numarasını not et, o 10'luk tamamlanmadan sonraki gruba geçme.
- Açıklamalar yalnız zip kopyasında ≤200 karaktere kısaltıldı (62 zip); kaynak repolar değişmedi.
