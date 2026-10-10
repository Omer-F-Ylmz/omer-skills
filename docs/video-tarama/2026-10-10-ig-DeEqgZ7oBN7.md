# Yorumlara “JÜRİ ” yaz, dokümanı paylaşayım!
## Künye
Yorumlara “JÜRİ ” yaz, dokümanı paylaşayım! · esadcom · süre: 0:36 · ? · https://www.instagram.com/reel/DeEqgZ7oBN7/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 12232 tk · claude-haiku-5-5: claude-haiku-5-5 · 25718 tk
## Özet
Girişimci, bir iş fikrine altı ay harcamadan önce Claude içinde 'LLM Council' (jüri) sistemi kurmayı anlatıyor. Dört kişilik jüri: inanan, şüpheci, yatırımcı ve bunların savunmalarını okuyup karar veren hakim. Ekranda Claude Code'da 'llm-council' skill'i yükleniyor, danışman ajanlar paralel başlatılıyor. Hazır dosya, yorumlara 'jüri' yazanlara paylaşılacak.
## Bölümler
- 0:00 Giriş: iş fikrini harcamadan önce jüri sistemi
- 0:06 Jüri personaları: inanan insan
- 0:14 Şüpheci ve yatırımcı
- 0:27 Hakimin kararı
- 0:32 Claude Code'da llm-council skill'inin çalıştırılması ve hazır dosya
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | iş akışı | yok | Jüri sisteminin kurulduğu ana yapay zekâ asistanı; çamaşırhane fikrine olumsuz yanıt veriyor. | 0:00 | Claude arayüzünde 'This will be the worst idea and a huge loss.' yanıtı (karede: Claude sohbet arayüzü, çamaşır toplama-teslim fikrine olumsuz madde işaretli yanıt ve Claude logosu) |
| Claude Code | yok | CLI | yok | Terminalde council komutunun ve ajanların çalıştığı ortam. | 0:32 | Terminalde 'council this:' istemi, Skill(llm-council) ve Agent(...) çıktıları · kanıt: kare (karede: Koyu terminal; council this istemi, Skill(llm-council), Agent(Council Advisor 1 - The Contrarian)) |
| llm-council | yok | skill | yok | Birden çok danışman ajanla soruyu tartıştırıp karar üreten skill. | 0:32 | Skill(llm-council) Successfully loaded skill (karede: 'Skill(llm-council)' ve altında 'Successfully loaded skill' satırları) |
| Claude Opus 4.8 | yok | teknik | yok | Terminalde sunucunun içinde çalıştığı model; bildirimde 'Opus 4.8 is now available' yazıyor. | 0:32 | Opus 4.8 is now available! · /model to switch · kanıt: kare (karede: Üst satırda 'Opus 4.8 is now available! · /model to switch') |
| Council Advisor | yok | teknik | yok | Paralel çalışan 5 danışman ajan; ilki The Contrarian. | 0:33 | Spawning all 5 advisors in parallel now. (karede: Agent(Council Advisor 1 - The Contrarian), Backgrounded agent satırı ve 'Spawning all 5 advisors in parallel now.') |
| /btw | yok | ipucu | yok | Hızlı yan soru sormak için Claude Code komutu; ipucu satırında görünüyor. | 0:33 | Tip: Use /btw to ask a quick side question (karede: 'Tip: Use /btw to ask a quick side questio...' satırı) |
| Jüri sistemini çalıştırma: pazarlama danışmanı için ürün formatı kararı | yok | prompt | yok | Council'a soru: 500 kişilik e-posta listesi olan bir pazarlama danışmanı, dijital ürün ile 97 dolarlık canlı atölye arasında karar veriyor; jüri değerlendirsin. | 0:32 | kaynak: kare |
| Çamaşır toplama-teslim iş fikrini Claude'a değerlendirtme | yok | prompt | yok | Çamaşır toplama ve teslim servisi fikrinin değerlendirilmesi; yanıt olumsuz, düşük marjlı, rekabetli ve lojistik zorlu diyor. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /model | Terminalde Claude modelini değiştirme ekranını açar (ekranda 'to switch' ipucu olarak görünür). (karede: Üstte 'Opus 4.8 is now available! · /model to switch' satırı.) | 0:32 | kare |
| /btw | Çalışan görev sırasında hızlı yan soru sormayı sağlar (ekranda ipucu olarak görünür). (karede: 'Tip: Use /btw to ask a quick side question' satırı.) | 0:33 | kare |
| ctrl+o | Arka plan ajanlarını yönetme ekranını açar ('↓ to manage · ctrl+o' ipucu). (karede: 'Backgrounded agent (↓ to manage · ctrl+o' satırı.) | 0:33 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Jüri dört kişiden oluşur: inanan, şüpheci, yatırımcı, hakim; her birine farklı persona verilir. | 0:06 | öneri |
| Hakim üç savunmayı okuyup fikrin yapmaya değer olup olmadığına karar verir. | 0:27 | özellik |
| Sistem altı ayını işe yaramayacak bir fikre harcamanı önler. | 0:00 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude | Claude | Cloud Double Sistemi kur |
| kare 0:00 | Çamaşır toplama-teslim fikri yanıtı | aday değil: konu dışı | Laundry pickup and delivery service for |
| konuşma 0:06 | Jüri personaları (inanan, şüpheci, yatırımcı, hakim) | llm-council | hepsine farklı personelar koyuyoruz |
| kare 0:32 | Skill(llm-council) | llm-council | Successfully loaded skill |
| kare 0:32 | Opus 4.8 | Claude Opus 4.8 | Opus 4.8 is now available! |
| kare 0:32 | /model | aday değil: genel kavram | /model to switch |
| kare 0:32 | Claude Code terminali | Claude Code | council this: istemi ve Agent çıktıları |
| kare 0:33 | Council Advisor 1 - The Contrarian | Council Advisor | Agent(Council Advisor 1 - The Contrarian) |
| kare 0:33 | /btw | /btw | Tip: Use /btw to ask a quick side question |
| açıklama | Yorumlara 'JÜRİ' yaz çağrısı | aday değil: sponsor/reklam | Yorumlara “JÜRİ ” yaz, dokümanı paylaşayım! |
| sözlük | Make | aday değil: konu dışı | Make · ekran · 0:01 sözlük eşleşmesi, videoda gösterilmiyor |
## Kareden okunanlar
- 0:00: Claude yanıtı: 'This will be the worst idea and a huge loss'; dört madde: düşük marj, çok rakip, lojistik kâbusu, kötü birim ekonomisi. Altyazı 'altı ayını işe yaramayacak'.
- 0:32: Terminal: Opus 4.8 bildirimi, 'council this:' istemi, Skill(llm-council) yüklendi, bağlam taraması, 'Framed question for advisors'.
- 0:33: 'Spawning all 5 advisors in parallel now.', Agent(Council Advisor 1 - The Contrarian) arka planda, Discombobulating 33s, /btw ipucu.
## Belirsizlikler
- Yorumlar girişsiz alınamadı; paylaşılan doküman bağlantısı bilinmiyor.
- Konuşmada 'Cloud Double Sistemi' geçiyor; muhtemelen Claude / LLM Council, kesin değil.
- Konuşmada dört kişilik jüri, ekranda 5 danışman ajan görünüyor; fark açıklanmıyor.
- Sözlükteki 'Make' eşleşmesi videoda gösterilmiyor; aday yapılmadı.
- Dil alanı belirsiz; konuşma Türkçe.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — İş fikrini tanımlayıp Claude'a değerlendirtme (örnek: çamaşırhane servisi; düşük marj, lojistik, rekabet yanıtı) — araçlar: Claude
- 2. adım — Llm-council skill'ini yükleme — araçlar: Claude Code, llm-council
- 3. adım — Model ve ipuçlarını kontrol etme (/model, /btw) — araçlar: Claude Code, Claude Opus 4.8
- 4. adım — Workspace ve hafızada bağlam taraması (2 desen ve hafıza aranır) — araçlar: Claude Code
- 5. adım — Kullanıcı sorusunu danışmanlar için çerçeveleme — araçlar: Claude Code, Claude Opus 4.8
- 6. adım — 5 danışmanı (Council Advisor 1 - The Contrarian dahil) paralel başlatma — araçlar: llm-council, Claude Code
- 7. adım — Arka plan ajanlarını izleme (ctrl+o) — araçlar: Claude Code
- 8. adım — Jüri dosyasını hazırlama ve yorumdan paylaşma (yorum 'jüri' ile link isteme) — araçlar: Instagram
## Promptlar
- Jüri sistemini çalıştırma: pazarlama danışmanı için ürün formatı kararı — Council'a soru: 500 kişilik e-posta listesi olan bir pazarlama danışmanı, dijital ürün ile 97 dolarlık canlı atölye arasında karar veriyor; jüri değerlendirsin.
- Çamaşır toplama-teslim iş fikrini Claude'a değerlendirtme — Çamaşır toplama ve teslim servisi fikrinin değerlendirilmesi; yanıt olumsuz, düşük marjlı, rekabetli ve lojistik zorlu diyor.
