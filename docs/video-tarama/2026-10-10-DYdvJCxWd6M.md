# Hermes Agent - Full Tutorial & Setup Guide (For Beginners)
## Künye
Hermes Agent - Full Tutorial & Setup Guide (For Beginners) · Metics Media · süre: 34:23 · en-ehkg1hFWq8A · https://youtu.be/DYdvJCxWd6M · şema 2
motor: parti 2026-10-10-short-7 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (46)
kareler: girdi ≤40000 jeton için 60→46
claude-sonnet-5-5: claude-sonnet-5-5 · 70260 tk · claude-haiku-5-5: claude-haiku-5-5 · 113117 tk
## Özet
Matt (Metics Media), yeni başlayanlar için Hermes Agent kurulumunu anlatıyor. Hostinger KVM 1 VPS üzerine tek tıkla Hermes Agent dağıtılıyor, OpenRouter anahtarı ve DeepSeek V4 Flash ana model olarak bağlanıyor, Telegram botu QR ile kuruluyor. Ardından masaüstü uygulaması uzak ağ geçidi olarak sunucuya bağlanıyor. Kalıcı bellek (düzeltme tercihi), skill'ler, kendi skill'ini yazıp cron ile zamanlayan ve ona ilk mesajı atan ajan gösteriliyor. Son bölümlerde OpenRouter maliyeti (105 istekte 13 sent), model değiştirme, loglar, gateway yeniden başlatma, alt ajanlar, profiller ve OpenClaw içe aktarma anlatılıyor.
## Bölümler
- 0:00 Giriş
- 1:23 Hermes Agent nedir?
- 2:13 Ajanın yaşayacağı yeri seçmek
- 4:02 Tek tıkla dağıtım (Hostinger)
- 8:04 İlk temas: tarayıcı paneli
- 9:37 Beyni bağlamak: modeller ve anahtarlar
- 13:45 Telefondan sohbet (Telegram)
- 16:37 Çalışanınla tanış
- 18:20 Masaüstü uygulaması
- 22:40 Öğret: kalıcı düzeltme
- 26:14 Sana ilk mesajı atan ajan
- 28:13 Maliyet ve model stratejisi
- 30:24 Loglar, düzeltmeler, güncellemeler
- 32:07 Buradan sonra neler yapılır
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Hermes Agent | yok | CLI | https://github.com/NousResearch/hermes-agent | Nous Research'ün açık kaynak, kendini geliştiren, sürekli çalışan yapay zekâ ajanı | 1:23 | Hermes Agent is a free open source AI agent from Nous Research |
| Hostinger | yok | iş akışı | yok | Hermes'i tek tıkla Docker şablonuyla kuran VPS barındırma servisi (KVM 1) | 4:02 | We're using Hostinger because their one click template instals Hermes for you |
| Docker Manager | yok | iş akışı | yok | Hostinger içindeki Docker uygulama yöneticisi; yeniden başlatma ve katalog | 7:04 | click Docker Manager on the left side, and then from there, click Compose |
| Traefik | yok | teknik | yok | Docker uygulamaları için HTTPS/ters vekil sunucu | 6:28 | Ekranda 'Enable HTTPS for your Docker applications with Traefik'; konuşmada traffic reverse proxy (karede: kanıttan) Ekranda 'Enable HTTPS for your Docker applications with Traefik'; konuşmada traffic reverse proxy |
| OpenRouter | yok | iş akışı | yok | Yüzlerce modele tek hesapla erişim sağlayan API servisi | 9:37 | we're using OpenRouter. is one account that gives you access to hundreds |
| DeepSeek V4 Flash | yok | iş akışı | yok | Ajanın ana modeli olarak seçilen ucuz, hızlı, araç kullanımında iyi model | 11:38 | We're picking DeepSeek-V4-Flash because it's cheap, it's fast |
| Nous Portal | yok | iş akışı | yok | Anahtarsız, aylık yaklaşık 20$ sabit ücretli alternatif abonelik | 12:41 | Hermes also offers something called Nous Portal, a flat rate subscription |
| Telegram | yok | iş akışı | yok | Ajanla telefondan konuşmak için QR ile kurulan bot kanalı | 13:45 | We're going to give your agent its own Telegram bot |
| Hermes masaüstü uygulaması | yok | iş akışı | yok | Uzak ağ geçidi ile sunucuya bağlanan resmi masaüstü uygulaması, HUD ve sesli mod | 18:20 | we'll point it at the server it already has · kanıt: yok |
| Hermes web paneli | yok | iş akışı | yok | Oturumlar, modeller, cron, skills, kanallar, loglar sayfalı tarayıcı kontrol paneli | 8:04 | Welcome to your Hermes dashboard. This is your agent's control room · kanıt: yok |
| Skills | yok | skill | yok | Ajanın kendi yazdığı veya Skills Hub'dan indirilen yeniden kullanılabilir prosedürler | 1:23 | it can write those steps down as a skill |
| Skills Hub | yok | skill | yok | Hermes'e indirilebilen binlerce skill'in göz atılabildiği katalog | 25:44 | At the bottom of this page, you can see skills hub |
| Google Workspace | yok | skill | yok | Takvim vb. için yerleşik skill; kurulum gerekmiyor | 25:44 | already built in is the Google Workspace, so we don't need to instal that |
| Kalıcı bellek | yok | teknik | yok | Tercihleri oturumlar arası saklayan memory aracı | 22:40 | you can see here it's saving that to memory · kanıt: yok |
| SOUL.md | yok | teknik | yok | Ajanın kimliğini ve davranışını tutan dosya | 24:43 | a file called SOUL.md that holds who it is and how it behaves |
| Cron / Scheduled jobs | yok | teknik | yok | Ajanın kendi kendine zamanlanmış görev çalıştırması | 26:14 | schedule itself, and then from then on, my phone buzzes · kanıt: yok |
| Alt ajanlar | yok | teknik | yok | delegate_task ile paralel çalışan yardımcı ajanlar | 32:07 | Ask it to split a job across sub-agents and it divides the work · kanıt: yok |
| Hermes Profiles | yok | teknik | yok | Masaüstünde ayrı yapılandırmalı bağımsız ortamlar (iş/kişisel) | 33:09 | there are profiles, so you can keep a work agent and a personal agent |
| OpenClaw | yok | iş akışı | yok | Yapılandırması Hermes'e içe aktarılabilen başka ajan aracı | 33:09 | if you're coming from OpenClaw, Hermes makes it easy to import |
| /model komutu | yok | ipucu | yok | Telegram'da sağlayıcı ve modeli değiştirme komutu | 29:14 | type a command /model · kanıt: yok |
| hermes doctor | yok | CLI | yok | Web konsolunda tam sağlık raporu veren komut | 31:26 | You can use the command Hermes Doctor, which will print a full health report |
| Claude Opus | yok | iş akışı | yok | Daha güçlü görev için modelin Opus 5'e değiştirilmesi örneği | 29:14 | let's say we wanted to use something like Opus 5 for a task |
| uv | yok | CLI | yok | Ajanın YouTube skill'i için bağımlılık kurarken kullandığı Python paket aracı | 26:16 | Ekran: 'Ran uv pip install yt-dlp' (karede: kanıttan) Ekran: 'Ran uv pip install yt-dlp' |
| yt-dlp | yok | CLI | yok | Ajanın YouTube araması için kurduğu bağımlılık | 26:18 | Ekran: 'Ran uv pip install yt-dlp 849ms' (karede: kanıttan) Ekran: 'Ran uv pip install yt-dlp 849ms' |
| youtube-transcript-api | yok | teknik | yok | YouTube altyazısı çekmek için ajanın kurduğu kütüphane | 26:16 | Ekran: from youtube_transcript_api import YouTubeTranscriptApi (karede: kanıttan) Ekran: from youtube_transcript_api import YouTubeTranscriptApi |
| Telegram QR kurulumu | yok | teknik | yok | BotFather'sız, QR okutarak bot oluşturma akışı | 14:06 | Ekran: 'Scan a QR code and confirm in Telegram. Hermes creates the bot' · kanıt: kare (karede: Ekran: 'Scan a QR code and confirm in Telegram. Hermes creates the bot') |
| Browser Use | yok | teknik | yok | Hermes'in tarayıcı aracı (browser_exec); ajan web'de gezinip sayfa okuyor, araştırma görevinde kullanılıyor. | 13:02 | Hermes sohbet ekranında 'browser-use: browser_exec' satırı görünüyor (karede: Hermes Agent v0.20.1 sohbet başlangıç ekranında araç listesinde 'browser-use: browser_exec' satırı.) |
| Python | yok | teknik | yok | Ajanın execute_code aracıyla çalıştırdığı programlama dili; kurulumda Python sanal ortamı da kullanılıyor. | 16:50 | execute_code — run Python that can chain Hermes tools (karede: Telegram'daki araç listesi mesajında 'execute_code — run Python' satırı.) |
| youtube-content | yok | skill | yok | Hermes skill'i: YouTube'da AI trend araması yapıp yalnız yeni videoları raporlayan skill (ajan yazdı). | 26:22 | skills/media/youtube-content/scripts/fetch_transcript.py (karede: Ajanın yazdığı skill yolu 'skills/media/youtube-content/scripts/fetch_transcript.py' ve açıklama 'Use for recurring YouTube AI trend checks. Reports only new.') |
| arXiv | yok | skill | yok | Hermes'in yerleşik arXiv skill'i; makale araması ve son makaleleri çekmek için curl ile arXiv API'sini kullanıyor. | 24:32 | export.arxiv.org/api/query ve 'Latest 10 papers in cs.AI' örneği (karede: Capabilities sayfasında 'arxiv — Research' skill'i seçili; içerikte export.arxiv.org API örnekleri.) |
| Tercih öncesi varsayılan çıktıyı görmek | yok | prompt | yok | Remote çalışanlar için verimlilik alışkanlıkları hakkında kısa bir yazı yaz. | 22:40 | kaynak: altyazı |
| Kalıcı bellek tercihi öğretme | yok | prompt | yok | Çok uzun; kısa, vurucu cümleler, en fazla üç paragraf, başlık ve madde işareti yok. Bunu tercih olarak kaydet. | 23:00 | kaynak: altyazı |
| Aynı oturumda tercihin uygulandığını doğrulama | yok | prompt | yok | Evden çalışırken odaklanmayı yönetme hakkında yazı yaz. | 23:42 | kaynak: altyazı |
| Yeni oturumda tercihin kalıcılığını sınama | yok | prompt | yok | Plajı bol en iyi Avrupa destinasyonları hakkında kısa yazı yaz. | 24:00 | kaynak: altyazı |
| Ajanın kendi skill'ini yazıp cron ile zamanlaması | yok | prompt | yok | YouTube'da yapay zekâ verimlilik trendlerini izle; kontrol için kendine skill yaz, gösterdiklerini takip et, birkaç saatte bir zamanla, yalnız yeni bir şey olunca mesaj at. | 26:14 | kaynak: altyazı |
| Alt ajanlarla paralel çalışma | yok | prompt | yok | Lizbon'da üç günlük plan yap; dört alt ajan: kalınacak mahalle, yemek, günübirlik gezi, ulaşım; sonunda tek rota ver. | 32:07 | kaynak: altyazı |
| OpenClaw'dan Hermes'e geçiş | yok | prompt | yok | OpenClaw yapılandırmamı içe aktarmak istiyorum, bana yol gösterir misin? | 33:09 | kaynak: altyazı |
| Ajanın tarayıcı ile araştırma yapmasını denemek | yok | prompt | yok | En iyi üç ayaklı çalışma masasını araştır ve tek paragraflık karşılaştırma ver. | 17:37 | kaynak: altyazı |
## Açıklama bağlantıları
- https://meticsmedia.com/hermes-JPY — Hostinger Hermes VPS indirim bağlantısı · aday: evet (Hostinger) · Hostinger VPS hizmetine yönlendiriyor; videoda kullanılan servis, indirim kodu ve yönlendirme var. · sınıf: affiliate
- https://hermes-agent.nousresearch.com — Hermes Agent ana sayfası · aday: evet (Hermes Agent) · Videoda anlatılan ana araç. · sınıf: diğer
- https://hermes-agent.nousresearch.com/docs/getting-started/installation — Hermes kurulum dokümanı · aday: evet (Hermes Agent) · Hermes Agent'ın kurulum belgesi, izleyici kullanabilir. · sınıf: diğer
- https://github.com/NousResearch/hermes-agent — Hermes Agent GitHub deposu · aday: evet (Hermes Agent) · Videodaki aracın kaynak deposu. · sınıf: diğer
- https://openrouter.ai — OpenRouter · aday: evet (OpenRouter) · Videoda model erişimi için kullanılan servis. · sınıf: diğer
- https://telegram.org/apps — Telegram indirme sayfası · aday: evet (Telegram) · Videoda kullanılan Telegram'ı indirme bağlantısı. · sınıf: diğer
- https://agentskills.io — Agent Skills standart sayfası · aday: hayır · Videoda gösterilmeyen/anlatılmayan, yalnız açıklamada geçen referans sayfa; skill kavramıyla ilgili genel bilgi. · sınıf: diğer
- https://meticsmedia.com/deals — Kanalın fırsatlar sayfası · aday: hayır · Referans/kampanya sayfası, videoda kullanılan araç değil. · sınıf: diğer
- https://youtu.be/XNcKUSL1CTE — Yazarın 'Ultimate Beginner's Guide to Hermes Agent' videosu · aday: hayır · Başka bir video; araç ya da servis değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://hermes-agent.nousresearch.com/install.sh / bash | Hermes Agent'ı macOS/Linux'ta terminalden kurar (ekranda gösterildi, çalıştırılmadı) (karede: Hermes Agent sitesindeki 'Install via terminal' kutusunda curl install.sh komutu) | 18:34 | kare |
| hermes auth add nous | Nous Portal ile OAuth girişi ekler (karede: Keys sayfasında Nous Portal altında komut) | 11:08 | kare |
| hermes auth add openai-codex | ChatGPT/Codex aboneliği ile giriş ekler (karede: Keys sayfasında ChatGPT or Codex Subscription altında komut) | 11:08 | kare |
| hermes auth add anthropic | Anthropic OAuth girişi ekler (karede: Anthropic OAuth satırı altında komut) | 11:12 | kare |
| hermes model | Sağlayıcı ve model seçme komutu (karede: Hata: No inference provider configured. Run 'hermes model') | 12:56 | kare |
| hermes setup | İlk kurulum sihirbazını çalıştırır (karede: Setup Required: /setup tam ilk kurulum sihirbazı) | 8:52 | kare |
| /model | Telegram'da sağlayıcı ve model değiştirir | 29:14 | altyazı |
| /sethome | Telegram sohbetini cron sonuçları için ana kanal yapar | 15:47 | altyazı |
| hermes gateway start | Ağ geçidini başlatır (karede: Channels sayfası notu: start the gateway with hermes gateway start) | 14:32 | kare |
| hermes doctor | Tam sağlık raporu yazdırır | 31:26 | altyazı |
| uv pip install yt-dlp | Ajanın YouTube işi için kurduğu bağımlılık (karede: Ajan çıktısında 'Ran uv pip install yt-dlp') | 26:18 | kare |
| hermes auth add <sağlayıcı> (örn. hermes auth add nous) | Seçilen sağlayıcı için OAuth girişi başlatır (ör. nous, openai-codex, qwen-oauth, xai-oauth). (karede: Keys sayfasında 'hermes auth add nous', 'hermes auth add openai-codex' gibi komutlar kopyalanabilir biçimde listeleniyor.) | 11:08 | kare |
| /help | Sohbette kullanılabilir komutların listesini gösterir. (karede: Hermes sohbet ekranında 'Setup Required' bölümünde '/help for commands' yazısı.) | 8:52 | kare |
| curl -sL https://www.nytimes.com/ (ajanın sayfa okuma çağrısı) | Ajan, araştırma için haber sitesi sayfasını indirir. (karede: Telegram'da ajanın shell çağrısı 'curl -sL https://www.nytimes.com/...' olarak görünüyor.) | 17:08 | kare |
| uv pip install --system youtube-transcript-api | youtube-transcript-api kütüphanesini sistem Python'una kurar. (karede: Ajan çıktısında 'Ran uv pip install --system youtube-transcript-api 1.1s' satırı.) | 26:16 | kare |
| python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print('ok')" | Kütüphanenin doğru kurulup içe aktarılabildiğini doğrular. (karede: Ajan çıktısında 'Ran python3 -c ... print(ok)' satırı ve 2.4s süre.) | 26:16 | kare |
| uv run python skills/media/youtube-content/scripts/fetch_transcript.py "<video-url>" --text-only | YouTube videosunun transkriptini metin olarak çeker; skill'in trend taramasında kullanılır. (karede: Ajan çıktısında 'Running uv run python skills/media/youtube-content/scripts/fetch_transcript.py ... --text-only' satırı.) | 26:22 | kare |
| curl -s 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10' | arXiv API'sinden cs.AI kategorisinin son 10 makalesini çeker (arXiv skill örneği). (karede: arXiv skill içeriğinde 'Latest 10 papers in cs.AI' başlığı ve curl komutu görünüyor.) | 24:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Hermes Agent MIT lisanslı, ücretsiz; yalnız model ve sunucu için ödeme yapılır. | 1:23 | özellik |
| Küçük bir bulut sunucu yaklaşık 6$/ay'dan başlıyor. | 2:13 | sayısal |
| KVM 1 planı bir ajanı rahatça çalıştırır; sonradan yükseltilebilir. | 4:02 | öneri |
| İndirim kuponu için en az 12 aylık dönem gerekir; 30 gün para iade garantisi var. | 5:02 | sayısal |
| Önceden işaretli 'Ready to Use AI' kutusunu kaldırmak öneriliyor; yaklaşık 12$ kredi ekliyor. | 5:02 | öneri |
| Nous Portal yaklaşık 20$/ay sabit ücret; OpenRouter'da 5$ haftalarca yeter. | 12:41 | karşılaştırma |
| 105 istekte toplam harcama 13 sent; yaklaşık dört milyon token, istek başına ~38.000 token. | 28:13 | sayısal |
| Okunan içeriğin dörtte üçü önbellekten geldi; 5$ yaklaşık 4.000 mesaja yeter. | 29:14 | sayısal |
| Telegram QR kodu yaklaşık üç dakika sonra sona erer. | 13:45 | özellik |
| Hermes 20+ platformu destekler; Telegram anında QR akışı sunan kanal. | 13:45 | özellik |
| Bir oturumdaki düzeltme tercih olarak bellekte saklanır ve yeni oturumda da geçerli olur. | 23:42 | özellik |
| Sunucuda çalıştırmak, ajanın kişisel dosyalara erişmesini önler; riskli işlerde izin ister. | 3:15 | özellik |
| Skills Hub 90.700'den fazla skill barındırıyor. | 25:00 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Hermes Agent | Hermes Agent | Ana araç, Nous Research ajanı |
| konuşma 0:00 | ChatGPT | aday değil: genel kavram | Yalnız 'ChatGPT with extra steps' karşılaştırması, kullanılmadı |
| konuşma 4:02 | Hostinger | Hostinger | VPS ve tek tıkla şablon |
| kare 4:40 | nexos.ai / Ready to Use AI | aday değil: sponsor/reklam | Hostinger'ın önceden işaretli ek paketi, kullanılmadı, kaldırıldı |
| kare 5:46 | Oxylabs AI Studio API Key | aday değil: konu dışı | Formda boş bırakılan isteğe bağlı alan |
| kare 6:28 | Traefik | Traefik | Docker Manager'da HTTPS önerisi; konuşmada reverse proxy |
| konuşma 7:04 | Docker Manager | Docker Manager | Elle dağıtım ve yeniden başlatma için kullanıldı |
| kare 7:12 | n8n (Hostinger uygulaması) | aday değil: konu dışı | Yalnız Hostinger menüsünde görünüyor, kullanılmadı |
| kare 7:28 | Katalogdaki diğer şablonlar (1Backend, 2FAuth, Ackee vb.) | aday değil: konu dışı | Yalnız katalog listesinde |
| konuşma 9:37 | OpenRouter | OpenRouter | Model erişimi için kuruldu |
| konuşma 11:38 | DeepSeek V4 Flash | DeepSeek V4 Flash | Ana model seçildi |
| kare 11:08 | Keys sayfasındaki diğer sağlayıcılar (Qwen, MiniMax, Kimi, Hugging Face, Xiaomi MiMo) | aday değil: konu dışı | Yalnız listede görünüyor, kullanılmadı |
| kare 11:46 | Model listesi (Claude Haiku, Sonnet 5, Gemini 3.7 Flash, Kimi K3, GPT-5.5 Pro vb.) | aday değil: konu dışı | Yalnız OpenRouter listesinde görünüyor |
| konuşma 12:41 | Nous Portal | Nous Portal | Alternatif abonelik olarak anlatıldı |
| konuşma 13:45 | Telegram | Telegram | QR ile bot kuruldu |
| konuşma 13:45 | Discord, Slack, WhatsApp, e-posta | aday değil: konu dışı | Yalnız desteklenen kanallar olarak sayıldı |
| konuşma 16:37 | Alt ajanlar | Alt ajanlar | Lizbon örneğinde çalıştırıldı |
| konuşma 18:20 | Hermes masaüstü uygulaması | Hermes masaüstü uygulaması | Kuruldu ve uzak ağ geçidine bağlandı |
| kare 19:14 | Sağlayıcı kurulum listesi (Fireworks AI, Alibaba Cloud, xAI Grok vb.) | aday değil: konu dışı | Yalnız ilk açılış ekranında; 'sonra seçeceğim' denildi |
| konuşma 22:40 | Kalıcı bellek | Kalıcı bellek | Tercih kaydı gösterildi |
| konuşma 24:43 | SOUL.md | SOUL.md | Kimlik dosyası olarak anlatıldı |
| konuşma 24:43 | Skills | Skills | Capabilities sayfasında gezildi |
| konuşma 25:44 | Skills Hub | Skills Hub | Hub tarayıcısı açıldı |
| konuşma 25:44 | Google Workspace | Google Workspace | Yerleşik skill olarak arandı |
| kare 24:00 | arxiv skill, claude-code, codex, opencode, comfyui, claude-design skill'leri | aday değil: konu dışı | Yalnız skill listesinde görünüyor; arxiv içeriği açıldı fakat kullanılmadı |
| kare 25:00 | Skills Hub kaynakları (Anthropic, HuggingFace, gstack, skills.sh) | aday değil: konu dışı | Yalnız hub filtre listesinde |
| konuşma 26:14 | Cron / Scheduled jobs | Cron / Scheduled jobs | Ajan dört saatte bir işi zamanladı |
| kare 26:16 | uv | uv | Ajan uv ile bağımlılık kurdu |
| kare 26:18 | yt-dlp | yt-dlp | Ajan tarafından kuruldu |
| kare 26:16 | youtube-transcript-api | youtube-transcript-api | Ajan tarafından kuruldu |
| kare 26:28 | Rapordaki araçlar (Wispr Flow, Granola, Veo 3.1, n8n, NotebookLM) | aday değil: konu dışı | Yalnız ajanın YouTube raporunda geçen içerik |
| kare 27:06 | Bolt, lonelyoctopus.com | aday değil: sponsor/reklam | Rapordaki video önizlemesinde görünen reklam/içerik |
| konuşma 28:13 | OpenRouter Activity | OpenRouter | Maliyet sayfası gösterildi |
| konuşma 29:14 | Claude Opus 5 | Claude Opus | Model değiştirme örneği |
| konuşma 29:14 | /model komutu | /model komutu | Telegram'da model değiştirildi |
| kare 29:32 | openwakeword, onnxruntime | aday değil: konu dışı | Yalnız loglardaki hata mesajında geçiyor |
| konuşma 31:26 | hermes doctor | hermes doctor | Web konsolunda anılan sağlık komutu |
| konuşma 33:09 | Hermes Profiles | Hermes Profiles | Profil oluşturma gösterildi |
| konuşma 33:09 | OpenClaw | OpenClaw | İçe aktarma promptu denendi |
| açıklama | agentskills.io | aday değil: konu dışı | Videoda anlatılmayan referans bağlantı |
| açıklama | meticsmedia.com/deals | aday değil: sponsor/reklam | Kanalın kampanya sayfası |
| yorum | Discord (yorumcu önerisi) | aday değil: konu dışı | Yorumda Telegram yerine öneriliyor, videoda kullanılmadı |
| yorum | Infinity Free, Llama/Ollama, Astra | aday değil: konu dışı | Yalnız izleyici yorumlarında |
| yorum | Twitter yanıt botu, Grok videosu isteği | aday değil: konu dışı | İzleyici istekleri |
| linkli sayfa | nymag.com (thecut, vulture, curbed, grubstreet) | aday değil: konu dışı | Ajanın araştırma sayfasında görünen siteler |
| linkli sayfa | replit.com, cline.bot | aday değil: konu dışı | OpenRouter sayfasındaki uygulama listesinde anılıyor |
## Kareden okunanlar
- 4:02: Hostinger sayfası: 'Up to 73% off for Hermes Agent', 'Deploy Hermes Agent in one click installation', 5.84$/ay, Choose plan
- 4:20: KVM 1 5.84$/ay (1 vCPU, 4 GB RAM, 50 GB NVMe), KVM 2 7.91$, KVM 4 11.69$, KVM 8 23.39$; 'MM–HERMES' coupon applied
- 4:40: Sepet: KVM 1, 24 ay; 'Ready to Use AI' işaretli (10 nexos.ai credits); mm-hermes -10%
- 5:46: Hermes Agent configuration: ADMIN_USERNAME 'hermes', ADMIN_PASSWORD (gizli), Nexos API Key ve Oxylabs AI Studio API Key boş
- 7:28: Hostinger Docker Manager kataloğu, 1017 şablon, arama kutusu
- 8:52: Hermes sohbetinde 'Setup Required' ve model sağlayıcı yok hatası; model claude-opus-4.6
- 11:08: Keys sayfası: Nous Portal, ChatGPT/Codex, Qwen, MiniMax, xAI Grok, GitHub Copilot için OAuth girişleri
- 11:44: Set Main Model penceresi: openrouter · 34 models, nous 0 models
- 13:28: Channels sayfası: Telegram, Discord, Slack, Mattermost, Matrix; 0 of 33 channels configured
- 14:14: Telefonda Create Bot: NousHostedHermesBot, bot adı Hermes Agent; yanında QR kodu
- 16:50: Telegram'da araç listesi: memory, skill_view, browser_exec, delegate_task, cronjob, text_to_speech, todo, clarify
- 18:34: hermes-agent.nousresearch.com: 'The agent that grows with you', Download for Mac OS ve curl install.sh komutu
- 19:32: Gateway Connection: Local gateway, Hermes Cloud, Remote gateway, Connect via SSH
- 24:00: Capabilities: Skills 77, Tools 24, MCP; hermes-agent skill, claude-code skill
- 25:00: Skills Hub: 90.700 skill, 82 built-in; Anthropic 17, HuggingFace 25, gstack 53, skills.sh 19967
- 26:16: Ajanın kurulum satırları: uv pip install youtube-transcript-api, uv pip install yt-dlp
## Belirsizlikler
- Ekrandaki model adları (Opus 4.6, Opus 5, GPT-5.6 vb.) listede göründü; yalnız DeepSeek V4 Flash ve kısaca Opus 5 gerçekten seçildi.
- Videoda 18:34 karesinde gösterilen curl install.sh komutu çalıştırılmadı, yalnız ekranda görüldü.
- Sahip yorumuna göre Telegram kurulumu video çekildikten sonra değişmiş; 'Save and Restart' adımı güncel olmayabilir.
- 'Ready to Use AI' ile gelen nexos.ai servisi ve Oxylabs AI Studio anahtarı kullanılmadı; yalnız formda görüldü.
- Telegram'da 'telegram setup' ve Mattermost, Matrix gibi kanallar yalnız listede göründü, kullanılmadı.
- Altyazı 'Opus 5' diyor; kare listesinde 'claude-opus-5' ve 'Opus 4.8' birlikte görünüyor.
- Site/landing içerik videosu değil; site_ui boş bırakıldı.
- Ekrandaki kanal yorumlarındaki Astra rotası ve Infinity Free sorusu videoda gösterilmedi.
## Atlanan segment oranı
0/40 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://meticsmedia.com/hermes-JPY | 4:12 | ekran | evet |
| hostinger.com/applications/hermes-agent | 4:02 | ekran | evet |
| cart.hostinger.com/pay/53f26147-9e40-4641-a53c-acaff492bd43 | 4:40 | ekran | evet |
| auth.hostinger.com/register | 5:32 | ekran | evet |
| hpanel.hostinger.com/purchase-new-vps/application-deploy | 5:46 | ekran | evet |
| hpanel.hostinger.com/vps/1903879/docker-manager | 6:24 | ekran | evet |
| hpanel.hostinger.com/vps/1903879/docker-manager/catalog | 7:28 | ekran | evet |
| nexos.ai | 4:40 | ekran | hayır |
| openrouter.ai | 9:37 | ses | evet |
| https://openrouter.ai/api/v1/chat/completions | 9:54 | ekran | hayır |
| openrouter.ai/workspaces/default/keys | 10:36 | ekran | evet |
| openrouter.ai/activity | 27:30 | ekran | evet |
| hermes-agent.nousresearch.com | 18:20 | ses | evet |
| https://hermes-agent.nousresearch.com/install.sh | 18:34 | ekran | evet |
| hermes-assets.nousresearch.com/Hermes-Setup.dmg | 18:42 | ekran | evet |
| https://github.com/NousResearch/hermes-agent | 24:00 | ekran | evet |
| https://hermes-agent.nousresearch.com/docs/getting-started/installation | açıklama | açıklama | evet |
| https://telegram.org/apps | açıklama | açıklama | evet |
| https://agentskills.io | açıklama | açıklama | hayır |
| https://meticsmedia.com/deals | açıklama | açıklama | hayır |
| https://youtu.be/XNcKUSL1CTE | açıklama | yorum | hayır |
| https://youtube.com/watch?v=162CvEUwVS58 | 26:22 | ekran | hayır |
| https://export.arxiv.org/api/query | 24:32 | ekran | hayır |
| skills.sh | 25:00 | ekran | hayır |
| https://www.hostinger.com | 4:02 | ekran | evet |
| https://hpanel.hostinger.com/vps/1903879/docker-manager/credentials | 7:44 | ekran | evet |
| https://arxiv.org/abs/2402.03300 | 24:32 | ekran | hayır |
| https://www.nytimes.com/ | 17:08 | ekran | hayır |
| https://nymag.com/ | 17:08 | ekran | hayır |
| https://t.me | 0:02 | ekran | evet |
| https://www.lonelyoctopus.com/ | 27:06 | ekran | hayır |
| https://hermes.app/dashboard | 17:18 | ekran | hayır |
| https://hermes-agent-5x5l.srv1903879.hstgr.cloud/cron | 8:40 | ekran | evet |
| https://meticsmatt.com | 5:40 | ekran | hayır |
## İş akışı
- 1. adım — Hostinger Hermes sayfasında KVM 1 planı seçildi — araçlar: Hostinger
- 2. adım — Faturalama süresi seçilip 'Ready to Use AI' kutusu kaldırıldı, kupon doğrulandı — araçlar: Hostinger
- 3. adım — Hesap açıldı ve ödeme tamamlandı — araçlar: Hostinger
- 4. adım — Admin kullanıcı adı ve şifre kaydedilip Deploy'a basıldı — araçlar: Hostinger, Docker Manager
- 5. adım — Gerekirse VPS > Docker Manager > Catalog üzerinden Hermes Agent elle dağıtıldı — araçlar: Docker Manager
- 6. adım — Hermes web paneline giriş yapıldı, sayfalar tanıtıldı — araçlar: Hermes web paneli
- 7. adım — OpenRouter hesabı açıldı, kredi eklendi, haftalık 10$ limit konuldu — araçlar: OpenRouter
- 8. adım — Anahtar Keys sayfasına girilip ana model DeepSeek V4 Flash seçildi, sohbetle test edildi — araçlar: Hermes web paneli, OpenRouter, DeepSeek V4 Flash
- 9. adım — Channels'tan QR ile Telegram botu oluşturulup /sethome ayarlandı — araçlar: Telegram, Hermes web paneli
- 10. adım — Telegram'dan araçlar soruldu ve ayaklı masa araştırması istendi — araçlar: Telegram, Hermes Agent
- 11. adım — Masaüstü uygulaması indirilip kuruldu — araçlar: Hermes masaüstü uygulaması
- 12. adım — Uygulama Remote gateway ile sunucu adresine bağlandı — araçlar: Hermes masaüstü uygulaması, Hermes web paneli
- 13. adım — Üslup düzeltmesi bellekte kaydedilip yeni oturumda doğrulandı — araçlar: Kalıcı bellek, Hermes masaüstü uygulaması
- 14. adım — Capabilities ve Skills Hub gezildi — araçlar: Skills Hub, Google Workspace
- 15. adım — Ajan YouTube skill'i yazıp dört saatte bir cron olarak zamanladı — araçlar: Cron / Scheduled jobs, uv, yt-dlp, youtube-transcript-api
- 16. adım — OpenRouter Activity'den maliyet kontrol edildi, model değiştirme gösterildi — araçlar: OpenRouter, /model komutu
- 17. adım — Loglar, gateway yeniden başlatma ve Docker restart gösterildi — araçlar: Hermes web paneli, Docker Manager, hermes doctor
- 18. adım — Alt ajanlarla Lizbon planı, profiller ve OpenClaw içe aktarma gösterildi — araçlar: Alt ajanlar, Hermes Profiles, OpenClaw
## Promptlar
- Tercih öncesi varsayılan çıktıyı görmek — Remote çalışanlar için verimlilik alışkanlıkları hakkında kısa bir yazı yaz.
- Kalıcı bellek tercihi öğretme — Çok uzun; kısa, vurucu cümleler, en fazla üç paragraf, başlık ve madde işareti yok. Bunu tercih olarak kaydet.
- Aynı oturumda tercihin uygulandığını doğrulama — Evden çalışırken odaklanmayı yönetme hakkında yazı yaz.
- Yeni oturumda tercihin kalıcılığını sınama — Plajı bol en iyi Avrupa destinasyonları hakkında kısa yazı yaz.
- Ajanın kendi skill'ini yazıp cron ile zamanlaması — YouTube'da yapay zekâ verimlilik trendlerini izle; kontrol için kendine skill yaz, gösterdiklerini takip et, birkaç saatte bir zamanla, yalnız yeni bir şey olunca mesaj at.
- Alt ajanlarla paralel çalışma — Lizbon'da üç günlük plan yap; dört alt ajan: kalınacak mahalle, yemek, günübirlik gezi, ulaşım; sonunda tek rota ver.
- OpenClaw'dan Hermes'e geçiş — OpenClaw yapılandırmamı içe aktarmak istiyorum, bana yol gösterir misin?
- Ajanın tarayıcı ile araştırma yapmasını denemek — En iyi üç ayaklı çalışma masasını araştır ve tek paragraflık karşılaştırma ver.
ikinci göz KAPALI: --ikinci-goz yok
