# Turn any Video into Game Ready Animations with Quickmagic AI and Unreal Engine 5.7
## Künye
Turn any Video into Game Ready Animations with Quickmagic AI and Unreal Engine 5.7 · Defonten · süre: 8:17 · en-orig · https://youtu.be/OHPrmKitwAg · şema 2
motor: parti 2026-10-09-short-42 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 49411 tk · claude-haiku-5-5: claude-haiku-5-5 · 77707 tk
## Özet
Defonten, odasında çektiği basit videoları QuickMagic AI ile hareket yakalama (mocap) animasyonuna çeviriyor. Videoyu yükleyip Unreal 5.6 formatını seçiyor, FBX olarak indiriyor, Unreal Engine'e aktarıyor ve IK Retargeter ile ücretsiz Paragon karakterlerine (Murdock, Wraith, Gideon) uyarlıyor. Sonuçların yine de temizlik gerektirdiğini belirtiyor.
## Bölümler
- 0:00 Giriş ve yükleme
- 2:39 İşleme ve önizleme
- 3:48 Unreal'e aktarma
- 5:22 Animasyon retargeting
- 7:25 Son değerlendirme ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| QuickMagic AI | yok | CLI | yok | Videodan yapay zekâ ile hareket yakalama yapan web platformu (AI Mocap) | 0:00 | use Quick Magic AI platform to come up with really cool looking animations |
| Unreal Engine 5.7 | yok | teknik | yok | Animasyonların içe aktarıldığı ve retarget edildiği oyun motoru | 3:48 | let's head over to Unreal. in latest versions of Unreal it became so much easier |
| IK Retargeter | yok | teknik | yok | Unreal'de animasyonu kaynak iskeletten hedef karaktere aktaran araç | 5:34 | Ekran metni: IK Retargeter ready; Retarget Animations penceresi (karede: kanıttan) Ekran metni: IK Retargeter ready; Retarget Animations penceresi |
| Paragon karakterleri | yok | teknik | yok | Hedef olarak kullanılan ücretsiz karakterler (Murdock, Wraith, Gideon) | 3:48 | I have a bunch of Paragon characters downloaded. They are free. · kanıt: yok |
| Unreal 5.6 FBX formatı | yok | teknik | yok | QuickMagic çıkış formatı, doğru kemik adlarıyla dışa aktarılır | 1:00 | let's choose this Unreal 5.6 format · kanıt: yok |
| VLC media player | yok | CLI | yok | Kaydedilen Landing.mp4 videosunu önizlemek için kullanıldı | 0:56 | Pencere başlığı Landing.mp4 - VLC media player (karede: kanıttan) Pencere başlığı Landing.mp4 - VLC media player |
| Chrome | yok | CLI | yok | QuickMagic sitesinin açıldığı tarayıcı (önerilen tarayıcı) | 0:42 | Ekranda Recommended Using Chrome Browser yazısı (karede: kanıttan) Ekranda Recommended Using Chrome Browser yazısı |
| Mixamo | yok | teknik | yok | Yorumda özel karakter rig'i için önerilen servis | açıklama | Yorumda Mixamo karakteri rig'leme önerisi; QuickMagic çıkış listesinde de görünür |
| Blender | yok | teknik | yok | Yorumda özel karakter için sözü edilen araç | açıklama | Yorum: Blender karakterini Unreal'e aktarıp animasyon uygulamak |
| Paragon Murdock | yok | teknik | yok | Unreal'ın ücretsiz Paragon karakterlerinden biri; retarget hedef iskeleti olarak kullanılıyor. | 5:22 | let's select our Murdoch for the target skeletal mesh |
| Fortnite Humanoid | yok | teknik | yok | IK Retargeter'ın kaynak iskelet için otomatik seçtiği şablon. | 5:24 | Using Fortnite Humanoid template for source skeleton. (karede: Log penceresinde 'Using Fortnite Humanoid template for source skeleton.' satırı) |
| UE4 Mannequin | yok | teknik | yok | IK Retargeter'ın hedef iskelet için kullandığı UE4 mankeni şablonu. | 5:39 | Using UE4 Mannequin template for target skeleton. (karede: Log penceresinde 'Using UE4 Mannequin template for target skeleton.' satırı) |
| Interchange | yok | teknik | yok | Unreal'ın içe aktarma çerçevesi; FBX import'ta varsayılan pipeline olarak kullanılıyor. | 4:43 | Default Assets Pipeline (InterchangeGenericAssetsPipeline) (karede: Import penceresinde 'Default Assets Pipeline (InterchangeGenericAssetsPipeline)' yazısı ve Asset Type ayarları) |
## Açıklama bağlantıları
- https://www.quickmagic.ai/register?code=Defonten — QuickMagic kayıt bağlantısı (referans kodlu) · aday: evet (QuickMagic AI) · İzleyicinin kullanabileceği araç; videoda kullanılan QuickMagic. Referans kodu var. · sınıf: affiliate
- https://learn.defonten.com/MasteringWorldCreator — World Creator masterclass kursu · aday: hayır · Yazarın kendi kursu; videoda kullanılmıyor, konu dışı. · sınıf: diğer
- https://www.youtube.com/watch?v=cypqGpxAX_0 — YouTube videosu · aday: hayır · Başka bir video bağlantısı, araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Gezinme çubuğu ve kahraman bölümü (navbar, hero section) | QuickMagic ana sayfasında üst menü (AI Mocap, AI Avatar, API, Documents, Pricing, Blog), Quick Login düğmesi, iskelet ve video yan yana gösterimi (karede: Koyu sayfada üstte QUICKMAGIC menüsü, mavi Quick Login düğmesi, solda renkli iskelet, sağda dans eden kişinin videosu) | 0:42 | kare |
| Adım göstergesi (stepper) | Video Editing, Format Selection, Function Selection üç adımlı akış ve Next/Reset düğmeleri (karede: Üstte üç noktalı adım çubuğu, mavi Next ve sarı Reset düğmeleri) | 1:38 | kare |
| Modal pencere (modal dialog) | Motion Generating: başlık, tam vücut/el seçimi, FPS, ilk poz ve Generate Now (karede: Ortada Motion Generating penceresi, solda kadın görseli, sağda form seçenekleri) | 2:13 | kare |
| İlerleme çubuğu (progress bar) | Yükleniyor ekranında %18 ilerleme çubuğu (karede: QUICKMAGIC logosu altında mavi çubuk 18% ve Loading yazısı) | 2:54 | kare |
| Kart ızgarası (card grid) | My Project sayfasında proje kartları, sırada bekleyen videoda dönen yükleme (karede: Landing, Cartoonish, Shooting, Entering, Exiting_2 kartları; ilk kartta video is in line) | 2:48 | kare |
| Kenar çubuğu gezinmesi (sidebar navigation) | Solda AIGC, My Project, AI Mocap menüsü ve V Coins kutusu (karede: Sol dikey menü, mor AI Avatar düğmesi, V Coins 259 kutusu) | 1:38 | kare |
| Bildirim (toast) | Üstte yeşil Upload Successfully mesajı (karede: My Project üstünde yeşil Upload Successfully bildirimi) | 2:45 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ücretsiz kullanıcılar en fazla 30 saniyelik ve 100 MB'lık video yükleyebilir. | 0:42 | sayısal |
| Unreal formatı doğru kemik adlarıyla dışa aktarıldığı için retargeting için doğru yoldur. | 1:00 | öneri |
| Sonuç yüzde yüz kusursuz değildir; yine temizlik ve düzeltme gerekir. | 2:39 | karşılaştırma |
| Unreal'in son sürümlerinde karakter retarget etmek çok daha kolay. | 3:48 | karşılaştırma |
| Tahmini maliyet 2.9 V; 24/30 FPS'te 1 saniye video 1 V-Coin. | 2:15 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Quick Magic AI platformu | QuickMagic AI | use Quick Magic AI platform to come up with really cool looking animations |
| altyazı 1:00 | Unreal 5.6 formatı | Unreal 5.6 FBX formatı | let's choose this Unreal 5.6 format |
| altyazı 3:48 | Unreal Engine | Unreal Engine 5.7 | let's head over to Unreal |
| altyazı 3:48 | Paragon karakterleri | Paragon karakterleri | bunch of Paragon characters downloaded. They are free |
| kare 5:34 | IK Retargeter | IK Retargeter | IK Retargeter ready; Retarget Animations penceresi |
| kare 0:56 | VLC media player | VLC media player | Landing.mp4 - VLC media player |
| kare 0:42 | Chrome tarayıcı | Chrome | Recommended Using Chrome Browser |
| kare 1:45 | Mixamo çıkış formatı | Mixamo | Output Format listesinde Mixamo kartı; yorumda da öneriliyor |
| yorum | Blender | Blender | Yorum: Blender karakterini Unreal'e aktarmak |
| yorum | Maya Time Editor | aday değil: konu dışı | Sahip yorumunda temizlik için Maya anılıyor, videoda kullanılmıyor |
| yorum | Attaku tools eklentisi | aday değil: konu dışı | Yorumcu Attaku tools plugin'ini öneriyor, videoda gösterilmiyor |
| açıklama | Müzik High Impact - ArcticFoxMusic | aday değil: konu dışı | Credits: Music: High Impact by ArcticFoxMusic |
| açıklama | learn.defonten.com World Creator kursu | aday değil: konu dışı | Sabit yorumda kurs bağlantısı |
| açıklama | YouTube bağlantısı cypqGpxAX_0 | aday değil: konu dışı | Açıklamada üçüncü bağlantı |
| kare 1:45 | Unity Anim, C4D, CC&iClone, Roblox R15, VMD-TDA formatları | aday değil: konu dışı | Yalnızca çıkış formatı listesinde görünüyor, kullanılmıyor |
| kare 3:51 | Paragon Murdock, Wraith, Gideon | Paragon karakterleri | Content Browser'da ParagonMurdock, ParagonWraith, ParagonGideon klasörleri |
## Kareden okunanlar
- 0:42: QuickMagic AI Mocap yükleme sayfası, V Coins 259, Output Format listesi (Unreal 5.6, Girl FBX, Boy FBX, Mixamo, Unreal 4, Unreal 5.5), serbest kullanıcı sınırı 30 sn ve 100M
- 1:45: Output Format listesinde VMD-TDA, Roblox R15, CC&iClone, C4D, Unity Anim; Only Face ücretli abonelere
- 2:13: Motion Generating: Title Landing, Full Body, Hand, 30 FPS, Original Pose, Export Format Unreal 5.6, Estimated Cost 2.9 V
- 2:48: My Project: Landing kartı video is in line; V Coins 230; Total 6
- 5:23: Retarget Animations: kaynak Landing_Unreal5_6, hedef Murdock; IK Retargeter ready; Export Animations
- 5:03: Content Browser'da QuickMagic klasörü; animasyon 902 kare, 30 fps, 30.07 sn; kaynak dosya Landing_Unreal5.6.fbx
## Belirsizlikler
- Video başlığında Unreal Engine 5.7 geçiyor ancak konuşmada Unreal 5.6 formatı ve 'latest versions' deniyor; sürüm teyit edilemedi.
- Sözlük eşleşmeleri (Three.js, Claude, Cursor, Framer vb.) videoda kullanılmıyor; OCR gürültüsü olarak değerlendirildi.
- Açıklamadaki üçüncü YouTube bağlantısının (cypqGpxAX_0) içeriği bilinmiyor.
- Yorumlardaki Attaku tools eklentisi videoda kullanılmıyor, aday yapılmadı. Maya yorumda geçiyor, videoda kullanılmıyor.
- Wraith ve Gideon'ın ayrı kareleri çoğu OCR'da bulanık; Gideon 'pirate skeleton' olarak anlatılıyor.
- Karede Hand seçeneğinin işaretli görünmesi konuşmadaki 'full body' ile tam örtüşmüyor.
- Müzik: High Impact (ArcticFoxMusic) açıklamada kredi olarak geçiyor; araç değil.
## Atlanan segment oranı
0/10 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.quickmagic.ai/register?code=Defonten | açıklama | açıklama | evet |
| https://learn.defonten.com/MasteringWorldCreator | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=cypqGpxAX_0 | açıklama | açıklama | hayır |
| quickmagic.ai/home | 0:32 | ekran | evet |
| quickmagic.ai/capture/index/uploadPc | 0:42 | ekran | evet |
| quickmagic.ai/capture/index/myProPc | 2:45 | ekran | evet |
| https://learn.defonten.com/MasteringWorldCreator | açıklama | yorum | hayır |
## İş akışı
- 1. adım — Videoları odada önceden çekmek (Landing, Shooting, Cartoonish vb.) — araçlar: yok
- 2. adım — QuickMagic sitesinde kayıt olup AI Mocap bölümüne girmek — araçlar: QuickMagic AI, Chrome
- 3. adım — Landing.mp4 videosunu dosya gezgininden seçip içe aktarmak, VLC'de önizlemek — araçlar: QuickMagic AI, VLC media player
- 4. adım — Giriş ve çıkış noktalarını platformda belirlemek (en fazla 30 sn) — araçlar: QuickMagic AI
- 5. adım — Çıkış formatı olarak Unreal 5.6'yı seçip mavi kutuya sürüklemek — araçlar: QuickMagic AI, Unreal 5.6 FBX formatı
- 6. adım — Tam vücut, 30 FPS, Original Pose ayarlarıyla Generate Now ile göndermek — araçlar: QuickMagic AI
- 7. adım — My Project'te işlemenin bitmesini beklemek ve önizlemeyi açmak — araçlar: QuickMagic AI
- 8. adım — FBX dosyasını ZIP olarak indirmek — araçlar: QuickMagic AI
- 9. adım — Unreal'de QuickMagic ve AnimationsRetargeted klasörlerini oluşturmak — araçlar: Unreal Engine 5.7
- 10. adım — FBX'i varsayılan ayarlarla, animasyon içe aktarma açık şekilde import etmek — araçlar: Unreal Engine 5.7
- 11. adım — İçe aktarılan animasyonu önizleyip kontrol etmek — araçlar: Unreal Engine 5.7
- 12. adım — Sağ tık ile Retarget Animations açıp hedef olarak Murdock'u seçmek — araçlar: IK Retargeter, Paragon karakterleri
- 13. adım — Retarget edilen animasyonu AnimationsRetargeted klasörüne export etmek — araçlar: IK Retargeter
- 14. adım — Aynı animasyonu Wraith ve Gideon'a retarget edip dışa aktarmak — araçlar: IK Retargeter, Paragon karakterleri
- 15. adım — Sonuçları sahnede oynatıp gözden geçirmek, karikatürvari hareketi göstermek — araçlar: Unreal Engine 5.7
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
