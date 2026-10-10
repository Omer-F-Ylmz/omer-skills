# aptransit.co

- **Ne:** Veri-odaklı 3D harita ürün sitesi · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** DO45w8HX6nA · **İncelendi:** 2026-10-10
- **Teknoloji:** Mapbox GL 2.12.0 · Turf.js 6 · anime.js 3.2.2 · 1 canvas (3D harita) · JS 474 KB
- **Etiketler:** harita-3d, mapbox, anime-js, canlı-veri

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Teknik: mapbox-gl.js 212 KB, turf.min.js 149 KB (coğrafi hesap), anime.js 7 KB, özel mta_box.js 80 KB; api.mapbox.com ile 14 istek, openweathermap.
- Font: Futura Md BT (ticari; alternatif Jost/League Spartan), H1 63px/400.
- Geçiş: opacity 0.2s ease (64 öğe), transform 0.5s ease-in-out, 50% yuvarlak (21 öğe — durak işaretleri).
- 6 fixed öğe, tam ekran harita; scrollY 0 (harita etkileşimi). Mobil burger, taşma yok.

## Öne çıkan efekt
- Mapbox 3D bina haritasında canlı metro konumları (anime.js ile geçiş)

## Bizde kullanım
- Veri-odaklı 3D harita ürün sitesi. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri.
- Dikkat: yalnız teknik/mekanizma çıkarıldı; görsel, font, 3D model ve kaynak kod kopyalanmaz. Ticari fontlar için ücretsiz alternatif yukarıda.
- Sınırlama: galeri örnekleri bu turda gezilmedi; ilgili JS dosyalarına inilmedi, mekanizma ölçülen DOM/CSS/ağ verisinden çıkarıldı.
