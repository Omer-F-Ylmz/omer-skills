## 1. Next.js uygulamasına gerçek zamanlı ortak düzenleme ekle: Yjs CRDT, WebSocket sunucusu, çevrimdışı birleştirme, imleç varlığı ve yük altında gecikme ölçümü.
### X
Varsayımlar: Next.js App Router kullanılıyor ve Postgres var. Vercel serverless kalıcı WebSocket bağlantısını tutamaz, bu yüzden WS sunucusu ayrı bir Node süreci olarak çalışır.
Kabul ölçütleri:
- İki istemci çevrimdışıyken düzenler, bağlantı gelince belgeler bayt bayt aynı olur.
- Oda başına 200 istemcide uçtan uca güncelleme p95 değeri 150 ms'nin altında kalır. Eşiği Ömer onaylar.

- **F0 Keşif (5k):** `graphify query "editör, auth, veri katmanı"` → `jev ilgili`. Durum `.claude/dalga.md` dosyasına yazılır.
- **F1 Mimari (15k):** Agent `Realtime Collaboration Engineer` + Skill `ecc:backend-patterns`.
  - **Tartışma:** y-websocket (en az kod) ile `@hocuspocus/server` karşılaştırılır. Hocuspocus'ta auth, kalıcılık ve Redis eklentileri hazır, öneri Hocuspocus.
  - Kalıcılık: Postgres bytea anlık görüntü + periyodik sıkıştırma. Böylece tombstone birikmesi sınırlanır.
  - İnceleyen: `inc-mimari-inceleme`.
- **F2 WS sunucusu (25k):** Agent `dil-websocket` (heartbeat, yeniden bağlanma, backpressure), Agent `ops-nginx-ters-vekil` (Upgrade başlıkları, `proxy_read_timeout`).
  - `onAuthenticate` içinde Next oturum JWT'si ve oda yetkisi doğrulanır. Mesaj boyutuna sınır konur.
  - Kapı: vitest birim testleri + Skill `security-reviewer` (WS upgrade auth, oda IDOR).
  - İnceleyen: `ecc:security-reviewer`.
- **F3 İstemci ve çevrimdışı (25k):** Skill `ecc:frontend-patterns` ve `ecc:react-performance`.
  - Kütüphaneler: yjs, TipTap `Collaboration`, `y-indexeddb`, `HocuspocusProvider`. `fe-pwa-cevrimdisi` yalnız uygulama kabuğu önbelleği istenirse kullanılır.
  - Kapı: Agent `qa-ozellik-tabanli` fast-check ile 3 Y.Doc'a rastgele işlem uygular, ağı bölüp birleştirir. Sonra `encodeStateAsUpdate` eşitliği kontrol edilir (yakınsama).
  - İnceleyen: `ecc:code-reviewer`.
- **F4 İmleç varlığı UI (15k):** Önce Skill `frontend-craft` (UI kuralı gereği zorunlu).
  - Parçalar: `y-protocols/awareness` + CollaborationCursor. Ad etiketlerinde kontrast kontrol edilir, katılım `aria-live="polite"` ile bildirilir.
  - Kapı: Agent `qa-erisilebilirlik-testi` (axe + klavye) ve frontend-craft Bölüm 6 tur raporu.
  - İnceleyen: `fe-tasarim-incele`.
- **F5 E2E (15k):** Agent `qa-playwright`.
  - Senaryo: 2 tarayıcı bağlamı açılır. Birinde `setOffline(true)` → düzenle → tekrar çevrimiçi → içerikler eşit ve imleç görünür olmalı.
  - Kapı: CI yeşil.
- **F6 Yük ve gecikme (20k):** Senaryoyu Agent `qa-yuk-testi` tasarlar.
  - Betik: Node ile `bench/ws-gecikme.mjs`. N sağlayıcı açılır, güncellemeye zaman damgası konur, alıcıda p50/p95/p99 hesaplanır. k6 kurulu değil ve gerek yok.
  - Tavan: yalnız staging, en çok 500 istemci, en çok 3 koşu.
  - Kapı: p95 eşiği. Aşılırsa Agent `ecc:performance-optimizer` devreye girer.
- **F7 Yayın (10k):** Skill `deploy-app` (WS sunucusu ayrı servis) → Agent `git-pr-yoneticisi`.
  - İnceleyen: `inc-uretim-hazirligi`.
  - **Tartışma:** Tek düğüm yeterli mi? Redis eklentisi ancak ölçüm gerektirirse eklenir.
### Y
Varsayımlar: App Router kullanılıyor, editör olarak TipTap/ProseMirror var, kalıcı veri Postgres'te. Değilse yalnız 2. fazdaki bağlayıcı değişir.

**Faz 1 · Tasarım (~10k)**
- Adım: belge modelini (Y.Doc, oda = belge id) çıkar. Kalıcılık için güncellemeler bayt dizisi olarak saklanır, N güncellemede bir sıkıştırılır. WS el sıkışmasında JWT ile oda yetkisi denetlenir.
- Araç: Agent Realtime Collaboration Engineer, Agent dil-websocket.
- Tartışma: y-websocket mi, Hocuspocus mu (kalıcılık ve yetki kancaları hazır gelir)? Yatay ölçekte Redis pub/sub gerekecek mi? Geri alınabilir bir karar olduğu için konsey yok.
- Kapı: oda başına yetki matrisi yazılı. WS mesajı ≤1 MB. Bağlantı hız sınırı belirlenmiş.

**Faz 2 · Uygulama (~40k)**
- Sunucu: ayrı Node WS süreci, Next route handler'da çalışmaz. Heartbeat 30 s, geri basınç, nginx'te `Upgrade` başlığı. Araç: Skill ecc:backend-patterns, Agent ops-nginx-ters-vekil.
- İstemci: yjs + y-websocket provider + y-indexeddb ile çevrimdışı tampon. Yeniden bağlanınca durum vektörü farkı gönderilir. Araç: Skill ecc:frontend-patterns, Agent fe-pwa-cevrimdisi.
- İmleç varlığı: awareness protokolü (ad, renk, seçim). Ekrandan çıkan kullanıcı 30 s içinde silinir. Awareness ayrı tutulur, böylece Y.Doc gereksiz render tetiklemez. Araç: önce Skill frontend-craft (UI kuralı), sonra Skill ecc:react-performance.
- İnceleme: her faz sonunda Agent ecc:code-reviewer.

**Faz 3 · Test + güvenlik + gecikme (~20k, test koşusu sonnet alt ajanında)**
- Birleştirme testi: 2 istemci çevrimdışıyken aynı paragrafa yazar. Bağlantı gelince iki Y.Doc bayt bayt aynı olmalı, kayıp karakter 0.
- Yük testi: k6 ile `k6/experimental/websockets`, rampa 50 → 500 eşzamanlı istemci, oda başı 20. Araç: Agent qa-yuk-testi.
  - Kapı: güncelleme yayılımı p95 ≤150 ms, p99 ≤400 ms. Hata oranı <%0.5. Sunucu RSS 30 dk boyunca artmamalı.
- Web kapısı: LCP ≤2.5 s, INP ≤200 ms, ilk yük JS ≤170 KB gz. Yjs dinamik import ile yüklenir.
- Erişilebilirlik: Agent qa-erisilebilirlik-testi, 0 ciddi ihlal. İmleç etiketleri ekran okuyucuda gürültü yapmamalı (`aria-hidden`).
- Güvenlik: Agent ecc:security-reviewer. Yetkisiz odaya katılma reddedilir, el sıkışmada Origin denetlenir. semgrep 0 yüksek, gitleaks 0 bulgu.

**Faz 4 · Yayın + kapanış (~5k)**
- Adım: önce staging. Geri alma, eski istemciye dönüş (≤5 dk). frontend-craft Section 6 tur raporu yazılır.
- Araç: Skill deploy-app.
- Kapanış: test, semgrep, gitleaks, a11y, k6 özeti. Rapor: commit, test sayısı, CI, sapmalar.
### Z
**Varsayımlar:** Next.js App Router, Node 20. WebSocket sunucusu ayrı bir süreç olarak çalışacak, çünkü Next route handler kalıcı WS bağlantısı tutamaz.

**F0 Hazırlık (~2k)**
- dalga.md yazılır (KARAR · kabul · durum).
- `graphify query "editör bileşeni, auth, kalıcılık"`.
- Skill /frontend-craft (UI kuralı, imleç katmanı için) + Skill ecc:frontend-patterns.

**F1 Tasarım (~10k)**
- Sunucu tasarımı: Agent Realtime Collaboration Engineer + Agent dil-websocket. Kapsam: heartbeat, backpressure, yeniden bağlanma, Redis pub/sub ile yatay ölçek.
- Kütüphaneler: yjs, @hocuspocus/server, y-indexeddb, y-protocols/awareness (ad, renk, imleç; 30 sn zaman aşımı).
- Kalıcılık: Yjs güncellemeleri Postgres bytea'da tutulur, `encodeStateAsUpdate` ile periyodik sıkıştırılır.
- Çevrimdışı: Agent fe-pwa-cevrimdisi (SW önbelleği, güncelleme akışı) + y-indexeddb.
- Auth: WS el sıkışmasında ≤5 dk ömürlü JWT, belge başına okuma/yazma yetkisi.
- Tartışma noktası: Hocuspocus (hazır auth/persist kancaları) mı, çıplak y-websocket (daha az bağımlılık) mı. Konsey yok, çünkü ikisi aynı protokolü kullanıyor ve karar geri alınabilir.
- İnceleme: ecc:code-reviewer.

**F2 Uygulama (~35k)**
- TDD: önce kırmızı test yazılır. İki Y.Doc çevrimdışı yazar; `applyUpdate` sonrası metinler eşit olmalı.
- `apps/collab` sunucusu ve `useCollab` kancası.
- İmleç katmanı: imleçler aria-hidden; katılımcı listesi ekran okuyucuya okunur.
- Skill ecc:react-performance: awareness ≤20 Hz throttle, imleç katmanı memo.
- Agent ops-nginx-ters-vekil: Upgrade başlıkları, proxy_read_timeout ≥75 sn.
- Skill sentry-nextjs-sdk: WS kopma ve yeniden bağlanma olayları, PII yok.
- İnceleme: ecc:code-reviewer.

**F3 Test + güvenlik (~15k, alt ajan sonnet)**
- Çakışma testi: Vitest + Agent qa-e2e-playwright, 2 sekme, headless, eşzamanlı çevrimdışı yazım. Kapı: birleşen durumlar eşit.
- Yük testi: Agent qa-yuk-testi, k6 `k6/experimental/websockets`. Tavan: en çok 500 VU × 10 dk, yalnız staging.
  - Kapı: yankı gecikmesi p95 ≤150 ms, p99 ≤400 ms, hata <%0.1.
  - Kapı: sunucu RSS artışı 10 dk'da ≤%10.
- Web kapıları: LCP ≤2.5 sn · CLS ≤0.1 · INP ≤200 ms · ilk yük JS ≤170 KB gz (editör dinamik import ile yüklenir).
- Erişilebilirlik: Agent qa-erisilebilirlik-testi 0 ciddi ihlal + klavye turu.
- Güvenlik: Agent ecc:security-reviewer. Kontroller: WS auth, belge ID'de IDOR, mesaj ≤1 MB, hız sınırı. Ek kapılar: semgrep 0 yüksek, gitleaks 0 bulgu.

**F4 Yayın + kapanış (~4k)**
- Skill ecc:production-audit.
- Önce staging, sonra özellik bayrağıyla %10 kullanıcı. Geri alma: bayrağı kapat (≤5 dk).
- frontend-craft Bölüm 6 tur raporu, kapanış raporu (commit · test · CI · sapma), dalga.md silinir.
- Atlanan araç: deploy-app, netlify ve cloudflare skill'leri. Neden: barındırma belli değil ve kalıcı WS gerekiyor.

## 2. Kotlin Android bankacılık uygulamasına biyometrik giriş ve sertifika sabitleme ekle; Play Store aşamalı yayın, çökme izleme ve KVKK aydınlatma metni.
### X
**Varsayımlar:** Compose, OkHttp/Retrofit, Gradle KTS; sunucu tarafında auth zaten var.

**F0 (~2k)**
- dalga.md yazılır.
- Skill departman-guvenlik (sıra: sır taraması → SAST → KVKK).
- `graphify query "login akışı, ağ istemcisi"`.

**F1 Tasarım + KVKK (~12k)**
- Skill ecc:android-clean-architecture: auth modülünün sınırları.
- Biyometrik giriş:
  - BiometricPrompt, BIOMETRIC_STRONG + CryptoObject.
  - Keystore anahtarında `setUserAuthenticationRequired(true)` ve `setInvalidatedByBiometricEnrollment(true)`.
  - Yenileme jetonu bu anahtarla şifrelenir.
  - Yedek giriş: cihaz PIN'i değil, uygulama şifresi.
- Sertifika sabitleme:
  - OkHttp CertificatePinner (SPKI sha256) + network_security_config pin-set expiration.
  - En az 1 yedek pin, farklı anahtar veya CA'dan.
  - Pin döndürme takvimi: Agent ops-sertifika-yenileme.
- KVKK sırası: Skill use-case-triage → Skill pia-generation → Agent sec-kvkk-gdpr-kontrol.
  - Biyometrik veri cihazda kalır, sunucuya gitmez.
  - Skill policy-monitor aydınlatma metnini taslaklar (amaç, hukuki sebep, aktarım, md.11 hakları). Son onay hukukçuda.
- Konsey (ecc:council 1 kez, ~60–90k): çökme verisi Sentry SaaS'a mı gider (yurt dışı aktarım, KVKK md.9), yoksa yurt içinde self-hosted Sentry mi kurulur? Gerekçe: aktarılan veri geri alınamaz ve iki makul seçenek var.
- Tartışma noktası: biyometrik kayıt değişince anahtar geçersizleşir ve kullanıcı yeniden şifreyle girmek zorunda kalır (UX ile güvenlik arasında seçim).

