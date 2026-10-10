# linear.app

- **Ne:** Linear – The system for product development · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** 83YfBtINu74 · **İncelendi:** 2026-10-10
- **Teknoloji:** Next.js (App Router) · Inter Variable + Berkeley Mono · 192 JS parçası · JS 0 KB (192 dosya), görsel 92 KB, video 0 KB
- **Etiketler:** ürün-sitesi, koyu-tema, scroll-anlatı, mikro-etkileşim

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Ne: ürün geliştirme aracı; en çok kopyalanan koyu SaaS sitesi.
- Renk: zemin #0f1011, metin #f7f8f8, ikincil #8a8f98 / #62666d / #d0d6e0 (açık→koyu gri basamakları).
- Font: Inter Variable (3647 öğe) + Berkeley Mono (kod/etiket, ücretsiz alternatif JetBrains Mono).
- Geçiş: `color 0.1s cubic-bezier(0.25,0.46,0.45,0.94)` (easeOutQuad) — 216 öğe; yani her etkileşim ≤100 ms hissi. Filter+transform 0.16s.
- Kaydırma: 231 SVG, 2 fixed; her adımda 1–6 transform (bölüm başına illüstrasyon kayması/ölçekleme). 9619px, mobil hamburger.
- JS parça sayısı 192 (boyut ölçülemedi; önbellek).

## Öne çıkan efekt
- Kaydırmayla beliren ürün illüstrasyonları, 0.1s hızlı renk geçişleri

## Bizde kullanım
- Koyu SaaS landing deseni. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
