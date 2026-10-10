# jeskojets.com

- **Ne:** Jesko Jets · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** b-LZ_Y9wor8 · **İncelendi:** 2026-10-10
- **Teknoloji:** Webflow · GSAP 3.13.0 + ScrollTrigger + SplitText · Lenis · Barba.js · Lottie · globe.gl (WebGL küre) · JS 626 KB (13 dosya), görsel 0 KB, video 0 KB
- **Etiketler:** pin-scroll, splittext, sayfa-geçişi, webgl-küre, lenis, gsap

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Ne: özel jet kiralama; Webflow üzerinde GSAP ile zenginleştirilmiş.
- Teknik yığın (ölçülen): gsap 3.13.0, ScrollTrigger, SplitText, Lenis (4 KB), Barba (sayfa geçişi), Lottie 75 KB, globe.gl 493 KB (CDN npm).
- Renk: #312726 sıcak koyu kahve, beyaz, #7a716e; font GT America Extended/Expanded (ticari, alternatif: Archivo Expanded/Space Grotesk).
- Geçişler: `all 0.2s cubic-bezier(0.77,0,0.175,1)` (easeInOutQuart) 31 öğe; `1s cubic-bezier(0.165,0.84,0.44,1)` (easeOutQuart) giriş; 2 fixed + sticky + 6 transform öğesi.
- Kaydırma: bölüm başlıkları ("We are distinction" → "Jesko Jets® is a…") sticky anlatı; 8725px.
- Bizde: Webflow'suz Next/Vite + GSAP + Lenis + SplitText; Barba yerine View Transitions API düşünülebilir.

## Öne çıkan efekt
- GSAP SplitText + ScrollTrigger + Lenis; globe.gl ile etkileşimli dünya

## Bizde kullanım
- Özel jet/lüks landing; sayfa geçişi. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
