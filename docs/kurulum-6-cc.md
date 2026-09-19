# KURULUM-6 · Claude Code kurulum satırları · 19 Eyl 2026

Kaynak: docs/kurulum-6-envanter.md. Satırlar kurulum değil, öneridir; her kalem kurulmadan önce `skillspector scan <klasör> --no-llm` (README kuralı) ve lisans kapısı geçerlidir. Anahtarlar yalnız `${VAR}` olarak yazılır; komutları Git Bash'te çalıştır (PowerShell'de `$env:VAR`). SKILL'ler için zip'ler dist/ altında, yükleme: docs/claude-ai-yukleme.md.

## PLUGIN (liste sırasıyla)

### thedotmack/claude-mem · PLUGIN+MCP · lisans Apache-2.0
```
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem@thedotmack
/plugin install claude-mem-cowork@thedotmack
```

### headroomlabs-ai/headroom · PLUGIN+MCP · lisans Apache-2.0
```
/plugin marketplace add headroomlabs-ai/headroom
/plugin install headroom@headroom-marketplace
```

### supabase-community/supabase-plugin · SKILL+PLUGIN · lisans YOK
- lisans yok → KURMA (lisans gelirse yeniden bakılır); satırlar yalnız kayıt için
- marketplace.json yok (yalnız .claude-plugin/plugin.json) → /plugin ile eklenemez; yerel deneme: `claude --plugin-dir .tmp/supabase-community__supabase-plugin`

### anthropics/skills · SKILL+PLUGIN · lisans YOK
- lisans yok → KURMA (lisans gelirse yeniden bakılır); satırlar yalnız kayıt için
```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
/plugin install claude-api@anthropic-agent-skills
/plugin install academy-guide@anthropic-agent-skills
/plugin install discernment-nudge@anthropic-agent-skills
```

### anthropics/claude-code · PLUGIN · lisans özel
```
/plugin marketplace add anthropics/claude-code
/plugin install agent-sdk-dev@claude-code-plugins
/plugin install claude-opus-4-5-migration@claude-code-plugins
/plugin install code-review@claude-code-plugins
/plugin install commit-commands@claude-code-plugins
/plugin install explanatory-output-style@claude-code-plugins
/plugin install feature-dev@claude-code-plugins
/plugin install frontend-design@claude-code-plugins
/plugin install hookify@claude-code-plugins
/plugin install learning-output-style@claude-code-plugins
/plugin install plugin-dev@claude-code-plugins
/plugin install pr-review-toolkit@claude-code-plugins
/plugin install ralph-wiggum@claude-code-plugins
/plugin install security-guidance@claude-code-plugins
```

### anthropics/claude-plugins-official · PLUGIN · lisans Apache-2.0
- kurulu (A-kovası: known_marketplaces; frontend-design, skill-creator, playwright, superpowers… buradan) → atla

### Leonxlnx/taste-skill · SKILL+PLUGIN · lisans MIT
```
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```

### nateherkai/scroll-craft · PLUGIN · lisans MIT
- kurulu (A-kovası: known_marketplaces, nateherk-design@nateherk 0.3.0) → atla

### 21st-dev/magic-mcp · SKILL+PLUGIN · lisans ISC
- kurulu (A-kovası: known_marketplaces 21st-dev/magic-mcp, 21st@21st-dev 1.0.1) → atla

### daveremy/nano-banana-2-mcp · SKILL+PLUGIN+MCP · lisans MIT
```
/plugin marketplace add daveremy/nano-banana-2-mcp
/plugin install nano-banana-2@nano-banana-2-plugins
```

### nextlevelbuilder/ui-ux-pro-max-skill · PLUGIN · lisans MIT
- kurulu (A-kovası: ~/.claude/skills/ui-ux-pro-max (ad eşleşmesi; md5 farklı sürüm)) → atla

### HermeticOrmus/design-mastery-claude-code · SKILL+PLUGIN · lisans MIT
```
/plugin marketplace add HermeticOrmus/design-mastery-claude-code
/plugin install design-mastery@design-mastery
```

### addyosmani/agent-skills · SKILL+PLUGIN · lisans MIT
```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

### upstash/context7 · SKILL+PLUGIN+MCP · lisans MIT
- kurulu (A-kovası: claude mcp list context7 (@upstash/context7-mcp); repodaki skill'ler kurulu değil) → atla

### KitJacky/cli-anything · PLUGIN · lisans Apache-2.0
```
/plugin marketplace add KitJacky/cli-anything
/plugin install cli-anything@cli-anything
```

### blader/humanizer · SKILL+PLUGIN · lisans MIT
```
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

