## 1. Yapay zekâ görsel üretimiyle ürün kataloğu hazırla, arka planları kaldır ve e-ticaret sitesine toplu yükle
### X
**(a) Araçlar**
- `hermoso:hermoso-product-photoshoot`: ürün çekimi istemlerini tutarlı bir seri olarak kurar (ışık, açı, sahne).
- `img` (`img:gemini` / `img:openai`): görseli üretir. Ücretli API olduğu için çağrı tavanı zorunlu.
- `rembg` (Python, MIT): arka planı yerelde toplu kaldırır, API maliyeti yok.
- `baoyu-compress-image`: WebP'ye çevirir ve boyut varyantlarını üretir.
- `accessible-content:alt-text-design`: her ürüne alt metin yazar.
- `otm-api-entegrasyon` (alt ajan): mağaza REST API'sine toplu yükler. Kimlik doğrulama, sayfalama, hız sınırı ve SKU ile upsert'i yönetir.

**(b) Sıra**
1. `departman-diger` ve `hermoso-product-photoshoot` ile SKU listesinden istem şablonu çıkarılır. Stil 3 örnekle onaylanır.
2. `img` ile toplu üretim yapılır. Tavan en çok SKU×2 görsel, çıktılar `ham/` klasörüne gider.
3. `rembg` betiği `python -I` ile, ayrı bir dizinde koşar ve şeffaf PNG üretir.
4. `baoyu-compress-image` ile WebP ve srcset varyantları hazırlanır.
5. `alt-text-design` ile alt metinler yazılıp yükleme CSV'sine eklenir.
6. `otm-api-entegrasyon` önce staging'e 3 üründen oluşan bir deneme yükler, sonra toplu yükler. Canlı mağazaya yükleme onayla yapılır.

**(c) Kapılar**
- **Maliyet:** API çağrı sayacı ve "en çok N" tavanı.
- **Ürün sadakati:** üretilen görsellerin %10'u gerçek ürünle göz kontrolüyle karşılaştırılır (Read). Gerçek ürüne uymayan görsel tüketiciyi yanıltır.
- **Test:** idempotentlik testi. Aynı CSV iki kez yüklenince kopya ürün oluşmamalı.
- **Güvenlik:** API anahtarı yalnız env'de tutulur. Repo `sec-sir-tarayici` ile taranır.
- **Lisans:** `ara-lisans-kontrol` ile görsel modelinin ticari kullanım şartı ve rembg/u2net lisansları okunur.
- **Erişilebilirlik:** boş alt metin kalmayacak.
- **KVKK:** insan modeli kullanılmazsa yok.
### Y
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

## 2. Go ile yazılmış WebSocket sohbet servisi: yatay ölçekleme, yük testi ve Docker dağıtımı
### X
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
### Y
**(a) Araçlar**
- `be-yatay-olcekleme`: durumsuz düğümler ve düğümler arası yayın (Redis pub/sub ya da NATS) kararını verir.
- `dil-websocket`: heartbeat, backpressure, yavaş istemciyi kesme ve yeniden bağlanma desenlerini kurar.
- `dil-go-eszamanlilik`: goroutine sızıntısı, kanallar ve context iptalini denetler.
- `ecc:go-test`: `go test -race` ve iki düğümlü entegrasyon testini koşar.
- `qa-yuk-testi` (k6, `k6/ws`): rampalı yük senaryosu ve geçti/kaldı eşikleri kurar.
- `sec-docker-guvenlik`: çok aşamalı, non-root, distroless imajı denetler.

**(b) Sıra**
1. `departman-diger` ve `be-yatay-olcekleme` ile mimari kararı verilir: oturum Redis'te, yayın Redis pub/sub üzerinden.
2. `dil-websocket` ve `dil-go-eszamanlilik` ile hub/istemci goroutine'leri, ping/pong, `SetReadLimit` ve yazma tamponu sınırı yazılır.
3. `ecc:go-test` ile `-race` testi ve testcontainers'ta Redis ile "düğüm A'dan gelen mesaj düğüm B'ye ulaşır" testi koşar.
4. Dockerfile ve compose hazırlanır: 3 replika, nginx'te Upgrade başlıkları (`ops-nginx-ters-vekil`). `sec-docker-guvenlik` inceler.
5. `qa-yuk-testi` staging'de çalışır: 1k'dan 10k bağlantıya rampa, eşikler p95 gecikme ve hata oranı < %1.
6. `dil-go-pprof` ile yük altında heap ve goroutine profili alınır. Sızıntı yoksa iş kapanır.

**(c) Kapılar**
- **Test:** `-race`, entegrasyon testleri ve golangci-lint CI'da.
- **Güvenlik:** `sec-sast-kosucu` (gosec), govulncheck ve trivy ile imaj taraması. Ayrıca Origin kontrolü (CSWSH), handshake'te auth ve bağlantı başına hız sınırı.
- **Yük testi:** yalnız kendi staging ortamında koşar. k6 eşikleri tutmazsa CI kırmızı olur.
- **KVKK:** `sec-loglama-gizlilik` ile mesaj gövdesinin loga yazılmadığı denetlenir. Saklama süresi belirlenir.
- **Erişilebilirlik:** yok (arayüz yok).

## 3. React Native uygulaması: çevrimdışı senkron, push bildirim, hata izleme ve CI ile mağaza yayını
### X
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
### Y
**(a) Araçlar**
- `ecc:react-native-patterns`: Expo dev client ile proje yapısı ve desenleri belirler.
- WatermelonDB (MIT): yerel veritabanı ve pull/push senkron protokolü sağlar.
- `mob-push-bildirim` ile `expo-notifications`: APNs/FCM token'ı ve izin isteme zamanını yönetir.
- `sentry-sdk-setup` ile `sentry-setup-releases`: hata izleme kurar ve sourcemap'leri yükler.
- `qa-mobil-qa` (Maestro): çevrimdışı ve senkron akışları için e2e testleri.
- `expo:eas-workflows` ile `expo:eas-app-stores`: CI derlemesi ve mağazaya gönderim.

