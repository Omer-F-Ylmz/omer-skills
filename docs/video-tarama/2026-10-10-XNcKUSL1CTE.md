# The Ultimate Beginner’s Guide to Hermes Agent
## Künye
The Ultimate Beginner’s Guide to Hermes Agent · Metics Media · süre: 1:43:37 · en-ehkg1hFWq8A · https://youtu.be/XNcKUSL1CTE · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: yok
kareler: girdi ≤40000 jeton için 60→0
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 233491 tk
## Özet
Metics Media'nın 1 saat 43 dakikalık Hermes Agent rehberi, kod yazmadan kendi AI ajanını kurmayı ve altı seviyede kullanmayı anlatıyor. Seviye 1'de Hostinger VPS'e tek tıkla Hermes kurulur ve Nous Portal üzerinden DeepSeek V4 Flash modeli bağlanır. Seviye 2'de Telegram botu ve Hermes masaüstü uygulaması bağlanır. Seviye 3'te Google Cloud'da OAuth ile Google Workspace skill'i kurulur, Drive, Gmail, Takvim ve Sheets bağlanır, Canva MCP tanıtılır. Seviye 4'te hafıza (MEMORY.md, USER.md), skill üretimi (concise-writer, /learn ile google-seo-starter) ve SOUL.md kişiliği anlatılır. Seviye 5'te fiş dosyalama cron işi, uçuş fiyat izleme işi, model seçimi, fallback zinciri ve Mixture of Agents denenir, maliyet gösterilir. Seviye 6'da alt ajanlar, Hermes profilleri (bots) ve Kanban proje panosu ile rezervasyon takibi işi kurulur; sonda güncelleme ve başarımlar gösterilir.
## Bölümler
- 0:00 Giriş
- 1:59 Seviye 1: Ajanını işe al / Hermes Agent nedir?
- 4:30 Ajanın yaşayacağı yeri seç
- 6:37 Hermes'i tek tıkla kur (Hostinger)
- 10:41 Ajanın kontrol panelini aç
- 12:34 AI modelini seç (Nous Portal)
- 18:26 Seviye 2: Her yerden eriş / Telegram ile sohbet
- 25:56 Hermes masaüstü uygulamasını bağla
- 31:42 Seviye 3: İşe koş / İlk araştırma görevi
- 34:26 Google Drive'ı ajana bağla
- 48:40 MCP ile herhangi bir uygulamayı bağla
- 50:55 Seviye 4: Eğit / Bir tercih öğret
- 52:57 Hermes hafızası nasıl çalışır
- 57:27 İş akışını skill'e çevir
- 1:01:33 Kişilik ver (SOUL.md)
- 1:04:02 Seviye 5: Sen yokken çalışsın
- 1:04:36 Haftalık bir işi otomatikleştir
- 1:09:27 Seni mesajlayan zamanlanmış iş
- 1:11:24 İşe göre doğru modeli seç
- 1:22:06 Hermes Agent ne kadar tutar
- 1:25:03 Seviye 6: Ekip ver / Alt ajanlara böl
- 1:26:30 Takım arkadaşlarını oluştur (profiller)
- 1:30:02 Kanban proje panosunu çalıştır
- 1:40:37 Hermes'i yeniden başlat ve güncelle
- 1:42:04 Ajanının açtığı başarımları gör
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Hermes Agent | yok | teknik | https://github.com/NousResearch/hermes-agent | Nous Research'ün açık kaynaklı AI ajan platformu; sunucuda çalışır, Telegram ve masaüstü uygulamasıyla konuşulur, skill ve hafıza kullanır. | 1:59 | Hermes Agent is a free open source AI agent made by a company |
| Hostinger VPS | yok | teknik | yok | Hermes'in tek tıkla kurulduğu, Docker Manager'lı sanal sunucu hizmeti; video indirimli bağlantıyla alınıyor. | 5:30 | They have a one-click Hermes template that does the setup |
| Docker Manager | yok | teknik | yok | Hostinger panelinde Hermes uygulamasını yöneten, katalogdan kurulum ve güncelleme yapılan Docker arayüzü. | 9:41 | click on the Docker Manager on the left side |
| Traefik | yok | teknik | yok | Hermes ile birlikte kurulan, sunucu bağlantısını güvenli hale getiren ters vekil (reverse proxy). | 9:41 | Traefik, which secures your connection to the server |
| Nous Portal | yok | teknik | yok | Hermes'in model sağlayıcısı; tek hesapla 200'den fazla modele erişim ve ajan araçları (web arama, tarayıcı, görsel) kredisi. | 12:34 | One account gets you access to more than 200 models |
| DeepSeek V4 Flash | yok | teknik | yok | Nous Portal'dan seçilen hızlı ve ucuz model; ana model olarak kullanılıyor, araç kullanımında iyi olduğu söyleniyor. | 15:39 | DeepSeek Flash is perfect for this. |
| DeepSeek V4 Pro | yok | teknik | yok | Fallback zincirinde ana model ve MoA referansı olarak önerilen DeepSeek modeli. | 1:17:33 | let's say we wanted to use DeepSeek V4 Pro for our main one |
| Claude Opus 5 | yok | teknik | yok | Araştırmacı profilinde ve MoA referansında kullanılan üst düzey Anthropic modeli. | 1:19:40 | let's say something like Opus 5 from Anthropic |
| Claude Fable 5.1 | yok | teknik | yok | Pahalı, güçlü model; fiyatı milyon token başına 10 dolar girdi ve 50 dolar çıktı olarak gösterildi. | 1:12:24 | Claude Fable 5.1, for comparison, is $10 per million tokens in |
| Claude Sonnet 5 | yok | teknik | yok | Fallback zinciri denemesinde adı geçen Anthropic modeli; MoA benchmark sonrası çıkarıldı. | 1:17:33 | Maybe we'll use something like Claude Sonnet 5 |
| GPT-5.6 Luna | yok | teknik | yok | MoA referans modellerinden biri olarak seçilen OpenAI modeli (Nous Portal üzerinden). | 1:19:40 | We'll say ChatGPT 5.6 Luna as an example. |
| Solar Pro 4 | yok | teknik | yok | Upstage'in ücretsiz model; fallback zincirinin son çare modeli olarak denendi. | 1:17:33 | Maybe we'll use something here like this Upstage Solar Pro 4 |
| OpenRouter | yok | teknik | yok | Nous Portal dışında kredi satın alınabilen model servisi; alternatif olarak anıldı. | 17:41 | You can buy credit as you go from a service like OpenRouter |
| OpenClaw | yok | teknik | yok | Hermes'e benzer kategoride sürekli çalışan kişisel ajan aracı; yapılandırma içe aktarma için anıldı. | 3:00 | And if you've heard of OpenClaw, this is the same category of tool |
| Telegram | yok | teknik | yok | Ajanla mesajlaşılan kanal; QR ile bot oluşturulup Hermes'e bağlandı, ana kanal olarak ayarlandı. | 18:26 | We're using Telegram because it's the easiest one to set up |
| Hermes Desktop | yok | teknik | yok | Hermes'in masaüstü uygulaması; sunucudaki ajana uzaktan bağlanır, ses ve HUD modu sunar. | 25:56 | For daily use, you want the desktop app. |
| Hermes HUD | yok | teknik | yok | Masaüstü uygulamasında ekranın üstünde yüzen küçük komut çubuğu (heads-up display). | 28:58 | the heads-up display mode or HUD · kanıt: yok |
| Hermes gateway | yok | teknik | yok | Ajanı dış dünyaya (Telegram gibi kanallara) bağlayan Hermes bileşeni; kanallar sayfasından yönetilir. | 11:43 | the gateway on the left side is the part that connects it |
| Google Workspace | yok | skill | yok | Google Drive, Gmail, Takvim, Docs, Sheets ve Kişiler'e OAuth ile bağlanan Hermes skill'i. | 35:26 | Set up the Google Workspace skills so you can use my Google Drive |
| Google Cloud Console | yok | teknik | yok | Google API'lerinin etkinleştirildiği, OAuth istemcisinin ve test kullanıcılarının ayarlandığı proje paneli. | 37:28 | First, we need to create a Google Cloud Platform project |
| OAuth | yok | teknik | yok | Google hesabına izin vermek için kullanılan yetkilendirme protokolü; masaüstü OAuth istemcisi oluşturuldu. | 41:33 | And OAuth client ID. From the application type dropdown, select desktop app. |
| Google Drive | yok | teknik | yok | Ajanın Inbox ve Outbox klasörleriyle dosya alışverişi yaptığı bulut depolama. | 35:26 | I'm using Google Drive because many of you already have it. |
| Gmail | yok | teknik | yok | Ajanın fiş e-postalarını okuyup etiketlediği posta servisi (ajanın ayrı Google hesabı). | 47:43 | If it can reach my email, is it going to start just sending things? |
| Google Calendar | yok | teknik | yok | Ajanın takvime blok ekleyip rezervasyon etkinlikleri oluşturduğu takvim servisi. | 49:42 | Look at my calendar for next week and add a 30-minute block |
| Google Sheets | yok | teknik | yok | Fiş kayıtlarının eklendiği Expenses tablosu ve bütçe tablosu için kullanılan elektronik tablo. | 1:04:36 | Google Sheet called Expenses with a Receipts tab |
| Google Docs | yok | teknik | yok | Ajanın özet raporunu Drive Outbox klasörüne Google Doc olarak kaydettiği belge servisi. | 45:39 | the summary is now a Google Doc inside my Drive's Outbox folder |
| MCP | yok | MCP | yok | Model Context Protocol; ajanın dış uygulamalara bağlanmasını sağlayan standart ve Hermes'in MCP kataloğu. | 48:40 | Many tools now speak a standard called MCP |
| Canva | yok | MCP | yok | Hermes MCP kataloğundan kurulup yetkilendirme adımları gösterilen Canva bağlantısı (bağlanmadı). | 48:40 | if you wanted to connect your Canva, you would simply click instal |
| Clarify | yok | teknik | yok | Hermes'in kullanıcıya soru sormak için çağırdığı araç; videoda form yüklenmedi, düz metin soruya dönüldü. | 35:26 | there's a tool called Clarify that Hermes can call |
| SOUL.md | yok | teknik | yok | Ajanın kalıcı kişiliğini ve davranışını tutan dosya; ajana sorularak güncellendi. | 1:02:34 | The permanent version is a file called SOUL.md |
| Hermes hafızası | yok | teknik | yok | MEMORY.md (ajan notları) ve USER.md (kullanıcı profili) dosyalarından oluşan kalıcı hafıza. | 52:57 | The AI model doesn't remember anything between messages. · kanıt: yok |
| concise-writer | yok | skill | yok | Kısa, net yazım tercihini adım adım kaydeden, ajanın konuşmadan ürettiği skill. | 57:27 | Save that editing workflow as a skill called concise-writer |
| google-seo-starter | yok | skill | yok | SEO başlangıç kılavuzu PDF'inden /learn komutuyla üretilen skill. | 59:29 | Turn this PDF into a reusable skill. |
| Skills Hub | yok | teknik | yok | Başkalarının yazdığı skill'lerin bulunduğu Hermes kütüphanesi; güvenlik taramasıyla gelir. | 1:00:31 | Skills Hub is a whole library of skills that other people have written. |
| Hermes Cron | yok | teknik | yok | Hermes'in zamanlanmış işleri (cron); iş betik veya model olarak çalışır, Telegram'a mesaj gönderebilir. | 1:08:40 | To turn this on, we can simply hit resume |
| Mixture of Agents (MoA) | yok | teknik | yok | /moa komutuyla bir isteği birden çok modele gönderip yanıtları tek yanıtta birleştiren teknik. | 1:18:37 | Hermes will send it to several different models at once · kanıt: yok |
| Fallback zinciri | yok | teknik | yok | Birincil model yanıt vermezse sırayla denenen yedek model listesi. | 1:16:29 | Give your agent a short list of models it drops to · kanıt: yok |
| Alt ajanlar | yok | teknik | yok | Ana ajanın işi bölüp paralel çalışan geçici yardımcı ajanlara dağıtması (subagent). | 1:25:03 | One subagent on things to do. One on best places to eat · kanıt: yok |
| Hermes profilleri (bots) | yok | teknik | yok | Ayrı bellek, skill, kişilik ve modele sahip kalıcı takım arkadaşları; masaüstünde bot olarak oluşturulur. | 1:26:30 | A teammate in Hermes is called a profile. · kanıt: yok |
| Kanban | yok | plugin | yok | Hermes'in Trello benzeri proje panosu eklentisi; kartlar sütunlar arasında ajanlara atanır. | 1:30:02 | Hermes has a project board called Kanban that works like Trello. |
| Playwright | yok | teknik | yok | Uçuş fiyatı izleme betiğinde tarayıcı otomasyonu için kurulan kütüphane (Chromium tabanlı). | 1:10:12 | Playwright installed (the AttributeError is just because playwright (karede: Ajan çıktısında 'Playwright installed' yazısı ve Python tarayıcı betiği (OCR okuması).) |
| Python | yok | teknik | yok | Google API bağımlılıklarını kontrol eden ve uçuş betiklerini çalıştıran programlama dili (venv ile). | 36:52 | python -c import google_auth_oauthlib, googleapiclient, google.oauth2 (karede: Ajan terminal çıktısında python -c komutu ve 'deps: OK' satırı (OCR okuması).) |
| Google Flights | yok | teknik | yok | Barcelona-Londra uçuş fiyatı izleme betiğinin veri aldığı Google uçuş arama sayfası. | 1:10:12 | www.google.com/travel/flights?hl=en&curr=EUR · kanıt: kare (karede: Tarayıcı adres çubuğunda Google Flights arama URL'si (OCR okuması).) |
| Model bağlandıktan sonra ajanın hazır yeteneklerini öğrenmek | yok | prompt | yok | Ajana ilk sorular soruluyor (ör. hangi araçların var?); ajanın yerleşik yetenekleri listelenmesi isteniyor. | 16:40 | kaynak: altyazı |
| Google Workspace bağlantısını başlatmak | yok | prompt | yok | Ajandan Drive, Takvim ve Sheets için Google Workspace skill'ini kurmasını ve gerekli soruları düz metin olarak sormasını ister. | 35:26 | kaynak: altyazı |
| Ajan için paylaşılan dosya düzeni kurmak | yok | prompt | yok | Drive'da Hermes adlı klasör oluşturup içine Inbox ve Outbox klasörleri koymasını ve bağlantıyı vermesini ister. | 44:36 | kaynak: altyazı |
| Google Takvim üzerinde gerçek bir iş yaptırmak | yok | prompt | yok | Takvimde gelecek hafta en boş öğleden sonraya 30 dakikalık bir blok eklemesini ister. | 49:42 | kaynak: altyazı |
| Tercihi düzeltme yoluyla öğretmek | yok | prompt | yok | Çok kelimeli yanıtı eleştirir; kısa, net, üç paragraf ve başlıksız/madde işaretsiz yazı tercihini kaydetmesini ister. | 50:55 | kaynak: altyazı |
| Hafızayı düzenli tutmak için indeks oluşturmak | yok | prompt | yok | Notlarını bir dizin dosyasında tutmasını, hafızasında bu dosyaya tek satırlık işaret bırakmasını ister. | 56:00 | kaynak: altyazı |
| Tekrarlanan yazım iş akışını skill'e dönüştürmek | yok | prompt | yok | Bu düzenleme akışını concise-writer adlı bir skill olarak kaydetmesini ister. | 57:27 | kaynak: altyazı |
| Kalıcı kişilik ayarlamak | yok | prompt | yok | Ajanın kalıcı SOUL.md kişiliğini güncelleyip sakin, doğrudan ton kullanmasını ve gereksiz soru sormamasını ister. | 1:02:34 | kaynak: altyazı |
| Haftalık admin işini otomatikleştirmek | yok | prompt | yok | Gmail'deki fiş ve faturaları günlük tarayıp Sheets tablosuna satır ekleyen, etiketleyen ve sadece okuma/etiketleme yetkisi olan bir cron işi ister; işi duraklatılmış oluşturmasını ister. | 1:04:36 | kaynak: altyazı |
| Uçuş fiyatı takibi için zamanlanmış iş kurmak | yok | prompt | yok | Barselona-Londra uçuş fiyatlarını izleyen, kendi skill'ini yazan ve her birkaç saatte bir yalnız yeni durumda Telegram'dan mesaj gönderen bir iş ister. | 1:09:27 | kaynak: altyazı |
| Model kesintilerine karşı yedek zincir kurmak | yok | prompt | yok | Birincil model, başka sağlayıcıdan model ve ucuz bir model olmak üzere üç yedekli model zinciri kurmasını ister. | 1:16:29 | kaynak: altyazı |
| Model seçimini karşılaştırmalı test etmek | yok | prompt | yok | Yedek zincir için MoA referans modellerini kıyaslayıp en uygun zinciri önermesini ister. | 1:18:37 | kaynak: altyazı |
| İşi alt ajanlara bölüp paralel çalıştırmak | yok | prompt | yok | Londra'dan Lizbon'a üç günlük gezi için üç alt ajanın paralel çalışıp tek plan döndürmesini ister. | 1:25:03 | kaynak: altyazı |
| Kanban panosunda doğru kart ataması için profil tanımları | yok | prompt | yok | Araştırmacı, yazar ve gözden geçiren profilleri için birer cümlelik iş tanımı yazmasını ister. | 1:26:30 | kaynak: altyazı |
| Çok adımlı bir işi panoya atamak | yok | prompt | yok | Lizbon gezisi için bütçe tablosu, gün gün plan, takvim etkinlikleri ve kontrol adımlarını içeren bir Kanban kartı açar; takılırsa Telegram'dan sorar. | 1:35:04 | kaynak: altyazı |
| Panodaki işi güncel tutan zamanlanmış iş | yok | prompt | yok | Her sabah rezervasyon onaylarını arayıp tablo, takvim ve etiket güncellemesi yapan, duraklatılmış bir iş ister. | 1:39:08 | kaynak: altyazı |
## Açıklama bağlantıları
- https://meticsmedia.com/hermes-EPQ — Hostinger VPS için indirim içeren kanal yönlendirme bağlantısı. · aday: hayır · Affiliate yönlendirme linki; aracın kendisi Hostinger VPS adayında. · sınıf: affiliate
- https://meticsmedia.com/nous-EPQ — Nous Portal için ilk ay indirimli kanal yönlendirme bağlantısı. · aday: hayır · Affiliate yönlendirme linki; aracın kendisi Nous Portal adayında. · sınıf: affiliate
- https://telegram.org/apps — Telegram uygulamasının indirme sayfası (telefon ve masaüstü). · aday: evet (Telegram) · Videoda kullanılan Telegram aracının resmi indirme sayfası. · sınıf: diğer
- https://hermes-agent.nousresearch.com — Hermes masaüstü uygulamasının resmi indirme sayfası. · aday: evet (Hermes Desktop) · Videoda kurulan Hermes masaüstü uygulamasının resmi kaynağı. · sınıf: diğer
- https://meticsmedia.com/deals — Kanalın önerilen ürün ve video bağlantıları listesi. · aday: hayır · Referans/ilham sayfası; kullanılan bir araç değil. · sınıf: diğer
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Hermes Agent ücretsiz ve açık kaynaklıdır; ödenen tek şey model ve sunucudur. | 1:59 | özellik |
| Hostinger Hermes şablonu kurulumu terminal yazmadan yapar. | 5:30 | özellik |
| Nous Portal 200'den fazla modele erişim verir; 20 dolarlık abonelik 22 dolar kredi sağlar. | 12:34 | sayısal |
| Ücretsiz Nous Portal katmanı yoğun ajan kullanımı için standart limitlerde yetersiz kalır. | 14:36 | öneri |
| DeepSeek V4 Flash araç kullanımında iyidir ve mesajı kuruşun kesri kadar maliyetlidir. | 16:40 | öneri |
| DeepSeek V4 Flash girdi milyonda 7 sent, çıktı milyonda 14 sent. | 1:11:24 | sayısal |
| Claude Fable 5.1 milyon token başına 10 dolar girdi, 50 dolar çıktı. | 1:12:24 | sayısal |
| MoA ile yapılan tek bir test Opus 5 çağrılarıyla 1,30 dolar tuttu. | 1:24:08 | sayısal |
| Hermes'te hafıza dosyaları her mesajla gönderildiği için birkaç yüz kelimede tutulur. | 54:58 | özellik |
| Telegram bot sohbetleri uçtan uca şifreli değildir; parola veya banka bilgisi gönderilmemelidir. | 21:31 | özellik |
| Masaüstü, Telegram ve web paneli aynı hafızayı paylaşır. | 28:58 | özellik |
| Zamanlanmış iş kural tabanlı betik olarak çalışırsa modeli her çalıştırmada çağırmaz, token tasarrufu sağlar. | 1:07:40 | özellik |
| Modeli sabitlenmemiş zamanlanmış işler, varsayılan model değişince çalışmayı reddeder. | 1:15:27 | özellik |
| MoA birden çok model yanıtını birleştirir; maliyet birkaç yanıt kadardır. | 1:18:37 | özellik |
| Alt ajanlar paralel çalışır ve iş bitince geçici olarak kaybolur. | 1:25:03 | özellik |
| Kanban kartı takılırsa sessiz kalır; Telegram ile oluşturulan kartlar bildirim gönderir. | 1:32:02 | özellik |
| Hermes 16 hazır otomasyonla gelir ve hepsi okunacak bir şey gönderir. | 1:04:02 | sayısal |
| Hermes başarım sistemi 60 rozet içerir; yazar 53'ünü henüz keşfetmemiştir. | 1:42:04 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 1:59 | Açık kaynaklı AI ajanı | Hermes Agent | Hermes Agent is a free open source AI agent |
| konuşma 2:30 | ChatGPT ve Claude karşılaştırması | aday değil: genel kavram | If you already pay for ChatGPT or Claude |
| konuşma 3:00 | OpenClaw'a benzerlik ve içe aktarma | OpenClaw | if you've heard of OpenClaw |
| konuşma 5:30 | Tek tık Hermes şablonlu VPS | Hostinger VPS | one-click Hermes template |
| kare 9:50 | Katalogdaki n8n ve Paperclip | aday değil: konu dışı | n8n, Paperclip (katalog) |
| kare 9:16 | Hostinger panelindeki Docker Manager | Docker Manager | Docker Mana |
| konuşma 9:41 | Güvenli bağlantı katmanı | Traefik | Traefik, which secures your connection |
| kare 7:32 | Ödeme sayfasındaki nexos.ai | aday değil: sponsor/reklam | nexos.ai (checkout ekranı) |
| konuşma 12:34 | 200+ model erişimi | Nous Portal | One account gets you access to more than 200 models |
| konuşma 15:39 | Ana model DeepSeek Flash | DeepSeek V4 Flash | DeepSeek Flash is perfect for this. |
| kare 15:10 | Qwen, MiniMax, Grok sağlayıcı listesi | aday değil: konu dışı | Qwen (via Qwen CLI) (sağlayıcı listesi) |
| konuşma 15:39 | Ücretli modeller ve Anthropic şirketi | aday değil: genel kavram | Anthropic's terms keep those plans to its own apps |
| konuşma 17:41 | Alternatif model servisi | OpenRouter | a service like OpenRouter |
| konuşma 18:26 | Mesajlaşma kanalı | Telegram | We're using Telegram because it's the easiest one |
| konuşma 18:26 | Discord, Slack, WhatsApp desteği | aday değil: genel kavram | including Discord, Slack, and WhatsApp |
| konuşma 25:56 | Masaüstü uygulaması | Hermes Desktop | For daily use, you want the desktop app. |
| konuşma 26:44 | Mac işletim sistemi | aday değil: genel kavram | I'm on a Mac |
| konuşma 28:58 | Ekranın üstünde yüzen mod | Hermes HUD | heads-up display mode or HUD |
| konuşma 31:42 | Ajanın okuduğu haber sitesi | aday değil: konu dışı | Saying it's reading New York Times |
| konuşma 34:26 | Google Drive bağlantısı | Google Drive | I'm using Google Drive because many of you |
| konuşma 35:26 | Google Workspace skill'i | Google Workspace | Set up the Google Workspace skills |
| konuşma 35:26 | Soru sorma aracı | Clarify | there's a tool called Clarify |
| konuşma 37:28 | Tarayıcı (Brave) | aday değil: genel kavram | go back to my Brave browser here |
| konuşma 37:28 | Google Cloud projesi | Google Cloud Console | First, we need to create a Google Cloud Platform project |
| konuşma 41:33 | OAuth istemcisi | OAuth | And OAuth client ID. |
| konuşma 44:36 | Drive Inbox/Outbox klasörleri | Google Drive | Create a drive folder called Hermes |
| konuşma 45:39 | Özet için Google Doc | Google Docs | a Google Doc inside my Drive's Outbox folder |
| konuşma 46:41 | Gmail erişimi | Gmail | that setup also gave your agent access to Gmail |
| konuşma 49:42 | Takvim etkinliği ekleme | Google Calendar | add a 30-minute block called change studio light bulbs |
| konuşma 48:40 | Dış uygulamaları bağlayan standart | MCP | Many tools now speak a standard called MCP |
| konuşma 48:40 | Canva MCP kurulumu | Canva | if you wanted to connect your Canva, you would simply click instal |
| kare 49:16 | MCP kataloğundaki Figma, ComfyUI, Cloudinary | aday değil: konu dışı | https://mcp.figma.com/mcp (katalog) |
| konuşma 50:55 | Notion ve GitHub örneği | aday değil: genel kavram | Notion, GitHub, your customer database |
| konuşma 52:57 | Ajanın hafızası | Hermes hafızası | The AI model doesn't remember anything between messages |
| konuşma 56:00 | Not indeksi dosyası | Hermes hafızası | keep an index file of your notes |
| konuşma 57:27 | Tekrarlanan iş akışı skill'i | concise-writer | Save that editing workflow as a skill called concise-writer |
| konuşma 59:29 | SEO kılavuzu PDF'i | google-seo-starter | Here, I found this SEO starter guide. |
| kare 1:01:04 | Skills Hub listesindeki siteler | aday değil: konu dışı | skills.sh, browse.sh, FindMy.app (listede) |
| konuşma 1:02:34 | Kalıcı kişilik dosyası | SOUL.md | The permanent version is a file called SOUL.md |
| konuşma 1:04:36 | Fiş dosyalama betiği | aday değil: başka adayın parçası (Hermes Cron) | run_receipt_filer.sh |
| konuşma 1:04:36 | Gmail fiş e-postaları | Gmail | search my Gmail for purchase receipts |
| konuşma 1:04:36 | Sheets fiş tablosu | Google Sheets | append a row to my Google Sheet Expenses |
| konuşma 1:09:27 | Uçuş fiyatı izleme işi | Hermes Cron | Watch Barcelona to London flight price trends |
| kare 1:10:02 | Denenen uçuş uç noktaları | aday değil: konu dışı | api.skypicker.com, api.tequila.kiwi.com |
| kare 1:10:04 | Denenen Skyscanner uç noktası | aday değil: konu dışı | https://www.skyscanner.net/api/revenue/v1/flights/ |
| kare 1:10:12 | Uçuş fiyat verisi kaynağı | Google Flights | www.google.com/travel/flights?hl=en&curr=EUR |
| kare 1:10:12 | Tarayıcı otomasyonu | Playwright | Playwright installed |
| kare 1:11:52 | Model listesindeki Kimi ve Qwen | aday değil: konu dışı | MOONSHOTAI/KIMI-K3 |
| konuşma 1:16:29 | Yedek model zinciri | Fallback zinciri | Give your agent a short list of models it drops to |
| konuşma 1:17:33 | Ana model olarak DeepSeek V4 Pro | DeepSeek V4 Pro | use DeepSeek V4 Pro for our main one |
| konuşma 1:17:33 | Üçüncü yedek olarak Claude Sonnet 5 | Claude Sonnet 5 | Maybe we'll use something like Claude Sonnet 5 |
| konuşma 1:17:33 | Son çare ücretsiz model | Solar Pro 4 | this Upstage Solar Pro 4 |
| konuşma 1:18:37 | Birden çok model yanıtı | Mixture of Agents (MoA) | Hermes will send it to several different models |
| konuşma 1:19:40 | MoA referansı Opus 5 | Claude Opus 5 | something like Opus 5 from Anthropic |
| konuşma 1:19:40 | MoA referansı GPT-5.6 Luna | GPT-5.6 Luna | ChatGPT 5.6 Luna as an example |
| konuşma 1:12:24 | Claude Fable fiyatı | Claude Fable 5.1 | Claude Fable 5.1, for comparison, is $10 |
| konuşma 1:25:03 | Üç alt ajan | Alt ajanlar | One subagent on things to do |
| konuşma 1:26:30 | Hermes profilleri | Hermes profilleri (bots) | A teammate in Hermes is called a profile |
| konuşma 1:30:02 | Proje panosu | Kanban | project board called Kanban that works like Trello |
| konuşma 1:30:36 | Git ile kurulum seçeneği | aday değil: genel kavram | Install from Git |
| konuşma 1:36:52 | Ekrandaki Linear adı | aday değil: konu dışı | Linear (ekran sözlüğü) |
| konuşma 1:42:04 | Başarım sayfası | aday değil: başka adayın parçası (Hermes Agent) | achievements... 60 of them |
| yorum | Yerel model çalıştırma (Ollama/Llama) | aday değil: konu dışı | I've run Hermes on local inference |
| yorum | Ayrı Google hesabı ve yönlendirme | aday değil: başka adayın parçası (Google Workspace) | The Google Workspace skill isn't tied to a special |
| yorum | Kripto ticareti isteği | aday değil: konu dışı | Crypto trading ek aisa topic |
| açıklama | Hostinger kayıt sayfası | aday değil: başka adayın parçası (Hostinger VPS) | auth.hostinger.com/register |
| açıklama | Kanalın YouTube videoları | aday değil: konu dışı | youtu.be video bağlantıları (deals sayfası) |
| açıklama | Google geliştirici sayfaları | aday değil: konu dışı | developers.google.com (linkli sayfa) |
| açıklama | Firefox bağlantısı | aday değil: konu dışı | firefox.com (linkli sayfa) |
| açıklama | Stripe ödeme ekranı | aday değil: konu dışı | checkout.stripe.com (ekran) |
## Kareden okunanlar
- 0:42: Hermes Agent v0.8.0 (2026.4.8) (OCR okuması; harfler bozuk olabilir)
- 6:00: curl -fsSL get.hermes.sh / bash
- 6:00: nano /opt/hermes/.env
- 9:16: Docker Manager
- 10:14: hpanel.hostinger.com/vps/.../docker-manager/catalog
- 9:50: n8n, Paperclip, Self hosting n8n (katalog listesi)
- 11:36: Box, OpenAI Codex CLI, Claude Design (katalog listesi)
- 15:10: hermes auth add xai-oauth; GitHub Copilot (ACP); Qwen; xAI Grok OAuth
- 15:42: anthropic/claude-haiku-4.5; openai/gpt-6-astra-flex
- 25:30: Cloudflare hata metni; inference-api.nousresearch.com
- 33:26: Deleted all three (test1.txt, test2.md, test3.json) — ajan çıktısı
- 49:06: github.com/NousResearch/hermes-agent
- 49:16: Atlassian Jira/Confluence, Comfy Cloud, Cloudinary, mcp.figma.com/mcp (katalog listesi)
- 49:34: canva.com/login ... (Canva yetkilendirme)
- 1:01:04: skills.sh, browse.sh, FindMy.app, gstack, Rive, Hugging Face (katalog listesi)
- 1:07:02: run_receipt_filer.sh (cron betiği)
- 1:07:30: Google Sheets: Expenses tablosu bağlantısı
- 1:07:48: Gmail etiketi: Files
- 1:10:02: api.skypicker.com, api.tequila.kiwi.com (denenen uçuş uç noktaları)
- 1:10:12: www.google.com/travel/flights?hl=en&curr=EUR
- 1:10:30: Mevcut en düşük gidiş-dönüş fiyatı 30 EUR (BCN-LON)
- 1:11:52: MOONSHOTAI/KIMI-K3; QWEN/QWEN3-235B-A22B-2507 (model listesi)
- 1:21:28: deepseek/deepseek-v4-pro reliable (6/6, $0.0013/task)
- 1:42:16: Başarım adları: Claude Confidant, Hermes tool calls (OCR)
## Belirsizlikler
- Kare görselleri eklenmedi; kare bilgileri yalnız OCR metninden okundu, görsel doğrulama yapılamadı.
- OCR bazı yerlerde bozuk okumalar üretti (ör. 'Hernes', 'Tor' vb.); tam komut ve URL'ler doğrulanamadı.
- Ekranda 'hermes run nightly-report' komutu (5:00) görülüyor ama videoda bağlamı anlatılmıyor.
- Clarify aracının video sırasında neden form yüklemediği belirsiz; video bunu bir hata olarak tanımlıyor.
- Gmail'in ana hesap mı ayrı hesap mı olacağı konusunda yorumcu soru sormuş; yanıtta iki yol önerilmiş (sahip yorumu).
- 'That and Astra' ifadesi ses kaydında geçiyor; Astra'nın hangi model olduğu netleşmedi.
- Ekranda görünen ama kullanılmayan MCP öğeleri (Figma, ComfyUI, Cloudinary, Atlassian Jira/Confluence) adaylara alınmadı.
- Skills Hub listesindeki skills.sh, browse.sh, FindMy.app, gstack, Rive, Hugging Face yalnızca listede görüldü, kullanılmadı.
- humanizer, headroom ve taste-skill ajanın düşünce metninde geçiyor; kullanılmadığı için adaylara alınmadı.
- Obsidian yalnızca ajanın 'vault yok' notunda geçiyor; kullanılmadı.
- n8n, Paperclip, Ackee ve OpenAI Codex CLI yalnızca katalog ekranında görüldü.
- Kimi, Qwen, Grok, MiniMax, Z.ai, Gemini ve GPT-5.6 sürümleri yalnızca model listesinde görüldü, kullanılmadı.
- Skyscanner ve Kiwi (Tequila) uç noktaları denendi fakat sonuç alınamadı; kullanılan araç olarak adaylara alınmadı.
- Sözlük eşleşmelerinin çoğu (Inter, Codex, Tripo, Stitch, Three.js, Make, Descript, Astro, Linear vb.) bu videoda anlatılmıyor; OCR/ses gürültüsü olarak yok sayıldı.
- Hostinger, Nous Portal ve model fiyatları video tarihindeki değerlerdir; değişebilir.
- Zaman damgaları bölüm başlangıçlarına göre yaklaşık verilmiştir.
- Bazı kurulum komutları ajanın kendi çıktısında görüldü; kullanıcının bunları çalıştırması gerekmiyor.
## Atlanan segment oranı
0/112 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- yok
## Promptlar
- Model bağlandıktan sonra ajanın hazır yeteneklerini öğrenmek — Ajana ilk sorular soruluyor (ör. hangi araçların var?); ajanın yerleşik yetenekleri listelenmesi isteniyor.
- Google Workspace bağlantısını başlatmak — Ajandan Drive, Takvim ve Sheets için Google Workspace skill'ini kurmasını ve gerekli soruları düz metin olarak sormasını ister.
- Ajan için paylaşılan dosya düzeni kurmak — Drive'da Hermes adlı klasör oluşturup içine Inbox ve Outbox klasörleri koymasını ve bağlantıyı vermesini ister.
- Google Takvim üzerinde gerçek bir iş yaptırmak — Takvimde gelecek hafta en boş öğleden sonraya 30 dakikalık bir blok eklemesini ister.
- Tercihi düzeltme yoluyla öğretmek — Çok kelimeli yanıtı eleştirir; kısa, net, üç paragraf ve başlıksız/madde işaretsiz yazı tercihini kaydetmesini ister.
- Hafızayı düzenli tutmak için indeks oluşturmak — Notlarını bir dizin dosyasında tutmasını, hafızasında bu dosyaya tek satırlık işaret bırakmasını ister.
- Tekrarlanan yazım iş akışını skill'e dönüştürmek — Bu düzenleme akışını concise-writer adlı bir skill olarak kaydetmesini ister.
- Kalıcı kişilik ayarlamak — Ajanın kalıcı SOUL.md kişiliğini güncelleyip sakin, doğrudan ton kullanmasını ve gereksiz soru sormamasını ister.
- Haftalık admin işini otomatikleştirmek — Gmail'deki fiş ve faturaları günlük tarayıp Sheets tablosuna satır ekleyen, etiketleyen ve sadece okuma/etiketleme yetkisi olan bir cron işi ister; işi duraklatılmış oluşturmasını ister.
- Uçuş fiyatı takibi için zamanlanmış iş kurmak — Barselona-Londra uçuş fiyatlarını izleyen, kendi skill'ini yazan ve her birkaç saatte bir yalnız yeni durumda Telegram'dan mesaj gönderen bir iş ister.
- Model kesintilerine karşı yedek zincir kurmak — Birincil model, başka sağlayıcıdan model ve ucuz bir model olmak üzere üç yedekli model zinciri kurmasını ister.
- Model seçimini karşılaştırmalı test etmek — Yedek zincir için MoA referans modellerini kıyaslayıp en uygun zinciri önermesini ister.
- İşi alt ajanlara bölüp paralel çalıştırmak — Londra'dan Lizbon'a üç günlük gezi için üç alt ajanın paralel çalışıp tek plan döndürmesini ister.
- Kanban panosunda doğru kart ataması için profil tanımları — Araştırmacı, yazar ve gözden geçiren profilleri için birer cümlelik iş tanımı yazmasını ister.
- Çok adımlı bir işi panoya atamak — Lizbon gezisi için bütçe tablosu, gün gün plan, takvim etkinlikleri ve kontrol adımlarını içeren bir Kanban kartı açar; takılırsa Telegram'dan sorar.
- Panodaki işi güncel tutan zamanlanmış iş — Her sabah rezervasyon onaylarını arayıp tablo, takvim ve etiket güncellemesi yapan, duraklatılmış bir iş ister.
ikinci göz KAPALI: --ikinci-goz yok
