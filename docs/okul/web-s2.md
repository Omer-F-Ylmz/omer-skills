# DERS KİTABI, Web S2: Animasyon / Scroll (GSAP, ScrollTrigger, smooth scroll)
Kaynak: docs/okul/kaynak/web-s2/ (resmi-gsap-skill-gsap-core/-scrolltrigger/-performance.md, skill-smooth-scroll.md). Alıntılar `tools/okul/alinti_denetle.py` ile alt dize olarak doğrulanır. Kapsam: kaynaklarda okunan kurallar; okunmayan kısımlar "KAYNAK EKSİK".

## A. En iyi yöntemler + tarif kartları

**Kart A1, Hareket yalnız transform/opacity**
> "Prefer: **x**, **y**, **scale**, **rotation**, **opacity**." (resmi-gsap-skill-gsap-performance.md)
> "Animate **transform** and **opacity**; use **will-change** in CSS only on elements that animate." (resmi-gsap-skill-gsap-performance.md)
> "Prefer **transform aliases** (`x`, `y`, `scale`, `rotation`, `xPercent`, `yPercent`, etc.) over animating the raw `transform` string" (resmi-gsap-skill-gsap-core.md)

**Kart A2, Fade: autoAlpha**
> "Prefer over `opacity` for fade in/out." (resmi-gsap-skill-gsap-core.md)
0'da `visibility: hidden` da set edilir; görünmez eleman tıklamayı engellemez.

**Kart A3, Zaman çizelgesi, delay zinciri değil**
> "Prefer timelines instead of chaining animations using `delay`." (resmi-gsap-skill-gsap-core.md)

**Kart A4, ScrollTrigger doğru yerde**
> "Correct: `gsap.timeline({ scrollTrigger: {...} }).to(".a", { x: 100 })`." (resmi-gsap-skill-gsap-scrolltrigger.md)
> "ScrollTriggers should only exist on top-level animations." (resmi-gsap-skill-gsap-scrolltrigger.md)

**Kart A5, scrub ya da toggleActions**
> "Use **scrub** for scroll-linked progress or **toggleActions** for discrete play/reverse; do not use both on the same trigger." (resmi-gsap-skill-gsap-scrolltrigger.md)

**Kart A6, Smooth scroll seçimi**
> "Still unsure, or the user just says "make it smooth"? Default to **Lenis**." (skill-smooth-scroll.md)
> "Running Lenis and ScrollSmoother together fights over the same scroll position and produces jitter." (skill-smooth-scroll.md)
GSAP ScrollTrigger ile birlikte: Lenis + ScrollTrigger eşleme tarifi (`references/lenis.md`) ya da yalnız ScrollSmoother.

## B. Hata kataloğu

| Hata | Nereden çıkar | Teşhis | Düzeltme |
|---|---|---|---|
| Pin boşluğu/sıçrama | Tetikleyiciler sırasız yaratıldı | dinamik/async oluşturma | > "Create ScrollTriggers in the order they appear on the page (top to bottom, scroll 0 → max)." (resmi-gsap-skill-gsap-scrolltrigger.md); sırasızsa `refreshPriority` |
| Dinamik içerikten sonra kayık başlangıç | Görsel/font yüklendi, yenilenmedi | trigger konumları | > "Call **ScrollTrigger.refresh()** after DOM/layout changes" (resmi-gsap-skill-gsap-scrolltrigger.md) |
| Çalışmayan ScrollTrigger | Eklenti kayıtsız | konsol | > "Forget to **gsap.registerPlugin(ScrollTrigger)** before using ScrollTrigger." (resmi-gsap-skill-gsap-scrolltrigger.md) (kaçın listesinde) |
| scrub + toggleActions birlikte | İki davranış istendi | trigger konfigürasyonu | > "If both exist, **scrub** wins." (resmi-gsap-skill-gsap-scrolltrigger.md) |
| Üretimde marker | Debug unutuldu | `markers: true` ara | > "Leave **markers: true** in production." (resmi-gsap-skill-gsap-scrolltrigger.md) (kaçın listesinde) |
| Sahte yatay scrollda kayma | containerAnimation'da ease | ease değeri | > "Use an ease other than **"none"** on the horizontal animation when using **containerAnimation**" (resmi-gsap-skill-gsap-scrolltrigger.md) (kaçın listesinde) |
| Layout'u animasyonla zorlama | width/top/left animasyonu | performans izi | > "Animate layout-heavy properties (e.g. `width`, `height`, `top`, `left`) when transform aliases" (resmi-gsap-skill-gsap-core.md) (kaçın listesinde) |
| Pin titremesi / yapışmama | ana scroll başka iş parçacığında | pin davranışı | > "Use `"fixed"` if pins jitter" (resmi-gsap-skill-gsap-scrolltrigger.md); yapışmıyorsa `"transform"` |
| React'te sızan tetikleyici | cleanup yok | unmount sonrası trigger | > "use the `useGSAP()` hook to ensure that all ScrollTriggers and GSAP animations are reverted and cleaned up" (resmi-gsap-skill-gsap-scrolltrigger.md) |

## C. Kalite kapısı kontrol listesi
- [ ] Yalnız transform/opacity animasyonu (A1); layout özelliği animasyonu yok.
- [ ] > "Use **gsap.matchMedia()** for responsive breakpoints and **prefers-reduced-motion** so animations can be reduced or disabled for accessibility." (resmi-gsap-skill-gsap-core.md)
- [ ] ScrollTrigger'lar sayfa sırasıyla, kayıtlı eklenti, `markers` kapalı, dinamik içerikten sonra `refresh()`.
- [ ] Tek smooth-scroll çözümü (Lenis ya da ScrollSmoother, ikisi değil).
- [ ] Hareket kalitesi ölçümü (fps/Long task): KAYNAK EKSİK: `fixing-motion-performance` sayısal eşik; S4 performans bölümünde ele alınır.

## D. Ucuz yol
- Hazır animasyon önce, `animasyon-atolyesi` tarifleri:
  > "Hero kademeli giriş, scroll'la belirme, ilerleme çubuğu" (skill-animasyon-atolyesi.md)
  > "Liste ↔ detay, paylaşılan öğe morfu, sayfa geçişi" (skill-animasyon-atolyesi.md)
  > "WebGL hero arka planı, parçacık/buhar/toz, fare etkileşimi" (skill-animasyon-atolyesi.md)
- Smooth scroll karar ağacı betiksiz, modelsiz: yukarıdaki A6 sırası; Lenis varsayılan (few KB, GSAP gerektirmez).

## E. Proje bağlantısı: freelance sitesi, TELVE
- Landing scroll anlatısı: ScrollTrigger + (Lenis eşleme). 3D sahneye bağlanan scroll → S3 (taslak).
- Çakışma kuralı Ömer'in dalında: smooth scroll tek yerde kurulur; TELVE'de iki sistem aynı anda açılmaz (A6 alıntısı).
- Lenis + ScrollTrigger eşlemesi (Lenis README):
  > "lenis.on('scroll', ScrollTrigger.update);" (resmi-lenis-readme.md)
