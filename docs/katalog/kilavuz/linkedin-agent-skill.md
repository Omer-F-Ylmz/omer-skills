# linkedin-agent-skill — 12 benzersiz kayıt

**Amaç:** Bir LinkedIn hesabını yöneten 11 skill: 21 hook formülüyle gönderi, yorum, yanıt, DM, gelen kutusu triyajı, profil puanı, haftalık plan, carousel, yeniden kullanım, insanlaştırma.

**İç yapı:** linkedin-agent [plugin] + linkedin-agent:li-<iş> alt skill'leri; içerik üretimi (post, carousel, repurpose), etkileşim (comment, reply, dm, inbox), analiz (audit, profile, plan), li-human.

## En güçlü parçalar
- `linkedin-agent:li-post` — Gönderi, hook ya da feed taslağı istendiğinde.
- `linkedin-agent:li-audit` — Analitik/eski gönderiler yapıştırılıp 'ne işe yarıyor' sorulduğunda.
- `linkedin-agent:li-plan` — Haftalık plan, içerik takvimi, 'ne paylaşsam' durumunda.
- `linkedin-agent:li-human` — Metni insan sesine çevirme, em dash temizleme, AI izi giderme.
- `linkedin-agent:li-repurpose` — Video/bülten/transkripti gönderilere çevirir.
- `linkedin-agent:li-profile` — Profil puanlama, başlık ve hakkında bölümü yeniden yazımı.

## Birlikte kullanım
- li-plan → li-post → li-human: plan, taslak, insanlaştırma.
- li-audit → li-plan: işe yarayanı bulup planı ona göre kurmak.
- sepia ailesi de-AI yazımında li-human ile örtüşür.

## Tuzaklar
- li-human ile sepia:sepia ve yerel insanlaştırma skill'leri çakışır.
- Skill'ler yapıştırılan metinle çalışır; LinkedIn API erişimi katalog metninde belirtilmemiş.

## Üyeler
- plugin (1): linkedin-agent
- skill (11): linkedin-agent:li-audit, linkedin-agent:li-carousel, linkedin-agent:li-comment, linkedin-agent:li-dm, linkedin-agent:li-human, linkedin-agent:li-inbox, linkedin-agent:li-plan, linkedin-agent:li-post, linkedin-agent:li-profile, linkedin-agent:li-reply, linkedin-agent:li-repurpose
