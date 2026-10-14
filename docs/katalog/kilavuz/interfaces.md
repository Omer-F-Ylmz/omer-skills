# interfaces — 15 benzersiz kayıt

**Amaç:** Ürün arayüzü kalitesi için skill'ler: tipografi, renk, düzen, erişilebilirlik, UI cilası ve arayüz metni; ayrıca bileşen stres testi, varyant ve inceleme.

**İç yapı:** interfaces [plugin] + interfaces:<konu> skill'leri; better-* ailesi (accessibility, colors, layout, typography, ui, writing) ve bunları birleştiren better-interface; araçlar (break, build-design, explain-interface, interface-review, state-machine, variant); ayrı interfaces-better-paket.

## En güçlü parçalar
- `interfaces:better-interface` — Tüm better-* skill'lerini erişilebilirlik, düzen, metin, tipografi ve renk üzerinden tek incelemede birleştirir.
- `interfaces:interface-review` — Bir dal, PR ya da commit edilmemiş değişikliğin getirdiği/geri bozduğu arayüz sorunlarını inceler.
- `interfaces:better-accessibility` — Klavye/odak, ARIA, erişilebilir ad, form ve ekran okuyucu duyurularını düzeltir.
- `interfaces:break` — Seçilen bileşeni ulaşılabilir her senaryoda geçici sayfada render edip stres testi yapar.
- `interfaces:build-design` — Figma ya da tasarım görselinden projenin mevcut token ve bileşenleriyle UI kurar.

## Birlikte kullanım
- interfaces:build-design → interfaces:variant → interfaces:interface-review.
- interfaces:state-machine + interfaces:break: çok durumlu bileşeni kapsamlı doğrulamak.
- interfaces:better-colors + interfaces:better-typography + design ailesindeki design-system.

## Tuzaklar
- interfaces-better-paket ile interfaces:better-* skill'leri örtüşür; çift yükleme bağlamı şişirir.
- interfaces:state-machine çok durumlu bileşen içindir; tek etkileşimin hissi için değil.

## Üyeler
- plugin (1): interfaces
- skill (14): interfaces-better-paket, interfaces:better-accessibility, interfaces:better-colors, interfaces:better-interface, interfaces:better-layout, interfaces:better-typography, interfaces:better-ui, interfaces:better-writing, interfaces:break, interfaces:build-design, interfaces:explain-interface, interfaces:interface-review, interfaces:state-machine, interfaces:variant
