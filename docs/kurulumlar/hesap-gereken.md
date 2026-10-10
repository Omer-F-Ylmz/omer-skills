# Hesap gereken servisler — öncelik sırası (TUR-6c-B1, 2026-10-10)

Anahtar/hesap değerleri asla yazılmaz; durum VAR/YOK boolean. "Hesap bağlayıcısı" = claude.ai Desktop bağlayıcısı mı, CC env mi sütununda.

## 1. Mevcut anahtarla karşılananlar (hesap gerekmez)

| servis | env adı | not |
|---|---|---|
| OpenRouter | OPENROUTER_API_KEY | openrouter.ai satırları (5) karşılanır |
| Gemini | GEMINI_API_KEY | ai.google.dev, generativelanguage.googleapis.com |
| Groq | GROQ_API_KEY | console.groq.com |
| Anthropic API | ANTHROPIC_API_KEY | Anthropic/Claude API satırları |
| Context7 | CONTEXT7_API_KEY | context7 MCP/CLI |
| 21st | 21ST_API_KEY | 21st.dev magic |
| Brave | BRAVE_API_KEY | brave search MCP |
| Stitch | STITCH_API_KEY | Google Stitch MCP |
| GitHub | GITHUB_PERSONAL_ACCESS_TOKEN | github MCP/gh |

## 2. Öncelik sıralı tablo (hesaplar.md derlemesi: kayıt URL + env adı + durum)

