# RET-KUR-1b (28 Eki 2026)

Anahtarlar HKCU\Environment'ta; yalnız varlık denetlendi, değer yazılmadı. Kurulum CC user scope (`${VAR}`), Desktop config (yedek `claude_desktop_config.json.bak28ret`; Desktop'ı yeniden başlat).

| Kalem | Kurulum | Doğrulama | Ücretsiz kota |
|---|---|---|---|
| Meta Ads | `meta-ads`: `uvx meta-ads-mcp` (pipeboard, BUSL-1.1), env META_ACCESS_TOKEN | tools/list 35 araç; Graph `/me` 200. **Token 27 Ara 2026'da sona erer** | API ücretsiz, reklam harcaması ayrı |
| Oxylabs | `oxylabs-ai-studio`: `uvx --with "mcp<2" oxylabs-ai-studio-mcp`, OXYLABS_API_KEY → OXYLABS_AI_STUDIO_API_KEY (kullanıcı adı/şifre gerekmedi) | tools/list döndü; anahtar geçerliliği ücretsiz çağrıyla doğrulanamadı (ücretli çağrı yasak) | deneme kredisi hesaba bağlı |
| Apify x4 | `apify-actors`: `npx @apify/actors-mcp-server` (4 kalem tek sunucu; mevcut `apify` gateway girişi korundu) | tools/list 12 araç; `/v2/users/me` 200 | aylık ücretsiz $5 kredi |
| fal.ai | `fal`: uzak http `https://mcp.fal.ai/mcp`, `Authorization: Key ${FAL_KEY}` | initialize + tools/list 200 | ücretsiz kota yok, kullandıkça öde |
| Modal | `uv tool install modal` 1.6.3 (CLI) | `modal token info` çalışıyor (workspace omery3899) | aylık $30 ücretsiz kredi |
| Higgsfield+Kling | `higgsfield-client` 0.2.0, venv `C:\Users\pc\.venvs\higgsfield`; resmî MCP OAuth ister, kurulmadı. Kling Higgsfield üzerinden | REST status `Key key:secret` ile 404 (Bearer 401) → kimlik geçti; üretim çağrısı yapılmadı | kredi bazlı |
| Rube/Composio | `composio`: uzak http `https://connect.composio.dev/mcp`, `x-consumer-api-key: ${COMPOSIO_API_KEY}` | tools/list döndü (v3 REST uç noktası anahtarı reddetti, MCP uç noktası kabul etti) | ücretsiz plan var |
| Telegram | bot `@ofclaudemy_bot` (getMe 200) | **KISMİ**: getUpdates boş, webhook yok, /start görünmüyor → chat_id yok, test mesajı gönderilmedi | ücretsiz |

Tarama: gitleaks (CC `.claude.json` + Desktop config kopyaları) temiz; semgrep p/secrets bulgu yok.
Sapma: Telegram `ret-denetim.tsv`'de KURULAMAZ(hesap) kaldı (12 diğer satır KURULDU). Oxylabs için `mcp<2` sabitlendi (paket FastMCP v2 ile bozuk). Desktop'ta http sunucular `mcp-remote` ile, `%VAR%` cmd kabuğunda genişliyor.
Telegram için Ömer'in bota yeniden `/start` yazması gerek; sonra getUpdates → tek test mesajı.
