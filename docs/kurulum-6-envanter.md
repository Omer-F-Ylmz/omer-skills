# KURULUM-6 envanter · 19 Eyl 2026 · 64 kaynak · clone --depth 1 · SkillSpector v2.11.2 --no-llm (skill başına)

Tür kuralı dosya kanıtıdır: kök `SKILL.md` ya da `skills/*/SKILL.md` → SKILL; `.claude-plugin/{marketplace,plugin}.json` → PLUGIN; package.json `bin` + MCP SDK/ad (ya da pyproject/go.mod MCP) → MCP; yalnız package.json → KÜTÜPHANE; hiçbiri → ÖRNEK. Birden çok kural tutarsa hepsi yazılır, ilk sıradaki birincildir. Elenme ölçütü: execution_successful=false, genel seviye HIGH/CRITICAL ya da en az bir HIGH/CRITICAL bulgu. Lisansı olmayan ya da açık olmayan skill taranmaz ve dist'e girmez.

## Repo satırları

| # | ad | tür | lisans | SKILL.md byte | skill sayısı | A-kovası | SkillSpector | not |
|---|---|---|---|---|---|---|---|---|
| 1 | microsoft/playwright-cli | SKILL | Apache-2.0 | 15663 | 1 | hayır | 0 geçti · 1 elendi | derin SKILL.md: 1 |
| 2 | thedotmack/claude-mem | PLUGIN+MCP | Apache-2.0 | 0 | 0 | hayır | - | derin SKILL.md: 30 · MCP kanıtı: package.json bin=claude-mem,./dist/npx-cli/index.js · plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 3 | headroomlabs-ai/headroom | PLUGIN+MCP | Apache-2.0 | 0 | 0 | hayır | - | MCP kanıtı: pyproject scripts + mcp · plugin: .claude-plugin/marketplace.json |
| 4 | gglucass/headroom-desktop | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 5 | supabase-community/supabase-plugin | SKILL+PLUGIN | YOK | 16274 | 2 | hayır | 0 geçti · 0 elendi · 2 taranmadı (lisans) | plugin: .claude-plugin/plugin.json |
| 6 | ibelick/ui-skills | SKILL | MIT | 44539 | 7 | hayır | 7 geçti · 0 elendi | - |
| 7 | zanwei/design-dna | SKILL | MIT | 8543 | 1 | evet · Portale/.claude/skills/design-dna md5 eşit | 0 geçti · 1 elendi | - |
| 8 | darkroomengineering/tempus | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 9 | darkroomengineering/satus | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | derin SKILL.md: 1 |
| 10 | darkroomengineering/lenis | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 11 | figma/code-connect | ÖRNEK | MIT | 0 | 0 | hayır | - | - |
| 12 | swup/swup | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 13 | gchahal1982/pixeljury | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 14 | trys/utopia-core-scss | KÜTÜPHANE | YOK | 0 | 0 | hayır | - | - |
| 15 | pmndrs/react-three-a11y | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | GitHub NOASSERTION, dosya: MIT |
| 16 | ai/size-limit | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 17 | seek-oss/capsize | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 18 | QwikDev/partytown | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 19 | 14islands/r3f-scroll-rig | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 20 | barvian/number-flow | KÜTÜPHANE | MIT | 0 | 0 | hayır | - | - |
| 21 | anthropics/skills | SKILL+PLUGIN | YOK | 273762 | 19 | kısmi · frontend-design, skill-creator claude-plugins-official üzerinden kurulu | 7 geçti · 7 elendi · 5 taranmadı (lisans) | derin SKILL.md: 1 · plugin: .claude-plugin/marketplace.json |
| 22 | anthropics/claude-code | PLUGIN | özel | 0 | 0 | kısmi · Claude Code CLI kurulu; repodaki plugin'ler kurulu değil | - | derin SKILL.md: 10 · plugin: .claude-plugin/marketplace.json · lisans özel: koşullar LICENSE dosyasından okunmalı |
| 23 | anthropics/claude-plugins-official | PLUGIN | Apache-2.0 | 0 | 0 | evet · known_marketplaces; frontend-design, skill-creator, playwright, superpowers… buradan | - | derin SKILL.md: 31 · plugin: .claude-plugin/marketplace.json |
| 24 | Leonxlnx/taste-skill | SKILL+PLUGIN | MIT | 309010 | 13 | kısmi · taste-skill-v1 = Portale design-taste-frontend-v1 (md5 eşit), 12/13 kurulu değil | 11 geçti · 2 elendi | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 25 | senlindesign/taste-skill | SKILL | YOK | 21706 | 1 | hayır | 0 geçti · 0 elendi · 1 taranmadı (lisans) | - |
| 26 | nateherkai/scroll-craft | PLUGIN | MIT | 0 | 0 | evet · known_marketplaces, nateherk-design@nateherk 0.3.0 | - | derin SKILL.md: 1 · plugin: .claude-plugin/marketplace.json |
| 27 | YildizDikme/threejs-fluid-reveal-portfolio | KÜTÜPHANE | YOK | 0 | 0 | hayır | - | - |
| 28 | YildizDikme/3d-camera-landing-page | KÜTÜPHANE | YOK | 0 | 0 | hayır | - | - |
| 29 | YildizDikme/3D-threejs-spiral-gallery | KÜTÜPHANE | YOK | 0 | 0 | hayır | - | - |
| 30 | 21st-dev/magic-mcp | SKILL+PLUGIN | ISC | 3503 | 1 | evet · known_marketplaces 21st-dev/magic-mcp, 21st@21st-dev 1.0.1 | 1 geçti · 0 elendi | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json · ISC: telif + izin notu korunur |
| 31 | davideast/stitch-mcp | MCP | Apache-2.0 | 0 | 0 | hayır | - | derin SKILL.md: 1 · MCP kanıtı: package.json bin=stitch-mcp,./bin/stitch-mcp.js |
| 32 | daveremy/nano-banana-2-mcp | SKILL+PLUGIN+MCP | MIT | 3474 | 1 | hayır | 1 geçti · 0 elendi | MCP kanıtı: package.json bin=nano-banana-2-mcp,./dist/index.js · plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 33 | nextlevelbuilder/ui-ux-pro-max-skill | PLUGIN | MIT | 0 | 0 | evet · ~/.claude/skills/ui-ux-pro-max (ad eşleşmesi; md5 farklı sürüm) | - | derin SKILL.md: 13 · plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 34 | HermeticOrmus/design-mastery-claude-code | SKILL+PLUGIN | MIT | 40161 | 4 | hayır | 3 geçti · 1 elendi | plugin: .claude-plugin/marketplace.json |
| 35 | Gustavosilveira23/claude-design-skills | SKILL | MIT | 117735 | 6 | hayır | 4 geçti · 2 elendi | - |
| 36 | addyosmani/agent-skills | SKILL+PLUGIN | MIT | 353572 | 25 | hayır | 14 geçti · 11 elendi | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json, plugin.json |
| 37 | vercel-labs/agent-skills | SKILL | YOK | 72760 | 9 | hayır | 0 geçti · 0 elendi · 9 taranmadı (lisans) | - |
| 38 | billhector/design-skills | SKILL | MIT | 46977 | 2 | hayır | 0 geçti · 2 elendi | - |
| 39 | usestrix/strix | SKILL | Apache-2.0 | 75202 | 9 | hayır | 6 geçti · 3 elendi | - |
| 40 | gishamer/skill-ui | KÜTÜPHANE | YOK | 0 | 0 | hayır | - | derin SKILL.md: 1 |
| 41 | upstash/context7 | SKILL+PLUGIN+MCP | MIT | 13382 | 3 | evet · claude mcp list context7 (@upstash/context7-mcp); repodaki skill'ler kurulu değil | 3 geçti · 0 elendi | derin SKILL.md: 7 · MCP kanıtı: packages/mcp/package.json bin=context7-mcp,dist/index.js · plugin: .claude-plugin/marketplace.json |
| 42 | dickwu/apple-design-skill | SKILL | YOK | 25100 | 1 | hayır | 0 geçti · 0 elendi · 1 taranmadı (lisans) | - |
| 43 | KitJacky/cli-anything | PLUGIN | Apache-2.0 | 0 | 0 | hayır | - | derin SKILL.md: 17 · plugin: .claude-plugin/marketplace.json |
| 44 | Panniantong/Agent-Reach | MCP | MIT | 0 | 0 | evet · uv receipt url Panniantong/agent-reach + ~/.claude/skills/agent-reach (elle budanmış) | - | derin SKILL.md: 1 · MCP kanıtı: pyproject scripts + mcp |
| 45 | CullinanCloud/omniroute | SKILL+MCP | MIT | 182158 | 45 | hayır | 29 geçti · 16 elendi | MCP kanıtı: package.json bin=omniroute,omniroute-reset-password |
| 46 | rebelytics/one-skill-to-rule-them-all | SKILL | CC-BY-4.0 | 53188 | 1 | hayır | 0 geçti · 1 elendi | CC-BY-4.0: atıf zorunlu (yazar + lisans bağlantısı) |
| 47 | blader/humanizer | SKILL+PLUGIN | MIT | 29102 | 1 | hayır | 0 geçti · 1 elendi | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 48 | merajmehrabi/puppeteer-mcp-server | MCP | MIT | 0 | 0 | hayır | - | MCP kanıtı: package.json bin=mcp-server-puppeteer,dist/index.js |
| 49 | modelcontextprotocol/servers | MCP | Apache-2.0 | 0 | 0 | hayır | - | GitHub NOASSERTION, dosya: Apache-2.0 · MCP kanıtı: src/everything/package.json bin=mcp-server-everything,dist/index.js; src/filesystem/package.json bin=mcp-server-filesystem,dist/index.js; src/memory/package.json bin=mcp-server-memory,dist/index.js |
| 50 | brave/brave-search-mcp-server | MCP | MIT | 0 | 0 | hayır | - | MCP kanıtı: package.json bin=brave-search-mcp-server,dist/index.js |
| 51 | github/github-mcp-server | MCP | MIT | 0 | 0 | hayır | - | MCP kanıtı: go.mod mcp-go |
| 52 | Graphify-Labs/graphify | MCP | Apache-2.0 | 0 | 0 | evet · uv graphifyy 0.9.57, METADATA Homepage Graphify-Labs/graphify | - | derin SKILL.md: 1 · MCP kanıtı: pyproject scripts + mcp |
| 53 | safishamsi/graphify | MCP | Apache-2.0 | 0 | 0 | evet · HEAD b9cd957 = Graphify-Labs/graphify (aynı repo) | - | derin SKILL.md: 1 · MCP kanıtı: pyproject scripts + mcp |
| 54 | DietrichGebert/ponytail | SKILL+PLUGIN | MIT | 17527 | 6 | hayır | 6 geçti · 0 elendi | derin SKILL.md: 6 · plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json, plugin.json |
| 55 | OldJii/code-review-mcp | MCP | MIT | 0 | 0 | hayır | - | MCP kanıtı: pyproject scripts + mcp |
| 56 | iansinnott/obsidian-claude-code-mcp | KÜTÜPHANE | 0BSD | 0 | 0 | hayır | - | 0BSD: koşulsuz |
| 57 | pbakaus/impeccable | PLUGIN | Apache-2.0 | 0 | 0 | evet · known_marketplaces, impeccable@impeccable 4.3.1 | - | derin SKILL.md: 24 · plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 58 | multica-ai/andrej-karpathy-skills | SKILL+PLUGIN | YOK | 2585 | 1 | hayır | 0 geçti · 0 elendi · 1 taranmadı (lisans) | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 59 | obra/superpowers | SKILL+PLUGIN | MIT | 168882 | 15 | evet · claude-plugins-official marketplace.json source=obra/superpowers, superpowers 6.3.0 (kapalı) | 7 geçti · 8 elendi | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 60 | worldflowai/everything-claude-code | SKILL+PLUGIN | YOK | 95867 | 11 | hayır | 0 geçti · 0 elendi · 11 taranmadı (lisans) | plugin: .claude-plugin/marketplace.json, .claude-plugin/plugin.json |
| 61 | garrytan/gstack | SKILL | MIT | 15215 | 1 | hayır | 0 geçti · 1 elendi | derin SKILL.md: 60 |
| 62 | Security-Phoenix-demo/security-skills-claude-code | PLUGIN | MIT | 0 | 0 | hayır | - | derin SKILL.md: 27 · plugin: .claude-plugin/marketplace.json |
| 63 | awesome-skills/code-review-skill | SKILL | MIT | 12052 | 1 | hayır | 0 geçti · 1 elendi | - |
| 64 | gist:e20ead11b3df4de46ab32b4a7269abe0 | ÖRNEK | YOK | 0 | 0 | hayır | - | - |

