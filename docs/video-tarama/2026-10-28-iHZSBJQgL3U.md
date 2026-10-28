# EKİP YAPAY ZEKAYI GÖRSEL VE VİDEO YAPIMINDA NASIL KULLANIYOR?
## Künye
EKİP YAPAY ZEKAYI GÖRSEL VE VİDEO YAPIMINDA NASIL KULLANIYOR? · Orkun v2 (Orkun Işıtmak) · süre: 11:28 · tr · https://youtu.be/iHZSBJQgL3U · şema 2
## Özet
Ork Factor kurgu ekibi (Hasan, Mert, Soner) grafik ve videoları Google Flow üzerinden üretiyor; Nano Banana Pro ile görsel, Veo 3.1 ve yeni Omni Flash ile video yapıyor.
Eski yöntem: Gemini'a "bunu JSON prompt'a çevir" deyip çıktıyı Flow'a yapıştırmak; bazen çok iyi, bazen çok kötü. Yeni yöntem: Gemini içindeki görsel/video bölümüne arkadaşına anlatır gibi yazmak, düşünce seviyesini en üste almak.
Omni Flash: videoyu yükle, "Orkun'u çıkar, kıyafeti değiştir" de; karakter yüz taraması, ses, çoklu video/foto referansı ile iteratif düzenleme. Flow'da maske ile bölgesel düzenleme ve yeni araçlar (Mask Magic, Shot Explorer vb.).
Örnekler: challenge logoları Nano Banana'dan, "animate like freeze and make background greenscreen" ile animasyon, drone fotoğrafına çizgi çizip yol tarif etme, geceden sabaha time lapse. Yapay zeka işin %90'ını çözüyor, kalan %10 post (green screen temizliği, tracking).
Sonra Google I/O özeti: Gemini 3.5 Flash (3.1 Pro'ya göre ~4 kat hızlı kod), Antigravity/Cursor'da seçilebilir; TPU 8t (eğitim) ve 8i (inference); Xreal karma gerçeklik gözlüğü; Android Studio'da web uygulamasını React Native/Android'e çevirme.
## Bölümler
- 0:00 Giriş ve Flow/Nano Banana — ekibin iş akışı, Gemini içinden görsel üretimi
- 1:00 JSON prompt'tan sohbet tabanlı prompt'a geçiş
- 2:02 Zaman kazancı — 3D animasyon iki hafta yerine üç gün
- 3:03 Omni Flash — video düzenleme, karakter, ses, kombin referans
- 4:04 Flow projeleri — Ork Factor challenge logoları, Nano Banana ile logo
- 5:05 Animasyon ve time lapse prompt örnekleri
- 6:06 Drone çizgi yöntemi ve post (%90/%10)
- 7:07 Google I/O: 3.5 Flash
- 8:08 TPU 8t/8i
- 9:08 Xreal gözlük
- 10:10 Android Studio React Native dönüşümü ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Google Flow | Google Flow (kayit, 1.00) | skill | yok | Google'ın video/görsel üretim ortamı; ekip tüm işi burada yapıyor | 0:00 | ekip "normalde Flow üzerinden yaptık", Google yeni ürünleri içine ekliyor |
| Omni Flash | Omni Flash (kayit, 1.00) | skill | yok | Video düzenleme/üretim modeli: kişi çıkar, kıyafet ve hareket değiştir, referansla birleştir | 3:03 | video yükleyip değişiklik yazılıyor, iteratif; kareden "Create with Omni" |
| Nano Banana Pro / Nano Banana 2 | nano-banana-2 (plugin, 1.00) | skill | yok | Görsel üretim modeli; logo ve challenge görseli | 0:00 | kareden "Nano Banana 2 ile içerik üretin" ekranı |
| Veo 3.1 | Veo 3.1 (kayit, 1.00) | skill | yok | Video modeli, Ork Dijital Banana'nın altında | 0:00 | konuşmada "View 3.1" olarak geçiyor, Veo diye okundu |
| Ork Dijital Banana | yok | CLI | yok | Ekibin kendi yaptığı araç; Nano Banana Pro ve Veo 3.1 kullanıyor | 0:00 | konuşma; yorumda GitHub'da public olacak mı diye soruluyor |
| Gemini uygulaması içinden görsel/video | marketing-skills:video (skill, 1.00) | iş akışı | yok | Dış prompt dönüşümü olmadan sohbette tarif et, prompt'u kendisi kurar | 1:00 | "arkadaşına anlatır gibi yaz", düşünce seviyesi en üstte |
| JSON prompt dönüştürme | yok | teknik | yok | Gemini'a isteği JSON prompt'a çevirtip Flow'a yapıştırmak; artık gerekmiyor | 1:00 | kare 1:00 JSON anahtarları; "bazen çok iyi bazen çok kötü" |
| Düşünce seviyesini en üste alma | yok | ipucu | yok | Model seçerken thinking level yüksek tutmak | 0:00 | "model seçerken düşünce seviyesini en yukarıya alırım" |
| Flow maske ile bölgesel düzenleme | yok | teknik | yok | Maskeyle yalnız seçili yeri değiştirmek | 4:04 | konuşma; kareden Mask Magic |
| Flow araçları (Mask Magic, Shot Explorer, Scene Explorer, Simple Sketch, Video Granulator, Blob Tracking, Frame Deconstructor, Prompt Tree, Story Sketch, Mockup) | yok | skill | yok | Flow'un Explore Tools listesi | 7:00 | kare OCR'da araç adları; yorumda nereden bulunur sorusu |
| Animasyon prompt'u: freeze + green screen | yok | ipucu | yok | Görseli donmuş canlandırma ve yeşil arka plana çevirmek, kompozisyonu bozmadan | 5:05 | ekranda "animate it like freeze and make background greenscreen (dont change position)" |
| Time lapse gece-gündüz prompt'u | yok | ipucu | yok | Drone fotoğrafından geceden sabaha time lapse, rengi bozma | 5:05 | Türkçe prompt gösteriliyor |
| Görüntü üstüne çizgi ile drone yolu | yok | teknik | yok | Fotoğrafa çizgi çizip kamera yolunu video modeline tarif etmek | 6:06 | kareler 6:52 ve 6:56: Google Earth New York üstünde kırmızı ok |
| Green screen temizliği ve tracking (post) | yok | iş akışı | yok | %90 yapay zeka, %10 kurguda temizlik ve izleme | 6:06 | konuşma |
| Gemini 3.5 Flash | Gemini 3.5 Flash (kayit, 1.00) | skill | yok | 3.1 Pro'dan yaklaşık 4 kat hızlı kod, Pro'ya yakın zeka | 7:07 | kare 8:40 model kartı "near-Pro intelligence at Flash-tier cost" |
| Antigravity | Antigravity (kayit, 1.00) | skill | yok | 3.5 Flash seçilebilen kod editörü | 7:07 | "Anti Gravity'de ya da Cursor'da" |
| Cursor | Cursor (kayit, 1.00) | skill | yok | 3.5 Flash seçilebilen kod editörü | 7:07 | aynı cümle |
| Android Studio React Native dönüşümü | yok | skill | yok | Web uygulamasını Android/React Native'e çevirip Play'e yayın | 10:10 | kareler 10:42 ve 10:44 canlı demo |
| Gemini 3.1 Flash Image | gemini-3.1-flash-image (kayit, 1.00) | skill | yok | Görsel modeli; 14 referans, karakter tutarlılığı | 8:40 | kare 8:40 model sayfası |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 3D animasyon normalde iki hafta, yapay zekayla üç gün | 2:02 | sayısal |
| Sabah grafik yapıp akşam video yayınlanan günler oldu | 2:02 | özellik |
| 3.5 Flash, 3.1 Pro'ya göre yaklaşık 4 kat hızlı kod yazıyor | 7:07 | sayısal |
| 3.5 Pro önümüzdeki ay çıkacak | 7:07 | özellik |
| Yapay zeka işin %90'ını çözüyor, %10 post gerekiyor | 6:06 | sayısal |
| Omni videoda kişiyi çıkarır, kıyafet ve hareketi değiştirir, diğerini aynı tutar | 3:03 | özellik |
| TPU: iki yeni çip, biri eğitim biri inference | 8:08 | özellik |
| Android Studio web uygulamasını React Native'e çevirip Play'de yayınlıyor | 10:10 | özellik |
| Hız/zeka benchmark'ında 3.5 Flash diğerlerine yakın kalite, daha hızlı | 8:08 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Flow | Google Flow | ekip ana aracı |
| konuşma 0:00 | Nano Banana Pro | Nano Banana Pro / Nano Banana 2 | görsel üretim |
| konuşma 0:00 | Veo 3.1 | Veo 3.1 | "View 3.1" ASR hatası |
| konuşma 0:00 | Ork Dijital Banana | Ork Dijital Banana | ekibin aracı |
| konuşma 1:00 | JSON prompt | JSON prompt dönüştürme | eski yöntem |
| konuşma 3:03 | Omni Flash | Omni Flash | video düzenleme |
| konuşma 3:03 | karakter yüz taraması | Omni Flash | aynı model özelliği |
| konuşma 4:04 | maske | Flow maske ile bölgesel düzenleme | maskeyle yer değiştirme |
| konuşma 5:05 | animate freeze prompt | Animasyon prompt'u: freeze + green screen | kare 5:18 |
| konuşma 5:05 | time lapse | Time lapse gece-gündüz prompt'u | kare 6:02 |
| konuşma 6:06 | green screen temizliği, tracking | Green screen temizliği ve tracking (post) | %10 post |
| konuşma 6:06 | drone çizgi | Görüntü üstüne çizgi ile drone yolu | kare 6:52 |
| kare 7:00 | Mask Magic, Shot Explorer vb. | Flow araçları (Mask Magic, Shot Explorer, Scene Explorer, Simple Sketch, Video Granulator, Blob Tracking, Frame Deconstructor, Prompt Tree, Story Sketch, Mockup) | Explore Tools listesi |
| konuşma 7:07 | 3.5 Flash | Gemini 3.5 Flash | 4 kat hızlı |
| konuşma 7:07 | Antigravity | Antigravity | kod editörü |
| konuşma 7:07 | Cursor | Cursor | kod editörü |
| konuşma 7:07 | 3.1 Pro | Gemini 3.5 Flash | karşılaştırma tabanı |
| kare 8:40 | 3.1 Flash Image | Gemini 3.1 Flash Image | model sayfası |
| kare 8:40 | Gemini 3.1 Flash-Lite | aday değil: genel kavram | yalnız model listesinde görünüyor |
| kare 8:40 | Gemma 4 | aday değil: genel kavram | model listesi satırı |
| kare 7:50 | Claude Sonnet/Opus/Haiku grafik | aday değil: genel kavram | benchmark grafiğinde rakip modeller |
| konuşma 8:08 | TPU 8t/8i | aday değil: konu dışı | donanım anlatımı, uygulanabilir ipucu yok |
| konuşma 9:08 | Xreal gözlük | aday değil: konu dışı | donanım tanıtımı |
| konuşma 10:10 | Android Studio React Native | Android Studio React Native dönüşümü | canlı demo |
| konuşma 10:10 | React Native | Android Studio React Native dönüşümü | dönüşüm hedefi |
| açıklama | linktr.ee/orkunisitmak | aday değil: konu dışı | kanal bağlantı sayfası |
| açıklama | youtube.com/orkunisitmak | aday değil: konu dışı | kanal bağı |
| linkli sayfa | friendsoforka.com, orkdigital.com | aday değil: konu dışı | linktree üzerindeki kanal/ürün bağları |
| kare 0:02 | orkfactor.com | aday değil: konu dışı | yarışma sitesi, video önizlemesi |
| yorum | Seedance | aday değil: genel kavram | yorumcu rakip video modeli diyor |
| yorum | Claude Code | aday değil: genel kavram | yorumcu şaka olarak anıyor |
| yorum | Ork dijital banana GitHub | Ork Dijital Banana | public olacak mı sorusu |
| yorum | 07:01 tool'lar nereden bulunur | Flow araçları (Mask Magic, Shot Explorer, Scene Explorer, Simple Sketch, Video Granulator, Blob Tracking, Frame Deconstructor, Prompt Tree, Story Sketch, Mockup) | izleyici soruyor |
| yorum | Gemini pro olmadan video | Gemini uygulaması içinden görsel/video | izleyici sorusu |
| konuşma 0:00 | Google I/O | aday değil: konu dışı | etkinlik anlatısı |
| konuşma 1:00 | düşünce seviyesi | Düşünce seviyesini en üste alma | model seçici ayarı |
## Site/UI teknikleri
| teknik | kanıt | kütüphane/araç | bizde |
|---|---|---|---|
| animasyonlu challenge haritası geçişleri (karakteristik harita) | 5:05 konuşma | tahmin: After Effects | yok |
| yeşil ekran animasyonlu logo | 5:18 kare m005 prompt | tahmin: Nano Banana + Flow | yok |
| 3B harita üstü çizgiyle kamera yolu | 6:52 kare m004120 | tahmin: Google Earth + Photoshop | yok |
## Kareden okunanlar
- 0:02 Ork Factor bölüm başlıkları, orkfactor.com bağlantısı (OCR bozuk)
- 5:18 prompt "animate it like freeze and make background greenscreen (dont change position)"
- 6:02 "bunu timelapse yapalım. geceden sabah olsun,"
- 6:52 Photoshop/Google Earth New York, kırmızı yol çizgisi, "Build your skills" kutusu
- 7:00 Flow Explore Tools: Mask Magic, Shot Explorer, Scene Explorer, Simple Sketch, Video Granulator, Blob Tracking, Frame Deconstructor, Prompt Tree, Story Sketch, Mockup, DepthWarp 4D
- 8:40 Gemini model sayfası: 3.5 Flash, 3.1 Flash-Lite, 3.1 Flash Image, 3 Pro Image
- 10:42 Android Studio, Pixel 10 Pro emülatörü, plan.md sekmesi, Theme.kt
## Belirsizlikler
- "View 3.1" büyük olasılıkla Veo 3.1; "Org Dijital Banana" için link yok.
- Sözlükteki Claude/Cursor/Hermes/Geist/Descript vb. eşleşmeleri çoğunlukla ASR veya OCR gürültüsü.
- OCR gürültülü (orkfactor.com bozuk); TPU 8t/8i adları OCR'dan.
- 7:50 grafikte rakip model adları kısmen bulanık; yorumcu sansür iddia ediyor.
## Atlanan segment oranı
0/12 (paket tam okuma)
