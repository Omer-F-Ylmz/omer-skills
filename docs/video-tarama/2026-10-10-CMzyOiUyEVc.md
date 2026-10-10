# How to Use Claude Code for FREE in 2026 | No Subscription, No GPU | OmniRoute + Kiro AI
## Künye
How to Use Claude Code for FREE in 2026 | No Subscription, No GPU | OmniRoute + Kiro AI · PROMPTA HUB by Daniel Voss · süre: 6:16 · en-orig · https://youtu.be/CMzyOiUyEVc · şema 2
motor: parti 2026-10-10-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 49148 tk · claude-haiku-5-5: claude-haiku-5-5 · 165774 tk
## Özet
Video, Claude Code'u abonelik ve GPU olmadan ücretsiz kullanmak için OmniRoute yerel proxy'si ile Kiro AI sağlayıcısını birleştirmeyi gösteriyor. Adımlar: Node.js kurulumu, OmniRoute'un npm ile kurulup çalıştırılması, Kiro AI'ya AWS Builder ID ile bağlanma, API Manager'dan anahtar üretme, Claude Code kurulumu, ortam değişkenlerini içeren bir .bat dosyası yazma, klasörü PATH'e ekleme ve 'cc' komutuyla başlatma. OmniRoute arka planda çalışmalı. Kullanım istatistikleri panelden izleniyor. Yorumlarda sınırlamalar ve hata raporları var.
## Bölümler
- 0:00 Giriş ve kurulum
- 0:31 Node.js kurulumu
- 1:14 OmniRoute yapılandırması
- 2:40 Claude Code kurulumu
- 3:53 Ortam değişkeni (PATH) ayarı
- 4:39 Başlatma ve kullanım takibi
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OmniRoute | yok | CLI | yok | Yerel yapay zekâ API proxy'si; Kiro AI üzerinden Claude Code için API anahtarı sağlar | 1:14 | Next up, we need to install Omni Route. This is what's going to give us the API key |
| Kiro AI | yok | teknik | yok | OmniRoute'a bağlanan ücretsiz Claude modeli sağlayıcısı (AWS Builder ID ile giriş) | 1:39 | Providers sayfasında Kiro AI bağlantısı ve Connect Kiro penceresi (karede: OmniRoute Providers sayfasında Kiro AI kartı '1 Connected' ve anahtar açık; Kiro AI sayfasında OAuth Account bağlantısı.) |
| Claude Code | yok | CLI | yok | Terminalde çalışan Anthropic kodlama aracı; OmniRoute üzerinden kullanılıyor | 2:40 | it's time to actually install Claude Code itself |
| Node.js | yok | CLI | yok | npm paketlerini çalıştırmak için gereken çalışma ortamı; sürüm 22 LTS öneriliyor | 0:31 | install Node.js, preferably version 22. Pick the LTS version |
| npm | yok | CLI | yok | OmniRoute ve Claude Code'u global kurmak için paket yöneticisi | 1:17 | npm install -g omniroute@latest komutu (karede: Konsolda 'npm install -g omniroute@latest' ve not defterinde npm install -g @anthropic-ai/claude-code satırları.) |
| Claude Sonnet 4.5 | yok | teknik | yok | kr/claude-sonnet-4.5 olarak Kiro üzerinden kullanılan model | 3:41 | ANTHROPIC_MODEL=kr/claude-sonnet-4.5 satırı .bat dosyasında (karede: Notepad'de cc1.bat içinde 'set ANTHROPIC_MODEL=kr/claude-sonnet-4.5' ve SMALL_FAST_MODEL satırı.) |
| Claude Haiku 4.5 | yok | teknik | yok | Kiro AI sayfasında listelenen kr/claude-haiku-4.5 modeli | 1:43 | Available Models listesinde kr/claude-haiku-4.5 (karede: Kiro AI sayfasında Available Models altında kr/claude-sonnet-4.5 ve kr/claude-haiku-4.5 kutuları.) |
| AWS Builder ID | yok | teknik | yok | Kiro AI'ya giriş yöntemi | 1:14 | hit add, select the AWS Builder ID option |
| .bat dosyası | yok | teknik | yok | API anahtarı ve ortam değişkenlerini ayarlayıp claude'u başlatan toplu iş dosyası (cc.bat) | 2:40 | we need to create a dot bat file. This is what's going to handle our API key · kanıt: yok |
| Windows PATH ortam değişkeni | yok | teknik | yok | cc.bat klasörünü PATH'e ekleyerek komutu her yerden çalıştırma (sysdm.cpl) | 3:53 | Copy the path to your cc.bat file, then in the window, click new. · kanıt: yok |
| Windows Notepad | yok | teknik | yok | Not defteriyle .bat dosyasını düzenleme | 3:30 | cc1.bat - Notepad penceresi · kanıt: kare (karede: Notepad penceresi 'cc1.bat - Notepad' başlığıyla, içinde set satırları.) |
| Windows PowerShell | yok | CLI | yok | OmniRoute'un arka planda çalıştığı terminal | 5:07 | OmniRoute is running günlüğü PowerShell penceresinde (karede: Windows PowerShell penceresinde 'OmniRoute is running', Dashboard ve API Base adresleri.) |
| Next.js | yok | teknik | yok | OmniRoute sunucusunun çalıştığı çerçeve (v16.0.10) | 1:34 | Konsolda 'Next.js 16.0.10' çıktısı (karede: OmniRoute konsolunda '▲ Next.js 16.0.10', Local http://localhost:20128.) |
| better-sqlite3 | yok | teknik | yok | OmniRoute'un kullandığı yerel SQLite eklentisi; Node 24+ ile uyumsuzluk uyarısı | 1:33 | Uyarı: OmniRoute uses better-sqlite3 (karede: OmniRoute başlangıcında sarı uyarı: better-sqlite3 native addon, Node.js 22 LTS önerisi, npm rebuild better-sqlite3.) |
| Substack | yok | teknik | yok | Komutların ve bağlantıların yayımlandığı makale platformu | 0:00 | all the commands used in this video will be available in an article on my Substack |
| Windows Dosya Gezgini | yok | teknik | yok | Klasör oluşturma, dosya uzantısı değiştirme, adres çubuğundan CMD açma | 3:15 | scripts klasöründe sağ tık menüsü ve yeni metin dosyası · kanıt: kare (karede: Dosya Gezgini 'scripts' klasörü, cc.bat ve New Text File; bağlam menüsü açık.) |
| Windows CMD | yok | CLI | yok | Windows komut istemi; node, npm, omniroute ve cc komutları burada çalıştırılıyor. | 0:31 | Hit Win + R and type CMD to open the console · kanıt: yok |
| Windows .bat betiği | yok | teknik | yok | cc.bat dosyası; ortam değişkenlerini ayarlayıp claude komutunu çalıştırıyor. | 2:40 | create a dot bat file. This is what's going to handle our API key · kanıt: yok |
| Ortam değişkenleri (PATH) | yok | teknik | yok | Windows sistem ayarlarındaki PATH girdisine betik klasörünü ekleyerek cc komutunu her yerden çağırma. | 3:53 | double-click on path. This is where we add the location of our dot bat file · kanıt: yok |
| Kurulumun çalıştığını ve kullanım istatistiklerinin güncellendiğini test etme | yok | prompt | yok | Claude Code'a konumu soruluyor ('Where you located'): Windows 11 makinesinde yerel CLI olarak çalıştığını ve Sonnet 4 modeliyle çalıştığını söylüyor. | 5:46 | kaynak: kare |
## Açıklama bağlantıları
- https://promptas.substack.com/p/how-use-claude-code-free-in-2026 — Videodaki tüm komut ve bağlantıları içeren Substack makalesi · aday: hayır · Yazarın kendi makalesi/rehber sayfası; izleyicinin kullanacağı bir araç ya da servis değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| node -v | Kurulu Node.js sürümünü gösterir (karede: Konsolda 'node -v' ve çıktı v24.14.1.) | 1:08 | kare |
| npm install -g omniroute@latest | OmniRoute'u global kurar (karede: Konsolda 'npm install -g omniroute@latest' satırı.) | 1:17 | kare |
| omniroute | OmniRoute sunucusunu başlatır, panel tarayıcıda açılır (localhost:20128) (karede: Konsolda 'omniroute' sonrası OmniRoute ASCII başlığı ve 'Starting server...'.) | 1:33 | kare |
| npm install -g @anthropic-ai/claude-code | Claude Code'u global kurar (karede: Not defterinde 'npm install -g @anthropic-ai/claude-code' satırı vurgulanmış.) | 2:51 | kare |
| sysdm.cpl | Sistem Özellikleri'ni açar; Gelişmiş sekmesinden Ortam Değişkenleri ile PATH düzenlenir (karede: Win+R Çalıştır penceresinde 'sysdm.cpl' yazılı.) | 3:54 | kare |
| cc | cc.bat dosyasını çalıştırıp Claude Code'u OmniRoute ayarlarıyla başlatır (karede: Konsolda 'C:\scripts>cc' ve Claude Code v2.1.96 açılış ekranı.) | 4:57 | kare |
| cmd (Dosya Gezgini adres çubuğuna) | Klasörde doğrudan konsol açar | 4:39 | altyazı |
| set ANTHROPIC_BASE_URL=http://localhost:20128/v1 (cc.bat içinde; AUTH_TOKEN, MODEL, SMALL_FAST_MODEL, DISABLE_NONESSENTIAL_TRAFFIC ile birlikte) | Claude Code'u yerel OmniRoute uç noktasına yönlendirir ve claude %* ile başlatır (karede: Notepad'de cc1.bat: @echo off, set ANTHROPIC_BASE_URL, AUTH_TOKEN, API_KEY, MODEL, SMALL_FAST_MODEL, DISABLE_NONESSENTIAL_TRAFFIC=1, claude %*.) | 3:41 | kare |
| cmd | Windows komut istemini açar | 0:31 | altyazı |
| set ANTHROPIC_BASE_URL=http://localhost:20128/v1 | Claude Code isteklerini yerel OmniRoute adresine yönlendirir (karede: Not uygulamasında 'set ANTHROPIC_BASE_URL=http://localhost:20128/v1' satırı) | 0:55 | kare |
| set ANTHROPIC_AUTH_TOKEN=[gizlendi] API KEY | OmniRoute'ta oluşturulan API anahtarını kimlik olarak verir (değer yer tutucu) (karede: cc.bat'te 'set ANTHROPIC_AUTH_TOKEN=' satırı, anahtar yerine yer tutucu) | 3:41 | kare |
| set ANTHROPIC_API_KEY= | API_KEY değişkenini boş bırakır (karede: Not uygulamasında 'set ANTHROPIC_API_KEY=' satırı boş) | 0:55 | kare |
| set ANTHROPIC_MODEL=kr/claude-sonnet-4.5 | Claude Code'un kullanacağı ana modeli seçer (karede: cc.bat'te 'set ANTHROPIC_MODEL=kr/claude-sonnet-4.5' satırı) | 3:41 | kare |
| set ANTHROPIC_SMALL_FAST_MODEL=kr/claude-sonnet-4.5 | Hafif/hızlı görevler için kullanılacak küçük modeli seçer (karede: cc.bat'te 'set ANTHROPIC_SMALL_FAST_MODEL=kr/claude-sonnet-4.5' satırı) | 3:41 | kare |
| set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 | Claude Code'un gereksiz ağ trafiğini kapatır (karede: Not uygulamasında 'set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1' satırı) | 0:55 | kare |
| claude %* | cc.bat içinde Claude Code'u çalıştırır; dosyaya verilen argümanları iletir (karede: cc.bat'in son satırı 'claude %*') | 3:41 | kare |
| Win + R → sysdm.cpl | Sistem Özellikleri penceresini açar; ortam değişkenleri buradan düzenlenir (karede: Not uygulamasında 'Win + R → sysdm.cpl' yazılı) | 3:54 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Kurulumla Claude Sonnet 4.5 terminalde Kiro AI üzerinden ücretsiz kullanılabiliyor; Anthropic aboneliği ve GPU gerekmiyor. | açıklama | özellik |
| OmniRoute arka planda çalışmıyorsa API anahtarı bağlanmaz ve Claude Code çalışmaz. | 5:42 | özellik |
| Oluşturulan API anahtarı kapatıldıktan sonra tekrar görülemez; yenisi oluşturulmalı. | 2:14 | özellik |
| Node.js için 22 LTS sürümü öneriliyor. | 0:31 | öneri |
| Kare 5:46'da Claude Code kendini Sonnet 4 modeliyle çalışan olarak tanıtıyor, .bat'ta ise sonnet-4.5 ayarlı. | 5:46 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude (yapay zekâ modeli) | Claude Sonnet 4.5 | Claude, the coolest, smartest, fastest, whatever you want to call it |
| konuşma 0:00 | Claude Code | Claude Code | I'll show you how to use Claude Code for free |
| konuşma 0:00 | Substack makalesi | Substack | available in an article on my Substack |
| konuşma 0:31 | Node.js | Node.js | install Node.js, preferably version 22 |
| kare 0:32 | nodejs.org indirme sayfası | Node.js | nodejs.org/en/download |
| kare 0:32 | Docker | aday değil: konu dışı | Node.js indirme sayfasında Docker seçeneği; videoda kullanılmıyor |
| kare 0:32 | npm | npm | npm install -g omniroute@latest |
| konuşma 0:31 | CMD konsolu / Win+R | aday değil: genel kavram | Hit Win + R and type CMD |
| konuşma 1:14 | OmniRoute | OmniRoute | we need to install Omni Route |
| konuşma 1:14 | Kiro AI | Kiro AI | click on Kiro AI |
| konuşma 1:14 | AWS Builder ID | AWS Builder ID | select the AWS Builder ID option |
| konuşma 1:14 | Google ile giriş | aday değil: genel kavram | I've set all my accounts up through Google |
| kare 1:34 | Next.js 16.0.10 | Next.js | Next.js 16.0.10 çıktısı |
| kare 1:33 | better-sqlite3 | better-sqlite3 | OmniRoute uses better-sqlite3 uyarısı |
| kare 1:39 | Providers listesi (Antigravity, Cursor IDE, DeepSeek, GLM Coding, Gemini CLI, GitHub Copilot, Kimi, Minimax, Mistral, NVIDIA NIM, OpenAI, OpenRouter, Perplexity, Qwen Code, xAI) | aday değil: konu dışı | Yalnız menüde listeleniyor, videoda kullanılmıyor (belirsizliklere de bakınız) |
| kare 1:43 | kr/claude-haiku-4.5 | Claude Haiku 4.5 | Kiro AI Available Models listesi |
| konuşma 2:14 | API Manager ve API anahtarı | OmniRoute | Head over to the API Manager section |
| konuşma 2:40 | .bat dosyası | .bat dosyası | we need to create a dot bat file |
| kare 3:30 | Notepad | Windows Notepad | cc1.bat - Notepad |
| kare 3:15 | Sağ tık menüsü (Git Bash, PyCharm, MobaXterm) | aday değil: konu dışı | Dosya Gezgini bağlam menüsü öğeleri, kullanılmıyor |
| kare 0:55 | Not defteri uygulaması (komut notları) | aday değil: konu dışı | Komutların tutulduğu not uygulaması, videoda araç olarak anlatılmıyor |
| konuşma 3:53 | Ortam değişkenleri / PATH | Windows PATH ortam değişkeni | double-click on path |
| kare 4:09 | PyCharm / Python PATH girdileri | aday değil: konu dışı | PATH listesinde önceden var olan girdiler |
| kare 5:07 | Windows PowerShell | Windows PowerShell | OmniRoute is running günlüğü |
| kare 5:21 | Limits & Quotas ve Analytics panelleri | OmniRoute | Kiro connected. Profile ARN not available |
| açıklama | Anthropic aboneliği / Ollama / GPU | aday değil: konu dışı | Açıklamada 'no Anthropic subscription, no GPU, no Ollama' olumsuzlama olarak geçiyor |
| açıklama | Claude Sonnet 4.5 | Claude Sonnet 4.5 | Claude Sonnet 4.5 right in your terminal |
| açıklama | Git | aday değil: konu dışı | Açıklamada 'Works with Git and files'; videoda gösterilmiyor |
| açıklama bağlantısı | promptas.substack.com makalesi | aday değil: konu dışı | Yazarın kendi rehber makalesi |
| linkli sayfa | Vercel, MacStadium, Cloudflare (Node.js sponsor bağlantıları) | aday değil: sponsor/reklam | Node.js sitesindeki ortak bağlantıları, videoda kullanılmıyor |
| linkli sayfa | Docker Desktop belgeleri | aday değil: konu dışı | docs.docker.com bağlantıları, videoda kullanılmıyor |
| linkli sayfa | Node.js v24.21.0 sürüm notları ve ikili doğrulama | Node.js | nodejs.org indirme sayfasının bağlantıları |
| yorum | Python, VS Code, Opus, Sonnet 4.6, Linux/macOS, settings.json | aday değil: konu dışı | İzleyici soruları; videoda gösterilmiyor |
| yorum | Kiro AI kısıtlamaları | Kiro AI | Sahip yanıtı: sınırlama büyük olasılıkla Kiro AI tarafından |
| yorum | OpenAI, OpenRouter vb. diğer sağlayıcılar | aday değil: konu dışı | Yorumda genel sağlayıcı şikâyeti |
| konuşma 4:39 | Claude Code başlatma ('cc') | Claude Code | type the name of your file and hit enter |
| kare 4:57 | Claude Code v2.1.96 ve native installer uyarısı | Claude Code | Claude Code has switched from npm to native installer |
| kare 3:15 | Dosya Gezgini | Windows Dosya Gezgini | scripts klasörü ve sağ tık Yeni menüsü |
## Kareden okunanlar
- 0:32: nodejs.org/en/download sayfası; v22.22.2 LTS seçili, Windows, Docker, npm; açılır listede v25.9.0, v24.15.0, v23.11.1, v22.22.2, v21.7.3.
- 0:55: Not defteri: node -v, npm install -g omniroute@latest, omniroute, npm install -g @anthropic-ai/claude-code, .bat içeriği (ANTHROPIC_BASE_URL=http://localhost:20128/v1, AUTH_TOKEN, API_KEY boş, MODEL ve SMALL_FAST_MODEL kr/claude-sonnet-4.5, DISABLE_NONESSENTIAL_TRAFFIC=1, claude %*), PATH için Win+R sysdm.cpl.
- 1:08: Konsolda node -v çıktısı v24.14.1.
- 1:34: OmniRoute başlığı, Node 24.14.1 uyarısı, Next.js 16.0.10, Local localhost:20128.
- 1:39: OmniRoute Providers: OAuth sağlayıcılar (Claude Code, Antigravity, OpenAI Codex, GitHub Copilot, Cursor IDE, Kimi Coding, Kilo Code, Cline, Qoder AI, Qwen Code, Gemini CLI, Kiro AI) ve API Key sağlayıcılar (OpenRouter, GLM Coding, Kimi, DeepSeek, Groq, Mistral, Perplexity vb.).
- 1:56: AWS giriş ekranı: e-posta, Continue with Google, Apple, GitHub, Amazon.
- 2:13: API Manager: 1 anahtar 'Test Claude', 4 model mevcut; Create API Key penceresi.
- 3:41: cc1.bat Notepad içeriği: @echo off, set ANTHROPIC_BASE_URL=http://localhost:20128/v1, AUTH_TOKEN=[gizlendi] API KEY, MODEL kr/claude-sonnet-4.5.
- 4:09: Ortam Değişkenleri penceresi; Path listesine C:\scripts ekli, Python ve PyCharm girdileri görünüyor.
- 5:00: Claude Code v2.1.96 açılış ekranı: 'Sonnet 4 · API Usage Billing', 'switched from npm to native installer' uyarısı.
- 5:21: Limits & Quotas: Kiro connected. Profile ARN not available for quota tracking; Analytics paneli sıfır token.
## Belirsizlikler
- Gösterilen kurulum komutları ekranda kısmen bozuk OCR ile okundu; npm install -g @anthropic-ai/claude-code komutu not defterinde net görünüyor.
- Claude Code kendini 'Sonnet 4' diye tanıtıyor, oysa .bat 'kr/claude-sonnet-4.5' ayarlıyor; gerçek model belirsiz.
- Videoda Docker, Descript, Spline gibi sözlük eşleşmeleri yalnızca Node.js sayfasında veya OCR gürültüsünde; kullanılmadıkları için aday yapılmadı.
- API anahtarı değeri ekranda maskeli; yazılmadı.
- Yorumlardaki Kiro AI kısıtları ve OAuth uyarısı videoda gösterilmedi; doğrulanamadı.
- Kare listesindeki zamanlar ile görsellerin birebir eşleşmesi tam doğrulanamadı.
## Atlanan segment oranı
0/9 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://promptas.substack.com/p/how-use-claude-code-free-in-2026 | açıklama | açıklama | hayır |
| nodejs.org/en/download | 0:32 | ekran | evet |
| https://docker.com/get-started/ | 0:32 | ekran | hayır |
| http://localhost:20128/v1 | 0:55 | ekran | hayır |
| http://localhost:20128 | 1:34 | ekran | hayır |
| localhost:20128/dashboard/onboarding | 1:36 | ekran | hayır |
| localhost:20128/dashboard/providers | 1:39 | ekran | hayır |
| localhost:20128/dashboard/providers/kiro | 1:42 | ekran | hayır |
| example.com | 1:56 | ekran | hayır |
| localhost:20128/dashboard/api-manager | 2:13 | ekran | hayır |
| http://localhost:2 | 5:14 | ekran | hayır |
| https://github.com/nodejs/node/releases/tag/v24.21.0 | 0:32 | ekran | hayır |
| https://github.com/nodejs/node#verifying-binaries | 0:32 | ekran | hayır |
| https://vercel.com/?utm_source=nodejs-website&utm_medium=Link | 0:32 | ekran | hayır |
| https://macstadium.com/?utm_source=nodejs-website&utm_medium=Link | 0:32 | ekran | hayır |
| https://www.cloudflare.com/?utm_source=nodejs-website&utm_medium=Link | 0:32 | ekran | hayır |
| https://docs.docker.com/desktop | 0:32 | ekran | hayır |
| https://docs.docker.com/desktop/linux/install | 0:32 | ekran | hayır |
## İş akışı
- 1. adım — Node.js LTS sürümünü indirip kurma — araçlar: Node.js, Windows kurulum sihirbazı
- 2. adım — Node.js sürümünü node -v ile doğrulama — araçlar: Windows CMD, Node.js
- 3. adım — OmniRoute'u npm ile global kurma — araçlar: npm, Windows CMD
- 4. adım — OmniRoute sunucusunu başlatma ve panelin açılmasını bekleme — araçlar: OmniRoute, Windows CMD
- 5. adım — Sağlayıcılar bölümünde Kiro AI'yı ekleme — araçlar: OmniRoute, Kiro AI
- 6. adım — AWS Builder ID ile giriş yapıp OAuth hesabını bağlama — araçlar: Kiro AI, AWS Builder ID
- 7. adım — API Manager'da yeni API anahtarı oluşturma ve kaydetme — araçlar: OmniRoute, Notepad
- 8. adım — Claude Code'u npm ile global kurma — araçlar: npm, Claude Code
- 9. adım — cc.bat dosyasını oluşturma; ortam değişkenlerini ve anahtarı yazma — araçlar: Notepad, Windows .bat betiği
- 10. adım — Dosya uzantısını .bat olarak değiştirme — araçlar: Windows Gezgini
- 11. adım — Betik klasörünü PATH ortam değişkenine ekleme — araçlar: Win + R (sysdm.cpl), Ortam değişkenleri (PATH)
- 12. adım — Betik klasöründe CMD açıp cc komutuyla Claude Code'u başlatma — araçlar: Windows CMD, Claude Code
- 13. adım — İlk açılıştaki anahtar uyarısında ikinci seçeneği deneme; gerekirse yeniden çalıştırma — araçlar: Claude Code
- 14. adım — OmniRoute'un arka planda çalıştığını doğrulama — araçlar: OmniRoute, Windows PowerShell
- 15. adım — Kredi takibini güncellemek için Claude Code'dan istek gönderme ve panelde kontrol etme — araçlar: Claude Code, OmniRoute
## Promptlar
- Kurulumun çalıştığını ve kullanım istatistiklerinin güncellendiğini test etme — Claude Code'a konumu soruluyor ('Where you located'): Windows 11 makinesinde yerel CLI olarak çalıştığını ve Sonnet 4 modeliyle çalıştığını söylüyor.
ikinci göz KAPALI: --ikinci-goz yok
