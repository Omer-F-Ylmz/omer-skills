# Anthropic Just Revealed 10 NEW Rules for Claude Skills
## Künye
Anthropic Just Revealed 10 NEW Rules for Claude Skills · Jay E | RoboNuggets · süre: 12:15 · en-orig · https://youtu.be/VQyYzLJ6xos · şema 2
motor: parti 2026-10-10-short-10 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 64864 tk · claude-haiku-5-5: claude-haiku-5-5 · 97011 tk
## Özet
Jay (RoboNuggets), Anthropic'in güncellenen 'Skill authoring best practices' rehberindeki 10 kuralı Claude 5.5 modelleri bağlamında anlatıyor: kademeli açılım (SKILL.md 500 satır altı, tek seviye referans), 100 satırı aşan dosyalara içindekiler listesi, serbestlik dereceleri, skill'leri kullanılan modellerde test etme, yazımı sadeleştirme (üçüncü şahıs açıklama), iş akışı kontrol listeleri, geri bildirim döngüleri, yaygın kalıplar (şablon, örnek, koşullu iş akışı), paylaşılabilirlik (kurulum talimatı) ve hook'lar. Örnek olarak bir 'invoicing' skill'i kullanılıyor. Tüm kuralları denetleyen bir prompt PDF'te, skill-creator-plus skill'i GitHub'da paylaşılıyor. Yorumlarda kuralların aslında yeni olmadığı eleştirisi var.
## Bölümler
- 0:00 Giriş
- 0:49 Kural 1: Kademeli açılım
- 2:08 Ücretsiz rehber: tüm skill'leri denetle
- 2:55 Kural 2: İçindekiler listesi
- 3:37 Kural 3: Serbestlik dereceleri
- 5:02 Kural 4: Kullanılan modellerde test
- 6:13 Kural 5: Yazımı sadeleştirme
- 7:01 Kural 6: İş akışları ve kontrol listeleri
- 7:48 Kural 7: Geri bildirim döngüleri
- 8:34 Kural 8: Yaygın kalıplar
- 9:31 Kural 9: Paylaşılabilirlik
- 10:21 Kural 10: Hook'lar
- 11:27 Kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Skill'leri çalıştıran ve hook'ları yürüten Anthropic aracı; ekranda panelde 'Raise an invoice' isteği gösteriliyor. | 1:28 | Claude Code panelinde 'Raise an invoice' ve Read SKILL.md, Read pricing.md satırları (karede: Sağ panelde 'Claude Code' başlığı, 'Raise an invoice' isteği, Read SKILL.md ve Read pricing.md satırları) |
| SKILL.md | yok | teknik | yok | Skill'in ana dosyası; 500 satırın altında tutulup diğer dosyalara bağlanıyor. | 0:49 | keep your main skill.md file under 500 lines |
| Progressive disclosure | yok | teknik | yok | Claude yalnızca gerektiğinde ilgili dosyayı yükler; SKILL.md içindekiler sayfası gibi çalışır. | 0:49 | Anthropic calls this progressive disclosure |
| Hooks | yok | teknik | yok | Claude Code'un belirli anda otomatik çalıştırdığı kod; kesin kurallar için skill yerine hook. | 10:21 | A hook is a bit of code that Claude code runs |
| PreToolUse hook | yok | teknik | yok | Komut çalışmadan önce tetiklenen hook; invoice-guard.sh ve security-check.sh örnekleri. | 10:32 | PreToolUse hook · invoice-guard.sh, Blocked: over $10,000 (karede: Terminalde 'PreToolUse hook · invoice-guard.sh' ve 'Blocked: over $10,000, needs sign-off' satırları) |
| Claude Haiku | yok | prompt | yok | Ucuz, daha az zeki model; skill yeterli rehberlik veriyor mu diye test ediliyor. | 5:02 | For Haiku, which is cheaper but less intelligent |
| Claude Sonnet | yok | prompt | yok | Orta seviye model; skill net ve verimli mi sorusu. | 5:02 | For Sonnet, which is a good middle tier |
| Claude Opus | yok | prompt | yok | En güçlü modellerden; skill aşırı açıklama yapıyor mu kontrolü. | 5:02 | for Opus and Fable, which are their smartest models |
| Fable | yok | prompt | yok | Anthropic'in en zeki modellerinden biri olarak anılıyor; test matrisinde sütun. | 5:46 | Test matrisinde Haiku, Sonnet, Opus, Fable sütunları (karede: 'Testing every model' tablosunda Haiku, Sonnet, Opus, Fable sütunları ve invoicing, weekly-report gibi skill satırları) |
| skill-creator-plus | yok | skill | https://github.com/robonuggets/skill-creator-plus | Jay'in skill'leri denetleyen, geliştiren ücretsiz skill'i; GitHub'da paylaşılıyor. | 11:27 | this skill I made called skill creator plus |
| skill-creator | yok | skill | https://github.com/anthropics/skills | Claude Code ile gelen Anthropic'in varsayılan skill oluşturucusu; Mart'ta güncellenmiş. | 11:27 | skill creator skill that comes default with Cloud Code |
| secure-operations | yok | skill | yok | Hook'u kendi içinde barındıran Anthropic örnek skill'i; her Bash komutundan önce güvenlik kontrolü. | 10:44 | name: secure-operations, hooks PreToolUse matcher Bash (karede: YAML frontmatter'da name: secure-operations, hooks: PreToolUse, matcher: "Bash", command: ./scripts/security-check) |
| invoicing | yok | skill | yok | Videoda örnek olarak kullanılan fatura skill'i (SKILL.md, pricing.md, clients.md, scripts). | 1:16 | invoicing klasörü SKILL.md, pricing.md, clients.md, scripts (karede: Explorer'da INVOICING klasörü; SKILL.md içinde name: invoicing, Steps 1-4) |
| pip | yok | CLI | yok | Skill içine bağımlılık kurulum talimatı örneği (pip install pypdf reportlab). | 9:44 | pip install pypdf reportlab (karede: Kod bloğunda 'pip install pypdf reportlab' ve 'If missing, install them') |
| pypdf | yok | teknik | yok | Anthropic rehberinin paylaşılabilirlik örneğindeki PDF kütüphanesi. | 9:26 | Install required package: 'pip install pypdf'; from pypdf import PdfReader (karede: Rehberde 'Install required package: pip install pypdf' ve 'from pypdf import PdfReader') |
| reportlab | yok | teknik | yok | Fatura skill'i için kurulması önerilen Python paketi. | 9:44 | pip install pypdf reportlab (karede: 'pip install pypdf reportlab' satırı) |
| Python | yok | teknik | yok | Skill betikleri (create_invoice.py, validate.py) Python ile çalışıyor. | 4:38 | scripts/create_invoice.py (karede: Explorer'da scripts/create_invoice.py ve SKILL.md'de Run scripts/create_invoice.py) |
| Skool | yok | iş akışı | yok | RoboNuggets topluluğunun barındığı platform; sınıf ve topluluk sayfaları gösteriliyor. | 2:20 | skool.com/robonuggets, Powered by skool (karede: RoboNuggets Community About sayfası, 'skool.com/robonuggets' ve Claude Living Masterclass sınıfı) |
| GitHub | yok | iş akışı | yok | skill-creator-plus ve anthropics/skills depolarını barındıran servis. | 11:04 | github.com/robonuggets, robonuggets / skill-creator-plus (karede: robonuggets / skill-creator-plus deposu, Code/Issues/Pull requests sekmeleri) |
| MCP | yok | teknik | yok | Rehberde araç adlarını sunucu önekiyle yazma örneği (BigQuery, GitHub MCP sunucuları). | 9:26 | BigQuery and GitHub are MCP server names (karede: Rehberde 'BigQuery and GitHub are MCP server names', bigquery_schema ve create_issue) |
| Claude Skills | yok | skill | yok | Claude'un SKILL.md dosyalarıyla yüklenen beceri paketleri; videonun ana konusu. | 0:00 | the way we build and use skills apparently need to change |
| docx-js | yok | teknik | yok | Yeni Word belgeleri oluşturmak için JavaScript kütüphanesi; Anthropic rehberindeki örnekte geçiyor. | 0:16 | Use docx-js for new documents. See [DOCX-JS.md] (karede: Rehber ekran görüntüsünde 'Use docx-js for new documents' satırı.) |
| npm | yok | CLI | yok | Node.js paket yöneticisi; Claude Code'un Bash çağrılarında npm install, npm run build ve npm test görünüyor. | 10:46 | Bash(npm install) · PreToolUse hook · security-check.sh (karede: Terminalde Bash(npm install) satırı ve altında PreToolUse hook · security-check.sh ✓ satırı.) |
| Git | yok | CLI | yok | Sürüm kontrol aracı; Claude Code'un Bash çağrısında git pull komutu görünüyor. | 10:48 | Bash(git pull) (karede: Terminalde Bash(git pull) satırı.) |
| Markdown | yok | teknik | yok | Skill dosyalarının yazıldığı biçim; editörde SKILL.md dosyası Markdown olarak görünüyor. | 1:24 | Ln 8, Col 1 UTF-8 Markdown (karede: Editörün alt durum çubuğunda 'Ln 8, Col 1 UTF-8 Markdown' yazısı.) |
| Skill'leri 10 kurala göre denetleme (PDF'teki 'The Skill Audit' promptu) | yok | prompt | yok | Skill klasöründeki her skill'i yazım kurallarına göre denetle; SKILL.md 500 satırı aşıyor mu, bağlı her dosyayı listele ve yalnızca başka dosya üzerinden ulaşılanları işaretle. Herhangi bir şeyi değiştirmeden önce değişiklik listesini göster. | 2:02 | kaynak: kare |
| Kural 1 için basit kademeli açılım denetimi | yok | prompt | yok | En çok kullanılan beş skill'i incele; her biri için SKILL.md 500 satırı aşıyor mu, hangi dosyalara bağlı, dolaylı ulaşılan dosya var mı söyle. Değiştirmeden önce listeyi göster. | 2:02 | kaynak: kare |
## Açıklama bağlantıları
- https://www.skool.com/robonuggets-free/classroom/750914f0?md=66ba31d1700544a8842eefa1f670caa1 — Ücretsiz Skool sınıfı; 10 kural PDF'i ve skill-creator-plus. · aday: hayır · Yazarın topluluk/ücretsiz kaynak sayfası; izleyicinin kullanacağı araç değil, videoda gösterilen Skool'un parçası. · sınıf: diğer
- https://www.skool.com/robonuggets — RoboNuggets ücretli topluluğu. · aday: hayır · Ücretli topluluk · sınıf: diğer · erişilemez: ücretli topluluk
- https://www.getrubric.app/ — Rubric uygulaması. · aday: hayır · Videoda gösterilmiyor ve anlatılmıyor; yalnızca açıklama bağlantısı. · sınıf: diğer
- https://blotato.com/?ref=robonuggets — Blotato; ortak araç bağlantısı. · aday: hayır · Videoda kullanılmıyor; yönlendirme parametresi var. · sınıf: affiliate
- https://n8n.partnerlinks.io/o3jqtj032c02 — n8n ortak bağlantısı. · aday: hayır · n8n videoda anlatılmıyor/kullanılmıyor. · sınıf: affiliate
- https://www.make.com/en/register?pc=robonuggets — Make kayıt bağlantısı. · aday: hayır · Make videoda kullanılmıyor; promosyon kodu var. · sınıf: affiliate
- https://try.elevenlabs.io/m5mn2jkv5rzk — ElevenLabs ortak bağlantısı. · aday: hayır · ElevenLabs videoda kullanılmıyor. · sınıf: affiliate
- https://www.apify.com?fpr=sffv1 — Apify ortak bağlantısı. · aday: hayır · Apify videoda kullanılmıyor. · sınıf: affiliate
- https://www.youtube.com/@RoboNuggets — Kanal sayfası. · aday: hayır · Sosyal profil bağlantısı. · sınıf: diğer
- https://www.instagram.com/robonuggets — Instagram profili. · aday: hayır · Sosyal profil bağlantısı. · sınıf: diğer
- https://www.tiktok.com/@robonuggets — TikTok profili. · aday: hayır · Sosyal profil bağlantısı. · sınıf: diğer
- https://www.twitter.com/robonuggets — Twitter profili. · aday: hayır · Sosyal profil bağlantısı. · sınıf: diğer
- https://www.linkedin.com/in/j-enri/ — Yazarın LinkedIn profili. · aday: hayır · Kişisel profil bağlantısı. · sınıf: diğer
- https://robolabs.so — ROBO Group ajans sitesi. · aday: hayır · Yazarın şirket sitesi; videoda araç olarak kullanılmıyor. · sınıf: diğer
- https://www.skool.com/robonuggets-free/classroom — Ücretsiz Skool sınıf listesi. · aday: hayır · Yazarın topluluk sayfası; araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip install pypdf | Skill'in PDF kütüphanesini kurar (rehberdeki iyi örnek). (karede: 'Install required package: pip install pypdf' ve 'from pypdf import PdfReader') | 9:26 | kare |
| pip install pypdf reportlab | Fatura skill'i için eksikse gerekli paketleri kurar. (karede: 'If missing, install them:' altında 'pip install pypdf reportlab') | 9:44 | kare |
| python scripts/send.py --amount 12400 | Fatura gönderir; PreToolUse hook 10.000$ üstünü engeller. (karede: 'Bash(python scripts/send.py --amount 12400)' ardından invoice-guard.sh engeli) | 10:32 | kare |
| /secure-operations | Hook içeren secure-operations skill'ini çağırır. (karede: Claude Code terminalinde '> /secure-operations', ardından Bash(npm install) ve security-check.sh ✓) | 10:46 | kare |
| npm install | Hook'un her Bash komutundan önce çalıştığını gösteren örnek komut. (karede: 'Bash(npm install)' altında 'PreToolUse hook · security-check.sh') | 10:46 | kare |
| git pull | Hook'un tetiklendiği örnek Bash komutu. (karede: OCR'da 'Bash(git pull)' satırı) | 10:48 | kare |
| npm run build | Hook'un tetiklendiği örnek Bash komutu. (karede: OCR'da 'Bash(npm run build)' satırı) | 10:50 | kare |
| npm test | Hook'un tetiklendiği örnek Bash komutu. (karede: OCR'da 'Bash(npm test)' satırı) | 10:52 | kare |
| head -100 | Claude'un iç içe referanslı dosyaları ilk 100 satırla önizlemek için kullanabileceği komut. (karede: Vurgulu 'Claude might use commands like head -100 to preview content') | 1:44 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Uzun skill dosyalarında Claude yalnızca ilk 100 satırı okuyabilir. | 0:00 | özellik |
| Ana SKILL.md 500 satırın altında tutulmalı, gerisi ayrı dosyalara bölünmeli. | 0:49 | öneri |
| İç içe referanslarda Claude üçüncü dosyanın yalnızca ilk 100 satırını önizleyebilir. | 1:44 | özellik |
| 100 satırdan uzun dosyaların en üstüne içindekiler listesi konmalı. | 2:55 | öneri |
| Eski modeller için yazılan skill'ler yeni modeller için fazla kuralcı olabilir ve çıktıyı kötüleştirebilir. | 5:02 | karşılaştırma |
| Üçüncü şahıs açıklama yazılmalı; birinci şahıs düşük modellerde keşfi bozabilir. | 6:13 | öneri |
| Mutlaka uyulması gereken kural skill'den hook'a taşınmalı. | 10:44 | öneri |
| Anthropic'in varsayılan skill-creator'ı bu yılın Mart ayında son güncellenmiş. | 11:27 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude 5.5 modelleri | Claude Opus | Claude's 5.5 models are here |
| konuşma 0:00 | Anthropic skills rehberi | aday değil: genel kavram | Anthropic just updated their official comprehensive guide for skills |
| konuşma 0:49 | SKILL.md | SKILL.md | keep your main skill.md file under 500 lines |
| konuşma 0:49 | Progressive disclosure | Progressive disclosure | Anthropic calls this progressive disclosure |
| kare 0:02 | anthropic.com/claude-opus-5-5 sayfası | Claude Opus | Claude Opus 5.5 duyuru sayfası |
| kare 0:02 | anthropic.com/claude-sonnet-5-5 sayfası | Claude Sonnet | Claude Sonnet 5.5 duyuru sayfası |
| kare 0:06 | Claude Platform Docs | aday değil: konu dışı | Skill authoring best practices dokümanı, referans sayfası |
| kare 0:16 | REDLINING.md / OOXML.md / DOCX-JS.md | aday değil: başka adayın parçası (SKILL.md) | Rehberdeki iç içe referans örnek dosyaları |
| kare 0:16 | head -100 | aday değil: genel kavram | Claude might use commands like head -100 |
| kare 0:40 | Unilever, Ogilvy, Lipton, P&G, Virgin, Knorr, HelloFresh, Hellmann's, Microsoft logoları | aday değil: konu dışı | Yazarın geçmiş markaları |
| kare 0:44 | University of Technology Sydney | aday değil: konu dışı | Yazarın eğitim bilgisi |
| kare 0:46 | Skool topluluk haritası | Skool | The RoboNuggets Community Map sekmesi |
| kare 1:16 | invoicing skill | invoicing | name: invoicing, clients.md, pricing.md, scripts |
| kare 1:28 | Claude Code paneli | Claude Code | Raise an invoice, Read SKILL.md |
| konuşma 1:49 | Tek seviye referans | aday değil: başka adayın parçası (Progressive disclosure) | have your skills only be one level deep |
| kare 2:12 | The 10 SKILL Rules PDF | aday değil: sponsor/reklam | Yazarın topluluk için sunduğu ücretsiz PDF |
| kare 2:18 | The Skill Audit promptu | aday değil: başka adayın parçası (invoicing) | Audit every skill in my skills folder against the skill-writing rules |
| konuşma 2:08 | RoboNuggets topluluğu | Skool | that's pretty much all we do over at the Robo Nuggets community |
| kare 2:28 | Claude Living Masterclass | aday değil: sponsor/reklam | Topluluk kursu tanıtımı |
| kare 2:30 | Agents-as-a-Service kursu | aday değil: sponsor/reklam | Topluluk kursu tanıtımı |
| kare 2:44 | taxrebates.ai | aday değil: konu dışı | Üye gönderisinde geçen müşteri sitesi |
| kare 3:18 | İçindekiler listesi (Contents) | aday değil: başka adayın parçası (SKILL.md) | pricing.md içinde ## Contents |
| konuşma 3:37 | Serbestlik dereceleri | aday değil: genel kavram | Anthropic calls this setting the degrees of freedom |
| kare 4:38 | scripts/create_invoice.py | Python | Explorer'da create_invoice.py |
| kare 4:58 | Claude Haiku | Claude Haiku | Claude Haiku (fast, economical) |
| kare 4:58 | Claude Sonnet | Claude Sonnet | Claude Sonnet (balanced) |
| kare 4:58 | Claude Opus | Claude Opus | Claude Opus (powerful reasoning) |
| kare 5:46 | Fable | Fable | Test matrisinde Fable sütunu |
| kare 5:46 | weekly-report, brainstorm, meeting-notes, client-emails | aday değil: başka adayın parçası (invoicing) | Test matrisindeki örnek skill adları |
| kare 6:12 | Context window | aday değil: genel kavram | The context window is a public good |
| kare 6:30 | Üçüncü şahıs açıklama | aday değil: genel kavram | description: Creates client invoices... |
| kare 6:46 | İş akışı kontrol listesi | aday değil: genel kavram | Copy this checklist and track your progress |
| kare 7:22 | fill_form.py / validate_fields.py / verify_output.py | Python | Rehberdeki betik komutları |
| kare 7:44 | Geri bildirim döngüsü | aday değil: genel kavram | Run it, fix what fails, repeat |
| kare 7:52 | STYLE_GUIDE.md / validate.py | aday değil: başka adayın parçası (SKILL.md) | Stil kılavuzu örnek dosyaları |
| kare 8:26 | Şablon kalıbı | aday değil: genel kavram | ALWAYS use this exact template structure |
| kare 8:44 | Örnekler kalıbı | aday değil: genel kavram | Examples convey the desired style |
| kare 8:54 | Koşullu iş akışı | aday değil: genel kavram | Creating new content? / Editing existing content? |
| kare 9:26 | pypdf | pypdf | from pypdf import PdfReader |
| kare 9:44 | reportlab | reportlab | pip install pypdf reportlab |
| kare 9:44 | pip | pip | pip install pypdf reportlab |
| kare 9:26 | MCP sunucuları BigQuery ve GitHub | MCP | BigQuery and GitHub are MCP server names |
| kare 9:32 | YAML frontmatter | aday değil: başka adayın parçası (SKILL.md) | YAML frontmatter requirements |
| kare 10:32 | invoice-guard.sh | PreToolUse hook | PreToolUse hook · invoice-guard.sh |
| kare 10:44 | secure-operations skill | secure-operations | name: secure-operations |
| kare 10:46 | security-check.sh | PreToolUse hook | PreToolUse hook · security-check.sh |
| kare 10:46 | npm | aday değil: konu dışı | Bash(npm install) örnek komut |
| kare 10:48 | Git | aday değil: konu dışı | Bash(git pull) örnek komut |
| kare 10:38 | code.claude.com/docs | Hooks | Claude skipped a rule that must hold every time: move the rule into a hook |
| kare 11:04 | robonuggets/skill-creator-plus | skill-creator-plus | github.com/robonuggets, skill-creator-plus Public |
| kare 11:04 | GitHub | GitHub | GitHub depo sayfası |
| kare 11:14 | anthropics/skills skill-creator | skill-creator | anthropics / skills / skill-creator |
| açıklama | skool.com/robonuggets-free sınıfı | Skool | Ücretsiz sınıf bağlantısı |
| açıklama | skool.com/robonuggets | aday değil: sponsor/reklam | Ücretli topluluk tanıtımı |
| açıklama | getrubric.app | aday değil: konu dışı | Videoda anılmayan açıklama bağlantısı |
| açıklama | Blotato | aday değil: sponsor/reklam | blotato.com/?ref=robonuggets ortak bağlantısı |
| açıklama | n8n | aday değil: sponsor/reklam | n8n.partnerlinks.io ortak bağlantısı |
| açıklama | Make | aday değil: sponsor/reklam | make.com/en/register?pc=robonuggets |
| açıklama | ElevenLabs | aday değil: sponsor/reklam | try.elevenlabs.io ortak bağlantısı |
| açıklama | Apify | aday değil: sponsor/reklam | apify.com?fpr=sffv1 ortak bağlantısı |
| açıklama | YouTube, Instagram, TikTok, Twitter, LinkedIn profilleri | aday değil: konu dışı | Sosyal medya bağlantıları |
| açıklama | robolabs.so | aday değil: konu dışı | Yazarın ajans sitesi |
| açıklama | Etiketler (#ClaudeCode, #AgentSkills vb.) | aday değil: konu dışı | Hashtag listesi |
| yorum | Codex | aday değil: konu dışı | Yorumcu 'claude code/codex work' diyor |
| yorum | Claude Desktop | aday değil: konu dışı | Yorumcu yedekleme videosu istiyor |
| yorum | ECC (everything-claude-code) | aday değil: konu dışı | Yorumcu 'I have been using ECC for some time' |
| yorum | VS Code | aday değil: konu dışı | Yorumcu skill'lerin VS Code klasörleri gibi olup olmadığını soruyor |
| yorum | Fable 5.5 | aday değil: konu dışı | Yorum: Wait for Fable 5.5 in few weeks |
| bağlantılı sayfa | platform.claude.com ve code.claude.com dokümanları | aday değil: konu dışı | Alt sayfalar videoda gösterilmeyen doküman bağlantıları |
| bağlantılı sayfa | mcp.apify.com, crawlee.dev, github.com/n8n-io/n8n | aday değil: sponsor/reklam | Ortak bağlantı sayfalarından gelen bağlantılar |
## Kareden okunanlar
- 0:02: anthropic.com/claude-opus-5-5 (22 Eylül 2026) ve anthropic.com/claude-sonnet-5-5 (28 Eylül 2026) duyuru sayfaları.
- 0:06: Claude Platform Docs: 'Skill authoring best practices', platform.claude.com/docs.
- 1:16: invoicing klasörü; SKILL.md: name: invoicing, description: Raises invoices., adımlar clients.md, pricing.md, scripts/invoice.py, onay için gönder.
- 1:28: Claude Code paneli: 'Raise an invoice'; Read SKILL.md, Read pricing.md; scripts 'not loaded'; pricing: gün $800, yarım gün $450, acil +%25.
- 2:12: 'The 10 SKILL Rules' PDF'i, 'Grab it in the description below'.
- 2:18: 'It audits all your skills' PDF sayfası ve '01 · THE SKILL AUDIT' prompt kartı.
- 2:20: RoboNuggets Community About sayfası: skool.com/robonuggets, 1.2k üye, 'Official member of the Claude Partner Network'.
- 2:28: Claude Living Masterclass: Volume A Setup, B Skills, C Memory modülleri.
- 2:30: Agents-as-a-Service kursu: 'LAND CLIENTS', 10K MRR yol haritası.
- 2:44: Topluluk gönderisi: https://taxrebates.ai, '$40k project delivered!'; lider tablosu.
- 3:18: pricing.md: Contents (Hourly rates, Project packages, Rush fees, Payment terms, Discounts); Design $120, Development $150, Copywriting $90.
- 3:24: pricing.md satır 240-241: '## Discounts – Returning clients: 10%'.
- 4:08: Serbestlik derecesi kaydırıcısı: High, Medium, Low; 'Week 4' rapor şablonu.
- 4:38: invoicing SKILL.md: 1 Gather line items, 2 Create the invoice (Never change the amounts), 3 Write the email; scripts/create_invoice.py.
- 4:58: Rehberde model testi: Haiku (fast, economical), Sonnet (balanced), Opus (powerful reasoning).
- 5:46: Test matrisi: invoicing, weekly-report, brainstorm, meeting-notes, client-emails × Haiku, Sonnet, Opus, Fable; Current session 0% used.
- 6:08: 'Wasted tokens': '## What is an invoice?' satırları üstü çizili.
- 6:24: 'Always write in third person' kutusu.
- 6:30: description: Creates client invoices and sends payment remind… (iyi) / description: I can help you with invoices… (kötü).
- 6:46: Rehberde araştırma sentezi kontrol listesi, Step 1-5.
- 7:10: Aylık fatura kontrol listesi, Step 1-5; Step 4 total kontrolü, geri dön satırı.
- 7:22: Rehberde fill_form.py, validate_fields.py, verify_output.py ve 'return to Step 2'.
- 7:56: Stil kılavuzu uyumu: taslak, kontrol listesi, sorun varsa revize, gereksinimler karşılanınca bitir.
- 8:26: Şablon kalıbı: strict 'ALWAYS use this exact template structure' / flexible 'Here is a sensible default format'.
- 8:44: Örnek kalıbı: commit mesajı girdi/çıktı; koşullu iş akışı Creating/Editing.
- 8:56: invoicing SKILL.md: New invoice? → Create; Editing an invoice? → Edit; scripts/make_invoice.py; Re-check the totals.
- 9:26: Rehberde 'Avoid assuming tools are installed', pip install pypdf, BigQuery/GitHub MCP sunucu adları.
- 10:32: Terminal ~/invoicing: Bash(python scripts/send.py --amount 12400), PreToolUse hook invoice-guard.sh, Blocked: over $10,000, needs sign-off.
- 10:44: secure-operations frontmatter: hooks, PreToolUse, matcher Bash, command ./scripts/security-check…
- 10:46: Claude Code ~/my-app: /secure-operations, Bash(npm install), security-check.sh ✓, 'hook on'.
- 11:04: github.com/robonuggets deposu robonuggets/skill-creator-plus: examples, references, scripts, LICENSE, README.md, SKILL.md.
- 11:14: anthropics/skills deposu, skills/skill-creator yolu; 'Anthropic's Skill Creator comes with Claude Code'.
## Belirsizlikler
- Ekranda 'Fable' modeli test matrisinde ve konuşmada anılıyor; resmi ürün adı ve sürümü doğrulanamadı.
- Yorumda 'Fable 5.5' ve OCR'da 'Fable 5 guide' geçiyor; bunlar videoda gösterilen bir model değil.
- Sözlük eşleşmeleri (Matter.js, Next.js, D3.js, MongoDB, Lottie, Three.js, React, Hermes Agent vb.) bulanık/OCR gürültüsü; videoda kullanılmadığı için aday yapılmadı.
- OCR'daki marka logoları (Unilever, Ogilvy, Lipton, P&G, Microsoft, HelloFresh vb.) yazarın geçmiş müşterileri; araç değil.
- Başlıktaki '10 yeni kural' iddiası yorumda eleştiriliyor: rehberin eski olduğu, kuralların yeni olmadığı söyleniyor.
- Açıklamadaki Zaman damgaları bölümü boş geldi; bölümler Chapter listesinden alındı.
- Kural 1 bölümündeki asıl audit prompt metni tam okunamadı; OCR kısmen bozuk, özet kareden çıkarıldı.
- Rubric (getrubric.app) açıklamada var ama videoda anılmıyor.
## Atlanan segment oranı
0/17 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://youtu.be/VQyYzLJ6xos | açıklama | açıklama | hayır |
| anthropic.com/claude-opus-5-5 | 0:02 | ekran | hayır |
| anthropic.com/claude-sonnet-5-5 | 0:02 | ekran | hayır |
| platform.claude.com/docs | 0:06 | ekran | hayır |
| skool.com/robonuggets | 2:20 | ekran | hayır |
| https://taxrebates.ai | 2:44 | ekran | hayır |
| invoice-guard.sh | 10:32 | ekran | hayır |
| code.claude.com/docs | 10:38 | ekran | hayır |
| security-check.sh | 10:46 | ekran | hayır |
| github.com/robonuggets | 11:04 | ekran | evet |
| https://www.skool.com/robonuggets-free/classroom/750914f0?md=66ba31d1700544a8842eefa1f670caa1 | açıklama | açıklama | hayır |
| https://www.skool.com/robonuggets | açıklama | açıklama | hayır |
| https://www.getrubric.app/ | açıklama | açıklama | hayır |
| https://blotato.com/?ref=robonuggets | açıklama | açıklama | hayır |
| https://n8n.partnerlinks.io/o3jqtj032c02 | açıklama | açıklama | hayır |
| https://www.make.com/en/register?pc=robonuggets | açıklama | açıklama | hayır |
| https://try.elevenlabs.io/m5mn2jkv5rzk | açıklama | açıklama | hayır |
| https://www.apify.com?fpr=sffv1 | açıklama | açıklama | hayır |
| https://www.youtube.com/@RoboNuggets | açıklama | açıklama | hayır |
| https://www.instagram.com/robonuggets | açıklama | açıklama | hayır |
| https://www.tiktok.com/@robonuggets | açıklama | açıklama | hayır |
| https://www.twitter.com/robonuggets | açıklama | açıklama | hayır |
| https://www.linkedin.com/in/j-enri/ | açıklama | açıklama | hayır |
| https://robolabs.so | açıklama | açıklama | hayır |
| https://www.skool.com/robonuggets-free/classroom | açıklama | yorum | hayır |
## İş akışı
- yok
## Promptlar
- Skill'leri 10 kurala göre denetleme (PDF'teki 'The Skill Audit' promptu) — Skill klasöründeki her skill'i yazım kurallarına göre denetle; SKILL.md 500 satırı aşıyor mu, bağlı her dosyayı listele ve yalnızca başka dosya üzerinden ulaşılanları işaretle. Herhangi bir şeyi değiştirmeden önce değişiklik listesini göster.
- Kural 1 için basit kademeli açılım denetimi — En çok kullanılan beş skill'i incele; her biri için SKILL.md 500 satırı aşıyor mu, hangi dosyalara bağlı, dolaylı ulaşılan dosya var mı söyle. Değiştirmeden önce listeyi göster.
ikinci göz KAPALI: --ikinci-goz yok
