## 1. Godot 4 ile çevrim içi çok oyunculu kart oyunu yap: yetkili sunucu, WebSocket durum senkronu, eşleştirme kuyruğu, hile önleme ve itch.io'ya dağıtım.
### X
**Varsayım:** Proje sıfırdan başlıyor, oyun 2 oyunculu ve sıra tabanlı. Sunucu ayrı bir VPS'te koşar, itch.io yalnız istemciyi barındırır. Yayın fazını `departman-surec-git-yayin` yönetir. Arayüz web değil Godot sahnesi olduğu için `frontend-craft` atlanır.

**F0 · Kural ve mesaj sözleşmesi (~25k)**
- **Adım:** tek sayfalık oyun dokümanı ve mesaj sözleşmesi yazılır: `join_queue`, `match_found`, `play_card`, `state{seq}`, `error`.
- **Araç:** oyun dokümanı için `oyn-oyun-dokuman`, yetki modeli için `oyn-ag-senkronu`.
- **Kapı:** her mesajın doğrulama kuralı yazılı olur. Rakibin eli ve deste sırası istemciye hiç gönderilmez.
- **İnceleyen:** `sec-tehdit-modelleme`. STRIDE ile sahte hamle, tekrar, gizli bilgiye bakma ve mesaj seli senaryolarını sınar.
- **Tartışma:** yetkili sunucu Godot headless mı, Node mu? Öneri: Godot headless. Kural kodu tek dosyada (`rules.gd`) kalır; Node seçilirse kuralların ikinci kopyası gerekir.

**F1 · Kural çekirdeği, test önce (~40k)**
- **Adım:** `rules.gd` saf bir fonksiyon olur: `apply(state, action) → state | hata`. Karıştırma ve seed yalnız sunucuda üretilir.
- **Araç:** `oyn-oyun-motoru-script`, godot MCP. Testler `godot --headless -s tests/run_rules.gd` ile koşar; assert tabanlıdır, eklenti gerekmez.
- **Kapı:** sıra dışı oynama, elde olmayan kart ve çift oynama testleri önce kırmızı görülür, sonra yeşile döner.
- **İnceleyen:** `ecc:code-reviewer`.

**F2 · Sunucu, durum senkronu, eşleştirme, hile önleme (~60k)**
- **Bağlantı:** Godot 4'ün yerleşik `WebSocketMultiplayerPeer`'ı kullanılır.
- **Senkron:** her eylemden sonra oyuncuya, ona özel kırpılmış bir anlık görüntü ve `seq` gönderilir. Yeniden bağlanan oyuncu son görüntüyü alır.
- **Eşleştirme:** sunucu içinde FIFO kuyruk tutulur; 2 oyuncu birleşince oda açılır. Kuyrukta zaman aşımı, kuyruktan çıkma ve heartbeat vardır.
- **Hile önleme:**
  - `@rpc("any_peer")` yalnız niyet taşır; sunucu peer id'yi ve kuralı doğrular.
  - `seq` ile tekrarlanan mesaj reddedilir.
  - Oyuncu başına hız sınırı uygulanır.
- **Araç:** heartbeat ve yeniden bağlanma için `dil-websocket`.
- **Kapı:** iki headless istemci betiği tam bir maçı ve kopup yeniden bağlanmayı oynar. Şu girişimler reddedilmelidir:
  - başkasının peer id'siyle hamle,
  - rakibin elini isteme,
  - saniyede 100 mesaj.
- **İnceleyen:** `oyn-ag-senkronu` ve `ecc:security-reviewer`.
- **Tartışma:** şimdilik tek süreç kullanılır. Oda başına ölçüm yapılmadan yatay ölçekleme kararı verilmez.

**F3 · İstemci ve Web dışa aktarımı (~40k)**
- **Adım:** Godot Web export tek iş parçacığıyla yapılır, böylece SharedArrayBuffer gerekmez. Sunucu adresi `wss://` olur, çünkü itch https'tir ve `ws://` engellenir.
- **Araç:** godot MCP, `test-playable-web-games` skill'i, headless playwright duman testi.
- **Kapı:** headless Chrome'da açılış, kuyruğa girme ve maç bitişi çalışır; konsolda 0 hata olur.

**F4 · Dağıtım (~35k)**
- **Sunucu:** `ops-systemd-birim` ile servis birimi, `ops-nginx-ters-vekil` ile TLS ve WebSocket upgrade.
- **İstemci:** `ship-web-games` skill'i ile itch.io'ya yüklenir. Yükleme için itch'in butler CLI'ı gerekir; kurulu değil, kurulum için onay alınır. Alternatif: itch panelinden zip yüklemek.
- **Sıra:** `departman-surec-git-yayin`. CI'da headless testler ve export koşar. Sürüm notu `build-game-changelog` ile yazılır.
- **Kapı:** canlıda iki sekme arasında bir maç oynanır.
- **İnceleyen:** `git-yayin-oncesi-kontrol`. Yayın kırılırsa `ops-dagitim-sorun-giderme` devreye girer.
- **Tavan:** itch'e en çok 3 yükleme denemesi. VPS ücretliyse önce onay alınır.
### Y
(Godot 4 çok oyunculu kart oyunu)
Varsayımlar: istemci HTML5 olarak itch.io'da, sunucu Ömer'in VPS'inde headless Godot olarak çalışır. Kabul ölçütü yoksa bu iş tasarım fazından sonra DUR raporuyla durur.

**Faz 0 · Hazırlık (5k)**
- Adım: dalga.md'ye KARAR ve kabul ölçütlerini yaz; yayın kısmı için departman-surec-git-yayin skill'ini aç.
- Araç: godot MCP (ToolSearch ile yüklenir).

**Faz 1 · Tasarım (15k)**
- Mimari: Agent oyn-ag-senkronu ile yetkili sunucu kurulur. İstemci yalnız niyet gönderir ("kart oyna", "pas"); kuralları sunucu doğrular.
- Protokol: Agent dil-websocket ile mesaj şeması kurulur. Her mesajda seq no ve sürüm alanı olur. Kalp atışı 5 s, yeniden bağlanınca tam durum anlık görüntüsü gönderilir.
- Hile önleme: Agent sec-tehdit-modelleme ile STRIDE modeli çıkar.
  - Desteyi sunucu kriptografik rastgeleyle karıştırır.
  - Her oyuncu yalnız kendi elini görür; durum oyuncu başına süzülür.
  - Sırası olmayan ya da geçersiz hamle reddedilir.
  - Mesaj hız sınırı için Agent be-hiz-sinirlayici kullanılır.
- Eşleştirme: sunucuda bellek içi FIFO kuyruğu (2–4 oyuncu), 30 s zaman aşımı. ELO ve dereceli mod yok, istenmedi.
- Tartışma noktası (konsey yok, geri alınabilir): sunucu Godot headless mı, ayrı Node mu? Öneri: Godot headless (WebSocketMultiplayerPeer), çünkü kural kodu istemciyle ortak kalır.
- Kapı: tehdit modelinde yüksek riskli her madde için bir test adı yazılmış olmalı.
- İnceleme: Agent ecc:code-reviewer, tasarım belgesi üzerinde.

**Faz 2 · Uygulama (50k)**
- Adım: kural motorunu saf GDScript sınıfı olarak yaz (ağdan bağımsız, test edilebilir). Sonra sunucu sahnesi, eşleştirme kuyruğu ve istemci arayüzü gelir.
- Araç: Agent oyn-oyun-motoru-script, godot MCP (sahne ve betik), Agent Realtime Collaboration Engineer (yeniden bağlanma ve anlık görüntü).
- Kapı: önce kırmızı görülen headless kural testleri yeşile döner (`godot --headless` godot MCP üzerinden). Kaydet→yükle tur testi aynı durumu vermeli. Hedef yapı uyarısız derlenmeli.
- İnceleme: Agent ecc:code-reviewer, faz sonunda.

**Faz 3 · Test + güvenlik (12k)**
- Adım: 2 istemci + sunucuyla yerel maç testi.
- Hile senaryoları: sahte kart oynama, başkasının sırası, seq tekrarı, saniyede 100 mesaj. Hepsi reddedilmeli ve bağlantı düşmemeli.
- Kapı:
  - 60 fps (kare ≤16.7 ms)
  - semgrep 0 yüksek, gitleaks 0 bulgu
  - arayüzde klavye ile oynanabilirlik: Agent qa-erisilebilirlik-testi, 0 ciddi ihlal
- İnceleme: Agent ecc:security-reviewer ile Agent sec-cikis-oncesi-guvenlik.

**Faz 4 · Yayın + kapanış (8k)**
- Sunucu: wss:// zorunlu (itch https sunar). TLS ve WebSocket yükseltmesi için Agent ops-nginx-ters-vekil; sunucu systemd birimiyle çalışır.
- Ücretli VPS/deploy tavanı: en çok 1 VPS, en çok 3 deploy denemesi.
- İstemci: Skill ship-web-games yönergesiyle tek iş parçacıklı web dışa aktarımı (SharedArrayBuffer gerekmez). İtch.io'ya zip yüklemesini Ömer elle yapar; butler'ın kurulu olduğu doğrulanmadı.
- Sürüm notu: Skill build-game-changelog.
- Kapı: itch sayfasından canlı maç kurulur. Hata çıkarsa Agent ops-dagitim-sorun-giderme.
- Kapanış raporu: commit · test sayısı · CI · sapmalar.

