---
name: departman-surec-inceleme
description: "İnceleme müdürü: review, sadeleştirme ve doğrulama sırası. Yapım bitince, commit ya da PR öncesi oku."
---

# Departman: surec-inceleme — iş sırası

Katalog: `docs/departmanlar/surec-inceleme.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

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

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:bl-render-ayari: renders are noisy or slow
ajan:inc-dogrulama-oncesi-bitis: Checks that claimed work is really done by
ajan:inc-ponytail-kod: code feels heavier than the task
ajan:inc-test-kalitesi-inceleme
ajan:inc-uretim-hazirligi: Reviews production readiness across logging, failure modes, security
ajan:oyn-oyun-denge: a game feels too easy or grindy
ajan:vid-gecis-ve-ritim: a cut feels slow or jumpy
sdp: ilir; baska repoda tetiklenmez
### yalnız Claude Code
aso: wants to audit or optimize an App Store
autoplan: Auto-review pipeline — reads the full CEO, design
health: Code quality dashboard
longitudinal-measurement: Tracking AI product quality over time — drift
ponytail: Lazy senior dev mode for any coding task
star-history-paket: GitHub yıldız geçmişi grafiği: refactor pass
<!-- dizin:son -->
