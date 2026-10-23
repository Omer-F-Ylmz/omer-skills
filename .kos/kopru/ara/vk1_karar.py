import json,sys,csv,re
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
rows=json.load(open('.kos/kopru/ara/vk1_rows.json',encoding='utf-8'))
inv=set(l.strip() for l in open('.kos/kopru/ara/vk1_env.txt',encoding='utf-8'))
# anahtar|tür|karar|kanıt(kurulu için envanter adı)|gerekçe
D="""
name:claude-skills|kavram|gürültü||genel terim; skill sistemi zaten kurulu
name:claude-md|kavram|gürültü||CLAUDE.md dosyası; araç değil (claude-md-management kurulu)
site:star-history.com|site|kurulu|star-history-paket|star-history paket skill'i kurulu
name:agent-skills|skill|kurulu|agent-skills|addy agent-skills eklentisi kurulu
name:claude-code|uygulama|kurulu|claude-code-guide|Claude Code ana araç
name:code-review|plugin|kurulu|code-review|code-review eklentisi kurulu
gh:star-history/star-history|repo|kurulu|star-history-paket|grafik servisi; paket skill'i yeterli
name:claude-agents|kavram|gürültü||genel terim (.claude/agents)
name:claude-code-setup|plugin|kurulu|claude-code-setup|eklenti kurulu
name:design-review|skill|kurulu|design-review|skill kurulu
gh:remotion-dev/remotion|kütüphane|kurulu|remotion-best-practices|skill kurulu; npm paketi proje başı. lisans: Remotion Lisansı (≤3 kişi ücretsiz)
name:claude-fable-5|model|gürültü||model adı, kurulacak araç yok
name:github-cli|CLI|kurulu|bin:gh|gh kurulu
name:install-skills|kavram|gürültü||genel eylem
site:github.com|site|gürültü||genel alan adı
site:remotion.dev|site|kurulu|remotion-best-practices|doküman; skill kurulu
name:browser-use|skill|kurulu|browser-use|skill kurulu (pip kütüphanesi ayrı: gerekirse proje başı)
name:claude-design|site|kurulu|design|claude-design köprüsü + design eklentisi (bellek notu)
name:frontend-design-skill|skill|kurulu|frontend-design|kurulu
name:nano-banana-2|plugin|kurulu|nano-banana-2|kurulu
site:apify.com|API-servis|kurulu|mcp:apify|Apify MCP kurulu
site:banger.show|site|KUR||Remotion video şablon sitesi; referans/incele
site:higgsfield.ai|API-servis|KUR||AI video servisi; hesap + MCP; ücretsiz muadil: fal.ai (kurulu)
site:insiderforce.io|site|KUR||bilinmiyor, doğrulanacak; ref bağlantısı olabilir (güvenlik tara)
site:microsoft.com|site|gürültü||genel alan adı
gh:activepieces/activepieces|uygulama|KUR||MIT çekirdek; self-host otomasyon (Zapier muadili)
gh:actualbudget/actual|uygulama|KUR||MIT; yerel bütçe uygulaması
gh:anthropics/claude-code|repo|kurulu|claude-code-guide|Claude Code kurulu
gh:anthropics/courses|repo|KUR||eğitim notebook'ları; klonla (lisans doğrula)
gh:apify/crawlee|kütüphane|KUR||Apache-2; npm crawlee proje başı
gh:christopherkahler/base|repo|KUR||bilinmiyor, doğrulanacak (lisans oku)
gh:dani-garcia/vaultwarden|uygulama|KUR||AGPL-3; self-host parola yöneticisi (kod gömme yok)
gh:documenso/documenso|uygulama|KUR||AGPL-3; self-host e-imza (document-signing skill ayrı)
gh:dubinc/dub|uygulama|KUR||AGPL-3 çekirdek; self-host link kısaltıcı
gh:immich-app/immich|uygulama|KUR||AGPL-3; self-host fotoğraf; Docker + disk gerekir
gh:kde/kdenlive|uygulama|KUR||GPL-3; video editörü, winget ile
gh:leonxlnx/taste-skill|skill|kurulu|taste-skill|MIT, kurulu (bellek: lisans kapısı)
gh:pbakaus/impeccable|skill|kurulu|impeccable|kurulu
gh:stirling-tools/stirling-pdf|uygulama|KUR||MIT çekirdek; PDF araç seti
gh:voltagent/awesome-design-md|repo|KUR||MIT; marka DESIGN.md koleksiyonu (design-md skill ayrı, kısmen)
gh:zachlatta/freeflow|uygulama|KUR||freeflow-paket skill'i var, aracın kendisi kurulu değil
gh:zackriya-solutions/meetily|uygulama|KUR||MIT; yerel toplantı notu (Whisper)
name:claude-api|skill|kurulu|claude-api|kurulu
name:claude-fable-5-1|model|gürültü||model adı
name:nvidia-nim|API-servis|KUR||ücretsiz NIM API anahtarı (hesap); ücretsiz havuza aday
site:21st.dev|MCP|kurulu|mcp:21st|MCP kurulu
site:amazon.com|site|gürültü||genel alan adı
site:blender.org|uygulama|kurulu|app:blender|Blender 5.2 kurulu
site:context.dev|API-servis|KUR||bilinmiyor, doğrula; context7 kurulu ayrı
site:crawlee.dev|kütüphane|KUR||crawlee dokümanı; bkz gh:apify/crawlee
site:dataforseo.com|API-servis|KUR||ücretli API (hesap); claude-seo:seo-dataforseo skill'i var
site:github.io|site|gürültü||genel alan adı
gh:affaan-m/ecc|repo|KUR||everything-claude-code; MIT; skill/ajan koleksiyonu
gh:anthropics/claude-plugins-official|repo|kurulu|claude-code-setup@claude-plugins-official|resmî marketplace etkin
gh:apify/impit|kütüphane|KUR||tarayıcı-taklidi HTTP istemcisi (MIT)
gh:berriai/litellm|kütüphane|KUR||MIT; pip litellm yok; OmniRoute zaten benzer
gh:calesthio/openmontagel|repo|KUR||yazım hatası: calesthio/OpenMontage; AGPL olabilir, lisans oku
gh:decolua/9router|CLI|KUR||9router-paket skill'i var, aracın kendisi yok
gh:diegosouzapw/omnicopilot|eklenti|KUR-sonra||OmniRoute için VSCode eklentisi (VS Code önkoşul)
gh:diegosouzapw/omniroute|uygulama|kurulu|bin:node|OmniRoute 127.0.0.1:20128'de çalışıyor (tools/ucuz_alt.py)
gh:firecrawl/firecrawl-docs|repo|KUR||doküman deposu; firecrawl-scraper skill'i kurulu
gh:github/gitignore|repo|KUR||CC0 şablonlar; referans klon yeterli
gh:herdrdev/herdr|CLI|kurulu|herdr|herdr skill/paket kurulu
gh:hermoso-ai/hermoso|plugin|kurulu|hermoso|eklenti kurulu
gh:igorbrigadir/twitter-advanced-search|repo|KUR||doküman; referans klon
gh:jakeschincar1ol/1inkedin-agent-:|repo|atla-güvenlik||typosquat görünümlü hesap/ad (1inkedin); kod çalıştırma
gh:nvidia/skillspectd|repo|KUR||yazım hatası: nvidia SkillSpector; lisans oku
gh:nvidia/skillspectrd|repo|KUR||yazım hatası: nvidia SkillSpector; gh:nvidia/skillspectd ile aynı
gh:pydantic/httpx2|kütüphane|kurulu|pip:httpx2|pip kurulu
gh:remotion-dev/skills|skill|kurulu|remotion-best-practices|kurulu
gh:router-for-me/cliproxyapi|CLI|KUR||MIT; CLI abonelikleri OpenAI-uyumlu API yapar (OmniRoute benzeri)
gh:tailwindlabs/tailwindcss|kütüphane|KUR||MIT; npm proje başı; tailwind-patterns skill'i kurulu
gh:zk/claude-mods|repo|KUR||bilinmiyor, doğrulanacak
ghuser:jsdelivr|site|gürültü||CDN, kurulacak şey yok
name:agent-sdk-dev|plugin|kurulu|agent-sdk-dev|kurulu
name:alt-ajanlar|kavram|gürültü||genel terim
name:andrej-karpathy-skills|skill|kurulu|andrej-karpathy-skills|kurulu
name:chatllm-abacus-ai|API-servis|KUR||Abacus ChatLLM (ücretli, hesap)
name:claude-code-mods|repo|KUR||bilinmiyor, doğrulanacak
name:claude-md-management|plugin|kurulu|claude-md-management|kurulu
name:claudepluginhub|site|KUR||eklenti dizini; katalog kaynağı olarak tara
name:code-modernization|plugin|KUR||resmî eklenti adayı; kurulu değil
name:code-simplifier|plugin|kurulu|code-simplifier|kurulu
name:codex-skill|skill|KUR||bilinmiyor, doğrulanacak (codex-review kurulu)
name:commit-commands|plugin|kurulu|commit-commands|kurulu
name:context7-mcp|MCP|kurulu|mcp:context7|kurulu
name:create-next-appelatest|CLI|KUR||yazım hatası: create-next-app@latest; npx ile anlık
name:csharp-lsp|plugin|kurulu|csharp-lsp|kurulu
name:design-dna|skill|kurulu|design|designlang:dna skill'i kurulu (design* eşleşmesi; tam ad designlang)
name:design-html|skill|KUR||bilinmiyor, doğrulanacak
name:document-generate|skill|kurulu|document-generate|kurulu
name:document-release|skill|kurulu|document-release|kurulu
name:example-skills|plugin|kurulu|example-skills|kurulu
name:explanatory-output-style|plugin|kurulu|explanatory-output-style|kurulu
name:fable-advisor|plugin|kurulu|fable-advisor|kurulu
name:framer-motion|kütüphane|KUR||MIT; npm motion/framer-motion proje başı (motion skill kurulu)
name:frontend-design|skill|kurulu|frontend-design|kurulu
name:github-mcp-server|MCP|kurulu|mcp:github|kurulu
name:google-fonts|site|KUR||yazı tipi kaynağı; yerel indirme proje başı
name:grill-me|skill|kurulu|grill|grill skill'i kurulu
name:gstack-upgrade|skill|kurulu|gstack-upgrade|kurulu
name:hostinger-api-mcp|MCP|kurulu|hostinger|hostinger eklentisi kurulu
name:image-generation-skill|skill|kurulu|image-generation-skill|kurulu
name:learning-output-style|plugin|kurulu|learning-output-style|kurulu
name:lua-lsp|plugin|KUR||resmî LSP eklentisi; Lua kullanılırsa
name:mattpocock-skills|skill|kurulu|mattpocock-skills|kurulu
name:mcp-git|MCP|kurulu|mcp:mcp-git|kurulu
name:muapi.ai/open-gener|API-servis|KUR||bilinmiyor, doğrula (kırpık metin)
name:next-js|kütüphane|KUR||MIT; proje başı npm
name:plan-ceo-review|skill|kurulu|plan-ceo-review|kurulu
name:plan-eng-review|skill|kurulu|plan-eng-review|kurulu
name:plugin-dev|plugin|kurulu|plugin-dev|kurulu
name:qa-only|skill|kurulu|qa-only|kurulu
name:scroll-craft|skill|kurulu|scroll-craft|kurulu
name:security-review|skill|kurulu|cc-skill-security-review|kurulu
name:setup-gbrain|skill|kurulu|setup-gbrain|kurulu
name:skill-creator|skill|kurulu|skill-creator|kurulu
name:vercel-cli|CLI|KUR||npm i -g vercel; MIT
name:write-a-prd|skill|kurulu|mattpocock-skills|mattpocock paketinin parçası
name:you-should-know|kavram|gürültü||genel terim
npm:@omniroute/opencode-provider|kütüphane|KUR||OpenCode kullanılırsa; OmniRoute sağlayıcısı
site:aemon.ai|API-servis|KUR||bilinmiyor, doğrula
site:aisa.one|API-servis|KUR||SEO/sosyal veri API'si (hesap, ücretli)
site:aloud.sh|CLI|KUR||bilinmiyor, doğrula
site:hermoso.ai|site|kurulu|hermoso|hermoso eklentisi kurulu
site:photoroom.com|API-servis|KUR||görsel arkaplan API (ücretli, hesap)
site:augmentcode.com|uygulama|KUR||Auggie CLI/eklenti; kapalı kaynak, ücretsiz katman
site:notion.site|site|gürültü||genel alan adı
site:chargeback.io|API-servis|KUR||SaaS; hesap
site:tavily.com|API-servis|kurulu|tavily|tavily eklentisi kurulu
site:chatbase.co|API-servis|KUR||SaaS (hesap)
site:abacus.ai|API-servis|KUR||bkz name:chatllm-abacus-ai
site:cheaperinference.com|API-servis|KUR||bilinmiyor, doğrula
site:claude.a|site|gürültü||kırık alan adı (claude.ai)
site:cline.bot|eklenti|KUR-sonra||Apache-2; VSCode ajan eklentisi (VS Code önkoşul)
site:cline.tools|eklenti|KUR-sonra||bkz site:cline.bot
site:rive.app|uygulama|KUR||Rive editörü (web) + MIT runtime; rivecn bileşenleri
site:composio.dev|API-servis|KUR||MCP/SDK katmanı (MIT SDK), hesap gerekir
site:mistral.ai|API-servis|KUR||ücretsiz API katmanı (hesap); ucretsiz_havuz'da mistral var
site:convex.com|API-servis|kurulu|convex|convex skill'i kurulu
site:cursor.com|uygulama|KUR||IDE; kapalı kaynak, ücretsiz katman
site:firecrawl.dev|API-servis|kurulu|firecrawl-scraper|firecrawl-scraper skill'i kurulu
site:highlightai.com|uygulama|KUR||masaüstü AI asistanı (kapalı)
site:msty.ai|uygulama|KUR||yerel LLM istemcisi; ücretsiz sürüm
site:riotters.com|site|KUR||bilinmiyor, doğrula
site:fal.ai|API-servis|kurulu|fal-generate|fal-* skill'leri kurulu
site:formabledocs.com|site|KUR||bilinmiyor, doğrula
site:gitmcp.io|MCP|KUR||uzak MCP, kurulum yok (URL ile eklenir); ücretsiz
site:graphifylabs.ai|CLI|kurulu|graphify|graphify kurulu
site:herdr.dev|CLI|kurulu|herdr|kurulu
site:insomnia.rest|uygulama|KUR||Apache-2; API istemcisi (Postman muadili)
site:instantly.ai|API-servis|KUR||soğuk e-posta SaaS (hesap)
site:apple.com|site|gürültü||genel alan adı
site:kali.org|uygulama|KUR||Kali WSL; pentest araç seti; WSL + disk gerekir
site:korabench.ai|site|KUR||bilinmiyor, doğrula
site:land-book.com|site|KUR||tasarım galerisi; docs/site-inceleme listesine referans ekle
site:localrank.so|API-servis|KUR||yerel SEO SaaS
site:manyreach.com|API-servis|KUR||soğuk e-posta SaaS
site:topview.ai|API-servis|KUR||AI video SaaS; ücretsiz muadil fal.ai
site:muz.li|site|KUR||tasarım ilham sitesi; referans listeye
site:memory2.co|site|KUR||bilinmiyor, doğrula
site:mintlify.com|API-servis|kurulu|mintlify|mintlify eklentisi kurulu
site:modal.com|API-servis|kurulu|modal|modal skill'i kurulu
site:modelcontextprotocol.io|site|gürültü||MCP doküman sitesi; mcp-builder kurulu
site:msty.studio|uygulama|KUR||bkz site:msty.ai
site:open-vsx.org|site|gürültü||genel kayıt sitesi
site:openseo.so|API-servis|KUR||SEO SaaS
site:postman.com|uygulama|KUR||API istemcisi; kapalı kaynak, ücretsiz katman
site:pypi.org|site|gürültü||genel kayıt sitesi
site:rankie.ai|API-servis|KUR||SEO SaaS
site:vercel.app|site|gürültü||genel barındırma alan adı
site:rive.cool|site|KUR||Rive ilham/kaynak sitesi
site:rivecn.com|kütüphane|KUR||Rive shadcn bileşenleri; lisans oku
site:ryandoser.com|site|KUR||SEO aracı sitesi; doğrula
site:serpapi.com|API-servis|KUR||ücretli API, 100 sorgu/ay ücretsiz
site:skillry.dev|site|KUR||skill dizini; katalog kaynağı olarak tara
site:snyk.io|CLI|KUR||güvenlik taraması; ücretsiz katman, PARÇA 2 güvenlik adayı
site:strix.ai|CLI|kurulu|bin:strix|strix kurulu
site:subclip.app|API-servis|KUR||video klip SaaS
site:pubtailer.com|site|gürültü||izleme/ref bağlantısı
site:typesafe.ai|plugin|kurulu|typesafe|typesafe eklentisi kurulu
vsx:itemName=Stripe.vscode-stripe|eklenti|KUR-sonra||VS Code kurulunca; stripe eklentisi ayrıca kurulu
vsx:itemName=anthropic.claude-code|eklenti|KUR-sonra||VS Code kurulunca (Claude Code uygulaması kurulu)
vsx:itemName=diegosouzapw.omnicopilot|eklenti|KUR-sonra||VS Code kurulunca
vsx:itemName=eamodio.gitlens|eklenti|KUR-sonra||MIT çekirdek; VS Code kurulunca
vsx:itemName=mongodb.mongodb-vscode|eklenti|KUR-sonra||Apache-2; VS Code kurulunca
vsx:itemName=ms-azuretools.vscode-azure-github-copilot|eklenti|KUR-sonra||MS lisansı; yalnız resmî VS Code
vsx:itemName=ms-dotnettools.csdevkit|eklenti|KUR-sonra||MS lisansı; Visual Studio 2022 zaten kurulu (işlevsel muadil)
vsx:itemName=ms-python.python|eklenti|KUR-sonra||MIT; VS Code kurulunca
vsx:itemName=ms-toolsai.jupyter|eklenti|KUR-sonra||MIT; VS Code kurulunca
vsx:itemName=ms-vscode-remote.vscode-remote-extensionpack|eklenti|KUR-sonra||MS lisansı; yalnız resmî VS Code
vsx:itemName=ms-vscode.cpptools|eklenti|KUR-sonra||MS lisansı; yalnız resmî VS Code
"""
dec={}
for l in D.strip().splitlines():
    k,t,kar,kan,ger=l.split('|');dec[k]=(t,kar,kan,ger)
