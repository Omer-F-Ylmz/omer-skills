# plan — 5 benzersiz kayıt

**Amaç:** gstack plan inceleme skill'leri: planı CEO/kurucu, tasarımcı, mühendislik müdürü ve geliştirici deneyimi gözüyle etkileşimli incelemek; soru hassasiyetini ayarlamak.

**İç yapı:** Tümü [skill], gstack etiketli; dört rol incelemesi (ceo, design, eng, devex) + plan-tune.

## En güçlü parçalar
- `plan-eng-review` — Mühendislik müdürü modunda plan incelemesi.
- `plan-ceo-review` — CEO/kurucu modunda plan incelemesi.
- `plan-design-review` — Tasarımcı gözüyle etkileşimli plan incelemesi.
- `plan-devex-review` — Etkileşimli geliştirici deneyimi incelemesi.

## Birlikte kullanım
- yerel-diger'deki autoplan dört incelemeyi sırayla koşar.
- pln ailesinin plan çıktısı bu incelemelere girer.

## Tuzaklar
- plan-tune v1 yalnız gözlemsel.
- gstack kurulumuna bağlı.

## Üyeler
- skill (5): plan-ceo-review, plan-design-review, plan-devex-review, plan-eng-review, plan-tune