**F2 Uygulama (~35k)**
- Skill ecc:kotlin-patterns + ecc:kotlin-coroutines-flows (auth durumu Flow ile).
- UI: /frontend-craft + Skill mobile-android-design. TalkBack etiketleri; biyometri reddedilince zarif düşüş.
- Skill sentry-android-sdk:
  - beforeSend ile IBAN, TCKN ve ad temizlenir.
  - Ekran görüntüsü ve view hierarchy kapalı; kullanıcı ID'si hash'lenir.
- Rıza ve aydınlatma: ayrı, önceden işaretsiz açık rıza kutusu; aydınlatma metni ilk açılışta gösterilir; saklama süresi yazılır; silme talebi ≤30 gün.
- Derleme hataları için Agent ecc:kotlin-build-resolver.
- İnceleme: Agent ecc:kotlin-reviewer + ecc:code-reviewer.

**F3 Test + güvenlik (~15k, alt ajan sonnet)**
- Skill ecc:kotlin-testing (Kotest/MockK) ile senaryolar: anahtarın geçersizleşmesi, iptal, 5 başarısız deneme → kilit.
- Pinning testleri: MockWebServer'da yanlış sertifika → SSLPeerUnverifiedException. Elle test: mitmproxy kullanıcı CA'sı reddedilmeli.
- Auth kapıları: erişim jetonu ≤15 dk, yenileme jetonu döndürme, giriş 5 deneme/dk.
- Mobil kapılar: soğuk açılış ≤2 sn (Macrobenchmark); biyometri olmayan cihazda düşüş; çevrimdışı → çevrimiçi oturum yenileme.
- Güvenlik: Agent ecc:security-reviewer + Agent sec-cikis-oncesi-guvenlik (MASVS-AUTH/NETWORK/STORAGE). Ek kapılar: semgrep 0 yüksek, gitleaks 0 bulgu, R8 açık.

**F4 Yayın (~6k)**
- Agent Mobile Release Engineer:
  - Play App Signing ve fastlane supply.
  - Sıra: internal → closed → üretimde %1 → %5 → %20 → %50 → %100.
- Agent git-canary-izleme: her basamak ≥48 saat.
  - Kapı: crash-free kullanıcı ≥%99.5, ANR <%0.47.
  - Kapı: giriş başarı oranındaki düşüş <%1.
- Geri alma: Play'de sürüm düşürülemez. Rollout durdurulur (≤5 dk), ardından düzeltme sürümü çıkar. Pin hatasını uzaktan kapatmanın yolu olmadığı için yedek pin zorunlu.
- Agent git-yayin-oncesi-kontrol ile go/no-go, Skill departman-surec-git-yayin, kapanış raporu.
- İstenmediği için plana alınmayanlar: root/tamper tespiti ve Play Integrity (bankacılıkta önerilir).
### Y
Varsayımlar: Compose + Retrofit/OkHttp kullanılıyor ve Play Console erişimi var.
Kabul ölçütleri:
- Oturum anahtarı yalnız BIOMETRIC_STRONG + CryptoObject ile açılır.
- Yanlış sertifikada bağlantı kesilir.
- Aşamalı yayının durdurma eşiği tanımlıdır.
- Aydınlatma metni hukuk onaylıdır.

- **F0 (5k):** Skill `departman-guvenlik` (sır taraması → SAST → KVKK) ve `departman-surec-git-yayin` (yayın sırası). Auth ve ağ katmanı `graphify` + `jev` ile bulunur.
- **F1 KVKK önce (15k):** Skill `use-case-triage` → `pia-generation` → `policy-monitor` (aydınlatma metni taslağı). Agent `sec-kvkk-gdpr-kontrol`.
  - **Tartışma:** Biyometrik şablon cihazda kalır ve uygulamaya gelmez. Bu durum m.6 özel nitelikli veri kapsamını etkiler mi? Hukukla netleştirilir.
  - **Tartışma:** Crashlytics ABD'ye aktarır (m.9). Alternatif kendi sunucumuzda Sentry.
  - Kapı: hukuk onayı (insan).
