# Jev uzak MCP (claude.ai web/mobil + Desktop)

- URL: `https://jev-mcp-lemon.vercel.app/mcp` (Vercel projesi `jev-mcp`, kök `mcp/jev`, stateless Streamable HTTP)
- Yetki: `X-Jev-Token` başlığı (Authorization değil). Eksik/yanlış → 401; `/mcp` dışındaki her yol 404.
- Vercel env (production): `JEV_MCP_TOKEN`, `OPENROUTER_API_KEY`.
- Deployment Protection değiştirilmedi: production alias korumasız, MCP'yi engellemiyor (tokensiz 401 doğrudan bizim handler'dan).

## claude.ai'ye bağlama
1. Token'ı panoya al (PowerShell; değer ekrana basılmaz):
   `[Environment]::GetEnvironmentVariable('JEV_MCP_TOKEN','User') | Set-Clipboard`
2. claude.ai → Customize → Connectors → Add custom connector
   - URL: `https://jev-mcp-lemon.vercel.app/mcp`
   - Kimlik doğrulama: No sign-in
   - Header: `X-Jev-Token` = panodaki değer
3. Desktop hesap connector'ını kendisi alır; yerel `jev` girdisi eklenmez (yedek: `tools/mcp-launch/jev.cmd`).

## Sızıntıda
- **Token sızarsa:** yenisini üret + User ortamına yaz, `$env:JEV_MCP_TOKEN | vercel.cmd env add JEV_MCP_TOKEN production` (önce `vercel.cmd env rm JEV_MCP_TOKEN production`), `vercel.cmd deploy --prod`, claude.ai connector başlığını güncelle.
- **Anahtar sızarsa:** sağlayıcıda (OpenRouter/TypeSafe) iptal et; yenisini Read-Host satırıyla yaz (PowerShell 5.1, değer ekrana düşmez):
  `$s = Read-Host -AsSecureString 'anahtar'; [Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)), 'User')`
  sonra `vercel.cmd env rm OPENROUTER_API_KEY production` + `$env:OPENROUTER_API_KEY | vercel.cmd env add OPENROUTER_API_KEY production` + `vercel.cmd deploy --prod`.
