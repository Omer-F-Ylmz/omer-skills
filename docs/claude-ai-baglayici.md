# claude.ai bağlayıcı listesi · 2026-09-17
Yol: Pro/Max → Customize → Connectors (claude.ai/customize/connectors) → "+" → Add custom connector · Team/Enterprise → Organization settings → Connectors → Add → Custom → Web.
UI'da URL + Advanced settings altında OAuth Client ID/Secret var. Request headers (`Authorization`, `x-api-key`) beta, kademeli açılıyor (anthropics/claude-ai-mcp #715 açık); bu hesapta 17 Eyl'de açık.
Kaynak: support.claude.com/en/articles/11175166 · context7.com/docs/resources/all-clients · learn.microsoft.com/en-us/training/support/mcp · github.com/21st-dev/magic-mcp

- 21st · https://21st.dev/api/mcp · `x-api-key` header (OAuth yok) · eklendi 17 Eyl (Request headers · `x-api-key` · No sign-in)
- context7 · https://mcp.context7.com/mcp · anahtarsız (anonim hız limiti); istenirse OAuth · eklenebilir (CC'deki yerel node kurulumu taşınmaz, uzak URL kullanılır)
- mslearn · https://learn.microsoft.com/api/mcp · yok (herkese açık) · eklenebilir
