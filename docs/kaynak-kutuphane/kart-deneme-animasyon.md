---
type: kaynak-deneme
status: ogrenildi
tags: [kaynak-kutuphane, animasyon, scroll, webgl]
relatedTo: [kaynak-kutuphane-1]
---
# Deneme: vanta + lenis + gsap/ScrollTrigger + lucide SVG (headless)
Yer: `<lib>/_deneme/animasyon/` (index.html, olc.py, ekran.png). Playwright headless, yerel http sunucu.
**Kanıt:** vanta canvas oluştu; lucide `rocket.svg` fetch→inline SVG yüklendi; ScrollTrigger scrub kutusu wheel(600) sonrası x: 74.7 → 288; sayfa hatası 0.
- Kurulum: CDN `three@r134` → `vanta.waves` (vanta three r134 ister) · `lenis@1.1.18` UMD · `gsap`+`ScrollTrigger`.
- Lenis↔GSAP bağı: `lenis.on('scroll',ScrollTrigger.update)`; `gsap.ticker.add(t=>lenis.raf(t*1000))`; `gsap.ticker.lagSmoothing(0)`.
- En sık 3 özelleştirme: vanta `color/waveHeight/shininess`; lenis `lerp/duration`; ScrollTrigger `start/end/scrub`.
- **Tuzak (kanıtlandı):** global `window.R` tanımlamak Lenis UMD'yi kırdı (`R is not a function`); sayfa genel değişkenlerine kısa/tek harfli ad verme (`KK` ile düzeldi).
- Tuzak: vanta yeni three sürümüyle çalışmaz (r134 sabit); SVG ikon `fetch` için dosya sunucusu şart (file:// değil).
- Performans: vanta her karede WebGL çizer; mobilde `VANTA.current.destroy()` ya da statik görsel; `prefers-reduced-motion` ayrıca ele alınmadı.
- Kime: landing hero arka planı, scroll-bağlı sahneler, ikon seti (lucide ISC / game-icons CC-BY atıf).
