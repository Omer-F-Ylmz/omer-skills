# Sadece 1 günde para bile kazandırabilecek bir prompt sitesi kurdum!
## Künye
Sadece 1 günde para bile kazandırabilecek bir prompt sitesi kurdum! · tahiryildiz · süre: 1:34 · ? · https://www.instagram.com/reel/DOq3CxcCO-T/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-22 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 39781 tk · claude-haiku-5-5: claude-haiku-5-5 · 102653 tk
## Özet
Tahir Yıldız, yazılımcı olmayan bir vibe coder olarak prompt paylaşımlarını tek yerde toplayan Pinterest tarzı bir galeri sitesi kurdu. Fotoğrafa tıklayınca prompt açılıyor ve kopyalanabiliyor. Dört aşama: Bolt ile ilk tasarım, GitHub üzerinden Cursor'a geçip geliştirme, görselleri Sirv'de barındırma, siteyi Netlify'da ücretsiz yayınlama. Açıklamada toplam süre 3-4 saat olarak veriliyor.
## Bölümler
- 0:00 Giriş: prompt sitesi fikri ve sorun
- 0:34 1- Bolt ile ilk tasarım
- 0:49 2- Cursor'a geçiş (GitHub ile)
- 0:57 3- Sirv ile görsel barındırma
- 1:07 4- Netlify ile yayına alma
- 1:18 Kapanış: site linki profilde
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Bolt | yok | plugin | yok | İlk promptla Pinterest tarzı galeri tasarımını tek seferde üreten yapay zekâ site oluşturucu | 0:39 | Bolt'a derdimi anlatan ilk promptumu verdikten sonra tek seferde kafamdaki tasarımı çıkarabildi. (karede: kanıttan) Bolt'a derdimi anlatan ilk promptumu verdikten sonra tek seferde kafamdaki tasarımı çıkarabildi. |
| Cursor | yok | CLI | yok | Projenin GitHub ile alınıp geliştirildiği yapay zekâlı kod editörü | 0:50 | GitHub bağlantısı ile birlikte Curser'a aldım. (karede: kanıttan) GitHub bağlantısı ile birlikte Curser'a aldım. |
| GitHub | yok | iş akışı | yok | Bolt projesini Cursor'a aktarmak ve Netlify'a bağlamak için kullanılan bağlantı | 0:50 | GitHub bağlantısı ile birlikte Curser'a aldım. |
| Sirv | yok | CLI | yok | Fotoğrafları barındıran görsel CDN servisi; Cursor'dan API ile bağlandı | 0:57 | Serve diye bir yer buldum. Curser'a serve'e bağlanması için bir prompt yazdım |
| Netlify | yok | CLI | yok | Siteyi ücretsiz yayınlayan hosting servisi | 1:12 | Bunun için de yine ücretsiz olan Netlify'ı kullandım. (karede: kanıttan) Bunun için de yine ücretsiz olan Netlify'ı kullandım. |
| Netlify Drop | yok | iş akışı | yok | Proje klasörünü sürükle-bırak ile yükleyip geçici bağlantı veren Netlify sayfası | 1:15 | Ekranda app.netlify.com/drop sayfası ve 'Drag & drop. It's online.' görünüyor. (karede: kanıttan) Ekranda app.netlify.com/drop sayfası ve 'Drag & drop. It's online.' görünüyor. |
| Bolt Hosting | yok | iş akışı | yok | Bolt içinde siteyi bolt.host adresinde yayınlayan seçenek | 0:40 | Ekranda 'Publish to Bolt Hosting' ve yayın başarılı mesajı görünüyor. (karede: kanıttan) Ekranda 'Publish to Bolt Hosting' ve yayın başarılı mesajı görünüyor. |
| claude-4-sonnet | yok | prompt | yok | Cursor'daki sohbet panelinde seçili görünen model | 0:54 | Ekran metninde 'claude-4-sonnet' yazıyor. (karede: kanıttan) Ekran metninde 'claude-4-sonnet' yazıyor. |
| npm | yok | CLI | yok | Node.js paket yöneticisi; projeyi 'npm run dev' komutuyla yerelde çalıştırmak için gösterildi. | 0:39 | npm run dev (karede: kanıttan) npm run dev |
| Bolt'ta ilk galeri tasarımı | yok | prompt | yok | Fotoğraflı bir web sayfası istendi: Pinterest benzeri galeri, fotoğrafa tıklayınca prompt gösterilsin, yükleme sistemi olsun, masonry düzen kullanılsın. | 0:37 | kaynak: kare |
| Silme özelliği | yok | prompt | yok | Galeriye kullanıcıların istemediği görselleri silebilmesi için silme seçeneği eklenmesi istendi. | 0:40 | kaynak: kare |
| Cursor'da admin panel | yok | prompt | yok | Admin panelde fotoğraflar için ekleme, çıkarma ve yer değiştirme özellikleri istenir. | 0:56 | kaynak: kare |
| Sirv entegrasyonu | yok | prompt | yok | Cursor'a Sirv'e bağlanması ve API ile fotoğrafları oraya göndermesi için prompt yazıldı (metni gösterilmedi). | 0:57 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Pinterest tarzı duvar ızgarası (Masonry grid layout) | Fotoğraflar mobilde 2, büyük ekranda 6 sütunlu uyarlanabilir ızgarada dizilir (karede: Bolt sohbetinde 'Pinterest-style masonry grid layout' ve '2 columns on mobile to 6 columns' satırları) | 0:39 | kare |
| Tıklayınca prompt gösteren pencere (Click-to-reveal modal overlay) | Fotoğrafa tıklayınca prompt zarif bir modal içinde açılır (karede: Bolt sohbetinde 'Click-to-reveal prompts in elegant modal overlays' ve ImageModal.tsx dosyası) | 0:39 | kare |
| 3B kart çevirme animasyonu (3D flip card animation) | Kartlara tıklanınca 3B çevrilerek prompt gösterilir (karede: Bolt sohbetinde 'Smooth 3D flip animation' satırı) | 0:39 | kare |
| 9:16 dikey görsel oranı (Portrait aspect ratio) | Örnek görseller 9:16 oranlı URL'lerle güncellendi (karede: Bolt sohbetinde 'Updated all sample images to use 9:16 aspect ratio URLs') | 0:39 | kare |
| Boş durum mesajı (Empty state) | Galeri boşken 'No images yet' ve yükleme yönlendirmesi gösterilir (karede: Önizlemede ortada 'No images yet' ve 'Gallery is empty. Upload some images via the admin panel!') | 0:39 | kare |
| Yönetim paneli ile yükleme ve silme (Admin panel) | Admin panelde fotoğraf ekleme, çıkarma ve yer değiştirme istenir | 0:56 | açıklama |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm run dev | Projeyi yerel geliştirme sunucusunda çalıştırır (karede: Bolt terminalinde 'npm run dev' yazıyor) | 0:39 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bolt ilk promptla tasarımı tek seferde çıkardı. | 0:34 | özellik |
| Ücretsiz Bolt üyeliği yüzünden geliştirme Cursor'da sürdürüldü. | 0:49 | karşılaştırma |
| Cursor daha esnek çalışma imkânı sağlar. | 0:55 | karşılaştırma |
| Netlify'a gönderilen site 1 dakika içinde hazırdı. | 1:12 | sayısal |
| Toplam süre açıklamada 3-4 saat; videoda 2-3 saatte yapılabileceği söyleniyor. | 1:18 | sayısal |
| Netlify ile site tamamen ücretsiz barındırıldı. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Prompt sitesi fikri | aday değil: konu dışı | Prompt sitesi kurdum |
| konuşma 0:34 | Bolt | Bolt | Önce Bolt ile başladım |
| konuşma 0:49 | Cursor ('Curser') | Cursor | Curser'a devam ettirmek istedim |
| konuşma 0:50 | GitHub | GitHub | GitHub bağlantısı ile birlikte |
| konuşma 0:52 | ChatGPT | aday değil: genel kavram | Cursor ChatGPT'yi içinde kullanabildiğiniz uygulama diye anlatıldı |
| konuşma 0:57 | Sirv ('Serve') | Sirv | Serve diye bir yer buldum |
| konuşma 1:07 | Netlify | Netlify | Ücretsiz olan Netlify'ı kullandım |
| kare 0:39 | Masonry grid layout | aday değil: genel kavram | Bolt sohbetinde masonry grid satırı |
| kare 0:39 | ImageModal.tsx, MasonryGrid.tsx, sampleImages.ts, App.tsx | aday değil: başka adayın parçası (Bolt) | Bolt'un oluşturduğu dosyalar |
| kare 0:39 | npm run dev | aday değil: genel kavram | Bolt terminalinde komut |
| kare 0:39 | 3D flip animation | aday değil: genel kavram | Bolt sohbetinde animasyon satırı |
| kare 0:40 | Bolt Hosting | Bolt Hosting | Publish to Bolt Hosting |
| kare 0:40 | pinterest-style-gall-v800.bolt.host | aday değil: başka adayın parçası (Bolt Hosting) | Bolt'un verdiği yayın adresi |
| kare 0:50 | Cursor dosya ağacı (netlify.toml, README.md, CLAUDE.md vb.) | aday değil: başka adayın parçası (Cursor) | Editör dosya listesi |
| kare 0:50 | cloudinary, GCS_SETUP.md | aday değil: başka adayın parçası (Cursor) | Yalnız dosya adı, anlatılmadı |
| ekran 0:49 | Stripe, Supabase | aday değil: konu dışı | Bolt entegrasyon menüsünde görünüyor |
| ekran 0:54 | claude-4-sonnet | claude-4-sonnet | Cursor model seçimi |
| ekran 0:13 | Ask Gemini / Make my own | aday değil: konu dışı | Örnek görsel sayfasında görünen arayüz |
| kare 1:12 | Netlify Projects paneli | Netlify | yildiztahir ekibi projeleri |
| ekran 1:15 | Netlify Drop | Netlify Drop | app.netlify.com/drop sayfası |
| ekran 1:08 | Astro v5 | aday değil: konu dışı | Netlify sayfasında reklam öğesi |
| ekran 1:02 | Sirv fiyat sayfası | Sirv | sirv.com/pricing sayfası |
| açıklama | #Vibecoding #cursor #bolt #reklamdegil | aday değil: genel kavram | Etiketler; reklam olmadığını belirtiyor |
| linkli sayfa | bolt.new | Bolt | Açıklamadaki bağlantılı sayfa |
| linkli sayfa | my.sirv.com signup | Sirv | Açıklamadaki bağlantılı sayfa |
| linkli sayfa | Netlify docs sayfaları | Netlify | CLI, AI Gateway ve primitives dokümanları |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:39: Bolt arayüzü: Pinterest-Style Gallery with Image Upload önizlemesi, 'No images yet', src/components/ImageModal.tsx ve MasonryGrid.tsx oluşturma adımları, 9:16 tasarım notları; altta 'seferde' altyazısı.
- 0:50: Cursor editörü: proje dosya ağacı (netlify.toml, README.md, CLAUDE.md, DEPLOYMENT.md vb.), sağda sohbet paneli; '2- Cursor' başlığı ve 'çok' altyazısı.
- 1:12: Netlify paneli: yildiztahir ekibi Projects sayfası, sol menüde Builds, Extensions, Domains, Members; '4 Netl' başlığı ve 'de' altyazısı.
## Belirsizlikler
- Yorumlar girişsiz alınamadı; yorumlardan ek bilgi yok.
- Açıklamadaki 'Link profilimde' sitesi videoda tahiryildiz.netlify.app olarak görünüyor (1:29), ama kare dışı OCR'dan.
- Süre tutarsız: başlıkta 1 gün, açıklamada 3-4 saat, konuşmada 3 saat ve 2-3 saat.
- Altyazıdaki 'Serve' ve 'Curser' büyük olasılıkla Sirv ve Cursor; ekranda Sirv ve Cursor yazıyor.
- 0:13 civarında 'Ask Gemini' ve 'Make my own' görünüyor; Gemini'nin videoda kullanıldığı net değil.
- Cursor dosya ağacında cloudinary, GCS_SETUP.md ve gallery-api.php dosyaları var; kullanıldıkları anlatılmadı.
- Bolt'ta Stripe, Supabase, GitHub entegrasyon menüsü görünüyor; kullanılmadı.
- claude-4-sonnet (0:54) ve bazı OCR öğeleri ekli karelerde değil, yalnız OCR metninden.
- ChatGPT yalnız benzetme olarak anıldı, araç olarak kullanılmadı.
- Açıklama bağlantılarındaki youtube.com bağlantısı videoda geçmiyor.
- EKSİK: rapor (süre dışı zaman: 9:16 > 1:34)
- EKSİK: rapor (süre dışı zaman: 9:16 > 1:34)
- EKSİK: rapor (süre dışı zaman: 9:16 > 1:34)
- EKSİK: rapor (süre dışı zaman: 9:16 > 1:34)
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://bolt.new | açıklama | açıklama | evet |
| https://pinterest-style-gall-v800.bolt.host | 0:46 | ekran | hayır |
| https://my.sirv.com/#/signup | açıklama | açıklama | evet |
| https://sirv.com | 0:57 | ekran | evet |
| https://sirv.com/pricing/ | 1:02 | ekran | evet |
| https://my.sirv.com/#/signin | 1:06 | ekran | evet |
| https://www.netlify.com | 1:09 | ekran | evet |
| https://app.netlify.com/teams/yildiztahir/projects | 1:12 | ekran | evet |
| https://app.netlify.com/drop | 1:15 | ekran | evet |
| https://youtube.com/watch?v=Evdv_HSFHBk | açıklama | açıklama | hayır |
| https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli | açıklama | açıklama | evet |
| https://www.netlify.com/docs/ai-gateway | açıklama | açıklama | evet |
| https://www.netlify.com/docs/primitives | açıklama | açıklama | evet |
| tahiryildiz.netlify.app | 1:29 | ekran | hayır |
| https://bolt.new/-/sb1-3x2udjvg | 0:39 | ekran | evet |
| https://pinterest-style-gall-v600.bolt.host | 0:40 | ekran | hayır |
## İş akışı
- 1. adım — Prompt paylaşımlarının dağınıklığı sorun olarak belirlendi, tek yerde toplayan site fikri kuruldu — araçlar: yok
- 2. adım — Bolt'ta ilk prompt yazıldı, Pinterest tarzı galeri tek seferde üretildi — araçlar: Bolt
- 3. adım — Bolt önizlemesinde galeri ve prompt penceresi kontrol edildi, silme özelliği istendi — araçlar: Bolt
- 4. adım — Site Bolt Hosting'e yayınlandı — araçlar: Bolt Hosting
- 5. adım — Ücretsiz üyelik sınırı nedeniyle proje GitHub bağlantısıyla Cursor'a alındı — araçlar: GitHub, Cursor
- 6. adım — Cursor'da admin panel istendi, proje yerelde çalıştırıldı — araçlar: Cursor, claude-4-sonnet
- 7. adım — Fotoğrafların barınması için Sirv bulundu — araçlar: Sirv
- 8. adım — Cursor'a Sirv bağlantısı için prompt yazıldı, API ile fotoğraflar gönderildi — araçlar: Cursor, Sirv
- 9. adım — Siteyi barındırmak için Netlify hesabı ve proje paneli açıldı — araçlar: Netlify
- 10. adım — Cursor'daki dosyalar Netlify'a gönderildi, site 1 dakikada hazır oldu — araçlar: Netlify, Netlify Drop, Cursor
- 11. adım — Yayınlanan site linki profile eklendi — araçlar: Netlify
## Promptlar
- Bolt'ta ilk galeri tasarımı — Fotoğraflı bir web sayfası istendi: Pinterest benzeri galeri, fotoğrafa tıklayınca prompt gösterilsin, yükleme sistemi olsun, masonry düzen kullanılsın.
- Silme özelliği — Galeriye kullanıcıların istemediği görselleri silebilmesi için silme seçeneği eklenmesi istendi.
- Cursor'da admin panel — Admin panelde fotoğraflar için ekleme, çıkarma ve yer değiştirme özellikleri istenir.
- Sirv entegrasyonu — Cursor'a Sirv'e bağlanması ve API ile fotoğrafları oraya göndermesi için prompt yazıldı (metni gösterilmedi).
