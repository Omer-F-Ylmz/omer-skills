---
name: departman-surec-plan
description: "Plan müdürü: niyet, spec, PRD ve plan sırası. Yeni iş ya da dalga başında, koda dokunmadan önce oku."
---

# Departman: surec-plan — iş sırası

Katalog: `docs/departmanlar/surec-plan.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

Skill dizini: bu klasörde `dizin.md` (Claude Code: alandaki TÜM kurulu skill'ler) ve `dizin-web.md` (claude.ai: yalnız yüklü olanlar) — ad — ne zaman. Adımdaki araç işe tam uymuyorsa ortamına uyan dizinde Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir. `ajan:` kayıtları alt ajandır: Claude Code'da Agent aracıyla (subagent_type = ad), claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

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
