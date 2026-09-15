# Uygulamanı Token Harcamadan Otomatik Test Etme Yöntemi
kanal: Burhan KOCABIYIK · süre: 7 dk · altyazı: otomatik tr
ana iddia: TestSprite CLI Claude Code'a bağlanıp uygulama linki verilince test planlarını kendisi çıkarır, tüm sayfaları ücretsiz gezer; test döngüsü Claude token'ı harcamadan otomatikleşir.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| TestSprite/testsprite-cli (TestSprite) | YENİ | ADAY | linke bulutta E2E: test planı çıkarır, sayfaları gezer, ekran kaydı + tıklama notlarını Claude Code'a döndürür; bakım iyi, kredi bazlı ve veri 3. tarafa gider |
| güncelleme sonrası ve gün sonu canlı linkte tüm sayfaları gezen E2E regresyon testi | YENİ | BİLGİ | CLAUDE.md değişiklik başına test ister, sayfa geneli regresyon kuralı yok; frontend-craft screenshot döngüsü yalnız görsel |
| Claude Code: /loop (bir terminalde sürekli test, diğerinde geliştirme) | ZATEN VAR | ELENDİ | yerleşik loop skill; test koşusunu ana context dışına almak CLAUDE.md CONTEXT DİSİPLİNİ'nde var |
| "bitirdim" dediğine güvenmeyip testle doğrulama, prompt→çıktı→test→tekrar döngüsü | ZATEN VAR | ELENDİ | CLAUDE.md hedef-güdümlü "kanıtsız bitti yok" + superpowers:verification-before-completion |
| diğer: Prototipal (konuşmacının uygulaması), Visual Studio Code?, GitHub, DOA (Skool) | YENİ | ELENDİ | test hedefi örneği / editör-platform / açıklamadaki promo; kurulacak araç değil |
## ölçütler (YENİ)
- TestSprite/testsprite-cli: bakım=pushed 2026-09-14, 3205★, arşiv değil, Apache-2.0 · çift=kısmi: frontend-craft Bölüm 2/9 screenshot döngüsü (görsel, akış testi yok), claude-in-chrome (yerleşik, Claude token'ı harcar); bulutta E2E koşan kurulu araç yok · izin=TestSprite hesabı + API anahtarı, global npm (Node 20.19+), setup repoya ajan skill dosyası yazar, uygulama trafiği TestSprite bulutuna gider, plan üretimi/koşular kredi harcar (README; video "ücretsiz" diyor) · context=setup'ın kurduğu skill açıklaması o projede her oturum, CLI yalnız çağrılınca, MCP şeması yok · kurulum: npm install -g @testsprite/testsprite-cli && testsprite setup (README ile doğrulandı; videoda install + anahtar soran ikinci komut)
- E2E regresyon testi: bakım=— (teknik, repo yok) · çift=kısmi: CLAUDE.md hedef-güdümlü (değişiklik başına test), frontend-craft Bölüm 2 (görsel) · izin=yok (araç seçimine bağlı) · context=CLAUDE.md'ye 1 satır (her oturum) · kurulum: —
- diğer: bakım=bilinmiyor (Prototipal, DOA repo yok; Visual Studio Code?, GitHub platform) · çift=örtüşme yok · izin=DOA Skool üyeliği; diğerleri kurulum dışı · context=kurulmadıkça yok · kurulum: —
## hedefler (BİLGİ)
- her güncelleme sonrası ve gün sonunda (GitHub'a push ile) canlı linkte tüm sayfaları gezen E2E regresyon testi; ajanın "bitti"si bunu geçmeden kapanış sayılmaz → CLAUDE.md (Hedef-güdümlü: regresyon)
---
## ek: test/güvenlik
- araç: TestSprite (testsprite.com; açıklamadaki link ?via=burhan-k affiliate parametreli) — AI test platformu, test planı çıkarır, sayfaları gezer
- araç: TestSprite CLI (github.com/TestSprite/testsprite-cli) — Claude Code'a bağlanır; açıklama "tek satırlık CLI kurulumu" der, videoda iki komut yapıştırılır
- yöntem: siteye gir → terminal bölümü → "Agents ve CLI" → yeni API anahtarı oluştur; API anahtarları sayfasında tüm anahtarlar listelenir
- ayar: API anahtarı ajana özel adla ("claude") oluşturuldu; anahtar saklama, verinin 3. taraf buluta gitmesi ve kredi/limit videoda konuşulmuyor
- komut: CLI sekmesindeki install komutu kopyalanır, Claude başlatılmadan Visual Studio (Code?) içinde yeni terminale yapıştırılır (komut metni altyazıda yok)
- komut: install sonrası ikinci kopyalanan komut yapıştırılır, TestSprite API anahtarını sorar, anahtar yapıştırılır → Claude'a yüklenir, projelere erişim görünür (komut metni altyazıda yok)
- komut: Claude Code prompt'u: "<Prototipal linki> bu linki TestSprite CLI'ını kullanarak test et" (yalnız "test et" de yeter denir)
- yöntem: CLI siteye gider, topladığını TestSprite'a gönderir; test planı çıkarır (fiyat sayfası, kataloglar), testleri teker teker koşar, sayfaları gezip aşağı kaydırır
- yöntem: çıktı: her sayfanın ekran videosu ve görüntüsü, kayıtta tıklanan yerler, tıklamalara göre notlar, geçen/geçmeyen takibi; bilgilendirme Claude'a döner
- ayar: dashboard'da proje ("Prototipal apps katalog"), önceki/yeni testler, kategori bilgileri; ilerleme Claude Code içinden de izlenir
- yöntem: örnek bulgu: testler sürerken "kategori filtresi çalışmıyor" bilgisi toplandı — dashboard'da gösterildi
- yöntem: ne zaman: geliştirirken sürekli, gün sonunda; projeyi bitirdikçe GitHub'a yükle, yanında testleri koş; canlıya alınmış uygulamanın tüm sayfalarını kontrol et
- yöntem: /loop ya da iki terminal: birinde sürekli test, diğerinde geliştirme
- yöntem: hacim büyükse (çok template/prompt) sayfa sayfa testi Claude Code yerine harici servise yaptır; "bitirdim, bakabilirsin" çıktısını testle doğrula
- sayı: CLI kurulumu 2 saniye — yalnız iddia (kurulum ekranda yapıldı, süre ölçülmedi)
- sayı: kurulum "d tane" paket ekledi (sayı ASR'de okunamıyor) — gösterildi? (terminal çıktısı, altyazıdan kesin değil)
- sayı: 11 test planı yazacak — gösterildi? (dashboard'dan okunuyor, altyazıdan kesin değil)
- sayı: ücretsiz, "çok fazla test", test için ek token masrafı yok — yalnız iddia (plan/limit/token ölçümü gösterilmedi)
