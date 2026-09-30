# Master 95% of Claude Code Skills in 28 Minutes
## Künye
Master 95% of Claude Code Skills in 28 Minutes · Nate Herk | AI Automation · süre: 27:18 · en-orig · https://youtu.be/zKBPwDpBfhs
motor: parti 2026-09-30-uzun-5 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
## Özet
Nate Herk, Claude Code skill'lerini anlatıyor: skill yeniden kullanılabilir talimat klasörüdür (SKILL.md + referanslar/scriptler). Canlı demoda dört ajan paralel çalışıyor (morning coffee, pulse check, Excalidraw diyagramı, YouTube yorum analizi). Skill anatomisi (YAML front matter, workflow), referans dosyaları, progressive context loading (3 seviye), geri bildirim döngüsü, altı adımlı skill yapım çerçevesi, skill-builder ile sıfırdan infografik skill'i kurulumu, hata ayıklama tablosu ve global skill'ler anlatılıyor.
## Bölümler
- 0:00 Giriş ve canlı demo
- 2:41 Skill nedir?
- 3:35 Neden önemli
- 5:24 Skill anatomisi
- 6:45 Referans dosyaları
- 11:00 Claude skill'i ne zaman kullanacağını nasıl bilir
- 13:17 Geri bildirim döngüsü ve ne zaman skill yapılır
- 17:13 Altı adımlı skill yapım çerçevesi
- 18:10 Canlı skill yapımı
- 22:54 Skill'i test etme ve iyileştirme
- 23:55 Test, hata ayıklama ve yaygın çözümler
- 26:57 Kapanış / topluluk
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| morning-coffee skill | yok | skill | yok | Takvim ve ClickUp görevlerine bakıp günün planını çıkaran kişisel asistan skill'i. | 0:30 | Morning Coffee briefing; 'Pretend it is morning' sekmesi, takvim ve acil işler listesi. (karede: VS Code'da 'Morning Coffee - February 26, 2026 (Thursday)' brifingi, Today's Calendar ve Urgent / Action Items başlıkları.) |
| pulse check skill | yok | skill | yok | Projeleri ve taahhütleri ClickUp'tan canlı kontrol eder; sabit liste ID'leri ve ClickUp searcher alt ajanı kullanır. | 14:18 | Pulse check skill, ClickUp list ID'lerini hardcode etti ve alt ajana devretti. |
| excalidraw-diagram skill | yok | skill | yok | Düzenlenebilir Excalidraw diyagramı (native JSON) üretir; kelimeler hep doğru çıkar. | 6:35 | SKILL.md: name excalidraw-diagram, Workflow, Step 1 Understand the concept. (karede: SKILL.md front matter'ında name: excalidraw-diagram ve description; altında '## Workflow' ve '### Step 1: Understand the concept'.) |
| excalidraw-visuals skill | yok | skill | yok | AI ile görsel üretir ama yazımlar bozuk çıkabilir; diyagram skill'i ile tamamlanır. | 2:41 | Excalibraw visuals skill; AI görsellerinde kelimeler yanlış yazılabiliyor. |
| idea-mining skill | yok | skill | yok | İçerik/video fikirleri üretir; kanal verisi, rakip listesi ve analiz scriptini proje dizininden referanslar (seçenek B). | 7:46 | Idea mining skill; YouTube channel.md, JSON, rakip listesi ve analiz scripti referans. |
| skill-builder skill | yok | skill | yok | Sorular sorarak yeni skill oluşturan, optimize eden ve denetleyen skill; SKILL.md + reference.md içerir. Ücretsiz Skool topluluğunda. | 8:48 | Skill builder'ı yükle, sana gereken her şeyi kurmana yardım eder. |
| infographic-builder skill | yok | skill | yok | Nano Banana (Key AI API) ile markalı 1:1 PNG infografik üretir, şeffaf logoyu üstüne bindirir. | 22:54 | Logo üstte, marka rehberi ve API referansı markdown dosyasında. |
| Progressive context loading | yok | teknik | yok | Üç seviye: YAML ad/açıklama (~100 token), tam SKILL.md (1000-birkaç bin token), gerekirse ek dosyalar. | 12:01 | Level one sadece name ve description; level three ek dosyalar yalnız gerekirse. |
| Geri bildirim döngüsü | yok | iş akışı | yok | Skill'i çalıştır, ajanı izle, geri bildirim ver, skill'i güncelle; tekrarla. | 13:17 | Invoke, watch the agent work, give feedback, then it fixes the skill. |
| Global skill'ler (~/.claude) | yok | ipucu | yok | Ev dizininde oluşturulan skill'ler her projede kullanılır; örn. global front-end design skill'i. | 25:57 | Global skill'ler home dizininde, tilda ile gösterilir; her projede erişilir. |
| Front matter seçenekleri | yok | ipucu | yok | disable-model-invocation, allowed tools, argument hint, model, context, hooks, agent alanları. | 24:55 | Disable model invocation, allowed tools, argument hint, model, context, hooks, agent. |
| Morning coffee skill'ini tetiklemek. | yok | prompt | yok | Pretend it is morning and I want you to run... | 0:30 | kaynak: kare |
| Yeni infografik skill'ini minimal bağlamla test etmek. | yok | prompt | yok | test it out with an infographic about cloud skills | 21:12 | kaynak: altyazı |
| Skill'i geri bildirimle güncellettirmek. | yok | prompt | yok | Logo şeffaf olmalı, üstüne bindirilsin; infografikler her zaman 1:1 olsun. | 22:14 | kaynak: altyazı |
## Açıklama bağlantıları
- https://get.glaido.com/nate — Glaido (sponsor/affiliate) bağlantısı · aday: hayır · Sponsor bağlantısı; videoda anlatılan bir araç değil.
- https://podcast.nateherk.com/apply — Podcast başvuru sayfası · aday: hayır · Tanıtım; skill içeriğiyle ilgisiz.
- https://www.hostinger.com/vps/claude-code-hosting — Hostinger VPS Claude Code hosting · aday: hayır · Sponsor/reklam bağlantısı; videoda işlenmiyor.
- https://www.instagram.com/nateherk/ — Instagram profili · aday: hayır · Sosyal medya profili.
- https://www.linkedin.com/in/nateherkelman/ — LinkedIn profili · aday: hayır · Sosyal medya profili.
- https://www.skool.com/ai-automation-society-plus/about?el=master-95-of-claude-code-skills-in-28-minutes&hcategory=youtube-videos&utm_campaign=ais-plus — Ücretli Skool topluluğu · aday: hayır · Ücretli topluluk; içeriğe erişilemiyor. · erişilemez: ücretli topluluk
- https://www.skool.com/ai-automation-society/about?el=master-95-of-claude-code-skills-in-28-minutes&hcategory=youtube-videos&utm_campaign=free-group — Ücretsiz Skool topluluğu (Agent Skills classroom: skill-builder) · aday: evet (skill-builder skill) · Skill-builder skill'i burada dağıtılıyor; ancak giriş gerektiriyor olabilir. · erişilemez: Skool girişi gerekli; içerik doğrulanamadı
- https://x.com/nateherk — X profili · aday: hayır · Sosyal medya profili.
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /skill-adı (örn. /school-post) | Skill'i slash komutuyla doğrudan tetikler. | 11:00 | altyazı |
| .claude/skills/skill-builder/ (SKILL.md + reference.md kopyala) | Skill-builder'ı projeye kurar. | 19:10 | altyazı |
| VS Code > Extensions > 'Claude Code' yükle | Claude Code eklentisini kurar; ücretli Anthropic hesabıyla giriş yapılır. | 18:10 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Skill önce yalnız name/description okunur (~100 token), tam SKILL.md 1000-birkaç bin token. | 12:01 | sayısal |
| SKILL.md 500 satırın altında tutulmalı; ayrıntılar ayrı dosyalara taşınmalı (docs önerisi). | 13:02 | öneri |
| Markdown işlemek API çağrısı/HTTP isteğinden daha hızlı ve ucuzdur. | 16:20 | karşılaştırma |
| Skill'ler Cursor, Antigravity, Codex gibi farklı ürünlerde çalışabilir. | 10:50 | özellik |
| Skill 10-30 kez çalıştırıldıkça iyileşir; ilk seferde mükemmel olmaz. | 13:17 | öneri |
| Skill'ler SOP gibidir; script çalıştırır, API çağırır, alt ajan kullanır (Not just text. Full automation). | 4:59 | özellik |
| Skill tetiklenmiyorsa YAML'ı daha spesifik yap; çok tetikleniyorsa disable model invocation kullan. | 24:55 | öneri |
## Kareden okunanlar
- 1:30: VS Code, Herk-2; 'Morning Coffee - February 26, 2026 (Thursday)' brifingi, takvim ve acil işler.
- 2:21: Yorum analizi: 'Cover cost and context limits upfront', 'Stop demoing toy examples for tool videos'.
- 3:08: 'Skills = Reusable instructions': Write Once, Save as Skill (.claude/skills/), Trigger Anytime, Same Result.
- 4:05: 'Why should you care?': Personal Productivity, Team Leverage, Monetization.
- 6:35: SKILL.md: name excalidraw-diagram, description, Workflow, Step 1 Understand the concept.
## Belirsizlikler
- Kare listesinde yalnız 8 kare var; 1. kare (0:30) 'Quick Demo' başlık kartı olabilir, sıra tam doğrulanamadı.
- Skool linkindeki skill-builder erişimi doğrulanamadı; repo URL'si yok.
- 'Key AI' adı altyazıda bozuk; muhtemelen kie.ai, doğrulanmadı.
- Kurulum komutları terminal komutu değil, arayüz/dosya adımlarıdır.
## Atlanan segment oranı
0/32 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
