---
name: departman-surec-plan
description: "Plan müdürü: niyet, spec, PRD ve plan sırası. Yeni iş ya da dalga başında, koda dokunmadan önce oku."
---

# Departman: surec-plan — iş sırası

Katalog: `docs/departmanlar/surec-plan.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

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
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- phoenix-prd-pipeline (13): phoenix-ambiguity-hunter, phoenix-batch-planner, phoenix-constraint-distiller, phoenix-context-curator, phoenix-contract-architect, phoenix-final-gate, phoenix-orchestrator, phoenix-pipeline-navigator, phoenix-requirements-engineer, phoenix-scope-cutter, phoenix-security-engineer, phoenix-verification-matrix, prd-generator · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-prd-pipeline/1.0.0/skills/<ad>/SKILL.md`
- phoenix-readiness-reviews (2): plan-readiness-review, production-readiness-review · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-readiness-reviews/1.0.0/skills/<ad>/SKILL.md`
- roblox-game-development-lifecycle (1): roblox-game-development-lifecycle · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:bl-modelleme-plani
ajan:bl-rig-iskelet: a model must pose or deform
ajan:pln-bagimlilik-haritasi: sequencing a large plan
ajan:pln-dalga-plani
ajan:pln-fikir-olgunlastir
ajan:pln-gorev-bolme: work must be sequenced
ajan:pln-kabul-olcutleri: a story lacks done criteria
ajan:pln-kapsam-kesici: scope grows or a deadline is near
ajan:pln-karar-kaydi: Records decisions with context, choice and reason in
ajan:pln-mimari-plan
ajan:pln-niyet-netlestirme: a task is ambiguous
ajan:pln-prd-yazar
ajan:pln-risk-kaydi: planning a risky change
ajan:pln-teknik-spec
ajan:vid-premiere-akis
### yalnız Claude Code
do: asked to execute, run, or carry out a
grilling: kaçın: başkasına soru formu → to-questionnaire
lifekernel-daily-circle: Run a 10-20 minute evening conversation that records
lifekernel-onboarding: Interview a new user and fill a Life
loop-me: Grill me about specs for the workflows I
pathfinder: asked to "find the ideal path," unify duplicated
wayfinder: Plan a huge chunk of work (more than
<!-- dizin:son -->
