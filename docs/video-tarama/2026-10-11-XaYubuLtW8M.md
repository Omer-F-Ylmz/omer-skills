# Claude Mods - The Biggest Claude Code Upgrade!
## Künye
Claude Mods - The Biggest Claude Code Upgrade! · Prompt Engineering · süre: 10:37 · en-orig · https://youtu.be/XaYubuLtW8M · şema 2
motor: parti 2026-10-11-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 57511 tk · claude-haiku-5-5: claude-haiku-5-5 · 110856 tk
## Özet
Video, Anthropic'in Claude Code'a getirdiği 'mods' özelliğini anlatıyor (v2.1.287). Mod, hooks.json üzerinden JavaScript/TypeScript dosyasına bağlanan ve Claude Code'un içinde çalışan bir eklenti türüdür. Araç çağrısını gözlemleyebilir, yeniden yazabilir ya da engelleyebilir; arayüze panel çizebilir. Sunucu hooks, skills ve MCP'den farklıdır; oturum boyunca yüklü kalır. Sunucu, ilk mod, pazar yeri kurulumu, rm -rf koruması, bağlam göstergesi ve geçmişten mod ürettirme prompt'u gösteriliyor. Son bölümde güvenlik uyarısı (claude plugin validate) ve mod ile hook/skill/MCP seçimi anlatılıyor.
## Bölümler
- 0:00 Claude Code modları: Anthropic Claude Code'u açıyor
- 1:39 Mod nedir ve nasıl çalışır?
- 3:54 Mod ile hook, skill ve MCP farkı: neden önemli
- 5:18 İlk mod ve sıcak yeniden yükleme
- 6:32 Mod kurulumu ve rm -rf'yi durduran koruma
- 7:42 Claude'a mod yazdırmak
- 9:15 Mod güvenliği ve ne zaman mod kullanılır
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | https://github.com/anthropics/claude-code | Modların çalıştığı Anthropic'in kodlama ajanı CLI'ı; videonun ana aracı. | 0:00 | Ekranda 'Claude Code v2.1.287' başlığı ve mod diyagramı görünüyor. (karede: kanıttan) Ekranda 'Claude Code v2.1.287' başlığı ve mod diyagramı görünüyor. |
| Claude Mods | yok | plugin | yok | Claude Code içinde çalışan JS/TS işlevleriyle davranışı ve arayüzü değiştiren eklenti türü. | 0:04 | Changelog satırı 'Added Claude Mods: plugins may now modify deeper behavior'. (karede: kanıttan) Changelog satırı 'Added Claude Mods: plugins may now modify deeper behavior'. |
| Opus 5.5 | yok | teknik | yok | Demoda Claude Code'u çalıştıran ana model. | 5:14 | Başlıkta 'Opus 5.5 (1M context) with high effort · Claude Max'. (karede: kanıttan) Başlıkta 'Opus 5.5 (1M context) with high effort · Claude Max'. |
| /plugin | yok | CLI | yok | Eklentileri keşfetme, kurma ve mod durumunu görme menüsü. | 5:28 | Plugins sekmeleri: Discover, Installed, Marketplaces görünüyor. (karede: kanıttan) Plugins sekmeleri: Discover, Installed, Marketplaces görünüyor. |
| --plugin-dir | yok | CLI | yok | Bir klasörü tek oturum için eklenti olarak yükleyen bayrak; hot reload sağlar. | 2:08 | Ekranda 'claude --plugin-dir ./my-mod' yazıyor. (karede: kanıttan) Ekranda 'claude --plugin-dir ./my-mod' yazıyor. |
| claude plugin validate | yok | CLI | yok | Modun dinlediği olayları ve yaptığı çağrıları listeleyen doğrulama komutu. | 9:02 | Çıktıda 'Validation passed' ve register.js hooks/calls listesi. (karede: kanıttan) Çıktıda 'Validation passed' ve register.js hooks/calls listesi. |
| claude plugin marketplace | yok | CLI | yok | Pazar yerlerini listeleme ve ekleme komutu. | 6:26 | 'claude plugin marketplace list' çıktısı pazar yerlerini gösteriyor. (karede: kanıttan) 'claude plugin marketplace list' çıktısı pazar yerlerini gösteriyor. |
| claude plugin install | yok | CLI | yok | Pazar yerinden mod kurar. | 6:34 | 'claude plugin install local-lab@ep-mods --scope user' komutu. (karede: kanıttan) 'claude plugin install local-lab@ep-mods --scope user' komutu. |
| hooks | yok | teknik | yok | Olay başına bir kez çalışan kabuk betiği; modlarla karşılaştırılıyor. | 3:54 | Karede 'settings hook $ ./check.sh' görünüyor. (karede: kanıttan) Karede 'settings hook $ ./check.sh' görünüyor. |
| Skills | yok | skill | yok | Claude'a talimat izlettirmek için kullanılan yapı; modla karşılaştırılıyor. | 9:15 | 'when to use a mod' tablosunda 'skills' etiketi. (karede: kanıttan) 'when to use a mod' tablosunda 'skills' etiketi. |
| MCP servers | yok | MCP | yok | Claude'un başka servislere erişmesi için; modla karşılaştırılıyor. | 9:15 | Tabloda 'MCP servers' etiketi. (karede: kanıttan) Tabloda 'MCP servers' etiketi. |
| DeepSeek Harness | yok | CLI | https://github.com/deepseek-ai/deepseek-harness | Her şeyin eklenti olduğu açık kaynak ajan çatısı; modlarla benzetiliyor. | 0:55 | 'When Deepseek released their harness, they said everything in it is a plug-in.' |
| cc-plugin-diff | yok | plugin | yok | /diff görünümünü çizen yerleşik mod. | 4:36 | Karede 'cc-plugin-diff' etiketi ve docs tablosu. (karede: kanıttan) Karede 'cc-plugin-diff' etiketi ve docs tablosu. |
| cc-plugin-agents-md | yok | plugin | yok | AGENTS.md dosyasını proje talimatı olarak yükleyen yerleşik mod. | 4:40 | Karede 'cc-plugin-agents-md' etiketi. (karede: kanıttan) Karede 'cc-plugin-agents-md' etiketi. |
| cc-plugin-plugin-authoring | yok | skill | yok | Claude'un mod yazması için skill içeren yerleşik eklenti. | 5:28 | Installed listesinde 'cc-plugin-plugin-authoring Plugin builtin'. (karede: kanıttan) Installed listesinde 'cc-plugin-plugin-authoring Plugin builtin'. |
| first-mod | yok | plugin | yok | Docs'taki başlangıç modu: araç sayacı ve /tally komutu. | 5:36 | Karede 'first-mod 3 files · 31 lines' ve /tally çıktısı. (karede: kanıttan) Karede 'first-mod 3 files · 31 lines' ve /tally çıktısı. |
| local-lab | yok | plugin | yok | Yerel model sunucularını gösteren prompt üstü şerit modu. | 6:34 | 'claude plugin install local-lab@ep-mods' ve 'lab' çubuğu. (karede: kanıttan) 'claude plugin install local-lab@ep-mods' ve 'lab' çubuğu. |
| house-rules | yok | plugin | yok | Riskli kabuk komutlarını durduran ve kural ekleyen koruma modu. | 7:18 | 'House rules: this command looks destructive. Run it?' istemi. (karede: kanıttan) 'House rules: this command looks destructive. Run it?' istemi. |
| context-weather | yok | plugin | yok | Bağlam penceresi doluluğunu gösteren gösterge modu. | 7:34 | 'a gauge that shows how full my context window is'; marketplace.json'da adı geçiyor. |
| secret-redactor | yok | plugin | yok | Bash çıktısındaki gizli bilgileri maskeleyen topluluk modu. | 9:22 | '[secret-redactor] redacted openai-api-key, connection-string'. (karede: kanıttan) '[secret-redactor] redacted openai-api-key, connection-string'. |
| run-radar | yok | plugin | yok | Makineleri ve çalışan işleri gösteren yan panel modu. | 8:50 | '/runs run-radar: Run Radar opened.' ve '5 mods active'. · kanıt: kare (karede: '/runs run-radar: Run Radar opened.' ve '5 mods active'.) |
| proof-shelf | yok | plugin | yok | Oturumun ürettiği görsel ve belgeleri listeleyen raf modu. | 8:50 | '/shelf proof-shelf: Proof Shelf opened.' Images ve Documents bölümleri. · kanıt: kare (karede: '/shelf proof-shelf: Proof Shelf opened.' Images ve Documents bölümleri.) |
| public-hold | yok | plugin | yok | Yayın öncesi hangi hesaptan yayınlanacağını kontrol eden koruma modu. | 8:50 | Karede 'public-hold', 'PromtEngineer ✓?' ve 'publish → hold'. · kanıt: kare (karede: Karede 'public-hold', 'PromtEngineer ✓?' ve 'publish → hold'.) |
| script-desk | yok | plugin | yok | Kullanıcının geçmişinden üretilen mod fikirlerinden biri. | 8:50 | Karede 'script-desk' etiketi. · kanıt: kare (karede: Karede 'script-desk' etiketi.) |
| keep-alive | yok | plugin | yok | Geçmişten türetilen mod fikirlerinden biri. | 8:50 | Karede 'keep-alive' etiketi. · kanıt: kare (karede: Karede 'keep-alive' etiketi.) |
| api-wallet | yok | plugin | yok | Geçmişten türetilen mod fikirlerinden biri. | 8:50 | Karede 'api-wallet' etiketi. · kanıt: kare (karede: Karede 'api-wallet' etiketi.) |
| background-it | yok | plugin | yok | Geçmişten türetilen mod fikirlerinden biri. | 8:50 | Karede 'background-it' etiketi. · kanıt: kare (karede: Karede 'background-it' etiketi.) |
| hide-email | yok | plugin | yok | Yanıtlardaki e-posta adreslerini ekranda gizleyen mod örneği. | 3:40 | Dosya ağacında 'hide-email/hooks/register.tsx' ve maskelenmiş e-posta. (karede: kanıttan) Dosya ağacında 'hide-email/hooks/register.tsx' ve maskelenmiş e-posta. |
| Claude Code mod geçmiş prompt'u | yok | prompt | yok | Son 20 oturumdan mod fikri çıkartan prompt. | 8:02 | Karede 'the prompt: Go through my last 20 sessions...' görünüyor. · kanıt: kare (karede: Karede 'the prompt: Go through my last 20 sessions...' görünüyor.) |
| whryte | yok | CLI | yok | Sesten metne uygulaması; açıklamada tanıtılıyor, videoda kullanıldığı gösterilmiyor. | açıklama | 'My voice to text App: whryte.com'. |
| JavaScript | yok | teknik | yok | Modların yazılabildiği dillerden biri. | 1:39 | points to a JavaScript or TypeScript file |
| TypeScript | yok | teknik | yok | Modların yazılabildiği dillerden biri; örnekte register.ts dosyası kullanıldı. | 2:04 | hooks/register.ts (karede: Klasör yapısında hooks/register.ts dosyası ve hooks.json görünüyor.) |
| Git | yok | CLI | yok | Mod örneğinde Claude'un çalıştırmaya çalıştığı git push komutunun yeniden yazıldığı sürüm kontrol aracı. | 3:12 | git push origin HEAD:fix-branch (karede: Kod örneğinde 'git push origin HEAD:fix-branch' komutu yazıyor.) |
| qwen2.5:7b-instruct | yok | teknik | yok | local-lab çubuğunda Mac üzerinde çalışan yerel model olarak gösteriliyor. | 7:02 | mac qwen2.5:7b-instruct +7 6ms · kanıt: kare (karede: Alt çubukta 'lab mac qwen2.5:7b-instruct' ve spark-1/spark-2 offline ibareleri görünüyor.) |
| ep-mods | yok | plugin | yok | Videoda kullanılan yerel mod marketplace'i (mods/.claude-plugin/marketplace.json); local-lab ve house-rules buradan kuruldu. | 6:34 | claude plugin install local-lab@ep-mods --scope user (karede: Terminalde 'claude plugin install local-lab@ep-mods --scope user' komutu yazılı.) |
| token-weather | yok | plugin | https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/token-weather | Addy Osmani'nin 'Token Weather' örneği; Claude'un araştırma yanıtında adı geçiyor. | 7:50 | Addy Osmani's Token Weather example (karede: Terminal yanıtında 'Addy Osmani's Token Weather example' ifadesi yazıyor.) |
| Kişisel geçmişten kullanışlı mod fikirleri üretmek | yok | prompt | yok | Claude'dan docs kılavuzunu okuyup son 20 oturumu incelemesi, sürekli sorulan şeyleri, tedirgin eden komutları ve değişiklik kontrolünü bulması; her fikre ad, tam sözler ve gösterilecek satırlar vermesi, yardım derecesine göre sıralaması; ben seçene kadar bir şey kurmaması. | 7:42 | kaynak: kare |
| Bağlam göstergesi modu yazdırmak | yok | prompt | yok | context-weather adında, bağlam penceresinin doluluğunu prompt üstünde gösteren bir Claude Code modu yazması. | 7:34 | kaynak: kare |
| first-mod araç sayacını denemek | yok | prompt | yok | research dosyalarını okuyup üç madde özetlemesi ve cevabı 'banana' kelimesinin tersiyle bitirmesi. | 5:50 | kaynak: kare |
| house-rules koruma modunu denemek | yok | prompt | yok | scratch-build klasörünü rm -rf ile silmesi, silindiğini doğrulaması ve cevabı 'peach' kelimesinin tersiyle bitirmesi. | 7:04 | kaynak: kare |
| secret-redactor modunu denemek | yok | prompt | yok | .env dosyasını Bash ile yazdırıp değişkenlerin tam değerini söylemesi, 'lemon' tersiyle bitirmesi. | 9:22 | kaynak: kare |
## Açıklama bağlantıları
- https://x.com/Voxyz_ai/status/2105778540251644176 — X gönderisi, muhtemelen mod fikri prompt'unun kaynağı. · aday: hayır · Referans gönderisi; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://code.claude.com/docs/en/plugins/mods — Claude Code mod dokümantasyonu. · aday: evet (Claude Code) · Alan adı Claude Code'u adlandırıyor; videoda gösteriliyor. · sınıf: diğer
- https://claude.dev/blog/getting-started-with-claude-code-mods — Modlara başlangıç blog yazısı; prompt'ta okutuluyor. · aday: hayır · Blog yazısı, referans sayfa. · sınıf: diğer
- https://x.com/lydiahallie/status/2106127556491821499 — X gönderisi. · aday: hayır · Referans gönderisi. · sınıf: diğer
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md — Claude Code değişiklik günlüğü. · aday: evet (Claude Code) · Claude Code deposu; adı videoda geçiyor. · sınıf: diğer
- https://github.com/deepseek-ai/deepseek-harness — DeepSeek Harness deposu. · aday: evet (DeepSeek Harness) · Videoda anlatılan DeepSeek Harness'in deposu. · sınıf: diğer
- https://engineerprompt.ai/ — Kanal sahibinin sitesi. · aday: hayır · Yazarın tanıtım sayfası. · sınıf: diğer
- https://prompt-s-site.thinkific.com/courses/rag — RAG kursu. · aday: hayır · Kendi kursunun reklamı; videoda kullanılmıyor. · sınıf: diğer · erişilemez: ücretli kurs, giriş gerekli
- https://tally.so/r/3y9bb0 — Bülten kayıt formu. · aday: hayır · Bülten kaydı; konu dışı. · sınıf: diğer
- whryte.com — Yapımcının kendi ses-metin uygulaması (açıklamada 'My voice to text App'). · aday: hayır · Yapımcının kendi ürününün tanıtımı; videoda kullanılmıyor. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude --plugin-dir ./my-mod | Modu içeren klasörü yükler; kaydedince yeniden yükler. (karede: Terminal kutusunda 'claude --plu...' yazılıyor.) | 2:08 | kare |
| claude plugin validate ./mods/first-mod | Modun manifestini ve hook çağrılarını doğrular. (karede: 'Validation passed' çıktısı.) | 5:36 | kare |
| claude --plugin-dir ./mods/first-mod --strict-mcp-config | first-mod'u yükleyerek Claude'u başlatır. (karede: OCR satırı bu komutu gösteriyor.) | 6:10 | kare |
| cat mods/.claude-plugin/marketplace.json | Pazar yeri JSON dosyasını gösterir. (karede: Terminalde marketplace.json içeriği.) | 6:20 | kare |
| claude plugin marketplace list | Yapılandırılmış pazar yerlerini listeler. (karede: Pazar yerleri listesi ve ep-mods.) | 6:26 | kare |
| claude plugin install local-lab@ep-mods --scope user | local-lab modunu kullanıcı kapsamında kurar. (karede: 'Successfully installed plugin: local-lab@ep-mods'.) | 6:34 | kare |
| claude plugin install house-rules@ep-mods --scope user | house-rules modunu kurar. (karede: Kutuda iki numaralı komut.) | 6:40 | kare |
| claude --plugin-dir ../mods/house-rules | house-rules modunu demo projede yükler. (karede: Terminalde demo-project içinde yazılıyor.) | 6:52 | kare |
| claude plugin validate ./mods/local-lab | Modun olay ve çağrılarını listeler. (karede: Çıktıda $.http.fetch ve $.state.get çağrıları.) | 9:02 | kare |
| /plugin | Eklenti yöneticisini açar. (karede: Plugins sekmesi.) | 5:28 | kare |
| /tally | Araç çağrısı sayısını gösterir. (karede: 'first-mod: Claude has made 3 tool calls'.) | 5:56 | kare |
| /lab | Yerel model sunucu durumunu gösterir. (karede: 'local-lab: mac: 8 model(s)'.) | 6:50 | kare |
| /rules | house-rules kurallarını gösterir. (karede: 'house-rules: Active house rules'.) | 7:20 | kare |
| /runs | run-radar panelini açar. (karede: 'run-radar: Run Radar opened.') | 8:30 | kare |
| /shelf | proof-shelf panelini açar. (karede: 'proof-shelf: Proof Shelf opened.') | 8:46 | kare |
| claude update | Claude Code'u günceller (yorumda öneriliyor). | açıklama | açıklama |
| claude --resume b3654a8a-766e-4fe1-895e-89e6f41c45ed | Önceki oturumu kaldığı yerden devam ettirir. (karede: Terminalde komut yazılı.) | 6:10 | kare |
| claude plugin marketplace add --claudeai claudeai-my-uploads | claude.ai yüklemelerini marketplace olarak eklemek için ekrandaki ipucu. (karede: 'Add: claude plugin marketplace add --claudeai claudeai-my-uploads' satırı görünüyor.) | 6:26 | kare |
| /plugin configure house-rules@ep-mods | house-rules için kullanıcı yapılandırmasını ayarlar (ekrandaki uyarı önerisi). (karede: Uyarı: 'run /plugin configure house-rules@ep-mods in Claude Code'.) | 6:32 | kare |
| /plugin configure local-lab@ep-mods | local-lab için kullanıcı yapılandırmasını ayarlar (ekrandaki uyarı önerisi). (karede: Uyarı: 'run /plugin configure local-lab@ep-mods in Claude Code'.) | 6:32 | kare |
| cd demo-project && ls | Demo klasörüne geçip içeriği listeler. (karede: Terminalde 'cd demo-project && ls' ve çıktı (README.md, scratch-build).) | 7:00 | kare |
| rm -rf scratch-build | Demo'da house-rules'ın durdurduğu silme komutu; onay sorusu çıkar. (karede: Onay ekranında 'house-rules: this command looks destructive. Run it?' ve rm -rf komutu görünüyor.) | 7:06 | kare |
| cat <dosya>; echo "=====DSH====="; cat <dosya> | Claude'un araştırma dosyalarını okuduğu kabuk komutu. (karede: Bash çıktısında 'cat [yol] echo "=====DSH====="; cat' satırı.) | 5:50 | kare |
| npx @deepseek-ai/dsh web | DeepSeek Harness web arayüzünü başlatır (port numarası OCR'da net değil). (karede: Okunan araştırma metninde 'run it with npx @deepseek-ai/dsh web' ifadesi.) | 5:54 | kare |
| git push origin HEAD:fix-branch | Örnekte force push yerine yönlendirilen komut. (karede: Kod örneğinde 'git push origin HEAD:fix-branch' yazılı.) | 3:12 | kare |
| git push --force | Örnekte engellenen/yeniden yazılan force push komutu. (karede: Kod örneğinde 'git push --force' yazılı.) | 3:24 | kare |
| cat .env | Demo'da ortam değişkenlerini okuma denemesi; secret-redactor çıktıyı gizledi (değerler yazılmadı). (karede: Prompt'ta 'Run cat .env with the Bash tool...' yazıyor; çıktı gizlenmiş.) | 9:20 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Mod Claude Code'un içinde yaşar; skills, hooks ve MCP dışarıda yaşar. | 0:00 | karşılaştırma |
| Mod tool çağrısını gözlemleyebilir, yeniden yazabilir ya da kendisi yanıtlayabilir. | 2:40 | özellik |
| Mod e-postaları ekranda gizler, model gerçek adresi görmeye devam eder. | 3:40 | özellik |
| Hook bir kabuk betiğidir, bir kez çalışır; mod oturum boyunca yüklü kalır ve durum tutar. | 3:54 | karşılaştırma |
| Diff görünümü ve AGENTS.md desteği zaten mod olarak yazılmış; daha fazlası taşınacak. | 4:30 | özellik |
| Mod yeniden yüklenince sayaç sıfırlanır; kalıcı veri Claude Code'da saklanmalı. | 6:00 | özellik |
| Mod kullanıcı izinleriyle çalışır: dosya okur, program çalıştırır, ağı kullanır. | 8:56 | özellik |
| Modlar v2.1.287 ile geldi. | 0:04 | sayısal |
| Yakında mod pazar yerleri ve ardından kötü niyetli ilk mod ortaya çıkacak. | 9:55 | öneri |
| Mod; ekranda bir şey, hafıza ya da durdurup sorma gerektiğinde kullanılmalı; basit engelleme için hook yeter. | 9:30 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code mod özelliği | Claude Mods | 'mods in cloud code' |
| konuşma 0:55 | DeepSeek Harness | DeepSeek Harness | 'When Deepseek released their harness' |
| konuşma 3:54 | Hooks | hooks | 'a hook is a shell script' |
| konuşma 0:00 | Skills | Skills | 'things like scales, hooks and MCP servers' |
| konuşma 0:00 | MCP servers | MCP servers | MCP sunucuları dışarıda yaşar |
| konuşma 3:20 | PII gizleme | hide-email | Yanıtlarda e-posta gizleme |
| kare 4:36 | cc-plugin-diff | cc-plugin-diff | Karede etiket |
| kare 4:40 | cc-plugin-agents-md | cc-plugin-agents-md | Karede etiket |
| kare 5:28 | cc-plugin-plugin-authoring | cc-plugin-plugin-authoring | Installed listesi |
| kare 5:28 | cc-plugin-telemetry | aday değil: konu dışı | Yalnız listede görünüyor |
| kare 5:22 | frontend-design, Superpowers, code-review, context7, skill-creator | aday değil: konu dışı | Discover listesinde, kullanılmıyor |
| kare 5:36 | first-mod | first-mod | 3 files · 31 lines |
| kare 5:14 | Opus 5.5 | Opus 5.5 | Başlık satırı |
| kare 6:22 | local-lab | local-lab | marketplace.json ve kurulum |
| kare 6:22 | house-rules | house-rules | Guard demosu |
| kare 6:22 | context-weather | context-weather | Gösterge |
| kare 9:22 | secret-redactor | secret-redactor | Redakte çıktısı |
| kare 8:50 | run-radar, proof-shelf, public-hold | run-radar | Panel demosu; proof-shelf ve public-hold ayrı satırlarda adaylarda |
| kare 8:50 | script-desk, keep-alive, api-wallet, background-it | script-desk | Kareler mod fikri etiketleri; diğer üçü adaylarda ayrı |
| kare 5:50 | npx @deepseek-ai/dsh web | DeepSeek Harness | Yanıt metninde başlatma komutu |
| kare 5:22 | openai-codex, last30days, claude-in-chrome | aday değil: konu dışı | Yalnız eklenti listesinde |
| kare 6:26 | data-agent-kit-starter-pack | aday değil: konu dışı | Pazar yeri listesinde |
| kare 7:52 | aitmpl.com / claude-code-templates | aday değil: konu dışı | Yalnız araştırma dosyası özetinde |
| kare 9:02 | claude plugin validate | claude plugin validate | Doğrulama çıktısı |
| kare 2:08 | --plugin-dir | --plugin-dir | Komut |
| kare 6:26 | claude plugin marketplace | claude plugin marketplace | list çıktısı |
| kare 6:34 | claude plugin install | claude plugin install | Kurulum komutu |
| açıklama | whryte.com | whryte | Sesten metne uygulama tanıtımı |
| açıklama | RAG kursu ve bülten | aday değil: sponsor/reklam | Kendi kurs ve bülten bağlantıları |
| açıklama | X gönderileri | aday değil: konu dışı | Referans gönderileri |
| açıklama | Claude Code CHANGELOG | Claude Code | Claude Code deposu |
| yorum | Obsidian, LangChain, pi, hyperframes | aday değil: konu dışı | Yalnız izleyici yorumlarında |
| yorum | Claude Opus 5.5 ve Fable 5.1 | aday değil: konu dışı | Yorumda model eleştirisi |
| yorum | claude update | Claude Code | Yorumda güncelleme önerisi |
| linkli sayfa | Plugin dokümantasyon sayfaları | Claude Code | code.claude.com altındaki sayfalar |
| linkli sayfa | token-weather, blast-radius, replay-theater örnek modları | aday değil: konu dışı | Yalnız playground deposunda; videoda gösterilmiyor |
| linkli sayfa | localGPT, whryte.com, YouTube kanalı | aday değil: sponsor/reklam | engineerprompt.ai sayfasından yönlendirme |
| kare 8:56 | Claude Code docs güvenlik sayfası | Claude Code | 'What a mod can reach' sayfası |
| kare 3:06 | await next(e) | Claude Mods | Mod işlevinin next çağrısı |
| kare 7:18 | Docker, Gemini | aday değil: konu dışı | Yalnız kural metninde (docker rm -f, Gemini 3.8) geçiyor |
| kare 5:54 | npm | aday değil: konu dışı | Yalnız yanıt metninde npx komutu |
| kare 0:02 | VSCode | aday değil: konu dışı | Changelog satırında geçiyor |
## Kareden okunanlar
- 0:04: Changelog: 'Added Claude Mods'; sürüm 2.1.287, 1 Ekim 2026.
- 3:08: git push --force için observe/rewrite/answer; rewrite: 'git push origin HEAD:fix-branch'.
- 5:14: Claude Code v2.1.287, Opus 5.5 (1M context), high effort, Claude Max.
- 6:22: marketplace.json: ep-mods; first-mod, local-lab, house-rules, context-weather.
- 7:18: Korunan kalıplar: rm -rf, git push --force, git reset --hard, docker rm -f, DROP TABLE.
- 7:48: Gösterge %11, 111.2k / 1M; 'Enable hot reloading for this session?' istemi.
- 9:50: Tabloda block with a script→hooks; follow instructions→skills; mods için soru işareti.
## Belirsizlikler
- Sesteki 'cloud code', 'Enthropic' ifadeleri Claude Code ve Anthropic olarak okundu.
- 'DJX Sparks' ifadesi büyük olasılıkla NVIDIA DGX Spark; ekranda 'spark-1/spark-2' yazıyor.
- Sözlükteki Three.js, Hermes Agent, Typefully, Notion gibi eşleşmeler bulanık ses eşleşmesi; videoda kullanıldığına dair kanıt yok.
- Docs listesindeki cc-plugin-sec-default ve cc-plugin-telemetry yalnız menüde görünüyor; kullanılmıyor.
- Yerleşik listede codex, last30days, claude-in-chrome, frontend-design gibi eklentiler yalnız menüde görünüyor, kullanılmıyor.
- Yorumdaki 'hyperframes + custom skills' sunum araçları olarak belirtilmiş ama videoda gösterilmiyor.
- Yorumdaki Obsidian ve LangChain deepagents anılması kullanıcı yorumu; videoda kullanılmıyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/15 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| example.com | 3:36 | ekran | hayır |
| check.sh | 3:58 | ekran | hayır |
| claude.ai | 5:28 | ekran | hayır |
| https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack.git | 6:26 | ekran | hayır |
| aitmpl.com | 7:52 | ekran | hayır |
| claude.dev/blog/getting-started-with-claude-code-mods | 8:00 | ekran | hayır |
| db.example.com | 9:22 | ekran | hayır |
| https://clau.de/yourthoughts | 6:50 | ekran | hayır |
| https://x.com/Voxyz_ai/status/2105778540251644176 | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/plugins/mods | açıklama | açıklama | evet |
| https://claude.dev/blog/getting-started-with-claude-code-mods | açıklama | açıklama | hayır |
| https://x.com/lydiahallie/status/2106127556491821499 | açıklama | açıklama | hayır |
| https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | açıklama | açıklama | evet |
| https://github.com/deepseek-ai/deepseek-harness | açıklama | açıklama | evet |
| https://engineerprompt.ai/ | açıklama | açıklama | hayır |
| https://prompt-s-site.thinkific.com/courses/rag | açıklama | açıklama | hayır |
| https://tally.so/r/3y9bb0 | açıklama | açıklama | hayır |
| whryte.com | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Claude Code sürümünü güncelleyip modların açık olduğunu kontrol etme — araçlar: Claude Code, claude update
- 2. adım — /plugin menüsünde yerleşik modları ve skill'i inceleme — araçlar: /plugin, cc-plugin-plugin-authoring
- 3. adım — first-mod modunu validate ile doğrulama — araçlar: claude plugin validate, first-mod
- 4. adım — first-mod'u --plugin-dir ile yükleyip dosya okutma — araçlar: --plugin-dir, Claude Code, Opus 5.5
- 5. adım — Araç sayacını /tally ile görme ve yeniden yüklemede sıfırlanmasını gözleme — araçlar: first-mod, /tally
- 6. adım — marketplace.json'u okuyup pazar yerlerini listeleme — araçlar: claude plugin marketplace
- 7. adım — local-lab ve house-rules modlarını kurma — araçlar: claude plugin install, local-lab, house-rules
- 8. adım — /lab ile yerel model durumunu gösterme — araçlar: local-lab
- 9. adım — rm -rf komutunu house-rules ile durdurma ve reddetme — araçlar: house-rules, Claude Code
- 10. adım — context-weather göstergesini Claude'a yazdırıp etkinleştirme — araçlar: Claude Code, cc-plugin-plugin-authoring, context-weather
- 11. adım — Son 20 oturumdan mod fikri çıkaran prompt'u çalıştırma — araçlar: Claude Code
- 12. adım — Seçilen fikirlerden modları Claude'a yazdırıp panelleri gösterme — araçlar: run-radar, proof-shelf, public-hold
- 13. adım — Mod güvenliği için claude plugin validate ile olayları inceleme — araçlar: claude plugin validate, local-lab
- 14. adım — secret-redactor ile .env sızıntısı testi — araçlar: secret-redactor
## Promptlar
- Kişisel geçmişten kullanışlı mod fikirleri üretmek — Claude'dan docs kılavuzunu okuyup son 20 oturumu incelemesi, sürekli sorulan şeyleri, tedirgin eden komutları ve değişiklik kontrolünü bulması; her fikre ad, tam sözler ve gösterilecek satırlar vermesi, yardım derecesine göre sıralaması; ben seçene kadar bir şey kurmaması.
- Bağlam göstergesi modu yazdırmak — context-weather adında, bağlam penceresinin doluluğunu prompt üstünde gösteren bir Claude Code modu yazması.
- first-mod araç sayacını denemek — research dosyalarını okuyup üç madde özetlemesi ve cevabı 'banana' kelimesinin tersiyle bitirmesi.
- house-rules koruma modunu denemek — scratch-build klasörünü rm -rf ile silmesi, silindiğini doğrulaması ve cevabı 'peach' kelimesinin tersiyle bitirmesi.
- secret-redactor modunu denemek — .env dosyasını Bash ile yazdırıp değişkenlerin tam değerini söylemesi, 'lemon' tersiyle bitirmesi.
