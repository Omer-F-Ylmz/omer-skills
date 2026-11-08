"""KATEGORI-1: elimizdeki her kalemi 23+1 sabit kategoriye ayırır (deterministik kural + önbellekli ücretsiz model).
CLI: python tools/kategori_sinifla.py [--yeniden] [--llm N] [--ornek]
  topla -> .kos/kopru/kategori/ogeler.jsonl (tekilleştirilmiş); sınıfla -> docs/envanter/kategori.tsv; özet -> kategori-ozet.md
  --llm N: belirsiz kalemler için en çok N ücretsiz-model çağrısı (önbellek .kos/kopru/kategori/llm.json, artan)
  --ornek: denetim için katmanlı örnek (kategori başına >=10) .kos/kopru/kategori/ornek.tsv
Env değeri okunmaz/yazılmaz; ~/.claude.json'dan yalnız mcpServers ANAHTAR adları alınır."""
import csv, json, os, re, sys, glob, random, collections
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

KOK = Path(__file__).resolve().parents[1]
ARA = KOK / ".kos/kopru/kategori"
CIKTI = KOK / "docs/envanter/kategori.tsv"
OZET = KOK / "docs/envanter/kategori-ozet.md"
csv.field_size_limit(10**9)

KATEGORILER = ["arastirma", "backend-dotnet", "backend-genel", "belge", "bilim", "bulut-devops", "frontend-ui", "git-yayin", "gorsel", "guvenlik",
               "inceleme", "is-finans-hukuk", "ml-ai", "mobil", "oyun", "pazarlama-reklam", "surec-plan", "test-qa", "veri-db",
               "verimlilik", "video", "3d-blender", "ajan-arac", "diger-genel"]

