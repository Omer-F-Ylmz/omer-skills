# otomasyon (DcQwBpXDSXs)

**Amaç:** AI Agent'i kurmak ve kullanmak için drag-and-drop ile iş akışları oluşturma.
**Araçlar:** n8n platformu, Ollama (yerel AI modelleri), Qdrant (vektör depolama), Postgres (veritabanı), Chat Model (Claude, GPT, Gemini), Tool Nodes (e-posta, HTTP, Slack, alt iş akışları)

**Adımlar**
1. [] n8n platformunu yükleyin ve AI Agent node'u ekleyin.
2. [] Chat Model node'u ekleyerek AI Agent'e bir zihin (Claude, GPT, Gemini veya yerel model) bağlayın.
3. [] Memory node'u ekleyerek konuşmayı hatırlaması için Window Buffer ayarlayın.
4. [] Tool node'ları ekleyerek e-posta, HTTP istekleri, Slack veya alt iş akışları gibi işlemleri yapabilmesini sağlayın.
5. [] Self-hosted AI Starter Kit'i docker komutu ile kurarak n8n, Ollama, Qdrant ve Postgres'i bir arada çalıştırın.
6. [] Agentin dosyaları aradıktan sonra cevap verebilmesi için Qdrant Vector Store'u ekleyin.

**Prompt/kod/ayar:** docker compose --profile cpu up
**Sonuç:** AI Agent'i drag-and-drop ile kurulumu ve kullanımı sağlayan bir otomasyon platformu.
**Bizde (öneri, modelden):** kurulu araçlarla nasıl n8n AI Agent'i yerel olarak kurup, Chat Model, Memory ve Tool node'ları kullanarak iş akışları oluşturulur?
**Daha iyi (öneri):** Kullanıcı dostu bir arayüz ve daha fazla entegrasyon desteği ile daha kolay kullanım sağlanabilir.
