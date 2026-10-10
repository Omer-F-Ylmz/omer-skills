# recent.design

- **Ne:** Tasarım ilham galerisi arayüzü (kart + dialog) · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** DO45w8HX6nA · **İncelendi:** 2026-10-10
- **Teknoloji:** React SPA (Vite, route-chunk) · Sentry · özel CDN · Inter + Departure Mono · JS 476 KB (70 dosya)
- **Etiketler:** galeri, sonsuz-akış, oklch-renk, mikro-etkileşim

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Renk oklch: #0b0b0b zemin, oklch(0.6 0.25 12) pembe-kırmızı vurgu, beyaz yarı saydam katmanlar (oklch(0 0 0/0.447)).
- Font: Inter değişken 13px (gövde), Departure Mono (etiket).
- Geçişler: arka plan 0.18s, opacity 0.12/0.18s, transform 0.12s hepsi cubic-bezier(0.2,0,0,1) — "snappy" tek easing.
- Akış: 55 video önizleme, 130 SVG; sayfa 154294px (mobil) = sonsuz kaydırma, kart tıklayınca feed-item-dialog.
- Mobil: burger; sw 375<390 (15px yatay taşma).

## Öne çıkan efekt
- İnce 0.12–0.18s cubic-bezier(0.2,0,0,1) hover/opacity; oklch renk

## Bizde kullanım
- Tasarım ilham galerisi arayüzü (kart + dialog). İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri.
- Dikkat: yalnız teknik/mekanizma çıkarıldı; görsel, font, 3D model ve kaynak kod kopyalanmaz. Ticari fontlar için ücretsiz alternatif yukarıda.
- Sınırlama: galeri örnekleri bu turda gezilmedi; ilgili JS dosyalarına inilmedi, mekanizma ölçülen DOM/CSS/ağ verisinden çıkarıldı.
