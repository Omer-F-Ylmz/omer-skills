# Yorumlara "Vibe"  yaz, seninle de rehberi paylaşayım. 🤝
## Künye
Yorumlara "Vibe"  yaz, seninle de rehberi paylaşayım. 🤝 · yasin.arsal · süre: 0:58 · ? · https://www.instagram.com/reel/DZs19rMRKMu/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 31905 tk · claude-haiku-5-5: claude-haiku-5-5 · 32037 tk
## Özet
Yasin Arsal, vibe coding ile yapılan uygulamalardaki üç güvenlik açığını anlatıyor: frontend'de açıkta kalan API anahtarları, rate limit eksikliği ve girdi doğrulaması yokluğu (SQL injection). Üçünü birden çözen bir prompt hazırladığını söylüyor. Prompt Cursor, VS Code veya başka bir yapay zekâ kodlama asistanına yapıştırılabiliyor. Rehber için yorumlara 'vibe' yazılması isteniyor. Açıklamada ek kurallar sayılıyor: .env, CORS, güvenlik header'ları, bcrypt, Zod/Pydantic, CLAUDE.md ve .cursorrules.
## Bölümler
- 0:00 Giriş: üç güvenlik açığı
- 0:06 Birincisi: açıkta kalan anahtarlar
- 0:25 İkincisi: rate limit olmaması
- 0:33 Üçüncüsü: girdi doğrulaması ve SQL injection
- 0:45 Çözüm promptu ve rehber çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Cursor | yok | CLI | yok | Güvenlik promptunun yapıştırılabileceği yapay zekâ kodlama aracı. | 0:45 | Cursor veya VS Code gibi araçlara ... yapıştırmanız yeterli |
| VS Code | yok | CLI | yok | Promptun yapıştırılabileceği editör olarak anıldı. | 0:45 | Cursor veya VS Code gibi araçlara |
| DevTools | yok | teknik | yok | Tarayıcı geliştirici araçlarıyla frontend'deki anahtarların kopyalanabildiği gösterildi. | 0:18 | yani isteyen herkes DevTools'u açıp (karede: Firefox DevTools Debugger paneli, breakpoint sağ tık menüsü; altyazı 'yani isteyen herkes DevTools'u açıp') |
| OpenAI | yok | teknik | yok | Açıkta kalabilecek API anahtarı örneği. | 0:12 | OpenAI anahtarınız, veritabanı bağlantı adresleriniz |
| Stripe | yok | teknik | yok | Açıkta kalabilecek ödeme anahtarı örneği. | 0:15 | Ekranda STRIPE_PUBLISHABLE_KEY ve STRIPE_SECRET_KEY satırları görünüyor (karede: OCR: STRIPE_PUBLISHABLE_KEY ve STRIPE_SECRET_KEY satırları (değerler yazılmadı)) |
| Rate limiting | yok | teknik | yok | İstek sınırlama ile aşırı istek ve DoS'a karşı koruma. | 0:26 | Ekranda RATE LIMITING ve DoS attack yazıyor (karede: OCR: 'RATE LIMITING', 'DoS attack', 'rate limits') |
| Input validation | yok | teknik | yok | Kullanıcı girdisini sunucuda doğrulama. | 0:33 | Ekranda 'input validation' yazıyor · kanıt: kare (karede: OCR: 'input' ve 'validation') |
| SQL INJECTION | yok | teknik | yok | Birleştirilmiş SQL sorgusuyla enjeksiyon saldırısı örneği. | 0:42 | Başlık SQL INJECTION; OR '1'='1' sorgusu gösteriliyor (karede: Siyah ekranda 'SQL INJECTION' başlığı, john/password123 ile SELECT sorgusu ve ' OR '1'='1' vurgusu) |
| .env | yok | ipucu | yok | Secret'ların yalnızca .env dosyasında tutulması, .gitignore'a eklenmesi. | açıklama | Secret'lar sadece .env'de yaşar. |
| Zod | yok | teknik | yok | Sunucu tarafı girdi doğrulama kütüphanesi. | açıklama | Doğrulamayı sunucuda yap, Zod ya da Pydantic ile. |
| Pydantic | yok | teknik | yok | Python tarafında sunucu doğrulama kütüphanesi. | açıklama | Zod ya da Pydantic ile |
| bcrypt | yok | teknik | yok | Parolaları hashlemek için önerilen algoritma. | açıklama | parolaları bcrypt ile hashle |
| helmet | yok | teknik | yok | Node'da güvenlik header'larını tek satırda ekleyen paket. | açıklama | Node'da helmet bunu tek satırda halleder. |
| CLAUDE.md | yok | ipucu | yok | Güvenlik kurallarını projenin köküne koyarak AI'a uygulatma. | açıklama | CLAUDE.md ya da .cursorrules olarak projenin köküne koy |
| .cursorrules | yok | ipucu | yok | Cursor için kural dosyası. | açıklama | CLAUDE.md ya da .cursorrules olarak projenin köküne koy |
| CORS | yok | teknik | yok | Production'da yıldız yerine yalnız bilinen origin'lere izin verme. | açıklama | Production'da CORS'u yıldız ile açık bırakma. |
| CSP, HSTS, X-Frame-Options | yok | teknik | yok | Eklenmesi önerilen güvenlik header'ları. | açıklama | Güvenlik header'larını ekle: CSP, HSTS, X-Frame-Options. |
| UUID | yok | teknik | yok | Yüklenen dosyayı UUID ile yeniden adlandırma. | açıklama | dosyayı UUID ile yeniden adlandır |
| Prompt injection | yok | teknik | yok | LLM'e ham girdi göndermenin riski. | açıklama | prompt injection gerçek bir tehdit |
| React | yok | teknik | yok | Gösterilen demo uygulamanın arayüz kütüphanesi. | 0:18 | Babel + TypeScript + React (karede: Sekme başlığında 'Babel + TypeScript + React' yazıyor; kaynak ağacında react-dom.production.min.js dosyası görünüyor.) |
| TypeScript | yok | teknik | yok | Gösterilen demo uygulamanın dili. | 0:18 | Babel + TypeScript + React (karede: Sekme başlığında 'Babel + TypeScript + React' yazıyor; kaynak ağacında index.tsx dosyası açık.) |
| Babel | yok | teknik | yok | Gösterilen demo projenin derleyici aracı. | 0:18 | Babel + TypeScript + React (karede: Sekme başlığında 'Babel + TypeScript + React' yazıyor.) |
| pnpm | yok | teknik | yok | Paket yöneticisi; yalnızca kaynak ağacı yolunda görünüyor. | 0:18 | rbd/pnpm-vol (OCR, kısmi) (karede: Kaynak ağacında dosya yolunda 'pnpm' ifadesi görünüyor; tam yol okunamıyor.) |
| Vibe coding uygulamalarında güvenlik kurallarını AI'a dayatmak | yok | prompt | yok | Üç güvenlik açığını (açıkta kalan anahtarlar, rate limit, girdi doğrulama) ve daha fazlasını çözecek kurallarla kod üret: secret'lar yalnız .env'de, public endpoint'lerde rate limit (429), sunucuda doğrulama, parametreli sorgu, kısıtlı CORS, güvenlik header'ları, genel hata mesajları, AI çağrılarında max_tokens ve kullanıcı bütçesi. | açıklama | kaynak: açıklama |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Vibe coding uygulamalarının çoğu API anahtarlarını yanlışlıkla doğrudan frontend'e gömüyor. | 0:09 | sayısal |
| Rate limit yoksa herkes backend'e sınırsız istek atıp API'yı çökertebilir. | 0:26 | özellik |
| Girdi doğrulaması yoksa veri enjekte edilip veritabanı bozulabilir; en tehlikeli açık budur. | 0:33 | özellik |
| Tek bir prompt üç açığı ve daha fazlasını çözüyor; Cursor, VS Code veya başka asistana yapıştırılabilir. | 0:45 | öneri |
| Kurallar CLAUDE.md veya .cursorrules olarak proje köküne konursa AI her seferinde uygular. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Vibe coding / üç güvenlik açığı | aday değil: genel kavram | Her Vibe Coding'de yapılmış uygulamada bu 3 güvenlik açığı var |
| konuşma 0:12 | OpenAI anahtarı | OpenAI | OpenAI anahtarınız |
| kare 0:15 | Stripe anahtarları | Stripe | STRIPE_SECRET_KEY satırı ekranda |
| kare 0:13 | Veritabanı bağlantı adresi (Database URL) | aday değil: genel kavram | Ekranda 'Datebase URL' |
| kare 0:18 | DevTools | DevTools | Altyazı: DevTools'u açıp |
| kare 0:18 | Babel + TypeScript + React / Webpack / index.tsx | aday değil: başka adayın parçası (DevTools) | DevTools örnek sayfası içeriği |
| kare 0:20 | mockifyPro sayfası | aday değil: başka adayın parçası (DevTools) | Network paneli örnek sayfası |
| kare 0:26 | Rate limiting / DoS | Rate limiting | RATE LIMITING |
| kare 0:33 | Input validation | Input validation | input validation |
| kare 0:39 | Java kod görüntüsü (HttpURLConnection) | aday değil: başka adayın parçası (Input validation) | Fon görüntüsü, araç olarak anlatılmıyor |
| kare 0:42 | SQL injection | SQL INJECTION | SQL INJECTION başlığı |
| konuşma 0:45 | Cursor | Cursor | Cursor veya VS Code |
| konuşma 0:45 | VS Code | VS Code | Cursor veya VS Code |
| konuşma 0:45 | Yapay zekâ kodlama asistanı | aday değil: genel kavram | herhangi bir yapay zeka kodlama asistanına |
| açıklama | GitHub | aday değil: konu dışı | API key'in GitHub'da açıkta kaldığını |
| açıklama | .env | .env | Secret'lar sadece .env'de yaşar. |
| açıklama | .gitignore | aday değil: başka adayın parçası (.env) | .gitignore'a .env eklemeyi unutma |
| açıklama | Zod | Zod | Zod ya da Pydantic ile |
| açıklama | Pydantic | Pydantic | Zod ya da Pydantic ile |
| açıklama | bcrypt | bcrypt | parolaları bcrypt ile hashle |
| açıklama | ORM / parametreli sorgu | aday değil: başka adayın parçası (SQL INJECTION) | ORM ya da parametreli sorgu kullan |
| açıklama | CORS | CORS | Production'da CORS'u yıldız ile açık bırakma |
| açıklama | CSP, HSTS, X-Frame-Options | CSP, HSTS, X-Frame-Options | CSP, HSTS, X-Frame-Options |
| açıklama | helmet | helmet | Node'da helmet bunu tek satırda halleder |
| açıklama | UUID | UUID | dosyayı UUID ile yeniden adlandır |
| açıklama | max_tokens / token bütçesi | aday değil: genel kavram | her çağrıya max_tokens limiti koy |
| açıklama | Prompt injection | Prompt injection | prompt injection gerçek bir tehdit |
| açıklama | CLAUDE.md | CLAUDE.md | CLAUDE.md ya da .cursorrules |
| açıklama | .cursorrules | .cursorrules | CLAUDE.md ya da .cursorrules |
| açıklama | Yorumlara 'Vibe' yaz rehber çağrısı | aday değil: sponsor/reklam | Yorumlara "Vibe" yaz, seninle de rehberi paylaşayım |
| yorum | Yorumlar | aday değil: konu dışı | yorum: girişsiz alınamıyor |
## Kareden okunanlar
- 0:18: Firefox DevTools Debugger: breakpoint menüsü, index.tsx, 'Babel + TypeScript + React' sekmesi; altyazı 'yani isteyen herkes DevTools'u açıp'.
- 0:20: Tarayıcı Network paneli, mockifyPro sayfası, fetch istekleri ve engellenmiş istek; altyazı 'bunları kopyalayabilir'.
- 0:42: 'SQL INJECTION' başlığı, string birleştirmeli SELECT sorgusu ve OR '1'='1' vurgusu; altyazı 'hatta zararlı sorgular bile çalıştırabilirler'.
## Belirsizlikler
- Anlatılan promptun tam metni videoda gösterilmiyor; özet açıklamadaki kurallara dayanıyor.
- 0:18 karesindeki Babel + TypeScript + React sayfası yalnızca DevTools gösterimi için stok görüntü; videoda kullanılmadığı için aday yapılmadı.
- 0:20 karesindeki mockifyPro sayfası DevTools örneği; araç olarak kullanılmıyor.
- Ses 'Codex' ve 'Hermes Agent' gibi sözlük eşleşmeleri bulanık (code, herkes); gerçek değil sayıldı.
- Yorumlar girişsiz alınamadı.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https:/firefox-devtools-example-babel-typesc... | 0:18 | ekran | hayır |
## İş akışı
- yok
## Promptlar
- Vibe coding uygulamalarında güvenlik kurallarını AI'a dayatmak — Üç güvenlik açığını (açıkta kalan anahtarlar, rate limit, girdi doğrulama) ve daha fazlasını çözecek kurallarla kod üret: secret'lar yalnız .env'de, public endpoint'lerde rate limit (429), sunucuda doğrulama, parametreli sorgu, kısıtlı CORS, güvenlik header'ları, genel hata mesajları, AI çağrılarında max_tokens ve kullanıcı bütçesi.
