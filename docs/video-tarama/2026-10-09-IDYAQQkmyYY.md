# Animation Layers | Cascadeur 2026.2 Feature Highlights
## Künye
Animation Layers | Cascadeur 2026.2 Feature Highlights · Cascadeur - The Future of Animation · süre: 3:27 · en-orig · https://youtu.be/IDYAQQkmyYY · şema 2
motor: parti 2026-10-09-short-43 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 44862 tk · claude-haiku-5-5: claude-haiku-5-5 · 82076 tk
## Özet
Cascadeur 2026.2 sürümünün öne çıkan özelliklerini tanıtan video: toplamalı animasyon katmanları (alfa), interpolasyonda easing, karakter dayanak noktalarının çarpışma mesh'lerine uyumu, iyileştirilmiş çarpışma delinme temizliği ve fizik filtresi, AutoPhysics uygulama seçeneği (tüm kareler/yalnız anahtarlar), PySide ile özel arayüz, FBX'ten doku/çoklu materyal içe aktarma ve Çince/Japonca/Korece dil paketleri.
## Bölümler
- 0:00 Animasyon katmanları (Animation Layers)
- 0:49 Interpolasyonda easing
- 1:17 Dayanak noktalarının çarpışma mesh'lerine uyumu
- 1:52 Çarpışma delinme temizliği
- 2:15 Delinme temizliği fizik filtresi ve AutoPhysics uygulama seçeneği
- 2:32 PySide ile özel arayüz
- 2:47 FBX materyal/doku içe aktarma
- 3:08 Dil paketleri
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Cascadeur | yok | CLI | yok | Üzerinde çalışılan 3B karakter animasyon yazılımı; 2026.2 sürümü tanıtılıyor. | 0:00 | Pencere başlığında Cascadeur ve Cascy.casc sahnesi görünüyor. (karede: Cascadeur penceresi, Cascy karakteri, Scene settings paneli) |
| Animation Layers | yok | teknik | yok | Toplamalı (additive) katmanlarla yıkıcı olmayan animasyon düzenleme; alfa sürümü. | 0:04 | Animation Layers penceresinde Base layer, ardından Additive layer 0 ve 1 görünüyor. (karede: Animation Layers paneli, Additive layer 0/1 ve Base layer) |
| Easing | yok | teknik | yok | Yörünge şeklini değiştirmeden anahtar kareler arası aralığı ayarlayan timeline tutamaçları. | 1:00 | We can adjust the spacing on the intervals without changing the shape of the trajectories. |
| AutoPosing | yok | teknik | yok | El/ayak kontrolcüleri çarpıştırıcılarla etkileşip ofset ve dönüşü otomatik ayarlıyor; dört ayaklı iyileştirmeleri var. | 1:41 | Kinematic mesh collision davranışı kayanın üzerine eklenip el kayaya oturtuluyor. (karede: UES_Manny sahnesinde sarı tel kafesli kaya, Kinematic mesh collision özelliği) |
| Collision Penetration Cleaning | yok | teknik | yok | Geometri kesişmelerini tek tıkla temizleyen araç; fizik filtresi olarak da var. | 1:52 | Scene settings'te Clean Floor/Kinematic/Dynamic Collisions ve Penetration Offset görünüyor. (karede: Collision Penetration Cleaning bölümü, KoreanDance sahnesi) |
| AutoPhysics | yok | teknik | yok | Fizik ayarlarıyla animasyonu düzelten araç; sonuç tüm karelere ya da yalnız anahtarlara uygulanır. | 2:29 | APPLY AUTOPHYSICS penceresinde All Frames ve Only keys düğmeleri var. (karede: Apply AutoPhysics iletişim kutusu) |
| PySide | yok | teknik | yok | Python API'ye entegre edilen, özel arayüz penceresi oluşturmayı sağlayan kütüphane (QML). | 2:32 | PYSIDE SHOWCASE penceresi sürgülerle ve Cascadeur PySide önizlemesiyle görünüyor. (karede: PySide Showcase penceresi, Intensity/Hue/Animation speed sürgüleri) |
| Python API | yok | teknik | yok | Cascadeur API'si; özel araç ve betikler için genişletildi. | 2:01 | We've made a huge progress extending the Cascadeur's API. |
| FBX | yok | teknik | yok | FBX içe aktarmada dokular ve çoklu materyal yuvaları otomatik aktarılıyor; CASC'a gömülüyor. | 2:49 | Demonstration.fbx kurt modeli ve M_wolf materyalleri Object properties'te listeleniyor. (karede: Demonstration.fbx sahnesi, kurt mesh'i, Material M_wolf_* listesi) |
| Dil paketleri | yok | teknik | yok | Çince (Basitleştirilmiş/Geleneksel), Japonca ve Korece arayüz desteği. | 3:08 | Dil menüsünde English, Chinese Simplified/Traditional, Japanese, Korean seçenekleri var. · kanıt: kare (karede: Sağ üstte dil açılır menüsü) |
| Tween machine | yok | teknik | yok | Cascadeur menü çubuğunda ve panellerinde görünen ara kare aracı. | 0:02 | Menü çubuğunda Tween machine ve Window menüsünde Tween machine listeleniyor. (karede: Window menüsünde Tween machine seçeneği) |
| Kinematic mesh collision | yok | teknik | yok | Kinematic mesh'lere çarpışma davranışı eklenmesi; AutoPosing hizalaması için gerekli | 1:41 | Add kinematic mesh collision behaviour. (karede: Alt sol köşede 'Add kinematic mesh collision behaviour.' ipucu yazısı; sahnede sarı çerçeveli kaya mesh'i görünüyor.) |
## Açıklama bağlantıları
- https://cascadeur.com/download — Cascadeur indirme sayfası · aday: evet (Cascadeur) · İzleyicinin kullanabileceği araç indirme sayfası; videoda gösterilen Cascadeur. · sınıf: diğer
- https://cascadeur.com/help/category/319 — Sürüm değişiklikleri yardım sayfası · aday: hayır · Dokümantasyon sayfası, ayrı bir araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kaydırıcı (slider) kontrolü | PySide Showcase'de Intensity, Hue, Animation speed ve Preview scale değerlerini ayarlayan kaydırıcılar (karede: Sol panelde CONTROLS sekmesinde dört renkli kaydırıcı; her birinin yanında yüzde/derece değeri rozeti var.) | 2:32 | kare |
| Açılır liste (dropdown) seçici | Color theme seçimi: Ocean, Sunset, Forest, Mono (karede: Color theme alanında 'Forest' seçili; açılır listede Ocean, Sunset, Forest, Mono seçenekleri görünüyor.) | 2:43 | kare |
| Parıltı (glow) efekti | Ortadaki yuvarlatılmış kare etrafında yumuşak ışıma (karede: Sağdaki canlı önizlemede 'Cascadeur PySide' yazılı yuvarlatılmış kare, çevresinde bulanık daireler ve ışıma görünüyor.) | 2:32 | kare |
| Bulanık arka plan daireleri (blur) | Önizleme alanında yarı saydam, bulanık dairelerin hareketli arka planı (karede: Koyu arka planda farklı boyutta yarı saydam daireler, önizleme kartının çevresinde konumlanmış.) | 2:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Toplamalı katmanlar yığılabilir; IK, FK ve global interpolasyon arasında geçilebilir. | 0:00 | özellik |
| Animasyon katmanları mocap temizliğinde karışım ve ağırlık üzerinde tam kontrol sağlar. | 0:00 | öneri |
| Çarpışma etkileşimi yalnız dinamik olmayan nesnelerle çalışır, karakterler arası değil. | 1:00 | özellik |
| Delinme temizleme büyük aralıklarda uzun sürebilir ama sonuç beklemeye değer. | 2:01 | özellik |
| Delinme temizleme fizik filtresi olarak eklendi ve uzuvların zemine düşmesini önler. | 2:01 | özellik |
| Sahne kaydedilince dokular CASC dosyasına gömülür. | 2:01 | özellik |
| Cascadeur web sitesinden ücretsiz indirilebilir. | 3:04 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Animation Layers | Animation Layers | You can now create additive layers and make non-destructive changes. |
| konuşma 0:00 | Mocap cleanup | aday değil: genel kavram | Animation layers are extremely useful for things like mocap cleanup. |
| konuşma 0:00 | IK/FK interpolasyon | aday değil: başka adayın parçası (Animation Layers) | switch between IK, FK, and global interpolation in them. |
| konuşma 0:49 | Easing | Easing | We've introduced a feature called easing. |
| konuşma 1:17 | Fulcrum points / çarpışma mesh | AutoPosing | hands and feet will now align with the scene geometry. |
| konuşma 1:52 | Penetration cleaning | Collision Penetration Cleaning | fix any geometry intersections with a single click. |
| konuşma 2:15 | AutoPhysics | AutoPhysics | snapping into physics now prompted to apply to all frames or key frames. |
| konuşma 2:32 | PySide | PySide | by integrating PySide, we allow users to create custom UI. |
| konuşma 2:49 | FBX import | FBX | When importing FBX, it will automatically import the textures. |
| konuşma 2:59 | CASC dosyası | aday değil: başka adayın parçası (Cascadeur) | it will bake the textures into the CASC file. |
| konuşma 3:08 | Çince, Japonca, Korece | Dil paketleri | support for multiple languages, namely Chinese, Japanese, and Korean. |
| kare 1:40 | MCP menüsü | aday değil: konu dışı | Scripts menüsünde MCP listelenmiş, kullanılmıyor. |
| kare 1:40 | Meshy menüsü | aday değil: konu dışı | Scripts menüsünde Meshy listelenmiş, kullanılmıyor. |
| kare 0:02 | Tween machine | Tween machine | Window menüsünde Tween machine işaretli. |
| kare 0:00 | Cascadeur | Cascadeur | Pencere başlığı Cascadeur. |
| açıklama | Python API | Python API | Custom UI in Python API via Pyside (QML). |
| açıklama | Dil paketleri | Dil paketleri | We've added support for language packs. |
| açıklama | https://cascadeur.com/download | Cascadeur | Açıklamadaki indirme bağlantısı. |
| açıklama | https://cascadeur.com/help/category/319 | aday değil: konu dışı | Yardım/sürüm notu sayfası. |
| linkli sayfa | YouTube oynatma listesi ve videolar | aday değil: konu dışı | cascadeur.com sayfalarından linklenen diğer YouTube videoları. |
| yorum | iClone | aday değil: konu dışı | Yorumda iClone ile ilişki soruluyor, videoda kullanılmıyor. |
| yorum | Marvelous Designer | aday değil: konu dışı | Yorumcu Marvelous Designer videosu istiyor. |
| yorum | Unreal Engine | aday değil: konu dışı | Yorumda root motion önizlemesi için anılıyor. |
| yorum | Cascadeur Mobile | aday değil: konu dışı | Yorumcu mobil sürüm için özellik öneriyor. |
| yorum | Blender | aday değil: konu dışı | Yorumda anılan hesap adı, videoyla ilgisiz. |
## Kareden okunanlar
- 0:04: Animation Layers penceresi: Base layer.
- 0:10: Animation layers sekmesi: Additive layer 0, Base layer.
- 0:13: Additive layer 1, Additive layer 0, Base layer.
- 0:37: Run_Xsens_007_add_steps.casc sahnesi, Animation layers sekmesi.
- 1:40: Scripts menüsü: Animation Scripts, MCP, Meshy, Quick export, Rig additional.
- 1:41: Add kinematic mesh collision behaviour bildirimi.
- 2:29: APPLY AUTOPHYSICS: All Frames / Only keys.
- 2:32: PYSIDE SHOWCASE: Intensity 68%, Hue 200°, Animation speed 1.00x, Preview scale 100%, Color theme Ocean.
- 2:43: Color theme seçenekleri: Ocean, Sunset, Forest, Mono.
- 3:08: Dil menüsü: English, Chinese Simplified, Chinese Traditional, Japanese, Korean.
- 3:17: DOWNLOAD FOR FREE NOW AT cascadeur.com!
## Belirsizlikler
- Scripts menüsündeki MCP ve Meshy öğeleri yalnız menüde görünüyor, videoda kullanılmıyor; aday yapılmadı.
- Sözlükteki Make, Stitch, Slack, Hermes Agent, Spline vb. eşleşmeler bulanık eşleşme; videoda kullanılmıyor.
- Tween machine yalnız menü/sekme olarak görünüyor; kullanımı gösterilmiyor, adaylığı zayıf.
- Katmanlar alfa sürümde; birleştirme (merge) adımı karede net görülmedi.
## Atlanan segment oranı
0/4 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| cascadeur.com | 3:17 | ekran | evet |
| https://cascadeur.com/download | açıklama | açıklama | evet |
| https://cascadeur.com/help/category/319 | açıklama | açıklama | hayır |
## İş akışı
- yok
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