## 2. Rust Actix Web mikroservisine gözlemlenebilirlik ekle: OpenTelemetry izleme, Prometheus metrikleri, Grafana panosu ve k6 yük testiyle CI'da SLO kapısı.
### X
**Varsayım:** Actix Web servisi zaten var ve CI GitHub Actions'ta. Kullanılacak skill'ler: `observability-and-instrumentation`, `ecc:rust-testing`.

**F0 · SLO tanımı (~15k)**
- **Adım:** SRE ajanı ve `pln-islevsel-olmayan-gereksinim` ile SLO'lar sayıya bağlanır. Örnek: kritik uçlarda p95 < 200 ms, hata oranı < %1.
- **Tartışma:** eşikler tahminle değil, staging'de ölçülen tabandan çıkarılır.

**F1 · İzleme / tracing (~40k)**
- **Adım:**
  - `tracing`, `tracing-opentelemetry` ve `opentelemetry-otlp` eklenir; middleware olarak `tracing-actix-web` kullanılır.
  - İz yayılımı W3C `traceparent` ile yapılır, örnekleme `ParentBased(TraceIdRatio)` olur.
  - İzler OTLP ile docker compose'daki otel-collector'a, oradan Jaeger'a gider.
- **Araç:**
  - bloklayan çağrı ve hata eşleme denetimi için `dil-actix-web`,
  - span adını route şablonu yapmak için `ops-dagitik-izleme`.
- **Kapı:**
  - `cargo test` ve `clippy -D warnings` geçer.
  - Bir istek atılır; in-memory exporter'da span'ın oluştuğu doğrulanır.
- **İnceleyen:** `ecc:code-reviewer`. Ayrıca `sec-loglama-gizlilik`, span özniteliklerinde kişisel veri ya da token olmadığını denetler.

**F2 · Prometheus metrikleri (~30k)**
- **Adım:**
  - `/metrics` için `actix-web-prom` kullanılır.
  - RED metrikleri eklenir: istek sayacı, süre histogramı ve hata sayısı. Histogramın kovaları SLO eşiği olan 0.2 s'yi içerir.
  - Etiketler yalnız `method`, route şablonu ve status sınıfıdır. Ham path etiket olmaz, böylece kardinalite sınırlı kalır.
  - `/metrics` yalnız iç portta açılır.
- **Araç:** `ops-prometheus` ile kayıt ve uyarı kuralları. Kurallar `promtool check rules` ve `promtool test rules` ile sınanır.
- **Tartışma:** metrikler OTLP ile mi, Prometheus pull ile mi taşınsın? Öneri: metrikler pull, izler OTLP. Böylece tek exporter zinciri olur ve hazır Prometheus araçları kullanılır.

**F3 · Grafana panosu (~25k)**
- **Adım:** pano JSON olarak repo'da tutulur ve provisioning ile yüklenir. İçerik: RED panelleri, hata bütçesi ve exemplar üzerinden ize bağlantı.
- **Araç:** `ops-grafana-pano`.
- **Kapı:** compose ortamında her panelin sorgusu Grafana HTTP API ile çalıştırılır; hiçbiri boş dönmemeli.

**F4 · k6 yük testi ve CI SLO kapısı (~40k)**
- **Adım:**
  - k6 senaryosu yükü kademeli artırır.
  - Eşikler: `http_req_duration: p(95)<200`, `http_req_failed: rate<0.01`. Eşik aşılırsa k6 sıfırdan farklı çıkış kodu verir ve CI işi kırmızı olur.
- **Araç:**
  - senaryo için `qa-yuk-testi`,
  - iş akışı için `git-ci-boru-hatti`; k6 resmi docker imajıyla koşar,
  - CI koşusunu izlemek için `gh run watch`.
- **Kapı:**
  - Bilerek yavaşlatılmış bir dalda kapı kırmızı olmalı (negatif test).
  - main dalında yeşil olmalı.
- **İnceleyen:** SRE ajanı eşiklerin anlamlı olduğunu denetler.
- **Tartışma:** paylaşımlı CI koşucusunda ölçüm gürültülü olur. Eşiğe pay bırakılır, en çok 1 kez tekrar koşulur. Kalıcı kırmızı tekrarla geçirilmez.
- **Tavan:** k6 her koşuda en çok 2 dk sürer; ücretli bulut yük servisi kullanılmaz.
### Y
(Actix Web gözlemlenebilirlik + SLO kapısı)
plan_kur bu işi RUTİN işaretledi, plan kısa tutuldu. Varsayılan SLO: p95 ≤300 ms, hata oranı <%1. Ömer'in başka hedefi varsa yalnız eşik değerleri değişir.

**Faz 1 · Uygulama (20k)**
- İzleme: tracing + tracing-actix-web + opentelemetry-otlp. Span adı yol şablonu olur, ham URL kullanılmaz. Örnekleme ortam değişkeniyle ayarlanır.
- Metrik: actix-web-prom ile `/metrics`. Etiketler yalnız method, route şablonu ve status olur (kardinalite sınırı).
- Araç: Agent dil-actix-web, Agent ops-dagitik-izleme, Agent ops-prometheus.
- Kapı: `cargo test` yeşil. Entegrasyon testi `/metrics` içinde `http_requests_total` görmeli ve traceparent başlığının yayıldığını doğrulamalı.

**Faz 2 · Pano + yük testi (12k)**
- Grafana: RED panosu JSON olarak repoya girer (provisioning). Agent ops-grafana-pano.
- k6: gerçekçi senaryo, 1 dk ısınma ve 3 dk sabit yük. Eşikler betikteki `thresholds` alanında. Agent qa-yuk-testi.

**Faz 3 · CI kapısı (8k)**
- GitHub Actions: servisi derle ve başlat, sonra `k6 run`. Eşik aşılırsa iş kırmızı olur ve birleştirme engellenir. Agent git-ci-boru-hatti.
- Kapı: bilinçli yavaşlatılmış bir dalda CI'ın kırmızı olduğu bir kez görülmeli. gitleaks 0 bulgu.
- İnceleme: Agent ecc:code-reviewer. Konsey yok.
- Kapanış raporu: commit · test · CI · sapmalar.

## 3. Laravel e-ticaret sitesini çok kiracılı SaaS'a dönüştür: kiracı başına veri yalıtımı, Postgres RLS, Paddle abonelik faturası, alt alan adı yönlendirme ve sıfır kesintili migration.
### X
**Varsayımlar:**
- Uygulama zaten Postgres üzerinde. MySQL ise önce ayrı bir taşıma işi gerekir.
- Bugünkü mağaza 1 numaralı kiracı olur.
- Model: tek şema, her tabloda `tenant_id`, üstüne RLS.

**Araç sırası:** önce `departman-veri-db`, ardından `supabase-postgres-best-practices`.

**F0 · Mimari (~30k)**
- **Adım:**
  - `be-coklu-kiraci-veri` ile kiracıya bağlı her şey envanterlenir: tablolar, kuyruk işleri, cache, depolama, oturum, e-posta.
  - Karar `pln-karar-kaydi` ile ADR olarak kaydedilir.
- **İnceleyen:** `sec-tehdit-modelleme`, kiracılar arası veri sızıntısı senaryolarına bakar.
- **Tartışma:** büyük bir kiracıya ayrı veritabanı verilecek mi? Şimdilik hayır; `tenant_id` sayesinde ileride ayırmak mümkün kalır.

**F1 · Kiracı çözümleme (~45k)**
- **Adım:**
  - Rota: `Route::domain('{tenant}.site.com')`. Middleware kiracıyı bulur, bulamazsa 404 döner.
  - Eloquent global scope eklenir; kayıt oluşturulurken `tenant_id` otomatik doldurulur.
  - Kuyruk işleri `tenant_id` taşır; cache anahtarları ve depolama yolları kiracı önekli olur.
  - Oturum çerezi kendi alt alan adıyla sınırlanır, alt alanlar arasında paylaşılmaz.
- **Araç:** `ecc:laravel-patterns`, `ecc:laravel-tdd`.
- **Kapı:**
  - A kiracısı B'nin sipariş id'sini isterse 404 alır.
  - `sec-acik-yonlendirme` ile giriş sonrası yönlendirme yalnız izin listesindeki alt alan adlarına gider.
- **İnceleyen:** `sec-yetkilendirme-matrisi`.

**F2 · Sıfır kesintili migration, expand/contract (~50k)**
Plan `db-migration-planlayici` ile yazılır; her adımın bir geri alma adımı vardır.
1. `tenants` tablosu ve boş geçilebilir `tenant_id` kolonu eklenir.
2. `tenant_id` yazan kod deploy edilir.
3. Mevcut satırlar 5k'lık partilerle 1 numaralı kiracıya doldurulur.
4. İndeksler `CREATE INDEX CONCURRENTLY` ile oluşturulur; bu migration'da `$withinTransaction = false` olur.
5. Önce `CHECK NOT VALID`, sonra `VALIDATE`, ardından `SET NOT NULL` uygulanır. FK de önce `NOT VALID`, sonra `VALIDATE` ile eklenir.

