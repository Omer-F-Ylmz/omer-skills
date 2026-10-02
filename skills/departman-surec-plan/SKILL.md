---
name: departman-surec-plan
description: "Plan müdürü: niyet, spec, PRD ve plan sırası. Yeni iş ya da dalga başında, koda dokunmadan önce oku."
---

# Departman: surec-plan — iş sırası

Katalog: `docs/departmanlar/surec-plan.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.

## Adımlar
1. **Niyet** — belirsiz istek: `brainstorming`; eksik gereksinim `interview-me`, ham fikir `idea-refine`.
2. **Spec** — `spec-driven-development`; ürün/PRD gerekirse `prd-generator` (tam hat `phoenix-orchestrator`).
3. **Plan** — `writing-plans` (dalga başında `.claude/dalga.md` ≤30 satır); görev kırılımı `planning-and-task-breakdown`.
4. **Plan incelemesi** — büyük işte `plan-eng-review`, tasarımlı işte `plan-design-review`; hazır mı kararı `plan-readiness-review`.
5. **Yürütme** — `executing-plans` ya da `subagent-driven-development`; yapımda ilgili departman müdürü, bitince `departman-surec-inceleme`.

## Kapılar
- Kabul kriteri yazılmadan yapım yok; belirsizlikte soru değil DUR raporu.
- Paid API/production çağrısı tavansız plana girmez.

## Çakışma
- Plan: `writing-plans` > `make-plan` > `autoplan`; aynı işte tek plan skill'i.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `phoenix-prd-pipeline:phoenix-ambiguity-hunter` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-ambiguity-hunter/SKILL.md`
- `phoenix-prd-pipeline:phoenix-batch-planner` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-batch-planner/SKILL.md`
- `phoenix-prd-pipeline:phoenix-constraint-distiller` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-constraint-distiller/SKILL.md`
- `phoenix-prd-pipeline:phoenix-context-curator` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-context-curator/SKILL.md`
- `phoenix-prd-pipeline:phoenix-contract-architect` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-contract-architect/SKILL.md`
- `phoenix-prd-pipeline:phoenix-final-gate` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-final-gate/SKILL.md`
- `phoenix-prd-pipeline:phoenix-orchestrator` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-orchestrator/SKILL.md`
- `phoenix-prd-pipeline:phoenix-pipeline-navigator` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-pipeline-navigator/SKILL.md`
- `phoenix-prd-pipeline:phoenix-requirements-engineer` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-requirements-engineer/SKILL.md`
- `phoenix-prd-pipeline:phoenix-scope-cutter` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-scope-cutter/SKILL.md`
- `phoenix-prd-pipeline:phoenix-security-engineer` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-security-engineer/SKILL.md`
- `phoenix-prd-pipeline:phoenix-verification-matrix` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/phoenix-verification-matrix/SKILL.md`
- `phoenix-prd-pipeline:prd-generator` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/prd-generator/SKILL.md`
- `phoenix-readiness-reviews:plan-readiness-review` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-readiness-reviews/1.0.0/skills/plan-readiness-review/SKILL.md`
- `phoenix-readiness-reviews:production-readiness-review` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-readiness-reviews/1.0.0/skills/production-readiness-review/SKILL.md`
- `roblox-game-development-lifecycle` · Orchestrate the full Roblox game development lifecycle · `C:/Users/pc/.claude/skills/roblox-game-development-lifecycle/SKILL.md`
<!-- profil-disi:son -->
