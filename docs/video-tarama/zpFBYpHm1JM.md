# Codex ve Claude Limitlerim Artık Bitmiyor! Ücretsiz Araç (Ponytail)
kanal: HQ NET · süre: 13 dk · altyazı: otomatik tr
ana iddia: Ponytail plugin'i (tek komutla Claude Code'a kurulan) modeli "tembel senior dev" gibi davrandırıp gereksiz kod/token üretimini azaltıyor; 9Router ise 40+ sağlayıcı üzerinden "sınırsız ücretsiz" AI kullanımı ve RTK tabanlı ek token tasarrufu vaat ediyor (sayılar kanalın kendi karşılaştırmasından, doğrulanmamış).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| dietrichgebert/ponytail | YENİ | ELE | Claude Code plugin marketplace'ten `/plugin install ponytail@ponytail`; kurulu RTK ile aynı niş (token/kod azaltımı) — çift; kendi benchmark'ı "%80-94 az kod" iddiası sonradan düzeltilmiş (bare-model karşılaştırma artefaktı) |
| decolua/9router | YENİ | ELE | 40+ sağlayıcıya proxy ile "ücretsiz sınırsız AI", ayrıca RTK entegrasyonu iddia ediyor (RTK zaten kurulu — çift); "ücretsiz sınırsız" iddiası sağlayıcı ToS riski taşıyor |
## ölçütler (ELE)
- dietrichgebert/ponytail: bakım=pushed 2026-09-14, MIT lisans var ama 140236 yıldız (basit bir "rule/skill" plugin için) şüpheli derecede yüksek · çift=RTK ile aynı kategori · izin=Claude Code plugin sistemi üzerinden (Windows dahil resmi destek), hesap/API anahtarı istemiyor · context=plugin etkinleşince 6 skill (`/ponytail`, `/ponytail-review` vb.) oturuma ekleniyor · kurulum: `/plugin install ponytail@ponytail`
- decolua/9router: bakım=pushed 2026-09-10, MIT, 29034 yıldız (yine şüpheli yüksek) · çift=RTK ile aynı niş + üstüne 40+ sağlayıcı hesap/API anahtarı yönetimi · izin=npm global kurulum veya Docker; "ücretsiz sınırsız" iddiası 3. taraf sağlayıcı hesaplarının ToS'unu zorlayabilir (risk) · context=proxy/router, arka planda çalışır, sohbete tool şeması eklemez ama trafiği yönlendirir · kurulum: `npm install -g 9router` (KURMA, yalnız rapor)
## hedefler (BİLGİ)
- yok
