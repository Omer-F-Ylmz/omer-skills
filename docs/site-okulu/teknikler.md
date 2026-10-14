# Ödüllü site teknikleri kataloğu (SİTE-OKULU-1, 14 Eki)

Kaynak: 10 site × (Playwright 1440+390, 8 kaydırma karesi, ~25 sn kayıt → Gemini 3.5-flash-lite JSON) + JS paket imza/GLSL taraması (`tools/site-okulu/cek.py`, `tara.py`; ham `.kos/site-okulu/<slug>/`, yayınlanmaz). Önceki ölçüm: TELVE `docs/r1/_ham/siteler.md` (ağ baytı bundan; aşağıdaki not).
Kural: teknik çıkarılır, varlık/metin/logo alınmaz (Ömer 29 Eyl). Site kartları: `docs/site-okulu/<slug>.md`.

## Site seçimi
| Site | Neden | Ölçülen öz |
|---|---|---|
| igloo.inc | Awwwards SOTY 2024; scroll kamera yolu + exploded | Svelte+three, pmndrs post, KTX2+draco+meshopt, 236 shader, scroll-datatexture.ktx2, ses |
| lusion.co | stüdyo vitrini; malzeme+akışkan | three r158, 156 shader (kırılma, matcap, bloom), GPGPU; 15 MB |
| activetheory.net | en hafif zengin site (0.95 MB) | Hydra motoru + Theatre.js, 228 shader (noise 100, fresnel 45), basis/KTX2 |
| landonorris.com | ürün-dışı marka hikâyesi, Webflow+3B | three r174 + gsap ST/SplitText + lenis + Rive; HDR çifti; WebGL küçük alanda |
| oryzo.ai | ürün (bardak altlığı) anlatısı | three r178, Gaussian splat (.sog 3 MB), Rive, SplitText; docH 56.7k |
| ciaoenergy.com | içecek — TELVE'ye en yakın | three r161 + gsap 3.15 SplitText/ST + lenis; MeshPhysical sheen/clearcoat; bölüm başına kamera pozu |
| shopify.com/editions | büyük marka, R3F | R3F + lenis + barba, KTX2/meshopt; 3B raf, mobilde kart yığını |
| bruno-simon.com | oyunlaştırılmış portföy | three r183 WebGPU+TSL, Rapier fizik, howler, 7.5 MB |
| messenger.abeto.co | Awwwards öne çıkan; stilize dünya | three r180, pmndrs post, toon/outline, glyph worker, 3B tipografi |
| apple.com/airpods-pro | ürün kaydırma sayfasının çıtası | WebGL kütüphanesi yok; video/kare dizisi scrub + maskeli tipografi; 22.7 MB |
Ödül etiketi yalnız igloo için kesin; diğerleri Awwwards SOTD/öne çıkan düzeyi (tarih doğrulanmadı).

## Teknikler
Her satır: **kim** · nasıl (kanıt) · HAZIR KAYNAK (lisans) · bizde · eksikse.

