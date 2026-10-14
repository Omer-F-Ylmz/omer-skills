# Güvenlik testi — birleşim tarifi
Ne zaman: Yayın öncesi, auth/ödeme/dosya yükleme eklenince ya da açık bir güvenlik denetimi istenince.

## Fazlar
1. Keşif ve tehdit modeli: `departman-guvenlik` — sır taraması, SAST, pentest ve KVKK sırasını verir · birlikte: `threat-modeling` veri akışı, giriş noktası ve güven sınırlarından sıralı STRIDE/DREAD tehditleri çıkarır.
2. Sır taraması: `gitleaks` — kodda ve git geçmişinde sızmış sırları tarar, zafiyet tarayıcı değildir · birlikte: `sec-gitleaks-gecmis` geçmişte koşar, allowlist ve baseline ayarlar.
3. Statik analiz: `semgrep` — kaynak koda benzeyen kalıplarla hata varyantı bulur · birlikte: `sec-sast-kosucu` bulguları dosya:satır ile ayıklar; özel kural gerekirse `sec-semgrep-kural`.
4. Bağımlılık: `sec-bagimlilik-acik` — manifestlerde açıklı ya da terk edilmiş paketi bulur, güvenli yükseltme önerir.
5. Dinamik test: `strix` — hedef uygulamada yapay zekâ ajanlarıyla sızma testi yapar · birlikte: `owasp-top-10-testing` Strix ile OWASP Top 10:2025 kategorilerinde gerçek istismar dener. Yalnız izinli hedefte.
6. Kod denetimi: `phoenix-security-review:security-assessment` — OWASP Top 10/ASVS ile denetim · birlikte: dal farkı için `tm-quick-security-assessment` birleştirme öncesi hızlı geçiş yapar.
7. Kapanış: `superpowers:verification-before-completion` — "temiz" demeden önce kanıt ister.

## İnceleme ajanları
- `security-appsec-engineer`: tehdit modeli, güvenli kod incelemesi, SAST/DAST entegrasyonu.
- `sec-owasp-top10`: zayıflığı OWASP Top 10 kategorisine eşler, düzeltme önerir.
- `security-architect`: güven sınırı ve derinlemesine savunma incelemesi.

## Güvenlik ve kalite kapıları
- `gitleaks` temiz; `semgrep` yüksek önem bulgusu yok.
- `strix` bulguları doğrulanmış PoC ile raporlanır.
- CI iş akışları: `gha-security-review`; CI'ya tarama eşiği: `sec-ci-guvenlik-tarama`.
- Kişisel veri varsa KVKK: `sec-kvkk-gdpr-kontrol` (rıza, saklama, silme).
- ZAP katalogda yok; dinamik test `strix` ile.

## Tartışma konseyi
- Karar: bulgunun gerçek mi yanlış pozitif mi olduğu, düzeltme önceliği.
- `ecc:council` — birden çok geçerli yol varken yapılandırılmış itiraz. Varsayılan Claude personaları: saldırgan, savunucu, ürün sahibi.

## Jeton bütçesi
- Keşif: orta (~15k, tahmini). Sır + SAST: küçük (~8k, tahmini), ham çıktı `okuyucu` alt ajanına.
- Dinamik test: büyük (~40k, tahmini). Denetim: orta (~20k, tahmini). Kapanış: küçük (~3k, tahmini).

## Kaçınılacaklar
- İzinsiz hedefe pentest.
- `gstack-cso` claude.ai'de çalışmaz; derlenmiş launcher ve container ister.
- Aynı işi gören denetim skill'lerini art arda koşmak (`security-review`, `security-audit`, `octo:octopus-security-audit`): birini seç.
- `gitleaks` çıktısını zafiyet listesi sanmak.

## Aday (kurulu değil)
yok
