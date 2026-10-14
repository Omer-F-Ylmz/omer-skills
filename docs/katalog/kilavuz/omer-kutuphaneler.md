# omer-kutuphaneler — 9 benzersiz kayıt

**Amaç:** Ömer'in onayladığı frontend kütüphaneleri: smooth scroll, rAF döngüsü, sayfa geçişi, R3F scroll/erişilebilirlik, bundle bütçesi, tipografi metrikleri, 3. parti script yükü, animasyonlu sayaç.

**İç yapı:** Tümü [kutuphane]; her girdi tek kütüphane ve 'X için' kullanım bağlamı; gruplar: scroll/animasyon (lenis, tempus, swup, r3f-scroll-rig), 3B (@react-three/a11y), performans (size-limit, partytown), UI (capsize, number-flow).

## En güçlü parçalar
- `lenis` — WebGL ile senkron smooth-scroll; scroll ağırlıklı landing/portfolyo.
- `@14islands/r3f-scroll-rig` — R3F WebGL'i smooth scroll'a ve DOM öğelerine bağlar.
- `size-limit` — CI'da aşımda hata veren JS bundle boyut bütçesi.
- `@builder.io/partytown` — Analytics/reklam scriptlerini web worker'a taşır.
- `@capsizecss/core` — Font metriğiyle öngörülebilir satır yüksekliği/boşluk.
- `swup` — Klasik MPA vitrin sitelerinde AJAX sayfa geçişi.

## Birlikte kullanım
- lenis + tempus + @14islands/r3f-scroll-rig: scroll ağırlıklı Three.js landing.
- size-limit + @builder.io/partytown: performans bütçesi.
- omer-skills omer-kutuphaneler skill'i pinli kurulum satırlarını verir.

## Tuzaklar
- swup çok sayfalı (MPA) siteler içindir; SPA'da uygun değil.
- Sürüm/pin bilgisi bu kayıtlarda yok; omer-kutuphaneler skill'inde.

## Üyeler
- kutuphane (9): @14islands/r3f-scroll-rig, @builder.io/partytown, @capsizecss/core, @number-flow/react, @react-three/a11y, lenis, size-limit, swup, tempus