| # | Servis | Ne açar | Ücretsiz katman | Kayıt URL | Env adı | Durum | Ö | Bağlayıcı mı, CC env mi |
|---|---|---|---|---|---|---|---|---|
| 2 | Netlify | MCP netlify + netlify-cli (site) | Free: 300 kredi limiti; bant 20 kr/GB, üretim deploy 15 kr (doğrulandı, netlify.com/pricing) | app.netlify.com/user/applications | NETLIFY_AUTH_TOKEN | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 3 | fal.ai | `@fal-ai/client`, görsel/video üretim API | Fiyat sayfasında ücretsiz kredi/plan yazmıyor; kullanım başına ödeme (doğrulandı: belirtilmemiş) | fal.ai/dashboard/keys | FAL_KEY | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 4 | Tripo3D | metinden/görselden 3D model (Blender/3D) | Free: 200 kredi/ay, 1 eşzamanlı iş, modeller herkese açık + ticari değil; API ayrı havuz, ücretsiz API doğrulanmadı (ikincil; tripo3d.ai/pricing 403) | platform.tripo3d.ai | TRIPO_API_KEY (varsayım) | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 5 | Higgsfield | video/görsel üretim, MCP mcp.higgsfield.ai (video, görsel) | Ücretsiz plan 0 kredi, yalnız 24 sa deneme (karta bağlı, sonra Plus'a yenilenir); eski kaynaklar 10 kredi/gün diyor (ikincil, 2026-10-03 değişikliği) | higgsfield.ai/pricing | OAuth (env yok) | — | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 6 | kie.ai (+docs.kie.ai, felores/kie-cli-mcp) | medya üretim API, CLI+MCP (video, görsel) | Kayıt kredisi dokümanda yok; ortak kredi bakiyesi, ücretli (ikincil) | kie.ai | KIE_API_KEY | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 7 | Gemini API | banana-claude görsel, genel LLM (görsel) | Flash/Flash-Lite ücretsiz, kart yok; Pro ücretsizden çıktı; limitler kaynağa göre değişir, AI Studio'daki kota esas (ikincil) | aistudio.google.com/apikey | GEMINI_API_KEY | **VAR** | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 8 | OpenRouter | model ağ geçidi (video/oto. altyapı) | ücretsiz modeller var (eski not) | openrouter.ai/keys | OPENROUTER_API_KEY | **VAR** | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 9 | Groq | hızlı LLM/ses çıkarımı (video transkript) | Ücretsiz, kart yok: küçük modellerde 30 RPM/14.4K istek/gün; büyüklerde ~1K istek/gün (ikincil; console.groq.com/settings/limits esas) | console.groq.com/keys | GROQ_API_KEY | **VAR** | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 10 | Mobbin | tasarım referansı, mobbin/skills + MCP (site/frontend) | Pro/Team plan + tarayıcı girişi ister; ücretsiz katman doğrulanamadı (mobbin.com/pricing 403) | mobbin.com | OAuth/tarayıcı girişi | — | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 11 | Pixellab | pixel-art üretimi (oyun) | "Try for free", kart yok; kapsam sayfada yazmıyor (ikincil) | pixellab.ai | PIXELLAB_API_KEY (varsayım) | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 12 | Upload-Post | video/sosyal paylaşım API (video) | ? | upload-post.com | UPLOAD_POST_API_KEY | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 13 | Google Search Console (mcp-gsc) | site SEO verisi MCP (site) | var (Google hesabı, ücretsiz API) | console.cloud.google.com | GSC_OAUTH_CLIENT_SECRETS_FILE | YOK | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 14 | Canva | MCP canva (görsel) | Canva ücretsiz plan var; MCP'ye OAuth (eski not: 401) | canva.com | OAuth (env yok) | — | Y | CC env (Desktop bağlayıcısı varsa oradan) |
| 15 | Stability AI (stableaudio, platform.stability.ai) | görsel/ses üretim API | ? | platform.stability.ai | STABILITY_API_KEY (varsayım) | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 16 | MiniMax (minimax.io, platform.minimax.cn) | video/ses üretim API | ? | platform.minimax.io | MINIMAX_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 17 | WaveSpeed | görsel/video API | ? | wavespeed.ai | WAVESPEED_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 18 | Luma | video üretim | ? | lumalabs.ai | LUMA_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 19 | Midjourney | görsel (yalnız abonelik, API yok) | yok (abonelik) | midjourney.com | — | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 20 | Lovable | site üretici (resmi skill/MCP yok) | ? | lovable.dev | — | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 21 | bolt.new | site üretici (skill yok) | ? | bolt.new | — | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 22 | Anima (animaapp.com) | tasarım→kod (skill yok) | ? | animaapp.com | — | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 23 | Adobe for Creativity | claude-plugins-official eklentisi (görsel) | ? (Adobe hesabı) | adobe.com | oturum (env yok) | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 24 | Cloudinary | görsel barındırma/dönüştürme (site) | ? | cloudinary.com | CLOUDINARY_URL | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 25 | Together AI | LLM/görsel API | ? | api.together.ai/settings/api-keys | TOGETHER_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 26 | Notion | resmi MCP/API | var (eski not) | notion.so/profile/integrations | NOTION_TOKEN | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 27 | Airtable | MCP airtable (kurulu) | var, kişisel token (eski not) | airtable.com/create/tokens | AIRTABLE_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 28 | Apify (+agent-skills) | MCP apify (otomasyon, kazıma) | aylık kredi (eski not) | console.apify.com/settings/integrations | APIFY_TOKEN | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 29 | n8n | MCP n8n-mcp (otomasyon) | kendi barındırma | kendi n8n → Settings → API | N8N_API_URL, N8N_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 30 | Zapier MCP | otomasyon | sınırlı görev (eski not) | mcp.zapier.com | URL hesaba özel | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 31 | Stripe (+docs, CLI) | ödeme SDK (.NET/site) | test modu (eski not) | dashboard.stripe.com/apikeys | STRIPE_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 32 | TestSprite | testsprite-cli (test) | ? | testsprite.com | TESTSPRITE_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 33 | CodeRabbit | `coderabbit` eklentisi (kod inceleme, .NET dahil) | ? | coderabbit.ai | CLI girişi (env yok) | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 34 | open-code-review (alibaba) | `ocr` CLI (kod inceleme) | araç ücretsiz, LLM sağlayıcı anahtarı ister | README | LLM sağlayıcı anahtarı | — | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 35 | Firecrawl | kazıma | ? | firecrawl.dev | FIRECRAWL_API_KEY | YOK | O | CC env (Desktop bağlayıcısı varsa oradan) |
| 36 | ScrapeGraphAI | kazıma (proje bağımlılığı) | var (eski not) | scrapegraphai.com | SGAI_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 37 | SerpApi | arama API | ? | serpapi.com | SERPAPI_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 38 | Anchor Browser | tarayıcı ajanı API | ? | docs.anchorbrowser.io | ANCHOR_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 39 | Inference.net | LLM API | ? | inference.net | INFERENCE_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 40 | Hostinger | MCP hostinger | yok (ücretli hosting) | hpanel.hostinger.com → API | HOSTINGER_API_TOKEN | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 41 | ClickHouse | MCP clickhouse (.NET/veri) | deneme (eski not) | clickhouse.cloud | CLICKHOUSE_HOST, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD | YOK (parola) | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 42 | Auth0 | MCP auth0 (beta) | var (eski not) | auth0.com/signup | `auth0 login` oturumu | — | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 43 | Azure (azure-skills, github-copilot-for-azure) | Azure eklentileri (.NET dağıtım) | azure.microsoft.com/free (eski not) | azure.microsoft.com/free | `az login` | — | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 44 | Neon | Postgres MCP | ? | console.neon.tech | NEON_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 45 | Datadog | MCP datadog | yok (kurumsal) | datadoghq.com | DD_API_KEY, DD_APP_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 46 | Composio | araç ağ geçidi | ? | app.composio.dev | COMPOSIO_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 47 | Arcade | araç ağ geçidi | ? | arcade.dev | ARCADE_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 48 | DeepSeek | Vibe-Trading ve LLM | ? | platform.deepseek.com | DEEPSEEK_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 49 | Letta (claude-subconscious) | konuşmaları Letta'ya yollar, claude-mem ile çakışır | var (eski not) | app.letta.com | LETTA_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 50 | DataForSEO (open-seo) | SEO verisi | yok | app.dataforseo.com | DATAFORSEO_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 51 | Lusha | satış verisi, kişisel veri riski | sınırlı (eski not) | lusha.com | LUSHA_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 52 | ZoomInfo | kurumsal satış verisi, işle ilgisiz | yok | zoominfo.com | (kurumsal) | — | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 53 | Tiger Data | Postgres/Timescale | var (eski not) | console.cloud.timescale.com | TIGER_PUBLIC_KEY, TIGER_SECRET_KEY | — | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 54 | Sent.dm | mesajlaşma API | ? | sent.dm | SENT_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 55 | httpSMS | SMS (kendi telefon) | var, kendi telefon (eski not) | httpsms.com | HTTPSMS_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 56 | IMG.LY | ticari SDK | ? | img.ly | lisans anahtarı | — | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 57 | Google Workspace CLI (googleworkspace/cli) | 95 skill, bağlam şişirir | Google hesabı OAuth | — | OAuth | — | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 58 | Alpha Vantage (Vibe-Trading) | finans verisi | ? | alphavantage.co | ALPHAVANTAGE_API_KEY | YOK | D | CC env (Desktop bağlayıcısı varsa oradan) |
| 59 | remorses/zele, superdesigndev/treg | e-posta CLI, araç ağ geçidi (lisanssız/özel) | — | — | OAuth / ? | — | D | CC env (Desktop bağlayıcısı varsa oradan) |

## 3. Yeni servisler (B1 listesinden, hesaplar.md'de yoktu; en alta)

| Servis | Kalemler | Kayıt URL | Env adı | Bağlayıcı mı, CC env mı |
|---|---|---|---|---|
| ahiggsfield/oli | 1: ahiggsfield/oli | ahiggsfield/oli | belirsiz (servis dokümanı) | CC env |
| aisstream.io | 1: aisstream.io | aisstream.io/apikeys | AISSTREAM_API_KEY | CC env |
| alibaba/open-code-review | 1: alibaba/open-code-review | alibaba/open-code-review | belirsiz (servis dokümanı) | CC env |
| omnisend.com | 1: api-docs.omnisend.com | app.omnisend.com | OMNISEND_API_KEY | CC env |
| getartcraft.com | 2: app.getartcraft.com, getartcraft.com | getartcraft.com | belirsiz (servis dokümanı) | CC env |
| atomicbot.ai | 1: atomicbot.ai | atomicbot.ai | belirsiz (servis dokümanı) | CC env |
| cal-com- | 1: cal-com- | cal-com- | belirsiz (servis dokümanı) | CC env |
| figma-developer-mcp | 1: figma-developer-mcp | figma.com/settings (Personal access tokens) | FIGMA_API_KEY | CC env |
| figma-developer-mcp-figma-api-key | 1: figma-developer-mcp-figma-api-key | figma.com/settings (Personal access tokens) | FIGMA_API_KEY | CC env |
| googleapis.com | 1: generativelanguage.googleapis.com | googleapis.com | belirsiz (servis dokümanı) | CC env |
| glips/figma-context-mcp | 3: glips/figma-contexi, glips/figma-context-mcp | figma.com/settings (Personal access tokens) | FIGMA_API_KEY | CC env |
| streamlinehq.com | 1: go.streamlinehq.com | streamlinehq.com | belirsiz (servis dokümanı) | CC env |
| sensortower.com | 2: help.sensortower.com, sensortower.com | sensortower.com | belirsiz (servis dokümanı) | CC env |
| higsfielda/ainfluencer-studio | 1: higsfielda/ainfluencer-studio | higsfielda/ainfluencer-studio | belirsiz (servis dokümanı) | CC env |
| iggsfielda/ai-influencer-studio | 1: iggsfielda/ai-influencer-studio | iggsfielda/ai-influencer-studio | belirsiz (servis dokümanı) | CC env |
| igsield.a | 1: igsield.a/aifuencer-studio | igsield.a | belirsiz (servis dokümanı) | CC env |
| iktof.com | 1: iktof.com | iktof.com | belirsiz (servis dokümanı) | CC env |
| letta-ai/claude-subconscious | 1: letta-ai/claude-subconscious | letta-ai/claude-subconscious | belirsiz (servis dokümanı) | CC env |
| higgsfleldl.al | 1: mcp.higgsfleldl.al | higgsfleldl.al | belirsiz (servis dokümanı) | CC env |
| higsfield.ai | 1: mcp.higsfield.ai | higsfield.ai | belirsiz (servis dokümanı) | CC env |
| hlgsfield.al | 1: mcp.hlgsfield.al | hlgsfield.al | belirsiz (servis dokümanı) | CC env |
| microsoft/azure-skills | 2: microsoft/azure-s, microsoft/azure-sk111s | microsoft/azure-skills | belirsiz (servis dokümanı) | CC env |
| microsoft/github-copilot-for-azure | 1: microsoft/github-copilot-for-azure | microsoft/github-copilot-for-azure | belirsiz (servis dokümanı) | CC env |
| nightvision | 1: nightvision | nightvision | belirsiz (servis dokümanı) | CC env |
| owalalife.com | 1: owalalife.com | owalalife.com | belirsiz (servis dokümanı) | CC env |
| trovebrands.com | 2: preferences.trovebrands.com, trovebrands.com | trovebrands.com | belirsiz (servis dokümanı) | CC env |
| tiktof.com | 1: tiktof.com | tiktof.com | belirsiz (servis dokümanı) | CC env |
| worldllabs.ai | 1: worldllabs.ai | worldllabs.ai | belirsiz (servis dokümanı) | CC env |
| worldllabs.aiflabs | 1: worldllabs.aiflabs | worldllabs.aiflabs | belirsiz (servis dokümanı) | CC env |
