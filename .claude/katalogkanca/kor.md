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
. AI görsel kataloğu, arka plan silme, toplu yükleme
**(a) Araçlar**
- `gorsel-uret` (skill): yerel ComfyUI oturumunu CC yönetir, işe bununla girilir.
- `tools/gorsel_uret.py` (betik): `ac · uret · buyut · arkaplan · kapat` alt komutları tek iş akışını karşılıyor.
- `comfyui` (CLI): yerel sunucu (127.0.0.1:8188), ücretli API çağrısı yok.
- `banana` (MCP): yalnızca ComfyUI kalitesi yetmezse yedek üretici olarak kullanılır.
- `deploy-app` (skill): ürün görsellerinin CDN'de ya da statik olarak barındırılması gerekirse.
- Toplu yükleme: **yok**. Listede Shopify/WooCommerce yükleme aracı yok, mağaza API'si ya da CSV içe aktarımı için küçük bir betik gerekir.

**(b) Sıra**
1. Skill `gorsel-uret`, ardından `gorsel_uret.py ac`. Pencere açmaz, arka planda çalışır.
2. Ürün başına istemle `gorsel_uret.py uret`. Yalnızca başarısız olanlar `banana`'ya gider.
3. Toplu olarak `gorsel_uret.py arkaplan` ile şeffaf PNG.
4. Mağazanın en düşük çözünürlüğünün altında kalanlara `gorsel_uret.py buyut`.
5. Yükleme betiği önce `--dry-run` ile ürün→görsel eşlemesini döker, Ömer onaylarsa canlıya yükler.
6. `gorsel_uret.py kapat`.

**(c) Kapılar**
- Görsel QA: rastgele k görsel Read ile açılır, kenar halesi, bozuk el/logo ve yazı hatası aranır.
- Sayım: üretilen görsel sayısı ürün sayısına eşit olmalı.
- Ücretli API sınırı: `banana` en çok N görsel.
- Güvenlik: mağaza token'ı yalnızca var/yok diye kontrol edilir, değeri basılmaz.
- Yayın: canlı yüklemeden önce açık onay.
- KVKK: insan model görseli yoksa gerekmez.

## 2. Go ile yazılmış WebSocket sohbet servisi: yatay ölçekleme, yük testi ve Docker dağıtımı
### X
. Go WebSocket sohbet servisi
**(a) Araçlar**
- `be-yatay-olcekleme` (ajan): durumsuz düğümler, Redis pub/sub ile mesaj dağıtımı, bağlantıları boşaltma tasarımı.
- `ecc:docker-patterns` (skill): çok aşamalı imaj, root olmayan kullanıcı, compose ile 3 replika, Redis ve LB.
- `ecc-devops-guvenlik-paket` (skill): imaj ve dağıtım güvenlik taraması.
- `departman-surec-git-yayin` (skill): commit, CI ve deploy sırası.
- `git-canary-izleme` (ajan): canary adımları ve geri çekilme eşikleri.
- `use-case-triage` (skill): sohbet mesajları kişisel veri olduğu için KVKK sınıflaması.
- Yük testi: **yok**. Listede k6 aracı yok, doğrudan k6 betiği yazılır.

**(b) Sıra**
1. Agent `be-yatay-olcekleme` ile mimari kararı.
2. Ana oturumda Go kodu (hub, Redis yayını, upgrade sırasında auth ve Origin kontrolü) ve testler.
3. Skill `ecc:docker-patterns` ile Dockerfile ve compose.
4. Alt ajan compose'a karşı k6 WebSocket yük testini çalıştırır, yalnızca özet döner.
5. Skill `ecc-devops-guvenlik-paket` ile imaj ve sır taraması.
6. Skill `departman-surec-git-yayin` ile CI ve deploy, Agent `git-canary-izleme` ile kademeli açılış.

