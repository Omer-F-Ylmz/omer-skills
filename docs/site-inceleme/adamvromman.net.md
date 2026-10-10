# adamvromman.net

- **Ne:** 3D nesne vitrini portföyü · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** rOs-TFUeuSg · **İncelendi:** 2026-10-10
- **Teknoloji:** Astro 5.15.5 · Three.js (FlyingObjects 747 KB) · Draco WASM · Matomo · Geist · JS 956 KB + video 10 MB
- **Etiketler:** webgl-hero, astro, uçan-3d-nesneler, draco

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Renk: siyah #000, açık gri #eee, elektrik-mavi #4000ff (vurgu, 12 zemin), yeşil #00c496, kırmızı #de0d00, #fe6147.
- Font: Geist 100–900, H1 76.8px/700 uppercase, satır = boyut (0.96-1.0 sıkı).
- Mekanizma: ayrı SingleFlyingObject bileşeni + draco_wasm; geçiş 0.1s ease-out (renk), 0.3s transform. 7 fade öğesi, 11 SVG.
- Ağırlık: JS 956 KB, video 10 MB — mobilde maliyetli; ders: lazy/viewport-bazlı yükleme.
- scrollY 0 kalıyor (sahne sabit, ilerleme dahili); mobil 390 taşmasız.

## Öne çıkan efekt
- Astro bileşeninde 3D uçan nesneler (Draco sıkıştırmalı), canvas sahnesi

## Bizde kullanım
- 3D nesne vitrini portföyü. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri.
- Dikkat: yalnız teknik/mekanizma çıkarıldı; görsel, font, 3D model ve kaynak kod kopyalanmaz. Ticari fontlar için ücretsiz alternatif yukarıda.
- Sınırlama: galeri örnekleri bu turda gezilmedi; ilgili JS dosyalarına inilmedi, mekanizma ölçülen DOM/CSS/ağ verisinden çıkarıldı.
