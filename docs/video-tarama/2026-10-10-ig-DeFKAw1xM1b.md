# PROMPT YORUMLARDA
## Künye
PROMPT YORUMLARDA · berkayabay.ai · süre: 0:55 · ? · https://www.instagram.com/reel/DeFKAw1xM1b/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 34264 tk · claude-haiku-5-5: claude-haiku-5-5 · 92550 tk
## Özet
55 saniyelik Türkçe Instagram reel'i: Supabase kullanıcılarına, bir güvenlik araştırmasında açık bulunan veritabanlarından yola çıkarak 5 güvenlik kontrolünü anlatıyor. Bunlar: RLS kapalı tablo (Security Advisor), 'herkes okuyabilir' kuralı (using true), tarayıcıda duran secret key, herkese açık depolama klasörü ve düz metin şifre (Supabase Auth önerisi). Kontrol promptu yorumlarda; yorumlara girişsiz erişilemedi. Konuşmada 300.000 site/16.000 uygulama deniyor, karede ise 141.261 site ve 16.326 açık yazıyor.
## Bölümler
- 0:00 Giriş: 16.000 uygulamanın veritabanı açık
- 0:09 Okunabilen veri örneği (anon isteği)
- 0:16 1) RLS ve Security Advisor
- 0:21 2) Herkes okuyabilir kuralı
- 0:29 3) Publishable ve secret key
- 0:39 4) Herkese açık dosya klasörü
- 0:45 5) Düz metin şifreler ve Supabase Auth
- 0:51 Kapanış: kontrol promptu yorumlarda
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Supabase | yok | teknik | yok | Açık kaynak arka uç/veritabanı servisi; videonun konusu, panel ekranları gösteriliyor. | 0:16 | Panel adresi supabase.com/dashboard / advisors / security (karede: Security Advisor sayfası, Supabase panel adresi) |
| Security Advisor | yok | teknik | yok | Supabase panelinde RLS kapalı tabloları uyaran güvenlik danışmanı. | 0:16 | Panel → Security Advisor; Errors 1, Warnings 1, Info 1 (karede: Security Advisor başlığı, Errors/Warnings/Info sekmeleri, Advisors menüsü) |
| RLS | yok | teknik | yok | Satır bazlı erişim güvenliği (Row Level Security); tablo kurallarıyla erişimi sınırlar. | 0:16 | Birincisi satır güvenliği yani RLS. |
| auth.uid() | yok | teknik | yok | Kuralda kullanıcının yalnız kendi verisini görmesini sağlayan fonksiyon. | 0:26 | Ekran metninde auth.uid() görünüyor (karede: Kare gönderilmedi; OCR metni auth.uid()) |
| Publishable key | yok | teknik | yok | Tarayıcıda durabilen herkese açık Supabase anahtarı. | 0:29 | Publishable key · TARAYICIDA OLABILIR (karede: Kare gönderilmedi; OCR metni) |
| Secret key | yok | teknik | yok | Tüm RLS kurallarını atlayan gizli anahtar; tarayıcıda olmamalı. | 0:30 | Secret key · BÜTÜN KURALLARI ATLAR (karede: Kare gönderilmedi; OCR metni) |
| Supabase Storage | yok | teknik | yok | Dosya depolama; herkese açık klasör riski anlatılıyor. | 0:39 | supabase.com/dashboard / storage / files; public/demo-belgeler · kanıt: kare (karede: Kare gönderilmedi; OCR metni) |
| Supabase Auth | yok | teknik | yok | Şifreleri güvenle yöneten Supabase kimlik doğrulama sistemi. | 0:50 | SUPABASE AUTH · Supabase Auth kullan (karede: Kare gönderilmedi; OCR metni) |
| JavaScript | yok | teknik | yok | app.js içinde createClient ile secret key'in tarayıcıya sızması örneği. | 0:33 | APP.JS · TARAYICIYA; const createClient( (karede: Kare gönderilmedi; OCR metni) |
| UpGuard | yok | teknik | yok | Araştırmanın kaynağı olarak açıklamada anılan güvenlik firması. | açıklama | Kaynak: UpGuard araştırması, 25 Eylül 2026 |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| alter policy "herkes okuyabilir" on public.demo_siparisler using ( true | Örnek SQL: kural herkese okuma izni veriyor (using true), yanlış örnek olarak gösteriliyor. (karede: Kare gönderilmedi; OCR metni) | 0:21 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 300.000 site tarandı, bunların 16.000 adedinde isim, telefon, şifre okunabildi. | 0:00 | sayısal |
| Karede 141.261 site tarandı ve 16.326 açık yazıyor; konuşmadaki 300.000 ile çelişiyor. | 0:05 | sayısal |
| RLS açıkken kuralda 'herkes okuyabilir' (using true) varsa hiçbir şey değişmemiş olur. | 0:21 | özellik |
| Secret key tüm kuralları atlar; tarayıcı kodunda durması anahtarı kapıya atmak gibidir. | 0:32 | özellik |
| Şifreyi kendi tabloda tutma, Supabase Auth kullan. | 0:48 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Supabase | Supabase | Supabase kullanıyorsan bu 5 şeye dikkat et |
| kare 0:05 | Araştırma haberi, 300.000 site / 16.326 açık | aday değil: genel kavram | SON DAKİKA, 300.000 site tarandı |
| kare 0:10 | GET /rest/v1/musteriler anon isteği | Supabase | anon isteği · giriş yok |
| konuşma 0:16 | RLS | RLS | Birincisi satır güvenliği yani RLS |
| kare 0:16 | Security Advisor | Security Advisor | Panel → Security Advisor |
| kare 0:21 | Policy 'herkes okuyabilir', using true | RLS | alter policy herkes okuyabilir |
| kare 0:26 | auth.uid() | auth.uid() | auth.uid() |
| kare 0:29 | Publishable key | Publishable key | Publishable key · TARAYICIDA OLABILIR |
| kare 0:30 | Secret key | Secret key | Secret key · sb_secret_ |
| kare 0:33 | app.js, createClient | JavaScript | APP.JS · TARAYICIYA; const createClient( |
| kare 0:35 | Sağ tık → Kaynağı görüntüle | aday değil: genel kavram | Sağ tık → Kaynağı görüntüle ile okunur |
| kare 0:39 | Storage herkese açık klasör | Supabase Storage | supabase.com/dashboard / storage / files |
| kare 0:45 | public.users düz metin şifre | aday değil: başka adayın parçası (Supabase) | Şifreler açık metin |
| kare 0:50 | Supabase Auth | Supabase Auth | Supabase Auth kullan |
| açıklama | UpGuard araştırması | UpGuard | Kaynak: UpGuard araştırması, 25 Eylül 2026 |
| açıklama | Prompt yorumlarda | aday değil: konu dışı | PROMPT YORUMLARDA |
| yorum | Yorumlar | aday değil: konu dışı | yorum: girişsiz alınamıyor |
## Kareden okunanlar
- 0:05: Başlık '141.261 site tarandı'; monitörde '300.000 site tarandı, 16.326'sı açık bulundu'; Supabase logosu.
- 0:10: GET /rest/v1/musteriler, anon isteği · giriş yok; ad, telefon, şifre tablosu (örnek veriler).
- 0:16: 01 · RLS, Panel → Security Advisor; supabase.com/dashboard / advisors / security; Errors 1, Warnings 1, Info 1.
## Belirsizlikler
- Yorumlara girişsiz erişilemedi; kontrol promptunun metni bilinmiyor.
- Konuşmada 300.000 site/16.000 uygulama, karede 141.261 site/16.326 açık deniyor; tutarsızlık var.
- Sözlük eşleşmeleri Ollama ve Hermes Agent videoda geçmiyor (ses hatası); aday alınmadı.
- Konuşmada 'Üçüncüsü' iki kez söyleniyor (dördüncü kastediliyor); 'SuboBase' Supabase'in yanlış yazımı.
- Panel menüsündeki Table Editor, SQL Editor, Database gibi öğeler yalnız menüde görünüyor; kullanılmadı.
- Açıklamadaki UpGuard kaynağı videoda doğrulanamadı.
- Yalnız 3 kare gönderildi; 0:16 sonrası bilgiler OCR metninden alındı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| supabase.com/dashboard | 0:16 | ekran | evet |
| supabase.com/dashboard/advisors/security | 0:16 | ekran | evet |
| supabase.com/dashboard/auth/policies | 0:21 | ekran | evet |
| supabase.com/dashboard/settings/api-keys | 0:30 | ekran | evet |
| siten.com | 0:33 | ekran | hayır |
| xyz.supabase.co | 0:33 | ekran | hayır |
| supabase.com/dashboard/storage/files | 0:39 | ekran | evet |
| example.com | 0:45 | ekran | hayır |
| supabase.com/dashboard/editor/users | 0:45 | ekran | evet |
| supabase.com/dashboard/auth/users | 0:50 | ekran | evet |
| view-source:siten.com/app.js | 0:33 | ekran | hayır |
| storage/v1/object/public/demo-belgeler/ | 0:39 | ekran | evet |
## İş akışı
- 1. adım — Reel girişinde araştırma haberi ve açık veritabanı sayıları gösterilir — araçlar: Supabase
- 2. adım — Anon isteğiyle girişsiz okunan örnek müşteri verisi gösterilir — araçlar: Supabase
- 3. adım — Panelde Security Advisor açılıp RLS kapalı tablo uyarısı kontrol edilir — araçlar: Supabase, Security Advisor, RLS
- 4. adım — RLS açık olsa da 'herkes okuyabilir' kuralı (using true) incelenir, auth.uid() ile düzeltme önerilir — araçlar: RLS, auth.uid()
- 5. adım — API anahtarları ayrılır: publishable key tarayıcıda olabilir, secret key olamaz — araçlar: Publishable key, Secret key
- 6. adım — app.js kaynağında secret key sızıntısı görüntüle-kaynak ile gösterilir — araçlar: JavaScript
- 7. adım — Herkese açık depolama klasöründeki dosyaların bağlantıyla açıldığı gösterilir — araçlar: Supabase Storage
- 8. adım — Düz metin şifre tablosu gösterilip Supabase Auth kullanımı önerilir — araçlar: Supabase Auth
- 9. adım — Kontrol promptunun yorumlarda olduğu söylenip takip çağrısı yapılır — araçlar: yok
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
