# Kurulum turu 3 — birleşik çıktı (tur-3d çift dikiş; kurulum yok)

Girdi: tur3-sonuc-1..6.tsv (717 satır). RED “bulunamadı/404” 240 satır yeniden arandı (gh search, difflib ≥0.75, ★≥50; betik 52 eşleşme verdi, elle doğrulamada 8 gerçek, 44 yanlış pozitif); AYRI-UYGULAMA alt sınıfları: (i) web servisi · (ii) masaüstü · (iii) kendi sunucu/geliştirici uygulaması.

## Özet sayılar

- AYRI-UYGULAMA: 68
- HESAP: 41
- KUR: 5
- KUR-duzeltmeli: 8
- RED: 577
- ZATEN: 18
- AYRI-UYGULAMA alt sınıf: i=28, ii=17, iii=23

## ÖNERİLMEZ

- purpledoubled/locally-uncensored — AGPL-3.0; ÖNERİLMEZ: sansürsüz model yöneticisi (gri alan)
- aiginxuancai/mintimage — LİSANS YOK; ÖNERİLMEZ (kopyalanamaz/kurulamaz)
- cita-777/metapi — Node/Docker; ÖNERİLMEZ: AI relay sitelerini birleştirir (üçüncü taraf anahtar/ToS gri alan)
- ndolestudio/httpsms — Go+PostgreSQL+Android uygulaması; AGPL-3.0; ÖNERİLMEZ: SMS/kişisel veri
- ntgroup/echomimic_ — KURTARILDI → antgroup/echomimic; iii; Apache-2.0 ★4313; GPU modeli; ÖNERİLMEZ: yüz/ses sentezi (kişisel veri/gri alan), GPU yok
- traderalice/oper — KURTARILDI → TraderAlice/OpenAlice; iii; AGPL-3.0 ★7259; AI trading ajanı; ÖNERİLMEZ: finansal hesap/anahtar, gerçek para riski
- xming521/weclone — py+GPU; AGPL-3.0; ÖNERİLMEZ: sohbet geçmişinden dijital ikiz (kişisel veri)

## Masaüstü uygulamaları (ii)

| ad | winget/kaynak | boyut | not |
|---|---|---|---|
| keshav1sharma/browseros-agent | winget BrowserOS.BrowserOS 155.0.8309.26 | 153 MB | AGPL-3.0; Chromium tabanlı tarayıcı, gezinti verisi işler |
| purpledoubled/locally-uncensored | release 3.0.5 x64-setup | 17 MB | AGPL-3.0; ÖNERİLMEZ: sansürsüz model yöneticisi (gri alan) |
| comfyui | winget Comfy.ComfyUI-Desktop 1.1.6 | ? + modeller GB | GPL-3.0; GPU şart; MCP ikinci adım |
| zseven-w/openpencil | winget ZSeven-W.OpenPencil 0.8.4 | 37 MB | MIT |
| openclaw/openclaw-windows-node | release OpenClawCompanion-Setup-x64 v2026.9.8-1 | 122 MB | MIT; winget yok |
| sterll/claude-terminal | npm claude-terminal@1.3.6 / release v1.3.6 | 246 MB | GPL-3.0; winget yok |
| cascadeur.com | msstore XPFMG5VK7FJPXL | ? | ticari; winget kaynağında yok |
| codexu/note-gen | release NoteGen_0.38.2_x64-setup.exe | 15 MB | GPL-3.0; winget yok |
| dmmaze/ballonstranslator | release v1.5.19 win_minium.zip | 31 MB (+modeller) | GPL-3.0; winget yok; telifli manga çevirisi: dikkat |
| jianchang512/pyvideotrans | github.com/jianchang512/pyvideotrans (v4.15) | ? (release dosyası yok) | GPL-3.0; winget yok |
| legeling/prompthub | winget legeling.PromptHub 0.5.9 | ~114 MB | AGPL-3.0; koşulları rapora |
| ollama.com/download | winget Ollama.Ollama 0.40.2 | ~1.5 GB | MIT; yerel LLM çalıştırıcı; telemetri: doğrulanmadı |
| ollama.com/search | winget Ollama.Ollama | ~1.5 GB | katalog sayfası; uygulama aynı |
| opera.com | winget Opera.Opera 137.0.6036.39 | ? (indirici) | Freeware (EULA); tarayıcı, gezinti verisi işler |
| syrizelink/openfic | winget Syrize.OpenFic 0.12.0 | ~118 MB | Apache-2.0 |
| zhouxiaoka/autoclip | release AutoClip.Desktop 1.5.5 x64-setup | 197 MB | MIT; winget yok |
| zseven-w/openpencstime | winget ZSeven-W.OpenPencil 0.8.4 | 37 MB | OCR→openpencil; MIT |

## Tüm satırlar

