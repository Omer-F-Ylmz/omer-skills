# Dev Pazarlama Ekibini tek Yapay Zekâ Ajanı ile Değiştirdim — Kodlama yok, Ücretsiz n8n Template
## Künye
Dev Pazarlama Ekibini tek Yapay Zekâ Ajanı ile Değiştirdim — Kodlama yok, Ücretsiz n8n Template · Burhan KOCABIYIK · süre: 25:25 · tr-orig · https://youtu.be/F0PIbAXhujs · şema 2
motor: parti 2026-10-10-short-15 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (56)
kareler: girdi ≤40000 jeton için 60→56
claude-sonnet-5-5: claude-sonnet-5-5 · 66672 tk · claude-haiku-5-5: claude-haiku-5-5 · 104434 tk
## Özet
Burhan Kocabıyık, n8n üzerinde Telegram'a bağlı tek bir 'Marketing Team Agent' kuruyor. Ajan altı alt otomasyonu araç olarak çağırıyor: UGC video (Arcads), arka planı silinmiş UGC video (fal.ai), blog yazısı (Tavily araştırması ve görsel), görsel oluşturma, görsel düzenleme (nano-banana/edit) ve Drive'da görsel arama. Canlı testlerle her akışın execution'ları gösteriliyor. Şablon Gumroad'dan ücretsiz indirilebiliyor.
## Bölümler
- 0:00 Giriş: tek ajan, altı otomasyon
- 1:01 Telegram'dan canlı test: görsel oluşturma
- 2:04 UGC video isteği ve Arcads
- 5:06 Ana ajanın yapısı: prompt, araçlar, model, hafıza
- 6:42 UGC video akışı: klasör, aktör seçimi, script, üretim
- 9:08 Bekleme döngüsü ve video indirme
- 10:11 Arka planı silinmiş UGC video (fal.ai)
- 14:10 Blog yazısı otomasyonu ve Tavily
- 17:28 Görsel prompt ajanı ve nano-banana
- 19:21 Görsel oluşturma testi (Amsterdam)
- 20:22 Görsel düzenleme: Catbox ve fal.ai
- 23:12 Görsel arama ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n | yok | iş akışı | yok | Tüm otomasyonu çalıştıran iş akışı motoru (n8n cloud). | 0:00 | tek bir agent'a bağladığım N8'in otomasyonu bütün pazarlama ekibinin yapacağı şeyleri |
| Telegram | yok | CLI | yok | Ajanla sohbet arayüzü; istekler ve sonuçlar buradan gidip geliyor. | 0:00 | her şey Telegram üzerinden çalışıyor |
| Arcads | yok | iş akışı | yok | Gerçek aktörlerle UGC reklam videosu üreten platform; API'si n8n'den çağrılıyor. | 3:38 | Arcads dashboard klasörleri ve aktör seçimi ekranı (karede: kanıttan) Arcads dashboard klasörleri ve aktör seçimi ekranı |
| fal.ai | yok | iş akışı | yok | Arka plan silme ve nano-banana görsel üretimi/düzenleme için model platformu. | 11:10 | queue.fal.run URL'leri ve fal.ai header auth (karede: kanıttan) queue.fal.run URL'leri ve fal.ai header auth |
| Nano Banana | yok | iş akışı | yok | fal.ai üzerinden görsel üretimi ve düzenleme modeli. | 18:21 | Falei Nano Banana'yı kullanıyorum. |
| OpenAI Chat Model | yok | iş akışı | yok | Ana ajanın ve alt ajanların dil modeli (GPT-4.1 olduğu söyleniyor). | 6:07 | OpenAI Chat Model düğümü ajana bağlı (karede: kanıttan) OpenAI Chat Model düğümü ajana bağlı |
| Tavily | yok | MCP | yok | Blog ajanının güncel web araştırması için kullandığı arama aracı. | 17:21 | burada ben Tavili'yi kullanıyorum |
| Google Drive | yok | iş akışı | yok | Üretilen videoların ve görsellerin kaydedildiği ve aramanın yapıldığı depo. | 10:11 | indirdikten sonra Drive'a kaydediyor |
| Google Sheets | yok | iş akışı | yok | Üretilen içeriklerin kaydı (Append row in sheet, Image Log). | 12:14 | sonrasında Google Sheet'e yüklemiş oluyorum |
| Catbox | yok | iş akışı | yok | Düzenlenecek görsele geçici URL veren dosya yükleme servisi (Litterbox). | 22:25 | burada da Catbox'u kullanıyorum |
| Structured Output Parser | yok | teknik | yok | Ajan çıktısını başlık ve prompt alanlarına zorlayan çıktı ayrıştırıcı. | 17:21 | kendisi buradan bir structured output çıkartıyor · kanıt: yok |
| Think | yok | iş akışı | yok | Ajana karmaşık kararlarda düşünme imkânı veren n8n aracı. | 6:20 | Think Tool Description: Use the tool to think about something (karede: kanıttan) Think Tool Description: Use the tool to think about something |
| Simple Memory | yok | iş akışı | yok | Ajanın sohbet hafızası. | 6:07 | Sonrasında simple memory var zaten. |
| Transcribe Audio | yok | iş akışı | yok | Sesli mesajı OpenAI ile metne çeviren düğüm. | 5:06 | Download Voice File ve Transcribe Audio düğümleri (karede: kanıttan) Download Voice File ve Transcribe Audio düğümleri |
| GPT-4.1 | yok | iş akışı | yok | Ajanın sohbet modeli olarak söylenen model. | 6:07 | chat modelinin içerisinde zaten 4.1 kullanıyorum · kanıt: yok |
| Gumroad | yok | iş akışı | yok | Şablonun ücretsiz indirildiği platform. | açıklama | benhurhan.gumroad.com/l/ghalj şablon bağlantısı |
| ChatGPT | yok | teknik | yok | Promptları Türkçeden İngilizceye çevirmek için önerilen araç. | 16:20 | chat GPT'ye bunu İngilizceye çeviri de diyebilirsiniz |
| Ana pazarlama ajanının araç seçimi | yok | prompt | yok | Marketing Team Agent sistem promptu: createImage, editImage, görsel veritabanı araması, blogPost, UGC video (arka planlı/arka plansız) ve Think araçlarını ne zaman kullanacağını söyler; UGC için workspace ID, script, cinsiyet ve yaş ister; çıktıda görsel bağlantısı tıklanabilir olmalı. | 5:52 | kaynak: kare |
| Blog yazısı üretimi | yok | prompt | yok | Blog ajanı: Tavily ile gerçek zamanlı araştırma yap, kaynak göstererek profesyonel, başlıklı, sonuç bölümlü blog yaz; çıktı yalnızca makale metni olsun. | 15:54 | kaynak: kare |
| Blog için görsel prompt üretimi | yok | prompt | yok | Görsel prompt ajanı: blog yazısından LinkedIn için uygun, pazarlama tarzı infografik promptu ve 2-4 kelimelik başlık üret; tırnak ve ek açıklama olmasın. | 17:14 | kaynak: kare |
| Görsel oluşturma prompt genişletme | yok | prompt | yok | Uzman görsel prompt mühendisi: basit görsel konusunu ana konu, arka plan, stil, ışık ve detaylarla zengin bir prompta genişlet; konuyu birebir tekrarlama. | 19:48 | kaynak: kare |
| UGC aktör seçimi | yok | prompt | yok | Aktör seçimi: get actors aracıyla uygun cinsiyet/yaştaki aktörü çek, aracın id çıktısını (actor.id değil) ve defaultVoiceId'yi döndür. | 7:32 | kaynak: kare |
## Açıklama bağlantıları
- https://arcads.ai/?via=burhan — Arcads yönlendirme bağlantısı · aday: evet (Arcads) · Videoda kullanılan Arcads aracı; via parametresi var. · sınıf: affiliate
- https://benburhan.gumroad.com/l/ghalj — Ücretsiz n8n şablonu (Gumroad) · aday: evet (Gumroad) · Gumroad üzerinden indirilen şablon, izleyicinin kullanabileceği servis. · sınıf: diğer
- https://www.burhankocabiyik.com/ — Sunucunun kişisel sitesi · aday: hayır · Tanıtım/portfolyo sayfası, araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /start | Telegram botu ile sohbeti başlatır (Marketing Team botu) (karede: Telegram sohbetinde '/start' yazılı mesaj ve bot yanıtı) | 1:38 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Tek ajan altı alt otomasyona bağlanarak bir pazarlama ekibinin işlerini yapıyor. | 0:00 | özellik |
| Videonun üretimi yaklaşık 10 dakika sürebilir; her 5 dakikada bir kontrol ediliyor. | 9:08 | sayısal |
| Promptlar İngilizce yazılınca daha iyi çalışıyor. | 16:20 | öneri |
| Yapay zekâyla üretilen UGC güveni azaltır; bu yüzden gerçek aktörlü Arcads öneriliyor. | 23:27 | karşılaştırma |
| Arka plan silme sonrası 1 dakika bekleniyor. | 11:12 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | n8n | n8n | N8'in otomasyonu |
| konuşma 0:00 | Telegram | Telegram | her şey Telegram üzerinden |
| konuşma 3:05 | Arcads | Arcads | Arcats'ı kullanacak |
| konuşma 11:12 | fal.ai | fal.ai | Fayı platformu |
| konuşma 18:21 | Nano Banana | Nano Banana | Falei Nano Banana'yı kullanıyorum |
| konuşma 6:07 | GPT-4.1 | GPT-4.1 | 4.1 kullanıyorum |
| konuşma 6:07 | Simple Memory | Simple Memory | simple memory var |
| kare 6:20 | Think aracı | Think | Think Tool Description |
| konuşma 17:21 | Tavily | Tavily | Tavili'yi kullanıyorum |
| konuşma 22:25 | Catbox | Catbox | Catbox'u kullanıyorum |
| konuşma 10:11 | Google Drive | Google Drive | Drive'a kaydediyor |
| konuşma 12:14 | Google Sheets | Google Sheets | Google Sheet'e yüklemiş |
| konuşma 17:21 | Structured Output Parser | Structured Output Parser | structured output çıkartıyor |
| konuşma 5:06 | Transcribe Audio | Transcribe Audio | mesaja çeviriyor |
| açıklama | arcads.ai?via=burhan | Arcads | affiliate bağlantı |
| açıklama | Gumroad şablon bağlantısı | Gumroad | ücretsiz şablon |
| açıklama | burhankocabiyik.com | aday değil: konu dışı | kişisel site |
| açıklama | skool.com/doa | aday değil: sponsor/reklam | topluluk tanıtımı |
| konuşma 14:10 | CoreMagnetB2B | aday değil: konu dışı | blog konusu örneği |
| ekran 16:24 | omgiletisim.com | aday değil: konu dışı | Tavily kaynak sonucu |
| konuşma 16:20 | ChatGPT | aday değil: genel kavram | Türkçeyi İngilizceye çevirt |
| yorum | HeyGen, Ollama, PostgreSQL, OpenAI, Llama | aday değil: konu dışı | izleyici yorumları |
| ekran 21:44 | Litterbox | Catbox | litterbox.catbox.moe |
| konuşma 15:18 | Image Prompt Agent | aday değil: başka adayın parçası (n8n) | n8n düğümü |
## Kareden okunanlar
- 0:28: n8n tuvalinde Trigger, Ses veya yazı, Pazarlama beyni, Sonuç, Beyin, Content oluşturma, Görsel oluşturma ve Görsel database bölümleri.
- 3:40: Arcads 'Select actors' penceresi; cinsiyet, yaş ve durum filtreleri, aktör kartları (Helen, Lauren).
- 5:52: Marketing Team Agent sistem mesajı: araç listesi ve talimatlar.
- 7:32: Get Actors düğümü, GET https://external-api.arcads.ai/v1/situations.
- 9:08: Wait düğümü: 5 dakika bekleme.
- 11:38: fal.ai kuyruğunda durum kontrolü, status COMPLETED.
- 16:24: Tavily düğümü: POST https://api.tavily.com/search, Header Auth.
- 17:28: CoreMagnetB2B infografiği: huni, 'Elevate your B2B sales'.
- 21:52: Edit düğümü URL'si queue.fal.run/fal-ai/nano-banana/edit.
## Belirsizlikler
- Sohbet modeli olarak 'GPT 4.1' söyleniyor; 'F modelini ekstra koyuyorum' cümlesi net değil (muhtemelen Think aracı).
- Arka plan silme modelinin tam adı ekranda 'fal-ai/ben/v2/video' görünüyor, OCR bulanık.
- Sözlük eşleşmeleri (Claude, React, Sora vb.) videoda kullanılmıyor, OCR gürültüsü; aday yapılmadı.
- 'Arcats/Arkas' ses tanıma hatası, Arcads olarak yorumlandı.
- Görsel oluşturma akışında gpt görsel API'si (api.openai.com) ile nano-banana arasında akış farkı net değil.
- Drive'daki arama sayfası/Google Sheet adı ekranda net okunamadı (PROTOTIPAL satırı).
## Atlanan segment oranı
0/25 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://arcads.ai/?via=burhan | açıklama | açıklama | evet |
| https://benburhan.gumroad.com/l/ghalj | açıklama | açıklama | evet |
| https://www.burhankocabiyik.com/ | açıklama | açıklama | hayır |
| https://app.arcads.ai/dashboard/product/0c98d250-7dae-4dbb-9531-8351f79b844e | 3:38 | ekran | evet |
| https://external-api.arcads.ai/v1/folders | 6:42 | ekran | evet |
| https://external-api.arcads.ai/v1/situations | 7:32 | ekran | evet |
| https://external-api.arcads.ai/v1/scripts/{{ $json.id }}/generate | 8:48 | ekran | evet |
| https://queue.fal.run/fal-ai/nano-banana/edit | 21:52 | ekran | evet |
| https://api.tavily.com/search | 16:24 | ekran | evet |
| https://litterbox.catbox.moe/resources/internals/api.php | 21:46 | ekran | evet |
| https://omgiletisim.com/2024-yilinin-ilk-yarisini- | 16:24 | ekran | hayır |
| coremagnetb2b.com | 14:10 | ekran | hayır |
| fal.ai | 11:10 | ekran | evet |
| https://drive.google.com/file/d/ | 12:58 | ekran | evet |
| https://api.openai.com | 0:52 | ekran | evet |
| skool.com/doa/about | açıklama | açıklama | hayır |
| skool.com/doa-zero/about | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Telegram'dan metin ya da sesli mesaj alındı; ses ise OpenAI ile metne çevrildi. — araçlar: Telegram, Transcribe Audio, n8n
- 2. adım — Ana pazarlama ajanı isteği anlayıp uygun araca yönlendirdi. — araçlar: Marketing Team Agent, OpenAI Chat Model, Think, Simple Memory
- 3. adım — Görsel oluşturma testi yapıldı: prompt genişletildi, görsel üretildi, Telegram'a gönderildi. — araçlar: n8n, OpenAI Chat Model, Telegram
- 4. adım — UGC video için Arcads'ta klasör oluşturuldu. — araçlar: Arcads, n8n
- 5. adım — Ajan Get Actors ile uygun aktör ve ses ID'sini seçti. — araçlar: Arcads, OpenAI Chat Model, Structured Output Parser
- 6. adım — Script oluşturulup video üretimi başlatıldı. — araçlar: Arcads
- 7. adım — 5 dakikalık bekleme döngüsüyle video durumu kontrol edildi. — araçlar: n8n
- 8. adım — Video indirilip Drive'a ve Sheets'e kaydedildi, Telegram'dan gönderildi. — araçlar: Google Drive, Google Sheets, Telegram
- 9. adım — Arka plansız UGC için video fal.ai'ya gönderilip arka plan silindi. — araçlar: fal.ai, n8n
- 10. adım — Blog istendi: Tavily ile araştırma yapıp blog yazıldı. — araçlar: Tavily, OpenAI Chat Model
- 11. adım — Blog için infografik promptu ve görsel nano-banana ile üretildi. — araçlar: Nano Banana, fal.ai
- 12. adım — Görsel düzenleme: görsel Catbox'a yüklendi, nano-banana/edit ile düzenlendi. — araçlar: Catbox, fal.ai, Nano Banana
- 13. adım — Görsel arama: Drive veritabanında benzer görsel arandı. — araçlar: Google Drive, Google Sheets
## Promptlar
- Ana pazarlama ajanının araç seçimi — Marketing Team Agent sistem promptu: createImage, editImage, görsel veritabanı araması, blogPost, UGC video (arka planlı/arka plansız) ve Think araçlarını ne zaman kullanacağını söyler; UGC için workspace ID, script, cinsiyet ve yaş ister; çıktıda görsel bağlantısı tıklanabilir olmalı.
- Blog yazısı üretimi — Blog ajanı: Tavily ile gerçek zamanlı araştırma yap, kaynak göstererek profesyonel, başlıklı, sonuç bölümlü blog yaz; çıktı yalnızca makale metni olsun.
- Blog için görsel prompt üretimi — Görsel prompt ajanı: blog yazısından LinkedIn için uygun, pazarlama tarzı infografik promptu ve 2-4 kelimelik başlık üret; tırnak ve ek açıklama olmasın.
- Görsel oluşturma prompt genişletme — Uzman görsel prompt mühendisi: basit görsel konusunu ana konu, arka plan, stil, ışık ve detaylarla zengin bir prompta genişlet; konuyu birebir tekrarlama.
- UGC aktör seçimi — Aktör seçimi: get actors aracıyla uygun cinsiyet/yaştaki aktörü çek, aracın id çıktısını (actor.id değil) ve defaultVoiceId'yi döndür.
ikinci göz KAPALI: --ikinci-goz yok