## Skill alt tablosu

| repo | skill adı | SKILL.md byte | lisans | SkillSpector | zip | sebep |
|---|---|---|---|---|---|---|
| microsoft/playwright-cli | playwright-cli | 15663 | Apache-2.0 | HIGH 80/100 · HIGH+CRIT 3 | yok | 3 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:471 · kök LICENSE kopyaya eklendi |
| supabase-community/supabase-plugin | supabase | 12979 | YOK | taranmadı | yok | lisans yok |
| supabase-community/supabase-plugin | supabase-postgres-best-practices | 3295 | YOK | taranmadı | yok | lisans yok |
| ibelick/ui-skills | baseline-ui | 3504 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ui-skills-baseline-ui.zip | - · kök LICENSE kopyaya eklendi |
| ibelick/ui-skills | create-design-md | 16462 | MIT | LOW 12/100 · HIGH+CRIT 0 | var · ui-skills-create-design-md.zip | - · kök LICENSE kopyaya eklendi |
| ibelick/ui-skills | fixing-accessibility | 4853 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ui-skills-fixing-accessibility.zip | - · kök LICENSE kopyaya eklendi |
| ibelick/ui-skills | fixing-metadata | 4551 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ui-skills-fixing-metadata.zip | - · kök LICENSE kopyaya eklendi |
| ibelick/ui-skills | fixing-motion-performance | 5716 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ui-skills-fixing-motion-performance.zip | - · kök LICENSE kopyaya eklendi |
| ibelick/ui-skills | improve-ui | 7946 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ui-skills-improve-ui.zip | - · kök LICENSE kopyaya eklendi |
| ibelick/ui-skills | ui-skills-root | 1507 | MIT | LOW 12/100 · HIGH+CRIT 0 | var · ui-skills-ui-skills-root.zip | - · kök LICENSE kopyaya eklendi |
| zanwei/design-dna | design-dna | 8543 | MIT | HIGH 57/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:55 · A: md5 eşit: C:\Users\pc\Desktop\Portale\.claude\skills\design-dna |
| anthropics/skills | academy-guide | 7902 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · skills-academy-guide.zip | - |
| anthropics/skills | algorithmic-art | 20173 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · skills-algorithmic-art.zip | - |
| anthropics/skills | brand-guidelines | 2308 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · skills-brand-guidelines.zip | - |
| anthropics/skills | canvas-design | 12068 | Apache-2.0 | LOW 6/100 · HIGH+CRIT 0 | var · skills-canvas-design.zip | - |
| anthropics/skills | claude-api | 86770 | Apache-2.0 | CRITICAL 100/100 · HIGH+CRIT 40 | yok | 40 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:59 |
| anthropics/skills | discernment-nudge | 10801 | Apache-2.0 | LOW 17/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: AR1 HIGH SKILL.md:191 |
| anthropics/skills | doc-coauthoring | 16190 | YOK | taranmadı | yok | lisans yok |
| anthropics/skills | docx | 7002 | özel | taranmadı | yok | lisans açık değil (özel) |
| anthropics/skills | frontend-design | 9461 | Apache-2.0 | LOW 13/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: AR2 HIGH SKILL.md:69 · A: ad + repo kurulu: frontend-design@claude-plugins-official |
| anthropics/skills | internal-comms | 1543 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · skills-internal-comms.zip | - |
| anthropics/skills | mcp-builder | 9328 | Apache-2.0 | CRITICAL 100/100 · HIGH+CRIT 5 | yok | 5 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:62 |
| anthropics/skills | pdf | 8386 | özel | taranmadı | yok | lisans açık değil (özel) |
| anthropics/skills | pptx | 21034 | özel | taranmadı | yok | lisans açık değil (özel) |
| anthropics/skills | skill-creator | 33653 | Apache-2.0 | CRITICAL 100/100 · HIGH+CRIT 4 | yok | 4 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:364 · A: ad + repo kurulu: skill-creator@claude-plugins-official |
| anthropics/skills | slack-gif-creator | 8095 | Apache-2.0 | LOW 7/100 · HIGH+CRIT 0 | var · skills-slack-gif-creator.zip | - |
| anthropics/skills | theme-factory | 3183 | Apache-2.0 | MEDIUM 37/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:23 |
| anthropics/skills | web-artifacts-builder | 3160 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · skills-web-artifacts-builder.zip | - |
| anthropics/skills | webapp-testing | 4008 | Apache-2.0 | HIGH 64/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: TM1 HIGH scripts/with_server.py:69 |
| anthropics/skills | xlsx | 8697 | özel | taranmadı | yok | lisans açık değil (özel) |
| Leonxlnx/taste-skill | brandkit | 16790 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-brandkit.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | industrial-brutalist-ui | 8548 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-industrial-brutalist-ui.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | gpt-taste | 7931 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-gpt-taste.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | image-to-code | 37670 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-image-to-code.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | imagegen-frontend-mobile | 41791 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · taste-skill-imagegen-frontend-mobile.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | imagegen-frontend-web | 37841 | MIT | MEDIUM 45/100 · HIGH+CRIT 3 | yok | 3 HIGH/CRIT, ilk: P6 HIGH SKILL.md:3 · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | minimalist-ui | 7986 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-minimalist-ui.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | full-output-enforcement | 2641 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-full-output-enforcement.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | redesign-existing-projects | 15238 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-redesign-existing-projects.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | high-end-visual-design | 10659 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-high-end-visual-design.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | stitch-design-taste | 12035 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · taste-skill-stitch-design-taste.zip | - · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | design-taste-frontend | 88459 | MIT | MEDIUM 37/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: P2 HIGH SKILL.md:272 · kök LICENSE kopyaya eklendi |
| Leonxlnx/taste-skill | design-taste-frontend-v1 | 21421 | MIT | LOW 8/100 · HIGH+CRIT 0 | var · taste-skill-design-taste-frontend-v1.zip | - · A: md5 eşit: C:\Users\pc\Desktop\Portale\.claude\skills\design-taste-frontend-v1 · kök LICENSE kopyaya eklendi |
| senlindesign/taste-skill | taste | 21706 | YOK | taranmadı | yok | lisans yok |
| 21st-dev/magic-mcp | 21st-ui | 3503 | ISC | LOW 0/100 · HIGH+CRIT 0 | var · magic-mcp-21st-ui.zip | - · A: md5 eşit: 21st@21st-dev · kök LICENSE kopyaya eklendi |
| daveremy/nano-banana-2-mcp | generate-image | 3474 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · nano-banana-2-mcp-generate-image.zip | - · kök LICENSE kopyaya eklendi |
| HermeticOrmus/design-mastery-claude-code | brand-systems | 9991 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · design-mastery-claude-code-brand-systems.zip | - · kök LICENSE kopyaya eklendi |
| HermeticOrmus/design-mastery-claude-code | design-masters | 10016 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · design-mastery-claude-code-design-masters.zip | - · kök LICENSE kopyaya eklendi |
| HermeticOrmus/design-mastery-claude-code | design-movements | 12102 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · design-mastery-claude-code-design-movements.zip | - · kök LICENSE kopyaya eklendi |
| HermeticOrmus/design-mastery-claude-code | design-principles | 8052 | MIT | LOW 17/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: P2 HIGH references/typography-fundamentals.md:128 · kök LICENSE kopyaya eklendi |
| Gustavosilveira23/claude-design-skills | creative-coding | 13555 | MIT | MEDIUM 21/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: AR2 HIGH references/restraint.md:156 · kök LICENSE kopyaya eklendi |
| Gustavosilveira23/claude-design-skills | design-system | 24114 | MIT | MEDIUM 23/100 · HIGH+CRIT 0 | var · claude-design-skills-design-system.zip | - · kök LICENSE kopyaya eklendi |
| Gustavosilveira23/claude-design-skills | figma-craft | 10944 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · claude-design-skills-figma-craft.zip | - · kök LICENSE kopyaya eklendi |
| Gustavosilveira23/claude-design-skills | ui-designer | 21547 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · claude-design-skills-ui-designer.zip | - · kök LICENSE kopyaya eklendi |
| Gustavosilveira23/claude-design-skills | ux-designer | 23352 | MIT | MEDIUM 27/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: AR2 HIGH references/patterns-and-flows.md:123 · kök LICENSE kopyaya eklendi |
| Gustavosilveira23/claude-design-skills | ux-research | 24223 | MIT | LOW 13/100 · HIGH+CRIT 0 | var · claude-design-skills-ux-research.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | api-and-interface-design | 14884 | MIT | LOW 20/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:226 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | browser-testing-with-devtools | 14539 | MIT | HIGH 65/100 · HIGH+CRIT 3 | yok | 3 HIGH/CRIT, ilk: YR1 HIGH SKILL.md:64 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | ci-cd-and-automation | 11332 | MIT | MEDIUM 27/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: PE3 HIGH SKILL.md:275 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | code-review-and-quality | 20555 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-code-review-and-quality.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | code-simplification | 13545 | MIT | MEDIUM 21/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: RA1 HIGH SKILL.md:155 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | constraint-driven-development | 21008 | MIT | MEDIUM 37/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:216 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | context-engineering | 15486 | MIT | MEDIUM 33/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: PE3 HIGH SKILL.md:65 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | debugging-and-error-recovery | 10913 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-debugging-and-error-recovery.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | deprecation-and-migration | 12642 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · agent-skills-deprecation-and-migration.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | documentation-and-adrs | 9848 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-documentation-and-adrs.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | doubt-driven-development | 16647 | MIT | MEDIUM 22/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: EA5 HIGH SKILL.md:144 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | frontend-ui-engineering | 10711 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-frontend-ui-engineering.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | git-workflow-and-versioning | 14141 | MIT | MEDIUM 23/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:189 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | idea-refine | 8111 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-idea-refine.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | incremental-implementation | 9629 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · agent-skills-incremental-implementation.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | interview-me | 14359 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-interview-me.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | observability-and-instrumentation | 13948 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · agent-skills-observability-and-instrumentation.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | performance-optimization | 21717 | MIT | LOW 10/100 · HIGH+CRIT 0 | var · agent-skills-performance-optimization.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | planning-and-task-breakdown | 10564 | MIT | LOW 11/100 · HIGH+CRIT 0 | var · agent-skills-planning-and-task-breakdown.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | security-and-hardening | 27993 | MIT | HIGH 76/100 · HIGH+CRIT 7 | yok | 7 HIGH/CRIT, ilk: YR4 HIGH SKILL.md:21 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | shipping-and-launch | 11404 | MIT | MEDIUM 27/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: AR2 HIGH SKILL.md:25 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | source-driven-development | 10038 | MIT | MEDIUM 47/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: YR4 HIGH SKILL.md:101 · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | spec-driven-development | 12595 | MIT | MEDIUM 21/100 · HIGH+CRIT 0 | var · agent-skills-spec-driven-development.zip | - · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | test-driven-development | 16517 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · agent-skills-test-driven-development.zip | - · aynı ad farklı kaynakta kurulu (superpowers@claude-plugins-official), A değil · kök LICENSE kopyaya eklendi |
| addyosmani/agent-skills | using-agent-skills | 10446 | MIT | LOW 11/100 · HIGH+CRIT 0 | var · agent-skills-using-agent-skills.zip | - · kök LICENSE kopyaya eklendi |
| vercel-labs/agent-skills | vercel-composition-patterns | 2975 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | deploy-to-vercel | 12082 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | vercel-react-best-practices | 7400 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | vercel-react-native-skills | 4560 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | vercel-react-view-transitions | 14739 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | vercel-cli-with-tokens | 10829 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | vercel-optimize | 17633 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | web-design-guidelines | 1270 | YOK | taranmadı | yok | lisans yok |
| vercel-labs/agent-skills | writing-guidelines | 1272 | YOK | taranmadı | yok | lisans yok |
| billhector/design-skills | design-auditor | 24715 | MIT | MEDIUM 28/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: P2 HIGH SKILL.md:288 · kök LICENSE kopyaya eklendi |
| billhector/design-skills | design-extractor | 22262 | MIT | MEDIUM 37/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: P2 HIGH SKILL.md:142 · kök LICENSE kopyaya eklendi |
| usestrix/strix | api-security-testing | 6392 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · strix-api-security-testing.zip | - · kök LICENSE kopyaya eklendi |
| usestrix/strix | application-security-testing | 4623 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · strix-application-security-testing.zip | - · kök LICENSE kopyaya eklendi |
| usestrix/strix | ci-security-scanning-with-strix | 9029 | Apache-2.0 | HIGH 70/100 · HIGH+CRIT 6 | yok | 6 HIGH/CRIT, ilk: SC2 HIGH SKILL.md:44 · kök LICENSE kopyaya eklendi |
| usestrix/strix | find-security-vulnerabilities-in-code | 4448 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · strix-find-security-vulnerabilities-in-code.zip | - · kök LICENSE kopyaya eklendi |
| usestrix/strix | fix-security-vulnerabilities-with-strix | 6074 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · strix-fix-security-vulnerabilities-with-strix.zip | - · kök LICENSE kopyaya eklendi |
| usestrix/strix | managed-pentesting-with-strix | 23960 | Apache-2.0 | MEDIUM 22/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: SC2 HIGH SKILL.md:16 · kök LICENSE kopyaya eklendi |
| usestrix/strix | owasp-top-10-testing | 6309 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · strix-owasp-top-10-testing.zip | - · kök LICENSE kopyaya eklendi |
| usestrix/strix | penetration-testing-with-strix | 9993 | Apache-2.0 | MEDIUM 22/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: SC2 HIGH SKILL.md:46 · kök LICENSE kopyaya eklendi |
| usestrix/strix | web-app-penetration-testing | 4374 | Apache-2.0 | LOW 0/100 · HIGH+CRIT 0 | var · strix-web-app-penetration-testing.zip | - · kök LICENSE kopyaya eklendi |
| upstash/context7 | context7-cli | 3011 | MIT | MEDIUM 21/100 · HIGH+CRIT 0 | var · context7-context7-cli.zip | - · kök LICENSE kopyaya eklendi |
| upstash/context7 | context7-mcp | 2783 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · context7-context7-mcp.zip | - · kök LICENSE kopyaya eklendi |
| upstash/context7 | find-docs | 7588 | MIT | LOW 12/100 · HIGH+CRIT 0 | var · context7-find-docs.zip | - · kök LICENSE kopyaya eklendi |
| dickwu/apple-design-skill | apple-design | 25100 | YOK | taranmadı | yok | lisans yok |
| CullinanCloud/omniroute | cli-a2a | 1834 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-a2a.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-backup-sync | 4281 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-backup-sync.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-batches | 2367 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-batches.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-chat | 1455 | MIT | MEDIUM 38/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: E4 HIGH SKILL.md:3 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-compression | 2175 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-compression.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-contexts | 4792 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-contexts.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-cost-usage | 3024 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-cost-usage.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-eval | 5558 | MIT | HIGH 79/100 · HIGH+CRIT 4 | yok | 4 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-health | 1395 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-health.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-keys | 2669 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-keys.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-mcp | 1794 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-mcp.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-models | 751 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-models.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-plugins-skills | 4580 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-plugins-skills.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-policy-audit | 3079 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-policy-audit.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-providers | 8965 | MIT | HIGH 56/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-resilience | 2135 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-resilience.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-routing | 1382 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-routing.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-serve | 10750 | MIT | HIGH 74/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-setup | 3368 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-setup.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-skill-collector | 8841 | MIT | CRITICAL 88/100 · HIGH+CRIT 3 | yok | 3 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | cli-tunnel | 1461 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-cli-tunnel.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | config-codex-cli | 863 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · omniroute-config-codex-cli.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-agents-a2a | 3275 | MIT | MEDIUM 44/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-api-keys | 2085 | MIT | MEDIUM 26/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:57 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-auth | 6162 | MIT | HIGH 56/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-budget | 1222 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-budget.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-cache | 1499 | MIT | MEDIUM 30/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:26 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-cli-tools | 9557 | MIT | MEDIUM 47/100 · HIGH+CRIT 10 | yok | 10 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:75 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-combos-routing | 7307 | MIT | HIGH 77/100 · HIGH+CRIT 4 | yok | 4 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-compression | 5736 | MIT | MEDIUM 47/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-context-rtk | 2192 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-context-rtk.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-db-backups | 852 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · omniroute-omni-db-backups.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-github-skills | 1289 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · omniroute-omni-github-skills.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-inference | 17438 | MIT | MEDIUM 50/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-mcp | 3733 | MIT | MEDIUM 45/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-models | 1615 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-models.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-providers | 6898 | MIT | HIGH 53/100 · HIGH+CRIT 3 | yok | 3 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-proxies | 845 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · omniroute-omni-proxies.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-resilience | 4277 | MIT | MEDIUM 44/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH SKILL.md:5 · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-settings | 10287 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-settings.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-sync-cloud | 2540 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-sync-cloud.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-tunnels | 853 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · omniroute-omni-tunnels.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-usage-logs | 2702 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-usage-logs.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-version-manager | 11395 | MIT | LOW 6/100 · HIGH+CRIT 0 | var · omniroute-omni-version-manager.zip | - · kök LICENSE kopyaya eklendi |
| CullinanCloud/omniroute | omni-webhooks | 880 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · omniroute-omni-webhooks.zip | - · kök LICENSE kopyaya eklendi |
| rebelytics/one-skill-to-rule-them-all | task-observer | 53188 | CC-BY-4.0 | CRITICAL 100/100 · HIGH+CRIT 26 | yok | 26 HIGH/CRIT, ilk: P5 CRITICAL references/weekly-review.md:459 |
| blader/humanizer | humanizer | 29102 | MIT | MEDIUM 37/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: AR2 HIGH SKILL.md:164 |
| DietrichGebert/ponytail | ponytail | 6757 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ponytail-ponytail.zip | - · kök LICENSE kopyaya eklendi |
| DietrichGebert/ponytail | ponytail-audit | 1693 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ponytail-ponytail-audit.zip | - · kök LICENSE kopyaya eklendi |
| DietrichGebert/ponytail | ponytail-debt | 1747 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ponytail-ponytail-debt.zip | - · kök LICENSE kopyaya eklendi |
| DietrichGebert/ponytail | ponytail-gain | 2023 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ponytail-ponytail-gain.zip | - · kök LICENSE kopyaya eklendi |
| DietrichGebert/ponytail | ponytail-help | 2867 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ponytail-ponytail-help.zip | - · kök LICENSE kopyaya eklendi |
| DietrichGebert/ponytail | ponytail-review | 2440 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · ponytail-ponytail-review.zip | - · kök LICENSE kopyaya eklendi |
| multica-ai/andrej-karpathy-skills | karpathy-guidelines | 2585 | YOK | taranmadı | yok | lisans yok |
| obra/superpowers | brainstorming | 17548 | MIT | HIGH 80/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: P2 HIGH scripts/server.cjs:174 · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | diagnosing-superpowers | 6904 | MIT | MEDIUM 32/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: AR2 HIGH prompts/request-conflicts.md:19 · kök LICENSE kopyaya eklendi |
| obra/superpowers | dispatching-parallel-agents | 6078 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · superpowers-dispatching-parallel-agents.zip | - · A: md5 eşit: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | executing-plans | 20405 | MIT | LOW 17/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:140 · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | finishing-a-development-branch | 7781 | MIT | LOW 17/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:116 · A: md5 eşit: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | receiving-code-review | 6203 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · superpowers-receiving-code-review.zip | - · A: md5 eşit: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | requesting-code-review | 2977 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · superpowers-requesting-code-review.zip | - · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | subagent-driven-development | 32577 | MIT | MEDIUM 23/100 · HIGH+CRIT 1 | yok | 1 HIGH/CRIT, ilk: TM1 HIGH SKILL.md:153 · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | systematic-debugging | 9465 | MIT | HIGH 52/100 · HIGH+CRIT 3 | yok | 3 HIGH/CRIT, ilk: PE3 HIGH SKILL.md:98 · A: md5 eşit: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | test-driven-development | 9578 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · superpowers-test-driven-development.zip | - · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | using-git-worktrees | 6813 | MIT | LOW 11/100 · HIGH+CRIT 0 | var · superpowers-using-git-worktrees.zip | - · A: md5 eşit: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | using-superpowers | 3192 | MIT | HIGH 58/100 · HIGH+CRIT 2 | yok | 2 HIGH/CRIT, ilk: AS1 HIGH references/codex-tools.md:3 · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | verification-before-completion | 3646 | MIT | LOW 7/100 · HIGH+CRIT 0 | var · superpowers-verification-before-completion.zip | - · A: md5 eşit: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | writing-plans | 9092 | MIT | LOW 0/100 · HIGH+CRIT 0 | var · superpowers-writing-plans.zip | - · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| obra/superpowers | writing-skills | 26623 | MIT | CRITICAL 100/100 · HIGH+CRIT 16 | yok | 16 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:318 · A: ad + repo kurulu: superpowers@claude-plugins-official · kök LICENSE kopyaya eklendi |
| worldflowai/everything-claude-code | backend-patterns | 13757 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | clickhouse-io | 10401 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | coding-standards | 11918 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | continuous-learning | 2150 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | eval-harness | 5213 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | frontend-patterns | 14942 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | project-guidelines-example | 10011 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | security-review | 12696 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | strategic-compact | 2118 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | tdd-workflow | 10172 | YOK | taranmadı | yok | lisans yok |
| worldflowai/everything-claude-code | verification-loop | 2489 | YOK | taranmadı | yok | lisans yok |
| garrytan/gstack | gstack | 15215 | MIT | CRITICAL 100/100 · HIGH+CRIT 30 | yok | 30 HIGH/CRIT, ilk: TM1 HIGH scripts/build-app.sh:79 |
| awesome-skills/code-review-skill | code-review-skill | 12052 | MIT | CRITICAL 100/100 · HIGH+CRIT 35 | yok | 35 HIGH/CRIT, ilk: AE1 HIGH SKILL.md:125 |

Toplam: 64 kaynak · 187 skill · 99 zip adayı (SkillSpector geçti) · 30 lisans nedeniyle taranmadı
