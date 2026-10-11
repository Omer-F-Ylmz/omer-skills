# IMAGE EXPAND ON SCROLL - GSAP Elementor Scrolltrigger
## Künye
IMAGE EXPAND ON SCROLL - GSAP Elementor Scrolltrigger · Nicolai Palmkvist · süre: 8:09 · en-orig · https://youtu.be/frpM0nlPKfY · şema 2
motor: parti 2026-10-11-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 50184 tk · claude-haiku-5-5: claude-haiku-5-5 · 169389 tk
## Özet
Nicolai Palmkvist, Elementor (flexbox container) içinde GSAP ScrollTrigger ile kaydırınca daire şeklindeki görselin tam genişliğe genişlediği (image expand on scroll) efekti sıfırdan kurar. Önce hazır şablonu (Gumroad) içe aktarmayı gösterir; sonra ana konteyner, metin konteyneri, sticky konteyner ve görsel konteyneri oluşturulur, HTML widget'ına jQuery/GSAP/ScrollTrigger kodu eklenir, CSS sınıfları verilir, yerleşim hatası (sticky konteynerin iç içe olması) düzeltilir ve mobil için duyarlı kod sürümü kullanılır.
## Bölümler
- 0:00 Efektin tanıtımı
- 0:39 Şablonu içe aktarma
- 1:27 Konteynerleri kurma
- 2:25 Sticky bölüm oluşturma
- 3:32 Görsel konteyneri kurulumu
- 4:16 Özel kodu uygulama
- 5:34 Yerleşim sorunlarını düzeltme
- 7:24 Duyarlı (responsive) yapma
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| GSAP | yok | teknik | yok | Animasyon kütüphanesi; daireyi tam genişliğe genişleten zaman çizelgesi (timeline) animasyonu. | 4:29 | Kod sayfasında gsap.min.js script etiketi ve gsap.registerPlugin görünür. (karede: kanıttan) Kod sayfasında gsap.min.js script etiketi ve gsap.registerPlugin görünür. |
| ScrollTrigger | yok | plugin | yok | GSAP eklentisi; kaydırmaya bağlı (scrub) animasyon tetikler. | 4:29 | ScrollTrigger.min.js script satırı ve ScrollTrigger.defaults görünür. (karede: kanıttan) ScrollTrigger.min.js script satırı ve ScrollTrigger.defaults görünür. |
| Elementor | yok | plugin | yok | WordPress sayfa oluşturucu; konteynerler, sticky, HTML widget burada kuruldu. | 1:27 | Elementor editörü, Edit Container paneli görünür. (karede: kanıttan) Elementor editörü, Edit Container paneli görünür. |
| Flexbox Container | yok | teknik | yok | Elementor flexbox konteyner özelliği; yerleşim için etkinleştirilmesi gerekir. | 1:27 | Flexbox Container Default/Active/Inactive seçenekleri görünür. (karede: kanıttan) Flexbox Container Default/Active/Inactive seçenekleri görünür. |
| jQuery | yok | teknik | yok | Kodun $(".sticky_circle_wrap") seçicileri için yüklenen kütüphane. | 4:29 | jquery.min.js 3.7.1 script satırı görünür. (karede: kanıttan) jquery.min.js 3.7.1 script satırı görünür. |
| Elementor Sticky (Motion Effects) | yok | teknik | yok | Konteyneri üstte yapışık tutan hareket efekti; Offset 100, Stay in Column. | 2:25 | Motion Effects altında Sticky: Top, Offset, Effects Offset, Stay In Column görünür. · kanıt: kare (karede: Motion Effects altında Sticky: Top, Offset, Effects Offset, Stay In Column görünür.) |
| Elementor Navigator | yok | ipucu | yok | Konteyner hiyerarşisini görmek için gezgin paneli. | 3:00 | Navigator panelinde Main container, Text container, Sticky, Expand images görünür. · kanıt: kare (karede: Navigator panelinde Main container, Text container, Sticky, Expand images görünür.) |
| Elementor HTML widget | yok | teknik | yok | Kodun yapıştırıldığı widget. | 4:40 | Edit HTML paneli ve widget arama sonucu HTML görünür. · kanıt: kare (karede: Edit HTML paneli ve widget arama sonucu HTML görünür.) |
| Gumroad | yok | iş akışı | yok | Hazır Elementor şablonunun indirildiği servis. | 0:55 | Forrest Tower Elementor Template sayfası, I want this! düğmesi görünür. (karede: kanıttan) Forrest Tower Elementor Template sayfası, I want this! düğmesi görünür. |
| Elementor Template Library | yok | iş akışı | yok | JSON şablonu içe aktarma kütüphanesi. | 1:10 | Import Template to Your Library, Select File görünür. · kanıt: kare (karede: Import Template to Your Library, Select File görünür.) |
| Chrome DevTools | yok | CLI | yok | Mobil görünümü (iPhone 12 Pro) test etmek için. | 7:49 | Dimensions: iPhone 12 Pro 390x844 ve Elements paneli görünür. · kanıt: kare (karede: Dimensions: iPhone 12 Pro 390x844 ve Elements paneli görünür.) |
| Google Earth | yok | teknik | yok | Tanıtımda Orman Kulesi konumunu göstermek için kullanıldı. | 0:24 | earth.google.com adres çubuğu ve harita görünür. (karede: kanıttan) earth.google.com adres çubuğu ve harita görünür. |
| Astra | yok | teknik | yok | WordPress teması (sınıf adlarında ast-). | 0:37 | OCR'da ast-single-post, astra-4 sınıfları geçiyor. |
| Envato Elements | yok | teknik | yok | Medya ekleme penceresinde sekme olarak görünür; görsel için kütüphane kullanıldı. | 4:04 | Insert Media penceresinde Envato Elements sekmesi görünür. (karede: kanıttan) Insert Media penceresinde Envato Elements sekmesi görünür. |
| ChatGPT | yok | teknik | yok | Yalnız Chrome yeni sekmesi kısayolunda görünür. | 4:27 | Yeni sekmede ChatGPT kısayolu görünür. (karede: kanıttan) Yeni sekmede ChatGPT kısayolu görünür. |
| WordPress | yok | teknik | yok | Sitenin çalıştığı içerik yönetim sistemi; Elementor düzenleyicisi wp-admin üzerinden açılıyor. | 0:36 | Adres çubuğunda wp-admin/post.php?...action=elementor adresi · kanıt: kare (karede: Tarayıcı adres çubuğunda michellewp.com/wp-admin/post.php?post=5980&action=elementor (OCR)) |
| cdnjs (Cloudflare CDN) | yok | teknik | yok | Cloudflare üzerinden JavaScript kütüphanelerini sunan CDN; GSAP ve jQuery bu adresten yükleniyor. | 4:29 | Script adreslerinde cdnjs.cloudflare.com/ajax/libs/ yolu · kanıt: kare (karede: Script etiketlerinde cdnjs.cloudflare.com adresi (OCR)) |
| CSS | yok | teknik | yok | Stil dili; container'lara CSS Classes alanından sınıf ekleniyor (sticky_circle_wrap, circle). | 4:16 | 'insert this sticky Circle WP ... CSS classes' |
| Google Chrome | yok | teknik | yok | Web tarayıcısı; sayfa yeni sekmede açılıp kaydırma testi yapılıyor. | 5:18 | 'so I'll just open in a new tab okay let's test it' · kanıt: yok |
## Açıklama bağlantıları
- https://nicolaipalmkvist.com/code-expand-images/ — Kod ve şablon sayfası (kod, sınıflar, duyarlı sürüm) · aday: hayır · Yazarın kendi kod/şablon sayfası; araç değil, videonun kaynak sayfası. · sınıf: diğer
- https://youtu.be/LceOy5dnaYI?si=w45iCWDWhMwCwzrP — Yazarın Elementor projeleri oynatma listesi/videosu · aday: hayır · Referans video; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://nicolaipalmkvist.com/?utm_source=youtube&utm_medium=subscription&utm_campaign=image-expand-round — Yazarın ana sayfası (UTM izleme parametreli) · aday: hayır · Referans ana sayfa; yalnız UTM izleme parametresi var, affiliate sayılmadı. · sınıf: diğer
- https://lifeonablock.com — Demo siteyi içeren yazar sitesi · aday: hayır · Demo/referans site; araç değil. · sınıf: diğer
- https://lifeonablock.com/forrest-tower — Forrest Tower demo sayfası · aday: hayır · Demo/referans sayfa; araç değil. · sınıf: diğer
- https://nicolaipalmkvist.com/?utm_source=youtube&utm_medium=subscription&utm_campaign=lifeonablock-live-demo — Yazarın ana sayfası, canlı demo kampanyası (UTM parametreli) · aday: hayır · Referans sayfa; yalnız UTM izleme parametresi var. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kaydırmayla daireden tam genişliğe genişleyen görsel (scroll-triggered image expand / scrub) | Daire şeklindeki görsel kaydırınca tam genişliğe açılır, geri kaydırınca daire olur; GSAP fromTo ile width 40em→100%, borderRadius 20em→0. (karede: Forest Tower sayfasında oval/daire görsel 'Making of Forrest tower Denmark' başlığıyla görünür.) | 0:00 | kare |
| Yapışkan bölüm (sticky section) | Sticky konteyner üstte yapışık kalır; görsel genişlerken sabit durur. (karede: Motion Effects altında Sticky: Top ve Offset 0 alanları görünür.) | 2:25 | kare |
| Ortalanmış arka plan görseli (cover background) | Görsel konteynerinde Position Center Center, No-repeat, Size Cover. (karede: Style panelinde Position Center Center, Repeat No-repeat, Display Size Cover görünür.) | 4:06 | kare |
| Koyu bölüm üzerinde ortalanmış başlık, metin ve düğme (hero text block) | Başlık, paragraf ve Explore project düğmesi ortalanmış; üstte rozet. (karede: Koyu zeminde 'Add Your Heading Text Here', paragraf, Explore project düğmesi ve How it was built rozeti.) | 2:03 | kare |
| Duyarlı (responsive) kırılma noktası | Mobilde hap şeklinde dikey görsel; kod 768px matchMedia kırılma noktası içerir. (karede: iPhone 12 Pro boyutunda mobil önizlemede dikey oval görsel görünür.) | 7:49 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Efekt ücretsizdir ve yalnızca birkaç satır kod eklemek yeterlidir; duyarlıdır. | 0:00 | özellik |
| Sticky ayarı için Offset ve Effects Offset 100 önerilir; ana konteyner CSS sınıfı sticky_circle_wrap, görsel konteyneri sınıfı circle olmalıdır. | 2:25 | öneri |
| Yükseklik 400vh, genişlik 100%; sticky bölüm 90vh; görsel konteyneri 600x600. | 1:27 | sayısal |
| Sticky konteyner metin konteynerinin içinde olmamalı; HTML widget en altta olmalı yoksa çalışmaz. | 5:34 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | ScrollTrigger | ScrollTrigger | Efekt ScrollTrigger olarak anlatılıyor. |
| açıklama | GSAP | GSAP | Açıklamada GSAP animasyonu. |
| konuşma 0:00 | Google Earth | Google Earth | 0:24 karelerinde Google Earth gösteriliyor. |
| konuşma 0:39 | Elementor editörü | Elementor | Editör içinde çalışılıyor. |
| konuşma 0:39 | Gumroad şablon sayfası | Gumroad | I want this ile indirme. |
| konuşma 0:39 | Elementor templates içe aktarma | Elementor Template Library | Import Template to Your Library. |
| konuşma 1:27 | flexbox container | Flexbox Container | Ayarlardan etkinleştirme. |
| konuşma 2:25 | sticky / motion effects | Elementor Sticky (Motion Effects) | Sticky Top, offset. |
| konuşma 2:25 | Navigator | Elementor Navigator | Konteyner hiyerarşisi. |
| konuşma 4:16 | HTML widget | Elementor HTML widget | Kod yapıştırma. |
| kare 4:29 | jQuery 3.7.1 | jQuery | script satırı. |
| kare 4:29 | gsap.min.js 3.8.0 | GSAP | script satırı. |
| kare 4:29 | ScrollTrigger.min.js | ScrollTrigger | script satırı. |
| kare 4:29 | cdnjs.cloudflare.com | aday değil: başka adayın parçası (GSAP) | Script CDN adresi. |
| kare 4:27 | ChatGPT kısayolu | aday değil: konu dışı | Yalnız yeni sekme kısayolu; kullanılmıyor. |
| kare 4:04 | Envato Elements sekmesi | Envato Elements | Medya penceresinde sekme. |
| kare 7:49 | Chrome DevTools mobil | Chrome DevTools | iPhone 12 Pro. |
| OCR 0:37 | Astra teması sınıfları | Astra | ast-single-post. |
| OCR 0:33 | Yer imleri (Fiverr, Paypal, VidiQ) | aday değil: konu dışı | Yer imi çubuğu. |
| OCR 7:55 | webguard.dk Reveal content demosu | aday değil: konu dışı | Sonraki video önerisi. |
| yorum | Elementor Pro / önbellek eklentisi | aday değil: konu dışı | Yazarın yorumundaki öneri. |
| açıklama | nicolaipalmkvist.com kod sayfası | aday değil: konu dışı | Kod/şablon sayfası. |
| sözlük | Claude Sonnet, Codex, Inter, Descript, Go, Make, Next.js, Llama, Framer Motion, Astro, TypeScript, Claude, Cloudflare, JavaScript, Canva, context7, Clash Display | aday değil: genel kavram | Sözlük eşleşmesi, videoda kullanılmıyor (Cloudflare yalnız CDN adresi). |
## Kareden okunanlar
- 0:00: webguard.dk/final-result-1/ sayfası, Forest Tower başlığı ve daire görsel; altyazı 'How to create this scroll'.
- 0:24: Google Earth haritası, 7X3G+7R Rønnede konumu.
- 1:01: Gumroad indirme sayfası: elementor-3470-2024-08-21 JSON ve ZIP dosyaları, Download düğmeleri.
- 1:10: Elementor Library: Import Template to Your Library, Select File.
- 1:47: Genişlik 100, yükseklik alanı; '400vh' yazısı.
- 1:55: Renk seçici ve #2C2A24 arka plan rengi.
- 2:59: Motion Effects: Sticky Top, Offset 0, Effects Offset 0, Stay In Column No.
- 4:29: Kod sayfası: 'CODE - IMAGE EXPAND ON SCROLL - GSAP Elementor', jquery 3.7.1, gsap 3.8.0, ScrollTrigger script satırları.
- 4:40: Edit HTML paneli, kodda sticky_circle_wrap ve width 40em, borderRadius 20em değerleri.
- 5:10: CSS Classes alanı; ipucu 'Add your custom class WITHOUT the dot'.
- 7:49: Mobil önizleme iPhone 12 Pro 390x844, DevTools.
## Belirsizlikler
- Sözlük eşleşmeleri (Claude Sonnet, Codex, Inter, Descript, context7, Clash Display vb.) videoda kullanılmıyor; bulanık eşleşmeler yanlış pozitif.
- Elementor Pro gerekliliği videoda belirtilmiyor; yorumda sticky için Pro gerektiği söyleniyor.
- Kurulum terminal komutu yok; yalnız HTML/CSS sınıf girişi var (sticky_circle_wrap, circle).
- Orman Kulesi'nin Google Earth gösterimi yalnızca tanıtım amaçlı; kare listesinde 0:24-0:28 altyazısı ile eşleşme belirsiz.
- Gumroad ve app.gumroad.com URL'lerinde OCR hataları var (c2aa88... / cc2aa88...).
- Elementor Pro'nun sticky'yi sağlayıp sağlamadığı ve Astra temasının kullanıldığı yalnızca OCR/sınıf adlarından çıkarıldı.
- Tüm 'zaman' değerleri kare ve altyazı saatlerine dayanır; bazı kare okumaları bulanık.
## Atlanan segment oranı
0/11 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://nicolaipalmkvist.com/code-expand-images/ | açıklama | açıklama | hayır |
| https://youtu.be/LceOy5dnaYI?si=w45iCWDWhMwCwzrP | açıklama | açıklama | hayır |
| https://nicolaipalmkvist.com/?utm_source=youtube&utm_medium=subscription&utm_campaign=image-expand-round | açıklama | açıklama | hayır |
| https://lifeonablock.com | açıklama | açıklama | hayır |
| https://nicolaipalmkvist.com/?utm_source=youtube&utm_medium=subscription&utm_campaign=lifeonablock-live-demo | açıklama | açıklama | hayır |
| lifebonablock.com | 0:26 | ekran | hayır |
| michellewp.com/wp-admin/post.php?post=5980&action=elementor | 0:36 | ekran | hayır |
| michellewp.com/rebuild/ | 0:37 | ekran | hayır |
| michellewp.gumroad.com/l/mpceq | 0:53 | ekran | evet |
| https://lifeonablock.com/forrest-tower/ | 0:57 | ekran | hayır |
| https://lifeonablock.com/code-expand-imagel | 0:58 | ekran | hayır |
| app.gumroad.com/d/cc2aa88a3cda0b7a1c4036a2c0aede21 | 1:03 | ekran | evet |
| michellewp.com/empty-page/ | 1:15 | ekran | hayır |
| lifeonablock.com/code-expand-image/ | 4:29 | ekran | hayır |
| https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js | 4:29 | ekran | evet |
| https://cdnjs.cloudflare.com/ajax/libs/gsap/3.8.0/gsap.min.js | 4:29 | ekran | evet |
| https://cdnjs.cloudflare.com/ajax/libs/gsap/3.8.0/ScrollTrigger.min.js | 4:29 | ekran | evet |
| webguard.dk/final-result-scrolltrigger-elementor/ | 7:55 | ekran | hayır |
| earth.google.com | 0:24 | ekran | evet |
| webguard.dk/final-result-1/ | 0:00 | ekran | hayır |
| app.gumroad.com/d/c2aa88a3cda0b7a1c4036a2c0aede21 | 1:01 | ekran | evet |
| https://app.gumroad.com/r/cc2aa88a3cda0b7a1c4036a2c0aede21/product_files | 1:03 | ekran | evet |
| https://cdnjs.cloudflare.com/ajax | 5:04 | ekran | evet |
| imeo.com | 7:49 | ekran | hayır |
## İş akışı
- 1. adım — Tanıtım: bitmiş efekt gösterilir (daireden tam genişliğe) — araçlar: Elementor, GSAP, ScrollTrigger
- 2. adım — İsteğe bağlı: Gumroad'dan hazır şablonu indirme — araçlar: Gumroad
- 3. adım — Elementor Library'den şablonu içe aktarma — araçlar: Elementor Template Library, Elementor
- 4. adım — Ana konteyner: flexbox, genişlik %100, yükseklik 400vh, arka plan rengi #2C2A24 — araçlar: Elementor, Flexbox Container
- 5. adım — Metin konteyneri: boxed 1330px; başlık, metin ve düğme ekleme — araçlar: Elementor
- 6. adım — Sticky konteyner: tam genişlik, 90vh, ortalı içerik, Sticky Top, offset 100 — araçlar: Elementor, Elementor Sticky (Motion Effects)
- 7. adım — Navigator ile konteynerleri adlandırma (Main, Text, Sticky) — araçlar: Elementor Navigator
- 8. adım — Expand images konteyneri: 600x600, ortalı, arka plan görseli (center, no-repeat, cover) — araçlar: Elementor
- 9. adım — Kod sayfasından JS kodunu kopyalayıp HTML widget'a yapıştırma — araçlar: Elementor HTML widget, GSAP, ScrollTrigger, jQuery
- 10. adım — CSS sınıflarını ekleme: ana konteynere sticky_circle_wrap, görsele circle — araçlar: Elementor
- 11. adım — Yeni sekmede önizleme ile test — araçlar: Elementor
- 12. adım — Hata düzeltme: sticky konteyneri metin konteynerinden çıkarıp HTML'yi en alta alma — araçlar: Elementor Navigator, Elementor HTML widget
- 13. adım — Güncelle, yenile; Stay in Column'u açarak sticky davranışını düzeltme — araçlar: Elementor, Elementor Sticky (Motion Effects)
- 14. adım — Duyarlı kod sürümünü HTML widget'a yapıştırma ve mobilde test — araçlar: Elementor HTML widget, Chrome DevTools
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
