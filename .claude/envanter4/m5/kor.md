## 1. E-ticaret mağazası: Stripe ödeme, sipariş veritabanı şeması ve kampanya günü için yük testi
### X
**(a) Araçlar**
1. `db-sema-tasarim` (ajan): orders, order_items, payments ve processed_events tablolarını kurar. Tutar kuruş cinsinden tamsayıdır, `payment_intent_id` UNIQUE'tir.
2. `ecc:database-migrations` (skill): ileri ve geri yönlü migration yazar, yerelde dener.
3. `Payments & Billing Engineer` (ajan): Checkout/PaymentIntent akışını, 3DS'yi, idempotent webhook işlemeyi ve kısıtlı (restricted) anahtarı kurar.
4. Stripe CLI (**kurulu değil**, kurmadan önce onay alınır): `stripe listen --forward-to` ve `stripe trigger` ile test modunda webhook dener.
5. `qa-yuk-testi` (ajan): kampanya günü için k6 senaryosu, yükselme profili ve geçme eşikleri hazırlar.
6. `sec-pci-dss-kapsam` (ajan): barındırılan Checkout ile PCI kapsamını SAQ A düzeyinde tutar.

**(b) Sıra**
1. `db-sema-tasarim`: şema ve indeksler; stok düşümü sipariş ile aynı işlemde (transaction) yapılır.
2. `ecc:database-migrations`: migration ve rollback yazılır, kopya veritabanında denenir.
3. `Payments & Billing Engineer`: Checkout, imzalı webhook ve olay ID'siyle tekilleştirme kurulur.
4. Stripe CLI: başarılı, başarısız, 3DS ve tekrar gelen olaylar tetiklenir.
5. `qa-yuk-testi`: k6 yalnız staging'de koşar. Stripe çağrısı taklit edilir, çünkü test modunun hız sınırı düşüktür. Tavan: en çok hedef trafiğin 2 katı VU ve 15 dakika. Eşikler: p95 < 500 ms, hata oranı < %1.
6. `sec-pci-dss-kapsam`: kart verisinin sunucuya hiç değmediği teyit edilir.

**(c) Kapılar**
- **Test:** aynı webhook iki kez gelirse tek sipariş oluşmalı ve stok eksiye düşmemeli (`qa-entegrasyon-testi`).
- **Güvenlik:** webhook imzası doğrulanır; anahtarlar depoda değil (`gitleaks`).
- **KVKK:** adres ve e-posta için saklama ve silme kuralı (`sec-kvkk-gdpr-kontrol`).
- **Migration:** geri alma yolu yazılı olmadan üretime çıkılmaz.
### Y
**(a) Araçlar**
- `db-sema-tasarim` (ajan): sipariş, sipariş kalemi, ödeme ve idempotency tablolarını; anahtarları ve kısıtları tasarlar. Para kuruş cinsinden tam sayı tutulur.
- `ecc:database-migrations` (skill): her migration'ın geri alma adımı olur ve önce yerelde denenir (öğrenim 98).
- `engineering-payments-billing-engineer` (ajan): Checkout veya PaymentIntent akışını, 3DS'i ve imzalı, idempotent webhook'u kurar.
- `Stripe CLI` (CLI, kurulu değil, kurulum onayı gerekir): `stripe listen` ve `stripe trigger` ile webhook'u yerelde test modunda dener.
- `qa-yuk-testi` (ajan): kampanya günü için k6 senaryosu, kademeli yük artışı ve geçti/kaldı eşikleri hazırlar.
- `ecc:database-reviewer` (ajan): yük testinden sonra indeksleri, kilit beklemelerini ve yavaş sorguları inceler.

**(b) Sıra**
1. `db-sema-tasarim`: şema yazılır. `stripe_payment_intent_id` ve webhook `event_id` alanları unique olur, stok düşümü tek transaction içinde yapılır.
2. `ecc:database-migrations`: up/down migration yazılır, yerelde ileri ve geri koşulur.
3. Payments ajanı: ödeme akışı ve webhook kodlanır. Restricted (kısıtlı) anahtar kullanılır (öğrenim 97). Test ve canlı anahtarlar ayrı tutulur.
4. `Stripe CLI`: başarılı, başarısız ve aynı olayın iki kez geldiği durumlar tetiklenir; sipariş durumları doğrulanır.
5. `qa-yuk-testi`: normal trafiğin 10 katı ramp ile k6 koşulur. Stripe çağrısı mock'lanır, çünkü test modunun hız sınırı var. Eşikler: p95 < 500 ms, hata oranı < %1.
6. `ecc:database-reviewer`: yük altında çıkan yavaş sorgular ve kilitlenmeler düzeltilir, ardından 5. adım tekrar koşulur.

**(c) Kapılar**
- Test: çift webhook'un ikinci siparişi oluşturmadığını ve migration'ın geri alındığını gösteren testler.
- Güvenlik: `sec-pci-dss-kapsam` ile kart verisinin sunucuya hiç değmediği doğrulanır (hosted Checkout). `sec-sir-tarayici` ile repoda `sk_` anahtarı olmadığı taranır. Webhook imzası zorunludur.
- KVKK: `sec-kvkk-gdpr-kontrol` ile adres ve telefon verisinin saklama süresi ve silme akışı belirlenir.
- Yük: k6 eşikleri tutmazsa iş "bitti" sayılmaz. Tavan: yük testi canlı Stripe'a en çok 0 istek atar.

## 2. Mobil uygulama için tanıtım videosu, App Store ekran görüntüleri ve lansman e-postası hazırla
### X
**(a) Araçlar**
1. `vid-video-senaryo` (ajan): 20–30 saniyelik açılış (hook), akış ve çekim listesi.
2. `app-store-screenshots` (skill): App Store ve Play için açıklamalı ekran görüntüsü sayfaları üretip dışa aktarır.
3. `vid-hyperframes-kompozisyon` + `hyperframes` (kurulu): HTML/GSAP ile videoyu ücretsiz yerel render eder.
4. `ffmpeg` (CLI): App Store önizleme biçimine kodlar, dikey türevini ve web sıkıştırmasını üretir.
5. `urn-eposta-metni` (ajan): konu satırı, tek hedef ve mağaza CTA'sı.
6. `fe-eposta-sablonu` (ajan): duyarlı, karanlık modu destekleyen ve Outlook'ta bozulmayan HTML e-posta.

**(b) Sıra**
1. `vid-video-senaryo`: kısa brief ve çekim listesi.
2. `app-store-screenshots`: gerçek uygulama ekranlarından gerekli boyutlarda setler.
3. `hyperframes`: ekran kayıtları ve açıklamalarla kompozisyon kurulur, render alınır.
4. `ffmpeg`: 15–30 saniye, mağazanın istediği çözünürlükte, 30 fps; ayrıca 9:16 türev.
5. `urn-eposta-metni`: metin yazılır.
6. `fe-eposta-sablonu`: şablon kurulur, önce yalnız test listesine en çok 5 alıcıyla gönderilir.

**(c) Kapılar**
- **Mağaza kuralı:** görüntüler gerçek uygulama ekranı olmalı, boyutlar doğrulanmalı.
- **Erişilebilirlik:** videoda altyazı (`accessible-content:multimedia-accessibility`); e-postada kontrast ve alt metin.
- **KVKK / İYS:** açık rıza, abonelikten çıkma bağlantısı ve İYS kaydı (`sec-kvkk-gdpr-kontrol`).
- **Gönderim:** onaysız toplu gönderim yok.
### Y
**(a) Araçlar**
- `vid-video-senaryo` (ajan): 30–45 saniyelik tanıtım videosu için kanca, sahne akışı ve çekim listesi yazar.
- `hyperframes-paket` (skill): HTML'den video render eder. Bu yerel bir yoldur; ücretli HeyGen veya Higgsfield kullanılmaz.
- `app-store-screenshots` (skill): mağaza ekran görüntüsü sayfalarını üretir ve headless olarak dışa aktarır.
- `frontend-craft` (skill): bu iş arayüze dokunduğu için kural gereği önce bu yüklenir; ekran görüntülerinin ve e-postanın görsel dili buradan gelir.
- `urn-eposta-metni` (ajan): lansman e-postasının konu satırını, tek hedefini ve çağrı düğmesini yazar.
- `fe-eposta-sablonu` (ajan): Outlook, Gmail ve karanlık modda bozulmayan HTML şablonu kurar.

**(b) Sıra**
1. `frontend-craft`: marka yönü ve DESIGN.md belirlenir.
2. `vid-video-senaryo`: senaryo ve çekim listesi yazılır; uygulama ekran kayıtları toplanır.
3. `hyperframes-paket`: video render edilir. Dikey ve yatay iki sürüm çıkar.
4. `app-store-screenshots`: iPhone 6.9", 6.5" ve iPad boyutlarında, başlıklı ekran görüntüleri headless dışa aktarılır.
5. `urn-eposta-metni`, ardından `fe-eposta-sablonu`: metin şablona yerleştirilir, videoya poster görseliyle link verilir.
6. `frontend-craft` Bölüm 6 tur raporu ile kapanış yapılır.

**(c) Kapılar**
- Erişilebilirlik: `accessible-content:multimedia-accessibility` ile videoda altyazı veya ekrana yazılı metin kontrol edilir. E-postada görsellerin alt metni ve kontrast kontrol edilir.
- Mağaza: piksel boyutları ve metin sınırları Apple ve Google kurallarına göre kontrol edilir; başlık metinleri isteğe bağlı olarak `marketing-skills:aso` ile gözden geçirilir.
- KVKK/İYS: ticari ileti onayı ve abonelikten çıkma linki zorunludur (`sec-kvkk-gdpr-kontrol`). Onay olmadan gönderim yapılmaz.
- Maliyet: ücretli medya üretimi yoktur. Gerekirse önce tavan konur.