1. **Sürekli kamera yolu** — igloo, oryzo, otsuka · kamera spline/anahtar dizisi scroll ilerlemesine bağlı; Gemini: "Z ekseninde uçuş, bulutların içinden geçiş" · three `CatmullRomCurve3.getPointAt(t)` + `lookAt` hedef eğrisi (MIT); Theatre.js sequence scrub (core Apache-2.0, studio AGPL → yalnız geliştirmede) · TELVE: yok (yörünge ≤30°, `camera.position` sabit poz) · K7'ye `kamera-yolu.ts` (eğri + GSAP ST scrub, 30 satır).
2. **Scroll→kamera veri dokusu** — igloo (`scroll-datatexture.ktx2` 1.26 MB) · Blender'da animasyonlu kamera kare kare RGBA float dokuya bake, shader/CPU `t` ile örnekler; çok parçalı animasyonu tek dokuda taşır · hazır: Blender → glTF kamera animasyonu + `AnimationMixer.setTime(t)` daha basit eşdeğer (MIT) · yok · önce glTF anim scrub; doku yalnız 100+ nesne animasyonunda.
3. **RT kompozit geçiş** — activetheory, igloo, oryzo · iki sahne ayrı `WebGLRenderTarget`'a, tam ekran quad'da `mix(a,b,mask)` · three `webgl_postprocessing_*`, pmndrs `TextureEffect`; Codrops sahne geçişi demoları (repo başına lisans; çoğu MIT) · TELVE: RT 1 dosyada var (sıvı), sahne geçişi yok · K7 `gecis.ts`: 2 RT + 1 ShaderMaterial.
4. **Noise/maske geçiş** — igloo (gecis/maske 44 shader), activetheory, apple (maskeli metin) · `uProgress` + simplex noise eşiği `smoothstep(p-w,p,n)` · webgl-noise (ashima, MIT); **lygia ticari kullanımda Patron lisansı ister — kullanma**; Shadertoy varsayılan CC BY-NC-SA → kod kopyalanmaz, yalnız fikir · TELVE: shader noise 0 · 3 ile aynı modülde maske fonksiyonu.
5. **Sıvı/akışkan** — lusion (advect/vorticity), igloo (akışkan 25) · ekran uzayı Navier-Stokes ping-pong FBO · Pavel Dobryakov WebGL-Fluid-Simulation (MIT); skill 2a fluid reveal · TELVE: kapta sıvı var (`sivi-glsl.js`, R0d) · ekran akışkanı gerekmez; imleç izi istenirse 2a.
6. **Parçacık GPGPU** — lusion, igloo (gl_PointSize 27), oryzo, santioni (curl) · `GPUComputationRenderer` konum/hız dokuları + curl noise · three `examples/jsm/misc/GPUComputationRenderer` + `webgl_gpgpu_birds` (MIT) · TELVE: gl_PointSize 2 dosyada (basit buhar), GPGPU yok · K7'ye iskelet; TELVE'de telve tozu/buhar için.
7. **Bloom / DoF / gren / kromatik / vinyet** — 10 siteden 8'i; Gemini post listesi igloo+activetheory+oryzo'da beşi birden · pmndrs `postprocessing` tek `EffectPass` içinde Bloom(mipmapBlur)+DepthOfField+Noise+ChromaticAberration+Vignette+SMAA birleşir → three `UnrealBloomPass` zincirinden ucuz (Zlib) · TELVE: EffectComposer 1 dosya (R2'de eklendi), DoF/kromatik yok · K7'ye `post.ts` pmndrs ile; mobilde yalnız Bloom+Vignette.
8. **Dither (bantlaşma önleme)** — 10 sitenin 8'inde en sık GLSL sınıfı (abeto 28, igloo 31, lusion 30) · koyu gradyanda 8-bit bantlaşmayı gürültüyle kırar · three malzeme `dithering: true` + post `NoiseEffect` düşük opaklık (MIT/Zlib) · TELVE: yok, oysa ort. luminans 0.07 (koyu) → **en ucuz kazanç** · tek satır.
9. **SplitText tipografi** — ciao, lando, oryzo, santioni · satır/kelime/harf `SplitText` + `ScrollTrigger` stagger, maskeli satır (`mask: "lines"`) · GSAP SplitText (Webflow sonrası tüm eklentiler ücretsiz, "GSAP Standard License" — MIT değil; Webflow rakibi araçta kullanılamaz) · TELVE: 0 · K7'ye `metin.ts` 15 satır.
10. **Dev tip + 3B katmanı** — abeto (3B blok harf), apple, igloo · DOM başlık `z-index` canvas'ın altında/üstünde; 3B harf: `TextGeometry`/troika-three-text (MIT) veya MSDF · TELVE: 12 px mono ×18 (teşhis #8) · tipografi kararı R3b; teknik: DOM tip + `mix-blend-mode` öncelikli.
11. **Yükleyici % sayacı** — ciao, lusion, activetheory, oryzo, igloo · `THREE.LoadingManager.onProgress` → sayaç, bitince giriş timeline · three (MIT) · TELVE: yükleyici yok (poster var) · K7 `yukleyici.ts`; LCP için poster korunur, sayaç poster üstünde.
12. **Ses tasarımı** — igloo (müzik ogg 2.9 MB, "Sound: Off"), santioni (drone 6.7 MB, tık kapısı), bruno (howler), activetheory · varsayılan kapalı, tık ile `AudioContext.resume`, scroll'a bağlı filtre/ses düzeyi · howler (MIT), Tone (MIT) · TELVE: `ses.ts` var · zayıf: scroll-bağlı katman yok; Freesound CC0 öğeleri.
13. **Talep üzerine render** — lando (WebGL küçük alanda), shopify (R3F) · görünür değilken döngü durur: R3F `frameloop="demand"` + `invalidate()`; vanilla `IntersectionObserver` + `setAnimationLoop(null)` · TELVE: IO 0, invalidate 0 → TBT 2.5 s bulgusunun (R2g) adayı · K7 `dongu.ts` 20 satır.
14. **Tek renderer çok sahne** — shopify, lando (çok küçük canvas alanı) · scissor/viewport ile DOM kutularına çizim · three `webgl_multiple_elements` (MIT), drei `<View>` (MIT) · TELVE: tek sahne · ürün kartları çoğalırsa.
15. **KTX2/meshopt boru hattı** — igloo, ciao, lando, abeto, shopify, activetheory (basis) · `npx @gltf-transform/cli optimize in.glb out.glb --texture-compress ktx2 --compress meshopt` (MIT; KTX-Software Apache-2.0) + `KTX2Loader`/`MeshoptDecoder` · TELVE: meshopt var, KTX2 0, doku haritası 0 (teşhis #3) · K7'ye `varlik:optimize` npm betiği.
16. **Mobil düşüş yolu** — shopify (mobilde kart yığını), lando, apple (DOM ağırlıklı) · GPU kademesi `detect-gpu` (pmndrs, MIT) → DPR ≤1.5, post kapalı, poster/video yedeği; `prefers-reduced-motion` · TELVE: reduced-motion 5 dosya, matchMedia 4 → var; GPU kademesi yok · K7'ye kademe fonksiyonu.
17. **Exploded view (parçalara ayrılma)** — igloo, apple · parça başına yön vektörü × scroll `t` · glTF'de parçalar ayrı node + GSAP · TELVE: 1 parça (teşhis #7) · içerik işi (Blender), kod 10 satır.
18. **Gaussian splat** — oryzo (.sog 3 MB) · gerçek çekim sahne → splat; PlayCanvas SOG / Spark (sparkjs, MIT) three içinde · yok · TELVE için gerekmez (ürün CG).
19. **Stilize/toon + outline** — abeto · `MeshToonMaterial` + pmndrs `OutlineEffect` / ters-normal kabuk · MIT/Zlib · yok · yön seçeneği olarak R3a'ya.
20. **Fizik/oyunlaştırma** — bruno · Rapier wasm (Apache-2.0) 1.7 MB · yok · TELVE kapsamı dışı.
21. **WebGPU + TSL** — bruno (r183), igloo/abeto/lando'da WebGPU yolu hazır · three `WebGPURenderer` + TSL düğüm malzemesi, WebGL2 yedeği otomatik · yok · bekle: WebGL2 hedefi yeterli.
22. **Rive UI animasyonu** — lando, oryzo · `@rive-app/canvas-lite` (MIT) · yok · ikon/mikro-etkileşim için Lottie'den hafif.

## Varlık hazır kaynakları (lisanslı)
Poly Haven HDR/doku/model CC0 (lando `studio_small_08`) · ambientCG CC0 · Sketchfab yalnız CC-BY/CC0 filtreli (atıf zorunlu) · Freesound CC0 · Google Fonts/fontsource OFL. Yasak: Shadertoy kodu (varsayılan NC), lygia (ticari Patron), ölçülen sitelerin varlıkları.

## Ölçüm sınırları
- `performance` transferSize çapraz kökende (TAO yok) 0 → lusion/lando/ciao baytı düşük çıktı; bütçe için TELVE r1 ağ ölçümü (`_ham/siteler.md`) geçerli.
- `image-seq` ve `splat` imza desenleri geniş (her pakette eşleşti); yalnız oryzo .sog ve apple bayt profili kanıt sayılır.
- Gemini yalnız ~25 sn kayıt görür; kamera/geçiş alanlarındaki "tahmin" etiketleri görüntüyle doğrulanmadı; kartlardaki "Kod çapraz" satırı GLSL/imzayla karşılaştırır (apple'ın bloom/DoF/kromatik tahmini kodla desteklenmiyor: 0 shader, image-seq). Başsız swiftshader: FPS yok.
