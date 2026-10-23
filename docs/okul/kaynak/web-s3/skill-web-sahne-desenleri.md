---
name: web-sahne-desenleri
description: "Premium landing, portfolyo ve 3D hero isinde ac: WebGL imlec reveal, scroll'a bagli 3D urun pozu, helezon galeri, editoryal tipografi ve sahne kalite kapisi. YildizDikme referanslarinin desen dokumu."
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

### 2d. Kapta gerçek zamanlı sıvı (TELVE-R0d dersleri)

1. Yüzey = GPU yükseklik alanı: dairesel 128² (mobil 64²) ızgarada dalga denklemi + sönüm + kısa dalga viskozitesi, CFL < 1/√2, sabit dt alt adımları. Kabın ivmesi kaynak terimi değil **duvar koşulu**: daire dışı hayalet hücre `h = h_merkez − dx·(a·n)/g` → duvar akış geçirmez, eğrilik ve duvarda tepe kendiliğinden çıkar. Dalga hızı ilk çalkalanma kipinden (Neumann j′11 = 1.841) istenen Hz'e ayarlanır.
2. Çizim: sıvı kapalı katı ağ; yüzeyin üstü `discard`, arka yüz = kapak (görüş ışını yükseklik alanıyla 2–3 sabit nokta yinelemesinde kesilir). Kenar: Beer-Lambert, analitik silindir kirişi. Dalga okunurluğu: normal eğimi yalnız gölgelemede ×1.5–2 + yansıyan "pencere" dikdörtgeni (Fresnel'li, ağız gölgesinde kısılır) → hareket eden speküler; pencereyi ışık tarafına koy.
3. Desen (latte art/crema): rengi değil **kaynak-uv** advekte et (kimlikten başlar), deseni her karede kaynak-uv'den yeniden çiz; MacCormack tek geçiş (geri izleme hatasını yarıla, kaynak 4 texele sıkıştır).
4. Örtük şekil (kalp vb.) kenarı `f`'de değil `f/|∇f|`'de eşiklenir + `min(fwidth, tavan)`: sivri uç/girintide ∇f→0, sabit eşik oradan dışarı kama sızdırır, dönüş kayması kamayı ışına çeker.
5. Açıdan desen: `atan` × tam sayı olmayan katsayı ±π'de dikiş çizer → birim çemberde 3B gürültü ya da `sin(k·θ)` (k tam sayı). Kapalı ağın üst diskinde duvar deseni çizilmez (`fwidth(y) > 0` = duvar).
6. Tuzak: meshopt nicemlemesi ham konumu düğüm matrisine taşır → ağdan yarıçap ölçerken konumu `matrix` ile kap uzayına çevir.
7. Döküm akışı: süreklilik `r ∝ √(v0/v)`, `v = √(v0² + 2gd)` (ağızda kalın, aşağıda ~⅓), yatay ilk hızla parabol, zayıf debide alttan damlaya kopma; çarpmada yükseklik alanına Gauss darbe + dişli taç halkası.
8. Doğrulama: başsız Chrome'da sabit adımlı `__T.adim`, 3 Hz kipini sağ/sol vuruşla pompala, halka/kenar ara-ton sayısı ile regresyon; Mantaflow ön-render sızdı ve ağır (80–99 MB/3 sn) → sitede gerçek zamanlı.
9. Taşma (R0f F1): hızlı ardışık vuruşta duvar tepesi ağın üst diskini aşar → disk ön yüzü hacim rengiyle düz kirişte kama çizer. Yüksekliği disk − 4 mm'de yumuşak min (k ≈ .016) ile doyur; görünen her sıvı parçası kapak gibi boyanır. Testte tek vuruş değil 10 toplu vuruş kullan.
10. Kalp SDF (R0d→R0f üç turda bulundu, yeniden türetme): iki daire lob ∪ uçtan loba **teğet** V (65°, hafif dışa bombe). iq kalbi 90° kare uçlu; V'yi `x/(1+k sin)` ile bükmek dalı lobun dışına taşırıp dikey basamak bırakır.
11. Döküm ipi (R0e→R0f): salınım tek düzlemde (sin/cos çifti sarmal = "burgulu ip"); eksenel bant yok, kenar Fresnel parlaması, süt ipi alfa yerine alpha-to-coverage (saydam liste cam iletim geçişinde kaybolur), espresso opak; kalınlık süreklilikle incelir (madde 7).
12. Katman sınırı ve dantel (R0e): sınır gürültüsünün eğimi < 1 tut (fbm 2 oktav, düşük genlik) — aşınca kendi üstüne katlanan "yırtık kâğıt" kenar; lacing yarı saydam ve kapakta yok; crema geniş degrade + benek genliği ≈ .015–.02 (yüksek değer "leopar" okunur).
13. Ölçüm tuzağı: döküm benzetimi sayfalar arasında belirlenimci değil (aynı kod benek 4.46/3.85) → maske farkı ölçümü için sabit tohum + sabit adım sayısı, iki çekimin ortalaması.

## 3. Sahne kalite kapısı
- Anahtar karede metin kontrastı (TELVE-R1): metni gizleyip aynı kareyi yeniden çek, başlık/gövde kutusundaki zeminin metne en yakın %5 lümenine karşı WCAG oranı ölç (medyan yetmez: K3'te medyan 16:1, en kötü %5 4.7:1 → parçacık şeridi metnin altındaydı). Betik: TELVE docs/r1/_ham/r1/kare/cek-r1.mjs.

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

Blender'dan gelen 3D ürün (ayrıntı: blender-uretim `references/web-aktarim.md`):
- Pişir/ortam kuralı: görüşten bağımsız olan (diffuse, AO) UV2 lightMap/aoMap'e pişer; yansıma ve parlaklık PMREM'li HDRI'de kalır. Scroll'da dönen ürün yalnız AO + HDRI (ışık nesneyle döner).
- Lightmap 8 bit PNG'de yoğunluk < 1; lightMapIntensity > 2 ise EXR ya da 16 bit PNG (bantlanma). Dokuda `flipY = false`.
- AgX eşleme: Blender AgX · Look None · Exposure 0 · Gamma 1 → three.js'te postprocessing varsa NoToneMapping + HalfFloat + ToneMappingEffect(AGX) zincir sonunda, yoksa AgXToneMapping → gri kart + krom küreyle toneMappingExposure taraması → eşleşene dek LUT yok.
- Başlangıç sayıları (builder.io): scroll p 0..1 → `rotation.y = π/2·p`, lerp `min(dt·6, 1)`; kamera z 3.2, fov 35; ambient 0.4 + Environment "city".

## 4. Hangi işte hangisi

| iş | sahne | raftan |
|---|---|---|
| Portfolyo / ajans / kişisel marka hero'su | 2a | tempus |
| Tek ürün lansmanı, ürün hikâyesi | 2b | number-flow, @react-three/a11y |
| Galeri, stüdyo, mimari portfolyo, scroll anlatısı (Portale gibi) | 2c | lenis, @14islands/r3f-scroll-rig |
| Hepsi | §1 dil + §3 kapı | size-limit, @capsizecss/core |
| 3D model / doku / HDR gereken sahne | — | blender-uretim `varlik_getir.py ara\|indir` (hazır varlık merdiveni; CC-BY ise kolofonda atıf) |

## 5. CC tarifine yazım

```
Hareket: web-sahne-desenleri 2b (poz tablosu, scrub 1.2); raf: lenis x.y, number-flow x.y — gerekçe: ...
Kabul: web-sahne-desenleri §3 kapısının tamamı; ek: mobil Lighthouse perf ≥ 85
```

## 6. Ödüllü site teknikleri (SİTE-OKULU-1)
10 ödüllü/öne çıkan site ölçüldü (igloo, lusion, activetheory, lando, oryzo, ciao, shopify, bruno, abeto, apple). Tam katalog + lisanslı hazır kaynak: omer-skills `docs/site-okulu/teknikler.md`; eksik matrisi `eksikler.md`.
- En sık ve en ucuz: dither (8/10 site; koyu gradyanda bantlaşmayı kırar) → `dithering:true` + düşük opaklık gren.
- Post tek geçişte: pmndrs `postprocessing` EffectPass (Bloom mipmapBlur + DoF + Noise + Vignette + SMAA); mobilde yalnız Bloom+Vignette.
- Kamera: bölüm başına poz (ciao) ya da sürekli yol (igloo, CatmullRomCurve3 + ScrollTrigger scrub); çok nesne animasyonu → glTF anim + `AnimationMixer.setTime(t)`.
- Tipografi: GSAP SplitText (ücretsiz, GSAP Standard License — MIT değil) maskeli satır stagger.
- Varlık: `@gltf-transform/cli optimize --texture-compress ktx2 --compress meshopt`; görünmezken render durdur (IntersectionObserver).
- Yasak kaynak: Shadertoy kodu (varsayılan CC BY-NC-SA), lygia (ticari Patron), ölçülen sitelerin varlıkları.
- Hazır modüller (SİTE-OKULU-2, K7 `tools/site-kit/sablon/src/sahne/`): kamera-yolu · dongu (talep üzerine render, boşta 0 kare/sn) · post (`'dusuk'` kademe) · gecis (RT kompozit, kenar ışımalı) · metin · yukleyici · parcacik (GPGPU). Notlar + tuzaklar: omer-skills `docs/site-okulu/lab-<teknik>.md`. Tuzak: DoF + kromatik aynı EffectPass'e girmez; RT'de ton eşleme için ToneMappingEffect.
