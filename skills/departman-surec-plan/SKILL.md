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
