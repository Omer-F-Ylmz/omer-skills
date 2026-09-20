---
name: web-sahne-desenleri
description: "Awwwards seviyesi site desenleri: WebGL reveal, scroll'a bağlı 3D ürün pozu, helezon galeri, editoryal tipografi ve sahne kalite kapısı. Premium landing, portfolyo ya da 3D hero işinde aç."
---

# Web sahne desenleri

Kaynak: YildizDikme'nin üç reposu (fluid reveal portfolyo, 3D kamera landing, helezon galeri) 20 Eyl 2026'da kod düzeyinde incelendi. Repoların lisansı yok: **kod kopyalanmaz, birebir aynısı yapılmaz.** Burada yalnız desenler kendi sözlerimizle ve bizim iyileştirmelerimizle duruyor. Markalı varlık (ör. üretici logolu 3D model) hiçbir işte kullanılmaz.

Kullanım sırası: DESIGN.md yazılırken §1'den dil seçilir → sahne §2'den seçilir → §3 kalite kapısı CC tarifinin kabul kriterine olduğu gibi girer. Kütüphaneler omer-kutuphaneler rafından, DESIGN.md → Hareket'e ad + sürüm + gerekçe ile yazılır.

## 1. Editoryal dil

İki referans sitenin ortak iskeleti. Tek tek değil, sistem olarak uygulanır.

