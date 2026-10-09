# Don’t start vibe coding with Claude Code until these 4 plugins are in.
## Künye
Don’t start vibe coding with Claude Code until these 4 plugins are in. · adilet.fndr · süre: 0:51 · ? · https://www.instagram.com/reel/Ddb1UVZIakr/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-26 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 17568 tk · claude-haiku-5-5: claude-haiku-5-5 · 32381 tk
## Özet
Kısa Instagram reel'i: Claude Code ile vibe coding'e başlamadan önce kurulması önerilen 4 eklenti tanıtılıyor. Ponytail (daha az kod ve token), OmniRoute (tek yerel uç nokta, 352 sağlayıcı, limit dolunca otomatik model geçişi), Graphify (kod tabanını bilgi grafiğine çevirir) ve Agent Skills (Addy Osmani'nin 24 skill'i). İzleyiciye 'coding' yorumu yazması söyleniyor.
## Bölümler
- 0:00 Giriş: 4 eklenti kurulumu
- 0:04 Ponytail: daha az kod, daha az token
- 0:11 OmniRoute: tek uç nokta, otomatik geçiş
- 0:25 Graphify: kod tabanı bilgi grafiği
- 0:32 Agent Skills: 24 skill
- 0:47 Kapanış: 'coding' yorumu çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Eklentilerin kurulduğu ana yapay zekâ kodlama aracı | 0:00 | Ekranda 'Welcome to Claude Code' ve terminal penceresi görünüyor (karede: Alt kısımda claude — ~/vibely terminali, /plugin komutları) |
| Claude Opus 5 | yok | teknik | yok | Terminalde görünen model adı | 0:00 | OCR: 'Claude Opus 5' (karede: Bu model adı gönderilen karelerde değil, OCR metninde görünüyor) |
| Ponytail | yok | plugin | yok | Claude'un daha az kod yazmasını sağlar, token kullanımını yarıya yakın azaltır | 0:04 | /plugin install ponytail@ponytail; ponytail 4.10.0 · 6 skills · 2 hooks (karede: Üç karede terminalde '/plugin install ponytail@ponytail' ve '✓ ponytail 4.10.0 · 6 skills · 2 hooks') |
| OmniRoute | yok | CLI | yok | Tek yerel uç noktada 352 sağlayıcı; limit dolunca otomatik model geçişi | 0:11 | npx omniroute; OmniRoute 3.8.50 · localhost:20128 · 352 providers (karede: README kartında 'OmniRoute', 'The Free AI Gateway', 'MIT license', v3.8.50; terminalde npx omniroute) |
| Graphify | yok | plugin | yok | Kod tabanını bilgi grafiğine çevirir; ajan dosyaları yeniden okumaz | 0:25 | Graphify, turns your entire codebase into a knowledge graph |
| Agent Skills | yok | skill | yok | Addy Osmani'nin 24 skill'lik paketi; aşamaya göre otomatik devreye girer | 0:32 | npx skills add addyosmani/agent-skills; 24 skills · 9 commands |
| Skills CLI | yok | CLI | yok | npx skills add ile skill paketini kurar | 0:32 | Ekran: npx skills add addyosmani/agent-skills |
| npx | yok | CLI | yok | OmniRoute ve skills kurulumunda çalıştırıcı | 0:11 | npx omniroute komutu (karede: Terminalde '> npx omniroute') |
| tree-sitter | yok | teknik | yok | Graphify'da 1.240 dosyayı LLM çağrısı olmadan ayrıştırma | 0:25 | OCR: parsing 1,240 files · tree-sitter · 0 LLM calls |
| Kimi K2 | yok | teknik | yok | OmniRoute sağlayıcı listesinde model; yedek model olarak geçiş | 0:14 | Providers listesi ve 'kimi-k2 - switched' (karede: Providers panelinde 'Kimi K2' anahtarı açık, '1 Connected') |
| DeepSeek | yok | teknik | yok | OmniRoute'ta ücretsiz katman sağlayıcı | 0:14 | Providers listesinde DeepSeek, free tier (karede: 'DeepSeek · free tier' kartı) |
| Gemini 2.5 | yok | teknik | yok | Limit dolunca geçilen sonraki en iyi model | 0:20 | OCR: switching → Gemini 2.5 - next best model |
| Groq | yok | teknik | yok | OmniRoute sağlayıcısı | 0:15 | Providers listesinde Groq, 1 Connected (karede: 'Groq · 1 Connected' kartı, anahtar açık) |
| Mistral | yok | teknik | yok | OmniRoute sağlayıcısı | 0:15 | Providers listesinde Mistral (karede: 'Mistral · free tier' kartı) |
| NVIDIA NIM | yok | teknik | yok | OmniRoute sağlayıcısı | 0:15 | Providers listesinde NVIDIA NIM (karede: 'NVIDIA NIM · free tier' kartı) |
| OpenRouter | yok | teknik | yok | OmniRoute sağlayıcısı | 0:15 | Providers listesinde OpenRouter, 1 Connected (karede: 'OpenRouter · 1 Connected' kartı) |
| Cloudflare AI | yok | teknik | yok | OmniRoute sağlayıcısı | 0:15 | Providers listesinde Cloudflare AI (karede: 'Cloudflare AI · 1 Connected' kartı) |
| Hugging Face | yok | teknik | yok | OmniRoute sağlayıcısı | 0:15 | Providers listesinde Hugging Face (karede: 'Hugging Face · 1 Connected' kartı) |
| Docker | yok | teknik | yok | Graphify'ın ayrıştırdığı dosyalar arasında Dockerfile/docker-compose | 0:26 | OCR: Dockerfile, docker-compose.yml |
| SaaS geliştirme ve tarih seçici ekleme örneği | yok | prompt | yok | Kullanıcı Claude Code'a bu hafta sonu bir SaaS geliştirmesini söylüyor; ardından 'add a date picker' ile Ponytail karşılaştırması gösteriliyor. | 0:06 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /plugin | Claude Code eklenti menüsünü açar (karede: Terminalde '> /plugin' satırı) | 0:12 | kare |
| /plugin install ponytail@ponytail | Ponytail eklentisini kurar (karede: Terminalde '> /plugin install ponytail@ponytail' ve onay satırı) | 0:04 | kare |
| npx omniroute | OmniRoute'u yerelde localhost:20128 üzerinde başlatır (karede: Terminalde '> npx omniroute' ve 'OmniRoute 3.8.50 · localhost:20128') | 0:11 | kare |
| npx skills add addyosmani/agent-skills | Agent Skills paketini kurar | 0:32 | altyazı |
| /spec /plan /build /test /review /ship | Agent Skills'in aşama komutları; her aşamada ilgili skill kendiliğinden devreye girer. | açıklama | açıklama |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ponytail token kullanımını %50'nin üzerinde azaltır, doğruluk kaybı yok | 0:04 | sayısal |
| OmniRoute 300+ ücretsiz sağlayıcıya bağlanır, limit dolunca otomatik geçer, ayda 1,6 milyar ücretsiz token | 0:11 | sayısal |
| Graphify kod tabanını bilgi grafiğine çevirir, ajan dosyaları yeniden okumaz | 0:25 | özellik |
| Agent Skills 24 skill içerir, doğru aşamada kendiliğinden devreye girer | 0:32 | özellik |
| Ponytail ile 404 satır/48.120 token yerine 1 satır/19.898 token (ekran karşılaştırması) | 0:06 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:00 | Claude Code | Claude Code | Welcome to Claude Code |
| ekran 0:00 | Claude Opus 5 | Claude Opus 5 | Claude Opus 5 |
| konuşma 0:04 | Ponytail | Ponytail | The first is Ponytail |
| ekran 0:11 | npx | npx | npx omniroute |
| konuşma 0:11 | OmniRoute | OmniRoute | OmniRoute 3.8.50 |
| ekran 0:12 | GitHub Trending rozeti | aday değil: konu dışı | GITHUB TRENDING #1 Repository Of The Week |
| ekran 0:12 | localhost:20128 | OmniRoute | OmniRoute yerel uç noktası |
| ekran 0:14 | Kimi K2 | Kimi K2 | Providers: Kimi K2 |
| ekran 0:14 | DeepSeek | DeepSeek | Providers: DeepSeek |
| ekran 0:20 | Gemini 2.5 | Gemini 2.5 | switching → Gemini 2.5 |
| ekran 0:15 | Groq | Groq | Groq 1 Connected |
| ekran 0:15 | Mistral | Mistral | Mistral free tier |
| ekran 0:15 | NVIDIA NIM | NVIDIA NIM | NVIDIA NIM free tier |
| ekran 0:15 | OpenRouter | OpenRouter | OpenRouter 1 Connected |
| ekran 0:15 | Cloudflare AI | Cloudflare AI | Cloudflare AI 1 Connected |
| ekran 0:15 | Hugging Face | Hugging Face | Hugging Face 1 Connected |
| ekran 0:15 | Amazon Q, Blackbox AI, Cerebras, Together AI vb. diğer sağlayıcılar | aday değil: başka adayın parçası (OmniRoute) | Providers listesi kartları |
| konuşma 0:25 | Graphify | Graphify | The third is Graphify |
| ekran 0:25 | tree-sitter | tree-sitter | parsing 1,240 files · tree-sitter |
| ekran 0:26 | Dockerfile, docker-compose.yml, README.md, pyproject.toml, .env.example | aday değil: başka adayın parçası (Graphify) | Ayrıştırılan örnek dosyalar |
| ekran 0:32 | npx skills add addyosmani/agent-skills | Skills CLI | Komut satırı |
| konuşma 0:35 | Agent Skills | Agent Skills | pack of 24 skills |
| ekran 0:37 | Addy Osmani | aday değil: konu dışı | Skill paketinin yazarı, araç değil |
| ekran 0:34 | skill adları (accessibility, debugging, security vb.) | aday değil: başka adayın parçası (Agent Skills) | Skill listesi |
| açıklama | /spec /plan /build /test /review /ship | aday değil: başka adayın parçası (Agent Skills) | Açıklamadaki komutlar |
| ekran 0:47 | Instagram yorum arayüzü | aday değil: konu dışı | Add a comment.. / Comments |
| açıklama | Comment CODING kurulum rehberi | aday değil: sponsor/reklam | Yorum yaz, kurulum rehberi gönderilir |
## Kareden okunanlar
- 0:12: OmniRoute README: 'The Free AI Gateway', 352 providers, 1,200+ models, MIT license, v3.8.50, #1 Repository Of The Week; terminalde /plugin install ponytail@ponytail ve npx omniroute
- 0:14: Providers paneli: 248 providers · 154 free; Kimi K2, DeepSeek, Gemini 2.5; Claude Code → OR → sağlayıcılar diyagramı; 'context ∞ · omniroute'
- 0:15: Providers paneli: 318 providers · 154 free; Kimi K2, Groq, OpenRouter, Cloudflare AI, Amazon Q, Hugging Face vb. kartları; 'over 300 other' başlığı
## Belirsizlikler
- Yorumlar girişsiz alınamadı; yorum kaynaklı URL/bilgi yok.
- Konuşmada 'OnlyRoute' deniyor, ekranda OmniRoute yazıyor; ekran adı kullanıldı.
- Sağlayıcı sayısı karelerde 248, 318 ve 352 olarak değişiyor.
- Graphify ve Agent Skills için repo URL'si videoda yok; skills komutundaki addyosmani/agent-skills yol bilgisi.
- Sözlük eşleşmeleri (Next.js, Outfit, Codex, Stitch, Grok, Inter, Go) videoda kullanılmıyor, aday yapılmadı; Grok kareden doğrulanamadı.
- Ekranda 'Amazon Q, Blackbox AI, Cerebras vb.' sadece sağlayıcı listesi; ayrı aday yapılmadı.
- '/plugin install ponytail@ponytail' ve Graphify kurulum komutu: Graphify komutu videoda gösterilmiyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| localhost:20128 | 0:12 | ekran | hayır |
## İş akışı
- 1. adım — Claude Code'u açıp SaaS yapma isteği ve 4 eklenti kurulum ekranı — araçlar: Claude Code, Claude Opus 5
- 2. adım — Ponytail eklentisini /plugin install ile kurma — araçlar: Claude Code, Ponytail
- 3. adım — Ponytail'li ve Ponytail'siz satır/token karşılaştırması (tarih seçici) — araçlar: Ponytail
- 4. adım — Testlerin geçtiğini doğrulama (42 passed) — araçlar: Ponytail
- 5. adım — OmniRoute'u npx ile başlatma — araçlar: OmniRoute, npx
- 6. adım — Sağlayıcıları (Kimi K2, DeepSeek, Groq vb.) bağlama — araçlar: OmniRoute
- 7. adım — Limit dolunca otomatik Gemini 2.5/Kimi K2'ye geçiş — araçlar: OmniRoute, Gemini 2.5, Kimi K2
- 8. adım — Graphify ile kod tabanını bilgi grafiğine çevirme — araçlar: Graphify, tree-sitter
- 9. adım — Grafik sorgusu ile dosya okumaya karşı token tasarrufu — araçlar: Graphify
- 10. adım — Agent Skills'i npx skills add ile kurma — araçlar: Skills CLI, Agent Skills
- 11. adım — Skill'lerin aşamalara göre otomatik devreye girmesini gösterme — araçlar: Agent Skills
- 12. adım — 4/4 eklenti hazır ve 'coding' yorumu çağrısı — araçlar: Claude Code
## Promptlar
- SaaS geliştirme ve tarih seçici ekleme örneği — Kullanıcı Claude Code'a bu hafta sonu bir SaaS geliştirmesini söylüyor; ardından 'add a date picker' ile Ponytail karşılaştırması gösteriliyor.
ikinci göz KAPALI: --ikinci-goz yok
