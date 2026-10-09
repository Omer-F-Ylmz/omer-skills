# Cascadeur + QuickMagic | Video Mocap Cleanup and Editing Timelapse
## Künye
Cascadeur + QuickMagic | Video Mocap Cleanup and Editing Timelapse · Cascadeur - The Future of Animation · süre: 11:57 · en-orig · https://youtu.be/4OHDiZgctqs · şema 2
motor: parti 2026-10-09-short-42 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 45742 tk · claude-haiku-5-5: claude-haiku-5-5 · 71081 tk
## Özet
Cascadeur ekibi, QuickMagic ile videodan çıkarılan dans mocap'ini Cascadeur'da Cassie karakterine retarget edip temizliyor. Animation Unbaking ve Fulcrum Motion Cleaning ile sağlam bir taban kuruluyor, ardından AutoPosing ile pozlar düzenleniyor (hızlandırılmış timelapse). Sonunda AutoPhysics ile ikincil hareket ve yumuşatma ekleniyor, final animasyon referans videoyla yan yana gösteriliyor.
## Bölümler
- 0:00 Stress Intro
- 0:18 Import Animation
- 0:46 Retargeting
- 1:44 Animation Unbaking
- 2:41 Editing Timelapse
- 9:32 AutoPhysics
- 10:36 Timelapse
- 11:19 Final Result
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Cascadeur | yok | CLI | yok | Animasyonun düzenlendiği, temizlendiği ve fizikle iyileştirildiği 3B animasyon yazılımı | 0:18 | Arayüzde Cascadeur başlığı, zaman çizelgesi ve Outliner görülüyor (karede: kanıttan) Arayüzde Cascadeur başlığı, zaman çizelgesi ve Outliner görülüyor |
| QuickMagic | yok | CLI | yok | Videodan mocap (hareket yakalama) için kullanılan servis; gövde ve eller yakalanıyor | 0:18 | We used Quick Magic for video mocap and it turned out brilliant. |
| Mixamo | yok | teknik | yok | Mocap dışa aktarımında kullanılan karakter iskeleti; T-pose ile otomatik rig sağlar | 0:18 | we use the Miximo character, mocap's full body and hands |
| Cassie | yok | teknik | yok | Animasyonun retarget edildiği son karakter (Cascy modeli) | 0:42 | Model menüsünde CASCY seçili, sonra kedi kafalı karakter yüklü (karede: kanıttan) Model menüsünde CASCY seçili, sonra kedi kafalı karakter yüklü |
| Quick rigging tool | yok | teknik | yok | İnsansı karakterleri otomatik rigleme aracı | 0:28 | Quick Rigging Tool penceresi, Add rig elements düğmesi (karede: kanıttan) Quick Rigging Tool penceresi, Add rig elements düğmesi |
| Retargeting | yok | teknik | yok | Edit menüsünden Retargeting Copy/Paste ile animasyonu karaktere aktarma | 0:46 | go to edit, retargeting, copy... go to edit, retargeting, paste. |
| Animation Unbaking | yok | teknik | yok | Bake edilmiş animasyondan anahtar kare seti çıkarır | 1:44 | the first thing we're going to do, we're going to use animation on baking |
| Fulcrum Motion Cleaning | yok | teknik | yok | Ayakların kaymasını önleyen temizleme aracı | 1:44 | Fulcrim motion cleaning to prevent the feet from sliding |
| AutoPosing | yok | teknik | yok | Pozları düzeltmek ve düzenlemek için kullanılan otomatik pozlama | 1:44 | I set auto posing to be more precise |
| AutoPhysics | yok | teknik | yok | İkincil hareket ve yumuşatma filtreleriyle fizik düzeltmesi | 9:32 | we can use autophysics to further improve the animation |
| Physics corrector | yok | teknik | yok | AutoPhysics filtresi, %100 ayarla kullanıldı | 9:32 | physics corrector as a 100 smooth trajectory |
| Smooth trajectory | yok | teknik | yok | Kütle merkezi yörüngesini yumuşatan AutoPhysics filtresi | 9:32 | smooth trajectory to smooth out the trajectory of the center of mass |
| Secondary motion | yok | teknik | yok | İkincil hareket filtresi | 9:32 | compensation motion and secondary motion |
| Compensation motion | yok | teknik | yok | AutoPhysics telafi hareketi filtresi | 9:32 | compensation motion and secondary motion |
| Discord | yok | teknik | yok | Cascadeur İngilizce topluluk sunucusu | açıklama | Join our English-speaking community on Discord |
| Cascy | yok | teknik | yok | Cascadeur'un dahili karakter modeli; retargeting hedefi olarak kullanılıyor. | 0:44 | Cascadeur model seçim ekranında CASCY kartı görünüyor. (karede: Model seçim ekranında ilk kart 'CASCY' etiketli; ızgarada UE5 MANNY, UE5 QUINN, UE4 MANNEQUIN gibi diğer modeller de var.) |
## Açıklama bağlantıları
- https://cascadeur.com/plans — Cascadeur fiyat planları · aday: evet (Cascadeur) · Videoda kullanılan Cascadeur yazılımının sitesi · sınıf: diğer
- https://cascadeur.com/learn — Cascadeur öğrenme sayfası · aday: evet (Cascadeur) · Videoda kullanılan Cascadeur yazılımının öğrenme kaynağı · sınıf: diğer
- https://discordapp.com/invite/Ymwjhpn — Discord topluluk daveti · aday: evet (Discord) · Discord servisi açıklamada topluluk için anılıyor · sınıf: diğer
- https://www.facebook.com/CascadeurEN/ — Cascadeur Facebook sayfası · aday: hayır · Sosyal medya takip bağlantısı, araç değil · sınıf: diğer
- https://twitter.com/Cascadeur_soft — Cascadeur Twitter hesabı · aday: hayır · Sosyal medya takip bağlantısı, araç değil · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| Edit > Retargeting Copy | Kaynak projede seçili karelerin animasyonunu retarget için kopyalar | 0:46 | altyazı |
| Edit > Retargeting Paste | Kopyalanan animasyonu karakter projesine yapıştırır | 0:46 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| QuickMagic mocap ayaklara çok dikkat ediyor, kaymayı önlüyor; bu Cascadeur'un fulcrum noktalarını doğru bulmasını sağlıyor. | 0:46 | özellik |
| AutoPosing daha hassas ayarlandı çünkü animasyonda çok ince hareket var. | 1:44 | öneri |
| Fizik küçük aralıklara uygulanmalı, aynı filtreler fazla üst üste bindirilmemeli. | 9:32 | öneri |
| Animasyon 1088 kare için Fulcrum motion cleaning tamamlandı. | 2:22 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Cascadeur | Cascadeur | show you how this animation was created and edited |
| konuşma 0:00 | Dori Dance | aday değil: konu dışı | referans video sahibi |
| konuşma 0:18 | QuickMagic | QuickMagic | We used Quick Magic for video mocap |
| konuşma 0:18 | Mixamo | Mixamo | we use the Miximo character |
| kare 0:28 | Quick rigging tool | Quick rigging tool | Quick Rigging Tool penceresi |
| kare 0:42 | Cassie / Cascy | Cassie | Models listesinde CASCY |
| kare 0:42 | Rokoko, Sabertooth, UEFN_Mannequin, Xsens MVN_Puppet | aday değil: konu dışı | yalnız model menüsünde listede görünüyor |
| konuşma 0:46 | Retargeting | Retargeting | edit, retargeting, copy |
| konuşma 1:44 | Animation Unbaking | Animation Unbaking | we're going to use animation on baking |
| konuşma 1:44 | Fulcrum Motion Cleaning | Fulcrum Motion Cleaning | prevent the feet from sliding |
| açıklama | AutoPosing | AutoPosing | AutoPosing to fix and edit the poses |
| konuşma 9:32 | AutoPhysics | AutoPhysics | use autophysics to further improve |
| konuşma 9:32 | Physics corrector | Physics corrector | physics corrector as a 100 |
| konuşma 9:32 | Smooth trajectory | Smooth trajectory | smooth trajectory |
| konuşma 9:32 | Secondary motion | Secondary motion | secondary motion |
| konuşma 9:32 | Compensation motion | Compensation motion | compensation motion |
| açıklama | Discord | Discord | Join our English-speaking community on Discord |
| açıklama | Facebook ve Twitter bağlantıları | aday değil: konu dışı | sosyal medya takip bağlantıları |
| açıklama | cascadeur.com/plans ve /learn | Cascadeur | Cascadeur sitesi |
| yorum | Marvelous Designer, Houdini, Maya, Blender | aday değil: konu dışı | yorumda kumaş simülasyonu için öneri; videoda kullanılmıyor |
| konuşma 11:19 | YouTube | aday değil: konu dışı | telif hakkı şakası |
## Kareden okunanlar
- 0:24: RIG MODE HELPER: 'Enter rig mode to rig the imported model?' Yes/No, T-pose Mixamo modeli
- 0:28: Quick rigging tool: 'For humanoid characters it's best to use the quick rigging tool. Launch it?'
- 0:42: Cascadeur ana menüsü: Models listesinde CASCY, UE5 MANNY, SABERTOOTH, ROKOKO vb.
- 1:26: LOAD VIDEO penceresi: duration 00:36.2, fps 30, frames 1090, Progress 99%
- 1:36: Timeline settings: Framerate 30, Start frame, Timecode seçili
- 1:52: Animation unbaking ayarları: Interpolation difference 10, AutoPosing precision, Fingers relative difference
- 9:48: AutoPhysics status: Iterations: 686, Termination: CONVERGENCE, Time: 0.746 sec.
- 10:18: WARNING: secondary motion vb. yalnız bir kez uygulanmalı, snap sonrası kapatılsın mı? Yes/No
- 10:48: AutoPhysics status: Iterations: 1058, Termination: NO_CONVERGENCE, Time: 20.005 sec.
## Belirsizlikler
- Altyazıdaki 'Cascader', 'Gasket', 'Miximo' oto-altyazı hatalarıdır; Cascadeur ve Mixamo olarak yorumlandı.
- 'Cassie' karakteri ekranda CASCY/Cascy olarak görünüyor.
- Sözlük eşleşmeleri (Claude Sonnet, Next.js, Stripe, React vb.) bulanık eşleşmeler; videoda bu araçlar kullanılmıyor.
- Fulcrum cleaning kare zamanı (2:22) kare listesinde yok, OCR'den alındı.
- Yorumlarda anılan Marvelous Designer, Blender, Houdini, Maya videoda kullanılmıyor (yorum tartışması).
- Timelapse bölümünde (2:41-9:32) konuşma yok, altyazı anlamsız müzik sözleri.
- Referans videonun sahibi Dori Dance (@doridance1389) için URL verilmedi.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/15 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://cascadeur.com/plans | açıklama | açıklama | evet |
| https://cascadeur.com/learn | açıklama | açıklama | evet |
| https://discordapp.com/invite/Ymwjhpn | açıklama | açıklama | evet |
| https://www.facebook.com/CascadeurEN/ | açıklama | açıklama | hayır |
| https://twitter.com/Cascadeur_soft | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Referans dans videosunu seçme — araçlar: Dori Dance
- 2. adım — Videodan mocap alma (gövde, eller, T-pose ile) — araçlar: QuickMagic, Mixamo
- 3. adım — Mocap'i Cascadeur'a aktarıp Rig Mode ile otomatik rigleme — araçlar: Cascadeur, Quick rigging tool
- 4. adım — Yeni projede Cassie karakterini yükleme — araçlar: Cascadeur, Cassie
- 5. adım — Retargeting Copy/Paste ile animasyonu aktarma — araçlar: Cascadeur, Retargeting
- 6. adım — Retarget sonucunu orijinalle karşılaştırma — araçlar: Cascadeur
- 7. adım — Referans videoyu sahneye yükleme ve başlangıç karesini ayarlama — araçlar: Cascadeur
- 8. adım — Animation Unbaking ayarlarını yapıp uygulama — araçlar: Animation Unbaking, AutoPosing
- 9. adım — Fulcrum noktalarını kontrol edip ayak kaymasını temizleme — araçlar: Fulcrum Motion Cleaning
- 10. adım — Küçük aralıklarda pozları adım adım düzeltme (timelapse) — araçlar: AutoPosing, Cascadeur
- 11. adım — Elleri ve parmakları düzenleme — araçlar: Cascadeur
- 12. adım — AutoPhysics filtrelerini ayarlayıp aralık bazında önizleme — araçlar: AutoPhysics, Physics corrector, Smooth trajectory, Secondary motion
- 13. adım — Fiziği snap ile uygulayıp sonraki aralığa geçme — araçlar: AutoPhysics
- 14. adım — Final animasyonu referansla karşılaştırma — araçlar: Cascadeur
## Promptlar
- yok