# ---- kural tabloları: kategori -> (güçlü=3, orta=2, zayıf=1) ASCII-katlanmış regex ----
R = {
 "arastirma": (r"research|literature|arxiv|scholar|citation|academic|\bpapers?\b|arastir|osint|fact.?check|wikipedia|systematic.review|notebooklm|perplexity|tavily|\bexa\b|firecrawl|web.?search|crawl|scrap(?:e|ing|er)|bright.?data|apify|pubmed|bibliograph|zotero|deep.?research|ders.?bankasi|find.?docs|docs.?search|documentation.lookup|context7",
               r"investigat|discover|knowledge.?base|wiki|market.?intel|trend|lookup|retriev|summariz|transcript|reddit|hacker.?news|\bnews\b|reader|ogren|kutuphane|kaynak|inceleme.?notu|learn|study|tutorial|egitim|ders",
               r"search|explor|insight|source|\bdocs?\b"),
 "backend-dotnet": (r"dotnet|\.net|c#|csharp|asp\.?net|entity.?framework|ef.?core|msbuild|nuget|blazor|xunit|nunit|mstest|linq|wpf|maui|signalr|razor",
                  r"minimal.?api|cs.?proj|sln|visual.?studio|unity.?cs",
                  r"net"),
 "backend-genel": (r"dotnet|\.net\b|\bc#|csharp|asp\.?net|entity.?framework|ef.?core|msbuild|nuget|blazor|backend|nestjs|fastapi|django|laravel|spring.?boot|express\.?js|graphql|microservice|grpc|rest.?api|golang|\bgo\b.*(?:pro|patterns)|rust.?(?:pro|patterns|async)|java.?(?:pro|coding)|kotlin|python.?(?:pro|patterns)|ruby|php|scala|elixir|haskell|\bnode(?:js)?\b.*backend|server.?side|api.?design|openapi|swagger|orm\b|hexagonal|ddd|domain.?driven|cqrs|event.?sourc|saga|sdk.?(?:dev|build)",
                  r"\bapi\b|endpoint|rest\b|server|middleware|authentication|oauth|jwt|webhook|queue|bullmq|celery|worker|python|typescript|javascript|node|bun\b|deno|\bc\+\+|cpp|rust|\bjava\b",
                  r"library|package|module|framework|\bcode\b"),
 "belge": (r"\bpdf\b|docx?\b|pptx?\b|xlsx?\b|\bword\b|excel|powerpoint|spreadsheet|slide|presentation|\bdeck\b|latex|\bocr\b|markitdown|document|belge|markdown|resume|\bcv\b|invoice.?draft|poster|report.?(?:writer|builder|generat)|proposal|memo|essay|manuscript|ebook|epub|handbook|readme|changelog.?writ",
         r"write|writing|writer|yaz|report|rapor|template|sablon|convert|format|notion|docs\b|docusign|google.?docs|sheets|libreoffice|office|carousel|infographic|article|blog|newsletter|copy.?edit|humaniz|prose",
         r"text|content|note"),
 "bilim": (r"scientific|science|\bbio(?:logy|info|rxiv|python|pharma|medic|conductor|service)|chem(?:istry|bl|oinf)|genom|protein|rdkit|physics|astro|quantum|neuro|molecul|clinical|medical|pharma|drug|alphafold|pubchem|\blab\b|laborator|mathemat|\bmath\b|sympy|statsmodel|astropy|qiskit|pennylane|cirq|dna|rna|cell|single.?cell|scanpy|anndata|healthcare|\bfda\b|trial|patient|epidem|ecolog|climate|geo(?:spatial|pandas|logy)|materials.?science|pymatgen|fluid|simulation.?science|biyoloji|fizik|kimya|tip\b|bilim",
          r"statistic|research.?method|experiment|hypothes|peer.?review|reproducib|dataset.?science|scikit.?(?:bio|survival)|imaging|microscop|sequenc|phylogen|pathway|enzyme|ligand|toxic|nutrition|fitness|wearable|medicine|surgery|hospital|nurs|therap",
          r"model|analysis|simulat"),
 "bulut-devops": (r"\baws\b|azure|\bgcp\b|google.?cloud|cloudflare|terraform|kubernetes|\bk8s\b|docker|helm|ci.?cd|github.?actions|deploy|vercel|netlify|railway|\brender\b|devops|serverless|lambda|observab|monitoring|\bsre\b|ansible|infrastructure|pulumi|nginx|hosting|hostinger|fly\.io|cloud.?run|datadog|grafana|prometheus|sentry|signoz|honeycomb|incident|runbook|on.?call|pagerduty|cdn|dns|tunnel|vps|ssh\b|systemd|linux.?admin|sysadmin|homelab|vpn|wireguard|network.?(?:config|engineer)|buildkite|circleci|jenkins|gitlab.?ci|istio|service.?mesh|bazel|nix|flox|depot|ubicloud|daytona|e2b|sandbox|bulut",
               r"cloud|container|pipeline|build|release.?pipeline|environment|\benv\b|secret|vault|iam\b|cost.?(?:optim|analys)|scal(?:e|ing)|queue|storage|bucket|backup|server|cron|schedule|uptime|health.?check|log(?:s|ging)\b|trace|tracing|otel|opentelemetry|metrics",
               r"ops|infra|platform"),
 "frontend-ui": (r"frontend|front.?end|\bui\b|\bux\b|react|\bvue\b|angular|svelte|next\.?js|nuxt|tailwind|\bcss\b|\bhtml\b|design.?system|component|shadcn|figma|gsap|framer|landing.?page|web.?design|typograph|layout|accessib|\ba11y\b|wcag|responsive|interface|scroll|animation|animate|motion|hover|glass|gradient|navbar|hero|sidebar|dashboard.?ui|storybook|radix|mui\b|bootstrap|astro\b|vite|webpack|pwa|web.?app|website|web.?sit|site.?(?:kit|build)|tasarim|arayuz|theme|palette|spacing|icon|font|brutalis|skeuomorph|aesthetic|slop|craft|impeccable|taste|awwwards|lenis|aos\b|parallax|three\.?js.*(?:landing|site)|interaction|micro.?interaction|empty.?state|onboarding.?ui|form.?design|usability|visual.?(?:hierarchy|design)|dark.?mode|webflow|framer|wix|squarespace|elementor|wordpress.?theme",
                r"design|web\b|page|browser|style|styling|color|colour|visual|prototype|wireframe|mockup|template|canvas|svg|lottie|pixel|screen|mobile.?first|dom\b|javascript|typescript|jsx|tsx|\bjs\b|\bts\b",
                r"look|feel|brand|beautiful|better"),
 "git-yayin": (r"\bgit\b|gitlab|pull.?request|\bpr\b|commit|branch|changelog|npm.?publish|merge|worktree|semantic.?release|versioning|version.?bump|rebase|cherry.?pick|\bfork\b|repo.?(?:prep|setup|scan)|git.?(?:hub|safety)|stack(?:ed|ing).?pr|yayin|dagit|pypi|distribution|marketplace.?publish|app.?store.?submit|launch.?(?:checklist|strategy)|production.?release|tag\b",
              r"github|release|publish|\bgh\b|\bship\b|issue|code.?owner",
              r"repo|repository|contribut|open.?source|license|readme|upstream|clone|version|push|pull"),
 "gorsel": (r"image|picture|photo|logo|illustrat|\bicon|poster|banner|thumbnail|midjourney|\bflux\b|stable.?diffusion|dall.?e|gpt.?image|imagen|nano.?banana|upscal|retouch|ideogram|graphic|infographic|mockup|comfyui|gorsel|resim|foto|background.?remov|style.?transfer|diffusion|leonardo|recraft|firefly|seedream|stability|sdxl|lora\b|inpaint|outpaint|portrait|character.?sheet|concept.?art|moodboard|mood.?board|visual.?asset|asset.?image|unsplash|stock.?image|meme|sticker|avatar.?image|pixel.?art|cover.?image|og.?image|screenshot|diagram|drawio|excalidraw|mermaid|figure",
            r"design|art\b|draw|paint|sketch|visual|color|palette|canvas|svg|render|generat|prompt|style|creative|brand.?(?:kit|asset)|photoshop|illustrator|canva|figma|gimp|inkscape|krita",
            r"look|aesthetic|beautiful"),
 "guvenlik": (r"secur|pentest|penetration|vulnerab|exploit|\bcve\b|owasp|\bxss\b|sqli|sql.?injection|injection|malware|reverse.?engineer|forensic|red.?team|blue.?team|purple.?team|offensive|threat|\bsoc\b|siem|crypto(?:graph|analysis)|bug.?bounty|\bctf\b|secrets?.?(?:scan|manag|rotat)|gitleaks|semgrep|\bsast\b|\bdast\b|firewall|zero.?trust|encrypt|phishing|ransomware|wifi.?(?:attack|hack)|burp|nmap|metasploit|binary.?analys|guvenlik|saldiri|hack(?:ing|er|ers)\b|ssrf|csrf|idor|privilege.?escal|active.?directory|kerberos|jwt.?attack|auth.?bypass|hardening|compliance.?(?:check|audit)|gdpr|hipaa|soc2|iso.?27001|pci|authn|iam\b|mfa|sandbox.?escape|fuzz|decompil|disassembl|ghidra|ida\b|radare|frida|apk.?reverse|trufflehog|snyk|trivy|strix|zeroleaks|shield|guard(?:rail)?|prompt.?injection|jailbreak|obliterat|uncensor|sansursuz|abliterat|\bwaf\b|ddos|honeypot|deception|incident.?respon|dfir|memory.?forensic|yara|sigma\b|mitre|attack.?(?:tree|chain)|stride",
               r"audit|risk|privacy|kvkk|policy|permission|credential|password|token.?leak|safe(?:ty)?|sanitiz|validat.?input|trust|verify.?identity|certificate|tls|ssl|ssh\b|vpn",
               r"protect|detect|scan"),
 "inceleme": (r"review|critique|audit|code.?review|inspect|teardown|incele|site.?inceleme|assess|evaluat(?:e|ion).?(?:site|design|code)|lint|static.?analys|code.?quality|tech.?debt|smell|refactor.?review|design.?review|ux.?review|heuristic|second.?opinion|ikinci.?gorus|grader|rubric|judge|hakem|peer.?review|walkthrough|postmortem|retrospective|health.?check|diagnos|troubleshoot|root.?cause|analy[sz]e",
              r"quality|feedback|compare|comparison|benchmark|verify|check|score|rating|rate\b|grade|polish|critic|red.?flag|slop",
              r"look|assess"),
 "is-finans-hukuk": (r"financ|accounting|invoice|\btax\b|legal|contract|\blaw\b|compliance|trading|\bstock|invest|portfolio|banking|payroll|\bhr\b|human.?resources|recruit|hiring|\bsales\b|\bcrm\b|business.?plan|startup|valuation|\bdcf\b|budget|\bcfo\b|procurement|supply.?chain|logistic|real.?estate|insurance|\bsec\b.?filing|earnings|market.?(?:data|analysis|breadth)|polymarket|defi\b|kalshi|crypto|bitcoin|ethereum|solana|hyperliquid|forex|options|futures|equity|bond|fund\b|quickbooks|xero|stripe|billing|revenue|pricing.?model|p&l|ledger|reconcil|audit.?support|sox|gdpr|nda\b|saas.?msa|agreement|clause|attorney|lawyer|counsel|court|patent|trademark|ihale|borsa|vergi|fatura|muhasebe|teklif|hukuk|finans|kripto|yatirim|backtest|trader|brokerage|hedge|macro|commodit|etf\b|dividend|ipo\b|m&a|merger|due.?diligence|lbo|cap.?table|carta|venture|investor|fundrais|pitch.?deck|unit.?economics|kpi|okr|erp|netsuite|salesforce|hubspot|pipedrive|zoho|odoo|sap\b|customer.?success|support.?ticket|helpdesk|zendesk|freshdesk|intercom|inventory|warehouse|ecommerce.?ops|shopify|dropship|amazon.?seller|etsy|marketplace.?seller|operations|\bops\b|vendor|expense|treasury|cash.?flow|forecast",
                     r"business|company|enterprise|customer|client|deal|lead|pipeline|quote|order|payment|paypal|wise\b|plaid|bank|loan|credit|debt|asset|money|price|cost|profit|margin|commerce|retail|store|shop|product.?manage|pm\b|stakeholder|strategy|founder|\bceo\b|executive",
                     r"market|team|office"),
 "ml-ai": (r"machine.?learning|\bml\b|\bllm|model.?(?:training|serving|eval)|fine.?tun|pytorch|tensorflow|transformers?\b|hugging.?face|\brag\b|embedding|vector.?(?:db|database|search|store)|prompt.?engineer|langchain|llamaindex|dspy|inference|vllm|quantiz|diffusion.?model|neural|\bnlp\b|computer.?vision|mlops|deep.?learning|reinforcement|\brl\b|grpo|lora|peft|unsloth|axolotl|gguf|ollama|llama\.?cpp|onnx|tensorrt|cuda|\bgpu\b|nemo|megatron|deepspeed|fsdp|accelerate|wandb|weights.?and.?biases|mlflow|tensorboard|openai|anthropic|gemini|claude.?api|gpt|mistral|qwen|deepseek|kimi|grok|whisper|\basr\b|\btts\b|speech.?(?:recog|synth)|voice.?clon|text.?to.?speech|speech.?to.?text|openrouter|omniroute|groq|sambanova|nvidia|nim\b|ai.?(?:model|sdk|engineer|product|safety|alignment|ethic)|alignment|guardrail|hallucinat|llm.?eval|benchmark.?model|model.?(?:router|routing|bakeoff|showdown)|agentic.?(?:eval)|eval.?harness|evals?\b|scikit|sklearn|xgboost|automl|datarobot|knowledge.?distill|model.?merg|pruning|moe\b|speculative|long.?context|tokeniz|sentencepiece|chroma\b|faiss|pinecone|qdrant|weaviate|milvus|cohere|replicate|together.?ai|fireworks|sglang|triton|ray\b|modal\b|runpod|lambda.?labs|skypilot|vertex.?ai|bedrock|sagemaker|foundry|ai.?foundry|copilot.?sdk|zapier.?ai|ai.?agent.?(?:train)|yapay.?zeka|makine.?ogren",
          r"\bai\b|artificial|intelligence|model|training|dataset|predict|classif|cluster|regress|generat(?:ive|ion)|prompt|agent.?framework|multimodal|vision|speech|audio.?model|openai|llm|chat.?bot|chatbot|assistant|copilot",
          r"smart|auto|learning"),
 "mobil": (r"android|\bios\b|swift(?:ui)?|kotlin|flutter|react.?native|expo\b|mobile|mobil|app.?store|xcode|jetpack|play.?store|watchos|ipados|visionos|objective.?c|cocoapods|gradle|capacitor|ionic|nativescript|maui|xamarin|testflight|apk\b|ipa\b|cordova|\beas\b|hig\b|human.?interface|wearos|android.?studio|compose.?multiplatform|kmp\b|swiftdata|app.?clip|widgetkit|healthkit|arkit|storekit",
          r"app\b|device|phone|tablet|touch|gesture|push.?notif|haptic|native",
          r"screen|ui"),
 "oyun": (r"\bgame|gaming|unity\b|unreal|godot|gamedev|level.?design|roblox|minecraft|pygame|phaser|oyun|gmod|shader|npc\b|rpg\b|fps\b|sprite|tilemap|matchmak|steam\b|mod.?(?:any|kit|ding|der)|modder|bukkit|spigot|fabric.?mod|forge.?mod|blockbench|aseprite|pixel.?art.?game|game.?(?:audio|art|design|dev|jam)|combat|quest|inventory.?system|loot|boss|enemy|vfx.?game|game.?vfx|bevy|love2d|raylib|defold|gamemaker|construct\b|rpg.?maker|twine|ink\b|narrative.?design|speedrun|esport|playable",
          r"player|score|level\b|quest|world|physics|character|animation.?system|ecs\b|engine|simulation|puzzle|arcade|casino|poker|chess",
          r"fun|play"),
 "pazarlama-reklam": (r"marketing|\bseo\b|\bads?\b|advertis|campaign|copywrit|social.?media|instagram|linkedin|tiktok|youtube.?(?:strategy|seo|growth)|content.?(?:calendar|strategy|marketing|plan)|email.?(?:marketing|sequence|campaign)|newsletter|\bbrand|growth|funnel|\bcro\b|landing.?page.?copy|influencer|affiliate|\bgeo\b.*(?:ai|search|citation)|audience|persona|hook|viral|reklam|pazarlama|\bugc\b|lead.?gen|outreach|cold.?(?:email|outreach)|social.?(?:post|content|listening|proof)|positioning|go.?to.?market|\bgtm\b|launch.?(?:plan|playbook)|pricing.?strategy|referral|retention|churn|a.?b.?test|ab.?test|conversion|utm|analytics.?(?:marketing)|google.?ads|meta.?ads|facebook.?ads|paid.?(?:ads|social|media)|ppc|sem\b|keyword|backlink|serp|sitemap|schema.?markup|programmatic.?seo|blog.?(?:write|strategy|seo)|thread|tweet|\bx\.com|twitter|reddit.?(?:marketing)|community.?(?:build|marketing)|pr\b.?(?:release|outreach)|press|public.?relations|sponsorship|creator|collab|ambassador|reel|shorts.?(?:strategy)|carousel|caption|hashtag|engagement|followers|monetiz|dropshipping|ecommerce.?(?:seo|marketing)|product.?(?:hunt|launch)|app.?store.?optim|\baso\b|brand.?(?:voice|guideline|identity)|tone.?of.?voice|storytelling|headline|cta\b|offer|lead.?magnet|webinar|event.?marketing|trade.?show|sms.?marketing|push.?marketing|crm.?marketing|loyalty|coupon|promo",
                      r"content|post\b|publish|social|audience|customer|brand|market|sales|promo|traffic|rank|visibility|reach|impression|click|ctr\b|roas|cpa|cpc|cpm|attribution|pixel|tracking|tag.?manager|gtm\b|analytics|ga4|seo|digital|online|web.?presence|storefront|engage",
                      r"write|copy|growth|launch"),
 "surec-plan": (r"\bplan(?:ning|ner)?\b|roadmap|project.?manag|\btask|todo|\bspec\b|\bprd\b|requirement|brainstorm|workflow|agile|sprint|scrum|kanban|estimat|decision|\badr\b|retrospective|milestone|plan.?kur|karar|gorev|\bokr\b|strateg|process|protocol|prioriti|backlog|epic|story|ticket|issue.?(?:triage|track)|linear|jira|asana|trello|monday|clickup|notion.?(?:plan|task)|basecamp|gantt|timeline|schedule|deadline|standup|retro\b|kickoff|checklist|runbook|playbook|sop\b|handoff|delegat|coordinat|orchestrat.?(?:plan)|think|reasoning|grill|interview.?me|clarif|scope|scoping|breakdown|decompos|blueprint|architecture.?(?:decision|plan)|design.?doc|rfc\b|proposal|charter|governance|raci|capacity|resourc.?plan|program.?(?:plan|manag)|portfolio.?manag|delivery|execution|goal|okr|habit|routine|weekly|daily.?(?:plan|brief|review)|morning|review.?cycle|operating.?(?:rhythm|cadence)|cadence|ritual|istek|yol.?haritasi|plan.?yaz|surec",
                r"organiz|structure|framework|method|approach|guideline|principle|rule|standard|convention|best.?practice|template|ceremony|meeting|agenda|notes?\b|minutes|summary|brief\b|report|status|update|progress|track|manage|lead|team|stakeholder|align|decide|choose|select|option|trade.?off|compare|evaluate|prioritize",
                r"work|flow|step|stage|phase"),
 "test-qa": (r"\btest|testing|\btdd\b|\bqa\b|\be2e\b|playwright|cypress|jest|vitest|pytest|coverage|mutation|regression|unit.?test|integration.?test|benchmark|flaky|fixture|quality.?assurance|verif|dogrula|selenium|load.?test|k6\b|puppeteer|webdriver|appium|detox|maestro|storybook.?test|snapshot|visual.?regress|chromatic|percy|a11y.?test|accessibility.?test|smoke|sanity.?check|acceptance|bdd|cucumber|gherkin|mock|stub|spy|assert|expect|spec.?test|contract.?test|pact|fuzz|chaos|soak|stress|perf.?test|lighthouse|web.?vitals|core.?web|synthetic|monitor.?test|canary|test.?plan|test.?case|test.?data|test.?env|test.?run|test.?report|test.?suite|test.?audit|ci.?test|red.?green|refactor.?test|characteriz|golden|approval.?test|property.?based|hypothesis.?test|quickcheck|fast.?check|jasmine|mocha|karma|ava\b|tap\b|rspec|junit|testng|nunit|xunit|mstest|testcontainers|wiremock|msw\b|nock|supertest|postman|newman|insomnia|bruno|hoppscotch|soapui|jmeter|gatling|locust|artillery|vegeta|wrk\b|ab\b|siege|autocannon|bombardier|hey\b|tsung|taurus|blazemeter|loadrunner|neoload|silk|tricentis|testim|mabl|functionize|katalon|ranorex|testcomplete|squish|robot.?framework|behave|lettuce|specflow|reqnroll|serenity|gauge|fitnesse|concordion|jbehave|yatspec|spock|kotest|scalatest|specs2|munit|utest|zio.?test|hedgehog|scalacheck|proptest|rapid|gopter|quickcheck",
             r"check|validat|assert|ensure|guarantee|confirm|prove|demonstrate|evidence|reproduc|bug|defect|issue|fix|debug|diagnos|trace|log|monitor|alert|incident|failure|error|exception|crash|hang|leak|race|deadlock|timeout|retry|flak",
             r"quality|reliab|stab|robust"),
 "veri-db": (r"database|\bdb\b|\bsql\b|postgres|mysql|sqlite|mongo|redis|supabase|prisma|\borm\b|drizzle|migration|data.?engineer|\betl\b|\belt\b|pandas|polars|\bdbt\b|warehouse|bigquery|snowflake|clickhouse|analytics|dashboard|data.?analy|data.?scien|\bcsv\b|jupyter|notebook|vector.?database|schema|nosql|veri.?(?:tabani|analiz)|dynamodb|cassandra|neo4j|graph.?db|cockroach|planetscale|neon\b|turso|d1\b|firestore|firebase|convex|pocketbase|appwrite|hasura|airtable|baserow|nocodb|metabase|superset|redash|looker|tableau|power.?bi|grafana.?dash|duckdb|parquet|arrow|spark|hadoop|kafka|airflow|dagster|prefect|dlt\b|fivetran|airbyte|segment|rudderstack|mixpanel|amplitude|posthog|plausible|umami|matomo|pendo|heap|fullstory|hotjar|clarity|datadog.?rum|elastic|opensearch|solr|meilisearch|typesense|algolia|lucene|index|query|queries|olap|oltp|data.?model|dimension|fact.?table|star.?schema|data.?vault|lakehouse|delta.?lake|iceberg|hudi|trino|presto|athena|redshift|synapse|databricks|fabric|qdrant|pinecone|chroma|weaviate|milvus|lancedb|pgvector|faiss|annoy|hnsw|data.?quality|great.?expectations|soda\b|monte.?carlo|data.?catalog|lineage|governance|mdm\b|data.?mesh|data.?contract|schema.?registry|avro|protobuf|json.?schema|data.?(?:viz|visual)|chart|plot|matplotlib|seaborn|plotly|d3\b|echarts|highcharts|visx|recharts|nivo|bokeh|altair|vega|observable|streamlit|dash\b|gradio|panel|voila|shiny|marimo|hex\b|deepnote|colab|kaggle|statistic|eda\b|exploratory|feature.?engineer|time.?series|forecast|etl|pipeline.?data|data.?pipeline",
            r"data|table|column|row|record|store|storage|cache|index|search|report|metric|kpi|insight|trend|aggregate|group|join|filter|sort|export|import|sync|replicat|backup|restore|snapshot",
            r"info|stat|number"),
 "verimlilik": (r"token|context|memory|compress|caveman|\bcost\b|\brtk\b|headroom|efficien|productiv|second.?brain|obsidian|\bnotes?\b|session|handoff|cache|saving|budget|hafiza|bellek|baglam|context.?mode|claude.?mem|compact|focus|habit|calendar|inbox|triage|email.?(?:triage|manage)|time.?track|pomodoro|journal|diary|reflect|knowledge.?manage|pkm\b|zettelkasten|roam|logseq|notion|evernote|onenote|bear\b|apple.?notes|reminders?|todoist|ticktick|things\b|omnifocus|remember|forget|recall|continuous.?learning|self.?improv|learn.?from|lesson|ders\b|dersler|ogren|kart\b|beyin|brain|mind\b|thinking.?partner|rubber.?duck|clarity|declutter|organiz|clean.?up|file.?organiz|storage.?clean|disk|ram\b|cpu\b|speed.?up|faster|optimi[sz]e.?(?:context|token|prompt)|prompt.?(?:cache|caching|compress)|lean|slim|diet|trim|prune|dedupe|dedup|compaction|summariz.?(?:session|conversation)|resume|restore|checkpoint|save.?session|session.?(?:save|restore|handoff|history)|history|recap|standup|daily|weekly|digest|briefing|morning|end.?of.?day|retro|reflection|review.?(?:week|day)|time.?block|deep.?work|flow.?state|distraction|attention|energy|burnout|wellbeing|mindful|meditat|sleep|routine|ritual|automation.?(?:personal)|shortcut|alias|snippet|clipboard|launcher|raycast|alfred|keyboard|hotkey|macro|autohotkey|window.?manage|tiling|terminal|shell.?(?:config|alias)|dotfiles|zsh|tmux|vim|neovim|emacs|vscode.?(?:setting|ext)|ide.?(?:config|setting)|statusline|status.?line|prompt.?(?:theme)|starship|p10k|oh.?my",
                r"personal|assistant|helper|utility|tool\b|tools\b|manage|organiz|track|log\b|list\b|queue|reading|bookmark|archive|inbox|capture|clip|highlight|annotation|flashcard|spaced|anki|memento|study|learn|revision|exam|quiz|course|class|lecture|teach|tutor|coach|mentor|guide",
                r"smart|easy|simple|quick|fast"),
 "video": (r"video|ffmpeg|remotion|editing|premiere|davinci|motion.?graphics|subtitle|caption|youtube|reel|shorts|audio|music|voice|\btts\b|speech|podcast|sound|whisper|lip.?sync|avatar|hyperframes|manim|lottie|after.?effects|\bclip|trailer|altyazi|\bses\b|film|cinema|cinematic|movie|animation|animat|storyboard|b.?roll|footage|montage|cut\b|trim|render|export.?video|transcod|encode|codec|h264|h265|hevc|vp9|av1|webm|mp4|mov\b|gif|stream|obs\b|livestream|twitch|screen.?record|loom|demo.?video|explainer|tutorial.?video|vlog|documentary|short.?form|tiktok.?video|seedance|sora|veo\b|kling|runway|pika|luma|hailuo|minimax|wan\b|ltx|hunyuan.?video|cogvideo|mochi|genmo|higgsfield|heygen|synthesia|d.?id|tavus|hedra|elevenlabs|suno|udio|lyria|stable.?audio|audiocraft|musicgen|bark\b|tortoise|xtts|coqui|piper|kokoro|chatterbox|resemble|descript|riverside|audacity|reaper|ableton|logic.?pro|fl.?studio|garageband|musescore|lilypond|midi|synth|daw\b|mix(?:ing)?|master(?:ing)?|foley|sfx|dubbing|voiceover|narrat|audiobook|karaoke|lyrics|songwrit|beat\b|bpm|stem|isolate.?vocal|demucs|spleeter|openunmix|voice.?(?:clon|conver|design|agent|chang)|rvc\b|so.?vits|bark|parler|styletts|orpheus|dia\b|sesame|cartesia|deepgram|assembly.?ai|speechmatics|rev\.?ai|otter|fireflies|transcri|diariz|pyannote|wav2vec|nemo.?asr|riva|vosk|kaldi|deepspeech|wenet|espnet|speechbrain",
           r"media|visual|motion|clip|scene|shot|frame|fps|resolution|duration|timeline|sequence|track|layer|effect|transition|filter|overlay|title|credit|intro|outro|thumbnail|cover|channel|creator|viral|hook|retention|watch.?time",
           r"play|record|stream"),
 "3d-blender": (r"blender|\b3d\b|three\.?js|webgl|gltf|\bglb\b|mesh|\bcad\b|freecad|modeling|rigging|sculpt|texture|\bpbr\b|render|\busd\b|point.?cloud|photogrammetry|3d.?print|openscad|solidworks|fusion.?360|onshape|autocad|rhino|grasshopper|maya\b|houdini|cinema.?4d|zbrush|substance|marmoset|keyshot|vray|cycles|eevee|arnold|redshift|octane|unreal.?(?:engine|mcp)|geometry.?nodes|shader.?(?:graph|node)|hdri|lighting.?rig|uv\b|retopo|bake|baking|normal.?map|displacement|bump|subsurface|volumetric|particle|fluid.?sim|cloth.?sim|rigid.?body|soft.?body|physics.?sim|armature|skeleton|bone|weight.?paint|shape.?key|morph|blendshape|facial|mocap|motion.?capture|retarget|animation.?clip|fbx|obj\b|stl\b|step\b|iges|dxf|dwg|svg.?3d|r3f|react.?three|drei|babylon|playcanvas|aframe|cesium|deck\.?gl|kepler|globe|orbit|isometric|low.?poly|voxel|magicavoxel|nerf|gaussian.?splat|splat|neural.?radiance|colmap|meshroom|realitycapture|polycam|luma.?ai|scaniverse|tripo|meshy|rodin|hunyuan3d|trellis|instantmesh|zero123|dreamfusion|shap.?e|point.?e|get3d|nvdiffrec|text.?to.?3d|image.?to.?3d|bambu|slicer|gcode|dfm|dfam|urdf|sdf\b|srdf|robot.?model|kinemat|ik\b",
               r"model|object|scene|camera|light|material|animation|character|asset|environment|landscape|terrain|water|cloud|sky|fire|smoke|vfx|fx\b|simulation|procedural",
               r"design|art|visual"),
 "ajan-arac": (r"\bmcp\b|mcp.?server|agent|subagent|orchestrat|\bcli\b|\btool|plugin|skill.?(?:creator|builder|author|install|manage|hub|market)|harness|\bhook|claude.?code|codex|automation|n8n|zapier|\bmake\.com|browser.?(?:use|automation|agent)|computer.?use|\bsdk\b|api.?integration|integrat|connector|baglayici|gateway|proxy|router|routing|mcptoon|toolbox|cc.?kopru|kopru|bridge|slash.?command|command.?(?:creator|dev)|ralph|loop\b|swarm|crew|autogen|langgraph|autogpt|babyagi|openhands|aider|cline|cursor|windsurf|continue\.dev|copilot|gemini.?cli|opencode|openclaw|hermes|paperclip|pi.?agent|a2a|acp\b|mcp.?(?:app|ui)|desktop.?commander|filesystem|shell|terminal|tmux|herdr|conductor|taskmaster|fleet|dispatch|delegat|parallel.?agent|multi.?agent|agent.?(?:team|swarm|ops|harness|memory|eval|sdk)|ruflo|autoharness|replica|\bea\b|everything.?claude|claude.?(?:flow|squad|mem|hud)|oh.?my|ecc\b",
               r"workflow|pipeline|runner|executor|scheduler|cron|daemon|service|server|client|adapter|wrapper|bridge|plugin|extension|addon|module|package|library|framework|platform|infra|setup|install|config|configure|manage|admin|ops|control|remote|local|cloud|api\b|rest\b|webhook|trigger|event|queue|message|bus|stream|sync|connect",
               r"auto|smart|helper|utility"),
}

