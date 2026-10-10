# Creating 3D Character with AI in 1 Min vs 1 H vs 10 H
## Künye
Creating 3D Character with AI in 1 Min vs 1 H vs 10 H · Stefan 3D AI · süre: 14:24 · en · https://youtu.be/VeOU0FnTjjc · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 58809 tk · claude-haiku-5-5: claude-haiku-5-5 · 82568 tk
## Özet
Stefan, aynı stilize tilki samuray karakterini yapay zekâ ile üç süre sınırıyla (1 dakika, 1 saat, yaklaşık 6-10 saat) üretir. Tripo P2 (Smart Mesh) ile parça parça model üretir, Blender'da birleştirir, AccuRIG ile rig'ler, Unreal Engine 5'e aktarır. Uzun sürümde UV açma, Substance Painter ile PBR, Nano Banana ile göz dokusu, kıyafet ve kuyruk fiziği eklenir. Sonuç: stilize karakterlerde retopoloji yerine doğrudan P2 low poly daha iyi.
## Bölümler
- 0:00 Üç süre sınırı meydan okuması
- 0:29 1 dakikalık sürüm
- 1:28 1 saatlik sürüm
- 5:03 6 saatlik sürüm başlıyor
- 8:11 UV açma ve materyaller
- 10:52 Rig, fizik ve Unreal
- 13:27 Son sonuç ve değerlendirme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Tripo | yok | CLI | yok | Yapay zekâ ile 3B model üretim servisi (Tripo Studio) | 0:29 | I gonna use Tripo and the recent P2 |
| Tripo P2 Smart Mesh | yok | teknik | yok | Quad'lı temiz low poly mesh üreten model; parça parça üretimde kullanıldı | 1:28 | same Tripo P2 with the smart mesh · kanıt: yok |
| Blender | yok | CLI | yok | Parçaları birleştirme, sculpt, UV, ağırlık boyama, rig düzenleme | 3:24 | Blender arayüzü ve tripo parçaları (karede: Blender Layout sekmesi, Scene koleksiyonunda tripo_ adlı parçalar, T-pozunda karakter) |
| Unreal Engine | yok | CLI | yok | Karakteri oyun motorunda çalıştırma, retarget, fizik | 1:20 | Unreal editörü LvL_ThirdPerson (karede: Unreal Editor, Outliner'da DirectionalLight, ExponentialHeightFog, ortada tilki karakter) |
| AccuRIG | yok | CLI | yok | Otomatik rig aracı (AccuRIG 2.1.0) | 4:14 | AccuRIG arayüzü, Rig Body (karede: AccuRIG penceresi, Load Character / Rig Body adımları, eklem noktaları, sayaç 00:54:13) |
| Substance Painter | yok | CLI | yok | PBR materyal, bake, kürk ve altın materyali uygulama | 9:16 | Substance Painter materyal kütüphanesi ve bake ayarları (karede: Texture Set List body/Cloth/gear, Assets'te Fur, Gold Armor materyalleri, Mesh Map Bakers) |
| Nano Banana | yok | CLI | yok | Göz dokusunu üretmek için görsel üretim modeli | 10:13 | generated some cool texture with nano banana |
| Modo | yok | CLI | yok | Referans görselden doku üretme/düzeltme aracı (altyazıda 'Modi'; kare 9:02'de tavşan kulağı AI texturing) | 9:02 | AI texturing aracı tavşan modeli üzerinde katmanlarla · kanıt: kare (karede: Tavşan başı üzerinde Generate paneli, Layers listesi, 'AI TEXTURING' küçük resmi) |
| Hunyuan retopology | yok | CLI | yok | Alternatif retopoloji seçeneği; yalnız anıldı | 5:03 | Tripo retrypology and also Hunyuan retrypology · kanıt: yok |
| Tripo retopology | yok | CLI | yok | Tripo'nun retopoloji özelliği; P2 ile karşılaştırıldı | 5:03 | Tripo retrypology and also · kanıt: yok |
| Blender sculpt modu | yok | teknik | yok | Parçaları birleştirmek için sculpt fırçaları | 3:29 | With Blender sculpting modes or Blender proportional editing · kanıt: yok |
| Proportional editing | yok | teknik | yok | Blender'da orantılı düzenleme ile parça birleştirme | 3:29 | Blender proportional editing that is like super easy |
| Weight Paint | yok | teknik | yok | Kemik ağırlıklarını boyama; sert aksesuarlara %100 ağırlık | 4:24 | Weight Paint modu ve Weights menüsü · kanıt: kare (karede: Blender Weight Paint modu, pelvis grubu için renk gradyanı, Weights menüsü açık) |
| Smart UV Project | yok | teknik | yok | Blender'da UV açma yöntemi (menüde); video notu Tripo'da UV önerir | 8:08 | UV Mapping menüsü (karede: UV Mapping menüsü: Unwrap Angle Based, Unwrap Conformal, Smart UV Project, Cube Projection; kulaklı kafa) |
| Clone brush | yok | teknik | yok | Blender Texture Paint'te doku hatalarını düzeltme | 8:54 | Clone fırçası aktif (karede: Texture Paint modu, Active Tool: Clone, Clone from Paint Slot seçeneği, el modeli) |
| IK Retargeter | yok | teknik | yok | Unreal'de animasyonu karaktere aktarma | 4:36 | Retarget Animations penceresi (karede: Retarget Animations, Source SKM_Quinn_Simple, Target 1houRigged, Batch Export Options) |
| Chaos Cloth | yok | teknik | yok | Unreal'de eşarp/kumaş fiziği | 13:12 | ChaosClothConfig ayarları (karede: Clothing paneli, ChaosClothConfig/ChaosClothSharedConfig, Dynamic Particles, Simulation Time) |
| Physics Asset | yok | teknik | yok | Kuyruk için fizik gövdeleri ve çarpıştırıcılar | 12:52 | Physics asset editörü, kuyruk kemikleri (karede: Physics Asset editörü, kapsül gövdeler, tail01-tail08 kemikleri seçili, Re-generate Bodies) |
| Game Animation Sample | yok | plugin | yok | Unreal parkur animasyon örnek projesi | 12:18 | GameAnimationSample projesi, Traversal Gym (karede: Unreal başlık GameAnimationSample, Outliner'da Traversal Gym, Teleporter_Sender) |
| Fortnite Humanoid template | yok | teknik | yok | Retarget için iskelet şablonu | 4:36 | Using Fortnite Humanoid template for target skeleton (karede: Retarget penceresi alt logunda 'Using Fortnite Humanoid template' satırı) |
| Tripo smart UV | yok | teknik | yok | Tripo'da UV; video notunda artık önerilen yöntem | 7:50 | Ekranda not: I recommend to do UV in Tripo now · kanıt: kare (karede: Altyazı kutusu 'This video recorded before Smart UV release', köşede 'Smart UV AI' küçük resmi) |
| Meshy | yok | CLI | yok | Alternatif 3B üretim servisi; yalnız yorumda geçiyor | açıklama | meshy and tripo which one is better for game |
| Mixamo | yok | CLI | yok | Yorumda önerilen otomatik rig servisi; videoda kullanılmadı | açıklama | throw it into mixamo for auto-rig |
| Third Person template | yok | teknik | yok | Unreal'ın ThirdPerson şablon seviyesi; karakteri test etmek için açıldı (LvL_ThirdPerson). | 1:20 | LvL_ThirdPerson (Play In Editor) · kanıt: kare (karede: Unreal Editor'de yeşil platform üzerinde karakter; Outliner'da LvL_ThirdPerson görünüyor.) |
| UEFN Mannequin | yok | teknik | yok | Retarget kaynağı olarak kullanılan Unreal manken iskeleti (SKM_UEFN_Mannequin). | 12:28 | Success! The IK Retargeter is ready to transfer animation from SKM_UEFN_Mannequin (karede: Retarget Animations penceresinde kaynak iskelet olarak turuncu manken görünüyor.) |
## Açıklama bağlantıları
- https://studio.tripo3d.ai/home?via=stefan&invite_code=GY5YYQ — Tripo Studio, yönlendirme ve davet koduyla · aday: evet (Tripo) · Videoda kullanılan Tripo servisi; via ve invite_code parametresi var; sponsor ifadesi açık değil · sınıf: affiliate
- https://top3d.ai — Yazarın kendi sitesi · aday: hayır · Videoda kullanılmayan referans/tanıtım sayfası · sınıf: diğer
- https://www.learn3d.ai/ — Yazarın 3B yapay zekâ kursu · aday: hayır · Ücretli kurs tanıtımı, izleyicinin kullanacağı araç değil · sınıf: diğer
- https://youtu.be/zp13W8z6WQM — Anılan video · aday: hayır · Başka YouTube videosu, araç değil · sınıf: diğer
- https://youtu.be/1vw39QCcQjg — Anılan video · aday: hayır · Başka YouTube videosu, araç değil · sınıf: diğer
- https://youtu.be/3SFDXcr-dQ4 — Anılan video · aday: hayır · Başka YouTube videosu, araç değil · sınıf: diğer
- https://discord.gg/am7nu68r9Z — Discord topluluk daveti · aday: hayır · Topluluk daveti, araç değil; kapalı/davet gerekebilir · sınıf: diğer · erişilemez: Discord daveti, giriş gerekli
- https://x.com/Stefan_3D_AI — Yazarın X profili · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://www.linkedin.com/in/stefan-3d-ai/ — Yazarın LinkedIn profili · aday: hayır · Sosyal medya profili · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Tripo P2 şu an retopolojiden çok daha iyi, özellikle quad'lı low poly üretiyor | 5:03 | karşılaştırma |
| 1 dakikalık sürüm gerçekte yaklaşık 3 dakika sürdü | 0:29 | sayısal |
| Parçalar 500-1000 poligon aralığında bölünmeli | 2:28 | öneri |
| Tam UV açma yaklaşık 30 dakika sürdü; P2 mesh'i mantıklı olduğu için kolay | 8:11 | sayısal |
| Yeni kullanıcılar bağlantıyla 500 kredi alır | 6:03 | özellik |
| Stilize karakterde doğrudan P2 low poly kullanılmalı; yüksek detaylı high poly varsa uzun yol mantıklı | 13:27 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:29 | Tripo | Tripo | I gonna use Tripo and the recent P2 |
| konuşma 1:28 | Smart Mesh P2 | Tripo P2 Smart Mesh | same Tripo P2 with the smart mesh |
| konuşma 3:29 | Blender sculpt ve proportional editing | Blender sculpt modu | Blender sculpting modes or Blender proportional editing |
| konuşma 3:29 | Blender | Blender | assemble them in Blender quickly |
| konuşma 3:29 | Aku rig | AccuRIG | quickly do the aqua rig |
| konuşma 4:30 | Unreal Engine | Unreal Engine | bringing my character to Unreal Engine |
| konuşma 5:03 | Tripo retopology | Tripo retopology | Tripo retrypology and also |
| konuşma 6:03 | Hunyuan retopology | Hunyuan retopology | Hunyuan retrypology |
| konuşma 8:11 | Modi | Modo | take it to Modi for example |
| konuşma 9:12 | Substance Painter | Substance Painter | it is substance painter for. Materials |
| konuşma 10:13 | Nano Banana | Nano Banana | generated some cool texture with nano banana |
| konuşma 11:52 | 3D AI kursu | aday değil: sponsor/reklam | join my 3D AI course |
| konuşma 12:52 | Unreal fizik ve clothing | Chaos Cloth | They did an update to clothing |
| konuşma 12:52 | Physics bone colliders | Physics Asset | set all these colliders right here in Unreal Engine |
| konuşma 11:52 | Parkour animasyon şablonu | Game Animation Sample | preset for this cool parkour animations |
| kare 4:36 | Fortnite Humanoid template | Fortnite Humanoid template | Using Fortnite Humanoid template for target skeleton |
| kare 4:36 | IK Retargeter | IK Retargeter | IK Retargeter is ready to transfer animation |
| kare 7:50 | Smart UV Tripo notu | Tripo smart UV | I recommend to do UV in Tripo now |
| kare 8:08 | Smart UV Project menüsü | Smart UV Project | UV Mapping menüsünde Smart UV Project |
| kare 8:54 | Clone brush | Clone brush | Clone from Paint Slot |
| kare 4:24 | Weight paint | Weight Paint | Assign from Bone Envelopes |
| kare 0:28 | GPT Image 2 etiketi | aday değil: konu dışı | Tripo arayüzünde yalnız menü etiketi |
| kare 0:28 | DCC Bridge | aday değil: konu dışı | Tripo üst çubuğunda menü düğmesi, kullanılmadı |
| yorum | Meshy | Meshy | meshy and tripo which one is better for game |
| yorum | Mixamo | Mixamo | throw it into mixamo for auto-rig |
| yorum | DarLink AI | aday değil: sponsor/reklam | I write my char bios on DarLink AI |
| yorum | Substance Painter | Substance Painter | set up the PBR in SUBSTANCE PAINTER |
| açıklama | Tripo Studio bağlantısı | Tripo | studio.tripo3d.ai ... via=stefan |
| açıklama | TRIPOCREW indirim kodu | Tripo | Use code TRIPOCREW to get 60% off |
| açıklama | top3d.ai | aday değil: konu dışı | Yazarın tanıtım sitesi |
| açıklama | learn3d.ai | aday değil: sponsor/reklam | Kurs satış sayfası |
| açıklama | Discord daveti | aday değil: konu dışı | discord.gg bağlantısı |
| açıklama | X ve LinkedIn profilleri | aday değil: konu dışı | Sosyal profil bağlantıları |
| açıklama | Anılan 3 YouTube videosu | aday değil: konu dışı | youtu.be bağlantıları |
| kare 9:02 | AI texturing aracı | Modo | Tavşan kulağı üzerinde Generate paneli |
## Kareden okunanlar
- 0:28: Tripo 3D Workspace, Generate Model: HD Model/Smart Mesh, Front/Left/Right/Back girişleri, sayaç 00:00:00
- 4:14: AccuRIG: Rig Body adımı, karakter yüksekliği 196.25 cm, sayaç 00:54:13
- 9:16: Substance Painter: body/Cloth/gear texture set, materyal kütüphanesi, sayaç 02:49:31
- 13:12: Unreal Clothing paneli: ChaosClothConfig, Simulation Time 0.18ms
## Belirsizlikler
- Sözlük eşleşmelerindeki React, Three.js, Cursor, Claude Code vb. videoda gösterilen araçlar değil, OCR/yorum gürültüsü; aday yapılmadı.
- 'Modi' (9:02) büyük olasılıkla Modo; karedeki araç adı net okunmuyor.
- Tripo P2 görsel adı ekranda 'Smart Mesh P2.0 Preview' ve 'GPT Image 2' etiketi görünüyor, kullanımı belirsiz.
- Video 6 saatlik sürümle bitiyor; başlıktaki 10 saat planlanan süre.
- Kurulum komutu videoda gösterilmedi.
- EKSİK: rapor (süre dışı zaman: 00:54:13 > 14:24)
- EKSİK: rapor (süre dışı zaman: 00:54:13 > 14:24)
- EKSİK: rapor (süre dışı zaman: 02:49:31 > 14:24)
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/17 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Tripo'da Smart Mesh P2.0 ile 1 dakikalık tek model üretimi — araçlar: Tripo, Smart Mesh P2.0
- 2. adım — Tripo'da texture üretimi (Texture, ikinci adım) — araçlar: Tripo
- 3. adım — Modeli Unreal Engine 5'e aktarıp ThirdPerson şablonunda test — araçlar: Unreal Engine 5, Third Person template
- 4. adım — 1 saatlik versiyon: modeli Tripo'da parçalara ayırıp her parçayı ayrı üretme ve poligon sayısı denemeleri — araçlar: Tripo, Smart Mesh P2.0
- 5. adım — Parçaları Blender'da birleştirme (sculpt ve proportional editing) — araçlar: Blender
- 6. adım — Hızlı rig: AccuRIG ile iskelet oluşturma ve el/parmak hizalama — araçlar: AccuRIG
- 7. adım — Rigid aksesuarlara 100% ağırlık boyama — araçlar: Blender
- 8. adım — Unreal'e aktarma, materyal ayarı ve animasyonun controller'a bağlanması — araçlar: Unreal Engine 5
- 9. adım — 6 saatlik versiyon: ek parçalar üretme, geometri düzeltme ve scarf'ı tek yüzeye çevirme — araçlar: Tripo, Smart Mesh P2.0, Blender
- 10. adım — UV açma (Unwrap Angle Based, Smart UV Project seçenekleri) ve Tripo Smart UV önerisi — araçlar: Blender, Tripo Smart UV
- 11. adım — Yeni UV'ye renk texture'ı bake etme ve texture düzeltme (clone brush) — araçlar: Blender
- 12. adım — PBR materyalleri (fur, altın süsler) uygulama ve bake — araçlar: Substance Painter
- 13. adım — Gözleri yeniden yapma: küre ve Nano Banana texture'ı — araçlar: Blender, Nano Banana
- 14. adım — AccuRIG ile karakter rig'i ve aksesuar ağırlık boyama — araçlar: AccuRIG, Blender
- 15. adım — Unreal'e aktarma, IK Retargeter ile parkour animasyonlarını hedef iskelete taşıma — araçlar: Unreal Engine 5, IK Retargeter, Fortnite Humanoid template, Game Animation Sample, UEFN Mannequin
- 16. adım — Unreal'da Physics Asset ile collider ayarları ve Chaos Cloth ile scarf/kuyruk fiziği — araçlar: Physics Asset, Chaos Cloth, Unreal Engine 5
- 17. adım — Final testi: Unreal'de karakterin hareket ve fizik kontrolü — araçlar: Unreal Engine 5
## Promptlar
- yok
