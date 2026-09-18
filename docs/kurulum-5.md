# KURULUM-5 — 18 Eyl 2026 · SkillSpector v2.11.2 `--no-llm --recursive` · kural: CRITICAL/DO NOT INSTALL → kalem DUR
## frontend-craft 1.5.3 (omer-skills, 0c21b87)
- §4'e 5 Vercel kuralı (vercel-labs/web-interface-guidelines, MIT) · dist/frontend-craft.zip 18.769 B (bsdtar; PS5.1 Compress-Archive `\` yol yazıyor, kullanma) · `claude plugin update` 1.5.2→1.5.3
## roblox-game-development-lifecycle — KAPALI
- kaynak AshExplained/roblox-skills a3a7b94 (2026-07-01) · bakım 9★, archived=false · çift yok · izin MIT, yalnız .md, script/hook yok · context 0 (off; açık hali SKILL 5.3k B)
- SkillSpector: LOW, 0 bulgu · yer ~/.claude/skills/roblox-game-development-lifecycle (+LICENSE)
- aç: settings.json `skillOverrides` içinden `"roblox-game-development-lifecycle"` satırını sil (uzman skill'ler kurulmadı; router bunlara yönlendirir → gerekirse ayrıca)
## privacy-legal — DUR (yapı)
- kaynak ZekaiSuni/claude-for-legal-turkish 6ede1c8 (2026-05-13; tarama penceresi dışı, ama belge skill'i için bakım yeterli, 104★, Apache-2.0)
- SkillSpector: LOW/SAFE, 0 bulgu
- DUR sebebi: tek SKILL.md değil, 9 skill'li plugin (cold-start-interview, dpa-review, dsar-response, pia-generation…) + CLAUDE.md + .mcp.json (3 uzak HTTP MCP: Google Drive, Slack, Yargı MCP/surucu.dev); hooks.json boş. `~/.claude/skills/privacy-legal` ve `<ad>/SKILL.md` zip'i bu yapıya uymuyor → karar gerek
## wpf-dev-pack — DUR (SkillSpector)
- kaynak christian289/dotnet-with-claudecode 0ac6c06 (2026-07-21) · 41★, MIT · 28 skill + agents + monitors + .mcp.json
- SkillSpector: 100/100 CRITICAL, DO NOT INSTALL · 0 CRITICAL, 24 HIGH, 24 MEDIUM (P2 gizli talimat, AS1 agent config erişimi, RA1 self-modification; çoğu docs/superpowers/plans) · ayrıca 4 SessionStart hook (`dotnet *.cs`, startup|resume|clear|compact)
- ileride açılacak skill'ler: wpf-rule-mvvm-constraints, make-wpf-viewmodel, wpf-rule-view-viewmodel-wiring-communitytoolkit (MVVM) · wpf-rule-resourcedictionary-patterns (XAML) · make-wpf-custom-control (ControlTemplate)
## hetzner-deploy — DUR (SkillSpector)
- kaynak fcakyon/claude-codex-settings plugins/hetzner-skills 38611a8 (2026-09-16) · 1.1k★, Apache-2.0 · hook yok (doğrulandı), yalnız SKILL.md + references
- SkillSpector: 100/100 CRITICAL, DO NOT INSTALL · 0 CRITICAL, 5 HIGH, 580 MEDIUM; HIGH'lar hcloud CLI satırı (SKILL.md:72, :135) ve references'taki `<!--` yorumları → büyük olasılıkla yanlış pozitif
- kur (onaylanırsa): klasörü `~/.claude/skills/hetzner-deploy`'a kopyala + `skillOverrides` "off"
## KURULMADI
- threejs-skills (CloudAI-X): lisans yok (taste-skill ile tutarlı). Lisans gelirse yeniden bak; zombi dalgası frontend-craft + Three.js resmi doküman (context7) ile gider.
- RoslynNavigator: csharp-lsp yetersiz kalırsa `dotnet tool install -g CWM.RoslynNavigator`, csharp-lsp kapatılarak A/B yapılır.
## ölçüm
- /skill-doctor listelenen context toplamı: öncesi ~12.040 · sonrası ~12.040 (71 satır; roblox satırı context "-") · plugin list 12 açık / 6 kapalı → aynı
