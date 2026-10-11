# PixelLab Character States: The New Way to Animate Sprites
## Künye
PixelLab Character States: The New Way to Animate Sprites · PixelLab · süre: 11:15 · en-orig · https://youtu.be/oCJWxfEwX-o · şema 2
motor: parti 2026-10-11-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 46222 tk · claude-haiku-5-5: claude-haiku-5-5 · 76192 tk
## Özet
PixelLab'in karakter oluşturucusuna eklenen 'States' (durumlar) özelliği anlatılıyor. Önce v3 modunda 32x44 özel boyutla, yüksek yukarıdan görünümlü maskeli bir maceracı üretiliyor. Ardından 'mid-walk' ve 'fighting pose' durumları oluşturulup bu durumlardan Custom Animation V3 ile animasyon üretiliyor. Ağız hataları Pixelorama'da temizleniyor, yön aynalama anlatılıyor. İnek (dört ayaklı) üzerinde yemek yeme, yürüme ve yatma durumları ile 'yatıyorken ayağa kalkma' interpolasyon geçişi gösteriliyor. Goblin kıyafet varyantları ve 176x176 canavar boss durumlarıyla bitiyor.
## Bölümler
- 0:00 Durumlara (states) giriş
- 1:04 Temel karakter üretme
- 2:26 Durum oluşturma ve animasyon
- 4:44 Temizlik ve aynalama
- 5:48 Hayvan karakterlerde durumlar
- 7:38 İnterpolasyon ve geçişler
- 9:15 Karakter varyantları ve bosslar
- 10:44 Sonuç
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| PixelLab | yok | CLI | yok | Piksel sanat karakter ve animasyon üreten web servisi; tüm iş akışı burada yürüyor. | 0:16 | Üst menüde PixelLab, Docs, API, Characters, Maps sekmeleri görünüyor. (karede: Tarayıcıda pixellab.ai; menüde PixelLab, Docs, API, Vibe coding, Editor, Creator, Characters, Objects, Maps.) |
| Character creator | yok | iş akışı | yok | Karakterin metinden 8 yönlü üretildiği ve durum/animasyon eklenen PixelLab bölümü. | 1:04 | Head over to the characters page; inside the character creator, we can create states. |
| Create State | yok | teknik | yok | Aynı karakteri metinle yeni poz/varyasyona çeviren yeni durum özelliği; 8 yönde tutarlı uygulanır. | 2:26 | Ekranda 'Create State' düğmesi ve 'Generate State' penceresi var. (karede: Karakter sayfasında mor 'Create State' düğmesi, 'States' bölümü ve alt kısımda '+' kartı.) |
| v3 | yok | teknik | yok | Karakter üretiminde Standard/Pro/v3 seçeneklerinden yeni v3 üretim modu. | 1:26 | Generation Mode altında v3 NEW seçili. (karede: Generation Mode: Standard, Pro NEW, v3 NEW (seçili); Humanoid kartı seçili; açıklama kutusunda maceracı metni.) |
| Custom Animation V3 | yok | teknik | yok | Kare sayısı ayarlı, ilk kareyi koruyabilen özel animasyon modeli. | 1:56 | Custom Animation V3 BETA paneli, Keep first frame kutusu. (karede: CUSTOM altında Custom Animation V3 seçili; Action Description, Frame Count: 8, 'Keep first frame (idle pose)' işaretli.) |
| Pixelorama | yok | plugin | yok | PixelLab içinde animasyon karelerini elle düzelten piksel editörü (ağız temizliği, çimen silme). | 4:18 | Splash ekranında 'pixelorama pixellab' logosu. (karede: Piksel manzara arka planında 'pixelorama pixellab' logosu; sol altta ejderha maskot.) |
| Interpolation | yok | teknik | yok | Başlangıç ve bitiş karesi verip arasını ürettirme; yatıştan ayağa kalkma geçişinde kullanıldı. | 7:12 | Choose End Frame penceresi; durum ve idle pose seçilebiliyor. (karede: 'Choose End Frame' penceresi: State altında laying down, mid-walk, eating from the floo, A cow; Idle Pose kutuları.) |
| Enhance prompt | yok | ipucu | yok | Kısa animasyon istemini ayrıntılı açıklamaya genişleten düğme. | 1:56 | Action Description kutusunun sağında küçük büyü düğmesi; metin uzun betime dönüşüyor. · kanıt: kare (karede: Action Description kutusunda sağ üstte mor düğme; 3:50 karesinde uzun 'fighting stance' betimi.) |
| Mirror animation | yok | ipucu | yok | Doğu/güneydoğu/kuzeydoğu animasyonlarını batı yönlerine aynalayarak 8 yönü hızlandırma. | 5:08 | 'Animation mirrored! 9 frames mirrored from East to West' bildirimi. · kanıt: kare (karede: Yeşil bildirim 'Animation mirrored!'; West kutusunda inek animasyonu.) |
| Skeleton animation | yok | teknik | yok | İnek eski yürüme karelerinin iskelet/şablonla üretilmesi; durumlara alternatif. | 5:48 | These older walk frames were made with skeletons, and they still work. · kanıt: yok |
| Character States | yok | teknik | yok | Aynı karaktere ek poz/durum (mid-walk, fighting pose, laying down, mid-grab vb.) üreten PixelLab özelliği; animasyonun ilk karesi olarak kullanılır. | 2:26 | create another one, mid-walk. So, instead of asking the animation tool |
| Temel karakter üretimi (v3) | yok | prompt | yok | Siyah kapüşonlu, içinde beyaz giysili, kırmızı Japon maskeli bir maceracı; yüksek yukarıdan görünüm, 32x44 özel boyut. | 1:04 | kaynak: kare |
| Dövüş duruşu durumu | yok | prompt | yok | Aynı karakter, dövüş pozunda. | 2:26 | kaynak: altyazı |
| Yürüme başlangıç durumu | yok | prompt | yok | Aynı karakter yürüyüşün ortasında (mid-walk) pozunda. | 2:26 | kaynak: altyazı |
| Mid-walk durumundan yürüme animasyonu | yok | prompt | yok | Yürüme döngüsü; istem geliştirildi, ilk kare korunarak üretildi. | 2:26 | kaynak: altyazı |
| Dövüş duruşu animasyonu | yok | prompt | yok | Dövüş duruşunda bekleme, savaşa hazır; 6 kare (ilk kareyle 7). | 3:26 | kaynak: kare |
| İnek durumları | yok | prompt | yok | İnek yerden yemek yiyor; ardından yürüyüş ortası; ardından yatıyor. | 5:48 | kaynak: altyazı |
| İnterpolasyonlu geçiş animasyonu | yok | prompt | yok | Ayağa kalk; başlangıç yatma durumu, bitiş normal idle. | 6:49 | kaynak: altyazı |
| Karakter kıyafet varyantları | yok | prompt | yok | Aynı goblin kırmızı kıyafetli; aynı goblin Noel kıyafetli. | 9:15 | kaynak: altyazı |
| Boss durumları | yok | prompt | yok | Ortası kapma: önündekini yakalıyor; bir de alevler içinde. | 10:17 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=oCJWxfEwX-o — PixelLab ana sayfası · aday: evet (PixelLab) · Alan adı videoda kullanılan servisi adlandırıyor; izleyici kullanabilir. UTM izleme parametresi var, açık sponsor ifadesi yok. · sınıf: diğer
- https://discord.gg/3cYE5fdkRX — Discord topluluk daveti · aday: hayır · Topluluk davet bağlantısı; araç değil, paylaşım yeri olarak anılıyor. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Animasyon çoğunlukla idle pozdan başlıyordu; durumlarla hareketi başlatan poz önceden üretilebiliyor. | 0:00 | özellik |
| Özel boyut 32x44 modelin karakter şekline odaklanmasına yardım ediyor. | 1:04 | öneri |
| İlk kare korunduğundan 6 üretilen kare toplam 7 kare animasyon verir. | 3:26 | sayısal |
| Durum üretimi 20-40 üretim maliyetinde; 8 yöne tutarlı uygulanır. | 2:30 | sayısal |
| Simetrik karakterde 8 yönlü yürüme seti 5 dakikadan kısa sürede kurulabilir. | 8:38 | sayısal |
| Durumlar yalnız animasyon için değil; kıyafet, hasarlı ve güçlendirilmiş varyantlar için de kullanılır. | 9:15 | özellik |
| Kılıç gibi tek taraflı ayrıntısı olmayan karakterde yönler aynalanabilir. | 4:44 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | PixelLab karakter oluşturucu güncellemesi | PixelLab | Pixelab's character creator just got a pretty important update. |
| konuşma 0:00 | States (durumlar) özelliği | Create State | inside the character creator, we can create states. |
| kare 0:16 | PixelLab ana sayfa ve menü | PixelLab | pixellab.ai sayfasında menü sekmeleri görünüyor. |
| kare 0:16 | Ejderha maskot | aday değil: konu dışı | Sol altta yeşil piksel ejderha maskot. |
| kare 0:30 | Çizim infografikleri (durum oluşturma rehberi) | aday değil: genel kavram | Elle çizilmiş infografik slaytları, araç adı yok. |
| kare 0:30 | React, Framer Motion, Emotion, Outfit (sözlük eşleşmesi) | aday değil: konu dışı | OCR'daki 'emotion' ve 'outfit' infografik sözcükleri. |
| konuşma 0:00 | Framer, Pika, Claude Sonnet, Make, Canva, Go, Astro, Next.js, Three.js, Hermes Agent | aday değil: konu dışı | Bulanık sözlük eşleşmeleri; videoda anlatılmıyor. |
| kare 4:56 | OCR 'Claude Code' eşleşmesi | aday değil: konu dışı | Videoda kullanıldığına dair kanıt yok. |
| konuşma 1:04 | Characters sayfası | Character creator | First, I'm going to head over to the characters page. |
| konuşma 1:04 | v3 üretim modu | v3 | see the newer V3 generation mode in action. |
| konuşma 1:04 | Yüksek yukarıdan kamera görünümü | aday değil: genel kavram | Ayar seçeneği. |
| konuşma 1:04 | Özel boyut 32x44, kare tuval | aday değil: genel kavram | Boyut ayarı. |
| kare 1:26 | Humanoid / Quadruped karakter tipleri | aday değil: genel kavram | Karakter tipi seçenekleri. |
| kare 1:54 | Animasyon tipi menüsü (Backflip, Kicking, vb.) | aday değil: konu dışı | Yalnız menüde listelenmiş, kullanılmadı. |
| konuşma 2:26 | Fighting pose ve mid-walk durumları | Create State | Let's start with ... fighting pose. And then ... mid-walk. |
| konuşma 2:26 | Custom animation V3 | Custom Animation V3 | choose custom animation V3, and for the prompt, walk loop. |
| kare 1:56 | Custom Animation (Pro) menü seçeneği | aday değil: konu dışı | Yalnız menüde göründü, kullanılmadı. |
| konuşma 2:26 | İstemi geliştirme (enhance prompt) | Enhance prompt | I'm going to enhance the prompt just to be safe. |
| konuşma 2:26 | İlk kareyi koruma ve kare sayısı | Custom Animation V3 | I'm leaving the first frame on. |
| konuşma 4:26 | Edit in Pixelorama | Pixelorama | I'll click edit in Pixelorama ... copy and paste the face. |
| kare 4:20 | Pixelorama araç menüleri (Inpaint, Remove Background vb.) | aday değil: konu dışı | OCR menü öğeleri, kullanılmadı. |
| konuşma 4:44 | Yön aynalama | Mirror animation | you can mirror some of these animations. |
| konuşma 5:48 | İnek karakter ve iskelet tabanlı eski kareler | Skeleton animation | These older walk frames were made with skeletons. |
| konuşma 5:48 | Yeme, yürüme ortası, yatma durumları | Create State | eating from the floor, mid-walk, laying down. |
| konuşma 6:49 | İnterpolasyon (başlangıç ve bitiş karesi) | Interpolation | give the tool a start frame and an end frame. |
| konuşma 9:15 | Goblin varyantları, Noel kıyafeti | Create State | same goblin wearing a Christmas outfit. |
| konuşma 10:17 | 176x176 boss, mid-grab ve on fire durumları | Create State | mid-grab, grabbing what's in front of it. And then one more, on fire. |
| açıklama | https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=oCJWxfEwX-o | PixelLab | Açıklamadaki ana bağlantı. |
| açıklama | https://discord.gg/3cYE5fdkRX | aday değil: konu dışı | Topluluk daveti; araç değil. |
| açıklama | Discord (paylaşım yeri) | aday değil: konu dışı | please share it in the Discord. |
| linkli sayfa | docs/tools/animate-with-text-pro | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | docs/tools/rotate | aday değil: konu dışı | Videoda anlatılmadı; belge sayfası. |
| linkli sayfa | docs/tools/consistent-style | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | docs/getting-started | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | docs/tools/create-image-flux | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | docs/tools/create-map | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | docs/tools/create-ui-elements-pro | aday değil: konu dışı | Videoda kullanılmadı. |
| linkli sayfa | youtu.be bağlantıları (Iaxk_8ftJ5s, r8ySiSRRvz4, 9eAlZlQmZBg, sE1s5ZYfxqk, fvPmuk-usgw) | aday değil: konu dışı | Diğer videolara bağlantılar. |
| linkli sayfa | youtu.be bağlantıları (BdoUMKhZ1Ys, Hhx9QZwYoZY, moCpjMOOBGk, j2bE9gq914U, zghUW8fGqsM, qVDkp1baJkU) | aday değil: konu dışı | Diğer videolara bağlantılar. |
| linkli sayfa | youtu.be/oCJWxfEwX-o (bu video) | aday değil: konu dışı | Videonun kendi bağlantısı. |
| yorum | .glb animasyonları ve Gemini ile poz yöntemi | aday değil: konu dışı | Yorumcunun kendi iş akışı; videoda gösterilmedi. |
| yorum | API/MCP kullanılabilir mi sorusu | aday değil: konu dışı | Yalnız soru; videoda anlatılmadı. |
| yorum | Pro ve v3 karşılaştırma sorusu | aday değil: konu dışı | Yalnız soru. |
| yorum | Orta yönlerdeki yürüme kalitesi ve NSFW soruları | aday değil: konu dışı | İzleyici soruları. |
## Kareden okunanlar
- 0:16: Menü: PixelLab, Docs, API, Vibe coding, Editor, Creator, Characters, Objects, Maps, Account, Sign out.
- 0:30: Çizim infografiği 'Creating different states of a character': duygu ve niyet, poza uygula, eylemleri keşfet, tutarlı tut.
- 0:42: 'Better animation starts': yalnız nötr/idle başlamaktan kaçın; çömelme, koşma, zıplama örnekleri.
- 0:48: 'Consistent character variations': ejderha karakter, koşma, duygu değişimi, ifade, dinamik duruş.
- 1:26: Mod: Standard, Pro NEW, v3 NEW (seçili); Humanoid; Quadruped yakında; Low Top-Down seçili, 48px.
- 1:48: Karakter sayfası: 84x84px, 8 directions, 0 animations, high top-down view; States 1.
- 1:56: Custom Animation V3 BETA, Frame Count 8, Keep first frame işaretli, Cost: 1 generations.
- 3:22: 'V3 Animation Job Submitted! Your animation is being generated in the background.'
- 4:50: Güney karede 'Regenerate animation (replaces current frames)' ipucu; animasyon 'MIXED FRAMES V3'.
- 7:04: Karakter 'laying down', 96x96px, Template: bear; Transitions altında Sitting Down, Standing Up.
- 7:12: Choose End Frame: laying down, mid-walk, eating from the floo, A cow.
- 5:28: Yeşil bildirimler: 'Animation mirrored! 9 frames mirrored from East to West' ve 'Refreshed'.
- 10:22: Boss 176x176px, 8 directions; States 2, biri 'Generating' durumda.
## Belirsizlikler
- Kare 1:26'da Low Top-Down ve 48px seçili görünüyor; anlatıcı yüksek yukarıdan ve 32x44 diyor, sonradan değiştirmiş olabilir.
- Yorumda Gemini, API/MCP anıldı ama videoda gösterilmedi; aday yapılmadı. Menüdeki API ve Vibe coding sekmeleri kullanılmadı.
- Custom Animation (Pro), Pixel Art Correction, Inpaint, Remove Background gibi yalnız menüde görünen öğeler kullanılmadı.
- Sunucu tarafındaki ana yapay zekâ modeli adı verilmiyor ('latest AI model'); sadece V3 denmiş.
- OCR'daki 'Claude Code' (4:56) ve sözlük eşleşmeleri (Framer, Pika, Next.js vb.) bulanık eşleşme; videoda bu araçlar yok.
- Bağlantıdaki utm parametreleri izleme amaçlı; affiliate/sponsor olarak değil 'diğer' sayıldı. Videoda açık sponsor ifadesi yok.
- Açıklama sayfasındaki docs ve youtu.be bağlantıları videoda kullanılmadı; içerikleri doğrulanmadı.
- İnek yürüyüşünde 8 kare seçilmiş, kare 5:20'de Cost: 2 gen yazıyor; aynalamada '9 frames' bildirimi çıkıyor, sebep belirsiz.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/16 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=oCJWxfEwX-o | açıklama | açıklama | evet |
| https://discord.gg/3cYE5fdkRX | açıklama | açıklama | hayır |
| pixellab.ai | 0:16 | ekran | evet |
| https://www.pixellab.ai/create-character | 0:19 | ekran | evet |
| pixellab.ai/create-character/new?prompt=adventurer+wearing+a+black+hood+and+inner+white+clothing%2C+wearing+a+red+japanese+mask | 1:24 | ekran | evet |
| pixelab.ai/pixellab.ai/create-character/new?prompt=adventurer+wearing+a+black+hood+and+inner+white+clothing%2C+wearing+a+red+japanese+mask | 1:35 | ekran | evet |
| https://www.pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/rotate | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-map | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/rotate | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-map | açıklama | açıklama | hayır |
| https://pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
| https://youtu.be/Iaxk_8ftJ5s | açıklama | açıklama | hayır |
| https://youtu.be/r8ySiSRRvz4 | açıklama | açıklama | hayır |
| https://youtu.be/9eAlZlQmZBg | açıklama | açıklama | hayır |
| https://youtu.be/sE1s5ZYfxqk | açıklama | açıklama | hayır |
| https://youtu.be/fvPmuk-usgw | açıklama | açıklama | hayır |
| https://youtu.be/BdoUMKhZ1Ys | açıklama | açıklama | hayır |
| https://youtu.be/Hhx9QZwYoZY | açıklama | açıklama | hayır |
| https://youtu.be/moCpjMOOBGk | açıklama | açıklama | hayır |
| https://youtu.be/j2bE9gq914U | açıklama | açıklama | hayır |
| https://youtu.be/zghUW8fGqsM | açıklama | açıklama | hayır |
| https://youtu.be/qVDkp1baJkU | açıklama | açıklama | hayır |
| https://youtu.be/oCJWxfEwX-o | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — PixelLab sitesinde Characters sayfasını açma — araçlar: PixelLab
- 2. adım — v3 modunda, maskeli maceracı istemi, yüksek yukarıdan görünüm ve 32x44 özel boyutla karakter üretme — araçlar: PixelLab, v3, Character creator
- 3. adım — Eski yöntemi anlatma: idle'dan doğrudan yürüme animasyonu istemenin sorunları — araçlar: PixelLab
- 4. adım — Create State ile 'fighting pose' ve 'mid-walk' durumlarını oluşturma — araçlar: Create State
- 5. adım — Mid-walk durumundan Custom Animation V3 ile 'walk loop' animasyonu üretme (istem geliştirme, ilk kare açık) — araçlar: Custom Animation V3, Enhance prompt
- 6. adım — Fighting pose durumundan 6 karelik 'fighting stance idle' animasyonu üretme — araçlar: Custom Animation V3, Enhance prompt
- 7. adım — Doğu yürüyüşünde ağız hareketini Pixelorama'da yüzü karelere kopyalayarak düzeltme — araçlar: Pixelorama
- 8. adım — Güneydoğu/kuzeydoğu sonuçlarını kontrol etme, hızlı olan güney animasyonunu yeniden üretmeye karar verme — araçlar: PixelLab
- 9. adım — Doğu, güneydoğu, kuzeydoğu animasyonlarını batıya aynalayıp kalan güney/kuzeyi üretme — araçlar: Mirror animation
- 10. adım — İnek karakterinde yerden yeme, yürüyüş ortası ve yatma durumlarını oluşturma ve inceleme — araçlar: Create State
- 11. adım — Yatma durumunu başlangıç, idle'ı bitiş kare yapıp 'Stand up' interpolasyon animasyonu üretme — araçlar: Custom Animation V3, Interpolation, Enhance prompt
- 12. adım — Güneydoğu yönünde aynı geçişi deneme; yeme durumundaki çimeni Pixelorama'da temizleme — araçlar: Custom Animation V3, Pixelorama
- 13. adım — Mid-walk durumundan doğu yönü 8 karelik yürüme animasyonu üretme; durum yönlerini Pixelorama'da düzeltme — araçlar: Custom Animation V3, Pixelorama
- 14. adım — Goblin/ogre için kırmızı kıyafet ve Noel kıyafeti varyant durumları oluşturma — araçlar: Create State
- 15. adım — 176x176 boss için 'mid-grab' ve 'on fire' durumlarını oluşturup karşılaştırma — araçlar: Create State
## Promptlar
- Temel karakter üretimi (v3) — Siyah kapüşonlu, içinde beyaz giysili, kırmızı Japon maskeli bir maceracı; yüksek yukarıdan görünüm, 32x44 özel boyut.
- Dövüş duruşu durumu — Aynı karakter, dövüş pozunda.
- Yürüme başlangıç durumu — Aynı karakter yürüyüşün ortasında (mid-walk) pozunda.
- Mid-walk durumundan yürüme animasyonu — Yürüme döngüsü; istem geliştirildi, ilk kare korunarak üretildi.
- Dövüş duruşu animasyonu — Dövüş duruşunda bekleme, savaşa hazır; 6 kare (ilk kareyle 7).
- İnek durumları — İnek yerden yemek yiyor; ardından yürüyüş ortası; ardından yatıyor.
- İnterpolasyonlu geçiş animasyonu — Ayağa kalk; başlangıç yatma durumu, bitiş normal idle.
- Karakter kıyafet varyantları — Aynı goblin kırmızı kıyafetli; aynı goblin Noel kıyafetli.
- Boss durumları — Ortası kapma: önündekini yakalıyor; bir de alevler içinde.
