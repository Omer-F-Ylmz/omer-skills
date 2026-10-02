---
name: departman-surec-inceleme
description: "İnceleme müdürü: review, sadeleştirme ve doğrulama sırası. Yapım bitince, commit ya da PR öncesi oku."
---

# Departman: surec-inceleme — iş sırası

Katalog: `docs/departmanlar/surec-inceleme.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.

## Adımlar
1. **Sadelik** — en kısa doğru çözüm `ponytail`; fazlalık avı `ponytail-review`, sadeleştirme `code-simplification`.
2. **Review** — diff için `code-review`; kapsamlı PR `pr-review-toolkit`; istek `requesting-code-review`.
3. **Yorum** — alınan yorumu doğrulayarak uygula `receiving-code-review`.
4. **Doğrulama** — kanıt `verification-before-completion`; üretime hazır mı `production-readiness-review`.
5. **Devir** — güvenlik → `departman-guvenlik`; commit/yayın → `departman-surec-git-yayin`.

## Kapılar
- Kanıtsız "bitti" yok; test çıktısı raporda.
- Üç başarısız denemeden sonra DUR raporu.
- Kod projelerinde büyüyen tek dosya (god-file) fark edilince parçalama önerilir; uygulama ayrı karar (24b, video 2n84xa99FRY).

## Çakışma
- Review: `code-review` > `review` (gstack) > `pr-review-toolkit`.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `agent-skills:api-and-interface-design` · Guides stable API and interface design · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/api-and-interface-design/SKILL.md`
- `agent-skills:browser-testing-with-devtools` · Tests in real browsers via Chrome DevTools MCP · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/browser-testing-with-devtools/SKILL.md`
- `agent-skills:ci-cd-and-automation` · Automates CI/CD pipeline setup · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/ci-cd-and-automation/SKILL.md`
- `agent-skills:code-review-and-quality` · Conducts multi-axis code review · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/code-review-and-quality/SKILL.md`
- `agent-skills:code-simplification` · Simplifies code for clarity · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/code-simplification/SKILL.md`
- `agent-skills:constraint-driven-development` · Establishes a project's quality bar as a written contract and stops agents quietly lowering it · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/constraint-driven-development/SKILL.md`
- `agent-skills:context-engineering` · Optimizes agent context setup · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/context-engineering/SKILL.md`
- `agent-skills:debugging-and-error-recovery` · Guides systematic root-cause debugging · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/debugging-and-error-recovery/SKILL.md`
- `agent-skills:deprecation-and-migration` · Manages deprecation and migration · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/deprecation-and-migration/SKILL.md`
- `agent-skills:documentation-and-adrs` · Records decisions and documentation · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/documentation-and-adrs/SKILL.md`
- `agent-skills:doubt-driven-development` · Subjects every non-trivial decision to a fresh-context adversarial review before it stands · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/doubt-driven-development/SKILL.md`
- `agent-skills:frontend-ui-engineering` · Builds production-quality, accessible, responsive user-facing UIs · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/frontend-ui-engineering/SKILL.md`
- `agent-skills:git-workflow-and-versioning` · Structures git workflow practices · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/git-workflow-and-versioning/SKILL.md`
- `agent-skills:idea-refine` · Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/idea-refine/SKILL.md`
- `agent-skills:incremental-implementation` · Delivers changes incrementally in thin, verifiable slices · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/incremental-implementation/SKILL.md`
- `agent-skills:interview-me` · Extracts what the user actually wants instead of what they think they should want · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/interview-me/SKILL.md`
- `agent-skills:observability-and-instrumentation` · Instruments code so production behavior is visible and diagnosable · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/observability-and-instrumentation/SKILL.md`
- `agent-skills:performance-optimization` · Optimizes application performance across frontend, backend, queries, and databases · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/performance-optimization/SKILL.md`
- `agent-skills:planning-and-task-breakdown` · Breaks work into ordered tasks · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/planning-and-task-breakdown/SKILL.md`
- `agent-skills:security-and-hardening` · Hardens code against vulnerabilities · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/security-and-hardening/SKILL.md`
- `agent-skills:shipping-and-launch` · Prepares production launches · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/shipping-and-launch/SKILL.md`
- `agent-skills:source-driven-development` · Grounds every implementation decision in official documentation · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/source-driven-development/SKILL.md`
- `agent-skills:spec-driven-development` · Creates specs before coding · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/spec-driven-development/SKILL.md`
- `agent-skills:test-driven-development` · Drives development with tests using the red-green-refactor loop · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/test-driven-development/SKILL.md`
- `agent-skills:using-agent-skills` · Discovers and invokes agent skills · `C:/Users/pc/.claude/plugins/cache/addy-agent-skills/agent-skills/0.6.10/skills/using-agent-skills/SKILL.md`
- `discernment-nudge:discernment-nudge` · > · `C:/Users/pc/.claude/plugins/cache/anthropic-agent-skills/discernment-nudge/8a1541c4a3ff/skills/discernment-nudge/SKILL.md`
<!-- profil-disi:son -->
