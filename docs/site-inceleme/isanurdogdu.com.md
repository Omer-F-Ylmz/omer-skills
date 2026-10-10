# isanurdogdu.com

- **Ne:** İsa Nurdoğdu — Yapay zeka sistemleri · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** 0sQxSXyVPwI · **İncelendi:** 2026-10-10
- **Teknoloji:** Next.js (App Router, Turbopack) · animasyon kütüphanesi yok; saf CSS · JS 158 KB (10 dosya), görsel 19 KB, video 0 KB
- **Etiketler:** editoryal, kinetik-tipografi, css-animasyon

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Renk: ink #000/#0d0d0f/#1b1b1e, kâğıt #f2f2f0, gri #6d6d73/#a9a9ae, vurgu amber #e8b04b (CSS değişkenleri --ink-*, --paper, --amber).
- Font: Bricolage Grotesque (başlık, 94.72px/700, letter-spacing −1.9px, satır 0.96) + Instrument Sans (gövde 17px) + JetBrains Mono (etiket); hepsi Google Fonts, next/font ile.
- Hareket: smooth-scroll yok, canvas yok; bölümler `rise 0.7s cubic-bezier(0.2,0.7,0.2,1)` ve `fade 1.1s` keyframe ile açılıyor; `prefers-reduced-motion: no-preference` sorgusuyla korunmuş (erişilebilirlik için örnek).
- Yapı: hero → Ne yapıyorum → Birlikte kuralım → Kısaca ben → Bana ulaş; sayfa 3332px, tek sütun. Mobil 390px taşma yok.
- Mekanizma: yalnız CSS; JS 158 KB (çoğu Next çalışma zamanı).

## Öne çıkan efekt
- Yükselme animasyonu: CSS keyframe rise 0.7s, ease (0.2,0.7,0.2,1)

## Bizde kullanım
- Kişisel/freelance portföy sayfası. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri, hareket-altyazi-3d-paket.
- Dikkat: yalnız teknik/desen alınır; görsel, font, 3B varlık ve metin kopyalanmaz. Ticari fontlar için ücretsiz alternatif kullanılır.
