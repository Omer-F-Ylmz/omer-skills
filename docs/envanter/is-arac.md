# İş → araç sırası (ENVANTER-1)

Amaç: iş başlarken kurulu aracın unutulmaması. **Departmanı olan işte sıra departman-* müdüründedir; bu dosya onu tekrar etmez, yalnız eksik kalanı ekler.** Çakışmada departman-* SKILL.md kazanır. Kaynak: `envanter.tsv` (ad, nerede, son kullanım), `bosluk.md`.
Kısaltma: CC = Claude Code, AI = Desktop/claude.ai, `*` = son 45 günde kullanıldı.

## 1. Departmanı olan işler — giriş ve eksik bağlar

| İş türü | Giriş (sıra orada) | Departman Dizin'inde olmayan, eklenecek kurulu araç |
|---|---|---|
| Arayüz, landing, bileşen, CSS | `departman-frontend`* | ajanlar `fe-*` 19 (Dizin'de yok); `infinite-canvas` MCP (tuval), `canva`/`Adobe for creativity` MCP (yalnız CC, yetki bekliyor) |
| Animasyon, scroll, 3D web sahne | `departman-frontend`* adım 4 → `animasyon-atolyesi` | `threejs-bloom`*, `web-sahne-desenleri`*, `webgpu-threejs-tsl` plugin (bağsız) |
| Test, e2e, görsel QA | `departman-test-qa`* | ajanlar `qa-*` 18; `chrome-devtools` MCP (bağsız, CC) |
| Güvenlik, sır, SAST | `departman-guvenlik`* | ajanlar `sec-*` 15; `strix-agent` CLI, `ecc-agentshield` CLI (kullanılmadı) |
| Veri, SQL, şema | `departman-veri-db`* | ajanlar `db-*` 22; `clickhouse` MCP, `drizzle-docs` MCP, `airtable` MCP (bağsız) |
| .NET, ASP.NET, backend | `departman-backend-dotnet` | ajanlar `be-*` 15; `binlog` MCP (ikisi), `mslearn`* MCP |
| Plan, PRD, görev bölme | `departman-surec-plan`* | ajanlar `pln-*` 14 |
| Kod inceleme | `departman-surec-inceleme` | ajanlar `inc-*` 12; `code-review` MCP (ikisi), `open-code-review` CLI (bağsız) |
| Git, PR, yayın, deploy | `departman-surec-git-yayin`* | `netlify` MCP, `hostinger` MCP, `vercel`* CLI (bağsız); ajanlar `git-*` 8 zaten listede |
| Belge, rapor, PDF/DOCX | `departman-belge`* | ajanlar `dok-*` 11; `markitdown`* MCP |
| Araştırma, video tarama, kütüphane | `departman-arastirma-ogrenme`* | ajanlar `ara-*` 9; `arxiv` `apify` `context7`* `hfspace` MCP; `agent-reach`* CLI |
| Skill/ajan/araç yazımı | `departman-surec-ajan-arac`* | — (ajn-* bağlı) |
| Bağlam, jeton, oturum | `departman-verimlilik`* | `context-mode`* `headroom`* `qmd` `codebase-memory-mcp` `codegraph` `serena` MCP; `claude-monitor` `claude-usage`* CLI |

## 2. Departmansız işler — araç sırası (müdür yok; ilk durak bu tablo)

| İş türü | Sıra (önce kurulu ve ölçülmüş olan) | Taraf notu |
|---|---|---|
| Video kurgu, kısa klip, altyazı | `video-cli`* (video tarama/indir) → `ffmpeg`* / `whisper-cli`* → `premiere-pro` MCP (kurgu) → `hyperframes` plugin (HTML→video) → ajanlar `vid-*`; çocuk shorts hattı: `edge-tts` (TR/EN ses) · Chatterbox Multilingual (ses klonlama, `Desktop\araclar\chatterbox`) · Remotion 4.0.537 (`Desktop\kids-shorts-sablon`) · ComfyUI (`Desktop\araclar\ComfyUI` yerel, henüz açılmadı; çalışan `C:\AI\ComfyUI`; Z-Image-Turbo, FLUX.2-klein-4B, Wan 2.2 TI2V-5B) | premiere-pro, hyperframes yalnız CC |
| Blender, 3D model, render | `blender`* plugin (1.3.0 CC + repo) → `blender-uretim`* / `blender-oturum`* → `blender`* MCP → ajanlar `bl-*` | blender MCP ikisi; skill zip AI'de |
| Oyun, mod | `mod-atolyesi`* → `godot` / `unity` MCP → `universal-modder` plugin → ajanlar `oyn-*` | godot/unity yalnız CC |
| Görsel üretim, logo, ikon | `nano-banana-2`* MCP → `figma` → `logo-design` / `llm-icon-finder` plugin → `fal` MCP | fal, canva yalnız CC; ücretli çağrıda tavan şart |
| Otomasyon, iş akışı, kazıma | `n8n-mcp` → `airtable` → `apify` MCP → ajanlar `otm-*` → `scrapling-skill` plugin | hepsi yalnız CC |
| Hukuk, sözleşme, KVKK | `commercial-legal` / `privacy-legal`* plugin → `Ironclad` MCP → ajan `dok-sozlesme-madde` → `sec-kvkk-gdpr-kontrol` | DocuSign, iManage yetki bekliyor |
| Pazarlama, reklam, içerik | `marketing-skills` / `claude-ads` plugin → ajanlar `urn-*` → `humanizer` plugin | hepsi kullanılmadı, yalnız CC |
| Altyapı, bulut, k8s | `azure` plugin+MCP → `terraform-skill` plugin → ajanlar `ops-*` | yalnız CC |
| ML, değerlendirme, LLM eval | `promptfoo-evaluation` plugin → ajanlar `ml-*` → `ajn-skill-test` | yalnız CC |
| Mobil | `expo` plugin+MCP → `android-skills` plugin → ajanlar `mob-*` | yalnız CC |
| Dil/çatı uzmanlığı (Go, Rust, Python…) | ajanlar `dil-*` 26 (ad = dil) | yalnız CC |

### KURULUM-VİDEO-1 durumu (2026-10-21)
- edge-tts 7.3.1 · kurulu (tr.mp3/en.mp3, `Desktop\kids-shorts-test`)
- Remotion 4.0.537 · kurulu; şablon 1080x1920 30fps 5 sn render ✓ (`Desktop\kids-shorts-sablon\out\test.mp4`, ffprobe 1080x1920 / 5.000 sn)
- Chatterbox-TTS 0.1.7 · MIT · torch 2.6.0+cu124 CUDA ✓ (`Desktop\araclar\chatterbox\venv`); TR/EN wav 3.84 sn / 4.32 sn; VRAM pik 3.37 GB (`olcum.py`)
- ComfyUI 0.38.0 · çalışan kurulum `C:\AI\ComfyUI` (.venv torch 2.14.1+cu130 CUDA ✓); headless `arka.py` ile 127.0.0.1:8188; `Desktop\araclar\ComfyUI` yok (çift kurulum yok)
- FLUX.1-schnell fp8 all-in-one checkpoint (17.2 GB, içinde text encoder + VAE) · `C:\AI\ComfyUI\models\checkpoints`; Apache-2.0
- ComfyUI-GGUF node (city96, Apache-2.0) · `C:\AI\ComfyUI\custom_nodes\ComfyUI-GGUF`; `gguf` 0.19.0 venv'e kuruldu
- Wan 2.2 TI2V-5B Q5_K_M GGUF (3.6 GB) · `C:\AI\ComfyUI\models\unet`; umt5_xxl fp8 + wan2.2_vae `C:\AI\ComfyUI\models` altında
- 1f ölçümü (`.kos\kopru\video\kurulum_uret.py`): FLUX 1080x1920 PNG 25 sn, min VRAM boş 2.26 GB, min RAM boş 2.51 GB (≈%92 dolu; %85 tavanı aşıldı); Wan i2v 704x1280 73 kare 24 fps (3.04 sn) 262 sn, min VRAM boş 3.73 GB, min RAM boş 3.75 GB; iş sonu `/free`
- VIDEO HATTI KURALI (Ömer 21 Eki): üretim tamamen yerel ve ücretsiz (ComfyUI+FLUX/Wan, Chatterbox/edge-tts, Remotion, ffmpeg); Claude yalnız senaryo + sahne listesi yazar (≤$0.10/reklam filmi)
- Log: `.kos\kopru\indir\{comfyui,flux,wan}.log` (indirmeler tamam)
- earshot (Leonxlnx/earshot, MIT) · 4 Kas 2026 · `C:\Projeler\_araclar\earshot` (.venv, torch CPU, CLAP+AudioSet ~1.1 GB); CC MCP `earshot` (user scope); skill `earshot` + `real-sound` (~/.claude/skills, omer-skills/skills). Desktop'tan: `python sosyal-oto\_kulak.py <video> [dlg.wav]` → critique + timeline + measure + sheet + whisper → `<video>.kulak.txt`. Video kalite kapısının ses ayağı (QC'den sonra şart)
- ai-website-cloner-template (JCodesMore, reel DfN3J7lRpmk) · `C:\Projeler\_araclar\ai-website-cloner` (npm install tamam); `/clone-website <url>` komutu ~/.claude/commands + skill `clone-website` (~/.claude/skills, omer-skills). Kullanım: o klasörde `claude --chrome` → `/clone-website https://site` (harita → gözlem → inşa → karşılaştırma). Portföy sitesi referans klonu için
- audio-studio-mcp (kanaworksai-hue/audio-studio-mcp, MIT, reel DfPlP_8BGy3) · 4 Kas 2026 · `C:\Projeler\_araclar\audio-studio-mcp` (.venv yalnız taban: mcp/numpy/soundfile). Cümleden yerel BGM + ses efekti (Stable Audio 3) MCP sunucusu. GPU bağımlılığı SONRA: `powershell -ExecutionPolicy Bypass -File install.ps1` (torch cu126 + model) → `claude mcp add --scope user audio-studio -- "C:\Projeler\_araclar\audio-studio-mcp\.venv\Scripts\audio-studio-mcp.exe"`
- VoiceStudio (debpalash/VoiceStudio, AGPL-3.0, reel DfU2nIgt8XK/DfSvS-CTqDA) · 4 Kas 2026 · `C:\Projeler\_araclar\VoiceStudio` (yalnız klon, bağımlılık kurulmadı; skill'leri `voicestudio`/`voicestudio-maintainer` zaten ~/.claude/skills'te). Yerel ElevenLabs alternatifi: ses klonlama, TTS, dublaj, transkripsiyon, sesli kitap. GPU bağımlılığı SONRA: `uv sync` (torch 2.8 cu128, whisperx, demucs; modeller ilk açılışta) ya da Releases'tan Windows kurulum paketi
- claude-video-edit (YildizDikme/claude-video-edit, MIT, reel YsBLOjneHpU) · 4 Kas 2026 · `C:\Projeler\_araclar\claude-video-edit` (.venv: numpy + faster-whisper, CPU). Konuşan kafa/tutorial/Shorts kurgusu: Whisper kelime-zamanlı kesim, GSAP sahneler, matematikten SFX, dürüst loudness. Skill: SKILL.md; önizleme `python scripts/serve.py --project . --port 5600` (Node 20+, Chrome, ffmpeg gerekli). earshot ile birlikte
- ffmpeg-skill (kajisho5/ffmpeg-skill, MIT, 3.1.1, reel DfKTbNQFMSW) · 4 Kas 2026 · `C:\Projeler\_araclar\ffmpeg-skill` (bağımlılık yok, stdlib). 42 FFmpeg aracı + MCP (`mcp/server.py`): kes/birleştir, sessizlik, dikey reframe, altyazı/karaoke, loudness, platform export, kontak sayfası doğrulama. Kurulum `npx ffmpeg-skill` (→ ~/.claude/skills/ffmpeg-skill); kontrol `python scripts/_contract.py doctor` ✓ (73 yetenek)
- agent-desktop (vercel-labs/agent-desktop, Apache-2.0, v1.1.0, reel DfSn_x9gMsx/DfTgGValSlF) · 4 Kas 2026 · `C:\Projeler\_araclar\agent-desktop` + hazır Windows ikili `_release\bin\agent-desktop.exe` (sha256 ✓, `--version` ✓). Ekran görüntüsü yerine erişilebilirlik ağacıyla computer-use CLI (~%84 daha az token). Kullanım: `agent-desktop snapshot --app <Uygulama> -i`; MCP `{"command":"<exe yolu>","args":["mcp"]}`; skill `npx skills add https://github.com/vercel-labs/agent-desktop --skill agent-desktop`
- gradientdeck design-md kütüphanesi (ui.gradientdeck.com, GitHub reposu YOK — site aynası, reel DfU9VHCoTGj) · 4 Kas 2026 · `C:\Projeler\_araclar\gradientdeck-design-md` (`library.json` 1276 girdi + `styles\<slug>.design.md` + `llms.txt`). Gerçek sitelerden çıkarılmış DESIGN.md'ler — awwwards/tasarım referans kaynakları: siteyi `library.json`'da (industry/theme/fonts/colors) seç, `<slug>.design.md`'yi CC'ye ver. Tek dosya: `https://ui.gradientdeck.com/styles/<slug>/design.md` (genişletilmiş: `design-extended.md`)
- n8n-workflows (Zie619/n8n-workflows, MIT, reel DfSPwlyg76_) · 4 Kas 2026 · `C:\Projeler\_araclar\n8n-workflows` (.venv py3.12, requirements kurulu). hazır n8n iş akışları (`workflows/` kategorili; diskte 2061 JSON sayıldı, reel "4000+" diyor). JSON'u n8n'e yapıştır ya da arama arayüzü: `.venv\Scripts\python run.py`. Otomasyon satışı işinde `n8n-mcp` ile birlikte
- day-trader-skill (Jakeschincariol/day-trader-skill, MIT, reel De9i2LVqwDh/DfUwMmzsur2) · 4 Kas 2026 · `C:\Projeler\_araclar\day-trader-skill` (bağımlılık yok, saf Python). 11 skill (scanner, news, entry, exit, risk, budget, timemachine, pelosi...). Time Machine: `python trader-timemachine\timemachine.py run|chart` (10.000 Monte Carlo replay). YALNIZ analiz/backtest — gerçek para işlemi yok. SEC araçları `SEC_USER_AGENT` ister. Skill tarafı zaten CC plugin'i olarak kurulu (`day-trader-skill@day-trader-skill` 2.0.0, envanter.tsv); bu klon kod/test için

## 3. Taraf kuralı (CC ↔ Desktop/claude.ai)

- AI'de alt ajan yok: tablodaki `xx-*` ajanları AI'de `departman-*/ajanlar/<ad>.md` talimatı olarak okunur (207 tanesi bu yolla var; 373 tanesi AI'de hiç yok).
- AI'de plugin yok: plugin skill'i AI'ye yalnız zip ile gider (1125'ten 213'ünün senkron kopyası var).
- Desktop MCP 18 (15'i CC ile ortak). CC'deki 46 MCP AI'de yok; AI'den CC aracına köprü `cc-kopru` (31 izinli CLI).
