# I Made 3D Parkour Animation With AI - Full Workflow
## Künye
I Made 3D Parkour Animation With AI - Full Workflow · Stefan 3D AI · süre: 20:40 · en · https://youtu.be/1eFShSYATOI · şema 2
motor: parti 2026-10-09-short-40 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (59)
kareler: girdi ≤40000 jeton için 60→59
claude-sonnet-5-5: claude-sonnet-5-5 · 62655 tk · claude-haiku-5-5: claude-haiku-5-5 · 228838 tk
## Özet
Stefan 3D AI, tek geliştiriciler için animasyonun en zor kısım olduğunu söyler. Blender'da inşaat sahası parkur sahnesini bloklar, Substance Painter ile doku kaplar, Tripo AI ile prop ve karakter parçaları üretir, Blender'da birleştirir. Karakteri Mixamo iskeletiyle Cascadeur'e alır. Otomatik pozlama, ara kare (in-betweening), video referansı, fizik, root motion AI ve retargeting ile parkur animasyonu yapar, sonunda Unreal Engine'e aktarır.
## Bölümler
- 0:00 Animasyon neden en zor kısım
- 1:08 Parkur sahnesini bloklama ve dokulama
- 2:41 Tripo AI ile 3B varlık üretimi
- 6:14 Cascadeur kurulumu ve Mixamo rig
- 8:50 Otomatik pozlama ve ara kare
- 11:33 Parkur için video referansı
- 12:46 Otomatik fizikle süzülme sorununu düzeltme
- 14:31 AI root motion üretimi
- 17:58 Retargeting ve Unreal Engine'e aktarım
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Cascadeur | yok | plugin | yok | Otomatik pozlama, ara kare, fizik ve root motion AI içeren animasyon yazılımı; videonun ana aracı. | 6:14 | Now Cascader part. Okay, so let's open the Cascader and let's create a new scene. |
| Tripo AI | yok | CLI | yok | Smart Mesh ile düşük poligonlu, dokulu 3B prop ve karakter parçası üreten servis. | 2:41 | Tripo arayüzü, Smart Mesh sekmesi ve poligon sayısı kaydırıcısı (karede: kanıttan) Tripo arayüzü, Smart Mesh sekmesi ve poligon sayısı kaydırıcısı |
| Blender | yok | CLI | yok | Sahe bloklama, varlıkları birleştirme ve rig temizliği için kullanıldı. | 1:08 | we built up the whole blocking in Blender |
| Substance Painter | yok | CLI | yok | Büyük yüzeylere malzeme, decal ve metin kaplamak için. | 2:08 | we quickly applied materials in Substance Painter |
| Mixamo | yok | CLI | yok | Karaktere iskelet eklemek için kullanılan servis. | 5:42 | adding a skeleton in Mixama as usual |
| Unreal Engine | yok | CLI | yok | Animasyonun son sahnede oynatıldığı oyun motoru; Live Link ile önizleme. | 17:58 | it's time to bring it all to Unreal Engine |
| ChatGPT | yok | CLI | yok | Sahne konsepti ve prop promptlarını ve görsellerini üretmek için. | 1:42 | ChatGPT sohbetinde parkur haritası promptu ve üretilen inşaat sahası görseli (karede: kanıttan) ChatGPT sohbetinde parkur haritası promptu ve üretilen inşaat sahası görseli |
| Nano Banana | yok | CLI | yok | Prop görsellerini üretmek için anılan görsel modeli (konuşmada 'Anabanana'). | 2:41 | with ChagiPT and Anabanana, we created a bunch of props · kanıt: yok |
| Sketchfab | yok | CLI | yok | Vinç gibi ücretsiz genel varlıkların alındığı site. | 1:08 | we actually took them from Sketchfab |
| NVIDIA Kimodo | yok | CLI | yok | Karşılaştırma için anılan AI animasyon modeli. | 0:48 | Kanal videosu listesinde 'AI Animation Just Got a Revolution — NVIDIA Kimodo' (karede: kanıttan) Kanal videosu listesinde 'AI Animation Just Got a Revolution — NVIDIA Kimodo' |
| Hunyuan Motion | yok | CLI | yok | Metinden animasyon üreten, daha önce işlenen model. | 0:48 | 'Free Text to Animation with only 8GB VRAM in ComfyUI' video kartı (karede: kanıttan) 'Free Text to Animation with only 8GB VRAM in ComfyUI' video kartı |
| ComfyUI | yok | CLI | yok | Hunyuan Motion videosunda geçen arayüz. | 0:48 | Video küçük resminde 'COMFY UI' etiketi (karede: kanıttan) Video küçük resminde 'COMFY UI' etiketi |
| Auto posing | yok | teknik | yok | Rig'i oynatınca vücudun geri kalanını takip ettiren önceden eğitilmiş Cascadeur aracı. | 7:14 | here is the main tool, which is auto posing |
| In-betweening | yok | teknik | yok | Anahtar kareler arası algoritmik ara animasyon. | 10:50 | press this in between button and it's completely different result |
| Auto physics | yok | teknik | yok | Animasyonu fizik ayarlarıyla yeniden hesaplayıp doğallaştıran araç. | 12:46 | enabling physics |
| Root motion | yok | teknik | yok | Difüzyon tabanlı, stil seçilebilen (run, walk, acrobatics) hareket üretimi. | 14:31 | this is a diffusional AI, which always gonna generate different movements |
| Retargeting | yok | teknik | yok | Animasyonu kopyalayıp karaktere yapıştırma. | 17:58 | Menüde 'Retargeting Copy' ve 'Retargeting Paste' seçenekleri (karede: kanıttan) Menüde 'Retargeting Copy' ve 'Retargeting Paste' seçenekleri |
| Quick Rigging Tool | yok | teknik | yok | Cascadeur'de Mixamo iskeletini tanıyıp rig oluşturan araç. | 6:20 | QUICK RIGGING TOOL penceresi, 'Add rig elements' düğmesi (karede: kanıttan) QUICK RIGGING TOOL penceresi, 'Add rig elements' düğmesi |
| Live Link | yok | teknik | yok | Cascadeur'den Unreal Engine'e canlı animasyon önizlemesi. | 17:58 | There is also a live link where you can drop the character |
| Toon Shader | yok | teknik | yok | Unreal Engine'de kullanılması planlanan, yalnız Albedo kullanan gölgelendirici. | 2:41 | In Unreal Engine, we intend to use Toon Shader |
| Font Black Ops One | yok | teknik | yok | Substance Painter'da decal metni için kullanılan yazı tipi. | 2:32 | Substance'ta 'Font Black Ops One' parametresi (karede: kanıttan) Substance'ta 'Font Black Ops One' parametresi |
| Smart Mesh | yok | teknik | yok | Tripo AI'ın poligon sayısı ayarlanabilen model üretim modu; prop'lar için optimize mesh üretiliyor. | 2:58 | Smart Mesh sekmesi ve Polycount ayarı ekranda görünüyor (karede: Tripo Generate Model paneli; Smart Mesh sekmesi seçili, Polycount slider'ı yaklaşık 1500 değerinde, koni görseli yüklü.) |
| Filament | yok | teknik | yok | Cascadeur'un sahne görselleştirmesi için kullandığı gerçek zamanlı render motoru (sürüm notunda). | 1:00 | Filament metni sürüm notu ekranında görünüyor (karede: Cascadeur sürüm notu sayfası; 'New LiveLink' başlığı ve LiveLink görseli. Filament açıklaması kısa süreli OCR metni olarak görünüyor.) |
| Load Video | yok | teknik | yok | Cascadeur'a referans video yükleyip kare karesine poz çıkarmak için kullanılan pencere. | 11:34 | LOAD VIDEO penceresi duration, fps ve frames bilgisini gösteriyor (karede: LOAD VIDEO penceresi; duration 00:07.1, fps 30, frames 217; Source olarak ref_main.mp4 seçili.) |
| Add kinematic mesh | yok | teknik | yok | Cascadeur'da bir mesh'i çarpışma (collision) nesnesi olarak ekleyen komut. | 13:16 | Commands > Collision menüsünde Add kinematic mesh vurgulanmış (karede: Cascadeur Commands menüsü, Collision alt menüsü açık; Add kinematic mesh kırmızı çerçeveyle vurgulanmış.) |
| Parkur sahnesi konsept görseli | yok | prompt | yok | Bulutlu şehir silüeti üzerinde, açık tonlu, modüler blok yerleşimli gökdelen çatısı inşaat parkur haritası istenir: beton platformlar, çelik destekler, boşluklar, uzun geçiş kirişi, vinç. Mirror's Edge benzeri akış, Arcane esintili stil. Negatif prompt: karanlık cyberpunk, sis, dağınıklık, gece vb. yok. | 1:42 | kaynak: kare |
## Açıklama bağlantıları
- https://studio.tripo3d.ai/home?via=stefan&invite_code=GY5YYQ — Tripo AI davet bağlantısı · aday: evet (Tripo AI) · Tripo AI araç servisi; yönlendirme ve davet kodu var. · sınıf: affiliate
- https://cascadeur.com/?ref=stefan — Cascadeur sitesi · aday: evet (Cascadeur) · Videoda kullanılan animasyon aracı; ref parametresi var. · sınıf: affiliate
- https://top3d.ai — 3B AI araçları liderlik tablosu · aday: hayır · Kanal sahibinin kendi referans sitesi, videoda kullanılmadı. · sınıf: diğer
- https://discord.gg/am7nu68r9Z — Discord topluluğu · aday: hayır · Topluluk daveti, araç değil. · sınıf: diğer
- https://x.com/Stefan_3D_AI — Kanal sahibinin X hesabı · aday: hayır · Sosyal medya profili. · sınıf: diğer
- https://www.linkedin.com/in/stefan-3d-ai/ — LinkedIn profili · aday: hayır · Sosyal medya profili. · sınıf: diğer
- https://www.learn3d.ai/3d-ai/parkour — Ücretli 3B AI kursu · aday: hayır · Kurs tanıtımı; videoda kullanılmadı. Ücretli olabilir. · sınıf: diğer · erişilemez: ücretli kurs sayfası, içeriğine bakılamadı
- https://Top3d.ai — 3B AI araçları liderlik tablosu · aday: hayır · Kanal sahibinin kendi referans sitesi, videoda kullanılmadı. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| F | Seçili zaman noktasına kare (frame) ekler. | 8:50 | altyazı |
| R | Root motion üretimini başlatır. | 14:31 | altyazı |
| Commands > Collision > Add kinematic mesh | Sahne nesnesini fizik için kinematik çarpışma ağı yapar. (karede: Commands menüsü, Collision alt menüsünde 'Add kinematic mesh' kırmızı daire içinde) | 13:16 | kare |
| Retargeting Copy / Retargeting Paste | Animasyonu kopyalayıp hedef karaktere yapıştırır. (karede: Sağ tık menüsünde 'Retargeting Copy' ve 'Retargeting Paste' ok ile işaretli) | 17:56 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Üç ila dört dakikada bir prop hazır olur; yaklaşık 15 prop yarım günden kısa sürede üretildi. | 3:41 | sayısal |
| Cascadeur'ün root motion aracı kendisine göre NVIDIA Kimodo'dan daha fazla kontrol sunuyor. | 18:58 | karşılaştırma |
| Root motion difüzyon tabanlıdır, her seferinde farklı hareket üretir. | 14:31 | özellik |
| Büyük yüzeyler için AI dokusu yetmez (en fazla 4K); Substance Painter ile 30 dakikadan kısa sürede kaplandı. | 2:08 | sayısal |
| Küçük parçalar için 4K doku gerekmez, 2K yeterli. | 3:41 | öneri |
| Video referansının kare hızı sahneyle aynı olmalı. | 11:33 | öneri |
| Fizik çalışması için nesneler çarpışmaya (collision) eklenmeli. | 15:31 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Cascadeur | Cascadeur | Ana animasyon aracı |
| konuşma 2:41 | Tripo | Tripo AI | Smart Mesh ile prop üretimi |
| konuşma 1:08 | Blender | Blender | Bloklama yapıldı |
| konuşma 1:08 | Sketchfab | Sketchfab | Ücretsiz vinç varlığı |
| konuşma 2:08 | Substance Painter | Substance Painter | Malzeme kaplama |
| konuşma 2:41 | ChatGPT | ChatGPT | Prop promptları |
| konuşma 2:41 | Anabanana | Nano Banana | Prop görselleri |
| konuşma 2:41 | Toon Shader | Toon Shader | Unreal'de kullanılacak |
| konuşma 5:42 | Mixamo | Mixamo | İskelet ekleme |
| konuşma 0:00 | Unreal Engine | Unreal Engine | Son aktarım |
| konuşma 0:00 | HiMotion / Hunyuan Motion | Hunyuan Motion | Önceki video |
| konuşma 0:00 | NVIDIA Kimodo | NVIDIA Kimodo | Karşılaştırma |
| kare 0:48 | ComfyUI | ComfyUI | Küçük resim etiketi |
| konuşma 7:14 | Auto posing | Auto posing | Ana araç |
| konuşma 10:50 | In-betweening | In-betweening | Ara kare |
| konuşma 12:46 | Fizik | Auto physics | Süzülmeyi düzeltti |
| konuşma 14:31 | Root motion | Root motion | AI hareket üretimi |
| konuşma 17:58 | Retargeting | Retargeting | Kopyala/yapıştır |
| konuşma 17:58 | Live Link | Live Link | Unreal önizleme |
| kare 6:20 | Quick Rigging Tool | Quick Rigging Tool | Rig penceresi |
| kare 2:32 | Font Black Ops One | Font Black Ops One | Decal fontu |
| konuşma 0:00 | Filament renderer | aday değil: konu dışı | Yalnız sürüm notunda göründü |
| kare 15:26 | Aaron Nemeth | aday değil: konu dışı | Örnek video sahibi atfı |
| açıklama | Discord, X, LinkedIn | aday değil: konu dışı | Sosyal bağlantılar |
| açıklama | top3d.ai | aday değil: konu dışı | Kanal sahibinin sitesi |
| açıklama | learn3d.ai kursu | aday değil: sponsor/reklam | Kendi kurs tanıtımı |
| yorum | AniJam | aday değil: konu dışı | Yorumcunun kullandığı araç |
| yorum | Motorica | aday değil: konu dışı | İzleyici önerisi |
| yorum | Endorphin | aday değil: konu dışı | Yorumda geçti |
| yorum | Nvidia Lyra | aday değil: konu dışı | Yorumda geçti |
| konuşma 0:00 | Parkur animasyon fikri | aday değil: genel kavram | Genel konu |
## Kareden okunanlar
- 0:02: 'What's the hardest part game development?' başlığı, Unreal Engine sekanserinde LEVEL 1 sahnesi.
- 1:42: ChatGPT sohbeti: parkur haritası promptu, negatif prompt, üretilen inşaat sahası görseli.
- 2:32: Substance Painter: Font Black Ops One, Text Level katmanları.
- 3:04: Tripo: 3D Workspace, Smart Mesh, Triangle topolojisi, poligon sayısı 2000.
- 6:20: Cascadeur Quick Rigging Tool, mixamorig kemikleri, 'Add rig elements'.
- 11:34: Load Video: fps 30, frames 217, süre 00:07.1.
- 15:26: Cascadeur Root motion paneli, Style: Acrobatic; Aaron Nemeth atfı.
- 18:22: Unreal Engine Live Link penceresi, Cascadeur yan yana.
## Belirsizlikler
- OCR ve sözlük eşleşmeleri (Framer Motion, Claude Code, Astro, Hermes Agent vb.) videoda kullanılmadı; yalnız gürültü/yanlış eşleşme sayıldı.
- Karakter üretim modelleri ve Mixamo kullanımı konuşmadan; kare kanıtı sınırlı.
- Yorumlardaki Anijam, Motorica, Endorphin, Nvidia Lyra yalnız izleyici yorumu; videoda kullanılmadı.
- Tripo menüsündeki Segment, Retopo, Texture Upscaler gibi öğeler yalnız menüde göründü.
- Cascadeur sürümü karede 2024.1.2 görünüyor; güncel sürüm belirsiz.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/25 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- yok
## Promptlar
- Parkur sahnesi konsept görseli — Bulutlu şehir silüeti üzerinde, açık tonlu, modüler blok yerleşimli gökdelen çatısı inşaat parkur haritası istenir: beton platformlar, çelik destekler, boşluklar, uzun geçiş kirişi, vinç. Mirror's Edge benzeri akış, Arcane esintili stil. Negatif prompt: karanlık cyberpunk, sis, dağınıklık, gece vb. yok.