## 3. Blender'da ürün modeli yap, web sitesinde three.js ile göster ve sayfa performansını ölç
### X
**(a) Araçlar**
1. `blender:blender-uretim` (skill): brief, ölçüler, kod olarak sahne ve render kontrol hattı.
2. `bl-python-betik` (ajan): `blender -b` ile modeli ve PBR malzemeyi headless kurar. Ekran kuralı gereği Blender penceresi açılmaz, bu yüzden canlı MCP kullanılmaz.
3. `tools/blender_dogrula.py` + `tools/blender_gorunum.py` (betik): sayısal kontrol ve 4 Workbench + 1 Eevee görünüm kanıtı.
4. `tools/glb_hat.py` (betik): GLB'yi meshopt + webp ile optimize eder, doğrular, önceki/sonraki boyutu (KB) gösterir.
5. `fe-webgl-3d-hero` (ajan): three.js sahnesi, Meshopt çözücü ve zayıf cihaz için poster yedeği.
6. `chrome-devtools` (MCP): headless Lighthouse ve performans izi.

**(b) Sıra**
1. `blender-uretim`: ölçüler mm cinsinden; poligon bütçesi ~50 bin üçgen, GLB hedefi ≤ 2 MB.
2. `bl-python-betik`: modelleme ve malzeme.
3. `blender_dogrula` → `blender_gorunum`: ölçek, pivot ve topoloji kontrolü; PNG kanıtı.
4. `glb_hat`: dışa aktarma, optimize ve doğrulama.
5. `fe-webgl-3d-hero`: geç yükleme, DPR ≤ 2, `prefers-reduced-motion`, mobilde poster.
6. `chrome-devtools`: mobil ve masaüstünde LCP, INP, CLS ve kare süresi; model eklenmeden önce ve sonra ölçülür.

