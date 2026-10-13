# Awwwards tarzı 3D scroll site — birleşim tarifi
Ne zaman: Hareket öncelikli, WebGL kahraman sahneli, scroll'a bağlı anlatım isteyen premium site.

## Fazlar
1. Yön ve keşif: `build-awwwards-quality-sites` — premium, sinematik, hareket öncelikli site isteği · birlikte: `web-sahne-desenleri` WebGL imleç, scroll'a bağlı 3D ürün pozu ve sahne kalite kapısı verir.
2. Plan: `fe-webgl-3d-hero` — three.js 3D kahraman sahnesini zayıf cihaz yedeğiyle planlar · birlikte: `ecc:motion-foundations` hareket tokenları ve reduced-motion kapısı kurar.
3. 3D sahne: `threejs` — sahne, ışık, malzeme, GLTF, performans · birlikte: `build-threejs-scroll-worlds` scroll'a bağlı kamera yolculuğu; model gerekirse `bl-glb-disa-aktar` küçük GLB çıkarır.
4. Scroll ve animasyon: `gsap-skills:gsap-scrolltrigger` — scroll animasyonu, parallax, pin · birlikte: `cinematic-gsap-lenis-motion-system` yumuşak scroll ve kademeli metin açılışı.
5. Performans: `gsap-skills:gsap-performance` — takılmayı azaltır · birlikte: `web-perf` Core Web Vitals ve Lighthouse performans puanını denetler.
6. İnceleme: `review-animations` — hareket kodunu yüksek zanaat çıtasıyla inceler · birlikte: `inclusive-interaction:motion-sensitivity` vestibüler hassasiyeti kontrol eder.
7. Kapanış: `superpowers:verification-before-completion`.

## İnceleme ajanları
- `fe-animasyon-tasarimci`: yalnız transform/opacity, reduced motion'a saygı.
- `impeccable`: genel arayüz denetimi.

## Güvenlik ve kalite kapıları
- Zayıf cihaz yedeği ve reduced-motion yolu çalışıyor.
- `web-perf` ile LCP ve etkileşim ölçüldü; `fixing-motion-performance` ile takılma giderildi.
- Erişilebilirlik: `ecc:accessibility`.
- Depoda sır yok: `gitleaks`.

## Tartışma konseyi
- Karar: 3D mi video mu, sahne ağırlığı ile performans dengesi.
- `ecc:council` — varsayılan Claude personaları: sanat yönetmeni, performans mühendisi, erişilebilirlik uzmanı.

## Jeton bütçesi
- Yön: orta (~12k, tahmini). Plan: küçük (~6k). 3D sahne: büyük (~50k). Scroll: orta (~20k). Performans + inceleme: orta (~15k). Kapanış: küçük (~3k). Hepsi tahmini.
- Referans site okuması `okuyucu` alt ajanına.

## Kaçınılacaklar
- Aynı sahnede birden çok scroll motoru (`gsap`, `animation-on-scroll`, `nateherk-design:scroll-craft`) karıştırmak.
- Reduced-motion yolu olmadan parallax.
- Sıkıştırılmamış büyük model yüklemek.

## Aday (kurulu değil)
- `@14islands/r3f-scroll-rig`: R3F WebGL'i smooth scroll'a ve DOM öğelerine bağlar.
- `tempus`: requestAnimationFrame döngü yöneticisi.