**(c) Kapılar**
- Test: `go test -race ./...` ve `go vet`. Düğümler arası mesajın teslim edildiği bir entegrasyon testi şart.
- Yük: sayısal eşikler önceden yazılır (örneğin p95 teslim süresi < X ms, hata < %Y, N eşzamanlı bağlantı).
- Güvenlik: WS upgrade sırasında auth, Origin izin listesi, mesaj boyutu ve hız sınırı, imajda sır olmaması.
- KVKK: `use-case-triage` ile saklama süresi kararı. Loglara mesaj içeriği yazılmaz.
- Canary: eşik aşılırsa otomatik geri alma.
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
. React Native: çevrimdışı senkron, push, hata izleme, mağaza yayını
**(a) Araçlar**
- `expo-mobil-paket` (skill): EAS build, submit ve update ile CI üzerinden mağaza yayını.
- `ecc:react-native-patterns` (skill): veri katmanı ve çevrimdışı kuyruk deseni.
- `mob-push-bildirim` (ajan): APNs/FCM token akışı, izin isteme zamanı, payload tasarımı.
- `sentry-react-native-sdk` (skill): hata izleme kurulumu ve source map yükleme.
- `mob-magaza-ekran-goruntusu` (ajan): mağazanın istediği ekran görüntüsü setleri.
- `use-case-triage` (skill): push token ve hata verisi için KVKK sınıflaması.

**(b) Sıra**
1. Skill `ecc:react-native-patterns`: yerel depo, yazma kuyruğu, çakışma kuralı (sürüm ya da son yazan kazanır) ve önce test.
2. Agent `mob-push-bildirim`: izin akışı ve token'ın backend'e kaydı.
3. Skill `sentry-react-native-sdk`: kurulum, `sendDefaultPii: false` ve `beforeSend` ile maskeleme.
4. Skill `use-case-triage`: push ve Sentry verileri için KVKK kararı, aydınlatma metni gereksinimi.
5. Skill `expo-mobil-paket`: EAS workflow ile önce internal build, sonra TestFlight ve Play internal track.
6. Agent `mob-magaza-ekran-goruntusu`, ardından Ömer onaylarsa `eas submit`.

**(c) Kapılar**
- Test: senkron için Jest (çevrimdışı yaz → çevrimiçi ol → çakışma senaryosu). Push ve izin reddi için mobil QA.
- Güvenlik: Sentry DSN ve FCM anahtarı yalnızca EAS secret'ta tutulur, değeri basılmaz.
- KVKK: `use-case-triage` ve Sentry PII ayarlarının kontrolü.
- Erişilebilirlik: listede RN için araç **yok**. `accessibilityLabel` ve dokunma hedef boyutu elle kontrol edilir.
- Ücretli kullanım: EAS build en çok N.
- Yayın: mağazaya göndermeden önce açık onay.

---
Atladıklarım: departman-* yönetici skill'lerinden yalnızca `departman-surec-git-yayin` listede vardı, diğerlerini açmadım. RN ve görsel işleri web UI olmadığı için `frontend-craft` uygulanmadı.

Riskler:
- 1. işte yükleme aracı yok. Mağaza platformu bilinmeden yükleme adımı tahmine dayanıyor.
- 2. işte yük testi aracı listede yok, eşik değerlerini (X, Y, N) Ömer'in vermesi gerekiyor.
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
- `git-dal-stratejisi` (ajan): Trunk tabanlı dal düzenini, dal adlarını ve merge/rebase kuralını önerir.
- `git-monorepo-etkilenen` (ajan): Bağımlılık grafiğini çıkarır ve yalnız etkilenen projeleri seçer.
- `git-ci-boru-hatti` (ajan): Seçilen projeler için önbellekli bir build/test/lint iş akışı yazar.
- `git-dal-koruma-kurali` (ajan): main dalı için zorunlu kontrolleri ve CODEOWNERS'ı tanımlar.
- `document-release` (skill): Sürüm notlarının ve CHANGELOG'un doğruluğunu denetler.
- `git` (CLI): Diff tabanı (`git diff --name-only base...HEAD`) ve tag/log kaynağı.

**(b) Sıra**
1. `git` ile mevcut dalları, tag'leri ve commit biçimini topla.
2. `git-dal-stratejisi` ile dal modeline ve conventional commit kuralına karar ver.
3. `git-monorepo-etkilenen` ile proje bağımlılık haritasını ve "etkilenen" hesabını çıkar.
4. `git-ci-boru-hatti` ile matris iş akışını (yalnız etkilenenler + önbellek) yaz.
5. `document-release` ile commit'lerden proje başına sürüm notu üretimini kur ve denetle.
6. `git-dal-koruma-kurali` ile zorunlu kontrolleri bağla.

