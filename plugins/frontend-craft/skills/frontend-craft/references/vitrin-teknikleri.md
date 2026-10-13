# Vitrin teknikleri — öne çıkan sitelerin mekanizma kataloğu

Kaynak: TASARIM-3 (13 Eki 2026) headless ölçüm, 64 site (d2: + IG-41 listesinden 18 site — cash.app, igloo.inc, unicorn.studio, spline, skiper-ui, originkit…): awwwards SOTD, siteinspire, land-book, lapa.ninja, onepagelove, godly seçkisi, vitrinlerin kendisi (21st.dev, recent.design, designprompts.dev, mobbin, refero, godly) + tasarim-katalog'un 20 sitesi. Yalnız **mekanizma** (yığın, ölçü, zamanlama); kod, varlık, birebir düzen kopyalanmaz. Dribbble/mobbin/refero canlı site değil ekran galerisi: yalnız referans görsel kaynağı.

**Okuma kuralı (jeton):** bu dosyanın tamamını okuma. DESIGN.md'de seçilen yönün başlığını `grep -n "^## "` ile bul, yalnız o bölümü oku. Editoryal dil (kıl çizgi, gren, `difference` nav, sticky hero, fluid reveal, scrub poz, helezon galeri) ve sahne kalite kapısı `web-sahne-desenleri`'nde — burada tekrarlanmaz; iki kaynak çakışırsa o skill geçerli.

## Ölçülen gerçekler (karar verirken dayanak)
- Yığın sıklığı (64 site, IG-41 vitrin listesi dahil): React 33 · GSAP 26 · Next 24 · Motion 22 · WebGL 21 · ScrollTrigger 21 · Lenis 18 · Three 13 · R3F/Astro/Nuxt 3'er · Barba 2. UI süreleri 0.15–0.3s baskın. Kalıp: **Lenis + GSAP/ScrollTrigger** (editoryal/ajans) ya da **Next + Motion (+R3F)** (ürün/stüdyo).
- Easing: en sık `cubic-bezier(.19,1,.22,1)` (expo-out), `cubic-bezier(.175,.885,.32,1.275)` (back-out, yalnız küçük öğe), `cubic-bezier(.4,0,.2,1)`. Süre basamakları 0.15 / 0.2–0.3 / 0.45 / 0.6 s; giriş animasyonu 0.8–1.2 s.
- Display tipi: ajans hero'larında h1 100–250 px (gövdenin 6–18 katı), satır yüksekliği 0.8–1.0, harf aralığı −0.01…−0.05em. Ürün sitelerinde h1 36–64 px, oran 2.5–4.
- Performans: ağır WebGL'li sitelerde masaüstü LCP 8–11 s (resn, nickho, maxima); yalın sitelerde 0.3–1 s (cuberto 0.46 s, basement 2.6 MB JS'e rağmen 0.6 s — hero DOM metni, WebGL sonradan). CLS bozulması preloader + font değişimi + geç yüklenen görsel: 0.24–0.73 (oathbiome, okaydev mobil, heronai). Ders: **LCP öğesi DOM metni/görseli olsun, canvas değil; preloader içeriği itmesin.**
- Erişilebilirlik: çoğu `prefers-reduced-motion` destekli; desteklemeyenler (activetheory, obys, resn) WebGL ağırlıklı. `:focus-visible` çoğunda yok — bizde zorunlu kalır.

## 1. Pürüzsüz kaydırma + scroll sahnesi (Lenis + GSAP ScrollTrigger)
- Ne zaman: editoryal/ajans/ürün hikâyesi, 4+ bölüm, pinlenmiş sahne. Dashboard, form, belge sitesinde **kullanma**.
- Tarif: `lenis` 1.3.x (`new Lenis({ lerp: .1 })`), `lenis.on('scroll', ScrollTrigger.update)`, `gsap.ticker.add(t => lenis.raf(t*1000))`, `gsap.ticker.lagSmoothing(0)`. Pin: `ScrollTrigger.create({ trigger, pin: true, scrub: 1, end: '+=150%' })`. Bölüm başına tek timeline.
- Sürüm: `gsap` 3.13+ (SplitText dahil tüm eklentiler ücretsiz), `lenis` 1.3.
- Performans: yalnız `transform`/`opacity` scrub; `will-change` yalnız pin süresince. Reduced-motion'da Lenis başlatılmaz, `scrub` yerine anlık durum.

