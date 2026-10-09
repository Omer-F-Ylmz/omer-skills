# Lightpanda: the headless browser designed for AI and automation
## Künye
Lightpanda: the headless browser designed for AI and automation · git.radar · süre: 1:07 · ? · https://www.instagram.com/reel/DdBlwBIFGvC/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-34 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 78544 tk · claude-haiku-5-5: claude-haiku-5-5 · 58297 tk
## Özet
Kısa tanıtım videosu: GitHub'da 34.926 yıldıza ulaşan, Zig ile sıfırdan yazılmış, yapay zekâ ajanları ve otomasyon için tasarlanmış hafif başsız (headless) tarayıcı Lightpanda. README'de Chrome'a göre 9 kat hızlı çalışma süresi ve 16 kat az bellek grafiği, brew/curl/Docker kurulumu, CDP sunucusu, Puppeteer/Playwright uyumu, fetch/serve komutları, ajan modu (PandaScript, çoklu LLM sağlayıcı) ve yerel MCP desteği gösteriliyor.
## Bölümler
- 0:00 Giriş: ağır tarayıcı sorunu ve Lightpanda tanıtımı
- 0:05 README ve karşılaştırma grafikleri
- 0:12 Kurulum: brew, curl, WSL, Docker
- 0:37 fetch ve serve komutları, dump seçenekleri
- 0:42 Puppeteer örneği ve Bidi protokolü
- 0:47 Ajan modu ve PandaScript
- 0:53 LLM sağlayıcıları ve ajan komutları
- 1:00 Yerel MCP ve skill desteği
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Lightpanda | yok | CLI | https://github.com/lightpanda-io/browser | Yapay zekâ ajanları ve otomasyon için Zig ile sıfırdan yazılmış hafif başsız tarayıcı | 0:00 | The headless browser built from scratch for AI agents and automation. (karede: GitHub README: Lightpanda Browser başlığı, panda logosu, 'written in Zig' notu) |
| Zig | yok | teknik | yok | Lightpanda'nın yazıldığı programlama dili | 0:00 | A new browser, written in Zig. (karede: README'de 'written in Zig' yazısı) |
| Homebrew | yok | CLI | yok | brew ile Lightpanda kurulumu | 0:14 | brew install lightpanda-io/browser/lightpanda · kanıt: kare (karede: Ekranda OCR ile okunan brew install lightpanda-io/browser/lightpanda satırı (kare görseli gönderilmedi)) |
| curl | yok | CLI | yok | Lightpanda ikilisini GitHub releases'tan indirme | 0:21 | curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/ (karede: OCR ile okunan curl indirme komutu (kare görseli gönderilmedi)) |
| WSL | yok | CLI | yok | Windows'ta Linux adımlarıyla Lightpanda çalıştırma | 0:28 | WSL not installed? Run wsl --install from an administrator (karede: OCR ile okunan WSL kurulum notu (kare görseli gönderilmedi)) |
| Docker | yok | CLI | yok | Resmi Lightpanda imajını çalıştırma, CDP sunucusu 9222 portunda | 0:34 | docker run -d --name lightpanda -p 127.0.0.1:9222:9222 (karede: OCR ile okunan docker run komutu (kare görseli gönderilmedi)) |
| Puppeteer | yok | teknik | yok | CDP sunucusuna bağlanan otomasyon istemcisi | 0:30 | Your automation client (Puppeteer, Playwright, etc.) can run (karede: OCR ile okunan README satırı (kare görseli gönderilmedi)) |
| Playwright | yok | teknik | yok | CDP sunucusuna bağlanan otomasyon istemcisi | 0:30 | Your automation client (Puppeteer, Playwright, etc.) can run (karede: OCR ile okunan README satırı (kare görseli gönderilmedi)) |
| CDP | yok | teknik | yok | Lightpanda'nın sunduğu Chrome DevTools Protocol sunucusu | 0:33 | exposing Lightpanda's CDP server on port 9222 (karede: OCR ile okunan README satırı (kare görseli gönderilmedi)) |
| WebDriver Bidi | yok | teknik | yok | --protocol webdriver ile Bidi sunucusu başlatma | 0:57 | Start a webdriver Bidi server · kanıt: kare (karede: 'Start a webdriver Bidi server' başlığı ve --protocol webdriver --protocol cdp açıklaması) |
| Agent mode | yok | CLI | yok | lightpanda agent ile düz İngilizce veya slash komutlarla tarayıcı sürme | 0:57 | lightpanda agent lets you drive the browser with a native agent. · kanıt: kare (karede: README 'Agent mode' bölümü, agent komut örnekleri) |
| PandaScript | yok | teknik | yok | Ajan oturumunun çıktısı olan deterministik JavaScript betiği; /save ile dışa aktarılır, lightpanda run ile oynatılır | 0:57 | The output of an agent session is a PandaScript (karede: Agent mode metninde mavi PandaScript bağlantısı, /save ve lightpanda run <script>.js) |
| Anthropic | yok | teknik | yok | Ajan modunda desteklenen LLM sağlayıcı | 0:57 | It supports Anthropic, OpenAI, Gemini, Google Vertex AI (karede: Agent mode paragrafındaki sağlayıcı listesi) |
| OpenAI | yok | teknik | yok | Desteklenen sağlayıcı; OPENAI_BASE_URL ile uyumlu uçlar | 0:57 | any OpenAI-compatible endpoint via OPENAI_BASE_URL (karede: Agent mode paragrafı) |
| Gemini | yok | teknik | yok | Desteklenen sağlayıcı; --provider gemini | 0:57 | It supports Anthropic, OpenAI, Gemini, Google Vertex AI (karede: Agent mode paragrafı) |
| Google Vertex AI | yok | teknik | yok | Desteklenen sağlayıcı; --provider vertex | 0:57 | Google Vertex AI, (karede: Agent mode paragrafı) |
| Mistral | yok | teknik | yok | Desteklenen LLM sağlayıcı | 0:57 | Mistral, Hugging Face, the Vercel AI Gateway (karede: Agent mode paragrafı) |
| Hugging Face | yok | teknik | yok | Desteklenen LLM sağlayıcı | 0:57 | Mistral, Hugging Face, the Vercel AI Gateway (karede: Agent mode paragrafı) |
| Vercel AI Gateway | yok | teknik | yok | Yüzlerce modele tek anahtarla erişim sağlayıcısı | 0:57 | the Vercel AI Gateway (one key for hundreds of models) (karede: Agent mode paragrafında mavi Vercel AI Gateway bağlantısı) |
| Ollama | yok | teknik | yok | Yerel model çalıştırma desteği | 0:57 | local models via Ollama or llama.cpp (karede: Agent mode paragrafı) |
| llama.cpp | yok | teknik | yok | Yerel model çalıştırma desteği | 0:57 | local models via Ollama or llama.cpp (karede: Agent mode paragrafı) |
| MCP | yok | MCP | yok | Yerel MCP sunucusu (JSON-RPC 2.0); lightpanda mcp | 1:00 | Native MCP and skill (karede: OCR ile okunan 'Native MCP and skill' başlığı (kare görseli gönderilmedi)) |
| Hacker News | yok | teknik | yok | Ajan görev örneği: news.ycombinator.com ilk haber | 0:58 | agent -task "top story on news.ycombinator.com?" · kanıt: kare (karede: Agent mode komut örneklerinde top story on news.ycombinator.com görevi) |
| GitHub | yok | teknik | yok | Lightpanda'nın kaynak deposunun ve sürüm dosyalarının barındırıldığı platform; videoda depo sayfası gösterilir. | 1:05 | Check out the project on GitHub to learn more. |
| Ajan modu örneği: Hacker News ilk haber | yok | prompt | yok | Ajana düz İngilizce görev verilir: news.ycombinator.com'daki en üst haber nedir? | 0:58 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/lightpanda-io/browser — Lightpanda GitHub deposu · aday: evet (Lightpanda) · Videoda anlatılan aracın deposu; izleyicinin kullanabileceği araç. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| brew install lightpanda-io/browser/lightpanda | Lightpanda'yı Homebrew ile kurar (karede: OCR ile okunan brew install satırı) | 0:14 | kare |
| curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/... | Lightpanda ikilisini GitHub releases'tan indirir (karede: OCR ile okunan curl satırı) | 0:21 | kare |
| wsl --install | Windows'ta WSL kurar (yönetici kabuğundan) (karede: OCR ile okunan WSL notu) | 0:35 | kare |
| docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser | Docker imajını çeker, CDP sunucusunu 9222'de başlatır (karede: OCR ile okunan docker run satırı) | 0:37 | kare |
| ./lightpanda fetch --obey-robots --dump html --log-format pretty --log-level info | Sayfayı getirir ve HTML çıktısı verir (karede: OCR ile okunan fetch satırı) | 0:41 | kare |
| ./lightpanda serve --obey-robots --log-format pretty --log-level info --host | CDP sunucusunu başlatır (karede: OCR ile okunan serve satırı) | 0:45 | kare |
| ./lightpanda serve ... --protocol webdriver --protocol cdp | Hem CDP hem Bidi sunucusu başlatır (karede: Bidi bölümünde ./lightpanda serve --obey-robots --log-format pretty --log-level info --ho) | 0:57 | kare |
| ./lightpanda agent --task "top story on news.ycombinator.com?" | Ajanı tek görevle çalıştırır (karede: Agent mode komut örnekleri) | 0:58 | kare |
| ./lightpanda agent --no-llm | LLM'siz REPL açar (karede: Agent mode kod bloğunda --no-llm # basic REPL, no LLM) | 0:57 | kare |
| ./lightpanda run session.js | Kaydedilmiş betiği tekrar oynatır (karede: Kod bloğunda run session.js # run a recorded script) | 0:57 | kare |
| ./lightpanda agent --list-models | Modelleri listeler (karede: OCR ile okunan agent --list-models satırı) | 0:58 | kare |
| ./lightpanda agent --provider gemini --task ".." | Belirli sağlayıcıyı zorlar (karede: OCR ile okunan provider gemini satırı) | 1:04 | kare |
| /save | Ajan oturumunu PandaScript olarak dışa aktarır (karede: Agent mode metninde Run /save to export one) | 0:57 | kare |
| --dump markdown / --dump png > page.png / --dump pdf > page.pdf | fetch çıktısını markdown, PNG veya PDF olarak dışa aktarır. (karede: OCR: '--dump markdown, or --dump png > page.png or --dump pdf > page.pdf' (0:37).) | 0:37 | kare |
| ./lightpanda serve --obey-robots --log-format pretty --log-level info --h… | CDP sunucusunu başlatır; son parametre ekranda kesik okunuyor. (karede: OCR: ./lightpanda serve --obey-robots --log-format pretty --log-level info --h (0:40).) | 0:40 | kare |
| VERTEX_API_KEY=<anahtar> ./lightpanda agent --provider vertex | Google Vertex AI sağlayıcısını API anahtarı ortam değişkeniyle seçer (anahtar değeri yazılmadı). (karede: OCR: VERTEX_API_KEY=[gizlendi] ./lightpanda agent --provider vertex (0:58).) | 0:58 | kare |
| AI_GATEWAY_API_KEY=<anahtar> ./lightpanda agent --provider vercel | Vercel AI Gateway sağlayıcısını seçer (anahtar değeri yazılmadı; model parametresi kesik). (karede: OCR: AI_GATEWAY_API_KEY=[gizlendi] ./lightpanda agent --provider vercel --mo... (0:59).) | 0:59 | kare |
| OPENAI_BASE_URL=https://my-gateway/v1 OPENAI_API_KEY=<anahtar> ./lightpanda agent | OpenAI uyumlu özel bir uç noktayı agent'a bağlar (anahtar değeri yazılmadı). (karede: OCR: OPENAI_BASE_URL=https://my-gateway/v1 OPENAI_API_KEY=[gizlendi] (0:59).) | 0:59 | kare |
| GOOGLE_CLOUD_PROJECT=my-proj ./lightpanda agent --provider vertex | Vertex AI için Google Cloud proje kimliğini ayarlayıp sağlayıcıyı seçer. (karede: OCR: GOOGLE_CLOUD_PROJECT=my-proj ./lightpanda agent --provider v... (1:00).) | 1:00 | kare |
| ./lightpanda agent --provider gemini --ask ".." | Soruyu belirli bir sağlayıcıyla (Gemini) çalıştırır. (karede: OCR: ./lightpanda agent --provider gemini --ask ".." (1:07).) | 1:07 | kare |
| "args": ["mcp"] | MCP yapılandırmasında Lightpanda'yı 'mcp' argümanıyla MCP sunucusu olarak başlatır. (karede: OCR: MCP yapılandırma kodunda "args": ["mcp"] satırı (1:04).) | 1:04 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Lightpanda GitHub'da 34.926 yıldıza ulaştı. | 0:00 | sayısal |
| Çalışma süresi 9 kat daha hızlı (README grafiği). | 0:05 | karşılaştırma |
| Tepe bellek kullanımı 16 kat daha az (123MB'a karşı 2GB). | 0:05 | karşılaştırma |
| Chromium veya WebKit çatalı değil, sıfırdan yazılmış yeni bir tarayıcı. | 0:00 | özellik |
| PandaScript betikleri deterministik ve token gerektirmez; modelsiz üretime verilebilir. | 0:57 | özellik |
| Ajan tarayıcıyla aynı süreçte çalıştığı için her araç çağrısı doğrudan işlemdir. | 0:57 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Lightpanda tanıtımı | Lightpanda | called Light Panda, has grabbed 34,926 stars |
| konuşma 0:00 | Otobüs/motosiklet benzetmesi | aday değil: genel kavram | giant, heavy tour bus |
| kare 0:00 | Zig | Zig | written in Zig |
| kare 0:00 | AGPL-3.0 lisansı | aday değil: genel kavram | AGPL-3.0 license |
| kare 0:00 | Discord rozeti | aday değil: genel kavram | discord 38 online |
| kare 0:05 | Chrome karşılaştırması | aday değil: genel kavram | Chrome çubuğu 46s, 2GB |
| kare 0:05 | AWS EC2 m5.large | aday değil: genel kavram | AWS EC2 m5.large instance |
| ekran 0:14 | brew install | Homebrew | brew install lightpanda-io/browser/lightpanda |
| ekran 0:21 | curl indirme | curl | curl -L -o lightpanda |
| ekran 0:28 | WSL | WSL | WSL not installed? |
| ekran 0:30 | Puppeteer | Puppeteer | Your automation client (Puppeteer, Playwright |
| ekran 0:30 | Playwright | Playwright | Puppeteer, Playwright, etc. |
| ekran 0:31 | Docker | Docker | Install from Docker |
| ekran 0:33 | CDP sunucusu | CDP | CDP server on port 9222 |
| ekran 0:39 | --dump markdown/png/pdf | aday değil: başka adayın parçası (Lightpanda) | --dump markdown |
| kare 0:57 | Bidi | WebDriver Bidi | Start a webdriver Bidi server |
| kare 0:57 | Agent mode | Agent mode | Agent mode |
| kare 0:57 | PandaScript | PandaScript | PandaScript |
| kare 0:57 | JavaScript | aday değil: başka adayın parçası (PandaScript) | vanilla JavaScript |
| kare 0:57 | Anthropic | Anthropic | It supports Anthropic |
| kare 0:57 | OpenAI | OpenAI | OpenAI-compatible endpoint |
| ekran 0:53 | Gemini | Gemini | Gemini |
| ekran 0:53 | Google Vertex AI | Google Vertex AI | Google Vertex AI |
| ekran 0:54 | Mistral | Mistral | Mistral |
| ekran 0:56 | Hugging Face | Hugging Face | Hugging Face |
| ekran 0:56 | Vercel AI Gateway | Vercel AI Gateway | Vercel AI Gateway |
| ekran 0:56 | Ollama | Ollama | Ollama |
| ekran 0:56 | llama.cpp | llama.cpp | llama.cpp |
| ekran 1:00 | Native MCP and skill | MCP | Native MCP and skill |
| ekran 1:00 | Claude | aday değil: konu dışı | Claude (yalnız sözlük eşleşmesi, bağlamı belirsiz) |
| ekran 0:58 | news.ycombinator.com | Hacker News | top story on news.ycombinator.com? |
| açıklama | github.com/lightpanda-io/browser | Lightpanda | https://github.com/lightpanda-io/browser |
| açıklama | Etiketler (#opensource, #zig vb.) | aday değil: genel kavram | #github #opensource #coding |
| açıklama | theranos.world sayfası | aday değil: konu dışı | https://www.theranos.world |
| yorum | Yorumlar alınamadı | aday değil: konu dışı | yorum: girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: GitHub lightpanda-io/browser sayfası, Public, 73 issue, 19 PR, README; Lightpanda Browser; AGPL-3.0, 35k yıldız, discord 38 online; Execution time 9x faster
- 0:05: Execution time 9x faster (5s/46s), Memory peak 16x less (123MB/2GB), Benchmarks: 933 gerçek sayfa, AWS EC2 m5.large
- 0:57: Bidi sunucusu bölümü, Agent mode metni, PandaScript, sağlayıcı listesi ve agent komut örnekleri
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Bağlantılı sayfa theranos.world (HN) videoyla ilgisiz görünüyor.
- Altyazıda 'Light Panda' yazılmış; doğru ad Lightpanda.
- Claude'un MCP bölümünde nasıl geçtiği net değil; yalnızca sözlük eşleşmesi, aday yapılmadı.
- Sözlük eşleşmeleri React, Inter, Roboto, Headless UI, Browser Use, Go videoda kullanılmıyor (yanlış eşleşme).
- OCR'da 0:14-0:45 arası satırlar bozuk; komutlar tahminen düzeltildi.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/lightpanda-io/browser | açıklama | açıklama | evet |
| https://github.com/lightpanda-io/browser/releases/ | 0:21 | ekran | hayır |
| localhost:922 | 0:39 | ekran | hayır |
| news.ycombinator.com | 0:58 | ekran | evet |
| https://www.theranos.world | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Sorunu anlat: ağır tarayıcılar ajanlar için fazla — araçlar: Lightpanda
- 2. adım — GitHub README'sini göster — araçlar: Lightpanda
- 3. adım — Hız ve bellek karşılaştırmasını göster — araçlar: Lightpanda
- 4. adım — brew ile kur — araçlar: Homebrew
- 5. adım — curl ile ikiliyi indir — araçlar: curl
- 6. adım — Windows'ta WSL kur — araçlar: WSL
- 7. adım — Docker ile çalıştır — araçlar: Docker, CDP
- 8. adım — fetch ile sayfa çıktısı al — araçlar: Lightpanda
- 9. adım — serve ile CDP sunucusu başlat ve Puppeteer bağla — araçlar: Lightpanda, Puppeteer
- 10. adım — Bidi protokolünü etkinleştir — araçlar: WebDriver Bidi
- 11. adım — Ajan modunu düz İngilizce görevle çalıştır — araçlar: Agent mode
- 12. adım — Oturumu PandaScript olarak kaydet ve tekrar oynat — araçlar: PandaScript
- 13. adım — LLM sağlayıcısı seç — araçlar: Anthropic, OpenAI, Gemini, Ollama
- 14. adım — MCP sunucusunu yapılandır — araçlar: MCP
## Promptlar
- Ajan modu örneği: Hacker News ilk haber — Ajana düz İngilizce görev verilir: news.ycombinator.com'daki en üst haber nedir?
ikinci göz KAPALI: --ikinci-goz yok
