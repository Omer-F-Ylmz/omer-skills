# adoratorio.com

- **Ne:** Ajans portföyü; sahne/grid geçişi · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** DO45w8HX6nA · **İncelendi:** 2026-10-10
- **Teknoloji:** Vue (Vite) · tek WebGL canvas · PP Adoratorio özel font · JS 140 KB
- **Etiketler:** ajans-vitrini, webgl-geçiş, sanal-kaydırma, vue

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Renk: #141414 zemin, #808080 gri, turuncu #ff752c (vurgu, 36 zemin), #e6e6e6.
- Font: PP Adoratorio özel (Regular/Medium); H1 13.3px — başlık görünür değil, tipografi görsel/imge içinde.
- Geçiş: renk 1s easeOutCubic, max-width+border-radius+transform 0.5s easeOutCubic (kart açılması); 5 fixed, sticky 2→3.
- scrollY 0 — DOM kaydırması yok, sanal; JS tek paket 140 KB (hafif).

## Öne çıkan efekt
- Vue + WebGL canvas, 1s cubic-bezier(0.215,0.61,0.355,1) renk geçişi

## Bizde kullanım
- Ajans portföyü; sahne/grid geçişi. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri.
- Dikkat: yalnız teknik/mekanizma çıkarıldı; görsel, font, 3D model ve kaynak kod kopyalanmaz. Ticari fontlar için ücretsiz alternatif yukarıda.
- Sınırlama: galeri örnekleri bu turda gezilmedi; ilgili JS dosyalarına inilmedi, mekanizma ölçülen DOM/CSS/ağ verisinden çıkarıldı.
