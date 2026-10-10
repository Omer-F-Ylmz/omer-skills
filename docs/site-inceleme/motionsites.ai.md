# motionsites.ai

- **Ne:** MotionSites AI — Official Premium AI Website Prompts · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** GPpYwjMoLio · **İncelendi:** 2026-10-10
- **Teknoloji:** React SPA (Vite, assets/index-*.js) · Tailwind · hls.js 151 KB · Meta Pixel · JS 651 KB (44 dosya), görsel 74438 KB, video 0 KB
- **Etiketler:** galeri, hls-video-arka-plan, shimmer-iskelet

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Ne: AI site prompt'ları satan vitrin; her şablon canlı video önizleme.
- Teknik: hls.js (m3u8) ile adaptif video; 25 video öğesi, sayfa görsel ağırlığı ~74 MB (çok ağır — bizde kopyalanmamalı).
- Geçişler 0.3s ease-out, `shimmer 1.6s` iskelet animasyonu, kart hover opacity 0.3s. Font sistem (-apple-system).
- Mobil 390px taşma yok, hamburger var.
- Örnekler: sitedeki Cinematic/Premium şablon kartları — hepsi tam ekran video hero + cam (blur) kart; mekanizma: <video> + backdrop-filter + metin katmanı.

## Öne çıkan efekt
- Kartlar hls.js ile akış videosu önizlemesi oynatıyor

## Bizde kullanım
- Hero için video arka plan + prompt satışı fikri. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