**(b) Sıra**
1. `departman-diger` ve `ecc:react-native-patterns` ile proje iskeleti ve gezinti kurulur.
2. WatermelonDB şeması ve senkronu yazılır: `lastPulledAt`, yazma kuyruğu, alan bazlı çakışma kuralı.
3. `mob-push-bildirim`: izin bağlamsal anda istenir. Token sunucuya gönderilir, kimlik bilgileri EAS credentials'ta tutulur.
4. `sentry-sdk-setup`: `sendDefaultPii: false` ve `beforeSend` ile maskeleme. EAS build'de sourcemap yüklenir.
5. `qa-mobil-qa` Maestro senaryosunu koşar: uçak modu → veri yaz → bağlan → senkron doğru mu, bildirime tıklayınca doğru ekran açılıyor mu.
6. `eas-workflows`: PR'da test ve lint, main'de build. `eas submit` önce TestFlight ve Play internal kanalına gider, ardından aşamalı yayın. Mağazaya gönderim onayla yapılır.

**(c) Kapılar**
- **Test:** çakışma çözümü için Jest birim testleri, Maestro e2e CI'da.
- **Güvenlik:** sırlar EAS secrets'ta, token'lar SecureStore'da. `sec-gitleaks-gecmis` ve `mukul975-mobile-security-paket` ile MASVS kontrolü.
- **KVKK:** `sec-kvkk-gdpr-kontrol` kullanılır. Push token ve cihaz kimliği kişisel veri sayılır, bu yüzden aydınlatma ve rıza gerekir. App Store privacy manifest ve Play Data safety formu doldurulur.
- **Erişilebilirlik:** `inclusive-interaction:touch-target-design` (dokunma hedefi 44/48 pt) ve `accessibilityLabel` kontrolü. Arayüze dokunduğu için kapanışta `frontend-craft` Bölüm 6 tur raporu verilir.

---
`departman-*` skill'leri ve `frontend-craft` yüklenmedi. Sebep: istek yalnız plan, iş yürütülmedi; her işte bunlar 1. adımda açılacak. Mağaza platformu (WooCommerce/Shopify), sohbet servisinin hedef bağlantı sayısı ve RN'de Expo kullanılıp kullanılmayacağı varsayım. Planlar bu varsayımlara göre değişebilir.

## 4. Monorepo'da git dal stratejisi, CI'da yalnız etkilenen projeler ve sürüm notları otomasyonu
### X
**(a) Araçlar** (`departman-surec-git-yayin` sırası)
- `ajan:git-dal-stratejisi`: dal adlandırma, trunk ya da kısa ömürlü dal, merge/rebase kuralı.
- `ajan:git-monorepo-etkilenen`: bağımlılık grafiği üzerinden yalnız etkilenen projeleri bulur, CI önbelleğini kurar.
- `ci-cd-and-automation` + `ajan:git-ci-boru-hatti`: iş akışı YAML'ını yazar ve yol filtreli matrisi kurar.
- `ajan:dok-degisiklik-gunlugu`: conventional commit'lerden proje başına sürüm notu üretir.
- `gh` CLI: PR, etiket ve release oluşturur; CI sonucunu okur.
- `gha-security-review`: workflow güvenliğini denetler (pull_request_target, sır sızıntısı, sabitlenmemiş action).

**(b) Sıra**
1. `ajan:git-dal-stratejisi` dal kuralını yazar, `git-dal-koruma-kurali` ile birlikte zorunlu kontrolleri ve CODEOWNERS'ı belirler.
2. `ajan:git-monorepo-etkilenen` proje grafiğini çıkarır, "değişen yol → etkilenen proje" eşlemesini kurar.
3. `ci-cd-and-automation` / `ajan:git-ci-boru-hatti` etkilenen projelere göre dinamik matris kurar ve önbellek ekler.
4. `ajan:dok-degisiklik-gunlugu` conventional commit kapsamından proje başına changelog ve sürüm artışı üretir.
5. `gh` etiket ve release taslağını oluşturur. Push ve yayın yalnız kullanıcı onayıyla yapılır.
6. `finishing-a-development-branch` ile kapanış; rapor ≤15 satır.

**(c) Kapılar**
- Test: Bir deneme PR'ında tek projeye dokunulur, yalnız o proje ve ona bağımlı projeler koşmalı. Kök dosya değişikliğinde tüm projeler koşmalı. Kanıt `gh run view` ile alınır.
- Güvenlik: Push öncesi `sec-gitleaks-gecmis` / `departman-guvenlik` adım 1 çalışır, workflow'lar için `gha-security-review`. Kırmızı CI varken yayın yok.
- KVKK: yok.
### Y
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

## 5. Startup yatırım sunumu: finansal model, pazar araştırması ve pptx slaytlar
### X
**(a) Araçlar** (`departman-belge` + `departman-arastirma-ogrenme`)
- `ecc:market-research` / `deep-research`: TAM/SAM/SOM ve rakip verisini kaynaklı toplar.
- `ajan:urn-finans-plani`: gelir sürücüleri, maliyet, runway ve senaryolar.
- `ajan:dok-xlsx-tablo`: formüllü finansal model (xlsx).
- `ecc:investor-materials`: yatırımcı anlatısı ve slayt akışı (problem → çözüm → pazar → model → talep).
- `ajan:dok-pptx-sunum`: pptx üretimi; her slaytta tek fikir.
- `fact-checker` + `humanizer`: rakam ve iddia doğrulaması, ardından AI izi temizliği.

