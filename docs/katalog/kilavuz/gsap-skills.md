# gsap-skills — 9 benzersiz kayıt

**Amaç:** Resmi GSAP skill'leri: tween, timeline, ScrollTrigger, eklentiler, yardımcılar, React/Vue/Svelte entegrasyonu ve animasyon performansı.

**İç yapı:** gsap-skills [plugin] + gsap-skills:gsap-<konu> skill'leri; çekirdek (core, timeline, utils, plugins), scroll (scrolltrigger), çerçeve (react, frameworks), performans (performance).

## En güçlü parçalar
- `gsap-skills:gsap-core` — JS animasyon kütüphanesi, tween ve easing gibi temel GSAP işleri için giriş.
- `gsap-skills:gsap-scrolltrigger` — Scroll tabanlı animasyon, parallax ve pinlenmiş bölümler.
- `gsap-skills:gsap-timeline` — Animasyonları sıralama ve keyframe koreografisi.
- `gsap-skills:gsap-react` — React/Next.js'te useGSAP ve unmount temizliği.
- `gsap-skills:gsap-performance` — Takılmayı azaltma, FPS ve akıcı 60 fps optimizasyonu.

## Birlikte kullanım
- gsap-skills:gsap-core → gsap-timeline → gsap-scrolltrigger: temel tween'den scroll sahnesine.
- gsap-skills:gsap-react / gsap-frameworks + gsap-performance: çerçeve içinde akıcı animasyon.
- taste-skill:gpt-taste ve build-threejs-scroll-worlds ile hareketli sayfa.

## Tuzaklar
- React için gsap-react, Vue/Nuxt/Svelte için gsap-frameworks ayrı; yanlış çerçeve skill'i temizlik kalıbını kaçırır.
- Eklenti kullanımı (flip, draggable, SVG çizimi) kayıt ister; gsap-plugins kapsamı atlanmamalı.

## Üyeler
- plugin (1): gsap-skills
- skill (8): gsap-skills:gsap-core, gsap-skills:gsap-frameworks, gsap-skills:gsap-performance, gsap-skills:gsap-plugins, gsap-skills:gsap-react, gsap-skills:gsap-scrolltrigger, gsap-skills:gsap-timeline, gsap-skills:gsap-utils
