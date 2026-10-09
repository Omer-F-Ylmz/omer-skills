# Claude Code'un Tasarım Sorununu Çözen Skill Güncellendi (Impeccable 4.0)
## Künye
Claude Code'un Tasarım Sorununu Çözen Skill Güncellendi (Impeccable 4.0) · Mert Durmazer | Digital Academy · süre: 15:20 · tr-orig · https://youtu.be/hvfflSAIDaE · şema 2
motor: parti 2026-10-09-uzun-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 225944 tk
## Özet
Mert Durmazer, açık kaynak Impeccable skill'inin 4.0 güncellemesini tanıtıyor. Skill, Claude Code'a yapay zekâ kaynaklı tasarım kalıplarını (mor gradyan, hep aynı fontlar, kart içinde kart) tespit ettirip daha iyi kararlarla değiştirtiyor. Video; kurulum (npx impeccable install, skill kurulumu, Node sürümü), Higgsfield MCP ile Recraft V4.1 üzerinden görsel üretimi bağlama, /impeccable init ile ürün bağlamı, Worlds (topluluk tasarım dünyaları) seçimi, bir landing/kanıt sayfası üretimi ve Live mode ile tarayıcıda seçili öğeye üç varyant üretip kabul etmeyi gösteriyor. Videoda ayrıca 'Pathfinder' ve 'onboarding aktivasyon' tarzı iki farklı dünya sonucu ve Impeccable'ın web sitesi/README ekranları gösteriliyor.
## Bölümler
- 0:00 Giriş: AI kaynaklı web tasarımının sorunu ve Impeccable'ın amacı
- 1:01 Impeccable ne yapıyor: kötü tasarım kalıplarını silme, GitHub ve site incelemesi
- 2:03 Yeni modlar: Live mode ve Worlds
- 3:03 Komut grupları ve Node sürüm gereksinimi
- 4:06 Kurulum: npx impeccable install ve skill kurulumu
- 5:06 İsteğe bağlı görsel üretim katmanı: Higgsfield MCP bağlantısı
- 6:07 /impeccable init: proje mülakatı, güncelleme ve dünya seçimi
- 8:10 Dünya ve kompozisyon seçimi, Recraft V4.1 ile reroll
- 10:13 Build: sayfanın üretilmesi
- 11:14 Live mode: tarayıcıda seçim, yorum ve varyant kabul
- 13:16 Ajan iş akışına yerleştirme ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Impeccable | yok | skill | https://github.com/pbakaus/impeccable | Claude Code gibi ajanlara yüklenen açık kaynak tasarım skill'i; 23 komut, canlı tarayıcı düzenleme ve 59 deterministik kural içeriyor. | 1:01 | Impecable'ın yaptığı şey şu... kötü tasarımları yok etmek. |
| Impeccable CLI | yok | CLI | https://www.npmjs.com/package/impeccable | npm paketi; skill kurulumu (npx impeccable install / skills install), detect ile kural taraması ve update komutlarını sağlar. | 4:10 | npx impeccable skills install çıktısı: Installed impeccable into .claude, .agents (karede: Terminalde 'npx impeccable skills install' komutu çalışıyor; Claude Code ve Codex harness'ları algılanıyor, kurulum tamamlanıyor.) |
| Claude Code | yok | CLI | yok | Terminal tabanlı yapay zekâ kodlama ajanı; Impeccable skill'i, MCP bağlantıları ve tüm tasarım akışı bu ajanın içinde çalışıyor. | açıklama | Claude Code'a bir arayüz yaptırdığında sonucun yapay zeka ürünü olduğu anında belli oluyor |
| Claude Opus 5 | yok | teknik | yok | Claude Code oturumunda ajanı çalıştıran ana model (1M bağlam, yüksek efor); durum çubuğunda görünüyor. | 4:32 | Opus 5 (1M context) with high effort · Claude Max (karede: Terminal alt çubuğunda 'Opus 5 (1M context)' modeli ve Claude Max planı görünüyor.) |
| Codex | yok | CLI | yok | OpenAI kodlama ajanı; Impeccable'ın desteklediği harness'lardan biri olarak anlatılıyor, skill'i Codex tarafına da kurulabiliyor. | 14:18 | İsterseniz Codex kullanırsınız. Codex'e de yaptırır. |
| Cursor | yok | teknik | yok | Yapay zekâ destekli kod editörü; açıklamada Impeccable'ın desteklediği ajanlar arasında sayılıyor, video içinde kurulumu yapılmadı. | açıklama | Claude Code'un yanı sıra Cursor, Codex ve Gemini CLI ile de çalışıyor |
| Gemini CLI | yok | CLI | yok | Google'ın komut satırı yapay zekâ ajanı; açıklamada Impeccable'ın desteklediği ajanlar arasında yer alıyor, video içinde kullanılmadı. | açıklama | Claude Code'un yanı sıra Cursor, Codex ve Gemini CLI ile de çalışıyor |
| Higgsfield MCP | yok | MCP | https://mcp.higgsfield.ai/mcp | Higgsfield görsel üretim platformunun MCP sunucusu; Claude Code'a OAuth ile bağlanıp görsel üretim araçlarını (generate_image_batch) kullandırıyor. | 5:48 | claude mcp list → higgsfield: https://mcp.higgsfield.ai/mcp (HTTP) - Connected (karede: Terminal raporunda 'higgsfield: https://mcp.higgsfield.ai/mcp (HTTP) - Connected' satırı; kimlik doğrulama OAuth ile yapılmış.) |
| Higgsfield | yok | MCP | higgsfield.ai | Görsel üretim modellerine erişim sağlayan platform; MCP üzerinden Recraft V4.1 gibi modellere bağlanılıyor. Narasyonda 'Hickfield' olarak geçiyor. | 5:06 | Burada Hickfield'ı vereceğim ama isterseniz |
| Recraft V4.1 | yok | teknik | yok | Görsel üretim modeli; utility modunda açık hex paleti ve arka plan alarak üç kompozisyonun görsellerini üretiyor. | 8:52 | Model chosen: Recraft V4.1 in utility mode - it takes an explicit hex palette (karede: Ajan çıktısında 'Model chosen: Recraft V4.1 in utility mode' yazıyor; higgsfield generate_image_batch çağrısı görülüyor.) |
| Impeccable Live | yok | skill | https://impeccable.style/docs/live | Impeccable'ın tarayıcıda canlı düzenleme modu; seçilen öğeye yorum, çizgi ya da aksiyon verilip üç varyant üretiliyor ve kabul edilince kaynağa yazılıyor. | 10:13 | Impackable live diyeceğiz ve canlı mod başlayacak |
| Impeccable Worlds | yok | skill | https://impeccable.style/live-mode | Topluluk ve insan incelemesinden geçmiş tasarım dünyaları; kullanıcı dünya seçiyor, ajan o dünyadan kompozisyon üretip uyguluyor. | 2:03 | Worlds dedikleri aslında tasarım dünyaları var topluluk tarafından üretilen · kanıt: yok |
| npm | yok | teknik | yok | Node paket yöneticisi; npm i impeccable ile Impeccable CLI paketi kuruluyor. | 3:50 | > npm i impeccable (karede: Impeccable'ın npm sayfasında 'npm i impeccable' komutu ve Quick Start bölümü görünüyor.) |
| Node.js | yok | teknik | yok | Impeccable'ın gerektirdiği çalışma zamanı; video sırasında sürüm kontrol edilip güncelleme gerektiği konuşuluyor. | 3:03 | Bu araç belirli bir not sürümünün üstünde olmasını istiyor |
| Azeret Mono | yok | teknik | yok | Ajanın ürettiği sayfada rakam ve etiketler için kullanılan monospace yazı tipi. | 11:20 | outline numerals over Azeret Mono · kanıt: kare (karede: Ajan mesajında varyant açıklaması; üretilen sayfanın rakamları ve etiketleri mono yazı tipiyle tanımlanıyor.) |
| Instrument Serif | yok | teknik | yok | Bir dünya brief'inde ('Instrument Serif') geçen serif yazı tipi; gösterilen başka bir dünyanın tipografi tarifinde yer alıyor. | 7:04 | Instrument Serif (dünya brief'i) (karede: Dünya brief'inde 'Instrument Serif' yazı tipi adı ve tipografi tarifi görünüyor.) |
| WebGL | yok | teknik | yok | Tarayıcıda GPU ile 3B/gölgelendirici grafik; dünya brief'inde 'webgl tracking-tear shader' olarak geçiyor. | 7:00 | a webgl tracking-tear shader, canvas noise banding (karede: Dünya brief'inde 'WEB LEVERAGE' satırında WebGL gölgelendirici tarifi görünüyor.) |
| GLSL | yok | teknik | yok | WebGL gölgelendiricilerinin yazıldığı gölgelendirici dili; dünya brief'inde anılıyor. | 7:00 | GLSL (dünya brief'i) (karede: Dünya brief'inde 'WEB LEVERAGE' satırında GLSL ifadesi görünüyor.) |
| Kie.ai | yok | teknik | yok | Görsel üretim modellerine API ile bağlanılabilen servis; narasyonda 'KY AI FI' olarak anılıyor, yorumda 'kie.ai' geçiyor. | 5:06 | isterseniz KY AI FI herhangi bir noktadan da bağlantı verebilirsiniz |
| Impeccable skill'inin Claude Code'a kurulması | yok | prompt | yok | Impeccable tasarım skill'ini kur; repo'daki kurulum talimatlarını oku ve çalıştır (Türkçe özet). | 4:42 | kaynak: kare |
| Güvenli kurulum ve sürüm kontrolü | yok | prompt | yok | Kurulumdan önce Node sürümünü kontrol et; yetersizse dur ve yükseltme önerisi ver, mevcut skill ve ayarları değiştirme; yapılan her değişikliği listele (Türkçe özet). | 4:56 | kaynak: kare |
| Görsel üretim MCP bağlantısı | yok | prompt | yok | Higgsfield MCP sunucusunu bu projeye bağla; kurulumu adım adım yürüt, gizli anahtarı ekrana yazdırma, sır gerekiyorsa beni durdur; bittiğinde /mcp ile yalnız bağlantının var olduğunu göster, veri çekme (Türkçe özet). | 5:08 | kaynak: kare |
| Higgsfield MCP kurulum talebi | yok | prompt | yok | Higgsfield MCP sunucusunu Claude Code projesine bağla; kurulum talimatları sitelerinde MCP ve CLI bölümünde (Türkçe özet). | 6:13 | kaynak: kare |
| Init sorularına yanıt ve içerik kuralları | yok | prompt | yok | Güncellemeyi yap; gerçek varlık ve sayı yok, tüm içeriği uydur ama bunların gerçek iddia olmadığı açıkça görünsün; Higgsfield MCP'yi kullan (Türkçe özet). | 6:36 | kaynak: kare |
| Landing page için init mülakatı yanıtı | yok | prompt | yok | Landing page yap; stack'i sen seç, içeriği sen uydur (Türkçe özet). | 7:08 | kaynak: altyazı |
| Live mode'da seçili öğe için düzenleme | yok | prompt | yok | Canlı modda seçili sonuç hücresinin çizgilerini daha kalın yap (Türkçe özet). | 10:58 | kaynak: kare |
| Dünya seçiminde reroll yönlendirmesi | yok | prompt | yok | Yeniden üretimde tasarım dili ve kompozisyonu özgün tasarıma daha yakın tut (Türkçe özet). | 9:32 | kaynak: kare |
| Mevcut sayfayı cilalama (demo) | yok | prompt | yok | Sadece pricing sayfasını cilala; keskin köşeleri ve sakin paletiyi koru, AI izlerini kaldır (Türkçe özet). | 0:02 | kaynak: kare |
## Açıklama bağlantıları
- https://www.skool.com/otomasyon — Digital Academy / Otomasyon topluluk sayfası (ücretli topluluk). · aday: hayır · Topluluk ve eğitim sayfası; izleyicinin kullanacağı bir araç değil. · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- https://digitalacademy.com.tr/claude-code-egitim.html — Digital Academy Claude Code eğitim sayfası. · aday: hayır · Eğitim satış/tanıtım sayfası; araç değil. · sınıf: diğer
- https://impeccable.style — Impeccable'ın resmi sitesi ve dokümantasyonu. · aday: evet (Impeccable) · Impeccable aracının resmi sitesi; kurulum ve komut dokümanı içeriyor. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kılavuz çizgili kağıt arka planı (ruled-line background) | Kağıt defter zemini ve kılavuz çizgileri (karede: Sayfa, ince yatay kılavuz çizgileriyle kağıt defter görünümünde; içerik bu zemin üzerinde hizalanmış.) | 10:12 | kare |
| Çift sütunlu düzen (two-column layout) ve dikey kenar çizgisi (vertical rule) | Sol kenarda ince dikey kenar sütunu; kayıt künyesi bu sütunda (karede: Sayfanın sol kenarında dar bir sütun ve ince dikey çizgi; ana içerik sağda.) | 10:12 | kare |
| Üstü çizili düzeltme (strikethrough) ve satır içi düzeltme | Önceki değer üstü çizili, düzeltilmiş değer altta yazılıyor (karede: Başlıkta bir değerin üzerinden çizgi geçiyor, düzeltilmiş değer hemen altında yazılıyor.) | 9:40 | kare |
| Kutu ve ok diyagramı (box-and-arrow flow diagram) | Kohort ayrımı için kutulu akış diyagramı (karede: Sağ üstte 'CONTROL' ve 'VARIANT' kutuları oklarla 'ACTIVATED' kutusuna bağlanıyor.) | 10:12 | kare |
| Damga etiketi (stamp badge) ve kırmızı kenarlıklı rozet | Yetersiz veri durumunu gösteren kırmızı damga (karede: Sayfanın ortasında kırmızı çerçeveli 'INSUFFICIENT' etiketi görünüyor.) | 10:12 | kare |
| Onay işaretli kontrol listesi (checklist) | Doğrulama maddeleri onay işaretiyle listeleniyor (karede: Sağ altta 'Checks' başlığı altında ✓ işaretli satırlar.) | 10:12 | kare |
| Varyant geçişi (variant cycling) ile kare kontrol | Tek bir sonuç hücresi üç varyant arasında döngüyle değiştiriliyor (karede: Sonuç hücresinde üç varyantın sırayla gösterilebildiği ajan mesajında belirtiliyor.) | 11:20 | kare |
| Yüzen aksiyon menüsü (floating action menu) ve araç çubuğu | Seçili öğe için yüzen aksiyon menüsü (bolder, quieter, typeset, colorize, adapt vb.) (karede: Seçili kart üzerinde 'Freeform, Bolder, Quieter, Distill, Polish, Typeset, Colorize, Adapt, Animate' seçenekleri.) | 13:36 | kare |
| Sıfır köşe yarıçapı (zero border-radius) ve düz tasarım | Sayfada sıfır köşe yarıçapı ve düz yüzeyler (karede: Kartlar ve kutular keskin köşeli, yuvarlatma yok.) | 10:12 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx impeccable install | Impeccable skill'ini proje köküne kurar; ardından Claude Code içinde /impeccable init çalıştırılır. | açıklama | açıklama |
| npx impeccable skills install | Skill'i algılanan harness'lara (Claude Code, Codex) kurar ve tasarım hook'unu sorar. (karede: Terminalde komut çalışıyor; Claude ve Codex harness'ları algılanıyor, 'Installed impeccable into .claude, .agents' yazıyor.) | 4:10 | kare |
| npm i impeccable | Impeccable npm paketini yükler (CLI ve tarama araçları). (karede: Impeccable npm sayfasında Install kutusunda 'npm i impeccable' görünüyor.) | 3:50 | kare |
| npx impeccable detect https://example.com | Canlı URL'yi Puppeteer ile açıp tasarım kalıplarını tarar. (karede: README'de 'Scan a live URL (requires Puppeteer)' başlığı altında komut görünüyor.) | 4:02 | kare |
| npx impeccable detect src/ | Kaynak dosyalarda (HTML, CSS, JSX, TSX, Vue, Svelte) 59 deterministik kuralla tarama yapar. (karede: npm sayfasının Quick Start bölümünde 'Scan files or directories for anti-patterns' komutu görünüyor.) | 3:50 | kare |
| npx impeccable skills install -y --providers=claude,codex --scope=project | Soru sormadan yalnız Claude ve Codex için proje kapsamında kurulum yapar. (karede: npm Quick Start bölümünde 'Non-interactive install for a specific scope' komutu görünüyor.) | 3:50 | kare |
| npx impeccable skills install --no-hooks | Hook manifestleri olmadan skill kurar veya günceller. (karede: npm Quick Start bölümünde 'Install or update skills without hook manifests' komutu görünüyor.) | 3:50 | kare |
| npx impeccable skills update | Skill'i en güncel sürüme yükseltir. (karede: npm Quick Start bölümünde 'Update skills to the latest version' komutu görünüyor.) | 3:50 | kare |
| npx impeccable skills link --source=.impeccable --providers=claude,cursor | Git submodule kopyasından skill'i harness'lara bağlar. (karede: npm Quick Start bölümünde 'Link skills from a Git submodule checkout' komutu görünüyor.) | 3:50 | kare |
| npx impeccable skills help | Tüm skill komutlarını listeler. (karede: npm Quick Start bölümünde 'List all available commands' komutu görünüyor.) | 3:50 | kare |
| npx -y impeccable@latest install -providers=claude,codex --scope=project --force | Ajanın yaptığı zorunlu yeniden kurulum; proje kapsamında Claude ve Codex için dosyaları yeniler. (karede: Claude Code bash çağrısında bu komut ve tail -30 çıktısı görünüyor.) | 5:36 | kare |
| npx impeccable update | Impeccable'ı günceller; mevcut oturumu değil sonraki oturumu etkiler ve eski global kopyayı da düzeltir. (karede: Init sırasında 'Runs npx impeccable update' açıklaması ve güncelleme uyarısı görünüyor.) | 6:28 | kare |
| cp -r dist/claude-code/.claude your-project/ | Repodaki Claude Code skill dosyalarını elle projeye kopyalar. (karede: README 'Option 5: Copy from Repository' bölümünde Claude Code için proje kopyalama komutu görünüyor.) | 1:04 | kare |
| node .claude/skills/impeccable/scripts/*.mjs --help | Kurulan skill betiklerinin çalıştığını yardım çıktısıyla doğrular. (karede: Claude Code doğrulama çağrısında bu komut ve '--help' çıktısı görünüyor.) | 5:46 | kare |
| claude mcp list | Claude Code'da kayıtlı MCP sunucularını ve bağlantı durumunu listeler. (karede: Rapor: 'claude mcp list → higgsfield: https://mcp.higgsfield.ai/mcp (HTTP) - Connected'.) | 5:48 | kare |
| /mcp | Claude Code sohbetinde MCP bağlantılarının varlığını gösterir (veri çekmez). (karede: Higgsfield promptunda 'run /mcp and show me only that the connection exists' isteği görünüyor.) | 5:08 | kare |
| /impeccable init | Proje bağlamını (PRODUCT.md, ardından DESIGN.md) kurup kullanıcıya mülakat sorar. (karede: Claude Code sohbetinde '/impeccable init' yazılı; soru akışı ve 'Running /impeccable init' görünüyor.) | 6:16 | kare |
| /impeccable hooks on/off | Tasarım hook'unu açar veya kapatır (UI dosyalarını düzenleme sonrası kontrol eder). (karede: Terminal çıktısında '/impeccable hooks on/off.' ifadesi görünüyor.) | 4:18 | kare |
| /impeccable live | Tarayıcıda canlı düzenleme modunu başlatır; seçim, yorum ve varyant akışını açar. | 10:13 | altyazı |
| /impeccable polish the pricing page. Keep our sharp corners and sober palette. | Mevcut pricing sayfasını cilalar, tasarım sistemini ve keskin köşeleri korur. (karede: Impeccable sitesinde sohbet komutu; ajan 'DESIGN.md loaded' ve '4 tells found' yanıtı veriyor.) | 0:02 | kare |
| /impeccable audit blog | Blog sayfalarını denetler ve bulguları listeler. (karede: Impeccable README kullanım örneklerinde '/impeccable audit blog' görünüyor.) | 1:04 | kare |
| /impeccable redo this hero section | Hero bölümünü baştan tasarlamasını ister. (karede: Impeccable sitesinde kullanım örneği olarak görünüyor.) | 1:04 | kare |
| /impeccable pin audit | Bir komutu bağımsız kısayol olarak (ör. /audit) oluşturur. (karede: 'Use /impeccable pin <command> to create standalone shortcuts (e.g., pin audit creates /audit)' metninde görünüyor.) | 1:04 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Impeccable kötü tasarım kalıplarını siler; iyi tasarım kararını kullanıcı verir. | 1:01 | özellik |
| Impeccable GitHub'da yaklaşık 59.000 yıldız aldı. | 1:01 | sayısal |
| Tek skill içinde 23'ten fazla komut bulunuyor (şekillendirme, cilalama, animasyon, tipografi vb.). | açıklama | sayısal |
| Live mode ile terminale dönmeden tarayıcıda seçili öğe düzenlenebiliyor. | 2:03 | özellik |
| Worlds topluluk tarafından üretilen tasarım dünyaları içerir ve kendi projeye aktarılabilir. | 2:03 | özellik |
| Impeccable belirli bir Node sürümünün üstünü gerektirir; eski sürümle araç bozuk çalışabilir. | 3:03 | öneri |
| Ajan, Live mode ile üç varyant üretip kabul edilen varyantı kaynak dosyaya yazıyor. | 11:14 | özellik |
| Bu iş akışıyla birbirinin kopyası olmayan, ajans müşterisi için değer üreten siteler yapılabilir. | 13:16 | öneri |
| Impeccable Claude Code dışında Cursor, Codex ve Gemini CLI ile de çalışıyor. | açıklama | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 1:01 | Impeccable (skill adı) | Impeccable | Impecable'ın yaptığı şey şu |
| altyazı 1:01 | GitHub sayfası ve 59.000 yıldız | Impeccable | Şu an 59.000 yıldızı var |
| kare 1:04 | Cursor kurulum notu ve Agent Skills | aday değil: genel kavram | Cursor skills require setup |
| kare 1:14 | Anthropic frontend-design (Claude için ilk tasarım skill'i) | aday değil: genel kavram | Anthropic's frontend-design was the first widely-used design skill |
| kare 1:02 | Mistral Vibe, Grok Build, Qoder, OpenCode, Pi harness kurulum listesi | aday değil: genel kavram | README'deki desteklenen harness listesi |
| kare 0:04 | Inter yazı tipi (kaçınılan font örneği) | aday değil: genel kavram | Don't use overused fonts (Arial, Inter, system defaults) |
| kare 1:22 | Astro ve Bun (repo commit'te göç) | aday değil: konu dışı | Migrate site from Bun to Astro |
| kare 5:56 | Twinmotion uygulaması (arka planda açık Epic Games) | aday değil: konu dışı | Twinmotion 2026.1 HF2 |
| kare 4:02 | Puppeteer (canlı URL tarama için gereksinim) | aday değil: genel kavram | Scan a live URL (requires Puppeteer) |
| kare 4:16 | Antigravity (algılanan harness) | aday değil: genel kavram | Antigravity |
| kare 4:10 | npx impeccable skills install komutu | Impeccable CLI | npx impeccable skills install |
| açıklama | npx impeccable install kurulum komutu | Impeccable CLI | Kurulum: npx impeccable install |
| kare 3:50 | npm i impeccable | npm | > npm i impeccable |
| kare 3:50 | npmjs.com sayfası (impeccable paketi) | Impeccable CLI | npmjs.com/package/impeccable |
| kare 3:50 | GitHub repo sayfası (pbakaus/impeccable) | Impeccable | github.com/pbakaus/impeccable |
| kare 3:50 | Vue, Svelte, TSX/JSX dosya tarama ifadesi | aday değil: genel kavram | TSX, Vue, and Svelte files for 59 deterministic rules |
| kare 4:30 | www.tek.org (tarayıcı yer imi) | aday değil: konu dışı | www.tek.org |
| kare 4:42 | Claude Code (ajan) kurulum promptu | Claude Code | Install the Impeccable design skill for me |
| kare 4:48 | GitHub API skill içeriği listeleme | aday değil: genel kavram | api.github.com/repos/pbakaus/impeccable/contents/skill |
| kare 4:56 | Node.js sürüm kontrolü | Node.js | node v25.8.1 (npm 11.11.0) |
| kare 4:32 | Opus 5 modeli durum çubuğunda | Claude Opus 5 | Opus 5 (1M context) with high effort |
| altyazı 3:03 | Impeccable komut grupları ve Node gereksinimi | Impeccable | Bu araç belirli bir not sürümünün üstünde |
| kare 5:02 | Higgsfield (skill klasörü ve MCP) | Higgsfield MCP | higgsfield-soul-id, higgsfield-video-explainer klasörleri |
| kare 5:08 | Higgsfield MCP kurulum promptu | Higgsfield MCP | Connect the Higgsfield MCP server to this Claude Code project |
| kare 5:48 | higgsfield.ai site | Higgsfield | higgsfield.ai · claude mcp list |
| kare 5:48 | https://mcp.higgsfield.ai/mcp MCP uç noktası | Higgsfield MCP | higgsfield: https://mcp.higgsfield.ai/mcp (HTTP) |
| kare 5:36 | npx -y impeccable@latest install komutu | Impeccable CLI | npx -y impeccable@latest install -providers=claude,codex |
| kare 5:46 | CLI çalışma testi (--help) | Impeccable CLI | node .claude/skills/impeccable/scripts/*.mjs --help |
| kare 6:16 | /impeccable init sohbet komutu | Impeccable | Running /impeccable init |
| kare 6:18 | agentic.com.tr (ajans örnek sitesi) | aday değil: konu dışı | agentic.com.tr |
| kare 6:22 | Next.js, Tailwind CSS, React, Vercel, Netlify (stack seçenekleri) | aday değil: genel kavram | Next.js + Tailwind / React, component-based, deploys to Vercel/Netlify |
| kare 6:28 | npx impeccable update komutu | Impeccable CLI | Runs npx impeccable update |
| kare 7:00 | WebGL gölgelendirici ve GLSL (dünya brief'i) | WebGL | a webgl tracking-tear shader |
| kare 7:00 | Canva ve Phosphor Icons ifadeleri | aday değil: genel kavram | Canva, Phosphor Icons |
| kare 7:04 | Instrument Serif yazı tipi | Instrument Serif | Instrument Serif |
| kare 7:58 | Antigravity IDE (dünya brief'i) | aday değil: genel kavram | VERIFY IN AntigraVity IDE |
| kare 8:52 | Recraft V4.1 model seçimi | Recraft V4.1 | Model chosen: Recraft V4.1 in utility mode |
| kare 9:32 | generate_image_batch araç çağrısı | Higgsfield MCP | higgsfield - generate_image_batch (MCP) |
| kare 9:32 | Üretilen üç kompozisyon görseli (Higgsfield çıktı linkleri) | aday değil: konu dışı | cloudfront.net görsel çıktıları |
| kare 9:36 | Azeret Mono yazı tipi (sayfa tipografisi) | Azeret Mono | outline numerals over Azeret Mono |
| kare 9:40 | Üstü çizili düzeltme (kanıt sayfası) | aday değil: genel kavram | THE LAB RECORD'S CARDINAL RULE - STRIKE |
| kare 9:40 | Strix ve Sentry (kod/güvenlik çıktısı) | aday değil: konu dışı | strix · Sentry |
| kare 10:12 | Linear (kompozisyon tasarım referansı) | aday değil: genel kavram | Linear |
| kare 10:16 | dur-kancasi.sh (stop hook betiği) | aday değil: konu dışı | dur-kancasi.sh |
| kare 10:34 | Canlı mod yardımcı sunucusu ve sayfa | Impeccable Live | Live mode is running. The page is open and instrumented |
| altyazı 10:13 | /impeccable live komutu | Impeccable Live | Impackable live diyeceğiz |
| kare 11:20 | Üç varyant (hiyerarşi, yapısal ayrıştırma, renk stratejisi) | Impeccable Live | Three variants are live on the result cell |
| altyazı 11:14 | iTerm (terminal uygulaması) | aday değil: konu dışı | iTerm (ses etiketi) |
| kare 13:36 | Canlı mod aksiyon menüsü | Impeccable Live | Freeform, Bolder, Quieter, Distill, Polish, Typeset |
| yorum | 'kie.ai da baglayabilirsiniz api ile' yorumu | Kie.ai | kie.ai da baglayabilirsiniz api ile |
| açıklama | Cursor, Codex, Gemini CLI uyumluluğu | Cursor | Cursor, Codex ve Gemini CLI ile de çalışıyor |
| açıklama | Skool topluluğu (otomasyon) | aday değil: sponsor/reklam | Türkiye'nin en çok kazandıran yapay zeka topluluğu |
| açıklama | Digital Academy eğitim sayfası ve Adım adım eğitim tanıtımı | aday değil: sponsor/reklam | Adım adım Türkçe yapay zeka eğitimleri |
## Kareden okunanlar
- 0:02: /impeccable polish the pricing page. Keep our sharp corners and sober palette. Impeccable sitesinde örnek bir cilalama komutu ve Aurelia demo otel sayfası görünüyor.
- 1:04: /impeccable audit blog, /impeccable redo this hero section, /impeccable pin <command> ve Cursor kurulum notu okunuyor.
- 3:50: npm i impeccable; 'Impeccable CLI': 59 deterministik kural; detect ve skills install komutları.
- 4:10: npx impeccable skills install çıktısı: harness listesi, kurulum konumu ve 'Done! type /impeccable init'.
- 4:42: Claude Code promptu: Impeccable kurulum talimatlarını çalıştırma isteği ve Opus 5 durum çubuğu.
- 5:08: Higgsfield MCP promptu: anahtar yazdırma yasağı, /mcp ile bağlantı doğrulama isteği.
- 5:48: Claude raporu: 'higgsfield: https://mcp.higgsfield.ai/mcp (HTTP) - Connected' ve proje kapsamı.
- 6:16: /impeccable init başlıyor; UPDATE_AVAILABLE uyarısı ve soru akışı görünüyor.
- 6:36: Kullanıcı yanıtı: 'yes update', 'no real assets', 'Invent all of the content'; 'use higgsfield mcp'.
- 7:00: Dünya brief'i: 'nineties mecha-anime crisis wall', 'Instrument Serif', 'WebGL', 'GLSL' gibi tasarım tarifleri.
- 8:52: Model seçimi: 'Recraft V4.1 in utility mode' ve hex paleti açıklaması.
- 9:32: Üç kompozisyon render edildi; seçim sayfası ve reroll yönlendirme metni.
- 9:40: 'THE LAB RECORD'S CARDINAL RULE - STRIKE' ve kurumsal kanıt sayfası başlığı.
- 10:12: Seçilen kompozisyon: 'DID THE NEW ONBOARDING IMPROVE ACTIVATION', 'INSUFFICIENT' damgası, 'Checks' listesi.
- 10:34: 'Live mode is running'; /impeccable live başladı; 'Pick an action' adımları.
- 11:20: Varyant seçenekleri: 'Three variants are live on the result cell'; Hiyerarşi, yapısal ayrıştırma, renk stratejisi.
- 13:36: Canlı mod aksiyon menüsü: Freeform, Bolder, Quieter, Distill, Polish, Typeset, Colorize, Adapt, Animate.
## Belirsizlikler
- Altyazıda ve ses etiketlerinde bozuk isimler var: 'Impecable/Impackable' Impeccable, 'Hickfield' Higgsfield olarak yorumlandı; 'KY AI FI' Kie.ai olabilir ama kesin değil; 'Xal' (5:06) kimliği belirsiz.
- Ses kaynaklı etiketler (Veo 2:03, Claude Sonnet 3:03, Slack 6:07, Geist 7:08, iTerm 11:14) altyazıda karşılığı olmadığı için doğrulanamadı; aday yapılmadı.
- OCR'da URL'ler bozuk okundu: 'impeccab.le.style' ve 'ipeccabile' ifadeleri impeccable.style olarak düzeltildi; dünya kartı URL'leri temsili olarak alındı.
- Stack seçimi: Next.js + Tailwind, React, Vercel, Netlify, Astro, Vue, Svelte, Angular seçenek menüsünde göründü; ajan 'You decide' seçeneğini kullandı, nihai stack video içinde açıkça belirtilmedi.
- Menü/liste/ekran metninde görünüp kullanılmayan öğeler aday yapılmadı: Mistral Vibe, Grok Build, Qoder, Rovo Dev, OpenCode, Pi, Trae, Hermes Agent (commit mesajı), Antigravity IDE, Puppeteer, Figma, Canva, Phosphor Icons, Three.js, Emotion, Find Skills, Git, Framer Motion, Descript, Bun, Go, JavaScript/TypeScript/Svelte dil yüzdeleri, Linear, Sentry, strix, Twinmotion (arka plan uygulaması), Notion, OpenAI, Python.
- Impeccable sürüm karışıklığı: video 4.0 başlığında; ekranda kurulan skill v4.1.1 (npm 3.6.0), init sırasında 4.0.4 görünüyor; ayrıca eski global kopya uyarısı var.
- Ajanın yardımcı bash çağrılarının (curl, stat, ls, python3 -c, node --wait, serve-question, live-poll, stop-review-gate-hook) tamamı kurulum_komutlar'a yazılmadı; yalnız gösterilen ve anlatılan ana komutlar alındı.
- Ekranda görünen API anahtarı benzeri değerler (anahtar kısa kimliği ve kullanıcıya ait terminal çıktıları) kayda alınmadı.
- Sayfa üretiminde 'localhost:3000' Impeccable demo sitesine ait; ajanın kendi sayfası 127.0.0.1:8777 ve canlı yardımcı 84ee üzerinde çalışıyor, bu ayrım videoda net değil.
- Kie.ai için video dışı yorum ('kie.ai da baglayabilirsiniz api ile') kaynaklı aday; narasyonla birebir eşleşme kesin değil.
- Video sonunda üretilen sayfanın (Did the new onboarding improve activation) yayın/dağıtım adımı gösterilmedi.
- Kanıt zamanı olarak kullanılan bazı kareler, OCR zamanlamasına dayanarak ±2 saniye sapabilir.
## Atlanan segment oranı
0/15 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.skool.com/otomasyon | açıklama | açıklama | hayır |
| https://digitalacademy.com.tr/claude-code-egitim.html | açıklama | açıklama | hayır |
| https://impeccable.style | açıklama | açıklama | evet |
| https://digitalacademy.com.tr | açıklama | açıklama | hayır |
| https://impeccable.style/docs/live | açıklama | açıklama | hayır |
| https://impeccable.style/live-mode | açıklama | açıklama | hayır |
| https://impeccable.style/#downloads | açıklama | açıklama | hayır |
| https://impeccable.style/neo-mirai/ | 2:50 | ekran | hayır |
| https://github.com/pbakaus/impeccable/commit/5ce4a5c6b5072877cbd22bcde9e68f9bf5818e51 | 1:23 | ekran | hayır |
| https://github.com/pbakaus/impeccable | 3:50 | ekran | evet |
| https://www.npmjs.com/package/impeccable?activeTab=code | 3:50 | ekran | evet |
| https://example.com | 4:02 | ekran | hayır |
| www.tek.org | 4:30 | ekran | hayır |
| https://raw.githubusercontent.com/pbakaus/impeccable/main/skill/SKILL.md | 4:42 | ekran | hayır |
| https://api.github.com/repos/pbakaus/impeccable/contents/skill | 4:48 | ekran | hayır |
| https://raw.githubusercontent.com/pbakaus/impeccable/main/package.json | 4:50 | ekran | hayır |
| https://mcp.higgsfield.ai/mcp | 5:48 | ekran | evet |
| higgsfield.ai | 5:48 | ekran | evet |
| agentic.com.tr | 6:18 | ekran | hayır |
| https://d8j0ntlcm91z4.cloudfront.net/user_34NcegihaLd2t0uqc1TCeeadap3/hf_20260814_224550_a1137139-92a1-4056-9d50-f43b022e06e5.png | 9:32 | ekran | hayır |
| https://d8j0ntlcm91z4.cloudfront.net/user_34NcegihaLd2t0uqc1TCeeadap3/hf_20260814_224550_4f1a4dd9-89cb-4063-9bf7-6bd58aed2ed9.png | 9:32 | ekran | hayır |
| https://impeccable.style/worlds/cards/pop-culture-shelf-arcade-command-center-hero.webp | 7:00 | ekran | hayır |
| https://impeccable.style/worlds/cards/signals-instruments-night-flight-six-pack-hero.webp | 7:08 | ekran | hayır |
| https://impeccable.style/worlds/cards/kinetic-sculpture-automata-crank-paper-menagerie-hero.webp | 8:04 | ekran | hayır |
| https://impeccable.style/worlds/cards/digital-design-canon-emergency-signal-degradation-hero.webp | 7:58 | ekran | hayır |
| https://impeccable.style/worlds/cards/paper-folds-pleats-deployable-curved-crease-shell-hero.webp | 8:06 | ekran | hayır |
| dur-kancasi.sh | 10:16 | ekran | hayır |
| kie.ai | açıklama | yorum | evet |
## İş akışı
- yok
## Promptlar
- Impeccable skill'inin Claude Code'a kurulması — Impeccable tasarım skill'ini kur; repo'daki kurulum talimatlarını oku ve çalıştır (Türkçe özet).
- Güvenli kurulum ve sürüm kontrolü — Kurulumdan önce Node sürümünü kontrol et; yetersizse dur ve yükseltme önerisi ver, mevcut skill ve ayarları değiştirme; yapılan her değişikliği listele (Türkçe özet).
- Görsel üretim MCP bağlantısı — Higgsfield MCP sunucusunu bu projeye bağla; kurulumu adım adım yürüt, gizli anahtarı ekrana yazdırma, sır gerekiyorsa beni durdur; bittiğinde /mcp ile yalnız bağlantının var olduğunu göster, veri çekme (Türkçe özet).
- Higgsfield MCP kurulum talebi — Higgsfield MCP sunucusunu Claude Code projesine bağla; kurulum talimatları sitelerinde MCP ve CLI bölümünde (Türkçe özet).
- Init sorularına yanıt ve içerik kuralları — Güncellemeyi yap; gerçek varlık ve sayı yok, tüm içeriği uydur ama bunların gerçek iddia olmadığı açıkça görünsün; Higgsfield MCP'yi kullan (Türkçe özet).
- Landing page için init mülakatı yanıtı — Landing page yap; stack'i sen seç, içeriği sen uydur (Türkçe özet).
- Live mode'da seçili öğe için düzenleme — Canlı modda seçili sonuç hücresinin çizgilerini daha kalın yap (Türkçe özet).
- Dünya seçiminde reroll yönlendirmesi — Yeniden üretimde tasarım dili ve kompozisyonu özgün tasarıma daha yakın tut (Türkçe özet).
- Mevcut sayfayı cilalama (demo) — Sadece pricing sayfasını cilala; keskin köşeleri ve sakin paletiyi koru, AI izlerini kaldır (Türkçe özet).
ikinci göz KAPALI: --ikinci-goz yok
