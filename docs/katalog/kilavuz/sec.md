# sec — 35 benzersiz kayıt

**Amaç:** Uygulama güvenliği denetim ajanları: sır/bağımlılık taraması, kimlik doğrulama (JWT, Auth0, Keycloak, MFA), enjeksiyon/XSS/yol geçişi, gizlilik (KVKK/GDPR, PII), LLM ve skill tedarik güvenliği.

**İç yapı:** Tümü [ajan], sec-<konu>; gruplar: tarama (sast, sir, gitleaks, bagimlilik), kimlik (jwt-*, auth0, keycloak, mfa), web açıkları, gizlilik/uyum, altyapı (docker, zero-trust), raporlama.

## En güçlü parçalar
- `sec-cikis-oncesi-guvenlik` — Yayın öncesi sır, auth, bağımlılık, başlık kontrol listesi.
- `sec-sir-tarayici` — Repo ve git geçmişinde sızmış sırları bulur; değerleri değil konumları raporlar.
- `sec-sast-kosucu` — Semgrep, CodeQL, Bandit, gosec kurallarını koşup bulguları file:line ile ayıklar.
- `sec-skill-tedarik-tarama` — Üçüncü taraf Claude skill/plugin'lerini kurulum öncesi gizli talimat ve sızdırmaya karşı tarar.
- `sec-tehdit-modelleme` — Güven sınırları ve sıralı önlemlerle STRIDE tehdit modeli.
- `sec-istem-enjeksiyon-savunma` — LLM uygulamalarını kullanıcı girdisi, belge ve araç sonucundan gelen istem enjeksiyonuna karşı sertleştirir.
- `sec-yetkilendirme-matrisi` — Rol×eylem matrisi kurup her uç noktanın uyguladığını kontrol eder.
- `sec-kvkk-gdpr-kontrol` — Kişisel veri akışlarını rıza, saklama, silme yükümlülüklerine eşler.
- `sec-guvenlik-raporu` — Ham bulguları düzeltme adımlı önceliklendirilmiş rapora çevirir.
- `sec-ai-kod-guvenlik` — AI üretimi kodda gömülü sır, eksik yetkilendirme, güvensiz varsayılan arar.

## Birlikte kullanım
- sec-sast-kosucu + sec-semgrep-kural: hazır kurallar ve projeye özel Semgrep kuralı.
- sec-sir-tarayici + sec-gitleaks-gecmis + cli ailesinden gitleaks.
- sec-tehdit-modelleme → sec-owasp-top10 → sec-guvenlik-raporu.
- sec-pentest-plani yalnız yetkili test kapsamı için; bulgular sec-guvenlik-raporu'na.

## Tuzaklar
- Çakışma: sec-jwt-denetci ile sec-jwt-oturum, sec-sir-tarayici ile sec-gitleaks-gecmis örtüşür.
- sec-pentest-plani yetkili (authorized) test şartı taşır; kapsam ve kurallar önce yazılmalı.
- phoenix-security ve davila7/mukul975 aileleriyle konu çakışması olabilir; katalog metninde ayrım belirtilmemiş.

## Üyeler
- ajan (35): sec-acik-yonlendirme, sec-ai-kod-guvenlik, sec-alt-alan-ele-gecirme, sec-api-guvenlik, sec-auth0, sec-bagimlilik-acik, sec-ci-guvenlik-tarama, sec-cikis-oncesi-guvenlik, sec-docker-guvenlik, sec-gitleaks-gecmis, sec-guvenilmeyen-kod-yalitimi, sec-guvenlik-baslik, sec-guvenlik-raporu, sec-injection-denetci, sec-istem-enjeksiyon-savunma, sec-jwt-denetci, sec-jwt-oturum, sec-keycloak, sec-kvkk-gdpr-kontrol, sec-llm-pii-maskeleme, sec-loglama-gizlilik, sec-mfa-kurtarma, sec-owasp-top10, sec-pci-dss-kapsam, sec-pentest-plani, sec-sast-kosucu, sec-semgrep-kural, sec-sifreleme-denetci, sec-sir-tarayici, sec-skill-tedarik-tarama, sec-tehdit-modelleme, sec-xss-csrf-denetci, sec-yetkilendirme-matrisi, sec-yol-gecisi, sec-zero-trust-ag
