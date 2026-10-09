# Slack içinde Claude'u etiketleyerek tüm verilerinizi ve raporlarınızı otomatik hazırlatın! ⚡
## Künye
Slack içinde Claude'u etiketleyerek tüm verilerinizi ve raporlarınızı otomatik hazırlatın! ⚡ · Esad Kılıç · süre: 0:36 · tr-orig · https://youtu.be/F0NvTpHAoeY · şema 2
motor: parti 2026-10-09-short-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 12475 tk · claude-haiku-5-5: claude-haiku-5-5 · 64434 tk
## Özet
Kısa videoda Esad Kılıç, Claude'un Slack içinde etiketlenerek çalışan gibi görev alabildiğini anlatıyor. Claude kanalı ve bağlamı okuyor, bağlı araçlardan (e-posta, Stripe vb.) veri çekip rapor hazırlıyor ve paylaşıyor. Doğru kurulum için detaylı bir rehber hazırladığını söylüyor; rehber için yoruma kelime yazılması isteniyor.
## Bölümler
- 0:00 Claude'un Slack entegrasyonu tanıtımı
- 0:13 Slack'te Claude ile veri analizi örneği
- 0:24 Bağlamı okuyup görevleri yürütme (blog, davet e-postası)
- 0:27 Doğru kurulum ve rehber çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude in Slack | yok | plugin | yok | Slack'te Claude'u etiketleyerek görev verme; kanalı ve bağlamı okuyup çalışan gibi iş yapıyor. | 0:00 | Slack içinde sadece cloud'u etiketleyip ona da iş verebiliyorsun. · kanıt: yok |
| Slack | yok | iş akışı | yok | Takım iletişim platformu; Claude burada etiketlenerek çalıştırılıyor. | 0:00 | tüm takımının Slack'i nasıl kullandığını değiştirecek |
| Claude Code | yok | CLI | yok | Ekrandaki terminal/kod görüntüsünde claude-code ve claude run komutları geçiyor. | 0:00 | OCR: claude-code, claude run analyze --team all (karede: kanıttan) OCR: claude-code, claude run analyze --team all |
| Claude Opus 4 | yok | teknik | yok | Ekran kodunda model olarak claude-opus-4 yazıyor. | 0:00 | OCR: model: "claude-opus-4" (karede: kanıttan) OCR: model: "claude-opus-4" |
| Stripe | yok | MCP | yok | Claude'a bağlanabilecek araç olarak veri çekilen servis. | 0:00 | email, smail stripe oradan veri çekerek |
| Amplitude | yok | MCP | yok | Aktivasyon oranı grafiğini sağlayan analitik aracı, Slack yanıtında gösteriliyor. | 0:13 | Amplitude başlıklı Activation rate grafiği. (karede: Amplitude kartı, Activation rate çizgi grafiği, 'Found it. A new onboarding flow was deployed on Monday') |
| Google Drive | yok | MCP | yok | Claude son blog yazısını Drive'dan aldı. | 0:24 | Claude yanıtında 'Grabbed latest blog from Drive'. · kanıt: kare (karede: Slack thread'inde Claude AGENT yanıtı: 'Grabbed latest blog from Drive', todo listesi) |
| Dispatch Console | yok | teknik | yok | Takımın tek yerden görev dağıttığı konsol; ekranda kısa görünüyor. | 0:28 | OCR: one place the whole team dispatches from • Dispatch Console (karede: kanıttan) OCR: one place the whole team dispatches from • Dispatch Console |
| Slack içinde metrik raporu hazırlatma | yok | prompt | yok | Claude'a Slack'te etiketle: geçen haftanın sprint metriklerine bak, veriyi çekip rapor hazırla ve ekiple paylaş. | 0:06 | kaynak: altyazı |
| Aktivasyon oranı artışının nedenini bulma | yok | prompt | yok | Platformun aktivasyon oranı son günlerde belirgin arttı; bunun nedeni ne? (Claude analiz edip yeni onboarding akışını buldu.) | 0:12 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| add Claude (Slack'e ekleme ifadesi) | Konuşmada Slack'e Claude eklemek için söylenen ifade; ekranda yazılı komut değil, ses 'add cloud' olarak yazıldı. | 0:00 | altyazı |
| claude run analyze --team all | Ekranda gösterilen Claude Code komutu; tüm takım için analiz çalıştırır. OCR okuması bozuk, tam metin doğrulanamadı. (karede: Ekran OCR metni: '→ claude run analyze --team all' satırı) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Slack'te etiketlenince kapalı ortamda veriyi çekip rapor hazırlıyor ve paylaşıyor. | 0:00 | özellik |
| Claude, bağlı araçlar (e-posta, Stripe) üzerinden veri çekerek gerçek bir çalışan gibi çalışıyor. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Slack | Slack | Slack'i nasıl kullandığını değiştirecek |
| konuşma 0:00 | Claude etiketleme özelliği | Claude in Slack | cloud'u etiketleyip ona da iş verebiliyorsun |
| konuşma 0:00 | Stripe | Stripe | email, smail stripe oradan veri çekerek |
| konuşma 0:00 | E-posta / Gmail bağlantısı | aday değil: genel kavram | email, smail |
| ekran 0:00 | claude-code | Claude Code | OCR: claude-code |
| ekran 0:00 | claude-opus-4 | Claude Opus 4 | OCR: model: claude-opus-4 |
| ekran 0:00 | claude run analyze komutu | Claude Code | OCR: claude run analyze --team all |
| kare 0:13 | Amplitude | Amplitude | Amplitude Activation rate kartı |
| kare 0:24 | Google Drive | Google Drive | Grabbed latest blog from Drive |
| ekran 0:28 | Dispatch Console | Dispatch Console | OCR: Dispatch Console |
| sözlük | Next.js | aday değil: konu dışı | Yalnız sözlük eşleşmesi, videoda gösterilmiyor |
| sözlük | Three.js | aday değil: konu dışı | Yalnız sözlük eşleşmesi, videoda gösterilmiyor |
| konuşma 0:34 | Kurulum rehberi | aday değil: konu dışı | Rehber hazırladığını söylüyor, içerik gösterilmiyor |
## Kareden okunanlar
- 0:13: Amplitude Activation rate grafiği; 'Found it. A new onboarding flow was deployed on Monday'.
- 0:24: Slack thread: Priya 'Oh nice, yes to both!'; Claude AGENT todo: blog satırı ekle, feature table ve beta invite email güncelle.
- 0:26: Thread penceresi: Claude kanal uyarısı, 'Blog + beta invite updated' özeti.
## Belirsizlikler
- Özelliğin resmi adı belirsiz; konuşmada 'cloud' (Claude) geçiyor.
- Altyazıda 'strike metrikleri' ve 'smail' ifadeleri ses tanıma hatası olabilir (sprint metrikleri, Gmail).
- Sözlük eşleşmesindeki Next.js ve Three.js videoda gösterilmiyor; yalnız OCR gürültüsü olabilir.
- Yoruma yazılacak kelime net duyulmuyor ('sik' ses hatası olabilir).
- Kare 0:13/0:24/0:26 dışında kareler görülmedi.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Slack kanalında (#product-eng-launches) proje konuşmasını ve Claude'a verilecek görevi başlatma — araçlar: Slack
- 2. adım — Claude'u @etiketleyerek triage görevi verme — araçlar: Slack, Claude
- 3. adım — Claude'un kanal bağlamını okuyup görevi anlaması — araçlar: Slack, Claude
- 4. adım — Amplitude üzerinden son 10 günün aktivasyon oranı verisini çekme — araçlar: Claude, Amplitude
- 5. adım — Veriyi analiz edip onboarding akışı değişikliğini nedensel olarak bulma — araçlar: Claude
- 6. adım — Google Drive'dan en son blog yazısını çekme — araçlar: Claude, Google Drive
- 7. adım — Blog'a 'What's in the beta' altına satır ekleme — araçlar: Claude
- 8. adım — Özellik tablosunu ve beta davet e-postasını güncelleme — araçlar: Claude
- 9. adım — Sonuçları thread'e yanıt olarak yazma ve #launch kanalına paylaşma — araçlar: Slack
- 10. adım — Stripe gibi bağlı araçlardan veri çekip rapor hazırlatma (anlatım) — araçlar: Claude, Stripe
- 11. adım — Komut satırından analiz çalıştırma (ekranda gösterilen komut) — araçlar: Claude Code
## Promptlar
- Slack içinde metrik raporu hazırlatma — Claude'a Slack'te etiketle: geçen haftanın sprint metriklerine bak, veriyi çekip rapor hazırla ve ekiple paylaş.
- Aktivasyon oranı artışının nedenini bulma — Platformun aktivasyon oranı son günlerde belirgin arttı; bunun nedeni ne? (Claude analiz edip yeni onboarding akışını buldu.)