## 2. Satır/karakter maskeli başlık girişi
- Ne zaman: display başlıklı hero ve bölüm başlıkları (her yönde kullanılabilir, en sık desen).
- Tarif: başlığı satırlara böl (`SplitText` `type:'lines', mask:'lines'` ya da elle `<span class=line><span>`), iç span `yPercent:110 → 0`, `stagger:.08`, `duration:1`, expo-out. Kaydırmayla gelenler `ScrollTrigger start:'top 85%'`, `once:true`.
- Performans: bölme font yüklendikten sonra (`document.fonts.ready`), yoksa satır kırılımı kayar (CLS). Metin DOM'da kalır → LCP/erişilebilirlik bozulmaz; `aria-label` gerekmez, span'lar `aria-hidden` değil.

## 3. Dev display tipi + kırpılmış wordmark
- Ne zaman: ajans/portfolyo/etkinlik; marka adı kısa (≤10 harf).
- Tarif: `font-size: clamp(4rem, 15vw, 16rem)`, `line-height:.85`, `letter-spacing:-.04em`, değişken font ağırlık ekseni (`font-variation-settings`) hover/scroll ile 100→800. Footer wordmark 18–22vw, `overflow:hidden` alt kenardan kırpık.
- Performans: tek değişken font dosyası (woff2, alt küme, `font-display:swap` + `size-adjust`'lı yedek) → CLS 0.
- Sınır (TASARIM-3 kör yargı: dev ölçeğin her yere yayılması puanı düşürdü): sayfada tek dev öğe (hero h1 ya da footer wordmark); bölüm başlıkları ve liste öğeleri ≤ `clamp(2rem, 5vw, 4.5rem)`; 1440×900 ilk ekranda h1 + değer cümlesi + CTA birlikte görünür, boş hero bandı yok.

## 4. Klip-yol / maske görsel açılışı
- Ne zaman: görsel ağırlıklı portfolyo, ürün, galeri.
- Tarif: `clip-path: inset(100% 0 0 0) → inset(0)` 1–1.2 s expo-out + içteki görsel `scale 1.2 → 1`. Hover'da `inset(4%)`. CSS-only sürüm: `animation-timeline: view(); animation-range: entry 0% cover 40%` (Chrome/Edge/Safari 26; desteklemeyende `@supports` ile statik).
- Performans: `clip-path` kompozitörde; görselde `width/height` öznitelikleri (CLS 0), ilk görsel `fetchpriority=high`, diğerleri `loading=lazy`.

## 5. Yatay kaydırma bölümü (pin + x)
- Ne zaman: süreç adımları, proje şeridi, zaman çizelgesi (etkinlik programı). Mobilde dikey yığına döner.
- Tarif: kapsayıcı pin, iç şerit `x: -(scrollWidth - innerWidth)`, `scrub:1`, `invalidateOnRefresh:true`; kartlar `containerAnimation` ile kendi girişini alır.
- Performans: şerit ≤ 8 kart; görseller lazy; `matchMedia('(min-width: 900px)')` dışında kurulmaz.

## 6. Sayfa geçişi (View Transitions / Barba)
- Ne zaman: çok sayfalı portfolyo/vaka sayfaları. Tek sayfalık landing'de gereksiz.
- Tarif: önce yerel — `@view-transition { navigation: auto; }` + ortak öğede `view-transition-name` (kart görseli → vaka hero'su). SPA'da `document.startViewTransition`. Barba 2.x yalnız eski tarayıcı desteği şartsa.
- Performans: sıfır JS kütüphanesi; reduced-motion'da `::view-transition-group(*) { animation: none }`.

## 7. Akıcı imleç + manyetik öğe
- Ne zaman: ajans/portfolyo masaüstü; ürün/SaaS'ta yalnız CTA'da manyetik.
- Tarif: `gsap.quickTo(el,'x',{duration:.5, ease:'power3'})` ile takipçi; manyetik buton: pointermove'da merkeze uzaklığın %25–35'i kadar `x/y`, ayrılınca `elastic.out(1,.4)` ile sıfır. `(pointer: fine)` dışında kurulmaz; gerçek imleç gizlenmez.
- Performans: tek rAF/quickTo; DOM ölçümü pointerenter'da bir kez.

## 8. Kayan şerit (marquee) + hıza tepki
- Ne zaman: müşteri logoları, sanatçı kadrosu, etkinlik duyurusu.
- Tarif: içerik iki kez, CSS `@keyframes translateX(-50%)` sonsuz; kaydırma hızına göre `timeScale` (ScrollTrigger `onUpdate: self.getVelocity()`), yön tersine döner. Hover'da `animation-play-state: paused`.
- Performans: yalnız transform; ekran dışında `IntersectionObserver` ile durdur; reduced-motion'da statik satır.

## 9. WebGL hero (Three/R3F/OGL) — DOM'a bağlı düzlem
- Ne zaman: marka hikâyesi 3D/doku istiyorsa (ürün, müzik, teknoloji). Bilgi sitesinde değil.
- Tarif: hafif seçenek OGL (~30 KB) ya da Three r17x; görsel düzlemleri DOM `<img>` kutusuna (`getBoundingClientRect`) eşlenir, shader'da kaydırma hızıyla bükülme/RGB kayması/gürültü geçişi. React'ta R3F + drei `<View>`. Ayrıntılı kurulum ve zayıf cihaz yedeği: `threejs-3d-paket`, `fe-webgl-3d-hero`.
- Performans: canvas **LCP öğesi olmamalı** — hero metni DOM'da, canvas `requestIdleCallback`/ilk etkileşim sonrası; `dpr` en çok 2, ekran dışında render durur; WebGL yoksa statik poster.

## 10. Etkileşimli vektör animasyonu (Rive / Lottie / Spline)
- Ne zaman: ikon/illüstrasyon durum makinesi (Rive), ürün 3D vitrini editörde hazırsa (Spline). Tek dekoratif döngü için CSS yeter.
- Tarif: `@rive-app/canvas` 2.x, durum makinesi girdisi hover/scroll'a bağlı; Spline `@splinetool/runtime` sahnesi tembel yüklenir.
- Performans: Spline sahnesi 1–5 MB → hero'da değil, bölüm görünür olunca; Rive dosyası < 100 KB hedef.

## 11. Preloader / sayaç
- Ne zaman: yalnız WebGL varlıkları gerçekten yükleniyorsa. İçerik sitesi için kullanma.
- Tarif: 0→100 sayaç gerçek yükleme olayına bağlı (`THREE.LoadingManager`/`Promise.all`), en çok 1.2 s; içerik arkada render edilmiş ve kaydırma kilitli değil.
- Performans: ölçülen CLS bozulmasının ana kaynağı — preloader `position:fixed` katman olur, içeriği itmez.

## Seçim tablosu (yön → desen)
| Yön | Desenler | Kütüphane |
|---|---|---|
| Editoryal / ajans | 1 · 2 · 3 · 4 · 7 · (web-sahne §1–2) | gsap + lenis |
| Ürün / SaaS | 2 (yalnız hero) · 4 · 8 (logo) · 6 | motion ya da yalnız CSS |
| Portfolyo | 3 · 4 · 6 · 7 | CSS + gsap ya da yalnız CSS |
| Etkinlik / müzik | 2 · 3 · 5 · 8 · 9 | gsap + lenis (+ ogl) |
| 3D ürün | 9 · 1 · (web-sahne §2b) | three/r3f + gsap |

Kural: bir sayfada en çok 3 desen + 1 kütüphane ailesi; her desen DESIGN.md → Hareket'e `desen ← gerekçe` satırıyla yazılır. CDN'den sürüm sabitli (`gsap@3.13`, `lenis@1.3`), satır içi tek dosya teslimlerinde yalnız CSS sürümleri (4, 6, 8) tercih edilir.