**(c) Kapılar**
- Test: İki deneme PR'ı açılır. Yaprak pakete dokunan PR'da yalnız o paket koşmalı. Ortak pakete dokunan PR'da ona bağlı tüm projeler koşmalı. Kontrol `git-monorepo-etkilenen` ve CI çıktısıyla yapılır.
- Güvenlik: İş akışı token'ının en az yetkiyle çalışması ve secret'ların PR'dan erişilememesi elle gözden geçirilir. Listede bunun için ayrı bir araç yok.
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
- `departman-belge` (skill): xlsx → pptx üretim sırasını belirler.
- `okuyucu` (ajan): Pazar büyüklüğü (TAM/SAM/SOM) ve rakip araştırmasını kaynaklı özet olarak döner.
- `db-bi-rapor` (ajan): Model metriklerini ve grafik verisinin yapısını tanımlar.
- `presentation-creator` (skill): Veri içeren yatırımcı sunumunun akışını kurar.
- `dok-pptx-sunum` (ajan): Slayt başına tek fikir ve tutarlı yerleşimle pptx üretir.
- Finansal model aracı: Listede yok. Model, `departman-belge` xlsx sırasıyla elle kurulur.

**(b) Sıra**
1. `departman-belge` ile çıktı sırasını belirle: model.xlsx → grafikler → deck.pptx.
2. `okuyucu` ile pazar araştırması yap. Web aramasına sayısal üst sınır konur, örneğin en çok 15 arama.
3. `db-bi-rapor` ile gelir sürücülerini, maliyet kalemlerini ve runway metriklerini tanımla.
4. Varsayım sekmesi olan 3 senaryolu xlsx modelini kur (`departman-belge` sırası).
5. `presentation-creator` ile hikâye akışını kur: problem → pazar → ürün → model → talep.
6. `dok-pptx-sunum` ile pptx'i üret ve slaytları görüntüye çevirerek gözle kontrol et.

**(c) Kapılar**
- Tutarlılık: Slayttaki her rakam modeldeki bir hücreye izlenebilmeli. Bu, bir betikle çapraz kontrol edilir.
- Kaynak: Her pazar rakamının kaynağı ve tarihi slayt notunda yazılı olmalı (`okuyucu` çıktısından).
- Erişilebilirlik: Kontrast, okunur font boyu ve grafiklerin yalnız renge dayanmaması kontrol edilir. Listede bunun için araç yok, kontrol elle yapılır.
- KVKK: Deck'te müşteri ya da kişi verisi varsa anonimleştirilir. Listede araç yok, kontrol elle yapılır.

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
- `okuyucu` (ajan): Netcode for GameObjects, Mirror ve Fish-Net ile barındırma seçeneklerini karşılaştıran doküman araştırması yapar.
- `oyn-ag-senkronu` (ajan): Otoriter sunucu, tahmin/uzlaştırma ve gecikme telafisi tasarlar. Hile korumasının çekirdeği bu tasarımdır.
- `oyn-oyun-motoru-script` (ajan): C# ağ betiklerini yazar (NetworkBehaviour, RPC, sunucu doğrulaması).
- `unity` (MCP): Sahneyi, NetworkManager'ı ve prefab kayıtlarını kurar, editörde koşturur.
- `git` (CLI): Dal ve commit işleri.
- Sunucu barındırma aracı: Listede yok. Seçenekler `okuyucu` ile araştırılır.

