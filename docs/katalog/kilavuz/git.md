# git — 15 benzersiz kayıt

**Amaç:** Git ve yayın ajanları: commit mesajı, PR yönetimi, çakışma çözümü, bisect, dal stratejisi/koruma, CI boru hattı (GitHub Actions, CircleCI), monorepo, LFS, canary ve yayın öncesi kontrol.

**İç yapı:** Tümü [ajan], git-<konu>; yerel git (bisect, cakisma, commit, dal), GitHub (pr, issue, dal-koruma), CI (ci-boru-hatti, circleci, yeniden-kullanilabilir, monorepo), yayın (canary, yayin-oncesi).

## En güçlü parçalar
- `git-bisect-rehber` — Betikli kontrolle git bisect yapıp regresyonu getiren commit'i bulur.
- `git-cakisma-cozucu` — İki tarafı anlayıp merge/rebase çakışmasını çözer ve testleri yeniden koşar.
- `git-yayin-oncesi-kontrol` — Test, migration, flag, rollback için go/no-go listesi.
- `git-pr-yoneticisi` — gh CLI ile taslaktan merge'e reviewer, check, merge stratejisi.
- `git-commit-mesaji` — Diff'ten kapsam ve gerekçeli conventional commit mesajı.
- `git-ci-boru-hatti` — Önbellekli ve net hata çıktılı build/test/lint CI workflow'u.
- `git-lfs-buyuk-dosya` — Git LFS kurar, ikili dosyalarla şişmiş geçmişten büyük dosyaları taşır.
- `git-monorepo-etkilenen` — Yalnız etkilenen projeleri derleyip test ederek monorepo CI'ı hızlandırır.

## Birlikte kullanım
- git-commit-mesaji → git-pr-yoneticisi → git-yayin-oncesi-kontrol → git-canary-izleme.
- git-ci-boru-hatti + git-yeniden-kullanilabilir-is-akisi + git-dal-koruma-kurali.
- git-dal-stratejisi + vrm-worktree-paralel: paralel ajan işinde dal/worktree.

## Tuzaklar
- git-lfs-buyuk-dosya geçmişi yeniden yazar; paylaşılan repoda koordinasyon gerekir.
- git-circleci yalnız CircleCI; git-ci-boru-hatti ile örtüşür.
- daymade-skills github-* eklentileriyle PR/review kapsamı çakışır.

## Üyeler
- ajan (15): git-bisect-rehber, git-cakisma-cozucu, git-canary-izleme, git-ci-boru-hatti, git-circleci, git-coklu-repo-senkron, git-commit-mesaji, git-dal-koruma-kurali, git-dal-stratejisi, git-issue-triyaj, git-lfs-buyuk-dosya, git-monorepo-etkilenen, git-pr-yoneticisi, git-yayin-oncesi-kontrol, git-yeniden-kullanilabilir-is-akisi
