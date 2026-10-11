# I Made Claude Code FREE Using 25+ AI Models
## Künye
I Made Claude Code FREE Using 25+ AI Models · Coding With Abbas · süre: 13:35 · en-orig · https://youtu.be/IZPGFAS_tRY · şema 2
motor: parti 2026-10-11-short-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 69620 tk · claude-haiku-5-5: claude-haiku-5-5 · 94638 tk
## Özet
Video, Claude Code'u Claude aboneliği olmadan OpenRouter üzerinden ücretsiz yapay zekâ modelleriyle kullanmayı anlatıyor. OpenRouter hesabında API anahtarı oluşturuluyor. Anahtar, projedeki .claude/settings.local.json dosyasına ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN ve boş ANTHROPIC_API_KEY olarak giriliyor. Ücretli modeller kredi hatası veriyor. Bu yüzden önce tek bir ücretsiz model (Nemotron 3.5 Lightning) özel model seçeneği olarak ekleniyor. Sonra rastgele ücretsiz model seçip limit dolunca sonrakine geçen openrouter/free yönlendiricisi ekleniyor. Bununla tek dosyalık minimal bir portfolyo sayfası üretiliyor. Hangi modellerin kullanıldığı OpenRouter Activity sekmesinden izleniyor. Sonuçta ücretsiz modellerin yavaş ve limitli olduğu, karmaşık işler için Sonnet/Opus gibi ücretli modellerin gerektiği söyleniyor.
## Bölümler
- 0:00 Giriş: Claude Code'u ücretsiz modellerle kullanma fikri
- 0:50 OpenRouter nedir, Freeway ve OmniRoute alternatifleri
- 1:26 OpenRouter hesabı ve API anahtarı oluşturma
- 2:10 OpenRouter dokümanında Claude Code kurulum rehberi
- 3:03 Global shell profili ile proje düzeyi ayar farkı
- 3:36 VS Code'da boş proje ve mevcut Claude aboneliği
- 3:56 settings.local.json dosyasını oluşturma
- 5:00 Ücretli modeller ve kredi hatası
- 5:40 Çıkış yapıp tek komutla giriş yapmadan başlatma
- 6:48 Ücretsiz model listesi ve openrouter/free
- 7:09 Tek bir ücretsiz modeli özel model olarak ekleme
- 9:12 openrouter/free ile otomatik yedek (fallback)
- 10:12 claude --model ile belirli modelle başlatma
- 10:50 Minimal HTML landing page üretme
- 12:16 Activity sekmesinden kullanılan modelleri izleme
- 13:17 Kapanış ve sınırlamalar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OpenRouter | yok | CLI | yok | Tek API üzerinden birçok sağlayıcının modellerine erişim sağlayan bulut ağ geçidi | 0:50 | OpenRouter is basically a single gateway where you can access models from different AI providers |
| Claude Code | yok | CLI | yok | Terminalde çalışan kodlama ajanı; OpenRouter'a bağlanarak ücretsiz modellerle kullanıldı | 3:36 | Terminalde Claude Code v2.1.276 karşılama ekranı (karede: VS Code terminalinde 'Claude Code v2.1.276', 'Sonnet 5 with medium effort · Claude Pro' ve çalışma klasörü yolu) |
| openrouter/free | yok | teknik | yok | Kullanılabilir ücretsiz modeller arasından rastgele seçen ve limit dolunca sonrakine geçen yönlendirici | 9:12 | openrouter/free ... selects the free model at random from models available in OpenRouter |
| Nemotron 3.5 Lightning | yok | teknik | yok | Tek başına özel model olarak eklenen ücretsiz NVIDIA modeli (nvidia/nemotron-3.5-lightning:free) | 8:58 | Model seçildi, 'hi' cevabı alındı; yaklaşık 2 dakika sürdü (karede: Terminalde '/model Set model to nvidia/nemotron-3.5-lightning:free', 'hi', 'Thought for 1m 39s' ve 'Worked for 1m 43s') |
| settings.local.json | yok | teknik | yok | Proje düzeyinde .claude klasöründe env değişkenlerini tutan Claude Code ayar dosyası | 3:56 | Claude klasöründe bu dosya oluşturuldu ve ayarlar yapıştırıldı (karede: VS Code gezgininde .claude > settings.local.json açık, boş dosya ve 'Generate code' ipucu) |
| ANTHROPIC_BASE_URL | yok | teknik | yok | Claude Code'un istek adresini OpenRouter API'sine yönlendiren ortam değişkeni | 4:12 | Anthropic base URL that we will set to openrouter/api |
| ANTHROPIC_AUTH_TOKEN | yok | teknik | yok | OpenRouter API anahtarını bearer jeton olarak taşıyan ortam değişkeni | 4:12 | Then our Anthropic auth token. And here we have to add our API key |
| ANTHROPIC_API_KEY | yok | teknik | yok | Çakışmayı önlemek için bilerek boş bırakılan ortam değişkeni | 4:12 | for the Anthropic API key simply set it to empty string |
| CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY | yok | teknik | yok | Ağ geçidindeki modelleri /model listesinde göstermeyi açan bayrak (1) | 4:48 | Ayar dosyasında değeri 1; sonra /model listesinde gateway modelleri çıktı (karede: settings.local.json içinde 'CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY': '1') |
| ANTHROPIC_CUSTOM_MODEL_OPTION | yok | teknik | yok | Model seçiciye tek bir özel model kimliği ekleyen değişken; NAME ile adı verilir | 7:40 | Claude Code dokümanından kopyalanıp env'e eklendi (karede: Claude Code Docs model-config sayfasında ANTHROPIC_CUSTOM_MODEL_OPTION, _NAME ve _DESCRIPTION export örneği) |
| /model | yok | teknik | yok | Claude Code'da model seçme komutu | 3:42 | Model seçim listesi açıldı (karede: Terminalde '/model' yazılı, 'Set the AI model for Claude Code (currently Sonnet 5)' açıklaması) |
| /logout | yok | teknik | yok | Kayıtlı Claude oturumunu kapatır; önbellekteki girişi temizler | 5:40 | Videoda çıkış yapılıp tekrar claude yazıldı (karede: Terminalde '/lou' yazılıyor, altında '/vercel:flags-sdk' ve '/code-review' önerileri) |
| claude --model | yok | CLI | yok | Claude Code'u belirli bir model kimliğiyle başlatan bayrak | 10:14 | you can type in here this command Claude {dash} model |
| VS Code | yok | CLI | yok | Proje klasörü, ayar dosyası düzenleme ve entegre terminal için kullanılan editör | 3:30 | VS Code'da portfolio-website klasörü açık (karede: Visual Studio Code penceresi, gezginde portfolio-website ve alt terminal) |
| Live Server | yok | plugin | yok | index.html'i tarayıcıda canlı önizleyen VS Code eklentisi (Go Live) | 11:36 | Sayfa 127.0.0.1:5500 adresinde açıldı (karede: Chrome'da 127.0.0.1:5500/index.html; Hakkında, Projeler, Beceriler bölümleri) |
| OpenRouter Activity | yok | teknik | yok | Kullanılan modelleri, istek sayısını ve token hacmini gösteren panel | 12:30 | Activity ve Explore sayfaları gösterildi · kanıt: kare (karede: Activity: Requests 47, Token volume 1.65M, portfolio-website anahtarı 1.45M tok) |
| Freeway | yok | CLI | yok | Birden çok sağlayıcıyı yerel kurulumla yönlendiren alternatif araç; yalnız anıldı | 0:50 | other tools like Freeway and OmniRoute that let you work with multiple providers |
| OmniRoute | yok | CLI | yok | Yerel çalışan alternatif yönlendirici; yalnız anıldı | 1:02 | we have other tools like Freeway and OmniRoute that works locally |
| OpenAI: GPT-5.6 Sol | yok | teknik | yok | Ücretli model denemesi; kredi yetersizliği hatası verdi | 5:22 | Seçilip 'hi' yazıldı, 402 hatası alındı (karede: 'Set model to OpenAI: GPT-5.6 Sol' ve 'API Error: 402 This request requires more credits') |
| Claude Sonnet | yok | teknik | yok | Abonelikle gelen Claude modeli; model listesinde gösterildi | 3:44 | Select model listesinde Default/Sonnet/Fable/Opus (karede: Select model: 1. Default (recommended) Sonnet 5, 2. Sonnet, 3. Fable 5.1, 4. Opus 5) |
| Claude Opus | yok | teknik | yok | Karmaşık işler için önerilen ücretli Claude modeli | 3:44 | Model listesinde Opus 5 (karede: Select model listesinde 'Opus 5 · Best for everyday, complex tasks') |
| Claude Fable | yok | teknik | yok | Model listesinde gösterilen en yetenekli Claude modeli | 3:44 | Listede Fable 5.1 (karede: 'Fable 5.1 · Most capable for your hardest and longest-running tasks') |
| Claude Haiku | yok | teknik | yok | Hızlı Claude modeli; gateway listesinde göründü | 4:58 | Model listesinde Haiku 4.5 (karede: 'Haiku 4.5 Fastest for quick answers · $1/$5 per Mtok') |
| DeepSeek V4 Flash 0731 | yok | teknik | yok | openrouter/free isteklerinde kullanılan modellerden biri; en yüksek paylı | 12:46 | Explore tablosunda en üst satır (karede: Explore tablosunda DeepSeek V4 Flash 0731 satırı, % of Total 10.6%) |
| Nex-N2.5-Pro | yok | teknik | yok | Router'ın kullandığı modellerden biri | 12:46 | Explore tablosunda listelendi (karede: Explore tablosunda Nex-N2.5-Pro, 4.3%) |
| HTML | yok | teknik | yok | Landing page tek dosyalık HTML olarak üretildi | 11:14 | index.html 213 satır yazıldı (karede: Terminalde 'Wrote 213 lines to index.html' ve 'Created a minimal, responsive single-file landing page') |
| npm | yok | CLI | yok | Claude Code'u npm ile kurma seçeneği | 2:38 | npm sekmesinde kurulum komutu (karede: 'npm install -g @anthropic-ai/claude-code', 'Requires Node.js 18 or newer') |
| GitHub | yok | teknik | yok | OpenRouter hesabına giriş için kullanılan hesap | 1:02 | I am already logged in with my GitHub account |
| Minimal HTML landing page (portfolyo sitesi) üretmek | yok | prompt | yok | Dosya sistemi boş projede, yalnızca HTML ile minimal bir landing page tasarlanması isteniyor; model openrouter/free seçili. | 10:55 | kaynak: altyazı |
| Modelin yanıt verdiğini ve kredi hatası olup olmadığını test etmek | yok | prompt | yok | Modelin çalıştığını doğrulamak için basit bir selamlama ('hi') gönderiliyor. | 5:22 | kaynak: kare |
## Açıklama bağlantıları
- https://openrouter.ai/api — OpenRouter API taban adresi (ANTHROPIC_BASE_URL değeri) · aday: evet (OpenRouter) · Videoda kullanılan OpenRouter servisinin adresi; izleyici kullanabilir. · sınıf: diğer
- https://youtu.be/qzPvSYVyqaw — Kanal sahibinin başka videosu (aylık 7 milyar ücretsiz token) · aday: hayır · Videoda anlatılmayan başka video; araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Koyu temalı tek sayfa (dark theme) CSS değişkenleriyle (--bg, --surface) tanımlandı; kod dosyası tek HTML içinde gömülü stil kullanıyor | Koyu renk tema (Dark theme) ve CSS değişkenleri (CSS custom properties) (karede: Terminalde index.html kodu: ':root { --bg: #0d1117; --surface: #161b22;') | 11:24 | kare |
| Sayfa başında başlık ve düğmeler içeren giriş alanı | Kahraman bölümü (Hero section) | 11:14 | altyazı |
| Hakkında metni, ince ayırıcı çizgilerle ayrılmış bölüm | Hakkında bölümü (About section) (karede: Tarayıcıda 'About' başlığı ve kısa metin, altında ayırıcı çizgi) | 11:36 | kare |
| Başlık ve açıklamalı satır listesi, aralarında çizgi | Proje listesi (Project list) (karede: 'Projects': Portfolio Website, Task CLI, Weather Dashboard satırları) | 11:36 | kare |
| Küçük kenarlıklı etiketler halinde sıralanan beceri rozetleri | Beceri etiketleri (Skill chips/tags) (karede: 'Skills' altında HTML/CSS, JavaScript, TypeScript, React, Node.js, Python, Git, Tailwind CSS etiketleri) | 11:36 | kare |
| Sayfa sonunda iletişim bölümü ve alt bilgi | İletişim bölümü ve alt bilgi (Contact section, footer) | 11:14 | altyazı |
| Tek sütunlu, ortalanmış dar içerik genişliği; duyarlı tasarım olarak anlatıldı | Duyarlı tek sütun yerleşim (Responsive single-column layout) (karede: Terminal: 'responsive single-file landing page ... embedded CSS') | 11:24 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://claude.ai/install.sh / bash | macOS/Linux/WSL'de Claude Code'u yerel yükleyiciyle kurar (karede: OpenRouter dokümanında 'macOS, Linux, WSL:' altında curl komutu) | 2:24 | kare |
| irm https://claude.ai/install.ps1 / iex | Windows PowerShell'de Claude Code'u kurar (karede: 'Windows PowerShell:' altında irm komutu) | 2:24 | kare |
| npm install -g @anthropic-ai/claude-code | Claude Code'u npm ile global kurar (Node.js 18+) (karede: npm sekmesinde 'Requires Node.js 18 or newer' ve kurulum komutu) | 2:38 | kare |
| source ~/.zshrc | Shell profilindeki yeni değişkenleri yeniden yükler (karede: Dokümanda 'source ~/.zshrc # or ~/.bashrc, or open a new terminal') | 3:18 | kare |
| claude | Proje klasöründe Claude Code'u başlatır (karede: Terminalde Claude Code v2.1.276 başlangıç ekranı) | 3:36 | kare |
| /model | Model seçme menüsünü açar (karede: Terminalde '/model' yazılı) | 3:42 | kare |
| /logout | Claude hesabından çıkış yapar (karede: Terminalde '/lou' yazılıyor) | 5:40 | kare |
| ANTHROPIC_BASE_URL="https://openrouter.ai/api" ANTHROPIC_AUTH_TOKEN="<anahtar>" ANTHROPIC_API_KEY="" claude | Ayar dosyası olmadan, ortam değişkenleriyle OpenRouter üzerinden giriş yapmadan Claude Code'u başlatır (karede: Terminalde ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_API_KEY ve claude satırları; 'Get this command from video description') | 6:06 | kare |
| claude --model nvidia/nemotron-3.5-lightning:free | Claude Code'u belirli bir model kimliğiyle başlatır | 10:14 | altyazı |
| claude --resume <oturum-kimliği> | Çıkışta gösterilen önceki oturumu devam ettirir (karede: Terminalde 'Resume this session with: claude --resume ...') | 8:32 | kare |
| /status | Bağlantının OpenRouter üzerinden olduğunu doğrular (dokümanda gösterildi) (karede: Dokümanda 'confirm your connection by running the /status command') | 4:48 | kare |
| export ANTHROPIC_BASE_URL="https://openrouter.ai/api" | Claude Code isteklerini OpenRouter API adresine yönlendirir. (karede: Shell profil bloğunda ANTHROPIC_BASE_URL="https://openrouter.ai/api" satırı.) | 2:54 | kare |
| export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY" | OpenRouter anahtarını bearer token olarak gönderir; anahtar değeri ortam değişkeninden okunur. (karede: Shell profil bloğunda ANTHROPIC_AUTH_TOKEN satırı ve 'Ordering matters' uyarısı.) | 3:18 | kare |
| export ANTHROPIC_API_KEY="" | Doğrudan Anthropic kimlik bilgisini boş bırakarak çakışmayı önler. (karede: Shell profil bloğunda ANTHROPIC_API_KEY="" satırı ('Must be explicitly empty').) | 2:50 | kare |
| export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 | Ağ geçidi üzerinden model keşfini açar (isteğe bağlı). (karede: Shell profil bloğunda CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 satırı.) | 2:50 | kare |
| .claude/settings.local.json (env: ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_API_KEY "", CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY) | Proje düzeyinde Claude Code'u OpenRouter'a bağlayan ayar dosyası; anahtar yerine yer tutucu kullanılır. (karede: VS Code'da .claude/settings.local.json dosyasında 'env' bloğu ve ANTHROPIC_BASE_URL satırı.) | 4:08 | kare |
| ANTHROPIC_BASE_URL="https://openrouter.ai/api" ANTHROPIC_AUTH_TOKEN="YOUR_NEW_KEY" ANTHROPIC_API_KEY="" claude | Claude Code'u OpenRouter bağlantısıyla, anahtarı komut satırında vererek başlatır (YOUR_NEW_KEY yer tutucudur). | açıklama | açıklama |
| export ANTHROPIC_CUSTOM_MODEL_OPTION="nvidia/nemotron-3.5-lightning:free" | Ücretsiz Nemotron modelini Claude Code model listesine özel model olarak ekler. (karede: settings.local.json içinde ANTHROPIC_CUSTOM_MODEL_OPTION_NAME satırı ve model kimliği alanı.) | 8:10 | kare |
| export ANTHROPIC_CUSTOM_MODEL_OPTION="openrouter/free" | openrouter/free yönlendiricisini özel model olarak ekler; yedekleme davranışını sağlar. | 9:12 | altyazı |
| claude --model <model-id> | Oturumu belirtilen modelle başlatır (örn. nvidia/nemotron-3.5-lightning:free). | 10:12 | altyazı |
| claude --resume <oturum-id> | Önceki Claude Code oturumunu kaldığı yerden sürdürür. (karede: Terminalde 'claude --resume f6fa655b-...' satırı görünüyor.) | 8:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| openrouter/free yaklaşık 25 ücretsiz modelden rastgele seçim yapar; limit dolarsa sonraki modele geçer. | 9:12 | özellik |
| Ücretsiz modeller yavaş olabilir; Nemotron'a 'hi' yazınca cevap yaklaşık 2 dakika sürdü. | 8:58 | sayısal |
| Ücretsiz modeller temel siteler, portfolyo ve basit uygulamalar için yeterli; karmaşık işler için Sonnet/Opus gibi ücretli modeller gerekir. | 11:14 | karşılaştırma |
| Proje düzeyi ayarla başlamak, global shell profilinden önerilir. | 2:50 | öneri |
| Anahtar dosyaya girildiğinde, giriş yapmadan başlatmak için komut kullanılabilir; Claude hesabı gerekmez. | 6:06 | özellik |
| Toplamda 47 istek ve 1,45 milyon token kullanıldı; DeepSeek %10,6 paya sahip. | 12:30 | sayısal |
| Bağlanınca model listesinde 16 model (ücretli) görünür; ücretli model seçilirse kredi hatası gelir. | 5:22 | özellik |
| Ücretsiz modeller kullanım ve hız limitine tabidir; sınırsız değildir. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | Kanalın önceki videoları (Nest.js, Docker, React, Zod, Redux) | aday değil: konu dışı | YouTube kanal video ızgarası |
| konuşma 0:00 | Claude Sonnet, Opus, Haiku, Fable modelleri | Claude Sonnet | Claude models like Haiku, Sonnet, Opus, and Fable |
| konuşma 0:00 | Claude Opus | Claude Opus | model listesinde Opus 5 |
| konuşma 0:00 | Claude Haiku | Claude Haiku | Haiku 4.5 listede |
| konuşma 0:00 | Claude Fable | Claude Fable | Fable 5.1 listede |
| konuşma 0:00 | Claude Code | Claude Code | Claude Code ekranı v2.1.276 |
| konuşma 0:50 | OpenRouter | OpenRouter | single gateway ... through one API |
| konuşma 0:50 | Google, Meta, Nvidia modelleri | aday değil: genel kavram | you can access Claude models, Google models, Meta models |
| konuşma 0:50 | Freeway | Freeway | other tools like Freeway and OmniRoute |
| konuşma 1:02 | OmniRoute | OmniRoute | Freeway and OmniRoute that works locally |
| konuşma 1:02 | GitHub hesabı | GitHub | logged in with my GitHub account |
| kare 1:26 | OpenRouter profil sayfası | OpenRouter | openrouter.ai/settings/profile |
| kare 1:53 | API anahtarı oluşturma | OpenRouter | New Key penceresi |
| kare 2:10 | OpenRouter dokümanı Quickstart | OpenRouter | OpenRouter Quickstart Guide |
| kare 2:12 | OpenRouter Agent SDK ve Client SDK | aday değil: genel kavram | Quickstart'ta yalnız listelenmiş seçenekler |
| kare 2:16 | Claude Code arama sonucu | Claude Code | claude code araması |
| kare 2:20 | Cursor, Codex CLI, OpenClaw, Hermes Agent kenar menüsü | aday değil: konu dışı | Dokümanın yan menüsünde yalnız listelenmiş |
| kare 2:24 | Yerel yükleyici curl/irm komutları | Claude Code | claude.ai/install.sh |
| kare 2:38 | npm ile kurulum | npm | npm install -g @anthropic-ai/claude-code |
| kare 2:38 | Node.js 18+ | aday değil: başka adayın parçası (npm) | Requires Node.js 18 or newer |
| kare 2:50 | Shell profile export satırları | ANTHROPIC_BASE_URL | export ANTHROPIC_BASE_URL |
| kare 2:56 | .claude/settings.local.json | settings.local.json | Project Settings File sekmesi |
| konuşma 3:03 | VS Code | VS Code | go back to my VS code |
| kare 3:42 | /model komutu | /model | terminalde /model |
| kare 3:44 | Sonnet 5 ve model seçici | Claude Sonnet | Select model: Sonnet 5 |
| konuşma 4:12 | ANTHROPIC_AUTH_TOKEN | ANTHROPIC_AUTH_TOKEN | Then our Anthropic auth token |
| konuşma 4:12 | ANTHROPIC_API_KEY boş | ANTHROPIC_API_KEY | set key to nothing |
| kare 4:48 | CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY | CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY | bayrak 1 |
| kare 5:06 | Gateway modelleri (GPT, Grok, Gemini, Qwen, Kimi, GLM) | aday değil: genel kavram | Yalnızca model listesinde görünüyor, kullanılmadı |
| kare 5:22 | OpenAI GPT-5.6 Sol denemesi ve 402 kredi hatası | OpenAI: GPT-5.6 Sol | 402 This request requires more credits |
| kare 5:40 | /logout ve /vercel ile /code-review öneri menüsü | /logout | terminalde /lou yazılı |
| kare 5:50 | Giriş yöntemi seçimi (abonelik, Console, 3rd-party) | aday değil: genel kavram | Claude Code karşılama menüsü |
| kare 6:06 | Anahtarı komut satırında veren başlatma komutu | Claude Code | ANTHROPIC_BASE_URL ... claude |
| kare 6:28 | Claude Code güvenlik notları | aday değil: konu dışı | Security notes ekranı |
| kare 6:48 | Free Models Router (openrouter/free) | openrouter/free | Free Models Router sayfası |
| kare 7:18 | TypeSafe Jev modeli | aday değil: konu dışı | Model listesinde yalnız göründü |
| kare 7:26 | Ücretsiz model listesi (Ling, Nex, Flux TTS, DeepSeek) | DeepSeek V4 Flash 0731 | models?variant=free |
| kare 7:32 | NVIDIA Nemotron 3.5 Lightning sayfası | Nemotron 3.5 Lightning | NVIDIA: Nemotron 3.5 Lightning (free) |
| kare 7:40 | ANTHROPIC_CUSTOM_MODEL_OPTION dokümanı | ANTHROPIC_CUSTOM_MODEL_OPTION | model-config sayfası |
| kare 8:58 | Nemotron ile 'hi' yanıtı | Nemotron 3.5 Lightning | Worked for 1m 43s |
| kare 10:14 | claude --model bayrağı ve model katalog uyarısı | claude --model | claude --model komutu |
| kare 11:24 | index.html oluşturma | HTML | Wrote 213 lines to index.html |
| kare 11:36 | Önizleme sayfası ve Live Server | Live Server | 127.0.0.1:5500/index.html |
| kare 11:36 | Tailwind CSS, Git, React becerileri (sayfa içeriği) | aday değil: konu dışı | Üretilen sayfadaki beceri etiketleri |
| kare 12:30 | OpenRouter Activity paneli | OpenRouter Activity | Requests 47 |
| kare 12:46 | Nex-N2.5-Pro modeli | Nex-N2.5-Pro | Explore tablosu |
| konuşma 12:16 | DeepSeek modeli | DeepSeek V4 Flash 0731 | 10% DeepSeek |
| açıklama | Model fallback (yedekleme) | openrouter/free | model fallbacks can help |
| açıklama | openrouter.ai/api | OpenRouter | Açıklama bağlantısı |
| yorum | Kanal sahibinin diğer videosu | aday değil: konu dışı | youtu.be/qzPvSYVyqaw |
| linkli sayfa | OpenRouter dokümanındaki Replit, Cline bağlantıları | aday değil: konu dışı | Bağlantılı sayfalar listesinde, videoda kullanılmadı |
## Kareden okunanlar
- 1:12: openrouter.ai ana sayfa: 'The Unified Interface For Every Model', 400T+ token, 10M+ kullanıcı, 80+ sağlayıcı, 500+ model
- 1:53: Anahtar oluşturma penceresi: Name, Expiration, Credit limit alanları; anahtar adı portfolio-website, süre 1 gün
- 2:50: OpenRouter dokümanı: shell profile için export satırları ve CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1
- 2:56: Project Settings File sekmesi: .claude/settings.local.json içindeki env bloğu
- 4:48: Ayar dosyasında ANTHROPIC_BASE_URL, boş ANTHROPIC_API_KEY ve gateway discovery bayrağı (anahtar değeri bu çıktıya yazılmadı)
- 5:06: Model listesi: GPT-5.6 Sol, GPT-6 Astra, Grok 4.6, Gemini 3.8 Flash, Qwen3.8 Max, Kimi K3, GLM 5.3; 'From gateway'
- 5:22: API Error: 402 — istek daha fazla kredi gerektiriyor
- 7:26: Ücretsiz model listesi: Ling 3.0 Flash, Nex-N2.5, Flux TTS, Nemotron 3.5 Lightning, DeepSeek V4 Flash 0731, Inkling Small
- 10:14: Uyarı: nvidia/nemotron-3.5-lightning:free bu sürümün model kataloğunda tanımlı değil; 200k token varsayılır
- 11:24: index.html 213 satır yazıldı; :root içinde --bg ve --surface CSS değişkenleri
- 12:30: Activity: toplam harcama $0.00, 47 istek, 1.65M token; portfolio-website anahtarı 1.45M tok
- 12:46: Explore tablosu: DeepSeek V4 Flash 0731 %10.6, Nemotron 3.5 Lightning %19.1, Nemotron 3 Super %10.6 ve diğerleri
## Belirsizlikler
- Videodaki API anahtarı ekranda göründü; bu çıktıya yazılmadı.
- Freeway ve OmniRoute yalnızca sözle anıldı, gösterilmedi; aday olarak işaretlendi ama kullanılmadı.
- Açıklamadaki 'Free-Way' yazımı ile konuşmadaki 'Freeway' farklı yazılmış; aynı araç sanılıyor.
- Bağlantılı sayfalardaki yüzlerce doküman URL'si tek tek urller'e yazılmadı; yalnız ekranda görünenler ve açıklama/yorum bağlantıları alındı.
- Kare listesinde 11:14 kare zamanı yok; HTML üretimi kareleri 11:24 ve 11:36'dan okundu. Prompt zamanı (10:55) yaklaşık.
- Model listesindeki Gemini 3.8 Flash, Qwen3.8 Max, Kimi K3, Grok 4.6 ve GLM 5.3 yalnızca menüde göründü; adaya yazılmadı.
- TypeSafe Jev ve Deepgram Flux TTS yalnızca model listesinde göründü, kullanılmadı.
- Activity ekranındaki 47 istek ve 1,45M token rakamı konuşma ile uyumlu; toplam 1,65M ekranda ayrıca görünüyor.
- Anlatıcı 'Sonar' dedi, ekranda Sonnet göründüğü için Sonnet yazıldı. '4 model' ve '25 model' sayıları konuşmadan alındı; sayfada 28 görünüyor.
- Model yanıt süresi: konuşmada 'yaklaşık 2 dakika', ekranda 1 dk 43 sn.
## Atlanan segment oranı
0/14 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://openrouter.ai/api | açıklama | açıklama | evet |
| https://youtu.be/qzPvSYVyqaw | açıklama | yorum | hayır |
| openrouter.ai | 1:02 | ses | evet |
| openrouter.ai/settings/profile | 1:26 | ekran | evet |
| openrouter.ai/workspaces/default/keys | 1:38 | ekran | evet |
| https://openrouter.ai/models | 2:10 | ekran | evet |
| openrouter.ai/docs/quickstart | 2:12 | ekran | evet |
| openrouter.ai/docs/cookbook/coding-agents/claude-code-integration#claude-code | 2:20 | ekran | evet |
| https://claude.ai/install.sh | 2:24 | ekran | evet |
| https://claude.ai/install.ps1 | 2:24 | ekran | evet |
| https://openrouter.ai/settings/credits | 5:22 | ekran | evet |
| https://code.claude.com/docs/en/security | 6:28 | ekran | hayır |
| openrouter.ai/openrouter/free/?utm_source=chatgpt.com | 6:48 | ekran | evet |
| https://docs.typesafe.ai/concepts/system-one | 7:18 | ekran | hayır |
| openrouter.ai/models?variant=free | 7:24 | ekran | evet |
| https://openrouter.ai/nvidia/nemotron-3.5-lightning:free | 7:32 | ekran | evet |
| code.claude.com/docs/en/model-config#special-model-behavior | 7:40 | ekran | evet |
| openrouter.ai/activity | 12:28 | ekran | evet |
| https://openrouter.ai/activity/explore | 12:36 | ekran | evet |
| 127.0.0.1:5500/index.html | 11:36 | ekran | evet |
| https://openrouter.ai/apps/url/https%3A%2F%2Fhermes-aBrowseserch.com%2F | 1:17 | ekran | hayır |
| https://github.com/OpenRouterTeam/skills/tree/main/skills | 2:12 | ekran | hayır |
| https://openrouter.ai/settings/keys | 2:44 | ekran | evet |
| https://code.claude.com/docs/en/microsoft-foundry | 6:00 | ekran | hayır |
| https://openrouter.ai/deepgram/flux-tts:free | 7:26 | ekran | hayır |
| https://openrouter.ai/nex-agi/nex-n2.5-pro:free | 7:28 | ekran | evet |
## İş akışı
- 1. adım — OpenRouter ana sayfasını tanıtma ve hesabı açma (GitHub ile girişli) — araçlar: OpenRouter, GitHub
- 2. adım — Dashboard'dan API Keys sayfasına gidip yeni anahtar oluşturma (ad portfolio-website, süre 1 gün) — araçlar: OpenRouter
- 3. adım — Docs'ta 'Claude code' arayıp entegrasyon rehberini açma — araçlar: OpenRouter
- 4. adım — Claude Code kurulum seçeneklerini (curl/irm/npm) ve Shell Profile / Project Settings seçeneklerini gösterme — araçlar: Claude Code, npm
- 5. adım — VS Code'da boş proje klasöründe claude başlatıp mevcut Pro abonelik modellerini /model ile gösterme — araçlar: VS Code, Claude Code, /model
- 6. adım — .claude/settings.local.json oluşturup env değerlerini (base URL, auth token, boş API key, discovery bayrağı) yapıştırma — araçlar: VS Code, settings.local.json, ANTHROPIC_AUTH_TOKEN
- 7. adım — Claude'u yeniden başlatıp 16 gateway modelini görme; ücretli GPT-5.6 Sol ile 'hi' deneyip 402 kredi hatasını alma — araçlar: Claude Code, OpenAI: GPT-5.6 Sol
- 8. adım — /logout ile çıkıp tek satırlık ortam değişkenli komutla giriş yapmadan başlatma — araçlar: Claude Code, /logout
- 9. adım — openrouter.ai/models'te ücretsiz filtresi ile Nemotron 3.5 Lightning'i seçme — araçlar: OpenRouter, Nemotron 3.5 Lightning
- 10. adım — Claude Code dokümanından ANTHROPIC_CUSTOM_MODEL_OPTION ve NAME değişkenlerini kopyalayıp modeli ekleme — araçlar: ANTHROPIC_CUSTOM_MODEL_OPTION, settings.local.json
- 11. adım — Claude'u yeniden başlatıp özel modeli seçme ve 'hi' ile test etme (≈2 dakika sürdü) — araçlar: Claude Code, Nemotron 3.5 Lightning
- 12. adım — openrouter/free kimliğini özel model olarak ayara yazma ve yeniden başlatıp seçme — araçlar: openrouter/free, settings.local.json
- 13. adım — claude --model ile belirli bir modelle başlatmayı gösterme — araçlar: claude --model
- 14. adım — openrouter/free seçili iken minimal HTML landing page promptunu verme — araçlar: Claude Code, openrouter/free, HTML
- 15. adım — Üretilen index.html'i Live Server ile açıp sayfayı kontrol etme — araçlar: Live Server, VS Code
- 16. adım — OpenRouter Activity ve Explore'dan kullanılan modelleri ve token payını inceleme — araçlar: OpenRouter Activity
## Promptlar
- Minimal HTML landing page (portfolyo sitesi) üretmek — Dosya sistemi boş projede, yalnızca HTML ile minimal bir landing page tasarlanması isteniyor; model openrouter/free seçili.
- Modelin yanıt verdiğini ve kredi hatası olup olmadığını test etmek — Modelin çalıştığını doğrulamak için basit bir selamlama ('hi') gönderiliyor.
ikinci göz KAPALI: --ikinci-goz yok
