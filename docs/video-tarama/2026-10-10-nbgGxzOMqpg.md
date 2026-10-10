# I Put the iOS Simulator in Cursor, Claude Code & Codex
## Künye
I Put the iOS Simulator in Cursor, Claude Code & Codex · Antoine van der Lee · süre: 1:40 · en-orig · https://youtu.be/nbgGxzOMqpg · şema 2
motor: parti 2026-10-10-short-14 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 44367 tk · claude-haiku-5-5: claude-haiku-5-5 · 56200 tk
## Özet
Antoine van der Lee, RocketSim 17'nin ilk kavram kanıtını (PoC) gösteriyor: iOS Simulator ekranı Cursor'ın tarayıcısında etkileşimli çalışıyor. Erişilebilirlik öğeleri listeleniyor, öğeler seçilip görsel geri bildirim yazılıyor, ekran görüntüsü kaydediliyor ve 'Copy prompt' ile ajana hazır prompt sohbet alanına yapıştırılıyor. Prompt öğe koordinatlarını ve RocketSim agent skill (rocketsim CLI) talimatını içeriyor. Özellik henüz yayımlanmamış PoC olarak sunuluyor; sabit yorumda sonradan yayımlandığı belirtiliyor.
## Bölümler
- 0:00 iOS Simulator'ü yapay zekâ araçlarına taşımak
- 0:12 RocketSim 17 kavram kanıtı
- 0:28 Erişilebilirlik ve Simulator bağlamı
- 0:42 Uygulama öğelerine görsel geri bildirim eklemek
- 1:03 Ajana hazır prompt kopyalamak
- 1:25 Simulator geri bildirimini koda bağlamak
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| RocketSim | yok | plugin | https://github.com/AvdLee/RocketSimApp | iOS Simulator'ü AI aracının tarayıcısına taşıyan, erişilebilirlik listesi ve görsel geri bildirim sunan uygulama (v17 PoC). | 0:12 | Altyazı: 'first proof of concept of Rocket Sim 17'; karede RocketSim başlığı. (karede: Sağda 'RocketSim iPhone Air - iOS 26.5' başlıklı simülatör, solunda Accessibility, sağında Visual Feedback paneli.) |
| Cursor | yok | CLI | yok | Demonun yürütüldüğü AI kodlama aracı; simülatör onun tarayıcı panelinde. | 0:00 | 'I'm right here in cursor'. (karede: Sol panelde ajan sohbeti, altta 'cursor/1e38c1e9' worktree etiketi.) |
| Claude Code | yok | CLI | yok | RocketSim'in köprü kurduğu AI kodlama araçlarından biri. | açıklama | Açıklama: 'into Cursor, Claude Code, and Codex'. |
| Codex | yok | CLI | yok | RocketSim'in desteklediği diğer AI kodlama aracı. | 0:00 | 'whether it's Claude, cursor, codex, it doesn't matter'. |
| GPT-5.6 Sol Medium | yok | teknik | yok | Cursor ajan sohbetinde seçili model. | 1:04 | Model seçici etiketi ekranda görünüyor. (karede: Sohbet giriş alanının altında 'GPT-5.6 Sol Medium' etiketi.) |
| RocketSim agent skill | yok | skill | yok | Prompt içinde ajana simülatörü başlatıp öğeleri doğrulatan skill. | 1:07 | Prompt metni: 'Use the RocketSim agent skill'. (karede: Yapıştırılan prompt'ta staticText satırları ve RocketSim agent skill talimatı.) |
| rocketsim CLI | yok | CLI | yok | 'rocketsim screen' ve 'rocketsim elements' komutlarıyla simülatör ve öğeleri kontrol eden CLI. | 1:07 | Prompt metninde 'rocketsim elements' ve 'rocketsim screen' geçiyor. (karede: Prompt satırlarında rocketsim screen / rocketsim elements ifadeleri.) |
| iOS Simulator | yok | teknik | yok | Xcode simülatörü; iPhone Air iOS 26.5 üzerinde çalışan hisse analiz uygulaması tarayıcıya akıtılıyor. | 0:12 | 'this is not the simulator' ve karede cihaz etiketi. (karede: RocketSim başlığı altında 'iPhone Air iOS 26.5'.) |
| Accessibility hierarchy | yok | teknik | yok | Tüm erişilebilirlik öğelerini listeleyen ve seçim sağlayan panel. | 0:12 | 'it lists all the accessibility elements'. |
| Visual Feedback paneli | yok | iş akışı | yok | Seçilen öğelere yorum yazılan, ekran görüntüsü kaydeden ve prompt kopyalayan panel. | 0:50 | Panelde 'Describe the visual change...' alanı ve 'Copy prompt' düğmesi. · kanıt: kare (karede: Sağ panelde 'Visual Feedback', '3 elements · Apple Inc., NASDAQ, • Technology' kartı.) |
| Worktree | yok | teknik | yok | Etkin git worktree bilgisi RocketSim arayüzünde gösteriliyor. | 0:28 | 'the work tree that's currently active'. |
| Etkileşimli inceleme modunun geliştirilmesi | yok | prompt | yok | Çarpı imleci (crosshair) etkinken ekranı dondur, öğe karelerini hover'da göster; sürükleyerek veya Cmd/Shift+tıkla ile birden çok öğe seç. | 0:00 | kaynak: kare |
| Öğelere görsel geri bildirim vermek | yok | prompt | yok | Seçilen öğeler için 'Increase the contrast' ve 'Better align these' gibi görsel değişiklik yorumları. | 0:50 | kaynak: kare |
| Kopyalanan ajana hazır geri bildirim promptu | yok | prompt | yok | Ajana RocketSim agent skill ile simülatörü başlatmasını, öğeleri rocketsim elements ile doğrulamasını ve ilgili kodu bulup uygulamasını söyler; öğe koordinatları listelenir. | 1:07 | kaynak: kare |
## Açıklama bağlantıları
- https://www.rocketsim.app — RocketSim ürün sayfası (Mac App Store'dan indirilebilir uygulama). · aday: evet (RocketSim) · İzleyicinin kullanabileceği araç; alan adı videoda gösterilen RocketSim'i adlandırıyor. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Erişilebilirlik ağacı yan paneli (accessibility tree sidebar) | Sol yan panelde erişilebilirlik öğe listesi; her satır bir UI öğesi (BUTTON, STATICTEXT vb.) ve sayıyı gösterir. (karede: Sol panelde 'Accessibility' başlığı ve '24 elements' sayacı, altında BUTTON, STATICTEXT, RADIOBUTTON satırları görünüyor.) | 0:00 | kare |
| Cihaz çerçevesi önizlemesi (device frame preview) | Simülatör uygulamasının cihaz çerçevesi içinde gösterilmesi. (karede: Ortada iPhone çerçevesi içinde 'All Symbols' ekranı görünüyor; üstte RocketSim cihaz seçici var.) | 0:00 | kare |
| Simülatör seçici açılır menü (dropdown) | Üstte cihaz ve iOS sürümünü seçen açılır menü. (karede: Cihaz çerçevesinin üstünde 'RocketSim' ve 'iPhone Air - iOS 26.5' etiketli açılır menü görünüyor.) | 0:00 | kare |
| Etkileşim ipucu çubuğu (hint bar) | Alt ipucu: tıklayarak etkileşim ve Option tıklayarak inceleme. (karede: Ekranın alt sağında 'Click, drag, scroll, or type to interact - Option-click to inspect' metni yazıyor.) | 0:00 | kare |
| Öğe sınır kutusu vurgusu (bounding box overlay) | Hover ile seçilen öğenin etrafında kırmızı dış çizgi; hangi öğenin hedeflendiği gösterilir. (karede: Ekran görüntüsünde 'Apple Inc.' başlığı etrafında kırmızı dikdörtgen çerçeve var.) | 0:49 | kare |
| Geri bildirim kartı (feedback card) ve metin alanı (textarea) | Bir öğeye bağlı geri bildirim kartı; üstte öğe adı, altta metin alanı ve öğenin küçük ekran görüntüsü bulunur. (karede: Sağ panelde 'staticText · On-device AI' başlıklı kart ve içinde yazılan 'in' metni görünüyor.) | 0:44 | kare |
| Çoklu öğe seçimi ve gruplama (multi-select grouping) | Birden çok öğe seçildiğinde tek kart altında gruplanır; kart öğe sayısını ve adlarını gösterir. (karede: Sağ panelde '3 elements · Apple Inc., NASDAQ, • Technology' yazan grup kartı ve boş açıklama alanı var.) | 0:50 | kare |
| Sürükleyerek dikdörtgen seçimi (drag rectangle selection) | Sürükleyerek dikdörtgen içinde öğe seçimi; seçilen öğeler ayrı kırmızı çerçevelerle işaretlenir. (karede: Simülatör ekranında 'Apple Inc.', 'NASDAQ' ve 'Technology' etiketleri kırmızı çerçevelerle seçili görünüyor.) | 0:50 | kare |
| Kopyala düğmesi ve kopyalandı durumu (copy button state) | Prompt kopyalandığında düğme 'Copied' durumuna geçer. (karede: Sağ panelin altındaki düğmede 'Copied' yazıyor.) | 1:02 | kare |
| Değişiklik özeti kartı (changes summary card) | Ajanın notları ve değişen dosyalar listesi tarayıcı panelinin üstünde gösteriliyor. (karede: Cursor'da '4 Files Changed' başlıklı kart; WebPreviewHTML.swift +14/-2 gibi satırlar var.) | 0:20 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| rocketsim screen | Simülatörü başlatıp ekranı ajana verir (prompt içinde). (karede: Prompt metninde 'Simulator with rocketsim screen'.) | 1:07 | kare |
| rocketsim elements | Her öğeyi doğrulamak için erişilebilirlik öğelerini listeler. (karede: Prompt metninde 'confirm each element via rocketsim elements'.) | 1:07 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Çalışan iOS uygulaması simülatör değil, AI aracının tarayıcısı içinde etkileşimli yaşıyor. | 0:12 | özellik |
| Seçilen öğeler gruplanıyor, ekran görüntüsü kaydediliyor ve prompt tek tıkla kopyalanıyor. | 0:42 | özellik |
| Kopyalanan prompt ajana öğenin kodda nerede yaşadığını söylüyor ve simülatörü koda bağlıyor. | 1:03 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Claude | aday değil: başka adayın parçası (Claude Code) | 'whether it's Claude, cursor, codex' |
| altyazı 0:00 | Cursor | Cursor | 'I'm right here in cursor' |
| altyazı 0:00 | Codex | Codex | 'codex, it doesn't matter' |
| açıklama | Claude Code | Claude Code | 'Cursor, Claude Code, and Codex' |
| altyazı 0:00 | RocketSim 17 | RocketSim | 'first proof of concept of Rocket Sim 17' |
| altyazı 0:12 | Stock analyzer uygulaması | aday değil: konu dışı | 'my stock analyzer app' |
| altyazı 0:12 | iOS Simulator | iOS Simulator | 'this is not the simulator' |
| altyazı 0:12 | Erişilebilirlik öğeleri | Accessibility hierarchy | 'lists all the accessibility elements' |
| altyazı 0:28 | Worktree | Worktree | 'work tree that's currently active' |
| kare 1:04 | GPT-5.6 Sol Medium | GPT-5.6 Sol Medium | Model etiketi |
| kare 0:50 | Visual Feedback paneli | Visual Feedback paneli | Panel başlığı |
| kare 1:07 | RocketSim agent skill | RocketSim agent skill | 'Use the RocketSim agent skill' |
| kare 1:07 | rocketsim CLI | rocketsim CLI | 'rocketsim elements' |
| kare 1:04 | WebPreviewHTML.swift dosyaları | aday değil: konu dışı | Değişen dosya listesi |
| kare 0:05 | 127.0.0.1:4995 canlı önizleme | aday değil: başka adayın parçası (RocketSim) | 'Live preview: http://127.0.0.1:4995/?token=[gizlendi]' |
| açıklama | rocketsim.app | RocketSim | Mac App Store bağlantısı |
| yorum | serve-sim | aday değil: konu dışı | 'nicer than serve-sim' |
| yorum | Codex tarayıcısı | Codex | 'inside the codex browser?' |
| linkli sayfa | Pulse (kean/Pulse) | aday değil: konu dışı | rocketsim.app sayfasındaki bağlantı |
| linkli sayfa | RocketSimApp GitHub | aday değil: başka adayın parçası (RocketSim) | github.com/AvdLee/RocketSimApp |
| linkli sayfa | physical-devices, location-simulation dokümanları | aday değil: konu dışı | rocketsim.app bağlantıları |
## Kareden okunanlar
- 0:00: Solda Cursor ajan sohbeti, sağda RocketSim iPhone Air simülatörü, Accessibility ve Visual Feedback ('No feedback yet') panelleri.
- 0:20: 'Live preview: http://127.0.0.1:4995/?token=[gizlendi]', '4 Files Changed', 'Validated interactively... 880 tests pass'.
- 0:44: 'staticText · On-device AI' kartına 'In' yazılıyor; AAPL ekranı.
- 0:49: Kartta 'Increase the contrast'; Apple Inc. üzerinde kırmızı seçim dikdörtgeni.
- 0:50: '3 elements · Apple Inc., NASDAQ, • Technology' kartı, 'Describe the visual change...'.
- 1:02: 'Copied' düğmesi, 'wmbs cursor/1e38c1e9', 'Inspecting — hover to highlight'.
- 1:04: Değişen dosyalar: WebPreviewHTML.swift, WebPreviewReviewScript.swift, WebPreviewStreamingScript.swift, WebPreviewHTMLTests.swift; 'Commit & Push', 'Open Xcodeproj'.
- 1:07: Yapıştırılan prompt: staticText 'Apple Inc.', 'NASDAQ', '• Technology' koordinatları ve RocketSim agent skill talimatı.
## Belirsizlikler
- Sözlük eşleşmeleri (React, Inter, Three.js, Next.js, Matter.js, design-dna, Make) videoda doğrulanamadı; adaya alınmadı.
- Yorumlarda anılan serve-sim videoda gösterilmediği için aday değil.
- Açıklamadaki RocketSim 17 'henüz yayımlanmadı' ifadesi sabit yorumla çelişiyor (sonradan yayımlandığı belirtiliyor).
- Altyazıdaki 'work tree' ifadesinin Cursor Worktree olduğu varsayıldı.
## Atlanan segment oranı
0/6 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.rocketsim.app | açıklama | açıklama | evet |
| http://127.0.0.1:4995/?token=[gizlendi] | 0:05 | ekran | hayır |
| www.rocketsim.app | açıklama | yorum | evet |
| https://github.com/AvdLee/RocketSimApp | açıklama | açıklama | hayır |
| https://github.com/kean/Pulse | açıklama | açıklama | hayır |
| https://github.com/kean | açıklama | açıklama | hayır |
| https://www.rocketsim.app/docs/features/physical-devices | açıklama | açıklama | hayır |
| https://www.rocketsim.app/docs/features/app-actions/location-simulation | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=ihVwU9usxgQ | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=xK3iI5TzuA4 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=zTbQck3ofcc | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=zukRdke1cP8 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=RQ7tXHyY5Ic | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — RocketSim 17 PoC'yi Cursor tarayıcı paneline açıp stok analiz uygulamasını etkileşimli çalıştırma — araçlar: RocketSim, Cursor, iOS Simulator
- 2. adım — Erişilebilirlik öğeleri listesini ve etkin worktree bilgisini inceleme — araçlar: RocketSim, Accessibility hierarchy, Worktree
- 3. adım — Çarpı imleciyle On-device AI öğesini seçip kontrastı artırma yorumu yazma — araçlar: RocketSim, Visual Feedback paneli
- 4. adım — Sürükleyerek 3 öğeyi gruplayıp hizalama geri bildirimi ekleme — araçlar: RocketSim, Visual Feedback paneli
- 5. adım — Ekran görüntüsü kaydını doğrulayıp Copy prompt ile prompt'u kopyalama — araçlar: RocketSim
- 6. adım — Prompt'u Cursor sohbet alanına yapıştırıp içeriğini (koordinatlar, skill talimatı) gösterme — araçlar: Cursor, RocketSim agent skill, rocketsim CLI
## Promptlar
- Etkileşimli inceleme modunun geliştirilmesi — Çarpı imleci (crosshair) etkinken ekranı dondur, öğe karelerini hover'da göster; sürükleyerek veya Cmd/Shift+tıkla ile birden çok öğe seç.
- Öğelere görsel geri bildirim vermek — Seçilen öğeler için 'Increase the contrast' ve 'Better align these' gibi görsel değişiklik yorumları.
- Kopyalanan ajana hazır geri bildirim promptu — Ajana RocketSim agent skill ile simülatörü başlatmasını, öğeleri rocketsim elements ile doğrulamasını ve ilgili kodu bulup uygulamasını söyler; öğe koordinatları listelenir.
ikinci göz KAPALI: --ikinci-goz yok