EK={
 'gh:pbákaus/ipeccabile':('skill','kurulu','impeccable','yazım hatası: pbakaus/impeccable; kurulu'),
 'name:skills@latest':('CLI','KUR','','npx skills@latest (skill kurucu CLI); anlık, kalıcı kurulum yok'),
 'npm:omniroute':('uygulama','kurulu','bin:node','OmniRoute çalışıyor (~/.omniroute/storage.sqlite var)'),
 'site:asp.net':('site','gürültü','','genel alan adı'),
 'site:creati':('site','gürültü','','kırık alan adı'),
'name:higgsfield.ai/mcp':('MCP','KUR','','higgsfield MCP; bkz site:higgsfield.ai'),
 'name:docs.firecrawl.dev/mcp-server':('MCP','kurulu','firecrawl-scraper','firecrawl MCP dokümanı; skill kurulu'),
 'name:console.apify.com/store-search':('API-servis','kurulu','mcp:apify','Apify mağazası; MCP kurulu'),
 'name:gitmcp.io/docs':('MCP','KUR','','bkz site:gitmcp.io'),
 'name:cskillry.dev/ai':('site','KUR','','yazım hatası: skillry.dev'),
 'name:skilly.dev/ai':('site','KUR','','yazım hatası: skillry.dev'),
 'name:rivecn.com/courses':('kütüphane','KUR','','bkz site:rivecn.com'),
 'name:github.com/langchain-aiflanggraph':('kütüphane','KUR','','langchain-ai/langgraph (MIT); langgraph skill kurulu, pip proje başı'),
 'name:higgsfield.ai/pricing':('site','gürültü','','fiyat sayfası; bkz site:higgsfield.ai'),
 'name:u8i3yg.abacusai.app/api-docs':('site','gürültü','','tek kullanımlık uygulama dokümanı'),
 'name:github.com/barty':('repo','KUR','','kırpık depo adı (barty/?), doğrulanacak'),
 'name:github.com/data':('site','gürültü','','kırık/genel yol'),
 'name:pixel-aoests':('kavram','gürültü','','kırık metin (pixel assets?)'),
 'name:cwc-makers':('?','KUR','','bilinmiyor, doğrulanacak'),
 'name:math-proof':('?','KUR','','bilinmiyor, doğrulanacak'),
 'gh:ςalesthio/openl':('repo','KUR','','yazım hatası: calesthio/OpenMontage; bkz gh:calesthio/openmontagel'),
 'ghuser:new':('site','gürültü','','kırık yol'),
 'name:muapi.ai/open-gener':('API-servis','KUR','','bilinmiyor, doğrulanacak (kırpık metin)'),
 'name:chatllm-abacus-ai':('API-servis','KUR','','Abacus ChatLLM (ücretli, hesap)')}
