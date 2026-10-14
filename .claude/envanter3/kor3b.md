## 1. Küçük bir muhasebe bürosu için 5 sayfalık pazarlama sitesi yap: KVKK uyumlu iletişim formu ve çerez bildirimi, SEO, güvenlik testi, Hostinger'a yayın.
### X
**Varsayım:** Site statik kurulacak (Astro static çıktısı), form PHP ile çalışacak. Analitik yoksa çerez bildirimi tek satırlık bir bilgi notuna iner.

**F0 Kabul ölçütleri (5k)**
- Önce `departman-guvenlik` ve `departman-surec-git-yayin` açılır.
- Kabul ölçütleri `pln-kabul-olcutleri` ajanıyla yazılır, `.claude/dalga.md`'ye ≤30 satır olarak kaydedilir.
- **Tartışma: form nereye gider?**
  - Formspree gibi bir dış hizmet, verinin yurt dışına aktarımı demek. Bu, KVKK md. 9 kapsamında ek yükümlülük doğurur.
  - **Öneri:** Hostinger'da PHP `mail()` ile işle, veri saklama.

**F1 Bilgi mimarisi ve tasarım (25k)**
- Sayfalar: Ana sayfa, Hizmetler, Hakkımızda, SSS, İletişim. Yapı `marketing-skills:site-architecture` ile çıkarılır.
- Arayüz kuralı gereği önce `/frontend-craft` yüklenir, ardından `fe-tasarim-yonu` ve `fe-astro`.
- **Kapı:** frontend-craft ekran görüntüsü döngüsü, `playwright-cli` headless. 375, 768 ve 1440 piksel genişlikte denenir.
- **İnceleyen:** `UI Finish-Gate Reviewer`.

**F2 SEO (15k)**
- `marketing-skills:seo-audit`, `marketing-skills:schema` (AccountingService ve LocalBusiness JSON-LD), `fe-meta-seo-duzeltici`.
- `sitemap.xml`, `robots.txt` ve canonical eklenir.
- **Kapı:** `chrome-devtools` MCP headless Lighthouse ölçümü. SEO ≥95, performans ≥90, LCP <2,5 sn.
- Yayından sonra `gsc` MCP ile sitemap gönderilir.

**F3 KVKK (15k)**
- Aydınlatma metni, açık rıza metni ve çerez metni `policy-monitor` ile yazılır. İşleme amacı `use-case-triage` ile netleştirilir.
- Formda şunlar olur:
  - Önceden işaretlenmemiş onay kutusu,
  - Aydınlatma metnine bağlantı,
  - Yalnız gerekli alanlar (veri minimizasyonu),
  - Saklama süresinin yazılması.
- **Kapı:** `sec-kvkk-gdpr-kontrol` ajanı veri akışını çıkarır. Hukuki metin son halinde avukat incelemesi notu düşülür.
- **Tartışma: analitik olacak mı?**
  - Analitik eklenirse çerez onay yönetimi (CMP) ve önceden onay gerekir.
  - **Öneri:** Analitik yok.

**F4 Güvenlik ve erişilebilirlik (20k)**
- PHP form koruması: honeypot, IP başına hız sınırı, girdi temizleme, başlık enjeksiyonu kontrolü (`sec-xss-csrf-denetci`).
- `.htaccess` ile CSP, HSTS ve X-Frame-Options (`sec-guvenlik-baslik`).
- **Kapılar:**
  - `gitleaks` 0 bulgu.
  - `strix` yalnız kendi staging adresine, en çok 1 koşu, 20 dakika. Yüksek önemde bulgu kalmayacak.
  - `qa-erisilebilirlik-testi`: axe ile 0 kritik bulgu, ayrıca klavyeyle gezinme denemesi.
- **İnceleyen:** `sec-cikis-oncesi-guvenlik`.

**F5 Yayın (10k)**
- Yayından önce açık onay alınır. Yayın dışarıya dönük bir adım.
- `hostinger` MCP ile dosya yükleme, SSL ve DNS ayarı; en çok 15 çağrı. Destek: `deploy-app`.
- **Kapı:** `git-yayin-oncesi-kontrol` ajanı.
- **Duman testi:** `playwright-cli` headless ile:
  - 5 sayfa 200 dönüyor mu,
  - Form gönderilince e-posta geliyor mu,
  - HTTP adresi HTTPS'e yönleniyor mu,
  - Güvenlik başlıkları yerinde mi.

**Toplam:** ~90k jeton.
### Y
Varsayım: statik HTML/CSS ve tek PHP form işleyici kullanılacak (Hostinger paylaşımlı hosting PHP destekliyor). Analitik yok, bu yüzden yalnız zorunlu çerez ve bilgi bandı yeterli. Analitik eklenirse onay alınmadan script yüklenmez. 5 sayfa: Ana · Hizmetler · Hakkımızda · SSS · İletişim. KVKK ve çerez metinleri footer'da durur.

**F0 Kurulum · 2k** — departman-guvenlik → departman-surec-git-yayin açılır, /frontend-craft yüklenir (kural sırası: frontend-craft > impeccable > ui-ux-pro-max). dalga.md'ye karar, kabul ölçütü ve durum yazılır.
**F1 Araştırma · 15k**
- İçerik ve anahtar kelime haritası: marketing-skills:content-strategy.
- Metinler: policy-monitor ile aydınlatma metni, çerez politikası ve İYS ticari ileti rızası (ayrı kutu).
- Kapı: sayfa listesi, form alanları ve saklama süresi dalga.md'de yazılı.
**F2 Tasarım + uygulama · 50k**
- frontend-craft: marka kararı → referans eşleme → ekran görüntüsü döngüsü.
- SEO: fe-meta-seo-duzeltici ile her sayfaya title, description, canonical ve OG. Ayrıca robots.txt, sitemap.xml ve AccountingService JSON-LD.
- Form: sunucu tarafında doğrulama, CSRF token, honeypot, IP başına hız sınırı ve mail başlık enjeksiyonu engeli. Kişisel veri diske ya da loga yazılmaz. "Aydınlatma okundu" ile "ticari ileti rızası" ayrı onay kutularıdır.
- `.htaccess` ile CSP, HSTS, nosniff ve Referrer-Policy: sec-guvenlik-baslik.
- İnceleme: fe-tasarim-incele, UI Finish-Gate Reviewer, ecc:code-reviewer, ardından frontend-craft Bölüm 6 tur raporu.
**F3 Test + güvenlik · 12k**
- e2e: qa-e2e-playwright ile playwright-cli, headless Chrome. Form başarı, hata ve hız sınırı; çerez bandı; 5 sayfa gezinme.
- a11y: qa-erisilebilirlik-testi (axe-core ve klavye turu), ciddi ihlal 0 olmalı.
- SEO/performans: marketing-skills:seo-audit ve chrome-devtools MCP Lighthouse. Eşikler: SEO ≥95, LCP ≤2,5 sn, JS ≤50 KB.
- KVKK: sec-kvkk-gdpr-kontrol ile veri akışı, saklama süresi ve silme talebi kanalı.
- Güvenlik:
  - semgrep (sec-sast-kosucu) ve gitleaks (sec-gitleaks-gecmis).
  - sec-owasp-top10 form için.
  - strix yalnız kendi önizleme alan adına, en çok 1 koşu.
  - ZAP baseline Docker varsa koşar, yoksa raporda gerekçesi yazılır.
- İnceleme: ecc:security-reviewer.
**F4 Yayın + kapanış · 3k**
- git-yayin-oncesi-kontrol ile go/no-go kararı.
- hostinger MCP: önce önizleme alt alan adı, sonra prod. En çok 2 yayın çağrısı.
- Geri alma: yayından önce dosya zip'i ve Hostinger yedeği alınır.
- Kontroller: SSL/DNS bakılır, canlıda 1 form gönderimiyle duman testi yapılır.
- Kapanış raporu: commit · test · CI · sapma.

Konsey: yok. Statik site; görsel yönü frontend-craft'ın marka kararı belirler, geri dönüşü zor karar yok.
Kullanılmayanlar:
- netlify: hedef Hostinger.
- swup, Vengeance UI, motionmaxxing: animasyon istenmedi.
- Claude Security, firecrawl, lighthouse CLI: kurulu değil; aynı işi strix, semgrep ve chrome-devtools karşılıyor.
- ab-testing, otm-pazarlama-otomasyonu: kapsam dışı.

## 2. ASP.NET Core ile randevu sistemi API'si: JWT kimlik doğrulama, EF Core + PostgreSQL migration, rol bazlı yetki, xUnit testleri ve OpenAPI dokümanı.
### X
Varsayım: güncel .NET, minimal API ve endpoint grupları kullanılacak. Roller Admin, Personel, Müşteri. Postgres yerelde Docker'da çalışır.

