## 1. Godot 4 ile çevrim içi çok oyunculu kart oyunu yap: yetkili sunucu, WebSocket durum senkronu, eşleştirme kuyruğu, hile önleme ve itch.io'ya dağıtım.
### X
**Varsayım:** Godot 4.3+ ve GDScript kullanılıyor; oyun 2–4 kişilik, sıra tabanlı. İstemci itch.io'da HTML5 olarak yayınlanıyor, sunucu ayrı bir VPS'te headless Godot olarak çalışıyor. Godot her zaman `--headless`, tarayıcı testleri Playwright headless (ekran kuralı).
**Açılacak skill'ler:** departman-guvenlik (hile, tehdit) ve departman-surec-git-yayin (CI, yayın). Oyun departmanı skill'i yoksa raporda bir satırla belirtilir.

**F0 Kapsam (≤15k)**
- Adım: oyn-oyun-dokuman ile tek sayfalık oyun tasarım belgesi; pln-kabul-olcutleri ile given/when/then ölçütleri.
- İnceleyen: pln-kapsam-kesici. MVP tek mod ve eşleştirmeden oluşur; rövanş ve sohbet yok.
- **Tartışma:** Sunucu headless Godot mu olsun, Node ws mi? Önerim headless Godot: kural kodu istemciyle aynı, tek dil ve tek kaynak.

**F1 Kural motoru (≤60k)**
- Adım: Sahneden bağımsız, saf GDScript `RuleEngine` (durum + hamle → yeni durum ya da hata). Yazan: oyn-oyun-motoru-script. Sahne çalıştırma ve hata okuma godot MCP ile.
- Kapı: GUT ya da gdUnit4 testleri (önce ara-lisans-kontrol). Testler geçersiz hamle reddini ve deste değişmezini (kart sayısı korunur) kapsar.
- İnceleyen: inc-test-kalitesi-inceleme.

**F2 Ağ ve durum senkronu (≤80k)**
- Adım: WebSocketMultiplayerPeer. İstemci yalnız niyet gönderir (`play_card(id)`); sunucu bunu RuleEngine ile doğrular ve her oyuncuya kendisine göre süzülmüş durumu yollar (rakibin elinden yalnız kart sayısı görünür). Her mesajda sıra numarası olur; yeniden bağlanan istemciye tam durum gönderilir.
- Araçlar: oyn-ag-senkronu (yetkili sunucu modeli), dil-websocket (heartbeat, yeniden bağlanma, backpressure).
- Kapı: 1 sunucu + 2 headless istemciyle entegrasyon testi, kopma ve yeniden bağlanma senaryosu dahil.
- İnceleyen: Realtime Collaboration Engineer.

**F3 Eşleştirme kuyruğu (≤30k)**
- Adım: Sunucuda bellek içi FIFO, zaman aşımı ve oda nesnesi. Kuyruğa `shortcut: tek süreç, yatay ölçek gerekince Redis` yorumu konur (o gün be-yatay-olcekleme).
- Kapı: 100 eşzamanlı katılımda çift eşleşme olmadığını gösteren test.

**F4 Hile önleme (≤40k)**
- Adım: Deste sunucuda `Crypto` tohumuyla karıştırılır; deste sırası istemciye hiç gitmez. Her niyet doğrulanır. Bağlantı başına hız sınırı (be-hiz-sinirlayici) ve kısa ömürlü oturum jetonu. Tehdit modeli sec-tehdit-modelleme (STRIDE) ile.
- Kapı: Kötü niyetli istemci testleri: sırası değilken hamle, elde olmayan kart, mesaj seli. Üçü de reddedilmeli.
- İnceleyen: differential-review:adversarial-modeler.
- **Tartışma:** İstemci tarafı tahmin (prediction) sıra tabanlı oyunda gereksiz; önermiyorum.

**F5 Dağıtım (≤45k)**
- Adım: `godot --headless --export-release "Web"` ile tek iş parçacıklı şablon; böylece itch.io'da COOP/COEP sorunu çıkmaz. Akış ship-web-games skill'iyle; itch.io'ya yükleme butler ile (kurulu değilse kurulumdan önce onay istenir).
- Sunucu tarafı: Linux headless export, ops-systemd-birim, ops-nginx-ters-vekil ile wss/TLS. https sayfası düz ws'e bağlanamaz, TLS zorunlu.
- CI (git-ci-boru-hatti): test → export → butler push. Sürüm notları build-game-changelog ile.
- Kapılar:
  - sec-sir-tarayici: BUTLER_API_KEY yalnız GitHub secret'ta.
  - test-playable-web-games + webapp-testing ile itch sayfasında duman testi.
  - sec-kvkk-gdpr-kontrol: kullanıcı adı ve IP en az düzeyde tutulur.
- İnceleyen: inc-uretim-hazirligi.
- **UI:** Lobi ve masa ekranı için önce /frontend-craft yüklenir; Godot'a uymayan maddeler raporda belirtilir.

**Toplam:** ≈270k jeton.
### Y
Varsayımlar: İstemci Godot 4.3+ ile tek iş parçacıklı Web dışa aktarımı olarak itch.io'da yayınlanır. Sunucu ayrı bir VPS'te `godot --headless` ile çalışır. Departman: Skill departman-surec-git-yayin (faz 4). frontend-craft atlandı, çünkü arayüz Godot Control ile yapılıyor, web DOM değil.
**Faz 0 · araştırma (15k)**
- Ağ modeli · Agent oyn-ag-senkronu: Sunucu yetkili olur ve tur tabanlı çalışır. İstemci yalnız niyet gönderir (`play_card(id)`). Sunucu bunu doğrular ve sıra numaralı durum farkını yayar.
- Taşıma katmanı · Agent dil-websocket: WebSocketMultiplayerPeer kullanılır, 10 sn'de bir kalp atışı gider. Yeniden bağlanan istemciye tam anlık görüntü gönderilir.
- Tartışma noktası, sunucu dili: Godot headless mi, Node mi? Önerim Godot headless, çünkü kural kodu (GDScript) istemciyle tek kaynakta kalır. Kapı: 2 saatlik deneme, 200 eşzamanlı bağlantıda RAM ≤500 MB. Tutmazsa `node`. Konsey gerekmiyor, deneme veriyi üretiyor.
**Faz 1 · tasarım (10k)**
- Mesaj şeması sürümlü olur. Eşleştirme kuyruğu ilk 30 sn FIFO çalışır, sonra ELO bandı genişler. Kuyruk sunucu belleğinde tutulur (shortcut: tek düğüm; ikinci sunucu gerekince dış kuyruğa geçilir).
- Hile önleme · Agent sec-tehdit-modelleme (STRIDE):
  - Gizli bilgi sunucuda kalır. İstemci yalnız kendi elini ve rakibin kart sayısını görür.
  - Kartlar sunucuda `Crypto.generate_random_bytes` tohumuyla karıştırılır.
  - Her eylemde sıra, sahiplik ve kural geçerliliği denetlenir. Oturum token'ı kullanılır, ileti sınırı ≤10/sn.
- İnceleme: Agent oyn-ag-senkronu tasarımı okur.
**Faz 2 · uygulama (40k)**
- Proje ve sahneler Godot MCP ile kurulur (ToolSearch "godot"). Kart, el ve masa mantığını Agent oyn-oyun-motoru-script yazar.
- Sıra: önce testli, saf bir kural motoru, sonra sunucu, istemci ve kuyruk.
- İnceleme: faz sonunda Agent ecc:code-reviewer.
**Faz 3 · test + güvenlik (12k)**
- `godot --headless -s tests/run.gd` ile assert tabanlı testler: kural motoru, kaydet→yükle turunda durum aynı kalır, yeniden bağlanma.
- Hile testi: Değiştirilmiş bir istemci 50 geçersiz eylem gönderir. Hepsi (%100) reddedilmeli ve sunucu çökmemeli. Paket dökümünde rakibin el verisi 0 kez geçmeli.
- Yük testi: `node` betiğiyle 100 sanal oyuncu (50 maç). Tur yanıtında p95 ≤100 ms.
- Web yapısı 60 fps tutmalı (kare ≤16.7 ms) ve dışa aktarım uyarısız derlenmeli. Tarayıcı testini Agent qa-e2e-playwright headless yapar, varsayılan tarayıcı açılmaz.
- Güvenlik: semgrep 0 yüksek, gitleaks 0 bulgu. İnceleme: Agent ecc:security-reviewer ve Agent sec-cikis-oncesi-guvenlik.
**Faz 4 · yayın + kapanış (8k)**
- Sunucu sürekli çalışır hale gelir (Agent ops-systemd-birim). TLS sonlandırma `wss://` ile Agent ops-nginx-ters-vekil'de yapılır, Upgrade başlığı iletilir. itch.io https'te çalıştığı için düz `ws://` engellenir.
- İstemcinin web yapısını ve itch.io sayfasını Skill ship-web-games hazırlar; sürüm notunu Skill build-game-changelog yazar. Yükleme dış yayın olduğu için Ömer'in onayıyla yapılır.
- Kapanış: Skill departman-surec-git-yayin ile commit ve CI, ardından commit·test·CI·sapma raporu.

## 2. Rust Actix Web mikroservisine gözlemlenebilirlik ekle: OpenTelemetry izleme, Prometheus metrikleri, Grafana panosu ve k6 yük testiyle CI'da SLO kapısı.
### X
**Varsayım:** Actix Web 4 ve tokio; CI GitHub Actions; docker compose kullanılabilir. Servis şu an `tracing` kullanmıyorsa ona geçirilir.
**Açılacak skill'ler:** Backend departman skill'i (yoksa raporda bir satır); CI fazında departman-surec-git-yayin.

**F0 SLO tanımı (≤15k)**
- Adım: pln-islevsel-olmayan-gereksinim ve SRE ajanıyla SLI'lar: p95 gecikme, 5xx oranı, erişilebilirlik.
- **Tartışma:** Eşik nereden gelecek? Önce mevcut sürümde bir k6 taban ölçümü; SLO = taban + pay. Uydurma sayı yok.

