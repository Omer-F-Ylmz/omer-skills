# Hesaplar (kurulum turu 3c)

Anahtar değerleri hiçbir dosyaya yazılmaz: `setx <ENV> <değer>` ile kullanıcı ortamına, değeri komut çıktısına basmadan. MCP tanımları `${ENV}` başvurusu kullanır; env gelince `claude mcp list` Connected olur. "Ücretsiz" sütunu: var / yok / ? (doğrulanmadı).

## A. Yazılımı kurulu, anahtar bekleyen (env adı yeterli)
| Servis | Kurulan | Env adı | Kayıt | Ücretsiz |
|---|---|---|---|---|
| Airtable | MCP airtable | AIRTABLE_API_KEY | airtable.com/create/tokens | var (kişisel token) |
| Netlify | MCP netlify + netlify-cli | NETLIFY_AUTH_TOKEN | app.netlify.com/user/applications | var |
| Vercel | vercel CLI | VERCEL_TOKEN | vercel.com/account/tokens | var (Hobby) |
| Apify | MCP apify | APIFY_TOKEN | console.apify.com/settings/integrations | var (aylık kredi) |
| n8n | MCP n8n-mcp | N8N_API_URL, N8N_API_KEY | kendi n8n örneği → Settings → API | örnek kendi barındırma |
| Hostinger | MCP hostinger | HOSTINGER_API_TOKEN | hpanel.hostinger.com → API | yok (ücretli hosting) |
| ClickHouse | MCP clickhouse | CLICKHOUSE_HOST, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD | clickhouse.cloud | var (deneme) |
| Auth0 | MCP auth0 (beta) | `auth0 login` oturumu | auth0.com/signup | var |
| Canva | MCP canva (http) | OAuth (env yok) | canva.com | var |
| Search Console | MCP gsc + C:\Projeler\uygulamalar\mcp-gsc | GSC_OAUTH_CLIENT_SECRETS_FILE | console.cloud.google.com | var |
| TestSprite | testsprite-cli | TESTSPRITE_API_KEY | testsprite.com | ? |
| Alibaba open-code-review | ocr CLI | LLM sağlayıcı anahtarı (README Configuration) | — | sağlayıcıya bağlı |
| Codex | plugin openai-codex | `codex login` | openai.com | ChatGPT planına bağlı |
| Azure | plugin azure-skills | `az login` | azure.microsoft.com/free | var (deneme kredisi) |
| Adobe | plugin adobe-for-creativity | Adobe oturumu | adobe.com | ? |
| Gemini | plugin banana-claude | GEMINI_API_KEY | aistudio.google.com/apikey | var |

## B. Web-only servisler (kurulacak paket yok)
| Servis | Env adı | Kayıt | Ücretsiz |
|---|---|---|---|
| OpenRouter | OPENROUTER_API_KEY | openrouter.ai/keys | var (ücretsiz modeller) |
| kie.ai (+ docs.kie.ai) | KIE_API_KEY | kie.ai | ? |
| MiniMax (minimax.io, platform.minimax.cn) | MINIMAX_API_KEY | platform.minimax.io | ? |
| Upload-Post | UPLOAD_POST_API_KEY | upload-post.com | ? |
| Groq | GROQ_API_KEY | console.groq.com/keys | var |
| Notion | NOTION_TOKEN | notion.so/profile/integrations | var |
| Sent.dm | SENT_API_KEY | sent.dm | ? |
| Stripe (+ docs) | STRIPE_API_KEY | dashboard.stripe.com/apikeys | var (test modu) |
| fal.ai | FAL_KEY | fal.ai/dashboard/keys | ? |
| Luma | LUMA_API_KEY | lumalabs.ai | ? |
| Anchor Browser | ANCHOR_API_KEY | docs.anchorbrowser.io | ? |
| Inference.net | INFERENCE_API_KEY | inference.net | ? |
| httpSMS | HTTPSMS_API_KEY | httpsms.com | var (kendi telefonun) |
| WaveSpeed | WAVESPEED_API_KEY | wavespeed.ai | ? |
| Gemini API | GEMINI_API_KEY | aistudio.google.com/apikey | var |
| Together AI | TOGETHER_API_KEY | api.together.ai/settings/api-keys | ? |
| Arcade | ARCADE_API_KEY | arcade.dev | ? |
| Zapier MCP | (URL hesaba özel) | mcp.zapier.com | var (sınırlı görev) |
| IMG.LY | lisans anahtarı | img.ly | ? |
| ZoomInfo | (kurumsal) | zoominfo.com | yok |

## C. Servis + kurulmayan yazılım (neden)
| Servis | Env adı | Kayıt | Ücretsiz | Kurulmadı çünkü |
|---|---|---|---|---|
| Firecrawl (cli + plugin) | FIRECRAWL_API_KEY | firecrawl.dev | var (kredi) | iki repo da lisanssız (lisans kapısı) |
| SerpApi | SERPAPI_API_KEY | serpapi.com | var (aylık 100) | `serpapi-mcp-server` PyPI'da doğrulanamadı |
| Neon | NEON_API_KEY | console.neon.tech | var | MCP anahtarı komut argümanı olarak ister (config'e sızar); pinli 1.0.0 yok, son sürüm 0.6.5 |
| Datadog | DD_API_KEY, DD_APP_KEY | datadoghq.com | deneme | npm paketi yok, SHA'lı kurulum tarifi yok |
| Composio | COMPOSIO_API_KEY | app.composio.dev | var | pinli alpha sürümü yok (npm 1.0.0) |
| DeepSeek | DEEPSEEK_API_KEY | platform.deepseek.com | ? | `@deepseek-ai/dsh-root` npm'de yok |
| MiroFish | LLM_API_KEY, ZEP_API_KEY | getzep.com | var | `mirofish` npm'de yok |
| DataForSEO (open-seo) | DATAFORSEO_API_KEY | app.dataforseo.com | yok | kendi barındırdığın uygulama |
| Letta (claude-subconscious) | LETTA_API_KEY | app.letta.com | var | konuşmaları Letta'ya yollar ve claude-mem ile çakışır; anahtar sonrası elle |
| Lusha | LUSHA_API_KEY | lusha.com | sınırlı | doğrulanmamış 4★ eklenti, kişisel veri riski |
| Tiger Data | TIGER_PUBLIC_KEY, TIGER_SECRET_KEY | console.cloud.timescale.com | var | kurulum yolu yok (`?`) |
| Stripe CLI | `stripe login` | stripe.com | var | Windows ikilisi pinli değil |
| Apify agent-skills | APIFY_TOKEN | console.apify.com | var | repo lisanssız |
| MiniMax stack | MINIMAX_API_KEY | platform.minimax.io | ? | doğrulanmadı |
| github-copilot-for-azure | az login | — | — | LICENSE ürün koşulları (özel), açık lisans değil |
| remorses/zele, superdesigndev/treg | OAuth / ? | — | — | lisanssız / özel lisans |
| ScrapeGraphAI | SGAI_API_KEY | scrapegraphai.com | var | proje bağımlılığı (tetikleyici.md) |
| Google Workspace CLI, Vibe-Trading | OAuth / ALPHAVANTAGE_API_KEY | — | — | 95 + 91 skill bağlam şişirir (tetikleyici.md) |
