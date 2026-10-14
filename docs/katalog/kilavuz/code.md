# code — 4 benzersiz kayıt

**Amaç:** Kod incelemesi ve sadeleştirme: diff/dal/PR incelemesi, merge öncesi kalite, çok dilli inceleme rehberi, okunabilirlik için sadeleştirme.

**İç yapı:** Tümü [skill]; üç inceleme varyantı (code-review, code-review-and-quality, code-review-skill) + code-simplifier.

## En güçlü parçalar
- `code-review-and-quality` — Kendi, başka ajanın ya da insanın kodunu merge öncesi incelemek.
- `code-review-skill` — React'ten Kotlin'e çok dil/çerçeve için inceleme rehberi.
- `code-simplifier` — Son değişen kodu netlik ve okunabilirlik için sadeleştirme.

## Birlikte kullanım
- code-review → code-simplifier.
- inc ailesi ajanlarıyla.

## Tuzaklar
- Üç inceleme skill'i örtüşür; claude-code-plugins code-review eklentisiyle de çakışır.

## Üyeler
- skill (4): code-review, code-review-and-quality, code-review-skill, code-simplifier
