# World Building in Blender - Ian Hubert
## Künye
World Building in Blender - Ian Hubert · Blender · süre: 35:44 · en-orig · https://youtu.be/whPWKecazgM · şema 2
motor: parti 2026-10-10-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (58)
kareler: girdi ≤40000 jeton için 60→58
claude-sonnet-5-5: claude-sonnet-5-5 · 61988 tk · claude-haiku-5-5: claude-haiku-5-5 · 86294 tk
## Özet
Ian Hubert'in Blender Conference konuşması: fotoğrafları görüntü dokusu olarak düşük poligonlu geometriye kamera projeksiyonuyla kaplayıp hızlı, gerçekçi ortamlar kurma, fSpy ile kamera eşleme, yeniden aydınlatma, Prospect ve kişisel projelerden örnekler, dünya kurma (world building), referans kullanma, prosedürel dokular ve 'Lazy Tutorial' güve simülasyonu.
## Bölümler
- 0:00 Giriş
- 1:00 Görüntü dokuları
- 1:56 Düşük poligon
- 3:13 UV açma
- 5:54 Specular haritaları
- 6:36 Yeniden aydınlatma
- 10:44 Bu hile mi?
- 11:47 Blender bir sanat ortamı
- 13:22 Boolean ile inşa
- 14:35 Hatalardan öğrenme
- 15:33 Dünya kurma nedir
- 16:05 Beynin yeniden bağlanması
- 16:51 Modelleyici deneyimi
- 19:13 Kişisel wiki
- 20:07 Prospect
- 21:50 Toz
- 22:16 Dynamo
- 24:03 Lazy Tutorial
- 27:12 Wild Rye
- 32:27 Birds Canals
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Blender | yok | CLI | yok | Tüm işin yapıldığı 3B yazılım; konuşmacı onu güçlü bir sanat ortamı olarak över. | 10:44 | Blender'ı hayatında kullandığı en iyi program olarak anlatıyor. |
| Image Textures | yok | teknik | yok | Fotoğrafları yüzeylere doku olarak kaplayıp ışık ve dokuyu hazır almak. | 1:00 | Görüntü dokularını sevdiğini ve ışığın içine pişmiş olduğunu anlatıyor. |
| Camera Projection Mapping | yok | teknik | yok | Fotoğrafı kameradan düşük poligonlu geometriye yansıtma; fotogrametri benzeri. | 1:00 | Buna kamera projeksiyon haritalama dediğini söylüyor. |
| Project from View | yok | teknik | yok | UV'leri kamera görünümünden yansıtarak fotoğrafı modele oturtma. | 4:13 | Görünümden projeksiyon yapıp elde edilen sonucu anlatıyor. |
| UV Unwrapping | yok | teknik | yok | Modeli açıp dokuyu eşleştirme; 15 yıl kaçındığı teknik. | 3:13 | UV açmanın gücünden ve 15 yıl uzak kalmasından söz ediyor. |
| Import Images as Planes | yok | plugin | yok | Fotoğrafı tek yüzeyli düzlem olarak içe aktarma; duvar için kullanıldı. | 3:13 | Import images as planes özelliğini sevdiğini söylüyor. |
| Sun lamp | yok | teknik | yok | Işığı güneş lambasına çevirip sahneyi aydınlatma. | 4:13 | Lambayı güneş lambasına çeviriyoruz diyor. |
| Cycles | yok | teknik | yok | Render motoru; OCR'da Render Engine Cycles görünüyor. | 4:30 | Render ayarları panelinde Cycles seçili. (karede: Render özellikleri panelinde 'Render Engine Cycles', Sampling, Light Paths, Film, Performance başlıkları.) |
| Principled BSDF | yok | teknik | yok | Kaplanmış dokuların materyal düğümü. | 5:18 | Materyal panelinde Principled BSDF yüzeyi görünüyor. (karede: Material panelinde Surface: Principled BSDF, Base Color görüntü dokusu, Subsurface alanları.) |
| Roughness / Clamp | yok | teknik | yok | Fotoğrafı roughness'a bağlayıp specular haritası gibi kullanma. | 5:54 | Specular haritanın elle boyanmadığını, roughness'a clamp ile bağlandığını söylüyor. · kanıt: yok |
| fSpy | yok | CLI | yok | Kamerayı fotoğrafa göre hizalayan ücretsiz bağımsız program (eski adı Blam). | 6:36 | Eskiden blam, şimdi f spy; kamerayı hizalayan ücretsiz program. |
| Blam | yok | plugin | yok | fSpy'ın eski adı; kamera eşleme eklentisi, kabin sahnesinde kullanıldı. | 7:36 | Kamerayı hizalamayı kolaylaştırmak için 'blam' yöntemini kullandığını söylüyor. |
| Emission plane | yok | teknik | yok | Fotoğrafı yayan düzleme çevirip CG nesneleri yerleştirme. | 6:36 | Emission plane yapıp başka CG nesneler koyabileceğini söylüyor. |
| Grass Essentials | yok | plugin | yok | Blender Guru'nun çim paketi; sahnede çim eklemek için. | 6:36 | Blender Guru grass essentials'ı çok sevdiğini söylüyor. |
| Noise modifier | yok | teknik | yok | Araba sürüşü animasyonunda gürültü modifier'ları; Graph Editor'da kanatlar için de. | 7:36 | Animasyon için çok sayıda noise modifier kullandığını söylüyor. |
| Car Rig Pro | yok | plugin | yok | Tek eğriyle fiziği yöneten ve tekerlekleri zemine oturtan araba rig eklentisi. | 9:38 | Add-on car rig pro'nun bir eğriyle fizik yönettiğini söylüyor. |
| Displacement / depth map | yok | teknik | yok | Arka planı derinlik haritasıyla yer değiştirilmiş düz yüzey yapma. | 9:38 | Arka planın derinlik haritasıyla displace edilmiş düz bir şey olduğunu söylüyor. · kanıt: yok |
| Boolean | yok | teknik | yok | 2002'deki şehirde bina ve park yapılarında boolean kullanımı. | 13:22 | Şehrin boolean ile yapıldığını, kapalı garajın iki küp olduğunu söylüyor. |
| Subsurf | yok | teknik | yok | Başlangıç düzeyinde herkesin açtığı alt bölme yüzeyi. | 14:35 | Öğrencilerin subsurf açıp extrude ettiğini anlatıyor. |
| Blend Swap | yok | ipucu | yok | Itfaiye musluğu/tabela varlığını paylaştığı site. | 16:51 | Bu asset'in Blend Swap'ta serbest olduğunu söylüyor. |
| Personal wiki | yok | iş akışı | yok | Dünya kurma için bağlantılı düğümlerden oluşan kişisel wiki. | 19:13 | Kişisel wiki yapılabileceğini ve kendi sitesinde bir tane olduğunu söylüyor. |
| Particle System | yok | teknik | yok | Güve emitter'ı; koleksiyon olarak render. | 25:03 | Emitter objesine particle system verip koleksiyon olarak render ettiriyor. |
| Boids | yok | teknik | yok | Güvelerin lambayı takip etmesi için Boid Brain kuralı. | 25:10 | Physics Type açılır listesinde Boids seçiliyor; Boid Brain'de Separate/Flock. (karede: Particle Settings Physics Type listesi: None, Newtonian, Keyed, Boids, Fluid; sonraki karede Instance Collection 'moths'.) |
| Graph Editor | yok | teknik | yok | Kanatlara noise modifier eklemek için kullanılan editör. | 24:03 | Kanatları çılgın yapmak için noise modifier'ı graph editor'da tuttuğunu söylüyor. |
| Voronoi Texture | yok | teknik | yok | Yağmur dalgalarını yer değiştirme ile üretmek için kullanılan doku düğümü. | 29:13 | Peynir gibi görünen düğümün Voronoi olduğunu söylüyor. |
| Procedural textures | yok | teknik | yok | Doğadaki düzen/rastgeleliği simüle eden prosedürel doku. | 29:13 | Prosedürel dokulara girdiğini ve Blender'ın araçlarını anlatıyor. |
| Generated box mapping | yok | teknik | yok | Roketlerde UV yerine üretilmiş kutu eşleme koordinatı. | 31:16 | 2011 konuşmasında yemin ettiği generated box mapping'i anlatıyor. · kanıt: yok |
| Photoscans | yok | ipucu | yok | Fotoğraf taramaları kullanma tavsiyesi. | 31:16 | Fotoğraf ve photo scan kullanın diyor. |
| ColorRamp | yok | teknik | yok | Gri tonlu değeri renk geçişine çeviren Blender düğümü; Voronoi çıktısını maskelemek için kullanılıyor. | 30:00 | ColorRamp düğümü shader düğüm ağında okunuyor. (karede: Shader düzenleyicide Voronoi Texture'dan ColorRamp'e bağlı düğüm ağı görünüyor.) |
| Photoshop | yok | teknik | yok | Adobe'nin görüntü düzenleme yazılımı; konuşmacı geleneksel doku boyama iş akışını anlatırken adını veriyor, gösterilmiyor. | 3:13 | you export that into like Photoshop and you do your paint over |
## Açıklama bağlantıları
- https://fund.blender.org — Blender Geliştirme Fonu bağış ve sponsor sayfası · aday: evet (Blender) · Alan adı videoda kullanılan Blender'ı adlandırıyor. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Kapak/çöp kutusu kapağı yalnızca yaklaşık 65 poligon. | 1:56 | sayısal |
| Görüntü dokulu yaklaşımda ışık ve doku önceden pişmiştir; yol izleme gerekmez. | 1:00 | özellik |
| fSpy ücretsiz bağımsız programdır ve kamerayı hizalar. | 6:36 | özellik |
| Konuşmacı 2002'de şehrini üç binayla ve boolean ile kurmuş. | 13:22 | sayısal |
| Moth Lazy Tutorial yüz binlerce kez izlenmiş. | 25:03 | sayısal |
| Prospect'te yaklaşık 2000 çekime toz eklendi. | 21:50 | sayısal |
| Referans kullanmak yanlış zihinsel kavramı atlamanızı sağlar; referans kullanın. | 28:12 | öneri |
| Yalnızca bir şey yapmaya çalışıyorsanız fotoğraf ve photoscan kullanın. | 31:16 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Ian Hubert / Blender Conference konuşması | aday değil: konu dışı | Konuşmacı kendini tanıtıyor. |
| ekran 0:00 | Intel 'brought to you by' | aday değil: sponsor/reklam | Ekranda brought to you by (intel). |
| ekran 0:00 | conference.blender.org | Blender | Alan adı ekranda görünüyor. |
| konuşma 1:00 | Image textures | Image Textures | Görüntü dokularını sevdiğini söylüyor. |
| konuşma 1:00 | Photogrammetry / camera projection mapping | Camera Projection Mapping | Buna kamera projeksiyon haritalama diyor. |
| konuşma 1:56 | Star Wars podracing, Fight Club, Matrix | aday değil: konu dışı | Sinema örnekleri. |
| konuşma 3:13 | UV unwrapping | UV Unwrapping | UV açmanın gücünü anlatıyor. |
| konuşma 3:13 | Photoshop | aday değil: genel kavram | Boyama için Photoshop'a aktarma örneği. |
| konuşma 3:13 | Import images as planes | Import Images as Planes | Özelliği sevdiğini söylüyor. |
| konuşma 4:13 | Sun lamp | Sun lamp | Lambayı güneşe çevirir. |
| konuşma 4:13 | Project from view | Project from View | Fotoğrafı görünümden yansıtır. |
| kare 4:30 | Cycles | Cycles | Render Engine Cycles. |
| kare 5:18 | Principled BSDF | Principled BSDF | Materyal panelinde görünüyor. |
| konuşma 5:54 | Specular maps / roughness clamp | Roughness / Clamp | Roughness'a clamp ile bağlandı. |
| konuşma 6:36 | fSpy | fSpy | Kamera hizalama programı. |
| konuşma 6:36 | Blam | Blam | fSpy'ın eski adı. |
| konuşma 6:36 | Emission plane | Emission plane | CG nesneleri yerleştirmek için. |
| konuşma 6:36 | Blender Guru grass essentials | Grass Essentials | Çim eklemek için kullanıldı. |
| konuşma 7:36 | Noise modifier | Noise modifier | Araba animasyonunda. |
| konuşma 8:37 | Ed Sheeran müzik videosu | aday değil: konu dışı | Proje örneği. |
| konuşma 9:38 | Car Rig Pro | Car Rig Pro | Araba eklentisi. |
| konuşma 9:38 | Depth map displacement | Displacement / depth map | Arka plan için. |
| konuşma 13:22 | Boolean | Boolean | Şehir boolean ile kuruldu. |
| konuşma 14:35 | Subsurf | Subsurf | Öğrenciler subsurf açıyor. |
| konuşma 16:51 | Blend Swap | Blend Swap | Asset paylaşımı. |
| konuşma 16:51 | Wikipedia | aday değil: genel kavram | İtfaiye musluğu araştırması. |
| konuşma 19:13 | Personal wiki | Personal wiki | Dünya kurma notları. |
| konuşma 20:07 | Prospect (Netflix) | aday değil: konu dışı | VFX yaptığı film. |
| konuşma 24:03 | Graph Editor | Graph Editor | Noise modifier burada. |
| kare 25:02 | Particle System | Particle System | Particle Settings paneli. |
| kare 25:10 | Boids | Boids | Physics Type Boids. |
| konuşma 27:12 | Blender Guru Grass Essentials | Grass Essentials | Çim paketi. |
| kare 30:02 | Voronoi Texture | Voronoi Texture | Manuel sayfası ve düğüm. |
| konuşma 29:13 | Prosedürel dokular | Procedural textures | Çim/kozalak desenleri. |
| konuşma 31:16 | Generated box mapping | Generated box mapping | 2011 konuşmasından. |
| konuşma 31:16 | Photoscans | Photoscans | Tavsiye. |
| açıklama | https://fund.blender.org | Blender | Alan adı Blender'ı adlandırır. |
| linkli sayfa fund.blender.org | Intel, NVIDIA, AMD, Adobe, BlenderKit vb. sponsor logoları | aday değil: sponsor/reklam | Fon sayfasında kurumsal sponsor listesi. |
| yorum | Photoshop (You suck at Photoshop) | aday değil: konu dışı | Yorumcu benzer eğitime atıf yapıyor. |
| yorum | Corridor Digital, Captain Disillusion | aday değil: konu dışı | Yorumlarda anılıyor. |
| sözlük | React, Next.js, Claude vb. eşleşmeleri | aday değil: konu dışı | Yanlış pozitif. |
## Kareden okunanlar
- 0:00: Ekranda 'brought to you by (intel)' ve conference.blender.org yazısı görünüyor.
- 2:10: Blender durum çubuğunda Faces:0/65 ve Tris:13 ile Matrix sahnesi karşılaştırması.
- 4:30: Render Engine Cycles, Device CPU, Sampling paneli.
- 6:52: Anahat penceresinde 'calibration.fspy' kamera/obje adı.
- 7:58: Anahat/Grafikte 'Grass Giant Wild Rye Master' yazısı.
- 8:22: 'geometry camera matching addon' yazısı.
- 25:10: Particle Settings Physics Type: None, Newtonian, Keyed, Boids, Fluid.
- 25:18: Boid Brain, Instance Collection 'moths', Rule Fuzziness 0.500.
- 30:02: Blender manuelinde Voronoi Node sayfası.
## Belirsizlikler
- Kare listesinde 66 giriş var ama 58 görsel eklendi; kareler tam eşlenemedi, zamanlar OCR'dan alındı.
- OCR'daki 'Quick D-NOISE' (5:30) yalnız menüde görünüyor, kullanıldığı doğrulanmadı.
- Sözlük eşleşmeleri (React, Next.js, Claude vb.) yanlış pozitif; videoyla ilgisi yok.
- Prospect'in Netflix'te olması ve Ed Sheeran klibi anıldı ama araç değil.
- Altyazı otomatik; isimler (fSpy, Blam, Car Rig Pro) ses tanımadan geliyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/43 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| conference.blender.org | 0:00 | ekran | hayır |
| https://fund.blender.org | açıklama | açıklama | evet |
## İş akışı
- yok
## Promptlar
- yok