**F0 · 2k** — departman-backend-dotnet → departman-veri-db sırası, dalga.md. Doküman kaynağı: mslearn MCP (JWT bearer, AddOpenApi) ve context7 (Npgsql).
**F1 Tasarım · 8k**
- dn-efcore-modelleme: Identity kullanıcısı, Service, StaffSchedule, Appointment (UTC timestamptz, Status).
- Çift rezervasyonu Postgres exclusion constraint (btree_gist, tstzrange) engeller; uygulama kontrolü ikinci kat.
- sec-yetkilendirme-matrisi ile rol×eylem matrisi çıkarılır. Müşteri yalnız kendi randevusunu görür (BOLA).
- Kapı: matris ve kabul ölçütleri dalga.md'de.
- Konsey noktası (auth): yok. Identity parolayı hash'ler (öğrenim 52), JWT zaten istenmiş ve harici IdP istenmemiş; iki makul seçenek yok.
**F2 Uygulama · 35k**
- dotnet-webapi ve dn-aspnet-core: endpoint'ler, ProblemDetails, middleware sırası.
- dn-identity-auth:
  - Algoritma sabit; iss, aud ve exp doğrulanır.
  - Erişim token'ı 15 dk; refresh token'da rotasyon ve iptal var.
  - Anahtar user-secrets ya da env'de durur.
  - Yetki policy tabanlı.
  - Login'e RateLimiter eklenir.
