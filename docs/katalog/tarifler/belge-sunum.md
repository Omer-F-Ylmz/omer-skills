# Belge ve sunum — birleşim tarifi
Ne zaman: Rapor, Word/PDF belgesi, sunum, tablo ya da proje dokümantasyonu üretimi.

## Fazlar
1. Girdi: `departman-belge` — docx/pptx/pdf/xlsx üretim sırası · birlikte: `markitdown` (MCP) PDF, DOCX, PPTX, XLSX'i Markdown'a çevirir.
2. Plan: `docs` — paylaşılan, yorumlanan belge türleri için varsayılan · birlikte: mimari karar varsa `documentation-and-adrs`.
3. Üretim: Word için `example-skills:docx`, sunum için `example-skills:pptx`, tablo için `example-skills:xlsx`. Tek belgeden anlatı slaytı için `claude-mem:wowerpoint`.
4. Dil: `sepia:sepia` — AI tadını temizler · birlikte: `writing-guidelines` yazım el kitabına göre denetler.
5. Erişilebilirlik: `accessible-content:readable-content` — geniş kitleye okunur metin · birlikte: `accessible-content:table-accessibility` tablolar için.
6. Kapanış: `superpowers:verification-before-completion` — dosya açılıp kontrol edildi kanıtı.

## İnceleme ajanları
- `Technical Writer`: geliştirici dokümanı, API başvurusu, README.
- `dok-pptx-sunum`: slayt başına tek fikir, tutarlı yerleşim.

## Güvenlik ve kalite kapıları
- Üretilen dosya gerçekten açılıyor; sayfa/slayt sayısı beklenen.
- Belgede sır ya da kişisel veri yok; varsa KVKK: `sec-kvkk-gdpr-kontrol`.
- Tablolar erişilebilir başlıklı.

## Tartışma konseyi
- Karar: belgenin ana mesajı ve hedef okur.
- `ecc:council` — varsayılan Claude personaları: yönetici okur, teknik okur, editör.

## Jeton bütçesi
- Girdi: orta (~15k, tahmini); uzun kaynak `okuyucu` alt ajanına.
- Plan: küçük (~5k). Üretim: orta (~20k). Dil: küçük (~6k). Erişilebilirlik: küçük (~4k). Kapanış: küçük (~3k). Hepsi tahmini.

## Kaçınılacaklar
- `xlsx` (kapalı) yerine kurulu `example-skills:xlsx` kullan.
- `gstack-document-generate` git push çalıştırır; dal ve izin kontrolsüz kullanma.
- Aynı sunum için birden çok deck skill'i (`octo:skill-deck`, `baoyu-slide-deck`, `presentation-creator`) denemek; birini seç.

## Aday (kurulu değil)
yok
