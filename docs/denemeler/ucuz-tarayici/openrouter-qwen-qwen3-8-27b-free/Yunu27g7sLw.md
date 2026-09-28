# Fable 5 vs Opus 4.8: Web Sitesi Testi! Devrim mi, Pazarlama mı?
## Künye
Fable 5 vs Opus 4.8: Web Sitesi Testi! Devrim mi, Pazarlama mı? · Yıldız Dikme · süre: 11:31 · en · yok
## Özet
Yıldız Dikme, Fable 5 ile Opus 4.8 modellerini aynı görevde karşılaştırıyor: elinde bir freelance işi için yaptığı animasyonlu "AETHRA" hero sitesi var ve bu siteyi birkaç ekran görüntüsü + çok kısa bir prompt'tan iki modele yeniden kurduruyor. Prompt'ta yalnızca Next.js + TypeScript, "parçacık efekti statik olmasın, akıcı olsun, responsive olsun" deniyor; kalan her detayı (imleç animasyonu, bulut yapısı, teknoloji seçimi) modele bırakıyor. Modeller ayrı portlarda (3000/3001) çalıştırılıp tarayıcıda karşılaştırılıyor. Fable 5 hem bulut yapısını hem de imlecin oluşturduğu dairesel boşluğu okuyup korurken, Opus 4.8 parçacık altyapısını Three.js ile kurmasına rağmen tasarımı kendi kafasına göre bozuyor ve dairesel etkileşimi kaçıryor. Vlogger sonuç olarak Fable 5'i 4-5 adım önde buluyor; fakat ilk görüntüyü de kusursuz kuramadığı için modelin "devrimci" değil iyi bir iyileştirme olduğunu, asıl gürültünün pazarlama + ayrı API/pazarlanma değişikliğinden kaynaklandığını savunuyor. Her iki model de iş üretmeye uygun; zor/görsel okuma ağırlıklı işler için Fable 5 tercih edilecek, Opus 4.8 de hâlâ aktif kullanılacak.
## Bölümler
- 0:00 Giriş — Fable 5 çevrimi, "devrim mi pazarlama mı" sorusu ve aynı screenshot+prompt ile ikili test planı
- 1:03 Tasarım tanıtımı — AETHRA hero'su: periyodik dalgalar, dağılan parçacıklar, hover'da dairesel boşluk
- 2:04 Ekran görüntüsü seçimi — çoklu kare, imleç animasyonunu ve bulut hareketini farklı konumlarda gösterme mantığı
- 3:06 Prompt içeriği — kısa tutulma, Next.js+TS, "statik değil", "smooth", detaylar modele bırakılma
- 4:07 Gönderim — Fable 5 ve Opus 4.8 için ayrı dosya/oturum, aynı prompt, port ayrımı
- 5:11 Sonuç karşılaştırma — 3000 (Fable) tasarım + imleç dairesi korunmuş; 3001 (Opus) bozuk
- 6:18 Opus analizi — dairesel boşluğu okuyamama, tasarımı kendi başına değiştirme; Fable her denemede daha yakın
- 7:18 Yorum — Fable 5 "4-5 adım önde", pazarlama eleştirisi, Opus'un Three.js ile parçacık kurması
- 8:21 Kullanım tercihi — zor/animasyon işler Fable'e; Opus 4.8 de projelerde devam
- 9:26 Erişim değişikliği — 12'ye kadar planda, sonrası ayrı token/kredi ödemeli API
- 10:30 Kapanış — devrimci değil iyi iyileştirme; her iki model de kullanılacak, yorum/abonelik çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Fable 5 | ? | teknik | yok | Testte kullanılan AI kodlama modeli; ekran görüntüsünden tasarımı ve imleç etkileşimini Okus'tan iyi okuyor | 5:11 | Fable tarafının imleç dairesini koruduğunu gözlemliyor, “came out closer to the result” |
| Opus 4.8 | ? | teknik | yok | Karşılaştırma modeli; parçacık altyapısını kuruyor ama görsel referansı okuyamıyor | 6:18 | Dairesel boşluğu anlayamadığı, tasarımı kendi başına bozduğu görülüyor |
| Next.js | ? | teknik | yok | Prompt'ta istenen framework; site bu zeminde kuruluyor | 4:39 | Prompt metni “build it with Next.js and TypeScript” diyor |
| TypeScript | ? | teknik | yok | Prompt'ta istenen dil; Next.js ile birlikte kullanılıyor | 4:39 | Prompt'ta “Next.js and TypeScript project” ibaresi var |
| Three.js | ? | teknik | yok | Parçacık/3B animasyon için kütüphane; Opus'un altyapıda seçtiği | 7:18 | Anlatıcı Opus'un “already set it up in Three.js” olduğunu söylüyor |
| Ekran görüntüsüyle tasarım okutma | ? | iş akışı | yok | Modeli teknik detay vermeden görsel referanstan site kurdurma yöntemi | 2:04 | Bulut yapısının hareketi için farklı konumlarda birden çok kare gönderiliyor |
| Kısa prompt + detayları modele bırakma | ? | ipucu | ? | Sadece framework + "statik değil/akıcı/responsive" demek, gerisini modele seçtir | 4:07 | “pick every detail yourself … choose the technology yourself” talimatı veriliyor |
| Parçacık efektinin hareketli olduğunu belirtme | ? | ipucu | yok | Yoksa modelin referansı statik görsel sanmasını önler | 3:06 | “Otherwise it might think it's an image” uyarısı |
| İmleç animasyonunu çoklu kareyle gösterme | ? | ipucu | yok | Hover dairesel boşluğunun farklı konumlarda kareyle gösterilmesi | 2:04 | Dairesel boşluk ve bulut hareketi için 3. kare ekleniyor |
| Ayrı portlarda çalıştırıp karşılaştırma | ? | ipucu | yok | İki modeli 3000/3001'de yanyana açıp farkı görselleştirme | 5:11 | “One on port 3000, one on port 3001” |
| AETHRA site/UI yapım promptu | ? | prompt | yok | Ekranda gösterilen, iki modele de gönderilen orijinal prompt (EN+TR) | 0:31 | Prompt kutuları tam ekranda; parçacık/3B/responsive maddeleri okunuyor |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Fable 5, Opus 4.8'den 4-5 adım önde | 7:18 | karşılaştırma |
| Fable 5 imlecin dairesel boşluğunu anladı, Opus 4.8 anlayamadı | 6:18 | özellik |
| Opus 4.8 prompt'a rağmen tasarımı kendi başına değiştirdi | 6:18 | özellik |
| Her denemede Fable 5 daha yakın sonuç veriyor | 6:18 | karşılaştırma |
| Opus 4.8 parçacık yapısını Three.js ile kurdu ama tasarımı okuyamadı | 7:18 | özellik |
| Fable'in dağınık sonucu 3-4 / 4-5 prompt ile düzeltilebilir | 6:18 | sayısal |
| Opus 4.8 ile Fable 5'in işi, birkaç prompt farkıyla yapılıyor | 8:21 | karşılaştırma |
| Fable 5 12'ye kadar planda, sonrası ayrı token/kredi API | 9:26 | sayısal |
| Opus 4.8 daha yavaş anlıyor, daha fazla promptla tolere edilebilir | 10:30 | karşılaştırma |
| Model devrimci değil; ilk gönderimde bulut yapısını dağınık kurdu | 10:30 | karşılaştırma |
## Site/UI teknikleri
| teknik | kanıt | kütüphane/araç | bizde |
|---|---|---|---|
| Parçacık bulut efekti (periyodik dalga + dağılım) | 1:33 kare + ASR | tahmin: Three.js | yok |
| 3B derinlik hissi, gerçek zamanlı organik hareket | 0:31 prompt karesi | tahmin: Three.js | yok |
| Hover'da dairesel boşluk / parçacıkları imlece çekme | 1:33, 6:48 kare | tahmin: Three.js | yok |
| Akıcı (smooth) animasyon, real-time | 0:31 prompt karesi | tahmin: Three.js | yok |
| Koyu/temiz premium hero yerleşimi + üst nav grid | 1:33 kare | yok | yok |
| Tipografi: dev AETHRA başlık + alt başlık | 1:33 kare | yok | yok |
## Kareden okunanlar
- 0:31 Prompt kutuları: “Next.js and TypeScript”, “particle effect must not be a static image”, “responsive and performant”, “choose … libraries yourself”
- 1:33 “AETHRA — AI-powered video intelligence”; nav: Products/Solutions/Support/Partners/About/Contact; “Get started” / “Explore the platform”
- 4:39 Oturum adı “Particle cloud landing page”; branch “fable main”; model kutusu “Fable 5 … faster than Opus 4.8”
- 5:44 Tarayıcı çubuğu “localhost:3000” (Fable sonucu)
- 6:48 Tarayıcı çubuğu “localhost:3001” (Opus sonucu)
## Belirsizlikler
- “Fable 5” ve “Opus 4.8” adları hem ASR'de hem ekranda geçiyor; gerçek üretici/model karşılığı (muhtemelen Claude/Anthropic serisi) doğrulanamıyor, kurgusal/altyazı adı olma ihtimali var
- Three.js adı yalnız ASR'de; ekranda/açıklamada görünmediği için kütüphane alanına “tahmin” işlendi
- AETHRA'nın gerçek marka mı yoksa test için uydurma başlık mı olduğu net değil
- “4-5 adım önde”, “4-5 prompt ile düzelir” gibi sayılar vloggerın öznel takdiri
## Atlanan segment oranı
0/11 (paket tam okuma)

rapor: Yunu27g7sLw · aday: 11 · Aynı screenshot+prompt ile Fable 5 ve Opus 4.8'e animasyonlu parçacık hero (AETHRA) kurduruldu; Fable 5 tasarım+imleç dairesini iyi okudu, Opus 4.8 Three.js altyapı kurdu ama tasarımı kaçırdı; sonuç "devrim değil, iyi iyileştirme + ayrı API/pazarlama" olarak çerçevelendi.
