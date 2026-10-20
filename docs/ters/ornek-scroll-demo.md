# ornek-scroll-demo — C:/Projeler/scroll-demo/index.html (kendi sayfamız)

**Mekanizma**: saf CSS kaydırma-güdümlü animasyon, JS yok. (1) `.progress` root ScrollTimeline ile scaleX 0→1; (2) `.stage` 300vh + `position: sticky` `.pin` + `view-timeline: --stage`; `.product` bu zaman çizelgesinde rotateY -40°→320°, scale .6→1.1; (3) `.features article` her biri `view()` ile entry 0%→cover 35% arası opacity/translateY reveal; `@supports` ve `prefers-reduced-motion` korumalı.

**Kanıt satırları** (index.html): `l.15 .stage { height: 300vh; view-timeline: --stage block; }` · `l.23 animation-timeline: scroll(root);` · `l.24 animation-timeline: --stage; animation-range: contain 0% contain 100%;` · `l.25 animation-timeline: view(); animation-range: entry 0% cover 35%;`
Çalışma zamanı (probe, headless): `document.getAnimations()` = grow/ScrollTimeline, spin/ViewTimeline, reveal ×3/ViewTimeline; `.product` matrix3d scroll 0'da m31 -0.6428, 100'de -0.6428 (rotateY -40° ve 320° → sin eşit); `.progress` scaleX 0 / 0.25 / 0.5 / 0.75 / 1 = scroll oranı (0.2498 … 1).

**Yeniden kurulum** (`ornek-scroll-demo.yeniden.html`, scroll olayı + JS, CSS timeline yok): piksel farkı (kanal farkı >16/255 olan piksel oranı, 1280x720) scroll 0%: 0.000 · 50%: 0.117 · 100%: 0.007; ortalama 0.041 → yeniden kurulum puanı 0.959. 50% farkı: contain aralığını `(y - stage.top)/stage.height` diye yaklaştırdım, gerçek aralık farklı (kapsayıcı büyükken contain uçları ters). Anlaşılan: mekanizma doğru, aralık matematiği yaklaşık.
Sınır: Lighthouse ölçülmedi. Probe RAM %90.9'da koştu (kural ≥%88 yasak; bilgiyle sonra fark edildi), sonraki adımlar RAM bekledi.
