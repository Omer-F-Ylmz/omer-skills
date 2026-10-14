# pinecone — 10 benzersiz kayıt

**Amaç:** Pinecone vektör veritabanı: hızlı başlangıç, CLI/MCP ile indeks ve vektör yönetimi, tam metin arama, Assistant ile alıntılı belge Q&A, n8n RAG akışları.

**İç yapı:** Tümü [skill], pinecone-<konu>; pinecone-help genel bakış, pinecone-paket 9 skill'lik derleme, erişim yolu başına skill (cli, mcp, docs, n8n).

## En güçlü parçalar
- `pinecone-quickstart` — Pinecone'a ilk kez başlarken rehberli tur.
- `pinecone-assistant` — Alıntılı belge Q&A için Assistant oluşturma, yönetme, sohbet.
- `pinecone-cli` — Toplu işlem, vektör yönetimi, yedek, namespace, CI/CD otomasyonu.
- `pinecone-full-text-search` — Yoğun/seyrek alanlı metin arama indeksi kurma ve belge alma.
- `pinecone-docs` — Pinecone kodu yazarken API parametresi ve vektör/kayıt formatı.
- `pinecone-n8n` — n8n'de Pinecone düğümleriyle RAG ve chat-with-docs akışları.

## Birlikte kullanım
- pinecone-help → pinecone-quickstart → pinecone-docs.
- pinecone-mcp + pinecone-query: MCP araçları ve metinle sorgu.
- pinecone-n8n + n8n ailesi.

## Tuzaklar
- pinecone-query yalnız integrated index'lerle çalışır (katalog açıkça uyarır).
- pinecone-paket diğer skill'lerin derlemesi; çift yükleme riski.
- Pinecone hesabı/API anahtarı gereksinimi katalog metninde açık yazılmamış.

## Üyeler
- skill (10): pinecone-assistant, pinecone-cli, pinecone-docs, pinecone-full-text-search, pinecone-help, pinecone-mcp, pinecone-n8n, pinecone-paket, pinecone-query, pinecone-quickstart
