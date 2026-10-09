# Comment “Fast” for the link
## Künye
Comment “Fast” for the link · albert.olgaard · süre: 0:32 · ? · https://www.instagram.com/reel/DdjdN0CCcU8/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-25 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 28048 tk · claude-haiku-5-5: claude-haiku-5-5 · 28833 tk
## Özet
Kısa reel: Laya adlı açık kaynak, yerel çalışan bir System 1 karar modeli tanıtılıyor. Anlatıma göre Jev yaklaşık 250 ms'de yanıt verirken Laya yaklaşık 30 ms'de yanıt veriyor, çünkü buluta gidip gelmiyor. Temel model her işte iyi değil, belirli kullanım alanları için ince ayar gerekiyor. Bu ince ayar Claude Code ile yapılabilir. Link için 'fast' yorumu isteniyor.
## Bölümler
- 0:00 Laya'nın tanıtımı: Jev'e hızlı açık kaynak alternatif
- 0:07 pip ile kurulum ve bulut API'ye karşı yerel çalışma
- 0:22 GitHub README ve dürüst sınırlar
- 0:25 Kullanım alanları ve ince ayar sonuçları
- 0:28 Claude Code ile ince ayar ve link çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Laya | yok | CLI | https://github.com/NandhaKishorM/laya | Yerel çalışan, çok dilli, otoregresif olmayan System 1 karar motoru; tek ileri geçişte tipli kararlar verir. | 0:22 | README başlığı 'Multilingual, non-autoregressive System 1 decision engine', sürüm v0.3.4. (karede: GitHub sayfası NandhaKishorM/laya; README'de laya logosu, 5.2k yıldız, 468 fork, v0.3.4, Apache-2.0 lisansı.) |
| Jev | yok | CLI | yok | Karşılaştırma referansı; yaklaşık 250 ms'de yanıt veren, kod yazamayan System 1 modeli. | 0:00 | Jev'in yaklaşık 250 milisaniyede yanıt verdiği anlatılıyor. |
| Claude Code | yok | CLI | yok | Laya'yı destek biletleri üzerinde ince ayarlamak için kullanılıyor. | 0:29 | Ekran metni: 'Claude Code' ve 'Fine-tune Laya on my support tickets'. (karede: Kare listesinde yok; bilgi OCR metninden (0:28-0:29).) |
| pip | yok | CLI | yok | Laya paketini kuran Python paket yöneticisi. | 0:08 | OCR: 'Successfully installed laya-0.3.4', 'pip', 'Terminal'. (karede: Kare yok; OCR metni terminalde pip kurulum çıktısını gösteriyor.) |
| GitHub | yok | teknik | yok | Laya deposunun barındırıldığı platform. | 0:22 | Adres çubuğunda github.com/NandhaKishorM/laya. (karede: Tarayıcıda GitHub depo sayfası, Code/Issues/Pull requests sekmeleri.) |
| laya-multilingual | yok | teknik | yok | Laya'nın çok dilli kontrol noktası; İngilizce'de daha zayıf. | 0:23 | README: 'laya-multilingual is weaker on English'. (karede: README 'Honest limits' maddesinde laya-multilingual kod biçiminde yazılı.) |
| RLCD | yok | teknik | yok | Laya'nın katı biçimde uygun puanlama kurallarıyla pekiştirmeli öğrenmeyle eğitilmesi. | 0:22 | README: reinforcement learning against strictly proper scoring rules (RLCD). · kanıt: kare (karede: README giriş paragrafında parantez içinde (RLCD) yazıyor.) |
| Laya'yı destek bileti sınıflandırma için ince ayarlamak | yok | prompt | yok | Claude Code'dan Laya modelini kullanıcının destek biletleri üzerinde ince ayarlaması isteniyor. | 0:29 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip install laya | Laya paketini kurar; çıktıda laya-0.3.4 görünür. Komut metni tam okunmadı, çıktıdan çıkarıldı. | 0:08 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Jev yaklaşık 250 ms'de yanıt verirken Laya yalnızca yaklaşık 30 ms'de yanıt veriyor. | 0:00 | karşılaştırma |
| Laya yerelde çalıştığı için buluta gidip gelmez, bu yüzden daha hızlıdır. | 0:00 | özellik |
| README'ye göre ince ayarlı kontrol noktası 0.766 doğruluk veriyor; temel modeller zero-shot'ta şansa yakın (0.362 ve 0.352). | 0:22 | sayısal |
| Temel model her işte iyi değil; belirli kullanım alanları için eğitilmeli, bunu Claude ile yapabilirsiniz. | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Jev | Jev | Jev'in 250 ms'de yanıt verdiği söyleniyor. |
| konuşma 0:00 | Laya (Naya olarak söylenen) | Laya | Yerel System 1 modeli olarak tanıtılıyor. |
| konuşma 0:00 | Claude | Claude Code | İnce ayarın Claude ile yapılabileceği söyleniyor. |
| konuşma 0:00 | bulut (cloud) | aday değil: genel kavram | Buluta gidip gelmek yerine yerel çalışma anlatılıyor. |
| kare 0:08 | pip | pip | Terminal kurulum çıktısı. |
| kare 0:08 | Terminal / Shell | aday değil: genel kavram | Terminal penceresi etiketi. |
| kare 0:11 | route(ticket) / handler.py | aday değil: genel kavram | Örnek kod parçası. |
| kare 0:12 | cloud API | aday değil: genel kavram | Bulut API ile yerel karşılaştırması. |
| kare 0:22 | GitHub | GitHub | Depo sayfası gösteriliyor. |
| kare 0:22 | RLCD | RLCD | README'de RLCD yazıyor. |
| kare 0:22 | Apache-2.0 lisansı | aday değil: genel kavram | Lisans etiketi. |
| kare 0:23 | laya-multilingual | laya-multilingual | README maddesinde geçiyor. |
| kare 0:23 | SST-5 | aday değil: genel kavram | Kıyaslama adı, yalnızca README'de anılıyor. |
| kare 0:25 | Model routing / Moderation / Prompt guardrails / Support triage | aday değil: genel kavram | Kullanım alanı listesi. |
| kare 0:25 | typed-decisions accuracy, epoch grafiği | Laya | İnce ayar eğitim ilerlemesi gösteriliyor. |
| kare 0:28 | Claude Code | Claude Code | Ekranda Claude Code ve ince ayar istemi. |
| kare 0:30 | Instagram yorumlar paneli | aday değil: konu dışı | Yorum çağrısı arayüzü. |
| ekran 0:22 | github.com/NandhaKishorM/laya | Laya | Depo adresi. |
| ekran 0:30 | github.com/NandhaKish | Laya | Yazar profili bağlantısı. |
| açıklama | Comment 'Fast' for the link | aday değil: konu dışı | Yorum çağrısı. |
## Kareden okunanlar
- 0:22: GitHub'da NandhaKishorM/laya deposu: README, Honest limits, 5.2k yıldız, 35 izleyici, 468 fork, v0.3.4 sürümü.
- 0:23: README 'Honest limits' maddesi vurgulanmış: temel kontrol noktaları zero-shot'ta şansa yakın; Laya hızlı bir temel model; ordinal skor soruları en zayıf (SST-5 0.372).
- 0:30: Instagram yorumlar paneli 'No comments yet'; github.com/NandhaKish yazılı bir mesaj kutusu; altyazı 'LINK TO THE MODEL'.
## Belirsizlikler
- Dilin adı konuşmada 'Naya' geçiyor, ekranda 'Laya' yazıyor; Laya kabul edildi.
- 'Jev' adı transkripsiyonda geçiyor, gerçek adı belirsiz (muhtemelen başka bir System 1 aracı).
- Sözlükteki Descript, v0, Codex, Go eşleşmeleri videoda gösterilmedi veya gerçek kullanım kanıtı yok.
- Tam pip komutu okunmadı, yalnız kurulum çıktısı var.
- Yorumlar girişsiz alınamadı.
- Kare listesindeki 3 kare 0:22, 0:23, 0:30'a ait; 0:29 prompt karesi görsel olarak doğrulanmadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/NandhaKishorM/laya | 0:22 | ekran | evet |
| github.com/NandhaKish | 0:30 | ekran | evet |
## İş akışı
- 1. adım — Laya'nın GitHub deposunu açıp README'yi incelemek — araçlar: GitHub
- 2. adım — README'deki 'Honest limits' bölümünü ve benchmark sonuçlarını okumak — araçlar: GitHub
- 3. adım — Terminalde pip ile laya-0.3.4 paketini kurmak — araçlar: pip, Terminal
- 4. adım — Karar yönlendirme örneğini (route, classify, escalate, refund) göstermek — araçlar: handler.py (örnek kod)
- 5. adım — Destek biletleriyle ince ayar yapmak için Claude Code'a istek yazmak — araçlar: Claude Code, Claude
- 6. adım — İzleyicinin bağlantıyı alması için yorumda 'fast' istemek — araçlar: Instagram yorumları
## Promptlar
- Laya'yı destek bileti sınıflandırma için ince ayarlamak — Claude Code'dan Laya modelini kullanıcının destek biletleri üzerinde ince ayarlaması isteniyor.
