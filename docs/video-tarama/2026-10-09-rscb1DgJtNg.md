# Claude Now Does Video (FOR FREE) Thanks To JavaScript
## Künye
Claude Now Does Video (FOR FREE) Thanks To JavaScript · Chase AI · süre: 14:10 · en-orig · https://youtu.be/rscb1DgJtNg · şema 2
motor: parti 2026-10-09-uzun-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 63942 tk · claude-haiku-5-5: claude-haiku-5-5 · 97155 tk
## Özet
Chase AI, Claude Code ile yalnızca JavaScript, Playwright ve FFmpeg kullanarak ücretsiz video üretmeyi anlatıyor. Her kare zamanın bir fonksiyonu olarak kodla çiziliyor, başsız tarayıcıda kontrol ediliyor ve MP4'e birleştiriliyor. Dört seviye var: prompt ve efor düzeyleri (storyboard istemek), araçlar ve kontrol döngüsü, referans görsel/video, son olarak tüm süreci kodlayan 'Animate' skill'i (cth9191/animate). Video sonunda ElevenLabs sesi, Skillry ilham sitesi ve Kevin Ngo'nun X profili öneriliyor.
## Bölümler
- 0:00 Claude + JavaScript
- 4:07 Seviye 1: Prompt yazma
- 7:19 Seviye 2: Araçlar ve döngü
- 9:56 Seviye 3: Referanslar
- 11:43 Seviye 4: Skill'ler
- 13:39 Kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Videoyu kodla üreten, kareleri kontrol eden ana yapay zekâ aracı | 0:00 | All you need is clawed code in JavaScript to create videos like these. |
| JavaScript | yok | teknik | yok | Her kareyi t zamanının fonksiyonu olarak çizen dil | 0:00 | it uses JavaScript ... to essentially create still images |
| Playwright | yok | CLI | yok | Başsız tarayıcıda kareleri çalıştırıp kontrol ettiren araç | 2:03 | we essentially run the video in a headless browser using something like playright |
| FFmpeg | yok | CLI | yok | Kareleri MP4'e birleştirir, contact sheet çıkarır | 2:03 | it stitches them all via a tool called FFmpeg, which is totally open source |
| Opus 5.5 | yok | teknik | yok | Testlerde kullanılan Claude modeli (Low, High, Ultra efor) | 3:54 | Sohbet kutusunun altında 'Opus 5.5 Low' yazıyor (karede: kanıttan) Sohbet kutusunun altında 'Opus 5.5 Low' yazıyor |
| Fable 5.1 | yok | teknik | yok | Opus 5.5 ile birlikte, prompt eksik olsa da doğru işi yapar denen model | 8:20 | opus 5.5 and fable 5.1 are so good that if you don't even mention these |
| ElevenLabs | yok | MCP | yok | Anlatım sesi üretimi; Claude'a bağlayıcı (connector/MCP) olarak ekleniyor | 9:08 | elevenlabs.io ana sayfası gösteriliyor, konuşmada MCP'den söz ediliyor (karede: kanıttan) elevenlabs.io ana sayfası gösteriliyor, konuşmada MCP'den söz ediliyor |
| Animate | yok | skill | https://github.com/cth9191/animate | Tüm süreci adım adım yürüten, 7 hazır stilli Claude Code skill'i | 11:43 | turning it into a skill, which is what I've done here |
| Skillry | yok | ipucu | yok | Opus 5.5 videolarını ve promptlarını gezdiren ilham sitesi (skillry.dev) | 10:56 | skillry.dev/ai-videos/opus-5-5 sayfası 'Browse 475 Opus 5.5 videos' başlığıyla (karede: kanıttan) skillry.dev/ai-videos/opus-5-5 sayfası 'Browse 475 Opus 5.5 videos' başlığıyla |
| Excalidraw | yok | iş akışı | yok | Seviye 2 prompt şemasını çizmek ve açıklamak için kullanılan beyaz tahta | 7:08 | excalidraw.com adresinde 'Level 2: the tools and a loop' şeması (karede: kanıttan) excalidraw.com adresinde 'Level 2: the tools and a loop' şeması |
| faster-whisper | yok | CLI | yok | Ses için kelime zamanlaması çıkarır; skill'in önkoşulu | 12:44 | things like faster whisper, and it'll even ask if you want the connector |
| Node.js | yok | CLI | yok | Playwright kurulumu için gereken çalışma ortamı (Node 18+) | 8:22 | Alt satırda 'Install once: Node 18+ · npm i -g playwright' (karede: kanıttan) Alt satırda 'Install once: Node 18+ · npm i -g playwright' |
| npm | yok | CLI | yok | Playwright'ı global kuran paket yöneticisi | 8:22 | 'npm i -g playwright && npx playwright install chromium' satırı (karede: kanıttan) 'npm i -g playwright && npx playwright install chromium' satırı |
| Bahnschrift Variable | yok | teknik | yok | Showreel örneğinde kullanılan değişken font (WGHT 300–700, WDTH 75–100) | 0:08 | Sol üstte 'BAHNSCHRIFT VARIABLE · WGHT 300-700 · WDTH 75→100' (karede: kanıttan) Sol üstte 'BAHNSCHRIFT VARIABLE · WGHT 300-700 · WDTH 75→100' |
| Remotion | yok | teknik | yok | Referans videonun üretildiği React tabanlı video aracı | 9:56 | This was created with Opus 5.5 and Remotion |
| Storyboard isteme | yok | ipucu | yok | Videoyu kodlamadan önce sahne karelerini onaylamak için storyboard istemek | 5:21 | ask for a storyboard · kanıt: yok |
| Contact sheet kontrol döngüsü | yok | iş akışı | yok | FFmpeg ile kontrol görseli çıkarıp bakma, düzeltme, yeniden render alma | 8:20 | Excalidraw şemasında 'use FFmpeg to pull a contact sheet, look at it, fix what's wrong' · kanıt: kare (karede: Excalidraw şemasında 'use FFmpeg to pull a contact sheet, look at it, fix what's wrong') |
| Referans görsel/video | yok | ipucu | yok | Stil ve kompozisyon için görsel ya da video referansı verme | 9:56 | Now, level three is where we ... start adding references · kanıt: yok |
| Efor düzeyleri | yok | ipucu | yok | Low, High ve Ultra karşılaştırması; sorun çoğu zaman efor değil prompttur | 4:07 | if you think your issue ... is an effort problem, it's probably not · kanıt: yok |
| Chromium | yok | teknik | yok | Playwright'in kurduğu headless tarayıcı; kareleri çizmek için kullanılır. | 12:38 | Playwright with Chromium gereksinimi ve npx playwright install chromium komutu (karede: Animate README 'Requirements' bölümünde 'npx playwright install chromium' komutu görünüyor.) |
| Python | yok | teknik | yok | Seslendirme zamanlaması için gereken çalışma ortamı (faster-whisper). | 12:38 | Python with faster-whisper (word timing) gereksinimi (karede: Animate README 'Requirements' metninde 'Python with faster-whisper (word timing)' görünüyor.) |
| Efor düzeylerini (Low, High, Ultra) karşılaştıran test promptu | yok | prompt | yok | 15 saniyelik, bir özgeçmiş showreel'i gibi dinamik hareketli grafik videosu istenir; en iyisini yap, hiçbir skill kullanma. | 4:07 | kaynak: kare |
| Seviye 2'deki araçlar ve döngü prompt şablonu | yok | prompt | yok | [KONU] nasıl çalışır konusunda 30 saniyelik, 16:9 animasyonlu anlatım; JavaScript canvas ile, sesi kodla üretilmiş, Playwright ve FFmpeg ile MP4. İsteğe bağlı ses dosyasına göre Whisper zamanlaması. Bitirmeden contact sheet çıkarıp bak, düzelt, yeniden render al, tekrarla. | 8:22 | kaynak: kare |
| Uzun üretim döngülerinden kaçınmak için storyboard isteme | yok | prompt | yok | Tek seferde uzun video üretmeden önce yedi kadar sahneyi gösteren storyboard kareleri iste, onay sonrası kodla. | 5:21 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.skool.com/chase-ai — Chase AI Plus topluluğu (Skool) · aday: hayır · Ücretli topluluk; videoda reklamı yapılan kendi ürünü, izleyicinin kullanacağı araç değil. · sınıf: diğer · erişilemez: ücretli topluluk
- https://www.skool.com/chase-ai-community — Skool topluluk sayfası · aday: hayır · Ücretli topluluk girişi; araç ya da servis değil. · sınıf: diğer · erişilemez: ücretli topluluk / giriş gerekli
- https://chaseai.io — Kanal sahibinin kişisel sitesi · aday: hayır · Videoda kullanılmayan, kişisel tanıtım sayfası. · sınıf: diğer
- https://www.chaseai.io — Kişisel sitenin www sürümü · aday: hayır · Aynı kişisel tanıtım sitesi; araç değil. · sınıf: diğer
- https://github.com/cth9191/animate — Animate skill deposu · aday: evet (Animate) · Videoda gösterilen, kurulumu anlatılan ve izleyicinin kullanabileceği skill. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Parçacık spirali arka planı (particle swirl canvas) | Jarvis panelinde ortada beyaz parçacıklardan oluşan dönen galaksi; Claude modunda mor ağ görünümü (karede: Ortada 'CLAUDE' yazısı üstünde mor noktalı küre; 3:42 karesinde 'ASTRA' altında beyaz spiral) | 3:48 | kare |
| Claude Code / Codex mod anahtarı (segmented toggle) | Üstte iki seçenekli geçiş; seçilene göre tema değişiyor (karede: Üstte 'Claude Code' ve 'Codex' düğmeleri, biri beyaz dolgulu) | 3:48 | kare |
| Üç sütunlu panel yerleşimi (three-column dashboard layout) | Solda sistem göstergeleri, ortada çekirdek, sağda skill kısayolları (karede: Solda 'SYSTEM VITALS', sağda 'SKILLS · QUICK ACCESS' kartları) | 3:42 | kare |
| Mini çizgi grafikleri ve büyük sayı kartları (sparkline stat cards) | Abone, Instagram ve video sayıları küçük grafiklerle (karede: '173K', '234K', '1.3K' değerleri altlarında çizgi grafik) | 3:42 | kare |
| Koyu tema ve ince çerçeveli kartlar (dark theme, outlined cards) | Siyah zemin, ince kenarlıklı kullanım kartı, mono yazı (karede: 'CLAUDE · WEEKLY USAGE' kartı turuncu çerçeveli, 'Unavailable' yazısı) | 3:48 | kare |
| Hareketi duraklatma kontrolü (pause motion toggle) | Animasyonu durduran bağlantı, durum etiketleri ile (karede: Altta 'Idle, Listening, Working' etiketleri ve 'Pause motion' bağlantısı) | 3:42 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm i -g playwright && npx playwright install chromium | Playwright'ı global kurar ve Chromium tarayıcısını indirir (karede: Alt satırda 'npm i -g playwright && npx playwright install chromium') | 8:22 | kare |
| /plugin marketplace add cth9191/animate | Animate deposunu Claude Code plugin marketplace'ine ekler (karede: README'de mavi seçili iki satırdan ilki) | 12:38 | kare |
| /plugin install animate@animate | Animate skill'ini plugin olarak kurar (karede: Seçili ikinci satır '/plugin install animate@animate') | 12:38 | kare |
| /animate a narrated 45s explainer of how DNS works, math style, 16:9, voice from ElevenLabs | Skill'i sesli anlatımlı math stilli videoyla çalıştırır (karede: README 'Use' bölümündeki /animate örnek listesi) | 12:38 | kare |
| /animate how a hash map works, in the math style | Math stilinde hash map anlatım videosu üretir (karede: Use bölümünde ikinci /animate satırı) | 12:38 | kare |
| render showreel --fps 60 --frames 900 | Claude'un yazdığı showreel'i 60 fps ve 900 kare olarak render eder. (karede: Claude Code çıktısında 'render showreel --fps 60 --frames 900' satırı ve altında '900 frames · 15.0 s · 128 bpm' yazıyor.) | 5:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude video üretmiyor; her kare için bir fonksiyon yazıyor, kareler MP4'e birleşiyor. | 0:00 | özellik |
| Saniyede 60 kare üretilip birleştirilerek 1 saniyelik video oluşuyor. | 2:03 | sayısal |
| Low yaklaşık 20 dakika, High yaklaşık 30 dakika, Ultra 8 saat sürdü. | 4:07 | sayısal |
| Low ve High da iyiydi, Ultra en iyisiydi; sorun genelde efor değil prompttur. | 4:07 | karşılaştırma |
| Önce storyboard istemek saatler süren üretim döngülerini önler. | 6:23 | öneri |
| ElevenLabs en iyisi, abonelik yaklaşık 5 dolar; sponsor değil. | 9:20 | sayısal |
| Referans videoya yakın kompozisyon üretiliyor, içerik tamamen farklı. | 10:56 | karşılaştırma |
| Skillry'de 475 Opus 5.5 videosu var; Yearly 79 dolar, Lifetime 169 dolar. | 11:10 | sayısal |
| Animate yedi hazır stille gelir; özel stil referansla eklenir. | 11:43 | özellik |
| Skill kurulumda Playwright, FFmpeg, faster-whisper gibi önkoşulları denetler. | 12:44 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | All you need is clawed code in JavaScript |
| konuşma 0:00 | JavaScript | JavaScript | it uses JavaScript |
| konuşma 0:00 | Remotion (gerek yok denmesi) | Remotion | You don't need Remotion. |
| konuşma 0:00 | After Effects | aday değil: konu dışı | You don't need After Effects. |
| konuşma 0:00 | 3Blue1Brown stili | aday değil: genel kavram | in the style of a three blue one brown video |
| konuşma 2:03 | Playwright | Playwright | headless browser using something like playright |
| konuşma 2:03 | Headless browser (Chromium) | aday değil: başka adayın parçası (Playwright) | clawed code has its own version of Chrome |
| konuşma 2:03 | FFmpeg | FFmpeg | stitches them all via a tool called FFmpeg |
| konuşma 2:03 | ElevenLabs | ElevenLabs | sound generated with 11 Labs |
| konuşma 3:05 | Chase AI Plus ve Claude Code/Codex Masterclass | aday değil: sponsor/reklam | a quick word from today's sponsor, me |
| konuşma 3:05 | AIOS (Jarvis paneli) | aday değil: sponsor/reklam | custom AIOS, which runs not only on Codeex |
| kare 3:42 | Codex | aday değil: sponsor/reklam | Jarvis panelinde 'Codex' modu ve 'GPT-6 Astra' |
| kare 3:42 | Obsidian | aday değil: sponsor/reklam | Jarvis panelinde 'Shared with Obsidian' |
| konuşma 4:07 | Opus 5.5 | Opus 5.5 | I gave Opus 5.5 a pretty simple prompt |
| konuşma 4:07 | Low / High / Ultra efor | Efor düzeyleri | I tested this on low, high, and ultra |
| konuşma 5:21 | Storyboard | Storyboard isteme | ask for a storyboard |
| kare 0:08 | Bahnschrift Variable | Bahnschrift Variable | BAHNSCHRIFT VARIABLE yazısı |
| kare 1:48 | Excalidraw | Excalidraw | excalidraw.com tarayıcıda |
| konuşma 8:20 | Fable 5.1 | Fable 5.1 | opus 5.5 and fable 5.1 are so good |
| konuşma 8:20 | Contact sheet | Contact sheet kontrol döngüsü | use ffmpeg to pull a contact sheet |
| kare 8:22 | Node 18+ | Node.js | Install once: Node 18+ |
| kare 8:22 | npm i -g playwright komutu | npm | npm i -g playwright && npx playwright install chromium |
| kare 8:22 | Whisper (ses zamanlama) | faster-whisper | (Whisper for voice timing) |
| konuşma 9:20 | ElevenLabs MCP/connector | ElevenLabs | They just came out with their MCB. |
| kare 9:08 | elevenlabs.io sayfası | ElevenLabs | Eleven v4 duyurusu ve 'Bringing technology to life' |
| konuşma 9:56 | Remotion (referans videosu) | Remotion | created with Opus 5.5 and Remotion |
| konuşma 9:56 | Referans görsel ve video | Referans görsel/video | start adding references |
| kare 10:04 | Para ve elektrik tarihi karşılaştırma videosu | aday değil: konu dışı | Yan yana 'REFERENCE' ve 'OURS' dikey videolar |
| kare 9:28 | Skillry sitesi | Skillry | skillry.dev/ai-videos/opus-5-5 |
| kare 11:10 | Skillry fiyat planları | aday değil: başka adayın parçası (Skillry) | $9.99 aylık, $79 yıllık, $169 ömür boyu |
| kare 11:20 | Kevin Ngo X profili | aday değil: konu dışı | x.com/kevin_t_ngo, 'Creative coding with AI' |
| kare 11:20 | X (Twitter) arayüzü, Grok | aday değil: konu dışı | Sol menüde Grok ve Premium |
| kare 11:12 | ChatGPT ve Grok etiketleri | aday değil: konu dışı | Skillry/X sayfalarında küçük görünen başlıklar |
| konuşma 11:43 | Animate skill | Animate | turning it into a skill |
| kare 11:44 | Animate stilleri (cut-paper, crosshatch, riso, sketchbook, math, pixel, isometric) | aday değil: başka adayın parçası (Animate) | README'de sekiz stil kartı |
| kare 11:44 | GitHub Actions / Deno önerilen iş akışları | aday değil: konu dışı | Sağ sütunda 'Publish Node.js Package' ve 'Deno' |
| kare 12:38 | Python | aday değil: başka adayın parçası (faster-whisper) | Python with faster-whisper (word timing) |
| konuşma 12:44 | faster-whisper | faster-whisper | things like faster whisper |
| kare 12:38 | /plugin komutları | aday değil: başka adayın parçası (Animate) | /plugin marketplace add cth9191/animate |
| açıklama | skool.com/chase-ai, chase-ai-community | aday değil: sponsor/reklam | Ücretli topluluk bağlantıları |
| açıklama | chaseai.io, www.chaseai.io | aday değil: konu dışı | Kişisel site |
| açıklama | github.com/cth9191/animate | Animate | Animate repo bağlantısı |
| yorum | Remotion ve Hyperframes tartışması | aday değil: konu dışı | My doubt is, why not use Remotion or Hyperframes? |
| yorum | Higgsfield, DaVinci Resolve, Three.js, WebGL, DeepSeek | aday değil: konu dışı | İzleyici yorumlarında geçiyor, videoda kullanılmıyor |
| linkli sayfa | awesome-opus5-5-videos listesi | aday değil: konu dışı | skillry.dev/ai-videos/opus-5-5 yönlendirmeli GitHub listesi |
## Kareden okunanlar
- 0:08: Bahnschrift Variable, WGHT 300-700, WDTH 75-100; büyük 'EASE' yazısı ve eğri grafikleri
- 0:36: Claude Code sohbetinde 'A video is a function' 45.7s, 16:9 60fps, math style, ElevenLabs narration (Alex); altta Opus 5.5 High
- 3:54: Showreel promptu ve Opus 5.5 Low; 15 saniyelik 1080p60, 128 BPM
- 8:22: Install once: Node 18+ · npm i -g playwright && npx playwright install chromium · FFmpeg · Whisper
- 11:36: Animate README: How it works tablosu (Intake, Story check, Look check, Storyboard, Build, Delivery)
- 12:38: /plugin marketplace add cth9191/animate; /plugin install animate@animate; Requirements: Claude Code, Node 18+, Playwright, ffmpeg
- 11:10: Skillry fiyatları: $9.99/ay, $79/yıl, $169 ömür boyu
## Belirsizlikler
- Chase AI Plus için 'sponsor, me' denmesi şaka; gerçek sponsorluk değil, bağlantı 'diğer' sınıfında.
- Fable 5.1 anlatıda geçiyor ama ekranda görünmüyor.
- Showreel karelerindeki iridescence ve ışın izleme benzeri OCR metni okunaksız; gölgelendirici tekniği adı doğrulanamadı.
- Storyboard prompt kanıtında kare zamanı net değil; storyboard paneli 5:34–5:40 karelerinde görünüyor.
- Jarvis paneli sponsor bölümünde gösterilen kendi ürünü; site_ui videonun asıl konusu değil.
- Yorumlardaki Remotion, Hyperframes, Higgsfield, DaVinci Resolve, Three.js tartışmaları videoda uygulanmadı.
## Atlanan segment oranı
0/16 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.skool.com/chase-ai | açıklama | açıklama | hayır |
| https://www.skool.com/chase-ai-community | açıklama | açıklama | hayır |
| https://chaseai.io | açıklama | açıklama | hayır |
| https://www.chaseai.io | açıklama | açıklama | hayır |
| https://github.com/cth9191/animate | açıklama | açıklama | evet |
| excalidraw.com | 1:48 | ekran | evet |
| github.com/cth9191/animate | 3:18 | ekran | evet |
| skool.com/chase-ai/classroom | 3:32 | ekran | hayır |
| elevenlabs.io | 9:08 | ekran | evet |
| skillry.dev/ai-videos/opus-5-5 | 9:28 | ekran | evet |
| skillery.dev | 10:56 | ses | evet |
| x.com/kevin_t_ngo | 11:20 | ekran | hayır |
| https://t.co/mt2OgbYbso | 11:20 | ekran | hayır |
| https://github.com/cth9191/animate/blob/main/docs/styles.png | 11:44 | ekran | hayır |
| https://github.com/yihui-dev/awesome-opus5-5-videos?utm_source=skillry&utm_medium=referral&utm_campaign=opus-5-5-videos | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Showreel promptunu Low efor ile Claude Code'a yazma — araçlar: Claude Code, Opus 5.5
- 2. adım — Aynı promptu High ve Ultra eforla çalıştırıp süre ve kaliteyi karşılaştırma — araçlar: Claude Code, Opus 5.5
- 3. adım — Uzun videodan önce storyboard isteyip sahne karelerini inceleme — araçlar: Claude Code
- 4. adım — Prompta süre, en-boy oranı, JavaScript ve ses yöntemini yazma — araçlar: Claude Code, JavaScript
- 5. adım — Playwright ve FFmpeg ile render yapılmasını isteme — araçlar: Playwright, FFmpeg
- 6. adım — İsteğe bağlı ses dosyasına göre görselleri zamanlama — araçlar: ElevenLabs, faster-whisper
- 7. adım — Contact sheet çıkarıp bakma, düzeltme, yeniden render alma — araçlar: FFmpeg, Playwright, Claude Code
- 8. adım — Şemayı anlatmak için akışı çizme — araçlar: Excalidraw
- 9. adım — Referans video ile aynı kompozisyonda yeni içerik üretme — araçlar: Claude Code, Remotion
- 10. adım — İlham için Skillry'deki Opus 5.5 videolarına bakma — araçlar: Skillry
- 11. adım — Animate skill'ini plugin olarak kurma — araçlar: Claude Code, Animate
- 12. adım — Skill'in intake, hikâye, stil kontrolü ve storyboard aşamalarını onaylama — araçlar: Animate
- 13. adım — Onaylanan panelleri kodlayıp render etme ve ses döngüsünde kontrol etme — araçlar: Animate, Playwright, FFmpeg, ElevenLabs
## Promptlar
- Efor düzeylerini (Low, High, Ultra) karşılaştıran test promptu — 15 saniyelik, bir özgeçmiş showreel'i gibi dinamik hareketli grafik videosu istenir; en iyisini yap, hiçbir skill kullanma.
- Seviye 2'deki araçlar ve döngü prompt şablonu — [KONU] nasıl çalışır konusunda 30 saniyelik, 16:9 animasyonlu anlatım; JavaScript canvas ile, sesi kodla üretilmiş, Playwright ve FFmpeg ile MP4. İsteğe bağlı ses dosyasına göre Whisper zamanlaması. Bitirmeden contact sheet çıkarıp bak, düzelt, yeniden render al, tekrarla.
- Uzun üretim döngülerinden kaçınmak için storyboard isteme — Tek seferde uzun video üretmeden önce yedi kadar sahneyi gösteren storyboard kareleri iste, onay sonrası kodla.
