# KURULUM-5 — 18 Eyl 2026 · SkillSpector v2.11.2 `--no-llm --recursive` · kural: CRITICAL bulgu → DUR, HIGH satır satır incelenir
## frontend-craft 1.5.3 (omer-skills, 0c21b87)
- §4'e 5 Vercel kuralı (vercel-labs/web-interface-guidelines, MIT) · dist/frontend-craft.zip 18.769 B (bsdtar; PS5.1 Compress-Archive `\` yol yazıyor, kullanma) · `claude plugin update` 1.5.2→1.5.3
## roblox-game-development-lifecycle — KAPALI
- kaynak AshExplained/roblox-skills a3a7b94 (2026-07-01) · bakım 9★, archived=false · çift yok · izin MIT, yalnız .md, script/hook yok · context 0 (off; açık hali SKILL 5.3k B)
- SkillSpector: LOW, 0 bulgu · yer ~/.claude/skills/roblox-game-development-lifecycle (+LICENSE)
- aç: settings.json `skillOverrides` içinden `"roblox-game-development-lifecycle"` satırını sil (uzman skill'ler kurulmadı; router bunlara yönlendirir → gerekirse ayrıca)
## privacy-legal → 3 KVKK skill'i — AÇIK (plugin kurulmadı: 3 uzak MCP istenmiyor)
- kaynak ZekaiSuni/claude-for-legal-turkish 6ede1c8 (2026-05-13; tarama penceresi dışı, belge skill'i için bakım yeterli) · 104★ · Apache-2.0 · LICENSE ve kaynak satırı SKILL.md frontmatter'ının hemen altında
- policy-monitor (aydınlatma · açık rıza · çerez/CMP · VERBIS), pia-generation (VKED/PIA), use-case-triage (+references/currency-watch.md). SkillSpector üçü de LOW, 0 bulgu. Alınmayanlar: dpa-review (Drive), dsar-response, matter-workspace, cold-start-interview, customize, reg-gap-analysis
- zip (claude.ai; description ≤200 kr'ye yalnız zip'te kısaltıldı): dist/policy-monitor.zip 7.064 B · dist/pia-generation.zip 6.173 B · dist/use-case-triage.zip 7.938 B
- not: skill'ler `~/.claude/plugins/config/claude-for-legal/privacy-legal/CLAUDE.md` practice profilini okumaya çalışır; dosya yoksa profilsiz çalışır
## wpf-dev-pack → 1 skill — KAPALI (plugin kurulmadı: 24 HIGH + 4 dotnet hook)
- kaynak christian289/dotnet-with-claudecode 0ac6c06 (2026-07-21) · 41★ · MIT · her skill ayrı tarandı, frontmatter'da hook yok
- wpf-rule-mvvm-constraints (MVVM): LOW, 0 HIGH → kuruldu · wpf-rule-resourcedictionary-patterns (XAML): 1 HIGH (P2, SKILL.md:19) → alınmadı · make-wpf-custom-control (ControlTemplate): 3 HIGH (P2, SKILL.md:260/299/374) → alınmadı
## hetzner-deploy — KAPALI
- kaynak fcakyon/claude-codex-settings 38611a8 (2026-09-16) · 1.1k★ · Apache-2.0 · hook yok · SkillSpector 100/100 CRITICAL, 0 CRITICAL bulgu, 5 HIGH, satırlar aynen:
  - SKILL.md:72 `│  └─ Replace rules → hcloud firewall replace-rules --rules-file <json> <name>` · SKILL.md:135 `hcloud ssh-key create --name deploy-key --public-key-from-file ~/.ssh/id_ed25519.pub`
  - references/getting-started/{configuration,create-a-server,setup}.md:1 `<!--` (yalnız date/title/tags/priority meta verisi) → hepsi komut/yorum, OFF kuruldu
- aç (KAPALI olanlar): settings.json `skillOverrides` içinden ilgili satırı sil (roblox-game-development-lifecycle · wpf-rule-mvvm-constraints · hetzner-deploy)
## KURULMADI
- threejs-skills (CloudAI-X): lisans yok (taste-skill ile tutarlı). Lisans gelirse yeniden bak; zombi dalgası frontend-craft + Three.js resmi doküman (context7) ile gider.
- RoslynNavigator: csharp-lsp yetersiz kalırsa `dotnet tool install -g CWM.RoslynNavigator`, csharp-lsp kapatılarak A/B yapılır.
## ölçüm
- /skill-doctor listelenen context toplamı: öncesi ~12.040 (71) · sonrası ~12.330 (74); +290 = 3 açık KVKK skill'i (80+120+90), 3 KAPALI skill context "-" · plugin list 12 açık / 6 kapalı, değişmedi
- not: SkillSpector'da CRITICAL skoru ≠ CRITICAL bulgu. Skor (100/100) HIGH/MEDIUM yığılmasından geliyor; bu dalgada hiçbir kalemde CRITICAL seviyeli bulgu yoktu, bu yüzden karar satır satır HIGH incelemesiyle verildi
- tur aşımı (14 → ~30): uzun yol (Filename too long) yüzünden clone'lar sparse/longpaths ile tekrarlandı; zip ters-bölü düzeltmesi ve plugin-değil-skill yapı keşfi ek tur aldı