- **Kapı:** önce üretim verisinin yerel kopyasında `lock_timeout` ile prova yapılır. `db-veri-kalitesi` satır sayılarının eşit kaldığını denetler. Üretime yalnız onayla geçilir.
- **İnceleyen:** Database Reliability Engineer.

**F3 · Postgres RLS (~40k)**
- **Adım:**
  - `db-rls-politika` ve `ecc:postgres-patterns` ile tablolarda `ENABLE` ve `FORCE RLS` açılır.
  - Politika `USING` / `WITH CHECK` koşulu: `tenant_id = current_setting('app.tenant_id', true)::bigint`.
  - Uygulama rolü tabloların sahibi olmaz ve `BYPASSRLS` yetkisi taşımaz.
- **Bağlantı:** middleware her işlemde transaction içinde `SET LOCAL` yapar, bu PgBouncer transaction modunda da güvenlidir. Ayar yoksa sorgu 0 satır döner (fail-closed).
- **Sıra:** önce `SET LOCAL` yapan kod deploy edilir, sonra RLS açılır. Geri alma: `DISABLE RLS`.
- **Kapı:**
  - Uygulama rolü ayar olmadan `SELECT` yaparsa 0 satır döner.
  - Başka kiracıya `INSERT` reddedilir.
  - `ecc:laravel-security` denetimi geçer.
- **Tartışma:** global scope ve RLS birlikte mi kalsın? Öneri: evet. Scope hatalı sorguyu erken yakalar, RLS son savunma hattıdır.

**F4 · Paddle abonelik faturası (~45k)**
- **Adım:**
  - `laravel/cashier-paddle` eklenir; `Tenant` modeli Billable olur ve plan özellik sınırlarını belirler.
  - Webhook imzası doğrulanır ve olaylar idempotent işlenir (`otm-webhook-tasarimci`).
  - Ödeme gecikirse kiracı salt okunur moda geçer.
  - Fiyat ve fatura sayfaları UI işidir: `frontend-craft` yüklenir, Section 6 raporu yazılır.
- **Araç:** Payments & Billing Engineer ajanı.
- **Kapı:**
  - Sandbox'ta uçtan uca akış sınanır: abonelik, yenileme, iptal, başarısız ödeme.
  - `sec-kvkk-gdpr-kontrol` ile fatura verisinin saklama süresi denetlenir.
- **Tavan:** sandbox'a en çok 30 çağrı. Canlı Paddle çağrısı yapılmaz; ilk canlı işlem yalnız onayla.

**F5 · Alt alan adı altyapısı ve yayın (~30k)**
- **Adım:**
  - Joker DNS kaydı açılır; alan adı Hostinger'daysa hostinger MCP kullanılır.
  - Joker TLS sertifikası DNS-01 doğrulamasıyla alınır.
  - nginx'te `*.site.com` tanımlanır (`ops-nginx-ters-vekil`).
- **Kapı:**
  - `sec-alt-alan-ele-gecirme`: silinen kiracıların sahipsiz DNS kaydı kalmamalı.
  - Deploy öncesi `ecc:laravel-verification` geçmeli.
- **Sıra:** `departman-surec-git-yayin`, ardından `git-canary-izleme` ile kademeli açılış.
- **İnceleyen:** `inc-uretim-hazirligi`.

---
Katalog araması ilk denemede üç işin çıktısını tek bir dosyaya döktüğü için her işi `--aday 40` ile ayrı ayrı yeniden çalıştırdım. Planlarda katalogda "kurulu değil" görünen hiçbir aracı kullanmadım; itch butler CLI katalogda yok ve bu ortamda kurulu olup olmadığını kontrol etmedim.

Hiçbir planı bir proje üzerinde doğrulamadım; Laravel'in Postgres'te olduğu ve Actix servisinin GitHub Actions'ta koştuğu varsayım.
### Y
(Laravel e-ticaret → çok kiracılı SaaS)
Varsayımlar: veritabanı zaten Postgres (MySQL ise önce ayrı bir taşıma dalgası gerekir, DUR). Paylaşılan şema + `tenant_id` + RLS kullanılır; isteğin kendisi bunu belirtiyor. Mevcut mağaza tenant 1 olur.

**Faz 0 · Hazırlık (6k)**
- Adım: departman-veri-db ve departman-guvenlik skill'lerini aç, dalga.md'yi yaz.
- Araç: Skill supabase-postgres-best-practices; Postgres'e dokunmadan önce zorunlu.

**Faz 1 · Tasarım (18k)**
- Yalıtım modeli ve model envanteri: Agent be-coklu-kiraci-veri. Her tablo için kiracıya ait mi, global mi kararı verilir.
- Kiracı bağlamı: middleware alt alan adından kiracıyı çözer. İstek transaction'ında `SET LOCAL app.tenant_id` ayarlanır (PgBouncer transaction modunda güvenli olan yol budur). Kuyruk işleri tenant_id taşır. Önbellek anahtarları ve depolama yolları kiracı önekli olur.
- RLS tasarımı: Agent db-rls-politika, Skill ecc:postgres-patterns.
  - Uygulama rolü tablo sahibi ya da süper kullanıcı olmaz; `FORCE ROW LEVEL SECURITY` açılır.
  - Benzersiz kısıtlar bileşik olur, örneğin (tenant_id, sku).
- Tartışma noktası (geri dönüşsüz): RLS ihlalinde 0 satır mı dönsün, hata mı fırlatılsın? Öneri: 0 satır dönsün, ayrıca bağlam ayarlanmamışsa middleware hata versin. Veri yoksa ecc:council 1 kez çalışır (~60–90k).
- İnceleme: Agent ecc:code-reviewer.

**Faz 2 · Sıfır kesintili migration (20k)**
- Expand/contract planı: Agent db-migration-planlayici, Agent db-veri-tasima.
  1. Nullable `tenant_id` ekle.
  2. Partiler halinde 1'e doldur.
  3. `CHECK … NOT VALID`, ardından `VALIDATE`, ardından NOT NULL.
  4. `CREATE INDEX CONCURRENTLY` (`$withinTransaction = false`).
  5. RLS politikasını en son aç.
- Kapı: her adımın geri alma adımı var. Önce yerelde ve staging'de denenir. Doldurma sonrası satır sayısı parite %100 olmalı. Üretime ancak onayla geçilir.

**Faz 3 · Uygulama (40k)**
- Alt alan adı yönlendirme: route domain grubu `{tenant}.alan.com`, `SESSION_DOMAIN` ayarı, wildcard DNS ve sertifika. Hostinger MCP kullanılır ama DNS değişikliği onay ister.
- Paddle: Laravel Cashier (Paddle).
  - Webhook imzası doğrulanır; olay kimliğiyle tekil işlenir.
  - Yeniden deneme tavanı 3. Paddle satıcı kayıtlı olduğu için kapsam PCI SAQ-A.
  - Yalnız sandbox kullanılır, en çok 50 sandbox çağrısı.
- Araç: Skill ecc:laravel-patterns, Skill ecc:laravel-tdd, Agent Payments & Billing Engineer, Agent otm-webhook-tasarimci.
- Kapı: önce kırmızı görülen testler yeşile döner.
  - Kiracılar arası sızıntı testi: kiracıya ait her model için A kiracısı B'nin verisini okuyamaz/yazamaz, 0 sızıntı.
  - Bağlamsız sorgu 0 satır döner.
  - Webhook tekrarı çift abonelik oluşturmaz.
- İnceleme: Agent db-rls-politika (politikalar), Agent ecc:code-reviewer.

