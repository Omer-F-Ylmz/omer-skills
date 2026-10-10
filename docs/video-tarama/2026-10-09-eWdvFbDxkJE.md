# Top 5 Claude Code Plugins (2026)
## Künye
Top 5 Claude Code Plugins (2026) · Charlie Automates · süre: 1:15 · en-orig · https://youtu.be/eWdvFbDxkJE · şema 2
motor: parti 2026-10-09-short-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 24173 tk · claude-haiku-5-5: claude-haiku-5-5 · 59559 tk
## Özet
Charlie Automates, 75 saniyelik kısa videoda Claude Code için 5 eklenti/araç tanıtıyor: herdr (arka planda çoklu ajan terminali, ses uyarısı), Graphify (Obsidian ile görselleştirilen ajan belleği), OmniRoute (Claude Code içinde herhangi bir model), Claude Code setup (Anthropic'in proje denetimi) ve Task Observer (mevcut skill'leri iyileten meta-skill). Araçlar GitHub README sayfaları üzerinden gösteriliyor; kurulum komutu gösterilmiyor.
## Bölümler
- 0:00 Giriş: ajan takımı ve $200 limit iddiası
- 0:06 1. herdr: arka plan sunucusu, çoklu terminal, ses uyarısı
- 0:24 2. Graphify: ajanlar için bellek, Obsidian ile görselleştirme
- 0:36 3. OmniRoute: Claude Code ile her model
- 0:46 4. Claude Code setup: hook, skill, MCP ve alt ajan önerileri
- 0:59 5. Task Observer: skill'leri iyileştiren meta-skill
- 1:07 Kapanış: 'Claude' yorumu yap, linkleri al
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| herdr | yok | CLI | https://github.com/herdrdev/herdr | Arka plan sunucusunda birden çok terminalde farklı ajanları çalıştırır; takılınca ya da bitince ses uyarısı verir. | 0:11 | README'de 'herdr is a background server; the terminals live inside it'; herdr.dev ekranda (karede: GitHub README: v.0.4.0.mp4 videosu, 'always running — herdr is a background server' metni, 'ALL RUNNING DIFFERENT MODELS' başlığı) |
| Graphify | yok | skill | yok | Verilen veri setinde anlamsal ilişkiler kuran ajan bellek çözümü; /graphify komutuyla çalışır. | 0:24 | README: 'Type /graphify in your AI coding assistant'; GitHub Trending #3 (karede: Graphify logosu, '#3 Repository Of The Day' rozeti, pypi v0.9.41, '2. GRAPHIFY' başlığı) |
| Obsidian | yok | CLI | yok | Graphify çıktısını görsel olarak izlemek için yanında kullanılıyor. | 0:24 | I stack it with Obsidian so I can visually see it |
| OmniRoute | yok | plugin | yok | Tek uç noktadan 339 sağlayıcı ve 90+ ücretsiz modelle Claude Code'a herhangi bir modeli bağlayan AI ağ geçidi. | 0:36 | README: 'OmniRoute — The Free AI Gateway', 'Never stop coding' (karede: README başlığı 'OmniRoute — The Free AI Gateway', 'Every AI tool → 339 providers — 90+ free', '3. OMNIROUTE') |
| Claude Code setup | yok | plugin | yok | Anthropic'in projeye uygun hook, skill, MCP ve alt ajanları öneren otomasyonu. | 0:46 | It's called Claude Code setup. You should run this on every Claude Code project |
| Task Observer | yok | skill | yok | Mevcut skill'leri izleyip nasıl iyileştirilebileceklerini söyleyen meta-skill. | 0:59 | README: 'task-observer - One Skill to Rule Them All' (karede: README 'task-observer - One Skill to Rule Them All', '5. TASK OBSERVER', 'meta-skill that builds and improves all your skills') |
| Claude Code | yok | CLI | yok | Eklentilerin çalıştığı ana ajan aracı. | 0:12 | Ekranda 'Claude Code v2.1.92' terminal başlığı (karede: herdr içinde terminal: Claude Code v2.1.92, Claude Max, Haiku 4.5) |
| Claude Haiku 4.5 | yok | teknik | yok | herdr demosunda Claude Code'da seçili model. | 0:18 | 'Haiku 4.5 with medium effort' ekranda · kanıt: kare (karede: 'Haiku 4.5 with medium effort' ekranda) |
| GPT-5.4-mini | yok | teknik | yok | herdr demosunda ajanlardan birinin modeli. | 0:15 | 'gpt-5.4-mini medium' ekranda (karede: Alt kısımda 'gpt-5.4-mini medium' satırı) |
| Codex | yok | CLI | yok | herdr çalışma alanı listesinde 'security-codex' oturumu görünüyor. | 0:15 | Kenar çubuğunda 'security-codex' (karede: Sol kenar çubuğunda security-droid, security-codex, perf-claude) |
| OpenRouter | yok | teknik | yok | OmniRoute README'sinde $10 top-up ile kıyaslanan servis. | 0:40 | '$10 OpenRouter top-up' ekranda (karede: Free-tiers panelinde '$10 OpenRouter top-up' satırı) |
| Gemini | yok | teknik | yok | OmniRoute'un desteklediği modeller ve Claude Code setup önizlemesindeki sorgu hedefi. | 0:36 | 'FREE Claude / GPT / Gemini - auto-fallback'; 'Google Gemini about Readonly' (karede: kanıttan) 'FREE Claude / GPT / Gemini - auto-fallback'; 'Google Gemini about Readonly' |
| Sub agents | yok | teknik | yok | Claude Code setup'ın önerdiği bileşenlerden biri. | 0:46 | recommends all the top hooks, skills, MCPs, and sub agents |
| Hermes Agent | yok | teknik | yok | Task Observer README'sinde entegrasyon desteği anılan otonom ajan. | 0:59 | 'Hermes and Openclaw setups' README'de (karede: Task Observer README paragrafı: 'their Hermes and Openc...') |
| Proje değerlendirmesi ister | yok | prompt | yok | Projeyle ilgili görüş istenir: 'wdyt on this project?' | 0:18 | kaynak: kare |
| Kod incelemesi | yok | prompt | yok | Mevcut değişiklikleri /review komutuyla inceletmek için yazılan istek. | 0:15 | kaynak: kare |
| Proje talimat dosyası oluşturma | yok | prompt | yok | Projeye Claude için talimat dosyası (CLAUDE.md) oluşturmak üzere /init çalıştırılır. | 0:21 | kaynak: kare |
| Çok modelli karşılaştırma | yok | prompt | yok | Birden çok modele aynı soru sorulur (örnek: 'gemini 1+2+3+4=?'), yanıtlar karşılaştırılır. | 0:54 | kaynak: kare |
## Açıklama bağlantıları
- https://charlieautomates.com/free-resources/#top-claude-code-plugins-2026 — Beş eklentinin tüm bağlantılarını içeren ücretsiz kaynak sayfası · aday: hayır · Yazarın kaynak/link listesi sayfası; araç değil, referans sayfası · sınıf: diğer
- https://www.skool.com/cc-strategic-ai/classroom/7cb51b97?md=b89457adad5e4ea6ad117250c75844f2 — Yazarın Skool topluluğundaki eklenti belgesi · aday: hayır · Topluluk sayfası, giriş/üyelik gerektirebilir · sınıf: diğer · erişilemez: erişilemez: giriş gerekli / topluluk sayfası
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| wc -l [yol]/src/*.rs [yol]/src/**/*.rs 2>/dev/null / tail -1 | herdr kaynak dosyalarının satır sayısını sayar; Claude Code ajanı çalıştırdı ve izin istedi. Yollar kısaltıldı. (karede: İzin istemi: 'Execute wc -l [yol]' ve 'Yes, and always allow low impact commands' seçenekleri.) | 0:15 | kare |
| /review | Claude Code'da mevcut değişiklikleri inceletir (sohbet komutu). (karede: Sağ paneldeki Claude Code girişinde '/review on my curr…' yazısı.) | 0:15 | kare |
| /init | Claude Code'da proje için CLAUDE.md talimat dosyası oluşturur (sohbet komutu). (karede: (karede OCR) 0 Contributing Apache-2.0 license README v.0.4.0.mp4 LLn-prexy 1 ) claude naster Claude Code v2.1.92 2 herer Ren /init to create a ClAllE.md file nith instruttions for Claude Wuleome back Can! master) | 0:21 | kare |
| /graphify | AI kodlama asistanında Graphify'ı çalıştırır (sohbet komutu). (karede: 'Type /graphify in your AI coding assistant' yazısı.) | 0:24 | kare |
| /quorum | Claude Code Setup örneğinde birden çok modele aynı soruyu sorar (sohbet komutu, OCR ile okundu). (karede: Sneak Preview'da '> /quorum is running…' satırı.) | 0:49 | kare |
| /llm | Örnek çıktıda birden çok modelli sorgu başlatır (sohbet komutu, OCR ile okundu). (karede: (karede OCR) :m README computers. Sneak Preview A simple sneak preview of some of the configured features is: * Welcome to Claude Code! /help for help, /status for your current setup cwd: /Users/rse/Work/speechflo) | 0:54 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Çoğu kişi, bu eklentilerin kaldırdığı limitler için ayda 200 dolar ödüyor. | 0:00 | sayısal |
| herdr arka planda birden çok terminalde farklı ajanları çalıştırır; takılma veya bitişte ses ile haber verir. | 0:06 | özellik |
| Graphify verilen veriler arasında anlamsal ilişkiler oluşturur. | 0:24 | özellik |
| OmniRoute ile Claude Code'da herhangi bir model kullanılabilir; böylece Claude Code neredeyse sınırsız ve ücretsiz olur. | 0:36 | özellik |
| OmniRoute 339 sağlayıcı, 90+ ücretsiz, tek uç nokta. | 0:36 | sayısal |
| Claude Code setup her projede çalıştırılmalı; hook, skill, MCP ve alt ajan önerir. | 0:46 | öneri |
| Task Observer 6 ayda 50 skill üzerinde 900'den fazla iyileştirme kaydedip uyguladı. | 0:59 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Claude Code can now run an entire agent team |
| konuşma 0:06 | herdr | herdr | The first one is called Herder. |
| kare 0:12 | herdr README | herdr | herdr is a background server |
| kare 0:15 | security-codex oturumu | Codex | kenar çubuğunda security-codex |
| kare 0:15 | gpt-5.4-mini | GPT-5.4-mini | gpt-5.4-mini medium |
| kare 0:18 | Haiku 4.5 | Claude Haiku 4.5 | Haiku 4.5 with medium effort |
| konuşma 0:24 | Graphify | Graphify | Number two is Graphify |
| konuşma 0:24 | Obsidian | Obsidian | I stack it with Obsidian |
| kare 0:24 | GitHub Trending rozeti | aday değil: konu dışı | #3 Repository Of The Day |
| kare 0:36 | OmniRoute | OmniRoute | OmniRoute — The Free AI Gateway |
| kare 0:36 | Cursor, Cline, Copilot, Antigravity | aday değil: başka adayın parçası (OmniRoute) | OmniRoute'un desteklediği istemci listesi |
| kare 0:40 | OpenRouter | OpenRouter | $10 OpenRouter top-up |
| kare 0:38 | Llama, DeepSeek, Mistral, MiniMax model listesi | aday değil: başka adayın parçası (OmniRoute) | free-tiers panosundaki model listesi |
| konuşma 0:46 | Claude Code setup | Claude Code setup | It's called Claude Code setup. |
| konuşma 0:46 | Hooks, skills, MCP, alt ajanlar | Sub agents | hooks, skills, MCPs, and sub agents |
| kare 0:49 | Gemini, OpenAI, DeepSeek sorguları | Gemini | LLM(Query Google Gemini about Readonly) |
| kare 0:49 | TypeScript Readonly örneği | aday değil: konu dışı | demo sorusu |
| konuşma 1:01 | Task Observer | Task Observer | Observer. This is a meta skill |
| kare 0:59 | Hermes Agent | Hermes Agent | Hermes and Openclaw setups |
| açıklama | charlieautomates.com kaynak sayfası | aday değil: konu dışı | Link sayfası; referans |
| açıklama | Skool topluluk bağlantısı | aday değil: konu dışı | Topluluk sayfası, erişilemez |
| açıklama | $200 aylık abonelik | aday değil: genel kavram | You're paying $200 a month |
| bağlantılı sayfa | Anthropic kursları ve docs bağlantıları | aday değil: konu dışı | Link sayfasındaki genel kaynaklar |
| bağlantılı sayfa | immich, Stirling-PDF, vaultwarden, meetily, actual, dub, activepieces, documenso, kdenlive, freeflow | aday değil: konu dışı | Videoda anılmıyor, link sayfasında başka listelerde |
| bağlantılı sayfa | awesome-design-md, impeccable, taste-skill | aday değil: konu dışı | Videoda anılmıyor |
| bağlantılı sayfa | herdr.dev docs sayfaları | herdr | herdr.dev dokümantasyon bağlantıları |
| yorum | 'Claude' yorumları | aday değil: konu dışı | Link almak için anahtar kelime yorumları |
## Kareden okunanlar
- 0:12: herdr README: v.0.4.0.mp4, 'ALL RUNNING DIFFERENT MODELS', 'always running — herdr is a background server'
- 0:15: herdr demo terminali: security-droid, security-codex, perf-claude, gpt-5.4-mini medium, izin istemi
- 0:24: Graphify README: #3 Repository Of The Day, pypi v0.9.41, app.graphify.com, '/graphify'
- 0:36: OmniRoute — The Free AI Gateway, 339 providers, 90+ free, Save 15–95% tokens
- 0:38: free-tiers panosu: ~1.51B free tokens/month, 19 countable free pools, 'NO MORE CLAUDE LIMITS'
- 0:40: Aynı pano, '$10 OpenRouter top-up', model listesi (Llama, Gemini 2.5 Flash, MiniMax-M2.7, Mistral Large 3)
- 0:49: Sneak Preview: Claude Code'da OpenAI, Google Gemini, DeepSeek sorguları, Sonnet 4 1M bağlam
- 0:59: task-observer README: 'One Skill to Rule Them All', CC-BY-4.0, 900 improvements across 50 skills
## Belirsizlikler
- Kare 0:49'daki 'Claude Code setup' README'sinin gerçek repo adı/URL'si net okunmuyor (görünüşe göre speechflow-cli ile ilgili bir yapılandırma).
- Graphify ve Task Observer repo URL'leri ekranda tam görünmüyor; bağlantılı sayfalarda doğrulanmadı.
- Konuşmada 'Herder' geçiyor, ekran ve açıklamada 'herdr' yazıyor; kanonik ad herdr alındı.
- Konuşmada 'Omni route' geçiyor, ekranda 'OmniRoute'.
- Sözlük eşleşmelerindeki Three.js, Slack, React vb. videoda gösterilmiyor; aday yapılmadı.
- 'Claude Code limitleri kaldırıyor' ve 'ücretsiz ve sınırsız' iddiaları doğrulanmış değil.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://charlieautomates.com/free-resources/#top-claude-code-plugins-2026 | açıklama | açıklama | hayır |
| https://www.skool.com/cc-strategic-ai/classroom/7cb51b97?md=b89457adad5e4ea6ad117250c75844f2 | açıklama | açıklama | hayır |
| https://herdr.dev | 0:11 | ekran | evet |
| https://app.graphify.com | 0:24 | ekran | evet |
| /dashboard/free-tiers (OmniRoute panosu) | 0:38 | ekran | hayır |
| https://charlieautomates.com/free-resources/#top-claude-code-plugins-2026 | yorum | yorum | hayır |
| https://www.skool.com/cc-strategic-ai/classroom/7cb51b97?md=b89457adad5e4ea6ad117250c75844f2 | yorum | yorum | hayır |
## İş akışı
- 1. adım — herdr ile birden çok ajan oturumunu arka planda ve farklı modellerle çalıştırma, takılınca ses uyarısı alma (README tanıtımı) — araçlar: herdr, Claude Code, Codex
- 2. adım — herdr içinde ajanın dosya okuma ve kabuk komutu (wc -l) için izin istemesini gösterme — araçlar: herdr, Claude Code
- 3. adım — Graphify'ı AI kodlama asistanında /graphify ile başlatma ve veri ilişkilerini anlatma — araçlar: Graphify, Claude Code
- 4. adım — Graphify çıktısını Obsidian ile görsel olarak inceleme (anlatım) — araçlar: Graphify, Obsidian
- 5. adım — OmniRoute README'si ve panosu ile ücretsiz sağlayıcı/model katmanlarını gösterme — araçlar: OmniRoute
- 6. adım — OmniRoute'u Claude Code ile birlikte kullanarak farklı modelleri bağlama (anlatım) — araçlar: OmniRoute, Claude Code
- 7. adım — Claude Code'da proje açılışında /init ve /review gibi komutları gösterme — araçlar: Claude Code
- 8. adım — Claude Code Setup README'sindeki örnek yapılandırmayı (sneak preview, /quorum) gösterme — araçlar: Claude Code Setup, Claude Code
- 9. adım — Task Observer README'sini açıp skill iyileştirme özelliğini anlatma — araçlar: Task Observer, skill
## Promptlar
- Proje değerlendirmesi ister — Projeyle ilgili görüş istenir: 'wdyt on this project?'
- Kod incelemesi — Mevcut değişiklikleri /review komutuyla inceletmek için yazılan istek.
- Proje talimat dosyası oluşturma — Projeye Claude için talimat dosyası (CLAUDE.md) oluşturmak üzere /init çalıştırılır.
- Çok modelli karşılaştırma — Birden çok modele aynı soru sorulur (örnek: 'gemini 1+2+3+4=?'), yanıtlar karşılaştırılır.