# etiket/ozet gürültü sözcükleri (tür/kaynak işaretleri; kategori sinyali değil)
GURULTU = re.compile(r"\b(?:by|alintida|alintiya|alnt\w*|yalniz|yalnz|adi|geciyor|geiyor|gore|envanterde|eslesme|eleme|bulunamadi|belirsiz|dizininde|cagri|var|k\d+|yapilis|ozellik|katalog|skill.?dizini|skill|ana.?liste|kurulmadi.?sirada|kayitsiz|kurulu.?kanitsiz|kurulu|obsidian.?\w*|video|yontem|betik|kopru|site.?ucretsiz|dizinde|yok|liste|arac|varlik|2\.?beyin|ders.?\w*|kart.?\w*|http|https|www|com|org|net|io)\b")

CY = {  # çok-yönlü araç adları (NİHAİ 0 listesi) -> ad+yol+etiket üzerinde aranır
 "REA": r"(?<![a-z0-9])rea(?![a-z0-9])|reverse-engineer-anything|leanrea|token-rea",
 "replica": r"replica",
 "ECC": r"(?<![a-z0-9])ecc(?![a-z0-9])|everything-claude-code|elainesmithburkel-code",
 "claude-code-setup": r"claude-code-setup|claude-automation-recommender",
 "Headroom": r"headroom",
 "RTK": r"(?<![a-z0-9])rtk(?![a-z0-9])",
 "context-mode": r"context-mode|(?:^|[:/ ])ctx-(?:search|index|stats|doctor|upgrade|purge|insight|batch|execute|fetch)",
 "graphify": r"graphify",
 "code-mode": r"code-mode(?![a-z])",
 "claude-mem": r"claude-mem|mem-search|thedotmack",
 "Obsidian": r"obsidian",
 "memory-MCP": r"memory-mcp|mcp-memory|server-memory|agentmemory|agent-memory-mcp|openmemory|mem0",
 "ruflo": r"ruflo|claude-flow",
 "autoharness": r"autoharness",
 "continuous-learning": r"continuous-learning",
 "mattpocock": r"mattpocock",
 "token-tasarruf": r"caveman|tokeneconomizer|token-rea|token-budget|token-economics|token-efficiency|context-diet|cost-cutter|token-receipts|token-max",
}
CY_RE = {k: re.compile(v) for k, v in CY.items()}