**Faz 4 · Güvenlik + KVKK (12k)**
- Araç: Skill ecc:laravel-security, Agent ecc:security-reviewer, Agent sec-alt-alan-ele-gecirme (sarkan CNAME), Agent sec-acik-yonlendirme (alt alanlar arası dönüş URL'si), Agent sec-kvkk-gdpr-kontrol (Paddle yurt dışı aktarım, veri işleyen sözleşmesi, kiracı silme/dışa aktarma).
- Kapı: semgrep 0 yüksek, gitleaks 0 bulgu.
- Web arayüzü: LCP ≤2.5 s, CLS ≤0.1, INP ≤200 ms, qa-erisilebilirlik-testi 0 ciddi ihlal. Arayüze dokunulursa önce /frontend-craft yüklenir.

**Faz 5 · Yayın + kapanış (6k)**
- Adım: Skill ecc:laravel-verification. Staging'de iki kiracıyla uçtan uca test. Üretim migration'ı onayla yapılır.
- Kapanış raporu: commit · test · CI · sapmalar.

---
- plan_kur iş 2'yi RUTİN işaretledi, o yüzden iş 2 için aday listesi gelmedi; araçlar listeli olmayan kurulu ajanlardan seçildi. Sıkıştırılmış çıktıyı geri çağırmadım (ek sorgu yasağı); oradaki iş 2 kapı satırları eksik kalmış olabilir.
- Henüz doğrulanmamış varsayımlar: itch.io yükleme aracı butler kurulu değil, iş 3'teki veritabanı zaten Postgres, SLO eşikleri p95 ≤300 ms ve hata <%1. Bunlar yanlışsa planın ilgili fazları değişir.

## 4. Electron masaüstü not uygulamasını Tauri'ye taşı: güvenli IPC, kod imzalama, otomatik güncelleme, yerel SQLite şifreleme ve erişilebilirlik denetimi.
### X
**Varsayımlar:** Tauri v2 kullanılacak. Ön yüz (React/Vue vb.) aynen kalacak, değişen yalnız ana süreç. Hedef Windows ve macOS. Electron sürümünde mevcut, şifresiz bir SQLite veritabanı var.

**F0 · Envanter ve tehdit modeli (15k)**
- Adım: `ipcMain`/`ipcRenderer`, `remote`, `nodeIntegration` ve `fs` kullanımlarını listele. Her çağrıyı bir Rust komutuyla eşle.
- Araç: Agent `Explore` (envanter), Agent `sec-tehdit-modelleme` (STRIDE; güven sınırı WebView ile Rust arası), Agent `pln-bogucu-incir-gocu` (taşıma sırası).
- Kapı: her IPC kanalının bir karşılığı olacak ve eşleme tablosu tam olacak. Eşleşmeyen kanal sıfır.
- İnceleyen: Agent `Desktop App Engineer`.
- Tartışma: tek seferde taşımak mı, Electron'u bir sürüm paralel tutmak mı? Öneri: tek sürüm geçişi, Electron bir sürüm boyunca indirilebilir kalsın.

**F1 · Güvenli IPC (40k)**
- Adım: `#[tauri::command]` komutları yazılacak, argümanlar `serde` ile tiplenecek ve doğrulanacak. Pencere başına izinler `capabilities/*.json` ile en dar haliyle verilecek. `tauri.conf.json` içinde sıkı CSP olacak, `dangerousRemoteDomainIpcAccess` kapalı kalacak, isolation deseni açılacak. `fs` ve `shell` eklentileri yalnız kapsamlı yollarla açılacak.
- Araç: Agent `ara-kutuphane-dokuman` (Tauri v2 izin şeması), Agent `Desktop App Engineer`.
- Kapı: `cargo test` ve `cargo clippy -D warnings` yeşil olacak. Agent `sec-sast-kosucu` (Semgrep) yüksek bulguda sıfır verecek. İzinsiz komut çağrısının reddedildiğini gösteren negatif test olacak.
- İnceleyen: Agent `ecc:security-reviewer`.

**F2 · Şifreli yerel SQLite (40k)**
- Adım: `rusqlite` + `bundled-sqlcipher` kullanılacak. Anahtar ilk açılışta üretilecek ve OS anahtarlığında (`keyring` crate) saklanacak; diskte ya da JS tarafında tutulmayacak. Eski veritabanı bir kerelik `sqlcipher_export` ile taşınacak, düz dosya ancak doğrulamadan sonra silinecek. WAL açık olacak.
- Araç: Agent `db-sqlite`, Agent `sec-sifreleme-denetci`.
- Kapı: taşıma testinde kayıt sayısı ve sağlama toplamı eşit olacak. Şifreli dosya `sqlite3` ile açılamayacak (test). Anahtar kaybı senaryosunun bir hata yolu olacak, veri sessizce sıfırlanmayacak.
- İnceleyen: Agent `ecc:code-reviewer`.
- Tartışma: `tauri-plugin-sql` (sqlx) SQLCipher'ı rahat desteklemez. Öneri: rusqlite ve kendi komutlarımız.

**F3 · Kod imzalama ve otomatik güncelleme (35k)**
- Adım: güncelleme için `tauri-plugin-updater` kullanılacak; minisign anahtar çifti olacak, özel anahtar yalnız CI secret'ında duracak. Windows'ta Authenticode, macOS'ta Developer ID imzası ve notarization yapılacak. Güncelleme manifesti HTTPS üzerinden sunulacak.
- Araç: Agent `git-ci-boru-hatti` (GitHub Actions matrisi), Agent `Secrets & Credential Hygiene Engineer`.
- Kapı: `signtool verify` ve `spctl -a` geçecek. İmzası bozuk güncelleme paketinin reddedildiği test olacak. Agent `sec-gitleaks-gecmis` sıfır sızıntı verecek. Secret değerleri hiçbir yerde basılmayacak.
- İnceleyen: Agent `Desktop App Engineer`.

**F4 · Erişilebilirlik ve uçtan uca (30k)**
- Adım: Skill `frontend-craft` (UI'ya dokunulduğu için zorunlu). Playwright ile dev sunucusunda axe-core çalıştırılacak. WebView2 ve WKWebView'da klavye ile gezinilecek, NVDA ve VoiceOver ile elle tur atılacak.
- Araç: Agent `qa-erisilebilirlik-testi`, Agent `ecc:a11y-architect`, Agent `qa-e2e-playwright`.
- Kapı: axe'de kritik ve ciddi bulgu sıfır olacak. Odak sırası ve görünür odak sağlanacak. frontend-craft Bölüm 6 tur raporu yazılacak.
- İnceleyen: Agent `UI Finish-Gate Reviewer`.

**Toplam:** yaklaşık 160k jeton.
### Y
Zor iş (masaüstü + güvenlik + DB + a11y). İlk adım masaüstü alanına uyan departman-* müdür skill'ini açmak; bu müdürün adı katalog çıktısında yoktu, oturum başında doğrulanmalı. UI'ye dokunduğu için `/frontend-craft` en başta yüklenir.
**F0 Keşif ve kabul ölçütleri** (~8k)
- Electron'un IPC kanallarını (`ipcMain.handle`, preload), `nodeIntegration` ayarlarını ve veri yolunu (userData, mevcut SQLite) çıkar · ara-graphify-sorgu, `jev ilgili` · kapı yok
- Hedefi yaz: özellik eşliği listesi, desteklenen işletim sistemleri, veri göçü (Electron'daki verinin ilk açılışta içe alınması) · pln-kabul-olcutleri, pln-bogucu-incir-gocu
- Tartışma: tek seferde mi taşınacak, yoksa Electron sürümü eşlik sağlanana dek yan yana mı yayınlanacak? Önerim yan yana çalıştırıp eşliği qa-ozellik-paritesi ile ölçmek.
**F1 Tauri v2 iskeleti ve güvenli IPC** (~25k)
- Her IPC kanalı tipli bir `#[tauri::command]` olur; yetki capabilities/permissions ACL ile pencere başına en az izin verilerek tanımlanır, sıkı CSP, `withGlobalTauri` kapalı · Desktop App Engineer, context7 (Tauri v2 dokümanı)
- Dosya ve kabuk eklentilerine kapsam (scope) daraltması · dil-yapilandirma
- Kapı: komut girdileri sınırda doğrulanır, yol geçişi testi (sec-yol-gecisi), `cargo test` ve ön yüz birim testleri yeşil olmalı
- İnceleyen: ecc:security-reviewer ve differential-review (IPC yüzeyindeki fark)
- Tartışma: isolation pattern gerekli mi? Not içeriği HTML olarak işleniyorsa evet.
**F2 Şifreli yerel SQLite** (~20k)
- `rusqlite` + `bundled-sqlcipher`; anahtar `keyring` ile işletim sisteminin anahtar zincirinde saklanır; WAL ve pragma'lar ayarlanır · db-sqlite, sec-sifreleme-denetci
- Göç betiği: düz Electron veritabanı → SQLCipher (`sqlcipher_export`), sayı ve sağlama kontrolüyle; başarılı olana kadar eski dosya silinmez · db-veri-tasima
- Kapı: göç testi önce kırmızı görülür sonra yeşile döner; şifreli dosya `sqlite3` ile açılamamalı; anahtar kaybı senaryosu yazılır
- İnceleyen: sec-sifreleme-denetci
- Tartışma: anahtar zincirine mi bağlanacak, ana parolayla mı? Anahtar zinciri kullanıcıya sürtünme getirmez ama makine taşınırken kurtarma gerekir.
**F3 Kod imzalama ve otomatik güncelleme** (~20k)
- Windows'ta signtool/Authenticode, macOS'ta Developer ID ile imza + notarization; ikisi de CI'da · git-ci-boru-hatti, gh
- `tauri-plugin-updater`: minisign anahtarı imza sertifikasından ayrı tutulur; manifest GitHub Releases'te; önce kanarya kanalı · git-canary-izleme
- Kapı: sırlar yalnız CI secret olarak durur, gitleaks + sec-sir-tarayici temiz çıkmalı; imzasız ya da kurcalanmış paket güncellemede reddedilmeli (negatif test)
- Tavan: notarization her sürümde en çok 5 gönderim. Sertifika ücreti Ömer'in onayına bağlı.
- İnceleyen: Secrets & Credential Hygiene Engineer
**F4 Erişilebilirlik denetimi** (~18k)
- Önce `frontend-craft` (öncelik kuralı), sonra fixing-accessibility ve interfaces:better-accessibility
- playwright-cli ile dev sunucusunda axe taraması, klavye turu, ekran okuyucu (NVDA/VoiceOver) kontrol listesi · qa-erisilebilirlik-testi, chrome-devtools-mcp:a11y-debugging
- Kapı: WCAG 2.2 AA'da axe hatası 0; odak sırası ve kontrast; WebView2/WKWebView farkları elle kontrol edilir
- İnceleyen: ecc:a11y-architect. Kapanışta frontend-craft Bölüm 6 tur raporu verilir.
**F5 Kapanış** (~8k): uçtan uca kontrol gerçek uygulamada (kur → göç → güncelleme), parite skoru, ≤15 satır kapanış raporu.

## 5. ESP32 sıcaklık sensörlerinden MQTT ile veri topla: TimescaleDB'ye yaz, anomali tespiti, Grafana uyarıları ve aşamalı OTA firmware güncellemesi.
### X
Zor iş (gömülü + veri + ML + ops). Plan departman-veri-db müdür skill'i ile açılır. Donanım kalibrasyonu kesinlikle atlanmaz.
**F0 Mimari ve kabul ölçütleri** (~10k)
- Veri akışı: ESP32 → MQTT/TLS → broker → ingest → TimescaleDB → Grafana · pln-mimari-plan, IoT Fleet Engineer
- Ölçülebilir hedefler: örnekleme aralığı, kabul edilebilir veri kaybı, uyarı gecikmesi (p95), cihaz sayısı · pln-islevsel-olmayan-gereksinim
- KVKK ön elemesi (konum ya da kişi bağı var mı) · use-case-triage; bağ varsa pia-generation
- Tartışma: broker Mosquitto mu EMQX mi? Önerim, küçük filo için ACL'li Mosquitto.
**F1 Firmware: ölçüm ve yayın** (~25k)
- ESP-IDF + esp-mqtt; konu şeması `site/{s}/dev/{id}/temp`; QoS1, LWT, çevrimdışı tampon (RTC/NVS) · Embedded Firmware Engineer, ops-mqtt, context7
- Sensör ofset/kalibrasyonu NVS'de tutulur; ölçüm referans termometreyle doğrulanır
- Cihaz başına mTLS sertifikası; broker ACL'i cihazı yalnız kendi konusuyla sınırlar · sec-tehdit-modelleme
- Kapı: birim testleri (Unity/`idf.py`), uzun süreli bağlantı kopma/yeniden bağlanma testi, kalibrasyon sapması ±0,5 °C içinde
- İnceleyen: mukul975-firmware-security-paket ve ecc:security-reviewer
**F2 Ingest ve TimescaleDB** (~20k)
- Hypertable `(time timestamptz, device_id, temp)`, sıkıştırma, saklama süresi ve continuous aggregate (1 dk/1 sa) · departman-veri-db, db-zaman-damgasi, db-sema-tasarim
- Ingest servisi (Python asyncio MQTT istemcisi) toplu ve idempotent yazar (`ON CONFLICT`) · be-mesaj-guvenilirligi, dil-asyncio
- Kapı: testcontainers ile entegrasyon testi (qa-entegrasyon-testi), aralık dışı/çift veri kontrolü (db-veri-kalitesi), k6/MQTT ile yük testi hedef cihaz sayısının ×3'üyle (qa-yuk-testi)
- İnceleyen: Database Optimizer
- Tartışma: Telegraf mı, özel servis mi? Doğrulama ve idempotent yazma gerekiyorsa özel servis.
**F3 Anomali tespiti** (~15k)
- Taban yöntem: SQL'de kayan medyan + MAD/z-skor; ek olarak "sensör sustu" ve "donmuş değer" kuralları · ml-zaman-serisi, ml-veri-bilimci
- Kapı: etiketli geçmiş veride geriye dönük test, yanlış alarm oranı hedefin altında kalmalı; ml-veri-sizintisi kontrolü
- Tartışma: ML modeli mi, istatistik eşiği mi? Önerim istatistik ile başlamak; model ancak eşik yetersiz kalırsa.
**F4 Grafana pano ve uyarılar** (~12k)
- Cihaz değişkenli pano, uyarı kuralları ve contact point; susturma/gruplama ile gürültü azaltma · ops-grafana-pano, otm-bildirim-yonlendirme
- Kapı: sentetik anomali basılır, uyarının hedef sürede düştüğü görülmeli; provisioning dosyaları git'te durur
**F5 Aşamalı OTA** (~22k)
- `esp_https_ota`, çift OTA bölümü, `APP_ROLLBACK_ENABLE` (sağlık kontrolü geçmezse geri döner), Secure Boot v2 ile imzalı imaj · Embedded Firmware Engineer
- Halkalar: test cihazı → %10 → %100; her halka arasında sağlık kapısı (bağlantı, ölçüm, sürüm raporu) · IoT Fleet Engineer, git-canary-izleme
- Kapı: kasıtlı bozuk imajla geri dönüş testi, imzasız imajın reddedildiği görülmeli, imaj sunucusunda sır taraması (gitleaks)
- İnceleyen: Security Architect
- Tartışma: OTA komutu MQTT üzerinden mi, cihazın kendi çektiği bir manifestle mi? Önerim manifest; MQTT yalnız tetik.
**F6 Kapanış** (~8k): uçtan uca kontrol (gerçek cihaz → pano → uyarı → OTA geri dönüşü), runbook (dok-runbook), ≤15 satır kapanış rapor.

---
Hiçbir dosya yazılmadı ya da değiştirilmedi. Katalog bir kez çağrıldı (iki iş tek Bash'te); ilk deneme Windows yol kaçışı yüzünden dosyayı bulamadı, aynı çağrıyı ileri eğik çizgilerle tekrarladım. Katalogda "kurulu değil" görünen araçlar (Tiger Data MCP, lighthouse, agent-desktop) plana konmadı.

İş 4'ün masaüstü müdür skill adı katalogda çıkmadı, oturumda doğrulanmalı. Ücretli adımlar sadece kod imzalama sertifikası ve Apple hesabı; ikisi de Ömer'in onayına bağlı.
### Y
**Varsayımlar:** ESP-IDF (PlatformIO üzerinden) kullanılacak. Broker Mosquitto, sunucu tek VPS üzerinde docker compose. Cihaz sayısı 100'ün altında.

**F0 · Mimari ve konu sözleşmesi (15k)**
- Adım: konu yapısı `site/{s}/dev/{id}/temp` olacak. Ölçümler QoS1 ile gidecek. Durum mesajı retained olacak ve LWT ile birlikte kullanılacak. Yük `{ts, seq, c, fw}` biçiminde olacak.
- Araç: Agent `ops-mqtt`, Agent `IoT Fleet Engineer`, Agent `sec-tehdit-modelleme`.
- Kapı: sözleşme dokümanı ve JSON Schema hazır olacak.
- İnceleyen: Agent `pln-mimari-plan`.
- Tartışma: alım katmanı Telegraf mı, küçük bir Python servisi mi? Öneri: Telegraf, çünkü kod gerektirmiyor. Tekilleştirme ve doğrulama için özel ihtiyaç çıkarsa Python servisine geçilir.

**F1 · Firmware: ölçüm ve yayın (40k)**
- Adım: zaman SNTP ile alınacak. Sensöre özel ofset kalibrasyonu yapılacak. Ağ koptuğunda ölçümler RAM halka tamponunda tutulup sonra gönderilecek. TLS ve cihaz başına kimlik bilgisi kullanılacak.
- Araç: Agent `Embedded Firmware Engineer`, `pio test` (Unity).
- Kapı: birim testleri yeşil olacak. Masadaki cihazda 24 saatlik koşuda kayıp %0,1'in altında kalacak. Kalibrasyon referans termometreyle ±0,5 °C içinde olacak.
- İnceleyen: Agent `ecc:code-reviewer`.

**F2 · Broker, alım ve TimescaleDB (35k)**
- Adım: Mosquitto'da anonim erişim kapalı olacak, ACL ile her cihaz yalnız kendi konusuna yazabilecek. Ölçümler hypertable'a gidecek, `UNIQUE(device_id, ts)` ve `ON CONFLICT DO NOTHING` ile tekilleştirilecek. Sıkıştırma ve saklama politikaları kurulacak, 1 dakika ve 1 saatlik sürekli kümeler (continuous aggregate) tanımlanacak.
- Araç: Agent `Database Optimizer`, Agent `db-zaman-damgasi` (UTC), Agent `db-indeks-danismani`.
- Kapı: docker compose ile entegrasyon testi yapılacak (Agent `qa-entegrasyon-testi`). Yinelenen mesaj tek satır olarak yazılacak. Yabancı konuya yayın ACL tarafından reddedilecek.
- İnceleyen: Agent `Database Reliability Engineer`.

**F3 · Anomali tespiti ve Grafana uyarıları (35k)**
- Adım: SQL ile dört kural tanımlanacak: fiziksel sınır, değişim hızı, kayan medyan/MAD z-skoru (>4) ve 10 dakikadan uzun veri gelmeyen sensör. Grafana'da pano ve SQL tabanlı uyarı kuralları olacak; bekleme süresi (`for`) ve sessize alma tanımlanacak.
- Araç: Agent `ml-zaman-serisi`, Agent `ops-grafana-pano`, Agent `otm-bildirim-yonlendirme`.
- Kapı: sentetik enjeksiyon testinde tespit oranı en az %95, sakin bir haftalık veride yanlış alarm günde 1'in altında olacak.
- İnceleyen: Agent `SRE (Site Reliability Engineer)`.
- Tartışma: ML modeli mi, istatistiksel kurallar mı? Öneri: başlangıçta kurallar. ML ancak yanlış alarm hedefi tutmazsa gündeme gelir.

**F4 · Aşamalı OTA (45k)**
- Adım: iki OTA bölümü ve `esp_https_ota` kullanılacak. Bootloader rollback açık olacak; yeni imaj sağlık kontrolünü (MQTT bağlantısı ve geçerli ölçüm) geçerse `mark_app_valid` çağrılacak. İmajlar imzalı olacak (Secure Boot v2 ya da imza doğrulama), imza anahtarı çevrimdışı tutulacak. Grup başına retained manifest `{ver, url, sha256}` yayınlanacak. Dağıtım halkaları: 1 cihaz → %10 → %50 → %100.
- Araç: Agent `IoT Fleet Engineer`, Agent `Embedded Firmware Engineer`, Agent `git-canary-izleme`.
- Kapı: masada bozuk imaj testi yapılacak ve cihazın otomatik geri döndüğü görülecek. Bir halkada rollback ya da kayıp kalp atışı %2'yi aşarsa dağıtım durdurulacak. SHA eşleşmezse imaj reddedilecek.
- İnceleyen: Agent `ecc:security-reviewer`.
- KVKK: sıcaklık verisi tek başına kişisel veri değil. Cihaz bir kişinin odasına ya da evine bağlanırsa Agent `sec-kvkk-gdpr-kontrol` devreye girer.

**Toplam:** yaklaşık 170k jeton.

---
Atladıklarım: departman-* yönetici skill adlarını doğrulamadım, plan araç adları yalnız oturumdaki ajan listesine dayanıyor. Bilinmesi gereken risk: `plan_kur.py` zor işleri RUTİN saydığı için PLAN-KUR-3 ölçümünü bozabilir; sınıflandırıcı kontrol edilmeli.

## 6. YouTube kanalı için otomatik kısa video hattı kur: uzun videonun transkriptinden öne çıkan anları seç, ffmpeg ile dikey kırp, altyazı göm, Remotion ile başlık animasyonu ekle.
### X
**Varsayım:** Kaynak videolar kanalın kendisine ait. YouTube'a otomatik yükleme kapsam dışı; çıktı `out/<video_id>/*.mp4` olur. Ekran kuralı geçerli: tüm render işleri headless çalışır, studio önizleme penceresi açılmaz.
- **F0 Brief (5k):** Shorts biçimi, kanca ve 15–60 sn süre aralığı belirlenir · Skill youtube-agent:yt-shorts, Skill reel-plan · kapı: klip sayısı, süre ve güvenli alan (alt %20 boş) yazılı · inceleyen: —
- **F1 Girdi (4k):** Video ve altyazı `yt-dlp` ile indirilir (Bash). Altyazı yoksa Skill watch (whisper) kullanılır. İndirilenler ayrı ve boş bir klasöre konur, güvenilmeyen veri sayılır · kapı: 429 hatası "altyazı yok" sayılmaz; beklenip en çok 3 kez yeniden denenir · inceleyen: ecc:code-reviewer
- **F2 An seçimi (6k):** Agent vid-kisa-klip-secici transkripti okuyup `klipler.json` üretir (start, end, kanca, puan). Başlık metnini Agent urn-baslik-yazimi yazar · kapı: pytest ile şema testi, süre 15–60 sn, klipler çakışmaz. LLM kullanılırsa video başına en çok 1 çağrı, koşu başına en çok 10 video · inceleyen: ecc:code-reviewer
- **F3 Dikey kırpma ve altyazı (8k):** Agent vid-ffmpeg-donusturucu kullanılır. `ffmpeg` önce `crop=ih*9/16:ih`, sonra `scale=1080:1920` uygular. Altyazı ASS dosyasından `subtitles` filtresiyle gömülür; ses −14 LUFS'a çekilir · kapı: ffprobe 1080×1920 doğrular, süre sapması ≤0,1 sn. Agent vid-kare-cikarici 3 kare alır; altyazı kayması ≤150 ms olmalı ve altyazı güvenli alanda kalmalı. Skill accessible-content:multimedia-accessibility ile altyazı kontrastı ≥4.5:1 · inceleyen: ecc:code-reviewer
- **Tartışma (F3):** Altyazıyı `ffmpeg` mi gömer, Skill remotion-captions mı (tek render geçişi)? Öneri: `ffmpeg`, çünkü iş tanımı bunu istiyor ve bu yol geri alınabilir. Konsey gerekmez.
  - **Kısayol:** Kırpma merkezden yapılır. Konuşmacı karenin ortasında değilse yüz takibine geçilir.
- **F4 Başlık animasyonu (8k):** Skill ecc:remotion-video-creation ve Agent vid-remotion-kurucu ile bir kompozisyon kurulur. Klip arka planda oynar, başlık ilk 2 sn içinde girip çıkar. Render Skill remotion-render ile headless yapılır · kapı: render çıkış kodu 0. Skill inclusive-interaction:motion-sensitivity ile saniyede en çok 3 parlama; başlık güvenli alanda kalır · inceleyen: ecc:code-reviewer
- **F5 Hat ve kapanış (6k):** `shorts_hat.py` tek betik olur: indir → seç → kırp → render. Video kimliğine göre önbellek tutar, `--dry-run` seçeneği vardır. Alt süreçler liste argümanla çağrılır (`shell=True` yok) · kapı: pytest 10 sn'lik örnek videoyla uçtan uca yeşil, semgrep 0 yüksek, gitleaks 0 bulgu · inceleyen: ecc:security-reviewer (başlık/dosya adı enjeksiyonu, indirilen dosyanın yolu)
- **Kapanış:** commit · test sayısı · CI · sapma, en çok 15 satır.
- **Bütçe:** ≈37k (brief 5k · üretim 26k · kontrol 6k). Konsey yok.
### Y
**Varsayım:** Hat kendi kanalının videolarını işler. Çıktı yayına hazır dikey klip olur, YouTube'a yükleme ayrıca onaylanır. Arka plan işleri yalnız `.kos/kopru/arka.py` üzerinden koşar; studio penceresi açılmaz, render headless yapılır.

**F0 · Karar ve lisans (8k)**
- Adım: hedef (30–60 sn, 1080×1920, haftalık adet) · araç: `vid-video-brief` ajanı, `reel-plan` skill.
- Lisans: `ara-lisans-kontrol` ajanı. Öğrenim 88'e göre remotion-video-paket hattı en çok 3 çalışanlı kâr amaçlı şirkette ücretsiz; ffmpeg build lisansı (GPL/LGPL) da yazılır.
- **Tartışma:** başlık katmanı için `vid-remotion-kurucu` mu `hyperframes:hyperframes` (HTML/GSAP) mı? Lisans koşulu tutmazsa hyperframes seçilir. Karar `pln-karar-kaydi` ile kaydedilir.

**F1 · Girdi ve transkript (10k)**
- Adım: video ve altyazı indirilir (`--write-subs`, kelime zaman damgası) · araç: `vid-ytdlp-indirme` ajanı, `yt-dlp` CLI.
- Altyazı yoksa yerel `whisper-cli` kullanılır. 429 hatasında "altyazı yok" denmez, beklenip yeniden denenir (öğrenim 87).
- Kapı: pytest; zaman damgaları artan sırada, boş segment yok.

**F2 · Öne çıkan an seçimi (15k)**
- Adım: transkriptten `clips.json` üretilir (start, end, hook, başlık) · araç: `vid-kisa-klip-secici` ajanı, `youtube-agent:yt-shorts`.
- LLM sıralaması `claude -p` ile yapılır, **video başına en çok 1 çağrı**.
- Kapı: `otm-sema-dogrulayici` ile JSON Schema denetimi. `qa-ozellik-tabanli` ile property testi: klip 15–60 sn, klipler çakışmaz, kesimler cümle sınırına düşer.

**F3 · Dikey kırpma ve altyazı gömme (15k)**
- Adım: ffmpeg `crop=ih*9/16:ih` ile ortadan kırpar, ASS altyazıyı `subtitles=` ile gömer · araç: `vid-ffmpeg-donusturucu` ve `vid-sosyal-video-bicim` ajanları (güvenli alan).
- shortcut: kırpma ortadan yapılır, yüz takibi yok. Konuşmacı kenarda kalırsa yükseltilir.
- Ses `loudnorm` ile −14 LUFS'a çekilir (`vid-ses-duzeni`), renk bt709'da tutulur (`vid-renk-uzayi`).
- Kapı: `ffprobe` ile 1080×1920 ve süre ±0,1 sn kontrolü. Erişilebilirlik için `accessible-content:multimedia-accessibility`: altyazı kontrastı, punto, güvenli alan.

**F4 · Başlık animasyonu (15k)**
- Adım: kırpılmış klip üstüne ilk 2 sn başlık katmanı · araç: `vid-remotion-kurucu` ajanı, `ecc:remotion-video-creation`, `vid-hareket-grafigi`.
- Render `remotion-render` ile CLI'dan headless alınır, `remotion-studio` kullanılmaz.
- Kapı: `inclusive-interaction:motion-sensitivity`, saniyede 3'ten az yanıp sönme. Props için vitest. 1 klip render duman testi yapılır, `vid-kare-cikarici` ile 3 kare gözle kontrol edilir.

**F5 · Hattın birleştirilmesi (12k)**
- Adım: tek komut çalışır (url → `shorts/*.mp4` + açıklama metni). Klip hash'i varsa o klip atlanır (idempotent) · araç: python betiği, metin için `youtube-agent:yt-seo`.
- Kapı: `ecc:security-reviewer`. subprocess argümanları liste olarak verilir, `shell=True` yok; yol geçişi `sec-yol-gecisi` ile denetlenir. Videoda konuk varsa `sec-kvkk-gdpr-kontrol` ile açık rıza aranır.
- İnceleyen: `ecc:code-reviewer` ve `inc-ponytail-kod`.
- **Tartışma:** otomatik yükleme dışa dönük bir adım. Ömer onaylarsa **günde en çok N yükleme** tavanı konur.

**Toplam ≈75k**

## 7. Astro ile iki dilli (TR/EN) teknik dokümantasyon sitesi kur: içerik koleksiyonları, Pagefind arama, SEO meta etiketleri, erişilebilirlik testi ve GitHub Actions ile yayın.
### X
**Varsayım:** Yayın GitHub Pages'e yapılır, varsayılan dil TR. İlk deploy ve push dışa açık iş olduğu için önce onay alınır. Arayüze dokunduğu için iş Skill frontend-craft ile başlar; süreç sahibi Skill departman-surec-git-yayin.
- **F0 Tasarım (15k):** Agent pln-teknik-spec URL şemasını (`/tr/…`, `/en/…`), `translationKey` eşlemesini ve çevirisi eksik sayfadaki davranışı yazar · kapı: kabul ölçütleri yazılı · inceleyen: —
- **Tartışma (F0):** Hazır resmi doküman teması mı, düz Astro mu? Hazır tema Pagefind ve i18n'i kendi getirir ama özelleştirmeyi kısıtlar. Öneri: düz Astro, çünkü iş Pagefind'ı ayrı bir adım olarak istiyor. Geri alınabilir, konsey gerekmez.
- **F1 İskelet ve içerik (20k):** Agent fe-astro i18n yönlendirmesini, `src/content.config.ts` dosyasını (glob loader + zod şeması: title, description, lang, translationKey), düzeni ve dil değiştiriciyi kurar. EN metinleri Agent dok-cevirmen-teknik ortak terim sözlüğüyle çevirir · kapı: `astro check` 0 hata. Parite testi: her TR sayfanın EN karşılığı var ya da "çeviri yok" uyarısı gösteriliyor · inceleyen: ecc:code-reviewer
- **F2 Arama (8k):** Build sonrası `npx pagefind --site dist` çalışır. `<main data-pagefind-body>` işaretlenir; her sayfada `<html lang>` doğru olduğu için dizin dile göre ayrılır · kapı: Agent qa-playwright testi, TR sorgusu yalnız TR, EN sorgusu yalnız EN sonuç döndürür · inceleyen: ecc:code-reviewer
- **F3 SEO (10k):** Agent fe-meta-seo-duzeltici ve Skill ecc:seo sayfa başına title, description, canonical, hreflang (tr/en/x-default), OG etiketleri, i18n'li sitemap ve robots.txt ekler · kapı: Skill marketing-skills:seo-audit çalışır. Betik kontrolü: her sayfada tek canonical, hreflang çiftleri karşılıklı, başlıklar tekil · inceleyen: ecc:code-reviewer
- **F4 Erişilebilirlik ve performans (12k):** Agent qa-erisilebilirlik-testi iki dilde tüm sayfalarda axe ve klavye turu yapar (skip link, odak, `lang`) · kapı: 0 ciddi ihlal, LCP ≤2.5 s, CLS ≤0.1, INP ≤200 ms, ilk yükte JS ≤170 KB gz · inceleyen: Agent ecc:a11y-architect
- **F5 CI ve yayın (10k):** Agent git-ci-boru-hatti iş akışını yazar: build → parite, Playwright ve axe testleri → PR'da artefakt önizlemesi → main'de `actions/deploy-pages`. Skill gha-security-review uygulanır: action'lar SHA ile sabitlenir, izinler en az olur (`pages: write`, `id-token: write`). Sonuç `gh run watch` ile izlenir · kapı: önce staging/önizleme, sonra sağlık kontrolü. Geri alma önceki başarılı deploy'un yeniden koşturulmasıdır, ≤5 dk sürer ve README'de yazılı. Ayrıca npm audit 0 yüksek, semgrep 0 yüksek, gitleaks 0 bulgu · inceleyen: ecc:security-reviewer (iş akışı izinleri)
- **Kapanış (3k):** frontend-craft Bölüm 6 tur raporu, ardından commit · test sayısı · CI · sapma, en çok 15 satır.
- **Bütçe:** ≈78k. Konsey yok.

Hiçbir şey yazılmadı ya da çalıştırılmadı; tek komut `plan_kur.py` oldu. Her iki planı da kapsam dışında bıraktıklarım:
- **6. iş:** Yüz takibi ve otomatik yükleme.
- **7. iş:** Hazır doküman teması önerilmedi. Önizleme Pages'te PR başına ayrı URL ile değil, indirilebilir artefakt olarak var.
### Y
**Varsayım:** Yayın GitHub Pages'e yapılır. Kök dil TR, EN sayfaları `/en/` altında durur. UI işi olduğu için önce `frontend-craft` yüklenir; iş Section 6 tur raporu olmadan kapanmaz.

**F0 · Karar (6k)**
- Adım: yığın ve URL şeması · araç: `departman-surec-git-yayin`, `frontend-craft`, güncel doküman için `context7` MCP.
- **Tartışma:** Starlight (Astro'nun doküman teması; i18n, Pagefind ve hreflang hazır gelir, MIT) mı, çıplak Astro mı? Öneri Starlight, çünkü daha az kod yazılır. Pages proje yolunun `base` değeri burada kesinleşir.

**F1 · İskelet (10k)**
- Adım: starlight şablonuyla kurulum, `locales: {root: tr, en}` · araç: `fe-astro` ajanı, npm.
- Kapı: `astro check` ve `astro build` yeşil.

**F2 · İçerik koleksiyonları ve çeviri (15k)**
- Adım: `content.config.ts` içinde zod şeması, terim sözlüğü · araç: `fe-astro`, `dok-cevirmen-teknik` ajanı.
- Kapı: vitest. Her TR sayfanın EN karşılığı vardır ya da bilinçli eksikler listesindedir. Frontmatter şemaya uyar.

**F3 · Pagefind arama (5k)**
- Adım: Starlight'ın yerleşik Pagefind'i kullanılır; `html lang` doğru olursa her dile ayrı indeks çıkar · araç: `qa-playwright` ajanı.
- Kapı: Playwright e2e. TR sayfada "kurulum" araması TR sonuç, EN sayfada EN sonuç döndürür.

**F4 · SEO (8k)**
- Adım: `site` ayarı, `@astrojs/sitemap`, canonical, og/twitter meta, robots.txt · araç: `ecc:seo` skill, `fe-meta-seo-duzeltici`.
- Kapı: `dist` HTML'ini tarayan bir node testi. Her sayfada title, description, canonical ve hreflang tr/en/x-default bulunur.
- İnceleyen: `ecc:seo-specialist`.

**F5 · Erişilebilirlik (10k)**
- Adım: sitemap'teki tüm sayfalar taranır · araç: `qa-erisilebilirlik-testi` ajanı, `@axe-core/playwright`, `web-design-guidelines`.
- Kapı: WCAG 2.2 AA'da serious/critical bulgu 0. Klavye turunda skip link çalışır, arama modalı odağı içinde tutar ve Esc ile kapanır.
- İnceleyen: `ecc:a11y-architect`. Bu fazda frontend-craft Section 6 raporu yazılır.

**F6 · CI ve yayın (10k)**
- Adım: PR'da build, check, vitest ve Playwright+axe koşar. main'de `withastro/action` ve `actions/deploy-pages` çalışır. İzinler en düşükte tutulur (`pages: write`, `id-token: write`), action'lar SHA'ya pinlenir · araç: `git-ci-boru-hatti` ajanı, `gh` CLI.
- Kapı: `gha-security-review`. Gerekli kontroller `git-dal-koruma-kurali` ile zorunlu yapılır.
- İnceleyen: `octo:personas:deployment-engineer` ve `ecc:code-reviewer`.
- Pages'i açmak ve push etmek dışa dönük adım, önce onay alınır.
- **Tartışma:** analitik olmazsa çerez bandı gerekmez (KVKK). Analitik eklenirse `sec-kvkk-gdpr-kontrol` devreye girer.

**Toplam ≈64k**

---
Hiçbir işi yürütmedim ve dosya yazmadım. İki iş birlikte kataloğa sorulunca çıktı dosyaya düştü; kuralınız gereği ikisini ayrı ayrı `--aday 40` ile yeniden çalıştırdım. Katalogda video için bir `departman-*` müdür skill'i çıkmadı, bu yüzden 6. işin F0'ında listeden doğrulanmalı.

Kurulu olmayan katalog kayıtlarını (lighthouse, HeyGen, OpenCut vb.) planlara yazmadım. Starlight, Pagefind ve axe katalogda yok, npm paketi olarak önerdim.

## 8. Yavaş çalışan bir Python betiğini cProfile ile profille ve en sıcak noktayı düzelt.
### X
**F1 Ölçüm** (~3k): Betik gerçekçi girdiyle `python -m cProfile -o prof.out betik.py` ile koşulur. `pstats` ile cumtime ve tottime'a göre ilk 15 satıra bakılır. Ham çıktıyı alt ajan **dil-python-profil** (sonnet) okur ve ana bağlama yalnızca en sıcak 3 fonksiyon gelir.
- Kapı: Duvar saati süresi `time.perf_counter` ile 3 koşuda ölçülür ve medyan taban olarak kaydedilir.

**F2 Düzeltme** (~4k): Önce mevcut çıktıyı sabitleyen bir pytest yazılır (altın dosya ya da assert) ve yeşil olduğu görülür. Sonra yalnızca en sıcak nokta düzeltilir: döngü içi tekrar işi, list yerine set/dict araması, `functools.lru_cache`, toplu I/O gibi. Yeni bağımlılık eklenmez.
- Kapı: pytest yeşil olmalı, yeniden profilde süre tabana göre ölçülebilir biçimde düşmeli ve çıktı birebir aynı kalmalı.
- İnceleme: **ecc:code-reviewer**.
- Tartışma noktası: Darboğaz algoritmik değil de I/O ya da GIL kaynaklıysa paralelleştirmeye geçilmez. Durum DUR raporu olarak sunulur.
### Y
**F1 Ölçüm (≈5k):** Önce temsilî bir girdiyle temel süreyi al: `python -m cProfile -o prof.out betik.py`. Ardından `pstats` ile `sort_stats("cumulative").print_stats(15)` ve `tottime` sıralamasına bak. · Alt ajan `dil-python-profil` (sonnet), yalnız ilk 5 sıcak fonksiyonun özetini döner. · Kapı: ölçüm 3 kez tekrarlanır, sapma %10'dan küçük olmalı.
**F2 Düzeltme (≈8k):** Önce sıcak noktayı kilitleyen bir çıktı-eşitlik testi yazılır (pytest, mevcut çıktıyla birebir karşılaştırma) ve yeşil görülür. Sonra yalnız en sıcak fonksiyona en küçük değişiklik yapılır: döngü içi tekrar işi dışarı almak, `list`→`set`/`dict` araması, `functools.lru_cache` gibi. · Ana oturumda yapılır. · Tartışma noktası: algoritma değişikliği mi, önbellek mi? Önbellek bellek ve geçersizleştirme riski getirir, bu yüzden girdi saf değilse seçilmez.
**F3 Doğrulama (≈3k):** cProfile yeniden koşulur ve hedef düşüş en az %30'dur. Eşitlik testi yeşil olmalı. · İnceleyen: `ecc:code-reviewer`.
**Toplam ≈16k.**

## 9. Postgres'te yavaş bir raporlama sorgusunun EXPLAIN ANALYZE çıktısını oku ve uygun indeksi öner.
### X
**F1 Okuma** (~3k): `EXPLAIN (ANALYZE, BUFFERS)` çıktısında şunlara bakılır: tahmini ve gerçek satır sayısı farkı, en pahalı düğüm (Seq Scan, Sort ya da Hash'in diske taşması), filtrede elenen satırlar. Gerekirse `pg_stat_statements` ile sorgunun sıklığı doğrulanır. Okumayı alt ajan **db-sorgu-optimize** yapar.
- Kapı: Tahmin ile gerçek arasında büyük sapma varsa indeksten önce `ANALYZE` koşulur ve istatistikler tazelenir.

**F2 Öneri** (~3k): **db-indeks-danismani** ile indeks seçilir. Sütun sırası eşitlik → aralık → sıralama olur. Gerekirse kısmi indeks (`WHERE`) ya da `INCLUDE` ile kapsayan indeks kullanılır. Mevcut indekslerle çakışma `pg_indexes` üzerinden kontrol edilir.
- Kapı: İndeks önce staging'de ya da bir kopyada `CREATE INDEX CONCURRENTLY` ile kurulur. Ardından EXPLAIN tekrar koşulur; plan değişmeli ve süre düşmeli. Yazma yükü maliyeti not edilir.
- İnceleme: **Database Optimizer**.
- Tartışma noktası: Raporlama sorgusu yük altındaki bir tabloda çalışıyorsa materialized view ya da read replica indeksten daha uygun olabilir. Bu karar Ömer'e bırakılır, production'a dokunulmaz.
### Y
**F1 Okuma (≈5k):** Sorgu `EXPLAIN (ANALYZE, BUFFERS)` ile staging ya da salt-okur replikada koşulur (`psql`). Plan en fazla 1 kez koşulur, çünkü üretim yükü oluşturur. Bakılacaklar: Seq Scan, tahmin ile gerçek satır farkının 10 katı aşıp aşmadığı, Sort/Hash'in diske taşması. Tahmin farkı büyükse önce `ANALYZE tablo` çalıştırılır. · Alt ajan: `db-sorgu-optimize`.
**F2 İndeks önerisi (≈6k):** Erişim desenine göre bileşik indeks önerilir: sütun sırası eşitlik → aralık → sıralama. Gerekirse kısmi indeks ya da `INCLUDE` ile kapsayan indeks kullanılır. Mevcut indekslerle çakışma `pg_indexes` ve `pg_stat_user_indexes` ile kontrol edilir. · Alt ajan: `db-indeks-danismani`. · Tartışma noktası: yazma maliyeti ve disk büyümesi okuma kazancına değer mi? Tablo yazma ağırlıklıysa materialized view alternatifi tartılır.
**F3 Kanıt (≈4k):** İndeks staging'de `CREATE INDEX CONCURRENTLY` ile kurulur ve EXPLAIN ANALYZE tekrarlanır. Kapı: süre en az 5 kat düşmeli ve yeni planda Index/Index Only Scan görünmeli. Üretime geçiş migration dosyasıyla yapılır, kilitlenmemesi için `CONCURRENTLY` zorunludur. · İnceleyen: `ecc:code-reviewer` (migration).
**Toplam ≈15k.**

## 10. Bir React bileşenindeki gereksiz yeniden render'ları bul ve düzelt.
### X
**F0** (~1k): Kural gereği önce `/frontend-craft` yüklenir.

**F1 Tespit** (~3k): React DevTools Profiler'da "why did this render" açık olarak gereksiz renderlar kaydedilir. Alt ajan **fe-react-bilesen-inceleme** şu nedenleri arar: her renderda yeniden oluşan obje veya fonksiyon prop'ları, geniş context, üst bileşendeki gereksiz state.
- Kapı: Mevcut render sayısı Vitest + RTL ile bir sayaç testine sabitlenir ve testin kırmızı yandığı görülür.

**F2 Düzeltme** (~4k): Önce kök neden giderilir: state aşağı taşınır ya da context bölünür. Bu yetmezse `React.memo`, `useCallback` ve `useMemo` yalnızca ölçülen noktada eklenir. React Compiler açıksa elle memo eklenmez.
- Kapı: Sayaç testi yeşil olmalı, `eslint-plugin-react-hooks` (exhaustive-deps) temiz geçmeli, Profiler'da render sayısı düşmeli. Görünüm değişmediği için erişilebilirlikte fark beklenmiyor; Section 6 tur raporu yazılır.
- İnceleme: **ecc:code-reviewer**.

Kontrol edilmeyenler: departman-* yönetici skill adları ve projede why-did-you-render ya da React Compiler olup olmadığı doğrulanmadı. Planlar gerçek kodu görmeden yazıldı.
### Y
**F1 Tespit (≈6k):** React DevTools Profiler'da "Highlight updates" ve "Why did this render" açılır, yavaş etkileşim kaydedilir. Yerine geçmek üzere bileşene geçici `console.count` konur; why-did-you-render yalnız projede zaten kuruluysa kullanılır. · Alt ajan: `fe-react-bilesen-inceleme`. Aradığı nedenler: her render'da yeni nesne/fonksiyon prop'u, geniş Context değeri, üst bileşen state'i, index key.
**F2 Düzeltme (≈8k):** Önce render sayısını kilitleyen bir test yazılır (`@testing-library/react` + `Profiler` onRender sayacı) ve kırmızı görülür. Kökte düzeltilir: state'i aşağı indirmek ya da Context'i bölmek. Yalnız gerekiyorsa `React.memo` ile `useCallback`/`useMemo` eklenir. React Compiler açıksa elle memo eklenmez. · Tartışma noktası: memo yaygınlaştırılırsa karşılaştırma maliyeti doğar. Ölçülen bir kazanç yoksa eklenmez.
**F3 Doğrulama (≈4k):** Test yeşil olmalı, mevcut suite de yeşil kalmalı. Profiler'da commit süresi düşmeli. UI değiştiği için `/frontend-craft` Section 6 tur raporu da gerekir. · İnceleyen: `ecc:code-reviewer`.
**Toplam ≈18k.**

Planlarda adı geçen ajan ve skill'lerin kurulu olup olmadığına yeni bir sorguyla bakmadım; liste bu oturumdaki ajan listesinden alındı. 9. iş için staging ya da replika ortamı varsayıldı. Yoksa EXPLAIN ANALYZE sorguyu gerçekten çalıştırır ve üretime yük bindirir.
