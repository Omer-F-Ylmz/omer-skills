# camera-webgi.vercel.app

- **Ne:** TweakPane'siz ürün 3D landing (TWEEN/GSAP ile) · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** iYwCzKy6W40 · **İncelendi:** 2026-10-10
- **Teknoloji:** WEBGi (Pixotronics, three tabanlı) · tek canvas · Draco · JS 837 KB · Vercel
- **Etiketler:** 3d-ürün, webgi, scroll-kamera, demo

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Teknik: src bundle 710 KB (WEBGi + Three + uygulama), draco_decoder 127 KB; pixotronics cloud function ile lisans/analitik isteği.
- Renk: siyah, gri #808080, kırmızı #be1921 (vurgu), zemin #f0f0f0; DM Sans 400/500/700, H1 184px/700, harf aralığı −1.84px.
- Geçiş: `all 0.6–0.8s ease-in-out`, transform 1s; sayfa 3600px; canvas fixed.
- Mobil: 915px yatay taşma (sw 915) — masaüstü demosu, mobil uyumsuz.
- WEBGi ticari kütüphane (lisans gerekli); kod/model kopyalanmaz.

## Öne çıkan efekt
- WEBGi viewer + kaydırmayla kamera yolu, "Pro" 184px başlık

## Bizde kullanım
- TweakPane'siz ürün 3D landing (TWEEN/GSAP ile). İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri.
- Dikkat: yalnız teknik/mekanizma çıkarıldı; görsel, font, 3D model ve kaynak kod kopyalanmaz. Ticari fontlar için ücretsiz alternatif yukarıda.
- Sınırlama: galeri örnekleri bu turda gezilmedi; ilgili JS dosyalarına inilmedi, mekanizma ölçülen DOM/CSS/ağ verisinden çıkarıldı.
