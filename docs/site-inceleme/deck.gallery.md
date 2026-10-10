# deck.gallery

- **Ne:** Deck.gallery - Beautifully designed decks, curated · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** ig-Ddqj0svm6yq · **İncelendi:** 2026-10-10
- **Teknoloji:** Astro (adalar) + React · Clerk (auth, 559 KB) · Inter · JS 933 KB (143 dosya), görsel 88 KB, video 0 KB
- **Etiketler:** galeri, sunum-arşivi, astro-adaları

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Ne: sunum (deck) tasarım galerisi.
- Renk beyaz zemin, #2b2b2b metin; geçişler `opacity 0.2s / transform 0.4s cubic-bezier(0.22,1,0.36,1)` (467 + 246 öğe).
- Teknik: Astro "island" mimarisi, 143 JS dosyası (933 KB, 559 KB yalnız Clerk). Dersler: auth kütüphanesi bütün sayfayı şişirir; bizde lazy yükle.
- Mobil sayfa 51289px (tek sütun uzun akış), taşma yok.

## Öne çıkan efekt
- Çok uzun masonry akışı (20132px) + easeOutQuint opacity/transform

## Bizde kullanım
- Çok uzun galeri sayfası performansı. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