- **F2 Biyometrik (25k):** Skill `android-paket` (güvenlik alt skill'i), `ecc:kotlin-patterns`, `ecc:kotlin-coroutines-flows`.
  - Uygulama: `androidx.biometric` BiometricPrompt ve Keystore AES-GCM anahtarı. Anahtarda `setUserAuthenticationRequired(true)` ve `setInvalidatedByBiometricEnrollment(true)` açık. Refresh token bu anahtarla şifrelenir.
  - Yedek yol: biyometrik kullanamayan kişi için uygulama şifresi.
  - **Tartışma:** CryptoObject zorunlu. Yalnız boolean callback'e dayanan doğrulama Frida ile atlatılır.
  - Kapı: Skill `ecc:kotlin-testing` (MockK) + emülatörde `adb -e emu finger touch 1` enstrümante testi. TalkBack ile prompt ve biyometriksiz yol denenir.
  - İnceleyen: `ecc:kotlin-reviewer` + `sec-sifreleme-denetci`.
- **F3 Sertifika sabitleme (20k):** OkHttp `CertificatePinner` + `network_security_config` içinde `<pin-set expiration>`.
  - SPKI sha256 ile en az 2 pin konur (birincil + yedek anahtar).
  - Agent `ops-sertifika-yenileme` pin rotasyon takvimini ve runbook'u çıkarır.
  - **Tartışma:** Pin süresi dolarsa istemci kilitlenir. Güvenlik açısından önlem pinleri gevşetmek değil, `IMMEDIATE` modunda zorunlu güncelleme.
  - Kapı: MockWebServer'a yanlış sertifika → `SSLPeerUnverifiedException` testi. Release APK `droidasc` ile açılır, pin, R8 ve gömülü sır kontrol edilir.
  - İnceleyen: Skill `security-reviewer` + `ecc:security-reviewer`.
- **F4 Çökme izleme (10k):** F1'de Sentry seçilirse Skill `sentry-android-sdk` kullanılır.
  - `sendDefaultPii=false`, `beforeSend` içinde IBAN ve TCKN maskelenir, mapping dosyası yüklenir.
  - Kapı: Agent `sec-loglama-gizlilik`. Staging'e en çok 5 test çökmesi gönderilir.
- **F5 Aşamalı yayın (15k):** Agent `Mobile Release Engineer` (Play App Signing, fastlane supply `--rollout 0.01`).
  - Agent `git-canary-izleme`: aşamalar %1 → 5 → 20 → 50 → 100. Crash-free oranı %99,5'in altına düşer ya da ANR %0,47'yi geçerse yayın durdurulur (halt).
  - Kapı: `git-yayin-oncesi-kontrol` + `sec-cikis-oncesi-guvenlik` + Play pre-launch raporu + `gradle test lint`.
  - Tavan: aşama başına en çok 10 Play API çağrısı. Her aşama dışarıya açık bir işlem olduğu için Ömer onaylar.
### Z
Varsayımlar: OkHttp/Retrofit ve Compose kullanılıyor. Yönetici skill'ler: Skill departman-guvenlik (güvenlik sırası) ve Skill departman-surec-git-yayin (yayın).

**Faz 1 · Tasarım + KVKK (~15k)**
- Biyometri: BiometricPrompt, yalnız `BIOMETRIC_STRONG` ve CryptoObject. Keystore anahtarı `setUserAuthenticationRequired(true)` ve `setInvalidatedByBiometricEnrollment(true)` ile üretilir. Yeni parmak izi eklenince anahtar düşer ve şifreyle yeniden kayıt istenir. Araç: Skill ecc:android-clean-architecture.
- Sabitleme: SPKI pin'leri hem network_security_config'e hem OkHttp CertificatePinner'a konur. En az 1 yedek anahtar pini ve `expiration` tarihi olur. Araç: Agent ops-sertifika-yenileme (rotasyon takvimi).
- KVKK: biyometrik şablon cihazdan çıkmaz, uygulama özel nitelikli veri işlemez. Aydınlatma metni bunu, çökme verisini ve yurt dışı aktarımı anlatır. Araç: Skill pia-generation, Skill policy-monitor, Agent sec-kvkk-gdpr-kontrol.
- Konsey 1 kez (~60-90k): pin hedefi ara CA mı, yaprak SPKI mı? Gerekçe: dağıtılmış eski sürümler kilitlenebilir, yani karar geri dönüşsüz ve iki seçenek de makul.
- Kapı: aydınlatma metni hukuk onayında. Açık rıza kutusu ayrı ve önceden işaretsiz. Saklama süresi yazılı.

**Faz 2 · Uygulama (~40k)**
- Kod: Skill ecc:kotlin-patterns ve Skill ecc:kotlin-coroutines-flows. Giriş ekranı için önce Skill frontend-craft, sonra Skill mobile-android-design. Derleme hatasında Agent ecc:kotlin-build-resolver.
- Çökme izleme: Skill sentry-android-sdk. `sendDefaultPii=false`, `beforeSend` ile IBAN/TCKN/token maskelenir, ekran görüntüsü kapalı.
- Auth: erişim jetonu ≤15 dk, yenileme jetonu döndürülür, sunucuda 5 deneme/dk sınırı.
- İnceleme: her faz sonunda Agent ecc:kotlin-reviewer ve Agent ecc:code-reviewer.

**Faz 3 · Test + güvenlik (~20k, sonnet alt ajanında)**
- Birim testleri: Skill ecc:kotlin-testing (MockK).
- Sabitleme testi: MockWebServer + HeldCertificate ile yanlış sertifikada bağlantı reddedilir (`SSLPeerUnverifiedException`).
- Biyometri testi: emülatörde `adb -e emu finger touch`. Hatalı parmak, yeni parmak kaydı ve iptal yolları denenir. İzin reddinde PIN'e zarif düşüş.
- Kapı: soğuk açılış ≤2 s. Log ve Sentry olayında PII 0. Agent ecc:security-reviewer ve Agent sec-cikis-oncesi-guvenlik. semgrep 0 yüksek, gitleaks 0 bulgu.

**Faz 4 · Aşamalı yayın (~8k)**
- Adım: önce iç test kanalı, sonra yüzde %1 → 5 → 20 → 50 → 100, her basamak ≥24 saat. Araç: Agent Mobile Release Engineer (fastlane supply), Agent git-canary-izleme.
- Durdurma eşiği: çökmesiz oturum <%99.5, ANR >%0.47 ya da kullanıcı çökmesi >%1.09 (Play vitals eşikleri) ise rollout durdurulur.
- Yayın öncesi: Agent git-yayin-oncesi-kontrol. Geri alma adımı yazılı olur.
- Kapanış raporu: commit, test sayısı, CI, sapmalar.

## 3. Kafka tabanlı sipariş olay akışını kur: outbox deseni, tam bir kez işleme, ölü mektup kuyruğu, şema kayıt defteri ve tüketici gecikmesi alarmı.
### X
**Varsayımlar:** sipariş servisi Postgres kullanıyor. Dil belirtilmemiş; plan Java istemcisine ya da librdkafka'ya göre yazıldı.

**F0 (~2k)**
- dalga.md yazılır.
- Skill departman-veri-db.
- `graphify query "sipariş yazma yolu, transaction sınırı"`.

**F1 Tasarım (~8k)**
- Agent ops-kafka:
  - Topic `orders.v1`; anahtar order_id, sırayı bu korur.
  - Ayarlar: RF=3, min.insync.replicas=2, acks=all; retention yazılır.
- Agent be-mesaj-guvenilirligi: outbox, idempotent tüketici ve DLQ deseni.
- Agent db-sema-tasarim:
  - `outbox` tablosu: id uuid, aggregate_id, type, payload, created_at.
  - `processed_events` tablosu: PK (consumer, event_id).
- Outbox yayıncısı: Debezium Outbox Event Router mı, `SKIP LOCKED` ile polling mi? Tartışma noktası. Geri alınabilir olduğu için konsey yok.
- "Tam bir kez" tanımı kabul ölçütüne yazılır:
  - Kafka EOS (idempotence, transactional.id, read_committed) yalnızca Kafka→Kafka yolunu kapsar.
  - DB yan etkisi, aynı transaction içinde `processed_events` kaydıyla tek kez uygulanır.
- Şema kayıt defteri: Confluent veya Apicurio.
  - Konsey (ecc:council 1 kez, ~60–90k): Avro mu Protobuf mu?
  - Gerekçe: topic'e veri yazıldıktan sonra format değiştirilemez.
  - Uyumluluk modu: BACKWARD_TRANSITIVE.
- KVKK: olaya adres veya telefon konmaz, yalnız referans ID taşınır (minimizasyon).

**F2 Uygulama (~35k)**
- TDD: önce kırmızı test. Aynı olay 2 kez teslim edilir; yan etki 1 kez olmalı.
- Akış:
  - İş transaction'ı içinde outbox insert yapılır, ardından yayıncı çalışır.
  - Tüketici read_committed, manuel commit ve `processed_events` ile işler.
- DLQ:
  - Topic'ler: `orders.v1.retry.1m`, `.retry.10m`, `.dlq`.
  - Serileştirme hatası doğrudan DLQ'ya gider; başlıkta hata nedeni ve orijinal offset tutulur.
  - Yeniden oynatma betiği: koşu başına en çok 1000 mesaj.
- Lag alarmı: kafka-lag-exporter → Agent ops-prometheus.
  - Uyarı: `kafka_consumergroup_lag > 1000 for 5m`.
  - Kritik: lag süresi >60 sn.
  - Uyarı: DLQ oranı >0.
- Pano: Agent ops-grafana-pano.
- İnceleme: ecc:code-reviewer.

**F3 Test + güvenlik (~12k, alt ajan sonnet)**
- Agent qa-entegrasyon-testi: Testcontainers ile Kafka + Postgres + Schema Registry.
- Agent qa-ozellik-tabanli: rastgele yinelenen ve sırasız teslim; kapı: son durum değişmez.
- Kaos testleri:
  - Tüketiciyi commit öncesi 100 kez öldür. Kapı: yan etki sayısı = olay sayısı.
  - Broker'ı yeniden başlat. Kapı: kayıp 0.
- Şema kapısı: CI'da uyumsuz şema kaydı reddedilmeli (negatif test).
- Alarm kapısı: `promtool test rules` ile alarm ≤6 dk içinde ateşlenmeli.
- Güvenlik: ecc:security-reviewer. Kontroller: SASL/SCRAM veya mTLS, ACL'ler, DLQ'da PII olmaması. Ek kapılar: semgrep 0 yüksek, gitleaks 0 bulgu.

**F4 Yayın (~4k)**
- Gölge mod: yeni tüketici ayrı bir grupla paralel çalışır, çıktılar karşılaştırılır, sonra geçiş yapılır.
- Geri alma: eski yol bayrakla açılır (≤5 dk). Outbox birikmeye devam ettiği için veri kaybolmaz.
- Agent dok-runbook (DLQ boşaltma, lag müdahalesi), kapanış raporu.

---
- **Araç çağrısı iki kez çalıştı:** `plan_kur.py` ilk denemede ters eğik çizgili yol yüzünden açılamadı, düz eğik çizgiyle yeniden çalıştırıldı; yani çıktı veren tek çağrı var.
- **Bütçe ve araç seçimi:** 1. ve 2. işin jeton bütçeleri sıkıştırılmış çıktıda okunamadı, bu yüzden 3. işin değerlerine (8k · 35k · 12k · 3k) bakarak tahmin ettim. Aday listede olmayan ama kurulu olan ajanları da ekledim: ops-prometheus, ops-grafana-pano, qa-entegrasyon-testi, qa-e2e-playwright, dok-runbook.
- **Kontrol etmediklerim:** yük ve kaos eşikleri genel varsayılan değerler; gerçek SLO ile karşılaştırmadım.
### Y
Varsayımlar: Postgres var, servis dili keşifte netleşir. Kafka için yerelde docker compose kullanılır.
- Kafka dışındaki bir yan etkide "tam bir kez" mümkün değil. Hedef: en az bir kez teslim + idempotent tüketici ile etkin tek kez. Kabul ölçütü buna göre yazılır.

- **F0 (5k):** Skill `departman-veri-db` (şema → migration → sorgu). `graphify query "sipariş oluşturma, transaction sınırı"` → `jev ilgili`.
- **F1 Tasarım (20k):** Agent `ops-kafka` ve Agent `be-mesaj-guvenilirligi`.
  - Topic `orders.v1`, anahtar `order_id` (sıra korunur). `acks=all` ve `enable.idempotence` açık.
  - **Tartışma:** Debezium Outbox Event Router (CDC, Connect işletmek gerekir) ile polling `FOR UPDATE SKIP LOCKED` karşılaştırılır. Hacim düşükse öneri polling.
  - **Tartışma:** Kafka EOS (transactional producer + `read_committed`) yalnız Kafka→Kafka adımlarında kullanılır.
  - İnceleyen: `inc-mimari-inceleme`.
- **F2 Outbox (20k):** Agent `db-sema-tasarim` + `db-migration-planlayici`.
  - Tablo: `outbox(id uuid, aggregate_id, type, payload, created_at, published_at)`. Yayınlanmamış satırlar için kısmi indeks konur.
  - Sipariş ve outbox kaydı aynı transaction'da yazılır.
  - Kapı: Agent `qa-entegrasyon-testi` (Testcontainers ile Postgres + Kafka). Rollback olursa olay çıkmamalı. Yayıncı çökerse olay tekrarlanabilir ama kaybolmamalı.
- **F3 Şema kayıt defteri (15k):** Apicurio (Apache-2) ile Confluent SR karşılaştırılır.
  - Confluent SR, Confluent Community License altında. Seçilirse koşulları rapora yazılır.
  - Avro, uyumluluk modu BACKWARD.
  - Kapı: Agent `otm-sema-dogrulayici` CI'da `/compatibility` uç noktasıyla kontrol eder. Kırıcı şema değişikliği içeren PR kırmızı olur.
- **F4 Tüketici ve DLQ (25k):** `processed_events(event_id PK)` kaydı ve iş yan etkisi aynı transaction'da yazılır, ofset sonra commit edilir.
  - Yeniden deneme: `orders.retry.1m` ve `.10m` → `orders.dlq`. Başlıklarda hata, deneme sayısı ve kaynak ofset tutulur.
  - Replay betiği tek çalıştırmada en çok 1000 mesaj işler.
  - Kapı: Agent `qa-ozellik-tabanli`. Tekrarlı ya da sıra dışı teslimde yan etki sayısı benzersiz olay sayısına eşit olmalı. Zehirli mesaj DLQ'ya tam 1 kez düşmeli.
  - İnceleyen: `ecc:code-reviewer`.
- **F5 Gecikme alarmı (15k):** kminion → Prometheus. Agent `ops-prometheus` ve `ops-grafana-pano`.
  - Kurallar: `lag > 1000 for 5m` ve zaman tabanlı lag eşiği.
  - Kapı: `promtool test rules`. Staging'de tüketici durdurulunca alarm en geç 6 dakikada tetiklenmeli.
- **F6 Güvenlik ve KVKK (10k):** Agent `sec-kvkk-gdpr-kontrol`.
  - Olay yükünde adres yerine `customer_id` taşınır. Topic ve DLQ için saklama süresi belirlenir.
  - Skill `security-reviewer`: SASL/SCRAM + TLS ve topic ACL'leri (yayıncı yalnız yazar, tüketici yalnız okur).
  - İnceleyen: `ecc:security-reviewer`.
- **F7 Kapanış (5k):** `dok-runbook` (DLQ replay ve lag alarmı) → `git-pr-yoneticisi`.

Katalog listede olmayan bazı ajanları da kullandım (`ops-prometheus`, `sec-loglama-gizlilik`, `inc-mimari-inceleme`, `dok-runbook`); hepsi oturumdaki ajan listesinde var. k6, Debezium, Apicurio ve kminion bu makinede kurulu değil, kurulu olup olmadıklarını da denetlemedim. En büyük iki risk iş 2'de: pin rotasyonu yanlış giderse istemciler kilitlenir, aydınlatma metni de hukuk onayı olmadan yayına çıkamaz.
### Z
Varsayımlar: Postgres sipariş veritabanı ve Kafka KRaft var. Dil belirtilmemiş; ilk iş bunu doğrulamak. Yönetici skill: Skill departman-veri-db.

**Faz 1 · Tasarım (~8k)**
- Konular: `orders.events` (anahtar = order_id, böylece sipariş başına sıra korunur), `orders.retry.1m/10m`, `orders.dlq`. Bölüm sayısı hedef tüketici sayısının 2-3 katı. Araç: Agent ops-kafka.
- Teslim semantiği: Kafka EOS yalnız Kafka içinde geçerli. Dış yan etki için idempotent tüketici gerekir: `processed_events(event_id PK)` tablosu, iş yazımıyla aynı DB işleminde. Araç: Agent be-mesaj-guvenilirligi.
- Tartışma: outbox Debezium CDC (Outbox Event Router SMT) ile mi, yoklama ile mi? Geri alınabilir olduğu için konsey yok. Bölüm anahtarı sonradan değiştirilemez, burada kesinleşir.
- KVKK: olayda yalnız customer_id taşınır, adres/ad taşınmaz. `retention.ms` yazılı olur.

**Faz 2 · Uygulama (~35k)**
- Outbox: `outbox` tablosu sipariş yazımıyla aynı işlemde doldurulur. Debezium yayınlar. Araç: Agent db-sema-tasarim.
- Şema kayıt defteri: Avro, uyumluluk `BACKWARD_TRANSITIVE`. CI'da uyumluluk denetimi yapılır, kırıcı değişiklik reddedilir. Araç: Agent otm-sema-dogrulayici.
- Üretici: `enable.idempotence=true`, `acks=all`. Tüketici: `isolation.level=read_committed`, otomatik commit kapalı.
- DLQ: seri çözme hatası doğrudan DLQ'ya gider. İş hatası 2 retry'dan sonra DLQ'ya düşer. Başlıklarda hata, kaynak offset ve deneme sayısı taşınır. DLQ için yeniden oynatma betiği yazılır.
- Gecikme alarmı: kafka_exporter `kafka_consumergroup_lag`. Alarm: `sum by (consumergroup) > 1000` 5 dk sürerse uyarı, 10k olursa kritik. Araç: Agent ops-prometheus, Agent ops-grafana-pano.
- İnceleme: her faz sonunda Agent ecc:code-reviewer.

**Faz 3 · Test + güvenlik (~12k, sonnet alt ajanında)**
- Entegrasyon testi: Testcontainers ile Kafka, Postgres ve Debezium. 10k sipariş girer, tam 10k yan etki çıkmalı. Tüketici batch ortasında öldürülür, tekrar 0. Araç: Agent qa-entegrasyon-testi.
- Değişmezler: "aynı event_id iki kez işlenmez" ve "sipariş başına sıra korunur". Araç: Agent qa-ozellik-tabanli.
- Zehirli mesaj DLQ'ya düşer, akış durmaz. Lag alarmı tetiklenmesi sahnelenip doğrulanır.
- Güvenlik: Agent ecc:security-reviewer. SASL/TLS ve konu başına ACL. semgrep 0 yüksek, gitleaks 0 bulgu.

**Faz 4 · Yayın + kapanış (~3k)**
- Adım: önce staging. Debezium connector durdurulursa outbox birikir ama veri kaybolmaz; geri alma adımı yazılı olur.
- Kapanış raporu: commit, test sayısı, CI, sapmalar.

---
plan_kur.py tek çağrıyla koşturuldu, ek sorgu yapmadım. Dosya yazmadım, hiçbir işi uygulamadım. Listede olmayan ama kurulu bildiğim araçları ekledim: frontend-craft, ops-prometheus, ops-grafana-pano, qa-entegrasyon-testi, qa-erisilebilirlik-testi.

Önemli risk: 2. işte KVKK metni hukuki onay olmadan yayınlanmamalı. 3. işin dili ve 1. işin editörü bilinmiyor; varsayımlar bunlara göre ayarlanmalı.

## 4. Go ile yazılmış CLI aracını Homebrew, Scoop ve winget üzerinden dağıt: çapraz derleme, imzalı ikililer, otomatik sürüm notu ve kendini güncelleme.
### X
**Varsayım:** Repo GitHub'da, CI GitHub Actions. Sürüm aracı olarak projeye GoReleaser yapılandırması eklenir; GoReleaser yerelde kurulmaz, CI'da action olarak koşar. Mac imzası için macOS runner gerekir.
**Başlangıç:** `.claude/dalga.md` yazılır (KARAR · kabul ölçütleri · durum). Test ve log okuma işi sonnet alt ajanına verilir.

**F1 Tasarım (8k)**
- Adım: hedefleri sabitle: darwin/linux/windows × amd64/arm64, `CGO_ENABLED=0 -trimpath`, sürüm bilgisi `-ldflags -X main.version`. Semver etiket ve conventional commit kuralı yazılır.
- Araç: Agent dil-cli-araci (bayraklar, `--version`, çıkış kodları) · Agent Developer Tooling Engineer (dağıtım topolojisi: tap repo, scoop bucket, winget-pkgs PR akışı)
- Tartışma 1, imza: Windows için OV sertifikası mı, Azure Trusted Signing mi; macOS için Developer ID ve notarization. Bunlar paralı ve geri dönüşsüz alımlar. İki seçenek de makul ve veri yok, bu yüzden ecc:council 1 kez (~60-90k) koşar, karar Ömer'den alınır.
- Tartışma 2, kendini güncelleme: paket yöneticisiyle kurulan kopya kendini değiştirmez. Kurulum yolu brew/scoop/winget ise yalnız ilgili güncelleme komutunu yazar. Kendini güncelleme yalnız elle indirilen ikilide çalışır.
- Kapı: kabul ölçütleri dalga.md'de · İnceleme: ecc:code-reviewer

**F2 Uygulama (35k)**
- Adım: `.goreleaser.yaml` yazılır: builds matrisi, arşiv + `checksums.txt`, brews (tap), scoops (bucket), winget (manifest + winget-pkgs PR), changelog (commit gruplarına göre).
- Adım: `release.yml` yazılır; etiket push edilince tetiklenir. Linux işi derler, mac işi `codesign` + `notarytool` koşar, Windows işi `signtool` koşar. `checksums.txt` cosign keyless ile imzalanır.
- Adım: `selfupdate` alt komutu: GitHub Releases'ten en son sürüm alınır, `checksums.txt` imzası gömülü açık anahtar/kimlikle doğrulanır, SHA-256 karşılaştırılır. Windows'ta çalışan exe önce `.old` adıyla yeniden adlandırılır, sonra atomik değiştirme yapılır.
- Adım: sürüm notu GoReleaser changelog'undan çıkar. Agent dok-degisiklik-gunlugu Added/Changed/Fixed şablonunu kurar. Skill version-bump sonraki etiketi önerir.
- Araç: Agent dil-go · Agent git-ci-boru-hatti · Agent ecc:go-build-resolver (derleme kırılırsa)
- Sırlar: tap/bucket/winget PAT'i ve imza sertifikası GitHub secrets'ta durur, değerleri hiçbir komutla basılmaz.
- İnceleme: Agent ecc:go-reviewer + ecc:code-reviewer

**F3 Test + güvenlik (12k)**
- Test: `go test -race ./...` 0 kırmızı. Kendini güncelleme için 3 test: geçerli imzada güncellenir, oynanmış checksum reddedilir, paket yöneticisi yolunda güncelleme yapmaz.
- Kuru sürüm: `goreleaser release --snapshot --clean` CI'da koşar. `brew audit --strict`, `winget validate --manifest` ve scoop manifest JSON doğrulaması 0 hata vermeli.
- İmza doğrulama: `cosign verify-blob` · `signtool verify /pa` · `codesign --verify` + `spctl -a` hepsi geçmeli.
- Güvenlik: Agent sec-sast-kosucu (gosec + semgrep, 0 yüksek) · `govulncheck ./...` 0 erişilebilir açık · Agent sec-gitleaks-gecmis (0 bulgu)
- İnceleme: Agent ecc:security-reviewer. Odak, güncelleme kanalının tedarik zinciri: sürüm geri düşürme ve imzasız varlık riski.

**F4 Yayın + kapanış (3k)**
- Adım: önce `v0.x.0-rc1` etiketi test tap/bucket'a gider. CI matrisinde (mac/win/linux) üç paket yöneticisiyle kurulur; `tool --version` etiketle eşleşmeli. rc1'den rc2'ye kendini güncelleme uçtan uca denenir.
- Dışa dönük adımlar Ömer onayından sonra koşar: gerçek etiket, tap push, winget-pkgs PR. Sürüm başına en çok 1 winget PR ve en çok 1 imza servisi oturumu.
- Kapı: Kapanış (6): test · semgrep · gitleaks · a11y (yalnız `NO_COLOR` ve okunur `--help`; görsel arayüz yok) · kanıt · rapor (commit · test · CI · sapma)
- Bitişte: `graphify update .` koşar, dalga.md silinir.
### Y
**Varsayım:** Depo GitHub'da, CI GitHub Actions. Apple Developer ID ve Windows Authenticode sertifikası alınmış ya da alınacak.
**Faz 0 · Keşif ve lisans (≈8k jeton)**
- Adım: mevcut `main.go`, sürüm değişkeni (`-ldflags -X`) ve komut yapısı okunur. Araç: `dil-cli-araci` ve `dil-go` ajanları (salt okuma).
- Adım: GoReleaser (MIT), cosign (Apache-2.0), `creativeprojects/go-selfupdate` (MIT) ve `minio/selfupdate` (Apache-2.0) için güncel doküman ve lisans kontrolü. Araç: `context7` MCP, `ara-lisans-kontrol` ve `ara-kutuphane-secimi`.
- Kapı: üç bileşenin lisansı MIT ya da Apache değilse DUR raporu.
**Faz 1 · Çapraz derleme (≈12k)**
- Adım: `.goreleaser.yaml` yazılır. Hedefler darwin/linux/windows × amd64/arm64, `CGO_ENABLED=0`, `-trimpath`, yeniden üretilebilir derleme için `mod_timestamp`. Araç: GoReleaser CLI (`goreleaser check`, `goreleaser release --snapshot --clean`).
- Kapı: `go test -race ./...`, `govulncheck ./...`, gosec. gosec `sec-sast-kosucu` ajanıyla koşar, ikililerin `--version` çıktısı da doğrulanır.
- İnceleyen: `Developer Tooling Engineer`.
**Faz 2 · İmza (≈12k)**
- Adım: `checksums.txt` cosign keyless (GitHub OIDC) ile imzalanır ve SBOM (syft) eklenir. macOS ikilisi GoReleaser `notarize` ile, Windows .exe signtool/Azure Trusted Signing ile Authenticode imzalanır.
- Kapı: CI'da `cosign verify-blob`, `codesign -dv`, `signtool verify /pa`. Sırlar yalnız Actions secrets'ta tutulur, kontrol `sec-sir-tarayici` ve `sec-gitleaks-gecmis` ile yapılır.
- İnceleyen: `sec-sifreleme-denetci`.
- Tartışma: sertifika maliyeti ve sağlayıcı seçimi (bir yıllık OV/EV sertifikası mı, Trusted Signing mi). Bütçe tavanı rakam olarak yazılır ve satın alma öncesi Ömer'e sorulur.
**Faz 3 · Paket yöneticileri (≈15k)**
- Adım: GoReleaser `brews` ayrı bir `homebrew-tap` reposuna, `scoops` bir `scoop-bucket` reposuna, `winget` bölümü manifesti `winget-pkgs` fork'una gönderir. `ops-winget-kurulum` ajanı manifesti inceler.
- Kapı: matris smoke testi. macOS'ta `brew install --build-from-source` + `brew test`, Windows'ta `scoop install` ve `winget validate` + `winget install --manifest`. Kontroller `git-ci-boru-hatti` ile kurulur.
- Tartışma: microsoft/winget-pkgs'e PR açmak dışa dönük bir adım. İlk PR elle onaylanır, sonrakiler otomatiğe bağlanır.
**Faz 4 · Sürüm notu (≈6k)**
- Adım: Conventional Commits ile GoReleaser `changelog.use: github` ve gruplar (feat/fix/perf). Sürüm etiketi release-please ile ya da elle verilir. Araç: `dok-degisiklik-gunlugu` ajanı, `document-release` skill'i (kuruluysa).
- Kapı: commit-lint CI adımı.
**Faz 5 · Kendini güncelleme (≈15k)**
- Adım: `tool update` alt komutu `go-selfupdate` ile GitHub Releases'tan yeni sürümü indirir. Yazmadan önce sağlama toplamını ve cosign imzasını doğrular, ikiliyi atomik değiştirir, Windows'ta `.old` adıyla yeniden adlandırır.
- Adım: brew, scoop ya da winget ile kurulmuşsa (yol algılanır) güncelleme yapılmaz, ilgili paket yöneticisinin komutu önerilir.
- Kapı: sahte release sunucusuyla (httptest) tablo testleri: bozuk imza, yarım indirme, aynı sürüm, düşük sürüm.
- İnceleyen: `agent-skills:security-auditor`.
- Tartışma: varsayılan davranış ne olsun: otomatik güncelleme mi, yalnız uyarı mı? Öneri: yalnız uyarı, güncellemeyi kullanıcı açık komutla başlatır.
**Faz 6 · Yayın provası (≈8k)**
- Adım: `v0.0.1-rc1` ön sürümüyle uçtan uca prova. Araç: `git-yayin-oncesi-kontrol` ve `sec-cikis-oncesi-guvenlik` ajanları.
- Kapı: üç kanaldan kurulum ve `tool update` gerçek makinede yeşil olmalı. Geri alma planı: release silinir, tap/bucket commit'i revert edilir.
### Z
**Ön koşul:** Eşleşen `departman-*` müdür skill'i açılır, bulunamazsa raporda tek satır gerekçe yazılır. Hedef depo okunur (`go.mod`, `main`, mevcut CI). Lisans kapısı: GoReleaser (MIT), go-selfupdate (MIT), cosign (Apache) proje bağımlılığıdır, bu ortama kurulmaz.

**F1 Tasarım (8k)**
- Hedefler belirlenir: `{linux,darwin,windows}×{amd64,arm64}`, CGO=0, `-trimpath`, ldflags ile `version/commit/date` gömülür. Araç: Agent `dil-cli-araci` (`version` ve `self-update` alt komutları, çıkış kodları).
- Dağıtım akışı: Bir etiket push'u şu zinciri başlatır: CI → GoReleaser → GitHub Release → Homebrew tap formülü, Scoop bucket manifesti, winget-pkgs PR'ı. Araç: Agent `Developer Tooling Engineer`.
- **Tartışma 1 (geri dönüşsüz, maliyetli): Windows imzası.** Seçenekler Azure Trusted Signing ya da OV/EV sertifika. Veri yoksa `ecc:council` bir kez çalışır (~60-90k). macOS için notarization: Apple Developer hesabı var mı, sorulur.
- **Tartışma 2: Kendini güncelleme ile paket yöneticisi çakışıyor.** Öneri: brew, scoop veya winget ile kurulduysa self-update kapalı kalır ve "`brew upgrade` kullan" mesajı verilir. Kurulum yolu çalıştırılabilir dosyanın yolundan anlaşılır.
- **Kapı:** Kabul ölçütleri `.claude/dalga.md` dosyasına yazılır (≤30 satır).

**F2 Uygulama (35k)**
- `.goreleaser.yaml` yazılır: builds, archives (Windows için zip), checksums, `signs` (cosign keyless ile `checksums.txt` imzası), `brews`, `scoops`, `winget` blokları. Araç: Agent `git-ci-boru-hatti`.
- Windows `.exe` imzası: GoReleaser `signs` içinde signtool ya da Trusted Signing hook'u kullanılır. Sırlar CI secret olarak tutulur, değerleri hiçbir çıktıda basılmaz.
- Otomatik sürüm notu: Conventional Commits ve GoReleaser `changelog` (gruplar: feat, fix, perf) kullanılır. Biçim incelemesi Agent `dok-degisiklik-gunlugu` ile yapılır.
- Self-update `go-selfupdate` ile yazılır: GitHub Release'ten okur, `checksums.txt` ile cosign imzası doğrulanmadan dosyayı değiştirmez. Windows'ta çalışan exe rename ile değiştirilir. Araç: Agent `dil-go`.
- Derleme hataları Agent `ecc:go-build-resolver` ile çözülür.

**F3 Test ve güvenlik (12k)**
- Testler: Önce kırmızısı görülen testler yazılır.
  - Sürüm karşılaştırma tablosu.
  - İmza bozuksa güncelleme reddedilir.
  - Paket yöneticisi kurulumunda self-update kapanır.
  - Yarıda kesilen indirmede eski ikili sağlam kalır.
  - Testler `go test -race ./...` ile koşar.
- Kuru koşu: `goreleaser release --snapshot --clean`, ardından `goreleaser check`. Kapı: 6 hedefin hepsi derlenmiş, checksum'lar eşleşiyor.
- **Kapılar:**
  - semgrep: 0 yüksek bulgu (Agent `sec-sast-kosucu`, gosec dahil).
  - gitleaks: 0 bulgu (Agent `sec-gitleaks-gecmis`).
  - `govulncheck`: 0 bulgu (Agent `sec-bagimlilik-acik`).
- İnceleme: Agent `ecc:go-reviewer`, ardından Agent `ecc:security-reviewer` (indirme, imza doğrulama, yol geçişi).

**F4 Yayın ve kapanış (3k + yayın)**
- `v0.x.0-rc.1` etiketiyle prerelease çıkılır. Tap ve bucket'a test dalı kullanılır, winget PR açılmaz.
- Kontrol: Windows'ta `scoop install`, Windows'ta winget kuru doğrulaması (`winget validate`, Agent `ops-winget-kurulum`), macOS'ta `brew install` (CI runner üzerinde).
- Gerçek yayın dışarıya açık bir işlemdir. **Sınır en çok 1 kararlı etiket ve en çok 1 winget-pkgs PR'ı; Ömer onayı alınmadan yapılmaz.** Öncesinde Agent `git-yayin-oncesi-kontrol` çalışır.
- **Kapanış:** test, semgrep, gitleaks, kanıt (release URL, imza doğrulama çıktısı), rapor (commit, test sayısı, CI, sapma). Her faz sonunda Agent `ecc:code-reviewer` çalışır.

## 5. PyTorch görüntü sınıflandırma modelini üretime al: ONNX dışa aktarma, FastAPI çıkarım servisi, GPU toplu işleme, kayma izleme ve A/B karşılaştırma.
### X
**Varsayım:** Model sınıflandırıcıdır (CNN veya ViT). Sunucuda tek NVIDIA GPU ve Docker var, servis FastAPI. Görüntüler kişisel veri (yüz, plaka) içerebilir, bu yüzden KVKK kapsamındadır.
**Başlangıç:** `.claude/dalga.md` yazılır. Test, yük ve log okuma işi sonnet alt ajanına verilir.

**F1 Tasarım (6k)**
- Adım: SLO'yu ölçülebilir yaz: p95 gecikme ≤ X ms, tek GPU'da ≥ Y img/s, doğruluk tabanı = mevcut test seti top-1.
- Araç: Agent ml-goruntu-isleme (ön işleme sözleşmesi: boyut, normalizasyon, renk sırası) · Agent ml-model-metrik (A/B metriği ve eşik)
- KVKK: Skill use-case-triage sonra Skill pia-generation. Ham görüntü saklanmaz; kayma için yalnız embedding özeti ve tahmin dağılımı tutulur, saklama süresi 30 gün. Agent sec-kvkk-gdpr-kontrol veri akışını onaylar.
- Tartışma: ONNX Runtime CUDA EP mi, TensorRT EP mi? Başlangıç ORT CUDA. TensorRT ancak F3 ölçümü SLO'yu kaçırırsa denenir. Ayrı model sunucusu yerine süreç içi dinamik toplama kullanılır. Karar geri alınabilir, konsey yok.

**F2 Uygulama (25k)**
- ONNX: `torch.onnx.export` (dynamic batch ekseni, opset sabit). Ardından `onnx.checker` ve onnxsim eşdeğeri kontrol koşar. Araç: Skill ecc:pytorch-patterns · Agent ecc:pytorch-build-resolver (dışa aktarma veya CUDA hatası çıkarsa).
- Servis: FastAPI `/predict` ve `/healthz`. Pydantic ile dosya boyutu ve MIME sınırı uygulanır. Araç: Skill fastapi-python + Skill ecc:fastapi-patterns.
- GPU toplama: asyncio kuyruğu, en çok 32 istek ya da en çok 5 ms bekleme. Tek `InferenceSession` paylaşılır, IO binding kullanılır. Kuyruk dolunca 503 döner (geri basınç).
- Kayma: her istekte tahmin dağılımı ve embedding özeti Prometheus'a yazılır. Saatlik iş PSI ve KS hesaplar; PSI > 0.2 alarm verir. Araç: Agent ml-tahmin-kaymasi-izleme · Agent ops-prometheus · Agent ops-grafana-pano.
- A/B: kullanıcı kimliği hash'iyle yapışkan yönlendirme. Önce gölge mod (B yalnız loglanır), sonra %10 trafik. Araç: Agent git-canary-izleme (abort eşikleri) · Agent ml-deney-izleme (model sürümü ve lineage).
- İnceleme: Agent ecc:fastapi-reviewer + ecc:code-reviewer

**F3 Kuru koşu + test + güvenlik (10k)**
- Parite: aynı 1000 görüntüde PyTorch ile ONNX arasında max abs fark ≤ 1e-4 ve top-1 uyumu ≥ %99.9.
- Test: pytest yeşil. Toplayıcı sırası ve zaman aşımı, 503 yolu, bozuk ve fazla büyük dosya test edilir. Araç: Agent qa-api-test.
- Yük: Agent qa-yuk-testi (k6) ile SLO p95 ve verim eşiği doğrulanır, VRAM tepe ≤ %90 kalmalı.
- A/B istatistiği: Agent urn-ab-test-istatistik örneklem boyutunu ve MDE'yi önceden yazar, SRM kontrolü yapar, ara bakışla (peeking) karar yasaktır.
- Güvenlik: semgrep 0 yüksek · gitleaks 0 · Agent sec-docker-guvenlik (root olmayan kullanıcı, ince imaj) · Agent ecc:security-reviewer (yükleme sınırı, görüntü ayrıştırma DoS'u)

**F4 Yayın + kapanış (3k)**
- Adım: önce gölge, sonra %10, sonra %50, sonra %100. Her basamakta git-canary-izleme eşikleri uygulanır (hata oranı, p95, PSI). Eşik aşılırsa A'ya otomatik dönülür.
- Üretime çıkış Ömer onayıyla yapılır.
- Kapı: Kapanış (6): test · semgrep · gitleaks · a11y (N/A, arayüz yok) · kanıt (parite ve yük çıktısı) · rapor (commit · test · CI · sapma)
- Bitişte: `graphify update .` koşar, dalga.md silinir.

plan_kur.py'yi iki iş için tek çağrıyla koşturdum ve araçları onun aday listesinden seçtim; başka hiçbir işi yapmadım ve hiçbir dosya yazmadım. Listede olmayan GoReleaser, cosign ve onnxruntime-gpu bu ortamda kurulu değil. Bunları yerel araç olarak değil, projenin kendi bağımlılığı olarak yazdım; ölçüm sayacı "kurulmamış ad" diye sayabilir.
### Y
**Ön koşul:** Eşleşen `departman-*` skill'i açılır. Model, eğitim betiği ve doğrulama seti okunur. Lisans kapısı: onnxruntime-gpu (MIT), FastAPI (MIT).

**F1 Tasarım (6k)**
- Servis sözleşmesi belirlenir: `POST /predict` (çoklu görsel, boyut/MIME sınırı), `/healthz`, `/metrics`. Araç: Skill `ecc:fastapi-patterns` ve Agent `ml-goruntu-isleme` (ön işleme eşitliği: resize, normalize, kanal sırası).
- **KVKK:** Görsellerde yüz veya kişisel veri varsa Skill `use-case-triage` çalışır. Gerekirse Skill `pia-generation` kullanılır. Görsel saklanmaz, yalnız istatistik loglanır.
- **Tartışma 1: A/B yöntemi.** Seçenekler shadow (risksiz, yalnız ajansal metrik) ile istek-id hash'iyle yüzde 90/10 bölme (etiketli sonuç gerekir). Öneri önce shadow, sonra bölme. İstatistik planı Agent `urn-ab-test-istatistik` hazırlar: örneklem büyüklüğü, MDE, erken bakma kontrolü.
- **Tartışma 2: Kayma referansı.** Doğrulama seti mi, ilk hafta trafiği mi? Konsey gerekmez, bu karar geri alınabilir.

**F2 Uygulama (25k)**
- ONNX dışa aktarım: `torch.onnx.export` (dynamic batch ekseni, opset sabit), ardından `onnx.checker`. Araç: Skill `ecc:pytorch-patterns`. CUDA/export hataları Agent `ecc:pytorch-build-resolver` ile çözülür.
- Servis: Skill `fastapi-python`. GPU toplu işleme için bir asyncio kuyruğu kurulur: `max_batch=32` ve `max_wait=5ms` yapılandırılabilir, oturum başlangıçta bir kez açılır, onnxruntime çağrısı event loop'u bloklamaz. Event loop denetimi Agent `dil-asyncio` yapar.
- Kayma izleme: Agent `ml-tahmin-kaymasi-izleme` ile tasarlanır. Girdi parlaklık/boyut dağılımı ve tahmin dağılımı için PSI, embedding için KS kullanılır. Hesap numpy/scipy ile yapılır, yeni bağımlılık eklenmez. Prometheus gauge ve alarm kuralları Agent `ops-prometheus` ile yazılır.
- A/B yönlendirme: `model_version` etiketi her yanıt ve metrikte bulunur. Deney kaydı Agent `ml-deney-izleme` ile tutulur.

**F3 Kuru koşu ve test (10k)**
- **Eşitlik kapısı:** Doğrulama setinde PyTorch ile ONNX arasında top-1 uyumu ≥%99,5 ve max|Δlogit| ≤1e-3.
- Testler (pytest): Önce kırmızısı görülen testler yazılır.
  - Toplu sonuç tekil sonuca eşittir.
  - Boş, bozuk, büyük görsel 4xx döner.
  - Hash bölmesi deterministiktir.
  - Sentetik kaymada PSI eşiği tetiklenir.
- Yük testi Agent `qa-yuk-testi` (k6) ile yapılır. **Kapılar:** p95 ≤ hedef ms, hata <%0,1, GPU belleği sınırda. Test süresi en çok 10 dakika.
- **Güvenlik kapıları:**
  - semgrep: 0 yüksek bulgu (Agent `sec-sast-kosucu`).
  - gitleaks: 0 bulgu.
  - pip-audit: 0 yüksek bulgu (Agent `sec-bagimlilik-acik`).
  - Docker non-root (Agent `sec-docker-guvenlik`).
- İnceleme: Agent `ecc:fastapi-reviewer`, ardından Agent `ecc:security-reviewer`.

**F4 Yayın ve kapanış (3k)**
- Canary: önce shadow, sonra %10, sonra %50, sonra %100. Durdurma eşikleri Agent `git-canary-izleme` ile belirlenir. Pano Agent `ops-grafana-pano` ile kurulur.
- Üretime geçiş Ömer onayına bağlıdır. **Sınır en çok 1 canary adımı/gün.**
- **Kapanış:** test, semgrep, gitleaks, kanıt (eşitlik raporu, k6 özeti), rapor (commit, test sayısı, CI, sapma). Her faz sonunda Agent `ecc:code-reviewer` çalışır.

GoReleaser, go-selfupdate, cosign ve onnxruntime-gpu katalogda yok. Bunları bu ortama kurulacak araç olarak değil, hedef projenin bağımlılığı olarak yazdım. Hiçbir dosyaya dokunmadım. macOS notarization için Apple hesabının ve 5. işteki p95 hedefinin değeri bilinmiyor, F1'de sorulmalı.
### Z
**Varsayım:** Elde eğitilmiş bir `.pt` modeli ve etiketli doğrulama seti var. Hedef tek GPU'lu bir Linux düğümü.
**Faz 0 · Kapsam ve KVKK (≈8k)**
- Adım: girdi görüntülerinde kişisel veri (yüz, plaka) var mı belirlenir, saklama süresi kararlaştırılır. Araç: `use-case-triage`, `pia-generation` skill'leri ve `sec-kvkk-gdpr-kontrol` ajanı.
- Kapı: kişisel veri varsa VKED taslağı onaylanmadan Faz 4'teki görüntü kaydı açılmaz.
- Adım: onnxruntime-gpu, FastAPI ve Evidently (Apache-2.0) dokümanı ve lisansı kontrol edilir. Araç: `context7`, `ara-lisans-kontrol`. alibi-detect BSL lisanslı olduğu için seçilmez.
**Faz 1 · ONNX dışa aktarma (≈12k)**
- Adım: `torch.onnx.export` (dynamo=True), dinamik batch ekseni, opset sabitlenir. Ardından `onnx.checker` ve onnxsim çalışır. Araç: `ecc:pytorch-patterns` skill'i. Hata çıkarsa `ecc:pytorch-build-resolver` ajanı.
- Kapı (parite): 1000 doğrulama görüntüsünde logit farkı ≤1e-3 ve top-1 eşleşmesi ≥%99.9. Ayrıca FP16 ile FP32 arasındaki doğruluk farkı ≤0.3 puan. Betik: `parite_testi.py` (pytest).
- İnceleyen: `ml-goruntu-isleme`. Ön işleme (resize, normalize) eğitimle bire bir aynı olmalı.
**Faz 2 · FastAPI servisi (≈15k)**
- Adım: `/predict` (multipart, boyut ve MIME sınırı), `/healthz`, `/metrics`. Pydantic şemaları, model sürümü yanıtta döner. Araç: `fastapi-python` ya da `ecc:fastapi-patterns` skill'i.
- Kapı: `qa-api-test` ile 4xx/5xx senaryoları. Güvenlik: kötü niyetli görüntü (decompression bomb), hız sınırı ve kimlik doğrulama, `sec-api-guvenlik` ve `sec-yol-gecisi` ajanlarıyla.
- İnceleyen: `ecc:fastapi-reviewer`.
**Faz 3 · GPU toplu işleme (≈15k)**
- Adım: asyncio kuyruğu ile dinamik mikro-batch (en çok 32 görüntü ya da 10 ms bekleme). ORT CUDA EP, IOBinding ve uygun yerde ThreadPool kullanılır.
- Tartışma: kendi batcher'ımız mı, Triton mu? Öneri: tek model ve tek GPU için kendi batcher'ımız. Triton ancak çoklu model ya da çoklu GPU gerekirse.
- Kapı: `qa-yuk-testi` ile k6. Hedefler p95 ≤ X ms ve ≥ Y img/s (sayılar Ömer'den alınır), GPU bellek tepesi kaydedilir, OOM'da 503 dönülür. Regresyon için `qa-benchmark-regresyon-kapisi`.
**Faz 4 · Kayma izleme (≈12k)**
- Adım: Prometheus'a gecikme, batch boyu, güven dağılımı ve sınıf oranları yazılır. Günlük Evidently işi, embedding ya da piksel istatistiği kaymasını (PSI/MMD) referans setiyle karşılaştırır. Araç: `ml-tahmin-kaymasi-izleme`, `ops-prometheus` ve `ops-grafana-pano` ajanları.
- Kapı: uyarı eşikleri sentetik kaymış veriyle doğrulanır, kaymasız veride yanlış alarm olmamalı. Loglarda kişisel veri olmadığı `sec-loglama-gizlilik` ile kontrol edilir.
- Tartışma: etiket gecikmesi nedeniyle gerçek doğruluk geç gelir. Ara vekil olarak güven ve kayma metrikleri kullanılır.
**Faz 5 · A/B karşılaştırma (≈12k)**
- Adım: kullanıcı ID'sinin hash'iyle bölünmüş trafik (önce gölge mod, sonra %10 canary). Model sürümü her yanıtta ve metrikte etiketlenir. Araç: `urn-ab-test-istatistik` (örneklem büyüklüğü, MDE, SRM kontrolü), `git-canary-izleme` (iptal eşikleri), `ml-deney-izleme` (sürüm soy kaydı).
- Kapı: SRM p>0.01, ön kayıtlı birincil metrik ve gecikme bozulmaması. Ara bakış (peeking) yasak.
- Tartışma: birincil metrik ne: iş metriği mi, etiketli doğruluk mu? Karar ADR'ye yazılır (`dok-adr-yazar`).
**Faz 6 · Üretim hazırlığı (≈8k)**
- Adım: Docker imajı (CUDA runtime tabanı, root olmayan kullanıcı), `sec-docker-guvenlik` ile denetlenir. Ardından `inc-uretim-hazirligi` gözden geçirmesi ve `dok-runbook` ile geri alma runbook'u (eski modele dönüş tek değişken).
- Kapı: uçtan uca doğrulama gerçek GPU'da yapılır.

Yazmadığım kısımlar: katalog 27 ve 25 aracın kurulu olmadığını söyledi ama hangileri olduğunu göstermedi. Planda katalogdan gelip benim ajan listemde olmayan skill'ler (`document-release`, `fastapi-python`, `ecc:pytorch-patterns`, `use-case-triage` vb.) hiç denetlenmedi, iş başlamadan kurulu oldukları doğrulanmalı. GoReleaser, cosign, Evidently ve k6 katalogda yok, yeni bağımlılık sayılır. Riskler: imza sertifikalarının maliyeti ve winget-pkgs'e PR açmak dışa dönük adımlar, Ömer'in onayını bekler.

## 6. Shopify mağazası için özel tema ve uygulama geliştir: ürün yapılandırıcı, Liquid bölümleri, ödeme sonrası yukarı satış, Core Web Vitals bütçesi ve erişilebilirlik denetimi.
### X
**Varsayım:** Shopify CLI (`shopify theme dev/check`, `shopify app dev`) projede kurulu; değilse iş durur ve DUR raporu yazılır. Yığın: Online Store 2.0 teması + Remix tabanlı uygulama.

**Faz 0 · Hazırlık**
- Adım: UI işi olduğu için önce Skill `frontend-craft` yüklenir. Kabul ölçütleri ve dalga.md hazırlanır.
- Araç: Skill `frontend-craft` · Agent `pln-kabul-olcutleri`
- Kapı: Her özellik için given/when/then ölçütü yazılmış olmalı.
- Bütçe: 4k

**Faz 1 · Tasarım**
- Adımlar:
  - Bölüm ve blok şeması: ürün yapılandırıcı bölümü ve app block, metafield/metaobject modeli.
  - Yukarı satış akışı ve performans bütçe dosyası.
- Araç: Skill `frontend-craft` (yön, Bölüm 6) · Skill `web-design-guidelines` · Agent `ecc:a11y-architect` (WCAG 2.2 bileşen sözleşmesi)
- İnceleme: `ecc:code-reviewer`
- Tartışma 1, yapılandırıcı tekniği: Liquid + küçük vanilla JS adası mı, React app block mı? **Önerim:** vanilla ada, çünkü ilk yükte JS ≤170 KB gz kapısı var.
- Tartışma 2, yukarı satış yeri: post-purchase extension mı (onay ve plan koşulu var), Thank-you Checkout UI extension mı? Mağaza planı bilinmiyor; bu geri dönüşsüz ve veri yoksa `ecc:council` 1 kez (~60-90k) çağrılır.
- Bütçe: 8k

**Faz 2 · Uygulama**
- Adımlar:
  - Liquid bölümleri ve şema ayarları.
  - Yapılandırıcı: varyant ve seçenek durumu, sepete line item property ile ekleme.
  - Yukarı satış extension'ı ve uygulama arka ucu.
- Araç: Shopify CLI · Agent `Payments & Billing Engineer` (yukarı satış ve ödeme akışı) · Skill `fixing-accessibility`
- Kapılar:
  - Ödeme: kart verisi sunucuya hiç değmez (PCI SAQ-A). Changeset JWT imzası sunucuda doğrulanır.
  - Webhook: HMAC doğrulanır, olay kimliğiyle tekil işlenir. Yeniden deneme tavanı 3, üstel bekleme.
  - Her sipariş değişikliği isteğinde idempotency anahtarı olur.
  - KVKK/GDPR: zorunlu webhook'lar (`customers/data_request`, `customers/redact`, `shop/redact`) uygulanır. Agent `sec-kvkk-gdpr-kontrol` ile doğrulanır.
- İnceleme: `ecc:code-reviewer`
- Bütçe: 35k

**Faz 3 · Test ve güvenlik** (koşum alt ajanda: sonnet, yalnız özet döner)
- Adımlar:
  - `shopify theme check`: 0 hata.
  - Yapılandırıcı ve yukarı satış için e2e (playwright headless).
  - Core Web Vitals ölçümü ve a11y denetimi.
- Araç: Agent `qa-e2e-playwright` · Skill `web-perf` + Agent `agent-skills:web-performance-auditor` · Agent `qa-erisilebilirlik-testi` (otomatik denetim + klavye turu) · Agent `sec-sast-kosucu` (semgrep) · Agent `sec-gitleaks-gecmis`
- Kapılar:
  - LCP ≤2.5 s · CLS ≤0.1 · INP ≤200 ms · ilk yük JS ≤170 KB gz
  - a11y 0 ciddi ihlal · test yeşil · semgrep 0 yüksek · gitleaks 0
- İnceleme: `ecc:security-reviewer`. Kabul denetimini taze bağlamlı ayrı bir ajan yapar, yalnız diff ve ölçütleri görür.
- Bütçe: 12k

**Faz 4 · Yayın ve kapanış**
- Adımlar:
  - Önce yayımlanmamış tema ve geliştirme mağazasında önizleme yapılır, sonra yayına alınır.
  - Geri alma: önceki tema yeniden yayımlanır, ≤5 dk, adım yazılı.
- Kapı: `frontend-craft` Bölüm 6 tur raporu · kapanış raporu (commit · test · CI · sapma)
- Ücretli çağrı tavanı: en çok 3 canlı mağaza yayını. Ödeme testi yalnız test modunda yapılır.
- Bütçe: 3k
### Y
**Varsayım:** Online Store 2.0 teması, Shopify CLI uygulama şablonu ve geliştirme mağazası var. UI işi olduğu için önce `Skill frontend-craft` yüklenir, Bölüm 6 tur raporu olmadan iş kapanmaz.

**Faz 0 · Hazırlık (3k)**
- `Skill departman-*` (frontend/e-ticaret) açılır, araç sırası belirlenir.
- `.claude/dalga.md` yazılır: KARAR, kabul ölçütleri, mevcut durum.

**Faz 1 · Tasarım (10k)**
- `Skill frontend-craft` ile görsel yön ve bölüm envanteri çıkarılır: hero, ürün, yapılandırıcı, koleksiyon.
- `Agent urn-urun-yoneticisi`: yapılandırıcı seçenekleri ve yukarı satış teklif kuralları.
- `Agent Payments & Billing Engineer`: ödeme sonrası akış. Ödeme sonrası eklentisi mi, Teşekkür sayfası UI eklentisi mi, burada seçilir.
- **Tartışma 1:** Yapılandırıcı fiyatı istemcide hesaplanırsa güvenilmez. Seçenekler: her kombinasyon ayrı varyant ya da Cart Transform Function. Fiyat sunucuda doğrulanmalı.
- **Tartışma 2:** Yapılandırıcı tema bölümü mü olacak, tema uygulama eklentisi bloğu mu? Blok, temayı değiştirince de taşınır.
- **Konsey:** Gerek yok, iki karar da geri alınabilir.
- Kapı: kabul ölçütleri `Agent pln-kabul-olcutleri` ile given/when/then biçiminde yazılır.

**Faz 2 · Uygulama (45k)**
- Liquid bölümleri JSON şablonlarla yazılır, ayarlar şemada tutulur. Araç: `shopify theme dev`. Kapı: `shopify theme check` 0 hata.
- Yapılandırıcı uygulama bloğu olarak yazılır. Seçimler metafield/metaobject'te tutulur, sepet satır özelliklerine aktarılır. JS bölüme göre gecikmeli yüklenir.
- Yukarı satış: değişiklik seti (changeset) jetonu uygulama sırrıyla doğrulanır, uygulamada idempotency anahtarı kullanılır. Webhook'larda HMAC imzası kontrol edilir ve olaylar kimliğe göre bir kez işlenir. Yeniden deneme en çok 3, üstel beklemeyle.
- Kart verisi Shopify'da kalır, sunucuya değmez (PCI kapsamı dışı).
- KVKK: zorunlu GDPR webhook'ları (`customers/data_request`, `customers/redact`, `shop/redact`) eklenir. İnceleme: `Agent sec-kvkk-gdpr-kontrol`.
- İnceleme: faz sonunda `Agent ecc:code-reviewer`.

**Faz 3 · Test, performans, güvenlik (15k)**
- E2E: `Agent qa-e2e-playwright`, headless. Yapılandır → sepete ekle → ödeme → yukarı satış akışı.
- Core Web Vitals: `Skill web-perf` ve `Agent agent-skills:web-performance-auditor`.
  - Bütçe: LCP ≤2.5 s, CLS ≤0.1, INP ≤200 ms, ilk yükte JS ≤170 KB gz.
  - Mobil profilde ölçülür; ana sayfa, ürün ve koleksiyon sayfalarında.
- Erişilebilirlik: `Agent qa-erisilebilirlik-testi` (axe + klavye turu) 0 ciddi ihlal. Yapılandırıcı denetimleri `Skill fixing-accessibility` ile düzeltilir. İnceleme: `Agent ecc:a11y-architect`.
- Güvenlik: semgrep 0 yüksek, gitleaks 0 bulgu. İnceleme: `Agent ecc:security-reviewer`.

**Faz 4 · Yayın ve kapanış (4k)**
- Tema `shopify theme push --unpublished` ile önizlemeye gönderilir. Uygulama sürümü `shopify app deploy` ile çıkar. Bu adım dışa dönük olduğu için önce Ömer onaylar.
- Geri alma ≤5 dk: önceki tema yayınlanır, önceki uygulama sürümü etkinleştirilir. Adımlar yazılı tutulur.
- Kabul denetimini işi yapmayan, taze bağlamlı ayrı bir alt ajan yapar; yalnız diff ve kabul ölçütlerini görür.
- Kapanış raporu: commit · test sayısı · CI · sapmalar, ayrıca frontend-craft Bölüm 6 raporu.
### Z
**F0 Kapsam ve karar (≈6k)**
- Adım: önce `Skill frontend-craft` yüklenir (UI kuralı). Ardından `Skill prd-yaz` ve `pln-kabul-olcutleri` ajanıyla kabul ölçütleri yazılır.
- CWV bütçesi p75 değerleriyle konur: LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1. Yapılandırıcının JS boyutu ≤40 KB gz olur.
- Erişilebilirlik hedefi WCAG 2.2 AA.
- Tartışma 1: yapılandırıcı nerede yaşayacak? Seçenekler theme app extension (app block) ile metaobject veya düz tema bölümü. Öneri app block, çünkü tema değişince taşınabilir kalır.
- Tartışma 2: ödeme sonrası eklenti erişimi ve mağaza planı (Plus gereği). `ara-kutuphane-dokuman` ile güncel Shopify dokümanından doğrulanır, varsayımla ilerlenmez.

**F1 Ortam (≈3k)**
- Shopify CLI, `shopify theme check` ve Lighthouse CI katalogda yok, kurulmaları gerekir.
- Dawn temasının lisansı `ara-lisans-kontrol` ile okunur.
- Geliştirme mağazası ve yayınlanmamış önizleme teması kullanılır. Canlı tema değişmez.

**F2 Liquid bölümleri (≈15k)**
- Adım: section ve block şemaları ile JSON şablonları yazılır. Çizim sırası `frontend-craft`, ardından `web-design-guidelines`.
- Kapı: `shopify theme check` 0 hata verir. `fe-responsive-kontrol` 3 genişlikte geçer.
- İnceleme: `UI Finish-Gate Reviewer`.

**F3 Ürün yapılandırıcı (≈20k)**
- Adım: varyant ve metaobject modeli kurulur. Seçimler line item properties ile taşınır. Yapılandırıcı tek bir JS adacığıdır.
- Tartışma: istemcinin hesapladığı fiyata güvenilmez. Fiyat ya varyant/SKU eşlemesinden ya da Shopify Functions (cart transform) ile sunucuda belirlenir.
- Kapı: `qa-e2e-playwright` headless akışı (seç → sepet → fiyat eşleşmesi). `qa-sinir-deger-analizi` ile seçenek sınırları denenir.
- İnceleme: `Code Reviewer`.

**F4 Uygulama ve ödeme sonrası yukarı satış (≈25k)**
- Adım: Remix şablonlu uygulama ve post-purchase extension yazılır. Webhook'lar `otm-webhook-tasarimci` desenine göre HMAC doğrulamalı ve idempotent olur.
- Kapı (güvenlik): `Skill VibeSec-Skill`, `sec-api-guvenlik` ve `gitleaks` (CLI) ile token/sır taraması.
- Kapı (KVKK): `sec-kvkk-gdpr-kontrol` çalışır. Zorunlu `customers/data_request`, `customers/redact` ve `shop/redact` webhook'ları test edilir.
- Kart verisine hiç dokunulmaz.
- İnceleme: `Application Security Engineer`.

**F5 CWV bütçesi (≈10k)**
- Araç: `Skill web-perf`, chrome-devtools MCP ile `chrome-devtools-mcp:debug-optimize-lcp`, Lighthouse CI headless (Opera açılmaz).
- Kapı: F0'daki bütçe CI'da kırmızı/yeşil kapı olur. Ana görsel `fe-gorsel-optimize` ile, kritik olmayan JS ise defer ile ele alınır.
- İnceleme: `agent-skills:web-performance-auditor`.

**F6 Erişilebilirlik denetimi (≈10k)**
- Araç: `qa-erisilebilirlik-testi` (axe ve klavye turu), `Skill fixing-accessibility`, `Skill interfaces:better-accessibility`, `inclusive-interaction:keyboard-review`.
- Yapılandırıcının odak sırası, aria-live fiyat duyurusu ve hata metinleri denetlenir.
- Kapı: axe'te kritik veya ciddi bulgu kalmaz, klavye turu %100 tamamlanır.
- İnceleme: `ecc:a11y-architect`.

**F7 Yayın (≈5k)**
- `git-yayin-oncesi-kontrol` çalışır. Önizleme Ömer'e gösterilir, onay gelirse tema yayınlanır. Eski tema geri dönüş için saklanır.
- frontend-craft Bölüm 6 tur raporu yazılır.
- Risk: post-purchase API erişimi alınamazsa F4 yukarı satışı sepete veya teşekkür sayfasına düşer. Bu karar yeniden Ömer'e sorulur.

## 7. Terraform ile AWS'de üç ortamlı altyapı kur: VPC, EKS kümesi, RDS çoklu AZ, gizli anahtar yönetimi, maliyet etiketleri ve felaket kurtarma tatbikatı.
### X
**F0 Karar (≈8k)**
- Araç: `ops-felaket-kurtarma` ile RTO/RPO belirlenir (öneri prod RTO ≤1 sa, RPO ≤5 dk). `octo:personas:cloud-architect` ve `pln-risk-kaydi` kullanılır.
- Tartışma 1: ortamlar ayrı AWS hesaplarında mı (Organizations), yoksa workspace ile mi ayrılacak? Öneri ayrı hesap ve ortam başına dizin, prod ayrı state ile yalıtılır.
- Tartışma 2: Terraform BUSL lisanslı, alternatifi OpenTofu (MPL). Koşullar rapora yazılır.
- Maliyet tavanı sayıyla konur, örneğin dev ≤$150/ay, stage ≤$300/ay, prod Ömer'le belirlenir. `apply` her zaman onay ister.

**F1 Bootstrap (≈6k)**
- Adım: S3 state (sürümlü, KMS ile şifreli) ve kilit (`use_lockfile` ya da DynamoDB) kurulur. GitHub Actions'tan AWS'ye OIDC rolü açılır, statik anahtar kullanılmaz.
- Araç: `ops-terraform` ajanı ve `terraform-skill` eklentisi. Eklenti kurulu değilse `/plugin` ile kurulur, öncesinde lisansı okunur.
- terraform, tflint, checkov, infracost ve aws CLI katalogda yok, kurulup lisansları kontrol edilir.

**F2 VPC ve EKS (≈20k)**
- VPC: terraform-aws-modules/vpc (Apache-2.0), 3 AZ, özel ve açık alt ağlar. NAT prod'da her AZ'de bir tane, dev'de tek.
- EKS: terraform-aws-modules/eks, yönetilen node grupları, Pod Identity/IRSA, özel API uç noktası. Workload ayarları `ops-k8s-is-yuku`.
- Kapı: `terraform validate`, tflint ve checkov'da yüksek seviye bulgu kalmaz. `terraform plan` diff'i insan tarafından okunur.
- İnceleme: `Cloud Security Architect`.

**F3 RDS çoklu AZ (≈10k)**
- Prod'da Multi-AZ, dev'de tek AZ. KMS şifreleme, PITR ve silme koruması açık. Ana parola `manage_master_user_password` ile yönetilir.
- İnceleme: `Database Reliability Engineer` ve `db-yedekleme-geri-yukleme`.

**F4 Gizli anahtar yönetimi (≈8k)**
- Secrets Manager ve KMS kullanılır. Sırlar EKS'ye External Secrets Operator ile taşınır. State'e sır yazılmaz, sensitive çıktılar denetlenir.
- Kapı: `gitleaks` ve `sec-sir-tarayici` ile sırlar yalnızca konumlarıyla raporlanır, değer basılmaz. Ek olarak checkov sır kuralları çalışır.
- İnceleme: `Secrets & Credential Hygiene Engineer`.

**F5 Maliyet etiketleri (≈6k)**
- Provider'da `default_tags` tanımlanır: Environment, Project, Owner, CostCenter. Cost allocation tag etkinleştirilir.
- AWS Budgets, F0 tavanının %80'inde alarm verir. PR'larda infracost diff'i görünür.
- Kapı: etiketsiz kaynak checkov veya özel kural ile kırmızı olur.
- İnceleme: `FinOps Engineer`.

**F6 CI (≈6k)**
- Araç: `git-ci-boru-hatti` ve `sec-ci-guvenlik-tarama`.
- PR'da fmt, validate, tflint, checkov ve plan çalışır. Prod `apply` manuel onaylı environment ile yapılır.
- İnceleme: `Code Reviewer`.

**F7 Felaket kurtarma tatbikatı (≈10k)**
- Adım: RDS yedeği AWS Backup ile ikinci bölgeye kopyalanır (cross-region copy). EKS durumu git'ten yeniden kurulur.
- Tatbikat stage'de yapılır: bölge kaybı varsayılır, restore edilir, RTO/RPO kronometreyle ölçülür. `dok-runbook` ile runbook yazılır. Oyun günü koordinasyonu `Incident Response Commander`'da.
- Kapı: ölçülen RTO/RPO hedefin altında kalır. Ardından kurtarma kaynakları yıkılır ve maliyet tavanı kontrol edilir.
- Tartışma: tam pilot-light DR mı, yalnızca yedekten restore mu? Karar prod maliyeti ile RTO arasındaki dengeye göre Ömer'le verilir.

Doğrulamadıklarım: Shopify post-purchase erişim koşulları ve Dawn lisansı, terraform-skill eklentisinin kurulu olup olmadığı. Katalog çıktısında Shopify'a özel bir araç yoktu.

Risk: 7. işte her `apply` ve DR tatbikatı gerçek AWS faturası doğurur. Maliyet tavanı konmadan başlanmamalı.
### Y
**Varsayım:** `terraform` ve `aws` CLI kurulu, kimlik bilgileri hazır; değilse DUR. Ortamlar dev, stg ve prod; bölge eu-central-1 (KVKK yurt dışı aktarım notu raporda yer alır).

**Faz 1 · Tasarım**
- Adımlar:
  - Hesap ve ortam yapısı.
  - CIDR planı: ortam başına /16, 3 AZ, public/private/db alt ağları.
  - State yapısı: ortam başına ayrı S3 state, `use_lockfile`.
  - Modül sınırları: vpc, eks, rds, secrets, tags.
- Araç: Agent `octo:personas:cloud-architect` · Agent `ops-terraform` · Agent `ops-felaket-kurtarma` (hedef RTO ≤1 sa, RPO ≤15 dk; varsayım)
- Tartışma: ortamlar ayrı AWS hesaplarında mı, tek hesap + workspace mı, dizin-başı-ortam mı? CIDR ve hesap yapısı sonradan değişmesi zor, geri dönüşsüz bir karar. **Önerim:** ayrı hesap + dizin-başı-ortam. Veri yoksa `ecc:council` 1 kez (~60-90k).
- İnceleme: `ecc:code-reviewer`
- Bütçe: 8k

**Faz 2 · Uygulama**
- Adımlar:
  - VPC modülü, EKS (yönetilen node grubu, Pod Identity).
  - RDS çoklu AZ: KMS ile şifreli, `manage_master_user_password`.
  - Secrets Manager + External Secrets.
  - Provider `default_tags`: env, owner, cost-center, app.
- Araç: Agent `ops-terraform` · Agent `ops-k8s-is-yuku` · Agent `Database Reliability Engineer` · Agent `Secrets & Credential Hygiene Engineer`
- Kapılar: `terraform fmt -check` / `validate` temiz. Plan çıktısında etiketsiz kaynak 0 (plan JSON betikle süzülür). State'te düz metin sır 0.
- İnceleme: `ecc:code-reviewer`
- Bütçe: 35k

**Faz 3 · Test ve güvenlik** (koşum alt ajanda: sonnet, yalnız özet döner)
- Adımlar: önce dev'e apply. Ardından public RDS/S3 yokluğu, IMDSv2, şifreleme ve en az yetki kontrolü.
- Araç: Agent `sec-sast-kosucu` (semgrep terraform kuralları) · Agent `sec-gitleaks-gecmis` · Agent `Cloud Security Architect`
- Kapılar: test yeşil · semgrep 0 yüksek · gitleaks 0 · 0.0.0.0/0 ingress yalnız ALB'de.
- İnceleme: `ecc:security-reviewer` · maliyet için Agent `FinOps Engineer` (etiket kapsamı %100, AWS Budgets alarmı)
- Bütçe: 12k

**Faz 4 · Felaket kurtarma tatbikatı ve yayın**
- Adımlar:
  - Tatbikatı stg'de yap: RDS `--force-failover`, bölgeler arası snapshot'tan geri yükleme, EKS iş yükünü yeniden kurma.
  - RTO/RPO'yu ölç.
  - Ortamlara sırayla geç: dev → stg → prod. Her `apply` öncesinde plan incelemesi ve insan onayı alınır.
- Araç: Agent `ops-felaket-kurtarma` · Agent `dok-runbook` (tatbikat ve geri alma runbook'u)
- Kapılar:
  - Ölçülen RTO ≤1 sa, RPO ≤15 dk.
  - Geri alma adımı yazılı.
  - Kapanış raporu: commit · test · CI · sapma.
- Ücretli çağrı tavanı: ortam başına en çok 3 `apply`, en çok 1 tatbikat. Aylık bütçe alarmları: dev ≤$300, stg ≤$600 (varsayım; prod tavanı onayla belirlenir).
- Bütçe: 3k + tatbikat 5k

---
- Her iki iş de zor sayıldı; `plan_kur.py` tek seferde çağrıldı.
- İş 6'nın jeton satırı ve iş 7'nin başlığı çıktıda sıkıştırılmış geldi. Ek sorgu yapmadım; iş 6'nın bütçelerini iş 7'ninkine göre tahmin ettim.
- Aday listesinde Shopify'a özel araç, terraform/aws CLI ya da başka bir IaC tarayıcısı yoktu. Bu yüzden bunlar "kurulu" varsayımıyla ve DUR koşuluyla yazıldı.
- Önerilen `vrm-maliyet-denetci` jeton maliyetine bakıyor, AWS maliyetine değil. Yerine `FinOps Engineer` konuldu.
### Z
**Varsayım:** Ortamlar dev, stg ve prod. Ayrı AWS hesapları (Organizations) ve ortam başına dizin kullanılır, Terraform workspace kullanılmaz.

**Ücretli kullanım tavanı (varsayılan, Ömer onaylayacak):** dev ≤150 $/ay, stg ≤300 $/ay. Ortam başına günde en çok 3 apply. DR tatbikatı en çok 1 kez, ≤4 saat.

**Faz 0 · Hazırlık (3k)**
- `Skill departman-*` (devops/altyapı) açılır.
- `dalga.md` yazılır: KARAR, kabul ölçütleri, tavanlar.

**Faz 1 · Tasarım (10k)**
- `Agent ops-terraform`: modüller (`modules/vpc`, `modules/eks`, `modules/rds`) ve ortam dizinleri (`envs/dev`, `envs/stg`, `envs/prod`).
  - State S3'te tutulur, kilit `use_lockfile` ile, şifreleme KMS ile.
  - Sürümler sabitlenir (pin).
- `Agent octo:personas:cloud-architect`: 3 AZ'li ağ, NAT sayısı (dev'de 1, prod'da AZ başına 1), EKS'e özel uç nokta.
- `Agent ops-felaket-kurtarma`: RTO/RPO hedefleri yazılır.
- `Agent FinOps Engineer`: etiket şeması. Sağlayıcıda `default_tags` ile env, owner, cost-center, app atanır.
- **Tartışma:** DR stratejisi pilot light mı, warm standby mı? `ops-felaket-kurtarma` ile `FinOps Engineer` maliyet ve RTO üzerinden karşılaştırır.
- **Konsey:** Veri yetmezse ve karar geri dönüşsüzse `ecc:council` en çok 1 kez çağrılır (~60-90k).

**Faz 2 · Uygulama (35k)**
- VPC: özel ve genel alt ağlar, akış günlükleri.
- EKS: yönetilen düğüm grupları, Pod Identity, `Agent ops-k8s-is-yuku` ile probe ve limitler.
- RDS çoklu AZ:
  - `deletion_protection` açık, yedek saklama ≥7 gün, KMS şifreleme.
  - Bölgeler arası snapshot kopyası.
  - Gözden geçirme: `Agent Database Reliability Engineer`.
- Gizli anahtarlar:
  - RDS'te `manage_master_user_password` kullanılır, böylece parola state'e düşmez.
  - Secrets Manager ve EKS'te External Secrets kullanılır.
  - İnceleme: `Agent Secrets & Credential Hygiene Engineer`.
- Kapılar: `terraform fmt -check` ve `terraform validate` temiz. Plan'da beklenmeyen silme 0. Yalnız dev'e apply edilir.
- İnceleme: faz sonunda `Agent ecc:code-reviewer`.

**Faz 3 · Test, güvenlik, maliyet (12k)**
- Modüllere `terraform test` yazılır. CI: `Agent git-ci-boru-hatti`; PR'da plan çalışır, apply onayla. GitHub→AWS bağlantısı OIDC ile yapılır, uzun ömürlü anahtar olmaz.
- Güvenlik: semgrep 0 yüksek, gitleaks 0 bulgu. IAM en az yetkiyle, SG'lerde 0.0.0.0/0 giriş yok. İnceleme: `Agent ecc:security-reviewer` ve `Agent Cloud Security Architect`.
- Maliyet: plan JSON'unda etiketlenebilir kaynakların %100'ü etiketli olmalı (`Agent otm-jq-donusum` betiği). Ortam başına AWS Budgets alarmı tavanda kurulur. İnceleme: `Agent ops-maliyet-optimize`.

**Faz 4 · DR tatbikatı ve yayın (8k)**
- Tatbikat stg'de yapılır: RDS PITR ve bölgeler arası snapshot geri yüklemesi, ardından EKS koddan yeniden kurulur.
- Kapı: ölçülen RTO/RPO, hedefin altında olmalı.
- `Agent dok-runbook`: geri yükleme runbook'u.
- Prod apply dışa dönük ve geri dönüşü zor olduğu için Ömer'in açık onayıyla yapılır. Geri alma: önceki commit'in planı uygulanır, RDS snapshot hazır tutulur.
- Kabul denetimini taze bağlamlı ayrı bir alt ajan yapar. Kapanış raporu: commit · test · CI · sapmalar.

---
Plan girdisi için iki işe tek `plan_kur.py` çağrısı yaptım. 6. işin çıktısındaki sıkıştırılmış kısmı açmadım, çünkü "ek sorgu yapma" denmişti. Bu yüzden 6. işin faz jeton bütçesi araçtan değil benim tahminim.

Shopify CLI, terraform, `terraform test` ve External Secrets aday listesinde yoktu. Bunları, işi yapan projenin kendi bağımlılıkları olarak yazdım. 7. işteki dolar tavanları da varsayım; Ömer'in onaylaması gerekiyor.

## 8. TypeScript projesinde ESLint uyarılarını düzelt ve kullanılmayan importları kaldır.
### X
**Faz 1 · Kapsam (≈3k jeton)**
- Adım: uyarıların başlangıç sayısını al. Araç: `npx eslint . --format json` ve `npx tsc --noEmit --noUnusedLocals`. Çıktıyı `jev log` ile özetle.
- Uyarıları kural bazında grupla: `no-unused-vars`, `no-explicit-any` ve diğerleri.

**Faz 2 · Düzeltme (≈8k jeton)**
- Önce `npx eslint . --fix` ile otomatik düzelen kuralları düzelt.
- Kullanılmayan importları elle sil. Yalnız tipte kullanılan importları `import type` yap.
- `any` ve daraltma uyarıları varsa `dil-ts-tip-daraltma` alt ajanını kullan.
- Yeni bağımlılık eklemiyorum: `eslint-plugin-unused-imports` kurulmayacak, iş tsc listesiyle yapılacak.
- **Tartışma:** Yalnız yan etki için yazılmış importlar (`import './polyfill'`, CSS) "kullanılmıyor" gibi görünür ama silinmez. Toplu `eslint-disable` de kullanılmaz. Gerçekten düzeltilemeyen her uyarı satır içi gerekçeyle bırakılır.

**Faz 3 · Kapı (≈3k jeton)**
- `npx eslint . --max-warnings 0`, `tsc --noEmit` ve mevcut test paketi çalıştırılır. Test koşusu sonnet alt ajanında yapılır, ana bağlama yalnız sayı döner.
- İnceleme: `inc-ponytail-kod`. Diff'in yalnız import ve uyarı satırlarına dokunduğunu doğrular.
### Y
**Faz 1: Durum tespiti** (~3k jeton)
- Adım: `npx eslint . --format json -o eslint.json` çalıştır, ardından `jev triage eslint.json` ile kural başına sayıyı çıkar. Araç: ESLint CLI, jev.
- Kapı: başlangıç sayısını kaydet (uyarı N, hata 0 olmalı) ve `tsc --noEmit` ile tabanın yeşil olduğunu doğrula.

**Faz 2: Otomatik düzeltme** (~4k)
- Adım: `npx eslint . --fix` çalıştır. Kullanılmayan importlar için proje `eslint-plugin-unused-imports` kullanıyorsa onun kuralı, kullanmıyorsa `@typescript-eslint/no-unused-vars` ve editörün "organize imports" komutu (`tsc` üzerinden) kullanılır. Yeni bağımlılık eklenmez.
- Kapı: önce `tsc --noEmit`, sonra `npm test`.

**Faz 3: Elle kalanlar** (~6k)
- Adım: `--fix` ile düzelmeyen uyarılar (`no-explicit-any`, `exhaustive-deps` gibi) tek tek ele alınır. Tip daraltma gerektirenlerde alt ajan `dil-ts-tip-daraltma` kullanılır.
- Tartışma noktası: `eslint-disable` yorumuyla susturmak mı, gerçekten düzeltmek mi? Varsayılan düzeltmek. Susturulan her satıra tek satırlık gerekçe yazılır ve rapora eklenir.
- Kapı: `eslint . --max-warnings 0`, `tsc --noEmit` ve `npm test` yeşil olmalı.

**Faz 4: İnceleme** (~3k)
- İnceleyen: `inc-ponytail-kod` diff'e bakar. Davranış değişikliği var mı ve yan etkili bir import (örneğin `import './polyfill'`) yanlışlıkla silindi mi, bunu kontrol eder.
- Kapanış raporu: uyarı sayısı N→0, test sayısı, commit.
### Z
**Ön koşul:** Lint çıktısını sonnet alt ajanı okur, ana bağlama yalnız kural başına sayı gelir. İçerik dar Read aralığıyla okunur.
**Faz 1 · Tespit (~3k jeton)**
- Adım: `npx eslint . -f json -o .claude/lint.json` çalıştırılır, ardından `jev triage .claude/lint.json` ile kural başına sayım çıkarılır. Araç: ESLint CLI, jev.
- Kapı: Değişiklikten önce `npx tsc --noEmit` yeşil olmalı. Kırmızıysa bu iş değil, ayrı bir iş olarak raporlanır.
**Faz 2 · Otomatik düzeltme (~4k)**
- Adım: `npx eslint . --fix` çalıştırılır. Kullanılmayan importları `@typescript-eslint/no-unused-vars` kuralı yakalar. Projede `eslint-plugin-unused-imports` zaten kuruluysa onun fix'i kullanılır. Yeni paket eklenmez.
- Tartışma noktası: Yan etkili importlar (`import './polyfill'`, CSS) ve `import type` dokunulmadan kalmalı. `git diff` bu importlar için ayrıca taranır.
**Faz 3 · Elle kalan uyarılar (~8k)**
- Adım: Kalanlar dosya dosya Edit ile düzeltilir. `any` ve daraltma uyarıları için dil-ts-tip-daraltma kalıpları kullanılır.
- Tartışma noktası: `// eslint-disable` yalnız gerekçe yorumuyla eklenir. Toplu disable eklenmez, kural kapatılmaz.
**Faz 4 · Kapı ve inceleme (~4k)**
- Kapı: `npx eslint . --max-warnings 0`, `npx tsc --noEmit` ve mevcut test komutu (`npm test`) yeşil olmalı.
- İnceleyen: inc-ponytail-kod diff'te davranış değişikliği ve gereksiz değişiklik arar.
- Bitiş: commit · test sayısı · CI durumu.

## 9. Dockerfile'daki Node temel imajını 18'den 20'ye yükselt ve derlemenin geçtiğini doğrula.
### X
**Faz 1 · Kapsam (≈3k jeton)**
- Node sürümünün geçtiği tüm yerleri bul: her `FROM node:18*` satırı (çok aşamalı derlemede birden fazla olabilir), `.nvmrc`, `package.json` içindeki `engines` ve CI'daki `setup-node`. Araç: Grep.
- **Tartışma (kritik):** Node 20'nin destek süresi 30 Nisan 2026'da bitti. Bugün yükseltmek, güvenlik yaması almayan bir sürüme geçmek demek. Başlamadan önce 20 mi yoksa 22/24 LTS mi olacağını sor. Karar 20 kalırsa bunu rapora sapma olarak yaz.

**Faz 2 · Değişiklik (≈3k jeton)**
- `node:18-<varyant>` etiketini `node:20-<aynı varyant>` yap (alpine/slim aynı kalsın). Mevcut digest sabitlemesi varsa yeni digest ile sabitle.
- CI'daki `setup-node` ve `engines` alanını aynı sürüme hizala.

**Faz 3 · Kapı (≈6k jeton)**
- `docker build --no-cache -t app:node20 .` çalıştır. Ardından `docker run --rm app:node20 node -v` ile sürümü doğrula.
- Testleri imajın içinde koş: `docker run --rm app:node20 npm test`.
- Riskli noktalar: native modüller (bcrypt, sharp vb.) yeniden derlenmeli. npm 10'un lockfile'ı değiştirip değiştirmediğini `git diff package-lock.json` ile kontrol et.
- Güvenlik: `sec-docker-guvenlik` incelemesi yapılır. `trivy`/`docker scout` kuruluysa CVE taraması da eklenir, değilse bu adımın atlandığı raporda yazılır.
- İnceleme: `ecc:code-reviewer`.
### Y
**Faz 1 · Envanter (~3k)**
- Adım: Grep ile `node:18`, `.nvmrc`, `engines` ve CI'daki `node-version` bulunur. Native modüller (`node-gyp`, `sharp`, `bcrypt`) lockfile'da işaretlenir. Araç: Grep.
- Tartışma noktası (kritik): Bugün 2026-10-14 ve Node 20'nin LTS desteği 2026-04-30'da bitti. Kullanıcıya bir satırla 22 LTS önerilir. Kullanıcı 20'de kalmak isterse 20 uygulanır.
**Faz 2 · Değişiklik (~2k)**
- Adım: `FROM node:18-<varyant>` satırı `node:20-<varyant>` yapılır. Varyant (alpine/slim) aynı kalır. Çok aşamalı derlemede her `FROM` satırı değişir. `.nvmrc`, `engines` ve CI matrisi aynı commit'te güncellenir.
- Tartışma noktası: Tag mı yoksa digest pin mi kullanılacak? Mevcut düzen digest ise digest korunur.
**Faz 3 · Doğrulama (~5k)**
- Kapı 1: `docker build --no-cache -t app:node20 .` çalıştırılır. Çıktıyı vrm-log-ozetleyici özetler.
- Kapı 2: `docker run --rm app:node20 node -v` v20 göstermeli. Konteyner içinde `npm test` (ya da `npm ci && npm run build`) yeşil olmalı.
- Kapı 3: Yerelde kuruluysa güvenlik taraması `trivy image app:node20` ya da `docker scout cves` ile yapılır. Kurulu değilse atlanır ve raporda belirtilir.
- İnceleyen: sec-docker-guvenlik root kullanıcı ve imaj boyutu farkına bakar.
- Bitiş: commit · test sayısı · CI durumu · imaj boyutu öncesi/sonrası.
### Z
**Faz 1: Hazırlık** (~2k)
- Adım: `Dockerfile` ve `.nvmrc`, `package.json` içindeki `engines` alanı ile CI'daki `node-version` taranır (Grep). Hepsinin birlikte güncellenmesi gerekir.
- Tartışma noktası: hangi etiket kullanılacak? Mevcut varyant korunur (`node:18-alpine` ise `node:20-alpine`). Tekrarlanabilirlik için digest sabitlemesi önerilir ama kullanıcı onayına bırakılır.

**Faz 2: Değişiklik ve derleme** (~4k)
- Adım: `FROM` satırı ve yukarıda bulunan sürüm yerleri güncellenir. Ardından `docker build --no-cache -t app:node20 .` çalıştırılır.
- Kapı: derleme exit 0 olmalı. Yerel modüller (`bcrypt`, `sharp` gibi) yeniden derlenirken hata çıkarsa `ecc:build-error-resolver` devreye girer.

**Faz 3: Doğrulama** (~4k)
- Adım: `docker run --rm app:node20 node -v` çıktısı v20.x olmalı. Uygulama container içinde ayağa kaldırılır ve sağlık uç noktası `curl` ile denenir. Test paketi container içinde (`npm test`) ya da CI'da koşturulur.
- Güvenlik kapısı: alt ajan `sec-docker-guvenlik` Dockerfile'ı inceler (root kullanıcı, sızan sırlar, imaj şişkinliği). `docker scout cves` ya da `trivy image` kuruluysa çalıştırılır. Kurulu değilse bu adım atlanır ve raporda belirtilir.

**Faz 4: İnceleme** (~2k)
- İnceleyen: `ecc:code-reviewer`. CI matrisinin ve `engines` alanının Dockerfile ile tutarlı olduğunu doğrular.

## 10. Jest test paketinde zaman aşımına uğrayan tek bir asenkron testi düzelt.
### X
**Skill:** superpowers:systematic-debugging. Kök neden kanıtlanmadan düzeltme yapılmaz.
**Faz 1 · Yeniden üretme (~4k)**
- Adım: `npx jest -t "<test adı>" --runInBand --detectOpenHandles` çalıştırılır ve zaman aşımının kırmızı olduğu görülür. Araç: Jest CLI.
**Faz 2 · Kök neden (~6k)**
- Adım: Testin ilgili satırları dar Read aralığıyla okunur. Aday nedenler:
  - Eksik `await` ya da `return`
  - Çağrılmayan `done` (async ile karışık kullanım)
  - Sahte zamanlayıcı ile gerçek Promise çakışması (`advanceTimersByTimeAsync`)
  - Çözülmeyen mock
  - Kapanmayan handle (sunucu, soket, DB)
- Tartışma noktası: `jest.setTimeout` ya da timeout değerini artırmak düzeltme sayılmaz. Bu ancak ölçülmüş gerçek bir süre varsa ve gerekçe yorumu eklenirse kabul edilir.
**Faz 3 · Düzeltme (~3k)**
- Adım: Kök neden tek yerde, en küçük diff ile düzeltilir. Ortak bir yardımcı değişiyorsa önce onu çağıran yerler Grep ile bulunur.
**Faz 4 · Kapı (~4k)**
- Kapı 1: Test 20 kez döngüde koşar (`for i in $(seq 20); do npx jest -t "<ad>" || break; done`). Yöntem qa-flaky-avci'den alınır.
- Kapı 2: Tam suite yeşil olmalı ve `--detectOpenHandles` uyarı vermemeli.
- İnceleyen: inc-test-kalitesi-inceleme, assert'in hâlâ anlamlı olup olmadığına ve yalnız bekleme süresinin değişip değişmediğine bakar.
- Bitiş: commit · test sayısı · CI durumu.

Yaptıklarım bir varsayıma dayanıyor: projelerin dosyalarını açmadım, varyant, CI yolu ve kurulu eklentiler varsayım. Asıl risk 9. işte: Node 20'nin desteği bitti, 20'ye geçmek de yeniden eskiyen bir sürüme geçmek olur.
### Y
**Faz 1: Yeniden üretme** (~3k)
- Adım: `npx jest path/to/file.test.ts -t "<test adı>" --runInBand` komutuyla zaman aşımı yeniden üretilir ve kırmızı sonuç gözle görülür. Kararsız (flaky) davranış şüphesi varsa `qa-flaky-avci` testi 20 kez döngüde koşturur.

**Faz 2: Kök neden** (~4k)
- Adım: aşağıdaki aday nedenler kontrol edilir. Araç: `superpowers:systematic-debugging` akışı.
  - `await` edilmemiş ya da hiç çözülmeyen bir promise
  - `done` ile `async` fonksiyonun birlikte kullanılması
  - `jest.useFakeTimers()` açıkken zamanlayıcının ilerletilmemesi (`advanceTimersByTimeAsync` eksik)
  - Mock'lanmamış gerçek ağ ya da veritabanı çağrısı
  - `afterEach` içinde kapatılmayan bir handle (`--detectOpenHandles` ile tespit edilir)
- Tartışma noktası: `jest.setTimeout` değerini artırmak mı, kök nedeni düzeltmek mi? Kök neden kanıtlanmadan süre artırılmaz.

**Faz 3: Düzeltme** (~3k)
- Adım: düzeltme yalnız ilgili test ya da mock satırlarında yapılır. Üretim kodunda hata çıkarsa önce onu yeniden üreten bir test yazılır.
- Kapı: önce testin kendisi 20 kez arka arkaya koşturulur (`--runInBand`), ardından paketin tamamı `npx jest` ile koşturulur.

**Faz 4: İnceleme** (~2k)
- İnceleyen: `qa-test-kokusu`. Düzeltmenin `sleep` eklemek ya da süreyi şişirmek gibi bir maskeleme olmadığını kontrol eder.

Planlarda adı geçen ajan, skill ve CLI'ların bu ortamda var olup olmadığını denetlemedim. `trivy`/`docker scout` kurulu değilse 9. işin güvenlik taraması atlanır. 8. işteki import temizliği, yan etkili importları silerse çalışma zamanında hata çıkarabilir.
### Z
**Faz 1 · Yeniden üretme (≈4k jeton)**
- Süreç `superpowers:systematic-debugging` ile yürütülür.
- Testi tek başına koştur: `npx jest <dosya> -t "<ad>" --runInBand --detectOpenHandles`. Zaman aşımı hatası kırmızı olarak görülmeden düzeltmeye geçilmez.

**Faz 2 · Kök neden (≈5k jeton)**
- Olası nedenler sırayla kontrol edilir:
  - eksik `await`/`return`;
  - hiç çağrılmayan `done`;
  - sahte zamanlayıcıların gerçek promise ile karışması (`advanceTimersByTimeAsync` gerekebilir);
  - hiç çözülmeyen bir mock;
  - açık kalan handle.
- **Tartışma:** `jest.setTimeout` veya test zaman aşımını artırmak çözüm sayılmaz. Bu yalnız işlem gerçekten yavaşsa ve süre ölçülerek kanıtlanmışsa kabul edilir.

**Faz 3 · Düzeltme ve kapı (≈4k jeton)**
- Kök nedeni en küçük değişiklikle düzelt.
- Testi 20 kez üst üste koştur (`qa-flaky-avci` yöntemi), sonra tüm paketi çalıştır. Bu koşular sonnet alt ajanında yapılır.
- İnceleme: `inc-test-kalitesi-inceleme`. Testin hâlâ anlamlı bir şeyi doğruladığını kontrol eder.

Atladığım: hiçbir projeye bakmadım. Varyant, CI dosyaları ve test adları varsayım.  
Risk: 9. işte Node 20'nin desteği bitmiş durumda. Hedef sürüm onaylanmadan uygulamaya geçilmemeli.