**F1 İzleme / tracing (≤50k)**
- Adım: `tracing`, `tracing-actix-web` (TracingLogger), `opentelemetry` + `opentelemetry-otlp` + `tracing-opentelemetry`. Hepsi aynı sürüm ailesine pinlenir; güncel uyum matrisi ara-kutuphane-dokuman ile alınır.
- Ayrıntılar: W3C traceparent yayılımı, giden HTTP çağrılarına bağlam aktarımı, `ParentBased(TraceIdRatio)` örnekleme. Span adı route şablonu olur (ops-dagitik-izleme, observability-and-instrumentation).
- Kapılar:
  - `cargo clippy -D warnings`.
  - ecc:rust-testing ile in-memory exporter testi: istek başına tek kök span, `http.route` dolu.
  - sec-loglama-gizlilik: span özniteliklerinde PII ya da jeton yok.
- İnceleyen: dil-actix-web (bloklayan çağrılar, kapanışta exporter flush).

**F2 Prometheus metrikleri (≤35k)**
- Adım: actix-web-prom ya da metrics-exporter-prometheus; ikisinden biri ara-kutuphane-secimi ile (lisans, bakım) seçilir. RED histogramı; etiketler method, route şablonu ve status sınıfı. Kardinalite ops-prometheus ile kontrol edilir. `/metrics` ayrı, iç bir portta çalışır.
- Kapı: Entegrasyon testi `/metrics`'i kazır ve ham path etiketi olmadığını doğrular.
- İnceleyen: ecc:security-reviewer (`/metrics` dışarı açık mı).

**F3 Gözlem yığını ve Grafana panosu (≤40k)**
- Adım: compose içinde otel-collector, Tempo, Prometheus ve Grafana. Pano JSON'u ve veri kaynakları repoda provisioning ile tutulur.
- Pano (ops-grafana-pano): RED satırı, exemplar'dan trace'e bağlantı.
- Kurallar: kayıt kuralları ve çok pencereli burn-rate uyarıları.
- Kapı: CI'da `promtool check rules` ve `promtool test rules`.
- İnceleyen: octo:personas:performance-engineer.

**F4 k6 ve CI'da SLO kapısı (≤45k)**
- Adım: qa-yuk-testi ile senaryo yazılır; k6 thresholds (`p(95)<X`, `http_req_failed rate<Y`). Eşik aşılırsa k6 sıfırdan farklı kodla çıkar ve CI işi kırmızı olur.
- CI (git-ci-boru-hatti): release build → servis + compose ayağa kalkar → k6 sabit VU ile en çok 2 dakika → sonuçlar artefakt olarak saklanır.
- Kapı (önce kırmızı): Kasıtlı yavaşlatılmış bir dalda kapının kırmızı yandığı görülür.
- İzleme: CI `gh run watch` ile izlenir; log okuma sonnet alt ajanında yapılır.
- **Tartışma:** Paylaşımlı runner gürültülü. Önerim PR'da gevşek mutlak eşik, gece tam koşu. Flaky çıkarsa qa-flaky-avci.

**F5 Kapanış (≤10k)**
- Adım: dok-runbook ile akış: uyarı → pano → trace.
- İnceleyen: ecc:code-reviewer (diff).

**Toplam:** ≈195k jeton.
### Y
Varsayımlar: CI GitHub Actions, yerelde docker compose. Arayüz yok, bu yüzden frontend-craft gerekmiyor. Departman: Skill departman-surec-git-yayin (faz 4).
**Faz 0 · SLO tanımı (8k)**
- Agent pln-islevsel-olmayan-gereksinim ve Agent SRE (Site Reliability Engineer) SLO'yu ölçülebilir hale getirir. Örnek: p95 ≤300 ms, hata oranı <%1, aylık %99.5 erişilebilirlik.
**Faz 1 · izleme (15k)**
- Agent ops-dagitik-izleme span adlarını, özniteliklerini ve örnekleme oranını (`traceparent` dahil) tasarlar.
- Agent dil-actix-web bunları uygular: `tracing-actix-web` ve `opentelemetry-otlp` kütüphaneleriyle OTLP üzerinden collector'a gönderim.
- Kapı: `opentelemetry_sdk` bellek içi dışa aktarıcısıyla bir test yazılır. Bir istek kök span'i ve doğru `http.route` değerini üretmeli.
**Faz 2 · metrikler (12k)**
- Agent ops-prometheus RED metriklerini (istek hızı, hata, süre) `actix-web-prom` kütüphanesiyle `/metrics` üzerinden açar.
- Tartışma noktası: OTel metrikleri collector üzerinden mi, doğrudan scrape mi? Önerim doğrudan scrape, daha az parça var.
- Kapılar:
  - Etiketlerde ham yol değil, rota kalıbı kullanılır. Yük testinden sonra seri sayısı ≤500 olmalı.
  - `/metrics` ayrı iç portta çalışır, dışarı açılmaz.
**Faz 3 · Grafana panosu (8k)**
- Agent ops-grafana-pano panoyu tasarlar: RED panelleri, p50/p95/p99, SLO yakma hızı, izden loga bağlantılar. Pano JSON dosyası olarak repoda tutulur.
- Kapı: compose'daki Grafana'da `/api/dashboards/uid/<uid>` 200 dönmeli ve tüm paneller veri göstermeli.
**Faz 4 · k6 + CI SLO kapısı (12k)**
- Agent qa-yuk-testi senaryoyu yazar: rampa 0→50 VU, 3 dk. Eşikler: `http_req_duration p(95)<300` ve `http_req_failed rate<0.01`.
- Agent git-ci-boru-hatti CI'yı kurar: compose ayağa kalkar, k6 koşar. Eşik aşılırsa k6 sıfır olmayan kodla çıkar ve iş kırmızı olur.
- Kapılar: `cargo test`, `cargo clippy -D warnings`, semgrep 0 yüksek, gitleaks 0.
- KVKK: Agent sec-loglama-gizlilik span'leri denetler. Özniteliklerde e-posta, token ya da gövde 0 kez geçmeli.
**İnceleme:** her faz sonunda Agent ecc:code-reviewer, faz 4'te Agent ecc:security-reviewer. Konsey gerekmiyor, tüm adımlar geri alınabilir.
**Kapanış (3k):** commit·test·CI·sapma raporu.

## 3. Laravel e-ticaret sitesini çok kiracılı SaaS'a dönüştür: kiracı başına veri yalıtımı, Postgres RLS, Paddle abonelik faturası, alt alan adı yönlendirme ve sıfır kesintili migration.
### X
**Varsayım:** Laravel 10 ya da 11; veritabanı zaten Postgres. MySQL ise F1'den önce bir db-veri-tasima fazı eklenir. Mevcut mağaza 1 numaralı kiracı olur.
**Açılacak skill'ler:**
- departman-veri-db: Postgres'e dokunmadan önce supabase-postgres-best-practices; geri alma adımı olmayan migration yok.
- departman-guvenlik.
- departman-surec-git-yayin.

**F0 Mimari karar (≤25k)**
- Adım: be-coklu-kiraci-veri ve Software Architect ile model: paylaşımlı şema + `tenant_id` + RLS. İstenen RLS bu modeli gerektiriyor; kiracı başına şema hem göçte pahalı hem de RLS'yi gereksiz kılar.
- Karar dok-adr-yazar ile ADR olarak yazılır.
- **Tartışma:** Hangi paket? stancl/tenancy, spatie/laravel-multitenancy ya da düz middleware. Önerim spatie'nin tek-veritabanı modu ya da düz middleware; lisans ara-lisans-kontrol ile.

