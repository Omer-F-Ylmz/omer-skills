# KURULUM-7 · KURULUM-6 envanterinin Claude Code'a kurulumu · 19 Eyl 2026

KARAR (Ömer): hiçbir şey elenmez; tek skill kaynağı claude.ai sync (`~/.claude/skills/synced`). dist ve elenen skill'ler ~/.claude/skills'e kopyalanmadı; claude.ai'ye yüklenecekler dist/yukle-7'de. Plugin/MCP user scope, hepsi açık. Kaynak: docs/kurulum-6-cc.md, docs/kurulum-6-envanter.md. Yedek: ~/.claude/settings.json.bak7, ~/.claude.json.bak7.

## Skill sayımı

- dist kökü 101 + _yerlesik 6 = 107: 101 synced'de bayt-aynı → zaten var; canvas-design, web-artifacts-builder synced'de farklı içerik → üzerine yazılmadı (example-skills plugin'i de getiriyor); algorithmic-art, brand-guidelines, internal-comms, slack-gif-creator → zaten var (example-skills plugin), claude.ai'de Directory'den açılır.
- Elenen 88 (HIGH/CRITICAL 58 + lisanssız 26 + Anthropic 4): 42 zaten var (plugin ya da synced; Anthropic 4 synced'de → atlandı) · 41 yukle-7 · 5 yeniden adlandırıldı (yukle-7).
- Denklem: zaten var 149 + yukle-7 46 + Directory 0 = 195 = 107 + 58 + 26 + 4.

### dist/yukle-7 (46 zip, gitignore)

`python tools/skill_denetim.py dist/yukle-7` → 46 zip · 0 hata (2 tur; 13 zipte ~/.claude ve kırık yol yalnız zip kopyasında onarıldı — gstack 239 dosyada yer tutucu, design-auditor/extractor kütüphane yolu ~/.design-library; 21 açıklama ≤200 kısaltıldı). En büyük: gstack 14,6 MB.

playwright-cli-playwright-cli.zip, design-dna-design-dna.zip, taste-skill-taste.zip, claude-design-skills-creative-coding.zip, claude-design-skills-ux-designer.zip, agent-skills-vercel-composition-patterns.zip, agent-skills-deploy-to-vercel.zip, agent-skills-vercel-react-best-practices.zip, agent-skills-vercel-react-native-skills.zip, agent-skills-vercel-react-view-transitions.zip, agent-skills-vercel-cli-with-tokens.zip, agent-skills-vercel-optimize.zip, agent-skills-web-design-guidelines.zip, agent-skills-writing-guidelines.zip, design-skills-design-auditor.zip, design-skills-design-extractor.zip, strix-ci-security-scanning-with-strix.zip, strix-managed-pentesting-with-strix.zip, strix-penetration-testing-with-strix.zip, apple-design-skill-apple-design.zip, omniroute-cli-chat.zip, omniroute-cli-eval.zip, omniroute-cli-providers.zip, omniroute-cli-serve.zip, omniroute-cli-skill-collector.zip, omniroute-omni-agents-a2a.zip, omniroute-omni-api-keys.zip, omniroute-omni-auth.zip, omniroute-omni-cache.zip, omniroute-omni-cli-tools.zip, omniroute-omni-combos-routing.zip, omniroute-omni-compression.zip, omniroute-omni-inference.zip, omniroute-omni-mcp.zip, omniroute-omni-providers.zip, omniroute-omni-resilience.zip, one-skill-to-rule-them-all-task-observer.zip, humanizer-humanizer.zip, superpowers-superpowers-brainstorming.zip (brainstorming → superpowers-brainstorming), superpowers-diagnosing-superpowers.zip, superpowers-superpowers-executing-plans.zip (executing-plans → superpowers-executing-plans), superpowers-superpowers-subagent-driven-development.zip (subagent-driven-development → superpowers-subagent-driven-development), superpowers-superpowers-using-superpowers.zip (using-superpowers → superpowers-using-superpowers), superpowers-superpowers-writing-skills.zip (writing-skills → superpowers-writing-skills), gstack-gstack.zip, code-review-skill-code-review-skill.zip

### Çift kopya: synced kopya off (`anthropic-skills:<ad>`), plugin/yerel kopya açık

Ölçüt: aynı ad (superpowers-tdd ↔ test-driven-development dahil) + frontmatter hariç gövde benzerliği ≥ 0,9. 53 skill:

21st-ui (21st 1.0), brand-systems (design-mastery 0.985), brandkit (taste-skill 1.0), canvas-design (example-skills 1.0), code-review-and-quality (agent-skills 1.0), debugging-and-error-recovery (agent-skills 1.0), deprecation-and-migration (agent-skills 1.0), design-masters (design-mastery 0.983), design-movements (design-mastery 0.983), design-taste-frontend-v1 (taste-skill 1.0), dispatching-parallel-agents (superpowers 1.0), documentation-and-adrs (agent-skills 1.0), frontend-craft (frontend-craft 1.0), frontend-ui-engineering (agent-skills 1.0), full-output-enforcement (taste-skill 1.0), generate-image (nano-banana-2 1.0), gpt-taste (taste-skill 1.0), high-end-visual-design (taste-skill 1.0), idea-refine (agent-skills 1.0), image-to-code (taste-skill 1.0), imagegen-frontend-mobile (taste-skill 1.0), impeccable (impeccable 1.0), incremental-implementation (agent-skills 1.0), industrial-brutalist-ui (taste-skill 1.0), interview-me (agent-skills 1.0), mcp-builder (example-skills 1.0), minimalist-ui (taste-skill 1.0), observability-and-instrumentation (agent-skills 1.0), performance-optimization (agent-skills 1.0), pia-generation (yerel 1.0), planning-and-task-breakdown (agent-skills 1.0), policy-monitor (yerel 1.0), ponytail (ponytail 1.0), ponytail-audit (ponytail 1.0), ponytail-debt (ponytail 1.0), ponytail-gain (ponytail 1.0), ponytail-help (ponytail 1.0), ponytail-review (ponytail 1.0), receiving-code-review (superpowers 1.0), redesign-existing-projects (taste-skill 1.0), requesting-code-review (superpowers 0.996), skill-creator (skill-creator 0.995), spec-driven-development (agent-skills 1.0), stitch-design-taste (taste-skill 1.0), superpowers-tdd (superpowers 0.969), test-driven-development (agent-skills 1.0), theme-factory (example-skills 1.0), ui-ux-pro-max (yerel 0.995), use-case-triage (yerel 1.0), using-agent-skills (agent-skills 1.0), using-git-worktrees (superpowers 1.0), verification-before-completion (superpowers 1.0), web-artifacts-builder (example-skills 1.0)

Sync sonrası (yukle-7 yüklenip CC'ye gelince) plugin kopyasıyla eşleşen 4 skill için tek blok:

```powershell
$p = "$env:USERPROFILE\.claude\settings.json"; $s = Get-Content $p -Raw | ConvertFrom-Json
foreach ($n in 'superpowers-brainstorming','superpowers-subagent-driven-development','superpowers-using-superpowers','superpowers-writing-skills') { $s.skillOverrides | Add-Member -NotePropertyName "anthropic-skills:$n" -NotePropertyValue 'off' -Force }
[IO.File]::WriteAllText($p, ($s | ConvertTo-Json -Depth 30), (New-Object Text.UTF8Encoding $false))
```

### Envanterdeki 187 skill

| repo | skill | durum |
|---|---|---|
| microsoft/playwright-cli | playwright-cli | yukle-7 (sync bekliyor) |
| supabase-community/supabase-plugin | supabase | zaten var (supabase) · lisans yok — kişisel kullanım |
| supabase-community/supabase-plugin | supabase-postgres-best-practices | zaten var (supabase) · lisans yok — kişisel kullanım |
| ibelick/ui-skills | baseline-ui | zaten var (synced) |
| ibelick/ui-skills | create-design-md | zaten var (synced) |
| ibelick/ui-skills | fixing-accessibility | zaten var (synced) |
| ibelick/ui-skills | fixing-metadata | zaten var (synced) |
| ibelick/ui-skills | fixing-motion-performance | zaten var (synced) |
| ibelick/ui-skills | improve-ui | zaten var (synced) |
| ibelick/ui-skills | ui-skills-root | zaten var (synced) |
| zanwei/design-dna | design-dna | yukle-7 (sync bekliyor) |
| anthropics/skills | academy-guide | zaten var (synced) |
| anthropics/skills | algorithmic-art | zaten var (example-skills) |
| anthropics/skills | brand-guidelines | zaten var (example-skills) |
| anthropics/skills | canvas-design | zaten var (synced off; example-skills açık) |
| anthropics/skills | claude-api | zaten var (claude-api) |
| anthropics/skills | discernment-nudge | zaten var (discernment-nudge) |
| anthropics/skills | doc-coauthoring | zaten var (example-skills) · lisans yok — kişisel kullanım |
| anthropics/skills | docx | zaten var (synced (Anthropic 4 kuralı)) |
| anthropics/skills | frontend-design | zaten var (frontend-design) |
| anthropics/skills | internal-comms | zaten var (example-skills) |
| anthropics/skills | mcp-builder | zaten var (synced) |
| anthropics/skills | pdf | zaten var (synced) |
| anthropics/skills | pptx | zaten var (synced (Anthropic 4 kuralı)) |
| anthropics/skills | skill-creator | zaten var (skill-creator) |
| anthropics/skills | slack-gif-creator | zaten var (example-skills) |
| anthropics/skills | theme-factory | zaten var (synced) |
| anthropics/skills | web-artifacts-builder | zaten var (synced off; example-skills açık) |
| anthropics/skills | webapp-testing | zaten var (example-skills) |
| anthropics/skills | xlsx | zaten var (synced) |
| Leonxlnx/taste-skill | brandkit | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | industrial-brutalist-ui | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | gpt-taste | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | image-to-code | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | imagegen-frontend-mobile | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | imagegen-frontend-web | zaten var (taste-skill) |
| Leonxlnx/taste-skill | minimalist-ui | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | full-output-enforcement | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | redesign-existing-projects | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | high-end-visual-design | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | stitch-design-taste | zaten var (synced off; taste-skill açık) |
| Leonxlnx/taste-skill | design-taste-frontend | zaten var (taste-skill) |
| Leonxlnx/taste-skill | design-taste-frontend-v1 | zaten var (synced off; taste-skill açık) |
| senlindesign/taste-skill | taste | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| 21st-dev/magic-mcp | 21st-ui | zaten var (synced off; 21st açık) |
| daveremy/nano-banana-2-mcp | generate-image | zaten var (synced off; nano-banana-2 açık) |
| HermeticOrmus/design-mastery-claude-code | brand-systems | zaten var (synced off; design-mastery açık) |
| HermeticOrmus/design-mastery-claude-code | design-masters | zaten var (synced off; design-mastery açık) |
| HermeticOrmus/design-mastery-claude-code | design-movements | zaten var (synced off; design-mastery açık) |
| HermeticOrmus/design-mastery-claude-code | design-principles | zaten var (design-mastery) |
| Gustavosilveira23/claude-design-skills | creative-coding | yukle-7 (sync bekliyor) |
| Gustavosilveira23/claude-design-skills | design-system | zaten var (synced) |
| Gustavosilveira23/claude-design-skills | figma-craft | zaten var (synced) |
| Gustavosilveira23/claude-design-skills | ui-designer | zaten var (synced) |
| Gustavosilveira23/claude-design-skills | ux-designer | yukle-7 (sync bekliyor) |
| Gustavosilveira23/claude-design-skills | ux-research | zaten var (synced) |
| addyosmani/agent-skills | api-and-interface-design | zaten var (agent-skills) |
| addyosmani/agent-skills | browser-testing-with-devtools | zaten var (agent-skills) |
| addyosmani/agent-skills | ci-cd-and-automation | zaten var (agent-skills) |
| addyosmani/agent-skills | code-review-and-quality | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | code-simplification | zaten var (agent-skills) |
| addyosmani/agent-skills | constraint-driven-development | zaten var (agent-skills) |
| addyosmani/agent-skills | context-engineering | zaten var (agent-skills) |
| addyosmani/agent-skills | debugging-and-error-recovery | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | deprecation-and-migration | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | documentation-and-adrs | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | doubt-driven-development | zaten var (agent-skills) |
| addyosmani/agent-skills | frontend-ui-engineering | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | git-workflow-and-versioning | zaten var (agent-skills) |
| addyosmani/agent-skills | idea-refine | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | incremental-implementation | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | interview-me | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | observability-and-instrumentation | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | performance-optimization | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | planning-and-task-breakdown | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | security-and-hardening | zaten var (agent-skills) |
| addyosmani/agent-skills | shipping-and-launch | zaten var (agent-skills) |
| addyosmani/agent-skills | source-driven-development | zaten var (agent-skills) |
| addyosmani/agent-skills | spec-driven-development | zaten var (synced off; agent-skills açık) |
| addyosmani/agent-skills | test-driven-development | zaten var (synced off; superpowers,agent-skills açık) |
| addyosmani/agent-skills | using-agent-skills | zaten var (synced off; agent-skills açık) |
| vercel-labs/agent-skills | vercel-composition-patterns | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | deploy-to-vercel | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | vercel-react-best-practices | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | vercel-react-native-skills | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | vercel-react-view-transitions | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | vercel-cli-with-tokens | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | vercel-optimize | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | web-design-guidelines | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| vercel-labs/agent-skills | writing-guidelines | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| billhector/design-skills | design-auditor | yukle-7 (sync bekliyor) |
| billhector/design-skills | design-extractor | yukle-7 (sync bekliyor) |
| usestrix/strix | api-security-testing | zaten var (synced) |
| usestrix/strix | application-security-testing | zaten var (synced) |
| usestrix/strix | ci-security-scanning-with-strix | yukle-7 (sync bekliyor) |
| usestrix/strix | find-security-vulnerabilities-in-code | zaten var (synced) |
| usestrix/strix | fix-security-vulnerabilities-with-strix | zaten var (synced) |
| usestrix/strix | managed-pentesting-with-strix | yukle-7 (sync bekliyor) |
| usestrix/strix | owasp-top-10-testing | zaten var (synced) |
| usestrix/strix | penetration-testing-with-strix | yukle-7 (sync bekliyor) |
| usestrix/strix | web-app-penetration-testing | zaten var (synced) |
| upstash/context7 | context7-cli | zaten var (synced) |
| upstash/context7 | context7-mcp | zaten var (synced) |
| upstash/context7 | find-docs | zaten var (synced) |
| dickwu/apple-design-skill | apple-design | yukle-7 (sync bekliyor) · lisans yok — kişisel kullanım |
| CullinanCloud/omniroute | cli-a2a | zaten var (synced) |
| CullinanCloud/omniroute | cli-backup-sync | zaten var (synced) |
| CullinanCloud/omniroute | cli-batches | zaten var (synced) |
| CullinanCloud/omniroute | cli-chat | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | cli-compression | zaten var (synced) |
| CullinanCloud/omniroute | cli-contexts | zaten var (synced) |
| CullinanCloud/omniroute | cli-cost-usage | zaten var (synced) |
| CullinanCloud/omniroute | cli-eval | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | cli-health | zaten var (synced) |
| CullinanCloud/omniroute | cli-keys | zaten var (synced) |
| CullinanCloud/omniroute | cli-mcp | zaten var (synced) |
| CullinanCloud/omniroute | cli-models | zaten var (synced) |
| CullinanCloud/omniroute | cli-plugins-skills | zaten var (synced) |
| CullinanCloud/omniroute | cli-policy-audit | zaten var (synced) |
| CullinanCloud/omniroute | cli-providers | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | cli-resilience | zaten var (synced) |
| CullinanCloud/omniroute | cli-routing | zaten var (synced) |
| CullinanCloud/omniroute | cli-serve | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | cli-setup | zaten var (synced) |
| CullinanCloud/omniroute | cli-skill-collector | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | cli-tunnel | zaten var (synced) |
| CullinanCloud/omniroute | config-codex-cli | zaten var (synced) |
| CullinanCloud/omniroute | omni-agents-a2a | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-api-keys | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-auth | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-budget | zaten var (synced) |
| CullinanCloud/omniroute | omni-cache | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-cli-tools | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-combos-routing | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-compression | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-context-rtk | zaten var (synced) |
| CullinanCloud/omniroute | omni-db-backups | zaten var (synced) |
| CullinanCloud/omniroute | omni-github-skills | zaten var (synced) |
| CullinanCloud/omniroute | omni-inference | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-mcp | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-models | zaten var (synced) |
| CullinanCloud/omniroute | omni-providers | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-proxies | zaten var (synced) |
| CullinanCloud/omniroute | omni-resilience | yukle-7 (sync bekliyor) |
| CullinanCloud/omniroute | omni-settings | zaten var (synced) |
| CullinanCloud/omniroute | omni-sync-cloud | zaten var (synced) |
| CullinanCloud/omniroute | omni-tunnels | zaten var (synced) |
| CullinanCloud/omniroute | omni-usage-logs | zaten var (synced) |
| CullinanCloud/omniroute | omni-version-manager | zaten var (synced) |
| CullinanCloud/omniroute | omni-webhooks | zaten var (synced) |
| rebelytics/one-skill-to-rule-them-all | task-observer | yukle-7 (sync bekliyor) |
| blader/humanizer | humanizer | yukle-7 (sync bekliyor) |
| DietrichGebert/ponytail | ponytail | zaten var (synced off; ponytail açık) |
| DietrichGebert/ponytail | ponytail-audit | zaten var (synced off; ponytail açık) |
| DietrichGebert/ponytail | ponytail-debt | zaten var (synced off; ponytail açık) |
| DietrichGebert/ponytail | ponytail-gain | zaten var (synced off; ponytail açık) |
| DietrichGebert/ponytail | ponytail-help | zaten var (synced off; ponytail açık) |
| DietrichGebert/ponytail | ponytail-review | zaten var (synced off; ponytail açık) |
| multica-ai/andrej-karpathy-skills | karpathy-guidelines | zaten var (andrej-karpathy-skills) · lisans yok — kişisel kullanım |
| obra/superpowers | brainstorming | yeniden adlandırıldı → superpowers-brainstorming (yukle-7; mevcut: superpowers) |
| obra/superpowers | diagnosing-superpowers | yukle-7 (sync bekliyor) |
| obra/superpowers | dispatching-parallel-agents | zaten var (synced off; superpowers açık) |
| obra/superpowers | executing-plans | yeniden adlandırıldı → superpowers-executing-plans (yukle-7; mevcut: superpowers) |
| obra/superpowers | finishing-a-development-branch | zaten var (superpowers) |
| obra/superpowers | receiving-code-review | zaten var (synced off; superpowers açık) |
| obra/superpowers | requesting-code-review | zaten var (synced off; superpowers açık) |
| obra/superpowers | subagent-driven-development | yeniden adlandırıldı → superpowers-subagent-driven-development (yukle-7; mevcut: superpowers) |
| obra/superpowers | systematic-debugging | zaten var (superpowers) |
| obra/superpowers | test-driven-development | zaten var (synced off;  açık) · ad: superpowers-tdd |
| obra/superpowers | using-git-worktrees | zaten var (synced off; superpowers açık) |
| obra/superpowers | using-superpowers | yeniden adlandırıldı → superpowers-using-superpowers (yukle-7; mevcut: superpowers) |
| obra/superpowers | verification-before-completion | zaten var (synced off; superpowers açık) |
| obra/superpowers | writing-plans | zaten var (synced) |
| obra/superpowers | writing-skills | yeniden adlandırıldı → superpowers-writing-skills (yukle-7; mevcut: superpowers) |
| worldflowai/everything-claude-code | backend-patterns | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | clickhouse-io | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | coding-standards | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | continuous-learning | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | eval-harness | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | frontend-patterns | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | project-guidelines-example | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | security-review | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | strategic-compact | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | tdd-workflow | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| worldflowai/everything-claude-code | verification-loop | zaten var (everything-claude-code) · lisans yok — kişisel kullanım |
| garrytan/gstack | gstack | yukle-7 (sync bekliyor) |
| awesome-skills/code-review-skill | code-review-skill | yukle-7 (sync bekliyor) |

## PLUGIN (kurulum-6-cc.md sırasıyla, 44 satır)

- P1 claude-mem@thedotmack · kuruldu
- P2 claude-mem-cowork@thedotmack · kuruldu · değişken: CMEM_API_KEY (hook'lar cmem.ai bulut senkronu; anahtarsız pasif)
- P3 headroom@headroom-marketplace · kuruldu · önkoşul: headroom CLI (PATH'te yok; hook `headroom init hook ensure`) · ANTHROPIC_BASE_URL yazmıyor
- P4 supabase@yerel-kurulum7 · kuruldu (marketplace.json yok → C:/Projeler/.tmp-kurulum6/.claude-plugin yerel marketplace) · önkoşul: Supabase oturumu (MCP "Needs authentication") · lisans yok
- P5 document-skills@anthropic-agent-skills · zaten vardı (docx/pdf/pptx/xlsx synced)
- P6 example-skills@anthropic-agent-skills · kuruldu · repo lisansı yok
- P7 claude-api@anthropic-agent-skills · kuruldu
- P8 academy-guide@anthropic-agent-skills · zaten vardı (synced)
- P9 discernment-nudge@anthropic-agent-skills · kuruldu
- P10 agent-sdk-dev@claude-code-plugins · kuruldu · lisans özel (Anthropic ticari koşulları; bu satırdan P22'ye kadar aynı)
- P11 claude-opus-4-5-migration@claude-code-plugins · kuruldu
- P12 code-review@claude-code-plugins · kuruldu
- P13 commit-commands@claude-code-plugins · kuruldu
- P14 explanatory-output-style@claude-code-plugins · kuruldu · SessionStart ~260 token
- P15 feature-dev@claude-code-plugins · kuruldu
- P16 frontend-design@claude-code-plugins · zaten vardı (frontend-design@claude-plugins-official)
- P17 hookify@claude-code-plugins · kuruldu · hook engeli (matcher'sız PreToolUse; .local.md kuralına göre her aracı engelleyebilir; plugin açık)
- P18 learning-output-style@claude-code-plugins · kuruldu · SessionStart ~675 token
- P19 plugin-dev@claude-code-plugins · zaten vardı (plugin-dev@claude-plugins-official, kapalı; dokunulmadı)
- P20 pr-review-toolkit@claude-code-plugins · kuruldu
- P21 ralph-wiggum@claude-code-plugins · kuruldu
- P22 security-guidance@claude-code-plugins · kuruldu · git commit/push'ta asyncRewake ajan incelemesi
- P23 claude-plugins-official · zaten vardı
- P24 taste-skill@taste-skill · kuruldu
- P25 scroll-craft (nateherk-design@nateherk) · zaten vardı
- P26 magic-mcp (21st@21st-dev) · zaten vardı
- P27 nano-banana-2@nano-banana-2-plugins · kuruldu · değişken: GEMINI_API_KEY (ücretli/kotalı; çağrı yapılmadı)
- P28 ui-ux-pro-max · zaten vardı (~/.claude/skills)
- P29 design-mastery@design-mastery · kuruldu
- P30 agent-skills@addy-agent-skills · kuruldu (SSH host-key hatası → tek komutluk GIT_CONFIG https insteadOf; global git ayarı değişmedi)
- P31 context7 · zaten vardı
- P32 cli-anything@cli-anything · kuruldu
- P33 humanizer@humanizer · kuruldu
- P34 ponytail@ponytail · kuruldu
- P35 impeccable · zaten vardı
- P36 andrej-karpathy-skills@karpathy-skills · kuruldu · lisans yok
- P37 superpowers · zaten vardı (açık)
- P38 everything-claude-code@everything-claude-code · kuruldu · lisans yok
- P39 phoenix-security-review@phoenix-security · kuruldu
- P40 phoenix-readiness-reviews@phoenix-security · kuruldu
- P41 phoenix-sast-rules@phoenix-security · kuruldu
- P42 phoenix-cti-search@phoenix-security · kuruldu
- P43 phoenix-prd-pipeline@phoenix-security · kuruldu
- P44 phoenix-docs-research@phoenix-security · kuruldu

## MCP (21 satır; anahtarlar ~/.claude.json'da `${VAR}` literal, düz anahtar 0)

- M1 claude-mem · zaten vardı (plugin: mcp-search ✔)
- M2 headroom · kuruldu ✔
- M3 stitch · kuruldu · önkoşul: gcloud + Google Cloud hesabı (init yapılmadı) ✘
- M4 nano-banana-2 · zaten vardı (plugin P27 ✔) · değişken: GEMINI_API_KEY
- M5 context7 · zaten vardı ✔
- M6 Agent-Reach · zaten vardı (CLI + skill)
- M7 omniroute · kuruldu · npx paket kurulumu rc=1 (136 s) → bağlanamıyor ✘
- M8 puppeteer · kuruldu ✔
- M9 mcp-everything · kuruldu ✔ (pin 2.0.0 npm'de yok → 2026.8.31)
- M10 mcp-fetch · kuruldu ✔ (0.6.3 PyPI'de yok → 2026.8.18)
- M11 mcp-filesystem · kuruldu ✔ (0.6.3 yok → 2026.8.31; dizinler C:/Users/pc/Desktop, C:/Projeler)
- M12 mcp-git · kuruldu ✔ (0.6.2 güncel mcp kütüphanesiyle kırık → 2026.8.18)
- M13 mcp-memory · kuruldu ✔ (0.6.3 yok → 2026.8.31)
- M14 mcp-sequential-thinking · kuruldu ✔ (0.6.2)
- M15 mcp-time · kuruldu ✔ (0.6.2 kırık → 2026.8.18)
- M16 brave-search · kuruldu · değişken: BRAVE_API_KEY
- M17 github (http) · kuruldu · değişken: GITHUB_PAT
- M18 github (Docker alternatifi) · önkoşul: Docker (eklenmedi)
- M19 Graphify-Labs/graphify · zaten vardı
- M20 safishamsi/graphify · zaten vardı (aynı repo; ikinci graphify kurulmadı)
- M21 code-review · kuruldu ✔ · değişken: GITHUB_TOKEN, GITLAB_TOKEN

Not: Git Bash'ten başlatılan süreçte `cmd /c npx` npx'i çözemiyor (PowerShell ortamında çalışıyor); `claude mcp list` PowerShell'den alındı.

## claude plugin list / claude mcp list özeti

- Plugin: önceki 16 (+4 synced kapalı) + bu dalgada 30 kurulum (P1–P4, P6, P7, P9–P15, P17, P18, P20–P22, P24, P27, P29, P30, P32–P34, P36, P38–P44), hepsi ✔ enabled. Kapalı kalan (önceden): plugin-dev, claude-md-management.
- MCP ✔: mslearn, claude-design, 21st, context7, headroom, puppeteer, mcp-everything, mcp-fetch, mcp-filesystem, mcp-git, mcp-memory, mcp-sequential-thinking, mcp-time, brave-search (anahtarsız başlıyor), code-review, plugin:claude-mem:mcp-search, plugin:nano-banana-2, plugin:dotnet-msbuild:binlog. ✘: stitch (önkoşul), omniroute, github (değişken), plugin:playwright (önceden de ✘). !: plugin:supabase (auth).

## Hook'lar (yeni plugin'ler · olay · matcher · komut · SessionStart token)

settings.json `hooks` bloğu .bak7 ile aynı (rtk / block-destructive / dotnet-format korunuyor); hiçbir plugin ANTHROPIC_BASE_URL/API_KEY yazmadı.

- claude-mem · Setup, SessionStart ×2, UserPromptSubmit, PostToolUse, PreToolUse (async), Stop, SessionEnd · çeşitli · node worker-service.cjs hook … · dinamik (bellek bağlamı)
- claude-mem-cowork · SessionStart, UserPromptSubmit, PostToolUse, PreToolUse, SubagentStop, Stop, SessionEnd · Task|Agent / * · node cmem-hook.mjs (cmem.ai HTTP) · dinamik
- headroom · SessionStart, PreToolUse · startup|resume / Bash|PowerShell · headroom init hook ensure · dinamik (CLI yok → hata verir, engellemez)
- explanatory-output-style · SessionStart · (tümü) · hooks-handlers/session-start.sh · ~260 token
- learning-output-style · SessionStart · (tümü) · hooks-handlers/session-start.sh · ~675 token
- hookify · PreToolUse, PostToolUse, Stop, UserPromptSubmit · (matcher yok = tüm araçlar) · python3 hooks/*.py · **hook engeli** (.local.md kurallarıyla her Bash/Grep/Read'i engelleyebilir)
- ralph-wiggum · Stop · (tümü) · hooks/stop-hook.sh
- security-guidance · SessionStart, UserPromptSubmit, PostToolUse ×2, Stop · Edit|Write|MultiEdit|NotebookEdit / Bash (git commit/push) · sg-python.sh ensure_agent_sdk.py, security_reminder_hook.py · dinamik
- everything-claude-code · PreToolUse ×4, PreCompact, SessionStart, PostToolUse ×4, Stop, SessionEnd ×2 · hedefli (Bash + belirli komutlar) · node -e … · dinamik
- ponytail · SessionStart, SubagentStart, UserPromptSubmit · startup|resume|clear|compact · node hooks/ponytail-activate.js · dinamik

## Görünürlük ve ölçüm

- L (etkin skill + komut açıklamaları, off hariç) = 97.257 karakter, 296 girdi → `SLASH_COMMAND_TOOL_CHAR_BUDGET` = 106.983 (ceil L×1,1).
- Girdi token'ı (boş klasör, `claude -p`, Git Bash): 49.952 → 78.076.
- Görülen skill sayısı 293; beklenen 311 (296 + 15 yerleşik; ölçüm anında hatayla off olan 5 synced skill düşülürse 306) → **sapma 13–18 (>5)**. Olası sebepler: ~300 girdiyi modelin sayma hatası, bare-ad skillOverrides anahtarlarının plugin skill'lerini de kapatması.
- ~/.claude/CLAUDE.md: graphify'ın iki satırı birleşti, skill öncelik kuralı eklendi (CLAUDE.md + RTK.md 3.185 karakter ≈ 850 token).

## Kurulmayanlar

- KÜTÜPHANE (18) ve ÖRNEK (2) kurulmadı; proje eşlemesi docs/kurulum-6-cc.md'de.

