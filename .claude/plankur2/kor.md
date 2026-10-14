## 1. Django + HTMX ile kuaför salonu online randevu sistemi kur: SMS hatırlatma, iyzico ile kapora ödemesi, KVKK aydınlatma metni ve açık rıza, Docker ile VPS'e yayın.
### X
**Varsayımlar:** PostgreSQL, tek VPS, tek salon (çok şubeli değil), SMS sağlayıcı Netgsm ya da İletimerkezi (REST). Katalogda iyzico aracı yok, bu yüzden ortamdaki Payments & Billing Engineer ajanı ve `find-docs` kullanılır.

- **F0 Kapsam (~6k):** kabul ölçütleri (çakışmasız slot, kapora olmadan randevu onaylanmaz, rıza kaydı) ve MVP kesimi.
  - Araç: `departman-guvenlik` ve `departman-surec-git-yayin` sırası, `pln-kabul-olcutleri`, `pln-kapsam-kesici`.
  - Kapı: ölçütler Given/When/Then biçiminde yazılır.
- **F1 Model ve randevu çekirdeği (~25k):** Salon, Hizmet, Personel, Randevu ve Rıza modelleri.
  - Araç: `ecc:django-patterns`, `ecc:django-tdd` (pytest-django).
  - Kapı: aynı slota iki eşzamanlı istek gelir, yalnızca biri kazanır (Postgres exclusion constraint + `select_for_update`). Bu test önce kırmızı görülür.
  - İnceleme: `ecc:django-reviewer`.
  - Tartışma: slot tablosu mu, dinamik hesap mı? Öneri: dinamik hesap ve çakışmayı DB kısıtı yakalar.
