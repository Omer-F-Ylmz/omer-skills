# Build an App With Claude Design
## Künye
Build an App With Claude Design · Claude · süre: 1:42 · en · https://youtu.be/COJAZQM1aeQ · şema 2
motor: parti 2026-10-10-short-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 20746 tk · claude-haiku-5-5: claude-haiku-5-5 · 38198 tk
## Özet
Anthropic tasarımcısı Nate, yan projesi için Claude Code içinde Claude Design kullanır: repoyu bağlar, Artifacts sekmesinde yeni tasarım açar, 'saçma bir onboarding' için seçenekler ürettirir, yorum bırakır, ayrıntıları editörde elle düzeltir, tıklanabilir prototip ister ve sonunda Claude'a 'build it' der.
## Bölümler
- 0:00 Giriş: günlük farklı şey fikri ve Nate'in tanıtımı
- 0:41 Claude Code'u açma, repoyu bağlama, Artifacts sekmesi
- 0:48 Yeni Design oluşturma ve prompt yazma
- 0:59 Claude'un beş artboard'lık onboarding seçenekleri
- 1:08 Yorum bırakma ve editörde elle düzeltme
- 1:13 Tıklanabilir prototip isteme
- 1:19 Prototipi yayınlama ve 'build it'
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Design | yok | CLI | yok | Claude Code içindeki Artifacts sekmesinden tasarım, artboard ve prototip üreten tasarım özelliği. | 0:48 | Artifacts sayfasında Design Beta kartı; yeni oturumda Design seçici görünüyor. (karede: Artifacts sayfasında Docs, Slides, Design Beta kartları; giriş kutusunda 'Design' ve 'Design system' seçicileri.) |
| Claude Code | yok | CLI | yok | Repoyu bağlayıp oturum açılan Claude uygulaması/kodlama ortamı. | 0:00 | I open up Claude Code, connect my repo |
| Sonnet 5.5 | yok | teknik | yok | Oturumun çalıştığı model, seçicide 'Sonnet 5.5 Medium'. | 0:41 | Giriş kutusunun altında model seçici yazıyor. (karede: Sağ altta 'Sonnet 5.5 Medium' model seçici.) |
| Artifacts | yok | teknik | yok | Tasarım, belge ve slaytların listelendiği sekme. | 0:46 | Sol menüde Artifacts; Yours/Shared with you listesi. (karede: Artifacts sayfası: All, Yours, Shared with you, Projects sekmeleri ve artifact listesi.) |
| Design system | yok | teknik | yok | Yeni tasarım girişinde seçilen tasarım sistemi seçeneği. | 0:48 | Giriş kutusunda 'Design system' açılır menüsü. (karede: Girişin üstünde 'Design' ve 'Design system' açılır menüleri.) |
| Bricolage | yok | teknik | yok | Claude'un tasarımlarda kullandığını söylediği yazı tipi (Bricolage type). | 0:59 | Sohbet metninde 'Bricolage type' ifadesi geçiyor. (karede: Claude yanıtında 'in the app's own yellow, ink and Bricolage type' (OCR parçalı).) |
| Artifact yorumları | yok | iş akışı | yok | Artboard üzerine @Claude yorumu bırakıp 'Send to Claude' ile gönderme. | 1:08 | @Claude yorum kutusu ve Send to Claude onay kutusu. · kanıt: kare (karede: Artboard üzerinde '@Claude Bi' yazılı yorum kutusu, 'Send to Claude' işaretli.) |
| Tasarım editörü | yok | teknik | yok | Properties/Code/Tweaks panelli, boyut, yerleşim ve dolgu ayarlı elle düzenleme editörü. | 1:11 | Button 'CAW' seçili, Properties paneli açık. · kanıt: kare (karede: Sağ panelde Properties/Code/Tweaks, katman ağacı, Size, Layout, Padding.) |
| Click-through prototype | yok | teknik | yok | B artboard'ının altında oynatılabilir Prototype.dc.html prototipi. | 1:19 | 'Click-through' bölümünde PLAY düğmeli prototip. (karede: Canvas'ta 'Click-through' başlığı altında 'Pro...' ve PLAY düğmeli artboard.) |
| Onboarding tasarım seçenekleri üretmek | yok | prompt | yok | Bu uygulama için saçma bir onboarding tasarla; mevcut ekrandan başla ve yeni fikirlerle bir dizi tasarım üret. | 0:54 | kaynak: kare |
| Kuş modu için tıklanabilir prototip istemek | yok | prompt | yok | Kuş modunu beğendim; tüm akışı hissedebileyim diye tıklanabilir prototipini yap. | 1:14 | kaynak: kare |
## Açıklama bağlantıları
- https://claude.ai/artifacts — Claude Artifacts sayfası · aday: evet (Artifacts) · Videoda kullanılan Artifacts sekmesine giden, izleyicinin kullanabileceği servis. · sınıf: diğer
- https://claude.com/blog/cowork-is-now-claude — Claude blog yazısı · aday: hayır · Blog duyurusu, kullanılabilir araç değil; videoda anlatılmıyor. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Tam ekran hero başlık (hero typography) ve ilerleme göstergesi (progress bar) | Onboarding ekranı A: iri başlıklı sarı kapak, ilerleme çubuğu ve koyu 'I'm in' düğmesi (karede: Sarı artboard 'Every day, one dumb thing.', altta ilerleme çubuğu ve 'I'm in' düğmesi.) | 0:59 | kare |
| Konuşma balonu (speech bubble) ve mascot illüstrasyonu (illustration), büyük CTA düğmesi | Kuş modu: konuşma balonlu başlık, büyük kuş çizimi ve turuncu CAW düğmesi (karede: Mavi artboard'da 'Today you may only make bird noises.' balonu, turuncu kuş, 'CAW' düğmesi.) | 1:08 | kare |
| Kaydırılabilir metin kutusu (scroll box) ve onay kutusu listesi (checkbox list) | Sahte şartlar ekranı: kaydırılabilir yasal metin, onay kutuları ve yeşil düğme (karede: Krem artboard'da 'Terms & Conditions of Doing Today's Thing', kutular ve 'I did not read this'.) | 1:08 | kare |
| Dönen çark (spin wheel) ve koyu mor arka plan | Şans çarkı ekranı: renkli dilimli çark ve sarı 'Spin it' düğmesi (karede: Koyu mor artboard'da renkli çark, 'Spin to meet today's thing.' ve 'Spin it'.) | 0:59 | kare |
| Sonsuz tuval üzerinde artboard yerleşimi (artboard canvas) | Mevcut ekran ile yeni fikirlerin yan yana artboard'larda gösterilmesi (karede: 'What we have' altında Current, 'New ideas' altında A, B, C, D artboard'ları, %28 zoom.) | 0:59 | kare |
| Tıklanabilir prototip (click-through prototype) ve CAW sayacı (counter) | Kuş akışı için oynatılabilir tıklama prototipi: kuş, saat seçimi, bildirim izni, CAW sayacı (karede: B altında 'Click-through' bölümü, PLAY düğmeli prototip artboard'ı; sohbette akış anlatılıyor.) | 1:19 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Nate küçük yan proje onboarding'i için bile hızlı bir tasarım denemesi (design spike) yapabildiğini söylüyor. | 0:30 | özellik |
| Claude beş artboard üretti: Current, A The dare, B Bird mode, C Terms & conditions, D Spin the wheel. | 0:59 | özellik |
| Claude yorumlara göre kuşu büyüttü ve A'nın başlığını 'Bet you won't.' yaptı. | 1:10 | özellik |
| Kodlamadan önce tasarımı Claude ile birlikte düşünmek öneriliyor. | 1:30 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Claude Design | Claude Design | here's how I use Claude design for my own personal projects |
| altyazı 0:00 | Claude Code | Claude Code | I open up Claude Code, connect my repo |
| kare 0:41 | Sonnet 5.5 Medium | Sonnet 5.5 | Model seçici sağ altta |
| kare 0:46 | Artifacts sekmesi | Artifacts | Artifacts sayfası listesi |
| açıklama | https://claude.ai/artifacts | Artifacts | Açıklama bağlantısı |
| açıklama | claude.com blog bağlantısı | aday değil: konu dışı | cowork-is-now-claude blog yazısı |
| kare 0:48 | Design system seçici | Design system | Giriş kutusunda açılır menü |
| kare 0:59 | Bricolage type | Bricolage | Claude yanıtında yazı tipi adı |
| kare 1:08 | @Claude yorumu | Artifact yorumları | Send to Claude yorum kutusu |
| kare 1:11 | Properties/Code/Tweaks editörü | Tasarım editörü | Button 'CAW' seçili özellik paneli |
| kare 1:19 | Prototype.dc.html | Click-through prototype | Created Prototype.dc.html |
| kare 0:59 | Current, A, B, C, D artboard'ları | aday değil: başka adayın parçası (Claude Design) | Tasarım çıktıları |
| kare 0:41 | Yan menü görev listesi (Fix streak counter vb.) | aday değil: konu dışı | Nate'in diğer oturum başlıkları |
| ekran 0:59 | youexample.com / example.com | aday değil: genel kavram | Yer tutucu e-posta alanı |
| yorum | ChatGPT | aday değil: konu dışı | Yorumcu mockup için kullandığını söylüyor |
| açıklama | Nate | aday değil: konu dışı | Anlatıcı/tasarımcı |
| ekran 0:00 | Claude-Design-Demo.mov | aday değil: konu dışı | Dosya adı etiketi |
## Kareden okunanlar
- 0:41: Claude Code ana ekranı: 'What's up next, Nate?', Sonnet 5.5 Medium, Local ve Select folder, görev listesi.
- 0:46: Artifacts sayfası: Docs, Slides, Design (Beta) kartları; Streak rules explainer, Big button haptics explorations gibi öğeler.
- 0:48: Yeni tasarım girişi: todays-thing, main, worktree, Design ve Design system seçicileri; 'What should this design show?'.
- 0:59: Silly onboarding designs oturumu; Claude beş artboard'ı açıklıyor; tuvalde Current ve A–D.
- 1:01: B artboard'ında @Claude yorum kutusu, 'Send to Claude' işaretli; C'de terms metni.
- 1:08: A artboard'ı 'Bet you won't.' başlıklı, Current ekranı 'Welcome to Today's Thing' ve e-posta alanı.
- 1:11: Düzenleyici: Properties/Code/Tweaks, Button 'CAW' seçili; sohbette iki yorum gönderildi ve 2 dosya düzenlendi.
- 1:19: Published artifact Today's Thing onboarding; Prototype.dc.html oluşturuldu; Click-through bölümü ve PLAY.
## Belirsizlikler
- Sözlük eşleşmelerindeki Next.js, Codex, Hermes Agent, design-dna, Canva, Inter vb. videoda gösterilmediği/anlatılmadığı için aday yapılmadı; yorumlardaki ChatGPT da yalnız yorumda geçiyor.
- Sol menüde görünen Projects, Customize, Docs, Slides yalnız menü öğesi; kullanılmadı.
- Bricolage OCR'da parçalı ('Bricolage type'); yazı tipi adı tam doğrulanamadı.
- Coffee molaları arasında geçen süre ve prototipin son 'build it' çıktısı gösterilmiyor; 1:30 'Nates-awesome-app.mov' bölümü sonucu net göstermiyor.
- Altyazıda bulanık eşleşmeler (Codex, design-dna, Hermes Agent) yanlış pozitif görünüyor.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://claude.ai/artifacts | açıklama | açıklama | evet |
| https://claude.com/blog/cowork-is-now-claude | açıklama | açıklama | hayır |
| youexample.com | 0:59 | ekran | hayır |
| example.com | 1:08 | ekran | hayır |
## İş akışı
- 1. adım — Claude Code'u açıp repoyu (todays-thing) bağlama — araçlar: Claude Code
- 2. adım — Artifacts sekmesini açma — araçlar: Artifacts
- 3. adım — Design türünde yeni tasarım oluşturma ve tasarım sistemi seçme — araçlar: Claude Design, Design system
- 4. adım — Mevcut ekrandan başlayıp saçma onboarding seçenekleri isteme — araçlar: Claude Design, Sonnet 5.5
- 5. adım — Claude'un repoyu okuyup beş artboard üretmesini bekleme — araçlar: Claude Design
- 6. adım — Seçenekleri inceleyip artboard'lara @Claude yorumları bırakma — araçlar: Artifact yorumları
- 7. adım — Yorumların Claude tarafından uygulanmasını (kuş büyütme, A başlığı) kontrol etme — araçlar: Claude Design
- 8. adım — Bazı ayrıntıları tasarım editöründe elle düzeltme — araçlar: Tasarım editörü
- 9. adım — Kuş modu için tıklanabilir prototip isteme — araçlar: Claude Design, Click-through prototype
- 10. adım — Prototipi oynatıp deneme — araçlar: Click-through prototype
- 11. adım — Claude'a 'build it' diyerek uygulamayı inşa ettirme — araçlar: Claude Code
## Promptlar
- Onboarding tasarım seçenekleri üretmek — Bu uygulama için saçma bir onboarding tasarla; mevcut ekrandan başla ve yeni fikirlerle bir dizi tasarım üret.
- Kuş modu için tıklanabilir prototip istemek — Kuş modunu beğendim; tüm akışı hissedebileyim diye tıklanabilir prototipini yap.
ikinci göz KAPALI: --ikinci-goz yok
