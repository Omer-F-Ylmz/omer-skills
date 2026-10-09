# A CRM where the AI agent does the research and data entry for you. Free, self-ho
## Künye
A CRM where the AI agent does the research and data entry for you. Free, self-ho · gittrend.io · süre: 0:28 · ? · https://www.instagram.com/reel/DbxCyfHAddF/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-23 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 15741 tk · claude-haiku-5-5: claude-haiku-5-5 · 49484 tk
## Özet
Kısa bir tanıtım videosu: trycompai/crm adlı açık kaynaklı, ajan öncelikli (agentic-first) bir CRM'in GitHub README'si gösteriliyor. Araştırma ajanı e-postaları ve toplantıları okuyup kişileri tanıyor, şirket verisini zenginleştiriyor ve takip planlıyor. Kendi zamanlamasıyla çalışıyor; tarayıcı kapansa da sürüyor. Kendi sunucunda barındırılan, Salesforce'a alternatif, MIT lisanslı bir proje. Ajan eve üzerinde, Bun/Postgres/Turborepo ile Vercel'de çalışıyor.
## Bölümler
- 0:00 Açık kaynak CRM tanıtımı (README)
- 0:14 Ajan mimarisi: eve, skill'ler, zamanlama, sandbox
- 0:19 İsteğe bağlı API anahtarları ve başlangıç listesi
- 0:24 Ajan sekmesi ve teknoloji yığını
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| trycompai/crm | yok | plugin | https://github.com/trycompai/crm | Araştırma ajanının notlarını tuttuğu açık kaynaklı, MIT lisanslı, kendi sunucuda barındırılan CRM | 0:00 | Sayfa başlığı GitHub - trycompai/crm; 'An open-source, agentic-first CRM' (karede: kanıttan) Sayfa başlığı GitHub - trycompai/crm; 'An open-source, agentic-first CRM' |
| eve | yok | teknik | yok | Vercel'in dosya sistemi öncelikli dayanıklı ajan çatısı; ajan bunun üzerinde çalışıyor | 0:14 | apps/agent is its own deployment, built on eve — Vercel's filesystem-first framework |
| Vercel AI Gateway | yok | teknik | yok | Model erişimi için sağlayıcı SDK'sı gerektirmeyen ağ geçidi | 0:27 | Model satırında Vercel AI Gateway — no provider SDK, OIDC on Vercel (karede: kanıttan) Model satırında Vercel AI Gateway — no provider SDK, OIDC on Vercel |
| Vercel | yok | teknik | yok | Dağıtım platformu | 0:26 | A Turborepo monorepo on Bun, deployed on Vercel. |
| Bun | yok | CLI | yok | Çalışma zamanı (runtime) | 0:00 | Rozet: runtime Bun (karede: kanıttan) Rozet: runtime Bun |
| Postgres | yok | teknik | yok | Veritabanı | 0:00 | Rozet: database Postgres (karede: kanıttan) Rozet: database Postgres |
| Turborepo | yok | teknik | yok | Monorepo yapısı | 0:26 | The stack: A Turborepo monorepo on Bun (karede: kanıttan) The stack: A Turborepo monorepo on Bun |
| NestJS | yok | teknik | yok | Olayları bildiren ve zekâ içermeyen API katmanı | 0:00 | The API deliberately has no intelligence... NestJS reports that something happened (karede: kanıttan) The API deliberately has no intelligence... NestJS reports that something happened |
| Google | yok | teknik | yok | Oturum açma ve posta/toplantı senkronu için Google hesabı | 0:11 | Sign-in is Google, the allow-list is one |
| RAPIDAPI_KEY (LinkedIn) | yok | teknik | yok | İsteğe bağlı LinkedIn araştırma kaynağı | 0:21 | [agent] on LinkedIn (RAPIDAPI_KEY) · kanıt: kare (karede: [agent] on LinkedIn (RAPIDAPI_KEY)) |
| Perplexity | yok | teknik | yok | İsteğe bağlı web araştırması (PERPLEXITY_API_KEY) | 0:27 | [agent] off Web research (PERPLEXITY_API_KEY) (karede: kanıttan) [agent] off Web research (PERPLEXITY_API_KEY) |
| Context.dev | yok | teknik | yok | İsteğe bağlı şirket marka verisi (CONTEXT_DEV_API_KEY) | 0:21 | Company brand data (CONTEXT_DEV_API_KEY) (karede: kanıttan) Company brand data (CONTEXT_DEV_API_KEY) |
| GitHub | yok | teknik | yok | Reponun ve README'nin gösterildiği platform | 0:00 | Sekme başlığı GitHub - trycompai/crm (karede: kanıttan) Sekme başlığı GitHub - trycompai/crm |
| FOR UPDATE SKIP LOCKED | yok | teknik | yok | İş kuyruğunda iki dağıtıcının ayrı iş almasını sağlayan kilit tekniği | 0:18 | claimDue leases rows with FOR UPDATE SKIP LOCKED · kanıt: kare (karede: claimDue leases rows with FOR UPDATE SKIP LOCKED) |
| AGENT_BRIDGE_SECRET | yok | teknik | yok | Ajan sekmesini açan imzalı belirteç köprüsü ayarı | 0:25 | Set AGENT_BRIDGE_SECRET to the same value in both processes (karede: kanıttan) Set AGENT_BRIDGE_SECRET to the same value in both processes |
| Company brand data | yok | teknik | yok | Şirket logosu ve marka verisi kaynağı; CONTEXT_DEV_API_KEY ile açılır. | 0:21 | Kare 3: '[agent] off Company brand data (CONTEXT_DEV_API_KEY)' (karede: kanıttan) Kare 3: '[agent] off Company brand data (CONTEXT_DEV_API_KEY)' |
| read_crm_history | yok | teknik | yok | Kullanıcının kendi yazışmalarını, toplantılarını ve imza bloklarını okuyan ajan aracı. | 0:18 | Kare 2 araç tablosu: 'read_crm_history, search_crm, identify_contact...' (karede: kanıttan) Kare 2 araç tablosu: 'read_crm_history, search_crm, identify_contact...' |
| search_crm | yok | teknik | yok | CRM kayıtlarında arama yapan ajan aracı. | 0:18 | Kare 2 araç tablosu: 'search_crm' · kanıt: kare (karede: Kare 2 araç tablosu: 'search_crm') |
| identify_contact | yok | teknik | yok | Bir kişiyi CRM'deki kayıtlarla eşleştiren ajan aracı. | 0:18 | Kare 2 araç tablosu: 'identify_contact' · kanıt: kare (karede: Kare 2 araç tablosu: 'identify_contact') |
| research_person | yok | teknik | yok | Bir kişi hakkında araştırma yapan ajan aracı. | 0:18 | Kare 2 araç tablosu: 'research_person' · kanıt: kare (karede: Kare 2 araç tablosu: 'research_person') |
| enrich_company | yok | teknik | yok | Şirket verisini dış kaynaklarla zenginleştiren ajan aracı. | 0:18 | Kare 2 araç tablosu: 'enrich_company' · kanıt: kare (karede: Kare 2 araç tablosu: 'enrich_company') |
| record_fact | yok | teknik | yok | Kanıtlanmış bir bilgiyi kayda yazan ajan aracı. | 0:18 | Kare 2 araç tablosu: 'record_fact' · kanıt: kare (karede: Kare 2 araç tablosu: 'record_fact') |
| schedule_recheck | yok | teknik | yok | Bir kişi için yeniden kontrol zamanını planlayan ajan aracı. | 0:18 | Kare 2 araç tablosu: 'schedule_recheck' · kanıt: kare (karede: Kare 2 araç tablosu: 'schedule_recheck') |
| web_search | yok | teknik | yok | Model sağlayıcısı tarafında çalışan web arama aracı. | 0:22 | Kare 3: 'web_search at the model provider' (karede: kanıttan) Kare 3: 'web_search at the model provider' |
| web_fetch | yok | teknik | yok | Uygulama çalışma zamanında sayfa çeken ajan aracı; ağ erişimi gerektirir. | 0:22 | Kare 3: 'web_fetch runs in the app runtime' · kanıt: kare (karede: Kare 3: 'web_fetch runs in the app runtime') |
| bash | yok | CLI | yok | Sandbox içinde çalışan kabuk komutu aracı; ağ ve veritabanı erişimi yok. | 0:18 | Kare 2: 'bash, grep, glob and a /workspace, with deny-all egress' (karede: kanıttan) Kare 2: 'bash, grep, glob and a /workspace, with deny-all egress' |
| grep | yok | CLI | yok | Sandbox içinde metin arama aracı. | 0:18 | Kare 2: 'bash, grep, glob and a /workspace' (karede: kanıttan) Kare 2: 'bash, grep, glob and a /workspace' |
| glob | yok | CLI | yok | Sandbox içinde dosya desenine göre listeleme aracı. | 0:18 | Kare 2: 'bash, grep, glob and a /workspace' (karede: kanıttan) Kare 2: 'bash, grep, glob and a /workspace' |
| claimDue | yok | teknik | yok | Vadesi gelmiş görevleri kiralayan iş kuyruğu fonksiyonu. | 0:18 | Kare 2: 'claimDue leases rows with FOR UPDATE SKIP LOCKED' (karede: kanıttan) Kare 2: 'claimDue leases rows with FOR UPDATE SKIP LOCKED' |
| evidence.md | yok | skill | yok | Ajanın kanıt değerlendirmesini tarif eden markdown skill dosyası. | 0:16 | Kare 2: '4 skills — evidence.md, identity-matching.md, data-boundaries.md' (karede: kanıttan) Kare 2: '4 skills — evidence.md, identity-matching.md, data-boundaries.md' |
| identity-matching.md | yok | skill | yok | Kişi kimliği eşleştirme kurallarını anlatan skill dosyası. | 0:16 | Kare 2: 'identity-matching.md' (karede: kanıttan) Kare 2: 'identity-matching.md' |
| data-boundaries.md | yok | skill | yok | Veri sınırlarını anlatan skill dosyası. | 0:16 | Kare 2: 'data-boundaries.md' (karede: kanıttan) Kare 2: 'data-boundaries.md' |
| writing-a-brief.md | yok | skill | yok | Ajanın okuduğu, sürümlendirilen brief yazım rehberi. | 0:19 | OCR 0:19: 'writing-a-brief.md — prose the agent reads, versioned like code' (karede: kanıttan) OCR 0:19: 'writing-a-brief.md — prose the agent reads, versioned like code' |
## Açıklama bağlantıları
- gittrend.io — Açıklamada 'More like this' ile yönlendirilen içerik sitesi. · aday: hayır · Araç değil; ilgili içerik sitesine yönlendirme. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Hoş geldin başlığı ve metrik kartları (dashboard KPI cards) | Welcome back, Ada başlığı altında gelir ve fırsat kartları (karede: Karanlık panelde 'Welcome back, Ada', $756K gibi metrik kartları) | 0:00 | kare |
| Alan grafiği (area chart) | Kapanan ve yeni boru hattı eğrileri (karede: Sarı ve yeşil dalgalı alan grafiği) | 0:00 | kare |
| Halka grafik (donut chart) | Aşamaya göre açık boru hattı, ortada $756K (karede: Turuncu halka grafik, ortasında $756K) | 0:00 | kare |
| Ekran görüntüsü ızgarası (screenshot grid) | Deals, Contacts, Companies, Overview sayfaları 2x2 (karede: Dört koyu temalı uygulama görüntüsü ve alt yazıları) | 0:18 | kare |
| Rozet (badge) | licence MIT, agent eve, runtime Bun, database Postgres (karede: README üstünde dört küçük rozet) | 0:18 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ajan kendi zamanlamasıyla çalışır; tarayıcı kapansa da sürer | 0:06 | özellik |
| API anahtarı olmadan da kendi e-posta ve toplantı geçmişini okuyarak çalışır | 0:20 | özellik |
| Küçük ekipler için Salesforce'a kendi sunucuda barındırılan alternatif | 0:00 | karşılaştırma |
| Sandbox'a DATABASE_URL verilmez; ağ ve veritabanı erişimi yoktur | 0:23 | özellik |
| 18 yazılmış araç ve 4 skill içerir | 0:14 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:00 | trycompai/crm GitHub reposu | trycompai/crm | GitHub - trycompai/crm sekmesi |
| ekran 0:14 | eve çatısı | eve | built on eve — Vercel's filesystem-first framework |
| ekran 0:27 | Vercel AI Gateway | Vercel AI Gateway | Model: Vercel AI Gateway — no provider SDK |
| ekran 0:26 | Vercel dağıtımı | Vercel | deployed on Vercel |
| ekran 0:00 | Bun | Bun | runtime Bun |
| ekran 0:00 | Postgres | Postgres | database Postgres |
| ekran 0:26 | Turborepo | Turborepo | A Turborepo monorepo on Bun |
| ekran 0:00 | NestJS | NestJS | NestJS reports that something happened |
| ekran 0:11 | Google oturum açma | Google | Sign-in is Google |
| ekran 0:21 | LinkedIn / RapidAPI anahtarı | RAPIDAPI_KEY (LinkedIn) | LinkedIn (RAPIDAPI_KEY) |
| ekran 0:27 | Perplexity web araştırması | Perplexity | Web research (PERPLEXITY_API_KEY) |
| ekran 0:21 | Company brand data | Context.dev | Company brand data (CONTEXT_DEV_API_KEY) |
| ekran 0:00 | GitHub | GitHub | Sekme ve README |
| ekran 0:18 | FOR UPDATE SKIP LOCKED | FOR UPDATE SKIP LOCKED | claimDue leases rows with FOR UPDATE SKIP LOCKED |
| ekran 0:25 | AGENT_BRIDGE_SECRET | AGENT_BRIDGE_SECRET | Set AGENT_BRIDGE_SECRET to the same value |
| açıklama | gittrend.io | aday değil: konu dışı | More like this → gittrend.io |
| açıklama | Salesforce | aday değil: konu dışı | Salesforce alternatifi olarak karşılaştırma |
| ekran 0:23 | web_fetch / web_search | aday değil: başka adayın parçası (eve) | web_fetch runs in the app runtime and web_search at the model provider |
| ekran 0:17 | bash, grep, glob sandbox araçları | aday değil: başka adayın parçası (eve) | A sandbox: bash, grep, glob and a /workspace |
| ekran 0:16 | Skill dosyaları (evidence.md vb.) | aday değil: başka adayın parçası (trycompai/crm) | evidence.md, identity-matching.md, data-boundaries.md |
| ekran 0:18 | cron ifadesi | aday değil: genel kavram | belongs in a task's dueAt, not in a cron expression |
| yorum | Yorumlar | aday değil: konu dışı | Yorumlar girişsiz alınamadı |
## Kareden okunanlar
- 0:00: GitHub README: CRM, An open-source, agentic-first CRM; rozetler MIT, eve, Bun, Postgres; altyazı 'AN OPEN-SOURCE CRM'
- 0:18: Deals/Contacts/Companies/Overview görüntüleri; ajan tablosu: 18 araç, 4 skill, 1 zamanlama, sandbox; altyazı 'A FEW COMMANDS'
- 0:27: İsteğe bağlı anahtar listesi, sandbox açıklaması, AGENT_BRIDGE_SECRET, yığın tablosu: eve, Vercel AI Gateway; altyazı 'I'LL SEND'
## Belirsizlikler
- Yorumlar girişsiz alınamadı; repo bağlantısı yorumda verilmiş olabilir.
- Kurulum komutları videoda gösterilmedi; yalnız 'birkaç komut' deniyor.
- Altyazıdaki 'Bolt', 'Astro', 'Inter', 'Express', 'TypeScript', 'Next.js' sözlük eşleşmeleri videoda kullanılmıyor; OCR gürültüsü olabilir (Bolt, 'bolt a chat box' ifadesinden).
- Ajanın kullandığı asıl model adı ekranda görünmüyor; yalnız Vercel AI Gateway geçiyor.
- README'de adı geçen skill dosyaları (evidence.md vb.) ayrı araç olarak ele alınmadı.
- gittrend.io açıklamada 'daha fazlası' için geçen bir yönlendirme sayfası; videoda kullanılmıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/trycompai/crm#readme | 0:00 | ekran | evet |
| gittrend.io | açıklama | açıklama | hayır |
| docs/api.md | 0:00 | ekran | hayır |
| docs/agent.md | 0:26 | ekran | hayır |
## İş akışı
- 1. adım — Kendi sunucuya kurulum: depo klonlanır, Bun ile bağımlılıklar kurulur ve PostgreSQL hazırlanır (videoda komut gösterilmiyor) — araçlar: trycompai/crm, Bun, PostgreSQL
- 2. adım — Google hesabı bağlanır ve posta kutusu eşitlenir — araçlar: Google, read_crm_history
- 3. adım — Ajan kendi zamanlamasıyla çalışır; vadesi gelen görevler kiralanır — araçlar: claimDue, FOR UPDATE SKIP LOCKED, PostgreSQL
- 4. adım — Ajan oturumu başlatır ve e-posta ile toplantıları okur — araçlar: eve, read_crm_history
- 5. adım — Kişi kimliği CRM kayıtlarıyla eşleştirilir — araçlar: search_crm, identify_contact, identity-matching.md
- 6. adım — Kişi ve şirket hakkında dış kaynaklardan araştırma yapılır — araçlar: research_person, enrich_company, LinkedIn, Company brand data, Perplexity, web_search, web_fetch
- 7. adım — Kanıt değerlendirilir ve yalnızca güçlü kanıt kayda yazılır; zayıf kanıt öneriye dönüşür — araçlar: record_fact, evidence.md
- 8. adım — Yeniden kontrol zamanı planlanır (dueAt ile) — araçlar: schedule_recheck
- 9. adım — Sandbox'ta dosya ve metin işlemleri yapılır; ağ ve veritabanı erişimi kapalı — araçlar: bash, grep, glob, /workspace
- 10. adım — Agent sekmesinde adımlar izlenir; belirsiz kişi için kullanıcıya soru sorulur — araçlar: trycompai/crm, AGENT_BRIDGE_SECRET
- 11. adım — Model çağrıları Vercel AI Gateway üzerinden yapılır; uygulama Turborepo monorepo olarak Vercel'e dağıtılır — araçlar: Vercel AI Gateway, Turborepo, Bun, Vercel
## Promptlar
- yok
