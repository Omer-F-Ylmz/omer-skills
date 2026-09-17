# Tarama Eylül · Bölüm 3 · 2026-09-17
Kaynak: claude.ai Bölüm 3 araştırması (17 Eyl). 41 aday · 12'si araştırma aşamasında elendi (Docker isteyen ZAP MCP'leri, çift kataloglar, olgunluğu düşük TR MCP'leri) · 3 UYGULA · 6 tetikleyici.
## UYGULA (KURULUM-4)
- dotnet-msbuild plugin (skill, ~100 token, build teşhisi) → kuruldu, 0.1.10.
- semgrep CLI · gitleaks + axe-core CLI → kapanış listesine (hook/MCP yok); komutlar `docs/kapanis-araclar.md`.
## Tetikleyici
| aday | tetikleyici |
|---|---|
| dotnet-blazor | Blazor projesi açılırsa |
| dotnet-test-migration | xUnit v3/MTP geçişi |
| hetzner-cloud skill (mcp.directory) | Hetzner deploy dalgası |
| Roblox Studio MCP (Roblox/studio-rust-mcp-server) | Roblox projesi başlayınca, Rojo ile |
| Sentry remote MCP | Sentry benimsenirse |
| claude.ai GitHub bağlayıcısı | ilk gerçek dalgada A/B (rapor yapıştırma yerine commit okuma) |
## ELE
- SQL MCP'leri (dab, mssql-mcp, postgres-mcp, dbhub, sqlite) → sqlcmd/psql/sqlite3 CLI var, önce CLI.
- GitHub MCP → gh CLI ile çift.
- Playwright MCP → Puppeteer döngüsü var; tek görev ~114k token.
- Chrome DevTools MCP → Puppeteer ile çift.
- Figma plugin · Cloudflare → kullanılmıyor.
- axecap / Duds MCP → axe CLI yeter.
- iyzico-mcp · efatura-mcp · iletimerkezi · Paraşüt → 0-2★, tek geliştirici, prod anahtarı ister.
- ZAP MCP (resmi) → yerel ZAP (Java) var.
- dotnet-diag / dotnet11 → gerek yok / preview.
- managedcode + Aaronontheweb katalogları → dotnet/skills ile çift.
- frontend-design zip → zaten var.
- Semgrep plugin (hook'lu) → CLI yeter; hook token ekler.
## omer-skills'te yazılacak (hazır olgun skill yok)
- tr-checkout (iyzico/PayTR) · tr-kvkk · tr-efatura · tr-kargo · questpdf