_TR = str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosucgiosuaiu")
def katla(s):
    return (s or "").translate(_TR).lower().replace("\ufffd", "")

# Gürültü üreten, kategori sinyali taşımayan kısa/çok anlamlı sözcükler (tablolardan atılır; denetim turlarında genişletildi)
KARA = set("""quest question questions analysis analyz report persona session cinematic hey ab tap ava dia bark cut mix beat bar wrk tsung rapid spock silk gauge behave lettuce serenity fitnesse karma mocha jasmine ink
construct dash panel hex index query queries dimension arrow delta heap segment clarity sigma tag things bear roam focus mind lean slim diet
trim prune daily weekly morning history resume restore terminal lesson kart tool bun deno love2d defold wan pi ray modal fork stream cut
fabric forge step ida ik luma runway pika dag go ecs fun play look feel smart auto easy simple quick fast info stat number work flow stage
phase screen ui look better beautiful lead team office market model object scene light material asset water cloud sky fire smoke fx
brand art draw paint sketch visual color design creative page browser style styling prototype canvas svg render generat prompt
read learn study tutorial ders egitim doc docs source search explor insight text content note write writing yaz report rapor
template sablon convert format library package module framework code server api endpoint rest node python typescript javascript
check validat assert ensure confirm prove evidence bug fix debug trace log monitor alert failure error exception crash hang leak race
timeout retry quality reliab stab robust data table column row record store storage cache report metric aggregate group join filter sort
export import sync backup snapshot personal assistant helper utility manage track list queue reading archive capture clip highlight
guide coach mentor course class lecture teach tutor exam quiz revision app device phone touch native player level world physics
character engine simulation puzzle content post publish social audience customer promo traffic rank visibility reach click digital
online engage copy growth launch organiz structure method approach guideline principle rule standard convention ceremony meeting
agenda minutes summary brief status update progress lead stakeholder align decide choose select option compare evaluate prioritize
business company enterprise client deal order payment bank loan credit debt asset money price cost profit margin commerce retail store
shop product strategy founder executive protect detect scan policy permission credential password safe trust verify certificate
mobile media motion scene shot frame resolution duration timeline sequence track layer effect transition overlay title credit intro
outro channel creator viral hook retention record environment landscape terrain procedural cloud tool tools adapter wrapper bridge
extension addon platform infra setup install config configure admin control remote local trigger event message bus connect
workflow pipeline runner executor scheduler cron daemon service client plugin""".split())
# KARA yalnız ZAYIF/ORTA kademelerde süzülür; güçlü kademe elle seçildi.

