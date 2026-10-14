## 1. Yapay zekâ görsel üretimiyle ürün kataloğu hazırla, arka planları kaldır ve e-ticaret sitesine toplu yükle
### X
**(a) Araçlar**
- `design-image-prompt-engineer` (alt ajan): Ürün kategorisi başına tutarlı stüdyo çekimi prompt şablonunu yazar.
- `gorsel-uret` skill + `tools/gorsel_uret.py`: Yerel ComfyUI'da `ac · uret · buyut · arkaplan · kapat` adımlarını yürütür; API maliyeti yoktur.
- `nano-banana-2` MCP: ComfyUI'ın başaramadığı ürünlerde yedek olarak kullanılır. Ücretlidir, en çok N görselle sınırlanır.
- `baoyu-compress-image`: Görselleri WebP'ye çevirir ve boyutlarını sabitler (örneğin ≤200 KB).
- `accessible-content:alt-text-design`: Her ürün için alt metni CSV'ye yazar.
- `otm-api-entegrasyon` (alt ajan): Mağaza REST API'sine kimlik doğrulamalı, sayfalı ve hız sınırlı toplu yükleme yapar. Mağaza WooCommerce ise yerine `WordPress Shopping Cart Engineer` kullanılır.

**(b) Sıra**
1. Ürün CSV'si (SKU, ad, kategori) hazırlanır; `design-image-prompt-engineer` kategori başına prompt şablonu yazar.
2. `gorsel_uret.py ac → uret` toplu üretim yapar, ardından `buyut` çalışır. Başarısız ürünler `nano-banana-2` ile yeniden üretilir (en çok N).
3. `gorsel_uret.py arkaplan` şeffaf PNG çıkarır, sonra `kapat` çalışır.
4. `baoyu-compress-image` WebP'ye çevirir ve tek boyuta getirir.
5. `alt-text-design` ile alt metinler CSV'ye eklenir.
6. `otm-api-entegrasyon` ile yükleme betiği yazılır. Betik SKU anahtarıyla idempotent çalışır ve önce dry-run yapar. Sırayla: önce staging'e 5 ürün, onay gelirse tümü. Oluşan ürün ID'leri geri alma listesine yazılır.

**(c) Kapılar**
- **Lisans:** ComfyUI model checkpoint'inin ticari kullanım koşulu okunur (örneğin FLUX.1-dev ticari kullanıma kapalı).
- **Yanıltıcı reklam:** Görsel gerçek ürünü doğru göstermelidir. Örneklem görseller Read ile göz kontrolünden geçer.
- **Maliyet:** Ücretli API çağrısı için sayısal tavan (N) konur.
- **Sır:** API anahtarı yalnız ortam değişkeninden okunur, hiçbir çıktıda basılmaz.
- **Erişilebilirlik:** Alt metni boş ürün yüklenmez.
- **Yükleme:** Dry-run ve staging zorunludur; ikinci çalıştırmada tekrar kayıt oluşmamalıdır.
### Y
**(a) Araçlar**
- `departman-diger` (skill): görsel üretim işi bu yöneticiye düşüyor, araç sırasını o belirliyor.
- `gorsel-uret` (skill) ve `python tools/gorsel_uret.py` (ac · uret · arkaplan · kapat): yerel ComfyUI ile üretim ve arka plan silme yapılır, API maliyeti çıkmaz.
- `design-image-prompt-engineer` (alt ajan): ürün başına tutarlı stüdyo fotoğrafı istemlerini yazar.
- `jev` (skill): yüzlerce görselde "arka plan temiz mi, ürün doğru mu" sorusunu toplu puanlar; elle bakmak gerekmez.
- `baoyu-compress-image` (skill): WebP'ye çevirir ve dosya boyutunu küçültür.
- `accessible-content:alt-text-design` (skill): her ürün görseline alt metin yazar.

