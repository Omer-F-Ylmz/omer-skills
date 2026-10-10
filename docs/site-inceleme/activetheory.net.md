# activetheory.net

- **Ne:** Active Theory · Creative Digital Experiences · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** DO45w8HX6nA · **İncelendi:** 2026-10-10
- **Teknoloji:** Özel WebGL motoru (Hydra, app.js 340 KB) · basis/draco · özel font NB Architekt · JS 398 KB (14 dosya), görsel 1 KB, video 0 KB
- **Etiketler:** webgl-hero, 3d-ürün, imleç-efekti, özel-motor

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Ne: yaratıcı ajans; tüm site tek canvas içinde çalışan özel motor (Hydra).
- Ölçüm: DOM'da 1 canvas+webgl, 2 fixed öğe, scrollHeight=viewport (720) — kaydırma DOM'da değil, motor içinde sanal; wheel ile sayfa konumu değişmedi.
- Varlıklar: basis_transcoder (KTX2/Basis doku sıkıştırma) ve draco_wasm (mesh sıkıştırma) — 3B varlıkları küçük tutma yöntemi; hydra-thread.js = worker ile iş parçacığı.
- Geçiş: 0.4s cubic-bezier(0.17,0.4,0.02,0.99); ticker marquee 9s linear. Font NB Architekt (ticari).
- Mobil 844 yüksek tek ekran, motor aynı.
- Bizde: tek-canvas yaklaşımı yerine Three/R3F + KTX2/Draco boru hattı alınır (threejs-3d-paket).

## Öne çıkan efekt
- Tek WebGL canvas tüm siteyi çiziyor, DOM yok denecek kadar az

## Bizde kullanım
- Etkileşimli 3B portfolyo. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
