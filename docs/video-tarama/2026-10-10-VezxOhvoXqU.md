# Train Claude on Your Design System (Advanced Workflow)
## Künye
Train Claude on Your Design System (Advanced Workflow) · UI Collective · süre: 26:18 · en-orig · https://youtu.be/VezxOhvoXqU · şema 2
motor: parti 2026-10-10-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (57)
kareler: girdi ≤40000 jeton için 60→57
claude-sonnet-5-5: claude-sonnet-5-5 · 59593 tk · claude-haiku-5-5: claude-haiku-5-5 · 228274 tk
## Özet
UI Collective'den video: Claude'a tasarım sistemini öğretmek için 5 özel skill oluşturuluyor. (1) Tasarım sistemi kuralları ve teknik borç, (2) bileşenler (Form, Navigation, Data Display olarak üç gruba ayrılmış), (3) renk tokenları/Figma değişkenleri, (4) yazı stilleri, (5) boşluk ve şekil (radius, border, layout değişkenleri). Skill'ler Figma MCP ile Figma dosyasından üretiliyor. Sonda tek promptla 'contact us' bölümü üretilip Figma'ya aktarılıyor. Değişkenlerin bağlı, bileşenlerin doğru kullanıldığı gösteriliyor. Kural: sayfa değil kart/bölüm bazında ilerlemek.
## Bölümler
- 0:00 Giriş ve sonuç önizlemesi
- 0:56 Tasarım sistemi kuralları ve teknik borç
- 7:15 Bileşen skill grubu
- 11:23 Tasarım tokenları ve Figma değişkenleri
- 14:45 Yazı stilleri
- 17:18 Boşluk ve şekil
- 23:27 Test: contact us bölümü
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | CLI | yok | Skill'leri üreten ve contact us tasarımını oluşturan ana yapay zekâ aracı. | 5:22 | Claude sohbet arayüzü 'Let's noodle', Opus 5 High seçili. (karede: Claude arayüzünde 'Let's noodle' başlığı ve alt köşede 'Opus 5 High'.) |
| Opus 5 | yok | teknik | yok | Skill üretiminde seçili model; Opus 4.8 ile karşılaştırılıyor. | 10:17 | Prompt kutusunda 'Opus 5 High'; konuşmada Opus 4.8 ile kıyas. (karede: Prompt kutusunun sağ altında 'Opus 5 High'.) |
| Opus 4.8 | yok | teknik | yok | Son testte kullanılan model; konuşmada karşılaştırma modeli. | 23:32 | Alt çubukta 'Opus 4.8 High', Bypass permissions. (karede: Sohbet alt çubuğunda 'Opus 4.8' ve 'High', 'Bypass permissions'.) |
| Figma | yok | iş akışı | yok | Tasarım sistemi kaynağı; bileşenler, değişkenler, stiller ve tasarım çıktısı burada. | 8:44 | Design System Sample dosyası, Form Elements/Navigation sayfaları. (karede: Figma'da 'Design System Sample' dosyası, sayfalar listesinde Form Elements, Field & Input, Dropdown.) |
| Figma MCP | yok | MCP | yok | Claude'un Figma dosyasını okuması için gerekli bağlantı. | 10:17 | Make sure you have Figma MCP connected. |
| Claude skills | yok | skill | yok | Tasarım sistemini öğreten 5 özel skill grubu. | 5:00 | Document this inside of an AI skill. |
| skill-creator | yok | skill | yok | Claude'un skill yazmadan önce konvansiyonlarına baktığı skill. | 10:44 | Claude metni skill-creator conventions kontrolünü anlatıyor. (karede: Sol panelde 'Let me check the skill-creator conventions before writing.') |
| Codex | yok | CLI | yok | Aynı yaklaşımın uygulanabileceği alternatif AI aracı. | 22:26 | You can use codec, you can use grock, you can use cursor. |
| Cursor | yok | CLI | yok | Aynı yaklaşım için alternatif araç olarak anılıyor. | 22:26 | You can use codec, you can use grock, you can use cursor. |
| Grok | yok | CLI | yok | Alternatif AI aracı olarak anılıyor. | 9:16 | Hey Claude, hey Codeex, hey Grock, hey anti-gravity. · kanıt: yok |
| Antigravity | yok | CLI | yok | Alternatif AI aracı olarak anılıyor. | 9:16 | Hey Claude, hey Codeex, hey Grock, hey anti-gravity. |
| Layout variables | yok | teknik | yok | Masaüstü/mobil değerlerini kullanım amacına göre tanımlayan basitleştirilmiş boşluk ölçeği. | 20:23 | We like to introduce something called layout variables. |
| Collective Kit | yok | teknik | yok | UI Collective'in tasarım sistemi kiti ve kursu; açıklamada collectivekit.co. | açıklama | Açıklamada https://collectivekit.co/ bağlantısı var. |
| Design System Labs | yok | iş akışı | yok | Kurumsal AI-hazır tasarım sistemi ajansı (DS Labs); danışmanlık sitesi gösteriliyor. | 0:40 | designsystemlabs.co açıklamada ve ekranda. (karede: Tarayıcıda 'DS Labs', 'We Help Companies Make Their Design Systems AI-Ready.') |
| Mobbin | yok | iş akışı | yok | Açıklamadaki mobbin.com/uicollective bağlantısı; videoda kullanılmıyor. | açıklama | Açıklamada http://mobbin.com/uicollective bağlantısı var. |
| Kurallar ve teknik borç skill'i | yok | prompt | yok | Ürün için tasarım sistemi kuralları ve teknik borcu (yanlış ama değişmesi gereken) yakalayan bir skill oluştur; tasarımlar yönergelerden sapmasın. | 5:22 | kaynak: kare |
| Bileşen grubu skill'i | yok | prompt | yok | 'Form Elements' sayfa grubundaki bileşenleri, varyant, özellik ve kullanım amaçlarıyla öğren; diğer grupları inceleme; hangi bileşenlerin ne zaman kullanılacağını öğreten skill oluştur ve Figma bağlantısı ver. | 10:17 | kaynak: kare |
| Renk tokenı skill'i | yok | prompt | yok | Dosyadaki tüm renk odaklı Figma değişkenlerini ve tasarım tokenlarını öğren (koleksiyon, mod, ad, değer, kullanım amacı); nasıl ve ne zaman uygulanacağını öğreten skill oluştur; çerçeve bağlantısı ver. | 13:58 | kaynak: kare |
| Yazı stili skill'i | yok | prompt | yok | Dosyadaki tüm yazı stillerini (ad, font, ağırlık, boyut, satır yüksekliği, harf aralığı, değişkenler) öğren; kullanım rehberi oluşturma; stilleri ve değişkenlerini belgeleyen skill üret. | 16:48 | kaynak: altyazı |
| Boşluk ve şekil skill'i | yok | prompt | yok | Radius, border width ve layout değişkenlerini öğren; kullanım rehberi oluşturma (kural varsa ekle); hangi değişkenlerin var olduğunu öğreten skill oluştur. | 22:26 | kaynak: altyazı |
| Skill'leri test etme | yok | prompt | yok | Tasarım sistemimizi kullanarak bir 'contact us' bölümü tasarla. | 23:32 | kaynak: kare |
## Açıklama bağlantıları
- https://uicollective.co/ — UI Collective web sitesi (üyelik, kurslar) · aday: hayır · Kendi site/tanıtım; izleyicinin kullanacağı araç değil, referans sayfa. · sınıf: diğer
- https://youtu.be/j_ZPV10bu54 — Tasarım sistemi videosu · aday: hayır · Başka YouTube videosu, araç değil. · sınıf: diğer
- https://designsystemlabs.co/ — Design System Labs ajans sitesi · aday: evet (Design System Labs) · Videoda gösterilen hizmet sitesi (DS Labs); alan adı hizmeti adlandırıyor. · sınıf: diğer
- https://youtu.be/L-tpK7Eeuow — Tasarım sistemi videosu · aday: hayır · Başka YouTube videosu, araç değil. · sınıf: diğer
- https://youtu.be/opTANvl9G1g — Tasarım sistemi videosu · aday: hayır · Başka YouTube videosu, araç değil. · sınıf: diğer
- https://youtube.com/playlist?list=PLkmvmF0zhgT_8FirlLcTQI01ayjYB-46_&si=nXKp-SabMlZvofSR — Tasarım sistemi oynatma listesi · aday: hayır · YouTube oynatma listesi, araç değil. · sınıf: diğer
- http://mobbin.com/uicollective — Mobbin UI Collective sayfası · aday: hayır · Referans/galeri sayfası; videoda kullanılmıyor. · sınıf: diğer
- https://collectivekit.co/ — Collective Kit tasarım sistemi kiti · aday: evet (Collective Kit) · Videoda anılan ürün, izleyicinin kullanabileceği kit. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Değişkene bağlı dolgu (Variable-bound fill) | Bölüm arka planı, surface/page değişkenine bağlı; ham hex değer kullanılmıyor. | 24:28 | altyazı |
| Tip stili uygulaması (Text style application) | Başlık ve gövde metinleri H-etiketli başlık ve body-md tip stillerinden geliyor. | 24:28 | altyazı |
| Bileşen örneği (Component instance) | Gönder düğmesi doğru Button bileşeninden örnek (instance) olarak geliyor. | 24:28 | altyazı |
| İki sütunlu düzen (Two-column layout) | Bölüm iki sütunlu: sol koyu bilgi paneli, sağ form paneli; genişlik 1240 px, sütun arası 48 px. | 24:28 | altyazı |
| Üst etiket ve başlık hiyerarşisi (Eyebrow and heading hierarchy) | Üst kısımda CONTACT etiketi ve büyük başlık 'Get in touch with our team' yer alıyor. | 24:28 | altyazı |
| Koyu bilgi paneli ve ikonlu satırlar (Dark info panel with icon rows) | Koyu bilgi panelinde e-posta, telefon ve adres satırları ikonlarla listeleniyor. | 24:28 | altyazı |
| Form alanları ve açılır liste (Input fields and dropdown) | Form panelinde ad, soyad, e-posta, şirket, konu açılır listesi ve mesaj alanı bulunuyor. | 24:28 | altyazı |
| Onay kutusu (Checkbox) | Gizlilik onayı onay kutusu (checkbox) ile formun alt kısmında yer alıyor. | 24:28 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Tek promptla üretilen modül doğru tipografi stillerini, değişkenleri ve bileşenleri kullanıyor. | 0:00 | özellik |
| Opus 5, bileşenleri yakalamada Opus 4.8 kadar iyi olmayabilir; kontrol edilmeli. | 10:18 | karşılaştırma |
| Tüm bileşenleri tek seferde vermek yerine üç gruba bölmek boşluk bırakmayı önler. | 9:16 | öneri |
| Tüm sayfa yerine kart kart, bölüm bölüm ilerlemek halüsinasyonu azaltır. | 23:27 | öneri |
| Üretilen tasarımda ham hex kodu yok, değişkenler ve bileşenler doğru bağlı. | 24:28 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude AI skills | Claude skills | AI skills öğretiliyor. |
| kare 5:22 | Opus 5 | Opus 5 | Opus 5 High seçili. |
| kare 23:32 | Opus 4.8 | Opus 4.8 | Alt çubukta Opus 4.8 High. |
| konuşma 10:17 | Figma MCP | Figma MCP | Figma MCP bağlı olmalı. |
| kare 10:44 | skill-creator | skill-creator | Skill-creator konvansiyonları kontrol ediliyor. |
| açıklama | collectivekit.co | Collective Kit | Açıklama bağlantısı. |
| kare 0:40 | DS Labs sitesi | Design System Labs | designsystemlabs.co ekranda. |
| açıklama | mobbin.com/uicollective | aday değil: konu dışı | Yalnızca açıklamada referans sayfa. |
| kare 0:26 | uicollective.co | aday değil: konu dışı | Kendi tanıtım sitesi. |
| konuşma 22:26 | Codex, Cursor, Grok | Codex | Alternatif araçlar olarak anılıyor. |
| konuşma 9:16 | Antigravity | Antigravity | Alternatif araç olarak anılıyor. |
| konuşma 20:23 | Layout variables | Layout variables | Boşluk ölçeği tekniği. |
| konuşma 2:57 | Radio button ve checkbox | aday değil: genel kavram | Kural örneği. |
| konuşma 17:18 | Border radius, border width, drop shadow | aday değil: genel kavram | Spacing and shape skill konusu. |
| yorum | figr | aday değil: konu dışı | Yorumcunun kullandığı alternatif; videoda yok. |
| kare 0:26 | Gemini, Lemon Squeezy, Chrome plugin kursları | aday değil: sponsor/reklam | UI Collective kurs tanıtım sayfası. |
## Kareden okunanlar
- 5:22: Let's noodle ekranı, Opus 5 High, kurallar/teknik borç promptu.
- 10:17: Form Elements bileşen promptu ve Figma linki.
- 10:48: navigation-components SKILL.md: dot-prefixed bileşenler kullanılmaz, iki Button seti.
- 13:58: Renk token promptu.
- 23:32: Opus 4.8 High, contact us promptu.
- 24:12: Figma'da H3/medium 48/64, body-md/regular 16/24, surface/page dolgusu.
## Belirsizlikler
- Videoda 'Opus 5' ve 'Opus 4.8' ekranda yazıldığı gibi alındı; son test Opus 4.8 ile görünüyor, konuşma ile uyumsuz olabilir.
- Altyazıdaki Codex/Grok/Cursor/Antigravity yalnızca alternatif olarak anılıyor, gösterilmiyor; yine de aday yazıldı.
- Sözlük eşleşmeleri (Framer, Outfit, Descript vb.) ses bulanık eşleşmeleri; videoda doğrulanamadı.
- OCR'daki UI Collective kurs listeleri (Gemini, Lemon Squeezy vb.) tanıtım sayfasından; kullanılmıyor.
- Kurulum komutu gösterilmedi veya söylenmedi.
## Atlanan segment oranı
0/29 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| uicollective.co | 0:26 | ekran | hayır |
| designsystemlabs.co | 0:40 | ekran | evet |
| https://www.figma.com/design/gYrP129VQnU0UcP3cjCBJv/Design-System- | 10:10 | ekran | evet |
| demo.design | 0:00 | ekran | hayır |
| company.com | 0:00 | ekran | hayır |
| https://uicollective.co/ | açıklama | açıklama | hayır |
| https://youtu.be/j_ZPV10bu54 | açıklama | açıklama | hayır |
| https://designsystemlabs.co/ | açıklama | açıklama | evet |
| https://youtu.be/L-tpK7Eeuow | açıklama | açıklama | hayır |
| https://youtu.be/opTANvl9G1g | açıklama | açıklama | hayır |
| https://youtube.com/playlist?list=PLkmvmF0zhgT_8FirlLcTQI01ayjYB-46_&si=nXKp-SabMlZvofSR | açıklama | açıklama | hayır |
| http://mobbin.com/uicollective | açıklama | açıklama | hayır |
| https://collectivekit.co/ | açıklama | açıklama | evet |
| https://www.figma.com/design/gYrP129VQnU0UcP3cjCBJv/Design-System-Sample?node-id=105-324&t=GYZoAf0N6XtKJH3i-1 | 10:10 | ekran | evet |
| https://www.figma.com/design/gYrP129VQnU0UcP3cjCBJv/Design-System-Sample?node-id=476-9048&t=GYZoAf0N6XtKJH3i-4 | 16:32 | ekran | evet |
| https://www.figma.com/design/gYrP129VQnU0UcP3cjCBJv/Design-System-Sample?node-id=162-28014&t=GYZoAf0N6XtKJH3i-4 | 13:56 | ekran | evet |
## İş akışı
- 1. adım — Kurallar ve teknik borç için skill promptu yazıldı ve çalıştırıldı — araçlar: Claude, Claude skills
- 2. adım — Figma'daki bileşen sayfaları Form, Navigation, Data Display olarak gruplandı — araçlar: Figma
- 3. adım — Her grup için bileşen skill'i promptu Figma bağlantısıyla çalıştırıldı — araçlar: Claude, Figma MCP, Opus 5
- 4. adım — Üretilen skill'ler (örn. navigation-components) okunup kontrol edildi ve kaydedildi — araçlar: Claude, skill-creator
- 5. adım — Token şablonunun bağlantısı Figma'da kopyalandı ve renk skill'i promptu çalıştırıldı — araçlar: Figma, Claude
- 6. adım — Yazı stilleri tablosu ve responsive değişkenler incelendi, yazı stili skill'i çalıştırıldı — araçlar: Figma, Claude
- 7. adım — Radius, border ve layout değişkenleri için boşluk ve şekil skill'i promptu çalıştırıldı — araçlar: Claude, Layout variables
- 8. adım — Skill'lerle 'contact us' bölümü tek promptla üretildi — araçlar: Claude, Opus 4.8
- 9. adım — Önizleme kontrol edildi, Figma'ya aktarıldı ve değişkenler, bileşenler, tipografi doğrulandı — araçlar: Figma, Claude
## Promptlar
- Kurallar ve teknik borç skill'i — Ürün için tasarım sistemi kuralları ve teknik borcu (yanlış ama değişmesi gereken) yakalayan bir skill oluştur; tasarımlar yönergelerden sapmasın.
- Bileşen grubu skill'i — 'Form Elements' sayfa grubundaki bileşenleri, varyant, özellik ve kullanım amaçlarıyla öğren; diğer grupları inceleme; hangi bileşenlerin ne zaman kullanılacağını öğreten skill oluştur ve Figma bağlantısı ver.
- Renk tokenı skill'i — Dosyadaki tüm renk odaklı Figma değişkenlerini ve tasarım tokenlarını öğren (koleksiyon, mod, ad, değer, kullanım amacı); nasıl ve ne zaman uygulanacağını öğreten skill oluştur; çerçeve bağlantısı ver.
- Yazı stili skill'i — Dosyadaki tüm yazı stillerini (ad, font, ağırlık, boyut, satır yüksekliği, harf aralığı, değişkenler) öğren; kullanım rehberi oluşturma; stilleri ve değişkenlerini belgeleyen skill üret.
- Boşluk ve şekil skill'i — Radius, border width ve layout değişkenlerini öğren; kullanım rehberi oluşturma (kural varsa ekle); hangi değişkenlerin var olduğunu öğreten skill oluştur.
- Skill'leri test etme — Tasarım sistemimizi kullanarak bir 'contact us' bölümü tasarla.
ikinci göz KAPALI: --ikinci-goz yok
