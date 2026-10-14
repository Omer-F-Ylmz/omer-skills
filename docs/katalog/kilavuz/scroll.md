# scroll — 4 benzersiz kayıt

**Amaç:** Scroll'a bağlı anlatım kalıpları: ilerleme zaman çizelgesi, scrub'lı görsel sekans, kelime kelime açılma ve scroll dünyası/fly-through.

**İç yapı:** Tümü [skill], scroll-<kalıp>; her biri kullanım bağlamını (onboarding, hero, manifesto, gezegen) listeler.

## En güçlü parçalar
- `scroll-scrubbed-visual-sequence` — Hero dönüşümü, ürün montajı, nesne dönüşü için scrub'lı sekans.
- `scroll-world-storytelling` — Scroll dünyası, fly-through landing, makaleden siteye dönüşüm.
- `scroll-progress-timeline` — Onboarding, checkout, yol haritası gibi ilerleme anlatıları.

## Birlikte kullanım
- scroll-scrubbed-word-reveal + scroll-scrubbed-visual-sequence.
- omer-kutuphaneler lenis ve gsap-skills ile.

## Tuzaklar
- animation-on-scroll ve yerel-diger'deki cinematic-scroll-storytelling ile çakışır.

## Üyeler
- skill (4): scroll-progress-timeline, scroll-scrubbed-visual-sequence, scroll-scrubbed-word-reveal, scroll-world-storytelling