**(b) Sıra**
1. `okuyucu` ile ağ kütüphanesini ve barındırma seçeneğini (Unity Multiplay, Edgegap, kendi VPS'in) kaynaklı karşılaştır.
2. `oyn-ag-senkronu` ile durum otoritesini, tick hızını, tahmin/uzlaştırmayı ve sunucu tarafı doğrulama kurallarını tasarla.
3. `oyn-oyun-motoru-script` ile C# betiklerini yaz. İstemci yalnız girdi gönderir, durumu sunucu hesaplar.
4. `unity` MCP ile NetworkManager'ı, prefab'ları ve Transport ayarlarını kur.
5. Headless dedicated server build'i `-batchmode -nographics` ile al. Ekran kuralı gereği pencere açılmaz.
6. `git` ile dala commit at. Barındırma dağıtımı ayrı onayla yapılır.

**(c) Kapılar**
- Test: Unity Test Framework'te play-mode testleri koşulur: host + 2 istemci senkronu, ağ simülatöründe 150 ms gecikme ve %5 paket kaybı. Listede bunun için araç yok, iş `unity` MCP ve batchmode koşusuyla yapılır.
- Hile: Sunucunun hız/teleport, yetkisiz RPC ve sahte hasar girdilerini reddettiği testlerle kanıtlanır.
- Güvenlik: İstemci build'inde secret ya da sunucu anahtarı olmamalı. Sunucu portu ve kimlik doğrulaması kontrol edilir. Listede bunun için araç yok, kontrol elle yapılır.
- KVKK: Oyuncu kimliği ve IP loglarının saklama süresi ve aydınlatma metni belirlenir. Listede araç yok, kontrol elle yapılır.

Kullanıcı kuralı her işten önce bir `departman-*` müdür skill'inin açılmasını istiyor. Kancanın "yalnız bu listeden seç" kısıtı yüzünden 4 ve 6 için bunu plana koymadım; listede yalnız `departman-belge` vardı. Hiçbir aracı çalıştırmadım. Bu yüzden araçların bu ortamda gerçekten kullanılabilir olduğunu, örneğin `unity` MCP'nin bağlı olup olmadığını, doğrulamadım.

## 7. AWS maliyet panosu: fatura verisini çek, Grafana panosu kur, haftalık Slack bildirimi gönder
### X
**(a) Araçlar**
- `ops-maliyet-optimize` (ajan): fatura verisinden hangi kırılımların (hizmet, etiket, hesap) gösterileceğine karar verir.
- `ops-grafana-pano` (ajan): Grafana panosunun panel düzenini ve şablon değişkenlerini tasarlar.
- `Slack` (MCP): haftalık bildirimi gönderir.
- `otm-bildirim-yonlendirme` (ajan): bildirim eşiklerini, sessiz saatleri ve tekrar sınırını belirler.
- AWS Cost Explorer / CUR çekimi: **yok**. `azure-resource-manager-mcp` yalnız Azure'a bağlanır, AWS için kullanılamaz.
- Haftalık zamanlayıcı: **yok**. Listede cron aracı bulunmuyor.

**(b) Sıra**
1. `ops-maliyet-optimize` ile metrikleri ve kırılımları seç.
2. Fatura verisini çeken betiği yaz. Listede bu iş için hazır bir araç yok.
3. `ops-grafana-pano` ile pano JSON'unu kur.
4. `otm-bildirim-yonlendirme` ile eşikleri ve mesaj şablonunu belirle.
5. `Slack` MCP ile önce test kanalına tek bir deneme mesajı gönder.
6. Haftalık zamanlamayı kur.

**(c) Kapılar**
- Maliyet: Cost Explorer API ücretli, istek başına yaklaşık 0,01 $. Haftada en çok N çağrı gibi sayısal bir tavan konmalı.
- Güvenlik: AWS ve Slack anahtarları yalnız ortam değişkeninde tutulur, değerleri hiçbir çıktıya basılmaz. Tarama aracı listede **yok**.
- Dış yayın: Slack'e ilk gerçek gönderimden önce onayın gerekiyor.
- Test: çekim betiğinin ayrıştırıcısına küçük bir self-check eklenir.
### Y
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
**(a) Araçlar**
- `ml-nlp` (ajan): işlem açıklamalarını kategorilere ayıran sınıflandırıcıyı tasarlar.
- `ml-dengesiz-sinif` (ajan): az görülen kategoriler için metrik, sınıf ağırlığı ve eşik seçer.
- `pia-generation` (skill): KVKK için VKED/PIA taslağını hazırlar.
- `report-with-html` (plugin): grafik ve pano görünümünü üretir.
- Banka CSV'si içe aktarma: **yok**. Encoding, ayraç ve TR ondalık biçimi için listede araç yok.
- UI disiplini: global kuralın zorunlu tuttuğu `frontend-craft` listede **yok**. Kural ile liste çelişiyor; listedışı istisna olarak açılmalı.

**(b) Sıra**
1. `pia-generation` ile veri kategorilerini, saklama süresini ve hukuki dayanağı yaz. Diğer adımlar bu kararlara bağlı.
2. CSV içe aktarıcıyı yaz ve her bankadan 2–3 gerçek örnek dosyayla test et.
3. `ml-nlp` ile sınıflandırıcıyı kur. İlk sürüm kural/anahtar kelime tabanlı, ardından basit bir model.
4. `ml-dengesiz-sinif` ile sınıf bazında F1 ve kabul eşiğini belirle.
5. `report-with-html` ile grafikleri hazırla. Bu adımda `frontend-craft` istisnası uygulanır.
6. Uçtan uca dene: CSV yükle, kategoriler atansın, grafikler çizilsin.

**(c) Kapılar**
- KVKK: VKED onaylanmadan gerçek banka verisi işlenmez. Veri yerelde ve şifreli durur, silme akışı bulunur.
- Test: içe aktarıcı için örnek dosya testleri, sınıflandırıcı için sınıf bazında metrik eşiği.
- Erişilebilirlik: grafiklerde renk körlüğüne uygun palet ve metin alternatifi. Ayrı bir a11y aracı listede **yok**.
- Güvenlik: CSV dosyası güvenilmeyen girdi sayılır, boyut ve tip doğrulaması yapılır.

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
**(a) Araçlar**
- `android-skills` (plugin): içindeki `android-permissions-security` skill'i izinleri tehlike düzeyine göre sınıflar.
- `android-paket` (skill): manifest ve güvenlik bağlamını sağlar.
- APK'yı kaynak koda çevirme (jadx/apktool): **yok**. Listede decompiler bulunmuyor.
- Gömülü anahtar taraması (gitleaks/semgrep): **yok**. Listede bu araçlar bulunmuyor.

**(b) Sıra**
1. Yetkiyi teyit et: APK senin mi, yoksa yetkili bir denetim kapsamında mı?
2. APK'yı yeni ve boş bir klasörde aç; içinden hiçbir betik ya da derleme aracı koşma.
3. Decompile et. Bunun için listedışı bir araç (jadx) gerekiyor.
4. `android-skills` ile manifest izinlerini listele ve tehlike düzeyine göre sınıfla.
5. Anahtarları desen taramasıyla bul: AWS, Google, Firebase ve benzeri biçimler.
6. Raporu yaz: dosya ve satır konumları, izin tablosu, risk sırası.

**(c) Kapılar**
- Yetki: sahibi sen olmadığın ya da izin almadığın bir APK analiz edilmez.
- Sır disiplini: bulunan anahtarların değeri rapora yazılmaz; yalnız türü, konumu ve ilk 4 karakteri maskeli olarak geçer. Hâlâ geçerli olan anahtarlar için rotasyon önerilir.
- İzolasyon: APK güvenilmeyen veri sayılır, Python ile okunacaksa `-I` bayrağı kullanılır.

---
Listede eksik kalanlar: 7 için AWS çekimi ve cron, 8 için CSV içe aktarma ve `frontend-craft`, 9 için decompiler ve sır tarayıcı. Bunlar için listedışı araç kararı senin. Uygulamada 7'deki Slack gönderimi ve ücretli API tavanı ile 9'daki yetki teyidi önce senin onayını bekliyor.

## 10. Hostinger'daki alan adının DNS kayıtlarını güncelle ve sitenin VPS'e yayınını doğrula.
### X
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
### Y
**(a) Araçlar**
- `hostinger` (MCP): alan adının DNS bölgesini ve VPS bilgisini doğrudan okuyup yazıyor.
- `deploy-app` (skill): VPS'teki uygulamanın yayında olduğunu doğruluyor (servis, port, ters vekil).
- `mcp-server-fetch` (CLI): alan adı üzerinden HTTP(S) yanıtını ve içeriği dışarıdan kontrol ediyor.
- `qa-only` (skill): canlı sitedeki tarayıcı ve API hatalarını raporluyor.
- `guvenlik-paket` (skill): yayın öncesi güvenlik kapısını sağlıyor (TLS, başlıklar).

**(b) Sıra**
1. `hostinger`: `ToolSearch 'hostinger'` ile araçları yükle. Mevcut DNS bölgesini ve VPS IP'sini oku, değişiklik öncesi bölgeyi yedekle.
2. Hedef kayıtlarla mevcut kayıtların farkını çıkar (A/AAAA/CNAME/TTL) ve Ömer'e onaya sun.
3. `hostinger`: onaylanan kayıtları güncelle.
4. `deploy-app`: VPS'te uygulamanın ayakta olduğunu ve vekilin alan adına baktığını doğrula.
5. `mcp-server-fetch` ile alan adından HTTPS yanıtını ve içerik eşleşmesini kontrol et. `qa-only` ile hata raporunu al.
6. `guvenlik-paket`: TLS sertifikası ve güvenlik başlıkları kapısını uygula.

**(c) Kapılar**
- **Onay:** DNS değişikliği dışa dönük ve geri alması zor, bu yüzden önce onay alınır. Eski bölgenin yedeği de saklanır.
- **Yayılım:** Değişikliğin yayıldığı TTL süresi beklenerek `mcp-server-fetch` ile doğrulanır.
- **Güvenlik:** Sertifika ve başlıklar `guvenlik-paket` ile kontrol edilir. Hostinger token'ının değeri hiçbir çıktıya basılmaz.
- **Erişilebilirlik ve KVKK:** yok.

## 11. 3D ürün modelinin GLB dosyasını web için sıkıştır, doku boyutlarını küçült ve mesh sayısını raporla.
### X
**(a) Araçlar**
- `glb_hat` (betik): meshopt + webp ile optimize ediyor, sonra validate ve inspect özeti çıkarıyor, önce/sonra KB'yi veriyor. Sıkıştırma ve mesh sayımı tek hatta.
- `bl-glb-disa-aktar` (ajan): `glb_hat` doku boyutunu küçültemiyorsa Blender'da dokuyu küçültüp yeniden dışa aktarıyor.
- `blender-uretim` (skill): kaynak .blend varsa headless (`-b`) bpy adımlarını yürütüyor.
- `blender-dogrulama` (CLI): önce/sonra görünüm IoU'su ve sayısal kapıyla görsel bozulmayı yakalıyor.
- `blender_dogrula` (betik): ölçek, pivot ve topoloji için sayısal ön kapı.

**(b) Sıra**
1. `glb_hat --help` ile bayrakları gör (doku yeniden boyutlandırma var mı). Orijinal GLB'nin kopyası üzerinde çalış.
2. `glb_hat inspect` ile başlangıç değerlerini al: mesh, primitive ve üçgen sayısı, doku çözünürlükleri, KB.
3. `glb_hat optimize` (meshopt + webp, varsa doku boyutu sınırı) çalıştır, ardından `validate`.
4. Doku küçültme bayrağı yoksa `bl-glb-disa-aktar` ve `blender-uretim` ile headless Blender'da dokuları küçültüp yeniden dışa aktar.
5. `blender_dogrula` ve ardından `blender-dogrulama` ile önce/sonra sayısal kapı ve görünüm IoU karşılaştırmasını yap.
6. Raporu hazırla: mesh sayısı, önce/sonra KB, doku boyutları.

**(c) Kapılar**
- **Test:** glTF validator'da 0 hata (`glb_hat validate`). IoU eşiği `blender-dogrulama` ile kontrol edilir.
- **Veri koruma:** orijinal dosyanın üzerine yazılmaz.
- **Ekran kuralı:** Blender yalnız `-b` ile çalışır, pencere açılmaz.
- **Güvenlik, erişilebilirlik ve KVKK:** yok.
### Y
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
- `skill_filo_denetim` (betik): bütün skill filosunu API'siz, salt okuma ile statik olarak denetliyor. İşin kendisi bu.
- `skill-ui` (CLI): kurulu skill'leri listeliyor. Repo ile kurulu filo arasındaki farkı çapraz kontrol ediyor.
- `context-mode-paket` (skill): büyük denetim çıktısını sandbox'ta gruplayıp bağlama yalnız özeti alıyor.

**(b) Sıra**
1. `python tools/skill_filo_denetim.py --help` ile salt-okuma ve API'siz çalışma bayraklarını teyit et.
2. Betiği koştur, çıktıyı dosyaya yaz.
3. `context-mode-paket` ile çıktıyı kural ve şiddete göre say, sorunlu skill listesini çıkar.
4. `skill-ui` ile kurulu filoyla karşılaştır: repoda olup kurulu olmayanlar ve tersi.
5. Yanlış pozitif kontrolü için 3–5 bulguyu dar aralıklı Read ile örnekle.
6. Raporu yaz: sorunlu skill, kural, şiddet.

**(c) Kapılar**
- **Maliyet:** API ve ücretli çağrı sayısı 0 olmalı.
- **Salt okuma:** koşu öncesi ve sonrası `git status` aynı kalmalı.
- **Doğruluk:** bulgular örneklenerek doğrulanır.
- **Güvenlik:** ortam değişkeni değerleri basılmaz.
- **Erişilebilirlik ve KVKK:** yok.

---
CLAUDE.md her işte önce bir `departman-*` müdür skill'inin açılmasını istiyor. Katalog kancası araçları yalnız verilen listeden seçmemi istediği ve listede `departman-*` olmadığı için planlara eklemedim.

Kontrol etmediklerim: `glb_hat`'in doku küçültme bayrağı olup olmadığına ve `skill_filo_denetim`'in bayraklarına bakmadım; ikisi de planlarda ilk adımda kontrol ediliyor. Risk: 10. iş canlı DNS'i değiştiriyor, onay ve bölge yedeği atlanmamalı.
