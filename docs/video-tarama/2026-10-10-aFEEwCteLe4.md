# Yapay Zeka Fikrimi Çalışan Bir Uygulamaya Dönüştürdüm! | Higgsfield API
## Künye
Yapay Zeka Fikrimi Çalışan Bir Uygulamaya Dönüştürdüm! | Higgsfield API · Poyraz Avsever · süre: 14:39 · tr-orig · https://youtu.be/aFEEwCteLe4 · şema 2
motor: parti 2026-10-10-short-7 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 66862 tk · claude-haiku-5-5: claude-haiku-5-5 · 243414 tk
## Özet
Poyraz Avsever, Higgsfield API ile fotoğrafı kısa videoya dönüştüren bir demo uygulamayı tek promptla Codex içinde (GPT-5.6 Sol) yaptırıyor. Konsolda Kling 3.0 Turbo (image-to-video) modelini seçiyor, API key oluşturuyor, doküman bağlantısını ve anahtarı prompta ekliyor. Çıkan Next.js uygulaması localhost'ta çalışıyor; bir üretim 0,31 dolara mal oluyor. Sonda maliyet/iş modeli fikirleri ve indirimler anlatılıyor. Video, Higgsfield ile #işbirliği olarak işaretli.
## Bölümler
- 0:00 Giriş
- 1:00 Higgsfield API bakalım
- 6:50 Promptumuzu gönderelim
- 8:19 Uygulama Sonucu
- 11:09 Peki nasıl oluyor bu
- 14:09 Kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Higgsfield API | yok | CLI | yok | Üretken görsel/video modellerini tek API üzerinden sunan, kullandıkça öde servis | 1:00 | Ben bunun için Hixfield'ın API'ını kullanacağım. (karede: Higgsfield API paneli, Dashboard, Explore models, Pricing menüsü) |
| Codex | yok | CLI | yok | Kodu yazan ana yapay zekâ kodlama aracı; proje klasörü Higgsfield API olarak açıldı | 1:00 | Aynı zamanda Codex ile beraber çalışacağız arkadaşlar. (karede: Sol menüde Codex başlığı, Projeler altında Higgsfield API) |
| GPT-5.6 Sol | yok | prompt | yok | Codex'te seçili ana model, Yüksek akıl yürütme düzeyi | 0:56 | Model seçici GPT-5.6 Sol Yüksek (karede: Alt sağda 'GPT-5.6 Sol Yüksek' model seçici) |
| Kling 3.0 Turbo | yok | teknik | yok | Fotoğraftan video üreten, ucuz ve hızlı model (image-to-video) | 4:32 | Ben buradan image to video turbo'yu seçiyorum. (karede: Explore / Kling 3.0 Turbo sayfası, Image-to-Video (Turbo)) |
| Kling 3.0 | yok | teknik | yok | Konsolda gösterilen Kling model ailesi (Standard, Pro, 4K, Turbo, Motion Control) | 3:44 | Örneğin ben burada Killing 3.0 modelini tercih etmek istiyorum. (karede: Kling 3.0 Standard sayfası, açılır listede varyantlar) |
| Seedance 2.5 | yok | teknik | yok | Konsolda listelenen ByteDance video modeli; API key kurulum promptunda adı geçiyor | 0:46 | Ekranda bytedance / Seedance 2.5 kartı (karede: Fiyat tablosu ve model kartlarında Seedance 2.5, Seedance 2.0) |
| MiniMax Hailuo 2.3 | yok | teknik | yok | %75 indirimli olarak anlatılan video modeli | 12:38 | Mesela bakın, Minimx Helu 2.3'te %75 bir indirim var. (karede: Fiyat sayfası 2. sayfa, MiniMax Hailuo 2.3 satırı %75 OFF) |
| Next.js | yok | teknik | yok | Uygulama iskeleti (App Router) | 6:28 | Next.js App Router, TypeScript ve Tailwind CSS kullan. (karede: Prompt metni: Next.js App Router, TypeScript ve Tailwind CSS kullan) |
| TypeScript | yok | teknik | yok | Uygulama dili ve Higgsfield SDK örnek dili | 6:28 | Prompt metninde TypeScript geçiyor (karede: Prompt metni ve API key kurulum sekmesi TypeScript) |
| Tailwind CSS | yok | teknik | yok | Arayüz stilleme çerçevesi | 6:28 | Prompt metninde Tailwind CSS geçiyor (karede: Prompt: Next.js App Router, TypeScript ve Tailwind CSS kullan) |
| @higgsfield/client | yok | CLI | yok | Resmî TypeScript SDK; npm ile kuruluyor | 6:02 | npm install @higgsfield/client dotenv (karede: TypeScript sekmesinde 'npm install @higgsfield/client dotenv') |
| npm | yok | CLI | yok | Paket yöneticisi; npm run dev ile geliştirme sunucusu | 8:22 | npm run dev dedim. (karede: PowerShell'de npm run dev, next dev çıktısı) |
| PowerShell | yok | CLI | yok | Komutların çalıştırıldığı terminal | 8:02 | PowerShell'imi açtım. (karede: Windows PowerShell penceresi) |
| dotenv | yok | teknik | yok | Ortam değişkeni (.env.local) yükleme kütüphanesi | 6:02 | npm install @higgsfield/client dotenv (karede: Kurulum komutunda dotenv) |
| tsx | yok | CLI | yok | TypeScript dosyalarını çalıştıran araç | 6:04 | npx tsx index.ts (karede: npx tsx index.ts ve --save-dev tsx typescript) |
| Excalidraw | yok | teknik | yok | Çizim aracı; draw.poyrazavsever.com üzerinden gösterilen kendi sürümü | 10:48 | Ekranda draw.poyrazavsever.com çizim tahtası (karede: Çizim arayüzü: yeşil dikdikörtgen, ok aracı, Arrow type paneli) |
| polling | yok | teknik | yok | Üretim durumunu düzenli sorgulama; webhook yerine kullanıldı | 7:56 | Arayüz ve polling: 2 saniyeden 10 saniyeye çıkan kontrol (karede: Codex yanıtında 'Arayüz ve polling (line 117)') |
| Higgsfield SDK | yok | teknik | yok | Higgsfield'ın resmi istemci kütüphanesi (@higgsfield/client); isteği gönderir ve sonucu bekler. | 5:00 | 'Install an official server-side SDK. cURL needs no package.' yönergesi (karede: Higgsfield API dokümanında kurulum adımı ve 'npm install @higgsfield/client dotenv' satırı) |
| Fotoğraftan video demo uygulamasını Codex'e yaptırmak | yok | prompt | yok | Bu klasörde Higgsfield API ile fotoğrafı kısa videoya çeviren çalışan demo uygulama yap. Next.js App Router, TypeScript, Tailwind. Yerelde çalışsın; hesap, ödeme, veritabanı olmasın. Önce docs kaynaklarını oku, modelin dokümanını kullan, desteklenmeyen parametre uydurma. Arayüz: Türkçe, sade, beyaz, kırmızı vurgu; fotoğraf yükleme (10 MB sınır), hareket tarifi, 'Videoyu oluştur' butonu, durum, yan yana sonuç, indirme. Polling kullan, sahte yanıt yok, butona basmadan ücretli üretim başlatma, maliyeti ucuz ayarlarla README'de belirt. | 6:50 | kaynak: kare |
| Uygulamada üretilecek videonun hareket tarifi | yok | prompt | yok | Kamera kişiye doğru yaklaşır ve kişi göz kırpar. | 9:20 | kaynak: kare |
## Açıklama bağlantıları
- https://higgsfield.ai/s/higgsfield-api-yt-poyrazavsever-kRAPBE — Higgsfield API tanıtım/yönlendirme bağlantısı · aday: evet (Higgsfield API) · Videoda kullanılan Higgsfield API servisini adlandırıyor; #işbirliği ve yönlendirme kodu var, açık 'sponsorluğunda' ifadesi yok. · sınıf: affiliate
- https://docs.higgsfield.ai — Higgsfield API dokümantasyonu · aday: evet (Higgsfield API) · Videoda doküman bağlantıları prompta verildi; Higgsfield servisinin dokümanı. · sınıf: diğer
- https://instagram.com/poyraz_avsever — Sunucunun Instagram hesabı · aday: hayır · Sosyal medya profili, araç değil. · sınıf: diğer
- https://linkedin.com/in/poyrazavsever — Sunucunun LinkedIn profili · aday: hayır · Sosyal medya profili, araç değil. · sınıf: diğer
- https://github.com/poyrazavsever — Sunucunun GitHub profili · aday: hayır · Kişisel profil, izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://poyrazavsever.com — Sunucunun kişisel web sitesi (prompt paylaşımı) · aday: hayır · Kişisel site/portfolyo; referans sayfa. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Tek sütun başlık + iki sütunlu kart yerleşimi (two-column card layout) | Sol kartta fotoğraf seçme ve hareket tarifi, sağ kartta üretim durumu paneli (karede: 'Fotoğrafını Canlandır' başlığı; solda '1. Fotoğrafını seç', sağda 'ÜRETİM DURUMU Hazır') | 8:30 | kare |
| Dosya yükleme alanı (upload dropzone) | Kesikli çerçeveli, yükleme ikonlu 'Fotoğraf seçmek için tıklayın' alanı; seçince önizleme ve 'Değiştir' düğmesi (karede: Yüklenen profil fotoğrafı önizlemesi, dosya adı ve 'Değiştir' düğmesi) | 9:10 | kare |
| Karakter sayaçlı metin alanı (textarea with character counter) | Hareket tarifi alanı, sağ üstte 0/1000 sayacı (karede: '2. Hareketi tarif et' alanı, 0/1000 ve yer tutucu metin) | 8:30 | kare |
| Kırmızı vurgulu birincil buton ve devre dışı durum (primary button, disabled state) | 'Videoyu oluştur' butonu; boşken gri, hazırken kırmızı (#dc2626 vurgu) (karede: Gri pasif buton; sonra kırmızı 'Videoyu oluştur' butonu) | 9:10 | kare |
| Durum göstergesi ve istek kimliği (status indicator, request ID) | 'İşleniyor' durumu, sarı nokta ve istek kimliği kutusu (karede: 'İşleniyor', 'İSTEK KİMLİĞİ' ve kimlik metni, buton 'İşleniyor') | 9:20 | kare |
| Önce/sonra yan yana karşılaştırma (before/after comparison) | Orijinal fotoğraf ve oluşturulan video yan yana; video oynatıcı ve 'Videoyu indir' butonu (karede: 'Önce ve sonra' bölümü, Orijinal fotoğraf / Oluşturulan video, 'Videoyu indir') | 13:24 | kare |
| Beyaz arka planlı sade tema (minimal light theme) | Türkçe, sade, beyaz zemin, kırmızı vurgu rengi (karede: Prompt maddesi: 'Türkçe, sade, beyaz arka planlı; kırmızı vurgu rengi #dc2626') | 6:24 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm install @higgsfield/client dotenv | Higgsfield resmî SDK ve dotenv paketlerini kurar (karede: API key penceresi TypeScript sekmesi: 'npm install @higgsfield/client dotenv') | 6:02 | kare |
| npm install --save-dev tsx typescript | TypeScript çalıştırma geliştirme bağımlılıklarını kurar (karede: '--save-dev tsx typescript' satırı) | 6:02 | kare |
| npx tsx index.ts | SDK örnek betiğiyle ilk video üretim isteğini çalıştırır (karede: Penceredeki 'npx tsx index.ts') | 6:04 | kare |
| cd "D:\Yazılım\video\higgsfield-api" | Proje klasörüne geçer (karede: PowerShell: cd "D:\Yazılım\video\higgsfield-api") | 8:16 | kare |
| npm run dev | Next.js geliştirme sunucusunu başlatır (localhost:3000) (karede: PowerShell: higgsfield-api@0.1.0 dev, next dev) | 8:22 | kare |
| export HF_CREDENTIALS="YOUR_KEY_ID:YOUR_KEY_SECRET" | Anahtar çiftini ortam değişkeni olarak tanımlar (ekranda yer tutucu değer; gerçek anahtar yazılmadı) (karede: API dokümanında 'export HF_CREDENTIALS="YOUR_KEY_ID:YOUR_KEY_SECRET"' satırı) | 4:52 | kare |
| HF_CREDENTIALS=<anahtar-kimliği>:<anahtar-sırrı> (.env.local) | Anahtarı yerel .env.local dosyasına yazmak için kullanılan satır; değer bu formda yazılmadı (karede: API anahtarı penceresinde '.env.local' başlığı ve HF_CREDENTIALS satırı) | 6:02 | kare |
| npm run lint | Kod kalitesi kontrolünü çalıştırır (Codex'in bildirdiği) (karede: Codex çıktısında 'npm run lint geçti' satırı) | 7:50 | kare |
| npm run typecheck | TypeScript tip kontrolünü çalıştırır (Codex'in bildirdiği) (karede: Codex çıktısında 'npm run typecheck geçti' satırı) | 7:50 | kare |
| npm run build | Üretim derlemesi alır (Codex'in bildirdiği) (karede: Codex çıktısında 'npm run build geçti' satırı) | 7:50 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Higgsfield API'de fiyatlar rakiplere göre yaklaşık %45-50'ye varan indirimli; indirim yaklaşık 4 gün 5 saat sonra bitecek. | 1:00 | karşılaştırma |
| Kling 3.0 Turbo için fal karşılaştırmasında Higgsfield saniyesi 0,077 dolar, fal 0,14 dolar. | 1:36 | sayısal |
| Tek video üretimi 31 cent harcadı; bakiye 70 dolardı. | 9:32 | sayısal |
| Uygulama tek promptla yaklaşık 12 dakikada soru sormadan yapıldı. | 8:19 | sayısal |
| Turbo model ucuz ve hızlı; üretim yaklaşık 20-30 saniye sürdü. | 9:20 | özellik |
| Üretilen videoda kamera yaklaştı ama göz kırpma tarifi yanlış olduğu için tam çıkmadı; kişide ve arka planda değişiklik yok. | 10:21 | özellik |
| MiniMax Hailuo 2.3'te %75 indirim var. | 12:38 | sayısal |
| Geliştirme kullanıcı lansmanı için yaklaşık bir iki gün sürer. | 13:10 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 1:00 | Higgsfield API | Higgsfield API | Ben bunun için Hixfield'ın API'ını kullanacağım. |
| konuşma 1:00 | Codex | Codex | Aynı zamanda Codex ile beraber çalışacağız |
| kare 0:56 | GPT-5.6 Sol | GPT-5.6 Sol | Model seçici GPT-5.6 Sol Yüksek |
| kare 0:46 | Seedance 2.5 | Seedance 2.5 | Model kartı bytedance / Seedance 2.5 |
| konuşma 4:03 | Kling 3.0 | Kling 3.0 | Killing 3.0 modelini tercih etmek istiyorum |
| konuşma 4:32 | Kling 3.0 Turbo | Kling 3.0 Turbo | image to video turbo'yu seçiyorum |
| konuşma 12:38 | MiniMax Hailuo 2.3 | MiniMax Hailuo 2.3 | %75 indirim var |
| kare 6:28 | Next.js | Next.js | Next.js App Router |
| kare 6:28 | TypeScript | TypeScript | TypeScript prompt metninde |
| kare 6:28 | Tailwind CSS | Tailwind CSS | Tailwind CSS prompt metninde |
| kare 6:02 | @higgsfield/client | @higgsfield/client | npm install @higgsfield/client dotenv |
| kare 6:02 | dotenv | dotenv | npm install ... dotenv |
| kare 6:04 | tsx | tsx | npx tsx index.ts |
| kare 8:22 | npm | npm | npm run dev |
| kare 8:02 | PowerShell | PowerShell | Windows PowerShell penceresi |
| kare 10:48 | Excalidraw (draw.poyrazavsever.com) | Excalidraw | Çizim tahtası arayüzü, ok aracı |
| kare 7:56 | polling | polling | Arayüz ve polling (line 117) |
| konuşma 0:00 | Selamlama ve fikir geliştirme tanıtımı | aday değil: genel kavram | Fikir nasıl geliştirilir, doğrulanır |
| kare 0:00 | Stüdyo posterleri (There is no cloud, Git commit) | aday değil: konu dışı | Arka plan posterleri |
| kare 0:30 | Atölye/workshop fotoğrafı | aday değil: konu dışı | Sunucunun daha önceki workshop'u |
| konuşma 2:00 | Google Play / App Store | aday değil: genel kavram | Google Play'e, App Store'a vereceğim parası |
| konuşma 12:09 | SaaS iş modeli | aday değil: genel kavram | aylık bir SAS tool olarak |
| konuşma 2:00 | Fal karşılaştırması | aday değil: konu dışı | Fiyat karşılaştırma tablosundaki rakip sütunu, kullanılmadı |
| kare 3:32 | Genjutsu / Cinema Studio / Wan / Grok modelleri | aday değil: konu dışı | Yalnız listede göründü |
| kare 1:22 | ChatGPT, Discord, yer imleri | aday değil: konu dışı | Tarayıcı yer imi çubuğu |
| kare 8:36 | Gemini, OneDrive, WhatsApp dosya gezgini öğeleri | aday değil: konu dışı | Dosya seçici klasör/dosya listesi |
| açıklama | Instagram profili | aday değil: konu dışı | instagram.com/poyraz_avsever |
| açıklama | LinkedIn profili | aday değil: konu dışı | linkedin.com/in/poyrazavsever |
| açıklama | GitHub profili | aday değil: konu dışı | github.com/poyrazavsever |
| açıklama | poyrazavsever.com | aday değil: konu dışı | Kişisel site, referans |
| açıklama | Higgsfield yönlendirme bağlantısı | Higgsfield API | higgsfield.ai/s/... linki |
| linkli sayfa | Genjutsu motion-transfer dokümanı | aday değil: konu dışı | Videoda kullanılmayan model |
| linkli sayfa | Webhooks dokümanı | aday değil: konu dışı | Videoda webhook yerine polling kullanıldı |
| linkli sayfa | console.higgsfield.ai | Higgsfield API | Konsol, API key ekranı |
| yorum | Antigravity CLI önerisi | aday değil: konu dışı | Yorumda önerildi, videoda kullanılmadı |
| yorum | Google AI Pro, VS Code, Python | aday değil: konu dışı | İzleyici sorusu, videoda kullanılmadı |
| kare 4:52 | Python SDK | aday değil: başka adayın parçası (@higgsfield/client) | Docs'ta Python sekmesi, kullanılmadı |
| kare 5:00 | cURL | aday değil: genel kavram | 'cURL needs no package' |
| kare 9:32 | Billing / bakiye | aday değil: başka adayın parçası (Higgsfield API) | $0.31 before discounts |
| kare 8:22 | localhost:3000 uygulaması | aday değil: başka adayın parçası (Next.js) | Çalışan demo uygulama |
## Kareden okunanlar
- 0:56: Codex arayüzü; proje Higgsfield API; model GPT-5.6 Sol Yüksek; soru: 'Higgsfield API içinde ne üzerinde çalışmalıyız?'
- 1:30: Higgsfield API fiyat sayfası; 'Cashback received $0.00', Seedance 2.5 from $0.144/s, Seedance 2.0 from $0.0985/s
- 1:36: 'Compare with others' tablosu: Kling 3.0 4K $0.231/s vs Fal $0.42/s, 45% lower
- 3:50: Billing sayfası bakiye $70.00, açılır ödeme penceresi 'Add funds', Buy for $5
- 4:16: Kling 3.0 Standard varyant listesi: Text to Video, Image to Video (Turbo), Motion Control (Pro)
- 4:56: API reference: parametreler prompt, duration, image_url, resolution (720p/1080p); subscribe örnek kodu
- 5:38: API Keys sayfası, 'Create API key' ve 'Calculate profit' düğmeleri
- 5:50: API key oluşturma penceresi, ad Youtube-video, son kullanma tarihi seçenekleri
- 7:20: Codex'te prompt maddeleri: sahte video yok, butonla başlat, #dc2626 kırmızı vurgu
- 7:52: Codex yanıtı: lint, typecheck, build geçti; Kling 3.0 Turbo, 5 saniye, 720p; npm run dev, localhost:3000
- 8:30: Uygulama: 'Fotoğrafını Canlandır', 'Higgsfield Video Lab', Kling 3.0 Turbo, JPEG/PNG/WebP en fazla 10 MB
- 13:24: Önce ve sonra bölümü, Videoyu indir butonu
## Belirsizlikler
- Sunucu 'sponsor değilim' benzeri ifade kullanıyor ama açıklama #işbirliği içeriyor; bağlantı bu yüzden 'affiliate' sınıflandı (açık sponsor ifadesi yok).
- API anahtarı değerleri ekranda görünüyor; rapora yazılmadı.
- Altyazıda 'Codex 56 Sol 56 Astra' geçiyor; ekranda model GPT-5.6 Sol Yüksek olarak görünüyor.
- Sözlük eşleşmeleri (Redis, Vercel, Framer Motion, Ollama, Redux, Canva, Descript, Make vb.) çoğunlukla OCR gürültüsü veya tarayıcı yer imi/sekme; videoda kullanılmadı.
- Altyazıdaki 'Ced 2,5' büyük olasılıkla Seedance 2.5; 'Killing 3' Kling 3.0.
- Menüde görünen modeller (Wan 3.0 Prime, Grok Imagine 2.0, Happy Horse 1.1, Genjutsu, Cinema Studio 4.0 vb.) yalnız listede göründü, kullanılmadı.
- Yorumda anılan Antigravity ve Google AI Pro, VS Code ile ilgili soru videoda kullanılmadı.
- Fiyat sayfasındaki tarihler (2026) ve 'Cashback' kampanyası değişebilir.
## Atlanan segment oranı
0/16 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://higgsfield.ai/s/higgsfield-api-yt-poyrazavsever-kRAPBE | açıklama | açıklama | evet |
| https://docs.higgsfield.ai | açıklama | açıklama | evet |
| https://instagram.com/poyraz_avsever | açıklama | açıklama | hayır |
| https://linkedin.com/in/poyrazavsever | açıklama | açıklama | hayır |
| https://github.com/poyrazavsever | açıklama | açıklama | hayır |
| https://poyrazavsever.com | açıklama | açıklama | hayır |
| https://docs.higgsfield.ai/docs/models/genjutsu/motion-transfer | açıklama | açıklama | hayır |
| https://console.higgsfield.ai | açıklama | açıklama | evet |
| https://docs.higgsfield.ai/docs/how-to/webhooks | açıklama | açıklama | hayır |
| open.higgsfield.ai/dashboard | 1:22 | ekran | evet |
| open.higgsfield.ai/pricing | 1:30 | ekran | evet |
| open.higgsfield.ai/explore | 3:20 | ekran | evet |
| open.higgsfield.ai/billing | 3:50 | ekran | evet |
| open.higgsfield.ai/models/kling-video/v3.0-turbo/image-to-video/playground | 4:32 | ekran | evet |
| open.higgsfield.ai/models/kling-video/v3.0-turbo/image-to-video/api-reference | 4:48 | ekran | evet |
| https://api.higgsfield.ai/kling-video/v3.0-turbo/image-to-video | 5:00 | ekran | evet |
| open.higgsfield.ai/api-keys | 5:38 | ekran | evet |
| https://docs.higgsfield.ai/docs/llms.txt | 6:28 | ekran | evet |
| https://docs.higgsfield.ai/docs/authentication | 6:28 | ekran | evet |
| https://docs.higgsfield.ai/docs/concepts/file-uploads | 6:28 | ekran | evet |
| https://docs.higgsfield.ai/docs/concepts/polling | 6:28 | ekran | evet |
| http://localhost:3000 | 7:52 | ekran | hayır |
| draw.poyrazavsever.com | 10:32 | ekran | evet |
| open.higgsfield.ai/models/minimax/hailuo-2.3/standard/image-to-video | 12:38 | ekran | evet |
| https://example.com/input.jpg | 4:56 | ekran | hayır |
| https://higgsfield.ai/s/higgsfield-api-yt-poyrazavsever-kRAPBE | açıklama | yorum | evet |
| open.higgsfield.ai/models/kling-video/v3.0/4k/text-to-video | 2:12 | ekran | evet |
| open.higgsfield.ai/models/bytedance/seedance-2.5/text-to-video | 2:18 | ekran | evet |
| http://localhost:4200/admin/home | 8:28 | ekran | hayır |
## İş akışı
- 1. adım — Codex'te Higgsfield API adında proje oluşturup boş klasörü kaynak klasör olarak bağlama — araçlar: Codex, GPT-5.6 Sol
- 2. adım — Higgsfield konsolunda fiyatlandırma ve rakip karşılaştırma tablosunu inceleme — araçlar: Higgsfield API
- 3. adım — Explore models'ta video filtresiyle modelleri listeleyip Kling 3.0'ı seçme — araçlar: Higgsfield API, Kling 3.0
- 4. adım — Billing sayfasında bakiyeyi ve para yükleme mantığını gösterme — araçlar: Higgsfield API
- 5. adım — Image-to-Video (Turbo) varyantını seçip API reference sayfasını inceleme — araçlar: Kling 3.0 Turbo, @higgsfield/client
- 6. adım — API keys sayfasında süreli API key oluşturup kopyalama — araçlar: Higgsfield API
- 7. adım — Hazırladığı uygulama promptunu Codex'e yapıştırma — araçlar: Codex, GPT-5.6 Sol
- 8. adım — Model doküman bağlantısını (Copy agent prompt metni) prompta ekleme — araçlar: Higgsfield API, Codex
- 9. adım — API anahtarını ve key ID'yi prompta ekleyip gönderme — araçlar: Codex, Higgsfield API
- 10. adım — Codex'in uygulamayı yazması, lint/typecheck/build testlerini çalıştırması — araçlar: Codex, Next.js, npm
- 11. adım — PowerShell'de proje klasörüne geçip npm run dev ile sunucuyu başlatma — araçlar: PowerShell, npm, Next.js
- 12. adım — localhost:3000'de uygulamayı açıp profil fotoğrafı yükleme — araçlar: Next.js, Tailwind CSS
- 13. adım — Hareket tarifini yazıp videoyu oluşturma, durumu polling ile izleme — araçlar: Kling 3.0 Turbo, Higgsfield API, polling
- 14. adım — Çıkan videoyu izleme, indirme ve billing'de 0,31 dolar maliyeti kontrol etme — araçlar: Higgsfield API
- 15. adım — Excalidraw ile iş akışını/sistemi anlatan şema çizme — araçlar: Excalidraw
- 16. adım — İş modeli fikirleri ve MiniMax Hailuo 2.3 indirimini anlatma — araçlar: MiniMax Hailuo 2.3, Higgsfield API
## Promptlar
- Fotoğraftan video demo uygulamasını Codex'e yaptırmak — Bu klasörde Higgsfield API ile fotoğrafı kısa videoya çeviren çalışan demo uygulama yap. Next.js App Router, TypeScript, Tailwind. Yerelde çalışsın; hesap, ödeme, veritabanı olmasın. Önce docs kaynaklarını oku, modelin dokümanını kullan, desteklenmeyen parametre uydurma. Arayüz: Türkçe, sade, beyaz, kırmızı vurgu; fotoğraf yükleme (10 MB sınır), hareket tarifi, 'Videoyu oluştur' butonu, durum, yan yana sonuç, indirme. Polling kullan, sahte yanıt yok, butona basmadan ücretli üretim başlatma, maliyeti ucuz ayarlarla README'de belirt.
- Uygulamada üretilecek videonun hareket tarifi — Kamera kişiye doğru yaklaşır ve kişi göz kırpar.
ikinci göz KAPALI: --ikinci-goz yok
