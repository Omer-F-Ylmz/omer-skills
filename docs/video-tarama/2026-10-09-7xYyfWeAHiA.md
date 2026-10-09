# Cheap AI Mocap that Actually Works - QuickMagic.Ai, Chaos Destruction, and Metahumans in UE5
## Künye
Cheap AI Mocap that Actually Works - QuickMagic.Ai, Chaos Destruction, and Metahumans in UE5 · Charlie Driscoll - Unreal Engine Filmmaking · süre: 19:43 · en-orig · https://youtu.be/7xYyfWeAHiA · şema 2
motor: parti 2026-10-09-short-42 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 148860 tk · claude-haiku-5-5: claude-haiku-5-5 · 234475 tk
## Özet
Charlie Driscoll, QuickMagic.Ai ile tek akıllı telefon kamerasından çekilen uzun bir koşu planını hareket yakalamaya (mocap) çevirir. Animasyonu Unreal Engine 5'e aktarıp bir MetaHuman'a retarget eder, ortaçağ savaş sahnesi kurar, Chaos Destruction ile kale yıkımı ve Niagara patlamaları ekler. Sonda aynı çekimi Sora ile üretmeye çalışır ve sonuçların zayıf kaldığını söyler.
## Bölümler
- 0:00 Giriş
- 0:37 QuickMagic'in gizli özelliği
- 2:55 Takip çekimi konsepti
- 3:09 Animasyonu yakalama
- 4:08 QuickMagic ile işleme
- 5:19 UE5'te MetaHuman'a uygulama
- 7:37 MetaHuman Performance Capture eğitimi
- 8:27 Rokoko Headrig ile QuickMagic
- 8:53 Sahneyi kurma ve Chaos Destruction
- 14:25 Arka plan karakterleri ve mocap paketleri
- 15:06 Final çekimi
- 15:37 Ek savaş sahnesi çekimleri
- 16:17 Çekimi Sora ile yeniden üretme denemesi
- 18:16 Üretken yapay zekâ üzerine düşünceler
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| QuickMagic.Ai | yok | iş akışı | yok | Tek kameralı, tarayıcı tabanlı yapay zekâ mocap servisi; hareketli kamerayı telafi eder. | 1:38 | easily the best single camera moap solution I have used or seen |
| Unreal Engine 5 | yok | iş akışı | yok | Sahne kurma, retarget, sequencer ve render için ana motor. | 0:00 | using Unreal Engine 5 we will build an entire medieval battle scene |
| MetaHuman | yok | iş akışı | yok | Animasyonun uygulandığı dijital insan karakter. | 6:19 | target skeletal mesh which can be any of the metahuman skeletons |
| Move Pro | yok | iş akışı | yok | Move AI'ın çok kameralı mocap çözümü; kanalda çoğunlukla kullanılıyor. | 0:37 | I use mostly move Pro the multi camera solution from move AI |
| Move One | yok | iş akışı | yok | Move AI'ın tek kameralı çözümü; karşılaştırma için denendi. | 1:38 | I've tried move one from move Ai |
| Radical Motion | yok | iş akışı | yok | Tek kameralı mocap çözümü; titremeyi azalttı ama ayak kayması vardı. | 1:38 | I've also tried radical motion which was really good |
| Rokoko Vision | yok | iş akışı | yok | Ücretsiz tek kameralı mocap çözümü; yazara göre zayıf. | 1:38 | the free roko Vision solution was pretty terrible · kanıt: yok |
| Rokoko Headrig | yok | iş akışı | yok | Yüz yakalama için takılan baş donanımı; QuickMagic'le birlikte denendi. | 8:27 | I recorded this wearing a roko head rig |
| Samsung S23 Ultra | yok | iş akışı | yok | Koşu çekimini kaydeden telefon. | 3:09 | my friend filmed me with my Samsung Note 23 ultro · kanıt: yok |
| Unreal Engine 4 Mannequin | yok | iş akışı | yok | QuickMagic çıktı iskeleti olarak seçildi. | 4:08 | I chose the Unreal Engine 4 mannequin |
| IK Retargeter | yok | teknik | yok | Animasyonu UE4 iskeletinden MetaHuman iskeletine aktaran retarget penceresi. | 5:58 | Retarget Animations penceresi, kaynak ve hedef mesh seçimi · kanıt: kare (karede: Retarget Animations penceresi, kaynak ve hedef mesh seçimi) |
| Level Sequence | yok | teknik | yok | Karakter, kamera ve efektlerin zamanlandığı sequencer. | 6:19 | we now want to create a new level sequence up here |
| LOD Sync | yok | teknik | yok | Forced LOD'u 0 yaparak MetaHuman'ı en yüksek LOD'da kilitleme. | 6:19 | change it from -1 to0 which will lock your metahuman into the highest LOD |
| MetaHuman Animator | yok | iş akışı | yok | Yüz animasyonunu temizlemek için kullanılan araç. | 7:37 | cleaning up the animation using metahuman animator for the face |
| Chaos Destruction | yok | teknik | yok | Kaleyi parçalamak için Unreal'in fizik ve yıkım sistemi. | 9:54 | unreal engines chaos physics engine chaos is super powerful |
| Fracture Mode | yok | teknik | yok | Static mesh'i cluster yöntemiyle parçalayıp geometry collection oluşturma. | 10:54 | change from selection mode to fracture mode |
| Anchor Field | yok | teknik | yok | Parçalanan bölümleri sabitleyen kısıt alanı. | 10:54 | these yellow volumes around which are called anchor fields |
| Bomb Field | yok | teknik | yok | Patlamanın yerini ve zamanını belirleyen alan. | 11:56 | pink orbs which are called bomb fields |
| Niagara | yok | teknik | yok | Patlama ve top mermisi izi için parçacık efektleri. | 13:56 | I just added some Niagara particle explosions to the impact areas |
| Adobe Premiere Pro | yok | iş akışı | yok | Kamera zamanlamasını kontrol etmek için render referansı olarak kullanıldı. | 12:00 | Adobe Premiere Pro 2025 penceresi, Running klibi zaman çizelgesinde (karede: kanıttan) Adobe Premiere Pro 2025 penceresi, Running klibi zaman çizelgesinde |
| Castle (Fab) | yok | iş akışı | yok | Köprülü modüler kale ortamı varlığı. | 8:38 | Fab sayfası: Castle, Kyrylo Sibiriakov (karede: kanıttan) Fab sayfası: Castle, Kyrylo Sibiriakov |
| Medieval Armour | yok | iş akışı | yok | Polyphoria'nın ortaçağ zırh paketi; MetaHuman'larla uyumlu. | 8:44 | Fab sayfası: Medieval Armour, Polyphoria (karede: kanıttan) Fab sayfası: Medieval Armour, Polyphoria |
| Modular Medieval NPC V2 | yok | iş akışı | yok | Kral dahil MetaHuman'lara uyan modüler kıyafet paketi; kral kıyafeti kullanıldı. | 8:56 | Fab sayfası: Modular Medieval NPC V2, Polyphoria (karede: kanıttan) Fab sayfası: Modular Medieval NPC V2, Polyphoria |
| Mocap - Pirates Animation Library | yok | iş akışı | yok | Kılıç dövüşü animasyonu için kullanılan 63 korsan mocap animasyonu paketi. | 14:10 | Fab sayfası: Mocap - Pirates Animation Library, Raised By Monsters · kanıt: kare (karede: Fab sayfası: Mocap - Pirates Animation Library, Raised By Monsters) |
| Run For Your Life | yok | iş akışı | yok | Reallusion'ın arka plan karakterleri için kullanılan kaçış animasyonu paketi. | 14:16 | YouTube: Escaping Movements For Action Films - Run For Your Life, Reallusion (karede: kanıttan) YouTube: Escaping Movements For Action Films - Run For Your Life, Reallusion |
| Sora | yok | iş akışı | yok | OpenAI'ın video modeli; aynı çekimi üretmek için denendi. | 16:17 | newest video model Sora anyway let's see if we can prompt |
| ChatGPT Pro | yok | iş akışı | yok | Sora erişimi için yükseltilen abonelik. | 16:17 | I upgraded to Chachi BT Pro |
| Proj Prod Chaos Destruction | yok | iş akışı | yok | Chaos yıkımı ayrıntılı anlatan, yazarın önerdiği YouTube eğitimi. | 10:18 | Realistic Destruction Effect / Unreal Engine 5, Proj Prod (karede: kanıttan) Realistic Destruction Effect / Unreal Engine 5, Proj Prod |
| Cascadeur | yok | iş akışı | yok | Yorumlarda QuickMagic animasyonunu temizlemek için önerilen araç. | açıklama | You can use Cascadeur to clean the animation from Quickmagic |
| Artlist | yok | iş akışı | yok | Ses efektleri ve müziğin lisanslandığı servis. | açıklama | All Sound Effects and Music licensed from Artlist.io |
| ElevenLabs | yok | iş akışı | yok | Sahnede ses/diyalog için kullanılan ses dosyası kaynağı. | 7:58 | Sequencer'da ElevenLabs_2024-08-30 adlı ses dosyası (karede: kanıttan) Sequencer'da ElevenLabs_2024-08-30 adlı ses dosyası |
| Field System | yok | teknik | yok | Chaos yıkımını Anchor Field ve Bomb Field ile bağlayan ve zamanlayan UE sistemi. | 11:56 | I add these pink orbs which are called bomb fields |
| Retarget Animations | yok | teknik | yok | UE5 animasyon retarget penceresi; UE4 Mannequin animasyonunu MetaHuman iskeletine aktarır. | 5:19 | retarget animation which will bring up this window |
| UE4 Mannequin | yok | teknik | yok | QuickMagic'te seçilen ve retarget kaynak iskeleti olarak kullanılan UE4 manken iskeleti. | 4:08 | I chose the Unreal Engine 4 mannequin |
| Sora ile sürekli takip çekimini üretmek | yok | prompt | yok | Sora için uzun, ayrıntılı prompt: bir kral kaleden panik içinde köprü üzerinde kaçar, geriye bakar, çevresinde mermiler duvarları patlatır, köylüler ve şövalyeler dövüşür, tek sürekli takip kamerası. | 16:08 | kaynak: kare |
## Açıklama bağlantıları
- https://discord.com/invite/thedarkestage — Kanalın Discord topluluğu · aday: hayır · Topluluk daveti; araç değil. · sınıf: diğer
- https://bit.ly/3K9ryCX — Kısaltılmış bağlantı; hedefi açıklamadan anlaşılmıyor · aday: hayır · Hedefi belirsiz kısa bağlantı. · sınıf: diğer
- https://patreon.com/CharlieDriscoll — Kanalın Patreon sayfası · aday: hayır · Ücretli topluluk sayfası. · sınıf: diğer · erişilemez: ücretli topluluk
- https://www.quickmagic.ai?code=clmew4 — QuickMagic.Ai yönlendirme kodlu bağlantı · aday: evet (QuickMagic.Ai) · Videoda kullanılan mocap servisi; kod parametresi var. · sınıf: affiliate
- https://www.fab.com/listings/6151fbba-0ad5-49d7-83a3-d6050b6fe8e0 — Fab varlık sayfası (büyük olasılıkla Castle) · aday: evet (Castle (Fab)) · Videoda kullanılan varlık paketi; hangisi olduğu doğrulanamadı. · sınıf: diğer
- https://www.fab.com/listings/45e6fa2e-518e-456c-aed6-422ea9437874 — Fab varlık sayfası · aday: evet (Medieval Armour) · Videoda kullanılan varlık paketi. · sınıf: diğer
- https://www.fab.com/listings/45c5e237-9b79-4180-9281-10cfef092919 — Fab varlık sayfası · aday: evet (Modular Medieval NPC V2) · Videoda kullanılan varlık paketi; hangisi olduğu doğrulanamadı. · sınıf: diğer
- https://www.fab.com/listings/4eb02787-c32d-4a10-b36b-bb237cffd738 — Fab varlık sayfası · aday: evet (Modular Medieval NPC V2) · Videoda kullanılan varlık paketi; hangisi olduğu doğrulanamadı. · sınıf: diğer
- https://actorcore.reallusion.com/3d-motion/pack/run-for-your-life?info=1 — Reallusion ActorCore 'Run For Your Life' hareket paketi · aday: evet (Run For Your Life) · Arka plan karakterlerinde kullanılan animasyon paketi. · sınıf: diğer
- https://www.fab.com/listings/98c8264f-5eeb-4d9e-a668-33eab83e3393 — Fab varlık sayfası · aday: evet (Mocap - Pirates Animation Library) · Videoda kullanılan varlık paketi; hangisi olduğu doğrulanamadı. · sınıf: diğer
- https://www.fab.com/listings/f9df4890-75d6-4f7e-a0b2-6774ba87c641 — Fab varlık sayfası · aday: evet (Mocap - Pirates Animation Library) · Videoda kullanılan varlık paketi; hangisi olduğu doğrulanamadı. · sınıf: diğer
- https://www.northwoodsrevolution.com/contact — Kanalın iletişim sayfası · aday: hayır · İletişim sayfası; araç ya da servis değil. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Move Pro lisansı yılda 7.000 dolar tutuyor. | 0:37 | sayısal |
| QuickMagic en iyi tek kameralı mocap çözümü; ayak kilidi güçlü, hareketli kamerayı telafi ediyor. | 1:38 | karşılaştırma |
| Kamera yana sabit bakarsa karakter koşu bandında gibi görünüyor; arkadan veya önden takip çalışıyor. | 3:09 | öneri |
| Çekim yaklaşık 28 V coin, yaklaşık 86 sent maliyetliydi. | 4:08 | sayısal |
| Yazar Sora çıktılarından etkilenmedi; metinden videonun kendi animasyonu kadar kesin olmadığını söylüyor. | 17:17 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Unreal Engine 5 | Unreal Engine 5 | using Unreal Engine 5 we will build an entire medieval battle scene |
| konuşma 0:37 | Move Pro / Move AI | Move Pro | I use mostly move Pro the multi camera solution from move AI |
| konuşma 1:38 | Move One | Move One | I've tried move one from move Ai |
| konuşma 1:38 | Radical Motion | Radical Motion | I've also tried radical motion which was really good |
| konuşma 1:38 | Rokoko Vision | Rokoko Vision | the free roko Vision solution was pretty terrible |
| konuşma 3:09 | Samsung telefon | Samsung S23 Ultra | my friend filmed me with my Samsung Note 23 ultro |
| kare 4:06 | QuickMagic giriş ekranı | QuickMagic.Ai | Log in sayfası, Continue with Google |
| konuşma 4:08 | UE4 Mannequin | Unreal Engine 4 Mannequin | I chose the Unreal Engine 4 mannequin |
| kare 0:10 | Mixamo çıktı seçeneği | aday değil: başka adayın parçası (QuickMagic.Ai) | Output Format listesinde Mixamo kutusu |
| konuşma 5:19 | Retarget | IK Retargeter | right click on your animation and go up here to retarget animation |
| konuşma 6:19 | Level sequence | Level Sequence | we now want to create a new level sequence up here |
| konuşma 6:19 | LOD sync | LOD Sync | in the hierarchy scroll down to the LOD sync |
| konuşma 7:37 | MetaHuman Performance Capture eğitimi | MetaHuman Animator | cleaning up the animation using metahuman animator for the face |
| konuşma 8:27 | Rokoko head rig | Rokoko Headrig | I recorded this wearing a roko head rig |
| kare 8:38 | Castle Fab sayfası | Castle (Fab) | Castle / Fab, Kyrylo Sibiriakov |
| kare 8:44 | Medieval Armour Fab sayfası | Medieval Armour | Medieval Armour, Polyphoria |
| kare 8:56 | Modular Medieval NPC V2 Fab sayfası | Modular Medieval NPC V2 | Modular Medieval NPC V2 / Fab |
| konuşma 9:54 | Chaos physics | Chaos Destruction | unreal engines chaos physics engine chaos is super powerful |
| kare 9:42 | Chaos GDC 2019 demosu | aday değil: konu dışı | YouTube: Chaos High-Performance Physics and Destruction System GDC 2019 |
| konuşma 9:54 | The Matrix Awakens demosu | aday değil: konu dışı | vehicles from The Matrix demo; kullanılmadı, yalnızca anıldı |
| kare 10:18 | Proj Prod YouTube eğitimi | Proj Prod Chaos Destruction | Realistic Destruction Effect / Unreal Engine 5 |
| konuşma 10:54 | Fracture modu | Fracture Mode | change from selection mode to fracture mode |
| konuşma 10:54 | Anchor fields | Anchor Field | yellow volumes ... called anchor fields |
| konuşma 11:56 | Bomb fields | Bomb Field | pink orbs which are called bomb fields |
| kare 12:00 | Adobe Premiere Pro | Adobe Premiere Pro | Adobe Premiere Pro 2025 penceresi |
| konuşma 13:56 | Niagara | Niagara | I just added some Niagara particle explosions |
| kare 14:10 | Pirates mocap kütüphanesi | Mocap - Pirates Animation Library | Fab: Mocap - Pirates Animation Library |
| kare 14:16 | Run For Your Life paketi | Run For Your Life | Reallusion YouTube: Run For Your Life |
| konuşma 14:25 | MetaHuman arka plan karakterleri | MetaHuman | these were all metahumans |
| konuşma 16:17 | Sora | Sora | newest video model Sora anyway |
| kare 0:26 | ChatGPT Pro | ChatGPT Pro | ChatGPT Pro, prompt metni |
| kare 7:58 | ElevenLabs ses dosyası | ElevenLabs | ElevenLabs_2024-08-30 ses dosyası sequencer'da |
| açıklama | Artlist.io | Artlist | All Sound Effects and Music licensed from Artlist.io |
| açıklama | Discord | aday değil: konu dışı | Topluluk Discord daveti |
| açıklama | Patreon | aday değil: konu dışı | patreon.com/CharlieDriscoll |
| yorum | Cascadeur | Cascadeur | You can use Cascadeur to clean the animation from Quickmagic |
| yorum | Veo 2, Kling, Runway | aday değil: konu dışı | Yorumda alternatif video üreticileri; videoda kullanılmadı |
| yorum | Meshy, Rodin, Tripo, Trellis, Meshtron | aday değil: konu dışı | Yorumda 3B üretici araçlar; videoda kullanılmadı |
| kare 1:20 | Xsens Awinda / iClone 8 kısa videosu | aday değil: konu dışı | Giriş kesitinde başka mocap örnekleri |
| kare 6:16 | Hazır klasör adları (ArmyVFX, ModularOrcs vb.) | aday değil: konu dışı | Content Browser'da klasör listesi, kullanılmadı |
| linkli sayfa | youtu.be/Aq7M1G30tf8 | aday değil: konu dışı | Fab sayfasından bağlanan video |
## Kareden okunanlar
- 0:10: QuickMagic arayüzü: Output Format listesi (Boy FBX, Girl FBX, Mixamo, Unreal 4, VMD, BIP), V Coins 34.
- 4:32: Motion Generating penceresi: Full Body, Original Pose, Moving Camera, Unreal 4, Estimated Cost 28 V.
- 5:12: Unreal Import Content penceresi; Skeleton None, dosya adı 20241206_165409_Unreal.fbx.
- 6:36: Sequencer'da MetaHuman_ControlRig (BP_Stephane) ve Body/Face kontrol rig izleri.
- 6:48: BP_Stephane detaylarında LODSync bölümü görünüyor.
- 10:50: Fracture aracı ipucu: Voronoi diyagramı ile 'clustered' desen.
- 12:00: Adobe Premiere Pro 2025: Running0003 klibi, Lumetri Color paneli.
- 14:10: Fab: Mocap - Pirates Animation Library, 63 korsan animasyonu.
- 16:00: Sora arayüzü: 480p, 20s seçenekleri, Recent galerisi.
## Belirsizlikler
- Açıklamadaki Fab bağlantılarının hangi pakete ait olduğu doğrulanamadı; eşleştirmeler tahmindir.
- bit.ly bağlantısının hedefi bilinmiyor.
- youtu.be/Aq7M1G30tf8 bağlantısı yalnızca bağlantılı sayfalarda geçiyor; hedefi doğrulanmadı.
- Sözlük eşleşmeleri (Framer Motion, Astro, Claude Code vb.) videoda kullanılmayan, bulanık eşleşmelerdir; aday yapılmadı.
- Cascadeur yalnızca yorumda öneri olarak geçiyor, videoda kullanılmadı; yine de aday olarak listelendi.
- Altyazıdaki 'Note 23 ultro' ifadesi ekranda 'John's S23 Ultra' olarak görünüyor.
- Altyazıdaki 'mostly move Pro' ifadesi otomatik çeviri hatası olabilir.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/26 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| QUICKMAGIC.AI | 0:34 | ekran | evet |
| www.uekits.com | 8:38 | ekran | hayır |
| https://discord.com/invite/thedarkestage | açıklama | açıklama | hayır |
| https://bit.ly/3K9ryCX | açıklama | açıklama | hayır |
| https://patreon.com/CharlieDriscoll | açıklama | açıklama | hayır |
| https://www.quickmagic.ai?code=clmew4 | açıklama | açıklama | evet |
| https://www.fab.com/listings/6151fbba-0ad5-49d7-83a3-d6050b6fe8e0 | açıklama | açıklama | evet |
| https://www.fab.com/listings/45e6fa2e-518e-456c-aed6-422ea9437874 | açıklama | açıklama | evet |
| https://www.fab.com/listings/45c5e237-9b79-4180-9281-10cfef092919 | açıklama | açıklama | evet |
| https://www.fab.com/listings/4eb02787-c32d-4a10-b36b-bb237cffd738 | açıklama | açıklama | evet |
| https://actorcore.reallusion.com/3d-motion/pack/run-for-your-life?info=1 | açıklama | açıklama | evet |
| https://www.fab.com/listings/98c8264f-5eeb-4d9e-a668-33eab83e3393 | açıklama | açıklama | evet |
| https://www.fab.com/listings/f9df4890-75d6-4f7e-a0b2-6774ba87c641 | açıklama | açıklama | evet |
| https://www.northwoodsrevolution.com/contact | açıklama | açıklama | hayır |
| https://youtu.be/Aq7M1G30tf8 | açıklama | açıklama | hayır |
| https://youtu.be/7xYyfWeAHiA | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=OHPrmKitwAg&t=57s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=4OHDiZgctqs&t=2s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=LZLFvwGo_wU | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=-6G3FbbQ7Uw | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=BGlwW93TUb0 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=EyqxCOtqkIg | açıklama | açıklama | hayır |
| gmail.com (satıcı e-posta alan adı) | 8:38 | ekran | hayır |
## İş akışı
- 1. adım — Arkadaş telefonla koşuyu arkadan/önden takip ederek çekti — araçlar: Samsung S23 Ultra
- 2. adım — Klibi QuickMagic'e yükleyip T-pose ile rol tespiti yapıldı — araçlar: QuickMagic.Ai
- 3. adım — UE4 Mannequin iskeleti seçildi; tam vücut ve eller, hareketli kamera, UE4 çıktısı ayarlandı — araçlar: QuickMagic.Ai, Unreal Engine 4 Mannequin
- 4. adım — Animasyon oluşturulup FBX olarak indirildi — araçlar: QuickMagic.Ai
- 5. adım — FBX Unreal Engine 5'e iskelet 'None' ile aktarıldı — araçlar: Unreal Engine 5
- 6. adım — Animasyon MetaHuman iskeletine retarget edilip dışa aktarıldı — araçlar: IK Retargeter, MetaHuman
- 7. adım — Level Sequence oluşturulup MetaHuman eklendi, Forced LOD 0 yapıldı — araçlar: Level Sequence, LOD Sync, MetaHuman
- 8. adım — Control rig izleri silinip animasyon vücut izine uygulandı — araçlar: Level Sequence
- 9. adım — Yüz için MetaHuman Animator ve Rokoko Headrig denemesi gösterildi — araçlar: MetaHuman Animator, Rokoko Headrig
- 10. adım — Castle, Medieval Armour ve Modular Medieval NPC V2 ile sahne kuruldu — araçlar: Castle (Fab), Medieval Armour, Modular Medieval NPC V2
- 11. adım — Kule ve duvarlar Fracture Mode ile parçalandı, geometry collection kaydedildi — araçlar: Chaos Destruction, Fracture Mode
- 12. adım — Anchor field ve bomb field yerleştirilip gecikmeler Premiere referansıyla ayarlandı — araçlar: Anchor Field, Bomb Field, Adobe Premiere Pro
- 13. adım — Niagara patlama ve top izleri sequencer'a eklendi — araçlar: Niagara, Level Sequence
- 14. adım — Arka plan MetaHuman'lar korsan ve Run For Your Life animasyonlarıyla donatıldı — araçlar: Mocap - Pirates Animation Library, Run For Your Life, MetaHuman
- 15. adım — Final çekim ve ek savaş çekimleri render edildi — araçlar: Unreal Engine 5
- 16. adım — Aynı çekim Sora ile farklı süre ve çözünürlüklerde denendi — araçlar: Sora, ChatGPT Pro
## Promptlar
- Sora ile sürekli takip çekimini üretmek — Sora için uzun, ayrıntılı prompt: bir kral kaleden panik içinde köprü üzerinde kaçar, geriye bakar, çevresinde mermiler duvarları patlatır, köylüler ve şövalyeler dövüşür, tek sürekli takip kamerası.