**F1 Expand migration (≤60k)**
- Adım (db-migration-planlayici):
  1. `tenants` tablosu.
  2. Kiracı tablolarına nullable `tenant_id`.
  3. Kuyruk işiyle 1000'lik parçalar halinde backfill.
  4. `CHECK … NOT VALID`, sonra `VALIDATE`.
  5. `CREATE INDEX CONCURRENTLY` (migration'da `$withinTransaction=false`); kısa `lock_timeout`.
  6. `tenant_id` yazan uygulama kodu, zorunlu hale getirilmeden önce deploy edilir.
- Kapılar:
  - Önce db-yedekleme-geri-yukleme ile PITR ve geri yükleme provası.
  - Anonimleştirilmiş prod kopyasında prova ve süre ölçümü (KVKK; veri qa-test-verisi ile hazırlanır).
  - Her migration'ın `down()` metodu var.
- İnceleyen: Database Reliability Engineer.

**F2 Veri yalıtımı ve RLS (≤60k)**
- Uygulama katmanı: kiracı çözen middleware ve Eloquent global scope.
- Veritabanı katmanı: uygulama rolü tablo sahibi ya da superuser değil; `ENABLE` + `FORCE ROW LEVEL SECURITY`. Politika: `tenant_id = current_setting('app.tenant_id')::bigint`.
- Bağlam: Her istekte transaction içinde `set_config(…, true)` çağrılır. PgBouncer transaction pooling'de oturum düzeyi SET başka isteğe sızar; bu yüzden SET LOCAL.
- Kiracı bağlamı ayrıca kuyruk işlerine, zamanlanmış görevlere, cache anahtarlarına ve dosya yollarına taşınır.
- Araçlar: db-rls-politika, ecc:postgres-patterns.
- Kapı (önce kırmızı, Pest): A kiracısı B'nin verisini Eloquent ile, ham `DB::select` ile ve kuyruk işi içinde göremez. Bağlam yokken sorgu 0 satır döner.
- İnceleyen: differential-review:adversarial-modeler ve sec-yetkilendirme-matrisi (BOLA).

**F3 Alt alan adı yönlendirme (≤35k)**
- Adım: `Route::domain('{tenant}.…')`; ayrılmış adlar: www, api, admin, app.
- Altyapı: wildcard DNS ve DNS-01 ile wildcard TLS (ops-dns-tls-sorun), ops-nginx-ters-vekil.
- Oturum çerezi: alt alana özel olur, `.example.com` olmaz; böylece kiracılar arası oturum sızması olmaz.
- Güvenlik: sec-alt-alan-ele-gecirme, sec-acik-yonlendirme (returnUrl).
- DNS Hostinger'daysa hostinger MCP kullanılır; her değişiklikten önce onay alınır.
- Kapı: Bilinmeyen alt alan 404 döner; ayrılmış adlar kiracı olarak kabul edilmez.

**F4 Paddle abonelik faturası (≤50k)**
- Adım: `laravel/cashier-paddle` (Paddle Billing); Billable model Tenant olur. Kurgu Payments & Billing Engineer ile.
- Webhook (otm-webhook-tasarimci): imza doğrulama ve event id tablosuyla idempotent işleyici. Abonelik durumu bir özellik kapısını besler (grace period dahil).
- Kapılar:
  - Yalnız sandbox; canlı çağrı en çok 0.
  - Webhook replay testi.
  - sec-sir-tarayici.
- Vergi: Paddle satıcı kaydı (MoR) olduğu için vergiyi Paddle yönetir.
- **UI:** Kayıt ve fatura sayfaları için önce /frontend-craft; kapanışta Section 6 raporu.

**F5 Contract ve yayın (≤35k)**
- Adım: Tüm kod yolları `tenant_id` yazdıktan sonra eski yollar kaldırılır. İlk yeni kiracı git-canary-izleme ile canary olarak açılır.
- CI kapıları (GitHub Actions, Postgres servis konteyneri):
  - ecc:laravel-verification: pint, larastan, Pest, kapsama.
  - ecc:laravel-security.
- KVKK: sec-kvkk-gdpr-kontrol. SaaS veri işleyen, mağaza veri sorumlusu; aradaki DPA dok-kullanim-kosullari ile hazırlanır.
- İnceleyen: ecc:code-reviewer ve inc-uretim-hazirligi.

**Toplam:** ≈265k jeton.

---
Kontrol etmediklerim: oyun ve backend departman skill'lerinin var olup olmadığı, butler/GUT/gdUnit4'ün kurulu olup olmadığı, crate ve paket sürümleri.
Risk: 3. işin planı veritabanının zaten Postgres olduğunu varsayıyor; MySQL çıkarsa iş belirgin şekilde büyür.
### Y
Varsayımlar: Mevcut mağaza 1 numaralı kiracı olur. Kiracı modeli paylaşımlı şema + `tenant_id` + RLS, çünkü RLS istenmiş. Bu yüzden konsey gerekmiyor. Departman: Skill departman-veri-db (faz 1–2), Skill departman-surec-git-yayin (faz 5). Kayıt ve fatura sayfaları arayüz olduğu için önce /frontend-craft yüklenir; kapanışta 6. bölüm raporu yazılır.
**Faz 0 · araştırma (15k)**
- Agent be-coklu-kiraci-veri kiracı bağlamının akışını haritalar: istek, kuyruk işi, artisan komutu, önbellek anahtarı, dosya yolu.
- Önce Skill supabase-postgres-best-practices, ardından Skill ecc:postgres-patterns yüklenir.
**Faz 1 · şema genişletme ve geri doldurma (15k)**
- Agent db-migration-planlayici genişlet/daralt sırasını kurar:
  - `tenant_id` boş bırakılabilir sütun olarak eklenir.
  - Indeksler `CREATE INDEX CONCURRENTLY` ile kurulur; bu migration'larda `$withinTransaction=false` olmalı.
  - Önce `CHECK ... NOT VALID`, sonra `VALIDATE`, sonra `SET NOT NULL`.
- Agent db-veri-tasima geri doldurmayı 5k'lık partilerle yapar. Kapı: tablo başına satır sayısı eşit olmalı ve `tenant_id IS NULL` olan satır 0 kalmalı.
- Benzersiz anahtarlar `(tenant_id, sku)` olur; bu adım daraltma aşamasına bırakılır. Her migration'ın bir `down()` geri alma adımı olur. Önce yerelde, sonra staging'de denenir; üretim onayla yapılır.
**Faz 2 · RLS (15k)**
- Agent db-rls-politika politikaları yazar: `USING` ve `WITH CHECK` ifadeleri `tenant_id = current_setting('app.tenant_id')::bigint` olur, ardından `ENABLE` ve `FORCE ROW LEVEL SECURITY`.
- Uygulamanın veritabanı rolü tablo sahibi olamaz, aksi halde RLS atlanır.
- Kiracı bağlamı her transaction'da `set_config('app.tenant_id', ?, true)` ile kurulur. Bu, pgbouncer'ın transaction modunda da güvenlidir.
- Tartışma noktası, sıra: Önce uygulama her yerde bağlam kuracak şekilde yayınlanır, sonra RLS açılır. Geri alma: `DISABLE ROW LEVEL SECURITY`.
- İkinci savunma katmanı olarak Eloquent global scope eklenir (Skill ecc:laravel-patterns).
**Faz 3 · alt alan adları + Paddle (20k)**
- Kiracı `Route::domain('{tenant}.site')` ve middleware ile çözülür. Bilinmeyen alt alan 404 döner. www, api ve admin alt alanları ayrılmıştır.
- `SESSION_DOMAIN` ayarlanmaz, böylece oturum çerezi kiracılar arasında paylaşılmaz.
- Güvenlik ajanları: Agent sec-alt-alan-ele-gecirme (wildcard DNS) ve Agent sec-acik-yonlendirme (returnUrl).
- Paddle Billing, `laravel/cashier-paddle` ile kurulur ve faturalanan model kiracı olur. Kurulum Agent Payments & Billing Engineer'dır, webhook alıcısı Agent otm-webhook-tasarimci'dir.
- Ödeme kapıları:
  - Webhook imzası `Paddle-Signature h1` ile doğrulanır. Aynı `event_id` ikinci kez işlenmez.
  - Yeniden deneme tavanı 3, üstel bekleme ile.
  - Kart verisi sunucuya hiç değmez (Paddle overlay, SAQ-A).
- Ücretli çağrı tavanı: yalnız sandbox, en çok 50 çağrı. Üretimde 0 çağrı.
**Faz 4 · test + güvenlik (15k)**
- Skill ecc:laravel-tdd ile yalıtım testleri: A kiracısı B'nin verisini Eloquent, ham SQL (uygulama rolüyle), kuyruk işi ve önbellek yoluyla okuyamamalı. Hepsi kırmızı görüldükten sonra yeşile döner.
- Mevcut e-ticaret testleri kiracı 1 ile %100 yeşil kalmalı. Webhook tekrar oynatma testi yapılır.
- Kayıt ve fatura sayfaları: LCP ≤2.5 s, CLS ≤0.1, INP ≤200 ms. Agent qa-erisilebilirlik-testi 0 ciddi ihlal bulmalı.
- Güvenlik: semgrep 0 yüksek, gitleaks 0. Skill ecc:laravel-security ve Agent sec-kvkk-gdpr-kontrol (kiracı başına silme ve saklama süresi) çalışır.
**Faz 5 · yayın (5k)**
- Skill ecc:laravel-verification çalışır. Wildcard TLS sertifikası (DNS-01) ve DNS değişikliği Ömer'in onayıyla yapılır.
- İnceleme: her faz sonunda Agent ecc:code-reviewer, faz 4'te Agent ecc:security-reviewer.
- Kapanış: Skill departman-surec-git-yayin ile commit·test·CI·sapma raporu.

Sapma: `plan_kur.py` iş 2'yi yanlışlıkla "RUTİN (web)" saydı ve aday listesi vermedi. İş 2'yi zor iş olarak planladım, araçları kurulu ajan listesinden seçtim. Bu, sınıflandırıcıda bir hata. Ayrıca araç çıktısının sıkıştırılan kısmını headroom ile geri aldım; yeni sorgu yapmadım.

Denetlemediklerim: butler CLI ve Godot test eklentilerinin kurulu olup olmadığına bakmadım, o yüzden ikisini de planda kullanmadım. İş 3'ün jeton bütçesi çıktıda kesik geldi, oradaki sayılar benim tahminim.

## 4. Electron masaüstü not uygulamasını Tauri'ye taşı: güvenli IPC, kod imzalama, otomatik güncelleme, yerel SQLite şifreleme ve erişilebilirlik denetimi.
### X
**F0 Keşif ve karar** · bütçe 15k
- Adım: Electron'daki IPC yüzeyi çıkarılır (ipcMain handler'ları, preload API'si, kullanılan Node modülleri) → taşıma listesi.
- Araç: `graphify query` → Agent `Desktop App Engineer` (envanter) → Agent `dok-adr-yazar` (ADR).
- Kapı: Envanterdeki handler sayısı koddaki `ipcMain.handle/on` sayısına eşit olmalı (Grep sayımı).
- Tartışma (Agent `Software Architect` ile `Desktop App Engineer`): taşıma "big-bang" mi olsun, yoksa ilk açılışta veri göçü yapan paralel bir Tauri sürümü mü? Önerim: paralel sürüm + köprü sürümü.

**F1 Güvenli IPC** · 25k
- Adım: Tauri v2 capabilities en az izinle kurulur; `fs`, `shell` ve joker izin olmaz. Her handler için tipli bir `#[tauri::command]` yazılır ve girdi Rust tarafında doğrulanır. Sıkı CSP konur, `withGlobalTauri` kapalı kalır.
- Araç: Skill `superpowers:test-driven-development`, Agent `sec-tehdit-modelleme` (STRIDE), `cargo test`.
- Kapı: Capability dosyalarında `*` geçmemeli. Her komutun geçersiz girdiyi reddettiğini gösteren testi olmalı. CSP'de `unsafe-eval` bulunmamalı.
- İnceleme: Agent `ecc:security-reviewer`.

**F2 Şifreli SQLite ve veri göçü** · 30k
- Adım: rusqlite `bundled-sqlcipher` kullanılır. Anahtar OS anahtarlığında (`keyring` crate) tutulur. İlk açılışta eski düz DB yedeklenir, şifreli DB'ye kopyalanır, doğrulanır ve ancak ondan sonra silinir.
- Araç: Agent `db-sqlite` (WAL, pragma), Agent `sec-sifreleme-denetci`.
- Kapı (test):
  - Dosya anahtarsız açılınca "file is not a database" hatası vermeli.
  - Göç öncesi ve sonrası satır sayısı ile içerik hash'i eşit olmalı.
  - Göç ikinci kez koşunca hiçbir şey yapmamalı.
  - Göç yarıda kesilince eski DB sağlam kalmalı.
- KVKK: Notlar kişisel veridir. Agent `sec-loglama-gizlilik` loglarda not içeriği olmadığını denetler.
- Tartışma: Anahtar anahtarlıkta mı tutulsun, kullanıcı parolasından mı türetilsin? Anahtarlık yolunda kurtarma derdi yok ama başka makineye taşıma kaybolur.

**F3 UI taşıma ve erişilebilirlik** · 30k
- Adım: Önce Skill `frontend-craft` yüklenir (CLAUDE.md zorunluluğu). `window.electron.*` çağrıları `@tauri-apps/api` `invoke` ile değiştirilir; renderer kodu olduğu gibi kalır.
- Araç: Agent `qa-erisilebilirlik-testi` (dev sunucusunda Playwright + axe, ayrıca klavye turu), Agent `qa-e2e-playwright` (not ekleme, düzenleme, arama akışları).
- Kapı:
  - axe'de ciddi ve kritik bulgu sayısı 0 olmalı.
  - Tüm akışlar yalnız klavyeyle tamamlanabilmeli.
  - NVDA ile manuel ekran okuyucu turu yapılmalı.
  - frontend-craft Bölüm 6 tur raporu çıkarılmalı.
- İnceleme: Agent `ecc:a11y-architect`.
- Tartışma: WebView2, WKWebView ve WebKitGTK arasındaki farklar. Linux'ta ayrıca smoke testi gerekir mi?

**F4 Kod imzalama ve otomatik güncelleme** · 30k
- Adım:
  - `tauri-plugin-updater` kurulur; minisign özel anahtarı yalnız CI secret'ında durur.
  - Windows'ta Authenticode, macOS'ta notarization yapılır.
  - CI matrisi win/mac/linux olur.
- Araç: Agent `git-ci-boru-hatti`, Agent `sec-sir-tarayici` (repoda anahtar kalmamalı).
- Kapı:
  - `signtool verify /pa` ve `spctl -a` geçmeli.
  - Kurcalanmış güncelleme paketi reddedilmeli (test).
  - Staging kanalında vN-1'den vN'e güncelleme uçtan uca çalışmalı.
- Tartışma (kritik): Mevcut Electron kullanıcıları nasıl taşınır? Son Electron sürümünün autoUpdater'ı Tauri kurucusunu indirir (köprü). Ayrıca güncelleme uç noktası GitHub Releases mı olsun, kendi sunucumuz mu?
- Tavan: Ömer onayı olmadan köprü sürümü en çok 1 kez yayınlanır; sertifika satın alma kararı Ömer'in.

**F5 Yayın** · 10k
- Araç: Agent `sec-bagimlilik-acik` (cargo ve npm), Agent `git-yayin-oncesi-kontrol`.
- Kapı: CI matrisi yeşil olmalı. Kapanış raporu: commit, test sayısı, CI, sapmalar.
### Y
Zor iş (masaüstü + güvenlik + veri + a11y). Planın dayanağı: `katalog_ara` A listesi ve oturumda kurulu ajanlar. Listede "kurulu değil" yazan araçları (agent-desktop, lighthouse, ZAP, jev-review) kullanmıyorum.

**F0 Keşif ve karar** (~15k)
- Adım: Electron'daki `ipcMain` kanallarını, `preload` API'lerini, `nodeIntegration` yerlerini ve native modülleri çıkar. `.claude/dalga.md` içine KARAR ve kabul ölçütlerini yaz.
- Araç: `graphify query` → `jev ilgili`, Explore alt ajanı (sonnet), `context7` (Tauri v2 capabilities, updater, sql belgeleri)
- Kapı: her IPC kanalının bir Tauri komut karşılığı olacak, eksik satır kalmayacak.
- İnceleyen: Desktop App Engineer
- Tartışma: Tauri v2 mi, v1 mi? Önerim v2, çünkü capability ve izin sistemi yerleşik geliyor.

**F1 İskelet + güvenli IPC** (~40k)
- Adım: `create-tauri-app` ile kur, mevcut web ön ucunu olduğu gibi taşı. Her kanal için bir `#[tauri::command]` yaz, girdiyi serde ile doğrula. `capabilities/*.json` dosyalarında yalnız gereken izinleri ver. Sıkı CSP koy, isolation pattern'i aç, `fs` kapsamını not dizinine daralt.
- Araç: Desktop App Engineer; `sec-tehdit-modelleme` (STRIDE, WebView→Rust güven sınırı)
- Kapı: `cargo test` ile komut başına geçerli ve geçersiz girdi testi. `ecc:security-reviewer` ile kapsam dışı dosya yolu (path traversal) ve izin taşması denetimi. `gitleaks` ile sır taraması.
- İnceleyen: `differential-review:adversarial-modeler`
- Tartışma: Ön uç Rust komutlarını çağırırken `invoke` ile JS arasındaki arayüz elle mi yazılsın, `tauri-specta` ile tip üretilerek mi? Önerim: elle yazmak, çünkü yeni bağımlılık eklemiyor.

**F2 Şifreli SQLite** (~35k)
- Adım: `rusqlite` + `bundled-sqlcipher` kullan. Anahtar `keyring` crate'i ile OS anahtar zincirinde dursun (Windows Credential Manager / macOS Keychain). Göç sırası: eski düz DB → `sqlcipher_export` → doğrulama → eski dosyayı güvenli silme. WAL ve pragmalar ayarlanacak.
- Araç: `departman-veri-db` skill'inin sırası, `db-sqlite`, `sec-sifreleme-denetci`
- Kapı: göç testi (satır sayısı ve içerik hash'i eşit olacak), yanlış anahtarla açma denemesi hata vermeli, `strings` ile şifreli dosyada düz metin kalmamalı. Göç başarısızsa eski DB'ye dokunulmaz (veri kaybı yok).
- İnceleyen: `sec-sifreleme-denetci`
- Tartışma: Anahtar zinciri yoksa (Linux'ta keyring servisi yoksa) parolaya dayalı anahtar türetme (KDF) mi, kurulumu reddetmek mi?

**F3 Kod imzalama + otomatik güncelleme** (~30k)
- Adım: `tauri signer generate` ile minisign anahtarı üret, `tauri-plugin-updater` ile `latest.json`'u GitHub Releases'tan sun. Windows'ta Authenticode (signtool / Azure Trusted Signing), macOS'ta notarization.
- Araç: Desktop App Engineer, `gh` (release ve secrets), `git-ci-boru-hatti` (tauri-action matrisi)
- Kapı: imzasız ya da kurcalanmış paket güncellemede reddedilmeli (negatif test). Sertifika parolası yalnız CI secret'ta durur, değeri hiçbir zaman basılmaz.
- İnceleyen: `git-yayin-oncesi-kontrol`
- Tartışma: Sertifika maliyeti (EV mi OV mi, Trusted Signing mi) Ömer'in kararı. Ücretli işlem için tavan: en çok 1 sertifika alımı, onaydan sonra.

**F4 Erişilebilirlik** (~30k)
- Adım: frontend-craft'ı yükle (UI'a dokunan iş). Klavye akışı, odak halkası, ARIA, kontrast ve yakınlaştırma ele alınacak.
- Araç: `qa-erisilebilirlik-testi`, `interfaces:better-accessibility`, `fixing-accessibility`; `playwright-cli` headless + `@axe-core/playwright` (Vite dev sunucusuna karşı), `chrome-devtools-mcp:a11y-debugging`
- Kapı: axe ile 0 kritik/ciddi bulgu, klavyeyle tüm akış tamamlanabilmeli, kontrast WCAG 2.2 AA. NVDA ile elle tur atmak Ömer'in işi; raporda bu ayrıca belirtilecek.
- İnceleyen: Section 508 Accessibility Specialist
- Kapanış: frontend-craft Section 6 tur raporu.

**F5 Eşdeğerlik + kapanış** (~20k)
- Adım: Electron ve Tauri yan yana çalıştırılır, aynı not senaryosu oynatılır. Paket boyutu ve açılış süresi ölçülür.
- Araç: `qa-ozellik-paritesi`, suite koşusu için `okuyucu` (sonnet)
- Kapı: eşdeğerlik listesi %100, CI yeşil.
- İnceleyen: `find-bugs` skill'i
- Kapanış raporu: commit, test sayısı, CI, sapmalar.

## 5. ESP32 sıcaklık sensörlerinden MQTT ile veri topla: TimescaleDB'ye yaz, anomali tespiti, Grafana uyarıları ve aşamalı OTA firmware güncellemesi.
### X
Zor iş (gömülü + veri + ML + ops). Dayanak aynı. "Kurulu değil" olan Tiger Data MCP ve claudex-loop kullanılmıyor.

**F0 Kapsam** (~15k)
- Adım: cihaz sayısını, örnekleme aralığını ve saklama süresini yazıya dök. KVKK triyajı: sensör ev ya da kişiyle ilişkiliyse konum kişisel veri sayılır.
- Araç: `departman-veri-db`, `use-case-triage`, `pln-islevsel-olmayan-gereksinim`
- Kapı: ölçülebilir hedefler, örneğin p95 alım gecikmesi < 5 sn ve OTA başarısı ≥ %99.
- İnceleyen: IoT Fleet Engineer

**F1 Firmware: ölçüm + MQTT** (~40k)
- Adım: ESP-IDF ile `esp-mqtt` üzerinden TLS (cihaz başına sertifika) ve QoS 1 kullan. Konu şeması `t/{site}/{cihaz}/temp`. Bağlantı kopunca RTC belleğinde tampon tut. Sensör kalibrasyon ofseti NVS'te saklanır; kalibrasyon atlanamaz.
- Araç: Embedded Firmware Engineer, `ops-mqtt` (QoS, retained, LWT), `context7` (ESP-IDF)
- Kapı: PlatformIO `native` birim testleri ve 2 gerçek kart üzerinde 24 saat bench, buz/oda/sıcak su ile 3 noktalı kalibrasyon kontrolü.
- İnceleyen: `mukul975-firmware-security-paket`
- Tartışma: Broker Mosquitto mu EMQX mi? Önerim Mosquitto: tek düğüm, ACL dosyası yeterli.

**F2 Alım + TimescaleDB** (~35k)
- Adım: Telegraf `mqtt_consumer` → PostgreSQL çıkışı (yeni kod yok). Hypertable'da `(cihaz_id, ts)` için tekil indeks, zaman `timestamptz` UTC. Continuous aggregate (1 dk / 1 sa), sıkıştırma ve saklama politikası.
- Araç: `db-sema-tasarim`, `db-zaman-damgasi`, Database Optimizer, `qa-entegrasyon-testi` (testcontainers ile timescale imajı)
- Kapı: aynı mesaj iki kez gelince tek satır (idempotency), saat farkı testi, `db-veri-kalitesi` ile aralık dışı değerler.
- İnceleyen: `db-yedekleme-geri-yukleme` (PITR ve geri yükleme provası)

**F3 Anomali tespiti** (~30k)
- Adım: önce SQL ile kayan medyan + MAD z-skoru (continuous aggregate üzerinde), artı "veri gelmedi" kuralı. ML'e ancak SQL kuralı kabul ölçütünü kaçırırsa geçilir.
- Araç: `ml-zaman-serisi`, `ml-model-metrik` (eşik ve yanlış alarm maliyeti)
- Kapı: etiketli geçmiş veride geri test (backtest), precision/recall hedefi F0'da belirlenir.
- İnceleyen: `ml-veri-sizintisi`
- Tartışma: eşik cihaz başına mı, site başına mı? Önerim cihaz başına, çünkü sensörler farklı ortamlarda.

**F4 Grafana uyarıları** (~20k)
- Adım: SQL veri kaynağı, pano (site → cihaz değişkenleri), unified alerting, susturma ve gruplama.
- Araç: `ops-grafana-pano`, `otm-bildirim-yonlendirme`
- Kapı: sentetik anomali enjekte edilince uyarı ≤ 2 dk içinde gelmeli. Kontrol HTTP API ve curl ile yapılır; tarayıcı açılmaz.
- İnceleyen: SRE (Site Reliability Engineer)

**F5 Aşamalı OTA** (~40k)
- Adım: `esp_https_ota`, Secure Boot v2 + imzalı imaj, `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`. Sağlık kontrolü geçmezse otomatik geri dönüş. Halkalar: %1 → %10 → %50 → %100, durdurma eşiği.
- Araç: IoT Fleet Engineer, `git-canary-izleme`, `sec-tehdit-modelleme`
- Kapı: bench'te bozuk imaj ve yarıda kesilen indirme ile geri dönüş testi, imzasız imaj reddedilmeli.
- İnceleyen: `differential-review:adversarial-modeler`
- Tartışma: Flash şifreleme geri dönüşü olmayan bir eFuse işlemi. Önce 1 kartta denenir, Ömer onayı olmadan filoya açılmaz.

**F6 Kapanış** (~10k)
- Adım: suite özeti `okuyucu` alt ajanından gelir, `dok-runbook` ile OTA geri alma ve broker arızası işlenir.
- Kapı: CI yeşil. Ücretli bulut kullanılırsa tavan en çok 1 yönetilen Timescale örneği.

---
Atladıklarım: listede "kurulu değil" yazan araçları ve ek katalog sorgularını kullanmadım. Hiçbir dosyaya yazmadım.

Riskler: eFuse işlemleri (F5) ve kod imzalama sertifikası (F3) geri alınamaz ya da ücretli; ikisi de Ömer'in onayını bekliyor.
### Y
**F0 Mimari** · 15k
- Adım: Broker, ingest ve anomali yöntemi seçilir; ADR yazılır.
- Araç: Skill `superpowers:brainstorming`, Agent `IoT Fleet Engineer`, Agent `dok-adr-yazar`.
- Tartışma (Agent `Software Architect` ile `IoT Fleet Engineer`):
  - Mosquitto mu, EMQX mi?
  - Ingest Telegraf ile mi, küçük bir Python tüketiciyle mi?
  - Anomali için SQL'de robust z-score (MAD) ve değişim hızı mı, yoksa ML mi?
  - Önerim: Mosquitto, Python tüketici ve MAD. ML'e veri birikince geçilir.

**F1 Firmware** · 30k
- Adım (ESP-IDF):
  - MQTT/TLS cihaz başına istemci sertifikasıyla kurulur; QoS1, LWT ve `site/{id}/temp` konusu kullanılır.
  - Saat SNTP ile alınır, veri UTC zaman damgasıyla gönderilir.
  - Bağlantı yokken ölçümler NVS halka tamponunda tutulur.
  - Sensör kalibrasyon ofseti tanımlanır.
- Araç: Agent `Embedded Firmware Engineer`; PlatformIO `native` ortamında host testleri.
- Kapı: Host testleri yeşil olmalı. 1 kartla 24 saatlik dayanıklılık testinde kayıp %0,1'in altında kalmalı. Wi-Fi 10 dakika kesilince tampon boşaltılmalı ve hiçbir ölçüm kaybolmamalı.
- İnceleme: Agent `ops-mqtt` (konu, QoS, retained kullanımı).

**F2 Broker ve ingest** · 25k
- Adım:
  - Cihaz başına ACL kurulur; her cihaz yalnız kendi konusuna yazabilir.
  - Tüketici idempotent yazar: `UNIQUE(device_id, ts)` + `ON CONFLICT DO NOTHING`.
  - Bozuk mesajlar dead-letter tablosuna gider.
- Araç: Agent `be-mesaj-guvenilirligi`, Agent `qa-entegrasyon-testi` (docker compose ile Mosquitto + Timescale), paho ile yazılmış simülatör betiği.
- Kapı:
  - 100 sanal cihaz 10 saniyede bir mesajla 1 saat koşmalı.
  - Tekrar gönderimde satır sayısı değişmemeli.
  - Başka cihazın konusuna yazma ACL'de reddedilmeli.
- İnceleme: Agent `ecc:security-reviewer`.

**F3 TimescaleDB** · 25k
- Adım: Hypertable, 1 dakikalık ve 1 saatlik sürekli agregalar, sıkıştırma ve saklama politikaları kurulur; kolonlar `timestamptz` olur.
- Araç: Agent `Database Optimizer`, Agent `db-zaman-damgasi`, Agent `db-yedekleme-geri-yukleme`.
- Kapı: 30 günlük sentetik veride pano sorgularının p95 süresi 200 ms'nin altında olmalı (EXPLAIN ANALYZE). Bir geri yükleme tatbikatı başarılı olmalı.

**F4 Anomali ve Grafana uyarıları** · 30k
- Adım:
  - Üç kural kurulur: MAD z-score, değişim hızı ve "sensör sustu" (veri yok).
  - Grafana uyarıları ve panolar kod olarak (provisioning YAML) tanımlanır.
  - Bildirim rotaları ve sessiz saatler ayarlanır.
- Araç: Agent `ml-zaman-serisi`, Agent `ops-grafana-pano`, Agent `otm-bildirim-yonlendirme`.
- Kapı: Etiketli sentetik anomali kümesinde recall 0,9 veya üstü olmalı. Tekrar oynatmada cihaz başına haftada en çok 1 yanlış uyarı çıkmalı. Test contact point'ine uyarının ulaştığı görülmeli.
- Tartışma: Eşik cihaz başına mı olsun, global mi? Mevsimsellik (gece/gündüz) şimdi mi ele alınsın, sonra mı?

**F5 Aşamalı OTA** · 30k
- Adım:
  - Çift OTA bölümü kullanılır; imzalı imaj HTTPS üzerinden imzalı bir manifestle indirilir.
  - Açılışta öz-test yapılır, başarılıysa `esp_ota_mark_app_valid_cancel_rollback`; başarısızsa geri dönülür.
  - Halkalar sırayla açılır: 1 test kartı, %5, %25, %100. Kalp atışı, çökme ya da boot döngüsü kötüleşirse yayılım durur.
- Araç: Agent `IoT Fleet Engineer`, Agent `git-canary-izleme`, Agent `sec-tehdit-modelleme` (OTA yolu).
- Kapı (donanımda, HIL):
  - Bozuk ve imzasız imaj reddedilmeli.
  - Güncelleme ortasında elektrik kesilince cihaz kurtulmalı.
  - Öz-testi geçemeyen sürümde geri dönüş çalışmalı.
- Tartışma (kritik): Secure Boot v2 ve flash şifreleme için yakılan eFuse geri alınamaz.
- Tavan: Onaysız olarak en çok 1 test kartında eFuse yakılır. Her halka geçişi Ömer onayıyla yapılır; ilk üretim halkası en çok 5 cihazdır.

**F6 Operasyon** · 10k
- Araç: Agent `dok-runbook` (broker çöküşü, OTA durdurma), Agent `inc-uretim-hazirligi`, Agent `sec-kvkk-gdpr-kontrol` (konum ve zaman kişisel veri sayılıyorsa saklama süresi).

---
Departman yönetici skill'lerinin adlarını doğrulamadığım için `departman-*` skill'leri plana koymadım. plan_kur.py'nin bu iki işi rutin sayması bir sınıflandırma hatası gibi görünüyor; PLAN-KUR-3 ölçümüne bir veri noktası olarak eklenebilir.

## 6. YouTube kanalı için otomatik kısa video hattı kur: uzun videonun transkriptinden öne çıkan anları seç, ffmpeg ile dikey kırp, altyazı göm, Remotion ile başlık animasyonu ekle.
### X
**Varsayımlar:** Kaynak kanalın kendi videoları. Yükleme istenmedi, plana alınmadı: dışarıya yayın olduğu için OAuth ve onay gerekir. Hedef format 1080×1920, klip başına ≤60 sn.

**F0 Brief (5k)**
- Adım: hook kuralları ve klip sayısı (en çok 5 klip/video). Araç: `Skill reel-plan`.
- Adım: başlık önerileri. Araç: `Agent urn-baslik-yazimi`.
- Kapı: brief'te kabul ölçütleri yazılı.

**F1 Girdi + an seçimi (8k)**
- Adım: video ve altyazıyı indir. Araç: `yt-dlp` (cli) ya da `Skill baoyu-youtube-transcript`.
- Adım: altyazı yoksa transkripti çıkar. Araç: `Skill watch` (whisper).
- Öğrenim: 429 sonrası gelen "altyazı yok" yanıtı hız sınırıdır, gerçek yokluk değildir. Bekleyip en çok 3 kez yeniden denenir.
- Adım: öne çıkan anları seç. Araç: `Agent vid-kisa-klip-secici`. Çıktı: `clips.json` (start, end, puan, hook).
- Tartışma: seçimi LLM puanı mı yapsın, kural mı (duraklama/vurgu)? Öneri: LLM, video başına en çok 1 çağrı. Kural yalnız yedek olarak kalır.
- Kapı: `clips.json` şema testi (pytest). Her klip 15–60 sn olmalı, klipler çakışmamalı.

**F2 Kesim + kırpma + altyazı (12k)**
- Adım: kes, 9:16 kırp, altyazıyı göm. Araç: `Agent vid-ffmpeg-donusturucu` ve `ffmpeg` (cli). Filtre: `-ss/-to`, `crop=ih*9/16:ih`, `subtitles=clip.ass`.
  - shortcut: kırpma ortadan yapılır; konuşmacı kenarda kalırsa yüz takibine geçilir.
- Adım: altyazıyı güvenli alana yerleştir. Araç: `Agent vid-sosyal-video-bicim`.
- Öğrenim: zamanlar kare ızgarasına `floor` ile oturtulur. `round(t·fps)` kareyi bir sonraki sahneye kaydırıyordu.
- Kapı: `ffprobe` ile 1080×1920 ve süre ≤60 sn kontrolü. Zaman aritmetiğine pytest yazılır. ffmpeg argümanları liste olarak verilir, `shell=True` kullanılmaz.

**F3 Remotion başlık (10k)**
- Adım: kompozisyonu kur. Araç: `Skill remotion-create`, ardından `Agent vid-remotion-kurucu`. Yapı: klip `<OffthreadVideo>` olarak girer, başlık 0–2 sn arası bir `<Sequence>` içinde.
- Adım: önizleme ve render. Araç: `Skill remotion-studio`, ardından `Skill remotion-render`.
- Adım: animasyon kuralları. Araç: `Skill inclusive-interaction:motion-sensitivity`.
- Tartışma: başlık klibin üstüne tam render mı edilsin, yoksa alfa kanallı katman olarak üretilip ffmpeg ile mi bindirilsin? Öneri: tam render. Tek adım olur, klip sayısı az.
- Kapı: Remotion render çıkış kodu 0. Her klipten 1 kare alınıp başlık ve altyazının çakışmadığına bakılır (Read ile).

**F4 Test + güvenlik + kapanış (8k + 3k)**
- Kapı: pytest yeşil, semgrep 0 yüksek, gitleaks 0 bulgu. Araçlar: `Agent sec-sast-kosucu`, `Agent sec-gitleaks-gecmis`.
- Kapı (erişilebilirlik): altyazı her klipte olmalı. Araç: `Skill accessible-content:multimedia-accessibility`.
- Adım: uçtan uca deneme, 1 gerçek video ile.
- Adım: başlık, açıklama ve etiketler `meta.json` dosyasına yazılır. Araç: `Skill youtube-agent:yt-seo`.

**İnceleme:** `ecc:code-reviewer` her faz sonunda, `ecc:security-reviewer` F4'te.

**Konsey:** yok. Tüm adımlar geri alınabilir.

**Toplam bütçe:** ~46k.
### Y
Varsayım: kanal sahibinin kendi videoları işlenir, hat yerelde çalışır, YouTube'a yükleme kapsam dışıdır.

- **Faz 0 · Karar (≈6k)**
  - Adım: `departman-arastirma-ogrenme` ile araç sırası belirlenir. `vid-video-brief` ajanı brief'i yazar: 9:16, 1080×1920, 15–60 sn, video başına en çok 5 kısa.
  - Tartışma 1: Remotion 3 kişiyi aşan şirkette ücretli lisans ister (öğrenim #88). Alternatif kurulu `hyperframes` eklentisi. Kullanıcı kararı yazılı alınır.
  - Tartışma 2: Remotion başlığı alfa kanallı katman (ProRes 4444/webm) olarak üretir, ffmpeg bunu kırpma ve altyazıyla tek geçişte birleştirir. Böylece video iki kez kodlanmaz. Önerim bu.
- **Faz 1 · Girdi (≈8k)**
  - Adım: `yt-dlp` CLI (`vid-ytdlp-indirme`) video ve altyazıyı indirir. Altyazı yoksa yerel `whisper-cli` kelime zaman damgalı transkript çıkarır (`baoyu-youtube-transcript` yedek).
  - Kural: 429 hatası "altyazı yok" sayılmaz, beklenip yeniden denenir (öğrenim #87).
  - Kapı: SRT/JSON ayrıştırıcıya pytest. KVKK için transkript dış LLM'e gitmez, konuk adı geçiyorsa `sec-llm-pii-maskeleme` kullanılır.
  - İnceleme: `dil-python-tip-guvenligi`.
- **Faz 2 · An seçimi (≈12k)**
  - Adım: `vid-kisa-klip-secici` ajanı ile `youtube-agent:yt-shorts` skill'i kural tasarlar. `sec.py` cümle sınırlı aday pencereler üretir, puanlar ve `clips.json` yazar (start, end, başlık, puan).
  - LLM puanlaması `claude -p` ile yapılırsa tavan video başına en çok 1 çağrı. Uzun istem stdin ile verilir.
  - Kapı: `otm-sema-dogrulayici` ile JSON şeması. `qa-sinir-deger-analizi` testleri: 15/60 sn sınırı, çakışma yok, cümle ortasında kesim yok.
  - İnceleme: `inc-test-kalitesi-inceleme`.
- **Faz 3 · ffmpeg dikey kırpma ve altyazı (≈15k)**
  - Adım: `vid-ffmpeg-donusturucu` ve `vid-sosyal-video-bicim` (güvenli alan) kullanılır. Kırpma `crop=ih*9/16:ih`, ölçek 1080:1920. Kelime zamanlarından ASS altyazı üretilir, `subtitles=` filtresiyle gömülür (Windows yol kaçışına dikkat). Ses `loudnorm -14 LUFS` (`vid-ses-duzeni`).
  - Yüz takipli kırpma ilk sürümde yok, ortadan kırpılır.
  - Kapı: ffprobe ile çözünürlük, süre ve ses akışı doğrulanır. `vid-kare-cikarici` temas sayfası çıkarır, ana oturum Read ile bakar. Renk soluksa `vid-renk-uzayi`.
  - İnceleme: `vid-gecis-ve-ritim`.
- **Faz 4 · Remotion başlık (≈15k)**
  - Adım: `remotion-create` ve `ecc:remotion-video-creation` skill'leri, `vid-remotion-kurucu` ajanı. Zamanlama ve easing `vid-hareket-grafigi` ile. Props zod şemalı (başlık, süre).
  - Render yalnız headless `remotion-render` ile yapılır. `remotion-studio` tarayıcı açtığı için ekran kuralı gereği kullanılmaz.
  - Kapı: tek kompozisyon render testi. `inclusive-interaction:motion-sensitivity` ile yanıp sönme ve hız sınırı.
  - İnceleme: `ecc:code-reviewer`.
- **Faz 5 · Hat (≈15k)**
  - Adım: tek giriş noktası `hat.py`: indir → transkript → seç → kırp/altyazı → başlık → birleştir. Her aşama çıktısı varsa atlanır, yani hat kaldığı yerden devam eder. Arka plan işi yalnız `.kos/kopru/arka.py` ile koşar.
  - Kapı: 60 sn'lik fixture videoyla uçtan uca pytest. `accessible-content:multimedia-accessibility` ile altyazı kontrastı, boyutu ve güvenli alanı.
  - İnceleme: `inc-ponytail-kod` ve `ecc:security-reviewer` (URL/yol girdisinden komut enjeksiyonu riski).
- **Faz 6 · Kapanış (≈4k)**
  - `departman-surec-git-yayin` ile commit. Rapor: test sayısı ve gerçek bir videoda tek uçtan uca koşu.

## 7. Astro ile iki dilli (TR/EN) teknik dokümantasyon sitesi kur: içerik koleksiyonları, Pagefind arama, SEO meta etiketleri, erişilebilirlik testi ve GitHub Actions ile yayın.
### X
**Varsayımlar:** Varsayılan dil TR, yollar `/tr/` ve `/en/`. Yayın GitHub Pages'e yapılır.

**F0 Hazırlık (5k)**
- Adım: UI kuralları. Araç: `Skill frontend-craft` (zorunlu, Bölüm 6 raporu kapanışta).
- Adım: yayın sırası. Araç: `Skill departman-surec-git-yayin`.

**F1 Tasarım (10k)**
- Adım: URL şeması, dil seçici ve gezinti derinliği. Araç: `Agent fe-site-mimarisi`.
- Tartışma: Starlight mı, yalın Astro mu? Starlight (MIT) i18n, Pagefind, içerik koleksiyonu şeması ve SEO metasını hazır getirir. Yalın Astro'da bunların hepsi elle yazılır. Öneri: Starlight; ilk hafta geri dönmek ucuz.
- Kapı: kabul ölçütleri yazılı. Araç: `Agent pln-kabul-olcutleri`.

**F2 Uygulama (40k)**
- Adım: iskelet. Araç: `Agent fe-astro` ve `npm create astro -- --template starlight`.
- Adım: içerik koleksiyonları. Yapı: `src/content/docs/{tr,en}`, `docsSchema` (zod).
- Adım: EN çeviri ve terim sözlüğü. Araç: `Agent dok-cevirmen-teknik`.
- Adım: Pagefind araması. Starlight'ta hazır gelir; dizin dile göre `html lang` ile ayrılır.
- Adım: SEO metası. Araçlar: `Agent fe-meta-seo-duzeltici` ve `Skill ecc:seo`. Kapsam: title/description, canonical, `hreflang` alternate, OG, `@astrojs/sitemap` (i18n), robots.txt.
- Kapı: `astro check` 0 hata.
- Kapı: dil eşi testi (küçük node betiği): her TR sayfanın EN karşılığı olmalı, ya da sayfa bilerek eksik işaretlenmiş olmalı.

**F3 Test + güvenlik (12k)**
- Kapı (erişilebilirlik): `@axe-core/playwright` ile 0 ciddi/kritik ihlal, klavye turu yapılır. Araç: `Agent qa-erisilebilirlik-testi`.
- Kapı (performans): Lighthouse CI ile LCP ≤2.5 sn, CLS ≤0.1, INP ≤200 ms, ilk yükte JS ≤170 KB gz.
- Kapı (SEO): `Skill marketing-skills:seo-audit`. Bozuk link, eksik canonical ve eksik hreflang sayısı 0 olmalı.
- Kapı (güvenlik): semgrep 0 yüksek, gitleaks 0 bulgu, `npm audit` yüksek bulgu 0.

**F4 Yayın + kapanış (8k + 3k)**
- Adım: deploy workflow'u yaz. Araç: `Agent git-ci-boru-hatti`. İçerik: `withastro/action` ve `actions/deploy-pages`. Yetkiler yalnız `pages: write` ve `id-token: write`, action'lar SHA'ya sabitlenir.
- Kapı: workflow incelemesi. Araç: `Skill gha-security-review`.
- Adım: önce önizleme. PR'da build artifact'i ve `astro preview` ile kontrol edilir.
- Adım: Pages'i açma ve ilk push dışarıya yayındır, onay alınır. İzleme: `gh run watch`.
- Kapı: sağlık kontrolü. `curl` ile `/tr/` ve `/en/` 200 dönmeli, arama sayfası açılmalı.
- Geri alma (≤5 dk): son başarılı deploy run'ı `gh run rerun` ile yeniden çalıştırılır, ya da `git revert` yapılır.

**İnceleme:** `ecc:code-reviewer` her faz sonunda, `ecc:security-reviewer` F3'te, `ecc:a11y-architect` F2 sonunda.

**Konsey:** yok. Starlight kararı geri alınabilir.

**Toplam bütçe:** ~78k.

---

Planlar aracın çıktısıyla yazıldı, ek sorgu yapılmadı. 6. işteki YouTube yüklemesini ve yüz takibiyle kırpmayı plana almadım. Kanalda Shorts süresi 60 sn'den farklı istenirse F1 kapısı değişir. Starlight ve Lighthouse CI projeye npm bağımlılığı olarak girer; bu ortamda kurulu olup olmadıklarına bakmadım.
### Y
Varsayım: varsayılan dil TR (`/tr/`, `/en/`), yayın GitHub Pages'e.

- **Faz 0 · Karar (≈6k)**
  - Adım: UI işi olduğu için önce `/frontend-craft` yüklenir. URL şeması ve gezinme derinliği `fe-site-mimarisi` ile.
  - Tartışma: Starlight mı, düz Astro mu? Starlight içerik koleksiyonlarını, Pagefind'ı, i18n'i, hreflang'i ve erişilebilir bileşenleri hazır getirir, kod çok azalır. Önerim Starlight.
  - Lisans: Starlight ve Pagefind MIT, `ara-lisans-kontrol` ile teyit edilir.
- **Faz 1 · İskelet (≈10k)**
  - Adım: `npm create astro -- --template starlight` ile kurulur. `fe-astro` ajanı çalışır, güncel doküman `context7` MCP'sinden gelir. `locales` (tr root, en) ayarlanır. `docs` koleksiyonunun zod şemasında title ve description zorunludur.
  - Kapı: `astro check` ve `astro build` yeşil.
  - İnceleme: `ecc:code-reviewer`.
- **Faz 2 · İçerik ve çeviri (≈15k)**
  - Adım: `dok-cevirmen-teknik` terim sözlüğüyle EN'e çevirir.
  - Kapı: TR ve EN slug eşleşmesini karşılaştıran node testi. Eksik çeviri CI'da uyarı verir.
  - İnceleme: `dok-icerik-editoru`.
- **Faz 3 · Arama (≈6k)**
  - Adım: Pagefind dil başına ayrı index üretir (`html lang` ile).
  - Kapı: `qa-playwright` testi. `/tr`'de "kurulum" araması yalnız TR sonuç, `/en`'de yalnız EN sonuç döndürür.
- **Faz 4 · SEO (≈10k)**
  - Adım: `ecc:seo` skill'i ve `fe-meta-seo-duzeltici` ajanı. `site` ayarı, canonical, OG etiketleri, i18n'li `@astrojs/sitemap` ve `robots.txt`.
  - Kapı: `dist` taranır. Her sayfada title, description, canonical ve hreflang (tr/en/x-default) bulunur.
  - İnceleme: `ecc:seo-specialist`.
- **Faz 5 · Erişilebilirlik (≈12k)**
  - Adım: `qa-erisilebilirlik-testi` ajanı, preview'da tüm sayfalara `@axe-core/playwright` uygular ve klavyeyle gezinmeyi dener. `web-design-guidelines` skill'i kullanılır.
  - Kapı: serious/critical ihlal 0, `lang` ve odak sırası doğru. Lighthouse kurulu olmadığı için atlanır, axe aynı denetimi karşılar.
  - Kapanışta frontend-craft Section 6 tur raporu yazılır.
- **Faz 6 · CI/CD (≈10k)**
  - Adım: `git-ci-boru-hatti` ile `withastro/action` ve `actions/deploy-pages` kurulur. PR'da build, check, arama ve axe testleri koşar, deploy yalnız `main`'de olur.
  - Kapı: `gha-security-review`. Action'lar SHA ile sabitlenir, izinler en dar tutulur (`pages: write`, `id-token: write`). `gh run watch` yeşil olmalı.
  - Pages'i açmak dışa dönük bir adım, önce kullanıcıdan onay alınır.
- **Faz 7 · Kapanış (≈4k)**
  - `departman-surec-git-yayin` ile commit ve PR.

---
İki iş de zor olduğu için katalog sorgulandı. İlk ortak çağrının çıktısı dosyaya düştü, kurala göre her iş için `--aday 40` ile ayrı ayrı yeniden çalıştırıldı.

Kapsam dışı bırakılanlar: 6'da YouTube'a yükleme ve yüz takipli kırpma, 7'de Lighthouse. Planlardaki araçların kurulu olduğu yalnız katalog etiketinden alındı, ayrıca doğrulanmadı.

## 8. Yavaş çalışan bir Python betiğini cProfile ile profille ve en sıcak noktayı düzelt.
### X
**Varsayım:** Betik ve tipik bir girdisi elde var, CPU kaynaklı yavaşlık beklenir. Asıl sıcak nokta G/Ç çıkarsa dalga durdurulur ve rapor yazılır.

**Faz 1 · Ölçüm (≤8k jeton)**
- Adım: `python -m cProfile -o prof.out betik.py <girdi>` ve `pstats` ile `sort_stats("cumulative").print_stats(15)`. Ham çıktı bağlama alınmaz, yalnız ilk 15 satır alınır.
- Araç: `dil-python-profil` alt ajanı (sonnet). Gerekirse `py-spy record` ile ikinci bir doğrulama yapılır.
- Kapı: Taban süre `time` ile 3 koşuda ölçülür, medyanı kaydedilir.

**Faz 2 · Kök neden (≤6k)**
- Adım: En yüksek tottime/cumtime satırı açılır, yalnız ~20 satırlık dar aralık Read ile okunur. Kök neden kanıtlanmadan düzeltme yapılmaz.
- Tartışma noktası: Algoritma mı değişecek (ör. O(n²) → dict/set), yoksa önbellek mi eklenecek (`functools.lru_cache`)? Varsayılan tercih algoritma, çünkü önbellek bayat veri riski getirir.

**Faz 3 · Düzeltme (≤8k)**
- Adım: Önce davranışı sabitleyen bir pytest yazılır (eski çıktı = yeni çıktı) ve kırmızı/yeşil durumu görülür. Sonra en küçük diff ile düzeltme yapılır.
- Kapı: pytest yeşil olmalı. Profil yeniden alınır, sıcak nokta listeden düşmeli ve medyan süre en az %30 iyileşmeli.
- İnceleme: `inc-ponytail-kod` (gereksiz soyutlama var mı).

**Kapanış:** commit · test sayısı · önce/sonra süresi.
### Y
Python betiğini cProfile ile profilleme ve en sıcak noktayı düzeltme.

**Faz 1: Ölç (≤8k jeton)**
- **Adım:** Temsilî girdiyle `python -m cProfile -o prof.out betik.py <girdi>` koşulur. Ardından `python -c "import pstats; pstats.Stats('prof.out').sort_stats('cumulative').print_stats(15)"` ile en çok süre alan 15 satır çıkarılır.
- **Neden pstats:** snakeviz tarayıcı açtığı için ekran kuralına aykırı, kullanılmaz.
- **Araç:** `dil-python-profil` alt ajanı (sonnet). Main session'a yalnız ilk 5 satır özeti döner.
- **Kapı:** Taban süre `timeit` ya da `time` ile 3 koşunun ortancası olarak kaydedilir.

**Faz 2: Kök nedeni kanıtla (≤5k jeton)**
- **Adım:** tottime ile cumtime karşılaştırılır. Sıcak fonksiyonun yalnız ilgili 20 satırı Read ile okunur.
- **Tipik nedenler:** döngü içinde liste araması (`in list`), tekrarlanan I/O, regex'in her seferinde derlenmesi, gereksiz kopya.
- **Tartışma noktası:** Algoritma değişikliği mi (set/dict, önbellek), yoksa yalnız I/O toplama mı? En küçük değişiklik seçilir.

**Faz 3: Düzelt ve kapı (≤10k jeton)**
- **Önce test:** Düzeltmeden önce mevcut çıktıyı kilitleyen bir golden test yazılır (pytest, aynı girdi → aynı çıktı) ve testin yeşil olduğu görülür.
- **Düzeltme:** Ardından en küçük değişiklik yapılır.
- **Kapı:**
  - Golden test yeşil kalmalı.
  - Profil yeniden alınır; sıcak satır ilk 5'ten düşmeli.
  - Süre kazancı ≥%30 olmalı; değilse rapora sapma olarak yazılır.
- **İnceleme:** `inc-ponytail-kod`. Gereksiz önbellek ya da soyutlama eklenmemiş olmalı.

## 9. Postgres'te yavaş bir raporlama sorgusunun EXPLAIN ANALYZE çıktısını oku ve uygun indeksi öner.
### X
**Varsayım:** Sorgu metni ve `EXPLAIN (ANALYZE, BUFFERS)` çıktısı elde var. Canlı veritabanına yazma yetkisi yok, iş yalnız öneri.

**Faz 1 · Plan okuma (≤6k)**
- Adım: En pahalı düğüm bulunur (Seq Scan, Sort ile disk taşması, Nested Loop'ta loops×rows). Tahmini satır ile gerçek satır arasındaki sapma kontrol edilir.
- Araç: `db-sorgu-optimize` alt ajanı. Plan uzunsa önce `jev log` çalıştırılır.
- Kapı: Sapma 10 katı aşarsa önce `ANALYZE tablo` (istatistik) önerilir. İndeks kararı ertelenir.

**Faz 2 · İndeks tasarımı (≤6k)**
- Araç: `db-indeks-danismani`.
- Adım: WHERE eşitlik sütunları → aralık sütunu → ORDER BY sırasıyla bileşik indeks kurulur. Filtre sabitse kısmi indeks, gerekli sütunlar azsa `INCLUDE` ile kapsayan indeks değerlendirilir.
- Tartışma noktası: Yazma maliyeti ve indeks boyutu, okuma kazancına karşı tartılır. `pg_stat_user_indexes` ile mevcut indekslerden biri genişletilebiliyorsa yenisi açılmaz.

**Faz 3 · Doğrulama (≤5k)**
- Adım: Staging'de ya da kopyada `CREATE INDEX CONCURRENTLY` çalıştırılır, ardından EXPLAIN ANALYZE yeniden alınır.
- Kapı: Plan Index Scan veya Index Only Scan'e geçmeli, süre en az %50 düşmeli. Canlı ortamda uygulama ayrı onaya bağlı.
- İnceleme: `Database Optimizer` ajanı öneriyi örnekleyerek kontrol eder.

**Çıktı:** DDL, önce/sonra plan özeti ve geri alma için `DROP INDEX CONCURRENTLY`.
### Y
Postgres raporlama sorgusunun EXPLAIN ANALYZE çıktısını okuyup indeks önerme.

**Faz 1: Plan al (≤6k jeton)**
- **Adım:** Kopya ya da staging veritabanında `psql` ile `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` koşulur. Üretimde ANALYZE koşulmaz, çünkü sorguyu gerçekten çalıştırır.
- **Araç:** `db-sorgu-optimize` alt ajanı.
- **Ajan döndürür:**
  - en pahalı düğüm,
  - tahmini ve gerçek satır sayısı farkı,
  - Seq Scan, Sort ve Hash spill durumu.
- **Kapı:** Bağlantı dizesi ve env değerleri basılmaz.

**Faz 2: Tanı (≤6k jeton)**
- **Adım:** Tahmin sapması büyükse önce `ANALYZE <tablo>` ile istatistik tazelenir. İndeks bu adımdan sonra düşünülür.
- **Araç:** `db-indeks-danismani`. WHERE, JOIN ve ORDER BY sütunlarına göre birleşik, kısmi ya da kapsayan (`INCLUDE`) indeks seçilir.
- **Tartışma noktası:** Sütun sırası (eşitlik → aralık → sıralama) ve yazma maliyeti. `pg_stat_user_indexes` ile var olan ya da kullanılmayan çift indeksler kontrol edilir.

**Faz 3: Doğrula (≤6k jeton)**
- **Adım:** Staging'de `CREATE INDEX CONCURRENTLY`, sonra EXPLAIN ANALYZE yeniden koşulur.
- **Kapı:**
  - Planda yeni indeks kullanılmalı.
  - Süre ve buffer sayısı düşmeli.
  - Sonuç satır sayısı aynı kalmalı.
- **Teslim:** Migration dosyası olarak öneri (CONCURRENTLY, transaction dışında) ve geri alma için `DROP INDEX CONCURRENTLY`.
- **İnceleme:** `db-migration-planlayici`, kilit ve kesinti riski açısından.

## 10. Bir React bileşenindeki gereksiz yeniden render'ları bul ve düzelt.
### X
**Varsayım:** Bileşen adı ve yavaşlığın göründüğü etkileşim biliniyor. UI'a dokunduğu için önce /frontend-craft yüklenir ve Bölüm 6 tur raporu kapanışta zorunlu.

**Faz 1 · Ölçüm (≤8k)**
- Adım: React DevTools Profiler'da "why did this render" açılır, etkileşim kaydedilir ve render sayısı ile süresi not edilir.
- Araç: playwright headless ile tekrarlanabilir bir etkileşim betiği yazılır. Varsayılan tarayıcı açılmaz.
- Alt ajan: `fe-react-bilesen-inceleme`. Yalnız şüpheli prop/state zincirini döner.

**Faz 2 · Kök neden (≤5k)**
- Tipik nedenler: her render'da yeni nesne, dizi ya da callback prop'u; büyük bir context değerinin değişmesi; üstte tutulan state.
- Tartışma noktası: Önce state'i aşağı taşımak ya da context'i bölmek denenir. `memo`, `useMemo` ve `useCallback` yalnız ölçülen sıcak noktada kullanılır. React Compiler açıksa elle memo eklenmez.

**Faz 3 · Düzeltme (≤8k)**
- Adım: Önce render sayısını sabitleyen bir test yazılır (RTL ve render sayacı) ve kırmızısı görülür. Sonra en küçük diff uygulanır.
- Kapı: Test yeşil olmalı ve Profiler'da render sayısı düşmeli. `qa-erisilebilirlik-testi` ile hızlı bir axe kontrolü yapılır, davranış ve odak değişmemeli.
- İnceleme: `ecc:code-reviewer`.

**Kapanış:** frontend-craft Bölüm 6 tur raporu · commit · test sayısı.

Hiçbir dosya yazılmadı, ortam yoklanmadı. Jeton bütçeleri tahmin, ölçülmedi.
### Y
React bileşenindeki gereksiz yeniden render'ları bulup düzeltme.

**Faz 0:** UI dokunduğu için önce `/frontend-craft` yüklenir; kapanışta Section 6 raporu verilir.

**Faz 1: Ölç (≤8k jeton)**
- **Adım:** React DevTools Profiler ya da test içinde `<Profiler onRender>` ile render sayısı ölçülür. Etkileşim playwright headless ile tetiklenir; varsayılan tarayıcı açılmaz.
- **Araç:** `fe-react-bilesen-inceleme` alt ajanı.
- **Ajan döndürür:**
  - satır içi obje ve fonksiyon prop'ları,
  - kararsız `key`,
  - fazla geniş context,
  - eksik ya da fazla effect bağımlılıkları.

**Faz 2: Test önce (≤6k jeton)**
- **Adım:** @testing-library ve Profiler sayacıyla testte beklenen render sayısı belirtilir (assert). Test önce kırmızı görülür.

**Faz 3: Düzelt (≤8k jeton)**
- **Adım:** Kök nedene göre en küçük düzeltme:
  - state'i alt bileşene indirme,
  - context'i bölme,
  - gerekiyorsa `React.memo`, `useCallback` veya `useMemo` (her yere değil).
- **Tartışma noktası:** memo maliyeti ile render maliyeti karşılaştırılır. Ucuz bileşende memo eklenmez.
- **Kapı:**
  - Render sayısı testi yeşil, mevcut testler yeşil.
  - `eslint-plugin-react-hooks` (exhaustive-deps) temiz.
  - Davranış değişmemeli.
- **İnceleme:** `agent-skills:code-reviewer`.

Sınıflandırma doğrulanmadı: 8–10'u "rutin" sayan bilgi, önceki PLAN-KUR-3 kaydındaki "7 zor + 3 rutin" notundan çıkarım. Bu yüzden `plan_kur` adayları kullanılmadı. Plandaki alt ajan ve araç adları bu ortamdaki listeden alındı. Kurulu olmayan araç olarak yalnız `pytest-benchmark` geçebilirdi; o da planda kullanılmadı.
