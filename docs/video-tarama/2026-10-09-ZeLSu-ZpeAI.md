# Claude Code Çalışırken Para Kazandıran Eklenti (Ücretsiz)
## Künye
Claude Code Çalışırken Para Kazandıran Eklenti (Ücretsiz) · İsa Nurdoğdu · süre: 0:34 · tr-orig · https://youtu.be/ZeLSu-ZpeAI · şema 2
motor: parti 2026-10-09-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 17132 tk · claude-haiku-5-5: claude-haiku-5-5 · 41226 tk
## Özet
İsa Nurdoğdu, Kickbacks adlı ücretsiz VS Code eklentisini tanıtıyor. Claude Code uzun işlem yaparken bekleme ekranında reklam gösterilir ve reklam görüntülenince kullanıcı gelir elde eder. Kurulum Claude'a yapıştırılan bir curl komutuyla yapılır. Videoyu kırmızı ışıkta beklerken para kazanmaya benzetiyor ve izleyiciyi yoruma 'claude' yazmaya çağırıyor.
## Bölümler
- 0:00 Giriş: bekleme süresi gelire dönüşüyor
- 0:04 Kickbacks.ai sitesi ve eklenti tanıtımı
- 0:07 Kurulum: Claude'a yapıştırılan komut
- 0:14 Bekleme ekranında reklam gösterimi
- 0:27 Kazanç ve kickbacks --init
- 0:30 Yoruma 'claude' yaz çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Kickbacks | yok | plugin | yok | Claude Code bekleme ekranında reklam gösterip geliri kullanıcıyla paylaşan ücretsiz VS Code eklentisi | 0:04 | Kickbacks adındaki ücretsiz VS COD eklentisini kuruyorsun (karede: Kickbacks.ai logosu ve 'GET PAID FOR WAITING' yazısı) |
| Claude Code | yok | CLI | yok | Uzun işlemin yapıldığı ve bekleme sırasında reklamın gösterildiği kodlama aracı | 0:00 | Cloud COD uzun bir işlem yaparken yine bekliyorsun (karede: Terminalde 'Migrate dashboard to App Router' görevi) |
| VS Code | yok | CLI | yok | Eklentinin kurulduğu kod editörü | 0:00 | ücretsiz VS COD eklentisini kuruyorsun |
| Claude | yok | CLI | yok | Kurulum komutunun yapıştırıldığı yapay zekâ asistanı | 0:07 | Just paste this into Claude — super easy. (karede: Yeşil kutuda 'Just paste this into Claude — super easy.' ve curl komutu) |
| Next.js | yok | teknik | yok | Terminalde App Router'a taşınan dashboard uygulamasının çatısı | 0:02 | import from next/navigation, App Router göçü (karede: useParams, useRouter from "next/navigation" ve app/orders/[id]/page.tsx) |
| SWR | yok | teknik | yok | Kod örneğinde veri çekmek için kullanılan kütüphane | 0:02 | import useSWR from "swr" (karede: import useSWR from "swr" satırı) |
| curl | yok | CLI | yok | Kickbacks vsix dosyasını indirmek için kullanılan komut | 0:07 | curl -L https://kickbacks.ai/vsix -o kickbacks.vsix (karede: Kopyalanabilir curl komutu) |
| Claude Sonnet | yok | teknik | yok | Ekranda sözlük eşleşmesi olarak görülen model adı | 0:07 | Sözlük eşleşmesi ekran 0:07 (karede: Bu karede Claude Sonnet yazısı net okunmuyor; yalnız Claude geçiyor) |
| Next.js dashboard'unu App Router'a taşıma | yok | prompt | yok | apps/dashboard uygulamasını App Router'a taşı; sipariş paneli şirketin yaşadığı yüzey, 3 uygulama daha olacağı için deseni ilk seferde doğru kur. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- https://isanurdogdu.com/kaynaklar/kickbacks — İsa Nurdoğdu'nun Kickbacks kaynak sayfası · aday: hayır · Kişisel kaynak sayfası; araç Kickbacks zaten aday, bağlantı araç servisi değil yönlendirme sayfası · sınıf: diğer
- https://isanurdogdu.com — Yaratıcının ana sayfası · aday: hayır · Referans sayfası; araç değil. · sınıf: diğer
- https://isanurdogdu.com/#kur — Yaratıcı sayfasındaki kurulum bölümü · aday: hayır · Referans sayfasının içi bağlantısı; araç değil. · sınıf: diğer
- https://db-ip.com — IP konum sorgulama servisi · aday: hayır · Videoda anılmıyor ve kullanılmıyor; yalnızca kickbacks.ai sayfasında bağlantılı. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kahraman başlık bölümü (Hero Section) ve altında karşılaştırma kartları | 'Get paid for waiting.' başlığı, 'WITHOUT KICKBACKS' ve 'WITH KICKBACKS' terminal kartları (karede: Koyu iki terminal kartı: Noodling .. ve Ramp · save time and money) | 0:07 | kare |
| Kopyala düğmeli kod bloğu (Copy Button Code Block) | Yeşil kutuda curl komutu ve Copy düğmesi (karede: Copy düğmeli curl komutu) | 0:07 | kare |
| Seçim kartı ve rozet (Radio Card, Badge) | Extension kartı, NEW şeridi, Surface targeting etiketi (karede: Extension kartı, işaretli radyo düğmesi, köşede NEW şeridi) | 0:07 | kare |
| Üst gezinme çubuğu (Navbar) | Logo ile Advertisers ve Users düğmeleri (karede: Sol üstte Kickbacks.ai logosu, sağda iki hap düğme) | 0:04 | kare |
| Kayan metin arka planı (Marquee / Ticker Background) | Arka planda sıralanmış reklam satırları (karede: Bulanık satırlar halinde reklam metinleri) | 0:04 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -L https://kickbacks.ai/vsix -o kickbacks.vsix | Kickbacks eklenti paketini indirir (karede: Yeşil kutuda curl -L https://kickbacks.ai/vsix -o kickbacks.vsix && code ...) | 0:07 | kare |
| kickbacks --init | Kickbacks kurulumunu başlatır | 0:28 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Reklam görüntülendiğinde kullanıcı gelir elde ediyor | 0:00 | özellik |
| Gelirin %50'si kullanıcıya gidiyor | 0:06 | sayısal |
| Geliştiricilere toplam 122.342 dolar kazandırılmış | 0:06 | sayısal |
| Bir sonraki uzun işlemden önce kurup denemeli | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Kickbacks eklentisi | Kickbacks | Kickbacks adındaki ücretsiz VS COD eklentisini kuruyorsun |
| konuşma 0:00 | Claude Code | Claude Code | Cloud COD uzun bir işlem yaparken yine bekliyorsun |
| konuşma 0:00 | VS Code | VS Code | ücretsiz VS COD eklentisini kuruyorsun |
| konuşma 0:00 | Kırmızı ışık benzetmesi | aday değil: genel kavram | kırmızı ışıkta beklerken para kazanmak gibi düşün |
| kare 0:02 | Next.js App Router göçü | Next.js | next/navigation içe aktarımı |
| kare 0:02 | useSWR | SWR | import useSWR from "swr" |
| kare 0:02 | @acme/ui ve @acme/types paketleri | aday değil: konu dışı | örnek terminal kodunda içe aktarım |
| kare 0:07 | curl komutu | curl | curl -L https://kickbacks.ai/vsix |
| kare 0:07 | Claude'a yapıştır talimatı | Claude | Just paste this into Claude — super easy. |
| kare 0:07 | Ramp reklamı | aday değil: başka adayın parçası (Kickbacks) | Ramp · save time and money |
| kare 0:14 | PromptZone reklamı | aday değil: başka adayın parçası (Kickbacks) | PromptZone ~ Where AI Builders Share & Learn |
| kare 0:14 | Kickbacks durum çubuğu | Kickbacks | Kickbacks ($0.19 today · $0.51) |
| ekran 0:27 | kickbacks --init | Kickbacks | kickbacks --init |
| açıklama | isanurdogdu.com/kaynaklar/kickbacks | aday değil: konu dışı | Yoruma claude yaz, bağlantıyı DM'den göndereyim |
| bağlantılı sayfa | db-ip.com | aday değil: konu dışı | Kickbacks.ai sayfasında geçen bağlantı |
| yorum | claude yorumları | Claude | Yorumlarda claude yazılı |
| kare 0:07 | Claude Sonnet | aday değil: konu dışı | Yalnızca sözlük eşleşmesinde geçiyor, karede görülmedi |
## Kareden okunanlar
- 0:00: Terminalde 'Migrate dashboard to App Router' istemi ve Thought for 2s
- 0:02: apps/dashboard/app/orders/[id]/page.tsx dosyası yazılıyor; useSWR ve next/navigation içe aktarımları
- 0:03: Koyu terminal çubuğu, K$ logosu ve $2,569 tutarı
- 0:04: Kickbacks.ai, GET PAID FOR WAITING
- 0:06: Get paid for waiting; 50% of the revenue goes to you; $122,342 earned by developers
- 0:07: Just paste this into Claude; curl -L https://kickbacks.ai/vsix -o kickbacks.vsix; Extension kartı
- 0:14: Kickbacks ($0.19 today · $0.51) durum çubuğu; PromptZone ~ Where AI Builders Share & Learn reklamı
- 0:32: 'claude' yazılı hap kutu ve Claude yaz linkini altyazısı
## Belirsizlikler
- Sözlük eşleşmesindeki Claude Sonnet ve Hermes Agent kareden doğrulanamadı.
- Karede görünen Go ve Go Live VS Code arayüzünün parçası, araç olarak kullanılmıyor.
- db-ip.com bağlantısı Kickbacks.ai sayfasından geliyor; videoda kullanıldığı görülmüyor.
- Kare 0:32 aslında yorum çağrısı gösteriyor; kickbacks --init OCR'da 0:27-0:28 geçiyor, karede doğrulanmadı.
- Ekranda görünen PromptZone reklamı; PromptZone'un araç olarak kullanılıp kullanılmadığı belirsiz.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://isanurdogdu.com/kaynaklar/kickbacks | açıklama | açıklama | hayır |
| Kickbacks.ai | 0:04 | ekran | evet |
| https://kickbacks.ai/vsix | 0:07 | ekran | evet |
| https://isanurdogdu.com | açıklama | açıklama | hayır |
| https://isanurdogdu.com/#kur | açıklama | açıklama | hayır |
| https://db-ip.com | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Claude Code'da uzun bir işlem (Next.js App Router göçü) başlatılıyor — araçlar: Claude Code, Next.js
- 2. adım — Bekleme süresinin gelire çevrileceği anlatılıyor — araçlar: Kickbacks
- 3. adım — Kickbacks.ai sitesi gösteriliyor — araçlar: Kickbacks
- 4. adım — Kurulum komutu Claude'a yapıştırılıyor — araçlar: Claude, curl
- 5. adım — Eklenti VS Code'a kuruluyor — araçlar: VS Code, Kickbacks
- 6. adım — Bekleme ekranında reklam görüntüleniyor ve günlük kazanç görülüyor — araçlar: Claude Code, Kickbacks
- 7. adım — kickbacks --init ile başlatma gösteriliyor — araçlar: Kickbacks
- 8. adım — Yoruma 'claude' yazma çağrısı yapılıyor — araçlar: yok
## Promptlar
- Next.js dashboard'unu App Router'a taşıma — apps/dashboard uygulamasını App Router'a taşı; sipariş paneli şirketin yaşadığı yüzey, 3 uygulama daha olacağı için deseni ilk seferde doğru kur.
ikinci göz KAPALI: --ikinci-goz yok