**(b) Sıra**
1. `ecc:market-research` pazar boyutunu ve rakipleri kaynak bağlantılarıyla çıkarır. Web çağrısı en fazla N olacak; tavanı başlamadan yazacağım.
2. `ajan:urn-finans-plani` varsayım tablosunu ve 3 senaryoyu kurar.
3. `ajan:dok-xlsx-tablo` modeli formüllü xlsx'e döker; sabit sayı girilmez.
4. `ecc:investor-materials` anlatı akışını çıkarır, `ajan:dok-pptx-sunum` pptx'i üretir. Grafikler xlsx'ten beslenir.
5. `fact-checker` sunumdaki her rakamın kaynağını ve xlsx hücresini eşler.
6. `humanizer` metinleri temizler, `dok-markitdown-donusum` ile pptx geri okunup son kontrol yapılır.

**(c) Kapılar**
- Tutarlılık: pptx'teki her sayı xlsx hücresiyle eşleşmeli. Bunu küçük bir python-pptx + openpyxl betiğiyle karşılaştırırım; fark varsa sunum çıkmaz.
- Kaynak: Kaynaksız pazar rakamı yazılmaz (`fact-checker`).
- Erişilebilirlik: Slaytlarda kontrast ve alt metin kontrol edilir (`accessible-content:alt-text-design`).
- KVKK: Müşteri ya da çalışan kişisel verisi slayta girmez. Gerekirse `sec-kvkk-gdpr-kontrol` kullanılır.
### Y
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

