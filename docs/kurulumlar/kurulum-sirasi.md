# Kurulum sırası (kurulum turu 2)

Girdi `kurulum-turu-1.md`: KUR + KUR-duzeltmeli + HESAP = 103 repo. **A = 61 araç** (script) · **B = 42** (Ömer elle). Bu adımda hiçbir şey kurulmadı. `tools/kurulum-turu.sh --kuru` ile 68/68 adım (61 araç + 7 env) hatasız ayrıştı.

Tur-1 düzeltmeleri: 6 npm yolu registry'de yok (open-generative-ai, life-kernel, remotion-monorepo, @remotion/skills, omnivoice-studio-monorepo, godot-mcp→@coding-solo/godot-mcp). Bunlar skill kopyası, MCP ya da B'ye taşındı. `claude-usage` PyPI adı başka bir projeye ait (anderslatif), git+SHA ile kurulur. `lenis` ve `remotion` proje bağımlılığı olduğu için global kurulmaz.

## B-0: önce Ömer karar verir
- `everything-claude-code@everything-claude-code` kurulu (eski ad). `ecc@ecc` aynı repo (affaan-m); ikisi birlikte skill'leri çift sayar. Script'ten önce: `claude plugin uninstall everything-claude-code@everything-claude-code`.

## A grubu: `bash tools/kurulum-turu.sh` (Git Bash)
Script şu sırayla çalışır: env → plugin → skill kopyası → npm → uv → MCP. Her adımda zaten kurulu olan atlanır, kurulum yapılır, doğrulanır; hata çıkarsa o araç geri alınır, loglanır ve sonrakine geçilir. Log `.kos/kurulum-2/kurulum-turu.log` dosyasına, uninstall komutları `.kos/kurulum-2/geri-al.sh` dosyasına yazılır. Pinler script'in VERI bloğunda (tam SHA / ==sürüm / @sürüm).
- **E env (7, önce):** DO_NOT_TRACK=1, HYPERFRAMES_NO_TELEMETRY=1, CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=1, CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1, OMNIVOICE_ANALYTICS_DISABLED=1, PHONE_HARNESS_TELEMETRY=0, ECC_HOOK_PROFILE=minimal (`setx`).
- **P plugin marketplace (28, her marketin TÜM plugin'leri):** webcmd, tastemaker, garden-skills, fable-advisor, filetree, webgpu-threejs-tsl, gsap-skills, linkedin-agent, interfaces (jakubkrehel), obsidian, mattpocock, sepia, nyldn (octo, img), obsidian-cli, flightdeck, cc-arcade · düzeltmeliler: **ecc**, android-skills, chrome-devtools-mcp, marketingskills, daymade-skills, mindful-claude, hyperframes, logo-design, context-mode, last30days, **open-design**, **designer-skills**. Pin yöntemi: marketplace eklenir, `~/.claude/plugins/marketplaces/<m>` SHA'ya checkout edilir, sonra install yapılır.
- **S skill kopyası (23 → `~/.claude/skills/<klasör>`):** vibesec, cloudflare security-audit, coleam00 excalidraw-diagram, elayadesign, emilkowalski (14), eyaprak (6), llama.cpp (2), stop-slop, herdr (5), ibelick ui-skills (7), jsmastery (9), moli (3), magnitude (2), **mengto (176)**, prompt-master, robonuggets excalidraw, video-to-website, geo-optimizer, scrapling, unlazy, remotion skills (12), life-kernel (8), voicestudio (4). Mevcut klasörle ad çakışması olursa o skill atlanır ve `CAKISMA` loglanır (iki excalidraw skill'i olası). Kopyalananlar `.kos/kurulum-2/skill-kopya.tsv` dosyasına yazılır.
- **N npm (2):** `rea-agents@6.1.0 --ignore-scripts`, `codeburn@0.9.25`.
- **U uv (5):** `markitdown[all]==0.1.8`, `phone-harness==0.3.0`, `mimic-client==0.1.0`, `droidasc==0.1.1.post3` (son ikisinin PyPI eşleşmesi doğrulanmadı, kurulamazsa log), `claude-usage` @ git SHA 3eea154.
- **M MCP (3, user scope, stdio):** drizzle-docs (`drizzle-docs-mcp@3.0.2`), godot (`@coding-solo/godot-mcp@0.1.1`, Godot gerekir), unity (`anklebreaker-unity-mcp@2.36.0`, Unity editör gerekir; sağlık kontrolü Unity açık değilse düşebilir).

## Düzeltmeler (KUR-duzeltmeli)
- Script içinde: telemetri env'leri (yukarıda), `--ignore-scripts` (rea), ECC hook profili `minimal`, daymade için `install.sh --dangerously-skip-permissions` yerine plugin yolu.
- **Kurulumdan sonra elle:**
  - ecc: gürültülü hook'lar için `setx ECC_DISABLED_HOOKS "pre:bash:tmux-reminder,post:edit:typecheck"`.
  - context-mode: hook'lar (PreToolUse/PostToolUse/PreCompact) `~/.claude/plugins/cache/context-mode/context-mode/<sürüm>/hooks/hooks.json` dosyasında; çıktı sıkıştırma headroom ile çakışırsa plugin'i `claude plugin disable context-mode@context-mode` ile kapat.
  - mindful-claude: hook'ları çekirdek işlev; bir gün dene, rahatsız ederse disable et.
  - codeburn: telemetri opt-in, ayarlar arayüzünde kapalı kalsın; ilk çalıştırmada ağ çağrısını izle.
  - unlazy: `check-supervisor.mjs` klonda yoktu; kurulumdan sonra skill klasöründeki script'leri oku.
  - android-skills: `play_store_scraper.py` dosyasında `verify_ssl=False` ile çağırma.
  - geo-optimizer: web demoyu çalıştırma, yalnız CLI kullan.
  - last30days: X_BEARER_TOKEN / SCRAPECREATORS_API_KEY (B gibi).
  - open-design ve designer-skills: bağlam şişmesi aşağıdaki kısma bloğuyla çözülür.

## B grubu (Ömer, tek tek)
**Hesap/anahtar (23):** anahtarı al, `setx <ENV> <değer>` (değeri hiçbir komutla yazdırma), sonra satırdaki kurulumu çalıştır. Sürümler tur-1 tablosunda pinli.
- mirofish: LLM_API_KEY, ZEP_API_KEY (getzep.com).
- banana-claude: GEMINI_API_KEY (aistudio.google.com).
- size-limit: GITHUB_TOKEN (github.com/settings/tokens). Paket adı tur-1'de "None", README'den doğrula.
- mcp-gsc: Google Search Console OAuth (console.cloud.google.com).
- apify agent-skills ve apify-mcp-server: APIFY_TOKEN (console.apify.com → Integrations).
- composio: COMPOSIO_API_KEY (app.composio.dev, alpha sürüm).
- n8n-mcp: N8N_API_KEY (kendi n8n örneği → Settings → API).
- deepseek-harness: DeepSeek anahtarı (platform.deepseek.com, alpha).
- open-seo: DATAFORSEO_API_KEY (app.dataforseo.com).
- firecrawl cli ve firecrawl plugin (ikisi aynı "firecrawl" market adı, yalnız birini kur): FIRECRAWL_API_KEY (firecrawl.dev).
- googleworkspace/cli (95 skill): OAuth client (console.cloud.google.com), etkileşimli giriş.
- vibe-trading (91 skill): ALPHAVANTAGE_API_KEY, DEEPSEEK_API_KEY.
- hostinger: HOSTINGER_API_TOKEN (hPanel → API).
- claudecode-minimax-stack: MINIMAX_API_KEY / OPENROUTER_API_KEY.
- neon: NEON_API_KEY (console.neon.tech).
- codex-plugin-cc: `codex login` etkileşimli (OpenAI hesabı).
- scrapegraph: SGAI_API_KEY.
- serpapi: SERPAPI_API_KEY (serpapi.com).
- stripe-cli: `stripe login` etkileşimli.
- testsprite: TESTSPRITE_API_KEY.
- tiger-cli: TIGER_PUBLIC_KEY/SECRET (console.cloud.timescale.com).

**Elle/GUI/başvuru (19):**
- GUI eklentisi: BlenderKit eklentisi + blendkit (Blender → Add-ons; telemetri bayrağı yok, login olayı yollar), DaVinci Resolve MCP (Resolve açık olmalı).
- Kendi ortamını isteyenler: Thinking Orbs, OmniVoice (Python/GPU ortamı), OpenMontage (AGPL; DO_NOT_TRACK zaten script'te), colibri.
- Başka paket yöneticisi: pint (composer, PHP projesi), zoetrope (`cargo install zoetrope@0.2.0 --locked`).
- Function-hook "mods": claude-toons (api.anthropic.com çağırır, ek maliyet), davekiss/env, cache-tax (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` gerekir; marketler SHA pinsiz).
- Uzak MCP: git-mcp (uzak kullanımda repo adları gitmcp.io'ya gider; yerel çalıştır).
- Paket bulunamadı: excalidraw-mcp (npm paketi doğrulanamadı), open-generative-ai (npm'de yok).
- Proje bağımlılığı, global kurulmaz: lenis, remotion.
- Yalnız okuma (başvuru listesi): awesome-claude-code, awesome-design-md.

## Doğrulama ve geri alma
- Script her plugin'den sonra `claude plugin list`, her MCP'den sonra `claude mcp list` (Connected) kontrolü yapar. Sonda `claude doctor` çalışır (90 sn sınırlı, çıktı log'a).
- Hata çıkan araç otomatik geri alınır (`plugin uninstall` / `mcp remove` / `npm uninstall -g` / `uv tool uninstall` / skill klasörü silme) ve `ATLANDI-HATA` loglanır.
- Tümünü geri almak için: `bash .kos/kurulum-2/geri-al.sh` (ters sırada çalıştırmak için `tac` ile).

## Bağlam kısma (settings.json'a BU ADIMDA yazılmadı)
Şema CLI'dan doğrulandı: `skillOverrides: { "<skill-adı>": "on" | "name-only" | "user-invocable-only" | "off" }`. `off` skill'i tümüyle engeller ("Remove the override to run it"), bu yüzden kullanılmaz. **`user-invocable-only`** skill'i model listesinden çıkarır, `/ad` ile çağrılınca yükler; Ömer kararına uyan değer bu.
1. **Ölçüm 0 (kurulumdan önce):** PowerShell'den `claude -p "/context"` çalıştır, skill satırının jetonunu not et.
2. **Kurulum.** Ardından her dev paket için `claude plugin details <p>@<m>` ile tahmini jeton maliyetini ölç, `claude -p "/context"` ile ölçüm 1'i al.
3. **Blok üret:** `bash tools/kurulum-turu.sh --blok > .kos/kurulum-2/overrides.json` komutu kurulu cache'ten gerçek skill adlarını okur ve şu paketleri kapsar: ecc, open-design, daymade-skills, designer-skills, marketingskills, hyperframes, android-skills, mattpocock plugin'leri ve mengto skill kopyaları. Anahtar biçimi plugin skill'lerinde `plugin:skill`, kopyalarda klasör adı. İlk anahtarı `/skills` listesiyle karşılaştır.
4. **Uygula (ayrı adım, Ömer onayıyla):** bloğu `~/.claude/settings.json` içine birleştir. PowerShell 5.1'de `ConvertTo-Json -Depth 100` kullan. `claude -p "/context"` ile ölçüm 2'yi al.
5. **Açma turu (1 hafta sonra):** transcript'lerden `/skill` çağrı sayılarını çıkar. ≥3 kez çağrılan skill'leri `on` yap. Model tarafından keşfi gereken ama açıklaması uzun olanları `name-only` yap.

Klon SKILL.md sayımına göre kapalı başlayacak skill sayısı ≈1994 (üst sınır; ecc 1027 sayısı çeviri kopyalarını da içerebilir). A grubunun toplamı 2153 skill, tüm adaylarınki 2634.
