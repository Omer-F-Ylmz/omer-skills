# Lovable Ücretsiz Oldu! Takipçim İçin Kod Yazmadan Sıfırdan Uygulama Geliştirdim - Lovable & Supabase
## Künye
Lovable Ücretsiz Oldu! Takipçim İçin Kod Yazmadan Sıfırdan Uygulama Geliştirdim - Lovable & Supabase · Ömer Göçmen | Yapay Zeka & Otomasyon · süre: 21:19 · tr-orig · https://youtu.be/ARsCKGoKut0 · şema 2
motor: parti 2026-10-10-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (56)
kareler: girdi ≤40000 jeton için 60→56
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 103474 tk
## Özet
Ömer Göçmen, Lovable'ın ücretsiz hafta sonunda, engelliler için bir forum sitesini (EngelDestek Forum) hiç kod yazmadan, yapay zekâ promptlarıyla ve Supabase arka ucuyla geliştirdiğini anlatıyor. Video; Lovable'da proje açma ve Supabase bağlama, Supabase Auth ve güvenlik ayarları, takip sistemi, bildirimler, takip edilenlerin gönderileri ve yayınlama adımlarını gösteriyor. Bildirim sisteminde RLS (Row Level Security) kaynaklı hata çıkıyor, Lovable'a verilen düzeltme promptlarıyla çözülüyor. Video ayrıca Supabase ücretsiz sürüm limitlerine ve ücretsiz hesap kısıtlarına değiniyor.
## Bölümler
- 0:00 Giriş ve fikrin kaynağı (ücretsiz Lovable hafta sonu)
- 1:00 Uygulama turu: giriş, kayıt, ana sayfa, gönderiler
- 2:01 Gönderi oluşturma, etiketler, haberler, skor tablosu
- 4:03 Kullanıcı detayı, gönderi düzenleme, profil
- 5:05 Lovable'da yeni proje ve Supabase bağlantısı
- 6:06 Supabase organizasyon ve proje yapısı, ücretsiz sürüm limiti
- 7:06 Supabase Authentication: kullanıcılar, e-posta şablonları, rate limit, politikalar
- 8:07 URL yapılandırması ve Attack Protection (Turnstile)
- 9:08 Table Editor ve SQL Editor ile tablo işlemleri
- 11:10 Supabase'e yeni proje oluşturma ve free limit hatası
- 12:12 Takip butonu ve takip tablosu için promptlar
- 14:13 Follows ve notifications tablolarının oluşması
- 15:15 Bildirim paneli ve okundu işaretleme
- 17:18 Takip edilenlerin gönderileri ve düzeltmeler
- 18:19 Yayınlama (Publish) ve gönderi bildirimi testi
- 19:19 Bildirim hatası ve RLS politikası düzeltmesi
- 20:21 Bildirimin çalışması ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Lovable | yok | teknik | yok | Promptla web uygulaması üreten, Supabase bağlantısı kurabilen yapay zekâ destekli geliştirme platformu. | 0:00 | Lovable - Build for the web (karede: kanıttan) Lovable - Build for the web |
| Supabase | yok | teknik | yok | Auth, veritabanı (PostgreSQL), storage ve edge functions sunan açık kaynaklı backend platformu. | 0:00 | Lovable'da entegre olabilen ve bize backend görevi sunabilen Zupa Base'den |
| PostgreSQL | yok | teknik | yok | Supabase'in altında çalışan ilişkisel veritabanı. | 6:26 | Listen to your PostgreSQL database in realtime (karede: kanıttan) Listen to your PostgreSQL database in realtime |
| Anthropic | yok | teknik | yok | Lovable sohbetinde seçilen ana yapay zekâ modeli sağlayıcısı (Anthropic). | 5:36 | Anthropic model seçici, sohbet kutusu altında (karede: kanıttan) Anthropic model seçici, sohbet kutusu altında |
| Row Level Security | yok | teknik | yok | Supabase/PostgreSQL'de satır bazlı erişim politikalarını uygulayan güvenlik özelliği (RLS). | 7:36 | Row Level Security is enabled, but no policies exist (karede: kanıttan) Row Level Security is enabled, but no policies exist |
| Cloudflare Turnstile | yok | teknik | yok | Supabase Attack Protection içinde login uçlarını bottan koruyan captcha sağlayıcısı. | 8:20 | Turinstile by Cloudflare (captcha provider) · kanıt: kare (karede: Turinstile by Cloudflare (captcha provider)) |
| Notepad++ | yok | teknik | yok | Lovable'a verilecek promptların saklandığı metin editörü. | 12:10 | Yeni 11 - Notepad++, prompt satırları, length 712 lines 6 · kanıt: kare (karede: Yeni 11 - Notepad++, prompt satırları, length 712 lines 6) |
| Lovable'da yeni proje oluşturma (Supabase bağlantılı blog) | yok | prompt | yok | Blog sitesi oluştur; arka planda Supabase olsun ve blog yazıları oraya kaydedilsin. | 5:40 | kaynak: kare |
| Giriş ve kayıt ekranındaki görseli değiştirme | yok | prompt | yok | Login ve kayıt sayfasındaki resmi verilen görsel bağlantısıyla değiştir. | 0:11 | kaynak: kare |
| Yorum yazma yetkisini sadece oturum açmış kullanıcılara verme (RLS) | yok | prompt | yok | Yorumu sadece giriş yapan kullanıcılar atsın (yetkilendirme kuralı). | 8:07 | kaynak: altyazı |
| Takip butonu ekleme | yok | prompt | yok | Kullanıcı detay sayfasında kullanıcıyı takip et butonu olsun. | 12:10 | kaynak: kare |
| Takip bildirimi için tablo ve tetikleyici | yok | prompt | yok | Bildirimler adında tablo oluştur; bir kullanıcı başka biri tarafından takip edilince bildirim alsın (ad, soyad seni takip etmeye başladı). | 12:10 | kaynak: kare |
| Bildirim okundu durumu ve panel konumu | yok | prompt | yok | Bildirimler kısmında tıklanan bildirim okundu olarak güncellensin; tümünü okundu işaretle butonu üst sağ köşeden bildirim paneline erişilebilir olsun. | 12:10 | kaynak: kare |
| Takip edilen gönderiler filtresi | yok | prompt | yok | Ana sayfada takip ettiklerim kısmı olsun; tıklanınca yalnız takip edilen kişilerin gönderileri görünsün. | 12:10 | kaynak: kare |
| Yeni gönderi bildirimi ve yönlendirme | yok | prompt | yok | Bir kişi gönderi oluşturduğunda takip ettiği kişilere bildirim gitsin (ad, soyad gönderi yayınladı); bildirime tıklayınca gönderiye gidilsin. | 12:10 | kaynak: kare |
| Bildirim kaydının oluşmama hatasını düzeltme | yok | prompt | yok | Takip ettiğimde notifications tablosuna kayıt gelmiyor; kontrol et ve doğru çalışsın. | 20:06 | kaynak: kare |
| Test sonucu hatası bildirimi | yok | prompt | yok | Takip edilen kişi gönderi paylaştığında bildirim gelmiyor; hata olarak bildirme. | 19:19 | kaynak: altyazı |
## Açıklama bağlantıları
- https://vibrant-threads-collective.lovable.app — Uygulamanın demo sitesi (EngelDestek Forum) · aday: hayır · Demo/referans sayfası; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://www.youtube.com/channel/UCaRvIDBtMJ687xSLPxLOS2Q/join — Kanal üyelik (Join) sayfası · aday: hayır · Ücretli kanal üyeliği; araç değil. · sınıf: diğer · erişilemez: ücretli üyelik gerekli
- https://youtu.be/nudCt2F7Tug — Yazarın başka bir YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://youtu.be/OPBIumlvDQo — Yazarın başka bir YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://youtu.be/e1DzQAh4Xw0 — Yazarın başka bir YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://youtu.be/BjqaV253lNI — Yazarın başka bir YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://youtu.be/gmYYHjlOJTI — Yazarın başka bir YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://www.youtube.com/watch?v=wlyl_yv7nSk&lc=Ugz7N1NOe3aQdwU6rwJ4AaABAg&ab_channel=%C3%96merG%C3%B6%C3%A7men — Yorum kimliğine bağlı YouTube videosu · aday: hayır · Yorum/kanal içeriği; araç değil. · sınıf: diğer
- https://www.youtube.com/watch?v=uKoi9uQLdCs&ab_channel=%C3%96merG%C3%B6%C3%A7men — Yazarın YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://www.youtube.com/watch?v=gXhVFwzN4_4&t=2s&ab_channel=%C3%96merG%C3%B6%C3%A7men — Yazarın YouTube videosu (2 sn başlangıç) · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://www.youtube.com/watch?v=bXBS2Hzr-vU&ab_channel=%C3%96merG%C3%B6%C3%A7men — Yazarın YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://www.youtube.com/watch?v=7tInlFRcTEQ&ab_channel=%C3%96merG%C3%B6%C3%A7men — Yazarın YouTube videosu · aday: hayır · Konu dışı; içeriği paketten doğrulanamadı. · sınıf: diğer
- https://www.linkedin.com/in/%C3%B6mer-g%C3%B6%C3%A7men-43a353227 — Yazarın LinkedIn profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
- https://www.tiktok.com/@omerrgcmn — Yazarın TikTok profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
- https://www.instagram.com/omerrgcmn — Yazarın Instagram profili · aday: hayır · Sosyal medya profili; araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Bölünmüş ekran giriş kartı (split-screen layout) | Giriş ekranında solda ortalanmış beyaz kart, sağda tam ekran görsel; kart içinde e-posta, şifre ve Giriş Yap butonu. (karede: 'Hoş Geldiniz' kartı solda, sağda çocuk görseli ve 'Engeldestek' yazısı.) | 1:20 | kare |
| Kahraman bölümü (hero section) | Ana sayfanın üstünde başlık, madde listesi ve sağda yuvarlatılmış görsel. (karede: 'EngelDestek Forum' büyük başlık, madde işaretli açıklamalar ve sağda grup fotoğrafı.) | 2:00 | kare |
| Gönderi kartları (card UI) | Gönderiler kart halinde; yazar adı, tarih, metin, görsel, etiketler ve etkileşim satırı. (karede: Gönderi kartında yazar 'Ömer Göçmen', tarih, görsel ve alt satırda Beğen, Yorum Yap, Paylaş.) | 1:45 | kare |
| Zengin metin editörü (rich text editor) | Gönderi formunda kalın, italik, altı çizili, liste ve bağlantı araç çubuğu bulunur. (karede: 'Formu Kapat' ve üstte Normal, B, I, U, S ve liste simgelerinden oluşan araç çubuğu.) | 2:06 | kare |
| Açılır form (accordion / collapsible panel) | 'Yeni Gönderi Oluştur' butonuyla gönderi formu açılır, 'Formu Kapat' ile kapanır. (karede: Büyük 'Yeni Gönderi Oluştur' kutusu; açıkken 'Formu Kapat' yazısı görünüyor.) | 2:06 | kare |
| Etiket sistemi (hashtag chips) | Gönderi altında #etiket rozetleri; sağ panelde 'Günün Etiketleri' listesi ve sayaçlar. (karede: Sağ kenar çubuğunda 'Günün Etiketleri' başlığı altında etiketler ve sayılar (örn. #farkındalık (2)).) | 0:00 | kare |
| Kenar çubuğu (sidebar) | Sağ tarafta günün etiketleri, TRT Engelliler Haberleri ve Diğer Haber Kaynakları blokları. (karede: Sağ kolonda 'TRT Engelliler Haberleri' ve 'Diğer Haber Kaynakları' başlıkları, haber linkleri.) | 0:00 | kare |
| Etkileşim butonları (action buttons) | Gönderi altında Beğen, Yorum Yap ve Paylaş butonları; sayaçlar gösterilir. (karede: 'Beğen (0)', 'Yorum Yap', 'Paylaş' butonları ve altında 'Yorumları Göster (0)'.) | 1:48 | kare |
| Beğeni durum değişimi (toggle state) | Beğen butonuna basınca sayaç artar ve buton koyu renge döner. (karede: 'Beğen (1)' ve mavi/koyu dolu buton görünümü.) | 3:42 | kare |
| Üst gezinme çubuğu (sticky navbar) | Üstte logo ve 'Ana Sayfa', 'Hakkımızda', 'Skor Tablosu', 'Gönderilerim', 'Profil', 'Çıkış' menüsü. (karede: Sayfanın üst kısmında EngelDestek logosu ve menü bağlantıları, sağda profil avatarı.) | 3:36 | kare |
| Skor tablosu (leaderboard) | İki sütunlu tablo: en çok beğenilen gönderiler ve en çok paylaşan kullanıcılar. (karede: 'Skor Tablosu' başlığı altında iki kart: 'En Çok Beğenilen Gönderiler' ve 'En Çok Paylaşan Kullanıcılar'.) | 3:58 | kare |
| Takip Et / Takibi Bırak butonu (follow toggle) | Kullanıcı profilinde takip durumuna göre buton metni değişir. (karede: Profil sayfasında sağ üstte 'Takibi Bırak' butonu.) | 14:28 | kare |
| Sağdan açılan bildirim paneli (slide-in drawer) | Üst sağdaki bildirim ikonundan açılır; 'Tümünü Okundu İşaretle' butonu listenin altındadır. | 16:04 | açıklama |
| Profil formu (form layout) | Ad, soyad ve profil fotoğrafı URL alanları ve Değişiklikleri Kaydet / İptal Et butonları. (karede: 'Profili Düzenle' ekranında Ad, Soyad, Profil Fotoğrafı (URL) alanları ve kaydet butonu.) | 4:28 | kare |
| Alt bilgi (footer) dört sütunlu yerleşim | Alt kısımda logo, Hızlı Linkler, Destek ve İletişim sütunları. (karede: Footer'da 'Hızlı Linkler', 'Destek' ve 'İletişim' başlıkları ile e-posta bilgisi.) | 2:08 | kare |
| Duyarlı tasarım (responsive design) | Sayfa mobil öncelikli düzende yapılandırılmış; yan panel gerektiğinde alta iner. | 16:04 | açıklama |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Lovable ücretsiz hafta sonu ücretsizdi ve bu fırsat kullanıldı. | 0:00 | özellik |
| Uygulama hiç kod yazılmadan yaklaşık 25-30 prompt ile yapıldı. | 10:10 | sayısal |
| Supabase ücretsiz sürümünde yalnızca bir proje oluşturulabiliyor. | 6:06 | sayısal |
| Ücretsiz Supabase limitine takılınca yeni proje oluşturulamıyor (free project limit hatası). | 11:10 | özellik |
| Takip tabloları ve ilişkiler Lovable'ın ürettiği SQL ile Supabase'de otomatik oluşturuldu. | 14:13 | özellik |
| Supabase Attack Protection ile login ekranına captcha (Turnstile) eklenebiliyor. | 8:07 | özellik |
| Yeni gönderi bildirimi son testte çalıştı; bildirime tıklanınca gönderiye gidiliyor. | 20:21 | özellik |
| Lovable'da Publish ile uygulama yayınlanabiliyor; alan adı bağlanabilir. | 18:19 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 · kare 0:00 | Lovable ile web sitesi geliştirme | Lovable | Lovable - Build for the web |
| konuşma 0:00 | Backend olarak Supabase | Supabase | Lovable'da entegre olabilen ... backend görevi sunabilen Zupa Base |
| kare 5:36 | Lovable model seçici: Anthropic | Anthropic | Pick your AI model; Anthropic seçili |
| kare 6:26 | Supabase'in veritabanı motoru | PostgreSQL | Listen to your PostgreSQL database in realtime |
| kare 7:36 | Satır bazlı güvenlik politikaları | Row Level Security | Row Level Security is enabled, but no policies exist |
| konuşma 8:07 · kare 8:20 | Login koruması için captcha sağlayıcısı | Cloudflare Turnstile | Turinstile by Cloudflare |
| konuşma 8:07 | Alternatif captcha seçeneği olarak anılan hCaptcha | aday değil: genel kavram | hash kapça ekleyebiliyorsunuz |
| kare 12:10 | Promptların saklandığı metin editörü | Notepad++ | Yeni 11 - Notepad++, prompt satırları |
| konuşma 4:03 | Profil fotoğrafının Google'dan alınması | aday değil: konu dışı | Ben bunu direkt Google'dan aldım |
| konuşma 7:06 | Google ile giriş seçeneği | aday değil: genel kavram | Google'la mı giriş yapacak |
| konuşma 7:06 · kare 7:12 | Kayıt onayı e-postası (yerleşik servis) | aday değil: başka adayın parçası (Supabase) | Confirmation maili ... Supabase yapıyor |
| kare 6:26 | Edge Functions bölümü (kullanılmadı) | aday değil: başka adayın parçası (Supabase) | Edge Functions |
| kare 8:58 | Storage bucket ekranı | aday değil: başka adayın parçası (Supabase) | storage/buckets |
| kare 6:26 | Realtime ayarı (Realtime off) | aday değil: başka adayın parçası (Supabase) | Realtime off |
| kare 9:08 · kare 13:56 | Tablo düzenleyici (Table Editor) | aday değil: başka adayın parçası (Supabase) | Table Editor |
| kare 9:48 | SQL düzenleyici (SQL Editor) | aday değil: başka adayın parçası (Supabase) | SQL Editor |
| kare 7:00–8:20 | Auth kullanıcıları, şablonlar, rate limit, politikalar, URL yapılandırması | aday değil: başka adayın parçası (Supabase) | Authentication > Rate Limits, Policies, URL Configuration |
| kare 8:20 | Attack Protection (bot koruması) ekranı | aday değil: başka adayın parçası (Supabase) | Bot and Abuse Protection |
| ses 9:08 | 'Table' sesi (Table Editor olarak anılmış) | aday değil: başka adayın parçası (Supabase) | Teable (ses eşleşmesi: table) |
| kare 10:14 · kare 10:38 | GitHub senkronizasyonu özelliği | aday değil: başka adayın parçası (Lovable) | GitHub Senkronizasyonu: Projenizin kodu |
| kare 10:14 | Lovable 'Supabase'i Bağla' butonu | aday değil: başka adayın parçası (Lovable) | Supabase'i Bağla |
| kare 10:38 | Lovable sohbet modu | aday değil: başka adayın parçası (Lovable) | sohbet modunu kullanın |
| kare 10:34 | Lovable belgeleri bağlantısı | aday değil: başka adayın parçası (Lovable) | https://docs.lovable.dev |
| konuşma 18:19 · kare 18:20 | Publish (yayınlama) düğmesi | aday değil: başka adayın parçası (Lovable) | publish seçeneği var |
| kare 10:00 | Next.js / TypeScript / React adları (blog şablonu metni) | aday değil: konu dışı | TypeScript ile Güvenli Kod |
| kare 5:30 | n8n.io tarayıcı yer imi | aday değil: konu dışı | n8n.io |
| kare 5:30 | ChatGPT ve WhatsApp yer imleri | aday değil: konu dışı | ChatGPT, WhatsApp |
| kare 0:00 · kare 3:24 | Engelli haber siteleri (TRT, Sondakika, Hürriyet, Engelliler.gen.tr, eczagundem) | aday değil: konu dışı | TRT Engelliler Haberleri |
| kare 12:10 | Görev çubuğunda Docker/dockerfile adları | aday değil: konu dışı | dockerfile |
| kare 12:42 | Görev/dosya adları (openshot-qt, obs64) | aday değil: konu dışı | openshot-qt.exe obs64.exe |
| kare 6:36 | Inter yazı tipi (Supabase arayüzü) | aday değil: konu dışı | Inter |
| ses 17:18 · kare 7:00 | 'Veo' ses eşleşmesi ve 'Spline' ekran adı; kullanım yok | aday değil: konu dışı | Veo (ses eşleşmesi) |
| açıklama | Kanal üyelik (Join) bağlantısı, ücretli ayrıcalık | aday değil: sponsor/reklam | Ayrıcalıklardan yararlanmak için bu kanala katılın |
| açıklama | Sosyal medya profilleri (LinkedIn, TikTok, Instagram) | aday değil: konu dışı | İletişim ve Sosyal Medya |
| açıklama | Lovable Supabase bağlantılı blog ve EngelDestek demo bağlantısı | aday değil: konu dışı | vibrant-threads-collective.lovable.app |
| yorum | Android uygulama için Dualite önerisi sorusu | aday değil: konu dışı | Lovable mı yoksa Dualite mı |
| ekran 0:00 · 2:00 | Tarayıcı/Chrome arayüzü (yeni sekme, yer imi çubuğu) | aday değil: genel kavram | Yeni Sekme |
## Kareden okunanlar
- 0:00: Sol panelde Lovable sohbeti ('Login ve kayıt sayfasındaki resmi değiştir'), sağda 'EngelDestek Forum' ana sayfa önizlemesi ve 'Günün Etiketleri' paneli.
- 0:11: Lovable sohbet mesajı: 'login ve kayıt sayfasındaki resmi aşağıdakiyle değiştir' ve görsel adresi.
- 1:20: Giriş ekranı: 'Hoş Geldiniz', e-posta ve şifre alanları, 'Giriş Yap', 'Hesabınız yok mu? Kayıt olun'.
- 1:45: Ana sayfa: 'Forumda Paylaşılan Son Gönderiler' ve gönderi kartları (Beğen, Yorum Yap, Paylaş).
- 2:06: Gönderi formu: 'Yeni Gönderi Oluştur' açık, zengin metin araç çubuğu ve 'Paylaş' butonu.
- 3:42: Skor tablosu bölümü: 'Forum başarı sıralaması', en aktif üyeler.
- 4:28: Profil düzenleme: Ad, Soyad, Profil Fotoğrafı (URL) alanları, 'Değişiklikleri Kaydet' ve 'Hesaptan Çıkış Yap'.
- 5:36: Lovable ana sayfa: 'Free Weekend: AI Showdown', model seçici 'Anthropic'.
- 5:42: Lovable çalışma alanı: 'Writing CreatePost.tsx', 'Supabase bağlantısı kurman gerekiyor' mesajı ve 'Modern kartlar' özellik listesi.
- 6:26: Supabase proje sayfası: 'og-forum', 'Tables 5 / Functions 0 / Replicas 0', PostgreSQL ve Realtime açıklamaları.
- 6:36: Supabase API sayfası: proje API adresi (proje kimliği) ve 'anon public' anahtar açıklaması; anahtar değeri yazılmadı.
- 7:00: Auth > Users: kullanıcı listesi (e-posta adresleri kişisel veri olduğu için yazılmadı).
- 7:12: Auth > Emails: 'Confirm Your Signup' şablonu ve yerleşik e-posta servisi uyarısı (rate limit).
- 7:36: Auth > Policies: comment_likes, comments, likes, posts, profiles tabloları için 'RLS etkin, politika yok' uyarısı.
- 7:54: Auth > URL Configuration: Site URL ve izinli yönlendirme URL listesi (lovable.app alan adları).
- 8:20: Attack Protection: Captcha secret alanı ve 'Turnstile by Cloudflare' kurulum bağlantısı; gizli değer yazılmadı.
- 8:44: Database > Schema Visualizer: comment_likes, comments, likes, posts, profiles tabloları ve ilişkileri.
- 9:08: Table Editor: 'profiles' tablosu; first_name, last_name, email, profile_image_url sütunları.
- 9:48: SQL Editor: 'User Profiles Management' sekmesi ve sorgu çalıştırma alanı.
- 10:00: Lovable: 'Add Advanced Features (Edge Functions)' notu ve 'Changes already applied' hata mesajı.
- 10:14: Lovable blog şablonu: 'Supabase'i Bağla' butonu ve blog metinleri (TypeScript, React, GitHub Senkronizasyonu).
- 11:04: Supabase yeni proje ekranı: organizasyon seçimi, proje adı, veritabanı şifresi, bölge seçimi.
- 12:10: Notepad++: 'Yeni 11' metin dosyası, 6 satır, bildirim ve takip promptları (length 712).
- 12:42: Görev listesi / dosya adları (openshot-qt.exe, obs64.exe): konu dışı.
- 13:20: Lovable SQL çıktısı: CREATE TABLE public.follows, notifications; ENABLE ROW LEVEL SECURITY; CHECK (follower_id != following_id).
- 13:22: Lovable SQL çıktısı: create_follow_notification() fonksiyonu, SECURITY DEFINER, AFTER INSERT trigger.
- 13:46: Lovable: 'Bu SQL komutlarını inceleyip onaylayın, ardından çalıştırın' ve RLS politikaları listesi.
- 14:28: Profil sayfası: sağ üstte 'Takibi Bırak' butonu ve gönderi bölümü.
- 15:04: Lovable promptu: 'Bildirimlere en üst sağ köşeden bildirim buton olsun'.
- 16:04: Lovable değişiklik özeti: notifications foreign key ekleme ve 'Bildirim paneli sağ taraftan açılır'.
- 16:56: Lovable değişiklik özeti: 'Tümünü Okundu işaretle' butonu listenin altına, bildirim ikonu profilin sağına taşındı.
- 17:52: Lovable uyarısı: '3 Supabase Errors' ve 'Review Errors'.
- 18:20: Lovable commit mesajı: 'feat: Add following posts and n...' ve yayın göstergesi.
- 19:38: Lovable düzeltme özeti: 'Fix: Notification RLS policy', RLS politikası basitleştirildi, tek tek insert.
- 20:06: Lovable: 'Mevcut INSERT politikasını kaldır' ve 'I have reviewed the SQL and it looks good. Please run it.'
## Belirsizlikler
- Açıklamada bölüm (chapter) bulunmuyor; bolumler alanı konuşma akışından çıkarılmış tahmini zaman damgalarıdır.
- Ses eşleşmeleri bulanık: 'Claude Fable' (1:00) büyük olasılıkla Lovable, 'cloudflayer' (8:07) Cloudflare, 'Teable' (9:08) table; 'Veo' (17:18) net değil ve araç olarak kullanılmadığı varsayıldı.
- n8n: açıklamadaki bağlantılı sayfalarda ve tarayıcı yer imlerinde (5:30) görünüyor, videoda kullanılmadı; aday yapılmadı.
- Ekranda Docker, NVIDIA app, OBS, OpenShot, Inter ve Spline gibi adlar yalnızca arka plan/menü öğesi olarak görünüyor; kullanımı netleşmediği için aday yapılmadı.
- Lovable'ın kullandığı yapay zekâ modeli 'Anthropic' olarak seçili görünüyor; model sürümü ekranda net okunmadı.
- Ücretsiz Supabase hesabında proje limiti ve e-posta gönderim limiti (yerleşik servis) nedeniyle kayıt/bildirim gecikmeleri yaşandı; limitlerin güncel değeri videoda doğrulanmadı.
- Supabase ekranlarında API anahtarı, veritabanı şifresi ve Turnstile gizli değeri görünüyor; bunlar bu formda yazılmadı.
- Yorumda Lovable ile Android uygulama için 'Dualite' önerisi soruluyor; videoda Dualite kullanılmadı, aday yapılmadı.
- Gönderi bildirimi hatasının video sonunda çözüldüğü gösteriliyor; tekrar testin kalıcılığı doğrulanmadı.
## Atlanan segment oranı
0/21 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| lovable.dev/projects/1cafdb25-dfca-41a8-a4d8-ed7141a0ea33 | 0:00 | ekran | evet |
| https://www.eczagundem.com/wp-content/uploads/2024/03/Generali-Sigorta-Down-Sendromu-scaled.jpg | 0:00 | ekran | hayır |
| Sondakika.com | 0:00 | ekran | hayır |
| Engelliler.gen.tr | 0:00 | ekran | hayır |
| engeldestek.co | 2:00 | ekran | hayır |
| https://1cafdb25-dfca-41a8-a4d8-ed7141a0ea33.lovableproject.com/tag/farkndalik | 2:54 | ekran | hayır |
| https://1cafdb25-dfca-41a8-a4d8-ed7141a0ea33.lovableproject.com/tag/birliktegüçlüyūz | 2:58 | ekran | hayır |
| https://1cafdb25-dfca-41a8-a4d8-ed7141a0ea33.lovableproject.com/tag/birliktegüzeliz | 3:00 | ekran | hayır |
| https://www.trthaber.com/etiket/engelliler/ | 3:24 | ekran | hayır |
| https://1cafdb25-dfca-41a8-a4d8-ed7141a0ea33.lovableproject.com/about | 3:36 | ekran | hayır |
| engeldestek.com | 3:54 | ekran | hayır |
| https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCh | 4:32 | ekran | hayır |
| n8n.io | 5:30 | ekran | hayır |
| lovable.dev | 5:36 | ekran | evet |
| lovable.dev/projects/25b8e230-7b90-4de0-a144-7e5f68a6914b | 5:42 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/protection | 5:48 | ekran | evet |
| supabase.com/dashboard/org/rqdlosgjsgkuhxmtjqfa | 5:52 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa | 5:56 | ekran | evet |
| https://ngpqguesmuluhpumhcqa.supabase.co | 6:36 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/users | 7:00 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/templates | 7:12 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/sessions | 7:26 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/rate-limits | 7:32 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/policies | 7:36 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/auth/url-configuration | 7:54 | ekran | evet |
| https://erisilebilir-forum-platformu.lovable.app/** | 7:54 | ekran | hayır |
| https://preview--vibrant-threads-collective.lovable.app/** | 7:54 | ekran | hayır |
| https://vibrant-threads-collective.lovable.app/** | 7:54 | ekran | hayır |
| domain.com | 7:54 | ekran | hayır |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/database/schemas | 8:44 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/storage/buckets | 8:58 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/logs | 9:02 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/api | 9:04 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/editor/17269 | 9:08 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/sql/ecd564eb-fd42-4f4b-837c-251f8a1b8824 | 9:48 | ekran | evet |
| https://docs.lovable.dev | 10:34 | ekran | hayır |
| https://supabase.com/dashboard/new/rqdlosgjsgkuhxmtjqfa | 11:04 | ekran | evet |
| id-preview--1cafdb25-dfca-41a8-a4d8-ed7141a0ea33.lovable.app/statistics | 12:22 | ekran | hayır |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/editor | 13:00 | ekran | evet |
| https://supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/editor/17287?schema=public | 13:40 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/editor/18578?schema=public | 13:56 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/editor/18587?schema=public | 14:02 | ekran | evet |
| supabase.com/dashboard/project/ngpqguesmuluhpumhcqa/editor/17321?schema=public | 14:08 | ekran | evet |
| https://supabase.com/dashboard/org/rqdlosgjsgkuhxmtjqfa | 14:10 | ekran | evet |
| vibrant-threads-collective.lovable.app | 17:52 | ekran | hayır |
| https://github.com/n8n-io/n8n | açıklama | açıklama | hayır |
| https://docs.lovable.dev/llms.txt | açıklama | açıklama | hayır |
| https://docs.lovable.dev/features/workspace | açıklama | açıklama | hayır |
| https://docs.lovable.dev/integrations/git-sync-overview | açıklama | açıklama | hayır |
| https://docs.lovable.dev/introduction/credits-and-usage | açıklama | açıklama | hayır |
| https://docs.lovable.dev/introduction/subscription-plans | açıklama | açıklama | hayır |
| https://docs.lovable.dev/features/chats | açıklama | açıklama | hayır |
| https://docs.lovable.dev/features/ai | açıklama | açıklama | hayır |
| https://trust.lovable.dev | açıklama | açıklama | hayır |
| https://vibrant-threads-collective.lovable.app | açıklama | açıklama | hayır |
| https://www.linkedin.com/in/%C3%B6mer-g%C3%B6%C3%A7men-43a353227 | açıklama | açıklama | hayır |
| https://www.tiktok.com/@omerrgcmn | açıklama | açıklama | hayır |
| https://www.instagram.com/omerrgcmn | açıklama | açıklama | hayır |
## İş akışı
- yok
## Promptlar
- Lovable'da yeni proje oluşturma (Supabase bağlantılı blog) — Blog sitesi oluştur; arka planda Supabase olsun ve blog yazıları oraya kaydedilsin.
- Giriş ve kayıt ekranındaki görseli değiştirme — Login ve kayıt sayfasındaki resmi verilen görsel bağlantısıyla değiştir.
- Yorum yazma yetkisini sadece oturum açmış kullanıcılara verme (RLS) — Yorumu sadece giriş yapan kullanıcılar atsın (yetkilendirme kuralı).
- Takip butonu ekleme — Kullanıcı detay sayfasında kullanıcıyı takip et butonu olsun.
- Takip bildirimi için tablo ve tetikleyici — Bildirimler adında tablo oluştur; bir kullanıcı başka biri tarafından takip edilince bildirim alsın (ad, soyad seni takip etmeye başladı).
- Bildirim okundu durumu ve panel konumu — Bildirimler kısmında tıklanan bildirim okundu olarak güncellensin; tümünü okundu işaretle butonu üst sağ köşeden bildirim paneline erişilebilir olsun.
- Takip edilen gönderiler filtresi — Ana sayfada takip ettiklerim kısmı olsun; tıklanınca yalnız takip edilen kişilerin gönderileri görünsün.
- Yeni gönderi bildirimi ve yönlendirme — Bir kişi gönderi oluşturduğunda takip ettiği kişilere bildirim gitsin (ad, soyad gönderi yayınladı); bildirime tıklayınca gönderiye gidilsin.
- Bildirim kaydının oluşmama hatasını düzeltme — Takip ettiğimde notifications tablosuna kayıt gelmiyor; kontrol et ve doğru çalışsın.
- Test sonucu hatası bildirimi — Takip edilen kişi gönderi paylaştığında bildirim gelmiyor; hata olarak bildirme.
ikinci göz KAPALI: --ikinci-goz yok
