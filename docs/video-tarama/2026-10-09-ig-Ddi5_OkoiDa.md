# Your vibe-coded app can cost you $100,000 with zero users
## Künye
Your vibe-coded app can cost you $100,000 with zero users · adilet.fndr · süre: 1:00 · ? · https://www.instagram.com/reel/Ddi5_OkoiDa/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-13 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 14935 tk · claude-haiku-5-5: claude-haiku-5-5 · 43931 tk
## Özet
Kısa reel: vibe-coding ile yapılmış bir uygulamanın başına gelebilecek beş büyük riski anlatıyor. (1) Netlify'da statik siteye DDoS ile gelen yüksek bant genişliği faturası ($104.500), (2) klavye erişimi ve alt metin eksikliği nedeniyle ADA erişilebilirlik davaları, (3) Supabase'de Claude'un oluşturduğu tablolarda RLS kapalıyken herkese açık anahtarla kullanıcı tablosunun okunması, (4) izinsiz SMS (TCPA) için mesaj başına $500, (5) kendini çağıran özyinelemeli bir crawl fonksiyonunun Google Cloud'da $72.000 fatura yaratması. Çözüm olarak video linkini Claude'a verip düzeltmesini istemek öneriliyor; sonda bir prompt'un yorumla gönderileceği söyleniyor.
## Bölümler
- 0:00 Giriş: statik landing page ve Netlify DDoS faturası
- 0:20 Erişilebilirlik (ADA) davası
- 0:26 Supabase RLS kapalı: kullanıcı tablosu açıkta
- 0:37 İzinsiz SMS: kişi başı $500
- 0:46 Özyinelemeli crawl fonksiyonu ve Google Cloud faturası
- 0:54 Çözüm: linki Claude'a gönder, 5 açık
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Netlify | yok | plugin | yok | Statik site barındırma; bant genişliği başına faturalandırma riski örneği, netlify.toml ile limit önerisi. | 0:05 | Ekran metni 'Deploy to Netlify', 'Bandwidth - Starter'; konuşmada 'Netlify bills per gigabyte'. (karede: kanıttan) Ekran metni 'Deploy to Netlify', 'Bandwidth - Starter'; konuşmada 'Netlify bills per gigabyte'. |
| Supabase | yok | CLI | yok | Veritabanı servisi; RLS kapalı tablolar ve public anahtarla REST erişimi gösterilir. | 0:26 | Karede yourapp · Free, users/profiles/waitlist/orders tabloları 'RLS off'. (karede: kanıttan) Karede yourapp · Free, users/profiles/waitlist/orders tabloları 'RLS off'. |
| Claude | yok | CLI | yok | Kodu/tabloları üreten ve düzeltmeyi yapacak ana yapay zekâ aracı. | 0:54 | Ekran metni 'Reply to Claude...'; konuşmada 'ask it to fix everything'. (karede: kanıttan) Ekran metni 'Reply to Claude...'; konuşmada 'ask it to fix everything'. |
| Row Level Security | yok | teknik | yok | Supabase'de satır bazlı erişim kontrolü; kapalıyken tablolar herkese açık okunur. | 0:26 | Karede tabloların yanında 'RLS off' etiketleri. (karede: kanıttan) Karede tabloların yanında 'RLS off' etiketleri. |
| curl | yok | CLI | yok | Supabase REST uç noktasına apikey başlığıyla istek atıp kullanıcıları listeleme. | 0:31 | Terminalde '$ curl https://xyz.supabase.co/rest/v1/users?select=* -H "apikey: ...'. (karede: kanıttan) Terminalde '$ curl https://xyz.supabase.co/rest/v1/users?select=* -H "apikey: ...'. |
| Google Cloud | yok | CLI | yok | Bütçe uyarılarının faturayı durdurmadığı örnek bulut servisi. | 0:52 | Ekran metni 'Google Cloud - Budget alert', '1,000 instances · 116 billion reads'. (karede: kanıttan) Ekran metni 'Google Cloud - Budget alert', '1,000 instances · 116 billion reads'. |
| netlify.toml | yok | teknik | yok | Bant genişliği sınırı ve rate limit önerisi için yapılandırma dosyası. | 0:56 | Ekran metni 'netlify.toml - bandwidth cap + rate limit'. (karede: kanıttan) Ekran metni 'netlify.toml - bandwidth cap + rate limit'. |
| JavaScript | yok | teknik | yok | Public anahtarın JS içinde göründüğü ve crawl.js fonksiyonunun yazıldığı dil. | 0:00 | 'public key that's already in your JavaScript'; ekranda crawl.js. |
| Beş güvenlik/maliyet açığını tek seferde düzeltme | yok | prompt | yok | Videonun bağlantısını Claude'a verip beş açığın (erişilebilirlik, RLS, SMS izni, bütçe/bant genişliği limiti, özyineleme) tümünü düzeltmesini istemek; netlify.toml'a bant genişliği sınırı ve rate limit, 3 görsele alt metin, klavye odağı eklenir. | 0:54 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Hero bölümü ve çağrı butonu (hero section, CTA button) | Sahte 'yourapp' landing page: 'Ship your idea this weekend.' başlığı, 'Join the waitlist' butonu. (karede: Tarayıcı penceresinde yourapp.com, Product/Pricing/Docs gezinme çubuğu, büyük başlık, beyaz Join the waitlist butonu, sağda üç görsel yer tutucusu.) | 0:00 | kare |
| Gezinme çubuğu (navbar) | Logo ile Product, Pricing, Docs bağlantıları. (karede: Pencere üstünde yourapp logosu ve Product Pricing Docs.) | 0:00 | kare |
| Görsel yer tutucu ızgarası (image placeholder grid) | Sağda bir büyük, iki küçük görsel yer tutucu. (karede: Sağ tarafta dağ ikonlu gri üç kutu.) | 0:00 | kare |
| Bulanıklaşan kinetik başlık metni (blur text reveal) | Üstte 'If you've vibe-coded' yazısında kelime vurgusu ve bulanıklık geçişi. (karede: Üstte 'If you've' gri, 'vibe-coded' bulanık beyaz.) | 0:00 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl https://xyz.supabase.co/rest/v1/users?select=* -H "apikey: <anahtar>" | Supabase REST uç noktasından users tablosunu public anahtarla çeker; RLS kapalıysa tüm satırları döndürür (anahtar değeri yazılmadı). (karede: Alt kısımdaki 'terminal · anyone's' penceresinde curl komutu ve altında JSON satırları.) | 0:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Statik bir sitenin Netlify faturası DDoS sonrası $104.500'e ulaştı. | 0:00 | sayısal |
| Geçen yıl 5.000'den fazla erişilebilirlik davası açıldı; çoğu küçük şirketlere karşı. | 0:12 | sayısal |
| Vibe-coded uygulamaların onda birinde RLS kapalı açığı var. | 0:35 | sayısal |
| Yazılı izin olmadan atılan SMS başına federal yasada $500; 10.000 SMS $5 milyon eder. | 0:44 | sayısal |
| Bütçe uyarıları harcamayı durdurmaz; bir startup $72.000 fatura ile uyandı. | 0:53 | sayısal |
| Videonun linkini Claude'a gönderip her şeyi düzelttirmek önerilir. | 0:54 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | vibe coding | aday değil: genel kavram | If you've vibe-coded an app |
| kare 0:00 | yourapp.com landing page | aday değil: konu dışı | Ship your idea this weekend. |
| konuşma 0:00 | DDoS | aday değil: genel kavram | until someone hits it with DDoS attack |
| konuşma 0:00 | Netlify | Netlify | Netlify bills per gigabyte |
| kare 0:20 | ADA davası belgesi | aday değil: genel kavram | Plaintiff brings this action under Title III |
| konuşma 0:12 | alt text / klavye erişilebilirliği | aday değil: genel kavram | no image has alt text |
| kare 0:32 | Supabase | Supabase | yourapp · Free, tables by Claude |
| kare 0:26 | RLS off | Row Level Security | users RLS off |
| kare 0:31 | curl isteği | curl | $ curl https://xyz.supabase.co/rest/v1/users |
| konuşma 0:40 | SMS/TCPA | aday değil: genel kavram | $500 per text under federal law |
| kare 0:46 | crawl.js | JavaScript | export async function crawl(url) |
| kare 0:52 | Google Cloud budget alert | Google Cloud | Google Cloud - Budget alert |
| kare 0:54 | Claude sohbet kutusu | Claude | Reply to Claude... |
| kare 0:56 | netlify.toml | netlify.toml | netlify.toml - bandwidth cap + rate limit |
| kare 0:57 | Adilet Instagram profili | aday değil: konu dışı | Adilet, AI Education for Everyone |
| açıklama | PROMPT yorum çağrısı | aday değil: sponsor/reklam | Comment “PROMPT” and I’ll send you |
## Kareden okunanlar
- 0:00: yourapp.com sayfası: 'Ship your idea this weekend.', Join the waitlist, Product Pricing Docs; üstte 'If you've vibe-coded'.
- 0:20: Mahkeme belgesi: United States District Court, Eastern District of New York, Jane Doe v. YOURAPP, INC., class action complaint, ADA Title III.
- 0:32: yourapp Free · 'tables by Claude'; users, profiles, waitlist, orders RLS off; terminalde curl ile supabase REST isteği ve e-posta listesi.
## Belirsizlikler
- Yorum girişsiz alınamadı; 'PROMPT' yorumuyla gönderilecek prompt içeriği bilinmiyor.
- Sözlük eşleşmeleri (Codex, Teable, Slack, Express, claude-api, Inter) bulanık/ilgisiz görünüyor; videoda kullanıldıkları doğrulanmadı.
- Konuşma dili belirtilmemiş; altyazı İngilizce görünüyor.
- Davadaki 'alt text/keyboard' ve 2025 ADA istatistiği (%64) kaynağı belirtilmiyor.
- Ekrandaki 'Superbase' yazımı konuşma transkriptinde; doğru ad Supabase.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| yourapp.com | 0:00 | ekran | hayır |
| https://xyz.supabase.co/rest/v1/users?select=* | 0:31 | ekran | evet |
| gmail.com | 0:32 | ekran | hayır |
| outlook.com | 0:32 | ekran | hayır |
| proton.me | 0:32 | ekran | hayır |
| icloud.com | 0:32 | ekran | hayır |
| yahoo.com | 0:32 | ekran | hayır |
| hey.com | 0:34 | ekran | hayır |
## İş akışı
- 1. adım — Statik landing page'i Netlify'a yayınlama ve bant genişliği faturası riskini gösterme — araçlar: Netlify
- 2. adım — Erişilebilirlik sorunlarını (klavye gezinmesi, alt metin eksikliği) listeleme — araçlar: yok
- 3. adım — Supabase'de users, profiles, waitlist, orders tablolarında RLS kapalı olduğunu gösterme — araçlar: Supabase, Claude
- 4. adım — Public anahtarla REST uç noktasından users tablosunu curl ile çekme — araçlar: curl, Supabase
- 5. adım — Bekleme listesine 10.000 alıcıya izinsiz SMS gönderilmesinin riskini anlatma — araçlar: yok
- 6. adım — Kendini çağıran crawl fonksiyonunu ve artan fatura bildirimlerini gösterme — araçlar: Claude
- 7. adım — Google Cloud bütçe uyarılarının harcamayı durdurmadığını gösterme — araçlar: Google Cloud
- 8. adım — Videonun bağlantısını Claude'a gönderip sorunların düzeltilmesini isteme — araçlar: Claude
- 9. adım — Düzeltme maddelerini sohbette sıralama: alt metin, klavye odağı, netlify.toml'a bant genişliği ve hız sınırı — araçlar: Claude, Netlify
## Promptlar
- Beş güvenlik/maliyet açığını tek seferde düzeltme — Videonun bağlantısını Claude'a verip beş açığın (erişilebilirlik, RLS, SMS izni, bütçe/bant genişliği limiti, özyineleme) tümünü düzeltmesini istemek; netlify.toml'a bant genişliği sınırı ve rate limit, 3 görsele alt metin, klavye odağı eklenir.
ikinci göz KAPALI: --ikinci-goz yok