**(c) Kapılar**
- **Render ve GLB:** render kanıtı dosya olarak var; glTF doğrulayıcı 0 hata verir; GLB ≤ 2 MB.
- **Performans:** mobilde LCP ≤ 2,5 sn.
- **Erişilebilirlik:** canvas için alternatif metin, klavyeyle döndürme ve reduced-motion (`qa-erisilebilirlik-testi`).
- **Lisans:** dış doku ve HDRI yalnız CC0.
### Y
**(a) Araçlar**
- `blender-uretim` (skill, önce `blender-oturum` ile açılır): bpy ile low-poly model, malzeme ve ışık kurar. Blender headless (`-b`) çalışır.
- `blender-dogrulama` (CLI): ölçek, pivot ve topolojiyi sayısal olarak kontrol eder; Workbench ve Eevee görünümlerini IoU ile karşılaştırır.
- `glb_hat` (betik): GLB'yi meshopt ve webp ile optimize eder, doğrular, önce/sonra KB değerini raporlar.
- `web-sahne-desenleri` (skill): Blender'dan web'e aktarım desenleri (AO ve HDRI pişirme, scroll'a bağlı ürün pozu) burada.
- `frontend-craft` (skill): arayüz kuralı gereği önce yüklenir.
- `web-perf` (skill): Lighthouse ve Core Web Vitals ölçümü yapar.

**(b) Sıra**
1. `blender-uretim`: model kurulur, UV2 açılır, AO pişirilir (`blender_pisir`).
2. `blender-dogrulama`: sayısal kapı ve görünüm kanıtı alınır.
3. `glb_hat`: GLB dışa aktarılır, optimize edilir, boyutu ölçülür.
4. `frontend-craft` ve `web-sahne-desenleri`: three.js sahnesi kurulur. Döndürülen ürün yalnızca AO ve HDRI ile aydınlatılır (öğrenim 92). Zayıf cihazda yerine poster görsel gösterilir.
5. `web-perf`: mobil profilde LCP, INP ve CLS ölçülür. Eşik aşılırsa 3. adıma dönülür.
6. `frontend-craft` Bölüm 6 tur raporu ile kapanış yapılır.

**(c) Kapılar**
- 3D kalite: `blender-dogrulama` sayısal kapısı geçilir. GLB yaklaşık 2 MB'ı aşmaz (öğrenim 91).
- Performans: LCP ≤ 2,5 sn, INP ≤ 200 ms, CLS ≤ 0,1. Mobilde 3D modeli kapatmak geçerli bir seçenektir (öğrenim 90).
- Erişilebilirlik: `prefers-reduced-motion` desteklenir, canvas'a açıklayıcı metin verilir, ürün klavyeyle döndürülebilir.
- Lisans: dışarıdan alınan varlıklar yalnızca CC0 olur (`varlik_indir`).

## 4. Podcast bölümünü transkripte dök, blog yazısına çevir ve sosyal medya kliplerini çıkar
### X
**(a) Araçlar**
1. `whisper-cli` (CLI, "tahmin" etiketli, önce `--help` ile doğrulanır): yerel transkript ve SRT.
2. `dok-blog-yazisi` (ajan): transkripti yapılandırılmış blog yazısına çevirir.
3. `vid-kisa-klip-secici` (ajan): transkriptten 3–5 öne çıkan klip aralığı seçer.
4. `ffmpeg` (CLI): klipleri keser, altyazıyı videoya gömer, sesi −14 LUFS'e normalize eder.
5. `vid-sosyal-video-bicim` (ajan): 9:16 ve 1:1 biçim, güvenli alanlar.
6. `urn-sosyal-medya-icerik` (ajan): platforma özel metin ve açılış cümlesi.

**(b) Sıra**
1. `whisper-cli`: transkript ve zaman damgaları; konuşmacılar elle etiketlenir.
2. `dok-blog-yazisi`: blog yazısı; her alıntı zaman damgasıyla sese karşı doğrulanır.
3. `vid-kisa-klip-secici`: 30–60 saniyelik aday aralıklar.
4. `ffmpeg`: kesme, altyazı gömme ve ses seviyesi.
5. `vid-sosyal-video-bicim`: kırpma. Podcast yalnız sesse dalga formu ve kapak görseli eklenir.
6. `urn-sosyal-medya-icerik`: gönderiler yalnız taslak olarak hazırlanır, yayın onayla yapılır.

**(c) Kapılar**
- **KVKK:** konuğun ses ve görüntüsünün kullanımı için izin (`sec-kvkk-gdpr-kontrol`).
- **Erişilebilirlik:** kliplerde gömülü altyazı, blogda tam transkript (`accessible-content:multimedia-accessibility`).
- **Doğruluk:** alıntılar örneklem alınarak sese karşı kontrol edilir.
- **Telif ve yayın:** müzik telifi kontrol edilir; otomatik yayın yapılmaz.
### Y
**(a) Araçlar**
- `whisper-cli` (CLI): yerel transkript ve SRT üretir. Açıklaması tahmin olarak işaretli, önce `--help` ile doğrulanır.
- `daymade-ses-paket` (skill): transkriptteki isim ve terim hatalarını düzeltir.
- `ecc-icerik-pazarlama-paket` (skill): blog yazısını, SEO'yu ve sosyal medya metinlerini hazırlar.
- `vid-kisa-klip-secici` (ajan): transkriptte zirve anları bulur ve zaman damgalarını verir.
- `vid-sosyal-video-bicim` (ajan): her platform için 9:16 ve 1:1 güvenli alanları belirler.
- `ffmpeg` (CLI): klipleri keser, yeniden çerçeveler, altyazıyı videoya yakar.

**(b) Sıra**
1. `whisper-cli`: transkript ve SRT çıkarılır.
2. `daymade-ses-paket`: transkript düzeltilir, konuşmacılar etiketlenir.
3. `ecc-icerik-pazarlama-paket`: transkriptten blog yazısı çıkarılır. Bu bir dökümden çok düzenlenmiş bir makaledir; alıntılara zaman damgası verilir.
4. `vid-kisa-klip-secici`: 15–60 saniyelik 3–5 aday klip seçilir.
5. `vid-sosyal-video-bicim` ve `ffmpeg`: klipler biçimlenir ve altyazı yakılır.
6. `ecc-icerik-pazarlama-paket`: her klip için platforma uygun gönderi metni yazılır.

**(c) Kapılar**
- Doğruluk: transkriptten 3 bölüm sesle karşılaştırılır; isim ve rakamlar kontrol edilir.
- KVKK: `sec-kvkk-gdpr-kontrol` ile konuğun yayın rızası ve transkriptte geçen üçüncü kişilerin verileri kontrol edilir.
- Erişilebilirlik: kliplerde yakılmış altyazı olur, blogda tam transkript linki verilir (`accessible-content:multimedia-accessibility`).
- Telif: kliplerdeki müzik kontrol edilir. Onay olmadan yayın yapılmaz. Ücretli API yoktur (whisper yerelde çalışır).

## 5. Oyun için tanıtım sitesi, Discord bot otomasyonu ve oyuncu analitiği panosu kur
### X
**(a) Araçlar**
- `frontend-craft` (skill): arayüz kuralı gereği önce yüklenir; tanıtım sitesinin ve panonun görsel yönü buradan gelir.
- `fe-astro` (ajan): az JavaScript'li, statik tanıtım sitesi kurar.
- `n8n-mcp` (MCP): Discord otomasyonunu (duyuru, yeni sürüm, rol olayları) n8n'in Discord düğümüyle kurar. Komutlu, sürekli çalışan bir bot için özel araç yok; o durumda discord.js ile elle yazılır.
- `db-clickhouse-sorgu` (ajan): oyuncu olay tablosunu (MergeTree, sıralama anahtarı, partition) ve materialized view'ları tasarlar.
- `clickhouse` (MCP): analitik sorguları koşar ve doğrular.
- `fe-dashboard-duzeni` (ajan): panoyu düzenler (DAU, retention, funnel).

**(b) Sıra**
1. `frontend-craft` ve `fe-astro`: tanıtım sitesi kurulur (hero, fragman, Discord daveti).
2. `db-clickhouse-sorgu`: olay şeması (`player_id` takma adlı, `event`, `ts`) ve toplama view'ları tasarlanır.
3. `clickhouse`: örnek verilerle DAU ve retention sorguları doğrulanır.
4. `fe-dashboard-duzeni`: pano yazılır.
5. `n8n-mcp`: Discord akışları kurulur. Hatalar `n8n-error-handling` ile yakalanıp bildirilir.
6. `frontend-craft` Bölüm 6 tur raporu ile kapanış yapılır.

**(c) Kapılar**
- KVKK: `sec-kvkk-gdpr-kontrol` ile oyuncu kimliklerinin takma adlı tutulduğu, IP saklanmadığı ve sitede çerez onayı olduğu kontrol edilir.
- Güvenlik: Discord token'ı ve ClickHouse kimlik bilgileri yalnızca ortam değişkeninde tutulur, `sec-sir-tarayici` ile repo taranır. Toplu DM gönderilmez.
- Erişilebilirlik: site ve pano `qa-erisilebilirlik-testi` ile kontrol edilir.
- Performans: site `web-perf` ile ölçülür. Panodaki grafiklerin renk körlüğüne uygunluğu kontrol edilir.

---
Ne `threejs` skill'inin, ne Stripe CLI'nin, ne de `whisper-cli` komutunun gerçekten çalıştığını doğrulamadım. Hafızaya göre `threejs` lisanssız olduğu için kurulmamış olabilir; 3. işte bu yüzden `web-sahne-desenleri` seçildi. Stripe MCP ve HeyGen için kurulum (KUR) kararı var ama kurulu değiller ve bu planlarda kullanılmıyorlar.
### Y
**(a) Araçlar**
1. `frontend-craft` (skill): marka yönü, DESIGN.md ve tur raporu.
2. `fe-astro` (ajan): az JS'li statik tanıtım sitesi (fragman, wishlist, Discord CTA).
3. `n8n-mcp` (MCP) + `using-n8n-mcp-skills`: Discord duyuru ve `/stats` akışları. Çalışan bir n8n sunucusu ayrıca gerekir; MCP sunucunun kendisi değildir.
4. `db-clickhouse-sorgu` (ajan): MergeTree olay tablosu ve günlük özet için materialized view.
5. `db-analitik-sorgu` (ajan): DAU/MAU, D1/D7 elde tutma ve huni sorguları.
6. `fe-dashboard-duzeni` (ajan): pano yerleşimi (Grafana + ClickHouse veri kaynağı ya da basit bir sayfa).

**(b) Sıra**
1. `frontend-craft`: yön künyesi.
2. `fe-astro`: site kurulur, Lighthouse ölçülür.
3. `db-clickhouse-sorgu`: `events(player_hash, event, ts, props)` tablosu, aylık bölümleme.
4. `db-analitik-sorgu`: metrik sorguları.
5. `fe-dashboard-duzeni`: pano.
6. `n8n-mcp`: yama notu → Discord kanalı; Discord etkileşim webhook'u → ClickHouse'tan `/stats` yanıtı.

**(c) Kapılar**
- **Discord güvenliği:** etkileşim imzası Ed25519 ile doğrulanır, işleme idempotenttir (`otm-webhook-tasarimci`).
- **Hata yönetimi:** her n8n akışında hata akışı var (`n8n-error-handling`); bot token depoda değil (`gitleaks`).
- **KVKK:** oyuncu ID'si hash'lenir, sitede analitik çerez rızası alınır, saklama süresi belirlenir; yaş sınırı varsa ebeveyn izni (`sec-kvkk-gdpr-kontrol`).
- **Erişilebilirlik:** site için `qa-erisilebilirlik-testi`.
- **Discord hız sınırı:** n8n'de yeniden deneme ile karşılanır.

Doğrulamadığım kurulum durumları:
- **5. iş, ClickHouse:** hacmin yüksek olduğu varsayıldı. Oyuncu sayısı azsa yerine Postgres yeterli olur.
- **3. iş, `threejs`:** belleğe göre bu skill lisans kapısında kurulmamış olabilir; bu yüzden `fe-webgl-3d-hero` seçildi.
- **4. iş, `whisper-cli`:** "tahmin" etiketli, gerçekten kurulu olup olmadığı önce `--help` ile denenmeli.
- **Bekleyen kurulumlar:** Stripe CLI kurulu değil, kurmak için onay gerekiyor. 5. iş için ise ayrıca çalışan bir n8n sunucusu gerekiyor.

## 6. Fintech API'si: JWT kimlik doğrulama, OWASP denetimi, OpenAPI dokümanı ve CI hattı
### X
. Fintech API: JWT, OWASP, OpenAPI, CI
**(a) Araçlar**
- `departman-guvenlik` (skill): auth, API ve yayın öncesi işlerde tarama, SAST ve pentest sırasını belirler.
- `dil-openapi-sozlesme` (ajan): sözleşme koddan önce yazılır; şemalar, hata gövdeleri ve sürümleme burada sabitlenir.
- `sec-jwt-denetci` (ajan): JWT'de algoritma sabitleme, exp/aud/iss kontrolü ve anahtar döndürmeyi denetler.
- `sec-owasp-top10` (ajan): API'deki BOLA, mass assignment ve hız sınırı açıklarını OWASP kategorilerine eşler.
- `git-ci-boru-hatti` (ajan): build, test, lint ve güvenlik adımlarını önbellekli bir CI'ya bağlar.
- `gitleaks` (CLI): depoda ve git geçmişinde sızmış anahtar arar.

**(b) Sıra**
1. `departman-guvenlik` ile sırayı belirle. Yığın .NET ise `dn-identity-auth` ve `dn-openapi-dokuman` kullanılır.
2. `dil-openapi-sozlesme` ile OpenAPI 3 sözleşmesini yaz: güvenlik şeması bearer JWT, her uç noktanın 401/403/422 hata gövdeleri.
3. JWT'yi ana oturumda uygula. Testleri önce yaz: süresi dolmuş, `alg=none` ve yanlış aud taşıyan token reddedilmeli. Ardından `sec-jwt-denetci` incelesin.
4. `sec-owasp-top10` ile uç noktaları tek tek tara. Nesne düzeyi yetki ve hız sınırı açıklarını kapat.
5. `git-ci-boru-hatti` ile CI'ya build, test, OpenAPI lint, SAST ve `gitleaks` adımlarını ekle.
6. `gitleaks` ile geçmişi tara, sonra PR aç.

**(c) Kapılar**
- Test: JWT negatif senaryoları ve API sözleşme testleri yeşil.
- Güvenlik: OWASP eşlemesinde açık bulgu yok, `gitleaks` temiz.
- Canlı pentest (`owasp-top-10-testing`) yalnız yazılı izin ve sınırlı hedefle yapılır.
- KVKK/PCI: kart verisi varsa tokenizasyon gerekir (`sec-pci-dss-kapsam`). Loglarda token ya da kişisel veri olmamalı.
### Y
**(a) Araçlar**
1. `departman-guvenlik` (skill): auth ve API işi bunun alanına giriyor. Güvenlik sırasını o belirler: önce sır taraması, sonra SAST, OWASP ve KVKK.
2. `dil-openapi-sozlesme` (ajan): sözleşme koddan önce yazılır. Böylece doküman ile kod aynı kaynaktan çıkar.
3. `dn-identity-auth` (ajan): JWT üretimi, doğrulaması ve policy tabanlı yetki için. Varsayımım ASP.NET Core; yığın farklıysa yalnız bu ajan değişir.
4. `sec-jwt-denetci` (ajan): fintech için ayrı bir JWT incelemesi gerekir. Algoritma, exp/aud/iss ve anahtar rotasyonuna bakar.
5. `sec-owasp-top10` (ajan): her endpoint'i OWASP Top 10 kategorilerine eşler. BOLA, mass assignment, rate limit ve injection buraya girer.
6. `git-ci-boru-hatti` (ajan): build, test, lint, gitleaks ve OpenAPI lint'i tek hatta toplar.

**(b) Sıra**
1. `departman-guvenlik` açılır ve araç sırası alınır.
2. `dil-openapi-sozlesme` OpenAPI 3 spec'ini yazar: bearerAuth şeması, problem+json hata gövdesi, sürümleme.
3. `dn-identity-auth` JWT'yi kurar: RS256/ES256, kısa exp, refresh rotasyonu, rol/policy.
4. `sec-jwt-denetci` JWT'yi inceler. Bulgular 3. adıma geri gider.
5. `sec-owasp-top10` ve departman sırasındaki gitleaks çalışır. BOLA ve rate limit, OWASP raporunda ayrıca işaretlenir.
6. `git-ci-boru-hatti` CI'ı kurar. Kapıların hepsi CI'da zorunlu olur.

**(c) Kapılar**
- **Test:** Negatif auth testleri. Süresi dolmuş token, yanlış aud, `alg=none` ve başka kullanıcının kaynağı 401 ya da 403 dönmeli.
- **Güvenlik:** gitleaks 0 bulgu vermeli. OWASP raporunda kritik ve yüksek bulgu kalmamalı.
- **Sözleşme:** OpenAPI lint geçmeli ve spec ile endpoint arasında fark olmamalı (CI).
- **KVKK/PCI:** Loglarda finansal veri ya da token olmamalı (departman-guvenlik KVKK adımı). Kart verisi varsa PCI kapsamı ayrıca incelenmeli.
- **Erişilebilirlik:** Yok, UI yok.

## 7. .NET Blazor iç yönetim paneli: EF Core şeması, rol bazlı yetki ve xUnit testleri
### X
. .NET Blazor yönetim paneli: EF Core, rol yetkisi, xUnit
**(a) Araçlar**
- `departman-backend-dotnet` (skill): EF, ASP.NET Core ve NuGet sırasını belirler.
- `frontend-craft` (skill): UI işi olduğu için önce yüklenmesi zorunlu; Bölüm 6 tur raporu da bundan çıkar.
- `dn-efcore-migration` (ajan): migration'ları üretir ve veriyi koruyup korumadığını inceler.
- `dn-identity-auth` (ajan): Identity, roller ve policy tabanlı yetkiyi kurar.
- `sec-yetkilendirme-matrisi` (ajan): rol × işlem matrisini çıkarır, her sayfanın ve uç noktanın bunu uyguladığını kontrol eder.
- `dn-xunit-test-yazar` (ajan): xUnit testlerini AAA düzeniyle yazar.

**(b) Sıra**
1. `departman-backend-dotnet` ile sırayı al, `frontend-craft` ile panelin tasarım yönünü belirle.
2. Varlıkları ve Fluent API yapılandırmasını ana oturumda yaz. Migration'ı `dn-efcore-migration` üretsin ve incelesin.
3. `dn-identity-auth` ile rolleri ve policy'leri kur. Blazor tarafında `[Authorize(Policy=…)]` ve `AuthorizeView` kullan.
4. `sec-yetkilendirme-matrisi` ile matrisi çıkar. Açık kalan sayfa varsa düzelt.
5. `dn-xunit-test-yazar` ile testleri yaz: matristeki her rol/işlem çifti için bir yetki testi ve SQLite in-memory ya da container üzerinde DbContext testleri.
6. `rtk dotnet test` ile koş. `--nologo` kullanma, xunit.v3/MTP'de çıkış kodu 5 veriyor; yerine `DOTNET_NOLOGO` kullan.

**(c) Kapılar**
- Test: `dotnet test` yeşil, matristeki her çift test edilmiş.
- Migration: geri alma yolu yazılı, önce veri kopyasında denenmiş.
- Erişilebilirlik: `frontend-craft` tur raporu tamam (klavye ve kontrast).
- Güvenlik: bağlantı dizesi depoda değil (`gitleaks`).
### Y
**(a) Araçlar**
1. `departman-backend-dotnet` (skill): .NET, EF ve API işinin sırasını belirler.
2. `frontend-craft` (skill): panel bir UI işi. Kural gereği önce bu yüklenir ve Section 6 tur raporu çıkarılır.
3. `dn-efcore-modelleme` (ajan): entity, ilişki ve Fluent API yapılandırması ile ilk migration için.
4. `dn-identity-auth` (ajan): Identity, roller ve policy tabanlı yetki için.
5. `sec-yetkilendirme-matrisi` (ajan): rol × eylem matrisini çıkarır. Her sayfa ve servisin bu matrise uyduğunu kontrol eder.
6. `dn-xunit-test-yazar` (ajan): matristen parametrik xUnit testleri ve EF entegrasyon testleri yazar.

**(b) Sıra**
1. `departman-backend-dotnet` ve `frontend-craft` yüklenir.
2. `dn-efcore-modelleme` şemayı ve ilk migration'ı çıkarır (`rtk dotnet ef`).
3. `dn-identity-auth` rolleri ve policy'leri kurar (Admin/Editor/Viewer). Yetki servis katmanında uygulanır.
4. Blazor sayfaları `frontend-craft` disipliniyle yazılır. AuthorizeView yalnız görünümü yönetir; asıl kontrol sunucuda kalır.
5. `sec-yetkilendirme-matrisi` her rol × eylem hücresini kodla eşler.
6. `dn-xunit-test-yazar` matristeki her hücre için bir test yazar ve testler koşulur.

**(c) Kapılar**
- **Test:** xUnit yeşil olmalı ve matristeki her hücrenin bir testi olmalı. xunit.v3 kullanılırsa `--nologo` yerine `DOTNET_NOLOGO` verilir; bayrak exit 5'e yol açıyor.
- **Güvenlik:** Sunucu tarafında yetki eksiği ve IDOR kalmamalı; `sec-yetkilendirme-matrisi` raporu temiz olmalı.
- **Migration:** `dotnet ef migrations script` ile üretilen SQL elle incelenir; veri kaybı olmamalı.
- **Erişilebilirlik:** `frontend-craft` Section 6 tur raporu ve klavyeyle gezinme kontrolü.
- **KVKK:** Personel verisi varsa loglarda yer almamalı.

## 8. Müşteri destek sohbet botu: RAG, kişisel veri maskeleme ve LLM maliyet izleme
### X
**(a) Araçlar**
1. `pia-generation` (skill): veri bir LLM sağlayıcısına gittiği için yurt dışı aktarım söz konusu. KVKK VKED/PIA taslağı bu yüzden ilk adımda hazırlanır.
2. `RAG Pipeline Engineer` (ajan): chunking, hibrit arama (BM25 + vektör), kaynak alıntılı yanıt ve retrieval eval'i için.
3. `sec-llm-pii-maskeleme` (ajan): kişisel veriyi LLM'e gitmeden önce maskeler.
4. `ecc:cost-aware-llm-pipeline` (skill): model kademeleri, istem önbelleği, istek başı token tavanı ve yedek sağlayıcı için.
5. `sentry-setup-ai-monitoring` (skill): her LLM çağrısının token, maliyet ve gecikmesini izler; bütçe alarmı kurar.
6. `ml-llm-degerlendirme` (ajan): altın soru seti ile regression kapısı kurar.

**(b) Sıra**
1. `pia-generation` hangi verinin işlendiğini, saklama süresini ve aktarımın dayanağını yazar.
2. `RAG Pipeline Engineer` bilgi tabanını indeksler ve kaynaklı yanıt akışını kurar.
3. `sec-llm-pii-maskeleme` maskelemeyi kurar:
   - Kapsam hem kullanıcı mesajı hem de getirilen belgedir.
   - Maskelenecekler: TCKN, telefon, e-posta, IBAN.
   - Maskeli değeri gerçek değere geri eşleme yalnız sunucuda yapılır.
4. `ecc:cost-aware-llm-pipeline` kademeli modelleri ve token tavanını kurar. Ücretsiz katmana bağlanılmaz; yedek sağlayıcı tutulur.
5. `sentry-setup-ai-monitoring` izlemeyi kurar: çağrı başı maliyet, günlük ve aylık tavan alarmı.
6. `ml-llm-degerlendirme` eval setini hazırlar: doğruluk, kaynaksız yanıt oranı, PII sızıntısı ve prompt injection vakaları. Eval koşusu en çok 50 ücretli çağrıyla sınırlı.

**(c) Kapılar**
- **KVKK:** PIA onaylanmalı. Birim testinde bilinen PII örnekleri sağlayıcıya giden payload'da ve loglarda görünmemeli.
- **Güvenlik:** Prompt injection eval vakaları geçmeli; gitleaks 0 bulgu vermeli.
- **Kalite:** Eval doğruluğu eşiğin üstünde olmalı, kaynaksız yanıt oranı tavanın altında kalmalı.
- **Maliyet:** Aylık sayısal tavan ve aşımda alarm.
- **Erişilebilirlik:** Sohbet arayüzü yazılırsa `frontend-craft` gerekir; bu da listeye 7. araç olarak eklenmek zorunda kalır.
### Y
. Destek sohbet botu: RAG, kişisel veri maskeleme, maliyet izleme
**(a) Araçlar**
- `RAG Pipeline Engineer` (ajan): parçalama, hibrit arama ve yeniden sıralamayı ölçümle tasarlar.
- `sec-llm-pii-maskeleme` (ajan): kişisel veriyi dış LLM'e gitmeden önce maskeler.
- `sec-kvkk-gdpr-kontrol` (ajan): veri akışını KVKK yükümlülüklerine eşler (saklama, silme, yurt dışı aktarım).
- `ecc:cost-aware-llm-pipeline` (skill): görevleri model katmanlarına yönlendirir ve bütçe tavanı koyar.
- `sentry-setup-ai-monitoring` (skill): LLM çağrısı başına token, maliyet ve gecikmeyi izler.
- `promptfoo-evaluation` (plugin): doğruluk, maskeleme ve istem enjeksiyonu için regresyon testleri koşar.

**(b) Sıra**
1. `sec-kvkk-gdpr-kontrol` ile hangi alanların kişisel veri olduğunu ve saklama sürelerini çıkar.
2. `RAG Pipeline Engineer` ile indeksleme ve getirme tasarımını yap. Belgeler indekslenmeden önce maskelenir.
3. `sec-llm-pii-maskeleme` ile maskeleme katmanını hem gelen soruya hem bağlama uygula. Testleri önce yaz: TCKN, IBAN, telefon ve e-posta örnekleri.
4. `ecc:cost-aware-llm-pipeline` ile basit sorular ucuz modele gitsin. Her konuşmaya jeton tavanı koy.
5. `sentry-setup-ai-monitoring` ile çağrı başına maliyeti ölç ve eşik aşılınca alarm ver.
6. `promptfoo-evaluation` ile altın soru seti ve enjeksiyon senaryolarını koş. Eval tavanı en çok 200 çağrı.

**(c) Kapılar**
- KVKK: maskeleme testleri yeşil, LLM'e giden logda ham kişisel veri yok.
- Güvenlik: istem enjeksiyonu senaryoları geçiyor.
- Maliyet: konuşma başına ve günlük bütçe tavanı sayıyla yazılı, alarm kurulu.
- Kalite: eval başarı eşiği yayından önce sabitlenmiş.

## 9. Kubernetes'e taşınan mikroservisler için gözlemlenebilirlik, alarm ve felaket kurtarma planı
### X
**(a) Araçlar**
1. `ops-k8s-is-yuku` (ajan): probe, requests/limits, PDB ve HPA. Sağlık sinyali her şeyin temeli olduğu için önce gelir.
2. `ops-dagitik-izleme` (ajan): OpenTelemetry ile context taşıma, span adlandırma ve örnekleme.
3. `ops-loki-log` (ajan): yapısal log, düşük kardinaliteli etiketler ve trace_id bağlantısı.
4. `ops-prometheus` (ajan): RED metrikleri, SLO ve burn-rate alarm kuralları.
5. `ops-grafana-pano` (ajan): servis başına RED, küme düzeyinde USE ve log/trace bağlantıları.
6. `ops-felaket-kurtarma` (ajan): RTO/RPO hedefleri, yedekleme, failover ve tatbikat planı.

Eşleşen bir `departman-*` ops skill'i listede yok.

**(b) Sıra**
1. `ops-k8s-is-yuku` probe'ları, kaynak sınırlarını ve PDB'yi kurar.
2. `ops-dagitik-izleme` OTel SDK'sını ve Collector'ı DaemonSet olarak kurar.
3. `ops-loki-log` JSON log şemasını ve etiket bütçesini belirler.
4. `ops-prometheus` SLO'ları tanımlar, çok pencereli burn-rate alarmlarını yazar ve Alertmanager yönlendirmesini kurar. Her alarmın bir runbook linki olur.
5. `ops-grafana-pano` panoları kurar.
6. `ops-felaket-kurtarma` DR planını çıkarır:
   - Servis başına RTO/RPO hedefi.
   - Velero ile küme yedeği ve PV snapshot.
   - Veritabanı için PITR.
   - Bölge kaybı senaryosu.
   - Çeyreklik tatbikat takvimi.

**(c) Kapılar**
- **Alarm testi:** `promtool test rules` ile alarm kurallarının birim testi. Staging'de bilinçli hata enjekte edilir ve alarmın düşüp düşmediğine bakılır.
- **DR tatbikatı:** Boş bir namespace ya da kümeye geri yükleme yapılır. Ölçülen RTO/RPO hedefle karşılaştırılır.
- **Kardinalite:** Aktif seri sayısına bir tavan konur.
- **Güvenlik/KVKK:** Loglarda token ve PII olmamalı; log saklama süresi yazılmalı.
- **Erişilebilirlik:** Yok.

Varsayım: bulut sağlayıcı belirsiz, plan sağlayıcıdan bağımsız yazıldı.
### Y
. Kubernetes mikroservisleri: gözlemlenebilirlik, alarm, felaket kurtarma
**(a) Araçlar**
- `ecc:kubernetes-patterns` (skill): probe, kaynak limiti, RBAC ve PDB manifest kalıpları.
- `ops-dagitik-izleme` (ajan): OpenTelemetry iz yayılımı, span adları ve örnekleme.
- `ops-prometheus` (ajan): metrikler, PromQL ve kardinalitesi düşük alarm kuralları.
- `ops-grafana-pano` (ajan): RED/USE panoları; panodan loga ve ize bağlantı.
- `ops-felaket-kurtarma` (ajan): RTO/RPO hedefleri, yedek, failover ve tatbikat planı.
- `dok-runbook` (ajan): her alarm için teşhis ve geri alma adımları.

**(b) Sıra**
1. `ecc:kubernetes-patterns` ile probe, limit ve PDB eksiklerini kapat. Küme AKS ise `azure:azure-kubernetes` da kullanılır.
2. `ops-dagitik-izleme` ile OTel collector'ı kur ve servisler arası trace context taşınsın.
3. `ops-prometheus` ile SLO tabanlı alarmları yaz (burn-rate). Alarmlar belirtiye göre olsun, nedene göre değil.
4. `ops-grafana-pano` ile servis başına RED panosu kur.
5. `ops-felaket-kurtarma` ile RTO/RPO değerlerini, etcd/Velero ve veritabanı PITR planını ve tatbikat takvimini çıkar.
6. `dok-runbook` ile her alarma bir runbook bağla.

**(c) Kapılar**
- Doğrulama: `promtool check rules` ve `promtool test rules` yeşil; manifestler `kubectl --dry-run=server` ya da kubeconform'dan geçiyor.
- DR: geri yükleme tatbikatı yapılmış, ölçülen RTO/RPO hedefin içinde.
- Güvenlik: manifestlerde sır yok (`gitleaks`), RBAC en az yetkiyle.
- Gürültü: alarm başına runbook var, deneme haftasında yanlış alarm sayısı kaydedilmiş.

## 10. Veri hattı: CSV içe aktar, temizle, Postgres'e yükle ve haftalık Excel raporunu e-postayla gönder
### X
. Veri hattı: CSV → temizle → Postgres → haftalık Excel e-postası
**(a) Araçlar**
- `departman-veri-db` (skill): şema, yükleme ve sorgu sırasını belirler.
- `otm-csv-temizleyici` (ajan): kodlama, ayraç, Türkçe ondalık biçimi ve tırnak sorunlarını çözer.
- `supabase-postgres-best-practices` (skill): Postgres'e dokunmadan önce yüklenmesi kural.
- `example-skills:xlsx` (skill): tipli sütunlu, formüllü haftalık rapor üretir.
- `otm-mail-otomasyon` (ajan): şablon, gönderim kısıtı ve onaysız gönderim yapılmaması kuralı.
- `otm-zamanlanmis-gorev` (ajan): haftalık zamanlama, kilit ve log.

**(b) Sıra**
1. `departman-veri-db` ile sırayı al, `supabase-postgres-best-practices` skill'ini yükle.
2. `otm-csv-temizleyici` ile temizleme betiğini yaz. Bozuk satırlar ayrı bir ret dosyasına düşsün. Testleri önce yaz: BOM, `;` ayraç ve `1.234,56` biçimi.
3. Veriyi staging tablosuna yükle, ardından ana tabloya upsert et; böylece aynı dosya iki kez yüklenirse sonuç değişmez. Migration'ın geri alma yolu yazılı olsun.
4. `example-skills:xlsx` ile haftalık özet sorgusundan raporu üret.
5. `otm-mail-otomasyon` ile gönderimi kur. İlk koşu yalnız kendine gider.
6. `otm-zamanlanmis-gorev` ile haftalık çalıştır. Hata olursa alarm verilsin; sessiz başarısızlık olmasın.

**(c) Kapılar**
- Test: gelen satır sayısı = yüklenen + reddedilen; aynı dosyanın ikinci yüklemesinde satır sayısı değişmiyor.
- Güvenlik: bağlantı dizesi ve SMTP bilgisi ortam değişkeninde (`gitleaks` temiz).
- KVKK: kişisel veri varsa `sec-kvkk-gdpr-kontrol` ile saklama ve alıcı listesi kontrol edilir; rapora gereken en az alan konur.
- Kapanış: xlsx gerçekten açılıyor. Gönderim tavanı haftada en çok 1 e-posta ve sabit alıcı listesi.

Yığın belirtilmediği için hiçbir kod tabanı incelenmedi; araç seçimleri genel varsayıma dayanıyor. 6. işin dili .NET ya da başka bir yığın çıkarsa araç listesi değişir.
### Y
**(a) Araçlar**
1. `departman-veri-db` (skill): Postgres sırasını belirler. Bu sıra `supabase-postgres-best-practices` skill'ini de yükler; öğrenim kaydı Postgres'e dokunmadan önce bunu istiyor.
2. `otm-csv-temizleyici` (ajan): encoding (UTF-8/Windows-1254), ayırıcı, TR ondalık ve tarih biçimi sorunları için.
3. `db-veri-kalitesi` (ajan): yüklemeden önce SQL ile tekrar, null ve aralık kontrolü yapar.
4. `dok-xlsx-tablo` (ajan): tipli sütunlu, özet sayfalı xlsx raporu üretir (openpyxl).
5. `otm-zamanlanmis-gorev` (ajan): haftalık zamanlama, kilit ve log için.
6. `otm-mail-otomasyon` (ajan): e-posta şablonu, ek ve gönderim kısıtı için.

**(b) Sıra**
1. `departman-veri-db` şemayı kurar: staging ve hedef tablo, doğal anahtarda UNIQUE.
2. `otm-csv-temizleyici` pandas ile temizleme adımını yazar.
3. `db-veri-kalitesi` staging tablosunda kontrolleri koşar. Reddedilen satırlar ayrı dosyaya yazılır; red oranı eşiği aşılırsa yükleme durur.
4. Yükleme tek transaction'da yapılır: COPY ile staging'e, oradan `INSERT … ON CONFLICT` ile hedef tabloya (departman-veri-db).
5. `dok-xlsx-tablo` haftalık sorguyu xlsx raporuna döker.
6. `otm-zamanlanmis-gorev` ve `otm-mail-otomasyon` haftalık işi ve gönderimi kurar. İlk koşu yalnız sana gider; gönderim haftada en çok 1 kez.

**(c) Kapılar**
- **Test:** pytest ile bozuk CSV fikstürlerinden beklenen temiz çıktı alınmalı. Aynı dosya iki kez yüklendiğinde satır sayısı değişmemeli (idempotency).
- **Veri kalitesi:** Red oranı eşiği.
- **Güvenlik:** DB ve SMTP sırları env'de tutulmalı; gitleaks 0 bulgu vermeli; SQL parametreli olmalı.
- **KVKK:** CSV kişisel veri içeriyorsa e-posta ekinde yalnız gerekli alanlar kalmalı ya da maskelenmeli. Alıcı listesi sınırlı olmalı; saklama süresi yazılmalı.
- **Onay:** İlk dış gönderim onayla yapılır.
- **Erişilebilirlik:** Yok.

---
Hiçbir iş yapılmadı, dosya yazılmadı; plan dışında bir araç da çalıştırılmadı. 6 araç sınırı yüzünden bazı ajanlar listeye girmedi: `gitleaks` ve `supabase-postgres-best-practices` ilgili departman skill'inin sırasından çağrılıyor, `sec-istem-enjeksiyon-savunma` 8'de eval setinin içine alındı. Strix pentest, ücretli bir çağrı tavanı tanımlanmadığı için plana konmadı.

## 11. Tüm ajan tanımlarının description alanlarını anlamı bozmadan kısa tek satıra sıkıştır. Ajan listesinin bağlamda tuttuğu jetonu önce ve sonra ölç.
### X
**(a) Araçlar**
- `departman-verimlilik` (skill): jeton tasarrufu işlerinde araç sırasını bu belirliyor.
- `python tools/ajan_katalog.py` (betik): ajanları ad, model, tek satır ve yol olarak listeliyor. Düzenlenebilir ajanlarla plugin ajanlarını buradan ayırırım.
- `ajn-ajan-tanimi-yazar` (ajan): kısa ve tek satırlık description kuralını uyguluyor.
- `claude -p --output-format json` (PowerShell'den çalışan CLI): gerçek girdi jetonunu önce ve sonra ölçüyor. `/context` yalnızca yerel tahmin verdiği için onun yerine bu kullanılıyor (öğrenim 105).
- `python tools/token_olc.py` (betik): oturum jsonl dosyalarından ikinci bir ölçüm alıyor.
- `python tools/tetik_olc.py` (betik): description kısalınca doğru ajanın hâlâ seçilip seçilmediğini ölçüyor. Anlamın bozulmadığını bu gösterir.

**(b) Sıra**
1. `departman-verimlilik` yüklenir. Temiz bir `claude -p` oturumunda boş istem 3 kez koşulur ve input_tokens medyanı temel değer olur. `token_olc` ile karşılaştırılır.
2. `ajan_katalog.py` ile düzenlenebilir ajanlar ve description uzunlukları çıkarılır. Plugin ve yönetilen ajanların dosyası değiştirilemez; bunlar raporda ayrıca listelenir.
3. `ajn-ajan-tanimi-yazar` kuralıyla toplu yeniden yazım yapılır: tek satır, en çok ~100 karakter, "ne yapar; ne zaman" biçiminde, ayırt edici tetik kelimesi korunur. Çok satırlı örnek blokları atılır. description dışındaki alanlara dokunulmaz.
4. Frontmatter doğrulanır: YAML ayrıştırma testi geçmeli, iki ajanın description'ı aynı olmamalı.
5. Aynı istem setiyle `tetik_olc` önce ve sonra koşulur; doğru ajan seçim oranları karşılaştırılır.
6. Ajan tanımları oturum ortasında yüklenmediği için ölçüm yeni bir `claude -p` oturumunda tekrarlanır. Fark sayıyla yazılır, ardından `ajan_katalog` yenilenir.

**(c) Kapılar**
- Test: YAML ve frontmatter için pytest.
- Kalite: tetik oranı öncekinin altına düşmemeli (`tetik_olc`).
- Maliyet tavanı: jeton ölçümü en çok 8 çağrı, tetik ölçümü en çok 40 çağrı.
- Güvenlik: commit öncesi gitleaks.
- KVKK: yok.
### Y
**(a) Araçlar**
1. `departman-verimlilik` (skill): Jeton işinde adım sırasını bu yönetici skill belirliyor.
2. `ajan_katalog` (betik): Bütün ajanları ad, model, tek satır açıklama ve dosya yolu olarak listeliyor. Böylece hangi tanımların düzenlenebildiği görülüyor.
3. `claude -p --output-format json` (CLI): Öncesi ve sonrası gerçek girdi jetonuyla ölçülüyor (öğrenim 105). PowerShell'den çalıştırılacak; `/context` yerel bir tahmine düşebildiği için kullanılmıyor.
4. `plugin-dev:agent-development` (skill): Açıklamanın "ne yapar + ne zaman" kuralını veriyor. Örnek blokları açıklamadan gövdeye taşınıyor.
5. `ajn-ajan-tanimi-yazar` (alt ajan, sonnet): Açıklamaları partiler halinde tek satıra indiriyor.
6. `tetik_olc` (betik): Kısaltılan açıklamayla ajanın hâlâ doğru istekte seçilip seçilmediğini ölçüyor.

**(b) Sıra**
1. `departman-verimlilik` açılır. `ajan_katalog` ile envanter çıkarılır. Yalnız düzenlenebilir ajanlar kapsama alınır: repodakiler ve `~/.claude/agents` içindekiler. Plugin ajanları kapsam dışında kalır; kaç tane olduğu rapora yazılır.
2. Önce ölçümü: `claude -p` boş istemle 3 kez koşulur ve girdi jetonlarının medyanı alınır. Ajan listesi payını ayırmak için ajanlar kapalıyken bir fark ölçümü de yapılır.
3. `plugin-dev:agent-development` kurallarıyla `ajn-ajan-tanimi-yazar` açıklamaları yeniden yazar. Hedef en çok ~100 karakterlik tek satırdır; tetik sözcükleri korunur.
4. Ana oturumda örneklem okunur (%10). Frontmatter'ın YAML olarak okunabildiği kontrol edilir.
5. Sonra ölçümü yeni bir `claude -p` oturumunda yapılır, çünkü oturum ortasında değişen ajan tanımları yüklenmiyor.
6. `tetik_olc` öncesi ve sonrası aynı istem setiyle koşulur. İsabeti düşen ajanın açıklaması eski haline döner.

**(c) Kapılar**
- Bütün `.md` dosyaları YAML olarak okunabilmeli (test).
- `git diff` yalnız `description:` satırlarına dokunmalı.
- `tetik_olc` isabeti düşmemeli.
- Jeton farkı 3 koşunun medyanıyla raporlanır.
- Güvenlik ve KVKK açısından uygulanacak bir kapı yok.

## 12. Blender'da düşük poligonlu bir Türk kahvesi makinesi modelle. Parçaları ayrı nesneler olsun, exploded-view animasyonu hazırla ve headless bpy betiğiyle web için GLB olarak dışa aktar.
### X
**(a) Araçlar**
- `blender-oturum` + `blender-uretim` (skill): Blender işinde önce bunlar yüklenir; bpy ürün modelleme kurallarını veriyor.
- `animasyon-atolyesi` (skill): hazır ve ölçülmüş bir "Blender patlatılmış görünüm" tarifi var.
- `bl-python-betik` (ajan): modelleme, malzeme, anahtar kareler ve dışa aktarma için tek bir headless betik yazar.
- `python tools/bpy_kontrol.py` (betik): betikte var olmayan bpy özniteliği ya da operatörü statik olarak yakalar.
- `blender-dogrulama` (CLI; `blender_dogrula` + `blender_gorunum`): sayısal kontrol ve görünüm kanıtı üretiyor.
- `python tools/glb_hat.py` (betik): meshopt ve webp ile küçültüp doğrular, önce/sonra KB verir.

**(b) Sıra**
1. `blender-oturum` ve `blender-uretim` yüklenir. Parça listesi çıkarılır: taban, gövde, su haznesi, cezve, cezve kapağı, kontrol paneli ve düğmeler. Hepsi ayrı nesne olur; pivot montaj noktasına konur ve adlar anlamlı verilir. Toplam ≤5k üçgen hedeflenir.
2. `bl-python-betik` tek bir `kahve.py` yazar; betik `blender -b -P` ile headless koşar (ekran kuralı). İçeriği: model, düşük maliyetli Principled malzemeler ve `animasyon-atolyesi` tarifine göre patlatma anahtar kareleri. Parçalar montaj ekseni boyunca sırayla açılır: 0–60. kare ayrılma, 60–90 bekleme, 90–150 birleşme, döngü.
3. `bpy_kontrol` betiği koşmadan önce statik olarak denetler.
4. Betik koşar. `blender_dogrula` nesne ve üçgen sayısını, uygulanmış ölçeği, pivotu ve non-manifold durumunu kontrol eder. `blender_gorunum` 4 Workbench ve 1 Eevee karesi alır.
5. GLB dışa aktarılır: animasyon dahil, modifier'lar uygulanmış, +Y yukarı. Ardından `glb_hat` optimize eder, doğrular ve inspect özetini basar.
6. Inspect çıktısında animation count ≥1 ve doğru nesne sayısı kontrol edilir; boyut raporlanır.

**(c) Kapılar**
- Statik kontrol: `bpy_kontrol`.
- Geometri: `blender_dogrula` (topoloji, ölçek, pivot).
- Görsel: `blender_gorunum` kanıt sayfası.
- GLB: glTF doğrulayıcı ve boyut bütçesi ≤2 MB (öğrenim 99), hedef <500 KB. Bu kontroller `glb_hat` içinde.
- MCP kullanılırsa `blender_bekci` hook'u devrede kalır.
- KVKK ve erişilebilirlik: yok.
### Y
**(a) Araçlar**
1. `blender:blender-uretim` (skill): Brief, ölçüler, sahnenin kod olarak kurulması ve render kontrolleri. Düşük poligon bütçesi burada belirlenir; örneğin toplam ≤5k üçgen.
2. `bl-python-betik` (alt ajan): Modelleme, animasyon ve dışa aktarma için tek bir headless bpy betiği yazar. Betik `blender -b --python` ile çalışır.
3. `animasyon-atolyesi` (skill): İçindeki hazır Blender patlatılmış görünüm tarifi kullanılır.
4. `glb_hat` (betik): GLB'yi meshopt ve webp ile optimize eder, doğrular, inceleme özeti çıkarır ve önce/sonra KB değerini verir.
5. `blender_dogrula` (betik): Nesne sayısı, üçgen sayısı ve isimlerden oluşan sayısal kapı.
6. `blender_gorunum` (betik): 4 Workbench görünümü (ön, yan, üst, 3/4) ve 1 Eevee kahraman karesiyle görsel kanıt üretir.

**(b) Sıra**
1. `blender-uretim` ile brief hazırlanır. Parçalar: taban, gövde, su haznesi, cezve yuvası, cezve, kapak ve düğme paneli; her biri ayrı nesne olacak. Gerçek ölçüler mm cinsinden yazılır ve poligon bütçesi belirlenir.
2. `bl-python-betik` betiği yazar. Her parça ayrı mesh olur ve pivotu montaj noktasına konur; uygulanmamış modifiye kalmaz.
3. `animasyon-atolyesi` tarifiyle patlatılmış görünüm hazırlanır. Her parça kendi ekseninde kademeli olarak açılır; kare anahtarları yalnız konum ve döndürme içindir. Animasyon tek klip olarak dışa aktarılır.
4. Aynı betikte glTF dışa aktarımı yapılır: animasyon açık, yalnız gereken nesneler seçili. Ardından `glb_hat` ile optimize ve doğrulama yapılır.
5. `blender_dogrula` ve ardından `blender_gorunum` koşulur; görüntü dosyaları kanıt olarak alınır.
6. Kapanışta Blender açık kalmaz: headless süreç biter ve `.blend` dosyası kaydedilir.

**(c) Kapılar**
- glTF doğrulaması 0 hata vermeli.
- GLB ≤2 MB olmalı (öğrenim 99).
- Parça sayısı brief ile aynı olmalı.
- Workbench ve Eevee kareleri görüntü dosyası olarak kanıtlanmalı; "oldu" demek yetmez.
- Ekran kuralı: yalnız `-b` kullanılır, pencere açılmaz.
- Varlık indirilmiyor; indirilirse yalnız CC0.
- Tarif bu betikleri "kurulu değil" diye listeliyor. İlk adımda `--help` ile var olup olmadıkları kontrol edilir. Yoksa yedek olarak `bl-gorsel-ani-kontrol` ve `bl-glb-disa-aktar` kullanılır.

## 13. Web için test edilmiş bir animasyon tarif kütüphanesi hazırla: GSAP SplitText ile başlık girişi, View Transitions ile sayfa geçişi ve dotLottie ikon animasyonu. Tarifler 60 fps ve reduced-motion kurallarına uysun.
### X
**(a) Araçlar**
1. `frontend-craft` (plugin): Arayüz işinde zorunlu ilk adım; `departman-frontend` sırasıyla birlikte kullanılır. Kapanışta Bölüm 6 tur raporu yazılır.
2. `animasyon-atolyesi` (skill): Var olan ölçülmüş tarif kütüphanesi. Yeni tarifler onun biçimine eklenir, ayrı bir kütüphane kurulmaz.
3. `gsap-skills:gsap-core` (skill): SplitText için `autoSplit`/`onSplit` ve `aria`, reduced-motion için `gsap.matchMedia`.
4. `context7` (MCP): dotLottie-web ve View Transitions için güncel API bilgisi. Burada `@view-transition` kuralı MPA içindir, `startViewTransition` SPA içindir.
5. `chrome-devtools` (MCP): Performans izi alınır; düşen kare sayısı ve uzun görevler 4× CPU kısıtlamasıyla ölçülür.
6. `playwright-cli` (CLI): Tarif testleri. `reducedMotion: 'reduce'` öykünmesi, geçiş sonrası odak ve ikonun duraklatılması kontrol edilir.

**(b) Sıra**
1. `frontend-craft` ve `animasyon-atolyesi` biçimi okunur. Her tarif aynı yapıda olur: kod, kullanım durumu, bütçe ve reduced-motion kolu.
2. `context7` ile üç API'nin güncel imzaları doğrulanır. Burada GSAP lisansı da okunur: standart lisans, MIT değil; koşullar rapora yazılır.
3. Başlık girişi: `gsap-core` ile SplitText kelime/satır bölmesi yapılır. Yalnız `transform` ve `opacity` canlandırılır. Reduced-motion açıkken metin hareketsiz ve hemen görünür olur.
4. Sayfa geçişi: MPA için `@view-transition { navigation: auto }` ve `::view-transition-*` kuralları yazılır. Desteklenmeyen tarayıcıda anında geçişe düşülür. Reduced-motion açıkken geçiş animasyonu kapanır.
5. İkon: dotLottie-web ile canvas oynatıcı kurulur. Ekran dışındayken donar; reduced-motion açıkken otomatik oynatma kapanır ve ikon tek karede durur.
6. `playwright-cli` testleri ve `chrome-devtools` izi her tarif için koşulur. Sonuçlar tarife ölçüm satırı olarak eklenir.

**(c) Kapılar**
- Performans: 4× CPU kısıtlamasında düşen kare olmamalı ve 50 ms'yi aşan uzun görev bulunmamalı (`chrome-devtools`).
- Reduced-motion: Her tarifte transform veya geçiş çalışmadığı Playwright öykünmesiyle doğrulanır.
- Erişilebilirlik: SplitText sonrası ekran okuyucu kelime değil tam başlık okumalı (`aria`). Geçişten sonra odak kaybolmamalı. Döngüde oynayan ikonun durdur seçeneği olmalı.
- Lisans: GSAP koşulları rapora yazılır; dotLottie-web lisansı kontrol edilir.
### Y
**(a) Araçlar**
- `frontend-craft` (plugin): UI işinde zorunlu ilk yükleme; Bölüm 6 tur raporu buradan geliyor.
- `animasyon-atolyesi` (skill): tarif kütüphanesi buraya giriyor; tarif biçimini ve ölçüm kuralını bu belirliyor.
- `gsap-skills:gsap-core` + `gsap-performance` (skill): SplitText API'si ve jank/fps kuralları için.
- `context7` (MCP): SplitText, View Transitions ve `@lottiefiles/dotlottie-web` için güncel API ve sürüm bilgisi.
- `playwright-cli` (CLI): reduced-motion emülasyonu ve son durum testleri.
- `chrome-devtools` (MCP): performans izi alıp kare süresini ve düşen kareleri ölçmek için.

**(b) Sıra**
1. `frontend-craft` ve `animasyon-atolyesi` yüklenir. Tarif biçimi belirlenir: demo HTML, JS, "ne zaman kullanılır", performans bütçesi ve reduced-motion davranışı.
2. `context7` ile güncel dokümanlar çekilir ve sürümler pinlenir. Kapsam: SplitText (mask, autoSplit, revert), View Transitions (aynı belge içi `startViewTransition` ve belgeler arası `@view-transition`), dotLottie web.
3. SplitText tarifi:
   - Bölme `document.fonts.ready` sonrasında yapılır.
   - Yalnızca transform ve opacity anime edilir.
   - `gsap.matchMedia` ile reduced-motion açıkken metin animasyonsuz, doğrudan görünür olur.
4. View Transitions tarifi:
   - Önce destek kontrolü yapılır, CSS öncelikli yazılır.
   - Reduced-motion açıkken `::view-transition-group(*)` animasyonu kapatılır.

   dotLottie tarifi:
   - Canvas üzerinde çalışır, IntersectionObserver ile tembel yüklenir.
   - Görünür değilken duraklatılır.
   - Reduced-motion açıkken statik tek kare gösterilir, otomatik oynatma kapanır.
5. Playwright testleri yazılır. Her tarif için normal modda son durum doğru olmalı, reduced-motion modunda animasyon olmamalı, konsolda hata çıkmamalı.
6. `chrome-devtools` ile 4× CPU kısıtlamasında iz alınır: kare ≤16,7 ms olmalı, layout/paint uyarısı çıkmamalı. Bölüm 6 tur raporu yazılır.

**(c) Kapılar**
- Test: playwright.
- Performans: 60 fps (`chrome-devtools` izi).
- Erişilebilirlik: reduced-motion üç tarifte de geçmeli. SplitText'in aria seçeneğiyle ekran okuyucu başlığı bölünmeden okumalı (axe ile).
- Lisans: GSAP standart lisans MIT değil, koşulları rapora yazılır. dotLottie lisansı okunur.

## 14. ZZZ için (XXMI) birden çok modu tuşla değiştirilebilen tek bir modda birleştir: ini birleştirme ve geçiş tuşları ekle. Yeşil doku hatasını da gider.
### X
**(a) Araçlar**
- `mod-atolyesi` (skill): ZZZ/XXMI için birleştirme, tuş ve onarım akışının ana skill'i.
- `oyn-mod-guvenlik-kontrol` (ajan): mod klasörlerinde exe, dll ve şüpheli betik arar.
- `oyn-mod-birlestirici` (ajan): hash, slot ve resource yeniden adlandırmasıyla tek bir ini kurar.
- `oyn-mod-onarim` (ajan): yeşil doku hatasını ini bölümleri, hash'ler ve loglar üzerinden teşhis eder.
- `oyn-mod-paketleme` (ajan): birleşik modu klasör düzeni ve tuş readme'siyle paketler.
- Ek araç: yok. Ayrı bir merge betiği aramam; `mod-atolyesi` akışı ve elle yazılan `$swapvar` yeterli.

**(b) Sıra**
1. Mods klasörü zip olarak yedeklenir. `oyn-mod-guvenlik-kontrol` tüm kaynak modları tarar.
2. `mod-atolyesi` yüklenir ve oyun ZZZ (XXMI/ZZMI) seçilir. Modların aynı karakteri ve aynı hash'leri hedeflediği doğrulanır.
3. `oyn-mod-birlestirici` tek bir `merged.ini` kurar:
   - `[Constants] global persist $swapvar` tanımlanır.
   - `[KeySwap]` bölümünde `type = cycle` ile tuş bağlanır.
   - Her modun override blokları `if $swapvar == N` koşulu altına girer.
   - Resource adlarına önek verilerek çakışma önlenir.
   - Eski ini'ler `DISABLED_` önekiyle devre dışı bırakılır.
4. Yeni tuşun XXMI tuşları (ör. F10 yeniden yükleme) ve diğer modlarla çakışmadığı kontrol edilir.
5. `oyn-mod-onarim` yeşil dokunun hangi mod ve durumda çıktığını bulur. XXMI logu ve ini hash'leri güncel hash'lerle karşılaştırılır; doku slotu ve DDS formatı (BC7 sRGB / BC5) incelenir. Kök neden kanıtlanmadan düzeltme yapılmaz; sonra en küçük düzeltme uygulanır.
6. Oyunda test yapılır: F10 ile yeniden yükleme, tuşla her durumu gezme, yeşil dokunun yokluğu. Ardından `oyn-mod-paketleme` paketi ve readme'yi hazırlar.

**(c) Kapılar**
- Güvenlik: `oyn-mod-guvenlik-kontrol` (exe/dll olmamalı).
- Geri alma: zip yedeği.
- Ini tutarlılığı: bölüm başlıkları ve resource adları benzersiz olmalı (Grep ile).
- Oyun içi test: oyunu ben çalıştıramam, bu adımı Ömer yapar.
- KVKK: yok.
### Y
**(a) Araçlar**
1. `mod-atolyesi` (skill): ZZZ/XXMI için birleştirme, ini, tuş ve onarım akışının ana kaynağı.
2. `oyn-mod-guvenlik-kontrol` (alt ajan): İndirilen modlarda exe, dll veya şüpheli betik olup olmadığını önce tarar.
3. `oyn-mod-birlestirici` (alt ajan): Hash, slot ve buffer eşleşmelerini yeniden düzenler ve birleşik ini'yi yazar.
4. `superpowers:systematic-debugging` (skill): Yeşil doku sorununda kök neden kanıtlanmadan düzeltme yapılmaz.
5. `oyn-mod-onarim` (alt ajan): Yeşil dokuyu ini bölümleri, hash'ler ve `d3dx.log` üzerinden teşhis eder.
6. `oyn-mod-paketleme` (alt ajan): Son klasör düzenini ve tuşları anlatan readme'yi hazırlar.

**(b) Sıra**
1. Bütün mod klasörlerinin yedeği alınır. `oyn-mod-guvenlik-kontrol` ile taranır.
2. `mod-atolyesi` ile her modun karakter hash'leri ve `TextureOverride`/`ShaderOverride` bölümleri listelenir. Aynı karakteri hedeflediklerinin doğrulanması gerekir.
3. `oyn-mod-birlestirici` birleşik ini'yi yazar. Yapı şöyle: `[Constants] global persist $swapvar`, `[KeySwap]` içinde `type = cycle` ve tuş tanımı; her modun bölümleri `if $swapvar == N … endif` bloğuna sarılır. Kaynak ini'lere `DISABLED` öneki verilir; böylece hash çakışması olmaz.
4. Yeşil doku: `systematic-debugging` ve `oyn-mod-onarim` birlikte çalışır. Önce sorunun hangi modda ve hangi slotta oluştuğu yeniden üretilir. Olası nedenler: normal veya material map'in diffuse slotuna bağlanması, yanlış DDS biçimi ya da güncellemeyle değişen hash. Düzeltme kanıtlanan tek nedene yapılır.
5. Ömer oyunda F10 ile yeniden yükler. Her tuş durumu ekran görüntüsüyle doğrulanır. Oyunu ben açmam; test Ömer'in elinde.
6. `oyn-mod-paketleme` ile klasör düzeni ve tuş listesini içeren readme hazırlanır.

**(c) Kapılar**
- Güvenlik: Tarama temiz değilse birleştirme yapılmaz.
- Yedek ve geri dönüş: Orijinal klasörler değişmeden saklanır.
- `d3dx.log` içinde yeni hata olmamalı.
- Her varyant ekran görüntüsüyle kanıtlanmalı ve yeşil doku hiçbir durumda görünmemeli.
- Üç denemede kök neden bulunamazsa iş durdurulup DUR raporu yazılır.

## 15. Mobil bankacılık uygulamasının onboarding ekranları için wireframe ve görsel tasarım yönü çıkar
### X
**(a) Araçlar**
1. `frontend-craft` (plugin): Arayüz işinde zorunlu ilk adım. Marka kimliği kararı, en çok 4 turluk ekran görüntüsü döngüsü ve Bölüm 6 raporu buradan gelir.
2. `interaction-design:onboarding-design` (skill): İlk oturum akışı, adım sayısı ve ilerleme göstergesi.
3. `prototyping-testing:wireframe-spec` (skill): Görsel tasarımdan önce iskelet: içerik öncelikleri ve bileşen yerleşimi.
4. `fe-tasarim-yonu` (alt ajan): 2 görsel yön önerisi ve seçilen yön için DESIGN.md brief'i. Bankacılıkta güven ve sakinlik öne çıkar.
5. `pixeljury` (CLI): 390 px genişlikte kontrast, taşma ve dokunma hedefi denetimi.
6. `sec-kvkk-gdpr-kontrol` (alt ajan): Kimlik ve biyometrik veri, açık rıza ve aydınlatma metni ekranlarının denetimi.

**(b) Sıra**
1. `frontend-craft` ile işe başlanır ve DESIGN.md önce yazılır; kod sonra gelir (öğrenim 102).
2. `onboarding-design` ile akış çıkarılır: değer önerisi (≤3 kart), telefon ve OTP, TCKN ve doğum tarihi, kimliğin NFC ile okunması, selfie ve canlılık kontrolü, aydınlatma metni ve ayrı açık rıza, şifre veya biyometri, bitti ekranı. Uzaktan kimlik tespitinde BDDK adımları referans alınır.
3. `wireframe-spec` ile 390 px'lik düşük detaylı HTML wireframe'ler hazırlanır. Her ekranın boş, hata ve bekleme durumları da çizilir.
4. `fe-tasarim-yonu` 2 yön önerir. Biri seçilir ve renk, tipografi ile güven işaretlerini içeren token'lar DESIGN.md'ye yazılır.
5. Görsel yön wireframe'e uygulanır. `pixeljury` ve `frontend-craft` ekran görüntüsü döngüsü en çok 4 tur sürer; farklar sayıyla raporlanır.
6. `sec-kvkk-gdpr-kontrol` rıza ve aydınlatma ekranlarını denetler. Bulgular uygulanır ve Bölüm 6 raporu yazılır.

**(c) Kapılar**
- KVKK: Açık rıza aydınlatma metninden ayrı olmalı ve kutucuklar varsayılan olarak işaretsiz olmalı. Biyometrik veri özel nitelikli veri olarak ayrıca belirtilmeli.
- Erişilebilirlik: WCAG 2.2 AA kontrastı ve en az 44×44 dokunma hedefi (`pixeljury`). Dinamik yazı boyutunda taşma olmamalı; ekran okuyucu etiketleri bulunmalı.
- Güvenlik ve UX: OTP otomatik doldurulabilmeli. Kimlik ekranlarında ekran görüntüsü engeli tasarım notu olarak yer almalı. Gerçek bir bankanın logosu veya adı kullanılmaz.

---
Araçların gerçekten kurulu olup olmadığını dosya sisteminde kontrol etmedim, çünkü katalog sorgusu yapma dendi. 12 numaradaki betikler katalogda var, ama tarif onları "kurulu değil" diye listeliyor; uygulamada ilk adım bunu netleştirmek olmalı. 14 numaradaki yeşil doku sorunu için kesin neden ancak oyunda yeniden üretildiğinde belli olur.
### Y
**(a) Araçlar**
- `frontend-craft` (plugin): UI işinde zorunlu ilk yükleme; kurala göre önce DESIGN.md yazılır (öğrenim 102).
- `interaction-design:onboarding-design` (skill): ilk oturum akışını kurar.
- `prototyping-testing:wireframe-spec` (skill): görsel tasarımdan önce ekran yapısını çıkarır.
- `tasarim-katalog` (skill): görsel yön, referans ve font seçimi.
- `stitch` (MCP): seçilen yönle mobil ekran konseptleri üretir.
- `sec-kvkk-gdpr-kontrol` (ajan): kimlik ve biyometri veri akışını KVKK yükümlülükleriyle eşler.

**(b) Sıra**
1. `frontend-craft` yüklenir. Brief'te belli olmayan noktalar varsayım olarak yazılır: marka, platform (iOS/Android), hedef kitle.
2. `onboarding-design` ile akış çıkarılır: karşılama → telefon/OTP → TCKN ve kimlik (NFC ya da kamera) → selfie ve canlılık → görüntülü görüşme → şifre ve biyometri → izinler → bitiş.
3. `wireframe-spec` ile ekran başına düşük çözünürlüklü yapı yazılır: adım göstergesi, bileşenler, boş/yükleme/hata durumları, geri dönüş ve "sonra devam et" yolu.
4. `tasarim-katalog` ile 2–3 yön önerilir (güven ve sakinlik ekseninde) ve biri seçilir. DESIGN.md'ye renk, tipografi ölçeği, boşluk, köşe ve hareket token'ları yazılır.
5. `stitch` ile en çok 6 ekran konsepti üretilir. Ekran görüntüsü döngüsü en çok 4 tur sürer; farklar sayıyla yazılır.
6. `sec-kvkk-gdpr-kontrol` veri akışını haritalar. Aydınlatma metni ve ayrı açık rıza ekranları wireframe'e işlenir. Bölüm 6 tur raporu yazılır.

**(c) Kapılar**
- KVKK: biyometri özel nitelikli veri; açık rıza ayrı alınmalı ve önceden işaretli olmamalı (`sec-kvkk-gdpr-kontrol`).
- BDDK uzaktan kimlik tespiti yönetmeliği: görüntülü görüşme adımı gerekiyor. Bunu denetleyecek araç yok; hukuk onayı elle alınır.
- Erişilebilirlik: kontrast ≥4.5:1, dokunma hedefi ≥44pt, dinamik yazı boyutu, ekran okuyucu sırası (`frontend-craft` kontrol listesi; HTML prototip yapılırsa pixeljury).
- Maliyet tavanı: `stitch` en çok 6 ekran.

Atladıklarım: kataloğu yeniden sorgulamadım ve adayların kurulu olup olmadığını doğrulamadım. Örneğin `stitch` ve `blender-dogrulama` aday listesinde kurulu görünüyor ama bakmadım.

Riskler:
- 11. işte plugin ajanlarının description'ları değiştirilemiyor, bu yüzden jeton kazancı yalnızca bizim ajanlarla sınırlı kalır.
- 14. işte yeşil dokunun kök nedenini görmeden yalnızca tahmin yürütebiliyorum; oyun içi test Ömer'de.
- 13. işte GSAP lisansı MIT değil.
