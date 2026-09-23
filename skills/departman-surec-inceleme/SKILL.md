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

## Çakışma
- Review: `code-review` > `review` (gstack) > `pr-review-toolkit`.
