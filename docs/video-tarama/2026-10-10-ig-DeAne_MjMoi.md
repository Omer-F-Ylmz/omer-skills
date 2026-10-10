# This is how to turn Claude into a system that automatically improves itself.
## Künye
This is how to turn Claude into a system that automatically improves itself. · austin.marchese · süre: 0:52 · ? · https://www.instagram.com/reel/DeAne_MjMoi/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-9 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 43584 tk · claude-haiku-5-5: claude-haiku-5-5 · 87886 tk
## Özet
Austin Marchese, Claude'un konuşma geçmişinin bilgisayarda da saklandığını, haftada iki kez çalıştırdığı /improve-system skill'i ile bu geçmişten hataları, oluşturulması gereken skill'leri ve tekrarlayan manuel işleri bulduğunu anlatıyor. Ücretsiz BuildPartner.ai eklentisi Claude'a kurulup /buildpartner:improve-system çalıştırılıyor; ekranda bug-report ve draft-email skill önerileri görülüyor.
## Bölümler
- 0:00 Giriş: kendini geliştiren sistem
- 0:07 Konuşma geçmişinin diskteki konumu
- 0:18 Geçmişi madencilik fikri
- 0:25 /improve-system çalıştırma ve bulgular
- 0:36 Skill'i otomatik bulup yazması
- 0:40 BuildPartner.ai eklentisini kurma
- 0:48 IMPROVE yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | CLI | yok | Sistemin içinde çalıştığı ana yapay zekâ aracı; konuşma geçmişini yerelde saklıyor ve skill çalıştırıyor. | 0:00 | Every conversation you have is saved by Claude |
| Claude Code | yok | CLI | yok | Oturumların çalıştığı ve BuildPartner eklentisinin bağlandığı kodlama aracı. | 0:04 | Sol üstte Chat and Cowork / Code sekmeleri; Code seçili (karede: kanıttan) Sol üstte Chat and Cowork / Code sekmeleri; Code seçili |
| /improve-system | yok | skill | yok | Konuşma geçmişini analiz edip hataları, yeni skill önerilerini ve otomasyonları çıkaran skill. | 0:25 | /buildpartner:improve-system komutu çalıştırılıyor (karede: kanıttan) /buildpartner:improve-system komutu çalıştırılıyor |
| BuildPartner.ai | yok | plugin | yok | Claude'a kurulan ücretsiz eklenti; improve-system ve build komutlarını sağlıyor. | 0:40 | Install BuildPartner.ai başlığı ve açılış sayfası (karede: kanıttan) Install BuildPartner.ai başlığı ve açılış sayfası |
| /buildpartner:build | yok | skill | yok | BuildPartner'ın adım adım rehberli kurulum/tutorial komutu. | 0:40 | Terminalde /buildpartner:build, Step 1-3 çıktısı (karede: kanıttan) Terminalde /buildpartner:build, Step 1-3 çıktısı |
| /bug-report | yok | skill | yok | Önerilen skill: bug report / feature request PDF üretimi. | 0:28 | Bugreport / feature request PDFs — build /bug-report (karede: kanıttan) Bugreport / feature request PDFs — build /bug-report |
| /draft-email | yok | skill | yok | Kişisel klasörde sıkışmış, e-posta taslağı yazan mevcut skill. | 0:28 | /draft-email is stranded (karede: kanıttan) /draft-email is stranded |
| /run-app | yok | skill | yok | Uygulamayı localhost'ta çalıştıran, daha önce doğru yapılmış skill örneği. | 0:30 | /run-app on Aug 6. Same pattern, same fix. (karede: kanıttan) /run-app on Aug 6. Same pattern, same fix. |
| Opus 5 | yok | teknik | yok | Kullanıcının en sık kullandığı model olarak istatistikte görünüyor. | 0:04 | Favorite model: Opus 5 (karede: kanıttan) Favorite model: Opus 5 |
| Notion | yok | MCP | yok | Bulgu metninde hedef olarak anılan Notion sayfası. | 0:30 | Notion page, and does it always write to internal-os/... (karede: kanıttan) Notion page, and does it always write to internal-os/... |
| Routines | yok | ipucu | yok | Claude Code kenar çubuğunda Daily morning brief rutini gösteriliyor. | 0:04 | Routines ve Daily morning brief (karede: kanıttan) Routines ve Daily morning brief |
| Oturum geçmişi (.jsonl) | yok | teknik | yok | Claude konuşmalarının bilgisayarda JSON Lines (.jsonl) dosyası olarak tutulduğu oturum kayıtları. | 0:00 | it's also stored on your computer · kanıt: yok |
| BuildPartner.ai eklentisini kurdurma | yok | prompt | yok | Kullanıcı Claude'dan BuildPartner.ai eklentisini kurmasını ve hesabına bağlamasını istiyor. | 0:43 | kaynak: kare |
| Tekrarlayan işleri otomasyon için bulma | yok | prompt | yok | Claude, son ~60 günlük oturumlardan tekrarlayan manuel işleri bulur; yalnız 3+ kez geçen ve kanıtlanabilir görevleri işaretler. | 0:28 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Gezinme çubuğu (navbar) | Üstte logo ve gezinme menüsü (Features, How it works, Pricing, FAQ, Login) (karede: BuildPartner.ai logosu ve Features/How it works/Pricing/FAQ/Login) | 0:40 | kare |
| Ana kahraman bölümü (hero section) | Büyük başlık, alt metin, e-posta alanı ve Get Started for Free düğmesi (karede: Build 10x faster with Claude Code, e-posta kutusu, turuncu düğme) | 0:40 | kare |
| Terminal mockup kartı (terminal mockup) | Sağda koyu terminal penceresi mockup'ı, /buildpartner:build çıktısı (karede: Koyu pencere, üç renkli nokta, Step 1-3 satırları) | 0:40 | kare |
| Logo şeridi (logo strip) | Altta güvenilen şirket logoları şeridi (karede: TRUSTED BY PROFESSIONALS AT: Anthropic, Granola, HeyGen, Fish Audio, Accio Work, Genspark, Hostinger) | 0:40 | kare |
| Kart ızgarası (card grid) | Özellik kartları ve How it works adım bölümü (karede: Step-by-step guides, Ask our experts, New builds kartları; How it works Step 1) | 0:43 | kare |
| Sayfa kaydırma (scroll) | Sayfa kaydırılarak gösteriliyor (karede: Açılış sayfası ilk karede hero, sonraki karede alt bölümler) | 0:43 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /buildpartner:improve-system | Oturum geçmişini analiz edip hataları, skill önerilerini ve otomasyon fırsatlarını çıkarır. (karede: Terminal girişinde /buildpartner:improve-system, Running a command) | 0:25 | kare |
| /improve-system | Eklenti kurulduktan sonra çalıştırılan sistem iyileştirme skill'i. | 0:45 | altyazı |
| /buildpartner:build | BuildPartner'ın adım adım rehberli kurulum akışını başlatır. (karede: Sitedeki terminal mockup'ında /buildpartner:build) | 0:40 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Konuşmalar yalnız Anthropic'te değil, bilgisayarda da saklanıyor. | 0:00 | özellik |
| Skill haftada iki kez çalıştırılıyor. | 0:18 | öneri |
| Saatler süren günlük işleri dakikalarda çalışan otomasyonlara çevirmeyi öneriyor. | 0:25 | özellik |
| Bug report PDF'i 19 günde 5 kez sıfırdan yeniden kurulmuş. | 0:28 | sayısal |
| BuildPartner.ai eklentisi ücretsiz. | 0:40 | özellik |
| Sitede 3.897 builder'ın katıldığı yazıyor. | 0:40 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude | Claude | Every conversation you have is saved by Claude |
| açıklama | Claude Code | Claude Code | Açıklamada #claudecode etiketi; kare 0:04'te Code sekmesi |
| açıklama | Anthropic | aday değil: konu dışı | Açıklamada #anthropic etiketi; sitede logo şeridinde referans |
| kare 0:04 | Opus 5 | Opus 5 | Favorite model: Opus 5 |
| kare 0:04 | Routines / Daily morning brief | Routines | Kenar çubuğunda Routines ve Daily morning brief |
| kare 0:04 | Artifacts, Dispatch, Dream, Customize menüleri | aday değil: konu dışı | Yalnız kenar çubuğu menüsünde görünüyor |
| kare 0:07 | Dosya gezgini (session-uuid.jsonl konumu) | aday değil: genel kavram | Search Results in projects; session-uuid>jsonl |
| kare 0:07 | Photoshop Project Files klasörü | aday değil: konu dışı | Dosya gezgininde Photoshop Project Files klasörü |
| konuşma 0:18 | /improve-system | /improve-system | I run one skill called Improved System |
| kare 0:25 | /buildpartner:improve-system | /improve-system | Terminal girişinde /buildpartner:improve-system |
| kare 0:28 | /bug-report | /bug-report | build /bug-report |
| kare 0:28 | /draft-email | /draft-email | /draft-email is stranded |
| kare 0:30 | /run-app | /run-app | /run-app on Aug 6. Same pattern, same fix. |
| kare 0:30 | Notion | Notion | Notion page, and does it always write to internal-os/... |
| kare 0:30 | Terry Black's / Blacks | aday değil: konu dışı | Dosya gezgini/proje adlarında Terry Black's |
| konuşma 0:40 | buildpartner.ai | BuildPartner.ai | install the free buildpartner.ai plugin inside Claude |
| kare 0:40 | /buildpartner:build | /buildpartner:build | Sitedeki terminal mockup'ında /buildpartner:build |
| kare 0:40 | Anthropic, Granola, HeyGen, Fish Audio, Accio Work, Genspark, Hostinger logoları | aday değil: konu dışı | TRUSTED BY PROFESSIONALS AT logo şeridi |
| açıklama | IMPROVE yorum çağrısı | aday değil: sponsor/reklam | comment "IMPROVE" and I'll send it through for free |
## Kareden okunanlar
- 0:04: Auto-Improving System başlığı; Claude Code arayüzü: 283 oturum, 16.841 mesaj, 9.4M token, favori model Opus 5, internal-os klasörü.
- 0:40: BuildPartner.ai açılış sayfası: Build 10x faster with Claude Code, 5 free credits, Anthropic/Granola/HeyGen/Fish Audio/Accio Work/Genspark/Hostinger logoları.
- 0:43: Sayfa alt bölümü: guides, experts, new builds kartları ve How it works, Sign up and install adımı.
## Belirsizlikler
- Yorumlar girişsiz alınamadığı için yorumlardaki URL/içerik görülemedi.
- Konuşma geçmişi dosya yolu kareden okunamadı ([yol] ve session-uuid.jsonl kısmen okunabiliyor).
- OCR'daki Three.js, Next.js, Inter, Matter.js sözlük eşleşmeleri videoda kullanıldığına dair kanıt değil; aday yapılmadı.
- Sidebar'daki Artifacts, Dispatch, Dream gibi öğeler yalnız menüde görünüyor, kullanılmıyor.
- Müşteri logoları (Anthropic, HeyGen, Hostinger vb.) yalnız sitede referans olarak görünüyor.
- Notion yalnızca öneri metninde anılıyor; kullanımı gösterilmiyor, aday olarak düşük güvenle eklendi.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| buildpartner.ai | 0:00 | ses | evet |
| https://www.instagram.com/reel/DeAne_MjMoi/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Claude konuşma geçmişinin bilgisayardaki dosya konumunu gösterme — araçlar: Claude
- 2. adım — Geçmişin hata ve çalışma biçimi bilgisi içerdiğini açıklama — araçlar: Claude
- 3. adım — BuildPartner.ai açılış sayfasını gösterme — araçlar: BuildPartner.ai
- 4. adım — Eklentiyi Claude'a kurma — araçlar: BuildPartner.ai, Claude Code
- 5. adım — /buildpartner:improve-system komutunu çalıştırma — araçlar: /improve-system, Claude Code
- 6. adım — Son ~60 günlük oturumları tarama (7 komut çalıştı) — araçlar: Claude Code
- 7. adım — Tekrarlayan manuel işleri listeleme (bug-report, draft-email) — araçlar: /improve-system, /bug-report, /draft-email
- 8. adım — Önerilen skill'i yazdırma ve tamamlanma kriterini sorma — araçlar: Claude Code
## Promptlar
- BuildPartner.ai eklentisini kurdurma — Kullanıcı Claude'dan BuildPartner.ai eklentisini kurmasını ve hesabına bağlamasını istiyor.
- Tekrarlayan işleri otomasyon için bulma — Claude, son ~60 günlük oturumlardan tekrarlayan manuel işleri bulur; yalnız 3+ kez geçen ve kanıtlanabilir görevleri işaretler.
ikinci göz KAPALI: --ikinci-goz yok
