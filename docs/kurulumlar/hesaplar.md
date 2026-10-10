## Açılacak hesaplar (öncelik sırası)

Derleme 2026-10-10. Kaynak: bu dosyanın eski bölümleri, tur3/4/5/5b sonuç TSV'leri (sınıf HESAP), tetikleyici.md, kurulum-3c raporu. Durum = Windows kullanıcı/makine/süreç ortamında değişken adı tanımlı mı (yalnız VAR/YOK; değer okunmadı). Ücretsiz sütunu: **doğrulandı** = resmi sayfa 2026-10-10 okundu; **ikincil** = resmi sayfa okunamadı/boş, arama sonuçları (kaynaklar çelişebilir); **eski not** = bu dosyadaki önceki not, yeniden doğrulanmadı; **?** = bilinmiyor. Öncelik: Y = site/frontend, video, görsel, Blender/3D işlerinde hemen değer · O = orta · D = düşük.

| # | Servis | Ne açar (iş kolu) | Ücretsiz katman | Kayıt URL | Env adı | Durum | Ö |
|---|---|---|---|---|---|---|---|
| 1 | Vercel | `vercel` CLI, deploy (site) | Hobby $0: 1M CDN isteği, 100 GB transfer, 1M fonksiyon çağrısı, 4 sa Active CPU/ay; kişisel/ticari olmayan (doğrulandı, vercel.com/pricing) | vercel.com/account/tokens | VERCEL_TOKEN | YOK | Y |
| 2 | Netlify | MCP netlify + netlify-cli (site) | Free: 300 kredi limiti; bant 20 kr/GB, üretim deploy 15 kr (doğrulandı, netlify.com/pricing) | app.netlify.com/user/applications | NETLIFY_AUTH_TOKEN | YOK | Y |
| 3 | fal.ai | `@fal-ai/client`, görsel/video üretim API | Fiyat sayfasında ücretsiz kredi/plan yazmıyor; kullanım başına ödeme (doğrulandı: belirtilmemiş) | fal.ai/dashboard/keys | FAL_KEY | YOK | Y |
| 4 | Tripo3D | metinden/görselden 3D model (Blender/3D) | Free: 200 kredi/ay, 1 eşzamanlı iş, modeller herkese açık + ticari değil; API ayrı havuz, ücretsiz API doğrulanmadı (ikincil; tripo3d.ai/pricing 403) | platform.tripo3d.ai | TRIPO_API_KEY (varsayım) | YOK | Y |
| 5 | Higgsfield | video/görsel üretim, MCP mcp.higgsfield.ai (video, görsel) | Ücretsiz plan 0 kredi, yalnız 24 sa deneme (karta bağlı, sonra Plus'a yenilenir); eski kaynaklar 10 kredi/gün diyor (ikincil, 2026-10-03 değişikliği) | higgsfield.ai/pricing | OAuth (env yok) | — | Y |
| 6 | kie.ai (+docs.kie.ai, felores/kie-cli-mcp) | medya üretim API, CLI+MCP (video, görsel) | Kayıt kredisi dokümanda yok; ortak kredi bakiyesi, ücretli (ikincil) | kie.ai | KIE_API_KEY | YOK | Y |
| 7 | Gemini API | banana-claude görsel, genel LLM (görsel) | Flash/Flash-Lite ücretsiz, kart yok; Pro ücretsizden çıktı; limitler kaynağa göre değişir, AI Studio'daki kota esas (ikincil) | aistudio.google.com/apikey | GEMINI_API_KEY | **VAR** | Y |
| 8 | OpenRouter | model ağ geçidi (video/oto. altyapı) | ücretsiz modeller var (eski not) | openrouter.ai/keys | OPENROUTER_API_KEY | **VAR** | Y |
| 9 | Groq | hızlı LLM/ses çıkarımı (video transkript) | Ücretsiz, kart yok: küçük modellerde 30 RPM/14.4K istek/gün; büyüklerde ~1K istek/gün (ikincil; console.groq.com/settings/limits esas) | console.groq.com/keys | GROQ_API_KEY | **VAR** | Y |
| 10 | Mobbin | tasarım referansı, mobbin/skills + MCP (site/frontend) | Pro/Team plan + tarayıcı girişi ister; ücretsiz katman doğrulanamadı (mobbin.com/pricing 403) | mobbin.com | OAuth/tarayıcı girişi | — | Y |
| 11 | Pixellab | pixel-art üretimi (oyun) | "Try for free", kart yok; kapsam sayfada yazmıyor (ikincil) | pixellab.ai | PIXELLAB_API_KEY (varsayım) | YOK | Y |
| 12 | Upload-Post | video/sosyal paylaşım API (video) | ? | upload-post.com | UPLOAD_POST_API_KEY | YOK | Y |
| 13 | Google Search Console (mcp-gsc) | site SEO verisi MCP (site) | var (Google hesabı, ücretsiz API) | console.cloud.google.com | GSC_OAUTH_CLIENT_SECRETS_FILE | YOK | Y |
| 14 | Canva | MCP canva (görsel) | Canva ücretsiz plan var; MCP'ye OAuth (eski not: 401) | canva.com | OAuth (env yok) | — | Y |
| 15 | Stability AI (stableaudio, platform.stability.ai) | görsel/ses üretim API | ? | platform.stability.ai | STABILITY_API_KEY (varsayım) | YOK | O |
| 16 | MiniMax (minimax.io, platform.minimax.cn) | video/ses üretim API | ? | platform.minimax.io | MINIMAX_API_KEY | YOK | O |
| 17 | WaveSpeed | görsel/video API | ? | wavespeed.ai | WAVESPEED_API_KEY | YOK | O |
| 18 | Luma | video üretim | ? | lumalabs.ai | LUMA_API_KEY | YOK | O |
| 19 | Midjourney | görsel (yalnız abonelik, API yok) | yok (abonelik) | midjourney.com | — | — | O |
| 20 | Lovable | site üretici (resmi skill/MCP yok) | ? | lovable.dev | — | — | O |
| 21 | bolt.new | site üretici (skill yok) | ? | bolt.new | — | — | O |
| 22 | Anima (animaapp.com) | tasarım→kod (skill yok) | ? | animaapp.com | — | — | O |
| 23 | Adobe for Creativity | claude-plugins-official eklentisi (görsel) | ? (Adobe hesabı) | adobe.com | oturum (env yok) | — | O |
| 24 | Cloudinary | görsel barındırma/dönüştürme (site) | ? | cloudinary.com | CLOUDINARY_URL | YOK | O |
| 25 | Together AI | LLM/görsel API | ? | api.together.ai/settings/api-keys | TOGETHER_API_KEY | YOK | O |
| 26 | Notion | resmi MCP/API | var (eski not) | notion.so/profile/integrations | NOTION_TOKEN | YOK | O |
| 27 | Airtable | MCP airtable (kurulu) | var, kişisel token (eski not) | airtable.com/create/tokens | AIRTABLE_API_KEY | YOK | O |
| 28 | Apify (+agent-skills) | MCP apify (otomasyon, kazıma) | aylık kredi (eski not) | console.apify.com/settings/integrations | APIFY_TOKEN | YOK | O |
| 29 | n8n | MCP n8n-mcp (otomasyon) | kendi barındırma | kendi n8n → Settings → API | N8N_API_URL, N8N_API_KEY | YOK | O |
| 30 | Zapier MCP | otomasyon | sınırlı görev (eski not) | mcp.zapier.com | URL hesaba özel | — | O |
| 31 | Stripe (+docs, CLI) | ödeme SDK (.NET/site) | test modu (eski not) | dashboard.stripe.com/apikeys | STRIPE_API_KEY | YOK | O |
| 32 | TestSprite | testsprite-cli (test) | ? | testsprite.com | TESTSPRITE_API_KEY | YOK | O |
| 33 | CodeRabbit | `coderabbit` eklentisi (kod inceleme, .NET dahil) | ? | coderabbit.ai | CLI girişi (env yok) | — | O |
| 34 | open-code-review (alibaba) | `ocr` CLI (kod inceleme) | araç ücretsiz, LLM sağlayıcı anahtarı ister | README | LLM sağlayıcı anahtarı | — | O |
| 35 | Firecrawl | kazıma | ? | firecrawl.dev | FIRECRAWL_API_KEY | YOK | O |
| 36 | ScrapeGraphAI | kazıma (proje bağımlılığı) | var (eski not) | scrapegraphai.com | SGAI_API_KEY | YOK | D |
| 37 | SerpApi | arama API | ? | serpapi.com | SERPAPI_API_KEY | YOK | D |
| 38 | Anchor Browser | tarayıcı ajanı API | ? | docs.anchorbrowser.io | ANCHOR_API_KEY | YOK | D |
| 39 | Inference.net | LLM API | ? | inference.net | INFERENCE_API_KEY | YOK | D |
| 40 | Hostinger | MCP hostinger | yok (ücretli hosting) | hpanel.hostinger.com → API | HOSTINGER_API_TOKEN | YOK | D |
| 41 | ClickHouse | MCP clickhouse (.NET/veri) | deneme (eski not) | clickhouse.cloud | CLICKHOUSE_HOST, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD | YOK (parola) | D |
| 42 | Auth0 | MCP auth0 (beta) | var (eski not) | auth0.com/signup | `auth0 login` oturumu | — | D |
| 43 | Azure (azure-skills, github-copilot-for-azure) | Azure eklentileri (.NET dağıtım) | azure.microsoft.com/free (eski not) | azure.microsoft.com/free | `az login` | — | D |
| 44 | Neon | Postgres MCP | ? | console.neon.tech | NEON_API_KEY | YOK | D |
| 45 | Datadog | MCP datadog | yok (kurumsal) | datadoghq.com | DD_API_KEY, DD_APP_KEY | YOK | D |
| 46 | Composio | araç ağ geçidi | ? | app.composio.dev | COMPOSIO_API_KEY | YOK | D |
| 47 | Arcade | araç ağ geçidi | ? | arcade.dev | ARCADE_API_KEY | YOK | D |
| 48 | DeepSeek | Vibe-Trading ve LLM | ? | platform.deepseek.com | DEEPSEEK_API_KEY | YOK | D |
| 49 | Letta (claude-subconscious) | konuşmaları Letta'ya yollar, claude-mem ile çakışır | var (eski not) | app.letta.com | LETTA_API_KEY | YOK | D |
| 50 | DataForSEO (open-seo) | SEO verisi | yok | app.dataforseo.com | DATAFORSEO_API_KEY | YOK | D |
| 51 | Lusha | satış verisi, kişisel veri riski | sınırlı (eski not) | lusha.com | LUSHA_API_KEY | YOK | D |
| 52 | ZoomInfo | kurumsal satış verisi, işle ilgisiz | yok | zoominfo.com | (kurumsal) | — | D |
| 53 | Tiger Data | Postgres/Timescale | var (eski not) | console.cloud.timescale.com | TIGER_PUBLIC_KEY, TIGER_SECRET_KEY | — | D |
| 54 | Sent.dm | mesajlaşma API | ? | sent.dm | SENT_API_KEY | YOK | D |
| 55 | httpSMS | SMS (kendi telefon) | var, kendi telefon (eski not) | httpsms.com | HTTPSMS_API_KEY | YOK | D |
| 56 | IMG.LY | ticari SDK | ? | img.ly | lisans anahtarı | — | D |
| 57 | Google Workspace CLI (googleworkspace/cli) | 95 skill, bağlam şişirir | Google hesabı OAuth | — | OAuth | — | D |
| 58 | Alpha Vantage (Vibe-Trading) | finans verisi | ? | alphavantage.co | ALPHAVANTAGE_API_KEY | YOK | D |
| 59 | remorses/zele, superdesigndev/treg | e-posta CLI, araç ağ geçidi (lisanssız/özel) | — | — | OAuth / ? | — | D |

**D uzun kuyruk** (hesap ister, kurulacak skill yok; 2026-10-10 itibarıyla ücretsiz katman denetlenmedi): Shopify, Vanta, PagerDuty, Cal.com, Strikingly, hostingdunyam, use.app, prova.so, craft.io, Abacus, butter.video, Cerebrium, flyhermes, Streamline, Greptile, Hyperagent, Kaikaku, Sensor Tower, Loomshot, Lidlezz, Serus, ssscript, Skillbit, vals.ai, wowmade, World Labs (worldlabs.ai).

## Hesap açılınca

Anahtarı Ömer kendisi girer: `setx AD "<DEĞER>"` (yeni terminalde geçerli; değer dosyaya/sohbete yazılmaz). Sonra `claude mcp list`. "Yol doğrulanmadı" = kurulum komutu kaynaklarda pinli yok, hesap açılınca README'den bakılır.

**Y**
1. Vercel: `setx VERCEL_TOKEN "<DEĞER>"`. CLI kurulu (`npm i -g vercel@63.1.2`). Doğrula: `vercel whoami`.
2. Netlify: `setx NETLIFY_AUTH_TOKEN "<DEĞER>"`. CLI/MCP kurulu (`npm i -g netlify-cli@27.12.0`, `@netlify/mcp@1.18.0`). Doğrula: `netlify status`.
3. fal.ai: `setx FAL_KEY "<DEĞER>"`; projede `npm i @fal-ai/client@1.10.1`.
4. Tripo3D: `setx TRIPO_API_KEY "<DEĞER>"` (ad varsayım; platform.tripo3d.ai'den doğrula). Kurulum yolu yok; Blender işinde API/Studio ile kullanılır.
5. Higgsfield: kurulum komutu yok; MCP `https://mcp.higgsfield.ai` OAuth ister (yol doğrulanmadı). Hesapta kart + otomatik yenilenen deneme olduğuna dikkat; kaydolmadan önce kredi tavanı koy.
6. kie.ai: `setx KIE_API_KEY "<DEĞER>"`; CLI/MCP: github.com/felores/kie-cli-mcp @aa43e3955591 (kurulumdan sonra SHA doğrula).
7. Gemini API: env zaten VAR. banana-claude marketplace kurulu; ek adım yok.
8. OpenRouter: env zaten VAR; ek adım yok.
9. Groq: env zaten VAR; ek adım yok.
10. Mobbin: tarayıcıdan Pro/Team girişi; resmi `mobbin/skills` + Mobbin MCP (yol doğrulanmadı, docs.mobbin.com).
11. Pixellab: `setx PIXELLAB_API_KEY "<DEĞER>"` (ad varsayım). Kurulum yolu yok.
12. Upload-Post: `setx UPLOAD_POST_API_KEY "<DEĞER>"`. Kurulum yolu yok (yalnız API).
13. GSC: Google Cloud'da OAuth istemcisi aç, JSON'u dosyaya koy, `setx GSC_OAUTH_CLIENT_SECRETS_FILE "<DOSYA_YOLU>"`. MCP `C:\Projeler\uygulamalar\mcp-gsc` kurulu.
14. Canva: `claude mcp add --transport http canva https://mcp.canva.com/mcp`, ardından OAuth (MCP kurulu, OAuth bekler).

**O**
- Stability: `setx STABILITY_API_KEY "<DEĞER>"` · MiniMax: `setx MINIMAX_API_KEY "<DEĞER>"` · WaveSpeed: `setx WAVESPEED_API_KEY "<DEĞER>"` · Luma: `setx LUMA_API_KEY "<DEĞER>"` · Cloudinary: `setx CLOUDINARY_URL "<DEĞER>"` · Together: `setx TOGETHER_API_KEY "<DEĞER>"` (kurulum yolu yok; yalnız API).
- Midjourney, Lovable, bolt.new, Anima: yalnız web hesabı; kurulum yok.
- Adobe: `/plugin install adobe-for-creativity@claude-plugins-official` (kurulu), Adobe girişi.
- Notion: `setx NOTION_TOKEN "<DEĞER>"` · Airtable: `setx AIRTABLE_API_KEY "<DEĞER>"` (MCP kurulu: `airtable-mcp-server@1.14.0`) · Apify: `setx APIFY_TOKEN "<DEĞER>"` (MCP apify kurulu) · n8n: `setx N8N_API_URL "<URL>"`, `setx N8N_API_KEY "<DEĞER>"` · Zapier: mcp.zapier.com'dan kişisel URL ile MCP ekle.
- Stripe: `setx STRIPE_API_KEY "<DEĞER>"`; projede `npm i stripe@23.0.0` · TestSprite: `setx TESTSPRITE_API_KEY "<DEĞER>"` (CLI kurulu).
- CodeRabbit: hesap + CLI girişi, sonra `claude plugin install coderabbit@claude-plugins-official` · open-code-review: LLM sağlayıcı anahtarı (README'ye göre) · Firecrawl: `setx FIRECRAWL_API_KEY "<DEĞER>"`.

**D**
- Env adı olanlar: `setx <AD> "<DEĞER>"` (tablodaki Env sütunu: SGAI_API_KEY, SERPAPI_API_KEY, ANCHOR_API_KEY, INFERENCE_API_KEY, HOSTINGER_API_TOKEN, CLICKHOUSE_*, NEON_API_KEY, DD_API_KEY/DD_APP_KEY, COMPOSIO_API_KEY, ARCADE_API_KEY, DEEPSEEK_API_KEY, LETTA_API_KEY, DATAFORSEO_API_KEY, LUSHA_API_KEY, TIGER_*, SENT_API_KEY, HTTPSMS_API_KEY, ALPHAVANTAGE_API_KEY).
- Hostinger, ClickHouse, Auth0 (`auth0 login`), Azure (`az login`): yazılım kurulu (A bölümü), yalnız anahtar/giriş bekler.
- Letta: claude-mem ile çakışır, anahtar gelse de elle karar · Lusha, ZoomInfo, zele, treg: kişisel veri/lisans riski, hesap açılmaz · Datadog/Neon/Composio/Tiger/IMG.LY: kurulum yolu pinli değil (tetikleyici.md, Önceki notlar C).

## Önceki notlar

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
| coderabbit (coderabbitai/skills, resmi marketplace plugin) | CodeRabbit CLI girişi (`coderabbit auth`), hesap | coderabbit.ai | — | MIT, tur-4; skill'ler girişsiz çalışmaz, kurulmadı |
| mrdainami/kie-mcp (+ kie.ai) | KIE_API_KEY | kie.ai | — | MIT, tur-6; MCP + generate-anything skill anahtarsız çalışmaz, kurulmadı |
| composio-mcp (ComposioHQ/composio) | Composio API anahtarı / hesap | composio.dev | — | MIT, tur-6; hesaplı, kurulmadı |
| windsor.ai, TikTok/Whop/Skool/MediaSilo/Lumio/Vanta ve benzeri ticari servisler | hesap / API anahtarı | — | — | tur-6, skill yok; ayrıntı tur6-sonuc.tsv |
| fastn (fastn-ai/fastn-mcp) | fastn hesabı/anahtarı | fastn.ai | — | MIT, tur-6b-1; kurulmadı |
| Aiven (Aiven-Open/mcp-aiven) | Aiven token | aiven.io | — | Apache-2.0, tur-6b-1; kurulmadı |
| EnesCinr/twitter-mcp | X (Twitter) API anahtarları | developer.x.com | — | MIT, tur-6b-1; kurulmadı |
| DeepSeek API, Gemini API (generativelanguage), Virlo, Placid, Smithery, Jamf, agent.pw | hesap / API anahtarı | — | — | tur-6b-1; Gemini skill'leri kuruldu, anahtar ayrı; ayrıntı tur6b-1-sonuc.tsv |
| Figma-Context-MCP (glips), Fastn, Sentry MCP (mcp.sentry.dev), OpenRouter, Pushover | Figma API anahtarı / Fastn / Sentry / OpenRouter / Pushover hesabı | — | — | tur-6b-2; kurulmadı (OpenRouterTeam/skills lisanssız) |