def _ust_bol(s):
    out, d, c, i = [], 0, "", 0
    inkls = False
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            c += s[i:i + 2]; i += 2; continue
        if ch == "[":
            inkls = True
        elif ch == "]":
            inkls = False
        elif not inkls:
            if ch == "(":
                d += 1
            elif ch == ")":
                d -= 1
            elif ch == "|" and d == 0:
                out.append(c); c = ""; i += 1; continue
        c += ch; i += 1
    if c:
        out.append(c)
    return out

def _govde(alt):
    """alt -> (kök, saf_mi). Baş \\b / (?<!..) atılır; baştaki [a-z0-9] dizisi kök, ?*+{ gelirse son harf düşer."""
    a = re.sub(r"^(?:\\b|\(\?<![^)]*\))+", "", alt)
    m = re.match(r"[a-z0-9]+", a)
    if not m:
        return "", False
    k = m.group(0)
    rest = a[len(k):]
    if rest[:1] in ("?", "*", "+", "{"):
        k = k[:-1]
    saf = (a == k)
    return k[:10], saf and len(k) <= 10

KOK_INDEX, GENEL = {}, []
def _kur():
    for kat, (s, m, w) in R.items():
        for kademe, (rx, ag) in enumerate(((s, 3), (m, 2), (w, 1))):
            for alt in _ust_bol(rx):
                if not alt:
                    continue
                kok, saf = _govde(alt)
                if kok in KARA:
                    continue
                c = re.compile(alt)
                if kok:
                    KOK_INDEX.setdefault(kok, []).append((kat, ag, None if saf else c, kok))
                else:
                    GENEL.append((kat, ag, c))
_kur()
_KELIME = re.compile(r"[a-z0-9]+")
_EK = frozenset(("s", "es", "ed", "er", "ers", "ing", "ion", "ions", "lar", "ler", "i", "si", "u", "yi", "in", "un"))

def skor(metin, cap=2):
    """kategori -> toplam skor (kök-dizinli eşleşme: kelime başı önek; her kademeden en çok cap sayılır)."""
    sayac = collections.Counter()
    gorulen = set()
    for mm in _KELIME.finditer(metin):
        tok, pos = mm.group(0), mm.start()
        for L in range(1, min(len(tok), 10) + 1):
            for kat, ag, c, kok in KOK_INDEX.get(tok[:L], ()):
                if (pos, kat, ag, kok) in gorulen:
                    continue
                if c is None:
                    # kisa kok (<5) yalniz tam sozcuk ya da yalin ek alir: ad!=adi, oyun!=oyunbaz, ram!=ramp
                    ok = len(kok) == L and (L == len(tok) or len(kok) >= 5 or tok[L:] in _EK)
                else:
                    ok = c.match(metin, pos) is not None
                if ok:
                    gorulen.add((pos, kat, ag, kok))
                    sayac[(kat, ag)] += 1
    for kat, ag, c in GENEL:
        n = len(c.findall(metin))
        if n:
            sayac[(kat, ag)] += n
    out = {}
    for (kat, ag), n in sayac.items():
        out[kat] = out.get(kat, 0) + ag * min(n, cap)
    return out