## 6. Unity oyununa çok oyunculu ağ senkronu, hile koruması ve sunucu barındırma
### X
**(a) Araçlar** (`departman-diger` → oyun satırı)
- `mod-atolyesi` → `unity` MCP (yalnız CC): proje keşfi ve sahne/prefab düzenlemesi.
- `ajan:oyn-ag-senkronu`: sunucu otoriteli model, istemci tahmini, uzlaştırma, gecikme telafisi.
- `ajan:ara-kutuphane-secimi`: Netcode for GameObjects, Mirror ve FishNet arasında seçim (lisans, bakım, Unity sürümü).
- `ajan:sec-tehdit-modelleme`: hile yüzeyi için STRIDE (hız/ışınlanma, sahte RPC, bellek düzenleme).
- `ajan:ara-teknoloji-secimi` / `hetzner-deploy`: barındırma seçimi (yönetilen oyun sunucusu ya da kendi VPS'te headless Linux build).
- `ajan:qa-yuk-testi`: eşzamanlı oyuncu ve tick bütçesi yük testi.

**(b) Sıra**
1. `unity` MCP projeyi okur, `ajan:ara-kutuphane-secimi` ağ kütüphanesini seçer. Lisans rapora yazılır.
2. `ajan:oyn-ag-senkronu` senkron tasarımını çıkarır (tick hızı, durum mu girdi mi senkronu, interpolasyon).
3. `ajan:sec-tehdit-modelleme` hile modelini çıkarır. Sunucu tarafında girdi doğrulama, hız/menzil sınırı ve RPC hız sınırı konur.
4. `ajan:oyn-oyun-motoru-script` + `unity` MCP kodu yazar. TDD için Unity Test Framework (EditMode/PlayMode) kullanılır.
5. `ajan:ara-teknoloji-secimi` barındırmayı seçer. Headless sunucu build'i yapılır, `hetzner-deploy` ya da seçilen sağlayıcıya dağıtılır. Dağıtım onayla ve maliyet tavanıyla yapılır.
6. `ajan:qa-yuk-testi` bot istemcilerle yük testi koşar, gecikme ve paket kaybı simüle edilir.

**(c) Kapılar**
- Test: PlayMode testi, sunucunun geçersiz hareket/RPC'yi reddettiğini kırmızı→yeşil kanıtlamalı. Yük testinde tick süresi eşik altında kalmalı.
- Güvenlik: İstemci verisine güvenilmez. Sunucu sırları build'e girmez (`sec-sir-tarayici`). Sunucu portları için `ops-ssh-sertlestirme` / `sec-zero-trust-ag` kullanılır.
- KVKK: Oyuncu kimliği, IP ve ban kayıtlarının saklama süresi `sec-kvkk-gdpr-kontrol` ile belirlenir.
- Maliyet: Sunucu ve yük testi için "en fazla N saat/örnek" tavanı başlamadan yazılır.

Atladıklarım: `unity` MCP'nin bağlı olduğunu ve `hetzner-deploy`'un çalıştığını doğrulamadım. Barındırma sağlayıcılarının güncel durumunu da araştırmadım; 5. adımdaki seçim bunu yapacak. `departman-arastirma-ogrenme` ile `departman-guvenlik`'i açmadım, onlara verdiğim araç adları dizinlerden.
Risk: 5. işte önce N değerini kararlaştırmamız gerekiyor. Pazar rakamları da doğrulanmadan yatırımcıya gitmemeli.
### Y
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

## 7. AWS maliyet panosu: fatura verisini çek, Grafana panosu kur, haftalık Slack bildirimi gönder
### X
**(a) Araçlar**
1. `aws` CLI (`ce get-cost-and-usage`): fatura verisini çeker. Listede AWS MCP yok, Azure araçları bu işe uymuyor.
2. ajan `FinOps Engineer`: etiket/hesap kırılımını ve hangi metriklerin izleneceğini belirler.
3. ajan `ops-grafana-pano`: panoyu tasarlar (servis/hesap/gün panelleri, şablon değişkenleri).
4. ajan `otm-zamanlanmis-gorev`: haftalık cron işini kilit ve log ile kurar.
5. `Slack` MCP: haftalık özeti kanala gönderir.
6. `gitleaks`: commit öncesi sır taraması yapar (departman-guvenlik adım 1).

**(b) Sıra**
1. `FinOps Engineer`: metrik setini ve kırılımları seçer. Kaynak ya CE API'si ya da CUR→S3→Athena olur; karar burada verilir.
2. `aws` CLI: salt-okuma IAM rolüyle (`ce:GetCostAndUsage`) son 90 gün çekilir ve sonuç biçimi doğrulanır.
3. `ops-grafana-pano`: veri kaynağı (Athena ya da JSON) ve pano JSON'u tasarlanır, pano provisioning dosyası olarak repoya girer.
4. `otm-zamanlanmis-gorev`: haftalık betik kurulur (çek → özetle → ilk 5 artış).
5. `Slack` MCP: önce test kanalına tek mesaj gider, onaydan sonra gerçek kanala geçilir.
6. `gitleaks` → commit.

**(c) Kapılar**
- **Maliyet:** CE API istek başı ücretli, betiğe sayısal tavan konur (en fazla N istek/çalışma).
- **Güvenlik:** IAM en az yetkiyle. Anahtar değerleri hiçbir komutla yazdırılmaz, yalnız var/yok kontrolü yapılır. `gitleaks` temiz değilse push yok.
- **Dış yayın:** Slack'e mesaj göndermeden önce onay alınır (test kanalı → gerçek kanal).
- **Test:** özet hesaplayan fonksiyon için sabit örnek JSON ile birim testi yazılır.
### Y
**Araçlar**
- `azure` plugin/MCP — bulut kaynak sorgusu (AWS yok; Cost Explorer için CLI'ye düşülür, taraf notu)
- CLI `aws ce get-cost-and-usage` — fatura verisini çekmenin birincil yolu
- `ops-grafana-pano` (ajan) — RED/USE panosu, değişken, veri kaynağı tasarımı
- `ops-prometheus`/CloudWatch veri kaynağı — Grafana'ya metrik bağlama
- `otm-zamanlanmis-gorev` (ajan) — haftalık cron + kilit
- `sec-sir-tarayici` (ajan) — AWS/Slack anahtarı commit öncesi kapı

**Sıra**
1. `aws ce` CLI ile maliyet verisini JSON çek (en fazla 1 çağrı/koşu, servis+gün kırılımı)
2. Grafana veri kaynağı: CloudWatch/Cost ya da ara DB; panoyu `ops-grafana-pano` ile taslakla
3. `ops-grafana-pano` panelleri (servis, hesap, trend) + eşik uyarısı
4. Haftalık özet betiği → Slack webhook; `otm-zamanlanmis-gorev` ile cron + tek örnek kilidi
5. `sec-sir-tarayici` / gitleaks: AWS & Slack token sızıntı taraması
6. Bir haftalık kuru koşu, bildirim içeriğini doğrula

**Kapılar**
- Güvenlik: gitleaks temiz olmadan push yok; Slack webhook + AWS anahtarı env'de, değer yazdırılmaz (`sec-sir-tarayici`)
- Maliyet: `aws ce` ücretli (sorgu başına ~0.01$) — tavan "koşu başına en fazla 1 çağrı"
- Test: cron kilidi + bildirim kuru koşu (`otm-zamanlanmis-gorev`)

## 8. Kişisel finans takip uygulaması: banka CSV içe aktarma, ML ile kategori sınıflandırma, grafikler ve KVKK
### X
**(a) Araçlar**
1. ajan `otm-csv-temizleyici`: banka CSV'lerinin farklılıklarını çözer (`;` ayırıcı, virgüllü ondalık, Windows-1254).
2. ajan `ml-scikit-learn`: TF-IDF + LogisticRegression ile sızıntısız bir pipeline kurar ve çapraz doğrulama yapar.
3. `frontend-craft`: UI işi olduğu için zorunlu. a11y/perf kabulünü ve 3 genişlikte screenshot'ı kapsar.
4. ajan `Data Visualization Engineer`: grafik türünü seçer, renk körlüğüne uygun kodlama yapar.
5. `use-case-triage` → `pia-generation`: KVKK sınıflaması ve VKED taslağı.
6. ajan `sec-kvkk-gdpr-kontrol`: veri akışını rıza, saklama ve silme yükümlülüklerine eşler.

**(b) Sıra**
1. `use-case-triage` → `pia-generation`: veri kategorileri, yerel işleme ve saklama süresi kararlaştırılır.
2. `otm-csv-temizleyici`: banka başına ayrıştırıcı yazılır, her banka için sentetik örnek CSV ile test edilir. Depo SQLite olur; departman-veri-db'nin Postgres adımı bu yüzden uygulanmaz.
3. `ml-scikit-learn`: önce basit kural/anahtar kelime tabanı ölçülür, ardından model ve kullanıcı düzeltmesiyle yeniden eğitim gelir.
4. `frontend-craft` + `Data Visualization Engineer`: içe aktarma ekranı, kategori düzeltme ve aylık grafikler.
5. `sec-kvkk-gdpr-kontrol`: tam veri akışı denetlenir, silme ve dışa aktarma uçları doğrulanır.
6. `security-review` + `gitleaks` → commit.

**(c) Kapılar**
- **Test:** ayrıştırıcı ve sınıflandırıcı için birim testi yazılır. Test verisi sentetik olur, gerçek hesap verisi kullanılmaz.
- **ML:** zamana göre bölme ile veri sızıntısı kontrol edilir. Metrik makro-F1'dir (sınıflar dengesiz).
- **Erişilebilirlik:** `frontend-craft` kabul kriterleri uygulanır (kontrast, klavye, grafiklerin metin özeti).
- **KVKK:**
  - İşlem metni dış LLM'e gönderilmez; gönderilirse önce `sec-llm-pii-maskeleme`.
  - Disk şifrelenir, IBAN/hesap no maskelenir.
  - Kullanıcı verisini silebilir ve dışa aktarabilir.
  - VKED onaylanmadan yayına çıkılmaz.
### Y
**Araçlar**
- `supabase-postgres-best-practices` — şema/RLS kuralları, kişisel finans verisi hassas
- `otm-csv-temizleyici` (ajan) — banka CSV kodlama/ayraç/sayı formatı
- `ml-scikit-learn` (ajan) — kategori sınıflandırma, sızıntısız pipeline
- `fe-dashboard-duzeni` (ajan) — grafikler, hesap özeti düzeni
- `use-case-triage` (skill) — KVKK: finansal veri işleme tetiği
- `pia-generation` (skill) — gerekirse KVKK etki değerlendirmesi

**Sıra**
1. `use-case-triage`: finansal + kişisel veri → KVKK yükümlülüğü belirle (başta)
2. `otm-csv-temizleyici`: banka CSV içe aktarma, UTF-8/ayraç/tutar ayrıştırma + doğrulama
3. `supabase-postgres-best-practices`: işlem/kategori şeması, RLS ile kullanıcı izolasyonu
4. `ml-scikit-learn`: kategori sınıflandırıcı, leak-free pipeline, dengesiz sınıf metrikleri
5. `fe-dashboard-duzeni`: harcama grafikleri, kategori dağılımı
6. `pia-generation` (tetiklenirse) + model ve import için assert tabanlı testler

**Kapılar**
- KVKK: `use-case-triage`→`pia-generation`; saklama/silme/rıza; veri yerelde, dış LLM'e ham işlem gönderilmezse `sec-llm-pii-maskeleme` gereksiz
- Güvenlik: RLS kiracı izolasyon testi (`db-rls-politika` ajanı); CSV parse doğrulama güven sınırı
- Test: sınıflandırıcı sızıntı kontrolü + CSV import testi (`ml-veri-sizintisi` ajanı)

## 9. Bir Android APK dosyasını kaynak koda çevirip istediği izinleri ve gömülü API anahtarlarını raporla.
### X
**(a) Araçlar**
1. `droidasc` CLI: APK'yı kaynak koda çevirir. Alternatifi `jadx`/`apktool` (listede yok, bildiğim araçlar). droidasc'ın lisansı kurulumdan önce okunur.
2. `android-skills:android-permissions-security`: manifest izinlerini tehlike düzeyine göre sınıflar.
3. `mukul975-mobile-security-paket`: mobil statik analiz kontrol listesi (exported bileşenler, ağ güvenliği yapılandırması).
4. ajan `sec-sir-tarayici`: gömülü anahtarları tarar; yalnız konumu raporlar, değeri asla yazmaz.
5. `gitleaks` (`--no-git` dizin taraması): anahtar desenlerinde ikinci kaynak.
6. ajan `sec-guvenlik-raporu`: bulguları öncelik ve düzeltme adımlarıyla rapora çevirir.

**(b) Sıra**
1. Yetki doğrulanır: APK kullanıcının kendi uygulaması mı, yoksa yazılı izin var mı? Yoksa iş durur.
2. APK yeni ve boş bir klasöre kopyalanır, `droidasc` ile çıktı ayrı bir klasöre açılır. Betikler başka dizinde tutulur, Python `-I` ile koşulur.
3. `android-permissions-security`: `AndroidManifest.xml` izinleri, exported bileşenler ve `network_security_config` incelenir.
4. `sec-sir-tarayici` + `gitleaks`: kaynak, `res/values/strings.xml`, assets ve native `.so` stringleri taranır.
5. `mukul975-mobile-security-paket`: bulunan anahtarın türü ve kapsamı değerlendirilir (Firebase/Maps gibi istemci anahtarı mı, gizli sunucu anahtarı mı).
6. `sec-guvenlik-raporu`: rapor yazılır (izin tablosu · anahtar türü · dosya:satır · maskeli önek · öneri).

**(c) Kapılar**
- **Yetki:** yalnız kullanıcının sahip olduğu ya da izin aldığı APK incelenir, kapsam dışı hedef yoktur.
- **Gizlilik:** anahtar değerleri rapora ve konsola tam yazılmaz, ilk 4 karakter + `***` gösterilir.
- **Doğrulama:** anahtarın canlı çalışıp çalışmadığı 3. taraf servise istek atılarak denenmez.
- **Güvenilmeyen dosya:** APK içeriği hiçbir zaman çalıştırılmaz, yalnız statik analiz yapılır.
- **Lisans:** droidasc MIT/Apache değilse lisans koşulları rapora yazılır.

Hiçbir şey koşulmadı; yalnız üç departman skill'i (güvenlik, veri-db, diğer) okundu. droidasc'ın lisansını ve AWS CE API'sinin güncel istek ücretini doğrulamadım.
### Y
**Araçlar**
- CLI `apktool` + `jadx` — APK'yı manifest + Java kaynağa çevir (birincil; kurulu değilse kurulum araştırması)
- Read aracı — AndroidManifest.xml'den izin listesi (dar aralık)
- `sec-sir-tarayici` (ajan) — decompile kaynakta gömülü API anahtarı/secret
- `sec-skill-tedarik-tarama` / `oyn-mod-guvenlik-kontrol` (ajan) — untrusted APK yalıtımı
- Grep — izin + anahtar desenleri (files_with_matches, konum)
- `sec-guvenlik-raporu` (ajan) — bulgu → önceliklendirilmiş rapor

**Sıra**
1. APK'yı yeni boş dizine koy (untrusted); `apktool d` ile manifest/kaynak çıkar
2. `jadx` ile Java'ya decompile (ayrı dizin, interpreter APK dizininden çalıştırılmaz)
3. Read ile `AndroidManifest.xml` → istenen `uses-permission` dökümü
4. Grep ile anahtar desenleri (`AIza`, `sk_`, `AKIA`, `api_key`) → konumlar; eşleşen satırı Read ile dar aralık
5. `sec-sir-tarayici` ile kaynakta secret doğrulama
6. `sec-guvenlik-raporu`: izinler + bulunan anahtarlar, risk önceliğiyle rapor

**Kapılar**
- Yetki: yalnız kullanıcının sahip/yetkili olduğu APK analiz edilir; kapsam dışı uygulama tersine çevrilmez
- Güvenlik: untrusted arşiv kuralı — her şey ayrı dizinde, `-I` ile Python, APK dizininden build/interpreter çalıştırma yok
- Gizlilik: bulunan gerçek anahtar değeri rapora **maskeli** yazılır, ham değer yazdırılmaz

Araç yok notu: AWS'ye özel MCP yok — 7'de Cost Explorer CLI'ye düşülür; APK için apktool/jadx kurulu değilse `ara-yeni-arac-kurulum-arastirma` ile önce kurulum adımı.

**Atladığım:** Araçların kurulu/ölçülü olup olmadığını (apktool, jadx, Grafana, aws CLI) doğrulamadım — plan "kuruluysa" varsayar; eksikse her iş kurulum adımıyla bir uzar. Risk: 8'de dış ML servisi kullanılırsa KVKK kapsamı büyür, plan yerel scikit-learn varsayıyor.

## 10. Hostinger'daki alan adının DNS kayıtlarını güncelle ve sitenin VPS'e yayınını doğrula.
### X
**(a) Araçlar**
- `departman-surec-git-yayin`: yayın sırasını ve "kullanıcı istemeden deploy yok" kapısını bu skill veriyor.
- `mcp:hostinger`: alan adının DNS kayıtlarını okuyup yazan araç. Bu skill'in dizininde "yalnız CC" olarak geçiyor; bağlı olup olmadığına bakmadım.
- `nslookup`/`curl -I`/`openssl s_client` (CLI): yayılımı, HTTP yanıtını ve sertifika zincirini kontrol eder.
- ajan `ops-dns-tls-sorun`: DNS ya da TLS kontrolü kırmızı çıkarsa kök nedeni bulur.
- ajan `sec-alt-alan-ele-gecirme`: değişiklikten sonra artık hiçbir yere gitmeyen CNAME kalmış mı diye bakar.
- `canary`: yayından sonra sağlık izler.

**(b) Sıra**
1. `mcp:hostinger`: mevcut DNS kayıtlarını salt okuma ile alıp dökümünü saklarım, geri dönüş bu dökümle yapılır. Sonra VPS'in IP'sini ve hedef kayıtları (A/AAAA/CNAME, TTL) seninle netleştiririm.
2. Fark tablosunu (eski → yeni) gösterip **onayını beklerim**, çünkü DNS değişikliği dışarıya etki eder.
3. `mcp:hostinger`: kayıtları yazarım; API çağrısı **en fazla 10**.
4. CLI: birkaç DNS çözücüde (1.1.1.1, 8.8.8.8) yayılımı denerim. Ardından `curl -I` ile http→https yönlendirmesini ve 200 yanıtını, `openssl` ile sertifikanın alan adıyla eşleşip eşleşmediğini ve bitiş tarihini kontrol ederim.
5. Kontrollerden biri kırmızıysa `ops-dns-tls-sorun` çalışır; yeşilse `sec-alt-alan-ele-gecirme` çalışır.
6. `canary`: ilk sağlık turunu atarım, ≤15 satırlık rapor yazarım.

**(c) Kapılar**
- Yazmadan önce kullanıcı onayı ve DNS dökümü.
- Hostinger token'ının yalnız var/yok bilgisi kontrol edilir, değeri hiçbir komutla basılmaz.
- TLS: alan adı eşleşmesi ve zincir tam olmalı (`openssl`).
- Güvenlik: hiçbir yere gitmeyen kayıt kalmamalı (`sec-alt-alan-ele-gecirme`). HSTS başlığına `curl -I` ile bakılır.
- Erişilebilirlik ve KVKK: yok.
### Y
**(a) Araçlar**
- `hostinger` MCP: DNS bölgesini okur ve yazar, VPS IP'sini verir. İş doğrudan buna denk geliyor.
- ajan `ops-dns-tls-sorun`: dig ile yetkili NS'den ve genel çözücülerden yayılmayı, openssl ile sertifika zincirini kontrol eder.
- `canary` (gstack): yayın sonrası HTTP 200'ü, http→https ve www yönlendirmesini izler.
- ajan `sec-alt-alan-ele-gecirme`: güncellemeden sonra boşta kalan CNAME/A kayıtlarını yakalar.
- `deploy-app`: yalnız VPS'te uygulama ayakta değilse yayın için gerekir.
- ajan `git-yayin-oncesi-kontrol`: dönüş planı ve go/no-go listesi.

**(b) Sıra**
1. `hostinger` MCP ile mevcut bölge kayıtlarını ve TTL'leri alıp dönüş için anlık görüntü olarak saklarım. VPS IP'sini de buradan alırım.
2. Planlanan A/AAAA/CNAME farkını çıkarırım; MX, SPF, DKIM ve TXT kayıtlarına dokunulmaz. Farkı onayına sunarım.
3. Onaydan sonra `hostinger` MCP ile kayıtları yazarım.
4. Ajan `ops-dns-tls-sorun` ile yetkili NS'yi ve 1.1.1.1/8.8.8.8'i sorgular, ardından openssl s_client ile alan adı ve sertifika uyumunu kontrol ederim.
5. `canary` ile kök, www ve https yönlendirmesinin 200 döndüğünü ve içeriğin VPS'ten geldiğini doğrularım (yanıt başlığı ya da sabit bir işaret metniyle).
6. Ajan `sec-alt-alan-ele-gecirme` ile kayıt temizliğini denetler, kapanış raporunu yazarım.

**(c) Kapılar**
- Onay: DNS'e yazmadan önce açık onayın gerekir; dış dünyayı etkileyen ve geri alınması zor bir adım.
- Dönüş: 1. adımdaki anlık görüntü dönüş yoludur.
- Güvenlik: geçerli TLS zinciri ve boşta kayıt kalmaması (`sec-alt-alan-ele-gecirme`).
- E-posta: MX ve SPF kayıtlarının değişmediği farkta kanıtlanır.
- Tavan: Hostinger API çağrısı en fazla N; N'yi işe başlamadan sen belirlersin.
- KVKK ve erişilebilirlik bu işte yok.

## 11. 3D ürün modelinin GLB dosyasını web için sıkıştır, doku boyutlarını küçült ve mesh sayısını raporla.
### X
**(a) Araçlar**
- `tools/glb_hat.py`: optimize (meshopt + webp) → validate → inspect özeti → önce/sonra KB. İşin çekirdeği bu betik.
- ajan `bl-glb-disa-aktar`: web için küçük GLB kuralları (doku tavanı, decimation ihtiyacı).
- `blender-oturum` (`tools/blender_oturum.py`): decimation ya da yeniden dışa aktarma gerekirse Blender'ı yalnız headless (`-b`) açar.
- `tools/blender_dogrula.py`: sayısal kapı. Ölçek, pivot ve topolojiyi kanıtlamaz, ilk kontrol olarak kullanılır.
- `tools/blender_gorunum.py`: önce/sonra görsel kanıt (4 Workbench görünümü ve IoU).
- `blender` MCP: yalnız betik yetmezse, yedek olarak.

**(b) Sıra**
1. Orijinal GLB'yi ayrı bir klasöre kopyalarım; orijinal korunur.
2. `glb_hat.py` inspect ile başlangıcı kaydederim: mesh ve primitive sayısı, doku çözünürlükleri, KB.
3. `glb_hat.py` ile optimize ederim. Dokular ürün için 2048, ikincil haritalar için 1024 tavanıyla webp'ye çevrilir. Betikte boyut parametresi yoksa kullandığı CLI'nin resize komutu (`--help` ile doğrulanır) aynı hatta eklenir.
4. Aynı betiğin validate adımında hata sayısının 0 olması gerekir.
5. `blender_dogrula.py` ve ardından `blender_gorunum.py` ile önce/sonra görünümleri headless karşılaştırırım.
6. Rapor: mesh sayısı, doku boyutları ve önce/sonra KB.

**(c) Kapılar**
- Biçim: glTF validator 0 hata (`glb_hat` validate).
- Görsel: önce/sonra IoU eşiği (`blender_gorunum`); doku inceltme ürün detayını bozmamalı.
- Performans: dosya boyutu bütçesini (ör. ≤ X MB) işe başlamadan sen belirlersin.
- Ekran kuralı: Blender yalnız `-b` ile çalışır, pencere açılmaz.
- Güvenlik, KVKK ve erişilebilirlik bu işte yok.
### Y
**(a) Araçlar**
- `blender-oturum` + `blender-uretim`: Blender'ın headless (`-b`) açılıp kapanmasını yönetir. Model önce Blender'da düzeltilecekse kullanılır.
- `tools/glb_hat.py`: repoda hazır duran GLB hattı. Meshopt sıkıştırması, webp dokular, `--doku` ile doku boyutu sınırı, sonra doğrulama, inspect özeti ve önce/sonra KB.
- `gltf-transform` CLI 4.5.1 (MIT): `glb_hat.py`'nin altında çalışan araç. `inspect` çıktısı mesh, primitive, üçgen ve doku sayısını verir.
- ajan `bl-glb-disa-aktar`: kaynak dosya `.blend` ise web için küçük GLB'yi o çıkarır.
- ajan `bl-gorsel-ani-kontrol`: ters normal ve eksik doku olup olmadığını tarar.
- `threejs-visual-validation`: önce/sonra halini headless render edip karşılaştırır.

**(b) Sıra**
1. `glb_hat.py` hattının ilk adımıyla (`gltf-transform inspect`) başlangıç ölçümünü alırım: KB, mesh sayısı, üçgen sayısı, doku çözünürlükleri. Girdi dosyası `Desktop\<Proje>\` altında olmalı.
2. Kaynak `.blend` ise `blender-oturum` (headless) ve `bl-glb-disa-aktar` ile export alırım. Zaten GLB ise bu adım atlanır.
3. `python tools/glb_hat.py <girdi.glb> --doku 1024` komutunu çalıştırırım. Doku sınırını sen değiştirebilirsin.
4. Doğrulama hata verirse `bl-gorsel-ani-kontrol` çalışır.
5. `threejs-visual-validation`: önce ve sonra halini aynı açıdan headless render edip görsel farka bakarım.
6. Rapor: önce/sonra KB, mesh/primitive/üçgen sayısı, doku boyutları.

**(c) Kapılar**
- Test: glTF doğrulamasında 0 hata (`glb_hat.py`).
- Görsel fark: kabul eşiği headless render ile (`threejs-visual-validation`).
- Lisans: modelin ve dokuların kaynağı rapora yazılır.
- Ekran kuralı: Blender yalnız `-b` ile, tarayıcı yalnız headless.
- Güvenlik, erişilebilirlik, KVKK: yok.

## 12. Bu repodaki bütün skill filosunun API'siz statik kalite denetimini çıkar ve sorunlu skill'leri listele.
### X
**(a) Araçlar**
- `tools/skill_filo_denetim.py`: KALİTE-3 Faz 1. Bütün filoyu API'siz ve salt okuma olarak statik denetler. İş tam olarak bu.
- `graphify query`: betiğin girdilerini, çıktılarını ve testlerini önce grafikten bulurum (CLAUDE.md kuralı).
- ajan `okuyucu` (sonnet): büyük denetim çıktısını kural başına özetler ve ilk k satırı çıkarır; ana bağlama yalnız özet gelir.
- `skillspector` CLI: işaretlenen ve 3. taraf skill'lerde gizli talimat ve dışa sızdırma taraması yapar. Yalnız çevrimdışı/statik modda; LLM çağırıyorsa bu adımı atlarım.
- ajan `plugin-dev-plugin-validator`: plugin manifest ve yapı doğrulaması.
- `jev log|triage`: büyük çıktıyı ilk elemeden geçirir. API kullanıyorsa yerine `okuyucu` geçer.

**(b) Sıra**
1. `graphify query "skill_filo_denetim"` ile kapsamı, çıktı yolunu ve mevcut testi bulurum, ardından betiğin `--help` çıktısına bakarım.
2. `python tools/skill_filo_denetim.py` salt okuma çalışır ve raporu dosyaya yazar.
3. Ajan `okuyucu` raporu kural başına sayar ve sorunlu skill'leri listeler: description >200 karakter, 3. tekil kişi değil, gövde >500 satır, kırık references, frontmatter hatası.
4. `skillspector` işaretli skill'leri tarar.
5. Ajan `plugin-dev-plugin-validator` manifestleri doğrular.
6. Ucuz modelin listesinden 3–5 satırı Read ile örnekleyerek doğrular, ardından nihai sorunlu skill listesini yazarım.

**(c) Kapılar**
- Salt okuma: denetimden önce ve sonra `git status` aynı olmalı.
- API'siz: betikte anthropic/requests importu olmadığını Grep ile kanıtlarım.
- Örnek doğrulama: ucuz modelin satırları örnekle kontrol edilir.
- Güvenlik: skillspector bulguları önem sırasıyla raporlanır.
- Lisans, KVKK ve erişilebilirlik bu işte yok.

`kalite3_hiz.py` (otomatik onarım) bilerek dışarıda bırakıldı; yalnız liste istendi.

Hiçbir aracı çalıştırmadım: Hostinger MCP'nin bağlı olduğu, `glb_hat.py`'nin doku boyutu parametresi ve skillspector'ın API'siz çalışıp çalışmadığı uygulamada doğrulanacak. Risk: 10. işte DNS yazımı canlıdır; anlık görüntü alınmadan ve sen onaylamadan yazılmaz.
### Y
**(a) Araçlar**
- `departman-surec-ajan-arac`: skill kurallarını (description ≤200 karakter, gövde ≤500 satır, tetik cümlesi) buradan alırım.
- `tools/skill_filo_denetim.py`: repoda hazır, API kullanmayan, salt okuyan filo denetimi. Gevşek skill'leri, plugin kurulum yollarını ve `synced` kopyalarını tarar. Yakaladığı sorunlar: açıklama yok, kısa ya da uzun; tetik yok; kırık bağlantı; çift kayıt; eski araç adı; kendi içinde çelişen kurallar; progressive disclosure yok.
- `tools/skill_denetim.py`: tek bir skill'e derin bakmak için. Başlığını okumadım, kapsamına skill'i açınca bakacağım.
- ajan `sec-skill-tedarik-tarama`: üçüncü taraf skill'lerde gizli talimat ya da veri sızdırma var mı diye statik tarar.
- `jev` (`jev triage`): büyük TSV'den yalnız öne çıkması gereken satırları ayırır.
- `departman-surec-inceleme`: kapanış incelemesi.

**(b) Sıra**
1. Filo denetimini çalıştırırım: `python tools/skill_filo_denetim.py --tsv docs/kutuphane/skill-denetim.tsv --ozet docs/kutuphane/skill-denetim-ozet.md`. Bu iki dosya yazılır.
2. `jev triage` ile TSV'yi sorun türüne göre gruplarım ve en ağır N skill'i çıkarırım.
3. En ağır N skill'e `skill_denetim.py` ile tek tek derin bakarım.
4. `sec-skill-tedarik-tarama`: yalnız üçüncü taraf kaynaklı ve işaretlenen skill'lere uygulanır.
5. Sorunlu skill listesini çıkarırım: ad · kaynak · sorun kodları · önerilen düzeltme. Düzeltme yapılmaz.
6. `departman-surec-inceleme` ile örnek satırları kaynağına bakarak doğrularım; özellikle ucuz modelin ürettiği satırları.

**(c) Kapılar**
- API'siz kalmalı: ücretli çağrı 0.
- Doğrulama: listeden rastgele 10 satır SKILL.md'ye bakılarak teyit edilir.
- Güvenlik: tedarik taraması sırasında bulunan sır değerleri rapora yazılmaz, yalnız konumu yazılır.
- Lisans: düzeltme için dış skill kodu alınacaksa, MIT/Apache değilse koşulları rapora yazılır.
- Erişilebilirlik ve KVKK: yok.

Doğrulamadıklarım: Hostinger MCP'nin bağlı olduğu ve VPS'in Hostinger'da mı yoksa başka bir yerde mi olduğu, `gltf-transform`'un kurulu olduğu, `skill_denetim.py`'nin tam kapsamı. 12'nin 1. adımı repoya iki rapor dosyası yazar; onay vermeden başlamam.