- dn-efcore-migration: InitialCreate, constraint için `migrationBuilder.Sql`, Down() yazılır.
- İnceleme: her PR'da ecc:csharp-reviewer.
**F3 Test · 12k**
- Araçlar: dn-xunit-test-yazar ve ecc:csharp-testing.
- Birim testler: çakışma kuralı, saat dilimi ve DST sınırları.
- Entegrasyon: WebApplicationFactory ve Testcontainers PostgreSQL. Constraint gerçek veritabanında sınanır; InMemory kullanılmaz.
- Senaryolar: tokensız 401 · yanlış rol 403 · başkasının randevusu 404 · çakışma 409 · süresi dolmuş token 401.
- Migration gidiş-dönüş: `dotnet ef database update 0` sonra tekrar ileri, temiz geçmeli.
- Koşu: `rtk dotnet test` ve `DOTNET_NOLOGO=1` (`--nologo` MTP'yi kırıyor).
- Bitirmeden önce inc-dogrulama-oncesi-bitis.
**F4 Güvenlik + KVKK · 8k**
- sec-jwt-denetci, sec-api-guvenlik (BOLA; mass assignment'a karşı ayrı DTO), sec-owasp-top10.
- semgrep ve gitleaks.
- sec-kvkk-gdpr-kontrol: ad, telefon, e-posta için saklama süresi, silme uç noktası, loglarda PII olmaması.
- İnceleme: ecc:security-reviewer ve inc-mimari-inceleme.
**F5 Doküman + kapanış · 3k**
- dn-openapi-dokuman: AddOpenApi, Bearer şeması, yanıt tipleri, örnekler. Kapı: `/openapi/v1.json` 200 dönüyor testi.
- `dotnet ef migrations script --idempotent` artefaktı üretilir. Prod'a yalnız yerelde denendikten sonra ve onayla uygulanır (öğrenim 53).

Kullanılmayanlar:
- auth0, omni-auth, netlify-identity: Identity seçildi.
- drizzle-docs: EF Core kullanılıyor.
- create-datadriven-aspnetcore: UI yok.
- api-platform-engineer: SDK ve gateway kapsam dışı.
- dok-api-dokumani: OpenAPI yeterli.
- Claude Security: kurulu değil.
### Y
**Varsayım:** .NET 9, minimal API, tek kiracılı (multi-tenant yok). Refresh token istenmediği için yok; erişim tokeni 15 dakika.

**F0 Plan (8k)**
- Sıra: `departman-backend-dotnet`, sonra `departman-veri-db`, sonra `departman-guvenlik`.
- `pln-kabul-olcutleri` ile kabul ölçütleri yazılır. Roller: Admin, Personel, Müşteri.
- Rol ve eylem matrisi `sec-yetkilendirme-matrisi` ile çıkarılır.
- **Tartışma: ASP.NET Identity mi, kendi Users tablosu mu?**
  - **Öneri:** Identity. Parola hash'leme ve hesap kilitleme hazır geliyor.

**F1 Model ve migration (20k)**
- Model `dn-efcore-modelleme` ile kurulur. Zamanlar `timestamptz` ve UTC (`db-zaman-damgasi`).
- **Tartışma: randevu çakışması nerede engellenir?**
  - **Öneri:** Postgres'te `EXCLUDE USING gist (personel_id WITH =, tstzrange WITH &&)`. Uygulama tarafındaki kontrol eşzamanlı isteklerde yarışa açık.
- Migration `dn-efcore-migration` ile yazılır.
- **Kapılar:**
  - `dotnet ef migrations has-pending-model-changes` temiz çıkar.
  - Testcontainers ile açılan boş PostgreSQL'e migration uygulanır, geri alma (down) denenir.

**F2 Kimlik doğrulama ve yetki (20k)**
- `dn-identity-auth` ile JWT Bearer ve rol politikaları.
- Doğrulanacaklar: issuer, audience, lifetime, signing key. Anahtar user-secrets ya da ortam değişkeninde durur, değeri hiçbir komutla basılmaz.
- **Kapı:** `sec-jwt-denetci`. `alg:none` reddediliyor mu, süre dolunca 401 dönüyor mu, saat kayması toleransı (clock skew) ne kadar.
- **İnceleyen:** `ecc:security-reviewer`.

**F3 Uç noktalar (20k)**
- `dotnet-aspnetcore:dotnet-webapi` ve `dn-webapi-endpoint` ile:
  - Randevu oluştur, listele, iptal et.
  - Personel uygunluğu.
- Hatalar ProblemDetails biçiminde.
- Nesne düzeyi yetki: müşteri yalnız kendi randevusunu görür (BOLA önlemi).
- Test önce yazılır: kırmızısı görülmeden kod yok.

**F4 Testler (25k)**
- `dn-xunit-test-yazar` ve `ecc:csharp-testing`.
- **Birim:** çakışma kuralı, iptal penceresi.
- **Entegrasyon:** WebApplicationFactory, Testcontainers ve Postgres ile. Kapsananlar:
  - Matristeki her satır için 401/403 testi,
  - Eşzamanlı iki randevuda biri 409 almalı.
- **Kapı:** `rtk dotnet test` yeşil.
  - `--nologo` kullanılmaz, xunit.v3/MTP'de exit 5 veriyor. Yerine `DOTNET_NOLOGO=1`.
- Koşu bir alt ajana (sonnet) verilir; ana bağlama yalnız sayı ve kırmızı test adları döner.

**F5 OpenAPI ve güvenlik (15k)**
- Yerleşik `AddOpenApi` kullanılır: Bearer security scheme, örnekler, yanıt tipleri (`dn-openapi-dokuman`).
- **Kapılar:**
  - Üretilen `openapi.json`, `dil-openapi-sozlesme` ile incelenir.
  - `api-security-testing` (strix): yalnız yerel ortamda, en çok 1 koşu.
  - `gitleaks` 0 bulgu.
- KVKK: randevuda ad ve telefon gibi kişisel veri var. Loglarda kişisel veri olmamalı (`sec-loglama-gizlilik`).

**F6 Kapanış (5k)**
- `ecc:csharp-reviewer` diff incelemesi, ardından `departman-surec-inceleme`, sonra commit.

**Toplam:** ~115k jeton.

## 3. Three.js tarayıcı oyununa 2-4 kişilik çok oyunculu yarış modu ekle: WebSocket senkron, gecikme telafisi, skor tablosu ve hile önleme.
### X
**Varsayım:** Oyunun mevcut kodu önce `graphify query` ile okunur. Sunucu Node + `ws`, otoriter (authoritative) yapıda.

**F0 Keşif ve karar (15k)**
- Ajanlar: `oyn-ag-senkronu` (netcode tasarımı) ve `dil-websocket`. Skill: `threejs`.
- **Tartışma 1: `ws` mi, Colyseus mu?**
  - 2-4 oyuncu ve basit oda yapısı için `ws` yeter; yeni bağımlılık gerekmez.
  - Oda eşleştirme (matchmaking) istenirse Colyseus'a geçilir. Önce lisansı okunur.
- **Tartışma 2: istemci yalnız girdi mi gönderir, yoksa konum mu?**
  - **Öneri:** Yalnız girdi. Hile önlemenin temeli bu.
- Kararlar `pln-karar-kaydi` ile tek satır ADR olarak yazılır.

**F1 Ortak simülasyon (20k)**
- Araç fiziği istemci ve sunucunun ortak kullanacağı bir modüle taşınır: sabit adımlı, 30 Hz tick.
- **Kapı:** `node:test` determinizm testi. Aynı girdi dizisi aynı konumu vermeli.

**F2 Sunucu (25k)**
- Oda, en çok 4 oyuncu, geri sayım, tur ve checkpoint takibi.
- Gelen her mesaj şema ile doğrulanır (güven sınırı). Mesaj hız sınırı ve en büyük boyut tanımlanır.
- Kopan istemci için heartbeat ve yeniden bağlanma.

**F3 İstemci senkronu (25k)**
- Kendi araç: istemci tahmini (prediction) ve sunucuyla uzlaştırma (reconciliation).
- Diğer araçlar: 100 ms tamponla interpolasyon.
- Gecikme telafisi: checkpoint ve bitiş zamanını sunucu kendi tick'iyle belirler.
- **Kapı:** Node bot istemcileriyle ölçüm. 4 bot, 150 ms gecikme ve %5 jitter yapay olarak eklenir.
  - Hedef: uzlaştırmadaki konum hatası ortalama 0,5 birimin altında.
  - İstemci başına bant genişliği 10 KB/sn altında.

**F4 Hile önleme ve skor tablosu (20k)**
- Sunucu tarafı kontroller:
  - Hız ve ivme üst sınırı,
  - Checkpoint sırası,
  - En kısa tur süresi,
  - Tick atlama tespiti.
- Skor tablosuna yalnız sunucunun ölçtüğü süreler girer (SQLite, `db-sqlite`).
- **Kapılar:**
  - Hile testi: konum ışınlama, hız hilesi ve checkpoint atlama gönderen sahte istemciler reddedilmeli.
  - `gitleaks` 0 bulgu.
- **İnceleyen:** `ecc:security-reviewer`, mesaj işleyicilerine bakar.

**F5 Arayüz: lobi ve skor tablosu (20k)**
- Arayüz kuralı gereği önce `/frontend-craft`.
- **Kapılar:**
  - `qa-e2e-playwright` headless: 4 tarayıcı bağlamıyla tam bir yarış.
  - Skor tablosu ve lobi `qa-erisilebilirlik-testi` ile denenir.
  - Kare süresi bütçesi 16 ms (`chrome-devtools` MCP headless ile ölçülür).

**F6 Kapanış (8k)**
- `oyn-ag-senkronu` netcode diff'ini inceler, ardından `ecc:code-reviewer`.
- Bu dalgada yayın yok. Yayın istenirse WebSocket için nginx vekili `ops-nginx-ters-vekil` ile kurulur.

**Toplam:** ~135k jeton.

---

Atlananlar: Refresh token (2), analitik ve CMP (1), oda eşleştirme ve sunucu yayını (3) kapsam dışı bırakıldı. Oyun kodunun yapısı henüz okunmadı. Hostinger hesabında PHP `mail()` açık mı ve oyunun fiziği deterministik mi, ikisi de doğrulanmadı.

Riskler: Hukuki metinler avukat onayı olmadan yayına girmemeli. Oyunun fiziği deterministik değilse 3'teki F1 baştan yazım demek, iş büyür.
### Y
Varsayım: oyun şu an tek oyunculu ve fizik istemcide JS ile çalışıyor. Sunucu Node + ws olacak. Skor tablosu yarış içi sıralama ve yarış sonu sonuçlarından oluşur; kalıcı liderlik tablosu istenmedi.

**F0 · 2k** — oyun-gelistirme-paket ve threejs skill açılır. Lobi ve skor UI'ı için /frontend-craft yüklenir. `graphify query` ile döngü, fizik ve girdi haritası çıkarılır. dalga.md yazılır.
**F1 Ağ tasarımı · 15k**
- oyn-ag-senkronu:
  - Sunucu otoriter; 30 Hz sabit tick.
  - İstemci yalnız sıra numaralı girdi yollar.
  - Kendi araç: tahmin + uzlaştırma (onaylanmamış girdiler yeniden oynatılır). Diğer araçlar: ~100 ms tamponla interpolasyon.
  - Gecikme telafisi: bitiş ve checkpoint geçişini sunucu, alt-tick enterpolasyonla hesaplar.
- Mesajlar: join · input · snapshot · result. Oda 2–4 kişi; hazır olunca geri sayım başlar.
- dil-websocket: heartbeat, yeniden bağlanmada koltuk 10 sn tutulur, mesaj boyut sınırı, Origin kontrolü.
- Konsey noktası (en çok 1, ecc:council) yalnız mevcut fizik Node'da headless koşamıyorsa açılır. Soru: simülasyonu render'dan ayırmak mı, sunucuda basit fizik mi? Koşabiliyorsa konsey yok.
**F2 Uygulama · 50k**
- oyn-three-oyun-sahne: istemci ve sunucunun paylaştığı `sim.js` ayrılır; `server/` (ws), istemci ağ katmanı, lobi ve sıralama/sonuç DOM overlay'i yazılır.
- Hile önleme:
  - Sunucu istemciden konum kabul etmez.
  - Girdiler sınırlanır: direksiyon −1..1, gaz 0..1, tick başına en çok N girdi.
  - Checkpoint sırası ve en kısa tur süresi doğrulanır.
  - Skoru yalnız sunucu yazar; odaya giriş katılım tokenıyla.
- oyn-oyun-denge: çarpışma cezası ve geride kalanı yakalama ayarı.
- İnceleme: ecc:code-reviewer ve frontend-craft Bölüm 6.
**F3 Test + güvenlik · 12k**
- Determinizm: aynı girdi dizisi istemcide ve sunucuda aynı durumu vermeli.
- Hile testleri: sahte konum paketi, girdi seli, sıra dışı checkpoint → hepsi reddedilmeli.
- Ağ: ws vekiliyle 150 ms ±50 jitter. Uzlaştırma sapması eşik altında kalmalı, görünür sıçrama olmamalı.
- e2e: playwright-cli headless Chrome. 4 bağlam aynı odada yarışı bitirir, sonuçlar her istemcide aynı çıkar.
- Performans: chrome-devtools MCP izinde 4 oyuncuyla kare süresi p95 ≤16,7 ms.
- a11y: qa-erisilebilirlik-testi ile lobi ve skor overlay'i.
- Güvenlik: semgrep ve gitleaks.
- İnceleme: ecc:security-reviewer ve oyn-oyun-dokuman ile kapsam kontrolü.
**F4 Kapanış · 3k** — rapor: commit · test · CI · sapma.

Kullanılmayanlar:
- puppeteer, webapp-testing: öğrenim 47'ye göre tek tarayıcı aracı playwright-cli.
- webgpu-tsl: WebGPU istenmedi.
- blender, bl-glb: yeni model yok.
- lenis, scroll-rig, ThreeUI: scroll ya da hero bölümü yok.
- SEO ve KVKK kapıları: oyunda yalnız takma ad var, kişisel veri yok.
- strix, ZAP: HTTP yüzeyi yok; ws için F3'teki hile testleri ve dil-websocket kontrolü var.

---
Atlananlar: hiçbir işe başlanmadı, dosya yazılmadı. plan_kur.py yalnız 1 kez çağrıldı; ilk deneme Bash'in ters eğik çizgileri yutması yüzünden yol hatası verdiği için ikinci çağrıyla 1 kez daha koştu. Çıktının sıkıştırılmış kısmı (hash ile duran tam metin) geri çağrılmadı, planlar görünen kapı ve aday listesine dayanıyor.

Riskler:
- İş 3: mevcut oyun kodunu görmedim, fiziğin Node'da çalışıp çalışmadığı belli değil. Bu, planın en büyük belirsizliği.
- İş 2: Testcontainers Docker ister, makinede Docker olduğu doğrulanmadı.

## 4. Blender'da parfüm şişesi ürün sahnesi kur: modelleme, cam malzeme, stüdyo ışığı, turntable render ve web için 2 MB altı GLB dışa aktarımı.
### X
— Blender parfüm şişesi ürün sahnesi

**Kabul ölçütleri:** GLB 2 097 152 bayttan küçük olacak; glTF-validator 0 hata verecek; turntable 120 kare / 24 fps döngü olacak, ilk ve son kare dikişsiz birleşecek; tüm adımlar headless (`blender -b`) koşacak.

**Faz 0 · Oturum (2k)**
- Adım: Önce `Skill blender-oturum`, sonra `Skill blender-uretim` açılır.
- Araç: Tüm çalıştırma `tools/blender_cli.py` ile headless yapılır; `blender_bekci` kancası açık kalır.
- Kullanılmayan: `mcp__blender` canlı GUI ister, ekran kuralını çiğner.

**Faz 1 · Modelleme (15k)**
- Adım: `bl-modelleme-plani` gövde, boyun, sprey ve kapağın oranlarını çıkarır. Topoloji Subdivision + Solidify ile kurulur (cam kalınlığı 2–3 mm). Ölçek gerçek metre olur, transform uygulanır.
- Araç: `bl-python-betik` tek bir bpy dosyası yazar.
- Kapı: `blender_dogrula` ölçek, pivot ve topolojiyi denetler; `bl-gorsel-ani-kontrol` ters normal ve non-manifold arar.
- İnceleme: `bl-sahne-temizlik` (adlandırma, koleksiyon).

**Faz 2 · Cam malzeme (10k)**
- Adım: `bl-malzeme-kurucu` camı kurar: Principled, Transmission 1, IOR 1.45–1.5, roughness ~0.02. Sıvı ayrı bir iç mesh olur (IOR 1.33, renk Base Color'da). Kapak metal olur.
- Kapı: Malzemeler GLB'ye taşınabilmeli. Yalnız Principled kullanılır (KHR transmission/ior/volume), node-group kullanılmaz.

**Faz 3 · Stüdyo ışığı (10k)**
- Adım: `bl-isik-kurulumu` ve öğrenim 58–60 uygulanır:
  - Cam için anahtar:dolgu:kenar oranı 3:1:1.2.
  - Kameraya görünmeyen softbox emisyon düzlemleri.
  - Arka ışık üründen geniş ama dar.
  - Önce mat gri + krom küre ile sınanır.
- Araç: HDRI `varlik_indir` ile Poly Haven'dan (CC0) alınır.
- Kapı: `blender_gorunum` kare kanıtı üretir (4 Workbench + 1 Eevee kahraman).

**Faz 4 · Turntable (12k)**
- Adım: `bl-urun-turntable` ve `bl-animasyon-anahtar` kullanılır. Bir boş nesne 0°'den 357°'ye lineer döner. Render Cycles'ta yapılır (cam kırılması için). `bl-render-ayari` düşük örnek + denoise ayarlar. ffmpeg kareleri mp4/webm döngüye çevirir.
- Kapı: İlk ve son kare farkı ölçülür; gürültü `blender_gorunum` çıktısında gözle denetlenir.

**Faz 5 · GLB dışa aktarım (10k)**
- Adım: `bl-glb-disa-aktar` ayrı bir dışa aktarım kopyası hazırlar: modifier uygulanır, gerekirse decimate yapılır, dokular en çok 1024 px webp olur.
- Araç: `tools/glb_hat.py` sırasıyla meshopt + webp, validate ve inspect çalıştırır; önce/sonra KB verir.
- Kapı: Boyut tavanı + validator 0 hata + `blender-dogrulama` CLI GLB hattı.

**İnceleme:** bpy betiğine `ecc:code-reviewer`, sahneye `bl-sahne-temizlik`.

**Konsey:** Yok. Cycles/Eevee seçimi ve decimate oranı geri alınabilir, ölçüt sayısal.

**Kapanış (3k):** commit · test (`blender_dogrula` + `glb_hat` çıktısı) · CI · sapma. **Toplam ~62k.**

**Kullanılmayanlar:**
- Web kapıları (Lighthouse, a11y, SEO, ZAP): sayfa istenmedi; GLB boyut tavanı performans bütçesi yerine geçer.
- `fe-webgl-3d-hero`, `threejs`: istenen bir sahne sayfası yok.
- `blender_pisir`: cama pişirme gerekmez.
- BlenderKit, Cell Fracture: kurulu değil ya da işle ilgisiz.
- `blender-lab-mcp`: dosya sistemindeki yeri belirsiz.
### Y
**Varsayımlar:** referans görsel yok, sahne prosedürel kurulur. Ekran kuralı gereği Blender yalnız headless (`-b`) koşar. GLB three.js'te açılacak.
**Faz 0 · Kurulum (~5k):** önce `Skill blender:blender-oturum`, ardından `Skill blender-uretim`. Oturum `python tools/blender_oturum.py ac sise.blend --yeni` ile açılır. `blender_bekci` hook'unun açık olduğu doğrulanır. 3B departman müdür skill'inin adı katalogda çıkmadı; adı `Skill` listesinden kontrol edilir.
**Faz 1 · Modelleme (~15k):**
- Adımlar: gövde, boyun, kapak ve ayrı bir sıvı mesh'i. Sıvı mesh'i gövdeden %1 içeride durur, yüzeyler çakışmaz.
- Araçlar: plan için `Agent bl-modelleme-plani`; bpy betiği için `Agent bl-python-betik` ve `tools/blender_cli.py`.
- Kapı: koşmadan önce `bpy_kontrol` (bpy'de olmayan API'leri yakalar). Ardından `blender_dogrula` ölçeği (gerçek boyut, ~10 cm), pivotu ve topolojiyi denetler; manifold olmayan kenar ve ters normal sayısı 0 olmalı.
- İnceleme: `Agent bl-gorsel-ani-kontrol`.
**Faz 2 · Malzeme ve ışık (~15k):**
- Cam: Principled BSDF, transmission 1, IOR 1.45, roughness 0.02. Sıvıda volume absorption. Kapak metal.
- Işık: 3 nokta stüdyo ışığı ve Poly Haven'dan CC0 stüdyo HDRI'si. HDRI `varlik_indir` ile, karanlık bir dekor ortamı olarak indirilir.
- Araçlar: `Agent bl-malzeme-kurucu`, `Agent bl-isik-kurulumu`, `Agent bl-kamera-kompozisyon`.
- Kapı: `blender_gorunum` 4 Workbench görünümü ve 1 Eevee kahraman karesi üretir. Kareler Read ile tek tek açılıp göz kontrolünden geçer.
- **Tartışma noktası:** cam görüntüsü render'da ve web'de farklı çıkar. Render tarafında Cycles kostikleri ve kalınlık verir. glTF tarafında yalnız `KHR_materials_transmission` + `KHR_materials_volume` taşınır; sıvı rengi `attenuationColor` alanına eşlenmelidir. Karar: malzeme iki hedef için ayrı ayarlanır, render için ayrı bir kopya tutulur.
**Faz 3 · Turntable (~10k):**
- Adımlar: 120 kare, 360°. Döner obje değil kamera ve ışık takımıdır, böylece yansımalar akar. Cycles 128 örnek, OIDN gürültü giderme.
- Araçlar: `Agent bl-urun-turntable`, `Agent bl-render-ayari`. Render `gpu_kilit` altında, `.kos/kopru/arka.py` ile arka planda koşar. Video ffmpeg ile mp4 (h264) ve webm döngüsüne çevrilir.
- Kapı: kare sayısı 120 olmalı. İlk ve son kare arasındaki fark eşik altında kalmalı ki döngüde sıçrama olmasın.
**Faz 4 · GLB (~10k):**
- Adımlar: modifier'lar uygulanır. Render malzemesinin yerine web malzemesi konur. Dokular en çok 1k ve webp.
- Araçlar: `Agent bl-glb-disa-aktar`, ardından `python tools/glb_hat.py` (meshopt + webp → validate → inspect).
- Kapı: dosya < 2 097 152 bayt (assert). gltf-validator 0 hata vermeli. three.js yükleme testi Playwright ile headless koşar; MeshoptDecoder tanımlı olmalı ve konsolda hata çıkmamalı.
- **Tartışma noktası:** meshopt mi Draco mu? `glb_hat` meshopt kullanıyor, değiştirilmez. Tüketen sitenin decoder'ı bu yüzden yüklemesi gerekir.
- İnceleme: `Agent bl-sahne-temizlik` (adlandırma, kullanılmayan veri); `glb_hat` önce/sonra KB raporu sunar.
**Faz 5 · Kapanış (~3k):** `blender_oturum.py kapat`, ardından `graphify update .`. Kapanış raporu ≤15 satır.
**Atlananlar:** etiket/logo dokusu ve AR (`.usdz`) çıktısı istenmediği için plana alınmadı. `Skill threejs` ve `web-sahne-desenleri` gerekmedi; sitede bir hero sahne istenirse eklenir.

## 5. Instagram Reels için otomatik video hattı: uzun videodan en iyi 3 anı seç, dikey kırp, altyazı ekle, sesi normalize et, zamanlanmış yükleme.
### X
— Instagram Reels otomatik video hattı

**Kabul ölçütleri:**
- 1 uzun videodan 3 çakışmasız klip çıkacak: 1080×1920, 15–60 s.
- Altyazı videoya yakılacak.
- Ses −14 LUFS ±1 olacak, tepe en çok −1 dBTP.
- `--kuru` kipi yükleme yapmayacak.
- Aynı klip iki kez yayınlanmayacak.

**Faz 0 · Kararlar (6k)**
- Adım: Yükleme Instagram Graph API ile yapılır. Business/Creator hesabı ve Meta uygulaması gerekir. Video kamuya açık bir URL'den çekildiği için geçici barındırma gerekir.
- Varsayım: Reels için yerel zamanlama yok, bu yüzden yerel zamanlayıcı kullanılır. Bu ve 24 saatlik yayın sınırı `ara-kutuphane-dokuman` ile resmi dokümandan doğrulanır.
- Tavan: Koşu başına en çok 3 yayın çağrısı; LLM puanlaması en çok 1 çağrı.

**Faz 1 · Girdi ve transkript (5k)**
- Adım: Kaynak yerel dosya ya da `yt-dlp` olur (yalnız hakları sahip olunan içerik). `whisper-cli` SRT ve kelime zaman damgaları çıkarır. ffmpeg `ebur128` ses enerjisini, `scdet` sahne sınırlarını bulur.

**Faz 2 · En iyi 3 anın seçimi (8k)**
- Adım: `vid-kisa-klip-secici` ve `reel-plan` kanca ölçütleri kullanılır. Puan transkript + enerji + sahne sınırından oluşur. Klipler cümle sınırına hizalanır.
- Kapı: `vid-kare-cikarici` her klibin başı ve sonu için kare kanıtı verir.
- İnceleme: `vid-gecis-ve-ritim` ilk 3 saniyedeki kancayı denetler.
- Not: `autoclip-paket` aday; lisansı okunmadan alınmaz.

**Faz 3 · Render (12k)**
- Adım: `vid-ffmpeg-donusturucu` ve `vid-sosyal-video-bicim` kullanılır:
  - Kırpma `crop=ih*9/16:ih`, merkez ya da `cropdetect` ile yapılır. Bu bir kestirme; konuşan kişi kadrajdan kayarsa yüz takibine geçilir.
  - Ölçek 1080×1920.
  - Altyazı `subtitles=` (libass) ile yakılır: Türkçe font, alt güvenli alanın üstünde.
  - Ses için `vid-ses-duzeni` kullanılır: `loudnorm` iki geçiş, I=−14, TP=−1, LRA=11.
- Kapı: `ffprobe` H.264/AAC, çözünürlük ve fps'i denetler; `ebur128` ±1 LU ölçer; `vid-renk-uzayi` bt709 ve tv range'i denetler.

**Faz 4 · Yükleme ve zamanlama (15k)**
- Adım: Tek bir Python betiği yazılır, iki kipi olur: `--kuru` (yalnız render + plan) ve uygula.
  - Durum dosyası klip hash'ini media_id'ye bağlar; bu idempotent olmayı sağlar.
  - Yayın sırası: container oluşturulur, FINISHED durumu beklenir, sonra `media_publish` çağrılır.
  - `be-dayaniklilik-kaliplari`: timeout, jitter'lı tekrar, en çok 3 deneme.
- Zamanlama: `otm-zamanlanmis-gorev` ile Windows Görev Zamanlayıcı kurulur; `.kos/kopru/arka.py` (CREATE_NO_WINDOW) üzerinden kilit ve log ile koşar.
- Token Credential Manager'da ya da ortam değişkeninde tutulur; değeri hiç basılmaz.
- Kapı:
  - `sec-sir-tarayici` + gitleaks.
  - Kuru koşu 2 kez çalıştırılır, aynı çıktıyı vermeli.
  - pytest seçimi, idempotent davranışı ve hata yolunu Graph API mock'u ile sınar.
- İnceleme: kod için `ecc:code-reviewer`; zamanlayıcı açılmadan önce `inc-uretim-hazirligi`.

**Faz 5 · İlk canlı koşu (2k):** Yayın dışa açık olduğu için Ömer'in onayı gerekir. Önce 1 klip, sonra 3 klip. Videoda başka kişiler varsa rıza, müzik varsa lisans gerekir; gerekirse `sec-kvkk-gdpr-kontrol` çalışır.

**Konsey:** Yok. Düz yanık altyazı için ffmpeg yeter, Remotion/HyperFrames gerekmez. Tetik basit bir zamanlayıcı, kuyruk gerekmez.

**Kapanış (3k):** commit · test · CI · sapma. **Toplam ~51k.**

**Kullanılmayanlar:**
- remotion, hyperframes: animasyonlu altyazı istenmedi.
- fal, Higgsfield, HeyGen, Blotato: üretim aracı değil, ücretli.
- `premiere-pro` MCP: GUI açar, ekran kuralını çiğner.
- n8n: tek betik yeterli.
- OpenChatCut: kurulu değil.

---
`plan_kur` çıktısının bir kısmı sıkışmış geldi (konsey satırı ve Blender jeton bütçesi); tam metni almadım, konsey kuralını ve Blender bütçesini bildiğim haliyle yazdım. "Ek sorgu yapma" talimatı yüzünden departman-* skill'lerini açmadım. Graph API'de Reels zamanlaması olmadığı ve yayın sınırı varsayım; Faz 0'da doğrulanacak.
### Y
**Varsayımlar:** kaynak bir yerel dosya ya da URL'dir. Hesap Instagram Business/Creator türündedir. Kişiye ait veri dolaşacağı için KVKK kapısı zorunlu.
**Faz 0 · Karar ve lisans (~8k):**
- Video departmanının müdür skill'i açılır (adı `Skill` listesinden doğrulanır).
- `Agent ara-lisans-kontrol` iki aday hattın lisansına bakar: `autoclip-paket` ve `socialclaw` CLI. Lisans MIT veya Apache değilse ilgili adım ffmpeg ve kendi betiğimizle yapılır.
- `Agent sec-skill-tedarik-tarama` bu iki aracı taranmadan kurulmasın diye kontrol eder.
- **Tartışma noktası:** yükleme Graph API ile doğrudan mı, üçüncü taraf bir zamanlayıcıyla mı? Öneri doğrudan Graph API. İki şart var: Graph API Reels'te yerel zamanlama sunmaz, zamanlamayı bizim yapmamız gerekir. `video_url` herkese açık olmalıdır, bu da bir barındırma yeri ister.
**Faz 1 · Alım ve transkript (~5k):**
- Kaynak URL ise `Agent vid-ytdlp-indirme`, ardından `whisper-cli` ile kelime zamanlı SRT/JSON.
- Kapı: `ffprobe` süre ve codec okur. Transkript boş kalırsa hat durur.
**Faz 2 · En iyi 3 anı seçme (~12k):**
- Adım: transkripte göre aday pencereler (15–60 sn), ses enerjisi ve sahne kesimiyle puanlanır, en iyi 3 seçilir, örtüşmeler atılır.
- Araçlar: `Agent vid-kisa-klip-secici`, kanca ölçütleri için `Skill reel-plan`.
- Kapı: LLM puanlama çağrısı video başına **en çok 3**. Seçici çıktısının pytest testi var (3 kayıt, örtüşme yok, süre sınırları içinde).
- **Tartışma noktası:** puanlamayı LLM mi yapsın, sezgisel kural mı? Önerim: sezgisel kurallar 10 adayı seçsin, LLM bunlardan 3'ü sıralasın.
**Faz 3 · Kırp, altyazı, ses (~15k):**
- Kırpma: 1080×1920. Başlangıçta merkez kırpma kullanılır; yüz takibi (mediapipe) ancak test videosunda konuşan kişi kadraj dışına düşerse eklenir.
- Altyazı: ASS biçiminde kelime vurgulu, Reels güvenli alanının içinde (alt ~%20 boş).
- Ses: `loudnorm` iki geçişli, hedef -14 LUFS ve -1 dBTP.
- Araçlar: `Agent vid-ffmpeg-donusturucu`, `Agent vid-sosyal-video-bicim`, `Agent vid-ses-duzeni`.
- Kapı: `ffprobe` boyutu 1080×1920 ve süreyi ≤90 sn doğrular. `ffmpeg ebur128` -14 LUFS ±1 LU içinde olmalı. 3 çıktının her birinden `Agent vid-kare-cikarici` ile bir kare alınıp Read ile güvenli alan kontrolü yapılır.
**Faz 4 · Zamanlanmış yükleme (~15k):**
- Adım: Graph API'de container oluşturulur, `status_code=FINISHED` beklenir, ardından `media_publish`. Gönderim saatleri kuyruk dosyasından okunur.
- Araçlar: `Agent otm-api-entegrasyon`. Zamanlama `Agent otm-zamanlanmis-gorev` ile Windows Görev Zamanlayıcı'da, `arka.py` (CREATE_NO_WINDOW) üzerinden koşar; ekranda pencere açılmaz.
- Kapı: `--dry-run` varsayılandır. Bir çalıştırmada **en çok 3** gönderi ve en çok 1 yeniden deneme. Token env var'dan okunur ve hiçbir yere basılmaz.
- Güvenlik: `Agent ecc:security-reviewer` ve `Agent sec-sir-tarayici` çalışır.
**Faz 5 · KVKK ve inceleme (~8k):**
- `Agent sec-kvkk-gdpr-kontrol`: videoda görünen ya da sesi duyulan kişilerin rızası, ses ve transkriptin saklama süresi; whisper yerelde kaldığı için dışarı ses gönderilmez.
- `Agent sec-llm-pii-maskeleme`: transkript LLM'e gitmeden önce PII maskelenir.
- Kod incelemesi: `Agent inc-ponytail-kod` ve `Agent ecc:code-reviewer`. Uçtan uca deneme önce dry-run ile, sonra test hesabına gerçek 1 gönderiyle yapılır.

Planlara müzik ekleme, A/B kanca denemesi ve çoklu platform istenmediği için almadım. Departman müdür skill adlarını doğrulamadım, katalogda çıkmadılar. Instagram Graph API'nin güncel kotası ve Reels'te `video_url` şartı Faz 0'da resmi dokümandan kontrol edilmeli.

## 6. TELVE çay markası sitesini (Astro + three.js + GSAP + Lenis) awwwards seviyesinde 3D animasyonlu scroll deneyimiyle baştan yeniden yap.
### X
**Ön koşul:** Önce `frontend-craft` yüklenir (global kural). Skill çakışırsa sıra frontend-craft > taste-* > diğerleri. Frontend için bir departman-* skill'i katalogda çıkmadı; adı açılışta doğrulanacak. Tarayıcı yalnız playwright headless, Blender yalnız `-b` ile çalışır.

**F0 Keşif ve yön (~15k)**
- Adım: mevcut siteyi denetle, marka varlıklarını ve 3–5 awwwards referansını çıkar.
- Araç: `taste-skill:redesign-existing-projects`, `frontend-craft` (marka kimliği kararı), `build-awwwards-quality-sites`, ajan `fe-tasarim-yonu`.
- Kapı: brief'te ton, palet, tipografi ve "neden TELVE" yazılı olmalı.
- Tartışma: Astro adası içinde vanilla three mi, R3F + `@14islands/r3f-scroll-rig` mi? Öneri vanilla three: React yükü yok ve tek canvas yeter.

**F1 Scroll senaryosu (~10k)**
- Adım: sahne sırası (çay bahçesi → hasat → demleme → ince belli bardak → ürünler), her sahne için pin/scrub süreleri.
- Araç: ajan `fe-scroll-hikayesi`, `build-threejs-scroll-worlds`, `scroll-craft`.
- Tartışma: tek kalıcı canvas mı, bölüm başına canvas mı? Öneri tek canvas, kamera yolu scroll ilerlemesine bağlı.

**F2 3D varlıklar (~25k)**
- Adım: bardak, demlik ve yaprakları modelle; GLB'yi Draco/meshopt ve KTX2 ile sıkıştır.
- Araç: `blender-uretim` (headless `-b`), ajan `bl-glb-disa-aktar`, `python tools/bpy_kontrol.py`.
- Kapı: bpy_kontrol 0 hata; hero GLB ≤1.5 MB; hazır model, HDRI ve font varsa lisans kontrolü (`ara-lisans-kontrol`).

**F3 İskelet (~30k)**
- Adım: Astro + content collections. Lenis, GSAP ScrollTrigger ile senkron çalışır (`lenis.on('scroll', ScrollTrigger.update)` + `gsap.ticker`). Sürümler `omer-kutuphaneler` pinleriyle sabitlenir.
- Araç: ajan `fe-astro`, `gsap-skills:gsap-scrolltrigger`, `lenis`. `tempus` eklenmez, gsap.ticker yeterli.
- Kapı: `astro build` yeşil; `size-limit` ile ilk yük JS ≤150 KB gz (three ayrı chunk'ta, tembel yüklenir).

**F4 Sahne ve hareket (~60k)**
- Adım: kamera yolu, ışık, malzeme; metin maske açılışları; zayıf cihaz için poster/video fallback; `prefers-reduced-motion` dalında statik akış.
- Araç: `threejs`, `cinematic-gsap-lenis-motion-system`, `gsap-skills:gsap-performance`, ajan `fe-webgl-3d-hero`, `inclusive-interaction:motion-sensitivity`.
- İnceleyen: ajan `fe-animasyon-tasarimci` (yalnız transform/opacity kuralı).
- Tartışma: DPR tavanı 1.5 mi 2 mi? Mobilde 1.5'te 60 fps ölçülürse 1.5 kalır.

**F5 Kapılar ve ekran turu (~40k)**
- Adım: frontend-craft Section 6 ekran görüntüsü döngüsü (390/768/1440 px), playwright headless.
- Kapılar:
  - Performans: Lighthouse CI, mobilde LCP <2.5 s, CLS <0.1, INP <200 ms; `fixing-motion-performance`.
  - Erişilebilirlik: playwright içinde axe 0 kritik bulgu, klavye turu (ajan `qa-erisilebilirlik-testi`).
  - SEO: meta, OG, canonical, sitemap (ajan `fe-meta-seo-duzeltici`).
  - KVKK: analitik varsa çerez onayı ve aydınlatma metni (`policy-monitor`).
- İnceleyenler: `UI Finish-Gate Reviewer`, `agent-skills:web-performance-auditor`, `ecc:a11y-architect`.

**F6 Kapanış (~10k)**
- Adım: önizleme dağıtımı, Section 6 tur raporu, commit.
- Araç: `netlify-frameworks` (hostun Netlify olduğu varsayımıyla; değilse departman-surec-git-yayin).
- Bütçe toplamı ≈190k jeton.
### Y
Astro statik kabuk + three.js/GSAP/Lenis ada; API maliyeti 0 (hepsi yerel), tahmini toplam ~80k.

**Faz 0 — Araştırma (15k)**
- Mevcut TELVE içerik/varlık envanteri · `fe-astro` + `firecrawl-mcp` (marka varlığı çekimi) · kapı: içerik bütünlük listesi · konsey: yalnız tasarım yönü belirsizse `fe-tasarim-yonu`, varsayılan yok.

**Faz 1 — Tasarım + yığın (10k)**
- Design brief + token/DESIGN.md · Skill `build-threejs-scroll-worlds` + `build-awwwards-quality-sites` (öncelik: frontend-craft > impeccable > ui-ux-pro-max) · kütüphane: `lenis`, `@14islands/r3f-scroll-rig`, `tempus` (pinli) · kapı: tasarım kontratı.

**Faz 2 — Uygulama (40k)**
- Astro iskelet + içerik koleksiyonları · `fe-astro` (minimal client JS, ada mimarisi).
- 3D hero + scroll sahneleri · `fe-webgl-3d-hero` (zayıf cihaz fallback şart) + Skill `cinematic-gsap-lenis-motion-system` · GLB varlık: `bl-glb-disa-aktar` (boyut ≤2MB mesh kapısı, `bl-gorsel-ani-kontrol`).
- a11y katmanı · `@react-three/a11y` + reduced-motion.
- kapı: CWV sayısal bütçe — LCP ≤2.5s, JS ≤170KB, 60fps scroll · araç: Lighthouse + `fixing-motion-performance`.

**Faz 3 — Test + kapı (12k)**
- E2E · `qa-e2e-playwright` (Chrome, headless).
- a11y · `qa-erisilebilirlik-testi` (axe-core, 0 kritik).
- SEO · `fe-meta-seo-duzeltici`.
- güvenlik (form/çerez) · `semgrep` + `gitleaks`; KVKK · `sec-kvkk-gdpr-kontrol`; başlık · `sec-guvenlik-baslik`.
- inceleme: `fe-tasarim-incele` + UI Finish-Gate Reviewer (tasarım), `ecc:code-reviewer` (kod), `ecc:security-reviewer` (güvenlik).

**Faz 4 — Yayın + kapanış (3k)**
- Netlify/Vercel önizleme + geri alma adımı · Skill `netlify-frameworks` · kapı: önizleme yeşil · rapor: commit·test·CI·sapma, 3 ekran görüntüsü → docs/kapanis-araclar.md.

Atladım/riskler: mevcut TELVE kodunu/içeriğini görmeden "baştan yeniden yap" kapsamını varsaydım; firecrawl ve her iki Firecrawl MCP kurulu değil (anahtar/kuyruk gerekir) — varlık çekimi manuel düşebilir.

## 7. Yayındaki Next.js e-ticaret sitesinin uçtan uca güvenlik testi: SAST, sır taraması, DAST, ödeme akışı ve yetkilendirme kontrolü, öncelikli bulgu raporu.
### X
**Ön koşul:** `departman-guvenlik` açılır ve tool sırası ona göre izlenir. Yazılı yetki ve kapsam (RoE) olmadan aktif test yapılmaz. Tercih staging; canlıdaysa düşük hız ve bakım penceresi. Ödeme yalnız sağlayıcının test/sandbox modunda denenir. DoS yapılmaz. Env değerleri hiçbir çıktıda basılmaz.

**F0 Kapsam ve tehdit modeli (~15k)**
- Adım: alan adları, roller (misafir, müşteri, admin), ödeme sağlayıcısı (Stripe/iyzico), test hesapları, durdurma kişisi.
- Araç: ajan `sec-pentest-plani`, ajan `sec-tehdit-modelleme` (STRIDE).
- Kapı: imzalı kapsam ve sayısal tavanlar:
  - DAST: en çok 5 istek/sn ve en çok 20k istek.
  - strix: en çok 300 LLM çağrısı / $15.
- Tartışma: canlı mı staging mi? Öneri staging + canlıda yalnız pasif tarama.

**F1 Sır taraması (~10k)**
- Adım: repo ve tüm git geçmişi; istemci bundle'ında `NEXT_PUBLIC_*` sızıntısı; herkese açık source map.
- Araç: `gitleaks detect --redact`, ajan `sec-sir-tarayici`.
- Kapı: bulgu yalnız konum olarak raporlanır; sızan anahtar için rotasyon notu (`Secrets & Credential Hygiene Engineer`).

**F2 SAST ve bağımlılıklar (~30k)**
- Adım:
  - semgrep/opengrep Next.js kuralları: server action'lar, route handler'lar, `dangerouslySetInnerHTML`, `next/image` remotePatterns SSRF.
  - `npm audit` / osv. Next sürümü middleware bypass'a karşı (CVE-2025-29927, `x-middleware-subrequest`) kontrol edilir.
- Araç: ajan `sec-sast-kosucu`, `phoenix-sast-rules:opengrep-rule-generator`, ajan `sec-bagimlilik-acik`, ajan `sec-injection-denetci`.

**F3 Yetkilendirme (~35k)**
- Adım: rol × eylem matrisi çıkarılır; her API ve server action için sahiplik kontrolü yapılır (IDOR/BOLA: başka kullanıcının siparişi, adresi, faturası). Mass assignment (`role`, `price` alanları) denenir. JWT/oturum: süre, iptal, cookie bayrakları.
- Araç: ajan `sec-yetkilendirme-matrisi`, ajan `sec-api-guvenlik`, ajan `sec-jwt-oturum`, playwright headless ile iki kullanıcı oturumu.
- Kapı: her bulgu yeniden üretilebilir bir istek çiftiyle kanıtlanır.

**F4 Ödeme akışı (~30k)**
- Adım: fiyat ve tutarın sunucuda yeniden hesaplandığı; kupon yarışı (paralel aynı kupon); idempotency; webhook imza doğrulaması ve tekrar oynatma; sepet adedinin eksi/0 değeri; 3DS dönüş URL'sinde açık yönlendirme.
- Araç: ajan `Payments & Billing Engineer`, ajan `sec-pci-dss-kapsam` (kart verisi hosted fields'ta mı), ajan `otm-webhook-tasarimci`, ajan `sec-acik-yonlendirme`.
- Tartışma: yarış testi canlıda yapılmaz, yalnız staging'de.

**F5 DAST (~35k, arka planda `.kos/kopru/arka.py`)**
- Adım: kimlikli ve kimliksiz tarama; güvenlik başlıkları (CSP, HSTS, CORS); XSS/CSRF.
- Araç: `web-app-penetration-testing`, `strix` CLI (F0 tavanıyla), ajan `sec-guvenlik-baslik`, ajan `sec-xss-csrf-denetci`.
- Tartışma: strix trafiği ve kodu LLM API'ye gönderir (KVKK riski). Öneri: kişisel veri içermeyen staging verisiyle çalıştırmak.

**F6 KVKK, doğrulama ve rapor (~25k)**
- Adım: loglarda ve hata sayfalarında kişisel veri (ajan `sec-loglama-gizlilik`, `sec-kvkk-gdpr-kontrol`). Yanlış pozitifler ayıklanır. Her bulguya CVSS, kanıt ve düzeltme adımı yazılır; sıralama Kritik → Düşük.
- İnceleyen: `agent-skills:security-auditor` (bulguları örnekleyerek doğrular), ajan `sec-guvenlik-raporu` (rapor).
- Bütçe toplamı ≈180k jeton.

Atladıklarım: departman/frontend skill adlarını ve 6 numaralı işin hostunu doğrulamadım, bütçeler tahmin. Asıl risk: 7 numaralı iş canlı sitede yazılı yetki olmadan başlatılırsa hukuki sorun doğar.
### Y
Üretim sitesine canlı DAST → yetkili kapsam + sayısal tavan şart; API maliyeti 0, tahmini ~55k.

**Faz 0 — Kapsam + tehdit modeli (10k)**
- Yazılı yetki, RoE, hedef URL/ortam · `sec-pentest-plani` · kapı: imzalı kapsam (bu olmadan DAST yok).
- STRIDE + güven sınırları · `sec-tehdit-modelleme` · konsey: yalnız kritik varlık sınırı belirsizse.

**Faz 1 — Statik + sır (12k)**
- SAST · `semgrep` (`sec-sast-kosucu`), triyaj file:line.
- sır taraması (geçmiş dahil) · `gitleaks` (`sec-gitleaks-gecmis`) · yanlış-alarm: test fikstürü/mock elenır.
- bağımlılık · `sec-bagimlilik-acik`.
- kapı: kritik bulgu 0 ya da gerekçeli; inceleme `ecc:security-reviewer`.

**Faz 2 — DAST + pentest (18k)**
- OWASP ZAP (prod build pnpm build+start, Docker) · `zaproxy` betiği · ceiling: ≤N istek/dk, prod'a yazma yok.
- ajan pentest · `strix` (yalnız kapsam içi, salt-okuma öncelik).
- ödeme akışı · `sec-pci-dss-kapsam` (kart verisi tokenizasyon/hosted field kontrolü, test modu).
- yetkilendirme · `sec-yetkilendirme-matrisi` (rol×endpoint, BOLA/mass-assignment) + `sec-api-guvenlik`.
- inceleme: `ecc:security-reviewer` + `differential-review:adversarial-modeler` (yüksek riskli bulgu).

**Faz 3 — Öncelikli rapor + kapanış (5k)**
- Bulguları sev×etki sırala, fix adımı · `sec-guvenlik-raporu` → docs/guvenlik-raporu.md.
- kapı: her kritik/yüksek bulguya repro + düzeltme; CVE/CWE eşleme.
- rapor: commit·test·CI·sapma; sır değerleri asla yazılmaz, yalnız konum.

Atladım/riskler: üretim sitesine canlı DAST yasal/operasyonel izin ister — imzalı kapsam gelmeden Faz 2 koşulamaz; Stripe MCP ve Claude Security plugin kurulu değil, ödeme testi test-modu anahtarı gerektirir.

## 8. README'deki kurulum komutundaki yazım hatasını düzelt.
### X
README'deki kurulum komutunda yazım hatası düzeltme. Tek satırlık iş olduğu için kısa plan.
- **F1 Bul** · `Grep -n` ile `README*` içinde kurulum komutunu bul. Ardından o satırın ±10 satırını `Read` ile oku. · Kapı: hatalı belirteç tek mi, kontrol et. Aynı komut `docs/` altında ya da başka README'lerde tekrar ediyorsa `Grep files_with_matches` ile bul ve hepsini düzelt. · ~1k jeton
- **F2 Düzelt** · `Edit` ile yalnız hatalı belirteci değiştir, çevredeki metne dokunma. · Kapı: düzeltilmiş komut gerçekten çalışmalı. `--help` ya da kuru koşu (`--dry-run` / `/plugin marketplace add` benzeri) ile sına. Bu bir paket kurulumuysa gerçek kurulumu çalıştırma. · ~1k jeton
- **İnceleme:** Yok, tek satırda inceleyici ajana gerek yok. CLAUDE.md'deki "basit işte bu ağırlık uygulanmaz" kuralı geçerli.
- **Tartışma noktası:** Doğru yazım belirsizse, örneğin paket adının iki farklı biçimi varsa, kayıt defterinden (`npm view` / `gh repo view`) doğrula. Tahminle düzeltme yapma.
- **Kapanış:** commit `docs: README kurulum komutu yazım hatası`. Test sayısı yok, CI'da yalnız markdown lint koşuyorsa o koşar.
### Y
**Faz 1: bul ve düzelt** (~2k jeton)
- Adım: Grep ile README'de kurulum satırını bul (`-n`, files_with_matches). Read ile ~10 satır oku, yazım hatasını tek Edit ile düzelt.
- Araç: Grep, Read, Edit. Skill ya da ajan gerekmiyor, tek satırlık iş.
- Kapı: düzeltilmiş komutu kaynağıyla karşılaştır (paket adı, marketplace yolu, bayrak). Komut zararsızsa (`--help`, `--dry-run`) bir kez koştur. Gerçek kurulum yapılmaz.
- İnceleme: gerekmiyor. `git diff` tek satır mı, ona bakılır.
- Tartışma noktası: yok. Aynı yazım hatası başka dokümanlarda da varsa raporda belirtilir, kapsam genişletilmez.

## 9. ffmpeg ile bir videonun ilk 10 saniyesini kes.
### X
ffmpeg ile videonun ilk 10 saniyesini kesme. Rutin iş.
- **F1 Keşif** · `ffmpeg -version` ve `ffprobe -v error -show_entries format=duration:stream=codec_name,codec_type -of csv=p=0 <girdi>` çalıştır. · Kapı: süre en az 10 sn olmalı ve codec'ler bilinmeli. · ~1k jeton
- **F2 Kes** · Alt ajan `vid-ffmpeg-donusturucu` komutu kurar. Ana öneri `ffmpeg -n -i <girdi> -t 10 -c copy <çıktı>`.
  - `-n` mevcut dosyanın üzerine yazmayı önler, girdi korunur.
  - Çıktı ayrı bir dosyaya, ayrı bir klasöre yazılır.
  - Arka planda koşacaksa `.kos/kopru/arka.py` ile pencere açmadan çalıştırılır.
  - · ~2k jeton
- **Kapı** · `ffprobe` ile çıktı süresini doğrula: 10 sn ± 0,1 sn olmalı. Ayrıca `vid-kare-cikarici` ile ilk ve son kareyi çıkarıp `Read` ile bak. Video oynatıcı açılmaz (ekran kuralı). · ~2k jeton
- **Tartışma noktası:** `-c copy` hızlı ve kayıpsızdır. Ancak anahtar kareye (keyframe) hizalandığı için süre 10 sn'yi biraz aşabilir. Tam kare doğruluğu gerekiyorsa `-c:v libx264 -crf 18 -c:a aac` ile yeniden kodlanır; bu yavaştır ve az da olsa kayıp verir. Varsayılan copy olsun, süre sapması 0,5 sn'yi geçerse yeniden kodlamaya geç.
- **İnceleme:** Yok. Kanıt `ffprobe` çıktısı.
### Y
**Faz 1: ön koşul** (~0,5k)
- Adım: `ffmpeg -version` ile kurulu mu bak. Girdi yolunu ve çıktı adını netleştir.
- Kapı: girdi dosyası var mı, çıktı yolu girdiyle aynı mı (aynıysa durulur).

**Faz 2: kes** (~1,5k)
- Adım: `ffmpeg -n -i girdi.mp4 -t 10 -c copy cikti.mp4` komutunu koş. `-n` var olan dosyanın üzerine yazmayı engeller.
- Araç: ffmpeg CLI. Komut takılırsa `vid-ffmpeg-donusturucu` ajanına danışılır.
- Tartışma noktası: `-c copy` hızlıdır ve kaliteyi korur, ama keyframe'e göre keser, süre 10 sn'den biraz sapabilir. Tam 10,000 sn gerekiyorsa yeniden kodlanır: `-c:v libx264 -crf 18 -c:a aac`.

**Faz 3: doğrula** (~0,5k)
- Kapı: `ffprobe -v error -show_entries format=duration` çıktısı 10 ± 0,1 sn olmalı. Ses ve görüntü akışının ikisi de var mı, ona da bakılır.
- İnceleme: gerekmiyor.

## 10. .NET projesinde bir DTO alanının adını CustomerName olarak değiştir.
### X
**Faz 0: netleştir** (~0,5k)
- Belirsizlik var: hangi DTO, eski alan adı ne? Bunlar bilinmeden başlanmaz.

**Faz 1: kapsam** (~2k)
- Adım: `graphify query "<Dto> <eskiAd>"`, ardından Grep ile tüm kullanımlar: mapping (AutoMapper/Mapster), controller'lar, validator, test, fixture, JSON örnekleri, OpenAPI.
- Araç: graphify, Grep.
- Tartışma noktası: alan adını değiştirmek JSON'daki adı da değiştirir ve API istemcilerini bozar. Seçenekler: (a) `[JsonPropertyName("eskiAd")]` ile JSON'daki ad korunur, (b) API'de kırıcı değişiklik yapılır ve sürüm notuna yazılır. İstemci varsa varsayılan (a).

**Faz 2: test önce** (~1,5k)
- Adım: serileştirme testi yaz, beklenen JSON adını doğrulasın. Önce kırmızı yandığı görülür.
- Araç: `dn-xunit-test-yazar` ajanı ya da elle xUnit.

**Faz 3: yeniden adlandır** (~2k)
- Adım: alanı ve tüm referanslarını Edit ile değiştir. Kodda dize olarak geçen eski adları ayrıca Grep ile ara (`nameof`, raw SQL, JS istemci).
- Kapı: `rtk dotnet build` 0 hata, ardından `rtk dotnet test` yeşil. `--nologo` kullanılmaz, gerekirse `DOTNET_NOLOGO=1`.

**Faz 4: inceleme** (~1,5k)
- İnceleme ajanı: `ecc:csharp-reviewer`, `git diff` üzerinde.
- Kapı: Grep ile eski adın kodda kalmadığı doğrulanır (bilinçli `JsonPropertyName` dışında).

DTO doğrudan EF entity'ye bağlıysa (DTO ile entity aynı sınıfsa) işe migration eklenir (`dn-efcore-migration`). Bu planda varsayılmadı.

Kontrol edilmeyenler: README içeriği, video dosyası ve .NET projesi açılmadı. Planlar varsayıma dayanıyor. 10'daki asıl risk JSON adının değişip istemcileri bozması.
### Y
.NET projesinde bir DTO alanını `CustomerName` olarak yeniden adlandırma. Rutin iş, ama API sözleşmesine dokunabilir.
- **F1 Kapsam** · `graphify query "<DTO adı> kullanımları"`, ardından `Grep -n` ile şunları ara:
  - eski alan adı: `.cs`, `.razor`, `.json`, `.http`, `.ts` istemcileri, test fixture'ları
  - `[JsonPropertyName]`, AutoMapper/Mapster profilleri, `nameof()`
  - EF yansıması
  - · Kapı: DTO dışarıya açık mı? Controller, OpenAPI ya da SignalR üzerinden dışarı açılıyorsa sözleşme değişikliği demektir. · ~4k jeton
- **F2 Kırmızı** · `rtk dotnet test` ile mevcut durumu kaydet. Mümkünse JSON serileştirme testi ekle: `customerName` anahtarını bekleyen bir test ilk koşuda kırmızı olmalı (`dn-xunit-test-yazar` kalıbı). · ~3k jeton
- **F3 Yeniden adlandır** · Elle sed kullanma. Alanı `Edit` ile değiştir, ardından F1 listesindeki her çağıran yeri tek tek düzelt. IDE rename kullanılamıyor, bu yüzden derleme hataları kontrol listesi olarak kullanılır: `rtk dotnet build`. · ~4k jeton
- **Kapı** · Sırayla:
  - `rtk dotnet build` uyarısız geçmeli.
  - `rtk dotnet test` yeşil olmalı.
  - `rtk dotnet format --verify-no-changes` geçmeli.
  - Sözleşme açıksa OpenAPI farkına bakılır (`dn-openapi-dokuman`).
  - Not: `dotnet test --nologo` kullanma (MTP exit 5 sorunu), yerine `DOTNET_NOLOGO` kullan.
  - · ~3k jeton
- **İnceleme:** `ecc:csharp-reviewer` diff'i inceler: kaçırılmış dize referansı, mapper ya da istemci var mı.
- **Tartışma noktası:** Sözleşme dışa açıksa iki yol var:
  - (a) Doğrudan yeniden adlandırma. İstemciler kırılır.
  - (b) C# adı `CustomerName` olur, eski JSON adı geçiş süresince `[JsonPropertyName("eski")]` ile korunur.
  - DTO yalnız içeride kullanılıyorsa (a) uygulanır. Dışa açıksa karar kullanıcıya bırakılır. Bu bir DTO alanı olduğu için EF migration gerekmez. Ancak aynı ad bir entity'de de varsa, o ayrı bir iş olarak (`dn-efcore-migration`) raporlanır.
- **Kapanış:** commit · test sayısı · CI · sözleşme kararı.

Mevcut README, video ve DTO dosyalarını açmadım. Planlar genel durum için yazıldı. 10'da asıl risk, sözleşme dışa açıkken istemcilerin sessizce kırılması.
