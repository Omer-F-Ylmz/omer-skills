# PixelLab Tutorial: How to Generate & Animate GBA-Style Sprites
## Künye
PixelLab Tutorial: How to Generate & Animate GBA-Style Sprites · PixelLab · süre: 12:40 · en-orig · https://youtu.be/moCpjMOOBGk · şema 2
motor: parti 2026-10-11-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 67120 tk · claude-haiku-5-5: claude-haiku-5-5 · 272375 tk
## Özet
PixelLab ile 'vibe coded' bir Zelda klonundaki yer tutucu kutuları GBA tarzı top-down piksel sanatla değiştirme eğitimi. Karakter Oluşturucu (Pro) ile 32x32 balıkçı üretilir, 8 yönlü döndürme alınır, Pixelorama ve Aseprite'te temizlenir; yürüme, koşma ve kılıç animasyonları üretilir (Custom Animation V3). Ardından Map Editor'da su/çimen tileset'i, ağaç/heykel/ev nesneleri, stil referansıyla şövalye, prenses, okçu NPC'leri, kalp ikonu ve ok mermileri yapılır. Ana mesaj: üret, temizle, canlandır, iyileştir; AI çıktısı elle düzeltme gerektirir.
## Bölümler
- 0:00 Projeye giriş
- 0:24 Karakter üretiminin temelleri
- 1:14 Hareket animasyonu
- 2:56 Özel dövüş animasyonları
- 3:44 Dünya ve harita oluşturma
- 5:24 İleri NPC animasyonu
- 8:24 Ölçekleme ve NPC güncellemeleri
- 10:50 Son rötuşlar ve UI öğeleri
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| PixelLab | yok | teknik | yok | Piksel sanat karakter, harita, nesne ve animasyon üreten AI web servisi; videonun ana aracı. | 0:20 | Ana sayfada 'Create unique pixel art assets for your game 10x faster with AI'. (karede: pixellab.ai ana sayfası: üst menüde PixelLab, Docs, API, Vibe coding, Editor, Creator, Characters, Objects, Maps; ortada 'PixelLab' başlığı ve Join Discord düğmesi.) |
| Character Creator | yok | teknik | yok | Karakter üretme sayfası; 8 yön döndürme ve animasyon ekleme burada yapılır. | 0:24 | Altyazı: 'We'll start on the Pixel Lab character creator page.' (karede: pixellab.ai/Characters sayfası: üstte 'Create' düğmeli arama çubuğu, altında karakter kartları ızgarası.) |
| Pro mode | yok | teknik | yok | Karakter oluşturucuda stil referansı/konsept görseli destekleyen, 8 yön üreten gelişmiş mod; 20-40 üretim harcar. | 0:38 | Ekranda 'Generation Mode: Standard / Pro NEW'; altyazı pro sürümü anlatıyor. (karede: Create Character sayfası, 'Create from Template' sekmesi, Generation Mode'da Pro seçili, Humanoid kartı seçili.) |
| Pixelorama | yok | teknik | yok | PixelLab'in site içi piksel editörü; sprite temizleme, kare düzenleme, 'Save to Character Creator'. | 1:04 | Altyazı: 'I'm going to click edit in Pixel Orama right here on the site.' (karede: 'PixelLab Pixelorama' editörü: sol menüde Create Image/Edit/Rotate/Animate; ortada 56×56 balıkçı sprite'ı, altta 8 kare zaman çizelgesi.) |
| Aseprite | yok | teknik | yok | Sprite'ları dışa aktarıp baş kopyalama, tuval boyutu ve ok döndürme için kullanılan harici piksel editörü. | 1:54 | Altyazı: 'I'm going to export the sprites and open them in Aseprite.' (karede: Aseprite v1.3.16.1, 'south.png' sekmesi açık; balıkçı sprite'ının başı seçili, solda palet.) |
| PixelLab Aseprite Extension | yok | plugin | yok | Aseprite içinde PixelLab araçlarını (Create image, Edit, Animate, Reduce colors vb.) açan eklenti paneli. | 11:58 | Ok sprite sheet'i Aseprite'te açılırken PixelLab menüsü görünüyor. · kanıt: kare (karede: Aseprite penceresinde 'PixelLab' açılır paneli: Create image, Edit image, Rotate, Animate, Map, Inpaint, Reduce colors, Create UI elements, Animate with skeleton (new).) |
| Custom Animation V3 | yok | teknik | yok | Metinle özel animasyon üreten V3 modeli; kare sayısı ayarlanır, ilk kare korunur; 1-8 üretim. | 1:30 | Kılıç saldırısı ve yürüme döngüsü için 'custom animation V3' kullanıldı. (karede: Add Animation sayfasında 'Custom Animation V3' seçili; Action Description, Frame Count: 8, 'Keep first frame (idle pose)' kutusu, 'Cost: 1 generation'.) |
| Enhance with AI | yok | teknik | yok | Kısa animasyon promptunu otomatik ayrıntılandıran düğme ('enhanced prompt'). | 2:56 | 'I hit the enhance with AI button and set it to six frames.' |
| Map Editor | yok | teknik | yok | Tileset ile harita çizilen, nesne ve karakter yerleştirilen PixelLab haritası aracı; otomatik döşeme (auto tiling) sunar. | 4:02 | Altyazı: 'thanks to auto tiling, drawing out our island is a breeze.' (karede: 'Untitled Map – PixelLab Map Editor': solda Terrains, Tools (Inpaint Map, Create Object, Place Asset); mavi su zemini çizilmiş.) |
| Create Tileset | yok | teknik | yok | Alt/üst zemin (su/çimen), geçiş yüzdesi ve stil seçenekleriyle tileset üreten araç. | 3:50 | Altyazı: 'hit new tile set... lower terrain to water and the upper terrain to grass'. (karede: 'Create Tileset' sayfası: Standard sekmesi, Tile Size 16×16/32×32, Lower Terrain / Upper Terrain 'Create New', Transition None/Small/Large/Full.) |
| Edit Image (pro) | yok | teknik | yok | Tileset'i metinle düzenleyen Pixelorama aracı (20 üretim); yeni katmana render eder. | 4:14 | Prompt: 'Make the grass and water prettier, more muted, no gradients.' (karede: Pixelorama 'Edit Image (pro)' paneli: Method 'Edit with text', Description alanında 'make the grass and wa', 'This tool costs 20 generations.') |
| Create Object | yok | teknik | yok | Haritada alan seçip metinle şeffaf arka planlı nesne (ağaç, heykel, çalı) üreten araç. | 4:40 | Altyazı: 'Using the create object tool, I select an area and prompt top-down tree.' (karede: Haritada 'AI Object Creation' paneli: seçili alan 120x136px, 'What object do you want to create?' alanında 'top-down tree'; ağacın etrafında seçim kutusu.) |
| Pro inpainting | yok | teknik | yok | Create Object içinde daha kaliteli sonuç veren ama 40 kat fazla üretim harcayan seçenek. | 4:40 | Altyazı: 'If you want higher-quality assets, turn on pro inpainting.' (karede: AI Object Creation panelinde 'Snap to grid' ve 'Pro inpainting' onay kutuları; kare 11:00'de 'Pro inpainting uses 40x more generations' uyarısı.) |
| Create image S-XL | yok | teknik | yok | Creator sekmesinde 16-768 px görsel üreten araç; 128x128 ahşap ev ve kalp ikonu için kullanıldı. | 5:00 | Altyazı: 'create image small to XL tool in the creator tab.' (karede: Creator sayfasında Tool: 'Create image S-XL (new)'; Description'da ev promptu, View High top-down, Width/Height 128, Detail 'Highly detailed'; sağda galeride ev.) |
| Create from style reference | yok | teknik | yok | Referans sprite yüklenerek aynı stilde yeni karakterler (şövalye, prenses) üreten Pro araç; 20 üretim. | 5:30 | Altyazı: 'create from style reference pro. I drop our south-facing player sprite in.' (karede: Tool: 'Create from style reference PRO', 'This tool costs 20 generations', yükleme alanı, Description 'fantasy weapons', Output 64x64 – 4x4 (16 frames).) |
| Generate 8 rotations | yok | teknik | yok | Seçilen tek sprite'tan 8 yönlü döndürme seti üreten araç. | 5:52 | Altyazı: 'run him through the generate eight rotations tool.' (karede: 'Select Tool' penceresi Animate sekmesi: 'Generate 8 rotations NEW – Create 8 directional views from reference' vurgulu.) |
| Create Character | yok | iş akışı | yok | Yeni güncelleme: rotasyon sayfasından tek tıkla karakter oluşturucuya aktarır ve iskeleti tahmin eder. | 10:32 | 'automatically imports everything, estimates the skeleton, and you're ready to animate' (karede: Create Character sayfası 'Create from Reference' sekmesi; yeşil bildirim '8-directional character loaded – All 8 direction images have been loaded.') |
| Create image Pro | yok | teknik | yok | Yüksek kaliteli görsel aracı; tek seferde sprite sheet üretir (ok mermileri için 32x32). | 11:38 | 'I'm using the pro tool here because it generates a bunch of frames at once.' (karede: Creator sayfası Tool: 'Create image PRO', Description 'single arrow in 8 directions', Output size 32x32, 'This tool costs 20 generations'.) |
| Mirror animasyon | yok | ipucu | yok | Yalnız S, SE, E, NE, N üret; doğu/güneydoğuyu temizleyip batı/güneybatıya yansıtarak üretim tasarrufu yap. | 2:16 | 'I can just mirror them for the west and southwest directions.' · kanıt: yok |
| Orta adım başlangıç karesi | yok | ipucu | yok | Yürüme animasyonunda ayakta duran kare yerine bacakları açık orta-adım karesini başlangıç yap (Discord'dan öğrenilen hile). | 6:24 | 'don't use a standing frame as your start frame. Use a frame where the character is already mid-stride.' · kanıt: yok |
| Tuval boyutunu küçültme | yok | ipucu | yok | Stil referansı sprite'ın tuvalini 56x56'dan 32x32'ye indirerek ölçek tutarlılığı sağla. | 8:24 | 'I'm going to reduce the canvas size down to 32 by 32.' · kanıt: yok |
| Dia | yok | teknik | yok | Videoda PixelLab sitesini açmak için kullanılan tarayıcı (menü çubuğunda görünür). | 0:32 | Menü çubuğunda 'Dia' uygulaması ve tarayıcı sekmeleri. (karede: macOS menü çubuğunda 'Dia File Edit View Tabs Bookmarks History Extensions Window Help'; adres çubuğunda pixellab.ai/create-character/new.) |
| Animate with Text | yok | teknik | yok | Mevcut bir kareden (ör. ara yürüyüş karesi) başlayarak metinle animasyon üreten araç | 6:24 | I go back to animate with text new, and I set that middle frame |
| Walking (6 frames) | yok | teknik | yok | Hazır 6 kareli yürüyüş şablonu; sekiz yön için animasyon üretir | 1:14 | I'm selecting walk six frames for all eight directions. |
| Running | yok | teknik | yok | Hazır 6 kareli koşma şablonu; güney, güneydoğu, doğu, kuzeydoğu, kuzey yönleri üretilip diğerleri aynalanıyor | 2:16 | For the run cycle, we hit add animation and choose running six frames. |
| Place Asset | yok | teknik | yok | Haritaya karakter ya da Object Creator nesnesi yerleştiren araç; karakteri ölçek için haritaya koydu | 3:44 | I even drop our character on the map to get a sense of scale. |
| Create UI Elements | yok | teknik | yok | UI bileşeni (ikon vb.) üreten araç; videoda 'small 2XL tool' olarak anılıyor, eşleşme tahmini | 10:50 | Let's head to the creator tab and use the small 2XL tool. |
| Ana karakter (balıkçı) üretimi | yok | prompt | yok | Küçük, GBA tarzı, yukarıdan bakışlı Zelda tarzı balıkçı karakteri; yüksek top-down kamera, 32x32. | 0:24 | kaynak: altyazı |
| Özel kılıç saldırı animasyonu | yok | prompt | yok | Hızlı kılıç saldırısı, Zelda tarzı; AI ile geliştirilmiş, 6 kare (ilk kareyle 7). | 2:56 | kaynak: altyazı |
| Tileset'i düzenleme | yok | prompt | yok | Su ve çimeni daha güzel, daha mat yap; gradyan olmasın. | 4:14 | kaynak: kare |
| Tileset'e doku ekleme | yok | prompt | yok | Dokuları olsun (önceki isteme eklendi). | 4:26 | kaynak: altyazı |
| Haritaya ağaç nesnesi | yok | prompt | yok | Yukarıdan bakışlı ağaç. | 4:40 | kaynak: kare |
| Ev nesnesi üretimi | yok | prompt | yok | 128x128, kılıç sembollü yukarıdan bakışlı ahşap ev. | 5:00 | kaynak: kare |
| Düşman/NPC üretimi | yok | prompt | yok | RPG şövalyeleri ve prensesleri (stil referansı: oyuncu sprite'ı). | 5:30 | kaynak: kare |
| Şövalye yürüme animasyonu | yok | prompt | yok | Yürüme döngüsü; ardından 'Knight holding a sword walking loop'. Geliştirilmiş prompt, 6 kare. | 6:24 | kaynak: altyazı |
| Ölçeği eşleşen NPC'ler | yok | prompt | yok | RPG karakterleri: okçu, çiftçi ve prenses; 32x32 tuvalle. | 8:24 | kaynak: kare |
| Okçu animasyonu | yok | prompt | yok | Yay ile ok atma (geliştirilmiş prompt). | 9:24 | kaynak: altyazı |
| Çalı nesnesi | yok | prompt | yok | Küçük çimen çalısı; boyama alanı biraz silinerek küçültüldü. | 10:50 | kaynak: kare |
| Can barı UI öğesi | yok | prompt | yok | Küçük kalp ikonu, 32x32. | 11:30 | kaynak: altyazı |
| Mermi sprite sheet | yok | prompt | yok | Sekiz yönde tek ok; 32x32. | 11:38 | kaynak: kare |
## Açıklama bağlantıları
- https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=moCpjMOOBGk — PixelLab ana sayfası · aday: evet (PixelLab) · Videoda kullanılan ana araç/servis; izleyici doğrudan kullanabilir. utm parametresi yalnız izleme, ortaklık kodu değil. · sınıf: diğer
- https://discord.gg/3cYE5fdkRX — PixelLab Discord topluluk daveti · aday: hayır · Topluluk daveti; videoda araç olarak kullanılmadı, yalnız hile kaynağı olarak anıldı. · sınıf: diğer
- https://api.pixellab.ai/v2/docs — PixelLab API v2 dokümanı · aday: hayır · Videoda gösterilmedi ya da kullanılmadı; yalnız açıklama ve yorumda geçiyor. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Pro karakter aracı çıktı başına yaklaşık 20-40 üretim harcar; V3 sprite boyutuna göre 1-8. | 1:14 | sayısal |
| Pro inpainting normal inpainting'ten 40 kat fazla üretim kullanır. | 4:40 | sayısal |
| Standart animasyon şablonları eşya tutmayan karakterlerle eğitildiği için kılıçlı şövalyede kötü sonuç verir; custom V3 öneriliyor. | 5:24 | öneri |
| Mid-stride başlangıç karesi daha doğal yürüme animasyonu verir. | 6:24 | öneri |
| Tuval küçülünce aynı batch'te daha fazla üretim seçeneği çıkar ve ölçek eşleşir. | 8:24 | karşılaştırma |
| Rotasyon sayfasındaki yeni Create Character düğmesi aktarımı ve iskelet tahminini otomatik yapar. | 10:26 | özellik |
| %50 geçiş genellikle en iyi görünümü verir. | 3:44 | öneri |
| Pro araç tek seferde sprite sheet üzerinde çok kare üretir. | 11:38 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Zelda klonu (vibe coded oyun) | aday değil: konu dışı | Ürün değil; üzerine varlık eklenen proje. |
| konuşma 0:00 | Game Boy Advance stili | aday değil: genel kavram | Estetik tarifi. |
| ekran 0:00 | localhost oyun adresleri | aday değil: konu dışı | Yerel test sunucusu adresleri. |
| ekran 0:20 | pixellab.ai | PixelLab | Ana sayfa gösteriliyor. |
| konuşma 0:24 | Character creator sayfası | Character Creator | We'll start on the Pixel Lab character creator page. |
| konuşma 0:24 | Pro sürüm (karakter) | Pro mode | I'm going to use the pro version. |
| konuşma 0:24 | Standart oluşturucu | aday değil: başka adayın parçası (Pro mode) | Standard creator, tweak proportions; Pro seçildi. |
| konuşma 0:24 | Yüksek top-down kamera, 32x32 | aday değil: başka adayın parçası (Pro mode) | Pro modun ayarları. |
| konuşma 0:24 | Sekiz yönlü rotasyon | aday değil: başka adayın parçası (Character Creator) | Karakter çıktısının parçası. |
| konuşma 0:24 | Pixel Orama / Pixelorama | Pixelorama | click edit in Pixel Orama. |
| konuşma 1:14 | Animasyon şablonları | aday değil: başka adayın parçası (Character Creator) | Walk, run, throw, push şablonları. |
| konuşma 1:14 | V3 modeli | Custom Animation V3 | V3 is much cheaper, 1 to 8. |
| konuşma 1:14 | Aseprite | Aseprite | export the sprites and open them in Aseprite. |
| konuşma 2:16 | Koşma (running six frames) | aday değil: başka adayın parçası (Character Creator) | Şablon animasyon. |
| konuşma 2:16 | Yön yansıtma | Mirror animasyon | mirror them for the west and southwest. |
| konuşma 2:56 | Throw, push, lead jab şablonları | aday değil: başka adayın parçası (Character Creator) | Şablon listesi, kullanılmadı. |
| konuşma 2:56 | Enhance with AI | Enhance with AI | I hit the enhance with AI button. |
| konuşma 3:44 | Maps sekmesi / tile set | Create Tileset | head to the maps tab and hit new tile set. |
| konuşma 3:44 | Auto tiling | Map Editor | thanks to auto tiling, drawing out our island is a breeze. |
| konuşma 3:44 | Edit image pro | Edit Image (pro) | edit in Pixelorama, then edit image pro. |
| konuşma 3:44 | Create object | Create Object | Using the create object tool, I select an area. |
| konuşma 4:46 | Create image small to XL | Create image S-XL | create image small to XL tool in the creator tab. |
| konuşma 5:24 | Create from style reference pro | Create from style reference | create from style reference pro. |
| konuşma 5:24 | Generate eight rotations | Generate 8 rotations | run him through the generate eight rotations tool. |
| konuşma 6:24 | Mid-stride başlangıç karesi hilesi | Orta adım başlangıç karesi | Use a frame where the character is already mid-stride. |
| konuşma 6:24 | Discord kanalı | aday değil: konu dışı | Hile bu topluluktan öğrenildi; araç olarak kullanılmadı. |
| konuşma 8:24 | Tuval 56x56'dan 32x32'ye | Tuval boyutunu küçültme | reduce the canvas size down to 32 by 32. |
| konuşma 10:26 | Create character düğmesi | Create Character | you can now just click this new create character button. |
| konuşma 11:38 | Create image pro | Create image Pro | I'm going to create image pro setting the size to 32 by 32. |
| kare 11:58 | PixelLab Aseprite paneli | PixelLab Aseprite Extension | Aseprite'te PixelLab menüsü açık. |
| kare 0:32 | Dia tarayıcı | Dia | Menü çubuğunda Dia. |
| kare 4:40 | Pro inpainting | Pro inpainting | Create Object panelinde seçenek. |
| kare 2:08 | chatgpt.com sekmesi | aday değil: konu dışı | Yalnız sekme listesinde 'Object Creator Overview'; kullanılmadı. |
| kare 2:04 | JJK MMO Prototype / LIMITLESS sekmeleri | aday değil: konu dışı | Tarayıcı sekme listesinde görünür. |
| açıklama | PixelLab ana sayfa bağlantısı | PixelLab | www.pixellab.ai?utm_source=youtube... |
| açıklama | Discord daveti | aday değil: konu dışı | discord.gg bağlantısı; topluluk. |
| açıklama | API v2 dokümanı | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | docs/tools/animate-with-text-pro | Custom Animation V3 | Animate with text aracının dokümanı. |
| linkli sayfa | docs/tools/rotate | Generate 8 rotations | Rotate araç dokümanı. |
| linkli sayfa | docs/tools/consistent-style | Create from style reference | Stil tutarlılığı aracı dokümanı. |
| linkli sayfa | docs/getting-started | aday değil: konu dışı | Genel başlangıç sayfası. |
| linkli sayfa | docs/tools/create-image-flux | aday değil: konu dışı | Videoda anılmayan görsel aracı dokümanı. |
| linkli sayfa | docs/tools/create-map | Map Editor | Harita aracı dokümanı. |
| linkli sayfa | docs/tools/create-ui-elements-pro | aday değil: konu dışı | Videoda kullanılmayan UI aracı. |
| linkli sayfa | Diğer youtu.be videoları | aday değil: konu dışı | Başka videolara bağlantılar. |
| yorum | MCP ve API tool parity | aday değil: konu dışı | Yalnız izleyici/sahip yorumu; videoda gösterilmedi. |
| yorum | Godot | aday değil: konu dışı | Yalnızca bir yorumda isteniyor. |
## Kareden okunanlar
- 0:00: Oyun penceresi 'Hyrule' bölgesi: LIFE kalpleri, B/A slotları, yeşil ejderha maskotu; adres localhost.
- 0:20: pixellab.ai ana sayfa: 'Create unique pixel art assets for your game 10x faster with AI', Join Discord.
- 0:24: Characters sayfası: arama çubuğu ve Create düğmesi, 'Character Creator page' başlık yazısı.
- 0:32: Altyazı 'a small GBA-style top-down fisherman, Zelda style'; Camera View High Top-Down seçili, 48px, Character Proportions kaydırıcıları.
- 0:38: Create Character: Generation Mode Standard/Pro (Pro seçili), Humanoid/Quadruped, Description 'small gba style top-down fisherman, zelda style'.
- 0:44: Boyut 32px, High Top-Down; 'Generate Character' düğmesi, 'This tool costs 20-40 generations', GENERATING yazısı.
- 0:50: Karakter sayfası: 56×56px, 8 directions, 0 animations; üst yazı 'size: 32x32 (sprite size, canvas size is bi...'.
- 1:10: Pixelorama'da 'Success: Character saved to Character Creator successfully! Please refresh the page'.
- 1:18: Add Animation: Movement (Idle, Jumping, Running, Walking), Combat, Interactions, Custom Animation V3 ve (Pro).
- 1:30: Custom Animation V3: Frame Count 8, 'Keep first frame (idle pose)', 'Cost: 1 generation', 'Generation takes 1-2 minutes per direction'.
- 1:38: 'Walking (6 frames)' kartı, South %5 üretiliyor; 'Animation Job Submitted!' bildirimi.
- 1:52: Finder'da animations, rotations klasörleri ve metadata.json; 'CONSISTENCY' yazısı.
- 3:50: Create Tileset: Tile Size 16×16, Top-down, Lower/Upper Terrain, Transition None/Small (25%)/Large (50%)/Full (100%).
- 3:54: Lower 'water', Upper 'grass', Transition Large (50%) seçili, Transition Description alanı.
- 3:56: Transition Description 'rocks'; Style Options: Outline (Selective), Shading (Basic), Detail Level (Medium).
- 4:14: Edit Image (pro): Method 'Edit with text', 'This tool costs 20 generations', Remove background işaretli.
- 4:40: Harita üstü yazı: Inpaint Map / Create Object / Place Assets açıklamaları; AI Object Creation 'top-down tree'.
- 11:00: Cool Map: AI Object Creation, Pro inpainting (40x), Paint/Erase, 'ERASER MODE ACTIVE'.
- 11:38: Create image PRO: 'single arrow in 8 directions', Output size 32x32, 32x32 – 8x8 grid (64 variations).
- 12:00: Aseprite 'Import Sprite Sheet' penceresi: Type By Rows, Width/Height 16, Columns 16, Rows 16.
## Belirsizlikler
- Oyunun 'vibe coded' yapıldığı ana yapay zekâ aracı ya da modeli videoda söylenmiyor; aday olarak yazılamadı.
- Açıklamadaki PixelLab bağlantısında utm parametreleri var; bunlar yalnız izleme olduğundan sınıf 'diğer' seçildi, ortaklık kodu görünmüyor.
- Create UI elements, Interpolate, Animate with skeleton, Multi-Image Edit, Try On gibi öğeler yalnız menüde görünüyor, videoda kullanılmıyor.
- Yorumdaki Godot ve MCP anıları yalnız izleyici yorumu; videoda kullanılmadı.
- Tarayıcı sekmelerinde görünen chatgpt.com (Object Creator Overview), JJK MMO Prototype ve Nikllo videoda kullanılmıyor.
- Sözlük eşleşmeleri (Framer Motion, Three.js, Next.js, Stripe vb.) bulanık OCR/ses eşleşmesi; videoda geçmiyor.
- Oyun 'Zelda klonu' olarak anılıyor; oyun motoru adı belirtilmiyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/15 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| http://localhost:3458 | 0:00 | ekran | hayır |
| http://localhost:3456 | 0:02 | ekran | hayır |
| http://localhost:52083 | 0:12 | ekran | hayır |
| pixellab.ai | 0:20 | ekran | evet |
| pixellab.ai/create-character/new?prompt=small+gba+style+top-down+fisherman%2C+zelda-style | 0:32 | ekran | evet |
| chatgpt.com | 2:08 | ekran | hayır |
| http://localhost:83379 | 3:37 | ekran | hayır |
| http://localhost:63238 | 8:28 | ekran | hayır |
| http://localhost:83238 | 8:30 | ekran | hayır |
| pixellab.ai/create-character/new?from=create&rotations=8 | 10:32 | ekran | evet |
| https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=moCpjMOOBGk | açıklama | açıklama | evet |
| https://discord.gg/3cYE5fdkRX | açıklama | açıklama | hayır |
| https://api.pixellab.ai/v2/docs | açıklama | yorum | hayır |
| https://www.pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | evet |
| https://www.pixellab.ai/docs/tools/rotate | açıklama | açıklama | evet |
| https://www.pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | evet |
| https://www.pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-map | açıklama | açıklama | evet |
| https://www.pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
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
| https://pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | evet |
| https://pixellab.ai/docs/tools/rotate | açıklama | açıklama | evet |
| https://pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | evet |
| https://pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-map | açıklama | açıklama | evet |
| https://pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
| pixellab.ai/pixellab.ai/create-character/new?from=create&rotations=8 | 10:40 | ekran | evet |
| http://ocalhost:63070 | 11:16 | ekran | hayır |
## İş akışı
- 1. adım — Yer tutucu kutulu Zelda klonunu gösterip hedefi belirleme — araçlar: PixelLab
- 2. adım — Pro modda 32x32 yüksek top-down balıkçıyı üretme — araçlar: Character Creator, Pro mode
- 3. adım — 8 yönü Pixelorama'da temizleyip karakter oluşturucuya kaydetme — araçlar: Pixelorama
- 4. adım — Walking (6 frames) animasyonunu 8 yön için üretme — araçlar: Character Creator
- 5. adım — Sprite'ları dışa aktarıp başı kopyalayarak tutarlılık sağlama, kalanı Pixelorama'da bitirme — araçlar: Aseprite, Pixelorama
- 6. adım — Koşma animasyonunu 5 yönde üretip yansıtma ve temizleme — araçlar: Character Creator, Pixelorama
- 7. adım — Kılıç saldırısını Custom Animation V3 ile üretip elle düzeltme — araçlar: Custom Animation V3, Enhance with AI, Pixelorama
- 8. adım — Su/çimen tileset'i oluşturup Pixelorama'da prompt ile güzelleştirme — araçlar: Create Tileset, Edit Image (pro), Pixelorama
- 9. adım — Adayı auto tiling ile çizip karakteri ölçek için yerleştirme — araçlar: Map Editor
- 10. adım — Ağaç ve heykel nesnelerini üretip evi indirerek haritaya sürükleme — araçlar: Create Object, Pro inpainting, Create image S-XL
- 11. adım — Stil referansıyla şövalye/prenses üretip 8 rotasyon alma — araçlar: Create from style reference, Generate 8 rotations
- 12. adım — Şövalyeyi V3 ile mid-stride kareden canlandırıp kask ve kılıcı düzeltme — araçlar: Custom Animation V3, Pixelorama
- 13. adım — Ölçeği 32x32 tuvalle düzeltip okçu/çiftçi/prenses üretme ve canlandırma — araçlar: Aseprite, Create from style reference, Create Character
- 14. adım — Çalı nesnesi, kalp ikonu ve ok sprite sheet'ini üretip Aseprite'te döndürme — araçlar: Create Object, Create image S-XL, Create image Pro, Aseprite
- 15. adım — Son prototipi oyun motorunda gösterme — araçlar: PixelLab
## Promptlar
- Ana karakter (balıkçı) üretimi — Küçük, GBA tarzı, yukarıdan bakışlı Zelda tarzı balıkçı karakteri; yüksek top-down kamera, 32x32.
- Özel kılıç saldırı animasyonu — Hızlı kılıç saldırısı, Zelda tarzı; AI ile geliştirilmiş, 6 kare (ilk kareyle 7).
- Tileset'i düzenleme — Su ve çimeni daha güzel, daha mat yap; gradyan olmasın.
- Tileset'e doku ekleme — Dokuları olsun (önceki isteme eklendi).
- Haritaya ağaç nesnesi — Yukarıdan bakışlı ağaç.
- Ev nesnesi üretimi — 128x128, kılıç sembollü yukarıdan bakışlı ahşap ev.
- Düşman/NPC üretimi — RPG şövalyeleri ve prensesleri (stil referansı: oyuncu sprite'ı).
- Şövalye yürüme animasyonu — Yürüme döngüsü; ardından 'Knight holding a sword walking loop'. Geliştirilmiş prompt, 6 kare.
- Ölçeği eşleşen NPC'ler — RPG karakterleri: okçu, çiftçi ve prenses; 32x32 tuvalle.
- Okçu animasyonu — Yay ile ok atma (geliştirilmiş prompt).
- Çalı nesnesi — Küçük çimen çalısı; boyama alanı biraz silinerek küçültüldü.
- Can barı UI öğesi — Küçük kalp ikonu, 32x32.
- Mermi sprite sheet — Sekiz yönde tek ok; 32x32.
