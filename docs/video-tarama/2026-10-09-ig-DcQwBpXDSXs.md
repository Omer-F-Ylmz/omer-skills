# ⚙️n8n turns building an AI agent into dragging boxes on a canvas.
## Künye
⚙️n8n turns building an AI agent into dragging boxes on a canvas. · fullstackparody · süre: 0:00 · ? · https://www.instagram.com/p/DcQwBpXDSXs/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-25 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 68081 tk · claude-haiku-5-5: claude-haiku-5-5 · 114678 tk
## Özet
9 görsellik Instagram kaydırmalı gönderi: n8n ile AI ajanı kurma rehberi. n8n'in ne olduğu, ajanın tek düğüm olması, sohbet modeli, bellek, araç düğümleri, Qdrant ile RAG ve self-hosted AI starter kit'in Docker ile kurulumu anlatılıyor. Altyazı ve süre yok, kanıtlar karelerden ve açıklamadan.
## Bölümler
- 0:00 Kapak: n8n AI Agents kurulum rehberi (görsel 1)
- 0:00 n8n nedir? (görsel 2)
- 0:00 Mimari: ajan tek düğüm (görsel 3)
- 0:00 Beyin: sohbet modeli (görsel 4)
- 0:00 Bellek: Window Buffer (görsel 5)
- 0:00 Araçlar ve MCP (görsel 6)
- 0:00 RAG: Qdrant (görsel 7)
- 0:00 Kurulum: starter kit (görsel 8)
- 0:00 Kapanış (görsel 9)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n | yok | iş akışı | yok | Kanvasta düğüm sürükleyerek iş akışı ve AI ajanı kurulan fair-code otomasyon platformu. | 0:00 | A fair-code automation platform. (karede: Görsel 2: 'What is n8n?' başlığı, fair-code platform metni, 198K+ GitHub stars, 1500+ integrations) |
| AI Agent | yok | teknik | yok | Sohbet modeli, bellek ve araçların bağlandığı n8n ajan düğümü. | 0:00 | the AI Agent node takes over (karede: Görsel 3: Chat Trigger'a bağlı AI Agent düğümü; altında Chat Model, Memory, Tool çıkışları) |
| Chat Trigger | yok | teknik | yok | Ajanı başlatan sohbet tetikleyici düğümü. | 0:00 | Chat Trigger (karede: Görsel 3: AI Agent'a bağlı yeşil sohbet ikonlu 'Chat Trigger' düğümü) |
| Anthropic Claude | yok | teknik | yok | Chat Model düğümünde seçilebilen model sağlayıcılarından biri. | 0:00 | Plug in Claude, GPT, Gemini, or a local model (karede: Görsel 4: Model açılır listesinde 'Anthropic Claude' satırı) |
| OpenAI | yok | teknik | yok | Chat Model olarak (OpenAI Chat Model) ve embeddings için kullanılan sağlayıcı. | 0:00 | OpenAI Chat Model (karede: Görsel 3: 'OpenAI Chat Model' düğümü; görsel 4 listede 'OpenAI'; görsel 7 'Embeddings' düğümünde OpenAI logosu) |
| Google Gemini | yok | teknik | yok | Chat Model için seçilebilen model sağlayıcısı. | 0:00 | Google Gemini (karede: Görsel 4: Model listesinde 'Google Gemini' satırı) |
| Ollama | yok | CLI | yok | Yerel modelleri çalıştırmak için kullanılan araç; starter kit'e dahil. | 0:00 | Ollama (local) (karede: Görsel 4: kırmızı daireyle işaretli 'Ollama (local)' satırı; görsel 8 metninde Ollama) |
| Window Buffer Memory | yok | teknik | yok | Son N mesajı oturum anahtarıyla tutan bellek düğümü. | 0:00 | A Window Buffer holds the last N messages (karede: Görsel 5: 'Window Buffer Memory' paneli, Session Key {{ $json.sessionId }}, Context Window Length 10) |
| Postgres Memory | yok | teknik | yok | Mimari şemasında bellek olarak bağlanan Postgres düğümü; starter kit'e dahil. | 0:00 | Postgres Memory · kanıt: kare (karede: Görsel 3: 'Postgres Memory' düğümü Memory çıkışına bağlı; görsel 8 'Postgres') |
| Notion Tool | yok | teknik | yok | Şemada araç olarak bağlanan Notion düğümü. | 0:00 | Notion Tool · kanıt: kare (karede: Görsel 3: Tool çıkışına bağlı turuncu anahtar ikonlu 'Notion Tool' düğümü) |
| Calculator | yok | teknik | yok | Ajana bağlanan hesap makinesi araç düğümü. | 0:00 | Calculator, HTTP request, Gmail, Slack (karede: Görsel 6: ai_tool çıkışına bağlı 'Calculator' düğümü) |
| HTTP Request | yok | teknik | yok | Ajanın API çağırmasını sağlayan araç düğümü. | 0:00 | Calculator, HTTP request, Gmail, Slack (karede: Görsel 6: küre ikonlu 'HTTP Request' düğümü) |
| Gmail | yok | teknik | yok | Ajanın e-posta göndermesini sağlayan araç düğümü. | 0:00 | Calculator, HTTP request, Gmail, Slack (karede: Görsel 6: 'Gmail' düğümü) |
| Slack | yok | teknik | yok | Ajan aracı olarak bağlanan Slack düğümü. | 0:00 | Calculator, HTTP request, Gmail, Slack (karede: Görsel 6: 'Slack' düğümü) |
| MCP | yok | MCP | yok | n8n yerel MCP düğümleriyle herhangi bir araç sunucusunu ajana bağlama. | 0:00 | Native MCP nodes plug in any tool server. (karede: Görsel 6: küp ikonlu 'MCP' düğümü, ai_tool çıkışına bağlı) |
| Qdrant | yok | teknik | yok | RAG için araç olarak eklenen vektör deposu. | 0:00 | Add a vector store like Qdrant as a tool. (karede: Görsel 7: kırmızı daireyle işaretli 'Qdrant Vector Store' düğümü, Embeddings ve Documents bağlı) |
| Embeddings | yok | teknik | yok | Belgeleri vektöre çeviren düğüm (OpenAI logolu). | 0:00 | Embeddings (karede: Görsel 7: OpenAI logolu 'Embeddings' düğümü, Qdrant'a ve Documents'a bağlı) |
| RAG | yok | teknik | yok | Ajanın önce dosyalarda arayıp onlardan yanıtlaması (retrieval-augmented generation). | 0:00 | retrieval-augmented generation, wired in one node. (karede: Görsel 7: 'RAG' etiketi ve 'Feed it your own docs' başlığı) |
| Self-hosted AI starter kit | yok | iş akışı | https://github.com/n8n-io/self-hosted-ai-starter-kit | n8n, Ollama, Qdrant ve Postgres'i tek komutla ayağa kaldıran paket. | 0:00 | bundles n8n, Ollama, Qdrant, and Postgres in one command. (karede: Görsel 8: terminalde git clone https://github.com/n8n-io/self-hosted-ai-starter-kit.git) |
| Docker Compose | yok | CLI | yok | Starter kit'i cpu profiliyle başlatan komut. | 0:00 | docker compose --profile cpu up · kanıt: kare (karede: Görsel 8: terminalde '$ docker compose --profile cpu up') |
| git | yok | CLI | yok | Starter kit deposunu klonlamak için kullanılan komut. | 0:00 | git clone https://github.com/n8n-io/ (karede: Görsel 8: terminalde git clone ve cd satırları) |
| Chat Model | yok | teknik | yok | Ajanın akıl yürütme motoru olarak bağlanan dil modeli düğümü; model seçimi burada yapılır. | 0:00 | The Chat Model node is the reasoning engine. (karede: Slayt 04: 'Chat Model' paneli, 'Model' açılır listesi; Anthropic Claude, OpenAI, Google Gemini, Ollama (local) seçenekleri.) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/n8n-io/self-hosted-ai-starter-kit.git | Starter kit deposunu klonlar. (karede: Görsel 8: terminalde '$ git clone https://github.com/n8n-io/ self-hosted-ai-starter-kit.git') | 0:00 | kare |
| cd self-hosted-ai-starter-kit | Klonlanan klasöre girer. (karede: Görsel 8: '$ cd self-hosted-ai-starter-kit') | 0:00 | kare |
| docker compose --profile cpu up | n8n, Ollama, Qdrant ve Postgres'i CPU profiliyle başlatır. (karede: Görsel 8: '$ docker compose --profile cpu up' ve yeşil 'n8n ready at http://localhost:5678') | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| n8n'in 198K+ GitHub yıldızı ve 1500+ entegrasyonu var. | 0:00 | sayısal |
| Ajan tek düğümdür; ona bir beyin, bir bellek ve araçlar bağlanır. | 0:00 | özellik |
| Model istenildiğinde değiştirilebilir, grafın geri kalanı değişmez. | 0:00 | özellik |
| Bellek olmadan her mesaj sıfırdan başlar. | 0:00 | özellik |
| Starter kit n8n, Ollama, Qdrant ve Postgres'i tek komutta paketler; modeller ve veri makineden çıkmaz. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 (0:00) | n8n | n8n | n8n AI Agents – The Complete Setup Guide |
| kare 1 (0:00) | @fullstackparody | aday değil: konu dışı | @fullstackparody |
| kare 2 (0:00) | GitHub | aday değil: genel kavram | 198K+ GitHub stars |
| kare 2 (0:00) | fair-code | aday değil: genel kavram | A fair-code automation platform. |
| kare 3 (0:00) | AI Agent düğümü | AI Agent | the AI Agent node takes over |
| kare 3 (0:00) | Chat Trigger | Chat Trigger | Chat Trigger düğümü |
| kare 3 (0:00) | OpenAI Chat Model | OpenAI | OpenAI Chat Model |
| kare 3 (0:00) | Postgres Memory | Postgres Memory | Postgres Memory |
| kare 3 (0:00) | Notion Tool | Notion Tool | Notion Tool |
| kare 4 (0:00) | Anthropic Claude | Anthropic Claude | Anthropic Claude |
| kare 4 (0:00) | Google Gemini | Google Gemini | Google Gemini |
| kare 4 (0:00) | Ollama (local) | Ollama | Ollama (local) |
| kare 4 (0:00) | GPT | OpenAI | Claude, GPT, Gemini |
| kare 5 (0:00) | Window Buffer Memory | Window Buffer Memory | Window Buffer Memory |
| kare 6 (0:00) | Calculator | Calculator | Calculator düğümü |
| kare 6 (0:00) | HTTP Request | HTTP Request | HTTP Request düğümü |
| kare 6 (0:00) | Gmail | Gmail | Gmail düğümü |
| kare 6 (0:00) | Slack | Slack | Slack düğümü |
| kare 6 (0:00) | MCP | MCP | Native MCP nodes |
| kare 6 (0:00) | sub-workflow | aday değil: genel kavram | or a whole sub-workflow |
| kare 7 (0:00) | Qdrant Vector Store | Qdrant | vector store like Qdrant |
| kare 7 (0:00) | Embeddings | Embeddings | Embeddings düğümü |
| kare 7 (0:00) | RAG | RAG | retrieval-augmented generation |
| kare 8 (0:00) | self-hosted AI starter kit | Self-hosted AI starter kit | The self-hosted AI starter kit bundles n8n |
| kare 8 (0:00) | git clone | git | $ git clone https://github.com/n8n-io/ |
| kare 8 (0:00) | docker compose | Docker Compose | docker compose --profile cpu up |
| kare 8 (0:00) | Postgres | Postgres Memory | Ollama, Qdrant, and Postgres |
| kare 8 (0:00) | localhost:5678 | aday değil: konu dışı | n8n ready at http://localhost:5678 |
| açıklama | Nikhil / @fullstackparody | aday değil: konu dışı | Nikhil / @fullstackparody |
| yorum | Yorumlar | aday değil: konu dışı | yorum: girişsiz alınamıyor |
## Kareden okunanlar
- Görsel 1: n8n AI Agents – The Complete Setup Guide; AI Agent düğümü iki araç düğümüne bağlı
- Görsel 2: What is n8n? fair-code platform; 198K+ GitHub stars, 1500+ integrations; Visual Canvas, Self-Host Free
- Görsel 3: Chat Trigger → AI Agent; Chat Model/Memory/Tool: OpenAI Chat Model, Postgres Memory, Notion Tool
- Görsel 4: Chat Model paneli: Anthropic Claude, OpenAI, Google Gemini, Ollama (local); bağlantı ai_languageModel
- Görsel 5: Window Buffer Memory: Session Key {{ $json.sessionId }}, Context Window Length 10; ai_memory
- Görsel 6: AI Agent'a ai_tool ile Calculator, HTTP Request, Gmail, Slack, MCP
- Görsel 7: AI Agent, Qdrant Vector Store (daire içinde), Embeddings, Documents
- Görsel 8: git clone, cd, docker compose --profile cpu up; 'n8n ready at http://localhost:5678'
- Görsel 9: Kapanış: Save this for your next build; Nikhil / @fullstackparody
## Belirsizlikler
- Süre 0:00 ve altyazı yok; tüm zamanlar 0:00 olarak yazıldı, görsel numarası başlıklarda belirtildi.
- Yorumlar girişsiz alınamadı.
- Sözlük eşleşmeleri Three.js, Canva ve Llama gönderide kullanılmıyor; aday yapılmadı.
- Notion Tool yalnızca mimari şemasında örnek olarak görünüyor; kullanımı gösterilmedi.
- Sunucunun çalıştığı ana yapay zekâ modeli belirtilmiyor (Chat Model seçimi kullanıcıya bırakılmış).
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/n8n-io/self-hosted-ai-starter-kit.git | 0:00 | ekran | evet |
| http://localhost:5678 | 0:00 | ekran | hayır |
| https://github.com/n8n-io/self-hosted-ai-starter-kit | 0:00 | ekran | evet |
## İş akışı
- 1. adım — Docker Compose gerektiren starter kit deposunu git ile klonla — araçlar: git, Self-hosted AI starter kit
- 2. adım — Klonlanan klasöre geç — araçlar: git
- 3. adım — cpu profiliyle yığını başlat (n8n, Ollama, Qdrant, Postgres) — araçlar: Docker Compose, n8n, Ollama, Qdrant, Postgres Memory
- 4. adım — n8n arayüzünü localhost:5678 adresinde aç — araçlar: n8n
- 5. adım — Chat Trigger düğümüyle tetikleyici ekle ve AI Agent düğümüne bağla — araçlar: Chat Trigger, AI Agent
- 6. adım — Chat Model düğümünde model seç (Claude, OpenAI, Gemini veya Ollama) — araçlar: Anthropic Claude, OpenAI, Google Gemini, Ollama
- 7. adım — Window Buffer Memory ekle, oturum anahtarını ve pencere uzunluğunu (10) ayarla — araçlar: Window Buffer Memory
- 8. adım — Araç düğümlerini bağla (Calculator, HTTP Request, Gmail, Slack, MCP) — araçlar: Calculator, HTTP Request, Gmail, Slack, MCP
- 9. adım — RAG için Qdrant vektör deposunu ve Embeddings düğümünü ekle, belgeleri yükle — araçlar: Qdrant, Embeddings, RAG
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
