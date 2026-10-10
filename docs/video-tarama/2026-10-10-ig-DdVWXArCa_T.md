# Want to learn AI automation?
## Künye
Want to learn AI automation? · rengatechnologies · süre: 0:00 · ? · https://www.instagram.com/p/DdVWXArCa_T/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 42525 tk · claude-haiku-5-5: claude-haiku-5-5 · 61943 tk
## Özet
Rengatechnologies'in Instagram karusel gönderisi: n8n ile AI ajanı kurulumunu 8 görselde anlatıyor. n8n tanıtımı, ajan mimarisi (Chat Trigger, AI Agent, model, bellek, araçlar), model seçimi (Claude, OpenAI, Gemini, Ollama), Window Buffer Memory, araç düğümleri ve yerel MCP, Qdrant ile RAG ve self-hosted AI starter kit'in docker compose ile kurulumu işleniyor. Video/ses yok, yalnız görsel gönderi.
## Bölümler
- 0:00 Kapak: n8n AI Agents tam kurulum rehberi
- 0:00 02 Genel bakış: n8n nedir
- 0:00 03 Mimari: ajan tek düğümdür
- 0:00 04 Beyin: sohbet modeli seçimi
- 0:00 05 Bellek: Window Buffer Memory
- 0:00 06 Araçlar: Tool düğümleri ve MCP
- 0:00 07 RAG: Qdrant ile kendi dokümanların
- 0:00 08 Kurulum: starter kit ile ücretsiz yığın
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n | yok | iş akışı | https://github.com/n8n-io/self-hosted-ai-starter-kit | Düğüm sürükleyerek iş akışı ve AI ajanı kurulan fair-code otomasyon platformu | 0:00 | What is n8n? A fair-code automation platform. (karede: kanıttan) What is n8n? A fair-code automation platform. |
| AI Agent node | yok | iş akışı | yok | Tetikleyiciden sonra devralan; model, bellek ve araç bağlanan ajan düğümü | 0:00 | the AI Agent node takes over (karede: kanıttan) the AI Agent node takes over |
| Chat Trigger | yok | iş akışı | yok | Ajanı başlatan sohbet tetikleyici düğümü | 0:00 | Chat Trigger düğümü AI Agent'a bağlı (karede: kanıttan) Chat Trigger düğümü AI Agent'a bağlı |
| Chat Model | yok | iş akışı | yok | Akıl yürütme motoru olan sohbet modeli düğümü | 0:00 | The Chat Model node is the reasoning engine. (karede: kanıttan) The Chat Model node is the reasoning engine. |
| Anthropic Claude | yok | iş akışı | yok | Chat Model olarak seçilebilen model | 0:00 | Model listesinde Anthropic Claude (karede: kanıttan) Model listesinde Anthropic Claude |
| OpenAI | yok | iş akışı | yok | Chat Model ve Embeddings olarak kullanılan servis | 0:00 | OpenAI Chat Model; Embeddings düğümü (karede: kanıttan) OpenAI Chat Model; Embeddings düğümü |
| Google Gemini | yok | iş akışı | yok | Chat Model seçeneği | 0:00 | Model listesinde Google Gemini (karede: kanıttan) Model listesinde Google Gemini |
| Ollama | yok | CLI | yok | Yerel model çalıştırma; starter kit'e dahil | 0:00 | Ollama (local); bundles n8n, Ollama, Qdrant (karede: kanıttan) Ollama (local); bundles n8n, Ollama, Qdrant |
| Window Buffer Memory | yok | iş akışı | yok | Son N mesajı oturum anahtarıyla tutan bellek düğümü | 0:00 | Window Buffer Memory, Context Window Length 10 (karede: kanıttan) Window Buffer Memory, Context Window Length 10 |
| Postgres | yok | iş akışı | yok | Postgres Memory olarak bellek, starter kit'te veritabanı | 0:00 | Postgres Memory düğümü; bundles ... Postgres (karede: kanıttan) Postgres Memory düğümü; bundles ... Postgres |
| Notion | yok | iş akışı | yok | Araç düğümü örneği (Notion Tool) | 0:00 | Notion Tool düğümü (karede: kanıttan) Notion Tool düğümü |
| Calculator | yok | iş akışı | yok | Ajan araç düğümü | 0:00 | Calculator ai_tool düğümü (karede: kanıttan) Calculator ai_tool düğümü |
| HTTP Request | yok | iş akışı | yok | Ajan araç düğümü | 0:00 | HTTP Request ai_tool düğümü (karede: kanıttan) HTTP Request ai_tool düğümü |
| Gmail | yok | iş akışı | yok | Ajan araç düğümü | 0:00 | Gmail ai_tool düğümü (karede: kanıttan) Gmail ai_tool düğümü |
| Slack | yok | iş akışı | yok | Ajan araç düğümü | 0:00 | Slack ai_tool düğümü (karede: kanıttan) Slack ai_tool düğümü |
| MCP (Native) | yok | MCP | yok | Herhangi bir araç sunucusunu bağlayan yerel MCP düğümleri | 0:00 | Native MCP nodes plug in any tool server. · kanıt: kare (karede: Native MCP nodes plug in any tool server.) |
| Qdrant | yok | iş akışı | yok | RAG için vektör deposu aracı | 0:00 | Add a vector store like Qdrant as a tool. (karede: kanıttan) Add a vector store like Qdrant as a tool. |
| RAG | yok | teknik | yok | Kendi dokümanlarından arayıp yanıtlayan retrieval-augmented generation | 0:00 | That is retrieval-augmented generation, wired in one node. (karede: kanıttan) That is retrieval-augmented generation, wired in one node. |
| self-hosted-ai-starter-kit | yok | iş akışı | https://github.com/n8n-io/self-hosted-ai-starter-kit | n8n, Ollama, Qdrant ve Postgres'i tek komutla çalıştıran paket | 0:00 | The self-hosted AI starter kit bundles n8n (karede: kanıttan) The self-hosted AI starter kit bundles n8n |
| Docker Compose | yok | CLI | yok | Yığını profile cpu ile ayağa kaldırır | 0:00 | docker compose --profile cpu up (karede: kanıttan) docker compose --profile cpu up |
| Git | yok | CLI | yok | Starter kit deposunu klonlar | 0:00 | git clone https://github.com/n8n-io/ (karede: kanıttan) git clone https://github.com/n8n-io/ |
| Embeddings | yok | teknik | yok | Belgeleri vektörlere dönüştüren n8n Embeddings düğümü; Qdrant'a bağlı. | 0:00 | Kare 7: "Embeddings" düğümü, "Documents" girdisi (karede: Kare 7'de 'Embeddings' düğümü, OpenAI benzeri logoyla; altta 'Documents' girişi.) |
| GitHub | yok | teknik | yok | Kodun barındırıldığı platform; starter kit deposu GitHub'dan klonlanıyor. | 0:00 | Kare 8: "git clone https://github.com/n8n-io/..." (karede: Kare 8 terminal komutunda github.com adresi.) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/n8n-io/self-hosted-ai-starter-kit.git | Self-hosted AI starter kit deposunu klonlar (karede: Terminal satır 1: $ git clone https://github.com/n8n-io/ self-hosted-ai-starter-kit.git) | 0:00 | kare |
| cd self-hosted-ai-starter-kit | Klonlanan klasöre girer (karede: Terminal satır 2: $ cd self-hosted-ai-starter-kit) | 0:00 | kare |
| docker compose --profile cpu up | n8n, Ollama, Qdrant ve Postgres'i CPU profiliyle başlatır (karede: Terminal satır 3: $ docker compose --profile cpu up) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| n8n 198K+ GitHub yıldızı ve 1500+ entegrasyona sahip | 0:00 | sayısal |
| n8n kendi sunucuda ücretsiz çalıştırılabilir veya bulutta kullanılabilir | 0:00 | özellik |
| Starter kit n8n, Ollama, Qdrant ve Postgres'i tek komutla paketler | 0:00 | özellik |
| Bellek olmadan her mesaj sıfırdan başlar | 0:00 | özellik |
| Model istenildiğinde değiştirilebilir, grafın geri kalanı değişmez | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 | n8n | n8n | n8n AI Agents |
| kare 1 | Rengatechnologies | aday değil: konu dışı | Hesap/marka adı |
| açıklama | #n8nworkflow #aiautomation #agenticai #aitools etiketleri | aday değil: genel kavram | Hashtagler |
| kare 2 | GitHub | aday değil: genel kavram | 198K+ GitHub stars |
| kare 3 | Chat Trigger | Chat Trigger | Chat Trigger düğümü |
| kare 3 | AI Agent | AI Agent node | AI Agent düğümü |
| kare 3 | OpenAI Chat Model | OpenAI | OpenAI Chat Model |
| kare 3 | Postgres Memory | Postgres | Postgres Memory |
| kare 3 | Notion Tool | Notion | Notion Tool |
| kare 4 | Chat Model | Chat Model | Chat Model paneli |
| kare 4 | Anthropic Claude | Anthropic Claude | Model listesi |
| kare 4 | Google Gemini | Google Gemini | Model listesi |
| kare 4 | Ollama (local) | Ollama | Model listesi |
| kare 4 | ai_languageModel | aday değil: başka adayın parçası (Chat Model) | Bağlantı türü |
| kare 5 | Window Buffer Memory | Window Buffer Memory | Bellek düğümü |
| kare 5 | Session Key $json.sessionId | aday değil: başka adayın parçası (Window Buffer Memory) | Parametre |
| kare 5 | ai_memory | aday değil: başka adayın parçası (Window Buffer Memory) | Bağlantı türü |
| kare 6 | Calculator | Calculator | Araç düğümü |
| kare 6 | HTTP Request | HTTP Request | Araç düğümü |
| kare 6 | Gmail | Gmail | Araç düğümü |
| kare 6 | Slack | Slack | Araç düğümü |
| kare 6 | MCP (Native) | MCP (Native) | Native MCP nodes |
| kare 6 | ai_tool | aday değil: başka adayın parçası (AI Agent node) | Bağlantı türü |
| kare 7 | Qdrant Vector Store | Qdrant | Vektör deposu düğümü |
| kare 7 | Embeddings | aday değil: başka adayın parçası (Qdrant) | Embeddings düğümü |
| kare 7 | retrieval-augmented generation | RAG | RAG anlatımı |
| kare 8 | self-hosted AI starter kit | self-hosted-ai-starter-kit | Kit anlatımı |
| kare 8 | git clone | Git | Terminal satır 1 |
| kare 8 | docker compose | Docker Compose | Terminal satır 3 |
| kare 8 | localhost:5678 | aday değil: başka adayın parçası (n8n) | n8n ready at http://localhost:5678 |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamıyor |
## Kareden okunanlar
- 1: TUTORIAL; n8n AI Agents; The Complete Setup Guide; Rengatechnologies; AI Agent, Web, Database düğümleri
- 2: What is n8n?; 198K+ GitHub stars; 1500+ integrations; Visual Canvas, Self-Host Free
- 3: Chat Trigger → AI Agent; Chat Model, Memory, Tool; OpenAI Chat Model, Postgres Memory, Notion Tool
- 4: Chat Model paneli: Anthropic Claude, OpenAI, Google Gemini, Ollama (local); ai_languageModel
- 5: Window Buffer Memory; Session Key {{ $json.sessionId }}; Context Window Length 10; ai_memory
- 6: AI Agent ai_tool: Calculator, HTTP Request, Gmail, Slack, MCP (Native)
- 7: AI Agent → Qdrant Vector Store → Embeddings → Documents
- 8: Terminal: git clone, cd, docker compose --profile cpu up; n8n ready at localhost:5678
## Belirsizlikler
- Video/ses yok, tüm zamanlar 0:00 (görsel gönderi); kare sırası zamanı göstermez.
- Yorumlar girişsiz alınamadı.
- Kare 8'de terminalde 4. satır numarası görünmüyor (3'ten 5'e atlıyor).
- Gmail ve Slack araç örnekleri; OpenAI Embeddings logosu OpenAI olarak yorumlandı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DdVWXArCa_T/ | 0:00 | açıklama | hayır |
| https://github.com/n8n-io/self-hosted-ai-starter-kit.git | 0:00 | ekran | evet |
| http://localhost:5678 | 0:00 | ekran | hayır |
## İş akışı
- 1. adım — n8n platformunu ve görsel tuvali tanıtma — araçlar: n8n
- 2. adım — Chat Trigger ile AI Agent düğümünü bağlama — araçlar: n8n, Chat Trigger, AI Agent node
- 3. adım — Chat Model düğümüne model seçme (Claude, OpenAI, Gemini veya Ollama) — araçlar: Chat Model, Anthropic Claude, OpenAI, Google Gemini, Ollama
- 4. adım — Window Buffer Memory ile oturum anahtarı ve bağlam uzunluğu (10) ayarlama — araçlar: Window Buffer Memory, Postgres
- 5. adım — Calculator, HTTP Request, Gmail, Slack ve yerel MCP araçlarını ajana bağlama — araçlar: Calculator, HTTP Request, Gmail, Slack, MCP (Native), Notion
- 6. adım — Qdrant vektör deposu ve Embeddings ile RAG kurma — araçlar: Qdrant, OpenAI, RAG
- 7. adım — Starter kit deposunu git ile klonlama — araçlar: Git, self-hosted-ai-starter-kit
- 8. adım — Klasöre girip docker compose ile yığını başlatma — araçlar: Docker Compose, n8n, Ollama, Qdrant, Postgres
- 9. adım — n8n'i localhost:5678 adresinde açma — araçlar: n8n
## Promptlar
- yok
