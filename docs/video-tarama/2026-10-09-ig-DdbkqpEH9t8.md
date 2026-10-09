# One free endpoint replaced a wall of paid
## Künye
One free endpoint replaced a wall of paid · bitbyybit · süre: 0:00 · ? · https://www.instagram.com/p/DdbkqpEH9t8/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-9 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (7)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 35558 tk · claude-haiku-5-5: claude-haiku-5-5 · 51751 tk
## Özet
Instagram görsel gönderisi (carousel), freellmapi adlı açık kaynak projeyi tanıtıyor. Proje, 34 ücretsiz LLM sağlayıcısını tek bir OpenAI uyumlu /v1 uç noktasının arkasında topluyor (635 model uç noktası, ayda ~7.4 milyar ücretsiz token iddiası). Kod değiştirmeden yalnız base URL değiştirilir. Bir ücretsiz katman limite ya da 429'a takılınca otomatik olarak sonraki sağlayıcıya geçer. Tek curl komutuyla yerelde çalışır, panel localhost:3001'de açılır.
## Bölümler
- 0:00 Giriş: tek URL, 635 ücretsiz model
- 0:00 Kaynak: GitHub deposu (The Source)
- 0:00 İddia: 7.4 milyar token, 34 sağlayıcı (The Claim)
- 0:00 Nedir: tek uç nokta (What it is)
- 0:00 Sayılar: 635 uç nokta ve sağlayıcı tablosu
- 0:00 Otomatik failover ve kurulum
- 0:00 Kapanış: follow for more
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| freellmapi | yok | CLI | https://github.com/tashfeenahmed/freellmapi | 34 ücretsiz LLM sağlayıcısını tek OpenAI uyumlu uç noktada toplayan yerel proxy; limitte otomatik sağlayıcı değiştirir. | 0:00 | GitHub deposu tashfeenahmed/freellmapi ve açıklamadaki 'one OpenAI-compatible URL' (karede: Görsel 2: github.com/tashfeenahmed/freellmapi deposu, 22.2k yıldız, 7.4 billion tokens per month açıklaması.) |
| OpenAI-compatible API | yok | teknik | yok | Mevcut OpenAI istemcisi kodunu değiştirmeden yalnız base URL değiştirerek kullanma yaklaşımı. | 0:00 | 'SWAP ONE BASE URL AND KEEP YOUR OPENAI CODE' · kanıt: kare (karede: Görsel 1 alt yazısı: SWAP ONE BASE URL AND KEEP YOUR OPENAI CODE; görsel 4: One OpenAI-compatible /v1 endpoint.) |
| Groq | yok | MCP | yok | Ücretsiz katmanı sağlayıcılar arasında listelenen LLM sağlayıcısı (66 uç nokta). | 0:00 | Sağlayıcı tablosunda Groq satırı: chat 62, embeddings 4, toplam 66 (karede: Görsel 5: tabloda Groq 62 / 4 / 0 / 0 / 66; kablo etiketi Groq.) |
| Gemini | yok | MCP | yok | Google'ın modeli/servisi; sağlayıcı tablosunda 60 uç nokta. | 0:00 | Tabloda Gemini satırı toplam 60 (karede: Görsel 5: Gemini 52 / 8 / 0 / 0 / 60.) |
| Mistral | yok | MCP | yok | Sağlayıcı tablosunda 49 uç nokta ile listelenen ücretsiz LLM sağlayıcısı. | 0:00 | Tabloda Mistral satırı toplam 49 (karede: Görsel 5: Mistral 42 / 7 / 0 / 0 / 49.) |
| Cerebras | yok | MCP | yok | Sağlayıcı tablosunda 32 uç nokta ile listelenen ücretsiz LLM sağlayıcısı. | 0:00 | Tabloda Cerebras satırı toplam 32 (karede: Görsel 5: Cerebras 28 / 4 / 0 / 0 / 32.) |
| NVIDIA | yok | MCP | yok | Sağlayıcı tablosunda 27 uç nokta ile listelenen sağlayıcı. | 0:00 | Tabloda NVIDIA satırı toplam 27 (karede: Görsel 5: NVIDIA 24 / 3 / 0 / 0 / 27.) |
| Cloudflare | yok | MCP | yok | Sağlayıcı tablosunda 26 uç nokta ile listelenen sağlayıcı. | 0:00 | Tabloda Cloudflare satırı toplam 26 (karede: Görsel 5: Cloudflare 22 / 4 / 0 / 0 / 26.) |
| OpenRouter | yok | MCP | yok | Tabloda en çok uç noktaya sahip sağlayıcı (95). | 0:00 | Tabloda OpenRouter satırı toplam 95 (karede: Görsel 5: OpenRouter 78 / 17 / 0 / 0 / 95.) |
| Together AI | yok | MCP | yok | Tabloda 23 uç noktalı sağlayıcı; commit'te together.ai eklendiği görülür. | 0:00 | Tabloda Together AI toplam 23; docs: add together.ai to providers table (karede: Görsel 5: Together AI 20 / 3 / 0 / 0 / 23; görsel 2 docs commit mesajı.) |
| Fireworks | yok | MCP | yok | Tabloda 21 uç noktalı sağlayıcı. | 0:00 | Tabloda Fireworks toplam 21 (karede: Görsel 5: Fireworks 18 / 3 / 0 / 0 / 21.) |
| Hyperbolic | yok | MCP | yok | Tabloda 18 uç noktalı sağlayıcı. | 0:00 | Tabloda Hyperbolic toplam 18 (karede: Görsel 5: Hyperbolic 16 / 2 / 0 / 0 / 18.) |
| Replicate | yok | MCP | yok | Tabloda 16 uç noktalı sağlayıcı. | 0:00 | Tabloda Replicate toplam 16 (karede: Görsel 5: Replicate 14 / 2 / 0 / 0 / 16.) |
| DeepInfra | yok | MCP | yok | Tabloda 14 uç noktalı sağlayıcı. | 0:00 | Tabloda DeepInfra satırı toplam 14 (karede: Görsel 5: Deepinfra 12 / 2 / 0 / 0 / 14.) |
| curl | yok | CLI | yok | Kurulum betiğini indirip bash'e aktaran komut satırı aracı. | 0:00 | Terminalde curl -fsSL ... / bash (karede: Görsel 6: terminalde curl -fsSL https://freellmapi.co/install.sh / bash.) |
| Otomatik failover | yok | teknik | yok | Sağlayıcı başına anahtar limitini izleyip 429/limit durumunda sıradaki sağlayıcıya geçme. | 0:00 | 'rotates to the next provider automatically' · kanıt: kare (karede: Görsel 6: auto failover başlığı ve açıklama; AUTO düğmesi Provider A-D.) |
| GitHub | yok | teknik | yok | Kaynak kodun barındığı platform; depo sayfası gösterilir. | 0:00 | Tarayıcı adres çubuğunda github.com/tashfeenahmed/freellmapi (karede: Görsel 2: GitHub deposu arayüzü, adres çubuğunda github.com/tashfeenahmed/freellmapi.) |
| bash | yok | CLI | yok | İndirilen kurulum betiğini kabukta çalıştırmak için boru ile verilen shell. | 0:00 | Kare 6 terminal: komut sonunda '/ bash'. (karede: kanıttan) Kare 6 terminal: komut sonunda '/ bash'. |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://freellmapi.co/install.sh / bash | freellmapi'yi yerelde kurar; panel localhost:3001'de açılır, anahtarlar eklenip yedek zinciri sıralanır. (karede: Görsel 6: terminalde curl -fsSL https://freellmapi.co/install.sh / bash, altında dashboard live at localhost:3001.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 34 ücretsiz LLM sağlayıcısı ve 635 ücretsiz model uç noktası tek URL arkasında. | 0:00 | sayısal |
| Ayda yaklaşık 7.4 milyar ücretsiz token sağlanıyor. | 0:00 | sayısal |
| 635 uç nokta: 584 chat, 41 embeddings, 7 transkripsiyon, 3 video. | 0:00 | sayısal |
| Kod değişmeden yalnız base URL değiştirilerek kullanılır. | 0:00 | özellik |
| Limit ya da 429 olunca otomatik sonraki sağlayıcıya geçer; hiçbir şey bozulmaz, ödeme yok. | 0:00 | özellik |
| Yerelde tek curl komutuyla çalışır; panel localhost:3001. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| açıklama | freellmapi / 34 ücretsiz LLM sağlayıcısı tek URL | freellmapi | 34 free LLM providers behind one OpenAI-compatible URL |
| kare 0:00 | OpenAI kodu, base URL değişimi | OpenAI-compatible API | SWAP ONE BASE URL AND KEEP YOUR OPENAI CODE |
| kare 0:00 | GitHub deposu tashfeenahmed/freellmapi | GitHub | Tarayıcı adres çubuğu github.com/tashfeenahmed/freellmapi |
| kare 0:00 | Groq | Groq | Tabloda Groq 66 ve kablo etiketi |
| kare 0:00 | Gemini | Gemini | Tabloda Gemini 60 |
| kare 0:00 | Mistral | Mistral | Tabloda Mistral 49 |
| kare 0:00 | Cerebras | Cerebras | Tabloda Cerebras 32 |
| kare 0:00 | NVIDIA | NVIDIA | Tabloda NVIDIA 27 |
| kare 0:00 | Cloudflare | Cloudflare | Tabloda Cloudflare 26 |
| kare 0:00 | OpenRouter | OpenRouter | Tabloda OpenRouter 95 |
| kare 0:00 | Together AI | Together AI | Tabloda Together AI 23 |
| kare 0:00 | Fireworks | Fireworks | Tabloda Fireworks 21 |
| kare 0:00 | Hyperbolic | Hyperbolic | Tabloda Hyperbolic 18 |
| kare 0:00 | Replicate | Replicate | Tabloda Replicate 16 |
| kare 0:00 | DeepInfra | DeepInfra | Tabloda DeepInfra 14 |
| kare 0:00 | curl kurulum komutu | curl | curl -fsSL https://freellmapi.co/install.sh / bash |
| kare 0:00 | Otomatik failover / 429 yönlendirme | Otomatik failover | rotates to the next provider automatically |
| kare 0:00 | localhost:3001 paneli | aday değil: başka adayın parçası (freellmapi) | dashboard live at localhost:3001 |
| kare 0:00 | Kablo/priz/AUTO düğmesi görselleri | aday değil: konu dışı | Dekoratif priz, kablo ve düğme görselleri |
| kare 0:00 | Hesap/depo menüleri, Issues, Pull requests | aday değil: başka adayın parçası (GitHub) | GitHub arayüzü sekmeleri |
| açıklama | Hashtag'ler #freellmapi #freeapi #llm #aitools #devtools | aday değil: genel kavram | Açıklama sonundaki etiketler |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- Görsel 1 · 0:00: 34 FREE LLM PROVIDERS; one url. 635 free models.; SWAP ONE BASE URL AND KEEP YOUR OPENAI CODE.
- Görsel 2 · 0:00: GitHub tashfeenahmed/freellmapi; Fork 2.3k, Star 22.2k, Issues 164, PR 48, 342 commits; son commit 'fix: put 402 on top of 429 (#387)'.
- Görsel 3 · 0:00: 7.4 billion tokens per month. 34 free LLM providers. 635 free model endpoints.
- Görsel 4 · 0:00: One OpenAI-compatible /v1 endpoint, 34 ücretsiz sağlayıcı katmanının önünde; more info github.com/tashfeenahmed/freellmapi.
- Görsel 5 · 0:00: 584 chat, 41 embeddings, 7 transcription, 3 video; sağlayıcı tablosu OpenRouter 95, Groq 66, Gemini 60, Mistral 49, Cerebras 32 vb.
- Görsel 6 · 0:00: curl -fsSL https://freellmapi.co/install.sh / bash; dashboard live at localhost:3001; add keys, reorder fallback chain.
- Görsel 7 · 0:00: follow for more.
## Belirsizlikler
- Video değil görsel gönderi; süre 0:00 olduğundan tüm zamanlar 0:00 olarak yazıldı.
- Terminal görselinde kullanıcı adı 'nikhil@macbook' görünüyor; depo sahibi tashfeenahmed, kurulum betiği alan adının (freellmapi.co) resmî olup olmadığı doğrulanmadı.
- Açıklamadaki ~7.4B token ve 635 uç nokta rakamları depo iddiasından alındı, doğrulanmadı.
- Açıklamada 'Comment url for link' var; yorumlara girişsiz erişilemedi, bağlantı bilinmiyor.
- Açıklamadaki 'Grok' sözlük eşleşmesi; ekranda yazılan ad Groq, xAI Grok ile karıştırılmamalı.
- Açıklama ve görseller OpenAI istemcisini anıyor ama OpenAI bir sağlayıcı olarak kullanılmıyor, yalnız uyumluluk hedefi.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/tashfeenahmed/freellmapi | 0:00 | ekran | evet |
| https://freellmapi.co/install.sh | 0:00 | ekran | evet |
| localhost:3001 | 0:00 | ekran | hayır |
## İş akışı
- 1. adım — Mevcut OpenAI istemci kodu korunur, yalnız base URL freellmapi uç noktasına çevrilir. — araçlar: freellmapi, OpenAI-compatible API
- 2. adım — Kurulum betiği curl ile indirilip bash'e verilerek yerelde kurulur. — araçlar: curl, freellmapi
- 3. adım — localhost:3001 panelinde sağlayıcı anahtarları eklenir. — araçlar: freellmapi
- 4. adım — Yedek (fallback) zinciri panelde yeniden sıralanır. — araçlar: freellmapi
- 5. adım — İstekler ücretsiz sağlayıcılara yönlendirilir; limit ya da 429'da sıradaki sağlayıcıya otomatik geçilir. — araçlar: freellmapi, Otomatik failover, Groq, Gemini, Mistral, Cerebras
## Promptlar
- yok
