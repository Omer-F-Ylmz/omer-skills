# Uygulaman hazır ama App Store’a nasıl yükleneceğini bilmiyor musun?
## Künye
Uygulaman hazır ama App Store’a nasıl yükleneceğini bilmiyor musun? · tahiryildiz · süre: 2:58 · ? · https://www.instagram.com/reel/DNbH6BMtMEB/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-38 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 41331 tk · claude-haiku-5-5: claude-haiku-5-5 · 68761 tk
## Özet
Tahir Yıldız, mobil uygulamanın App Store'a yüklenmesini 9 aşamada anlatıyor: React Native ile geliştirme, Apple Developer hesabı, App Store Connect'te uygulama ve Bundle ID oluşturma, Expo EAS ile IPA build alma, Transporter ile Verify/Deliver, TestFlight testi, mağaza bilgilerini doldurma ve incelemeye gönderme.
## Bölümler
- 0:00 Giriş ve 1. aşama: Geliştirme (React Native)
- 0:28 2. aşama: Apple Developer hesabı
- 0:39 3. aşama: App Store Connect'te uygulama ve Bundle ID oluşturma
- 1:05 4. aşama: Expo EAS ile build alma (IPA)
- 1:36 5. aşama: Transporter ile Verify ve Deliver
- 2:00 6. aşama: TestFlight ile test
- 2:14 7-9. aşamalar: Mağaza bilgileri, gerekli alanlar, incelemeye gönderme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| React Native | yok | teknik | yok | Hem Android hem iOS için uygulama geliştirme çatısı; videoda 1. aşamada öneriliyor. | 0:00 | React Native ile yazdığınıza emin olmanız lazım. |
| Expo | yok | CLI | yok | React Native projesi için build alma servisi/araç zinciri; iOS build için kullanılıyor. | 1:05 | React Native kullandığınız için Expo kullanmış oluyorsunuz. |
| EAS CLI | yok | CLI | yok | Expo Application Services komut satırı aracı; iOS build (IPA) almak için kullanılıyor. | 1:12 | Expo dokümanında EAS CLI kurulumu ve eas build komutları gösteriliyor. (karede: kanıttan) Expo dokümanında EAS CLI kurulumu ve eas build komutları gösteriliyor. |
| Cursor | yok | CLI | yok | Terminali içinde build komutunun çalıştırıldığı kod editörü. | 1:21 | kopyalayıp cursordaki terminale eas build yazman yeterli |
| App Store Connect | yok | iş akışı | yok | Uygulamanın oluşturulduğu, TestFlight ve mağaza bilgilerinin yönetildiği Apple paneli. | 0:39 | appstoreconnect.apple.com/apps adresi ve uygulama listesi görünüyor. (karede: kanıttan) appstoreconnect.apple.com/apps adresi ve uygulama listesi görünüyor. |
| Apple Developer | yok | iş akışı | yok | Geliştirici hesabı ve Bundle ID/Certificates, Identifiers & Profiles sayfası; hesap 99 dolar. | 0:28 | App Store'da Apple Developer uygulaması ve Certificates, Identifiers & Profiles sayfası. (karede: kanıttan) App Store'da Apple Developer uygulaması ve Certificates, Identifiers & Profiles sayfası. |
| Transporter | yok | CLI | yok | IPA dosyasını Verify edip Deliver ile App Store Connect'e gönderen Apple uygulaması. | 1:36 | Transporter uygulamasını indirmek için App Store'a giriyoruz ve Transporter yazıyoruz. |
| TestFlight | yok | iş akışı | yok | Uygulamanın arkadaşlara test ettirildiği Apple test aşaması. | 2:00 | Test Flight kısmına gelmiş olması lazım. |
| Bundle ID | yok | teknik | yok | Uygulama kimliği; com.tahiryildiz.uygulamaadı biçiminde girilir. | 0:59 | Bundle ID alanına com.tahiryildiz... yazılıyor. (karede: kanıttan) Bundle ID alanına com.tahiryildiz... yazılıyor. |
| EAS Build | yok | CLI | yok | Expo'nun bulut build servisi; iOS için IPA dosyası üretir | 1:21 | eas build --platform all (karede: Expo dokümanındaki terminal bloğunda 'eas build --platform all' komutu yazıyor) |
| Node.js | yok | teknik | yok | Expo proje gereksinimleri arasında geçen JavaScript çalışma ortamı | 1:17 | Node, Yarn, npm, CocoaPods, or Xcode (karede: Expo dokümanındaki sürüm gereksinimi metni) |
| Yarn | yok | teknik | yok | Expo proje gereksinimleri arasında geçen paket yöneticisi | 1:17 | Node, Yarn, npm, CocoaPods, or Xcode · kanıt: kare (karede: Expo dokümanındaki sürüm gereksinimi metni (OCR'de 'Yam' olarak okunmuş)) |
| npm | yok | teknik | yok | Expo proje gereksinimleri arasında geçen Node paket yöneticisi | 1:17 | Node, Yarn, npm, CocoaPods, or Xcode (karede: Expo dokümanındaki sürüm gereksinimi metni) |
| CocoaPods | yok | teknik | yok | iOS bağımlılıklarını yöneten paket yöneticisi | 1:17 | Node, Yarn, npm, CocoaPods, or Xcode (karede: Expo dokümanındaki sürüm gereksinimi metni) |
| Xcode | yok | teknik | yok | Apple'ın iOS ve macOS geliştirme ortamı | 1:17 | Node, Yarn, npm, CocoaPods, or Xcode (karede: Expo dokümanındaki sürüm gereksinimi metni) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| eas build | Expo EAS ile iOS build alır ve IPA dosyası üretir. | 1:21 | altyazı |
| eas build --platform all | Android ve iOS için aynı anda build alır. | 1:21 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Mobilden Apple Developer üyeliği webden daha ucuz; normalde 99 dolar. | 0:28 | sayısal |
| React Native ile yazılan uygulama hem Android hem iOS için uygun olur. | 0:00 | özellik |
| Mac olmadan da iOS için uygulama geliştirilebilir. | 0:00 | özellik |
| Deliver'dan önce Verify yapılması öneriliyor. | 1:36 | öneri |
| TestFlight'ta arkadaşlara test ettirip bug ve crash tespit etmek çok önemli. | 2:09 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | React Native | React Native | React Native ile yazdığınıza emin olmanız lazım. |
| konuşma 0:28 | Apple Developer hesabı | Apple Developer | Apple Developer hesabı açmanız lazım. |
| kare 0:28 | Apple Developer uygulaması (App Store) | Apple Developer | Apple Developer, Developer Tools görünüyor. |
| kare 0:35 | SwiftUI arama sonuçları / WWDC24 videoları | aday değil: konu dışı | Apple Developer uygulamasında SwiftUI arama sonuçları. |
| kare 0:39 | App Store Connect | App Store Connect | appstoreconnect.apple.com/apps adresi görünüyor. |
| kare 0:39 | Sessiva, Kombinly, kwikZap, Nox Calendar uygulamaları | aday değil: konu dışı | App Store Connect listesindeki kendi uygulamaları. |
| konuşma 0:59 | Bundle ID | Bundle ID | com.tahiryildiz.uygulamanın adı şeklinde girmeniz yeterli. |
| kare 1:12 | Expo / EAS Build / EAS CLI dokümanı | EAS CLI | Expo dokümanında Install the latest EAS CLI. |
| konuşma 1:05 | Expo | Expo | Expo kullanmış oluyorsunuz. |
| konuşma 1:21 | Cursor terminali | Cursor | cursordaki terminale eas build yazman yeterli |
| konuşma 1:36 | IPA dosyası | aday değil: başka adayın parçası (EAS CLI) | Build çıktısı IPA uzantılı dosya. |
| konuşma 1:36 | Transporter uygulaması | Transporter | Transporter yazıyoruz, Verify ve Deliver. |
| konuşma 2:00 | TestFlight | TestFlight | Test Flight kısmına gelmiş olması lazım. |
| kare 2:25 | Description, Keywords, Support URL alanları | aday değil: başka adayın parçası (App Store Connect) | iOS App Version 1.3.1 formu. |
| kare 2:25 | Xcode Cloud sekmesi | aday değil: konu dışı | Sessiva sayfasında yalnız sekme olarak görünüyor. |
| kare 2:25 | forms.gle destek URL'si | aday değil: konu dışı | Support URL alanında görünüyor. |
| açıklama | #appstore #appyapmachallenge #vibecoding | aday değil: genel kavram | Açıklamadaki etiketler. |
| linkli sayfa | apple.com / appstoreconnect.apple.com | App Store Connect | Bağlantılı sayfa appstoreconnect.apple.com/apps. |
## Kareden okunanlar
- 0:00: Yorum yanıtı: 'Nasıl Google play store veya app storeye nasıl çıkarıyoruz' (kalbeislam).
- 0:39: App Store Connect uygulama listesi: Sessiva, Kombinly, kwikZap, Nox Calendar.
- 2:25: Sessiva iOS App Version 1.3.1: Description, Keywords, Support URL, Copyright alanları.
- 2:47: Liste: Ekran görüntüleri, Açıklamalar, Anahtar kelimeler, Kategori, Destek URL'leri, Gizlilik politikası linki, App Privacy soruları, App Review notları.
## Belirsizlikler
- Kare listesi yol olarak verildi, görseller yalnız ilk 60 karedir; son bölümler altyazı/OCR'dan okundu.
- Altyazıda 'eosbuild' yazıyor; eas build olarak yorumlandı.
- 'Add for Review' ifadesi muhtemelen 'Submit/Add for Review' butonudur.
- Yorumlar girişsiz alınamadı.
- Sözlük eşleşmeleri (Clash Display, Descript, Claude, Pyright vb.) videoda kullanılmıyor, bulanık eşleşme sayıldı.
- Bir app mağazası ekranında Transporter dışında SwiftUI, WWDC içerikleri yalnız Apple Developer uygulamasında görünüyor.
## Atlanan segment oranı
0/3 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://appstoreconnect.apple.com/apps | 0:39 | ekran | evet |
| http://www.apple.com | açıklama | açıklama | hayır |
| https://forms.gle/7Pv4q39cmBUcXxiPA | 2:25 | ekran | hayır |
| http://example.com | 2:27 | ekran | hayır |
| http://exemple.com | 2:25 | ekran | hayır |
| https://forms.gle/7Pv4q39cmBUcXxjPA | 2:25 | ekran | hayır |
## İş akışı
- 1. adım — Uygulamayı React Native ile geliştirme (Expo kullanımı) — araçlar: React Native, Expo
- 2. adım — Apple Developer hesabı açma (bireysel ya da şirket adına) — araçlar: Apple Developer
- 3. adım — App Store Connect'te yeni uygulama kaydı oluşturma (platform, ad, dil, SKU) — araçlar: App Store Connect
- 4. adım — Certificates, Identifiers & Profiles üzerinden Bundle ID oluşturma (com.tahiryildiz.uygulamaadi) — araçlar: Apple Developer
- 5. adım — Bundle ID seçip uygulamayı Create ile oluşturma — araçlar: App Store Connect
- 6. adım — Expo proje gereksinimlerini kontrol etme (Node.js, npm, Xcode) — araçlar: Node.js, npm, Xcode
- 7. adım — Cursor terminalinde iOS build başlatma — araçlar: Cursor, EAS Build
- 8. adım — Build tamamlanınca IPA dosyasını alma — araçlar: EAS Build
- 9. adım — Transporter'da Apple Developer hesabıyla giriş yapma ve IPA ekleme — araçlar: Apple Transporter, Apple Developer
- 10. adım — Verify ile doğrulama, ardından Deliver ile App Store Connect'e gönderme — araçlar: Apple Transporter
- 11. adım — App Store Connect'te yüklenen uygulamanın göründüğünü kontrol etme — araçlar: App Store Connect
- 12. adım — TestFlight'ta test sürümü dağıtma; bug ve crash kontrolü — araçlar: TestFlight
- 13. adım — Mağaza sayfası alanlarını doldurma (ekran görüntüleri, açıklama, anahtar kelimeler, destek URL) — araçlar: App Store Connect
- 14. adım — Apple'ın zorunlu alanlarını tamamlama (App Privacy, yaş derecelendirmesi, App Review notları) — araçlar: App Store Connect
- 15. adım — Add for Review ile incelemeye gönderme ve Apple kalite kontrolü — araçlar: App Store Connect
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
