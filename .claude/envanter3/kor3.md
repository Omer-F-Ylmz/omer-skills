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
**Müdürler:** frontend-craft (UI zorunlu), departman-guvenlik, departman-surec-git-yayin.
**F0 Kapsam ve yığın** (6k)
- Adım: kabul ölçütleri dalga.md'ye yazılır. 5 sayfa: Ana sayfa, Hizmetler, Hakkımızda, SSS, İletişim. KVKK aydınlatma metni ve çerez politikası alt bilgiden açılır.
- Konsey (consciousness-council, ~15k): yığın seçimi. Seçenekler Astro statik + PHP form uç noktası ya da WordPress. Hostinger paylaşımlı barındırmada PHP hazır; önerim Astro + PHP (fe-astro).
**F1 Tasarım ve uygulama** (50k)
- Adım: yön ve tokenlar belirlenir, sonra sayfalar yazılır.
- Araç: frontend-craft > impeccable > ui-ux-pro-max; marketing-skills:content-strategy ile hizmet metinleri.
- Kapı: 3 genişlikte ekran görüntüsü, frontend-craft 6. bölüm tur raporu.
- İnceleme: fe-tasarim-incele, UI Finish-Gate Reviewer.
**F2 KVKK formu ve çerez** (10k)
- Form yalnız ad, e-posta, telefon ve mesaj alır. Açık rıza kutusu ayrıdır ve işaretli gelmez. Aydınlatma metni bağlantısı formun yanında durur.
- Sunucu tarafı: doğrulama, CSRF belirteci, honeypot ve IP başına hız sınırı. Saklama süresi yazılır.
- Çerez: yalnız zorunlu çerez varsa bilgilendirme bandı yeter. Analitik eklenirse onaydan önce hiçbir betik yüklenmez.
- Araç ve kapı: policy-monitor (metinler), sec-kvkk-gdpr-kontrol (veri akışı), fe-cerez-oturum-hata (onay öncesi çerez sayısı 0 mı).
**F3 SEO** (6k)
- Sayfa başına title, description ve canonical; sitemap.xml, robots.txt; JSON-LD AccountingService + LocalBusiness.
- Araç: fe-meta-seo-duzeltici, marketing-skills:seo-audit; ölçüm chrome-devtools MCP performans izi ile.
- Kapı: LCP < 2,5 s, her sayfada tek H1.
**F4 Test ve güvenlik** (15k)
- Test: playwright-cli headless Chrome; form iyi yol, hatalı giriş ve rıza yokken red. a11y: qa-erisilebilirlik-testi + axe-core, 0 ciddi ihlal.
- Güvenlik: semgrep, gitleaks, sec-guvenlik-baslik (.htaccess'e CSP/HSTS), sec-owasp-top10 (form uç noktası).
- DAST: ZAP Docker'da arka.py ile, yalnız staging'e.
- Ajan pentest: strix staging'e, en çok 1 koşu, LLM harcaması en çok 2 $.
- İnceleme: ecc:code-reviewer, ecc:security-reviewer; bulgular sec-guvenlik-raporu ile raporlanır.
**F5 Yayın** (5k)
- Önce git-yayin-oncesi-kontrol. Sonra hostinger MCP ile alan adı/DNS, SSL ve yükleme: en çok 1 yayın + 1 geri alma.
- Yayın dışa dönük olduğu için senin onayın alınır. Canlıda duman testi: form postası gerçekten ulaşıyor mu.
**Kapanış** (3k): 6 maddelik kapanış listesi; commit · test · CI · sapma.
**Kullanılmayanlar:**
- netlify: hedef Hostinger.
- lighthouse: kurulu değil; yerine chrome-devtools MCP.
- swup / Vengeance UI: 5 sayfalık vitrin sitede gereksiz.

## 2. ASP.NET Core ile randevu sistemi API'si: JWT kimlik doğrulama, EF Core + PostgreSQL migration, rol bazlı yetki, xUnit testleri ve OpenAPI dokümanı.
### X
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
### Y
**Müdürler:** departman-backend-dotnet, departman-veri-db.
**F0 Kabul ve model** (8k)
- Varlıklar: Hizmet, Uzman, Müsaitlik, Randevu, Kullanıcı. Roller: Admin, Uzman, Müşteri.
- Araç: dn-efcore-modelleme, ecc:postgres-patterns.
- Kritik karar: çift rezervasyonu engellemek. Öneri: PostgreSQL `EXCLUDE USING gist (uzman_id WITH =, tstzrange WITH &&)`. Uygulama kodundaki kontrol yarış durumunda delinir.
- Konsey (ecc:council, ~70k, tek kullanım): auth yaklaşımı. Seçenekler ASP.NET Identity + kendi JWT'miz ya da harici IdP (auth0 MCP). Öğrenim notu (öğrenim 67): parolayı kendi tablonda tutma.
**F1 İskelet ve auth** (15k)
- Minimal API endpoint grupları, ProblemDetails.
- JWT: kısa ömürlü erişim belirteci + yenileme belirteci. İmza anahtarı user-secrets/env'den gelir, repoya girmez.
- Rol politikaları: `RequireRole` ve kaynak sahipliği kontrolü (müşteri yalnız kendi randevusunu görür).
- Araç: dotnet-aspnetcore:dotnet-webapi, dn-aspnet-core, dn-identity-auth.
- Kapı: sec-jwt-denetci (algoritma, exp, aud, iss, saat kayması).
**F2 EF Core + PostgreSQL migration** (8k)
- Araç: dn-efcore-migration, Npgsql.
- Kapı: her migration'ın Down'u Testcontainers'ta denenir; `dotnet ef migrations script --idempotent` çıktısı gözden geçirilir.
- Üretime yalnız onayla gider (öğrenim 68).
- İnceleme: ecc:database-reviewer.
**F3 Uç noktalar** (12k)
- Randevu oluştur, iptal et, listele; müsaitlik sorgusu; sayfalama.
- Tüm zamanlar UTC `timestamptz` olarak saklanır.
- Araç: dn-webapi-endpoint.
**F4 xUnit testleri** (12k)
- Araç: dn-xunit-test-yazar, ecc:csharp-testing. Entegrasyon için WebApplicationFactory + Testcontainers PostgreSQL.
- Önce kırmızı görülecek testler: çakışan randevu 409; başkasının randevusu 403/404; süresi dolmuş JWT 401; rol matrisi.
- Koşu: `rtk dotnet test`. `--nologo` verilmez, DOTNET_NOLOGO kullanılır (MTP exit 5 notu).
- İnceleme: dotnet-test:test-quality-auditor yalnız örnekleme.
**F5 OpenAPI** (5k)
- Microsoft.AspNetCore.OpenApi; Bearer güvenlik şeması; yanıt tipleri ve örnekler.
- Araç: dn-openapi-dokuman. Kapı: belge spectral ya da dil-openapi-sozlesme ile doğrulanır.
**F6 Güvenlik ve KVKK** (8k)
- semgrep, gitleaks; sec-api-guvenlik (BOLA, mass assignment, login'de hız sınırı).
- sec-kvkk-gdpr-kontrol: telefon ve e-posta loglara düşmemeli, saklama ve silme süresi belirli olmalı.
- İnceleme: ecc:csharp-reviewer (her PR), ecc:security-reviewer, inc-mimari-inceleme.
**Kapanış** (3k): test sayısı, migration up/down kanıtı, commit · CI · sapma.
**Not ve kullanılmayanlar:**
- plan_kur bu işe yanlışlıkla "blender" grubunu da ekledi; o grup yok sayıldı.
- netlify-*, drizzle-docs, db-supabase-kurucu: başka yığın.
- Doküman sorgusu gerekirse mslearn yeterli.

## 3. Three.js tarayıcı oyununa 2-4 kişilik çok oyunculu yarış modu ekle: WebSocket senkron, gecikme telafisi, skor tablosu ve hile önleme.
### X
**Müdürler:** oyun-gelistirme-paket, threejs; lobi ve skor tablosu UI olduğu için frontend-craft zorunlu.
**F0 Keşif** (10k)
- Önce graphify query: oyun döngüsü, araç fiziği, giriş, sahne yapısı. Gerekirse ecc:code-explorer.
- Kapı: fizik deterministik mi (sabit dt)? Değilse önce sabit adıma geçilir, mevcut testler yeşil kalmalı.
**F1 Ağ modeli** (8k)
- Konsey (ecc:council, ~70k): sunucu-otoriter Node `ws` mı, host-istemci mi? Hile önleme için öneri sunucu-otoriter.
- Tasarım (oyn-ag-senkronu):
  - 20–30 Hz sunucu tick'i; istemci sıra numaralı girdiler gönderir.
  - Kendi araç: tahmin + uzlaştırma. Rakipler: 100 ms tamponla interpolasyon.
  - Çarpışma ve bitiş çizgisi: sunucuda geri sarmalı gecikme telafisi.
  - Simülasyon modülü istemci ve sunucuda ortak kullanılır.
**F2 WebSocket katmanı** (15k)
- Araç: dil-websocket. Kalp atışı, yeniden bağlanma, backpressure, mesaj boyutu sınırı, Origin kontrolü, oda belirteci.
- Lobi: 2–4 oyuncu, hazır ve geri sayım.
- Yayın gerekirse: ops-nginx-ters-vekil ile wss.
**F3 Senkron ve telafi** (20k)
- Araç: oyn-three-oyun-sahne, threejs.
- Kapı: birim testleri; aynı girdi dizisi istemci ve sunucuda aynı durumu üretmeli. Uzlaştırma 150 ms gecikme + %5 kayıpla test edilir.
**F4 Hile önleme** (8k)
- Sunucu tarafı kontroller: girdi hızı ve aralığı, hız tavanı, checkpoint sırası, bitiş zamanını yalnız sunucu yazar, istemci konumu kabul edilmez.
- Kapı: sahte istemci testleri (hız hilesi, checkpoint atlama, girdi seli) reddedilmeli.
- İnceleme: ecc:security-reviewer.
**F5 Skor tablosu UI** (12k)
- Yarış sonu tablosu sunucu verisinden çizilir; kalıcı liderlik tablosu istenmedi, atlanır.
- Araç: frontend-craft. Kapı: axe-core 0 ciddi ihlal, klavye ile gezinme, 3 genişlikte ekran görüntüsü.
- İnceleme: fe-tasarim-incele.
**F6 Uçtan uca ve performans** (12k)
- playwright-cli headless Chrome; 4 ayrı tarayıcı bağlamıyla tam yarış; bağlantı kopup geri gelme senaryosu.
- Kare süresi ölçümü: 4 oyuncuda p95 < 16,7 ms.
- Güvenlik: semgrep, gitleaks.
- İnceleme: ecc:code-reviewer.
**Kapanış** (3k): test sayısı, gecikme simülasyonu kanıtı, commit · CI · sapma.
**Kullanılmayanlar:**
- SEO ve KVKK kapıları: oyun modunda sayfa veya kişisel veri formu yok.
- webgpu-threejs-tsl, blender, bl-glb-disa-aktar: render ve model değişmiyor.
- puppeteer: playwright varken ikincisi açılmaz.

Kontrol etmediğim şeyler: `plan_kur` çıktısının ilk 80 satırı ve iş 3'ün tam aday listesi okundu; ek sorgu yapılmadı. ZAP ve lighthouse bu makinede kurulu değil, bu yüzden 1. işte ZAP'ın Docker'da çalışabildiği önce doğrulanmalı.
### Y
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

## 4. Blender'da parfüm şişesi ürün sahnesi kur: modelleme, cam malzeme, stüdyo ışığı, turntable render ve web için 2 MB altı GLB dışa aktarımı.
### X
— Blender parfüm şişesi ürün sahnesi

**Faz 0 · Kurulum (~3k)**
- Adım: oturumu aç, çıktı klasörü `out/parfum/`. Araç: `Skill blender-oturum` → `python tools/blender_oturum.py ac parfum.blend --yeni`. Her bpy işi `-b` ile koşar (`tools/blender_cli.py`); pencere açılmaz.
- Kapı: `blender_bekci` hook'u açık.

**Faz 1 · Modelleme (~12k)**
- Adım: gövde (Bevel + Subdivision), kalın cam taban, ayrı sıvı mesh'i (iç yüzeyden ~0,5 mm içeride), kapak, pompa. Gerçek ölçek: 1 birim = 1 m, şişe ~10 cm.
- Araç: `Agent bl-modelleme-plani` ölçüleri ve topolojiyi çıkarır. `Skill blender-uretim` + `Agent bl-python-betik` bpy betiğini yazar.
- Kapı: `python tools/blender_dogrula.py` (ölçek, pivot, manifold) ve `Agent bl-gorsel-ani-kontrol` (ters normal, kapalı kabuk).
- İnceleme: `Agent ecc:code-reviewer` bpy betiğine bakar.

**Faz 2 · Malzeme + ışık (~15k)**
- Malzemeler: cam için Principled BSDF (Transmission 1, IOR 1,45, Roughness 0–0,05). Sıvı IOR 1,33 ve renkli. Kapak fırçalanmış metal. Araç: `Agent bl-malzeme-kurucu`.
- Işık: kameraya görünmeyen softbox ve emisyon düzlemleri. Arka ışık ürünün sığacağı genişlikte, oranlar anahtar:dolgu:kenar = 3:1:1,2 (öğrenim 59/60). Önce mat gri malzeme ve krom küreyle denenir. Araç: `Agent bl-isik-kurulumu`. HDRI gerekirse `python tools/varlik_indir.py` ile Poly Haven'dan CC0 indirilir.
- Kapı: `python tools/blender_gorunum.py` 4 Workbench + 1 Eevee görüntüsü üretir. Kenar parlaması ve kırılma kare üzerinde kontrol edilir.

**Faz 3 · Turntable render (~10k)**
- Adım: 360° dönüş, 120 kare, doğrusal easing, sonu başa dikişsiz bağlanır. Cycles: 128–256 örnek, denoise açık, caustics kapalı, transparent ve transmission sekmeleri ≥12.
- Araç: `Agent bl-urun-turntable`, `Agent bl-render-ayari`, `Agent bl-animasyon-anahtar`.
- Kapı: ilk, orta ve son kare okunur, ilk/son dikiş farkı göz kontrolüyle doğrulanır. Döngü videosu `Agent vid-ffmpeg-donusturucu` ile birleştirilir.

**Faz 4 · Web GLB < 2 MB (~10k)**
- Adım: render sahnesinden ayrı bir dışa aktarım kopyası hazırlanır: dekimasyon, uygulanmış modifier'lar, dokular 1K webp. Cam KHR_materials_transmission/ior/volume ile çıkar.
- Araç: `Agent bl-glb-disa-aktar` → `python tools/glb_hat.py` (meshopt + webp → validate → inspect, önce/sonra KB).
- Kapı: dosya < 2 048 KB, glTF validator 0 hata, `blender-dogrulama` CLI'nin GLB hattı ve IoU ölçümü.
- İnceleme: `Agent bl-sahne-temizlik` (adlandırma, kullanılmayan veri).

**Konsey (en çok 1, ~15k):** `consciousness-council`. Soru: GLB'de gerçek transmission mı (three.js'te pahalı, mobilde zayıf), yoksa pişmiş sahte cam mı (`tools/blender_pisir.py`)? Karar ölçütü boyut ve mobil FPS.

**Kapanış (~3k):** commit · test sayısı · CI · sapmalar.

**Kullanılmayanlar:** frontend-craft, SEO, ZAP/OWASP ve KVKK kapıları atlandı, çünkü kapsamda web sayfası yok. Sayfaya gömülürse `fe-webgl-3d-hero` ve `@react-three/a11y` eklenir. threejs paketleri ve BlenderKit atlandı, çünkü hedef yalnız dosya ve CC0 yeterli.
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
### Y
— Instagram Reels otomatik video hattı

**Faz 0 · Brief + karar (~5k)**
- Kabul ölçütleri: 3 klip, her biri 15–60 sn; 1080×1920, H.264/AAC; −14 LUFS, true peak −1 dBTP; altyazı güvenli alanın içinde; zamanlanmış yayın.
- Araç: `Agent vid-reel-kanca-merdiveni` (kanca ölçütü), `Skill reel-plan`.
- Kapı: kaynak videonun telif ve lisans kontrolü. Kişi görünüyorsa `Agent sec-kvkk-gdpr-kontrol`.

**Faz 1 · Transkript + an seçimi (~8k)**
- Adım: yerel transkript kelime zaman damgasıyla üretilir. LLM transkripti puanlar (kanca + kapanmış fikir), en iyi 3 aralık seçilir ve cümle sınırına yuvarlanır.
- Araç: `whisper-cli`, `Agent vid-kisa-klip-secici`. Kaynak URL ise `Agent vid-ytdlp-indirme`.
- Kapı: seçilen aralıklar JSON'a yazılır, her biri `Agent vid-kare-cikarici` ile kareden doğrulanır.

**Faz 2 · Kırpma, altyazı, ses (~15k)**
- Dikey kırpma: ffmpeg `crop=ih*9/16:ih`. Özne merkezde değilse yüz takibiyle kaydırılır (opencv/mediapipe, ayrıca bkz. konsey).
- Altyazı: whisper SRT/ASS dosyası 2–3 kelimelik öbeklerle yakılır, alt UI bölgesinin üstünde kalır.
- Ses: iki geçişli `loudnorm` (I=−14, TP=−1, LRA=11).
- Araç: `Agent vid-ffmpeg-donusturucu`, `Agent vid-sosyal-video-bicim`, `Agent vid-ses-duzeni`. Betik `tools/reels_hat.py`, `--kuru` bayrağı ve idempotent çıktı adlarıyla yazılır.
- Kapı: `ffprobe` ile çözünürlük, codec ve süre; `loudnorm` ölçüm çıktısı; renk aralığı için `Agent vid-renk-uzayi`; her klipten 3 kare.
- İnceleme: `Agent vid-gecis-ve-ritim` (kanca ve kesim ritmi), `Agent ecc:code-reviewer`.

**Faz 3 · Zamanlanmış yükleme (~12k)**
- Adım: Instagram Graph API ile yayın: `media_type=REELS` → konteyner durumunu yokla → `media_publish`. API yerel dosya almaz, `video_url` herkese açık bir URL olmalı. Bu yüzden kısa ömürlü imzalı URL kullanılır. API zamanlama sunmaz; Windows Görev Zamanlayıcı yayın saatinde betiği tetikler, kilit dosyası ve log tutulur.
- Araç: `Agent otm-zamanlanmis-gorev`, `Agent otm-api-entegrasyon`, `Agent be-dayaniklilik-kaliplari` (jitter'lı yeniden deneme, en çok 3).
- Kapı: token .env'de durur, değeri basılmaz; `Agent sec-sir-tarayici` ve `gitleaks`. Sayısal tavan: günde en çok 3 yayın, deneme başına en çok 1 yayın. `content_publishing_limit` önceden okunur. İlk gerçek yayından önce Ömer'in onayı alınır.
- İnceleme: `Agent ecc:security-reviewer` (token, URL), `Agent inc-uretim-hazirligi`.

**Faz 4 · Uçtan uca kuru koşu + test (~10k)**
- Adım: 2 dk'lık örnek videoyla tüm hat `--kuru` modda koşar; yayın adımı yalnız istek gövdesini yazar.
- Testler: pytest ile aralık yuvarlama, crop hesabı ve kilit davranışı.

**Konsey (en çok 1, ~70k):** `ecc:council`. Soru: tetik ve kuyruk mimarisi (Görev Zamanlayıcı + yerel kuyruk mu, n8n mi) ve kırpma yöntemi (merkez mi, yüz takibi mi). Hesap riski olan dış yayın kararı olduğu için seçildi.

**Kapanış (~3k):** commit · test sayısı · CI · sapmalar.

**Kullanılmayanlar:** Remotion, HyperFrames ve Premiere atlandı, çünkü kesme ve yakma işi ffmpeg'le yetiyor. fal, Higgsfield ve HeyGen atlandı, çünkü üretim gerekmiyor ve ücretli. autoclip-paket konseyde yalnız yedek seçenek.

---
`plan_kur.py` bir kez çağrıldı, ek sorgu yapılmadı. Hiçbir dosya yazılmadı. İki nokta doğrulanmadı: Graph API yayın kotası (kesin sayı `content_publishing_limit` ucundan okunmalı) ve Reels'in yalnız Business/Creator hesapla yayınlanabildiği. Cam transmission'ın GLB'de 2 MB altında kabul edilebilir görünüp görünmediği de Faz 4 ölçümüne bağlı.

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
**İş:** TELVE çay sitesi — Astro + three.js + GSAP + Lenis, awwwards seviyesi 3D scroll.
UI işi: `/frontend-craft` önce yüklenir; Section 6 round raporu olmadan kapanmaz.

**Faz 1 — Araştırma + tasarım yönü (~15k)**
- Marka varlıkları/referans · firecrawl-mcp (KUR) veya WebFetch · Skill `build-awwwards-quality-sites` + `build-threejs-scroll-worlds` scroll dünyası planı
- Konsey (kritik): tasarım yönü + yığın — Astro islands sınırı vs tam SPA; `fe-tasarim-yonu` brief, karar `docs/karar` yerine dalga.md
- Kapı: yok (plan fazı) · inceleme: —

**Faz 2 — Uygulama (~50k)**
- İskelet · `fe-astro` (islands, minimal JS) · scroll motoru `lenis` + `tempus` (pinli kurulum, omer-kutuphaneler)
- 3D hero + scroll sahneleri · `fe-webgl-3d-hero` (zayıf cihaz fallback şart) · Skill `gsap-scrolltrigger-storytelling` / `cinematic-gsap-lenis-motion-system`
- GLB varlık · `bl-glb-disa-aktar` (boyut/mesh bütçesi) — model gerekirse; yoksa atla
- Erişilebilir sahne · `@react-three/a11y` yalnız R3F kullanılırsa; vanilla three'de atla
- Kapı: perf `fixing-motion-performance` (transform/opacity, reduced-motion) · a11y `qa-erisilebilirlik-testi` (axe-core)
- İnceleme: `fe-tasarim-incele` + UI Finish-Gate Reviewer (jenerik görünüm) · kod `ecc:code-reviewer`

**Faz 3 — Test + güvenlik + SEO (~12k)**
- E2E · `qa-e2e-playwright` (Chrome, headless) · görsel QA birkaç genişlikte
- Güvenlik · semgrep + gitleaks (form/çerez varsa) · `sec-guvenlik-baslik` CSP/HSTS
- KVKK · `sec-kvkk-gdpr-kontrol` yalnız iletişim formu/çerez varsa · SEO `fe-meta-seo-duzeltici`
- İnceleme: `ecc:security-reviewer`

**Faz 4 — Kapanış (~3k):** commit · test sayısı · CI · sapma, ≤15 satır · `docs/kapanis-araclar.md`
Kullanılmadı: oyun kapıları (web sitesi, oyun değil); strix/ZAP (statik pazarlama sitesi, DAST aşırı).

## 7. Yayındaki Next.js e-ticaret sitesinin uçtan uca güvenlik testi: SAST, sır taraması, DAST, ödeme akışı ve yetkilendirme kontrolü, öncelikli bulgu raporu.
### X
**İş:** Yayındaki Next.js e-ticaret sitesi — uçtan uca güvenlik testi, öncelikli bulgu raporu.
`departman-guvenlik` skill'i açılır; sıra: sır → SAST → DAST → pentest → rapor.

**Faz 1 — Kapsam + yetki (~6k)**
- Yetkili kapsam/RoE · `sec-pentest-plani` (recon fazları, hedef URL, ödeme test modu)
- Konsey (kritik): risk önceliği + kapsam — prod'a DAST sınırı, ödeme akışı yalnız Stripe test modu
- **Tavan:** DAST/pentest çağrıları en çok 1 tam tarama turu; ödeme akışı test modu, canlı işlem 0
- Kapı: yetki onayı (plan) · inceleme: —

**Faz 2 — Statik tarama (~15k)**
- SAST · semgrep (`sec-sast-kosucu`), file:line triyaj · opengrep kural gerekirse `opengrep-rule-generator-research`
- Sır · gitleaks geçmiş dahil (`sec-gitleaks-gecmis`) — konum raporlanır, değer asla · fikstür/mock yanlış alarm elenir
- Bağımlılık · `sec-bagimlilik-acik` (güncel CVE, güvenli yükseltme)
- Kapı: bulgu eşiği · inceleme: `ecc:security-reviewer`

**Faz 3 — Dinamik + yetkilendirme (~12k)**
- DAST · ZAP (prod build pnpm build+start, localhost:3000, zap-report.html) — ADAY aracı, kurulum gerekir
- Ajan pentest · strix (hedef uygulamada zafiyet) · ödeme akışı Stripe MCP test modu
- Yetkilendirme · `sec-yetkilendirme-matrisi` (rol×aksiyon, her endpoint zorluyor mu) · `sec-owasp-top10` eşleme
- Kapı: — · İnceleme: `ecc:security-reviewer` + `differential-review:adversarial-modeler` (yüksek risk bulgular)

**Faz 4 — Rapor (~5k):** `sec-guvenlik-raporu` öncelikli bulgu + düzeltme adımı · kapanış ≤15 satır
Kullanılmadı: web tasarım/a11y/SEO kapıları (test işi, yeniden yapım değil); frontend-craft (UI üretimi yok).

Atladığım/kontrol etmediğim: ZAP ve strix bu ortamda kurulu değil (karar ADAY/CLI) — Faz 3 başlamadan kurulum+yetki teyidi gerekir; aksi halde SAST+pentest-ajanıyla sınırlı kalınır. TELVE'de R3F mi vanilla three.js mi kararı verilmedi, a11y/scroll-rig seçimi ona bağlı.
### Y
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

## 8. README'deki kurulum komutundaki yazım hatasını düzelt.
### X
**Faz 1: bul ve düzelt** (~2k jeton)
- Adım: Grep ile README'de kurulum satırını bul (`-n`, files_with_matches). Read ile ~10 satır oku, yazım hatasını tek Edit ile düzelt.
- Araç: Grep, Read, Edit. Skill ya da ajan gerekmiyor, tek satırlık iş.
- Kapı: düzeltilmiş komutu kaynağıyla karşılaştır (paket adı, marketplace yolu, bayrak). Komut zararsızsa (`--help`, `--dry-run`) bir kez koştur. Gerçek kurulum yapılmaz.
- İnceleme: gerekmiyor. `git diff` tek satır mı, ona bakılır.
- Tartışma noktası: yok. Aynı yazım hatası başka dokümanlarda da varsa raporda belirtilir, kapsam genişletilmez.
### Y
README'deki kurulum komutunda yazım hatası düzeltme. Tek satırlık iş olduğu için kısa plan.
- **F1 Bul** · `Grep -n` ile `README*` içinde kurulum komutunu bul. Ardından o satırın ±10 satırını `Read` ile oku. · Kapı: hatalı belirteç tek mi, kontrol et. Aynı komut `docs/` altında ya da başka README'lerde tekrar ediyorsa `Grep files_with_matches` ile bul ve hepsini düzelt. · ~1k jeton
- **F2 Düzelt** · `Edit` ile yalnız hatalı belirteci değiştir, çevredeki metne dokunma. · Kapı: düzeltilmiş komut gerçekten çalışmalı. `--help` ya da kuru koşu (`--dry-run` / `/plugin marketplace add` benzeri) ile sına. Bu bir paket kurulumuysa gerçek kurulumu çalıştırma. · ~1k jeton
- **İnceleme:** Yok, tek satırda inceleyici ajana gerek yok. CLAUDE.md'deki "basit işte bu ağırlık uygulanmaz" kuralı geçerli.
- **Tartışma noktası:** Doğru yazım belirsizse, örneğin paket adının iki farklı biçimi varsa, kayıt defterinden (`npm view` / `gh repo view`) doğrula. Tahminle düzeltme yapma.
- **Kapanış:** commit `docs: README kurulum komutu yazım hatası`. Test sayısı yok, CI'da yalnız markdown lint koşuyorsa o koşar.

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
### Y
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
