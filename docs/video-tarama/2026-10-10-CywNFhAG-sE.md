# Extended Tutorial - On Scroll Video
## Künye
Extended Tutorial - On Scroll Video · Nicolai Palmkvist · süre: 1:58 · en-orig · https://youtu.be/CywNFhAG-sE · şema 2
motor: parti 2026-10-10-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 18956 tk · claude-haiku-5-5: claude-haiku-5-5 · 38704 tk
## Özet
Nicolai Palmkvist, önceki videoda eksik kalan kısmı anlatıyor: Elementor'da kaydırmayla video oynatma efektinin CSS sınıfları nereye eklenir. Yeni bir container (400vh yüksekliğinde, tam genişlik) açılır, ilk CSS sınıfı container'ın Advanced bölümüne, ikinci sınıf self-hosted Video widget'ına eklenir. Ardından HTML widget'ı eklenip kod yapıştırılır. Yayınlayınca ilk denemede çalışmaz çünkü video öğesi üstte, kod en altta olmalıdır. Düzeltilip yeniden yayınlanınca kaydırdıkça video oynar.
## Bölümler
- 0:00 Giriş: CSS sınıflarının nereye ekleneceği
- 0:37 Container oluşturma (400vh, tam genişlik) ve CSS sınıfı ekleme
- 1:00 Video widget'ı ekleme ve ikinci CSS sınıfı
- 1:27 HTML widget'ı ve kodu ekleme
- 1:42 Yayınlama, hata düzeltme ve son test
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Elementor | yok | plugin | yok | WordPress sayfa oluşturucu; container, video ve HTML widget'ları ile efekt kuruluyor. | 0:15 | Edit Container paneli, Structure listesi ve Elementor sekme başlıkları görünüyor. (karede: kanıttan) Edit Container paneli, Structure listesi ve Elementor sekme başlıkları görünüyor. |
| WordPress | yok | teknik | yok | Sitenin çalıştığı CMS; wp-admin üzerinden Elementor düzenleyici açılıyor. | 0:11 | Adres çubuğunda wp-admin/post.php?post=903&action=elementor yazıyor. (karede: kanıttan) Adres çubuğunda wp-admin/post.php?post=903&action=elementor yazıyor. |
| Hostinger | yok | CLI | yok | Test sitesinin barındırıldığı servis (hostingersite.com alan adı). | 0:11 | Adres çubuğunda snow-tarsier-901043.hostingersite.com görünüyor. (karede: kanıttan) Adres çubuğunda snow-tarsier-901043.hostingersite.com görünüyor. |
| Scrolling Code (HTML widget) | yok | teknik | yok | Kaydırmayla video oynatmayı sağlayan, HTML widget'ına yapıştırılan style/script kodu. | 0:18 | Sayfada <style> ile .scrolling-video ve .vs-spacer CSS kuralları ve 'Copy classes' görünüyor. · kanıt: kare (karede: Sayfada <style> ile .scrolling-video ve .vs-spacer CSS kuralları ve 'Copy classes' görünüyor.) |
| scrolling-video-container | yok | teknik | yok | Container'a eklenen CSS sınıfı. | 0:18 | Copy classes altında scrolling-video-container ve scrolling-video satırları görünüyor. · kanıt: kare (karede: Copy classes altında scrolling-video-container ve scrolling-video satırları görünüyor.) |
| scrolling-video | yok | teknik | yok | Video widget'ına eklenen CSS sınıfı. | 0:18 | Copy classes altında ikinci satır scrolling-video yazıyor. (karede: kanıttan) Copy classes altında ikinci satır scrolling-video yazıyor. |
| Video widget self-hosted | yok | teknik | yok | Medya kütüphanesinden kendi barındırılan video seçilen Elementor widget'ı. | 1:03 | Source açılır menüsünde YouTube, Vimeo, Dailymotion, VideoPress seçenekleri görünüyor. · kanıt: kare (karede: Source açılır menüsünde YouTube, Vimeo, Dailymotion, VideoPress seçenekleri görünüyor.) |
| HTML widget | yok | teknik | yok | Kodun yapıştırıldığı Elementor widget'ı. | 1:27 | Widget listesinde HTML widget'ı görünüyor, arama kutusuna yazılmış. (karede: kanıttan) Widget listesinde HTML widget'ı görünüyor, arama kutusuna yazılmış. |
| Kling | yok | teknik | yok | Medya kütüphanesindeki video dosyaları kling adını taşıyor; video seçiliyor. | 1:07 | Insert Media'da kling-1080.mp4, kling-allkey.mp4 gibi dosya adları görünüyor. (karede: kanıttan) Insert Media'da kling-1080.mp4, kling-allkey.mp4 gibi dosya adları görünüyor. |
| CSS | yok | teknik | yok | Container ve videoya sınıf vermek; konum, boyut ve gizleme kuralları için kullanılıyor. | 0:00 | where to add the CSS classes |
## Açıklama bağlantıları
- https://nicolaipalmkvist.com/code-for-aura-video/ — Efekt için CSS sınıfları ve kodun bulunduğu sayfa · aday: hayır · Videonun kodunu barındıran kaynak/referans sayfası; araç ya da servis değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kaydırmayla video oynatma (scroll-driven video, scrubbing) | Sayfa kaydırıldıkça video ileri, yukarı kaydırınca geri oynar. | 1:58 | altyazı |
| Yapışkan konumlandırma (position: sticky) | Kodda sticky konumlu sarmalayıcı video kaydırma sırasında ekranda sabit tutar. (karede: Kodda position: sticky; ve height: 100vh; satırları görünüyor.) | 1:35 | kare |
| Yüksek container (400vh scroll alanı) | Container min yüksekliği 400vh yapılarak kaydırma mesafesi oluşturulur. | 0:39 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Container'ın VH değeri 400 olmalı ve tam genişlik 100 olmalı. | 0:39 | öneri |
| Video öğesi üstte, kod (HTML widget) en altta olmalı; yoksa efekt çalışmaz. | 1:42 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | CSS sınıfları | scrolling-video-container | Container'ın CSS sınıfı olduğunu söylüyor. |
| konuşma 0:00 | Video widget | Video widget self-hosted | Video widget'ı ve Advanced içinde CSS sınıfı. |
| kare 0:15 | Elementor düzenleyici | Elementor | Edit Container paneli. |
| kare 0:11 | wp-admin adresi | WordPress | post.php?post=903&action=elementor |
| kare 0:11 | hostingersite.com | Hostinger | Adres çubuğu alan adı. |
| kare 0:18 | Kod sayfası | Scrolling Code (HTML widget) | <style> kodu görünüyor. |
| açıklama | code-for-aura-video bağlantısı | aday değil: konu dışı | Referans kod sayfası, araç değil. |
| konuşma 1:01 | HTML widget | HTML widget | HTML widget'ı sürükleyip kodu ekliyor. |
| kare 1:07 | kling dosyaları | Kling | Media Library'de kling-1080.mp4. |
| kare 0:00 | yer imi çubuğu (Notion, ChatGPT, Slack, Fiverr, Convertkit, Lummi vb.) | aday değil: konu dışı | Yalnız tarayıcı yer imlerinde, videoda kullanılmıyor. |
| kare 1:03 | YouTube/Vimeo/Dailymotion/VideoPress kaynak seçenekleri | aday değil: başka adayın parçası (Video widget self-hosted) | Source menüsü seçenekleri. [sebep: başka adayın parçası — Video widget — self-hosted] |
| kare 1:43 | WP Rocket, Elementor önizleme çubuğu | aday değil: konu dışı | Yönetim çubuğunda yazıyor, kullanılmıyor. |
| kare 1:30 | Edit with AI / Angie | aday değil: konu dışı | Menüde görünüyor, kullanılmıyor. |
| yorum | yorum verilmedi | aday değil: konu dışı | Pakette yorum yok. |
## Kareden okunanlar
- 0:00: Elementor Edit Video paneli, Advanced sekmesi, Structure: Container > Video, Scrolling Code; araba videosu.
- 0:15: Edit Container Advanced, CSS Classes alanında scrolling-video-conta... yazıyor.
- 0:18: nicomkvist.com/code-for-aura-video sayfasında <style> kodu ve Copy classes: scrolling-video-container, scrolling-video.
- 0:34: Boş Elementor #1697 sayfası, sol panelde Widgets listesi, 'Drag widget here'.
- 0:39: Edit Container Layout: Flexbox, Boxed, Min Height, 'To achieve full height Container use 100vh'.
- 1:03: Video Placeholder, Source YouTube, Link alanı, Video Options.
- 1:07: Insert Media, Media Library 19 öğe, kling dosyaları.
- 1:27: Widget listesi: Heading, Image, Divider, HTML, Shortcode, Menu Anchor vb.; araba videosu yüklenmiş.
## Belirsizlikler
- Bu paketin gösterdiği tam kod (script kısmı) okunamıyor; yalnız style bölümü görünüyor.
- Sözlük eşleşmeleri (Clash Display, Claude Code, Codex, Descript, Framer Motion, Inter vb.) yer imi çubuğu veya bulanık sesten geliyor; videoda kullanılmıyor, aday yapılmadı.
- Kling videoların üretim aracı mı yoksa yalnız dosya adı mı olduğu belli değil.
- WordPress.org bağlantılı sayfa olarak listelenmiş ama ekranda doğrudan URL görünmüyor.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://nicolaipalmkvist.com/code-for-aura-video/ | açıklama | açıklama | hayır |
| snow-tarsier-901043.hostingersite.com/wp-admin/post.php?post=903&action=elementor | 0:00 | ekran | hayır |
| nicomkvist.com/code-for-aura-video/ | 0:18 | ekran | hayır |
| snow-tarsier-901043.hostingersite.com/wp-admin/post.php?post=1697&action=elementor | 0:37 | ekran | hayır |
| www.youtube.com/watch?v=XHOmBV | 1:03 | ekran | hayır |
| snow-tarsier-901043.hostingersite.com/elementor-1697/ | 1:43 | ekran | hayır |
| https://nicolaipalmkvist.com | açıklama | açıklama | hayır |
| https://wordpress.org | açıklama | açıklama | evet |
| snow-tarsier-901043.hostingersite.com | 1:43 | ekran | evet |
| https://www.youtube.com/watch?v=XHOmBV | 1:03 | ekran | hayır |
## İş akışı
- 1. adım — Önceki videodaki hazır sayfa (Scrolling Effect) açılıp container ve video CSS sınıfları gösterilir — araçlar: Elementor, WordPress
- 2. adım — Kod sayfasından CSS sınıfları ve kod incelenir — araçlar: Scrolling Code (HTML widget)
- 3. adım — Yeni boş sayfada container oluşturulur, tam genişlik ve 400vh ayarlanır — araçlar: Elementor
- 4. adım — Container'ın Advanced bölümüne scrolling-video-container sınıfı eklenir — araçlar: Elementor, scrolling-video-container
- 5. adım — Video widget'ı sürüklenir ve kaynak self-hosted seçilir — araçlar: Elementor, Video widget self-hosted
- 6. adım — Medya kütüphanesinden video seçilir — araçlar: WordPress, Kling
- 7. adım — Video widget'ının Advanced bölümüne scrolling-video sınıfı eklenir — araçlar: Elementor, scrolling-video
- 8. adım — HTML widget'ı eklenir ve kod yapıştırılır — araçlar: HTML widget, Scrolling Code (HTML widget)
- 9. adım — Sayfa yayınlanıp önizlenir; çalışmadığı görülür — araçlar: Elementor
- 10. adım — Sıra düzeltilir (video üstte, kod altta) ve tekrar yayınlanır — araçlar: Elementor, HTML widget
- 11. adım — Sayfa yenilenip kaydırma testi yapılır — araçlar: Hostinger
## Promptlar
- yok
