# Pazarlama / kurumsal site — birleşim tarifi
Ne zaman: Landing, kurumsal tanıtım ya da fiyat sayfası; dönüşüm ve SEO hedefli iş.

## Fazlar
1. Araştırma ve konum: `ecc:marketing-campaign` — araştırma, konumlandırma ve içerik üretimi fazları · birlikte: `marketing-skills:site-architecture` hangi sayfanın olacağını ve bağlantılarını planlar.
2. Tasarım yönü: `frontend-craft:frontend-craft` — marka kararı, referans eşleme, 3 genişlikte screenshot, a11y/perf kabulü · birlikte: `tasarim-katalog` jenerik olmayan referans, font ve kütüphane seçer.
3. Metin: `marketing-skills:copywriting` — ikna eden site metni, AI kalıplarından kaçınır · birlikte: `sepia:sepia` kalan AI tadını temizler.
4. Uygulama: `landing-page` — yapı, yerleşim kalıbı, dönüşüm stratejisi · birlikte: fiyat sayfası varsa `pricing-page`.
5. SEO ve meta: `fixing-metadata` — başlık, canonical, Open Graph · birlikte: `marketing-skills:seo-audit` teknik SEO sorunlarını teşhis eder.
6. Dönüşüm ve test: `marketing-skills:cro` — sayfa ve form dönüşümü · birlikte: `fe-donusum-optimize` test edilebilir değişiklik önerir; tarayıcı kontrolü `playwright` (MCP).
7. Kapanış: `superpowers:verification-before-completion`.

## İnceleme ajanları
- `impeccable`: hiyerarşi, tipografi, renk, erişilebilirlik denetimi.
- `web-design-guidelines`: UI kodunu Web Interface Guidelines'a göre gözden geçirir.
- `fe-site-mimarisi`: URL şeması, gezinme derinliği, iç bağlantı.

## Güvenlik ve kalite kapıları
- Erişilebilirlik: `ecc:accessibility`; gezinme: `cognitive-accessibility:wayfinding-navigation`.
- SEO: `marketing-skills:seo-audit` temiz; meta etiketleri tam.
- İletişim formu kişisel veri topluyorsa KVKK: `sec-kvkk-gdpr-kontrol`.
- Depoda sır yok: `gitleaks`.

## Tartışma konseyi
- Karar: konumlandırma, ana mesaj, fiyat paketi.
- `marketing-skills:marketing-council` — uzman danışman kurulu benzetimi. Teknik yığın kararı için `ecc:council`. Varsayılan Claude personaları.

## Jeton bütçesi
- Araştırma: orta (~15k, tahmini); rakip sayfa okuması `okuyucu` alt ajanına.
- Tasarım + uygulama: büyük (~50k, tahmini). Metin: orta (~10k). SEO/CRO: küçük (~8k). Kapanış: küçük (~3k), hepsi tahmini.

## Kaçınılacaklar
- Skill çakışmasında sıra: `frontend-craft:frontend-craft` > `impeccable` > diğerleri; `ecc:frontend-design-direction` geri planda kalır.
- Aynı sayfa için birden çok landing skill'i (`landing-page`, `landing-page-design`) karıştırmak.
- Ölçümsüz "dönüşüm arttı" iddiası.

## Aday (kurulu değil)
yok
