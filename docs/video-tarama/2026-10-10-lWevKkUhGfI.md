# N8N ile Otomatikleştirilmiş Veo 3 Viral Videoları Oluşturun! (Ücretsiz Workflow) | n8n + Veo 3
## Künye
N8N ile Otomatikleştirilmiş Veo 3 Viral Videoları Oluşturun! (Ücretsiz Workflow) | n8n + Veo 3 · Ömer Göçmen | Yapay Zeka & Otomasyon · süre: 16:34 · tr-orig · https://youtu.be/lWevKkUhGfI · şema 2
motor: parti 2026-10-10-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 73669 tk · claude-haiku-5-5: claude-haiku-5-5 · 94901 tk
## Özet
Ömer Göçmen, Google'ın Veo 3 modelini fal.ai API'si üzerinden n8n içinde otomatikleştiren kodsuz bir iş akışını anlatıyor. Akış sırasıyla Schedule Trigger, Gemini ile çalışan 'Ideas AI Agent' (fikir, başlık, ortam üretir), Google Sheets'e fikir kaydı, 'Prompts AI Agent' (Veo 3 için ayrıntılı prompt), fal.ai'ye POST isteği, 600 sn bekleme, GET ile video URL'si alma ve Sheets'te final_output sütununu güncelleme adımlarından oluşuyor. fal.ai hesabı, API key üretimi, Header Auth credential kurulumu ve Veo 3 fiyatlandırması (saniye başı 0,50/0,75 dolar) gösteriliyor. Yazar krediyi bitirdiği için canlı video üretemiyor. Önceden çalıştırılmış sonuçları ve Sheets'teki mp4 bağlantılarını gösteriyor. Orijinal şablonda OpenAI vardı, yazar yerine Gemini koymuş. Workflow açıklamadaki gist bağlantısından paylaşılıyor.
## Bölümler
- 0:00 Giriş: Veo 3 ve n8n ile otomasyon fikri
- 1:01 Workflow'a genel bakış ve fal.ai'ye geçiş
- 1:26 fal.ai paneli, kredi ve API key oluşturma
- 2:42 fal.ai'de Veo 3 modelini bulma ve kredi hatası
- 3:14 Schedule Trigger düğümü
- 4:05 Ideas AI Agent, çıktı formatı ve Output Parser
- 5:36 Gemini modeli ve credential
- 6:08 Google Sheets'e fikir kaydı (Append Row)
- 8:56 Prompts AI Agent: Veo 3 promptu
- 10:04 Create Video: fal.ai'ye POST isteği ve Header Auth
- 12:02 Wait for Veo3 ve Get Video düğümleri
- 13:14 Veo 3 fiyatlandırması
- 14:15 Log Final Video: Sheets'te final_output güncelleme ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n | yok | teknik | yok | Kodsuz iş akışı otomasyon platformu; tüm hattın kurulduğu araç (localhost:5678'de çalışıyor). | 1:26 | Sol üstte n8n logosu, 'Workflow Automation - n8n' sekmesi, canvas. (karede: 1:26 karesinde n8n canvas'ı: Schedule Trigger, Ideas AI Agent, Log the Idea, Create Video, Wait for Veo3, Get Video, Log Final Video düğümleri.) |
| fal.ai | yok | teknik | yok | Veo 3 ve diğer modelleri API olarak sunan servis; video üretimi buradan yapılıyor. | 1:01 | Panel: fal-ai/veo3, API Keys, Billing; URL fal.ai/dashboard. (karede: 0:00 karesinde fal.ai Dashboard: Most Recent Models içinde fal-ai/veo3, luma-photon/flash/modify, ffmpeg-api/extract-frame.) |
| Veo 3 | yok | teknik | yok | Google'ın sesli video üretim modeli; fal-ai/veo3 uç noktası üzerinden çağrılıyor. | 0:00 | Bunu arkadaşlar Google'ın VO modeliyle yapıyoruz. VO3 modeliyle. (karede: 2:48 karesinde fal-ai/veo3 Playground: 'Veo 3 by Google, the most advanced AI video generation model'.) |
| Gemini 2.0 Flash Thinking Experimental | yok | teknik | yok | İki AI Agent'ın kullandığı dil modeli (n8n Google Gemini Chat Model düğümü, Gemini API credential). | 5:36 | Model alanında models/gemini-2.0-flash-thinking-exp seçili. · kanıt: kare (karede: 5:36 karesinde 'Google Gemini Chat Model' paneli, credential 'Google Gemini(PaLM) Api account 2', model models/gemini-2.0-flash-thinking-exp.) |
| Google Sheets | yok | teknik | yok | Fikir, caption, ortam ve final video URL'sinin log olarak tutulduğu e-tablo (veo-sheet). | 6:08 | Sheets düğümü Append Row; tabloda id, idea, caption, final_output sütunları. (karede: 7:00 karesinde 'veo-sheet' Google E-Tablolar: id, idea, caption, production, environment_prompt sütunları ve Yeti satırları.) |
| Schedule Trigger | yok | teknik | yok | Akışı zamanlı başlatan n8n düğümü; günlük, gece yarısı. | 3:46 | Trigger Interval Days, Days Between Triggers 1, Trigger at Hour Midnight. (karede: 3:46 karesinde Schedule Trigger paneli: Trigger Interval: Days, Days Between Triggers: 1, Trigger at Hour: Midnight, Minute 0.) |
| AI Agent | yok | teknik | yok | n8n AI Agent düğümü; 'Ideas AI Agent' fikri, 'Prompts AI Agent' Veo 3 promptunu üretiyor. | 4:05 | İki tane AI agent'ımız var. Biri ideas AI agent diğeri ise prompts AI agent. (karede: 4:14 karesinde Ideas AI Agent paneli: Prompt (User Message), Require Specific Output Format açık, System Message.) |
| Structured Output Parser | yok | teknik | yok | Ajan çıktısını JSON örneğinden üretilen şemaya zorlayan parser düğümü ('Parser'). | 5:00 | Schema Type: Generate From JSON Example; JSON Caption, Idea, Environment, Status. · kanıt: kare (karede: 5:12 karesinde Parser paneli: Schema Type 'Generate From JSON Example', JSON örneği Caption/Idea/Environment/Status (Diver Removes Nets Off Whale).) |
| Think | yok | teknik | yok | Canvas'ta Ideas AI Agent'a Tool olarak bağlı Think düğümü; konuşmada anlatılmıyor. | 1:26 | Canvas'ta 'Think' düğümü, Tool girişine kesikli çizgiyle bağlı. (karede: 1:30 karesinde sağ üstte 'Think' düğümü ve 'Tool' etiketi, Parser ile birlikte.) |
| HTTP Request | yok | teknik | yok | Create Video (POST) ve Get Video (GET) düğümleri; fal.ai kuyruğuna istek atar. | 10:04 | Method POST, URL https://queue.fal.run/fal-ai/veo3, Send Body raw JSON. (karede: 10:04 karesinde Create Video paneli: Method POST, URL queue.fal.run/fal-ai/veo3, Generic Credential Type, Header Auth, Send Body açık, Body { "prompt": ... }.) |
| Header Auth | yok | teknik | yok | fal.ai isteklerinde Authorization başlığıyla API key göndermek için n8n credential türü. | 10:36 | Generic Auth Type Header Auth; credential 'Header Auth account 2'. (karede: 10:36 karesinde 'Header Auth account 3' penceresi: Name ve Value alanları.) |
| Wait | yok | teknik | yok | Video üretimi için 600 saniye bekleten n8n düğümü ('Wait for Veo3'). | 12:02 | Resume After Time Interval, Wait Amount 600, Wait Unit Seconds. (karede: 12:02 karesinde 'Wait for Veo3' paneli: Resume After Time Interval, Wait Amount 600,00, Wait Unit Seconds.) |
| OpenAI Chat Model | yok | teknik | yok | Orijinal (workflow 19) şablondaki model düğümü; yazar yerine Gemini kullanmış. | 1:26 | Canvas'ta 'OpenAI Chat Model' düğümü; konuşmada 'Open AI yerine Gemini kullandım'. (karede: 1:26 karesinde 'OpenAI Chat Model' düğümü kırmızı uyarı işaretiyle, Ideas AI Agent'a bağlı.) |
| Google OAuth2 (Client ID/Secret) | yok | teknik | yok | Google Sheets credential'ı için OAuth2 Client ID ve Secret ile hesap bağlama. | 6:54 | Google Sheets account 4 penceresi: OAuth2 (recommended), Client ID, Client Secret. · kanıt: kare (karede: 6:54 karesinde 'Google Sheets account 4': OAuth2 seçili, OAuth Redirect URL, boş Client ID ve gizli Client Secret.) |
| ROW()-1 | yok | teknik | yok | Sheets id sütununa satır numarasından 1 çıkaran n8n ifadesi; eşleştirme anahtarı. | 8:08 | id alanında =ROW()-1 ifadesi. (karede: 9:14 karesinde Values to Update/Map alanında 'id =ROW()-1'; 6:44 karesinde Log the Idea id =ROW()-1.) |
| Google Gemini | yok | teknik | yok | Ideas ve Prompts AI agent'larında kullanılan dil modeli; seçilen model gemini-2.0-flash-thinking-exp. | 5:36 | models/gemini-2.0-flash-thinking-exp (karede: Google Gemini Chat Model düğümünde models/gemini-2.0-flash-thinking-exp model seçimi görünüyor) |
| JavaScript | yok | teknik | yok | n8n alanlarında {{ }} içine yazılan ifadelerin dili; satır numarası ve veri eşlemesi için kullanılıyor. | 4:28 | Anything inside {{ }} is JavaScript (karede: Düzenleyicide 'Anything inside {{ }} is JavaScript' ipucu metni görünüyor) |
| Ideas AI Agent'a konu vermek | yok | prompt | yok | Ideas AI Agent kullanıcı mesajı: konuşan bir Yeti'nin selfie çubuğuyla kameraya vlog yaptığı bir fikir ver. | 4:14 | kaynak: kare |
| Fikir/başlık/ortam çıktısının kuralları ve formatı | yok | prompt | yok | Sistem mesajı: tek satırlık JSON dizisi olarak tek fikir üret. Caption 13 kelimeden kısa, 1 emoji ve 12 küçük harfli hashtag; Idea ve Environment (20 kelime altı) alanları; Status her zaman 'for production'; gerçeküstü olabilir. | 4:28 | kaynak: kare |
| Fikri Veo 3 promptuna dönüştürmek | yok | prompt | yok | Prompts AI Agent kullanıcı mesajı: bu fikir için Veo3 promptu ver; fikir ve ortam önceki düğümden (Log the Idea) ifadelerle aktarılır. | 8:56 | kaynak: kare |
| Ayrıntılı Veo 3 promptu üretme kuralları | yok | prompt | yok | Sistem promptu: Google Veo3 için gerçekçi selfie tarzı klip yaz; tek paragraf, 750-1500 karakter; tek isimsiz karakter, bir cümle diyalog, fiziksel eylem; lens, film stoku, ses, arka plan, günün saati; altyazı/ekran yazısı yok, isim verme. | 9:14 | kaynak: kare |
| fal.ai arayüzünde Veo 3 denemesi | yok | prompt | yok | fal.ai oyun alanı örnek promptu: New York kaldırımında sokak röportajı; mikrofonlu kişi Veo3 modelini sorar, diğeri cevap verir. | 2:48 | kaynak: kare |
| Üretilen promptu fal.ai'ye göndermek | yok | prompt | yok | Create Video gövdesi: JSON içinde 'prompt' alanına Prompts AI Agent çıktısı (json.output) konur. | 11:48 | kaynak: kare |
## Açıklama bağlantıları
- https://gist.githubusercontent.com/omergocmen/674304349c86b619e9a34f4acea62da9/raw/51d2ccb8ff326ded28fab6fa3e428e6d378f4296/workflow.json — Videodaki n8n workflow'unun JSON dosyası (gist) · aday: hayır · Paylaşılan şablon dosyası; araç/servis bağlantısı değil, izleyici için indirme materyali. · sınıf: diğer
- https://youtu.be/nudCt2F7Tug — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil, içeriği pakette yok. · sınıf: diğer
- https://youtu.be/OPBIumlvDQo — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://youtu.be/e1DzQAh4Xw0 — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://youtu.be/BjqaV253lNI — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://youtu.be/gmYYHjlOJTI — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=wlyl_yv7nSk&lc=Ugz7N1NOe3aQdwU6rwJ4AaABAg&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu (yorum bağlantılı) · aday: hayır · Başka video; lc parametresi yorum kimliği, yönlendirme değil. · sınıf: diğer
- https://www.youtube.com/watch?v=uKoi9uQLdCs&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=gXhVFwzN4_4&t=2s&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=bXBS2Hzr-vU&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://www.youtube.com/watch?v=7tInlFRcTEQ&ab_channel=%C3%96merG%C3%B6%C3%A7men — Kanal sahibinin başka videosu · aday: hayır · Başka video; araç bağlantısı değil. · sınıf: diğer
- https://www.linkedin.com/in/%C3%B6mer-g%C3%B6%C3%A7men-43a353227 — Yazarın LinkedIn profili · aday: hayır · Sosyal medya profili; videoda kullanılan araç değil. · sınıf: diğer
- https://www.tiktok.com/@omerrgcmn — Yazarın TikTok profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
- https://www.instagram.com/omerrgcmn — Yazarın Instagram profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| POST https://queue.fal.run/fal-ai/veo3 | Veo 3 modeline video üretim isteğini kuyruğa gönderir; yanıtta request_id ve status/response URL'leri döner. (karede: Create Video düğümünde 'POST: https://queue.fal.run/fal...' yazısı) | 9:26 | kare |
| GET https://queue.fal.run/fal-ai/veo3/requests/{request_id} | Kuyruktaki isteğin durumunu ve bitince video URL'sini sorgular. (karede: Get Video düğümünde 'https://queue.fal.run/fal-ai/veo3/requests/{{ $json.req...' ifadesi) | 12:40 | kare |
| Authorization: Key <API_ANAHTARI> | fal.ai isteklerinde kimlik doğrulama başlığı; anahtar değeri n8n Header Auth kimlik bilgisine girilir. (karede: Header Auth penceresinde Name ve Value alanları, Name alanında Authorization) | 10:36 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Google Veo 3 API'si kapalıydı; fal.ai entegre edince n8n'den kullanılabilir oldu. | 0:00 | özellik |
| GitHub hesabıyla bağlanana 1 kredi veriliyor; yazar tek denemede -5 dolara düştü. | 2:00 | sayısal |
| Tek video için yaklaşık 6 dolar kredi gitti. | 2:00 | sayısal |
| Veo 3 saniye başı 0,50 dolar (ses kapalı) ya da 0,75 dolar (ses açık); 5 sn sesli video 3,75 dolar. | 13:14 | sayısal |
| Video üretimi 3, 5 ya da 10 dakika sürebilir; bu yüzden 600 sn bekleniyor. | 12:14 | sayısal |
| Gemini esnek ve limitleri yüksek olduğu için OpenAI yerine seçildi. | 5:07 | karşılaştırma |
| Google Sheets credential'ı için Sheets'in bulunduğu hesabın Client ID/Secret'i kullanılmalı. | 7:07 | öneri |
| Header Auth adı 'Authorization', değeri 'Key <API key>' biçiminde olmalı; Key'in K'si büyük. | 11:12 | öneri |
| Sheets güncellemesi fikir sütunuyla eşleştirilerek doğru satırın final_output'u yazılır. | 15:18 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | TikTok, YouTube Shorts, Instagram (sokak röportajı videoları) | aday değil: konu dışı | TikTok'ta YouTube Shorts kısmında ya da Instagram kısmında çok sık sokak röportajı |
| konuşma 0:00 | Veo 3 | Veo 3 | Bunu arkadaşlar Google'ın VO modeliyle yapıyoruz |
| konuşma 0:00 | Google Flow | aday değil: konu dışı | Yalnızca Google'ın flowu üzerinden gidip deneyimleyebiliyorduk |
| konuşma 0:00 | fal.ai | fal.ai | Fİ'ın VO3'ünü kendi sitesine entegre etmesiyle çözüldü |
| konuşma 0:00 | n8n | n8n | Bugün ise bu modeli Nen üzerinden nasıl otomatize ederiz? |
| kare 0:00 | Dark Reader tarayıcı eklentisi | aday değil: konu dışı | Araç ipucu 'Dark Reader – Bu siteye erişimi var' |
| kare 0:00 | luma-photon/flash/modify, ffmpeg-api/extract-frame (dashboard listesi) | aday değil: konu dışı | Most Recent Models listesinde görünüyor, kullanılmadı |
| konuşma 1:01 | Ücretsiz dolaşan workflow | n8n | Bakın her yerde dolaşan bir workflow. Aslında bu ücretsiz |
| konuşma 1:26 | GitHub ile giriş | aday değil: konu dışı | Herhangi bir şekilde Gitap'la ya da Google'la accountuzu oluşturabiliyorsunuz |
| kare 2:28 | fal.ai Account sayfası | fal.ai | fal.ai/dashboard/account/details sayfası |
| konuşma 2:02 | fal.ai API keys | fal.ai | API keys kısmına gelip API key'leri buradan oluşturabiliyorsunuz |
| kare 2:42 | Hunyuan Video (arama önerisi) | aday değil: konu dışı | fal-ai/hunyuan-video önerisi, kullanılmadı |
| kare 2:42 | Recraft 20b (arama önerisi) | aday değil: konu dışı | fal-ai/recraft-20b menüde görünüyor |
| kare 2:56 | Veo 2 / Veo 2 image-to-video | aday değil: konu dışı | Arama 'veo' sonuçlarında listeleniyor, kullanılmadı |
| kare 2:48 | fal-ai/veo3 Playground | Veo 3 | Veo 3 / Text to Video / fal.ai |
| konuşma 3:03 | Open AI yerine Gemini | OpenAI Chat Model | Open AI yerine Cemin kullandım. Modeli değiştirdim |
| konuşma 3:03 | Schedule Trigger | Schedule Trigger | Burada schedule trigger diye bir tane nodumuz var |
| konuşma 4:05 | Ideas AI Agent | AI Agent | Biri ideas AI agent diğeri ise prompts AI agent |
| konuşma 4:05 | Prompts AI Agent | AI Agent | Bu da fikirden prompt oluşturan |
| konuşma 4:05 | Require Specific Output Format | Structured Output Parser | Require specific output formatı seçiyoruz |
| konuşma 5:07 | Output Parser | Structured Output Parser | Output parser diye bir tane alan var |
| kare 1:30 | Think düğümü | Think | Canvas'ta Think, Tool girişine bağlı |
| kare 1:32 | Chat Model Memory etiketi | aday değil: başka adayın parçası (AI Agent) | Ideas AI Agent altında Chat Model, Memory, Tool girişleri |
| konuşma 5:07 | Gemini 2.0 Flash Thinking Experimental | Gemini 2.0 Flash Thinking Experimental | Cemini 2.0 Flash Thinking Experimental'ı seçtim ben |
| konuşma 5:07 | Gemini API key | aday değil: başka adayın parçası (Gemini 2.0 Flash Thinking Experimental) | Sadece API'yi girmeniz yeterli oluyor |
| kare 5:40 | generativelanguage.googleapis.com | aday değil: başka adayın parçası (Gemini 2.0 Flash Thinking Experimental) | Host alanında https://generativelanguage.googleapis.com |
| konuşma 6:08 | Google Sheets (Log the Idea) | Google Sheets | Bir Sheets nodu tutuyoruz |
| konuşma 7:07 | Client ID ve Secret | Google OAuth2 (Client ID/Secret) | Client ID ve Secret yazarak Google account bağlayabiliyorsunuz |
| konuşma 7:07 | Append row işlemi | aday değil: başka adayın parçası (Google Sheets) | Operation append row demişim |
| konuşma 8:08 | ROW()-1 ifadesi | ROW()-1 | D kısmına row -1 demişim |
| kare 7:04 | docs.google.com spreadsheets veo-sheet bağlantısı | Google Sheets | docs.google.com/spreadsheets/d/…/edit?gid=0 |
| kare 7:04 | accounts.google.com SignOutOptions ve gmail.com hesabı | aday değil: konu dışı | Hesap menüsü URL'si ve e-posta adresi |
| konuşma 9:09 | Google VO3 için prompt yaz | Veo 3 | Google VO3 için prompt yaz diyoruz |
| kare 9:14 | Kodak Vision3 500T, 16mm (üretilen prompttaki film stoku) | aday değil: konu dışı | Prompt çıktısında 'Film Stock: Kodak Vision3 500T' |
| konuşma 10:11 | Create Video POST isteği | HTTP Request | Öncelikle bir post isteği atıyoruz FI kısmına |
| kare 10:04 | queue.fal.run/fal-ai/veo3 | fal.ai | POST: https://queue.fal.run/fal-ai/veo3 |
| konuşma 10:11 | Generic credential type / Header Auth | Header Auth | Generic old type kısmına header out demişiz |
| konuşma 11:12 | Authorization / Key başlığı | aday değil: başka adayın parçası (Header Auth) | Buraya authorization yazıyoruz... key diyorum |
| konuşma 11:12 | Send Body raw JSON | aday değil: başka adayın parçası (HTTP Request) | Body content type RAW seçiyoruz |
| konuşma 12:14 | Wait for Veo3 (600 sn) | Wait | Bekletme nodu vasıtasıyla 600 saniye bekletebiliyoruz |
| kare 12:20 | What happens next düğüm menüsü (Discord, Slack, Gmail, Telegram, Notion vb.) | aday değil: konu dışı | Wait aranırken listelenen düğümler, kullanılmadı |
| konuşma 12:14 | Get Video GET isteği (request_id) | HTTP Request | Request ID'yi almışım ve VO3 kısmına GET isteği atmışım |
| konuşma 13:14 | Veo 3 fiyatlandırması | Veo 3 | Her saniye için 50 cent... sesle 0.75 |
| konuşma 14:15 | Log Final Video (Update Row) | Google Sheets | Bu da bir update row sheetsi |
| kare 15:14 | v3.fal.media mp4 çıktı bağlantısı | aday değil: konu dışı | final_output sütunundaki ..._output.mp4 URL'si |
| açıklama | workflow.json gist bağlantısı | aday değil: konu dışı | gist.githubusercontent.com/omergocmen/…/workflow.json |
| açıklama | Yazarın diğer YouTube videoları (11 bağlantı) | aday değil: konu dışı | youtu.be ve youtube.com/watch bağlantıları |
| açıklama | LinkedIn, TikTok, Instagram profilleri | aday değil: konu dışı | Sosyal medya bağlantıları |
| açıklama | #veo3 #n8n #nocode vb. etiketler | aday değil: konu dışı | Açıklama sonundaki hashtag listesi |
| linkli sayfa | fal.ai docs (compute, serverless, documentation, docs.fal.ai) | fal.ai | fal.ai/docs/documentation/… bağlantılı sayfalar |
| yorum | Cursor (izleyici talebi) | aday değil: konu dışı | Yorum: lütfen cursorun yeni özelliklerini incelermisin |
| yorum | Gemini Pro hesabında doğrudan Veo 3 | aday değil: konu dışı | Yorum: gmail hesabım pro gemini var veo 3 kullanabiliyorum |
## Kareden okunanlar
- 0:00: fal.ai Dashboard: Most Recent Models (ffmpeg-api/extract-frame, luma-photon/flash/modify, veo3); sekmeler veo-sheet, Workflow Automation - n8n, My workflow 20 - n8n.
- 1:26: n8n canvas 'My workflow 19': OpenAI Chat Model, Parser, Think, Ideas AI Agent, Log the Idea, Prompts AI Agent, Create Video, Wait for Veo3, Get Video, Log Final Video.
- 2:00: fal.ai sağ üstte kırmızı daireyle -$5.00 bakiye.
- 2:36: 'New key secret' penceresi: Scope API, Name alanı, 'Your FAL_KEY will be shown here once created'.
- 2:48: fal-ai/veo3 Playground: örnek sokak röportajı promptu, Aspect Ratio 16:9, fiyat notu $3.75.
- 3:06: Result Error: 'Not enough credits — You need to add some credits to run this model.'
- 4:14: Ideas AI Agent: Prompt 'Give me an idea about [a Yeti speaking to a camera...]', Require Specific Output Format açık; çıktıda Caption, Idea, Environment, Status.
- 5:36: Google Gemini Chat Model: model models/gemini-2.0-flash-thinking-exp.
- 6:44: Log the Idea: Append Row, Document By ID, Sheet Sayfa1, Map Each Column Manually, id =ROW()-1.
- 7:00: veo-sheet tablosu: id, idea, caption, production, environment_prompt sütunları.
- 10:04: Create Video: POST https://queue.fal.run/fal-ai/veo3; çıktı status IN_QUEUE, request_id, response_url, status_url, cancel_url.
- 12:02: Wait for Veo3: After Time Interval, 600,00 Seconds.
- 12:40: Get Video: GET https://queue.fal.run/fal-ai/veo3/requests/{{ $json.request_id }}, Header Auth.
- 15:12: Sheets final_output sütunu: https://v3.fal.media/files/tiger/…_output.mp4 bağlantıları.
## Belirsizlikler
- Yazar kredisi bittiği için Get Video çıktısı canlı gösterilmedi; mp4 URL'leri önceki çalıştırmalardan.
- Konuşmada 'Cemin/Cemina' = Gemini, 'VO 3' = Veo 3, 'FI/Fayı' = fal.ai olarak yorumlandı (ASR hatası).
- Think düğümünün amacı anlatılmıyor; Chat Model Memory etiketi yalnızca canvas'ta görünüyor.
- fal.ai menü/listelerinde görünen Hunyuan Video, Recraft 20b, Veo 2, Luma Photon, ffmpeg extract-frame videoda kullanılmadı; aday yapılmadı.
- Sözlük eşleşmelerinden Make, Framer Motion, Descript, Stable Diffusion, Canva, Express, Next.js, Notion, Telegram, Discord, Slack, Flux, Redis, Claude vb. OCR gürültüsü/menü öğesi; videoda kullanılmadı.
- Videoda terminal ya da slash komutu yok; kurulum_komutlar boş.
- Header Auth değeri ve API key'ler ekranda görünüyor olabilir; değerler yazılmadı.
- Açıklamadaki bağlantılar için sayfa içeriği pakette yok; sınıflandırma yalnızca URL'ye dayanıyor.
## Atlanan segment oranı
0/17 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://gist.githubusercontent.com/omergocmen/674304349c86b619e9a34f4acea62da9/raw/51d2ccb8ff326ded28fab6fa3e428e6d378f4296/workflow.json | açıklama | açıklama | evet |
| https://fal.ai | 0:00 | ekran | evet |
| https://fal.ai/dashboard/account/details | 2:26 | ekran | evet |
| https://fal.ai/dashboard/keys | 2:30 | ekran | evet |
| https://fal.ai/models/fal-ai/veo3 | 2:48 | ekran | evet |
| https://fal.ai/models/fal-ai/hunyuan-video | 2:51 | ekran | hayır |
| https://generativelanguage.googleapis.com | 5:40 | ekran | evet |
| https://queue.fal.run/fal-ai/veo3 | 9:26 | ekran | evet |
| https://v3.fal.media/files/tiger/e2lnP99Kzdwsad70SesYRXr9_output.mp4 | 15:14 | ekran | hayır |
| https://docs.google.com/spreadsheets/d/…/edit?gid=0 | 7:04 | ekran | hayır |
| https://fal.ai/docs/documentation/compute | açıklama | açıklama | hayır |
| https://fal.ai/docs/documentation/serverless | açıklama | açıklama | hayır |
| https://fal.ai/docs/documentation | açıklama | açıklama | hayır |
| https://docs.fal.ai | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — fal.ai hesabı oluşturma ve kredi bakiyesini kontrol etme — araçlar: fal.ai
- 2. adım — fal.ai API anahtarı oluşturma (Account > API Keys) — araçlar: fal.ai
- 3. adım — fal.ai Veo 3 playground'da deneme çalıştırması; kredi hatasının görülmesi — araçlar: fal.ai, Veo 3
- 4. adım — n8n'de Schedule Trigger düğümünü günlük zamanlama ile ayarlama — araçlar: n8n
- 5. adım — Ideas AI Agent ile fikir üretme ve Output Parser ile JSON çıktı şemasını tanımlama — araçlar: n8n, Google Gemini, Output Parser
- 6. adım — Log the Idea: fikri Google Sheets'e append ile kaydetme — araçlar: n8n, Google Sheets
- 7. adım — Google Sheets kimlik bilgisini Google client ID ve secret ile bağlama — araçlar: n8n, Google Sheets
- 8. adım — Prompts AI Agent ile Veo 3 prompt'u üretme — araçlar: n8n, Google Gemini
- 9. adım — Create Video: fal kuyruğuna POST isteği ile video isteği gönderme; Header Auth ile API anahtarı tanımlama — araçlar: n8n, fal.ai, Veo 3, Header Auth
- 10. adım — Wait for Veo3: 600 saniye bekleme — araçlar: n8n
- 11. adım — Get Video: request ID ile GET isteği atıp video URL'sini alma — araçlar: n8n, fal.ai
- 12. adım — Kredi hatası kontrolü ve kredi yüklenmesi gerektiğinin fark edilmesi — araçlar: fal.ai
- 13. adım — Log Final Video: final_output sütununu Sheets'te update ile güncelleme — araçlar: n8n, Google Sheets
- 14. adım — Sheets'te final_output bağlantılarını ve satır eşlemesini kontrol etme — araçlar: Google Sheets
## Promptlar
- Ideas AI Agent'a konu vermek — Ideas AI Agent kullanıcı mesajı: konuşan bir Yeti'nin selfie çubuğuyla kameraya vlog yaptığı bir fikir ver.
- Fikir/başlık/ortam çıktısının kuralları ve formatı — Sistem mesajı: tek satırlık JSON dizisi olarak tek fikir üret. Caption 13 kelimeden kısa, 1 emoji ve 12 küçük harfli hashtag; Idea ve Environment (20 kelime altı) alanları; Status her zaman 'for production'; gerçeküstü olabilir.
- Fikri Veo 3 promptuna dönüştürmek — Prompts AI Agent kullanıcı mesajı: bu fikir için Veo3 promptu ver; fikir ve ortam önceki düğümden (Log the Idea) ifadelerle aktarılır.
- Ayrıntılı Veo 3 promptu üretme kuralları — Sistem promptu: Google Veo3 için gerçekçi selfie tarzı klip yaz; tek paragraf, 750-1500 karakter; tek isimsiz karakter, bir cümle diyalog, fiziksel eylem; lens, film stoku, ses, arka plan, günün saati; altyazı/ekran yazısı yok, isim verme.
- fal.ai arayüzünde Veo 3 denemesi — fal.ai oyun alanı örnek promptu: New York kaldırımında sokak röportajı; mikrofonlu kişi Veo3 modelini sorar, diğeri cevap verir.
- Üretilen promptu fal.ai'ye göndermek — Create Video gövdesi: JSON içinde 'prompt' alanına Prompts AI Agent çıktısı (json.output) konur.
ikinci göz KAPALI: --ikinci-goz yok
