# REVEAL CONTENT ON SCROLL - GSAP Elementor Scrolltrigger
## Künye
REVEAL CONTENT ON SCROLL - GSAP Elementor Scrolltrigger · Nicolai Palmkvist · süre: 9:18 · en-orig · https://youtu.be/yezd-afdvjc · şema 2
motor: parti 2026-10-11-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 52028 tk · claude-haiku-5-5: claude-haiku-5-5 · 170097 tk
## Özet
Nicolai Palmkvist, Elementor içinde GSAP ScrollTrigger ile kaydırmada içerik/görsel açılan (reveal) bir efekti sıfırdan kuruyor. Kapsayıcılar (container) iç içe kurulup CSS sınıfları verilir, sağ sütun sticky yapılır, görsel arka plan olarak eklenir. Sonra bir HTML widget'ına GSAP kodu yapıştırılır, test edilir, renk kodları değiştirilir ve sorun olursa kullanılacak ek CSS gösterilir.
## Bölümler
- 0:00 Efektin tanıtımı
- 0:30 Proje kurulumu
- 0:58 Ana kapsayıcıyı kurma
- 2:20 Metin içerik alanını oluşturma
- 3:50 Başlık ve metin ekleme
- 4:18 Sağ sütunu kurma
- 5:01 Sticky görselleri ayarlama
- 5:34 Görseli biçimlendirme
- 6:28 Sihirli kodu ekleme
- 7:24 Açılma efektini test etme
- 7:49 Renkleri özelleştirme
- 8:26 CSS sorun giderme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Elementor | yok | teknik | yok | WordPress sayfa oluşturucu; tüm efekt burada kapsayıcılarla kuruluyor | 0:30 | Elementor düzenleyici paneli ve kapsayıcı ayarları kullanılıyor (karede: Edit Container paneli, Layout/Style/Advanced sekmeleri ve Elementor widget listesi) |
| GSAP | yok | teknik | yok | Greensock animasyon kütüphanesi; kaydırma efektinin temeli | 0:00 | Açıklama: Greensock library kullanarak GSAP ile scroll-trigger efekti |
| ScrollTrigger | yok | teknik | yok | GSAP eklentisi; kaydırmaya bağlı animasyon tetikler | 5:23 | Kodda ScrollTrigger.defaults ve ScrollTrigger.min.js script satırı (karede: Kod: ScrollTrigger.defaults({ markers: false }) ve cdnjs ScrollTrigger.min.js script etiketi) |
| gsap.matchMedia | yok | teknik | yok | Masaüstü genişliğine özel animasyon koşulu | 6:13 | Kodda let mediaAnimation = gsap.matchMedia() satırı (karede: Kod satırları: let mediaAnimation = gsap.matchMedia(); mediaAnimation.add("(min-width: 666px)")) |
| clip-path inset | yok | teknik | yok | Görselin kırpılarak açılmasını sağlayan CSS tekniği | 6:47 | gsap.set(photos, { clipPath: 'inset(100% 0% ... (karede: Kod: gsap.set(photos, { clipPath: 'inset(100% 0% ...) |
| cdnjs | yok | teknik | yok | GSAP script dosyalarını yükleyen CDN | 5:23 | cdnjs.cloudflare.com/ajax/libs/gsap/3.11.0/gsap.min.js (karede: Script src adresi cdnjs.cloudflare.com/ajax/libs/gsap/3.11.0/gsap.min.js) |
| Elementor Sticky | yok | teknik | yok | Motion Effects altında sticky top ve stay in column | 5:01 | Sağ sütunda sticky Top ve Stay in Column açılıyor · kanıt: kare (karede: Motion Effects: Sticky Top, Sticky On cihaz etiketleri, Stay in Column anahtarı) |
| HTML widget | yok | teknik | yok | GSAP kodunun yapıştırıldığı Elementor widget'ı | 6:28 | Edit HTML paneline script kodu yapıştırılmış (karede: Edit HTML paneli ve HTML Code alanında script etiketleri) |
| Custom CSS | yok | teknik | yok | Elementor'un özel CSS alanı; sorun giderme CSS'i buraya girilir | 8:57 | Add your own custom CSS alanı görünüyor (karede: Custom CSS paneli: Add your own custom CSS, selector{ ... }) |
| Gumroad | yok | teknik | yok | Hazır Elementor şablonunun indirildiği servis | 1:42 | Gumroad sayfasında şablon indirme ve satın alma (karede: Download Reveal Content On Scroll - Elementor Website Template, I want this! düğmesi) |
| Elementor Pro | yok | teknik | yok | Motion Effects için gerekli sürüm | 8:38 | Sayfada Elementor pro etiketi görünüyor; yorumda Motion Effects için gerektiği yazıyor (karede: lifeonablock.com sayfasında Elementor pro metni) |
| WordPress | yok | teknik | yok | Sitenin çalıştığı CMS | 0:04 | WordPress yönetim çubuğu görünüyor (karede: Üstte WordPress yönetim çubuğu: Customize, Edit with Elementor) |
| Media Library | yok | teknik | yok | WordPress medya kitaplığından görsel seçimi | 7:16 | Insert Media penceresi açık · kanıt: kare (karede: Insert Media, Media Library sekmesi ve Attachment Details) |
| Flexbox | yok | teknik | yok | Kapsayıcıların yön, hizalama ve boşluk düzeni için kullanılan CSS esnek kutu modeli. | 0:33 | Container Layout: Flexbox (karede: Elementor kapsayıcı ayarlarında Layout bölümünde Flexbox ve Min Height alanları görünüyor.) |
| CSS sticky | yok | teknik | yok | Görseli kaydırma sırasında sabit tutan CSS konumlandırma (position: sticky); Elementor'un sticky ayarı bunu uyguluyor. | 5:01 | activate the sticky at the top and toggle on stay in column · kanıt: yok |
## Açıklama bağlantıları
- https://nicolaipalmkvist.com/reveal-code/ — Kod ve sınıf sayfası · aday: hayır · Yazarın kendi kod/kaynak sayfası; izleyicinin kullanacağı araç değil · sınıf: diğer
- https://www.youtube.com/watch?v=s7n9vRFvmM0 — Başka YouTube videosu · aday: hayır · Video bağlantısı, araç/servis değil · sınıf: diğer
- https://be.elementor.com/visit/?bta=216842&nci=5761 — Elementor yönlendirme bağlantısı · aday: evet (Elementor) · Alan adı Elementor aracını adlandırıyor; bta/nci yönlendirme parametresi var · sınıf: affiliate
- https://www.youtube.com/watch?v=LceOy5dnaYI — Tüm şablonlar videosu · aday: hayır · Video bağlantısı, araç değil · sınıf: diğer
- https://lifeonablock.com/live-demo-1/ — Canlı demo sayfası · aday: hayır · Demo site; referans sayfası · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kaydırmada görsel açılma efekti (Scroll reveal, clip-path inset) | Sağ taraftaki görsel her bölümde yukarıdan açılır, yukarı kaydırınca geri kapanır (karede: Mavi ve kahverengi görsel arasında geçiş; görselin yarısı açılmış) | 0:01 | kare |
| Kaydırmayla yumuşak arka plan rengi geçişi (Smooth background color change) | Her bölümde sayfa arka planı yavaşça değişir (lacivert, kahve, yeşil) (karede: '1. Smooth Background change' etiketi, kahverengi arka plan) | 0:15 | kare |
| Yapışkan sağ sütun (Sticky column) | Görsel alanı sabit kalır, metinler normal kayar (karede: Sticky Top ve Stay in Column ayarları) | 5:07 | kare |
| İki sütunlu yerleşim (Two-column Flexbox layout) | Solda metin, sağda görsel; kapsayıcılar yatay yönde (karede: Navigator'da left ve right kapsayıcıları, yan yana başlık ve düğme) | 3:28 | kare |
| Tam ekran yükseklikli bölümler (100vh sections) | Her metin bölümü ekran yüksekliğinde ve ortalı (karede: Min Height 100 vh ayarı, Justify Content ortalı) | 3:28 | kare |
| Yuvarlatılmış köşeli görsel kartı (Border radius 40px) | Görsel 40 piksel köşe yuvarlamalı, min. yükseklik 600px, arka plan olarak kaplar (cover) (karede: CSS: border-radius:40px; height:400px; overflow:hidden; position:relative;) | 8:38 | kare |
| Mutlak konumlandırma (Absolute positioning) | Görsel kapsayıcısı Absolute konumlanır, dikey konum yüzde ile (karede: Position seçeneklerinde Fixed ve Custom positioning uyarısı) | 6:19 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Efekt yalnızca birkaç satır kodla yapılabilir, yeni başlayanlara uygun | açıklama | özellik |
| Üç şey oluyor: değişen arka plan, normal kayan metin, her seferinde açılan görsel | 0:00 | özellik |
| Heading'in 'reveal' sınıfı olması şart, yoksa çalışmaz | 3:50 | öneri |
| Motion Effects için Elementor Pro gerekir; alternatif olarak sticky CSS konabilir | açıklama | özellik |
| Sorun yaşarsan ek CSS (scroll-behavior auto, border-radius) ekle | 8:26 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Efekt tanıtımı | GSAP | Açıklamada GSAP ScrollTrigger efekti |
| kare 0:30 | Elementor düzenleyici | Elementor | Edit Container paneli |
| kare 0:04 | WordPress yönetim çubuğu | WordPress | Edit with Elementor çubuğu |
| kare 0:04 | Rank Math SEO | aday değil: konu dışı | Yönetim çubuğunda görünüyor, kullanılmıyor |
| kare 2:11 | WP Rocket | aday değil: konu dışı | Yönetim çubuğunda, kullanılmıyor |
| kare 1:42 | Gumroad şablon sayfası | Gumroad | Şablon satın alma ve indirme |
| kare 5:23 | cdnjs GSAP script | cdnjs | cdnjs.cloudflare.com script adresi |
| kare 5:23 | ScrollTrigger.defaults | ScrollTrigger | Kod satırı |
| kare 6:13 | gsap.matchMedia | gsap.matchMedia | mediaAnimation = gsap.matchMedia() |
| kare 6:47 | clipPath inset | clip-path inset | gsap.set(photos, { clipPath: 'inset(100% |
| kare 5:07 | Sticky ve Stay in column | Elementor Sticky | Motion Effects paneli |
| kare 6:28 | HTML widget | HTML widget | Edit HTML paneli |
| kare 8:57 | Custom CSS alanı | Custom CSS | Add your own custom CSS |
| kare 7:16 | Medya kitaplığı | Media Library | Insert Media penceresi |
| yorum | Elementor Pro Motion Effects | Elementor Pro | Yorum: Motion Effects için Elementor Pro gerekir |
| açıklama | Elementor yönlendirme bağlantısı | Elementor | be.elementor.com bta parametresi |
| açıklama | nicolaipalmkvist.com/reveal-code | aday değil: konu dışı | Yazarın kod sayfası, araç değil |
| açıklama | lifeonablock.com/live-demo-1 | aday değil: konu dışı | Demo site |
| açıklama | YouTube video bağlantıları | aday değil: konu dışı | Başka video bağlantıları |
| kare 9:12 | Watermelon GSAP sayfası | aday değil: konu dışı | Sonraki video için gösterilen demo sayfası |
| kare 5:39 | Lovethispic.com | aday değil: konu dışı | Görsel kaynağı filigranı |
| kare 5:34 | Border radius | Custom CSS | 40px köşe yuvarlama CSS'de |
| yorum | my-sticky-container CSS | aday değil: konu dışı | Yorumda önerilen alternatif, videoda gösterilmiyor |
| sözlük | Three.js, Claude, Codex, Next.js vb. | aday değil: konu dışı | Videoda kullanılmayan bulanık sözlük eşleşmeleri |
## Kareden okunanlar
- 0:00: webguard.dk/final-result-scrolltrigger-elementor/ adresinde Architect Nicolai sayfası, 01 Projects Making of Swedish Barn House
- 0:15: '1. Smooth Background change' kırmızı ok etiketi
- 1:42: Gumroad: Download Reveal Content On Scroll - Elementor Website Template, Nicolai Palmkvist
- 5:23: GSAP cdnjs script satırları ve ScrollTrigger.defaults({ markers: false })
- 6:47: Kod: details.forEach, ScrollTrigger.create, start: "200 bottom", onToggle, bgColor = colors[i + 1]
- 8:21: const colors = ["#2E4D71", "#ff0010", ...] ikinci renk kırmızıya değiştirildi
- 8:38: CSS: border-radius:40px; height:400px; overflow:hidden; position:relative; scroll-behavior: auto !important;
- 9:12: michellewp.com/gsap-show-video-elementor-2/ Watermelon sayfası
## Belirsizlikler
- Sözlük eşleşmeleri (Three.js, Claude, Next.js, Codex vb.) videoda kullanılmıyor; bulanık ses eşleşmeleri, aday yapılmadı.
- Videoda konuşma sunucusunun çalıştığı yapay zekâ aracı yok.
- Yorumdaki .my-sticky-container CSS çözümü videoda gösterilmiyor, yalnız yorumda.
- Kod satırlarındaki OCR hataları nedeniyle bazı renk kodları tam okunamadı.
- Altyazıda 'Greensock' ve 'Elementor' dışında terminal/kurulum komutu yok.
## Atlanan segment oranı
0/14 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://nicolaipalmkvist.com/reveal-code/ | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=s7n9vRFvmM0 | açıklama | açıklama | hayır |
| https://be.elementor.com/visit/?bta=216842&nci=5761 | açıklama | açıklama | evet |
| https://www.youtube.com/watch?v=LceOy5dnaYI | açıklama | açıklama | hayır |
| https://lifeonablock.com/live-demo-1/ | açıklama | açıklama | hayır |
| https://nicolaipalmkvist.com/?utm_source=youtube&utm_medium=subscription&utm_campaign=lifeonablock-live-demo | açıklama | açıklama | hayır |
| webguard.dk/final-result-scrolltrigger-elementor/ | 0:00 | ekran | hayır |
| michellewp.gumroad.com/l/vdxlqq | 1:45 | ekran | evet |
| https://michellewp.gumroad.com/l/jibhmn | 1:45 | ekran | evet |
| app.gumroad.com/d/7d81337c3133e4e1c51baa2f01536246 | 1:46 | ekran | evet |
| lifeonablock.com/gsap-code-scrolltrigger/ | 2:11 | ekran | hayır |
| https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.0/gsap.min.js | 5:23 | ekran | evet |
| https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.0/ScrollTrigger.min.js | 5:23 | ekran | evet |
| Lovethispic.com | 5:39 | ekran | hayır |
| michellewp.com/gsap-show-video-elementor-2/ | 9:13 | ekran | hayır |
| https://youtu.be/yezd-afdvjc | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=LceOy5dnaYI | açıklama | yorum | hayır |
| https://lifeonablock.com/live-demo-1/ | açıklama | yorum | hayır |
| https://lifeonablock.com | açıklama | açıklama | hayır |
| webguard.dk/wp-admin/post.php?post=1063&action=elementor | 0:37 | ekran | hayır |
| https://pp.gumroad.com/r/7d81337c3133e4e1c51baa2f01536246/product_files | 1:47 | ekran | hayır |
| https://app.gumroad.com/r/7d81337c3133e4e1c51baa2f01536246/product_files?product_file_ids%5B%5D=WWr | 1:48 | ekran | hayır |
| lifeonablock.com/gsap-code-scroltrigger/ | 2:15 | ekran | hayır |
| https://ifeonablock.com/wp-admin/post-new.php | 4:11 | ekran | hayır |
| Lovethispio.com | 5:41 | ekran | hayır |
| https://cdnjs.cloudflare.com/ajax | 6:47 | ekran | evet |
| webguard.dk/reveal-generalprovel | 7:24 | ekran | hayır |
## İş akışı
- 1. adım — Bitmiş sonucu gösterip üç parçayı anlatma: arka plan, metin, görsel — araçlar: Elementor, GSAP, ScrollTrigger
- 2. adım — Hero bölümü hazır sayfada yeni boş kapsayıcıyı ekleme — araçlar: Elementor
- 3. adım — Birinci kapsayıcıyı tam genişlik (%100) yapma, ikinci kapsayıcıyı boxed 1200px ile içine koyma — araçlar: Elementor
- 4. adım — Arka planı lacivert yapıp padding'i kaldırma — araçlar: Elementor, Navigator
- 5. adım — Hazır şablonu indirip içe aktarma seçeneğini gösterme — araçlar: Gumroad, Elementor
- 6. adım — CSS sınıflarını kod sayfasından kopyalayıp kapsayıcılara girme (gallery, left, desktopContent, desktopContentSection) — araçlar: Elementor, lifeonablock.com
- 7. adım — Sol kapsayıcıya %50 genişlik, 100vh bölüm ve içerik ekleme — araçlar: Elementor
- 8. adım — Başlık, metin ve düğme ekleyip başlığa reveal sınıfı verme — araçlar: Elementor
- 9. adım — Sol kapsayıcıyı çoğaltıp sağ yapma, eski sınıfları silme — araçlar: Elementor
- 10. adım — Sağ kapsayıcıda Sticky Top ve Stay in column açma, desktopPhoto sınıfı verme — araçlar: Elementor, Motion Effects
- 11. adım — Görsel kapsayıcısına arka plan görseli, 600px yükseklik, no-repeat, cover, 40px köşe ve Absolute konum verme — araçlar: Elementor, Media Library
- 12. adım — HTML widget'ına GSAP kodunu yapıştırma — araçlar: HTML widget, GSAP, ScrollTrigger
- 13. adım — Bölümleri ve görsel kapsayıcıyı çoğaltıp görselleri değiştirme, güncelleme ve yeni sayfada test etme — araçlar: Elementor
- 14. adım — JavaScript'teki colors dizisinde ikinci rengi kırmızıya değiştirme — araçlar: HTML widget
- 15. adım — Sorun için ek CSS'i ilk ve üçüncü kapsayıcıların Custom CSS alanlarına ekleme — araçlar: Custom CSS, Elementor
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
