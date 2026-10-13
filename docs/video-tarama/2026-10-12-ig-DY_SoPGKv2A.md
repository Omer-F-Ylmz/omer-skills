# Follow me then comment “FLOW” and I’ll send you the setup guide.
## Künye
Follow me then comment “FLOW” and I’ll send you the setup guide. · kayvon.ai · süre: 0:35 · ? · https://www.instagram.com/reel/DY_SoPGKv2A/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-12-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 33512 tk · claude-haiku-5-5: claude-haiku-5-5 · 39430 tk
## Özet
Kısa reel, Ruflo adlı açık kaynaklı çoklu ajan orkestrasyon platformunu tanıtıyor. Anlatıcıya göre 60 ajan paralel çalışıyor, bellek paylaşıyor ve her çalıştırmadan sonra gelişiyor; planlama, kod, test ve güvenlik ajanları var. Maliyet yönlendirmesi basit görevleri ücretsiz katmana, zor görevleri uygun modele gönderiyor; %75 API tasarrufu iddia ediliyor. GitHub README'si, flo.ruv.io sohbet arayüzü, maliyet panosu ve depo istatistikleri gösteriliyor. Video 'FLOW' yorumu için takip çağrısıyla bitiyor.
## Bölümler
- 0:00 Giriş: Ruflo ve 60 paralel ajan
- 0:02 README: yetenekler ve Claude Code kurulum satırı
- 0:09 flo.ruv.io çoklu model sohbeti ve goal.ruv.io
- 0:14 Ajan rolleri ve paylaşılan bellek şeması
- 0:20 Maliyet yönlendirme panosu (%75 tasarruf)
- 0:30 GitHub Pulse ve sürümler
- 0:34 Yorum çağrısı (FLOW)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Ruflo | yok | plugin | https://github.com/ruvnet/ruflo | Claude için açık kaynaklı çoklu ajan orkestrasyon platformu; MCP sunucusu olarak eklenir | 0:00 | It's called Ruflo and this thing is insane. |
| Claude Code | yok | CLI | yok | Ruflo'nun MCP sunucusu olarak eklendiği komut satırı aracı | 0:02 | README'de Add Ruflo as an MCP server in Claude Code satırı (karede: README üstünde 'claude mcp add ruflo -- npx ruflo@latest mcp start' satırı okunuyor) |
| MCP | yok | MCP | yok | Ruflo araçlarını Claude'a bağlayan Model Context Protocol sunucusu | 0:02 | claude mcp add ruflo ... mcp start (karede: README'de MCP sunucusu ekleme satırı) |
| npm | yok | CLI | yok | npx ile Ruflo'yu çalıştırma; 21 npm eklentisi | 0:02 | npx ruflo@latest mcp start (karede: README satırında npx ruflo@latest) |
| flo.ruv.io | yok | teknik | yok | Ruflo'nun çoklu model sohbet arayüzü; paralel MCP araç çağrısı | 0:09 | Multi-model chat at flo.ruv.io with parallel MCP tool calling (karede: README satırı flo.ruv.io çoklu model sohbetini anlatıyor) |
| goal.ruv.io | yok | teknik | yok | GOAP A* planlayıcı; sade dilde hedefleri çalıştırılabilir plana çevirir | 0:09 | GOAP A* planner at goal.ruv.io (karede: README satırında goal.ruv.io) |
| OpenRouter | yok | teknik | yok | README'de 6 öncü modelin sağlandığı servis | 0:16 | 6 curated frontier models ... via OpenRouter (karede: README tablosunda 'via OpenRouter' ifadesi) |
| Qwen 3.6 Max | yok | teknik | yok | Ruflo web arayüzünde varsayılan model | 0:16 | Qwen 3.6 Max (default) (karede: README tablosunda model listesi) |
| Claude Sonnet 4.6 | yok | teknik | yok | README'deki hazır modellerden biri | 0:16 | Claude Sonnet 4.6 model listesinde (karede: README tablosunda model listesi) |
| Claude Haiku 4.5 | yok | teknik | yok | README'deki hazır modellerden biri | 0:16 | Claude Haiku 4.5 model listesinde (karede: README tablosunda model listesi) |
| Gemini 2.5 Pro | yok | teknik | yok | README'deki hazır modellerden biri | 0:16 | Gemini 2.5 Pro model listesinde (karede: README tablosunda model listesi) |
| Gemini 2.5 Flash | yok | teknik | yok | README'deki hazır modellerden biri | 0:16 | Gemini 2.5 Flash model listesinde (karede: README tablosunda model listesi) |
| ruvLLM | yok | teknik | yok | Kendi kendini geliştiren yerel model katmanı; MicroLoRA adaptörleri | 0:16 | Native support for ruvLLM (karede: README satırı ruvLLM yerel model katmanı) |
| AgentDB | yok | teknik | yok | HNSW indeksli ajan veritabanı / paylaşılan bellek | 0:02 | HNSW-indexed AgentDB with 150x-12,500x faster search (karede: README tablosunda Vector Memory satırı) |
| SONA | yok | teknik | yok | Sinirsel öğrenme desenleri; yerel öğrenme | 0:02 | SONA neural patterns, ReasoningBank (karede: README tablosunda Self-Learning satırı) |
| Docker | yok | teknik | yok | Web arayüzünün Docker olarak paketlenmesi | 0:16 | Web UI is shipped as Docker (karede: README satırında Dockerfile) |
| Ollama | yok | CLI | yok | Yerel model sağlayıcısı; Tier-2 sağlayıcı sürümü | 0:30 | Ruflo 3.6.27 — Ollama provider (Tier-2) (karede: Sürüm listesinde Ollama provider satırı) |
| Akıllı model yönlendirme | yok | teknik | yok | Basit görevleri ücretsiz katmana, zorları uygun modele yönlendirme | 0:20 | Basic tasks route to a free tier automatically. · kanıt: yok |
| MicroLoRA | yok | teknik | yok | Yerel model katmanında yönlendirilen küçük LoRA adaptörleri; yörüngelerden öğreniyor. | 0:16 | Routes to MicroLoRA adapters, learns from your trajectories (karede: kanıttan) Routes to MicroLoRA adapters, learns from your trajectories |
| GOAP A* planner | yok | teknik | yok | Düz dilde verilen hedefleri yürütülebilir adımlara çeviren planlayıcı; goal.ruv.io üzerinden sunuluyor. | 0:09 | GOAP A* planner at goal.ruv.io — plain-English goals (karede: kanıttan) GOAP A* planner at goal.ruv.io — plain-English goals |
| MongoDB | yok | teknik | yok | Veritabanı; Ruflo web arayüzü gömülü Mongo ile birlikte geliyor. | 0:16 | Web UI is shipped as Docker with embedded Mongo (karede: kanıttan) Web UI is shipped as Docker with embedded Mongo |
| Kubernetes | yok | teknik | yok | Konteyner orkestrasyon platformu; Ruflo'nun kendi bulutunuza dağıtım seçeneklerinden biri. | 0:16 | Deploy to your own Cloud Run / Fly / Kubernetes / docker-compose (karede: kanıttan) Deploy to your own Cloud Run / Fly / Kubernetes / docker-compose |
| Tercihi Ruflo belleğine kaydetmek | yok | prompt | yok | Ruflo'nun ruflo_memory_store aracına 'preferences' ad alanında, 'editor_theme' anahtarıyla tercihi kaydetmesini isteyen talimat. | 0:09 | kaynak: kare |
| Uzun süreli bellek özelliğini göstermek | yok | prompt | yok | 'remember my favorite color is indigo' diyerek bilgiyi kaydettirip haftalar sonra sormak; Ruflo'nun hatırlaması bekleniyor. | 0:16 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Gösterge paneli kartı (dashboard card) | Maliyet gösterge paneli kartı; aylık API maliyeti ve tasarruf değerlerini gösteriyor. (karede: 'API COST DASHBOARD' kartında Monthly/Optimized maliyet ve -75% rozeti) | 0:20 | kare |
| Akış diyagramı (flow diagram) | İstek yönlendirme akışı; istekler yönlendiriciden model katmanına dağılıyor. (karede: 'ROUTING FLOW' bölümünde Request → Router → Optimized/Free Tier düğümleri) | 0:20 | kare |
| Tablo yerleşimi (table layout) | README özelliklerini iki sütunlu tabloda gösteriyor. (karede: 'What It Gets' tablosu; sol sütunda özellik adları, sağda açıklamalar) | 0:02 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude mcp add ruflo -- npx ruflo@latest mcp start | Ruflo'yu Claude Code'a MCP sunucusu olarak ekler (karede: README üstünde komut satırı görünüyor) | 0:02 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 60 ajan aynı anda çalışıyor ve her çalıştırmada gelişiyor | 0:00 | sayısal |
| Bulut API maliyetini %75 düşürüyor | 0:20 | sayısal |
| GitHub'da ajan çerçeveleri arasında bir numara, 14.000+ yıldız | 0:00 | sayısal |
| Basit görevler ücretsiz katmana otomatik yönlenir | 0:20 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Ruflo | Ruflo | It's called Ruflo |
| kare 0:02 | Claude Code | Claude Code | Add Ruflo as an MCP server in Claude Code |
| kare 0:02 | MCP | MCP | claude mcp add ruflo |
| kare 0:02 | npm | npm | npx ruflo@latest mcp start |
| kare 0:02 | AgentDB | AgentDB | HNSW-indexed AgentDB |
| kare 0:02 | SONA | SONA | SONA neural patterns |
| kare 0:09 | flo.ruv.io | flo.ruv.io | Multi-model chat at flo.ruv.io |
| kare 0:09 | goal.ruv.io | goal.ruv.io | GOAP A* planner at goal.ruv.io |
| kare 0:16 | OpenRouter | OpenRouter | via OpenRouter |
| kare 0:16 | Qwen 3.6 Max | Qwen 3.6 Max | Qwen 3.6 Max (default) |
| kare 0:16 | Claude Sonnet 4.6 | Claude Sonnet 4.6 | model listesinde |
| kare 0:16 | Claude Haiku 4.5 | Claude Haiku 4.5 | model listesinde |
| kare 0:16 | Gemini 2.5 Pro | Gemini 2.5 Pro | model listesinde |
| kare 0:16 | Gemini 2.5 Flash | Gemini 2.5 Flash | model listesinde |
| kare 0:16 | ruvLLM | ruvLLM | Native support for ruvLLM |
| kare 0:16 | Docker | Docker | Web UI is shipped as Docker |
| kare 0:16 | MongoDB | aday değil: başka adayın parçası (Docker) | Docker içinde gömülü Mongo; ayrı kullanılmadı |
| kare 0:16 | Kubernetes / Cloud Run / Fly | aday değil: genel kavram | Dağıtım seçeneği olarak listelenmiş |
| kare 0:16 | vLLM, LM Studio, Together, Groq | aday değil: genel kavram | Uyumlu uç nokta örnekleri listesinde |
| kare 0:20 | API Cost Dashboard | Akıllı model yönlendirme | Intelligent model routing - live |
| kare 0:30 | Ollama provider | Ollama | Ruflo 3.6.27 — Ollama provider (Tier-2) |
| kare 0:30 | GitHub Pulse | aday değil: başka adayın parçası (Ruflo) | Pulse - ruvnet/ruflo |
| kare 0:33 | Cognitum.One | aday değil: konu dışı | Depo sayfasında görünen bağlantı |
| açıklama | #ZeroToFounder ReelsCreator | aday değil: konu dışı | Açıklamada etiket olarak geçiyor |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:02: README: 'claude mcp add ruflo -- npx ruflo@latest mcp start', What You Get tablosu (100+ Agents, Swarm, Vector Memory, 32 plugin); altyazı '60 AGENTS'
- 0:16: README tablosu: 6 model, ruvLLM, 5 sunucu grubu, kendi MCP'ni getir, Docker; altyazı 'ALL IMPROVING'
- 0:20: API Cost Dashboard: aylık 250, optimize 250 görünüyor, -75%, $750 saved; altyazı 'IT SLASHES'
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Açıklamada bağlantı yok; 'ücretsiz katman' hangi modeli kasteder belli değil.
- Panodaki 250/250 değerleri OCR'da tutarsız; %75 iddiası doğrulanmadı.
- Konuşmadaki 'cloud' büyük olasılıkla 'Claude' demek.
- Instagram reel'inin kendisi, #ZeroToFounder ve ReelsCreator etiketleri araç olarak kullanılmadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com | 0:09 | ekran | hayır |
| flo.ruv.io | 0:09 | ekran | evet |
| goal.ruv.io | 0:09 | ekran | evet |
| https://www.instagram.com/reel/DY_SoPGKv2A/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Ruflo'yu tanıtma: 60 paralel ajan iddiası — araçlar: Ruflo
- 2. adım — README'de yetenek tablosunu gösterme — araçlar: Ruflo, GitHub
- 3. adım — Claude Code'a MCP sunucusu ekleme komutunu gösterme — araçlar: Claude Code, MCP, npm
- 4. adım — flo.ruv.io çoklu model sohbetini gösterme — araçlar: flo.ruv.io, OpenRouter
- 5. adım — Ajan rolleri ve paylaşılan bellek şemasını gösterme — araçlar: AgentDB
- 6. adım — Maliyet yönlendirme panosunu gösterme — araçlar: Akıllı model yönlendirme
- 7. adım — GitHub Pulse ve sürümleri gösterme — araçlar: GitHub, Ollama
- 8. adım — FLOW yorumu için çağrı — araçlar: yok
## Promptlar
- Tercihi Ruflo belleğine kaydetmek — Ruflo'nun ruflo_memory_store aracına 'preferences' ad alanında, 'editor_theme' anahtarıyla tercihi kaydetmesini isteyen talimat.
- Uzun süreli bellek özelliğini göstermek — 'remember my favorite color is indigo' diyerek bilgiyi kaydettirip haftalar sonra sormak; Ruflo'nun hatırlaması bekleniyor.
ikinci göz KAPALI: --ikinci-goz yok
