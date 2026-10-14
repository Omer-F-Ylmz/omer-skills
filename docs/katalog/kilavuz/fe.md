# fe — 43 benzersiz kayıt

**Amaç:** Ön yüz uzman ajanları: CSS/Tailwind, bileşen, tasarım sistemi, performans (görsel, font, sanal liste), çerçeveye özel (Astro, Qwik, Remix) ve eski kod bakımı (jQuery, AngularJS).

**İç yapı:** Tümü [ajan], fe-<konu> adlı tek iş odaklı; gruplar: CSS (css-*, tailwind*), tasarım (tasarim-*, tipografi, karanlik-mod), performans, çerçeve, legacy bakım, içerik/SEO.

## En güçlü parçalar
- `fe-css-hata-bulucu` — Overflow, stacking context, specificity, flex/grid sürprizlerinde CSS hata ayıklama.
- `fe-react-bilesen-inceleme` — Gereksiz render, effect ve bundle ağırlığı yüzünden yavaş React UI'larında.
- `fe-tasarim-sistemi-kurucu` — Tasarım token'ları, bileşen kuralları ve DESIGN.md üretir.
- `fe-tasarim-yonu` — Görünüm kararsızken cesur görsel yön seçip tasarım brief'i yazar.
- `fe-responsive-kontrol` — Mobil, tablet, masaüstü genişliklerde düzeni kontrol edip kırılmaları listeler.
- `fe-gorsel-optimize` — Modern format, srcset, lazy loading ve hero/LCP görsel optimizasyonu.
- `fe-bos-durum-yazar` — Boş, yükleniyor ve hata durumlarını yardımcı metin ve CTA ile tasarlar.
- `fe-cerez-oturum-hata` — Ayarlanmayan/gönderilmeyen çerezler ve beklenmedik oturum kapanmaları.
- `fe-sanal-liste` — Çok uzun liste/tablolarda windowing, satır yüksekliği, scroll geri yükleme.
- `fe-eposta-sablonu` — Outlook, Gmail, Apple Mail için karanlık modlu duyarlı HTML e-posta.

## Birlikte kullanım
- fe-tasarim-yonu → fe-tasarim-sistemi-kurucu → fe-bilesen-yazar → fe-tasarim-incele.
- fe-tipografi-uzmani + fe-web-font-yukleme: ölçek/eşleşme ve hızlı font yükleme.
- fe-tailwind + fe-tailwind-duzenleyici: yazım ve sonradan sınıf toparlama.
- fe-scroll-hikayesi + fe-animasyon-tasarimci: sahne planı ve transform/opacity hareketi.

## Tuzaklar
- fe-animasyon-tasarimci yalnız transform/opacity kullanır ve reduced motion'a uyar; ağır efekt beklenmemeli.
- fe-webgl-3d-hero ve fe-webxr performans bütçesi/zayıf cihaz fallback'i ister.
- fe-tailwind ile fe-tailwind-duzenleyici, fe-bilesen-yazar ile fe-bilesen-kutuphanesi kapsamları örtüşür.
- fe-site-mimarisi ile marketingskills site-architecture benzer konuyu kapsar.

## Üyeler
- ajan (43): fe-angularjs-bakim, fe-animasyon-tasarimci, fe-astro, fe-bilesen-kutuphanesi, fe-bilesen-yazar, fe-bos-durum-yazar, fe-cerez-oturum-hata, fe-css-hata-bulucu, fe-css-konteyner-sorgusu, fe-css-mimarisi, fe-cursor-efekt, fe-dashboard-duzeni, fe-donusum-optimize, fe-eposta-sablonu, fe-form-tasarimci, fe-gorsel-optimize, fe-ikon-sistemi, fe-jquery-bakim, fe-karanlik-mod, fe-meta-seo-duzeltici, fe-navigasyon-tasarimci, fe-pwa-cevrimdisi, fe-qwik, fe-react-bilesen-inceleme, fe-remix, fe-responsive-kontrol, fe-rollup-kutuphane-paketi, fe-sanal-liste, fe-scroll-hikayesi, fe-site-mimarisi, fe-slayt-kurucu, fe-tailwind, fe-tailwind-duzenleyici, fe-tasarim-incele, fe-tasarim-sistemi-kurucu, fe-tasarim-yonu, fe-tipografi-uzmani, fe-ux-metin-yazar, fe-web-font-yukleme, fe-webgl-3d-hero …
