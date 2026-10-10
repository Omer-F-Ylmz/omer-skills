# jesperlandberg.com

- **Ne:** Tasarımcı-mühendis portföyü; sahne tabanlı vitrin · **Sınıf:** V (galeri/vitrin) · **Kaynak video:** _SVU3oC4JX8 · **İncelendi:** 2026-10-10
- **Teknoloji:** Nuxt (Vue) · tek WebGL canvas · Basis transcoder · Mux video · DatoCMS · JS 480 KB
- **Etiketler:** webgl-sahne, nuxt, sanal-kaydırma, siyah-minimal

## Ölçülenler (playwright, 1280×720; mobil 390×844)
- Renk: saf #000 zemin, #fff metin (103 öğe) — tek renk, vurgu yok.
- Font: ABC Diatype Plus değişken (ticari; alternatif Inter/Geist), başlık 23.9px/700 — çok küçük tipografi, görsel iş eserlerinde.
- Kaydırma: scrollY hep 0 — içerik canvas içinde, tekerlek sanal ilerletiyor. 3 fixed öğe, opacity 0.3–0.5s cubic-bezier(0,0,0.2,1).
- Mux (stream.mux.com) HLS video önizlemeleri; Basis KTX2 doku çözücü → sıkıştırılmış doku ile WebGL galeri.
- Mobil 390: taşma yok, H=844 (tek ekran).

## Öne çıkan efekt
- Tek tam ekran WebGL sahnesi; sayfa DOM kaydırması yok (scrollHeight=720)

## Bizde kullanım
- Tasarımcı-mühendis portföyü; sahne tabanlı vitrin. İlgili skill: frontend-craft, scroll-craft, web-sahne-desenleri.
- Dikkat: yalnız teknik/mekanizma çıkarıldı; görsel, font, 3D model ve kaynak kod kopyalanmaz. Ticari fontlar için ücretsiz alternatif yukarıda.
- Sınırlama: galeri örnekleri bu turda gezilmedi; ilgili JS dosyalarına inilmedi, mekanizma ölçülen DOM/CSS/ağ verisinden çıkarıldı.
