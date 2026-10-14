# TELVE + K7 site kiti eksik matrisi (SİTE-OKULU-1)

Durum kanıtı: TELVE `src/` imza sayımı (14 Eki, @426b5d5) + `docs/r1/teshis.md` + R2g; K7 = `tools/site-kit/sablon` (astro, gsap 3.15, lenis, three 0.186; sahne/sayfa.ts, sivi-glsl.js).
Teknik no'ları `teknikler.md` ile aynı. Öncelik: P0 = R3b'de ilk dalga (ucuz + teşhis bulgusunu kapatır), P1 = yön seçimine göre, P2 = kapsam dışı/bekle.

| # | Teknik | TELVE | K7 | Kapatma yolu | Öncelik |
|---|---|---|---|---|---|
| 8 | Dither | yok | yok | malzemelere `dithering:true` + post Noise 0.03 | P0 |
| 7 | Post (bloom/DoF/gren/kromatik/vinyet) | zayıf (composer var, DoF/kromatik yok) | yok | pmndrs `postprocessing` tek EffectPass; mobil kademede kısıtlı | P0 |
| 15 | KTX2 doku + meshopt | zayıf (meshopt var, doku 0) | yok | `@gltf-transform/cli optimize` betiği + KTX2Loader | P0 |
| 9 | SplitText tipografi | yok | yok | GSAP SplitText + ST stagger, maskeli satır | P0 |
| 13 | Talep üzerine render | yok | yok | IntersectionObserver + `setAnimationLoop(null)`; R2g TBT 2.5 s ile birlikte ölç | P0 |
| 1 | Sürekli kamera yolu | yok (sabit pozlar) | yok | CatmullRomCurve3 + ST scrub | P0 |
| 11 | Yükleyici % sayacı | yok (poster) | yok | LoadingManager.onProgress, poster üstünde | P1 |
| 17 | Exploded view | zayıf (1 parça) | — | Blender'da cezve/fincan parçaları ayrı node + yön × t | P1 |
| 3 | RT kompozit sahne geçişi | yok (RT yalnız sıvı) | yok | 2 RT + mix(mask) modülü | P1 |
| 4 | Noise/maske geçiş | yok | yok | 3 ile aynı modül, webgl-noise (MIT) | P1 |
| 6 | GPGPU parçacık | zayıf (basit nokta) | yok | GPUComputationRenderer + curl (buhar/telve tozu) | P1 |
| 12 | Ses tasarımı | zayıf (ses.ts, scroll bağı yok) | yok | scroll→filtre/ses düzeyi; Freesound CC0 | P1 |
| 16 | Mobil düşüş yolu | var (reduced-motion, matchMedia) / GPU kademesi yok | yok | detect-gpu kademesi → DPR/post | P1 |
| 10 | Dev tip + 3B katman | zayıf (12 px mono ×18) | yok | DOM dev tip + blend; 3B harf gerekmez | P1 |
| 2 | Scroll veri dokusu | yok | — | önce glTF kamera anim + AnimationMixer.setTime | P2 |
| 5 | Ekran akışkanı | var (kapta sıvı) | var (sivi-glsl) | gerekmez | — |
| 14 | Tek renderer çok sahne | yok | yok | yalnız kart çoğalırsa | P2 |
| 19 | Toon/outline | yok | yok | yön seçeneği (R3a) | P2 |
| 18/20/21/22 | Splat · fizik · WebGPU · Rive | yok | yok | TELVE kapsamı dışı | P2 |

## İçerik eksikleri (teknik değil, teşhis'ten)
Kapsam %25 (12 sahneden 3), doku haritası 0, gölge/AO 0, figür–zemin kontrastı 2.9:1 → bunlar modülle değil Blender + yön kararıyla kapanır (R3a yönleri). Teknik katalog bu eksikleri büyütmez; P0 teknikler içerik olmadan "ödüllü" görünüm vermez.

## K7'ye eklenecek modüller (kurulum tarifi `docs/atlas/site-3d.md` §C)
`post.ts` · `kamera-yolu.ts` · `metin.ts` · `dongu.ts` · `yukleyici.ts` · `gecis.ts` · `kademe.ts` + `varlik:optimize` betiği. Yalnız iskelet; TELVE'ye uygulama R3b.
