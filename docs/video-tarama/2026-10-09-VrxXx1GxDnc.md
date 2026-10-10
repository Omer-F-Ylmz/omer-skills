# My new ui concept Softies, made in figma and blender 3d
## Künye
My new ui concept Softies, made in figma and blender 3d · Andrii Bachinskyi · süre: 1:02 · en-orig · https://youtu.be/VrxXx1GxDnc · şema 2
motor: parti 2026-10-09-short-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 17511 tk · claude-haiku-5-5: claude-haiku-5-5 · 30704 tk
## Özet
Andrii Bachinskyi, 'Softies' adlı oyuncak markası için bir arayüz konsepti tasarımını gösteriyor. Figma'da gradyanlı çerçeve, başlık, çizgiler ve büyük numara hazırlanıyor. Blender'da Geometry Nodes ile Grid, Delete Geometry, Instance on Points, Noise Texture, Trim Curve ve Curve to Mesh kullanılarak animasyonlu çizgiler üretiliyor. BlenderKit'ten sevimli bir kedi modeli ekleniyor, kamera animasyonuyla render alınıyor ve sonuç birleştiriliyor. Yazar yorumda 'Soft' yazanlara Figma ve Blender dosyalarını gönderiyor.
## Bölümler
- 0:00 Figma'da tasarım: gradyanlı çerçeve, başlık, çizgiler, numara
- 0:14 Açıklama metni ve büyük başlık
- 0:20 Blender'da Geometry Nodes: düzlem, grid, silme
- 0:27 Çizgileri instance olarak ekleme, mesh to curve
- 0:30 Noise ile bükme, Trim Curve ile animasyon
- 0:36 Curve to mesh, subdivide, materyal
- 0:43 Layout, render ayarı, BlenderKit kedisi
- 0:53 Render ve birleştirme
- 0:56 Yorum yaz, dosyaları al
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Figma | yok | CLI | yok | Arayüz tasarımı: gradyanlı çerçeve, metin, çizgiler ve numara için tasarım aracı. | 0:00 | Frame with a gradient in Figma is a good starting point |
| Blender | yok | CLI | yok | 3B sahne, geometri düğümleri, materyal ve render için kullanılan 3B yazılım. | 0:20 | Now go to Blender, creating a plane and clicking geometric nodes |
| Geometry Nodes | yok | teknik | yok | Çizgileri prosedürel üreten ve animasyonlayan Blender düğüm sistemi. | 0:24 | Düğüm editörü başlığında Plane.006 > GeometryNodes > Geometry Nodes.004 yolu var. (karede: kanıttan) Düğüm editörü başlığında Plane.006 > GeometryNodes > Geometry Nodes.004 yolu var. |
| Grid node | yok | teknik | yok | Düzlemin geometrisini ızgaraya çeviren düğüm. | 0:24 | Size X, Size Y, Vertices X, Vertices Y alanlı düğüm Delete Geometry'ye bağlı. (karede: kanıttan) Size X, Size Y, Vertices X, Vertices Y alanlı düğüm Delete Geometry'ye bağlı. |
| Delete Geometry | yok | teknik | yok | Işleme yükünü azaltmak için ızgaranın bir kısmını siler. | 0:24 | Delete Geometry düğümü Less Than ve Combine XYZ ile bağlı. (karede: kanıttan) Delete Geometry düğümü Less Than ve Combine XYZ ile bağlı. |
| Instance on Points | yok | teknik | yok | Çizgileri noktalar üzerine instance olarak yerleştirir. | 0:27 | Instance on Points düğümü ekranda, altyazı 'add lines as instances'. (karede: kanıttan) Instance on Points düğümü ekranda, altyazı 'add lines as instances'. |
| Mesh to Curve | yok | teknik | yok | Çizgi mesh'ini eğriye çevirir. | 0:27 | Doing mesh to curve |
| Noise Texture | yok | teknik | yok | Çizgileri bükmek için gürültü uygular. | 0:30 | We connect the noise node to twist our lines |
| Trim Curve | yok | teknik | yok | Çizgilerin çizilme animasyonunu sağlar. | 0:32 | Then trimming nodes for animating lines |
| Curve to Mesh | yok | teknik | yok | Eğriyi Curve Circle profiliyle kalınlık verilen mesh'e çevirir. | 0:36 | Convert curve to mesh and shape it |
| Subdivide Mesh | yok | teknik | yok | Mesh'i bölerek pürüzsüzleştirir, Set Shade Smooth ile birlikte. | 0:39 | We can subdivide assign material and animate the trimming node |
| BlenderKit | yok | plugin | yok | Sahneye hazır kedi modeli eklemek için Blender eklentisi. | 0:45 | Altyazı 'adding the cute Kitty from Blender Kit', yan panelde BlenderKit sekmesi. (karede: kanıttan) Altyazı 'adding the cute Kitty from Blender Kit', yan panelde BlenderKit sekmesi. |
| Screencast Keys | yok | plugin | yok | Blender yan panelinde görünen tuş gösterim eklentisi. | 0:45 | Sağ yan panelde Screencast Keys sekmesi görünüyor. (karede: kanıttan) Sağ yan panelde Screencast Keys sekmesi görünüyor. |
| Principled BSDF | yok | teknik | yok | Materyal için kullanılan gölgelendirici düğümü. | 0:47 | Ekran metninde Principled BSDF, Color Ramp, Material Output. |
| Bodymovin | yok | teknik | yok | Animasyonu PNG dizisi JSON olarak web için dışa aktarma yöntemi (yorumda). | açıklama | Yorumda: PNG sequence in JSON through Bodymovin |
| Three.js | yok | teknik | yok | Animasyonu web sitesinde kullanma seçeneği (yorumda). | açıklama | Yorumda: or with Three.js |
| After Effects | yok | teknik | yok | Hareket tasarımı öğrenmek için önerilen araç (yorumda). | açıklama | Yorumda: Blender for 3D, After Effects for motion |
## Açıklama bağlantıları
- https://drive.google.com/file/d/1Jzf_ttNRDKGLrakGaJsPxRWVOBLuxfs0/view?usp=sharing — Figma ve Blender proje dosyalarının Google Drive paylaşımı · aday: hayır · Yazarın kendi dosya paylaşımı; izleyicinin kullanacağı araç ya da servis değil, dosya indirme bağlantısı. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Gradyan arka planlı çerçeve (gradient frame) | Figma tasarımında sayfanın gradyan dolgulu çerçevesi. (karede: (karede OCR) Position -265 X -706 Y Rotation L0° 4 Layout Flow %0 ↑8 00 Dimensions W 1600 H 1000 Clip content Appearance Opacity Corner radius CC0 100% Libraries Custom + × B8 □ Fill Linear 10 Linear Stroke Effect) | 0:08 | kare |
| Başlık, büyük numara ve açıklama metni yerleşimi (hero typography layout) | SOFTIES başlığı, 'We create cozy, cuddly toys' metni ve numara. | 0:03 | altyazı |
| Animasyonlu 3B çizgi arka planı (animated 3D lines background) | Blender'da üretilip render edilen, Trim Curve ile çizilen bükülmüş çizgiler. | 0:32 | altyazı |
| Kırmızı perde dokulu 3B arka plan (3D curtain backdrop) | Kesitlerde ekranın alt ve üstünde kırmızı perde benzeri arka plan görünüyor. (karede: Düğüm editörünün altında ve üstünde kırmızı perde benzeri arka plan görünüyor.) | 0:24 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Izgaranın bir kısmı silinerek bilgisayarın aşırı yüklenmesi önleniyor. | 0:24 | öneri |
| Çıktı video, PNG dizisi (Bodymovin ile JSON) ya da Three.js ile web için kullanılabilir. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Figma | Figma | Frame with a gradient in Figma |
| konuşma 0:20 | Blender | Blender | Now go to Blender |
| konuşma 0:20 | Geometry Nodes | Geometry Nodes | clicking geometric nodes |
| kare 0:24 | Grid node | Grid node | Grid düğümü Size X/Y, Vertices X/Y |
| kare 0:24 | Delete Geometry | Delete Geometry | Delete Geometry düğümü |
| kare 0:27 | Instance on Points | Instance on Points | Düğüm ekranda |
| konuşma 0:27 | Mesh to curve | Mesh to Curve | doing mesh to curve |
| konuşma 0:30 | Noise düğümü | Noise Texture | connect the noise node |
| konuşma 0:32 | Trim Curve | Trim Curve | trimming nodes for animating lines |
| konuşma 0:36 | Curve to mesh | Curve to Mesh | Convert curve to mesh |
| konuşma 0:39 | Subdivide | Subdivide Mesh | We can subdivide |
| kare 0:45 | BlenderKit | BlenderKit | adding the cute Kitty from Blender Kit |
| kare 0:45 | Screencast Keys | Screencast Keys | Yan panel sekmesi |
| ekran 0:47 | Principled BSDF | Principled BSDF | OCR: Principled BSDF |
| ekran 0:08 | Linear gradyan | aday değil: genel kavram | OCR Linear, Stops; gradyan türü |
| ekran 0:29 | Sketchfab | aday değil: konu dışı | Yalnız eklenti paneli metni; kullanımı görülmedi |
| yorum | Bodymovin | Bodymovin | PNG sequence in JSON through Bodymovin |
| yorum | Three.js | Three.js | or with Three.js |
| yorum | After Effects | After Effects | After Effects for motion |
| açıklama | Google Drive bağlantısı | aday değil: konu dışı | Dosya paylaşım bağlantısı, referans niteliğinde |
| yorum | Instagram | aday değil: konu dışı | Yorumda 'Write to me on Instagram' |
| ekran 0:56 | Comment 'Soft' çağrısı | aday değil: konu dışı | Comment 'Soft' and get the files |
| konuşma 0:00 | Sözlük eşleşmeleri (Next.js, Framer, Meshy vb.) | aday değil: konu dışı | Bulanık sözlük eşleşmesi, videoda kullanılmadı |
## Kareden okunanlar
- 0:24: Plane.006 > GeometryNodes > Geometry Nodes.004; Grid, Delete Geometry, Less Than, Combine XYZ, Position düğümleri; altyazı 'deleting part of it so the PC doesn't catch fire'.
- 0:27: Instance on Points düğümü, Grid, Delete Geometry, Less Than; altyazı 'add lines as instances'; üstte Figma ve Blender simgeleri.
- 0:45: Transform paneli, Scene Collection içinde Kitty night lamp.003, Plane.005, Plane.006; BlenderKit ve Screencast Keys sekmeleri; altyazı 'adding the cute Kitty from Blender Kit'.
## Belirsizlikler
- Altyazı otomatik; 'damp to the big title' muhtemelen 'and drop'/'and damn' hatası.
- Sözlükteki Next.js, Framer, Meshy, Descript, Material UI, uv, Inter gibi eşleşmeler bulanık eşleşme; videoda kullanıldıkları doğrulanamadı.
- OCR'daki 'Linear' Figma gradyan türüdür, Linear uygulaması değil; 'Sketchfab' yalnız BlenderKit/eklenti sekmesinde görünüyor, kullanıldığı görülmedi.
- 'React', 'Inter' gibi OCR eşleşmeleri kullanıldığı kanıtlanmayan menü/ekran metni.
- Kurulum komutu yok.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://youtu.be/VrxXx1GxDnc | açıklama | açıklama | hayır |
| https://drive.google.com/file/d/1Jzf_ttNRDKGLrakGaJsPxRWVOBLuxfs0/view?usp=sharing | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Figma'da gradyanlı çerçeve oluşturma — araçlar: Figma
- 2. adım — Başlık metnini yazma, çizgiler çizme ve önemli numarayı ekleme — araçlar: Figma
- 3. adım — Açıklama metni ve büyük başlığı ekleme — araçlar: Figma
- 4. adım — Blender'da düzlem oluşturup Geometry Nodes'u açma — araçlar: Blender, Geometry Nodes
- 5. adım — Geometriyi Grid düğümüne çevirip bir kısmını silme — araçlar: Grid node, Delete Geometry
- 6. adım — Çizgileri instance olarak ekleme ve mesh to curve yapma — araçlar: Instance on Points, Mesh to Curve
- 7. adım — Noise düğümünü bağlayıp çizgileri bükme — araçlar: Noise Texture
- 8. adım — Çizgileri Trim Curve ile animasyonlama — araçlar: Trim Curve
- 9. adım — Eğriyi mesh'e çevirip şekillendirme, subdivide ve materyal atama — araçlar: Curve to Mesh, Subdivide Mesh, Principled BSDF
- 10. adım — Trim düğümünü animasyonlama — araçlar: Trim Curve
- 11. adım — Layout'a geçip materyali ekleme, render görünümünü açma — araçlar: Blender
- 12. adım — BlenderKit'ten kedi modelini ekleme — araçlar: BlenderKit
- 13. adım — Kamerayı kurup kediyi çoğaltma ve animasyonlama — araçlar: Blender
- 14. adım — Render alma — araçlar: Blender
- 15. adım — Render ile Figma tasarımını birleştirme — araçlar: Figma, Blender
## Promptlar
- yok