# tür varsayılanları: içerik sinyali yoksa (zayıf, guven=dusuk)
TUR_VARSAYILAN = {"karar": "surec-plan", "rapor": "surec-plan", "istek": "surec-plan", "proje": "surec-plan", "kota": "verimlilik",
                  "gecmis": "verimlilik", "kalite": "test-qa", "kombin": "ajan-arac", "hesap": "ajan-arac", "model": "ml-ai",
                  "tasarim": "frontend-ui", "sablon": "frontend-ui", "baglayici": "ajan-arac", "mcp": "ajan-arac", "cli": "ajan-arac",
                  "ajan": "ajan-arac", "eklenti": "ajan-arac", "plugin": "ajan-arac", "betik": "ajan-arac", "donanim": "diger-genel",
                  "uygulama": "diger-genel", "klon": "diger-genel", "kalem": "diger-genel", "kart": "diger-genel", "site": "diger-genel"}

def siniflandir(ad, tur, ozet="", etiket="", yol="", dep=""):
    """-> (birincil, ikincil[list], guven, yontem, gerekce). Saf kural; model çağrısı yok."""
    n = re.sub(r"[-_:/.]+", " ", katla(ad))
    t = GURULTU.sub(" ", katla(f"{ozet} {etiket} {dep}")[:600])
    sn, st = skor(n), skor(t)
    toplam = collections.Counter()
    for k, v in sn.items():
        toplam[k] += 2 * v
    for k, v in st.items():
        toplam[k] += v
    if tur in ("mcp", "cli", "ajan", "plugin", "eklenti", "baglayici"):
        toplam["ajan-arac"] += 2
    if dep in DEP_HARITA:
        toplam[DEP_HARITA[dep]] += 3
    if toplam.get("backend-dotnet", 0) >= 3 and "backend-genel" in toplam:  # .NET sinyali varsa genel backend puani .NET'e akar
        toplam["backend-dotnet"] += toplam.pop("backend-genel")
    if not toplam:
        v = TUR_VARSAYILAN.get(tur, "diger-genel")
        return v, [], "dusuk", "tur-varsayilan", f"icerik sinyali yok; tur={tur}"
    sirali = toplam.most_common()
    (b, s1) = sirali[0]
    s2 = sirali[1][1] if len(sirali) > 1 else 0
    # genel (çok kategoriye sızan) 'ajan-arac' ve 'surec-plan' zayıf eşleşmelerde ikinci sıraya itilir
    if s1 < 4 and b in ("ajan-arac", "surec-plan", "verimlilik", "test-qa", "veri-db") and len(sirali) > 1:
        for k, v in sirali[1:]:
            if v >= s1 - 1 and k not in ("ajan-arac", "surec-plan", "verimlilik"):
                b, s1 = k, v
                break
    GEN = ("ajan-arac", "surec-plan", "verimlilik", "inceleme", "arastirma", "test-qa")
    if b in GEN:  # genel sınıf alan sınıfıyla yakınsa alan kazanır, genel ikincil kalır
        for k, v in sirali[1:]:
            if k not in GEN and v * (1.2 if b == "ajan-arac" else 1.5) >= s1 and v >= 3:
                b, s1 = k, v
                break
    ik = [k for k, v in sirali if k != b and v >= max(3, 0.5 * s1)][:2]
    if s1 >= 8 and s1 >= 1.8 * s2:
        g = "yuksek"
    elif s1 >= 4 and s1 > s2:
        g = "orta"
    else:
        g = "dusuk"
    return b, ik, g, "kural", f"skor {b}={s1}" + (f" {sirali[1][0]}={s2}" if len(sirali) > 1 else "")

DEP_HARITA = {"arastirma-ogrenme": "arastirma", "backend-dotnet": "backend-dotnet", "belge": "belge", "frontend": "frontend-ui", "guvenlik": "guvenlik",
              "surec-ajan-arac": "ajan-arac", "surec-git-yayin": "git-yayin", "surec-inceleme": "inceleme", "surec-plan": "surec-plan",
              "test-qa": "test-qa", "veri-db": "veri-db", "verimlilik": "verimlilik"}

def cok_yonlu(*alanlar):
    m = katla(" ".join(a or "" for a in alanlar))
    return [k for k, rx in CY_RE.items() if rx.search(m)]

# ------------------------------------------------------------------ toplama
def _norm(ad):
    return katla(ad).strip().lower()

def _oku(p, n=500):
    try:
        with open(p, "rb") as f:
            return f.read(n * 4).decode("utf-8", "replace")
    except OSError:
        return ""

def _readme_ozet(d):
    for ad in ("README.md", "readme.md", "README.rst", "README.txt", "Readme.md", "package.json", "pyproject.toml"):
        s = _oku(Path(d) / ad, 700)
        if s:
            s = re.sub(r"!?\[[^\]]*\]\([^)]*\)|<[^>]+>|[#*`>|=_]+|https?://\S+", " ", s)
            return re.sub(r"\s+", " ", s).strip()[:400]
    return ""

def _skill_desc(p):
    s = _oku(p, 700)
    m = re.search(r"^description:\s*[>|]?-?\s*(.*?)(?:\n\w[\w-]*:|\n---)", s, re.S | re.M)
    return re.sub(r"\s+", " ", m.group(1)).strip()[:400] if m else re.sub(r"\s+", " ", s)[:200]

def _satirlar(yol, ayirac="\t"):
    with open(yol, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.reader(f, delimiter=ayirac, quotechar=None))

def topla():
    """kaynak -> {(norm_ad, tur): kayit}; ham satır sayısı kaynak başına döner."""
    ogeler, ham = {}, collections.Counter()
    def ekle(kaynak, ad, tur, yol="", ozet="", etiket="", dep=""):
        ad = (ad or "").strip()
        if not ad:
            return
        ham[kaynak] += 1
        k = (_norm(ad), tur)
        o = ogeler.get(k)
        if o is None:
            ogeler[k] = {"ad": ad, "tur": tur, "yol": yol, "ozet": ozet, "etiket": etiket, "dep": dep, "kaynaklar": [kaynak]}
        else:
            if kaynak not in o["kaynaklar"]:
                o["kaynaklar"].append(kaynak)
            if len(ozet) > len(o["ozet"]):
                o["ozet"] = ozet
            o["etiket"] = (o["etiket"] + " " + etiket).strip()[:200] if etiket and etiket not in o["etiket"] else o["etiket"]
            o["dep"] = o["dep"] or dep
            o["yol"] = o["yol"] or yol
    for r in _satirlar(KOK / ".kos/kopru/kaynak-dizin/dizin.tsv")[1:]:
        r += [""] * (5 - len(r))
        ekle("dizin", r[1], r[0], r[2], r[3], r[4])
    for r in _satirlar(KOK / "docs/envanter/envanter.tsv")[1:]:
        r += [""] * (10 - len(r))
        ekle("envanter", r[0], r[1], r[2], r[4], r[5], r[6])
    for r in _satirlar(KOK / ".kos/kopru/kalem-denetim.tsv")[1:]:
        r += [""] * (6 - len(r))
        ekle("kalem-denetim", r[1], "kalem", f"kalem-denetim:{r[0]}", r[3].replace("/", " "), "")
    # klon dizinleri
    jobs = []
    for kok, kaynak in ((Path("C:/Projeler/_araclar/v"), "_araclar/v"),
                        (Path("C:/Users/pc/Desktop/Claude ile yapılanlar/araclar/ana-liste"), "ana-liste")):
        if kok.is_dir():
            jobs += [(kaynak, d) for d in kok.iterdir() if d.is_dir()]
    for kok in (Path("C:/Projeler/_araclar/npm-kalem"), Path("C:/Projeler/_araclar/venv-kalem")):
        if kok.is_dir():
            jobs.append((f"_araclar/{kok.name}", kok))
    with ThreadPoolExecutor(8) as ex:
        for (kaynak, d), oz in zip(jobs, ex.map(lambda j: _readme_ozet(j[1]), jobs)):
            ad = d.name.split("__", 1)[-1]
            ekle(kaynak, ad, "klon", str(d).replace("\\", "/"), (d.name.replace("__", " ") + " " + oz).strip())
    # ~/.claude skills / agents / plugin önbelleği / MCP anahtar adları
    home = Path.home() / ".claude"
    sk = [d for d in (home / "skills").iterdir() if d.is_dir()] if (home / "skills").is_dir() else []
    with ThreadPoolExecutor(8) as ex:
        for d, oz in zip(sk, ex.map(lambda d: _skill_desc(d / "SKILL.md"), sk)):
            ekle("~/.claude/skills", d.name, "skill", str(d).replace("\\", "/"), oz)
    for p in list((home / "agents").glob("*.md")) + list((KOK / ".claude/agents").glob("*.md")):
        ekle("agents", p.stem, "ajan", str(p).replace("\\", "/"), _skill_desc(p))
    for p in glob.glob(str(home / "plugins/cache/*/*/*/.claude-plugin/plugin.json")):
        try:
            j = json.loads(_oku(p, 4000) or "{}")
        except ValueError:
            m = re.search(r'"name"\s*:\s*"([^"]+)"', _oku(p, 2000)); j = {"name": m.group(1) if m else ""}
            m = re.search(r'"description"\s*:\s*"([^"]*)"', _oku(p, 2000)); j["description"] = m.group(1) if m else ""
        if isinstance(j, dict):
            ekle("plugins/cache", j.get("name") or Path(p).parents[1].parent.name, "plugin", p.replace("\\", "/"), str(j.get("description", ""))[:400])
    try:
        cj = json.loads(_oku(Path.home() / ".claude.json", 10**7))
        adlar = set(cj.get("mcpServers", {}))
        for pr in cj.get("projects", {}).values():
            adlar |= set(pr.get("mcpServers", {}))
        for a in sorted(adlar):
            ekle("~/.claude.json", a, "mcp", "~/.claude.json#mcpServers", "")
    except (ValueError, OSError):
        pass
    return ogeler, dict(ham)