**(b) Sıra**
1. `departman-diger` açılır. Ürün listesinden (CSV) her ürün için istem `design-image-prompt-engineer` ile yazılır.
2. `gorsel_uret ac`, ardından ürün başına `uret`. Önce 3 ürünlük bir deneme yapılır, sonra hepsi üretilir.
3. `gorsel_uret arkaplan` ile toplu arka plan silinir, sonra `kapat`.
4. `jev` toplu puan verir. Eşiğin altında kalanlar 2. adıma geri döner.
5. `baoyu-compress-image` ile WebP'ye çevrilir. Alt metinler `alt-text-design` ile yazılır.
6. Siteye toplu yükleme için katalogda hazır bir araç **yok**. Mağazanın API'si ya da CSV içe aktarması için kısa bir betik yazılır. Mağaza platformu belirsiz, bu bir varsayım. Önce 3 ürünle deneme yükleme (dry-run) yapılır.

**(c) Kapılar**
- **Maliyet:** Yerel ComfyUI yetmezse fal veya nano-banana yedeği devreye girer. Bunun için sayısal bir tavan konur, örneğin "en çok N görsel".
- **Güvenlik:** Mağaza API anahtarı ortam değişkeninden okunur, değeri hiçbir yere yazdırılmaz.
- **Kalite:** `jev` eşiği ve 3 ürünlük deneme yüklemesi.
- **Erişilebilirlik:** Her görselde alt metin bulunmalı.
- **KVKK:** Görsellerde insan figürü yoksa geçerli değil.

## 2. Go ile yazılmış WebSocket sohbet servisi: yatay ölçekleme, yük testi ve Docker dağıtımı
### X
**(a) Araçlar**
- `dil-go` (alt ajan): idiomatic hub ve handler kodu yazar.
- `dil-websocket` (alt ajan): heartbeat, yeniden bağlanma ve geri basınç (backpressure) tasarımı.
- `be-yatay-olcekleme` (alt ajan): durumsuz düğümler ve düğümler arası pub/sub katmanı (ör. Redis).
- `ecc:golang-testing` (skill): tablo tabanlı testler ve `-race` ile koşum.
- `qa-yuk-testi` (alt ajan): k6 senaryosu, kademeli artış profili ve geç/kal eşikleri.
- `ecc:docker-patterns` (skill): çok aşamalı Dockerfile ve compose ile çok kopyalı kurulum.

**(b) Sıra**
1. `departman-diger` (Go dil uzmanlığı) açılır. `be-yatay-olcekleme` ile ölçekleme mimarisi kararı verilir.
2. `dil-websocket` ile protokol, heartbeat ve backpressure kuralları belirlenir.
3. Önce test (`ecc:golang-testing`), sonra kod (`dil-go`).
4. `ecc:docker-patterns` ile imaj hazırlanır. Compose 3 kopya + Redis + `ops-nginx-ters-vekil` (WebSocket upgrade) ile ayağa kalkar.
5. `qa-yuk-testi` ile k6 koşulur: bağlantı sayısı, p95 gecikme, hata oranı.
6. `departman-surec-git-yayin` ile commit ve CI.

**(c) Kapılar**
- **Test:** `go test -race` yeşil olmalı. Bir düğümden gönderilen mesajın başka düğüme ulaştığını gösteren entegrasyon testi gerekir.
- **Yük:** k6'da eşikler tutmalı (p95 < X ms, hata < %1). Sayılar varsayım, kabul ölçütü yoksa DUR raporu verilir.
- **Güvenlik:**
  - `sec-docker-guvenlik`: imaj root olmayan kullanıcıyla çalışmalı ve içinde sır bulunmamalı.
  - `semgrep` CLI: gosec kurallarıyla statik tarama.
  - WebSocket Origin kontrolü ve kimlik doğrulama.
- **KVKK:** Sohbet içerikleri loglara yazılmamalı.
### Y
**(a) Araçlar**
- `dil-websocket` (alt ajan): Hub tasarımını yapar: heartbeat, backpressure, düğümler arası fan-out için Redis pub/sub.
- `ecc:golang-testing`: Tablo tabanlı testler ve httptest ile WebSocket entegrasyon testi yazar; testler `go test -race` ile koşar.
- `ecc:docker-patterns`: Multi-stage Dockerfile (distroless, nonroot) ve compose dosyası (redis + 3 chat + nginx) hazırlar.
- `ops-nginx-ters-vekil` (alt ajan): Upgrade/Connection başlıklarını, `proxy_read_timeout` değerini ve `least_conn` dengelemeyi ayarlar.
- `qa-yuk-testi` (alt ajan): k6 ile WebSocket senaryosu, kademeli yük profili ve geçme eşikleri tanımlar.
- `sec-docker-guvenlik` (alt ajan): İmajda root kullanıcı, gömülü sır ve şişkin katman olup olmadığını denetler.

