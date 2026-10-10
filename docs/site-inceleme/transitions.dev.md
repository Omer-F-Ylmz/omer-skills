# transitions.dev

- **Ne:** Transitions.dev: UI transitions for AI agents · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** ig-Dd3wMMsnz2P · **İncelendi:** 2026-10-10
- **Teknoloji:** Statik/SSR sayfa · Cloudflare · 3 canvas · Inter · JS 33 KB (6 dosya), görsel 2701 KB, video 0 KB
- **Etiketler:** galeri, geçiş-kütüphanesi, blur-geçiş

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Ne: AI ajanları için UI geçiş reçeteleri.
- Ana geçiş: `opacity, transform, filter 0.3s cubic-bezier(0.22,1,0.36,1)` — blur→net + yer değiştirme birleşimi; 65 öğede aynı.
- Renk #0d0d0d zemin, yarı saydam siyah paneller (rgba(0,0,0,0.28)); Inter + Roboto Mono + Saans. Görsel 2.7 MB, JS 33 KB (çok hafif).
- Mobil 375 genişlikte (390 viewport) 15 px yatay taşma ölçüldü.
- Bizde: bu blur+transform üçlüsü hazır geçiş token'ı olarak alınabilir.

## Öne çıkan efekt
- opacity+transform+filter(blur) 0.3s easeOutQuint geçişi

## Bizde kullanım
- Sayfa/öğe geçişi kütüphanesi için kaynak. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