# ------------------------------------------------------------------ ücretsiz model (belirsizler)
TANIM = ("arastirma=web/literatur arastirma, arama, scraping, ogrenme kaynaklari; backend-dotnet=.NET/C#/ASP.NET/EF Core/MSBuild; backend-genel=.NET disi sunucu tarafi diller/frameworkler (Python/Django/Go/Java/PHP/Node/Rust backend), API tasarimi; "
 "belge=pdf/docx/xlsx/pptx, dokuman, rapor yazimi, markdown; bilim=bilim/biyoloji/kimya/fizik/tip; bulut-devops=cloud, docker, k8s, CI/CD, deploy, izleme; "
 "frontend-ui=web arayuz, UI/UX, CSS, React, tasarim sistemi, web animasyon/shader; git-yayin=git, GitHub, PR, release, yayin; gorsel=gorsel uretim/duzenleme, logo, ikon; "
 "guvenlik=guvenlik, pentest, tersine muhendislik, zafiyet; inceleme=review, audit, kod/tasarim elestirisi, site inceleme; is-finans-hukuk=finans, muhasebe, hukuk, satis/CRM, IK, trading, para kazanma; "
 "ml-ai=ML/LLM/model egitimi/inference/RAG/prompt, AI kurslari; mobil=iOS/Android/Flutter/React Native; oyun=oyun gelistirme/modlama; pazarlama-reklam=pazarlama, SEO, reklam, sosyal medya, icerik uretimi; "
 "surec-plan=planlama, spec, proje yonetimi, karar, gorev; test-qa=test, QA, dogrulama, kalite kontrol; veri-db=veritabani, SQL, veri analizi/muhendisligi, dashboard; "
 "verimlilik=token/hafiza/baglam tasarrufu, kisisel verimlilik, not/ikinci beyin; video=video/ses/muzik/altyazi/montaj/motion video; 3d-blender=3D, Blender, three.js, CAD; "
 "ajan-arac=MCP/CLI/ajan/orkestrasyon/otomasyon araclari, eklenti/skill altyapisi, ajan frameworkleri; diger-genel=hicbirine uymayan/ipucu yok")
HATA = []
KATSTR = ", ".join(KATEGORILER)
_LLM_KURAL = ("KURALLAR: (1) Kalemin ASIL AMACINA gore sec; tesadufi sozcuge (review, test, report, team...) gore degil. "
 "(2) Alan kazanir: satis/CRM/IK/finans/hukuk/trading/muhasebe araclari is-finans-hukuk; bilimsel kutuphane ve alan skilleri bilim (veri analizi kutuphanesi veri-db); "
 "sadece genel ajan/MCP/skill altyapisi ajan-arac. (3) 'Alintida yalniz adi geciyor (ipucu)' satirlarinda ad+ipucundan urunun ne yaptigini bil, ona gore sec. "
 "(4) Ad bir video/hesap kimligi, rastgele kod ya da gercekten ipucusuz ise diger-genel. (5) Bozuk karakter (?) yok say.")
def llm_istem(oge_listesi):
    satir = [f"{i}|{o['tur']}|{o['ad'][:60]}|{re.sub(chr(10), ' ', o['ozet'])[:220]}" for i, o in enumerate(oge_listesi)]
    return (f"Her satir bir arac/skill/kaynak/yontem kalemi (indeks|tur|ad|ozet). Kaleme EN IYI uyan BIRINCIL kategoriyi ve en cok 1 IKINCIL sec. Kategoriler: {TANIM}. "
            f"{_LLM_KURAL} Cikti: her kalem icin tek satir 'indeks|birincil|ikincil_veya_-' , baska hicbir sey yazma.\n" + "\n".join(satir))
def llm_belirsiz(ogeler, sonuc, N, parti=110):
    sys.path.insert(0, str(KOK / "tools"))
    import ucretsiz_havuz
    onc = {"skill": 0, "plugin-skill": 0, "katalog": 0, "mcp": 0, "cli": 0, "ajan": 0, "plugin": 0, "arac": 0, "baglayici": 1, "klon": 1, "kalem": 2, "uygulama": 1}
    ad = ARA / "llm.json"
    onbellek = json.loads(ad.read_text(encoding="utf-8")) if ad.exists() else {}
    gs = {"dusuk": 0, "orta": 1, "yuksek": 2}
    adaylar = [k for k, s in sonuc.items() if "|".join(k) not in onbellek]
    adaylar.sort(key=lambda k: (onc.get(k[1], 3), gs[sonuc[k]["guven"]], -len(ogeler[k]["ozet"])))
    adaylar = adaylar[: N * parti]
    gruplar = [adaylar[i:i + parti] for i in range(0, len(adaylar), parti)]
    def isle(g):
        istem = llm_istem([ogeler[k] for k in g])
        try:
            m, kaynak, lg = ucretsiz_havuz.cagir("ozet", istem, max_tokens=2500, zaman=120)
        except Exception as e:  # kota/ağ: bekleme yok, sonraki gruba
            return g, None, str(e)[:60]
        if not m:
            HATA.append(str(lg)[:200])
        return g, m, kaynak
    yeni = 0
    with ThreadPoolExecutor(10) as ex:
        for g, m, kaynak in ex.map(isle, gruplar):
            if not m:
                continue
            for ln in m.splitlines():
                p = ln.strip().split("|")
                if len(p) >= 2 and p[0].strip().isdigit() and int(p[0]) < len(g) and p[1].strip() in KATEGORILER:
                    ik = p[2].strip() if len(p) > 2 and p[2].strip() in KATEGORILER and p[2].strip() != p[1].strip() else ""
                    onbellek["|".join(g[int(p[0])])] = {"b": p[1].strip(), "i": ik, "m": kaynak}
                    yeni += 1
            ad.write_text(json.dumps(onbellek, ensure_ascii=False), encoding="utf-8")
    ad.write_text(json.dumps(onbellek, ensure_ascii=False), encoding="utf-8")
    if HATA:
        print("llm hata ornek:", len(HATA), HATA[0])
    return yeni, len(adaylar)