**(b) Sıra**
1. `dil-websocket` hub'ı tasarlar:
   - düğüm başına bağlantı kaydı ve Redis pub/sub,
   - ping/pong ile yazma deadline'ı,
   - sınırlı gönderim tamponu (yavaş istemci düşürülür),
   - azami mesaj boyutu,
   - el sıkışmada Origin ve token kontrolü.
2. `ecc:golang-testing` testleri yazar: önce hub birim testleri, ardından iki hub'ın Redis üzerinden çapraz teslim testi. Tümü `go test -race` ile koşar.
3. `ecc:docker-patterns` Dockerfile'ı (`CGO_ENABLED=0`, nonroot) ve compose dosyasını yazar. SIGTERM'de bağlantılar boşaltılarak kapanılır.
4. `ops-nginx-ters-vekil` WebSocket proxy ayarını yapar. Durum Redis'te tutulduğu için sticky session gerekmez.
5. `qa-yuk-testi` k6 testini önce 1, sonra 3 replikaya karşı koşar; böylece ölçeklemenin işe yaradığı kanıtlanır. Eşikler: teslim p95 < X ms, hata oranı < %1.
6. `sec-docker-guvenlik` incelemesi yapılır, ardından rolling update ile dağıtılır.

**(c) Kapılar**
- **Test:** `-race` temiz olmalı, düğümler arası teslim testi yeşil olmalı. Bağımlılıklar `govulncheck` ile taranır.
- **Yük:** k6 eşikleri geçilmeli; 3 replikada kapasite artışı ölçülmeli.
- **Güvenlik:** WebSocket kimlik doğrulaması ve Origin kontrolü (CSWSH'ye karşı), bağlantı ve mesaj hız sınırı, imajda sır olmaması, nonroot imaj.
- **KVKK:** Sohbet içeriği kişisel veridir. Mesaj gövdeleri loglanmaz ve saklama süresi tanımlanır.

## 3. React Native uygulaması: çevrimdışı senkron, push bildirim, hata izleme ve CI ile mağaza yayını
### X
**(a) Araçlar**
- `expo:expo-data-fetching` (skill): veri çekme ve çevrimdışı önbellek katmanı.
- `Realtime Collaboration Engineer` (alt ajan): çevrimdışı öncelikli senkron ve çakışma çözümü.
- `mob-push-bildirim` (alt ajan): APNs/FCM token akışı, izin isteme zamanlaması, bildirim içeriği.
- `sentry-react-native-sdk` (skill): hata izleme ve source map yükleme.
- `expo:eas-app-stores` (skill): eas.json, imzalama, sürüm numaraları, mağazaya gönderim.
- `expo` (MCP): EAS build durumu ve doküman.

**(b) Sıra**
1. `departman-diger` (mobil) açılır. Senkron ve çakışma modeli `Realtime Collaboration Engineer` ile kararlaştırılır.
2. Yerel depo ve kuyruk `expo:expo-data-fetching` ile yazılır. Test önce yazılır.
3. `mob-push-bildirim` ile token kaydı ve bildirim işleme.
4. `sentry-react-native-sdk` kurulur ve source map yüklemesi ayarlanır.
5. `expo:eas-app-stores` ile eas.json ve CI iş akışı (`gh`) hazırlanır. Önce dahili test kanalına (TestFlight / internal track) gönderilir.
6. `expo` MCP ile build durumu izlenir. Mağaza yayını bu adıma kadar hazırlanır; mağazaya göndermek dışarıya açık bir işlem olduğu için gönderim kullanıcı onayıyla yapılır.

**(c) Kapılar**
- **Test:** `ecc:react-testing` ile senkron kuyruğu, çakışma ve tekrar deneme testleri. Uçak modunda çalıştırma denemesi gerekir.
- **Güvenlik:**
  - Push token ve Sentry DSN'i repoya konmaz.
  - `sec-cikis-oncesi-guvenlik` ile yayın öncesi kontrol listesi.
- **KVKK:**
  - Sentry'de `sendDefaultPii:false` ve kişisel veri süzme açık olmalı.
  - Push izni açık rızaya bağlanır.
  - `policy-monitor` ile aydınlatma metni ve mağaza gizlilik etiketleri kontrol edilir.
- **Erişilebilirlik:** Katalogda mobil a11y aracı **yok**. VoiceOver ve TalkBack ile elle kontrol edilir.
- **frontend-craft:** Bu skill web arayüzüne özgü, bu yüzden atlandı (gerekçesi bu satır).

Bu planlar yalnız araç katalog listesindeki adlarla hazırlandı; departman skill'leri, ajan tanımları ve dosyalar açılmadı. Hiçbir şey kurulmadı veya çalıştırılmadı. İş 1'de mağaza platformu bilinmediği için yükleme adımı varsayıma dayanıyor. İş 2'deki yük eşikleri de kabul ölçütü olmadan uydurma sayılar.
### Y
**(a) Araçlar**
- `Realtime Collaboration Engineer` (alt ajan): Offline-first senkronu tasarlar: yerel depo (expo-sqlite), outbox kuyruğu, çakışma kuralı.
- `mob-push-bildirim` (alt ajan): APNs/FCM token yaşam döngüsünü, izin isteme zamanlamasını ve payload yapısını tasarlar.
- `sentry-react-native-sdk`: Hata izlemeyi kurar; release'i sürüm ve build numarasıyla eşler, source map'leri yükler.
- `expo:eas-app-stores`: `eas.json`, imzalama, sürüm/build numarası ve mağaza gönderimini (submit) ayarlar.
- `gh` CLI: GitHub Actions'ta lint, test ve `eas build --non-interactive` adımlarını kurar ve izler.
- `sec-kvkk-gdpr-kontrol` (alt ajan): Push token, cihaz kimliği ve Sentry verisinin veri akışını, rızasını ve saklama süresini eşler.

**(b) Sıra**
1. `Realtime Collaboration Engineer` senkronu tasarlar:
   - idempotent mutation ID,
   - last-write-wins ya da sunucu sürüm numarası,
   - ağ geri gelince üstel geri çekilmeyle (backoff) boşaltma.
   Çakışma senaryoları Jest testine dökülür.
2. `mob-push-bildirim` push akışını kurar: izin bağlamsal anda istenir, token sunucuya kaydedilir ve geçersiz token'lar temizlenir.
3. `sentry-react-native-sdk` kurulur (`sendDefaultPii: false`) ve EAS build sırasında source map'ler yüklenir.
4. `gh` ile CI kurulur: PR'da lint ve test, main dalında EAS preview build.
5. `expo:eas-app-stores` ile production profili ayarlanır, sürüm otomatik artırılır, TestFlight ve Play iç test kanalına submit edilir.
6. `sec-kvkk-gdpr-kontrol` incelemesi yapılır. iOS PrivacyInfo ve Play Data Safety formları doldurulur. Ardından aşamalı yayın yapılır.

**(c) Kapılar**
- **Test:** Offline → online geçişi ve çakışma Jest testleri CI'da yeşil olmalı. Gerçek cihazda uçak modu denemesi elle yapılır.
- **Güvenlik:** İmza anahtarları ve EAS token'ı yalnız CI secret'larında tutulur, log'a basılmaz.
- **KVKK:** Push ve hata izleme için aydınlatma metni hazırlanır. Sentry'ye kişisel veri gitmez.
- **Erişilebilirlik:** Bu iş için ayrı araç seçilmedi. `accessibilityLabel` ve ekran okuyucu kontrolü elle yapılır.
- **Maliyet:** EAS build ve Sentry kotası için sayısal tavan konur (en çok N build).

Eşleşen müdür skill'leri açılmadı ve katalog dışı ek sorgu yapılmadı; planlar adaylar ve bilinen araçlarla yazıldı. İşte en büyük risk modelin ticari lisansı, işte offline senkronda çakışma kuralının seçimi; ikisi de uygulamaya geçmeden netleşmeli.

## 4. Monorepo'da git dal stratejisi, CI'da yalnız etkilenen projeler ve sürüm notları otomasyonu
### X
**(a) Araçlar**
- `git-dal-stratejisi` (ajan): trunk tabanlı akış, kısa ömürlü dal, dal adı kuralı ve merge/rebase kararını verir.
- `git-monorepo-etkilenen` (ajan): bağımlılık grafiğinden etkilenen projeleri bulur (nx affected / turbo --filter / yol filtresi) ve önbelleği kurar.
- `git-ci-boru-hatti` (ajan): build/test/lint workflow'unu yazar; etkilenen proje listesini CI matrisine bağlar.
- `dok-degisiklik-gunlugu` (ajan): conventional commit'lerden proje başına sürüm notu üretir.
- `gha-security-review` (skill): workflow güvenliğini denetler (permissions, pull_request_target, action'ların SHA ile sabitlenmesi).
- `gh` (CLI): main koruması, zorunlu check'ler, PR ve release işlemleri.

**(b) Sıra**
1. `departman-surec-git-yayin` adım 1, `git-dal-stratejisi`: dal modeli ve commit kuralı (conventional + scope = proje adı). Varsayım: monorepo aracı (nx/turbo/yok) repodan okunur.
2. `git-monorepo-etkilenen`: etkilenen projeleri hesaplar. Taban `origin/main`, merge-base üzerinden alınır.
3. `git-ci-boru-hatti`: PR'da yalnız etkilenenler koşar. main'de ve gecelik koşuda tam suite güvenlik ağı olur.
4. `dok-degisiklik-gunlugu`: tag'lenen projenin commit'lerinden CHANGELOG ve release notu üretir. Kayıt `gh release create` ile açılır.
5. `gha-security-review`: tüm workflow'ları denetler.
6. `gh`: main koruması ve zorunlu check'ler (`git-dal-koruma-kurali` önerisi, `gh api` ile uygulanır).

**(c) Kapılar**
- Test: tek pakete kasıtlı değişiklik yapılır. Yalnız o paket ve ona bağımlı olanlar koşmalı. Kök config değişince tam suite koşmalı. "0 proje etkilendi" sonucu yanlış negatif sayılır ve CI kırmızıya düşer.
- Güvenlik: push'tan önce sır taraması (`departman-guvenlik` adım 1, gitleaks). Ardından `gha-security-review`.
- Yayın: kırmızı CI'da merge ve release yok. Kullanıcı istemeden push/deploy yok.
### Y
**(a) Araçlar**
- `departman-surec-git-yayin` (skill): Git/CI/yayın işinde araçların hangi sırayla kullanılacağını belirler.
- `git-dal-stratejisi` (ajan): Dal adlandırmasını, trunk mı release dalı mı seçimini, merge ya da rebase kararını verir.
- `git-monorepo-etkilenen` (ajan): Bağımlılık grafiğinden etkilenen projeleri çıkarır ve önbelleği planlar.
- `git-ci-boru-hatti` (ajan): Etkilenen projeleri bir matrise dönüştüren build/test/lint workflow'unu yazar.
- `dok-degisiklik-gunlugu` (ajan): Conventional commit'lerden proje başına sürüm notu üretir. Araç (changesets ya da release-please) seçimi de burada yapılır, ikisi de katalogda yok.
- `gha-security-review` (skill): Workflow izinlerini, `pull_request_target` kullanımını ve action pinlemeyi denetler.

**(b) Sıra**
1. `departman-surec-git-yayin` ile araç sırası okunur.
2. `git-dal-stratejisi` ile dal modeli ve commit kuralı belirlenir. Bu karar dalga.md dosyasına yazılır.
3. `git-monorepo-etkilenen` ile proje grafiği ve "etkilenen" hesabı çıkarılır. Komut ilk olarak dry-run modunda koşar.
4. `git-ci-boru-hatti` etkilenen listeden matris kuran workflow'u yazar.
5. `dok-degisiklik-gunlugu` etiket ile commit'ten proje başına release notes adımını ekler.
6. `gha-security-review` denetimi çalışır, ardından `gh` CLI ile PR açılır ve CI izlenir.

**(c) Kapılar**
- Test: Tek bir pakete dokunan sahte bir PR açılır. Yalnız o paket ve ona bağlı olanlar koşmalı. Paylaşılan bir dosyaya dokunulduğunda tüm projeler koşmalı.
- Güvenlik: `gha-security-review` çalışır. Token izinleri en dar seviyeye çekilir.
- Dal koruma: Required check'ler, etkilenen projeler matrisinin özet işine bağlanır.
- Erişilebilirlik ve KVKK: yok.

## 5. Startup yatırım sunumu: finansal model, pazar araştırması ve pptx slaytlar
### X
**(a) Araçlar**
- `ecc:investor-materials` (skill): deck, model ve özet metninin birbiriyle tutarlı kalmasını sağlar.
- `deep-research` (skill): kaynaklı TAM/SAM/SOM, rakip ve trend araştırması yapar.
- `urn-finans-plani` (ajan): gelir sürücüleri, maliyet, runway ve 3 senaryo kurar.
- `dok-xlsx-tablo` (ajan): formüllü xlsx modeli kurar; varsayımlar tek sayfada durur.
- `example-skills:pptx` (skill): .pptx üretir ve küçük resim (thumbnail) ile kontrol eder.
- `fact-checker` (skill): deck'teki her pazar rakamını kaynağa karşı doğrular.

**(b) Sıra**
1. `ecc:investor-materials`: anlatı iskeleti kurulur (problem → çözüm → pazar → model → traction → ekip → istek). Şirket verisi (gelir, maliyet, ekip) kullanıcıdan gelir; yoksa DUR raporu yazılır.
2. `deep-research`: pazar büyüklüğü bottom-up hesaplanır, her rakam kaynak ve tarih taşır. En fazla 30 web araması.
3. `urn-finans-plani`, ardından `dok-xlsx-tablo`: 36 aylık model, birim ekonomisi, runway ve hassasiyet tablosu.
4. `example-skills:pptx`: slayt başına bir fikir. Rakamlar xlsx'ten alınır, elle yazılmaz.
5. `fact-checker`: deck ↔ xlsx ↔ kaynak üçlü kontrolü.
6. Thumbnail ile görsel kontrol yapılır (taşma, hiyerarşi); düzeltme turu.

**(c) Kapılar**
- Tutarlılık: deck'teki her sayı bir xlsx hücresine eşlenir. Bir sapma bile kapanışı engeller.
- Kaynak: kaynaksız pazar iddiası yazılmaz. Projeksiyonlar "ileriye dönük" ibaresi taşır.
- Erişilebilirlik: kontrast, görsellerde alt metin, okuma sırası (`example-skills:pptx` kontrolü).
- Gizlilik/KVKK: müşteri adları ve kişisel veri, izin yoksa anonimleştirilir.
- Sapma: departmanın `wowerpoint` adımı yerine `pptx` seçildi, çünkü çıktı .pptx dosyası. `humanizer` atlandı; deck metni kısa maddelerden oluşuyor ve öncelik rakam doğrulamasında.
### Y
**(a) Araçlar**
- `departman-belge` (skill): pptx/xlsx üretimi için araç sırasını verir.
- `urn-finans-plani` (ajan): Gelir sürücülerini, maliyetleri, runway'i ve üç senaryoyu modeller.
- `brave-search` (MCP): Pazar büyüklüğü, rakipler ve emsal yatırım turları için güncel veri bulur.
- `okuyucu` (ajan, sonnet): Arama sonuçlarını kaynaklı özetler. Ana bağlama ham sayfa girmez.
- `example-skills:pptx` (skill): Slaytları üretir ve küçük resim (thumbnail) ile görsel kontrol yapar.
- `markitdown` (MCP): Bitmiş pptx'teki metni çıkarır. Rakamlar modelle karşılaştırılır.

**(b) Sıra**
1. `departman-belge` ile araç sırası okunur.
2. `okuyucu` ajanı `brave-search` ile TAM/SAM/SOM, rakip ve emsal verisini toplar. En çok 20 arama yapılır ve her rakamın yanında kaynak URL'si olur.
3. `urn-finans-plani` 36 aylık modeli, varsayım sayfası ve senaryolarla kurar.
4. Sunum akışı belirlenir: problem, çözüm, pazar, iş modeli, traction, finans, ekip, istek. Her slaytta tek fikir olur.
5. `example-skills:pptx` ile deste üretilir ve küçük resim kontrolü yapılır.
6. `markitdown` slayt metnini çıkarır ve rakamlar modelle eşleştirilir.

**(c) Kapılar**
- Doğruluk: Modelde basit bir kendi kendine kontrol olur: gelir eksi gider kümülatif nakdi vermeli, runway nakdi aylık yakıma bölünce çıkmalı. Slayttaki ve modeldeki rakamlar `markitdown` ile birebir tutmalı.
- Kaynak: Kaynaksız pazar rakamı kullanılmaz. `okuyucu` çıktısından örneklem alınarak doğrulama yapılır.
- Maliyet: Arama tavanı en çok 20'dir.
- Erişilebilirlik: Slaytta kontrast ve okunabilir punto aranır. Ayrı bir araç yok, bu kontrol `example-skills:pptx` görsel kontrolü içinde yapılır.
- KVKK: yok, kişisel veri yok.

## 6. Unity oyununa çok oyunculu ağ senkronu, hile koruması ve sunucu barındırma
### X
**(a) Araçlar**
- `unity` (MCP): Unity sürümünü okur, sahne/NetworkObject kurulumunu yapar, play mode'da host + 2 istemci denemesi koşturur.
- `ara-teknoloji-secimi` (ajan): netcode kütüphanesini (NGO / Mirror / FishNet) ve barındırmayı (kendi VPS'te headless server ya da yönetilen hizmet) maliyet ve lisansla karşılaştırır.
- `oyn-ag-senkronu` (ajan): otoriter sunucu, tick hızı, delta snapshot, prediction/reconciliation ve lag compensation tasarımı yapar.
- `sec-tehdit-modelleme` (ajan): hile vektörleri için STRIDE modeli çıkarır (hız/ışınlanma, paket oynama, cooldown/hasar sahteciliği, bellek düzenleme).
- `sec-docker-guvenlik` (ajan): headless Linux server imajını denetler (root olmayan kullanıcı, ince imaj, sır yok).
- `qa-yuk-testi` (ajan): bot istemcilerle yük testi ve geçme eşikleri.

**(b) Sıra**
1. `unity` MCP ile proje sürümü ve mevcut ağ kodu okunur. `ara-teknoloji-secimi` kütüphaneyi ve barındırmayı seçer, lisanslar okunur.
2. `oyn-ag-senkronu`: senkron spec'i çıkar (neyin sunucuda, neyin istemcide tahmin edildiği).
3. `sec-tehdit-modelleme`: her vektör bir sunucu doğrulamasına bağlanır (hız/pozisyon sınırı, hasar ve cooldown sunucuda, RPC rate limit).
4. Kod ana oturumda yazılır, sahne `unity` MCP ile kurulur. Play mode testleri 150 ms gecikme / %2 kayıp simülasyonuyla koşar.
5. Headless Linux server build alınır, Docker imajı `sec-docker-guvenlik` ile denetlenir. CI ve deploy `departman-surec-git-yayin` sırasıyla yapılır.
6. `qa-yuk-testi`: en fazla N bot, en fazla M dakika. Eşikler: tick süresi, p95 RTT, rubber-band oranı.

**(c) Kapılar**
- Test: reconciliation ve otorite kuralları için Unity Test Framework play mode testleri. Hile senaryosu testi: sahte hız paketi gönderilir, sunucu reddetmeli.
- Güvenlik: istemciye güvenilmez, kontrol listesi `sec-tehdit-modelleme`'den gelir. Sunucuda yalnız oyun UDP portu açık olur. Root'suz imaj (`sec-docker-guvenlik`).
- Maliyet: barındırma ve yük testi ücretli. Başlamadan önce aylık sunucu tavanı ve bot sayısı tavanı yazılır.
- KVKK: oyuncu kimliği ve IP kaydedilecekse saklama süresi belirlenir. Bu durumda ek araç olarak `sec-kvkk-gdpr-kontrol` gerekir.
- Sapma: `mod-atolyesi` ve `universal-modder` atlandı; ikisi de başkasının oyununu modlamak için, burada kendi oyunun geliştiriliyor.

Bu yanıtta yalnız plan var; repo, Unity projesi ve şirket verisi incelenmedi.

Önceden bilmen gereken riskler:
- **5. iş:** Rakamlar sende yoksa iş ilk adımda durur.
- **6. iş:** İstemci tarafı anti-cheat (EAC vb.) biler
### Y
**(a) Araçlar**
- `unity` (MCP): Unity editöründe sahneyi, prefab'ları ve betikleri yönetir.
- `oyn-ag-senkronu` (ajan): Otoriter sunucu, tahmin/uzlaştırma ve lag compensation tasarlar. Netcode kütüphanesi (NGO, Mirror ya da FishNet) burada seçilir, katalogda yok.
- `oyn-oyun-motoru-script` (ajan): C# oyun mantığını ve RPC'leri yazar.
- `sec-tehdit-modelleme` (ajan): Hile yüzeyi için STRIDE çıkarır: istemci otoritesi, speed/teleport hilesi, sahte RPC.
- `DevOps Automator` (ajan): Headless Linux server build'i, Docker imajı ve barındırma seçimini yapar.
- `sec-zero-trust-ag` (ajan): Sunucu ağını kurar. Yalnız oyun portu açık kalır, yönetim erişimi kısıtlanır.

**(b) Sıra**
1. Bu iş katalogda yönetici skill'i olmayan `departman-diger` kapsamında. Sıra doğrudan ajanlarla kurulur.
2. `oyn-ag-senkronu` otorite modelini, tick hızını ve senkron edilecek durum listesini belirler. Bu karar dalga.md dosyasına yazılır.
3. `sec-tehdit-modelleme` hile vektörlerini sıralar ve sunucu tarafı doğrulama kurallarını çıkarır.
4. `oyn-oyun-motoru-script` ile `unity` MCP birlikte NetworkObject'leri ve sunucu yetkili hareket/hasar akışını kurar.
5. `DevOps Automator` dedicated server build'ini (`-batchmode -nographics`), Docker imajını ve sunucu kurulumunu hazırlar. Ücretli sunucu varsa sayısal bir tavan konur, örneğin en çok 1 VPS.
6. `sec-zero-trust-ag` ile güvenlik duvarı ve SSH sertleştirmesi yapılır, ardından canlı deneme koşar.

**(c) Kapılar**
- Test:
  - Play Mode'da çok örnekli koşu yapılır, 150 ms gecikme ve %2 paket kaybı simüle edilir.
  - Sapma eşiği ve yeniden uzlaştırma doğrulanır.
  - Sunucu tarafı doğrulama kuralları için EditMode birim testleri yazılır. Testler bir alt ajanda koşar.
- Güvenlik ve hile:
  - `sec-tehdit-modelleme` listesindeki her vektörün bir testi olur. Örneğin hız sınırı aşan input reddedilmeli.
  - İstemci hiçbir durumda otorite olmaz.
- Sunucu: `sec-zero-trust-ag` kontrol listesi uygulanır. Sır taraması `gitleaks` ile yapılır, katalogda var ama 6 aracın dışında kaldı.
- KVKK: Oyuncu hesabı ya da IP logu tutulacaksa saklama süresi ve aydınlatma metni gerekir. Katalogda KVKK aracı yok.
- Erişilebilirlik: yok, ağ katmanında geçerli değil.

Kontrol etmediklerim: Seçimleri yalnız kancanın verdiği katalogla sınırladım. Planlardaki changesets/release-please, NGO/Mirror/FishNet ve `departman-diger` katalogda olmadığı için yalnız seçenek olarak geçiyor. Unity'nin güncel barındırma servislerinin durumunu araştırmadım.

Risk: `unity` MCP açık bir editö