- **F2 HTMX arayüzü (~25k):** hizmet seçimi, slot seçimi, form, onay.
  - Araç: `/frontend-craft` (zorunlu), HTMX belgesi için `find-docs`, ekran döngüsü için `playwright` MCP (headless).
  - Kapı: `qa-erisilebilirlik-testi` (axe'te 0 kritik bulgu, klavyeyle gezinme) ve frontend-craft Bölüm 6 tur raporu. CSRF jetonu `hx-headers` ile gönderilir.
  - İnceleme: `fe-tasarim-incele`, `sec-xss-csrf-denetci`.
- **F3 SMS hatırlatma (~15k):** randevudan 24 saat ve 2 saat önce gönderim. Tekrar gönderimi `hatirlatma_gonderildi_at` sütunu engeller.
  - Araç: sağlayıcı istemcisi için `otm-api-entegrasyon`, metin için `marketing-skills:sms`.
  - Tartışma: Celery+Redis mi (`ecc:django-celery`), cron'la çalışan yönetim komutu ve systemd timer mı? Öneri: cron, çünkü tek iş ve tek sunucu var.
  - Kapı: sahte sağlayıcıyla birim testi. Gerçek SMS gönderimi staging'de en çok 5 adet.
- **F4 iyzico kapora (~20k):** Checkout Form (barındırılan sayfa) kullanılır, kart verisi sunucuya hiç değmez. Callback'te ödeme `retrieve` ile sunucu tarafında doğrulanır. İşlem idempotent olur (conversationId = randevu id).
  - Araç: Payments & Billing Engineer, iyzipay için `find-docs`, `otm-webhook-tasarimci`, `sec-pci-dss-kapsam` (SAQ-A teyidi).
  - Kapı: sandbox test kartlarıyla başarılı, başarısız ve tekrar gelen callback testleri. Canlıda en çok 1 gerçek işlem yapılır ve iade edilir. Sandbox ile canlı anahtarlar ayrı ortam değişkenlerinde tutulur.
  - İnceleme: `ecc:security-reviewer`.
  - Tartışma (kullanıcı kararı): iptal süresi ve kaporanın iadesi ya da yanması.
- **F5 KVKK (~15k):**
  - Aydınlatma metni ayrı bir sayfa olur ve bir onay kutusu gerektirmez.
  - Açık rıza (pazarlama SMS'i, İYS) ayrı ve önceden işaretsiz bir kutudur. Hatırlatma SMS'i bilgilendirme mesajıdır, rızaya bağlanmaz.
  - Rıza kaydında sürüm, zaman damgası ve kanal tutulur. Saklama ve silme komutu yazılır.
  - Araç: VKED için `pia-generation`, metinler ve İYS için `policy-monitor`.
  - Kapı: `sec-kvkk-gdpr-kontrol` ve `sec-loglama-gizlilik` (loglarda telefon numarası maskeli olmalı). Son metni hukukçu onaylar; rapora "hukuki görüş değildir" notu düşülür.
- **F6 Docker ve VPS (~20k):** compose içinde web (gunicorn), Postgres, nginx ve certbot.
  - Araç: `ecc:docker-patterns`, `deploy-app`, `ops-nginx-ters-vekil`, `ops-ssh-sertlestirme`, `sec-guvenlik-baslik`. VPS Hostinger'daysa `hostinger` MCP de kullanılır.
  - Kapılar:
    - `manage.py check --deploy` 0 uyarı verir (`ecc:django-verification`).
    - `sec-docker-guvenlik`: konteyner root olarak çalışmaz, imajda sır bulunmaz.
    - `sec-cikis-oncesi-guvenlik` ve `/security-review` geçilir.
    - `git-yayin-oncesi-kontrol`'de geri alma (rollback) adımı yazılıdır.
- **Atlananlar:**
  - `azure:python-appservice-deploy`: hedef VPS.
  - Stripe MCP: kurulu değil, ayrıca iyzico istendi.
  - strix ve ZAP: kurulu değil. Yayın sonrası dinamik tarama için ayrı onay gerekir.
### Y
**Faz 1: Tasarım (~8k)**
- Adımlar: veri modeli (Salon, Personel, Hizmet, Randevu, Kapora, RızaKaydı), randevu akışı (slot seç → kapora öde → onay) ve HTMX parça şablonları.
- Araç: `fe-tasarim-sistemi-kurucu` (ajan) ile DESIGN.md. Hatırlatma zamanlaması `marketing-skills:sms` ile çıkar (24 saat ve 2 saat önce).
- Kapı: kabul ölçütleri yazılı olmalı. Çift randevuyu engellemek için `(personel, başlangıç)` benzersiz kısıtı tasarımda yer almalı.
- Tartışma: SMS sağlayıcısı (Netgsm veya İleti Merkezi) ve kaporanın iade koşulu. Bunlar iş kararı, Ömer'e DUR raporu gider.

**Faz 2: Uygulama (~40k, tahmini; çıktının bu kısmı sıkışık geldi)**
- Adımlar:
  - Django ve django-htmx ile randevu CRUD.
  - Kapora ödemesi iyzipay ile, barındırılan Checkout Form üzerinden. Kart verisi sunucuya hiç gelmez (PCI SAQ-A).
  - Ödeme ve iade isteklerinde idempotency anahtarı, 3DS zorunlu.
  - Ödeme callback'i imza doğrulamasından sonra, olay kimliği üzerinden yalnız bir kez işlenir.
  - SMS gönderimi Celery beat ve Redis ile, tekrar önleme anahtarıyla. Gönderim günlüğe yazılır ve günde en çok 300 SMS gider.
  - KVKK aydınlatma metni ve açık rıza.
- Araç: KVKK metni için `policy-monitor` ve `pia-generation` skill'leri kullanılır. Açık rıza ayrı bir kutudur ve önceden işaretli gelmez. Saklama süresi yazılı olur, silme talebi en geç 30 günde karşılanır.
- Kapı: pytest yeşil olmalı. Callback çift gelirse tek kayıt oluşmalı. Ödeme testleri yalnız iyzico sandbox'ta koşar, en çok 20 çağrı.
- İnceleme: her alt adımın sonunda `ecc:code-reviewer` ve `ecc:django-reviewer`. N+1 sorguları için `django-perf-review`.
- Tartışma: kapora ödenmediğinde slot bekletilsin mi? Önerim 15 dakika bekletmek; süre dolunca slot serbest kalır.

**Faz 3: Test ve güvenlik (~12k)**
- Araç: `departman-guvenlik` sırasına uyulur. Django tarafı `ecc:django-security` ile, Dockerfile ve compose `sec-docker-guvenlik` ile incelenir (root olmayan kullanıcı, imajda sır yok).
- Kapı:
  - semgrep'te 0 yüksek bulgu, gitleaks'te 0 bulgu.
  - `qa-erisilebilirlik-testi` ile 0 ciddi ihlal.
  - LCP ≤ 2,5 sn, CLS ≤ 0,1, INP ≤ 200 ms, ilk yüklemede JS ≤ 170 KB (gz).
  - Staging'de ZAP baseline taraması Docker içinde koşar.
- İnceleme: `ecc:security-reviewer`.

**Faz 4: Yayın ve kapanış (~3k)**
- Adımlar:
  - docker compose ile web, worker, beat, Postgres, Redis ve Caddy (TLS) ayağa kalkar.
  - Önce staging, sonra prod. Sağlık kontrolü için `/healthz`.
  - Geri alma en çok 5 dakika sürer: önceki imaj etiketiyle `compose up`.
- Araç: `ecc:django-verification`, `departman-surec-git-yayin`. VPS ve DNS işleri `hostinger` MCP ile yapılır; prod öncesi Ömer onayı gerekir.
- Kapı: kapanışta test, semgrep, gitleaks, a11y ve kanıt; ardından rapor.
- Konsey: yok. Prod'a ilk yayın geri alınabilir.

## 2. Flutter mobil uygulamasına çevrimdışı çalışan not senkronu ekle: SQLite yerel depo, çakışma çözümü, Firebase kimlik doğrulama, push bildirim ve uçtan uca test.
### X
**Varsayımlar:** notlar kişiye özel (paylaşımlı düzenleme yok). Sunucu tarafı Firestore. Push'un amacı "diğer cihazı senkrona uyandırmak" (sessiz data mesajı). Not hatırlatıcısı istenirse ayrıca netleştirilir.

- **F0 Tasarım (~10k):** veri modeli: `id(uuid)`, `version`, `updatedAt`, `deleted(tombstone)`, `dirty`. Değişiklikler önce yerel outbox tablosuna yazılır.
  - Araç: senkron ve çakışma tasarımı için Realtime Collaboration Engineer, `pln-kabul-olcutleri`.
  - Tartışma 1: Firestore'un yerleşik çevrimdışı önbelleği SQLite'ı gereksiz kılar. Ancak SQLite açıkça istendi, bu yüzden SQLite yerel tek doğruluk kaynağı olarak kalır.
  - Tartışma 2: çakışma politikası. Son yazan kazanır yöntemi veri kaybettirir. Öneri: `version` ile çakışma tespiti; aynı nottaki eşzamanlı gövde düzenlemesinde "çakışan kopya" üretilir ve veri kaybı olmaz.
- **F1 Yerel depo (~20k):** drift (ya da sqflite) şeması, migration'lar, outbox.
  - Araç: `db-sqlite` (WAL, migration), `ecc:dart-flutter-patterns`.
  - Kapı: `flutter analyze` 0 uyarı, migration yükseltme testi, `flutter test`.
  - İnceleme: `ecc:flutter-reviewer`.
- **F2 Senkron ve çakışma (~30k):** önce outbox gönderilir, sonra `updatedAt > lastSync` olan kayıtlar çekilir. Yeniden denemede üstel geri çekilme (backoff) var, her işlem idempotent. Bağlantı geri gelince senkron tetiklenir.
  - Araç: `qa-ozellik-tabanli` ile yakınsama testi (rastgele işlem dizisi verilir, iki cihaz aynı sonuca ulaşmalı ve not kaybolmamalı).
  - Kapı: bu özellik testleri ve çakışan kopya testi önce kırmızı görülür, sonra yeşile döner.
  - İnceleme: `ecc:flutter-dart-code-review`, ardından `inc-test-kalitesi-inceleme`.
- **F3 Firebase Auth (~15k):** e-posta ve Google girişi. Belge yolu `users/{uid}/notes/{id}`. Çıkışta yerel veritabanı temizlenir ya da hesaba bağlanır.
  - Araç: FlutterFire için `find-docs`, Identity & Access Engineer.
  - Kapı: Firestore güvenlik kuralları emülatörde `@firebase/rules-unit-testing` ile test edilir: başkasının notuna okuma ve yazma reddedilir. Ayrıca `sec-cikis-oncesi-guvenlik`.
  - Tartışma: çıkış yapınca senkronlanmamış not ne olur? Öneri: kullanıcıya uyarı göster ve önce gönder.
- **F4 Push (~15k):** FCM token cihaz başına `users/{uid}/devices` altında saklanır. Not değişince Cloud Function diğer cihazlara sessiz data mesajı yollar. Uygulama arka planda senkron yapar.
  - Araç: `mob-push-bildirim`, `mob-calisma-izni` (iOS ve Android 13 bildirim izni).
  - Kapı: bildirim izni reddedilse de senkron çalışmaya devam eder. Gerçek cihaz push testi en çok 10 mesajla sınırlı.
- **F5 Uçtan uca (~20k):** `integration_test` ve Firebase Emulator Suite (Auth + Firestore + Functions).
  - Senaryo: A cihazında çevrimdışı düzenleme, B cihazında aynı notun düzenlenmesi, bağlantının geri gelmesi, ardından çakışan kopyanın kontrolü.
  - Araç: `qa-mobil-qa` (döndürme, uçak modu), derleme hatası çıkarsa `ecc:dart-build-resolver`.
  - Kapı: Android emülatöründe e2e testi yeşil. CI'da emülatörle koşulur (`git-ci-boru-hatti`).
  - Doğrulama: `inc-dogrulama-oncesi-bitis` ayrı bağlamda çalışır (öğrenim #100).
- **F6 Kapanış (~5k):** `departman-surec-inceleme` sırası izlenir. Not içeriği kişisel veri olduğu için hesap silme akışı ve `sec-kvkk-gdpr-kontrol` kontrolü yapılır.
- **Atlananlar:**
  - `ecc:e2e-testing` ve `qa-playwright`: web içindir, Flutter'a uymaz.
  - Supabase, Convex ve Netlify araçları: Firebase istendi.
  - `sentry-flutter-sdk`: istenmedi.
### Y
**Faz 1: Tasarım (~8k)**
- Adımlar:
  - Yerel şema drift (SQLite) ile kurulur. Notlarda `id(uuid)`, `updatedAt`, `version`, `deleted` ve `dirty` alanları olur.
  - Senkron kuyruğu (outbox) yerelde tutulur, sunucu tarafı Firestore'dur.
- Araç: push akışı `mob-push-bildirim` (ajan) ile tasarlanır; FCM token kaydı ve izin isteme zamanı burada belirlenir.
- Tartışma: çakışma çözümü kritik karar.
  - Önerim alan bazında last-write-wins: `version` karşılaştırılır, gövde çakışırsa "çakışan kopya" not olarak saklanır ve veri kaybolmaz.
  - CRDT gereksiz karmaşa getirir; yalnız eşzamanlı ortak düzenleme istenirse düşünülür.
  - Konsey açılmaz, karar geri alınabilir.

**Faz 2: Uygulama (~35k)**
- Adımlar:
  - drift repository'si ve outbox.
  - connectivity_plus ile ağ geri gelince push/pull. Pull, `updatedAt` imleciyle artımlı yapılır.
  - Firebase Auth (firebase_auth). Jetonu SDK yeniler; hız sınırı tarafında Firebase'in giriş limiti 5 deneme/dk ile karşılaştırılır.
  - Firestore kuralları: kullanıcı yalnız kendi `uid` yolunu okuyup yazabilir.
  - Bildirim izni `mob-calisma-izni` ile ele alınır; izin reddedilirse uygulama bildirimsiz çalışmaya devam eder.
  - firebase_messaging; sunucudan gönderim günde kullanıcı başına en çok 20 bildirim, tekrar önleme anahtarıyla.
- Kapı: drift migration testleri ve çakışma birim testleri yeşil olmalı. Sırlar repoda olmaz.
- İnceleme: `ecc:flutter-reviewer` ve `ecc:code-reviewer`.
- Elenen aday: `auth0` MCP. Yığın Firebase olduğu için uymuyor.

**Faz 3: Test ve güvenlik (~12k)**
- Araç: `departman-test-qa` kullanılır; uçtan uca testler integration_test ve Firebase Emulator Suite ile koşar.
- Kapı:
  - İki cihaz çevrimdışıyken aynı nota yazar, sonra ikisi de bağlanır. Beklenen: hem kazanan hem çakışan kopya tutulur, veri kaybı 0.
  - Soğuk açılış ≤ 2 sn.
  - Firestore kural testleri yeşil.
  - semgrep'te 0 yüksek bulgu, gitleaks'te 0 bulgu.
- İnceleme: `ecc:security-reviewer`. Doğrulamayı kodu yazandan ayrı bir bağlam yapar.
- Elenen aday: `test-playable-web-games`, oyun QA'sı için olduğundan uymuyor.

**Faz 4: Yayın ve kapanış (~3k)**
- Araç: `Mobile Release Engineer` (ajan) ile önce dahili test kanalına (Play internal / TestFlight) çıkılır, sonra kademeli yayın.
- Kapı: kapanışta test, semgrep, gitleaks ve kanıt; ardından rapor.
- Elenen adaylar: `deploy-app` ve `azure-validate`, web ve Azure için oldukları için uymuyor.

## 3. Şirket içi PDF sözleşmeleri için RAG soru-cevap botu kur: belge ayrıştırma, parçalama, vektör veritabanı, yerel LLM ile yanıt, kaynak gösterme ve kalite değerlendirme seti.
### X
**Varsayımlar:**
- Veri şirket dışına çıkmaz; her şey yerelde çalışır (Ollama).
- Sözleşmeler Türkçe ağırlıklı ve yüzlerce PDF ölçeğinde.
- Taranmış (görüntü) PDF oranı bilinmiyor; F1'de ölçülür.

- **F0 Kapsam ve erişim (~8k):** kim hangi sözleşmeyi görebilir? Erişim matrisi çıkarılır, kabul ölçütleri yazılır.
  - Araç: `sec-yetkilendirme-matrisi`, `pln-kabul-olcutleri`.
  - Tartışma (kritik): belge düzeyinde yetki filtresi aramanın içinde mi uygulanır, sonradan mı? Öneri: metadata filtresiyle arama içinde. Sonradan süzme sızıntıya açıktır.
- **F1 Ayrıştırma (~20k):** sayfa numarası ve madde başlıkları korunur.
  - Araç: `example-skills:pdf` (pdfplumber; sayfa ve tablolar), `dok-markitdown-donusum` / `markitdown` MCP (karşılaştırma için).
  - Kapı: 10 örnek PDF'te metin, sayfa eşleşmesi ve tablolar elle örneklenir. Taranmış PDF oranı ölçülür.
  - Tartışma: OCR. markitdown OCR yapmaz. Oran %5'in üstündeyse OCR fazı eklenir (Tesseract `tur`); altındaysa bu PDF'ler raporlanıp atlanır.
- **F2 Parçalama (~15k):** madde sınırına duyarlı parçalama ("Madde 5", "5.1" kalıpları) ve fazla uzun maddeyi pencereyle bölme. Her parçanın metadata'sı: dosya, sayfa, madde no, taraflar, tarih.
  - Araç: `ecc:regex-vs-llm-structured-text` (ucuz regex yolu önce).
  - Kapı: parçalayıcı birim testleri (madde bölünmesi, sayfa taşması).
  - İnceleme: `inc-test-kalitesi-inceleme`.
- **F3 Vektör DB ve arama (~20k):**
  - Gömme: bge-m3 (Ollama, çok dilli).
  - Hibrit arama: BM25 + vektör. Sözleşme terimleri ve madde numaraları için BM25 şart.
  - Araç: `db-vektor-veritabani`, RAG Pipeline Engineer.
  - Tartışma: Chroma/LanceDB gömülü mü, Qdrant mı, pgvector mı? Öneri: gömülü LanceDB (tek süreç, hibrit desteği var). Şirkette Postgres varsa pgvector. Önce `qmd` MCP ile hızlı bir taban çizgisi denenir.
- **F4 Yerel LLM ve kaynak gösterme (~20k):** model ve kuantizasyon (ör. Qwen2.5-7B Q4) VRAM'e göre seçilir.
  - İstem kuralları: yalnız verilen parçalardan yanıt verilir; her iddia `[dosya s.X m.Y]` biçiminde kaynaklanır; kaynak yoksa "belgede yok" denir.
  - Araç: `ml-yerel-llm-cikarim`, `sec-istem-enjeksiyon-savunma` (belge içindeki talimatlar veri olarak işlenir).
  - Kapı: atıf doğrulayıcı. Gösterilen sayfada alıntı metni gerçekten geçmiyorsa yanıt reddedilir. Bunun için assert tabanlı bir test yazılır.
- **F5 Değerlendirme seti (~25k):** 60 soruluk altın set: 40 yanıtlanabilir, 10 çok belgeli, 10 yanıtsız. Soru tipleri: fesih, cezai şart, süre, yenileme. Setin doğruluğunu hukuk ekibi onaylar.
  - Araç: `ml-llm-degerlendirme`, soru tipleri için `dok-sozlesme-madde`.
  - Kapı:
    - Arama recall@5 ≥ 0.85
    - Atıf doğruluğu ≥ 0.90
    - Yanıtsız sorularda ret oranı ≥ 0.90
    - Sonuçlar regresyon kapısı olarak CI'a girer.
  - Hakem: yerel model + insan örneklemesi. Ücretli API yok; kullanılırsa en çok 60 çağrı.
- **F6 Teslim (~10k):** basit arayüz ya da CLI, sorgu logu (PII maskeli).
  - Araç: `sec-kvkk-gdpr-kontrol`, `sec-loglama-gizlilik`, `departman-surec-inceleme`.
  - Doğrulama: ayrı bağlamda `inc-dogrulama-oncesi-bitis`.
- **Atlananlar:**
  - `pinecone-paket`: bulut, veri dışarı çıkar.
  - Ironclad, iManage, Definely, Google Drive: kaynak yerel PDF.
  - `knowledge-base-skills` eklentisi: kurulu değil. Kurulursa F3'te taban çizgisi olarak denenebilir.

---

Üç iş de zor iş sayıldı; katalog tek Bash çağrısında çalıştı ve ek sorgu yapılmadı. Hiçbir dosya yazılmadı.

Varsayımlar doğrulanmadı: iyzico Python SDK sürümü, VPS sağlayıcısı, push'un hatırlatma mı senkron mu olduğu, makinedeki GPU/VRAM. Planlar bu cevaplara göre değişir.

KVKK metinleri hukuki görüş yerine geçmez; hukukçu onayı gerekir.
### Y
**Faz 1: Tasarım (~6k)**
- Adımlar:
  - Altyapı belirlenir: VRAM ölçülür, model ve bağlam tavanı yazılır.
  - Altın soru seti en az 50 sorudur. Her soruda beklenen yanıt, sözleşme adı ve sayfa/madde bulunur.
- Araç: `departman-arastirma-ogrenme` ile yığın kararı verilir. Yerel LLM ve embedding Ollama üzerinden çalışır (ör. qwen2.5 7B + bge-m3).
- Tartışma: vektör veritabanı.
  - Önerim pgvector: tek servis olur ve metadata süzgeci sağlar.
  - Alternatif Qdrant. Yalnız 1M'yi aşan parça ölçeği gerekirse seçilir.
  - Konsey açılmaz, karar geri alınabilir.

**Faz 2: Uygulama (~25k)**
- Adımlar:
  - Ayrıştırma `dok-markitdown-donusum` ile yapılır. Taranmış PDF'lerde OCR gerekiyorsa DUR raporu yazılır.
  - Parçalama madde/başlık sınırında yapılır: 500–800 token, %10 örtüşme. Her parçada `dosya`, `sayfa` ve `madde` metadata'sı olur.
  - Embedding'ler ve indeks `db-vektor-veritabani` (ajan) ile kurulur: HNSW ve sözleşme süzgeci.
  - Yanıt üretimi: top-k=5 parça alınır, yanıt yalnız bu bağlamdan ve kaynak etiketli üretilir. Kaynak bulunamazsa "bulunamadı" denir.
  - Belge içeriği güvenilmeyen girdi olarak ele alınır; prompt enjeksiyonuna karşı sistem talimatı ayrı tutulur.
- Kapı: ayrıştırma ve parçalama birim testleri yeşil olmalı. Sözleşmeler şirket içi olduğu için hiçbir çağrı dış API'ye gitmez; bu, ağ izleme ile doğrulanır.
- İnceleme: `ecc:database-reviewer` ve `ecc:code-reviewer`.
- Elenen adaylar: `pdf-engine-architect` HTML'den PDF üretimi için, `azure` bulut için, `migration-planlayici` canlı şema taşıma için; hiçbiri bu işe uymuyor.

**Faz 3: Değerlendirme ve güvenlik (~10k)**
- Adımlar: 50 soruluk set koşulur. Recall@5, kaynak gösterim doğruluğu ve yanıt doğruluğu ölçülür. Hakemi yerel LLM yapar, sonuçlar ayrıca elle örneklenir.
- Kapı:
  - Kaynak gösterim doğruluğu ≥ %90, p95 yanıt süresi ≤ 5 sn.
  - semgrep'te 0 yüksek bulgu, gitleaks'te 0 bulgu.
  - `secret-serialization` ile loglarda sözleşme metni sızmadığı doğrulanır.
- İnceleme: `ecc:security-reviewer`.
- Tartışma: eşik tutmazsa önce parça boyu ve reranker denenir. Model büyütmek VRAM tavanına bağlıdır.

**Faz 4: Kapanış (~3k)**
- Araç: CI `gh` ile kontrol edilir, dokümantasyon `gstack-document-release` ile güncellenir.
- Kapı: kapanışta test, değerlendirme raporu ve kanıt; ardından rapor.

---

`plan_kur.py` tek seferde çalıştırıldı ve hiçbir dosya yazılmadı. Çıktının iki bloğu sıkışık geldi; "ek sorgu yok" kuralı gereği açmadım, bu yüzden 1. işin faz jeton bütçeleri benim tahminim. Katalog bazı uyumsuz araçlar önerdi; bunları her işte "Elenen aday" satırında gerekçesiyle eledim.

## 4. Mevcut Express.js REST API'sini GraphQL'e kademeli taşı: şema tasarımı, N+1 önleme, kimlik doğrulama, hız sınırı, sözleşme testleri ve geriye dönük uyum.
### X
— Express REST → GraphQL kademeli geçiş (zor)

**Faz 0 · hazırlık · 3k**
- Adım: `departman-surec-inceleme` skill'i açılır, inceleme sırası alınır. `.claude/dalga.md` dosyasına KARAR ve kabul ölçütleri yazılır. Grep ile REST rotaları ve servis katmanı çıkarılır.
- Kapı: rota envanteri tam olmalı. Rota sayısı Grep ile ve elle karşılaştırılır.

**Faz 1 · tasarım · 8k**
- Adım: `api-and-interface-design` skill'i ile SDL şeması tasarlanır. Önce şema yazılır; sayfalama cursor ile yapılır; hatalar tip olarak tanımlanır. Her REST ucu bir Query ya da Mutation alanına eşlenir.
- Araç: `otm-sema-dogrulayici` ajanı mevcut REST yanıtlarından JSON Schema anlık görüntüsü alır. Bu, sözleşme testlerinin tabanıdır.
- Kapı: her REST ucunun bir GraphQL karşılığı olmalı. Şema lint'i hatasız geçmeli.
- Tartışma: tek seferde geçiş mi, strangler mı? Öneri strangler: `/graphql` uç noktası Express'in yanına bağlanır, REST olduğu gibi kalır.
- İnceleyen: `ecc:code-reviewer`

**Faz 2 · uygulama · 35k**
- Adım: `ecc:backend-patterns` skill'i kullanılır. Resolver'lar mevcut servis katmanını çağırır, iş mantığı kopyalanmaz.
- N+1: istek başına bir `dataloader` örneği context içinde oluşturulur.
- Kimlik doğrulama: mevcut Express auth middleware'i `context.user`'ı doldurur. Yetki kontrolü resolver'da, alan düzeyinde yapılır.
- Hız sınırı: mevcut rate-limit `/graphql`'e de uygulanır. Ek olarak sorgu derinliği ≤7 tutulur ve karmaşıklık tavanı konur.
- Kapı: istek başına DB sorgu sayısı sabit kalmalı. Bunu sorgu sayacı ile yazılan bir test ölçer. p95 ≤300 ms olmalı. Hız sınırı 100 istek/dk/anahtar. Erişim jetonu ≤15 dk, yenileme jetonu döndürülür. Giriş denemesi 5/dk ile sınırlı.
- İnceleyen: `ecc:code-reviewer`

**Faz 3 · test ve güvenlik · 20k**
- Adım: `inc-dogrulama-oncesi-bitis` ajanı parite testini koşar. Her REST anlık görüntüsü eşdeğer GraphQL sorgusunun yanıtıyla karşılaştırılır.
- Adım: `api-security-testing` skill'i (Strix) yalnız yerel ortamda **en çok 1 koşu** çalıştırılır, çünkü ücretli LLM çağrısı yapar.
- Kapı: parite %100, testler yeşil, semgrep'te 0 yüksek bulgu, gitleaks'te 0 bulgu. Introspection üretimde kapalı olmalı.
- İnceleyen: `ecc:security-reviewer`

**Faz 4 · yayın ve kapanış · 4k**
- Adım: GraphQL bir bayrak arkasında açılır; geri almak için bayrak kapatılır. REST uçlarına `Deprecation` ve `Sunset` başlıkları eklenir.
- Kapı: bir REST ucu ancak kullanım metriği 0'a indiğinde kaldırılır. Sözleşme testi kırmızıysa yayın yapılmaz.
- Tartışma: REST'i kaldırmak geri dönüşsüz tek karardır. Kullanım verisi varsa karar veriye göre verilir. Veri yoksa `ecc:council` 1 kez çalıştırılır (~60–90k).
- Kapanış raporu: commit · test sayısı · CI · sapmalar. `dalga.md` silinir.
### Y
— Express REST → GraphQL kademeli geçiş (zor: API + güvenlik + test)
Ön adım: `departman-surec-inceleme` ve `departman-guvenlik` müdür skill'leri açılır. Keşif, test koşusu ve log okuma işleri sonnet alt ajana verilir.

- **F0 Keşif** · adım: route envanteri, middleware zinciri (auth, rate limit), servis katmanı ve mevcut REST testleri çıkarılır · araç: `graphify query` (yoksa `ara-graphify-sorgu`), `ecc:backend-patterns` · kapı: mevcut REST suite yeşil, bu temel çizgi olur · inceleyen: — · bütçe ~8k
- **F1 Şema** · adım: önce SDL yazılır (schema-first), kaynak→tip eşlemesi yapılır, Relay cursor sayfalama, ortak hata modeli ve `@deprecated` politikası belirlenir · araç: `api-and-interface-design`, `dil-graphql` ajanı, `find-docs` (yoga/apollo güncel API) · kapı: `graphql-inspector validate` + `@graphql-eslint` · inceleyen: `octo:personas:graphql-architect` · tartışma: graphql-yoga (MIT, envelop eklentileri) mı Apollo Server 4 mü? Öneri: yoga, çünkü derinlik/maliyet/rate eklentileri hazır geliyor · bütçe ~15k
- **F2 Boğucu incir iskeleti** · adım: `/graphql` REST'in yanına mount edilir. Resolver'lar mevcut servis katmanını çağırır, REST'e HTTP ile dönmez · araç: `pln-bogucu-incir-gocu` · kapı: REST suite hâlâ yeşil, geriye uyum korunuyor · inceleyen: `ecc:code-reviewer` · bütçe ~10k
- **F3 N+1** · adım: istek başına DataLoader `context` içinde kurulur, ilişkili alanlar batch'lenir · araç: `dataloader` (MIT), `dil-graphql` · kapı: sorgu sayacı testi (ORM hook'u). Örneğin 50 kayıt + ilişki için DB sorgusu ≤ 3, önce kırmızı görülür · inceleyen: `ecc:performance-optimizer` · bütçe ~10k
- **F4 Kimlik doğrulama** · adım: mevcut Express auth middleware'i yeniden kullanılır (`context.user`). Yetki alan/resolver düzeyinde, rol×işlem matrisiyle denetlenir. Prod'da introspection kapatılır · araç: `sec-yetkilendirme-matrisi`, `sec-jwt-denetci` · kapı: matristeki her hücre için bir test, yetkisiz istek → `FORBIDDEN` · inceleyen: `ecc:security-reviewer` · tartışma: direktif (`@auth`) mi resolver içi kontrol mü? Öneri: az alan varsa resolver içi kontrol · bütçe ~12k
- **F5 Hız sınırı + maliyet** · adım: derinlik limiti, `graphql-query-complexity`, kullanıcı+maliyet anahtarlı `rate-limiter-flexible`; mevcut Redis yeniden kullanılır · araç: `be-hiz-sinirlayici` · kapı: derinlik/maliyet aşımı testleri, limit aşımında doğru hata kodu dönmeli · inceleyen: `ecc:security-reviewer` · tartışma: istek sayısı mı maliyet bazlı mı? Tek `/graphql` uç noktasında istek sayısı anlamsız kalır, bu yüzden maliyet bazlı · bütçe ~10k
- **F6 Sözleşme + geriye uyum** · adım: CI'da `graphql-inspector diff` main şemasıyla karşılaştırılır, kırıcı değişiklik → fail. REST↔GraphQL parity testleri (aynı veri, aynı sonuç). Ayrı tüketiciler varsa Pact · araç: `ecc:contract-first`, `git-ci-boru-hatti`, `gh` · kapı: CI yeşil + kasıtlı kırıcı PR'ın kırmızı olduğu görülür · inceleyen: `pr-review-toolkit:pr-test-analyzer` · bütçe ~12k
- **F7 Kademeli geçiş + güvenlik** · adım: istemci başına feature flag; REST uçlarına `Deprecation`/`Sunset` (RFC 8594) başlıkları; trafik ölçülür; REST trafik 0 olmadan silinmez · araç: `api-security-testing` (Strix, staging'de **en çok 1 koşu**), `sec-loglama-gizlilik` · kapı: Strix'te high bulgu 0. KVKK: GraphQL değişkenleri (PII) loglanmaz · inceleyen: `departman-surec-inceleme` → `inc-dogrulama-oncesi-bitis` · bütçe ~12k
- Lisans: yoga, dataloader, inspector, query-complexity MIT; rate-limiter-flexible ISC. `ara-lisans-kontrol` ile teyit edilecek. **Toplam ~90k.**

## 5. Vue 3 yönetim panelinde yavaş yüklenen dashboard'u hızlandır: paket boyutu analizi, sanal liste, API önbellekleme, Lighthouse ölçümü ve performans regresyon kapısı CI'da.
### X
— Vue 3 dashboard hızlandırma (zor: frontend + perf + CI)
Ön adım: `/frontend-craft` yüklenir (UI işi kuralı) ve eşleşen `departman-*` frontend müdürü açılır. Ölçüm işleri sonnet alt ajanda koşar. Tarayıcı yalnız headless açılır.

- **F0 Taban ölçümü** · adım: prod build ile Lighthouse 3 koşu, medyan alınır (LCP, TBT, INP, JS KB). DevTools performance izi ve ağ şelalesi çıkarılır · araç: `npx @lhci/cli` (Apache-2.0; katalogdaki `lighthouse-chrome-devtools` kurulu değil), `chrome-devtools` MCP, `rollup-plugin-visualizer` · kapı: sayılar `dalga.md`'ye yazılır · inceleyen: — · bütçe ~10k
- **F1 Kök neden** · adım: süre payı ölçülerek paket / render (uzun liste) / ağ (şelale, tekrarlı istek) olarak sınıflandırılır · araç: `web-perf`, `performance-optimization` · kapı: her darboğaz bir ölçümle kanıtlanmış olur · inceleyen: `agent-skills:web-performance-auditor` · tartışma: düzeltme sırası ölçülen paya göre seçilir, sezgiyle değil · bütçe ~8k
- **F2 Paket boyutu** · adım: route/widget bazında `defineAsyncComponent` ve dinamik import; grafik kütüphanesinde modüler import (ör. `echarts/core`); gerekirse `manualChunks` · araç: `size-limit` (`omer-kutuphaneler` pinli satırı), `ecc-frontend-paket` (Vue/Vite) · kapı: size-limit bütçesi (taban −%30 hedefi) + vitest yeşil · inceleyen: `ecc:vue-reviewer` · bütçe ~12k
- **F3 Sanal liste** · adım: uzun tablo için önce yüklü bir sanallaştırıcı aranır, yoksa `@tanstack/vue-virtual` (MIT). `aria-rowcount`/`aria-rowindex` ve klavye gezinmesi korunur · araç: `fe-sanal-liste` ajanı · kapı: bileşen testi + Playwright kaydırma testi + axe (`qa-erisilebilirlik-testi`), ihlal 0 · inceleyen: `ecc:vue-reviewer` · tartışma: sanallaştırma mı sunucu sayfalaması mı? Satır sayısı ~500'ün altındaysa sayfalama daha basit, onu seç · bütçe ~12k
- **F4 API önbellek** · adım: projede vue-query/pinia önbelleği var mı bakılır, yoksa `@tanstack/vue-query` (`staleTime`, dedupe). Şelale paralel isteklere çevrilir. Sunucu tarafında ETag/`Cache-Control` · araç: `be-onbellek-gecersizlestirme` · kapı: aynı anahtarlı iki widget → 1 istek testi; mutasyon sonrası invalidation testi. KVKK: kişisel veri localStorage'a kalıcı yazılmaz (`sec-kvkk-gdpr-kontrol`) · inceleyen: `ecc:code-reviewer` · bütçe ~10k
- **F5 CI regresyon kapısı** · adım: GitHub Actions'ta `lighthouserc` (numberOfRuns 3, LCP < 2.5 s, TBT < 200 ms, perf ≥ 0.9) + size-limit. Admin girişi için msw mock API ile preview build kullanılır · araç: `qa-benchmark-regresyon-kapisi`, `git-ci-boru-hatti`, `gh` · kapı: kasıtlı yavaşlatılmış PR'ın kırmızı olduğu görülür · inceleyen: `pr-review-toolkit:pr-test-analyzer` · tartışma: gürültü toleransı. Medyan + %10 pay mı mutlak eşik mi? Öneri: önce mutlak eşik · bütçe ~12k
- **F6 Uçtan uca doğrulama** · adım: gerçek uygulamada önce/sonra ölçümü aynı koşullarda tekrarlanır · araç: `chrome-devtools` MCP, `ecc:benchmark` · kapı: frontend-craft Bölüm 6 tur raporu; SEO yok (panel auth arkasında) · inceleyen: `departman-surec-inceleme` → `inc-dogrulama-oncesi-bitis` · bütçe ~8k
- **Toplam ~72k.**

Planlar eşit derinlikte değil: iki iş de birden çok alana dokunduğu için ikisini de zor saydım; listede rutin iş yoktu. Katalog tek çağrıda koşuldu, ek sorgu yapılmadı, dosya yazılmadı. Repo kodu görülmediği için ORM, Redis, grafik kütüphanesi ve yüklü bağımlılıklar tahmin. Her faz başında bunlar doğrulanmalı.

Lisanslar hafızadan yazıldı, kontrol edilmedi. Strix ücretli LLM çağrısı yapar, bu yüzden en çok 1 koşuyla sınırlandı.
### Y
— Vue 3 dashboard hızlandırma (zor)

**Faz 0 · taban ölçüm · 5k**
- Adım: UI işi olduğu için önce `frontend-craft:frontend-craft` yüklenir.
- Adım: `web-perf` skill'i ile dashboard'da Lighthouse 3 kez koşulur, medyan alınır.
- Adım: paket analizi için Vite'in visualizer'ı kullanılır. Projede zaten ne varsa o kullanılır.
- Kapı: taban sayılar (LCP, INP, CLS, JS gz) `dalga.md`'ye yazılır.

**Faz 1 · tasarım · 6k**
- Adım: `interaction-design:doherty-threshold` skill'i ile algılanan gecikme ele alınır. Hedef: 400 ms altında iskelet ya da geri bildirim göstermek.
- Adım: en ağır parçaların bölünme planı çıkarılır. Örnek: grafik kütüphanesi ve tablo.
- Tartışma: istemci önbelleği için kütüphane mi eklenmeli, basit bir SWR yeterli mi? Önce bağımlılıklara bakılır. Kütüphane yoksa basit SWR ile `Cache-Control`/`ETag` yeterli olabilir.

**Faz 2 · uygulama · 30k**
- Adım: `performance-optimization` skill'i kullanılır. Rota ve widget'lar `defineAsyncComponent` ve dinamik `import()` ile tembel yüklenir.
- Adım: `fe-sanal-liste` ajanı uzun tabloyu sanallaştırır. Projede kurulu sanal liste kütüphanesi varsa o kullanılır.
- Adım: API önbelleği kullanıcıya bağlı anahtarla tutulur ve çıkışta temizlenir. Bu bir KVKK gereği: aynı tarayıcıda veri başka kullanıcıya sızmamalı.
- Kapı: ilk yükteki JS ≤170 KB gz olmalı. 10 bin satırlık listede kaydırma takılmamalı.
- İnceleyen: `ecc:code-reviewer`

**Faz 3 · test ve güvenlik · 12k**
- Adım: `agent-skills:web-performance-auditor` ajanı ve `web-perf` skill'i ile yeniden ölçüm yapılır.
- Adım: `qa-erisilebilirlik-testi` ajanı sanal listeyi klavye ve `aria-rowcount` açısından kontrol eder.
- Kapı: LCP ≤2.5 s, CLS ≤0.1, INP ≤200 ms. Erişilebilirlikte 0 ciddi ihlal. Testler yeşil, semgrep'te 0 yüksek, gitleaks'te 0 bulgu.
- İnceleyen: `ecc:security-reviewer`. Odak: önbellekte kiracılar arası veri sızıntısı.

**Faz 4 · CI kapısı ve kapanış · 6k**
- Adım: `qa-benchmark-regresyon-kapisi` ajanı CI'a Lighthouse CI assert'leri ve paket boyutu bütçesi ekler.
- Kapı: paket %5'ten, LCP %10'dan fazla artarsa CI kırmızı olur. frontend-craft Bölüm 6 tur raporu hazırlanır.
- Konsey: yok, çünkü tüm adımlar geri alınabilir.
- Kapanış raporu: commit · test sayısı · CI · sapmalar.

---
plan_kur'un önerdiği şu adayları alakasız diye eledim: taste-skill, azure-validate, db-elasticsearch, otm-api-entegrasyon, design-ui-finish-gate-reviewer ve n8n/reel öğrenimleri. `ecc:database-reviewer` bu oturumun ajan listesinde yok, o yüzden kullanmadım. Her iki planda da önce projede bir kütüphanenin zaten kurulu olup olmadığına bakılacak; bunu henüz kontrol etmedim.

## 6. Unity ile 2D platform oyunu için seviye editörü yap: tilemap, kaydet/yükle JSON, oynanış testi, düşman yapay zekası ve Steam için yapı paketleme.
### X
**Unity 2D seviye editörü.** Yığın Unity. Web arayüzü olmadığı için (Unity EditorWindow) frontend-craft atlandı.

**Faz 1: Tasarım (8k)**
- Adım: Kaydedilecek veriyi tanımla. Tilemap katmanları, düşman yerleşimleri ve başlangıç/çıkış noktaları JSON'a girer. JSON'da sürüm alanı bulunur.
- Adım: Düşman davranışını belirle. Durumlar devriye, kovalama ve saldırıdır; algı menzili ve bekleme süresi de tanımlanır.
- Araç: Agent `oyn-dusman-ai` ve Agent `oyn-seviye-tasarim`. Geçici sprite gerekirse Skill `gorsel-uret`.
- Kapı: Şema belgesinde her alanın türü ve varsayılan değeri yazılı.
- İnceleyen: ecc:code-reviewer.
- Tartışma noktası: JSON şemasının sürümleme kuralı. Oyuncu seviyeleri dağıtıldıktan sonra şemayı değiştirmek geri dönüşsüzdür, bu yüzden geçiş (migration) kuralı şimdi yazılır. Konsey yok.

**Faz 2: Uygulama (40k)**
- Adım: Tile boyama için EditorWindow yaz. Unity'nin hazır Tilemap ve Tile Palette araçları kullanılır, yenisi yazılmaz.
- Adım: Kaydetme/yükleme için `JsonUtility` kullan. Dış paket eklenmez.
- Adım: Düşman yapay zekası için tek bir durum makinesi bileşeni yaz.
- Adım: "Oyna" düğmesi yaz. Düğme seviyeyi geçici bir sahneye yükler ve Play Mode'a geçer.
- Araç: Sahne ve derleme işleri için `unity` MCP (ToolSearch ile bulunur). Kod sahne ve prefab'ları onun üzerinden sürer.
- Kapı: Unity Test Framework (EditMode) yeşil.
- İnceleyen: ecc:code-reviewer.

**Faz 3: Test ve denge (12k)**
- Adım 1: Kaydet → yükle tur testi. Tüm tile'lar ve düşmanlar aynı durumda dönmeli.
- Adım 2: PlayMode testi. Düşman oyuncuyu menzile girince kovalamalı, menzilden çıkınca devriyeye dönmeli.
- Adım 3: Profiler ile ölçüm.
- Kapı: 60 fps (kare süresi ≤16.7 ms). Windows yapısı uyarısız derlenir. semgrep 0 yüksek bulgu, gitleaks 0 bulgu.
- Güvenlik: Bozuk ya da dev boyutlu JSON yüklenince çökme olmamalı. Bu bir güven sınırı olduğu için doğrulanır.
- İnceleyen: ecc:security-reviewer (JSON ayrıştırma) ve ecc:code-reviewer.

**Faz 4: Steam paketleme ve kapanış (3k)**
- Adım 1: Batchmode ile Windows yapısı al (`-batchmode -buildTarget Win64`).
- Adım 2: Depot klasörünü ve `app_build.vdf` dosyasını hazırla.
- Adım 3: Skill `version-bump`. Klasör yapısı için Agent `oyn-mod-paketleme`.
- Kapı: Önce yerel yapının duman testi yapılır. Steam'e yükleme öncesi bir geri alma adımı yazılır: önceki build ID'ye dönme ≤5 dk.
- Steam'e yükleme dışarıya açık bir iştir ve Ömer'in onayı gerekir. steamcmd ve Steamworks hesabı listede yok, bu yüzden plan yerel depot'ta biter.
- Kapanış: test · semgrep · gitleaks · rapor (commit · test sayısı · CI · sapma).

**Toplam:** ~63k
### Y
**Varsayımlar:** Projede Unity 2022.3 LTS ya da Unity 6 kurulu. Seviye editörü oyunun içinde çalışacak, yani oyuncu da Steam sürümünde kullanabilecek. Kesin karar F0'da verilir.

**F0 · Keşif ve karar (≤8k jeton)**
- **Adım:** İlgili departman-* müdür skill'i açılır. `Packages/manifest.json` Read ile okunur; 2D Tilemap, Input System ve Test Framework paketlerinin varlığına bakılır.
- **Araç:** unity MCP ile sahne envanteri çıkarılır. oyn-seviye-tasarim ajanı öğe listesini çıkarır: zemin, tehlike, düşman doğma noktası, kontrol noktası, çıkış.
- **Kapı:** Kabul ölçütleri pln-kabul-olcutleri ile yazılır ve `.claude/dalga.md` dosyasına girer.
- **Tartışma:** Oyun içi editör mü, yalnız geliştiriciye açık EditorWindow mu? Öneri oyun içi editör: aynı Tilemap kullanılır, oynanış testi tek tuşla başlar ve Steam sürümünde de çalışır.

**F1 · Veri modeli ve JSON (≤20k)**
- **Adım:** `LevelData{int version; Vector2Int size; TileEntry[] tiles; EntitySpawn[] entities}` yapısı kurulur. Tilemap ile LevelData arasında iki yönlü dönüştürücü yazılır. Dosyalar `persistentDataPath/levels/` altına kaydedilir.
- **Araç:** oyn-oyun-motoru-script ajanı ve JsonUtility. JsonUtility Dictionary desteklemediği için dizi kullanılır. Newtonsoft yalnız çok biçimli varlık gerekirse eklenir.
- **Kapı:**
  - EditMode testleri `Unity -batchmode -nographics -runTests -testPlatform EditMode` ile koşar: kaydet-yükle sonrası veri aynı kalmalı, eski sürüm dosya yüklenebilmeli.
  - Güvenlik (sec-yol-gecisi ajanı): yüklemede boyut sınırı, tile id aralık denetimi ve dosya adında yol geçişi engeli.
- **İnceleme:** ecc:csharp-reviewer.
- **Tartışma:** JsonUtility mi Newtonsoft mu? Öneri JsonUtility, çünkü yeni bağımlılık gerektirmez.

**F2 · Editör araçları (≤30k)**
- **Adım:** Boya, sil, doldur, katman seçimi, varlık yerleştirme, komut yığınıyla geri alma, kaydet/yükle arayüzü.
- **Araç:** unity MCP (prefab ve sahne işleri), `Tilemap.SetTile` / `GetTilesBlock`, `Grid.WorldToCell`.
- **Kapı:**
  - EditMode testi: boya → kaydet → yükle zinciri.
  - Erişilebilirlik: her araca klavye kısayolu; tuşlar Input System ile yeniden atanabilir.
  - /frontend-craft atlanır, çünkü web arayüzü içindir ve uGUI'ye uymaz. Gerekçe raporda yazılır.
- **İnceleme:** ecc:csharp-reviewer.

**F3 · Oynanış testi (≤15k)**
- **Adım:** Editörden oyuna geçişte LevelData bellekte tutulur, oyuncu doğma noktasına konur. Esc ile editöre dönülür ve durum sıfırlanır.
- **Kapı:** PlayMode testleri: doğma, ölüm sonrası yeniden doğma, çıkış tetiği. Seviye doğrulayıcı doğma noktası ve çıkışın varlığına bakar, zıplama yüksekliğine göre basit BFS ile çıkışa ulaşılabilirliği denetler.

**F4 · Düşman yapay zekası (≤25k)**
- **Adım:** Durum makinesi Devriye → Kovala → Saldır → Dön. Kenar ve duvar raycast ile bulunur. Algı menzil ve görüş çizgisiyle çalışır, saldırıda bekleme süresi vardır. Parametreler ScriptableObject'te tutulur.
- **Araç:** oyn-dusman-ai ajanı. Yalnız uçan düşman için oyn-yol-bulma ile tile ızgarasında A* kullanılır.
- **Kapı:**
  - PlayMode testleri: düşman kenardan düşmez, menzile giren oyuncuyu kovalar, menzil dışında geri döner.
  - Performans: 50 düşmanla AI süresi kare başına 2 ms'nin altında kalmalı; Profiler unity MCP üzerinden okunur.
- **İnceleme:** ecc:csharp-reviewer ve inc-ponytail-kod.
- **Tartışma:** Durum makinesi mi davranış ağacı mı? Öneri durum makinesi, çünkü 4 durum için yeterli.

**F5 · Steam paketleme (≤20k)**
- **Adım:**
  - `BuildScript.Build` yazılır, `Unity -batchmode -quit -executeMethod` ile çağrılır.
  - Steamworks.NET eklenir; lisansı önce okunur. `steam_appid.txt` yalnız geliştirmede kullanılır.
  - steamcmd ile `app_build`/`depot_build` .vdf dosyalarından `beta` dalına yüklenir.
- **Araç:** steamcmd katalogda yok; resmi kurulum adımlarını ara-yeni-arac-kurulum-arastirma ajanı bulur. Yükleme öncesi git-yayin-oncesi-kontrol ajanı koşar.
- **Kapı:**
  - Başsız duman testi: build bir seviyeyi otomatik yükleyip kapanmalı.
  - sec-sir-tarayici: Steam kimlik bilgisi repoda olmamalı; env değerleri hiç basılmaz.
  - Build boyutu ölçülür.
- **Onay:** Yükleme dışa dönük bir iş, Ömer onaylamadan yapılmaz. Sürüm başına en çok 1 yükleme, yalnız `beta` dalına.
- **Tartışma:** Steam Workshop ile seviye paylaşımı bu işin kapsamı dışında; ayrıca karar gerekir.

**Kurallar ve kapanış:**
- Ekran kuralı: Unity yalnız `-batchmode -nographics` ile koşar. unity MCP için editörü Ömer açar; ajan editör penceresi açmaz.
- Testler sonnet alt ajanda koşar, ana bağlama yalnız sayılar ve kırmızı test adları gelir. Kapanış raporu ≤15 satır.
- Toplam bütçe yaklaşık 125k jeton.

## 7. Abonelik tabanlı SaaS için Stripe faturalandırma ekle: plan yükseltme/düşürme, webhook işleme, başarısız ödeme yeniden deneme, fatura PDF'i ve muhasebe dışa aktarımı.
### X
**Stripe abonelik faturalandırması.** Yığın bilinmiyor. Skill `departman-test-qa` test fazını yönetir.

**Faz 0: Keşif (15k)**
- Adım: Yığını ve kullanıcı/abonelik tablolarını belirle.
- Araç: Bash (`gh`) ve okuma.
- Convex bulunursa faz 2 Skill `convex-billing` ile yürür. Bulunmazsa resmi Stripe SDK kullanılır.

**Faz 1: Tasarım (dahil)**
- Adım: Hangi verinin nerede tutulacağına karar ver. Plan ve durum için doğru kaynak Stripe'tır; DB yalnız webhook ile güncellenen bir kopya tutar.
- Adım: İşlenecek webhook olaylarını belirle:
  - `customer.subscription.updated` ve `customer.subscription.deleted`
  - `invoice.paid` ve `invoice.payment_failed`
- Araç: Agent `otm-webhook-tasarimci`. İmza doğrulama, olay kimliğiyle tekil işleme ve hızlı 2xx yanıtı tasarlanır.
- Tartışma noktası: Fark ücretlendirme (proration) yöntemi `create_prorations` mı `always_invoice` mı olacak? Bu doğrudan para işidir ve Ömer karar verir. Konsey yok, veri var.

**Faz 2: Uygulama (50k)**
- Plan yükseltme/düşürme: `subscriptions.update` ve ödeme ekranı (checkout) için Stripe'ın hazır Customer Portal'ı kullanılır. Kendi arayüz yazılmazsa frontend-craft gerekmez.
- Başarısız ödeme yeniden denemesi: Stripe'ın kendi akıllı yeniden deneme (Smart Retries) ayarları kullanılır. Kendi kodumuz yalnız `payment_failed` olayında kullanıcıya bildirim gönderir ve erişimi kısıtlar.
- Fatura PDF'i: Stripe'ın `invoice.invoice_pdf` bağlantısı kullanılır. Ayrı bir PDF üretici yazılmaz.
- Muhasebe dışa aktarımı: Faturalar ve balance transactions sayfalı olarak CSV'ye yazılır.
- Kapı: Her ödeme ve iade isteğinde idempotency anahtarı. 3DS/SCA. PCI SAQ-A (kart verisi sunucuya hiç değmez). Webhook imzası doğrulanır. Yeniden deneme tavanı 3, üstel bekleme.
- İnceleyen: ecc:code-reviewer.

**Faz 3: Test ve güvenlik (12k)**
- Adım: SDK'nın test imza başlığıyla imzalanmış örnek olaylar hazırla. Şu durumlar sınanır:
  - aynı olayın iki kez gelmesi
  - imzanın bozuk olması
  - olayların sırasız gelmesi
  - plan düşürmede fark ücretinin doğru hesaplanması
  - CSV'deki toplamların Stripe toplamlarıyla eşleşmesi
- Araç: Skill `departman-test-qa`.
- Kapı: test yeşil · semgrep 0 yüksek bulgu · gitleaks 0 bulgu (Stripe anahtarı yalnız ortam değişkeninde).
- Arayüz eklenirse ek kapı: LCP ≤2.5 s, CLS ≤0.1, INP ≤200 ms, erişilebilirlikte 0 ciddi ihlal.
- KVKK: Kişisel veri en aza indirilir. Fatura saklama süresi (VUK/TTK) muhasebeyle teyit edilir.
- İnceleyen: ecc:security-reviewer (webhook, anahtarlar, KVKK).

**Faz 4: Yayın ve kapanış (3k)**
- Adım: Önce Stripe test modunda staging. Canlı anahtara geçiş Ömer'in onayıyla yapılır.
- Adım: Webhook uç noktası kaydedilir. Geri alma için eski uç nokta devre dışı bırakılır.
- Araç: `gh` (PR ve CI).
- Kapanış: test · semgrep · gitleaks · kanıt · rapor.

**Toplam:** ~80k

Çıkardığım adaylar:
- İş 6: blender-oturum, strix, qa-yuk-testi, platform-detection.
- İş 7: pricing-page, animation-systems, bl-glb, fatura-kutusu, taste-skill, omni-webhooks, git-yeniden-kullanilabilir-is-akisi, opensource-pipeline.

Risk: Stripe CLI (`stripe listen`) ve steamcmd kurulu listede yok, o yüzden planlarda ikisini de kullanmadım. Webhook testleri yalnız imzalı örnek olaylara dayanıyor; canlı akışı staging'de ayrıca denemek gerekecek.
### Y
**Varsayımlar:** Mevcut SaaS reposu ve yığını kullanılır. Stripe yalnız test modunda çalışır. Türkiye'deki müşteriler için e-Arşiv faturası zorunlu olabilir.

**F0 · Keşif ve karar (≤8k jeton)**
- **Adım:** İlgili departman-* müdür skill'i açılır. `graphify query "auth user plan payment"` çalıştırılır. Payments & Billing Engineer ajanı yığına uygun SDK'yı seçer (Stripe.net ya da stripe-node). Kabul ölçütleri `dalga.md`'ye yazılır.
- **Öğrenim notu:** İlk iş kısıtlı (restricted) Stripe anahtarı oluşturmak.
- **Tartışma 1:** Stripe'ın barındırdığı Checkout ve Customer Portal mı, özel arayüz mü?
  - Öneri barındırılan çözüm: PCI kapsamı SAQ A'da kalır; yükseltme, düşürme ve kart güncelleme hazır gelir.
  - Özel arayüz seçilirse önce /frontend-craft yüklenir.
- **Tartışma 2:** Asıl kayıt Stripe'ta tutulur. Yerel veritabanında yalnız `subscriptions(status, price_id, current_period_end)` aynası olur.

**F1 · Kurulum (≤10k)**
- **Adım:**
  - Stripe CLI kurulur. Katalogda ADAY durumunda, kurulu değil. Lisansı ara-lisans-kontrol okur, kurulum adımlarını ara-yeni-arac-kurulum-arastirma bulur.
  - Stripe MCP kurulur (katalog kararı KUR). Yalnız test anahtarıyla bağlanır; izinleri ajn-mcp-kurulum-denetci denetler.
  - Ürün ve fiyatlar kodla değil, CLI fixture ile oluşturulur.
- **Kapı:** sec-sir-tarayici ve gitleaks. Anahtar yalnız env'de durur, değeri hiçbir komutla basılmaz.

**F2 · Abonelik, yükseltme ve düşürme (≤25k)**
- **Adım:**
  - Checkout Session `mode=subscription` ile açılır.
  - Portal ayarı: yükseltme anında ve kıst hesaplı yapılır (`create_prorations`); düşürme dönem sonunda geçerli olur (subscription schedule).
  - Erişim kararı yerel aynadan okunur.
- **Araç:** Payments & Billing Engineer ajanı; yığın .NET ise dn-webapi-endpoint.
- **Kapı:** qa-api-test. Stripe test clock ile kıst hesaplı fatura tutarları doğrulanır.
- **Tartışma:** Yükseltme anında mı, dönem sonunda mı geçerli olsun?

**F3 · Webhook (≤25k)**
- **Adım:**
  - İmza ham gövdeyle `constructEvent` üzerinden doğrulanır.
  - Her olay `event.id` tekil tablosuna yazılır; aynı olay iki kez işlenmez.
  - Uç hemen 2xx döner, asıl iş kuyruğa gider.
  - Olaylar sırasız gelebilir; bu yüzden nesnenin güncel hali API'den yeniden çekilir.
- **Olaylar:** `checkout.session.completed`, `customer.subscription.*`, `invoice.paid`, `invoice.payment_failed`, `invoice.finalized`.
- **Araç:** otm-webhook-tasarimci ve be-mesaj-guvenilirligi ajanları.
- **Kapı:** Her olay `stripe listen --forward-to` ve `stripe trigger` ile denenir. Ayrıca çift teslim testi yapılır ve geçersiz imzanın 400 döndüğü doğrulanır.
- **İnceleme:** ecc:security-reviewer ve sec-owasp-top10.

**F4 · Başarısız ödeme ve yeniden deneme (≤15k)**
- **Adım:**
  - Smart Retries ve hatırlatma e-postaları Stripe Billing ayarlarından açılır; kod yazılmaz.
  - Uygulama tarafı: `past_due` durumunda uyarı bandı ve ek süre; `unpaid` ya da `canceled` durumunda erişim kapanır.
  - Stripe'a yapılan çağrılara timeout, yeniden deneme ve idempotency key eklenir (be-dayaniklilik-kaliplari).
- **Kapı:** Test clock ile 4 yeniden deneme simüle edilir; reddedilen test kartı `4000 0000 0000 0341` kullanılır.
- **Tartışma:** Ek süre kaç gün olsun? Bu bir iş kararı, Ömer verir.

**F5 · Fatura PDF'i (≤15k)**
- **Adım:**
  - Stripe faturanın PDF'ini zaten üretiyor (`invoice.invoice_pdf`); bunu listelemek için kod gerekmez.
  - Türkiye'de Stripe PDF'i yasal fatura sayılmaz. GİB e-Arşiv için `invoice.paid` olayında bir entegratör API'si üzerinden fatura kesilir.
- **Araç:** departman-belge; özel PDF tasarımı istenirse dok-pdf-uretici.
- **Kapı (KVKK):** sec-kvkk-gdpr-kontrol ve pia-generation. VUK'a göre fatura verisinin 10 yıl saklanması gerekir.
- **Kritik tartışma:** Stripe PDF'i yeterli mi, yoksa entegratör mü gerekiyor? Müşterilerin ülkesine bağlı; kararı Ömer verir.

**F6 · Muhasebe dışa aktarımı (≤15k)**
- **Adım:** `balance_transactions` ve `invoices` verileri CSV'ye aktarılır. Biçim: UTF-8 BOM, `;` ayraç, Türkçe ondalık. Tutarlar tam sayı kuruş olarak tutulur.
- **Araç:** otm-csv-temizleyici ve otm-veri-esleme ajanları.
- **Kapı:** Mutabakat testi: CSV toplamı Stripe ödeme (payout) toplamına eşit olmalı.

**F7 · Kapanış (≤10k)**
- **İnceleme:** Payments & Billing Engineer, ecc:security-reviewer ve sec-pci-dss-kapsam.
- **Testler:** Sonnet alt ajanda koşar.
- **Tavanlar:**
  - Test modunda koşu başına en çok 200 API çağrısı.
  - Canlı moda geçiş Ömer'in onayıyla olur. Canlıda en çok 1 duman testi işlemi yapılır: en küçük plan, sonra iade edilir.
- **Toplam bütçe:** Yaklaşık 125k jeton.

---
Katalog iki iş için tek Bash çağrısında sorgulandı. Bunu yapmadım: departman-* skill adlarını ve repo yığınını kontrol etmedim. Riskler:
- **İş 6:** steamcmd katalogda yok, kurulum adımları sonradan araştırılacak.
- **İş 7:** e-Arşiv entegratörü seçilmezse Türkiye'deki müşterilere kesilen faturalar yasal olmaz.

## 8. package.json'daki lodash sürümünü 4.17.21'e yükselt.
### X
**Faz 1: Keşif** (~1k jeton)
- Adım: `package.json` içinde lodash satırını Grep ile bul. Bağımlılık mı devDependency mi, aralık `^`, `~` ya da sabit mi, bakılır. Lockfile türü de belirlenir (npm, pnpm ya da yarn).
- Araç: Grep, `npm ls lodash` ile dolaylı kopyalar görülür.
- Tartışma: Mevcut aralık biçimi korunur, yani `^4.17.21` ya da sabit `4.17.21` olur. Dolaylı eski kopyalar için `overrides` eklenmez. Yalnız rapora yazılır.

**Faz 2: Değişiklik** (~1k)
- Adım: Projenin paket yöneticisiyle kurulur: `npm install lodash@4.17.21`. Bu komut hem `package.json` hem lockfile'ı günceller. Elle düzenleme yapılmaz.
- Kapı: `git diff --stat` ile yalnız `package.json` ve lockfile değişmiş olmalı.

**Faz 3: Doğrulama** (~1.5k)
- Kapı (test): `npm test`, ardından build betiği varsa `npm run build`.
- Kapı (güvenlik): `npm audit --omit=dev`. Lodash kaynaklı bulgu sayısı sıfır olmalı.
- İnceleyen: Ayrı ajan yok, çünkü değişiklik 10 satırın altında. Dolaylı kopya varsa rapora tek satır yazılır.
### Y
**F0 Keşif** (~1k)
- **Adım:** `package.json` içinde lodash'ın mevcut sürümüne, yazım biçimine (`^`/`~`/tam) ve dolaylı kopyalara bakılır.
- **Araç:** Grep ve `npm ls lodash`.
- **Kapı ve karar:** Mevcut sürüm 4.17.21'den büyükse bu bir sürüm düşürme olur. O durumda iş durur ve Ömer'e DUR raporu verilir.

**F1 Yükseltme** (~2k)
- **Adım:** Mevcut yazım biçimi korunur, `npm install lodash@4.17.21` çalıştırılır ve lock dosyası birlikte güncellenir.
- **Araç:** npm CLI. Proje pnpm veya yarn kullanıyorsa lock dosyasına göre o araç seçilir.
- **Tartışma noktası:** Dolaylı kopyalar 4.17.21'in altında kalırsa `overrides` eklenip eklenmeyeceğine karar verilmeli. İstenmediği için varsayılan olarak eklenmez, yalnız raporda yazılır.

**F2 Kapı** (~2k)
- **Test:** `npm test` ya da projenin test betiği çalışır.
- **Güvenlik:** `npm audit --omit=dev` çalışır. 4.17.21, CVE-2021-23337 (template komut enjeksiyonu) ve CVE-2020-28500 (ReDoS) açıklarını kapatır.
- **İnceleme:** Ayrı inceleme ajanı gerekmez; diff 2 satır artı lock dosyası.

**Toplam bütçe:** ~5k.

## 9. Bir PNG logoyu 512x512 WebP'ye dönüştür.
### X
**Faz 1: Girdi kontrolü** (~1k)
- Adım: Kaynak PNG'nin boyutu, en-boy oranı ve alfa kanalı Pillow ile okunur: `python -c "from PIL import Image; ..."`.
- Tartışma: Bu işin tek kritik kararı şu: logo kare değilse kırpılmaz. Oran korunur ve logo 512×512 şeffaf tuvale ortalanır. Kaynak 512 pikselden küçükse büyütme bulanıklık yaratır. Bu durumda rapora not düşülür, SVG kaynağı varsa o tercih edilir.

**Faz 2: Dönüşüm** (~1k)
- Araç: Pillow. Sırası `Image.thumbnail((512,512), LANCZOS)`, ardından RGBA tuvale yapıştırma, sonra `save("logo.webp", "WEBP", lossless=True)`. Logo düz renkli olduğu için kayıpsız kaydedilir. Pillow yoksa `cwebp -lossless -resize` kullanılır.
- Çıktı yeni dosyadır, kaynak PNG'nin üzerine yazılmaz.

**Faz 3: Kapı** (~1k)
- Kapı: Pillow ile `size==(512,512)` ve `mode=="RGBA"` kontrol edilir. Ardından çıktı Read ile görsel olarak açılır, kenar ve şeffaflık bozulmamış olmalı.
- İnceleyen: Yok, iş tek adımlık.
### Y
**F0 Keşif** (~1k)
- **Adım:** Kaynak PNG'nin boyutuna, en-boy oranına ve alfa kanalı olup olmadığına bakılır. Aynı logonun SVG'si varsa o kaynak olarak tercih edilir.
- **Araç:** Python Pillow (`Image.open(...).size`, `.mode`).

**F1 Dönüştürme** (~2k)
- **Adım:** Logo, oranı korunarak (contain) şeffaf 512×512 tuvalin ortasına yerleştirilir ve lossless WebP olarak kaydedilir.
- **Araç:** Pillow tek seferlik bir satırla: `thumbnail` → `Image.new("RGBA", (512, 512), (0, 0, 0, 0))` → `paste` → `save(..., "WEBP", lossless=True)`. Pillow yoksa `magick` ya da `cwebp` kullanılır.
- **Tartışma noktası:** Kare olmayan logoda kırpma mı, boşluk ekleme mi? Varsayılan boşluk eklemek; kırpma logo kaybettirir.
- **Uyarı:** Kaynak 512'den küçükse büyütme bulanıklaştırır. Bu durumda Ömer'e yazılır.

**F2 Kapı** (~1k)
- **Kontrol:** Pillow ile `size == (512, 512)` ve `mode == "RGBA"` doğrulanır, ardından çıktı Read ile görsel olarak incelenir.
- **Ekran kuralı:** Hiçbir görüntüleyici açılmaz.
- **İnceleme:** Ajan gerekmez.

**Toplam bütçe:** ~4k.

## 10. Python betiğindeki print çağrılarını logging.info ile değiştir.
### X
**Faz 1: Keşif** (~1.5k)
- Adım: `print(` çağrıları Grep ile `-n` kullanılarak listelenir. Özel durumlar ayrılır: `file=sys.stderr`, `end=`/`sep=` argümanları ve stdout'u okuyan testler (`capsys`).
- Tartışma 1: `logging`'in varsayılan düzeyi WARNING'dir. Yapılandırma olmadan `info` mesajları görünmez. Bu yüzden `if __name__ == "__main__":` içine `logging.basicConfig(level=logging.INFO, format="%(message)s")` eklenir.
- Tartışma 2: `logging` stdout'a değil stderr'e yazar. Betiğin çıktısı boru hattıyla başka bir programa veriliyorsa bu değişiklik o kullanımı bozar. Öyle bir kullanım varsa `basicConfig(stream=sys.stdout)` kullanılır, kanıt Grep ile aranır.

**Faz 2: Değişiklik** (~1.5k)
- Adım: Edit ile `print(x)` → `logging.info(x)` yapılır. Birden çok argüman varsa f-string yerine `logging.info("%s %s", a, b)` biçimi kullanılır. Ek olarak `import logging` gelir.
- `sep`/`end` kullanan satırlar çevrilmez, rapora yazılır.

**Faz 3: Kapı** (~1.5k)
- Kapı: `ruff check --select T201` ile kalan `print` sayısı sıfır olmalı. Betik eski ve yeni haliyle çalıştırılıp çıktılar karşılaştırılır, mesaj metinleri aynı olmalı.
- Kapı (test): `pytest` çalıştırılır. `capsys` kullanan testler `caplog`'a geçirilir.
- İnceleyen: Ayrı ajan yok, fark küçük.

Hiçbir dosya yazılmadı ya da değiştirilmedi. Paket yöneticisi türü, logo boyutu ve betiğin stdout tüketicisi kontrol edilmedi. Planlar varsayılan durumları esas alıyor.
### Y
**F0 Keşif** (~2k)
- **Adım:** Betikteki `print(` satırları ve `sep`, `end`, `file=sys.stderr` argümanları bulunur.
- **Adım:** stdout'u okuyan çağıranlar (pipe, `subprocess`, testler) aranır.
- **Araç:** Grep (`-n`) ve Read (dar aralık).
- **Tartışma noktası:** logging varsayılan olarak stderr'e yazar. stdout'u ayrıştıran bir çağıran varsa bu davranış değişikliği onu kırar; o durumda DUR raporu verilir.

**F1 Değişiklik** (~3k)
- **Adım:** `import logging` eklenir ve her `print(a, b)` → `logging.info("%s %s", a, b)` olur.
- **Adım:** `logging.basicConfig(level=logging.INFO, format="%(message)s")` yalnız `if __name__ == "__main__":` içine konur. Bu olmazsa INFO kayıtları hiç görünmez.
- **Tartışma noktası:** `file=sys.stderr` olan print'ler warning/error mı olmalı? İstek "info" dediği için info kalır, fark raporda belirtilir.

**F2 Kapı** (~1k)
- **Test:** `python -m py_compile`, varsa pytest.
- **Kontrol:** Grep ile kalan `print(` sayısının 0 olduğu doğrulanır; ruff varsa `ruff check --select T201`.
- **İnceleme:** ≤10 satırlık değişiklik için yalnız testler yeter. Daha büyükse `ecc:code-reviewer` incelemesi.

**Toplam bütçe:** ~6k.

---
Atladıklarım: departman-* skill'lerini açmadım, gerçek dosyaları incelemedim; yollar ve sürümler henüz bilinmiyor.
Risk: lodash 4.17.21 sonrasında yeni bir 4.x yaması çıkmış olabilir (hatırladığım kadarıyla CVE-2025-13465, `_.unset`/`_.omit`; doğrulamadım). `npm audit` bunu işaretlerse 4.17.21'de kalıp kalmamayı Ömer seçmeli.