out=[];bad=[]
for r in rows:
    k=r['k']
    if k in dec: t,kar,kan,ger=dec[k]
    elif k in EK: t,kar,kan,ger=EK[k]
    elif len(re.sub(r'[^a-z]','',k.split(':',1)[-1].lower()))<3 or k.startswith(('site:com.tr','site:.co','site:xcom','site:ocalhost','site:cacrush','site:candy','vsx:')):
        t,kar,kan,ger='gürültü','gürültü','','kırık/boş metin, araç adı çıkarılamadı'
    else: t,kar,kan,ger='?','KUR','','sınıflanmadı: doğrulanacak'
    if kar=='kurulu' and not (kan in inv or any(e.startswith(kan) for e in inv)): bad.append((k,kan))
    out.append((k,t,r['nv'],';'.join(r['v'][:6]),kar,kan,ger))
print('kanıt yok:',bad)
from collections import Counter
print(Counter(o[4] for o in out),len(out))
w=csv.writer(open('.kos/kopru/rapor/video-kur-1-p1.tsv','w',encoding='utf-8',newline=''),delimiter='\t')
w.writerow(['aday','tür','video_sayısı','kaynak_videolar','karar','kanıt','gerekçe'])
for o in out: w.writerow(o)
print('sınıflanmadı:',[o[0] for o in out if o[1]=='?'])
