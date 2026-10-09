# Pazarlama skill paketi (30+ skill)
ad: Pazarlama skill paketi (30+ skill)
tur: skill
video: BiEvvC_66AQ
repo: coreyhaines31/marketingskills
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/coreyhaines31/marketingskills
telemetri: Skill'ler markdown olduğu için telemetri beklenmiyor, ama repo içeriğini tam taramadım, kesin değil. tools/ altında üçüncü taraf ortak entegrasyon rehberleri var (Converly, Ploy). Bunlar kullanılırsa o servislerin kendi veri politikaları geçerli olur.
yildiz: bilinmiyor
alt_tur: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Corey Haines'in hazırladığı, AI kodlama ajanları (Claude Code, Codex, Cursor, Windsurf ve Agent Skills spec'ini destekleyenler) için pazarlama skill koleksiyonu. Videoda "30+" deniyor. README'deki güncel liste yaklaşık 50 skill içeriyor: SEO/içerik, CRO, copy, reklam ve ölçümleme, büyüme/elde tutma, satış/GTM, strateji. Videodaki kısa adlar (page-cro, signup-cro, paid-ad) repoda farklı: cro, signup, ads gibi.
## Mekanizma
Her skill skills/&lt;ad&gt;/ altında bir markdown (SKILL.md) dosyasıdır. Ajan, açıklamadaki "When the user wants to..." tetikleyicisine bakarak ilgili görevde skill'i yükler. Tüm skill'ler önce "product-marketing" skill'inin ürettiği bağlam belgesini (ürün, hedef kitle, konumlandırma) okur. Skill'ler "Related Skills" bölümüyle birbirine çapraz referans verir. Kod çalıştırmaz, çoğunlukla çerçeve ve iş akışı talimatıdır. Repoda ayrıca tools/ altında entegrasyon rehberleri ve CLI regresyon testleri var.
## Kanıt
- Tek kurulumda 30'dan fazla pazarlama skill'i var → doğrulandı · README skill tablosu ve skills/ ağacı yaklaşık 50 klasör gösteriyor (ab-testing, ad-creative, ads, ai-seo, analytics, seo-audit, cro, signup, onboarding, popups, paywalls vb.).
- Kategoriler: SEO & Content, CRO, Content & Copy, Paid & Measurement → doğrulandı · README mimari şeması bu kategorileri ve ek olarak Growth & Retention, Sales & GTM, Strategy kategorilerini listeliyor.
- Skill adları videodaki gibi (page-cro, signup-cro, paid-ad vb.) → çürütüldü · Repoda adlar cro, signup, ads, copywriting, emails şeklinde; video eski sürüm ya da kısaltılmış adlar göstermiş olabilir.
- Tek komutla kurulum → sınanamadı · README kesildiği için kurulum komutunu görmedim; plugin manifest dosyaları var.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repoda .claude-plugin/marketplace.json ve plugin.json var, yani Claude Code plugin marketplace'i ile kurulabilir. Tam komut README'nin kesilen kısmında olduğu için doğrulanmadı.
- Alternatif: skills/ klasörünü .claude/skills/ (proje) ya da ~/.claude/skills/ altına kopyalamak.
- Kurulumdan sonra önce product-marketing skill'i ile bağlam belgesini oluşturmak gerekir.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Pazarlama işlerinde (SEO denetimi, CRO, copy, reklam, e-posta dizileri, fiyatlandırma, lansman) ajana hazır çerçeve ve kontrol listesi verir. Her seferinde prompt yazma ihtiyacını azaltır, çıktıyı tutarlı yapar.
## Maliyet/risk
Düşük: salt markdown, MIT lisanslı. Dikkat edilecekler: (1) çok sayıda skill açıklaması bağlamı şişirebilir, gerekenleri seçerek kur; (2) "Verified Partners" ortak ürünleri tanıtır, README tarafsız kaldığını söylüyor ama öneriler yine de gözden geçirilmeli; (3) skill'ler üçüncü taraf CLI/servis kurmayı önerebilir, çalıştırmadan önce incele; (4) çerçeveler genel ve İngilizce/SaaS odaklı, Türkiye pazarına uyarlama gerekebilir.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill olarak var, doğrudan kurulabilir. Kendi sürümümüz için: (1) MIT lisansı gereği fork et ve ihtiyaç duyulan 8-10 skill'i seç (seo-audit, ai-seo, cro, copywriting, emails, ads, analytics, product-marketing); (2) açıklamaları Türkçe tetikleyicilerle genişlet; (3) Türkiye pazarına özel örnekler ekle; (4) product-marketing bağlam belgesini proje başına tek dosya olarak tut; (5) kullanılmayanları çıkararak bağlam maliyetini düşür.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Ortak bağlam skill'i (product-marketing): tüm skill'ler önce ürün/kitle/konumlandırma belgesini okur
kaynak: https://github.com/coreyhaines31/marketingskills
### Skill'ler arası çapraz referans (copywriting ↔ cro ↔ ab-testing, seo-audit ↔ schema ↔ ai-seo)
kaynak: https://github.com/coreyhaines31/marketingskills
### Claude Code ve Codex plugin manifestleri, çok ajanlı uyumluluk (Agent Skills spec)
kaynak: https://github.com/coreyhaines31/marketingskills
### Geniş kapsam: SEO, AI-SEO, CRO, copy, reklam, analitik, e-posta, SMS, fiyatlandırma, lansman, PR, referans programları
kaynak: https://github.com/coreyhaines31/marketingskills
## Destek
- BiEvvC_66AQ · 0:18 · SEO, CRO, içerik/copy, ücretli reklam ölçümü gibi alanlarda tek kurulumda 30'dan fazla pazarlama skill'i. · kanıt: Karede kategorilere ayrılmış skill şeması görülüyor. (karede: Şema: 'SEO & Content' (seo-audit, ai-seo, site-arch, programm, schema, content), 'CRO' (page-cro, signup-cro, onboard, form-cro, popup-cro, paywall), 'Content & Copy' (copywritng, copy-edit, cold-email, email-seq, social), 'Paid Measure…' (paid-ad, ad-crea, ab-test, analytic…).)
