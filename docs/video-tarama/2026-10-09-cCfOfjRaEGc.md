# free-claude-code: Run Claude Code Without Paying Anthropic
## Künye
free-claude-code: Run Claude Code Without Paying Anthropic · Hungry Labs · süre: 0:18 · en-orig · https://youtu.be/cCfOfjRaEGc · şema 2
motor: parti 2026-10-09-short-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (5)
claude-sonnet-5-5: claude-sonnet-5-5 · 18341 tk · claude-haiku-5-5: claude-haiku-5-5 · 45171 tk
## Özet
18 saniyelik kısa video, free-claude-code adlı GitHub deposunu tanıtıyor. Bu proxy, Claude Code'dan gelen Anthropic Messages API trafiğini NVIDIA NIM, OpenRouter, DeepSeek, LM Studio, llama.cpp veya Ollama gibi başka sağlayıcılara yönlendiriyor. Böylece aynı arayüz ve iş akışıyla Anthropic'e ödeme yapılmıyor. README'deki kurulum adımları (uv, Python 3.14, .env, uvicorn) ekranda gösteriliyor. Depo yaklaşık 19.000 yıldıza sahip.
## Bölümler
- 0:00 Sorun: Claude Code maliyeti ve proxy tanıtımı
- 0:10 README Quick Start: kurulum adımları
- 0:15 19 bin yıldız ve açıklamadaki bağlantı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| free-claude-code | yok | CLI | https://github.com/Alishahryar1/free-claude-code | Claude Code'un Anthropic API trafiğini başka sağlayıcılara yönlendiren proxy | 0:00 | This proxy sits between your terminal and any model provider you want (karede: GitHub deposu Alishahryar1 / free-claude-code, başlık 'Free Claude Code', 'CLAUDE CODE FOR FREE' yazısı) |
| Claude Code | yok | CLI | yok | Proxy'nin arkasında kullanılan Anthropic kodlama aracı | 0:00 | README: Use Claude Code CLI, VS Code, JetBrains ACP, or chat bots (karede: README başlığı altında 'Use Claude Code CLI, VS Code, JetBrains ACP...' metni) |
| NVIDIA NIM | yok | CLI | yok | Varsayılan sağlayıcı arka ucu | 0:10 | For the default NVIDIA NIM path: NVIDIA_NIM_API_KEY (karede: Edit .env bölümü: NVIDIA_NIM_API_KEY, MODEL=nvidia_nim/z-ai/glm4.7) |
| OpenRouter | yok | CLI | yok | Desteklenen sağlayıcı arka ucu | 0:10 | Six provider backends: NVIDIA NIM, OpenRouter, DeepSeek... (karede: What You Get listesinde altı sağlayıcı sayılıyor) |
| DeepSeek | yok | CLI | yok | Desteklenen sağlayıcı arka ucu | 0:10 | Six provider backends: NVIDIA NIM, OpenRouter, DeepSeek... (karede: What You Get listesinde sağlayıcılar arasında DeepSeek) |
| LM Studio | yok | CLI | yok | Yerel model sağlayıcı arka ucu | 0:10 | Six provider backends: NVIDIA NIM, OpenRouter, DeepSeek, LM Studio (karede: What You Get listesinde LM Studio) |
| llama.cpp | yok | CLI | yok | Yerel model sağlayıcı arka ucu | 0:10 | LM Studio, llama.cpp, and Ollama (karede: What You Get listesinde llama.cpp) |
| Ollama | yok | CLI | yok | Yerel model sağlayıcı arka ucu | 0:10 | llama.cpp, and Ollama (karede: What You Get listesinde Ollama) |
| uv | yok | CLI | yok | Python paket/ortam yöneticisi; kurulum ve sunucu çalıştırmada kullanılıyor | 0:10 | uv self update; uv python install 3.14 (karede: Install Requirements bölümünde uv komutları) |
| Python 3.14 | yok | teknik | yok | Proxy'nin gerektirdiği Python sürümü | 0:10 | install uv and Python 3.14 (karede: Install Requirements: 'Install Claude Code, then install uv and Python 3.14') |
| Uvicorn | yok | CLI | yok | Proxy sunucusunu çalıştıran ASGI sunucusu | 0:10 | uv run uvicorn server:app --host 0.0.0.0 --port 8082 (karede: 3. Start The Proxy altında uvicorn komutu) |
| Anthropic Messages API | yok | teknik | yok | Proxy'nin taklit ettiği ve yönlendirdiği API protokolü | 0:00 | routes Anthropic Messages API traffic from Claude Code (karede: README açıklama paragrafı) |
| Discord | yok | iş akışı | yok | Uzaktan kodlama oturumları için isteğe bağlı bot sarmalayıcı | 0:10 | Optional Discord or Telegram bot wrapper (karede: What You Get listesi maddesi) |
| Telegram | yok | iş akışı | yok | Uzaktan kodlama oturumları için isteğe bağlı bot sarmalayıcı | 0:10 | Optional Discord or Telegram bot wrapper (karede: What You Get listesi maddesi) |
| Whisper | yok | teknik | yok | İsteğe bağlı yerel sesli not transkripsiyonu | 0:10 | voice-note transcription through local Whisper or NVIDIA NIM (karede: What You Get son madde) |
| Pytest | yok | teknik | yok | Depoda test çerçevesi rozeti | 0:16 | TESTING PYTEST rozeti (karede: README rozet satırı: TESTING PYTEST) |
| Ruff | yok | teknik | yok | Kod biçimlendirme rozeti | 0:16 | CODE FORMATTING RUFF rozeti · kanıt: kare (karede: README rozet satırı: CODE FORMATTING RUFF) |
| Loguru | yok | teknik | yok | Loglama kütüphanesi rozeti | 0:16 | LOGGING LOGURU rozeti (karede: README rozet satırı: LOGGING LOGURU) |
| ty | yok | teknik | yok | Tür denetimi rozeti | 0:16 | TYPE CHECKING TY rozeti · kanıt: kare (karede: README rozet satırı: TYPE CHECKING TY) |
| GitHub | yok | teknik | yok | Deponun barındığı platform | 0:00 | GitHub depo sayfası gösteriliyor (karede: GitHub depo ana sayfası) |
| curl | yok | CLI | yok | macOS/Linux'ta uv yükleyicisini indirmek için kullanılıyor | 0:10 | curl -LsSf https://astral.sh/uv/install.sh / sh (karede: macOS/Linux kod bloğunda curl komutu) |
| PowerShell | yok | CLI | yok | Windows'ta uv kurulumu, .env kopyalama komutlarını çalıştırır | 0:10 | PowerShell uses: Copy-Item .env.example .env (karede: Windows PowerShell kod bloğu ve Copy-Item satırı) |
| Git | yok | CLI | yok | Depoyu yerel makineye klonlamak için kullanılıyor | 0:10 | git cl (ekranda kesik) ve cd free-claude-code (karede: Clone And Configure bölümünde kesik git clone satırı) |
| z-ai/glm4.7 | yok | teknik | yok | Varsayılan NVIDIA NIM modeli olarak .env dosyasında tanımlanıyor | 0:10 | MODEL="nvidia_nim/z-ai/glm4.7" (karede: Quick Start .env ayar kod bloğu) |
| VS Code | yok | teknik | yok | Proxy'nin desteklediği istemcilerden biri | 0:00 | Use Claude Code CLI, VS Code, JetBrains ACP, or chat bots through your own (karede: README tanıtım paragrafı) |
| JetBrains ACP | yok | teknik | yok | Proxy'nin desteklediği istemcilerden biri | 0:00 | Use Claude Code CLI, VS Code, JetBrains ACP, or chat bots through your own (karede: README tanıtım paragrafı) |
| README ekran görüntüsündeki örnek kod analizi isteği | yok | prompt | yok | Kod tabanını modülerlik, sınıf tasarımı, kapsülleme, optimizasyon, sadelik ve ölü kod açısından incele. | 0:16 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/Alishahryar1/free-claude-code — free-claude-code GitHub deposu · aday: evet (free-claude-code) · Videoda anlatılan ve izleyicinin kullanabileceği proxy aracının deposu · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -LsSf https://astral.sh/uv/install.sh / sh | macOS/Linux'ta uv'yi kurar (karede: macOS/Linux bölümünde curl komutu) | 0:10 | kare |
| powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/in... | Windows PowerShell'de uv'yi kurar (komut kesik görünüyor) (karede: Windows PowerShell bölümünde powershell komutu) | 0:10 | kare |
| uv self update | uv'yi günceller (karede: Her iki platform bölümünde uv self update) | 0:10 | kare |
| uv python install 3.14 | Python 3.14 kurar (karede: Her iki platform bölümünde uv python install 3.14) | 0:10 | kare |
| git clone ... && cd free-claude-code | Depoyu klonlar ve klasöre girer (komut kısmen kapalı) (karede: Clone And Configure bölümünde 'git cl' ve 'cd fre') | 0:11 | kare |
| cp .env.example .env | Örnek yapılandırmayı .env olarak kopyalar (karede: Clone And Configure kod bloğu) | 0:10 | kare |
| Copy-Item .env.example .env | PowerShell'de .env dosyasını oluşturur (karede: PowerShell uses: bölümü) | 0:10 | kare |
| uv run uvicorn server:app --host 0.0.0.0 --port 8082 | Proxy sunucusunu 8082 portunda başlatır (karede: 3. Start The Proxy altında komut satırı) | 0:10 | kare |
| git cl… (kesik; tam URL görünmüyor) | free-claude-code deposunu yerel makineye klonlar (karede: Clone And Configure kod bloğunda kesik git clone satırı) | 0:10 | kare |
| cd free-claude-code | Klonlanan depo dizinine geçer (karede: Clone And Configure kod bloğunda ikinci satır) | 0:11 | kare |
| MODEL="nvidia_nim/z-ai/glm4.7" | .env dosyasında varsayılan model olarak NVIDIA NIM üzerindeki z-ai/glm4.7 modelini ayarlar (karede: Quick Start .env ayar kod bloğu) | 0:10 | kare |
| NVIDIA_NIM_API_KEY=<kendi-anahtariniz> | .env dosyasında NVIDIA NIM API anahtarını tanımlar (değer kaydedilmedi) (karede: Quick Start .env ayar kod bloğu, anahtar satırı) | 0:10 | kare |
| ANTHROPIC_AUTH_TOKEN=<yerel-anahtar> | .env dosyasında Claude Code'un proxy'ye göndereceği yerel yetkilendirme değerini tanımlar (değer kaydedilmedi) (karede: Quick Start .env ayar kod bloğu, token satırı) | 0:10 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Code her düşünmede gerçek para harcar; proxy ile Anthropic'e ödeme yapılmaz. | 0:00 | karşılaştırma |
| Depo yaklaşık 19.000 yıldıza sahip ve hızla artıyor. | 0:15 | sayısal |
| Aynı arayüz ve iş akışı korunur. | 0:11 | özellik |
| Model başına yönlendirme: Opus, Sonnet, Haiku ve yedek trafik farklı sağlayıcılara gönderilebilir. | 0:10 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Cloud code costs real money every time your agent thinks |
| konuşma 0:00 | Anthropic | aday değil: genel kavram | so you never pay Anthropic a cent |
| konuşma 0:00 | Proxy | free-claude-code | This proxy sits between your terminal and any model provider |
| konuşma 0:15 | 19.000 yıldız | aday değil: genel kavram | 19,000 stars and climbing fast |
| kare 0:00 | GitHub | GitHub | GitHub depo sayfası |
| kare 0:00 | MIT license | aday değil: genel kavram | README: MIT license |
| kare 0:00 | Anthropic-compatible proxy | free-claude-code | README alt başlığı |
| kare 0:00 | VS Code, JetBrains ACP | aday değil: başka adayın parçası (free-claude-code) | Desteklenen istemci listesinde geçiyor; videoda kullanılmıyor |
| kare 0:00 | NVIDIA NIM | NVIDIA NIM | README sağlayıcı listesi ve .env |
| kare 0:00 | OpenRouter | OpenRouter | README sağlayıcı listesi |
| kare 0:00 | DeepSeek | DeepSeek | README sağlayıcı listesi |
| kare 0:00 | LM Studio | LM Studio | README sağlayıcı listesi |
| kare 0:00 | llama.cpp | llama.cpp | README sağlayıcı listesi |
| kare 0:00 | Ollama | Ollama | README sağlayıcı listesi |
| kare 0:16 | Pytest, Ruff, Loguru, ty rozetleri | Pytest, Ruff, Loguru, ty | README rozet satırı |
| kare 0:10 | uv | uv | uv self update, uv python install 3.14 |
| kare 0:10 | Python 3.14 | Python 3.14 | Install Python 3.14 |
| kare 0:10 | Uvicorn | Uvicorn | uv run uvicorn server:app |
| kare 0:10 | PowerShell | aday değil: başka adayın parçası (free-claude-code) | Windows kurulum komutlarının kabuğu |
| kare 0:10 | Git | aday değil: başka adayın parçası (free-claude-code) | git clone adımı |
| kare 0:10 | Claude Sonnet, Opus, Haiku | aday değil: başka adayın parçası (free-claude-code) | Model başına yönlendirme maddesinde yalnız adı geçiyor |
| kare 0:10 | Discord, Telegram | Discord, Telegram | Opsiyonel bot sarmalayıcı maddesi |
| kare 0:10 | Whisper | Whisper | Opsiyonel sesli not transkripsiyonu maddesi |
| kare 0:10 | Anthropic Messages API | Anthropic Messages API | README açıklaması |
| kare 0:16 | Star History | aday değil: konu dışı | README'deki yıldız grafiği bölümü |
| açıklama | GitHub repo bağlantısı | free-claude-code | https://github.com/Alishahryar1/free-claude-code |
| açıklama | #GitHub #OpenSource #ClaudeCode #AI #Free | aday değil: genel kavram | Etiketler |
| yorum | Kimi, ultracode | aday değil: konu dışı | Yorumcu kendi kullandığı modelleri anlatıyor; videoda yok |
| yorum | /login sorunu | aday değil: konu dışı | Yorumcunun Claude Code giriş şikâyeti |
## Kareden okunanlar
- 0:00: GitHub deposu Alishahryar1/free-claude-code, MIT license, 'CLAUDE CODE FOR FREE' başlığı, Issues 40, Pull requests 28
- 0:01: Aynı depo sayfası, 'Claude Code costs real money every time' altyazısı
- 0:10: Quick Start: curl/uv komutları, powershell kurulumu, cp .env.example .env, NVIDIA_NIM_API_KEY, MODEL=nvidia_nim/z-ai/glm4.7, ANTHROPIC_AUTH_TOKEN
- 0:16: README terminal görüntüsü, 'Link in description' altyazısı, Star History bölümü
- 0:17: Depo sayfası, 'CLAUDE CODE FOR FREE' başlığı
## Belirsizlikler
- Yorumlardan biri Claude Code'un /login istediğini söylüyor; proxy'nin bunu aşıp aşmadığı videoda gösterilmiyor.
- Yorumdaki Kimi, ultracode: videoda gösterilmiyor, yalnız yorumda geçiyor.
- Ekrandaki komutlar README'de gösteriliyor; videoda çalıştırılmıyor.
- Altyazıdaki 'Cloud code' büyük olasılıkla 'Claude Code' demek.
- Sözlükteki Codex, Descript, Inter eşleşmeleri bulanık ses eşleşmesi; videoda anlatılmıyor.
- Model adı karede 'glm4.7' okunuyor, OCR hatalı olabilir.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/Alishahryar1/free-claude-code | açıklama | açıklama | evet |
| https://github.com/Alishahryar1/free-claude-code | açıklama | yorum | evet |
| https://astral.sh/uv/install.sh | 0:10 | ekran | evet |
| https://astral.sh/uv/in | 0:10 | ekran | evet |
## İş akışı
- 1. adım — GitHub'da free-claude-code deposu açılır ve dosya yapısı gösterilir — araçlar: GitHub, free-claude-code
- 2. adım — README'de proxy'nin Anthropic Messages API trafiğini sağlayıcılara yönlendirdiği gösterilir — araçlar: free-claude-code, Anthropic Messages API
- 3. adım — Gereksinimler kurulur: Claude Code, uv, Python 3.14 — araçlar: Claude Code, uv, Python 3.14
- 4. adım — Depo klonlanır ve .env.example .env olarak kopyalanır — araçlar: Git, PowerShell
- 5. adım — .env içinde sağlayıcı, model ve yerel token seçilir — araçlar: NVIDIA NIM
- 6. adım — Proxy uvicorn ile başlatılır — araçlar: uv, Uvicorn
- 7. adım — Claude Code terminalde proxy üzerinden kod analizi örneği çalıştırır — araçlar: Claude Code, free-claude-code
- 8. adım — Star History ve açıklamadaki bağlantı gösterilir — araçlar: GitHub
## Promptlar
- README ekran görüntüsündeki örnek kod analizi isteği — Kod tabanını modülerlik, sınıf tasarımı, kapsülleme, optimizasyon, sadelik ve ölü kod açısından incele.
