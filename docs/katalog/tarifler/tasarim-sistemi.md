# Tasarım sistemi — birleşim tarifi
Ne zaman: Token, renk, tipografi ve bileşen kütüphanesi kurmak ya da var olanı denetlemek.

## Fazlar
1. Keşif: `departman-frontend` — hangi tasarım aracı hangi sırayla · birlikte: var olan arayüzden `create-design-md` tasarım dilini ve tokenları çıkarır.
2. Yön: `tasarim-katalog` — kanıtlı, jenerik olmayan referans, font ve kütüphane · birlikte: `gstack-design-consultation` estetik, tipografi, renk, boşluk ve hareketle tam sistem önerir.
3. Token katmanı: `design-systems:design-token` — token katmanını kurar · birlikte: `interfaces:better-colors` palet, semantik token ve kontrast; `ui-design:typography-scale` tipografi ölçeği.
4. Bileşen: `fe-bilesen-kutuphanesi` — API, varyant, erişilebilirlik, doküman · birlikte: `design-systems:component-spec` bileşen tanımı.
5. Uygulama: `frontend-craft:frontend-craft` — tasarım-uygulama disiplini, 3 genişlikte screenshot · birlikte: Tailwind ise `fe-tailwind`.
6. Denetim: `designer-toolkit:design-token-audit` — tokenların atlanıp atlanmadığını bulur · birlikte: `interfaces:interface-review` dal farkında gerilemeleri yakalar.
7. Belge ve yönetişim: `design-systems:documentation-template` · birlikte: birden çok ekip katkı veriyorsa `design-systems:design-system-governance`.

## İnceleme ajanları
- `impeccable`: hiyerarşi, tipografi, renk, erişilebilirlik.
- `gstack-plan-design-review`: her tasarım boyutunu 0–10 puanlar.

## Güvenlik ve kalite kapıları
- Erişilebilirlik: `design-systems:accessibility-audit`; renk kontrastı `interfaces:better-colors`.
- Karanlık mod semantik token ile: `fe-karanlik-mod`.
- Uygulama tasarıma uyuyor: `design-ops:design-qa-checklist`.

## Tartışma konseyi
- Karar: marka yönü ve token adlandırması.
- `ecc:council` — varsayılan Claude personaları: tasarımcı, ön yüz geliştirici, erişilebilirlik uzmanı.

## Jeton bütçesi
- Keşif: orta (~10k, tahmini). Yön: orta (~12k). Token: orta (~10k). Bileşen: büyük (~30k). Uygulama: büyük (~35k). Denetim: orta (~10k). Belge: küçük (~6k). Hepsi tahmini.
- Referans site okuması `okuyucu` alt ajanına.

## Kaçınılacaklar
- Skill çakışmasında sıra: `frontend-craft:frontend-craft` > `impeccable` > diğerleri.
- `gstack-plan-design-review` kapsam kapısı tutmazsa sert durur; kapsamı önce netleştir.
- `example-skills:brand-guidelines` Anthropic markasını uygular; kendi marka için kullanma.

## Aday (kurulu değil)
yok