| ad | sınıf | kaynak | pin/winget | not |
|---|---|---|---|---|
| harry0703/moneyprinterturbo | AYRI-UYGULAMA (iii) | github.com/harry0703/MoneyPrinterTurbo | git clone @ b819f7e1213c (uygulama olarak) | py+Docker/WebUI; LLM anahtarı; ffmpeg |
| claude.com | ZATEN | claude.com |  | Claude hesabı/Claude Code kullanımda |
| airtable | HESAP | github.com/domdomegg/airtable-mcp-server | claude mcp add --scope user airtable -- npx -y airtable-mcp-server@1.14.0 | MIT ★456 push 2026-09-09; npm airtable-mcp-server 1.14.0 |
| netlify.com | HESAP | netlify.com | npm i -g netlify-cli@27.12.0 | URL 200; Netlify hesabı; CLI MIT |
| convex | KUR | github.com/get-convex/agent-skills | ~/.claude/skills/ kopyası @ 2cfe645c87f9 | Apache-2.0 ★65 push 2026-10-01; skill, anahtar gerekmez (convex npm yalnız proje bağımlılığı) |
| microsoft/github-copilot-for-azure | HESAP | github.com/microsoft/GitHub-Copilot-for-Azure | ~/.claude/skills/ kopyası @ f2526ae58149 | ★255 push 2026-10-09; lisans SPDX NOASSERTION (LICENSE dosyası var: kurulumdan önce oku); Azure aboneliği ister |
| remote-control | ZATEN | - |  | Claude Code yerleşik özelliği; kurulacak paket yok |
| developer.chrome.com | RED | developer.chrome.com |  | doküman sitesi (URL 200), kurulacak şey yok |
| platform.claude.com | ZATEN | platform.claude.com |  | Anthropic API konsolu; hesap mevcut |
| openrouter.ai | HESAP | openrouter.ai |  | URL 200; yalnız API, npm paketi yok |
| quickchart.io | RED | quickchart.io |  | anahtarsız HTTP grafik API'si; kurulacak şey yok (typpo/quickchart sunucu kodu ayrı) |
| kie.ai | HESAP | kie.ai |  | URL 200; yalnız API |
| minimax.io | HESAP | minimax.io |  | URL 200; yalnız API |
| upload-post.com | HESAP | upload-post.com |  | URL 200; yalnız API |
| awwwards.com | RED | awwwards.com |  | galeri sitesi, kurulacak şey yok |
| community.n8n.io | RED | community.n8n.io |  | forum, kurulacak şey yok |
| deepseek-ai/eepeekhamness | ZATEN | github.com/deepseek-ai/deepseek-harness |  | OCR bozuk; gerçek repo deepseek-harness MIT ★246332, kurulum-turu-1.md'de HESAP GEREKIR olarak sınıflandı |
| fl/www.trendyol | RED | - |  | bulunamadı (gh api 404; arama yalnız ★0-8 Trendyol MCP'leri, eşleşme doğrulanamaz) |
| imessage | RED | github.com/anipotts/imessage-mcp |  | macOS'a özgü (Messages veritabanı); makine Windows. Referans: MIT ★27 push 2026-10-05 |
| jev/soguk-sais | RED | - |  | bulunamadı (gh api 404, arama boş) |
| keshav1sharma/browseros-agent | AYRI-UYGULAMA (ii) | github.com/browseros-ai/BrowserOS | winget BrowserOS.BrowserOS 155.0.8309.26 · 153 MB | AGPL-3.0; Chromium tabanlı tarayıcı, gezinti verisi işler |
| opencode.ai | AYRI-UYGULAMA (iii) | opencode.ai | npm i -g opencode-ai@1.18.35 | npm i -g opencode-ai@1.18.35; ayrı ajan CLI, MIT |
| research/v23_snowy_elephant | RED | - |  | bulunamadı (gh api 404, arama boş) |
| vscode.dev | RED | vscode.dev |  | web editörü, kapsam dışı |
| zapler.com | AYRI-UYGULAMA (i) | zapler.com |  | URL 200; web servisi, paket/repo bulunamadı; içerik doğrulanmadı |
| docs.kie.ai | HESAP | docs.kie.ai |  | kie.ai dokümanı (aynı API) |
| docs.typesafe.ai | RED | docs.typesafe.ai |  | URL 200 ama paket/repo bulunamadı |
| vercel.com | HESAP | vercel.com | npm i -g vercel@63.1.2 | Vercel hesabı; CLI Apache-2.0 |
| anthropics/claude-code-playground | KUR-duzeltmeli | github.com/anthropics/claude-code-playground | ~/.claude/skills/ kopyası (skills/<ad>) @ 569c5283d9a0 | Apache-2.0 ★177 push 2026-10-08; demo deposu, yalnız skills/ klasörü uygun; skills/ içeriği Tur 3c'de okunmadan kurulmaz |
| console.groq.com | HESAP | console.groq.com |  | Groq hesabı; yalnız API |
| purpledoubled/locally-uncensored | AYRI-UYGULAMA (ii) | github.com/PurpleDoubleD/locally-uncensored | release 3.0.5 x64-setup · 17 MB | AGPL-3.0; ÖNERİLMEZ: sansürsüz model yöneticisi (gri alan) |
| tasteskill.dev | ZATEN | tasteskill.dev |  | taste-skill (MIT) zaten kurulu |
| docs.claude.com | ZATEN | docs.claude.com |  | Anthropic dokümanı, kurulacak şey yok |
| robolabs.so | RED | robolabs.so |  | URL 200 ama paket/repo bulunamadı |
| hermes-agent.nousresearch.com | AYRI-UYGULAMA (i) | hermes-agent.nousresearch.com |  | Hermes Agent: ayrı ajan çerçevesi, CC eklentisi değil |
| pinterest.com | RED | pinterest.com |  | sosyal site, kurulacak şey yok |
| a24.raviklaassens.com | RED | a24.raviklaassens.com |  | kişisel/portfolyo sitesi |
| ackblitz-labs/bolt.diy | AYRI-UYGULAMA (iii) | github.com/stackblitz-labs/bolt.diy | git clone @ 10d94fb8daec | Node 20+/pnpm; LLM anahtarı |
| agent-teams | ZATEN | - |  | Claude Code yerleşik özelliği; kurulacak paket yok |
| agricidaniel/claude-ads | KUR-duzeltmeli | github.com/AgriciDaniel/claude-ads | claude plugin marketplace add AgriciDaniel/claude-ads + install (pin ac2164493391: kurulumdan sonra SHA doğrula) | MIT ★9848 push 2026-10-07; plugin+py betikleri: betik izinleri okunmadan açılmaz; reklam platformu token'ları isteğe bağlı |
| alion/wjtzbodlenpqjrtcpsv | RED | - |  | bulunamadı (anlamsız ad, gh api 404) |
| anthropics/sk111s | ZATEN | github.com/anthropics/skills |  | OCR bozuk; anthropics/skills, example-skills@anthropic-agent-skills kurulu |
| anthropics/sk11ls | ZATEN | github.com/anthropics/skills |  | aynı (OCR bozuk); example-skills@anthropic-agent-skills kurulu |
| app.notion.com | HESAP | app.notion.com |  | Notion hesabı; resmi barındırılan MCP/API |
| app.pocketsflow.com | AYRI-UYGULAMA (i) | app.pocketsflow.com |  | web uygulaması, URL 200 |
| apps/ecc-tools | AYRI-UYGULAMA (i) | github.com/apps/ecc-tools |  | GitHub App (ecc.tools), repo değil; ecc eklentisi zaten kurulu |
| arc/chart.tax | RED | - |  | bulunamadı (gh api 404; arama ilgisiz) |
| besyayt-outpttg/-altina-kaydet-ve | RED | - |  | bulunamadı (OCR parçası, anlamsız) |
| caveman | ZATEN | github.com/JuliusBrussee/caveman |  | Apache-2.0 ★110773 push 2026-10-09 @ 2e08b9177c07; envanterde npm @caveman-ai/cli@1.3.4 kurulu (aynı proje olduğu doğrulanmadı; npm 'caveman |
| cchainpocket.pocketsflow.com/product-video | AYRI-UYGULAMA (i) | chainpocket.pocketsflow.com/product-video |  | pocketsflow alt yolu, URL 200 |
| chatgpt.com | RED | chatgpt.com |  | rakip hizmet, kurulacak şey yok (403) |
| claude-code-curriculum-deploy.vercel.app | RED | claude-code-curriculum-deploy.vercel.app |  | tek müfredat sitesi, kurulacak şey yok |
| claude-code/testing | RED | - |  | bulunamadı (anlamsız ad) |
| comfyui | AYRI-UYGULAMA (ii) | comfyui + artokun/comfyui-mcp | winget Comfy.ComfyUI-Desktop 1.1.6 · ? + modeller GB | GPL-3.0; GPU şart; MCP ikinci adım |
| console.typesafe.ai | RED | console.typesafe.ai |  | URL 403; paket/repo bulunamadı |
| docs.github.com | RED | docs.github.com |  | doküman sitesi |
| draftly.space/3d-builder | RED | - |  | bulunamadı (gh api 404, arama boş) |
| firefox.com | RED | firefox.com |  | tarayıcı, kapsam dışı |
| geminicli.com | AYRI-UYGULAMA (iii) | geminicli.com | npm i -g @google/gemini-cli@0.63.0 | npm i -g @google/gemini-cli@0.63.0; ayrı ajan CLI, Apache-2.0 |
| ghcr.io | RED | ghcr.io |  | kapsayıcı kayıt defteri, kurulacak şey yok |
| h-mmer/pentest-a | RED | - |  | kapsam dışı |
| hand_addiione/point.r | RED | - |  | bulunamadı (gh api 404) |
| hoainho/mg2thr | RED | - |  | bulunamadı (gh api 404; kullanıcı hoainho'nun benzer adlı repo'su yok) |
| hunter | RED | hunter.io |  | doğrulanabilir kaynak yok (Hunter.io MCP repoları ★0; npm 'hunter' boş yer tutucu) |
| iilab-al/peagent | RED | github.com/IILab-AI/PEagent |  | ★26 son push 2025-04-07, lisans/kullanım belirsiz |
| img.ly | HESAP | img.ly |  | URL 200; ticari SDK (lisans anahtarı); kurulum yolu doğrulanmadı |
| interfaces.dev | RED | interfaces.dev |  | URL 200 ama paket/repo bulunamadı |
| ir.minimax.cn | RED | ir.minimax.cn |  | yatırımcı ilişkileri sitesi |
| jev-chat/jev-chat-jarvis | KUR-duzeltmeli | github.com/jev-chat/jev-chat-jarvis | ~/.claude/skills/ kopyası @ fdf8d28c811b | MIT ★7522 push 2026-10-08; kökte cn/ ve global/; hangisi skill olduğu ve izinleri kurulumdan önce okunmalı |
| key.ai | RED | key.ai |  | URL 200 ama paket/repo bulunamadı |
| lovable | RED | github.com/Brad-Cat/lovable-claude-code-skills |  | kaynak zayıf (★1); lovable.dev web uygulaması; npm 'lovable' boş |
| lovable.dev | AYRI-UYGULAMA (i) | lovable.dev |  | web uygulaması (URL 403) |
| mcp.higgsfield.a | RED | mcp.higgsfield.a |  | URL doğrulanamadı (OCR kesik, mcp.higgsfield.ai olabilir); bulunamadı |
| mukul975/anthropic-cybersecurity-skills | RED | - |  | kapsam dışı |
| nsole.apiry.com/sto | RED | - |  | bulunamadı (OCR kesik, bağlantı hatası) |
| omer/omer_vault | RED | - |  | bulunamadı (gh api 404) |
| ongyi-mai/z-image-turbo | RED | Tongyi-MAI/Z-Image-Turbo |  | bulunamadı (GitHub'da yok; model GPU ister) |
| param-shankar/hiervue-ai-interviewer | RED | github.com/Param-shankar/Hiervue-AI-Interviewer- |  | ★3 son push 2024-04-21, lisans yok |
| quickmagic.ai/home | AYRI-UYGULAMA (i) | quickmagic.ai |  | web uygulaması, URL 200 |
| reactbits.dev | RED | reactbits.dev |  | React bileşen kitaplığı, skill/MCP değil |
| remotion-dev/element-p | RED | - |  | bulunamadı (gh api 404) |
| remotion-dev/ski1ls | ZATEN | github.com/remotion-dev/skills |  | OCR bozuk; remotion-* skill'leri envanterde (12 adet) kurulu; lisans SPDX yok (★4961) |
| replit.com | AYRI-UYGULAMA (i) | replit.com |  | web IDE |
| schemastore/schemastore | RED | github.com/SchemaStore/schemastore |  | Apache-2.0 ★3855; JSON şema veri deposu, kurulacak araç değil |
| sent.dm | HESAP | sent.dm |  | URL 200; mesajlaşma API'si |
| sponsors/leonxlnx | RED | - |  | GitHub Sponsors sayfası, repo değil |
| stripe.com | HESAP | stripe.com | npm i stripe@23.0.0 (proje bağımlılığı) | Stripe hesabı; SDK MIT |
| tastecode.dev | RED | tastecode.dev |  | URL 200 ama paket/repo bulunamadı |
| ts.ai | RED | ts.ai |  | URL 200 ama paket/repo bulunamadı |
| tt-a1i/archify | KUR | github.com/tt-a1i/archify | ~/.claude/skills/ kopyası @ 7f483b61e8f6 | MIT ★81166 push 2026-10-09; diyagram skill'i; SKILL.md yolunu kopyalamadan önce doğrula |
| v0.app | AYRI-UYGULAMA (i) | v0.app |  | Vercel web uygulaması |
| xoogler.key.ai | RED | xoogler.key.ai |  | URL 200 ama paket/repo bulunamadı |
| zseven-w/openpencil | AYRI-UYGULAMA (ii) | github.com/ZSeven-W/openpencil | winget ZSeven-W.OpenPencil 0.8.4 · 37 MB | MIT |
| canvasui.dev | RED | canvasui.dev |  | URL 200 ama paket/repo bulunamadı |
| gunlukmenu.com | RED | gunlukmenu.com |  | tek site, kurulacak şey yok |
| docs.fal.ai | HESAP | docs.fal.ai | npm i @fal-ai/client@1.10.1 (proje bağımlılığı) | fal hesabı; npm @fal-ai/client MIT |
| docs.stripe.com | HESAP | docs.stripe.com |  | stripe.com ile aynı |
| kimaki.dev | RED | kimaki.dev |  | URL 200 ama paket/repo bulunamadı |
| tldraw.com | AYRI-UYGULAMA (i) | tldraw.com |  | web çizim uygulaması |
| app.lumalabs.ai | HESAP | app.lumalabs.ai |  | Luma hesabı; web uygulaması |
| openship.io | AYRI-UYGULAMA (i) | openship.io |  | URL 200; web servisi, paket/repo bulunamadı |
| omarchy.org | RED | omarchy.org |  | Linux dağıtımı, kapsam dışı |
| docs.anchorbrowser.io | HESAP | docs.anchorbrowser.io |  | URL 200; API hesabı |
| gist.github.com | RED | gist.github.com |  | GitHub gist sitesi |
| knadh/listmonk | AYRI-UYGULAMA (iii) | github.com/knadh/listmonk | sabit @ 82db22ce7a06 | Go binary/Docker + PostgreSQL; AGPL-3.0 |
| cal.com | AYRI-UYGULAMA (i) | cal.com |  | web takvim uygulaması |
| docs.inference.net | HESAP | docs.inference.net |  | URL 200; API hesabı |
| lordicon.com | AYRI-UYGULAMA (i) | lordicon.com |  | animasyonlu simge servisi (web) |
| platform.minimax.cn | HESAP | platform.minimax.cn |  | minimax API konsolu |
| releases.ubuntu.com | RED | releases.ubuntu.com |  | ISO indirme sitesi |
| supabase.com | ZATEN | supabase.com |  | supabase eklentisi ve MCP bağlı |
| code.visualstudio.com | RED | code.visualstudio.com |  | editör, kapsam dışı |
| docs.httpsms.com | HESAP | docs.httpsms.com |  | URL 200; SMS API hesabı |
| arena.ai | AYRI-UYGULAMA (i) | arena.ai |  | model karşılaştırma web sitesi |
| artificialanalysis.ai | RED | artificialanalysis.ai |  | benchmark sitesi, kurulacak şey yok |
| ccsub.net | RED | ccsub.net |  | URL 200 ama paket/repo bulunamadı |
| cdn.jsdelivr.net | RED | cdn.jsdelivr.net |  | CDN, kurulacak şey yok |
| citevue.com | AYRI-UYGULAMA (i) | citevue.com |  | URL 200; web servisi, paket/repo bulunamadı |
| davila7/claude-code-templates | KUR-duzeltmeli | github.com/davila7/claude-code-templates | claude plugin marketplace add davila7/claude-code-templates + install (pin a34435945926: kurulumdan sonra SHA doğrula) | MIT ★32502 push 2026-10-09; plugin+npm 1.29.7; CLI analitik/telemetri içerebilir: kaynakta ara ve kapat, .mcp.json ve .env.example izinlerin |
| docs.openclaw.ai | AYRI-UYGULAMA (i) | docs.openclaw.ai |  | OpenClaw ayrı ajan, CC eklentisi değil |
| docs.pocketsflow.com | RED | docs.pocketsflow.com |  | servis/site (URL 200), kurulacak paket yok |
| docs.upload-post.com | RED | docs.upload-post.com |  | servis/site (URL 200), kurulacak paket yok |
| firecrawl/firecrawl-docs | RED | github.com/firecrawl/firecrawl-docs |  | ★99 push 2026-10-09 lisans yok; dokümantasyon deposu, kurulacak şey yok; Firecrawl CLI/eklenti zaten kurulum-turu-1'de HESAP |
| instacart/snacks | RED | github.com/instacart/snacks |  | Apache-2.0 ★82 push 2025-05-30; Instacart React bileşen kütüphanesi (ic-snacks), skill/eklenti değil |
| newbondlab.com | RED | newbondlab.com |  | servis/site (URL 200), kurulacak paket yok |
| openclaw/openclaw-windows-node | AYRI-UYGULAMA (ii) | github.com/openclaw/openclaw-windows-node | release OpenClawCompanion-Setup-x64 v2026.9.8-1 · 122 MB | MIT; winget yok |
| physicsteachermomma.com | RED | physicsteachermomma.com |  | servis/site (URL 200), kurulacak paket yok |
| roadtoglobal.org | RED | roadtoglobal.org |  | servis/site (URL 200), kurulacak paket yok |
| selenium.dev | RED | selenium.dev |  | doküman sitesi (URL 200); tarayıcı otomasyonu için playwright zaten var |
| sterll/claude-terminal | AYRI-UYGULAMA (ii) | github.com/sterll/claude-terminal | npm claude-terminal@1.3.6 / release v1.3.6 · 246 MB | GPL-3.0; winget yok |
| wavespeed.ai | HESAP | wavespeed.ai |  | WaveSpeed görsel/video API servisi (URL 200); paket doğrulanmadı |
| 10web.io/website-builder | RED | 10web.io/website-builder |  | bulunamadı: URL açılmadı (404) |
| 127.0.0.:3080 | RED | 127.0.0.:3080 |  | bulunamadı: URL açılmadı (ERR) |
| 127.0.8.1:5173 | RED | 127.0.8.1:5173 |  | bulunamadı: URL açılmadı (ERR) |
| 127.o.o.1:4343.you | RED | 127.o.o.1:4343.you |  | bulunamadı: URL açılmadı (ERR) |
| 1ss/1o8 | RED | github.com/1ss/1o8 |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 247.cappenlabs.com.br | RED | 247.cappenlabs.com.br |  | servis/site (URL 200), kurulacak paket yok |
| 2sgithub.com/mirayatech | RED | 2sgithub.com/mirayatech |  | bulunamadı: URL açılmadı (ERR) |
| 310.0k/1.0m | RED | github.com/310.0k/1.0m |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 320.0k/1.0m | RED | github.com/320.0k/1.0m |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 350-creatives/channel | RED | github.com/350-creatives/channel |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 350-creatives/transcri | RED | github.com/350-creatives/transcri |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 4.9k/month | RED | github.com/4.9k/month |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 40.0k/1.0m | RED | github.com/40.0k/1.0m |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 60.0k/1.0m | RED | github.com/60.0k/1.0m |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 90c-4555-98de-43ee44a6adef/scratchpad | RED | github.com/90c-4555-98de-43ee44a6adef/scratchpad |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| 90s/irving | RED | github.com/90s/irving |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| abaaesthetic.com | RED | abaaesthetic.com |  | bulunamadı: URL açılmadı (ERR) |
| abatable.com | RED | abatable.com |  | servis/site (URL 200), kurulacak paket yok |
| ably.com | RED | ably.com |  | servis/site (URL 200), kurulacak paket yok |
| aboutamazon.com | RED | aboutamazon.com |  | servis/site (URL 200), kurulacak paket yok |
| acme/order-service | RED | github.com/acme/order-service |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| acme/submissions-apl | RED | github.com/acme/submissions-apl |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| activecampaign | RED | - |  | bulunamadı: resmi skill/MCP yok; npm activecampaign@1.2.5 eski API sarmalayıcı SDK |
| adamjelley.github.io | RED | adamjelley.github.io |  | servis/site (URL 200), kurulacak paket yok |
| addilone/polnt.r | RED | github.com/addilone/polnt.r |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| adele.uxpin.com | RED | adele.uxpin.com |  | servis/site (URL 200), kurulacak paket yok |
| adobe-for-creativity | HESAP | - | /plugin install adobe-for-creativity@claude-plugins-official | claude-plugins-official pazaryeri listesinde mevcut (ad doğrulandı, içerik/lisans doğrulanmadı); Adobe hesabı ister |
| aerr/esterecties.tet | RED | github.com/aerr/esterecties.tet |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| agent.minimax.cn | RED | agent.minimax.cn |  | servis/site (URL 200), kurulacak paket yok |
| agsfield.ai/mcp | RED | agsfield.ai/mcp |  | bulunamadı: URL açılmadı (ERR) |
| ai.google.dev | HESAP | ai.google.dev |  | Gemini API doküman/anahtar sitesi (URL 200); tek başına kurulacak paket yok, Gemini API anahtarı gerekirse HESAP |
| ai.studio | RED | ai.studio |  | servis/site (URL 200), kurulacak paket yok |
| aiginxuancai/mintimage | AYRI-UYGULAMA (iii) | github.com/aiginxuancai/mintimage | git clone lisans netleşince (kod kopyalama yok) | LİSANS YOK; ÖNERİLMEZ (kopyalanamaz/kurulamaz) |
| aixploria.com | RED | aixploria.com |  | servis/site (URL 200), kurulacak paket yok |
| alibaba/open-code-review | HESAP | github.com/alibaba/open-code-review | npm i -g @alibaba-group/open-code-review@1.12.13 (repo @ fabbdb296b0d); eklenti: plugins/open-code-review/README.md#claude-code | Apache-2.0 ★45173 push 2026-10-08; Go CLI `ocr` + CC eklentisi (plugins/open-code-review, .claude-plugin); LLM sağlayıcı anahtarı ister; ins |
| allaboutcookies.org | RED | allaboutcookies.org |  | servis/site (URL 403), kurulacak paket yok |
| amandabraga.com | RED | amandabraga.com |  | servis/site (URL 200), kurulacak paket yok |
| amazon.jobs | RED | amazon.jobs |  | servis/site (URL 200), kurulacak paket yok |
| amazon.science | RED | amazon.science |  | servis/site (URL 200), kurulacak paket yok |
| anara.com | RED | anara.com |  | servis/site (URL 200), kurulacak paket yok |
| angles/sub-questions | RED | github.com/angles/sub-questions |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| animationworkshop.via.dk | RED | animationworkshop.via.dk |  | servis/site (URL 200), kurulacak paket yok |
| anthropic-ai/claude-agent-sdk-win32-x64 | RED | github.com/anthropic-ai/claude-agent-sdk-win32-x64 |  | GitHub deposu yok (404); npm platform ikilisi @anthropic-ai/claude-agent-sdk bağımlılığı, tek başına kurulmaz |
| anthropic/claude-opus-5.5 | RED | github.com/anthropic/claude-opus-5.5 |  | bulunamadı: model adı, repo yok (404) |
| anthropic/claude-sonnet-5 | RED | github.com/anthropic/claude-sonnet-5 |  | bulunamadı: model adı, repo yok (404) |
| anthropics/claude-plugins-community | RED | github.com/anthropics/claude-plugins-community |  | Apache-2.0 ★4600 push 2026-10-05; salt-okunur topluluk pazaryeri aynası: kurulacak tek şey yok, her eklenti ayrı aday olarak değerlendirilir |
| anthropics/sk1lls | RED | github.com/anthropics/sk1lls |  | bulunamadı (404): OCR bozuk ad |
| antigravity.google | AYRI-UYGULAMA (i) | antigravity.google |  | Google Antigravity IDE (URL 200), CC eklentisi değil |
| antihub-project/antigv-plugin | RED | github.com/antihub-project/antigv-plugin |  | AntiHub-Project/Antigv-plugin ★33 push 2026-02-26; lisans NOASSERTION; Antigravity→OpenAI vekil sunucusu (hesap belirteci aktarımı), CC ekle |
| api-inference.modelscope.ai | RED | api-inference.modelscope.ai |  | bulunamadı: URL açılmadı (404) |
| api.htpsms.com | RED | api.htpsms.com |  | bulunamadı: URL açılmadı (ERR) |
| api.openaf. | RED | api.openaf. |  | bulunamadı: URL açılmadı (ERR) |
| api.siliconflow.en | RED | api.siliconflow.en |  | bulunamadı: URL açılmadı (ERR) |
| api.together.ai | HESAP | api.together.ai |  | Together AI API (URL 200); eklenti değil, API anahtarlı servis |
| apify/instagram-reel-scraper | RED | github.com/apify/instagram-reel-scraper |  | bulunamadı: GitHub deposu yok (Apify mağaza aktörü, 404) |
| apihub.agnes-ai.com/v1 | RED | apihub.agnes-ai.com/v1 |  | bulunamadı: URL açılmadı (404) |
| app.brantial.ai/2344joverview | RED | app.brantial.ai/2344joverview |  | bulunamadı: URL açılmadı (404) |
| app.emergent.sh/home | RED | app.emergent.sh/home |  | web uygulaması (vibe-coding servisi), URL 200; CC eklentisi/CLI doğrulanmadı |
| app.n8n-mcp.com | ZATEN | app.n8n-mcp.com |  | n8n-mcp (czlonkowski/n8n-mcp MIT ★23052) kurulum-turu-1'de HESAP olarak kayıtlı; bu satır barındırılan servis |
| app.notion.com/chat | RED | app.notion.com/chat |  | Notion giriş/OAuth alt yolu (URL 200); Notion MCP (mcp.notion.com) envanterde ayrı kayıtlı |
| app.notion.com/login | RED | app.notion.com/login |  | Notion giriş/OAuth alt yolu (URL 200); Notion MCP (mcp.notion.com) envanterde ayrı kayıtlı |
| app.notion.com/oauth2callback | RED | app.notion.com/oauth2callback |  | Notion giriş/OAuth alt yolu (URL 200); Notion MCP (mcp.notion.com) envanterde ayrı kayıtlı |
| app.notion.com/onboarding | RED | app.notion.com/onboarding |  | Notion giriş/OAuth alt yolu (URL 200); Notion MCP (mcp.notion.com) envanterde ayrı kayıtlı |
| app.notion.com/signup | RED | app.notion.com/signup |  | Notion giriş/OAuth alt yolu (URL 200); Notion MCP (mcp.notion.com) envanterde ayrı kayıtlı |
| app.notion.com/verifynopopupblockerhtmlandredirect | RED | app.notion.com/verifynopopupblockerhtmlandredirect |  | Notion giriş/OAuth alt yolu (URL 200); Notion MCP (mcp.notion.com) envanterde ayrı kayıtlı |
| app.omagic.ai | RED | app.omagic.ai |  | servis/site (URL 200), kurulacak paket yok |
| app.upload-post.com/api-keys | RED | app.upload-post.com/api-keys |  | Upload-Post servis paneli (URL 200); resmi CC paketi doğrulanmadı |
| arc/bashboard.tax | RED | github.com/arc/bashboard.tax |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| arcade.dev | HESAP | arcade.dev |  | Arcade MCP/araç ağ geçidi servisi (URL 200); paket doğrulanmadı |
| arculus.cappenlabs.com.br | RED | arculus.cappenlabs.com.br |  | servis/site (URL 200), kurulacak paket yok |
| ark.cn-beijing.volces.com | RED | ark.cn-beijing.volces.com |  | servis/site (URL 401), kurulacak paket yok |
| articleforge.com | RED | articleforge.com |  | servis/site (URL 200), kurulacak paket yok |
| artstation.com | RED | artstation.com |  | servis/site (URL 403), kurulacak paket yok |
| arxiyorg | RED | - |  | bulunamadı: OCR bozuk ad, kaynak bulunamadı |
| astra.grandviewresearch.com | RED | astra.grandviewresearch.com |  | servis/site (URL 200), kurulacak paket yok |
| astral.st | RED | astral.st |  | bulunamadı: URL açılmadı (ERR) |
| audience/performance | RED | github.com/audience/performance |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| aut.ac.nz | RED | aut.ac.nz |  | servis/site (URL 403), kurulacak paket yok |
| auth0 | HESAP | - | claude mcp add auth0 -- npx -y @auth0/auth0-mcp-server@0.1.0-beta.19 run (repo @ 10390b40dc48); beta: kurmadan önce izin kapsamını gözden ge | auth0/auth0-mcp-server MIT ★122 push 2026-10-06; npm @auth0/auth0-mcp-server yalnız 0.1.0-beta.19 (beta): yönetim API'sine erişir, geniş yet |
| autodownload/profile_downloads | RED | github.com/autodownload/profile_downloads |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| automationorbit.com | RED | automationorbit.com |  | servis/site (URL 200), kurulacak paket yok |
| b0o/schemastore.nvim | RED | github.com/b0o/schemastore.nvim |  | Apache-2.0 ★1040; Neovim eklentisi, CC ile ilgisiz |
| base-ui.21st.dev | RED | base-ui.21st.dev |  | 21st.dev bileşen sitesi; 21st MCP envanterde kayıtlı |
| basketikun/infinite-canvas | AYRI-UYGULAMA (iii) | github.com/basketikun/infinite-canvas | git clone @ dab19adc0847 (uygulama olarak) | Node; üretim sağlayıcı anahtarları |
| bei/code-frome | RED | github.com/bei/code-frome |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| bing.com | RED | bing.com |  | arama motoru sitesi, kurulacak şey yok |
| birthandbondbysheethal.com | RED | birthandbondbysheethal.com |  | servis/site (URL 200), kurulacak paket yok |
| blotato.com | RED | blotato.com |  | servis/site (URL 200), kurulacak paket yok |
| boards.greenhouse.lo | RED | boards.greenhouse.lo |  | bulunamadı: URL açılmadı (ERR) |
| brandmark.io | RED | brandmark.io |  | servis/site (URL 200), kurulacak paket yok |
| browser-use/brow | AYRI-UYGULAMA (iii) | github.com/browser-use/brow | sabit @ c75e8476e26d | KURTARILDI → browser-use/browser-use; iii; MIT ★117430; py kütüphane/ajan, LLM anahtarı ister |
| browser-use/brows | AYRI-UYGULAMA (iii) | github.com/browser-use/brows | sabit @ c75e8476e26d | KURTARILDI → browser-use/browser-use; iii; MIT ★117430; py kütüphane/ajan, LLM anahtarı ister |
| browser-use/jev-ultrafast | AYRI-UYGULAMA (iii) | github.com/browser-use/jev-ultrafast | git clone @ 1231850a0bf1 (uygulama olarak) | py 3.11+; LLM anahtarı |
| bs-393/ai-labs-claude-skills | KUR-duzeltmeli | github.com/bs-393/ai-labs-claude-skills | sabit @ 1a12bc7aadcc | KURTARILDI → ailabs-393/ai-labs-claude-skills; MIT ★455 push 2025-11 (bayat); packages/ skill'lerini elle kopyala, install-skills.mjs okunma |
| bspcertification.org | RED | bspcertification.org |  | servis/site (URL 200), kurulacak paket yok |
| build.nvidia.com/models | RED | build.nvidia.com/models |  | NVIDIA model kataloğu sitesi (URL 200), kurulacak şey yok |
| buildmyagent.io | RED | buildmyagent.io |  | servis/site (URL 200), kurulacak paket yok |
| builtkindly.com | RED | builtkindly.com |  | servis/site (URL 200), kurulacak paket yok |
| c./program | RED | github.com/c./program |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| c440.0k/1.0m | RED | github.com/c440.0k/1.0m |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| canva.com | HESAP | canva.com | claude mcp add --transport http canva https://mcp.canva.com/mcp (OAuth) | Canva hesabı; mcp.canva.com/mcp 401 döndü (uç var, OAuth ister); paket/lisans doğrulanmadı |
| canvas-ui/particle-reveal-react | RED | github.com/canvas-ui/particle-reveal-react |  | bulunamadı: GitHub 404, arama uygun sonuç vermedi (OCR bozuk ad) |
| caoa.com.br | RED | caoa.com.br |  | servis/site (URL 200), kurulacak paket yok |
| cappen.com | RED | cappen.com |  | servis/site (URL 200), kurulacak paket yok |
| careers.gogle.com | RED | careers.gogle.com |  | bulunamadı: URL açılmadı (ERR) |
| cartoonitalia.it | RED | cartoonitalia.it |  | servis/site (URL 200), kurulacak paket yok |
| cascadeur.com | AYRI-UYGULAMA (ii) | cascadeur.com | msstore XPFMG5VK7FJPXL · ? | ticari; winget kaynağında yok |
| casky.ai | RED | casky.ai |  | servis/site (URL 200), kurulacak paket yok |
| catsgym.com | RED | catsgym.com |  | servis/site (URL 200), kurulacak paket yok |
| cfpb/capital-framework | RED | github.com/cfpb/capital-framework |  | RED: arşivli (archived=true), son push 2020-07, CC0 UI çerçevesi; Claude aracı değil |
| chainpocket.pocketsflow.com | RED | chainpocket.pocketsflow.com |  | servis/site (URL 200), kurulacak paket yok |
| channel/conversation | RED | github.com/channel/conversation |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| chaos.com | RED | chaos.com |  | servis/site (URL 200), kurulacak paket yok |
| chartjs.org | RED | chartjs.org |  | servis/site (URL 200), kurulacak paket yok |
| checkout/page.tax | RED | github.com/checkout/page.tax |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| chromedevtools/chrome-devtox | RED | github.com/chromedevtools/chrome-devtox |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| circleback | RED |  |  | RED: bulunamadı: tek aday IagoElion/circleback-mcp-server 0★ üçüncü taraf, resmi kaynak doğrulanamadı |
| cita-777/metapi | AYRI-UYGULAMA (iii) | github.com/cita-777/metapi | uygulama: repo klonu @ 88634b0d7207 (ayrı çalıştırma) | Node/Docker; ÖNERİLMEZ: AI relay sitelerini birleştirir (üçüncü taraf anahtar/ToS gri alan) |
| claims-ani/toctc | RED | github.com/claims-ani/toctc |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| claims-ani/tocts | RED | github.com/claims-ani/tocts |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| claude-code-website-design/temporary | RED | github.com/claude-code-website-design/temporary |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| claude-mcp-list | RED |  |  | RED: bulunamadı: tek bir araç değil, 'awesome' liste adı (composio-community/awesome-claude-plugins vb.); kurulacak paket yok |
| claude.a | RED | claude.a |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| claude.aj/settings | RED | github.com/claude.aj/settings |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| clickhouse | HESAP |  | uv tool install mcp-clickhouse==0.7.0 (repo @ d21fe75a6f09; sürümü kurulumdan sonra doğrula) | resmi ClickHouse/mcp-clickhouse, Apache-2.0, 883★, push 2026-10-06, PyPI mcp-clickhouse 0.7.0; ClickHouse sunucusu/hesabı gerekir; ekleme mc |
| cnam.fr | RED | cnam.fr |  | servis/site (URL 200), kurulacak paket yok |
| codexu/note-gen | AYRI-UYGULAMA (ii) | github.com/codexu/note-gen | release NoteGen_0.38.2_x64-setup.exe · 15 MB | GPL-3.0; winget yok |
| codity.ai | RED | codity.ai |  | servis/site (URL 200), kurulacak paket yok |
| colab.google | RED | colab.google |  | servis/site (URL 200), kurulacak paket yok |
| community.quickchart.io | RED | community.quickchart.io |  | servis/site (URL 200), kurulacak paket yok |
| console.clyouthe | RED | console.clyouthe |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| contrib/add-host | RED | github.com/contrib/add-host |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| control-center/con | RED | github.com/control-center/con |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| controlrigmoduwmodtaes/med-tes | RED | github.com/controlrigmoduwmodtaes/med-tes |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| convaiinnovations/laya | RED | github.com/convaiinnovations/laya |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| corona-partners.com | RED | corona-partners.com |  | servis/site (bot engeli 406), kurulacak paket yok |
| cotis-dev/otis-dev-ff | RED | github.com/cotis-dev/otis-dev-ff |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| cp.23/vlaydrat | RED | github.com/cp.23/vlaydrat |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| create-video@latest | AYRI-UYGULAMA (iii) |  | npx create-video@4.0.534 (proje başında tek seferlik) | npx create-video@4.0.534; Remotion lisansı (şirket koşulu) |
| creativeocean.com | RED | creativeocean.com |  | servis/site (URL 200), kurulacak paket yok |
| creativeskillnet.ie | RED | creativeskillnet.ie |  | servis/site (URL 200), kurulacak paket yok |
| creatorstoolbox.com/most-popular-resources | RED | creatorstoolbox.com/most-popular-resources |  | servis/site (URL 200), kurulacak paket yok |
| creditgenie.com | RED | creditgenie.com |  | servis/site (URL 200), kurulacak paket yok |
| cskool.com/ai-profit-lab | RED | cskool.com/ai-profit-lab |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| cskool.com/aiworkshop | RED | cskool.com/aiworkshop |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| ctdocuments/reallusi | RED | github.com/ctdocuments/reallusi |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| customjanimation/motionivideotomotion | RED | github.com/customjanimation/motionivideotomotion |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| d3/vega | RED | github.com/d3/vega |  | KURTARILDI → vega/vega; BSD-3 ★12015; JS grafik kütüphanesi, Claude aracı değil |
| d8j0ntlcm91z4.cl.oudfront.net | RED | d8j0ntlcm91z4.cl.oudfront.net |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| danielravina/steml | RED | github.com/danielravina/steml |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| dash/confia.ison | RED | github.com/dash/confia.ison |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| dashboard.composio.dev | RED | dashboard.composio.dev |  | servis/site (URL 200), kurulacak paket yok |
| dashboard.n8n-mcp.com | RED | dashboard.n8n-mcp.com |  | servis/site (URL 200), kurulacak paket yok |
| dashboard.render.com | RED | dashboard.render.com |  | servis/site (URL 200), kurulacak paket yok |
| dashboard.stripe.com | RED | dashboard.stripe.com |  | servis/site (URL 200), kurulacak paket yok |
| dashboard.stripe.com/coupons | RED | dashboard.stripe.com/coupons |  | servis/site (URL 200), kurulacak paket yok |
| dashboard.stripe.com/products | RED | dashboard.stripe.com/products |  | servis/site (URL 200), kurulacak paket yok |
| datadog | HESAP |  | mcp: repo klonu, SHA kurulumda alınacak (datadog-labs/mcp-server) | datadog-labs/mcp-server (resmi organizasyon), MIT, 45★, push 2026-09-25; npm @datadog/mcp-server yok; Datadog hesabı gerekir; sürüm/SHA kuru |
| date/party-size | RED | github.com/date/party-size |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| davidlubofsky.com | RED | davidlubofsky.com |  | servis/site (URL 200), kurulacak paket yok |
| de.ai/new | RED | de.ai/new |  | servis/site (URL 200), kurulacak paket yok |
| dealnews.com | RED | dealnews.com |  | servis/site (URL 200), kurulacak paket yok |
| decentralizedfuture.xyz | RED | decentralizedfuture.xyz |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| deepseek-ai/dsh-client-ui | RED | github.com/deepseek-ai/dsh-client-ui |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| deepseek-ai/dsh-system-prompt | RED | github.com/deepseek-ai/dsh-system-prompt |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| deepseek.com | RED | deepseek.com |  | servis/site (URL 200), kurulacak paket yok |
| demo.playwright.dev | RED | demo.playwright.dev |  | RED: bulunamadı (URL erişilemez: ERR 404) |
| demodesk.com | RED | demodesk.com |  | servis/site (URL 200), kurulacak paket yok |
| depreciation/amortization | RED | github.com/depreciation/amortization |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| depseek-a/deepseek-amess | RED | github.com/depseek-a/deepseek-amess |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| dermeaclinic.com | RED | dermeaclinic.com |  | servis/site (URL 200), kurulacak paket yok |
| design.minimax.cn | RED | design.minimax.cn |  | servis/site (URL 200), kurulacak paket yok |
| designrocket.io | RED | designrocket.io |  | servis/site (URL 200), kurulacak paket yok |
| desyayroutputs/altinak | RED | github.com/desyayroutputs/altinak |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| desyaytoutptts/-altine-kaydet-ve-dortk | RED | github.com/desyaytoutptts/-altine-kaydet-ve-dortk |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| desyaytoutputs/altine-kayelet-ve-dorul | RED | github.com/desyaytoutputs/altine-kayelet-ve-dorul |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| developer.royalcanin.com | RED | developer.royalcanin.com |  | servis/site (URL 200), kurulacak paket yok |
| developers.googleblog.com | RED | developers.googleblog.com |  | servis/site (URL 200), kurulacak paket yok |
| dhh.dk | RED | dhh.dk |  | servis/site (URL 200), kurulacak paket yok |
| dimartarmizi/omn | RED | github.com/dimartarmizi/omn |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| discord.supabase.com | RED | discord.supabase.com |  | servis/site (URL 200), kurulacak paket yok |
| discuss.ai.google.dev | RED | discuss.ai.google.dev |  | servis/site (URL 200), kurulacak paket yok |
| dmmaze/ballonstranslator | AYRI-UYGULAMA (ii) | github.com/dmmaze/ballonstranslator | release v1.5.19 win_minium.zip · 31 MB (+modeller) | GPL-3.0; winget yok; telifli manga çevirisi: dikkat |
| docs.arcade.dev | RED | docs.arcade.dev |  | servis/site (URL 200), kurulacak paket yok |
| docs.file.ai | RED | docs.file.ai |  | servis/site (URL 200), kurulacak paket yok |
| docs.go..it7usp=driv | RED | docs.go..it7usp=driv |  | RED: bulunamadı (URL erişilemez: ERR UnicodeError) |
| docs.google.. | RED | docs.google.. |  | RED: bulunamadı (URL erişilemez: ERR UnicodeError) |
| docs.microsoft.com | RED | docs.microsoft.com |  | servis/site (URL 200), kurulacak paket yok |
| docs.netlify.com | RED | docs.netlify.com |  | servis/site (URL 200), kurulacak paket yok |
| docs.pafiling | RED | docs.pafiling |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| docs.skyvern.com | RED | docs.skyvern.com |  | servis/site (URL 200), kurulacak paket yok |
| doi.oro | RED | doi.oro |  | RED: bulunamadı (URL erişilemez: ERR URLError) |
| doing/install.s | RED | github.com/doing/install.s |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| domaiyoucgetilbuilst-ingi/gdm | RED | github.com/domaiyoucgetilbuilst-ingi/gdm |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| dorukyalcinsoy.com/my | RED | dorukyalcinsoy.com/my |  | RED: bulunamadı (URL erişilemez: ERR 404) |
| drafly/d-e | RED | github.com/drafly/d-e |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| dream-num/univer | RED | github.com/dream-num/univer |  | RED: Apache-2.0, 22508★, push 2026-10-09; ofis (tablo/doc/slayt) JS kütüphanesi, kurulacak skill/MCP yok; ürün geliştirirken npm bağımlılığı |
| dropbox | RED |  |  | RED: bulunamadı: resmi Dropbox MCP yok; tek aday ngs/dropbox-mcp-server 7★ üçüncü taraf OAuth belirteci ister |
| dropbox/scooter | RED | github.com/dropbox/scooter |  | RED: SCSS UI çerçevesi, son push 2022-08, lisans NOASSERTION; Claude aracı değil |
| dspjobhub.com | RED | dspjobhub.com |  | servis/site (URL 200), kurulacak paket yok |
| e-projects/ai-video | RED | github.com/e-projects/ai-video |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| e-sutomao/026-03-29-firecravi-ci-reseach | RED | github.com/e-sutomao/026-03-29-firecravi-ci-reseach |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| edolus.com | RED | edolus.com |  | servis/site (URL 200), kurulacak paket yok |
| eds-js/reoct | RED | github.com/eds-js/reoct |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| eepbeepmeep/yuegp | RED | github.com/eepbeepmeep/yuegp |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| eloialonso.github.io | RED | eloialonso.github.io |  | servis/site (URL 200), kurulacak paket yok |
| eloialonso/diamond | RED | github.com/eloialonso/diamond |  | RED: MIT, 2114★, son push 2024-12; RL/difüzyon araştırma kodu (GPU eğitimi), Claude aracı değil |
| eloistree/2024_03_19_hackwowgroup | RED | github.com/eloistree/2024_03_19_hackwowgroup |  | RED: 0★, lisans yok, hackathon not deposu; araç değil |
| email/andoutreach | RED | github.com/email/andoutreach |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| emanueleielo/junie-system-prompt | RED | github.com/emanueleielo/junie-system-prompt |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| emergent.sh | RED | emergent.sh |  | servis/site (URL 200), kurulacak paket yok |
| emp0.com | RED | emp0.com |  | servis/site (URL 200), kurulacak paket yok |
| en.aau.dk | RED | en.aau.dk |  | servis/site (URL 200), kurulacak paket yok |
| engineering/academic | RED | github.com/engineering/academic |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| eom/codeeraterfeads-findertm1angsirg | RED | github.com/eom/codeeraterfeads-findertm1angsirg |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| erictechpro/social-invest | RED | github.com/erictechpro/social-invest |  | RED: 3★, lisans yok (yalnız kişisel kullanım, kopyalanmaz); yatırım fenomeni takip uygulaması, olgunluk düşük |
| etollaindcss/tyoc | RED | github.com/etollaindcss/tyoc |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| evals.typesafe.ai | RED | evals.typesafe.ai |  | servis/site (URL 200), kurulacak paket yok |
| everything-claude-code | ZATEN |  |  | affaan-m/ECC (MIT, 275955★, push 2026-10-09) zaten ecc eklentisi olarak kurulu |
| examples/-anditethandlesbenchmark | RED | github.com/examples/-anditethandlesbenchmark |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| experiments.thisiswhitespace.com | RED | experiments.thisiswhitespace.com |  | servis/site (URL 200), kurulacak paket yok |
| fal-ai/fal | RED | github.com/fal-ai/fal |  | RED: Apache-2.0, 965★, push 2026-10-09; Python SDK/sunucusuz ML platformu, Claude aracı değil; kullanılırsa FAL_KEY hesabı gerekir |
| fal-ai/fal-dart | RED | github.com/fal-ai/fal-dart |  | RED: MIT, 12★, son push 2024-09; Dart/Flutter istemci SDK'sı, araç değil |
| fal-ai/fal-java | RED | github.com/fal-ai/fal-java |  | RED: MIT, 15★, son push 2024-09; JVM istemci SDK'sı, araç değil |
| fal-ai/fal-js | RED | github.com/fal-ai/fal-js |  | RED: MIT, 187★, push 2026-10-07; JS istemci SDK'sı (kütüphane), skill/MCP değil; kullanılırsa HESAP FAL_KEY |
| fal-ai/fal-swift | RED | github.com/fal-ai/fal-swift |  | RED: MIT, 214★, son push 2024-06; Swift istemci SDK'sı, araç değil |
| fal-ai/kling | RED | github.com/fal-ai/kling |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| fal-ai/sync-1.6.0 | RED | github.com/fal-ai/sync-1.6.0 |  | RED: bulunamadı (GitHub API 404; OCR bozuk ad olabilir) |
| fctp.it | RED | fctp.it |  | servis/site (URL 200), kurulacak paket yok |
| feat/todo-skeleton | RED | github.com/feat/todo-skeleton |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| felores/kie-cli-mcp | HESAP | github.com/felores/kie-cli-mcp | npm/mcp: github.com/felores/kie-cli-mcp @aa43e3955591 (kurulumdan sonra SHA doğrula) | Kie.ai medya API CLI+MCP; MIT, 80★, push 2026-10-07; ücretli üretim API sınırı gerekir |
| figma-plugin | ZATEN | - |  | envanterde figma girdisi var (_inv_*); ek kurulum gereksiz |
| figma.com | AYRI-UYGULAMA (i) | figma.com |  | Figma tasarım uygulaması; hesap |
| file.ai | RED | file.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| filec/cascadeurno | RED | github.com/filec/cascadeurno |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| filmakademie.de | RED | filmakademie.de |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| filmmore.eu | RED | filmmore.eu |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| find-skills | RED | - |  | kurulu değil; kaynak belirsiz ad, ayrı aday notu docs/kurulumlar/adaylar/find-skills-install-skills.md |
| folder/20241206_165409_unreal.fbx | RED | github.com/folder/20241206_165409_unreal.fbx |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| fondazionecsc.it | RED | fondazionecsc.it |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| fontjoy.com | AYRI-UYGULAMA (i) | fontjoy.com |  | tarayıcı font eşleştirici; kurulum yok |
| fullstory | RED | - |  | bulunamadı: resmi olmayan 0★ repolar (creevey-equals/fullstory-mcp vb.) |
| g2/capterra | RED | github.com/g2/capterra |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| gabbitt.co.uk | RED | gabbitt.co.uk |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| gentlestories.online | RED | gentlestories.online |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| geojson.io | AYRI-UYGULAMA (i) | geojson.io |  | tarayıcı harita aracı; kurulum yok |
| ghcr.io/zseven | RED | ghcr.io/zseven |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| git-for-windows.github.io | ZATEN | git-for-windows.github.io |  | Git for Windows kurulu (git/Git Bash çalışıyor) |
| github.00m/s8arch | RED | github.com/github.00m/s8arch |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| github.comfowner | RED | github.comfowner |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| glaido.com | RED | glaido.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| gle.com/search | RED | gle.com/search |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| globalgatewayteachertraining.com | RED | globalgatewayteachertraining.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| globalprivacycontrol.org | RED | globalprivacycontrol.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| gnano-banana-pro/edit | RED | github.com/gnano-banana-pro/edit |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| gncr.1o/zseven | RED | github.com/gncr.1o/zseven |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| google-cloud-storage | RED | - |  | kurulum nesnesi değil: gcloud/SDK servisi |
| google-stitch | RED | - |  | bulunamadı: resmi kaynak yok; gabelul/stitch-kit 45★ (apache-2.0) üçüncü taraf, doğrulanmadı |
| gpt-4o/gemini | RED | github.com/gpt-4o/gemini |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| gpt-4o/geminiuwanitg | RED | github.com/gpt-4o/geminiuwanitg |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| gpt-5.4/medium | RED | github.com/gpt-5.4/medium |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| graphify.com | RED | graphify.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| greengadgetguru.com | RED | greengadgetguru.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| grok.com | AYRI-UYGULAMA (i) | grok.com |  | Grok model servisi; hesap |
| gsap.com | RED | gsap.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| gsap.com/showcase | RED | gsap.com/showcase |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| guillaumecolombel.fr | RED | guillaumecolombel.fr |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| gumroad.com | RED | gumroad.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| hackernews.com | RED | hackernews.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| hand_additiona/pointj | RED | github.com/hand_additiona/pointj |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| hayaaesthetics.com | RED | hayaaesthetics.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| hayatintegrated.com | RED | hayatintegrated.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| help.ketone.com | RED | help.ketone.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| heretic-project.org | RED | heretic-project.org |  | kapsam dışı |
| hermes-masterclass.vercel.app | RED | hermes-masterclass.vercel.app |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| heygen.com | AYRI-UYGULAMA (i) | heygen.com |  | HeyGen video servisi; hesap |
| higgsfield.ai/privacy-policy | RED | higgsfield.ai/privacy-policy |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| higgsfield.ai/terms-of-use-a | RED | higgsfield.ai/terms-of-use-a |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| hler/regexp_parser | RED | github.com/hler/regexp_parser |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| hoainho/img2threeis-showcase | RED | github.com/hoainho/img2threeis-showcase |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| hostinger | RED | - |  | bulunamadı: yalnız 0★ üçüncü taraf repolar |
| htpsfimcp.chatplace.io/mcp | RED | htpsfimcp.chatplace.io/mcp |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| hugainaface.c | RED | hugainaface.c |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| huyml.co | RED | huyml.co |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| hvperframes/heygen | KUR | github.com/hvperframes/heygen | sabit @ f85614ecb222 | KURTARILDI → heygen-com/hyperframes; Apache-2.0 ★59796 push 2026-10-10; .claude-plugin/marketplace.json var |
| hwchase17/langchain | RED | github.com/hwchase17/langchain |  | langchain-ai/langchain olarak taşındı; MIT 147503★ kütüphane, skill/eklenti değil |
| hypit-ai/hypit | RED | github.com/hypit-ai/hypit |  | lisans NOASSERTION (belirsiz); yüz/ses değiştirip viral video klonlama uygulaması, skill değil |
| iadt.ie | RED | iadt.ie |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ibanfirst.com/dashboard | RED | ibanfirst.com/dashboard |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ikaijua/awesome-aitools | RED | github.com/ikaijua/awesome-aitools |  | araç listesi (CC-BY-4.0, 6217★); kurulacak nesne değil |
| illoca.unseen.co | RED | illoca.unseen.co |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| imaginefrontier.com | RED | imaginefrontier.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| inbox/fmfcgzqhvrbzcdhndhcm | RED | github.com/inbox/fmfcgzqhvrbzcdhndhcm |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| inferen-sh/skil1s | RED | github.com/inferen-sh/skil1s |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| inference.net | RED | inference.net |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| infistar.ai | RED | infistar.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| insider.windows.com | RED | insider.windows.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ip-52-53-175-49.tetra-data.tinyfish.io | RED | ip-52-53-175-49.tetra-data.tinyfish.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| iquine.com.br | RED | iquine.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| itchangesfree/open | RED | github.com/itchangesfree/open |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| jack000/fontjoy | RED | github.com/jack000/fontjoy |  | 2017 sonrası push yok; font eşleştirme uygulaması, skill değil (MIT, 1436★) |
| jesperlandberg.com | RED | jesperlandberg.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| jev/cevap-bekliyor | RED | github.com/jev/cevap-bekliyor |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| jev/finans-resmi | RED | github.com/jev/finans-resmi |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| jev/sea-tarih | RED | github.com/jev/sea-tarih |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| jev/son-tarih | RED | github.com/jev/son-tarih |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| jharilela/n8n-workflows | RED | github.com/jharilela/n8n-workflows |  | lisans yok (kişisel kullanım), 46★; n8n iş akışı dökümü |
| jianchang512/pyvideotrans | AYRI-UYGULAMA (ii) | github.com/jianchang512/pyvideotrans | github.com/jianchang512/pyvideotrans (v4.15) · ? (release dosyası yok) | GPL-3.0; winget yok |
| joaotavora/eglot | RED | github.com/joaotavora/eglot |  | Emacs LSP istemcisi (GPL-3.0); bu ortamla ilgisiz |
| jobs.lever.co | RED | jobs.lever.co |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| kanaafertility.com | RED | kanaafertility.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ketone.com | RED | ketone.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| keygraph.io | RED | keygraph.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| kimi.ai | AYRI-UYGULAMA (i) | kimi.ai |  | Kimi model servisi; hesap |
| kling.ai | AYRI-UYGULAMA (i) | kling.ai |  | Kling video üretim servisi; hesap |
| koishizzp/esm3-agent | RED | github.com/koishizzp/esm3-agent |  | lisans yok, 1★; protein modeli ajanı, kapsam dışı |
| lakr233/vphone-c | RED | github.com/lakr233/vphone-c |  | KURTARILDI → Lakr233/vphone-cli; MIT ★15101; macOS/Xcode aracı, Windows'ta çalışmaz |
| langchain-ai/langchain-nextjs-template | RED | github.com/langchain-ai/langchain-nextjs-template |  | Next.js başlangıç şablonu (MIT, 2535★); skill/araç değil |
| leadedu.com.br | RED | leadedu.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| legeling/prompthub | AYRI-UYGULAMA (ii) | github.com/legeling/prompthub | winget legeling.PromptHub 0.5.9 · ~114 MB | AGPL-3.0; koşulları rapora |
| lennxink/taate-satl1 | RED | github.com/lennxink/taate-satl1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| letta-ai/claude-subconscious | HESAP | github.com/letta-ai/claude-subconscious | claude plugin marketplace add letta-ai/claude-subconscious (pin 4f766fbae398) | Letta ajanı Claude Code eklentisi; MIT, 2903★, push 2026-09-25; konuşmaları Letta sunucusuna gönderir (telemetri/gizlilik riski), claude-mem |
| lighpanda-io/browseirelcases | RED | github.com/lighpanda-io/browseirelcases |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| lightricks/pr-2026-01-29 | RED | github.com/lightricks/pr-2026-01-29 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| lingfengqaq/webnovel-writer | RED | github.com/lingfengqaq/webnovel-writer |  | GPL-3.0 web roman yazma ajanı (7400★); projeyle ilgisiz, GPL |
| livingrichwithcoupons.com | RED | livingrichwithcoupons.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| llm-benchmarks.diegoromero.es | RED | llm-benchmarks.diegoromero.es |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| llms.anchorbrowser.io | RED | llms.anchorbrowser.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| login/login.com | RED | github.com/login/login.com |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| logs/editor.g | RED | github.com/logs/editor.g |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| logs/editor.log | RED | github.com/logs/editor.log |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| looplj/axonhub | AYRI-UYGULAMA (iii) | github.com/looplj/axonhub | docker/binary: github.com/looplj/axonhub @e863c6fe1942 | Go binary/Docker; Apache-2.0 |
| lordicon.com/licenses | RED | lordicon.com/licenses |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| lrepositorm/on.nt | RED | github.com/lrepositorm/on.nt |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ltodavannd/ai01 | RED | github.com/ltodavannd/ai01 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ltodavaond/aio1 | RED | github.com/ltodavaond/aio1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ltodavaood/aio1 | RED | github.com/ltodavaood/aio1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ltssssss_jack/videos | RED | github.com/ltssssss_jack/videos |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| lucasrosati/claude-code-memory-setup | RED | github.com/lucasrosati/claude-code-memory-setup |  | claude-mem zaten kurulu; aynı iş (bellek kurulum rehberi), MIT 1015★; çift bellek katmanı istemiyoruz |
| lukaponikvar/alxpravo | RED | github.com/lukaponikvar/alxpravo |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| lumalabs.ai | AYRI-UYGULAMA (i) | lumalabs.ai |  | Luma video üretim servisi; hesap |
| lusha | HESAP | - | claude plugin: github.com/lusha-oss/lusha-mcp-plugin (SHA kurulumdan önce çözülecek) | lusha-oss/lusha-mcp-plugin (MIT, 4★) yalnız aday; satış verisi/kişisel veri tarama riski, ücretli hesap; doğrulanmadı |
| madslorentzen/a-customne | RED | github.com/madslorentzen/a-customne |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| main/cover-aispiay | RED | github.com/main/cover-aispiay |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| main/cover-display | RED | github.com/main/cover-display |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| mainframe-two.vercel.app | RED | mainframe-two.vercel.app |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| maozi-114/mintima | RED | github.com/maozi-114/mintima |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| marketplace.reallusion.com | RED | marketplace.reallusion.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| mativ.com.pe | RED | mativ.com.pe |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| mattn/go-sqlite3 | RED | github.com/mattn/go-sqlite3 |  | Go kütüphanesi (MIT, 9247★, push 2026-09-28); skill/CLI/MCP değil |
| mayl-yaz3lim/seuklyat-pano | RED | github.com/mayl-yaz3lim/seuklyat-pano |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| maysunsolar.com | RED | maysunsolar.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| maysunsolar.it | RED | maysunsolar.it |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| mcp.zapier.com | HESAP | mcp.zapier.com |  | barındırılan Zapier MCP; Zapier hesabı ve ücretli görev sınırı; URL/anahtar kullanıcıya özel |
| meetingdevices.withgoogle.com | RED | meetingdevices.withgoogle.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| megalinter.github.io | RED | megalinter.github.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| meta.ai | RED | meta.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| metr.org | RED | metr.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| mh/apartmentanimation | RED | github.com/mh/apartmentanimation |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| mh/mh_character.fbx | RED | github.com/mh/mh_character.fbx |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| microsoft/azure-s | HESAP | github.com/microsoft/azure-s | claude plugin marketplace add microsoft/azure-skills (pin 0727d81638d6: kurulumdan sonra SHA doğrula) | OCR → microsoft/azure-skills: resmî eklenti (MIT, 1554★, push 2026-10-09); Azure aboneliği gerekir |
| microsoft/azure-sk111s | HESAP | github.com/microsoft/azure-sk111s | claude plugin marketplace add microsoft/azure-skills (pin 0727d81638d6) | OCR → microsoft/azure-skills (yukarıdaki satırla aynı kaynak) |
| minimaxi.com/v1 | RED | minimaxi.com/v1 |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| mirayatech123/mirayatechl23 | RED | github.com/mirayatech123/mirayatechl23 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| miro.cam | RED | miro.cam |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| mizorewww/laya-mlx | RED | github.com/mizorewww/laya-mlx |  | Apple MLX çalışma zamanı (Apache-2.0, 6853★); Windows'ta çalışmaz, kütüphane |
| mlabenne/harmless_atpaca | RED | github.com/mlabenne/harmless_atpaca |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| mm0/world | RED | github.com/mm0/world |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| modernc.org/libc | RED | modernc.org/libc |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| morningside.ai | RED | morningside.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| motricese.com.br | RED | motricese.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| msitarzewski/agency-agents | KUR-duzeltmeli | github.com/msitarzewski/agency-agents | agent dosyası kopyası ~/.claude/agents/ @f99f6aa910a4 | MIT, 158525★, push 2026-10-07; dev yığını: yalnız seçili bölümler (engineering/design/security) kopyalanır, toplu kurulum betiği çalıştırılm |
| mssolarmodules.com | RED | mssolarmodules.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| multimodalart/qwen-image-multiple-a | RED | github.com/multimodalart/qwen-image-multiple-a |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| musistudio/claude-code-router | RED | github.com/musistudio/claude-code-router |  | MIT, 37604★, push 2026-10-09; yerel vekil ANTHROPIC_BASE_URL'yi ele geçirir, headroom vekiliyle çakışır; sağlayıcı anahtarı ister |
| n.dev/lab-guess | RED | n.dev/lab-guess |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| n8n.io | AYRI-UYGULAMA (i) | n8n.io |  | n8n iş akışı uygulaması; hesap/sunucu |
| nandhakishorm/laya | RED | github.com/nandhakishorm/laya |  | karar modeli kütüphanesi (Apache-2.0, 31970★); skill/MCP değil |
| nateherkai/herk-2.0 | RED | github.com/nateherkai/herk-2.0 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| nathanhodgson.ai | RED | nathanhodgson.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ndard/motion-control | RED | github.com/ndard/motion-control |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ndolestudio/htpsms-go | RED | github.com/ndolestudio/htpsms-go |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ndolestudio/httpsms | AYRI-UYGULAMA (iii) | github.com/ndolestudio/httpsms |  | Go+PostgreSQL+Android uygulaması; AGPL-3.0; ÖNERİLMEZ: SMS/kişisel veri |
| neondoorlit.com | RED | neondoorlit.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| netflix.com | RED | netflix.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| netlify | HESAP |  | npm i -g @netlify/mcp@1.18.0 | resmî @netlify/mcp (ISC) 1.18.0; netlify-cli 27.12.0 (MIT, 1921★); Netlify hesabı |
| nev/ed.etart | RED | github.com/nev/ed.etart |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| news-oceanacidification-icc.org | RED | news-oceanacidification-icc.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| news.ycombinator.com | RED | news.ycombinator.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| nexrone.com | RED | nexrone.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| nimble | RED |  |  | bulunamadı: belirsiz ad, GitHub aramasında ilgili skill/CLI/MCP yok |
| nizos/tdd-guard | KUR-duzeltmeli | github.com/nizos/tdd-guard | npm i -g tdd-guard@1.7.0 (repo @7245912d8a36) | MIT, 2360★, push 2026-10-05; Claude Code TDD hook'u (npm + .claude-plugin); hook her Write/Edit'te ek model çağrısı yapar: kurulumdan önce h |
| nominatim.openstreetmap.org | RED | nominatim.openstreetmap.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| notion.com | AYRI-UYGULAMA (i) | notion.com |  | Notion uygulaması; hesap |
| now./acy | RED | github.com/now./acy |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| ntgroup/echomimic_ | AYRI-UYGULAMA (iii) | github.com/ntgroup/echomimic_ | sabit @ c32b3a557003 | KURTARILDI → antgroup/echomimic; iii; Apache-2.0 ★4313; GPU modeli; ÖNERİLMEZ: yüz/ses sentezi (kişisel veri/gri alan), GPU yok |
| nvidia/nemotron-3-ultra-550b-a55b | RED | github.com/nvidia/nemotron-3-ultra-550b-a55b |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| oa-icc.ipsl.fr | RED | oa-icc.ipsl.fr |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ocalhost:4173 | RED |  |  | yerel geliştirme adresi; kurulum nesnesi değil |
| od/workffle_upioad_re | RED | github.com/od/workffle_upioad_re |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| odysseeclinic.com.au | RED | odysseeclinic.com.au |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ollama.com/download | AYRI-UYGULAMA (ii) | ollama.com/download | winget Ollama.Ollama 0.40.2 · ~1.5 GB | MIT; yerel LLM çalıştırıcı; telemetri: doğrulanmadı |
| ollama.com/search | AYRI-UYGULAMA (ii) | ollama.com/search | winget Ollama.Ollama · ~1.5 GB | katalog sayfası; uygulama aynı |
| om/google-maps | RED | github.com/om/google-maps |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| omacom/try-omarchy | RED | github.com/omacom/try-omarchy |  | Omarchy (Linux masaüstü) deneme betiği; MIT, 2543★; işle ilgisiz |
| omacom/try-omarchy-windows | RED | github.com/omacom/try-omarchy-windows |  | Omarchy deneme betiği (MIT, 579★); işle ilgisiz |
| omni.cappenlabs.com.br | RED | omni.cappenlabs.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| one/few-step | RED | github.com/one/few-step |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| onurtirpan.com | RED | onurtirpan.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| openai/apt-oss-20b | RED | github.com/openai/apt-oss-20b |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| openresearch.sh | RED | openresearch.sh |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| opera.com | AYRI-UYGULAMA (ii) | opera.com | winget Opera.Opera 137.0.6036.39 · ? (indirici) | Freeware (EULA); tarayıcı, gezinti verisi işler |
| orets/wasdakavair | RED | github.com/orets/wasdakavair |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| orms.gle | RED | orms.gle |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| our.today | RED | our.today |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| outreach-pack/tracker | RED | github.com/outreach-pack/tracker |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| owser-use/web-ui | AYRI-UYGULAMA (iii) | github.com/owser-use/web-ui |  | OCR→browser-use/web-ui; py 3.11+; LLM anahtarı |
| pacvetemergency.com | RED | pacvetemergency.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| pandas | RED |  |  | Python veri kütüphanesi (PyPI, BSD-3); skill/MCP değil |
| paneruntimniplatform/socket | RED | github.com/paneruntimniplatform/socket |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| partnerle.com | RED | partnerle.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| pen-webui/open | AYRI-UYGULAMA (iii) | github.com/pen-webui/open |  | OCR→open-webui/open-webui; Docker/py; özel lisans (branding koşulu), AGPL değil |
| penglonghuang/chinese-novelist-skill | KUR | github.com/penglonghuang/chinese-novelist-skill | ~/.claude/skills/ kopyası @6a64a0465103 | MIT, 3340★, push 2026-10-06; Çince roman yazma skill'i, ilgi düşük; SkillSpector kurulumdan önce çalıştırılır |
| peoplewinningbets/shorts | RED | github.com/peoplewinningbets/shorts |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| pinterest-style-gall-v600.boit.host | RED | pinterest-style-gall-v600.boit.host |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| pixeleyehospitals.com | RED | pixeleyehospitals.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| pixels.market/illustrati | RED | github.com/pixels.market/illustrati |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| plugins.omarchy.org | RED | plugins.omarchy.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ponytail:ponytail-review | ZATEN |  |  | ponytail@ponytail eklentisi kurulu (_inv_plugin) |
| portal.nousresearch.com | RED | portal.nousresearch.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| pptr.dev | RED | pptr.dev |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| praiaguadalupe.com.br | RED | praiaguadalupe.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| preethiudhayaraja.com | RED | preethiudhayaraja.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| preymaker.com | RED | preymaker.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| prodeagroup.com | RED | prodeagroup.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| producthunt.com | RED | producthunt.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| project/weather-forecast-motion | RED | github.com/project/weather-forecast-motion |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| prompt-caching | RED |  |  | kavram/özellik adı; kurulabilir kaynak yok |
| prosple | RED |  |  | bulunamadı: GitHub aramasında ilgili kaynak yok |
| protocols.io | RED | protocols.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| prototipal.com | RED | prototipal.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| pycache_/_init_.cpython-314.pyc | RED | github.com/pycache_/_init_.cpython-314.pyc |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| python.langchain.com | RED | python.langchain.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| qixing-jk/all-api-hub | RED | github.com/qixing-jk/all-api-hub |  | tarayıcı eklentisi, New-API hesap panosu (AGPL-3.0, 4923★); işle ilgisiz |
| quickmagic.ai/captu | RED | quickmagic.ai/captu |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| quickmagic.ai/horn | RED | quickmagic.ai/horn |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| rbd/pnpm-vol | RED | github.com/rbd/pnpm-vol |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| rccl.cappenlabs.com.br | RED | rccl.cappenlabs.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| rea-agentcompany | RED |  |  | kapsam dışı |
| rea-agents@latest | RED |  |  | kapsam dışı |
| react-bits/pixelcard-js-css | RED | github.com/react-bits/pixelcard-js-css |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| react-three/fiber | RED | github.com/react-three/fiber |  | OCR → pmndrs/react-three-fiber (MIT, 32819★); npm kütüphanesi, skill değil |
| reactbits.dev/text | RED | reactbits.dev/text |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| reat/cloud-render-worker | RED | github.com/reat/cloud-render-worker |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| recommended/info | RED | github.com/recommended/info |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| remorses/zele | HESAP | github.com/remorses/zele | npm i -g zele@0.10.0 (repo @0caa71ed56bf) | Gmail/Outlook e-posta+takvim CLI; 299★, push 2026-10-08, lisans yok — yalnız kişisel kullanım; OAuth ile posta erişimi (izin riski yüksek) |
| remotion.dev/brand | RED | remotion.dev/brand |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| replicate/replicate-javascript | RED | github.com/replicate/replicate-javascript |  | SDK kütüphanesi (Apache-2.0, 597★, push 2025-11-17); skill/MCP değil |
| riomarrecife.com.br | RED | riomarrecife.com.br |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| riverside.com | AYRI-UYGULAMA (i) | riverside.com |  | Riverside kayıt servisi; hesap |
| robonuggets-design-inspo.vercel.app | RED | robonuggets-design-inspo.vercel.app |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| rubrio-references/index.htmi | RED | github.com/rubrio-references/index.htmi |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| s0/3imus.php | RED | github.com/s0/3imus.php |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| saif.google | RED | saif.google |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| sam-machine/creations | RED | github.com/sam-machine/creations |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| sampies/cascy.esc | RED | github.com/sampies/cascy.esc |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| sana-video/longsana | RED | github.com/sana-video/longsana |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| santalarch.com | RED | santalarch.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| santifer.io | RED | santifer.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| santionispirits.com | RED | santionispirits.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| say1/kanit | RED | github.com/say1/kanit |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| search.brave.com/search | RED | search.brave.com/search |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| security.demodesk.com | RED | security.demodesk.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| seewhateyesee.org | RED | seewhateyesee.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| selmakcby/vault-radar | RED | github.com/selmakcby/vault-radar |  | MIT, 15★, push 2026-08-31; not okuma radarı, kanıt/ilgi düşük |
| serverisidebar/rowl | RED | github.com/serverisidebar/rowl |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| shadows/extra-large | RED | github.com/shadows/extra-large |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| share.descrint | RED | share.descrint |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| sign-in/register | RED | github.com/sign-in/register |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| signin.anchorbrowser.io | RED | signin.anchorbrowser.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| sivanhavkin/entelgia | RED | github.com/sivanhavkin/entelgia |  | MIT, 12★; deneysel bilişsel mimari araştırması, skill/MCP değil |
| skilthat | RED |  |  | bulunamadı: GitHub aramasında sonuç yok |
| skool.cc. | RED | skool.cc. |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| skool.cu. | RED | skool.cu. |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| skyvern-ai/skyvern | AYRI-UYGULAMA (iii) | github.com/skyvern-ai/skyvern |  | py+Docker+PostgreSQL; AGPL-3.0 |
| smtg-ai/claude-squad | AYRI-UYGULAMA (iii) | github.com/smtg-ai/claude-squad |  | Go+tmux (Windows'ta tmux yok → WSL); AGPL-3.0 |
| socialcameo.com | RED | socialcameo.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| sourcegraph | RED |  |  | bulunamadı: belirsiz ad; yalnız düşük yıldızlı topluluk MCP/skill'i (13–41★), Sourcegraph hesabı ister |
| spacestongyi-mal/z-image-turbolike | RED | github.com/spacestongyi-mal/z-image-turbolike |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| spanner | RED |  |  | bulunamadı: belirsiz ad, yalnız 0–2★ deneysel MCP'ler |
| sre/thart.tox | RED | github.com/sre/thart.tox |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| start.ccstrategic.io/skool | RED | start.ccstrategic.io/skool |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| status.claude.com | RED | status.claude.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| status.stripe.com | RED | status.stripe.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| status/sectoraathird-partysservige | RED | github.com/status/sectoraathird-partysservige |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| stratosphere.io | RED | stratosphere.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| strikethrough/dim | RED | github.com/strikethrough/dim |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| strix | RED |  |  | kapsam dışı |
| studiomeala.com | RED | studiomeala.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| subscribe.wordpress.com | RED | subscribe.wordpress.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| supabase-community/create-t3-turbo | RED | github.com/supabase-community/create-t3-turbo |  | MIT, 330★, push 2024-05; başlangıç şablonu |
| supabase-community/nextjs-subscription-payments | RED | github.com/supabase-community/nextjs-subscription-payments |  | MIT, 97★; SaaS şablonu |
| supabase-community/vercel-ai-chatbot | RED | github.com/supabase-community/vercel-ai-chatbot |  | sohbet uygulaması şablonu (854★, 2024-05'ten beri durgun) |
| supabase/agent-sk111 | KUR | github.com/supabase/agent-sk111 | ~/.claude/skills/ kopyası @c9be0e931b79 | OCR → supabase/agent-skills: resmî Supabase skill'leri (MIT, 2706★, push 2026-10-02); Supabase işi çıkınca; SkillSpector kurulumdan önce |
| superdesigndev/treg | HESAP | github.com/superdesigndev/treg |  | 'OpenRouter for agent tools' (4933★, push 2026-10-09, lisans NOASSERTION/özel); barındırılan hizmet, anahtar ister; lisans koşulu okunmalı |
| superpowers:subagent-driven-development | ZATEN |  |  | superpowers eklentisi kurulu (obra/superpowers, 296882★) |
| support.claude.com | RED | support.claude.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| susearch/vi3_anowy_elophant | RED | github.com/susearch/vi3_anowy_elophant |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| sustainability.aboutamazon.com | RED | sustainability.aboutamazon.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| svgexport.io | RED | svgexport.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| syrizelink/openfic | AYRI-UYGULAMA (ii) | github.com/syrizelink/openfic | winget Syrize.OpenFic 0.12.0 · ~118 MB | Apache-2.0 |
| taekchef/claude-code-zh-cn | RED | github.com/taekchef/claude-code-zh-cn |  | MIT, 789★; Çince arayüz yerelleştirmesi, ilgisiz |
| tasks/t.ask-2.js0m | RED | github.com/tasks/t.ask-2.js0m |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| teapearce.github.io | RED | teapearce.github.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| tecs/teu.os.ef | RED | github.com/tecs/teu.os.ef |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| tengilemalamala.com | RED | tengilemalamala.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| thebirthwave.com | RED | thebirthwave.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| thsopics/know.-plugins | RED | github.com/thsopics/know.-plugins |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| tienda.zapler.com | RED | tienda.zapler.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| tinyhumans.ai | RED | tinyhumans.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| todavanod/aio1 | RED | github.com/todavanod/aio1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| todavaood/ai01 | RED | github.com/todavaood/ai01 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| todavgood/aio1 | RED | github.com/todavgood/aio1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| todaygond/aio1 | RED | github.com/todaygond/aio1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| todaygood/aio1 | RED | github.com/todaygood/aio1 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| todomvc.com | RED | todomvc.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| tong-io/tongflow | AYRI-UYGULAMA (iii) | github.com/tong-io/tongflow |  | Docker+DB; AGPL-3.0 |
| traderalice/fixa...390b3fte | RED | github.com/traderalice/fixa...390b3fte |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| traderalice/oper | AYRI-UYGULAMA (iii) | github.com/traderalice/oper | sabit @ 87bc415260aa | KURTARILDI → TraderAlice/OpenAlice; iii; AGPL-3.0 ★7259; AI trading ajanı; ÖNERİLMEZ: finansal hesap/anahtar, gerçek para riski |
| trendyol.comfapplefiphone-15-128-gb-mavi-p-762254881 | RED | trendyol.comfapplefiphone-15-128-gb-mavi-p-762254881 |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| trufflesecus | RED |  |  | OCR → trufflesecurity/trufflehog (28400★); gizli anahtar tarayıcı, gitleaks kurulu ve örtüşür |
| trust.file.ai | RED | trust.file.ai |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| tt-a1i.github.io | RED | tt-a1i.github.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| tt-a1i/axchify | RED | github.com/tt-a1i/axchify |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| turkolister.co.uk | RED | turkolister.co.uk |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| types/spdx-expression-parse | RED | github.com/types/spdx-expression-parse |  | OCR → @types/spdx-expression-parse (npm 4.0.0); tür paketi |
| typesafe-ai/system-one-adapter-python | RED | github.com/typesafe-ai/system-one-adapter-python |  | MIT, 385★; Python kütüphanesi |
| typesafe:typesafe-ai | RED |  |  | bulunamadı: skill kaynağı yok (yalnız typesafe-ai Python kütüphanesi) |
| typpo/quickchart-csharp | RED | github.com/typpo/quickchart-csharp |  | MIT, 23★; istemci kütüphanesi |
| typpo/quickchart-java | RED | github.com/typpo/quickchart-java |  | lisans yok, 11★; istemci kütüphanesi |
| typpo/quickchart-js | RED | github.com/typpo/quickchart-js |  | MIT, 75★; istemci kütüphanesi |
| typpo/quickchart-php | RED | github.com/typpo/quickchart-php |  | MIT, 46★; istemci kütüphanesi |
| typpo/quickchart-python | RED | github.com/typpo/quickchart-python |  | MIT, 66★; istemci kütüphanesi |
| typpo/quickchart-ruby | RED | github.com/typpo/quickchart-ruby |  | MIT, 14★; istemci kütüphanesi |
| unity6tksorceress.igames/msic-geraunity | RED | github.com/unity6tksorceress.igames/msic-geraunity |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| unreallabsai/unreal-agent | RED | github.com/unreallabsai/unreal-agent |  | MIT, 2180★; ajan çalışma çatısı, skill/MCP değil, ilgisiz |
| unseen.co | RED | unseen.co |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| usercontent.com/christopherkahl | RED | usercontent.com/christopherkahl |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| utube.com | RED | utube.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| v267/v268 | RED | github.com/v267/v268 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| v3b.fal.media | RED | v3b.fal.media |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vault-index/brain-build | RED | github.com/vault-index/brain-build |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| vault/claude.mc | RED | github.com/vault/claude.mc |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| vectorize-io/hindsight | RED | github.com/vectorize-io/hindsight |  | MIT, 47692★; ajan belleği; claude-mem ile örtüşür, ikinci bellek enjektörü riski |
| velammalnexus.com | RED | velammalnexus.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vercel-labs/agent-browser | KUR-duzeltmeli | github.com/vercel-labs/agent-browser | npm i -g agent-browser@0.39.0 (repo @44af39842650) | Apache-2.0, 43722★, push 2026-10-09; tarayıcı otomasyon CLI'ı; Playwright MCP ile örtüşür, yalnız gerekirse; kurulumda tarayıcı indirir, yer |
| vercel-labs/agent-ski11s | RED | github.com/vercel-labs/agent-ski11s |  | OCR → vercel-labs/agent-skills (32127★) lisans yok: lisans kapısı, kurulmaz |
| vercel-labs/next-skills | RED | github.com/vercel-labs/next-skills |  | lisans yok (983★, push 2026-09-16): lisans kapısı, kurulmaz |
| vercel.com/new | RED | vercel.com/new |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vercel.com/viktoroddy-1863s | RED | vercel.com/viktoroddy-1863s |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vibely.app | RED | vibely.app |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| visx.21st.dev | RED | visx.21st.dev |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vitest/coverage-v8 | RED | github.com/vitest/coverage-v8 |  | OCR → @vitest/coverage-v8 (npm 5.0.3, MIT); test kütüphanesi |
| vmicheli.github.io | RED | vmicheli.github.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vowautoparts.us | RED | vowautoparts.us |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| vswyh1971/aiev | RED | github.com/vswyh1971/aiev |  | 0★, lisans yok |
| wallpapers/light-m | RED | github.com/wallpapers/light-m |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| wangrongsheng/awesome-llm-resources | RED | github.com/wangrongsheng/awesome-llm-resources |  | Apache-2.0, 9012★; bağlantı listesi |
| wavect.io | RED | wavect.io |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| wcodescascadeur/cascadeuranimatians | RED | github.com/wcodescascadeur/cascadeuranimatians |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| wecanfixeverything.com | RED | wecanfixeverything.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| whisper-flow | RED |  |  | dimastatz/whisper-flow (985★): gerçek zamanlı yazıya dökme çatısı, skill/MCP değil |
| workos | RED |  |  | bulunamadı: resmî skill/MCP kaynağı doğrulanamadı (npm @workos-inc/mcp 404) |
| worktree/revert-pr-3087 | RED | github.com/worktree/revert-pr-3087 |  | bulunamadı: GitHub 404 (OCR bozuk ya da var olmayan ad) |
| worldnuclearreport.org | RED | worldnuclearreport.org |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| ww.trendyol.comfapple | RED | ww.trendyol.comfapple |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| www.skol.com/tirendaz-academy | RED | www.skol.com/tirendaz-academy |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| xingyeai.com | RED | xingyeai.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
| xming521/weclone | AYRI-UYGULAMA (iii) | github.com/xming521/weclone |  | py+GPU; AGPL-3.0; ÖNERİLMEZ: sohbet geçmişinden dijital ikiz (kişisel veri) |
| yarnpkg/cli-dist | RED | github.com/yarnpkg/cli-dist |  | OCR → @yarnpkg/cli-dist (npm 4.18.1, BSD-2); paket yöneticisi |
| zai-org/zcode | AYRI-UYGULAMA (iii) | github.com/zai-org/zcode |  | Node; Apache-2.0; ayrı ajan çatısı |
| zhizhuodemao/js-reverse-mcp | RED | github.com/zhizhuodemao/js-reverse-mcp |  | kapsam dışı |
| zhouxiaoka/autoclip | AYRI-UYGULAMA (ii) | github.com/zhouxiaoka/autoclip | release AutoClip.Desktop 1.5.5 x64-setup · 197 MB | MIT; winget yok |
| zoominfo | HESAP |  |  | Zoominfo/zoominfo-mcp-plugin (8★, push 2026-09-30); ZoomInfo kurumsal hesabı; işle ilgisiz |
| zseven-w/openpencstime | AYRI-UYGULAMA (ii) | github.com/zseven-w/openpencstime | winget ZSeven-W.OpenPencil 0.8.4 · 37 MB | OCR→openpencil; MIT |
| ×.com | RED | ×.com |  | web sitesi/servis; kurulabilir skill/CLI/MCP kaynağı yok |
