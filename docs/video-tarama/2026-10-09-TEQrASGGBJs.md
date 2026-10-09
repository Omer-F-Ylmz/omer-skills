# Rigging a Horse in Cascadeur | AutoPosing for Quadrupeds
## Künye
Rigging a Horse in Cascadeur | AutoPosing for Quadrupeds · Cascadeur - The Future of Animation · süre: 16:38 · en-orig · https://youtu.be/TEQrASGGBJs · şema 2
motor: parti 2026-10-09-short-40 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 47362 tk · claude-haiku-5-5: claude-haiku-5-5 · 70533 tk
## Özet
Cascadeur'da bir at modelini Quick Rigging Tool'un dörtayaklı (quadruped) ön ayarıyla riglemeyi anlatan eğitim. Omuz kemiği (scapula) eksikliği için sahte eklemler eklenir, auto posing test edilir, kulak ve ağız için kutu kontrolcüler üretilir, rigid body boyutları ve kütleleri ayarlanarak kütle merkezi öne kaydırılır, sahne .casc olarak kaydedilir.
## Bölümler
- 0:00 İlk rig kurulumu
- 1:34 Bacak ve kuyruk eklem mantığı
- 3:38 İlk rig'in üretilmesi
- 4:38 Omuz kemiği eklemlerinin oluşturulması
- 6:38 Rig'in test edilmesi ve iyileştirilmesi
- 8:58 Kulak ve ağız iyileştirmesi
- 12:58 Fizik ve son ayarlar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Cascadeur | yok | CLI | yok | Animasyon ve rigleme yazılımı; tüm eğitim bu programda yapılır | 0:00 | Kareler Cascadeur arayüzünü gösteriyor; 15:50'de cascadeur.com indirme ekranı (karede: Cascadeur menü çubuğu (Tween machine, Mirror tool) ve SK_Horse sahnesi) |
| Quick Rigging Tool | yok | plugin | yok | Ekleme eşleyerek kontrolcü rig'i üreten araç; Humanoid ve Quadruped sekmeleri var | 0:00 | Here I enable quick rigging mode and switch the quadriped preset (karede: QUICK RIGGING TOOL penceresi, QUADRUPED sekmesi, Add rig elements düğmesi) |
| Auto posing | yok | teknik | yok | Kilitlenen noktalarla otomatik poz veren mod; scapula kontrolcüsü yoksa hata verir | 3:38 | auto posing mode isn't working |
| Rigid bodies | yok | teknik | yok | Fizik için mavi rig elemanları; boyut ve kütle ile kütle merkezi ayarlanır | 12:58 | weight information within the specific rig elements called rigid bodies |
| Collision capsule | yok | teknik | yok | Diğer nesnelerle çarpışmayı yöneten kapsül; boyutu ayarlanır | 14:59 | It is a collision capsule which handles collisions with other objects |
| Discord | yok | CLI | yok | Topluluk sunucusu bağlantısı (açıklamada) | açıklama | Join our English-speaking community on Discord |
| Box controller | yok | teknik | yok | Kemikleri seçilebilir kutu şeklinde kontrolcülere dönüştüren kontrolcü türü; kulak ve ağız için kullanıldı. | 8:58 | While in box controller mode, choose the appropriate option within the commands tab. |
| Rigid body | yok | teknik | yok | Karakter parçalarını kütle, elipsoid ve kapsül ile temsil eden fizik elemanı; kütle merkezi ayarında kullanıldı. | 12:58 | You can find the weight information within the specific rig elements called rigid bodies. |
| Manipulator locker | yok | teknik | yok | Seçili kontrolcü noktalarını kilitleyip hareketini sabitleyen özellik; ayak ve omurga noktaları için kullanıldı. | 6:38 | Right here, I'll immediately lock some of the key points. |
| Direction controller | yok | teknik | yok | Baş gibi bölgeleri yön vererek kontrol eden kontrolcü; atın burnundaki yönlendirici ile kafa kontrol edildi. | 7:38 | controlled correctly via a directional controller located on the horse's muzzle. |
## Açıklama bağlantıları
- https://cascadeur.com/plans — Cascadeur planlar sayfası · aday: evet (Cascadeur) · Videoda kullanılan Cascadeur yazılımının plan/indirme sayfası; araç bağlantısı · sınıf: diğer
- https://cascadeur.com/learn — Cascadeur öğrenme sayfası · aday: evet (Cascadeur) · Alan adı videoda kullanılan Cascadeur aracını adlandırıyor · sınıf: diğer
- https://discordapp.com/invite/Ymwjhpn — Discord topluluk daveti · aday: evet (Discord) · Discord hizmeti; açıklamada anılıyor, topluluk aracı olarak izleyici kullanabilir · sınıf: diğer
- https://www.facebook.com/CascadeurEN/ — Facebook sayfası · aday: hayır · Sosyal medya takip bağlantısı; videoda kullanılan araç değil · sınıf: diğer
- https://twitter.com/Cascadeur_soft — Twitter hesabı · aday: hayır · Sosyal medya takip bağlantısı; videoda kullanılan araç değil · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| Ctrl + Z | Eklem seçimi için döndürülen eklemlerdeki değişiklikleri geri alır | 1:01 | altyazı |
| Commands > CopyPaste object > Duplicate object | Oluşturulan omuz eklemini çoğaltır (karede: Commands menüsü açık; Add, CopyPaste object, Rig info gibi öğeler görünüyor) | 4:48 | kare |
| Commands > Add > Joint | Sahneye yeni eklem ekler (karede: Commands menüsünde Add alt menüsü: Joint, Locator, Lights, Ruler) | 4:48 | kare |
| File > Save As... | Rig'li sahneyi .casc proje dosyası olarak kaydeder (karede: Save Scene Horse.fbx.casc penceresi, tür Cascadeur project file (*.casc)) | 15:34 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Quick rigging şablonu omuz kemiği olan kedigiller için tasarlanmış; atlarda omuz kemiği çoğu zaman yoktur | 1:34 | özellik |
| Omuz kemiği kontrolcüsü yoksa auto posing çalışmaz; sahte eklemler eklenince çalışır | 4:38 | özellik |
| Kütle merkezini öne almak için ön bölgelerin ağırlığı artırılır; gerçekçi değerler gerekmez | 14:59 | öneri |
| Rigid body'ler mesh içinde gevşekçe kalmalı, tam eşleşme şart değil | 13:58 | öneri |
| Rig bir kez kurulup sahne kaydedilirse her animasyonda yeniden kurmak gerekmez | 16:01 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Cascadeur | Cascadeur | Videonun ana aracı; arayüz karelerde görünüyor |
| konuşma 0:00 | Quick rigging mode | Quick Rigging Tool | Here I enable quick rigging mode |
| konuşma 0:00 | Quadruped preset | aday değil: başka adayın parçası (Quick Rigging Tool) | switch the quadriped preset for it |
| konuşma 3:38 | Auto posing modu | Auto posing | auto posing mode isn't working |
| konuşma 12:58 | Rigid bodies | Rigid bodies | called rigid bodies. They are these blue elements |
| konuşma 14:59 | Collision capsule | Collision capsule | It is a collision capsule |
| konuşma 4:38 | Outliner | aday değil: genel kavram | drag the name of the new joint onto parent |
| konuşma 9:59 | Point ve box controller modları | aday değil: başka adayın parçası (Quick Rigging Tool) | adjust the point controllers |
| açıklama | Discord | Discord | Join our English-speaking community on Discord |
| açıklama | cascadeur.com/plans | Cascadeur | Alan adı Cascadeur'u adlandırıyor |
| açıklama | cascadeur.com/learn | Cascadeur | Alan adı Cascadeur'u adlandırıyor |
| açıklama | Facebook | aday değil: konu dışı | Takip bağlantısı |
| açıklama | Twitter | aday değil: konu dışı | Takip bağlantısı |
| yorum | Blender | aday değil: konu dışı | Yorumcu Cascadeur'dan Blender'a live link istiyor |
| yorum | Minecraft rig | aday değil: konu dışı | Yorumcu Minecraft rig eğitimi istiyor |
| yorum | taste-skill | aday değil: konu dışı | Yorumda 'it tastes just like raisins'; araçla ilgisiz |
| kare 5:14 | Transform paneli | aday değil: genel kavram | Global/Local position alanları |
| linkli sayfa | Diğer Cascadeur YouTube videoları | aday değil: konu dışı | cascadeur.com sayfasında listelenen videolar |
## Kareden okunanlar
- 0:00: Cascadeur arayüzü, SK_Horse outliner'da, boş at modeli
- 0:08: RIG MODE ON penceresi: 'Rigging mode will save all data except: Custom tangents data (in graph editor)'
- 4:12: Hata: Auto posing tool: no object with name: 'scapula_l'
- 4:22: Rig'de horse_Pelvis_bone_MainPoint, horse_NeckBase_bone_MainPoint gibi noktalar
- 5:14: Transform: Global position 0, 154.22, 42.647
- 10:56: Box size multiplier is 2
- 13:12: Physics settings: Mass 3.8, Ellipsoid 15.759 / 28.559 / 28.559
- 14:58: Capsule collision: Length 16.759, Radius 17.159
- 15:50: DOWNLOAD FOR FREE NOW AT cascadeur.com!
## Belirsizlikler
- Sözlük eşleşmeleri (Next.js, Three.js, Meshy, Lenis vb.) bu videoyla ilgisiz; yanlış eşleşme sayıldı.
- Yorumlardaki Blender ve taste-skill videoda kullanılmadığı için aday yapılmadı.
- Altyazıdaki '10 pixels' kaydırma birimi doğru olmayabilir; kareden birim doğrulanamadı.
- Ctrl+Z komutu kuruluma değil, kullanıma ait; yine de söylendiği için listelendi.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/18 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://cascadeur.com/plans | açıklama | açıklama | evet |
| https://cascadeur.com/learn | açıklama | açıklama | hayır |
| https://discordapp.com/invite/Ymwjhpn | açıklama | açıklama | hayır |
| https://www.facebook.com/CascadeurEN/ | açıklama | açıklama | hayır |
| https://twitter.com/Cascadeur_soft | açıklama | açıklama | hayır |
| cascadeur.com | 15:50 | ekran | evet |
| https://www.youtube.com/watch?v=n86WObMfVkU | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=-WjVIPc0jT0 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=iDr-KMdpzs4 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=1eFShSYATOI | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=4xGKY7-PrBI | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=PJyRc4Z5EtM | açıklama | açıklama | hayır |
| https://youtu.be/c134z16J6Oc | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=VuPWSuwzrZY | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=TEQrASGGBJs | açıklama | açıklama | hayır |
| https://www.youtube.com/embed/BsMK31XRz2s | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Atın modelini açıp rigging moduna geçmek (RIG MODE ON onayı) — araçlar: Cascadeur, Rigging mode
- 2. adım — Quick Rigging Tool'u açıp QUADRUPED sekmesini seçmek — araçlar: Quick Rigging Tool
- 3. adım — Pelvis, omurga, boyun ve baş noktalarını atamak — araçlar: Quick Rigging Tool
- 4. adım — Boyun eklemlerini döndürüp incelemek ve Ctrl+Z ile geri almak — araçlar: Cascadeur
- 5. adım — Ön ve arka bacak eklemlerini (dirsek, bilek, topuk) ve kuyruk eklemlerini atamak — araçlar: Quick Rigging Tool
- 6. adım — Sol taraf için isim girip sağ taraf için ayna nesnesi oluşturmak — araçlar: Quick Rigging Tool, Create mirror object
- 7. adım — Rig'i Generate rig ile üretmek — araçlar: Quick Rigging Tool
- 8. adım — Animasyon moduna geçip rig'i test etmek; scapula eksikliği hatasını görmek — araçlar: Cascadeur, Auto posing
- 9. adım — Commands > Add > Joint ile omuz kemiği eklemi oluşturup konumlandırmak — araçlar: Cascadeur
- 10. adım — Eklemi Copy/Paste object ve Duplicate object ile çoğaltmak — araçlar: Cascadeur
- 11. adım — Object properties > Transform bölümünden X ekseninde +10 ve -10 ile kaydırmak — araçlar: Cascadeur
- 12. adım — Eklemleri sol/sağ olarak yeniden adlandırmak ve Outliner'da üst kemiğe sürükleyip bağlamak — araçlar: Cascadeur
- 13. adım — Omuz eklemlerini Quick Rigging Tool'da atayıp kontrolcü üretmek — araçlar: Quick Rigging Tool
- 14. adım — Auto posing modunda test etmek; omurga ve ayak noktalarını kilitlemek — araçlar: Auto posing, Manipulator locker
- 15. adım — Baş yönlendirme kontrolcüsünü ve bacak/kuyruk tepkisini test etmek — araçlar: Auto posing, Direction controller
- 16. adım — Varsayılan poza dönmek için Box controller modunda kutuları seçip komutu uygulamak — araçlar: Box controller
- 17. adım — Kulak ve ağız kemikleri için kutu kontrolcüleri oluşturmak, Box size multiplier ile boyutlandırmak ve aynalamak — araçlar: Quick Rigging Tool, Box controller, Create mirror object
- 18. adım — Kutu kontrolcülerini animasyon modunda test etmek; joint görünümünü kapatmak — araçlar: Cascadeur, Box controller
- 19. adım — Rigid body boyutlarını Physics settings üzerinden küçültmek ve kapsül çarpışmasını mesh'e uydurmak — araçlar: Rigid body, Physics settings, Capsule collision
- 20. adım — Rigid body kütlelerini artırarak kütle merkezini ön omuza yaklaştırmak — araçlar: Rigid body, Physics settings
- 21. adım — Varsayılan pozu kontrol edip File > Save As ile Horse.fbx.casc olarak kaydetmek — araçlar: Cascadeur
## Promptlar
- yok
