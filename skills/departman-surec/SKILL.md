---
name: departman-surec
description: "Süreç müdürü: plan, spec, review, git, yayın ve kapanış sırası. Yeni iş, dalga, commit/PR ya da ship adımında oku."
---

# Departman: surec — iş sırası

Katalog: `docs/departmanlar/surec.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.

## Adımlar
1. **Niyet** — belirsiz istek: `brainstorming`; spec gerekirse `spec-driven-development`.
2. **Plan** — `writing-plans` (dalga başında `.claude/dalga.md` ≤30 satır); uygulama `executing-plans` ya da `subagent-driven-development`.
3. **Yapım disiplini** — en kısa doğru çözüm `ponytail`; ilgili departman müdürü (frontend, backend-dotnet, veri-db).
4. **Review** — `code-review` (diff), sadeleştirme `simplify`; alınan yorum `receiving-code-review`.
5. **Git** — `commit` (kırmızı ve yeşil ayrı commit), push öncesi `departman-guvenlik` adım 1.
6. **Yayın** — `ship` / `land-and-deploy`, yayın sonrası `canary`; belge güncelleme `document-release`.
7. **Kapanış** — `finishing-a-development-branch`; rapor ≤15 satır (commit · test · CI · sapma), omer-kurallar:15.

## Kapılar
- Kanıtsız "bitti" yok (`verification-before-completion`).
- Paid API/production çağrısı tavansız koşmaz.
- Üç başarısız denemeden sonra DUR raporu.

## Çakışma
- Plan: `writing-plans` > `plan` (agent-skills/ecc) > `autoplan`; aynı işte tek plan skill'i.
- Review: `code-review` > `review` (gstack) > `review-pr`.
