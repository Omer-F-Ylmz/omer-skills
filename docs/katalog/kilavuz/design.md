# design — 16 benzersiz kayıt

**Amaç:** Tasarım sistemi çıkarma/denetleme, tasarım danışmanlığı, AI slop'a karşı ön yüz zevki, varyant üretimi ve tasarım tarihi bilgisi; ayrıca oyun savaş/karşılaşma tasarımı.

**İç yapı:** Ad kalıbı design-<konu>; 15 [skill] + 1 [ajan] (design-persona-walkthrough); gruplar: sistem (auditor, extractor, dna, system), süreç (consultation, shotgun, review, html), ön yüz zevki (taste-frontend, taste-frontend-v1, first-ui-prompting), bilgi (masters, movements), oyun (action-combat, game-encounters).

## En güçlü parçalar
- `design-extractor` — Web sitesi URL'sinden görsel tasarım sistemi çıkarıp DESIGN.md, Tailwind v4 teması ve erişilebilirlik raporu üretir.
- `design-auditor` — Projenin CSS, Tailwind config ve HTML şablonlarından tasarım sistemini denetler.
- `design-review` — Görsel tutarsızlık, boşluk, hiyerarşi sorunu, AI slop ve yavaş etkileşim bulan tasarımcı gözü QA.
- `design-consultation` — Ürünü anlayıp alanı araştırarak eksiksiz tasarım sistemi önerir.
- `design-shotgun` — Birden çok AI tasarım varyantı üretir, karşılaştırma panosu açar, geri bildirimle yineler.
- `design-taste-frontend` — Brief'i okuyup doğru tasarım yönünü çıkaran anti-slop ön yüz skill'i (landing, portföy, redesign).

## Birlikte kullanım
- design-consultation → design-shotgun → design-html → design-review: tasarımdan son HTML'e.
- design-extractor / design-dna + design-system: referanstan token çıkarıp sistemi genişletmek.
- design-persona-walkthrough + design-review: persona bakışı ve görsel QA.

## Tuzaklar
- Çift kopyalar: design-taste-frontend(-v1) taste-skill'de, design-masters/design-movements design-mastery'de de var.
- design-taste-frontend-v1 yalnız eski davranışa bağlı projeler için korunur; yeni işte varsayılan design-taste-frontend.

## Üyeler
- skill (15): design-action-combat, design-auditor, design-consultation, design-dna, design-extractor, design-first-ui-prompting, design-game-encounters, design-html, design-masters, design-movements, design-review, design-shotgun, design-system, design-taste-frontend, design-taste-frontend-v1
- ajan (1): design-persona-walkthrough
