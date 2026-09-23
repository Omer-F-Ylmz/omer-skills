---
name: departman-surec-git-yayin
description: "Git ve yayın müdürü: commit, PR, CI, deploy, canary ve kapanış sırası. Commit, push, ship ya da deploy adımında oku."
---

# Departman: surec-git-yayin — iş sırası

Katalog: `docs/departmanlar/surec-git-yayin.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.

## Adımlar
1. **Dal** — yalıtım gerekirse `using-git-worktrees`; akış kuralları `git-workflow-and-versioning`.
2. **Commit** — `commit-commands` (kırmızı ve yeşil ayrı commit); push öncesi `departman-guvenlik` adım 1.
3. **CI** — `ci-cd-and-automation`; kırmızı CI'da yayın yok.
4. **Yayın** — `ship` / `land-and-deploy`; Vercel `deploy-to-vercel`; yayın sonrası `canary`.
5. **Kapanış** — `finishing-a-development-branch`; rapor ≤15 satır (commit · test · CI · sapma), omer-kurallar:15.

## Kapılar
- Kullanıcı istemeden push/deploy yok; default dalda önce dal aç.
- Sır taraması temiz olmadan push yok.
