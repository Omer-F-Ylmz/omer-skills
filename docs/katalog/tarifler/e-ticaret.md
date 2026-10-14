# E-ticaret — birleşim tarifi
Ne zaman: Ürün kataloğu, sepet, ödeme ve sipariş akışı olan mağaza işi.

## Fazlar
1. Platform seçimi: WooCommerce ise `engineering-wordpress-shopping-cart`, Drupal Commerce ise `engineering-drupal-shopping-cart` — katalog, ödeme ağ geçidi, checkout ve sipariş yönetimi. Platformdan bağımsız iş için katalogda özel araç yok — genel: `superpowers:writing-plans`.
2. Katalog verisi: katalogda özel araç yok — genel: `ecc:postgres-patterns` şema, indeks ve RLS kalıpları.
3. Ödeme: `engineering-payments-billing-engineer` — PSP entegrasyonu, idempotent ödeme, webhook, SCA/3DS, PCI kapsamını daraltma · birlikte: `otm-webhook-tasarimci` imza kontrolü ve idempotent alıcı tasarlar. Convex projesinde `convex-billing`.
4. Ön yüz ve checkout: `frontend-craft:frontend-craft` — tasarım-uygulama disiplini · birlikte: `fe-form-tasarimci` checkout formunda net etiket ve satır içi doğrulama; `cognitive-accessibility:error-prevention-recovery` hata önleme.
5. Test: `qa-e2e-playwright` — kullanıcı akışı için kararlı Playwright e2e testleri · birlikte: `fe-donusum-optimize` checkout engellerini bulur.
6. Kapanış: `superpowers:verification-before-completion`.

## İnceleme ajanları
- `engineering-payments-billing-engineer`: ödeme kodunun ikinci gözü.
- `security-appsec-engineer`: güvenli kod incelemesi.
- `superpowers:requesting-code-review`: birleştirme öncesi.

## Güvenlik ve kalite kapıları
- PCI-DSS: `Compliance Auditor` (SOC 2, ISO 27001, HIPAA, PCI-DSS denetimi).
- KVKK: `sec-kvkk-gdpr-kontrol` (müşteri verisi, rıza, saklama, silme).
- Sır taraması `gitleaks`; statik analiz `semgrep`; dinamik test `strix`.
- SEO: `marketing-skills:seo-audit`; erişilebilirlik: `ecc:accessibility`.

## Tartışma konseyi
- Karar: platform (WooCommerce/Drupal/özel) ve ödeme sağlayıcısı seçimi.
- `ecc:council` — varsayılan Claude personaları: mağaza sahibi, ödeme mühendisi, güvenlik.

## Jeton bütçesi
- Platform: orta (~12k, tahmini). Veri: orta (~10k). Ödeme: büyük (~35k). Ön yüz: büyük (~40k). Test: orta (~15k). Kapanış: küçük (~3k). Hepsi tahmini.
- Sağlayıcı dokümanı okuması `okuyucu` alt ajanına.

## Kaçınılacaklar
- Kart verisini kendi sunucunda tutmak; PCI kapsamını büyütmek.
- Webhook'u imzasız ve idempotent olmadan işlemek.
- Aynı iş için agency ve engineering kopyasını birlikte çağırmak; birini seç.

## Aday (kurulu değil)
yok
