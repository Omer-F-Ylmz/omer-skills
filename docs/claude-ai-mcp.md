# claude.ai / Claude Desktop MCP listesi · KURULUM-7b · 19 Eyl 2026

Kaynak: `claude mcp list` + `~/.claude.json` mcpServers + plugin `.mcp.json`. Anahtar değerleri burada yok; `<DEGISKEN_ADI>` yer tutucu.
Canlı Desktop config (MSIX): `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json` (yedek `.bak7b`; `%APPDATA%\Claude` yok). Yalnız anahtarsız yereller birleştirildi.

## Uzak (http) — claude.ai Settings → Connectors → Add custom connector

- mslearn · `https://learn.microsoft.com/api/mcp` · auth yok
- claude-design · `https://api.anthropic.com/v1/design/mcp` · OAuth (Anthropic hesabı)
- 21st · `https://21st.dev/api/mcp` · header `x-api-key: <TWENTYFIRST_API_KEY>`
- github · `https://api.githubcopilot.com/mcp/` · header `Authorization: Bearer <GITHUB_PERSONAL_ACCESS_TOKEN>`

## Yerel (stdio) — claude_desktop_config.json `mcpServers` parçası (canlı config'te)

- headroom · `"headroom": {"command": "uvx", "args": ["--from", "headroom-ai[mcp]==0.37.0", "headroom", "mcp", "serve"], "env": {"HOME": "C:/Users/pc"}}`
- puppeteer · `"puppeteer": {"command": "cmd", "args": ["/c", "npx", "-y", "puppeteer-mcp-server@0.7.2"]}`
- mcp-sequential-thinking · `"mcp-sequential-thinking": {"command": "cmd", "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-sequential-thinking@0.6.2"]}`
- mcp-memory · `"mcp-memory": {"command": "cmd", "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-memory@2026.8.31"]}`
- mcp-filesystem · `"mcp-filesystem": {"command": "cmd", "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem@2026.8.31", "C:/Users/pc/Desktop", "C:/Projeler"]}`
- mcp-fetch · `"mcp-fetch": {"command": "uvx", "args": ["mcp-server-fetch@2026.8.18"]}`
- mcp-git · `"mcp-git": {"command": "uvx", "args": ["mcp-server-git@2026.8.18"]}`
- mcp-time · `"mcp-time": {"command": "uvx", "args": ["mcp-server-time@2026.8.18"]}`
- binlog (dotnet-msbuild plugin) · `"binlog": {"command": "dotnet", "args": ["dnx", "Microsoft.AITools.BinlogMcp", "--yes", "--prerelease"]}`
- playwright (plugin) · `"playwright": {"command": "cmd", "args": ["/c", "npx", "-y", "@playwright/mcp@latest"]}`

## Anahtar elle — canlı config'e girmez (Desktop kullanıcı env değişkenini sunucuya taşımaz)

- context7 · `"context7": {"command": "cmd", "args": ["/c", "npx", "-y", "@upstash/context7-mcp", "--api-key", "<CONTEXT7_API_KEY>"]}`
- code-review · `"code-review": {"command": "uvx", "args": ["code-review-mcp@2.0.0"], "env": {"GITHUB_TOKEN": "<GITHUB_TOKEN>", "GITLAB_TOKEN": "<GITLAB_TOKEN>"}}`
- nano-banana-2 (plugin) · `"nano-banana-2": {"command": "cmd", "args": ["/c", "npx", "-y", "nano-banana-2-mcp@0.1.1"], "env": {"GEMINI_API_KEY": "<GEMINI_API_KEY>"}}`
- claude-mem-cowork (plugin, MCP sunucusu yok; cmem.ai `/api/mcp`) · `<CMEM_API_KEY>`, `<CMEM_USER_ID>` · CMEM_API_KEY tanımlanırsa oturum verisi cmem.ai'ye gider

## Önkoşul eksik / bağlanmıyor — config'e girmez

- stitch · `@_davideast/stitch-mcp@0.9.0 proxy` · gcloud kimliği yok · 22 Eyl sonrası ayrı kalem
- omniroute · `omniroute@3.8.49 --mcp` · yerel OmniRoute sunucusu yok · 22 Eyl sonrası ayrı kalem
- supabase (plugin) · `https://mcp.supabase.com/mcp` · OAuth: CC'de bağlı; claude.ai/Desktop'ta ayrıca OAuth gerekir
- claude-mem mcp-search (plugin) · yerel claude-mem worker + plugin kökü (`CLAUDE_PLUGIN_ROOT`) gerekir; Desktop'ta taşınamaz
- Obsidian gerektiren MCP: yok

## Desktop bölümü · KURULUM-11 güncellemesi (20 Eyl 2026)

Canlı config artık **16** stdio tanımı içeriyor (önce 10). Yedek: `claude_desktop_config.json.bak11`.

Eklenen (K3 kuru testiyle kanıtlı): `brave-search` 8, `context7` 2, `stitch` 16,
`omniroute` 110, `code-review` 12, `claude-mem` 15 araç.
Düzeltilen: `headroom` → CC'deki kanıtlı tanıma hizalandı (`.local\bin\headroom.EXE mcp serve`).

Anahtarlar config'e düz yazılmaz: `env` bloğu yok → süreç kullanıcı ortam değişkenlerini
devralır; argüman gerekiyorsa `cmd /c ... %VAR%` ile cmd.exe genişletir. Kanıt ve tam
tablo: `docs/desktop-eslesme.md`.

Önceki "yapısal olarak taşınamaz" notu **claude-mem için geçersiz**: `CLAUDE_PLUGIN_ROOT`
tanımsızken sarmalayıcı `~/.claude/plugins/cache/thedotmack/claude-mem` yoluna düşüyor ve
sunucu 15 araçla açılıyor. Desktop config'ine doğrudan betik yoluyla girdi.

Yerel MCP'ler yalnız **Chat** sekmesinde kullanılabilir; Cowork ve Code oturumları
`status=unsupported` olan VM paketine bağlı (`logs/cowork_vm_node.log`).