- **Palet:** 1 zemin + 1 mürekkep + 2 ara ton + en fazla 1 aksan. Açık sitede sıcak kırık beyaz zemin, neredeyse siyah mürekkep; ritim için bazı bölümler koyu ters çevrimle kesilir. Koyu sitede sıcak siyah zemin, krem metin, tek sıcak aksan (amber/bakır).
- **Üç ses:** display (karakterli serif ya da display) + gövde + mono etiket. Etiket sesi her yerde aynı: mono, BÜYÜK HARF, 10.5–12 px, harf aralığı 0.16–0.34em. Bölüm numarası, meta, durum, görsel altı hep bu sesle. Yasak font listesi (DESIGN.md) geçerli.
- **Başlık ritmi:** büyük display satırı + altında farklı aileden italik satır (0.5–0.7em). Dev başlıklarda satır yüksekliği 0.95–1.05, harf aralığı −0.01 ile −0.02em.
- **Yapı çizgiyle kurulur:** 1 px kıl çizgi (mürekkebin %10–14 alfası). Hücreli ızgara için kapsayıcıya çizgi rengini arka plan verip `gap: 1px` kullan: kenarlık hesabı olmadan kusursuz iç çizgiler.
- **Akışkan boşluk:** yatay kenar `clamp(1.25rem, 4vw, 4rem)`, bölüm dikeyi `clamp(5rem, 10vw, 9rem)`. Metin sütunu 38–60ch.
- **Tek hareket eğrisi:** bütün geçişlerde aynı easing (ör. `cubic-bezier(.2,.8,.2,1)`), süreler basamaklı: 0.3 / 0.4 / 0.6 / 1.0 s. İki farklı eğri karışmaz.
- **Nav:** `mix-blend-mode: difference` ile her zeminde okunur; menü açılışı satır satır 50 ms gecikmeli.
- **Doku:** sabit konumlu, %6–8 opak SVG gren ya da kontur çizgisi katmanı (`pointer-events: none`). Görseli değil yüzeyi zenginleştirir.
- **Hero:** `100svh`/`100dvh` + `isolation: isolate`. Güçlü kalıp: sticky hero + üstüne kayan içerik katmanı (içerik hero'yu örterek gelir).
- **Galeri:** 12 kolon bento (7/5 ve 8/4 span), 4:5 ve 16:10 oranlar. Hover: görsel 1.04 → 1 ölçek + parlaklık 0.78 → 1, 1.2 s.
- **Mikro etkileşim:** alt çizgi `scaleX(.35) → 1`, ok 3–4 px kayma, adım kartında üst çizginin genişlemesi. Hepsi aynı eğriyle.
- **Kapanış:** koyu CTA bölümü, 8–10vw başlık; footer'da 18–22vw dev wordmark.
- **Loader:** editoryal kapak (üst/alt meta satırı + SVG çizgi çizimi). Kaydırmayı kilitlemez; 1.2 s'yi aşarsa içerik arkada hazır olur.

## 2. Sahne desenleri

### 2a. Fluid reveal — imlecin izinde ikinci görsel açılır

Kurulum:
1. İki ping-pong render target (kare, ~512) iz maskesini tutar (R kanalı).
2. Simülasyon geçişi: önceki maske × sönüm (0.96–0.98) + önceki→şimdiki fare segmentine uzaklıkla yumuşak çizgi.
3. Gösterim geçişi: iki doku cover-UV ile örneklenir; maske eşiği (~0.02) ve DPR'a bölünmüş çok ince kenarla karışır. Eşiğin hemen altında hafif gölge hale: açık zeminde hareket okunur.
4. Boşta kalınca: iki farklı frekanslı sinüs toplamıyla sentetik imleç, lerp ile yumuşak devralma. Gerçek fare her zaman kazanır.

Segment uzaklığı (en-boy düzeltmeli):

```glsl
float segDist(vec2 p, vec2 a, vec2 b) {
  vec2 ab = b - a;
  float h = clamp(dot(p - a, ab) / max(dot(ab, ab), 1e-6), 0.0, 1.0);
  return length(p - a - ab * h);
}
// kullanmadan önce p.x, a.x, b.x değerlerini uAspect ile çarp
```

Bizim farkımız: en-boy düzeltmesi (kare simde iz yassılaşmaz) · `HalfFloatType`, desteklenmezse 8 bit + yüksek yoğunluk · bütün sabitler uniform (JS ayarı ile shader literal'i ayrışmaz) · reduced-motion'da sentetik imleç kapalı · görünmezken döngü durur · dokunmatikte kaydırma engellenmez · sentetik imleç 5 s sonra söner ya da duraklat düğmesi vardır.

### 2b. Poz tablosu + tek scrub timeline — ürün hero'su

1. Model yüklenince merkeze alınır, en büyük boyutu 1'e normalize edilir: pozlar modelden bağımsız olur.
2. Her bölüm için bir poz: `{ id, position, rotation, scale }`. Bölümün `data-section` değeri poz `id`si ile aynıdır.
3. Tek GSAP timeline, `scrollTrigger: { trigger: 'main', start: 'top top', end: 'bottom bottom', scrub: 1–1.5 }`. Her segment `ease: 'none'` ve `i - 1` anında başlar; sinematik yumuşatmayı scrub yapar, eğri üst üste bindirilmez.
4. Kompozisyon: model hangi taraftaysa metin karşı tarafta.
5. Giriş: model yerinde, yalnız Y ekseninde ~140° turntable (`sine.inOut`, ~3.5 s); hero metni ortasında stagger ile gelir.
6. Mobil (<1024 px): konum çarpanı ~0.1 (merkeze yakın), ölçek ×1.1, küçük dikey ofset.
7. GPU kademesi, mobil: DPR `[0.85, 1.1]`, antialias kapalı, `powerPreference: 'low-power'`, üçüncü ışık yok, HDR yerine RoomEnvironment + PMREM. Masaüstü: DPR `[1, 2]`, stüdyo HDR.
8. Işık: key (sol-üst, güçlü) + fill (sağ-ön, yumuşak) + rim (arka, yalnız masaüstü). ACES tone mapping, exposure 1.2–1.3.

Bizim farkımız: kaydırma hiç kilitlenmez; giriş sürerken kullanıcı kaydırırsa giriş anında biter ve scrub devralır · reduced-motion'da giriş yok, bölüm başına anlık poz · model lisanslı ve markasız · GLB derleme öncesi düzeltilir (gltf-transform: spec-gloss → metal-rough, meshopt/Draco), çalışma zamanında doku kurtarma hilesi gerekmez · konsol logu yok · güncel sürümler (Next 16, React 19, R3F 9, drei 10) · CTA gerçek hedefe gider · istatistikler `tabular-nums` + number-flow.

### 2c. Helezon galeri + kaydırma hızı itkisi

1. Kavisli karo: silindir şeridi (~24 segment). Tur başına N karo, yarıçap aşağı doğru daralır, dikey aralık sabit.
2. Dönüş: sabit taban hız + Lenis `velocity` × katsayı itkisi, her karede ×0.9 sönüm.
3. Kamera Y'si kaydırma ilerlemesine lerp ile bağlı; masaüstünde fareyle ±0.1 rad paralaks eğimi.
4. Shader: karo kenarında vinyet + kameraya uzaklıkla koyulaşma ve hafif desatürasyon (derinlik).
5. Lenis → `ScrollTrigger.update` senkronu; WebGL `requestIdleCallback` ile LCP'den sonra başlar, canvas hazır olunca opaklık geçişiyle görünür.
6. Sahne: sticky hero + üstüne kayan içerik; hero'ya radyal vinyet ve alta zemin rengine gradient.

Bizim farkımız: tek paylaşılan materyal + doku atlası ya da InstancedMesh (karo başına materyal yok) · karo en-boy oranına göre cover-UV, fotoğraf esnemez · arka yüz `gl_FrontFacing` ile koyulaşır · reduced-motion'da taban dönüş ve itki 0 · sürekli dönüş için duraklat düğmesi · hero içerik altında kalınca render durur · Lenis 1.x'te `syncTouch` (eski `smoothTouch` yok), tek rAF (Lenis `autoRaf` ya da tempus).

## 3. Sahne kalite kapısı

Her WebGL/scroll sahnesinin CC tarifine kabul kriteri olarak girer:

- [ ] `prefers-reduced-motion` hem CSS'te hem JS/WebGL döngüsünde uygulanıyor
- [ ] Sahne görünmezken (IntersectionObserver + `visibilitychange`) render duruyor
- [ ] 5 s'den uzun otomatik hareketin durdurma kontrolü var
- [ ] Kaydırma hiçbir aşamada kilitlenmiyor; loader kaydırmayı engellemiyor
- [ ] Mobil GPU kademesi uygulanmış; mobil Lighthouse performans ≥ 85, LCP < 2.5 s
- [ ] LCP öğesi metin ya da poster görsel; WebGL LCP'den sonra başlıyor
- [ ] Çizim çağrısı ≤ 50, mobilde doku ≤ 2048 px
- [ ] size-limit ile JS bütçesi tanımlı ve CI'da koşuyor
- [ ] WebGL yoksa ya da context kaybolursa statik poster görünüyor
- [ ] Canvas dekoratifse `aria-hidden`; etkileşimliyse @react-three/a11y ile odak ve klavye
- [ ] Konsol logu, markalı ya da lisanssız varlık yok
- [ ] web-design-guidelines ve frontend-craft kabul kriterleri geçiyor

Görünürlük + reduced-motion iskeleti:

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
let onScreen = true;
new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; }).observe(canvas);
function frame(t) {
  if (onScreen && !document.hidden) render(t, { animate: !reduce.matches });
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

## 4. Hangi işte hangisi

| iş | sahne | raftan |
|---|---|---|
| Portfolyo / ajans / kişisel marka hero'su | 2a | tempus |
| Tek ürün lansmanı, ürün hikâyesi | 2b | number-flow, @react-three/a11y |
| Galeri, stüdyo, mimari portfolyo, scroll anlatısı (Portale gibi) | 2c | lenis, @14islands/r3f-scroll-rig |
| Hepsi | §1 dil + §3 kapı | size-limit, @capsizecss/core |

## 5. CC tarifine yazım

```
Hareket: web-sahne-desenleri 2b (poz tablosu, scrub 1.2); raf: lenis x.y, number-flow x.y — gerekçe: ...
Kabul: web-sahne-desenleri §3 kapısının tamamı; ek: mobil Lighthouse perf ≥ 85
```
