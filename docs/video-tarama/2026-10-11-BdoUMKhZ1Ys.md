# Build a Complete RPG UI Set with PixelLab AI
## Künye
Build a Complete RPG UI Set with PixelLab AI · PixelLab · süre: 4:45 · en-orig · https://youtu.be/BdoUMKhZ1Ys · şema 2
motor: parti 2026-10-11-uzun-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 48073 tk · claude-haiku-5-5: claude-haiku-5-5 · 73943 tk
## Özet
PixelLab AI'nin UI Creator aracıyla bir oyun için eksiksiz piksel sanat arayüz seti hazırlanıyor. Önce şekillerle yerleşim kuruluyor, tek cümlelik renk/malzeme tarifiyle üretim yapılıyor, sonra elemanlara bölünüyor, 9-slice işaretleniyor, Pixelorama editöründe temizleniyor, boş sağlık çubuğu özel durum (state) olarak üretiliyor ve dolu hali elle düzenleniyor. Sonuç oyunda test ediliyor. Envanter slotları için UI aracı yerine 'Create from style reference' aracı, bir düğme stil referansı ve arka plan kaldırma ile kullanılıyor.
## Bölümler
- 0:00 Giriş: oyunda arayüz yok, UI aracına gidiş
- 0:50 UI Creator'da şablon yerleşimi ve çıktı boyutu
- 1:07 Stil tarifi ve arayüz üretimi
- 1:26 Elemanlara bölme (Split into elements)
- 2:04 9-slice işaretleme
- 2:25 Pixelorama'da temizleme ve galeriye kaydetme
- 2:41 Özel durum (state) ile boş sağlık çubuğu
- 3:14 Dolu sağlık çubuğu, gün/gece çubuğu ve oyunda test
- 3:45 Create from style reference ile envanter slotları
- 4:18 Sonuç ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| PixelLab | yok | iş akışı | yok | Piksel sanat oyun varlıkları üreten yapay zekâ servisi; videonun ana aracı | 0:19 | Ana sayfa PixelLab menüsü: Docs, API, Editor, Creator, UI, Maps (karede: kanıttan) Ana sayfa PixelLab menüsü: Docs, API, Editor, Creator, UI, Maps |
| UI Creator | yok | iş akışı | yok | Şekil yerleştirip tarifle eşleşen piksel UI üreten araç | 0:26 | Create UI sayfası, Output size ve + Button, + Health bar düğmeleri (karede: kanıttan) Create UI sayfası, Output size ve + Button, + Health bar düğmeleri |
| Split into elements | yok | teknik | yok | Üretilen şablonu tek tek eleman görsellerine ayırır | 1:34 | Split preview 9 pieces, Split into 9 elements düğmesi (karede: kanıttan) Split preview 9 pieces, Split into 9 elements düğmesi |
| 9-slice | yok | teknik | yok | Köşeleri bozmadan paneli yeniden boyutlandırmak için kılavuz işaretleme | 2:07 | 9-slice · Panel penceresi, L 37 R 37 T 37 B 37, Save 9-slice (karede: kanıttan) 9-slice · Panel penceresi, L 37 R 37 T 37 B 37, Save 9-slice |
| Add states | yok | teknik | yok | Elemanlar için hover, pressed gibi hazır ya da özel durum görselleri üretir | 2:46 | Add states penceresi: Hover, Pressed, Disabled, Selected, Locked, Add custom state · kanıt: kare (karede: Add states penceresi: Hover, Pressed, Disabled, Selected, Locked, Add custom state) |
| Pixelorama | yok | CLI | yok | PixelLab içine gömülü piksel sanat editörü; temizlik ve doldurma için kullanıldı | 2:28 | Başlık 'PixelLab Pixelorama', Pencil, Bucket, Save to Gallery (karede: kanıttan) Başlık 'PixelLab Pixelorama', Pencil, Bucket, Save to Gallery |
| Create from style reference | yok | iş akışı | yok | Referans görselin stilinde yeni öğeler üreten Creator aracı (Pro) | 4:06 | Tool: Create from style reference PRO, Style reference images · kanıt: kare (karede: Tool: Create from style reference PRO, Style reference images) |
| Remove background | yok | teknik | yok | Üretilen karelerden arka planı kaldıran seçenek | 4:18 | Remove background onay kutusu işaretli (karede: kanıttan) Remove background onay kutusu işaretli |
| Gallery | yok | iş akışı | yok | Üretimlerin ve kaydedilen düzenlemelerin saklandığı PixelLab galerisi | 2:25 | Pixelorama'da Save to Gallery ve Editing image from gallery (karede: kanıttan) Pixelorama'da Save to Gallery ve Editing image from gallery |
| Yerleşim şablonuna renk ve malzeme stili verme | yok | prompt | yok | Derin kömür grisi arduvaz, soğuk demir çerçeve ve keskin ocak ateşi turuncusu vurgularıyla piksel sanat arayüz seti istendi. | 1:07 | kaynak: kare |
| Sağlık çubuğu için boş durum görseli | yok | prompt | yok | Sağlık çubuğunun boş halini özel durum olarak üret; durum adı 'empty health bar'. | 2:52 | kaynak: kare |
| Envanter slotları setini düğme stilinde üretme | yok | prompt | yok | Kılıç, kalkan, yay ve ok, bomba, kırmızı ve yeşil iksir ile diğer RPG macera eşyaları için envanter slotu üret; arka plan kaldırma açık. | 4:06 | kaynak: kare |
## Açıklama bağlantıları
- https://pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=BdoUMKhZ1Ys — PixelLab ana sayfası · aday: evet (PixelLab) · Videoda kullanılan servis; izleyici kullanabilir. utm parametreleri yalnız kampanya izleme, yönlendirme kodu yok · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Gün/gece çevrimi karartma kaplaması (day-night cycle overlay) | Oyun sahnesi zamana göre aydınlıktan geceye geçiyor, meşaleler çevresi aydınlık kalıyor (karede: (karede OCR) 22:20 Night day 1.4x auto ON WASD/ArrousS Move SPACE: Suord SHIFT: Run 0: Item E: Interact ENTER: Inventory [ ] day speed N night D dayC auto-cycle H hide UI) | 0:14 | kare |
| Sol üst gün/gece göstergesi (HUD meter) | Güneş ve ay simgeli çubuk gün saatini gösteriyor (karede: (karede OCR) Q 100/100 PLAYER STATUS LEVEL: 05 18 ATTACK: 12 DEFENSE: RUPEES: 170 10 BOMBS: ARROWS: 30 PRESS U OR CLICK STATS TO CLOSE) | 3:45 | kare |
| Üst orta sağlık çubuğu (health bar HUD) | Kırmızı dolgulu çubuk ve altında 100/100 yazısı (karede: (karede OCR) Q 100/100 PLAYER STATUS LEVEL: 05 18 ATTACK: 12 DEFENSE: RUPEES: 170 10 BOMBS: ARROWS: 30 PRESS U OR CLICK STATS TO CLOSE) | 3:45 | kare |
| Sağ üst ikon düğme sırası (icon button row) | Envanter, harita, istatistik, görev ve yardım düğmeleri (karede: (karede OCR) Q 100/100 PLAYER STATUS LEVEL: 05 18 ATTACK: 12 DEFENSE: RUPEES: 170 10 BOMBS: ARROWS: 30 PRESS U OR CLICK STATS TO CLOSE) | 3:45 | kare |
| Ortada açılır panel penceresi (modal panel) | Player Status paneli istatistik listesi ve kaydırma çubuğu ile (karede: (karede OCR) Q 100/100 PLAYER STATUS LEVEL: 05 18 ATTACK: 12 DEFENSE: RUPEES: 170 10 BOMBS: ARROWS: 30 PRESS U OR CLICK STATS TO CLOSE) | 3:45 | kare |
| Izgara envanter yerleşimi (inventory grid) | Kılıç, kalkan, yay, bomba ve iksir slotları 4x2 ızgarada (karede: (karede OCR) s Q 100/100 SUBSCRIBE /b INVENTORY PRESS I OR CLICK INVENTORY TO CLOSE SHARE LIKE) | 4:43 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| UI aracı düzenleme, bölme, 9-slice ve durum üretimini tek yerde sunuyor | 1:07 | özellik |
| Envanter slotları için stil referansı aracı, büyük bir yerleşim düşünmeden aynı stilde çok seçenek verdiği için daha iyi | 3:14 | öneri |
| Tek eleman için tek özel durum üretimi 25 generation maliyetli | 2:58 | sayısal |
| Stil referansı aracı 25 generation harcıyor | 4:06 | sayısal |
| Dolu sağlık çubuğunu ayrı durum olarak üretmek yerine elle doldurmak daha kolay | 3:14 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | PixelLab kanalı ve pixellab.ai | PixelLab | Welcome back to the Pixelab channel |
| konuşma 0:00 | UI aracı | UI Creator | click the UI tab, which will take me to the new UI tool |
| konuşma 1:07 | Elemanlara bölme | Split into elements | click split into elements |
| konuşma 2:04 | Dokuz dilim | 9-slice | So, let's try the nine slice |
| konuşma 2:10 | Durumlar | Add states | create states for each asset |
| kare 2:28 | Pixelorama editörü | Pixelorama | Başlık 'PixelLab Pixelorama' |
| konuşma 3:14 | Stil referansı aracı | Create from style reference | I think using the style reference tool is better |
| konuşma 4:16 | Arka plan kaldırma | Remove background | with remove background enabled |
| kare 2:25 | Galeriye kaydetme | Gallery | Save to Gallery düğmesi |
| kare 2:28 | Inpaint, Rotate, Animate, Map menü öğeleri | aday değil: konu dışı | Pixelorama sol menüde listeleniyor, kullanılmıyor |
| kare 4:04 | Create S-XL image, Create tiles vb. araç listesi | aday değil: konu dışı | Select Tool penceresinde yalnız listede |
| kare 5:00 | Oyun sahnesi ve karakter | aday değil: konu dışı | Test için gösterilen demo oyun |
| kare 0:19 | Maps sayfası | aday değil: konu dışı | Tarayıcı önerisinde Map Editor listesi |
| kare 0:19 | Characters sayfası | aday değil: konu dışı | Tarayıcı önerisinde Characters listesi |
| kare 0:20 | Discord | aday değil: konu dışı | Ana sayfada Join Discord düğmesi |
| kare 4:43 | Abone ol, beğen, paylaş animasyonu | aday değil: konu dışı | Kapanışta Subscribe, Like, Share düğmeleri |
| açıklama | pixellab.ai ana sayfa bağlantısı | PixelLab | Açıklamadaki utm parametreli bağlantı |
| linkli sayfa | docs/tools/create-ui-elements-pro | UI Creator | UI elemanı üretim aracı belge sayfası |
| linkli sayfa | docs/tools/consistent-style | Create from style reference | Tutarlı stil aracı belge sayfası |
| linkli sayfa | docs/tools/animate-with-text-pro | aday değil: konu dışı | Videoda kullanılmayan animasyon aracı sayfası |
| linkli sayfa | docs/tools/rotate | aday değil: konu dışı | Videoda kullanılmayan döndürme aracı sayfası |
| linkli sayfa | docs/tools/create-image-flux | aday değil: konu dışı | Videoda kullanılmayan görsel üretim aracı sayfası |
| linkli sayfa | docs/tools/create-map | aday değil: konu dışı | Videoda kullanılmayan harita aracı sayfası |
| linkli sayfa | docs/getting-started | aday değil: genel kavram | Başlangıç belgesi |
| linkli sayfa | docs/ways-to-use-pixellab | aday değil: genel kavram | Kullanım yolları belgesi |
| linkli sayfa | Diğer PixelLab YouTube videoları (youtu.be bağlantıları) | aday değil: konu dışı | Açıklamadaki diğer video bağlantıları |
| yorum | Unity ve sağlık çubuğu etkileşimi isteği | aday değil: konu dışı | Yorumda Unity ile sağlık çubuğu eğitimi istenmiş |
| yorum | İskelet aracı sorusu | aday değil: konu dışı | Yorumda iskelet aracı eğitimi istenmiş |
## Kareden okunanlar
- 1:24: Galeride 'Generating... 40%' kartı, tarif 'deep charcoal slate, framed by cool iron...'
- 1:34: Split preview 9 pieces; Day/Night meter, Health bar, Panel, Avatar frame kutuları
- 2:07: 9-slice Panel: L 37 R 37 T 37 B 37, 148x148 px
- 2:58: 1 element × 1 state = 1 new state image (258×258px), 25 generations
- 4:06: Create from style reference PRO, 25 generations, en çok 8 referans görsel
- 4:18: Referans 39x39px, çıktı 39x39, 8x8 (64 kare), Remove background işaretli
## Belirsizlikler
- Açıklamadaki utm parametreli bağlantı kampanya izleme; yönlendirme/indirim kodu olmadığı için 'diğer' sınıfı verildi, affiliate olabilir.
- Sözlük eşleşmeleri (Claude Sonnet, Canva, Stripe, Next.js vb.) altyazıda bulanık eşleşme; videoda kullanıldıkları görülmedi, aday yapılmadı.
- Tarayıcıdaki 'Chat' düğmesi ve 'Add tabs or files' kutusunun hangi yapay zekâ aracına ait olduğu belli değil.
- Pixelorama menüsündeki Inpaint, Rotate, Animate, Map, Reduce Colors, Try On, Resize, Multi-Image Edit yalnız menüde görünüyor, kullanılmıyor.
- Creator araç seçim menüsündeki diğer araçlar (Create S-XL image, Create tiles vb.) yalnız listede.
- Oyun sahnesi ve diğer oyun detayları (meşale, karakter) PixelLab ile yapıldığı belirtilmediği için aday yapılmadı.
- Pixel Art Correction (new) menüde görünüyor; 4:20 civarında 'Correcting pixels' yazısı geçse de kullanımı net değil.
- Durum üretiminde yazan 'empty health bar 215×35' boyutu kareden okundu, çıktı görseli 258×258 olarak da anılıyor.
- EKSİK: rapor (süre dışı zaman: 22:20 > 4:45)
- EKSİK: rapor (süre dışı zaman: 5:00 > 4:45)
## Atlanan segment oranı
0/5 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=BdoUMKhZ1Ys | açıklama | açıklama | evet |
| pixelab.ai | 0:00 | ses | evet |
| pixellab.ai | 0:19 | ekran | evet |
| pixellab.ai/maps | 0:19 | ekran | hayır |
| pixellab.ai/create-character | 0:19 | ekran | hayır |
| pixellab.ai/create-ui | 0:19 | ekran | evet |
| pixellab.ai/docs | 0:19 | ekran | hayır |
| https://pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/rotate | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-map | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/ways-to-use-pixellab | açıklama | açıklama | hayır |
| https://youtu.be/Iaxk_8ftJ5s | açıklama | açıklama | hayır |
| https://youtu.be/r8ySiSRRvz4 | açıklama | açıklama | hayır |
| https://youtu.be/9eAlZlQmZBg | açıklama | açıklama | hayır |
| https://youtu.be/oCJWxfEwX-o | açıklama | açıklama | hayır |
| https://youtu.be/sE1s5ZYfxqk | açıklama | açıklama | hayır |
| https://youtu.be/fvPmuk-usgw | açıklama | açıklama | hayır |
| https://youtu.be/BdoUMKhZ1Ys | açıklama | açıklama | hayır |
| https://youtu.be/Hhx9QZwYoZY | açıklama | açıklama | hayır |
| https://youtu.be/moCpjMOOBGk | açıklama | açıklama | hayır |
| https://youtu.be/j2bE9gq914U | açıklama | açıklama | hayır |
| https://youtu.be/zghUW8fGqsM | açıklama | açıklama | hayır |
| https://youtu.be/qVDkp1baJkU | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Oyunun arayüzsüz haliyle gün/gece sahnesi gösterilir — araçlar: PixelLab
- 2. adım — pixellab.ai açılır ve UI sekmesinden Create ile yeni UI başlatılır — araçlar: PixelLab, UI Creator
- 3. adım — Sağ üstte çıktı boyutu 344x192 seçilir, düğme, sağlık çubuğu, panel ve avatar çerçevesi şekilleri yerleştirilip yeniden adlandırılır — araçlar: UI Creator
- 4. adım — Stil tarifi yazılıp Generate UI ile üretim yapılır — araçlar: UI Creator
- 5. adım — Üretilen şablon açılıp Split into elements ile 9 parçaya bölünür — araçlar: Split into elements
- 6. adım — Panel için 9-slice kılavuzları işaretlenip kaydedilir — araçlar: 9-slice
- 7. adım — Sağlık çubuğu Edit ile Pixelorama'da açılıp başıboş pikseller temizlenir, galeriye kaydedilir — araçlar: Pixelorama, Gallery
- 8. adım — Add states ile özel 'empty health bar' durumu üretilir — araçlar: Add states
- 9. adım — Orijinal sağlık çubuğu Pixelorama'da doldurulur, dolu ve boş durumlar elde edilir — araçlar: Pixelorama
- 10. adım — Gün/gece çubuğu temizlenip kaydedilir — araçlar: Pixelorama, Gallery
- 11. adım — Varlıklar oyuna alınıp sağlık çubuğu, düğmeler ve panel test edilir — araçlar: PixelLab
- 12. adım — Bir düğme kopyalanıp Creator'da Create from style reference aracına stil referansı olarak yapıştırılır — araçlar: Create from style reference
- 13. adım — Envanter slotu tarifi ve Remove background ile üretim yapılır — araçlar: Create from style reference, Remove background
- 14. adım — Envanter slotları oyunda kontrol edilir — araçlar: PixelLab
## Promptlar
- Yerleşim şablonuna renk ve malzeme stili verme — Derin kömür grisi arduvaz, soğuk demir çerçeve ve keskin ocak ateşi turuncusu vurgularıyla piksel sanat arayüz seti istendi.
- Sağlık çubuğu için boş durum görseli — Sağlık çubuğunun boş halini özel durum olarak üret; durum adı 'empty health bar'.
- Envanter slotları setini düğme stilinde üretme — Kılıç, kalkan, yay ve ok, bomba, kırmızı ve yeşil iksir ile diğer RPG macera eşyaları için envanter slotu üret; arka plan kaldırma açık.
