# cli — 101 benzersiz kayıt

**Amaç:** Ajanın kabuktan çağırdığı kurulu komut satırı araçları: çalışma zamanları, paket yöneticileri, MCP sunucu/vekilleri, bağlam sıkıştırıcılar, güvenlik tarayıcıları, video/medya araçları.

**İç yapı:** Tür [cli]: npm kapsamlı paketler (@playwright/cli, @upstash/context7-mcp), mcp-server-* sunucuları, yerel araçlar (jev, rtk, headroom, graphify) ve tek seferlik çalıştırıcı çiftleri (npx/bunx/uvx).

## En güçlü parçalar
- `graphify` — Kod/dosyalardan bilgi grafiği kurup query/path/explain ile sorgular; grep yerine kod tabanı keşfi.
- `jev` — Büyük log/dosyayı bağlam dışında süzer, triage/ilgili/kanıt verir.
- `rtk` — Komut çıktısını LLM bağlamına girmeden süzüp özetler; token tasarrufu.
- `gh` — GitHub PR, issue, CI ve API işlemleri; yerel git değil.
- `gitleaks` — Kodda ve git geçmişinde sızmış sırları tarar.
- `semgrep` — Kaynak koda benzeyen kalıplarla hata varyantı bulan hafif statik analiz.
- `uvx` — Python aracını kurmadan tek seferlik çalıştırır; MCP/CLI başlatmak için.
- `video` — Videoyu kademeli izler: özet, sor, kare, whisper.
- `markitdown` — Çeşitli dosyaları Markdown'a çevirir.
- `@modelcontextprotocol/inspector` — MCP sunucularını incelemek için resmi denetleyici.

## Birlikte kullanım
- graphify + jev: önce grafik sorgusu, sonra jev ilgili/triage ile dar kanıt.
- video/crv + whisper-cli + ffmpeg: kare, transkript ve medya kesme hattı.
- npx/uvx/bunx ile mcp-server-fetch, mcp-server-git, @upstash/context7-mcp gibi MCP sunucularını başlatmak.
- strix + gitleaks + semgrep: sızma testi, sır taraması ve statik analiz ayrı katmanlar.

## Tuzaklar
- Çakışan çiftler: graphify/graphifyy, jev/jev-cli, headroom/headroom-ai, video/video-cli, strix/strix-agent, summarize/@steipete/summarize.
- omniroute 352 sağlayıcılı yönlendirici; brave-search-mcp-server, stitch-mcp (Google Cloud kimlik) dış hizmet ister.
- comfyui yerel sunucu (127.0.0.1:8188), bulut API değil; whisper-cli açıklaması '(tahmin)' işaretli.
- ui-to-vue-converter açıklaması Çince; droidasc/rea-agents/mimic-client tersine mühendislik kapsamında.

## Üyeler
- cli (79): @_davideast/stitch-mcp, @alibaba-group/open-code-review, @brave/brave-search-mcp-server, @caveman-ai/cli, @gltf-transform/cli, @googleworkspace/cli, @larksuite/cli, @modelcontextprotocol/inspector, @playwright/cli, @steipete/summarize, @testsprite/testsprite-cli, @tobilu/qmd, @upstash/context7-mcp, agent-browser, agent-reach, blender-dogrulama, bun, bunx, claude-monitor, claude-real-video, claude-usage, code-review-mcp, codeburn, comfyui, corepack, crv, dotnet, droidasc, ecc-agentshield, ffmpeg, gh, git, gitleaks, graphify, graphifyy, headroom, headroom-ai, jev, jev-cli, markitdown …
- skill (22): cli-a2a, cli-anything, cli-backup-sync, cli-batches, cli-chat, cli-compression, cli-contexts, cli-cost-usage, cli-eval, cli-health, cli-keys, cli-mcp, cli-models, cli-plugins-skills, cli-policy-audit, cli-providers, cli-resilience, cli-routing, cli-serve, cli-setup, cli-skill-collector, cli-tunnel