### DietrichGebert/ponytail · SKILL+PLUGIN · lisans MIT
```
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

### pbakaus/impeccable · PLUGIN · lisans Apache-2.0
- kurulu (A-kovası: known_marketplaces, impeccable@impeccable 4.3.1) → atla

### multica-ai/andrej-karpathy-skills · SKILL+PLUGIN · lisans YOK
- lisans yok → KURMA (lisans gelirse yeniden bakılır); satırlar yalnız kayıt için
```
/plugin marketplace add multica-ai/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

### obra/superpowers · SKILL+PLUGIN · lisans MIT
- kurulu (A-kovası: claude-plugins-official marketplace.json source=obra/superpowers, superpowers 6.3.0 (kapalı)) → atla

### worldflowai/everything-claude-code · SKILL+PLUGIN · lisans YOK
- lisans yok → KURMA (lisans gelirse yeniden bakılır); satırlar yalnız kayıt için
```
/plugin marketplace add worldflowai/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

### Security-Phoenix-demo/security-skills-claude-code · PLUGIN · lisans MIT
```
/plugin marketplace add Security-Phoenix-demo/security-skills-claude-code
/plugin install phoenix-security-review@phoenix-security
/plugin install phoenix-readiness-reviews@phoenix-security
/plugin install phoenix-sast-rules@phoenix-security
/plugin install phoenix-cti-search@phoenix-security
/plugin install phoenix-prd-pipeline@phoenix-security
/plugin install phoenix-docs-research@phoenix-security
```

## MCP

```bash
# thedotmack/claude-mem · lisans Apache-2.0
# MCP plugin içinde gelir (4 arama aracı) → PLUGIN bölümündeki satır yeterli; ayrı `claude mcp add` yok
# headroomlabs-ai/headroom · lisans Apache-2.0
claude mcp add headroom -s user -- uvx --from "headroom-ai[mcp]==0.37.0" headroom mcp serve
# davideast/stitch-mcp · lisans Apache-2.0
# önce kimlik: cmd /c npx -y @_davideast/stitch-mcp@0.9.0 init  (gcloud oturumu, Google Cloud hesabı ister)
claude mcp add stitch -s user -- cmd /c npx -y @_davideast/stitch-mcp@0.9.0 proxy
# daveremy/nano-banana-2-mcp · lisans MIT
claude mcp add nano-banana-2 -s user -e GEMINI_API_KEY=${GEMINI_API_KEY} -- cmd /c npx -y nano-banana-2-mcp@0.1.1   # ücretli/kotalı Gemini
# upstash/context7 · lisans MIT
# kurulu (A-kovası: context7 MCP bağlı) → atla
# Panniantong/Agent-Reach · lisans MIT
# kurulu (A-kovası: agent-reach CLI + skill) → atla; MCP modu kullanılmıyor
# CullinanCloud/omniroute · lisans MIT
claude mcp add omniroute -s user -- cmd /c npx -y omniroute@3.8.49 --mcp   # sağlayıcı anahtarları omniroute panelinde, burada değil
# merajmehrabi/puppeteer-mcp-server · lisans MIT
claude mcp add puppeteer -s user -- cmd /c npx -y puppeteer-mcp-server@0.7.2
# modelcontextprotocol/servers · lisans Apache-2.0
claude mcp add mcp-everything -s user -- cmd /c npx -y @modelcontextprotocol/server-everything@2.0.0   # test/demo sunucusu
claude mcp add mcp-fetch -s user -- uvx mcp-server-fetch@0.6.3
claude mcp add mcp-filesystem -s user -- cmd /c npx -y @modelcontextprotocol/server-filesystem@0.6.3 <izinli-dizin>
claude mcp add mcp-git -s user -- uvx mcp-server-git@0.6.2
claude mcp add mcp-memory -s user -- cmd /c npx -y @modelcontextprotocol/server-memory@0.6.3
claude mcp add mcp-sequential-thinking -s user -- cmd /c npx -y @modelcontextprotocol/server-sequential-thinking@0.6.2
claude mcp add mcp-time -s user -- uvx mcp-server-time@0.6.2
# brave/brave-search-mcp-server · lisans MIT
claude mcp add brave-search -s user -e BRAVE_API_KEY=${BRAVE_API_KEY} -- cmd /c npx -y @brave/brave-search-mcp-server@2.1.4 --transport stdio
# github/github-mcp-server · lisans MIT
claude mcp add --transport http github -s user https://api.githubcopilot.com/mcp/ -H "Authorization: Bearer ${GITHUB_PAT}"
# yerel alternatif (Docker): claude mcp add github -s user -e GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_PAT} -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
# Graphify-Labs/graphify · lisans Apache-2.0
# kurulu (A-kovası: graphifyy 0.9.57 CLI + skill) → atla
# safishamsi/graphify · lisans Apache-2.0
# Graphify-Labs/graphify ile aynı repo (HEAD b9cd957) → atla
# OldJii/code-review-mcp · lisans MIT
claude mcp add code-review -s user -e GITHUB_TOKEN=${GITHUB_TOKEN} -e GITLAB_TOKEN=${GITLAB_TOKEN} -- uvx code-review-mcp@2.0.0   # token yalnız ilgili platform için
```

## KÜTÜPHANE

- gglucass/headroom-desktop (MIT): Headroom'un masaüstü tepsi uygulaması (ücretli abonelik, 7 gün deneme) · Claude Code token maliyetini düşürmek isteyen her proje
- darkroomengineering/tempus (MIT): requestAnimationFrame tabanlı hafif animasyon döngüsü · scroll/animasyon ağırlıklı landing
- darkroomengineering/satus (MIT): Next.js 16 + React 19 + Tailwind v4 (+ WebGL) başlangıç kiti · yeni Next.js landing/site
- darkroomengineering/lenis (MIT): smooth-scroll kütüphanesi · scroll ağırlıklı landing/portfolyo
- swup/swup (MIT): çok sayfalı sitelerde sayfa geçiş animasyonu · klasik MPA vitrin siteleri
- gchahal1982/pixeljury (MIT): AI üretimi arayüzü render edip görsel/a11y QA yapan CLI · frontend-craft kabul turlarına yardımcı QA
- trys/utopia-core-scss (YOK): Utopia akışkan tipografi/spacing SCSS karşılığı · responsive tipografi ölçeği kuran projeler (lisans yok, kopyalanmaz)
- pmndrs/react-three-a11y (MIT): react-three-fiber sahnelerine a11y katmanı · erişilebilir Three.js/R3F sahnesi
- ai/size-limit (MIT): JS bundle boyut bütçesi, CI'da aşımda hata · frontend perf bütçesi (Next.js/Vite)
- seek-oss/capsize (MIT): font metriğiyle öngörülebilir satır yüksekliği/boşluk · tipografi hassas tasarım sistemleri
- QwikDev/partytown (MIT): 3. parti scriptleri web worker'a taşır · analytics/reklam yükü olan perf kritik siteler
- 14islands/r3f-scroll-rig (MIT): R3F WebGL'i smooth scroll'a bağlar · scroll ağırlıklı Three.js landing
- barvian/number-flow (MIT): animasyonlu sayı/sayaç bileşeni · istatistik/fiyat sayacı olan arayüzler
- YildizDikme/threejs-fluid-reveal-portfolio (YOK): imleçle görsel açan Three.js editoryal portfolyo şablonu · örnek site, REF olarak açılır (lisans yok)
- YildizDikme/3d-camera-landing-page (YOK): Next.js + R3F + GSAP 3D kamera landing (README yok) · örnek site, REF olarak açılır (lisans yok)
- YildizDikme/3D-threejs-spiral-gallery (YOK): GLSL + Lenis + GSAP spiral galeri hero'su · örnek site, REF olarak açılır (lisans yok)
- gishamer/skill-ui (YOK): Agent Skill keşif/kurma/yayınlama masaüstü uygulaması + CLI · skill deposu yönetimi (lisans yok)
- iansinnott/obsidian-claude-code-mcp (0BSD): Obsidian topluluk eklentisi; vault'u MCP ile açar, Claude Code WebSocket ile kendisi bulur (`claude mcp add` gerekmez) · Obsidian not entegrasyonu

## ÖRNEK

- figma/code-connect (MIT): REF olarak açılır → .tmp/figma__code-connect
- gist:e20ead11b3df4de46ab32b4a7269abe0 (YOK): REF olarak açılır → .tmp/gist__e20ead11b3df4de46ab32b4a7269abe0