def nasil(tur, ad, yol):
    return {"skill": f"Skill ile cagir: {ad}", "plugin-skill": f"Skill ile cagir: {ad}", "plugin": f"/plugin install {ad}",
            "mcp": f"MCP: mcp__{ad}__* (ToolSearch ile yukle)", "cli": f"{ad} --help", "ajan": f"Agent subagent_type={ad}",
            "katalog": f'mcptoon skills resolve "{ad}"', "betik": f"python {yol}", "klon": f"README oku, kur: {yol}", "kalem": f"kaynak: {yol}",
            "site": f"incele: {yol}", "baglayici": f"baglayici: {ad} (claude.ai ayarlari)"}.get(tur, f"oku: {yol}")

def main(argv):
    ARA.mkdir(parents=True, exist_ok=True)
    yeniden, llmN = "--yeniden" in argv, 0
    if "--llm" in argv:
        llmN = int(argv[argv.index("--llm") + 1])
    ogp = ARA / "ogeler.json"
    if ogp.exists() and not yeniden:
        d = json.loads(ogp.read_text(encoding="utf-8")); ogeler = {tuple(k.split("\x1f")): v for k, v in d["ogeler"].items()}; ham = d["ham"]
    else:
        ogeler, ham = topla()
        ogp.write_text(json.dumps({"ham": ham, "ogeler": {"\x1f".join(k): v for k, v in ogeler.items()}}, ensure_ascii=False), encoding="utf-8")
    sonuc = {}
    for k, o in ogeler.items():
        b, ik, g, y, ger = siniflandir(o["ad"], o["tur"], o["ozet"], o["etiket"], o["yol"], o["dep"])
        sonuc[k] = {"b": b, "ik": ik, "guven": g, "yontem": y, "ger": ger}
    if llmN:
        print("llm yeni/aday:", llm_belirsiz(ogeler, sonuc, llmN))
    lp = ARA / "llm.json"
    lc = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else {}
    for k, s in sonuc.items():
        v = lc.get("|".join(k))
        if v:
            ik = [v["i"]] if v["i"] else [x for x in s["ik"] if x != v["b"]][:1]
            s["b"], s["ik"], s["guven"], s["yontem"], s["ger"] = v["b"], ik, "orta", "ucretsiz-model", f"model:{v['m']}"[:80]
    satir = []
    for k, o in ogeler.items():
        s = sonuc[k]
        cy = cok_yonlu(o["ad"], o["yol"] if o["tur"] in ("katalog", "skill", "plugin-skill", "plugin", "mcp", "cli", "ajan", "baglayici") else "")
        satir.append([o["ad"], o["tur"], o["yol"], s["b"], ";".join(s["ik"]), ";".join(cy), s["guven"], s["yontem"], s["ger"][:80]])
    if CIKTI.exists():  # baska oturumun (KATEGORI-KAPSAM) eklediği satırlar: ogeler'de olmayan anahtarlar korunur
        yeni_anahtar = {(r[0], r[1]) for r in satir}
        csv.field_size_limit(10**7)
        with open(CIKTI, encoding="utf-8", newline="") as f:
            for r in list(csv.reader(f, delimiter="\t", quotechar='"'))[1:]:
                if len(r) == 9 and (r[0], r[1]) not in yeni_anahtar and r[3] in KATEGORILER:
                    r[4] = ";".join(x for x in r[4].replace(",", ";").split(";") if x in KATEGORILER)
                    satir.append(r)
    satir.sort(key=lambda r: (r[3], r[1], r[0].lower()))
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", quotechar='"', lineterminator="\n")
        w.writerow(["ad", "tur", "yol", "birincil", "ikincil", "cok_yonlu", "guven", "yontem", "gerekce"])
        for r in satir:
            w.writerow([re.sub(r"[\t\r\n]+", " ", c) for c in r])
    ozet_yaz(satir, ham, len(ogeler))
    if "--ornek" in argv:
        ornek_yaz(satir, ogeler)
    print("tekil:", len(ogeler), "ham:", sum(ham.values()), dict(collections.Counter(r[3] for r in satir)))
    print("guven:", dict(collections.Counter(r[6] for r in satir)))

def ozet_yaz(satir, ham, n):
    tur_say = collections.defaultdict(collections.Counter)
    for r in satir:
        tur_say[r[3]][r[1]] += 1
    cy = collections.Counter()
    for r in satir:
        for t in filter(None, r[5].split(";")):
            cy[t] += 1
    L = ["# Kategori özeti (KATEGORI-1)", "", f"Tekil kalem: {n} · ham satır: {sum(ham.values())} · her kalem bir birincil kategori aldı (boş birincil: {sum(1 for r in satir if not r[3])}).", "",
         "Kaynak ham satırları: " + ", ".join(f"{k}={v}" for k, v in ham.items()), "",
         "Çok-yönlü etiket: " + ", ".join(f"{k}={v}" for k, v in cy.most_common()), ""]
    for kat in KATEGORILER:
        rs = [r for r in satir if r[3] == kat]
        L += [f"## {kat} — {len(rs)}", "tür: " + ", ".join(f"{t}={c}" for t, c in tur_say[kat].most_common(8)), ""]
        gor = sorted((r for r in rs if r[6] != "dusuk"), key=lambda r: (r[1] not in ("skill", "plugin-skill", "mcp", "cli", "plugin", "ajan"), r[0]))
        for r in random.Random(7).sample(gor, min(10, len(gor))):
            L.append(f"- {r[0][:60]} ({r[1]})")
        L.append("")
    OZET.write_text("\n".join(L), encoding="utf-8")

def ornek_yaz(satir, ogeler, kat_basi=14):
    rnd = random.Random(int(os.environ.get("KATEGORI_TOHUM", "42")))
    sec = []
    for kat in KATEGORILER:
        rs = [r for r in satir if r[3] == kat]
        sec += rnd.sample(rs, min(kat_basi, len(rs)))
    idx = {(_norm(o["ad"]), o["tur"]): o for o in ogeler.values()}
    with open(ARA / "ornek.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["n", "ad", "tur", "ozet", "birincil", "ikincil", "yontem"])
        for i, r in enumerate(sec, 1):
            o = idx.get((_norm(r[0]), r[1]), {})
            w.writerow([i, r[0][:70], r[1], re.sub(r"[\t\r\n]+", " ", o.get("ozet", ""))[:220], r[3], r[4], r[7]])

def yeni_kalem(kalemler, model=True):
    """KALICI KONTROL (NIHAI 36(J) kurulumun SON adimi): yeni kalem -> kural -> bagimsiz ikinci model -> uyusmazsa/dusuk guvende Sonnet hakem
    -> kategori.tsv'ye eklenir. kalemler: [{ad, tur, ozet?, yol?}]. Zaten kayitli (ad, tur) atlanir. Doner: [(ad, birincil, yontem)]."""
    mevcut = set()
    with open(CIKTI, encoding="utf-8", newline="") as f:
        for r in csv.reader(f, delimiter="\t"):
            mevcut.add((_norm(r[0]), r[1]))
    yeniler = [k for k in kalemler if (_norm(k["ad"]), k["tur"]) not in mevcut]
    if not yeniler:
        return []
    if model:
        import kategori_denetim as D
        sonuc = D.kalem_kontrol(yeniler)
    else:
        sonuc = []
        for k in yeniler:
            b, ik, g, _, _ = siniflandir(k["ad"], k["tur"], k.get("ozet", ""), "", k.get("yol", ""), "")
            sonuc.append((b, ik, g, "kural-denetimsiz", "model kapali"))
    with open(CIKTI, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", quotechar='"', lineterminator="\n")
        for k, (b, ik, g, y, ger) in zip(yeniler, sonuc):
            cy = cok_yonlu(k["ad"], k.get("yol", ""))
            w.writerow([re.sub(r"[\t\r\n]+", " ", c) for c in (k["ad"], k["tur"], k.get("yol", ""), b, ";".join(ik), ";".join(cy), g, y, ger[:80])])
    return [(k["ad"], r[0], r[3]) for k, r in zip(yeniler, sonuc)]


if __name__ == "__main__":
    if "--yeni-kalem" in sys.argv:  # --yeni-kalem "ad|tur|ozet|yol" [...]
        ks = []
        for a in sys.argv[sys.argv.index("--yeni-kalem") + 1:]:
            p4 = (a.split("|") + ["", "", ""])[:4]
            ks.append({"ad": p4[0], "tur": p4[1] or "kalem", "ozet": p4[2], "yol": p4[3]})
        print(yeni_kalem(ks))
    else:
        main(sys.argv[1:])
