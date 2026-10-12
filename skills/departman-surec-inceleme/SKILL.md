---
name: departman-surec-inceleme
description: "İnceleme müdürü: review, sadeleştirme ve doğrulama sırası. Yapım bitince, commit ya da PR öncesi oku."
---

# Departman: surec-inceleme — iş sırası

Katalog: `docs/departmanlar/surec-inceleme.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

Skill dizini: bu klasörde `dizin.md` (Claude Code: alandaki TÜM kurulu skill'ler) ve `dizin-web.md` (claude.ai: yalnız yüklü olanlar) — ad — ne zaman. Adımdaki araç işe tam uymuyorsa ortamına uyan dizinde Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir. `ajan:` kayıtları alt ajandır: Claude Code'da Agent aracıyla (subagent_type = ad), claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

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
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- discernment-nudge (1): discernment-nudge · `C:/Users/pc/.claude/plugins/cache/anthropic-agent-skills/discernment-nudge/8a1541c4a3ff/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->
