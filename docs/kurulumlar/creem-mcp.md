---
type: kurulum
status: bekliyor-anahtar
tags: [mcp, creem, odeme, link27]
relatedTo: [docs/link27-kalan-kurulum.md]
---

# Creem MCP (Selenium39/mcp-server-creem, MIT)

Durum: klonlandı, `npm install` + `npm run build` geçti. `CREEM_API_KEY` yok → bağlanmadı.

Yer: `C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27\Selenium39__mcp-server-creem\build\index.js`

## Anahtar gelince

1. Ortama `CREEM_API_KEY` koy (değeri dosyaya yazma). İlk deneme `CREEM_TEST_MODE=true`.
2. mcptoon gateway'ine ekle (ya da `claude mcp add`):

```json
"creem": {
  "command": "node",
  "args": ["C:/Users/pc/Desktop/Claude ile yapılanlar/araclar/link27/Selenium39__mcp-server-creem/build/index.js"],
  "env": { "CREEM_API_KEY": "${CREEM_API_KEY}", "CREEM_TEST_MODE": "true" }
}
```

3. Smoke: ürün listeleme aracı test modunda tek çağrı.
