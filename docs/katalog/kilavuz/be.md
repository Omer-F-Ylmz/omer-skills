# be — 15 benzersiz kayıt

**Amaç:** Arka uç dağıtık sistem tasarım ajanları: dayanıklılık, mesaj güvenilirliği, saga, önbellek, hız sınırı, çoklu kiracılık, dosya yükleme, çift kayıt defteri, emir eşleştirme.

**İç yapı:** Tümü [ajan], be-<konu>; gruplar: güvenilirlik (dayaniklilik, mesaj, saga), performans/ölçek (onbellek, hiz-sinirlayici, yatay-olcekleme), veri/finans, dosya, iş kuyrukları.

## En güçlü parçalar
- `be-mesaj-guvenilirligi` — Outbox, idempotent tüketici, dead-letter, saga; kayıp/çift olaylarda.
- `be-dayaniklilik-kaliplari` — Kararsız uzak çağrılara timeout, jitter'lı retry, circuit breaker, bulkhead.
- `be-onbellek-gecersizlestirme` — TTL, write-through, geçersizleştirme, stampede koruması; bayat veride.
- `be-cift-kayit-defteri` — Tam sayı birim, değişmez kayıt, idempotent transfer; bakiye kaymasında.
- `be-bellek-sizintisi-avcisi` — Yeniden başlatana kadar büyüyen bellekte heap snapshot ile sızıntı avı.
- `be-coklu-kiraci-veri` — Paylaşımlı şema, kiracı başına şema/DB izolasyonunu seçip uygular.
- `be-hiz-sinirlayici` — Token bucket, sliding window, dağıtık sayaçla API hız sınırı.
- `be-buyuk-dosya-yukleme` — Presigned URL, multipart/devam ettirilebilir yükleme, zararlı yazılım taraması.

## Birlikte kullanım
- be-mesaj-guvenilirligi + be-saga-telafi: paylaşımsız işlemde olay ve telafi.
- be-dayaniklilik-kaliplari + be-hata-turu-hiyerarsisi: retry edilebilir/ölümcül ayrımı.
- be-dosya-yukleme + be-buyuk-dosya-yukleme; sec ailesinden sec-yol-gecisi ile güvenlik.

## Tuzaklar
- be-dosya-yukleme ile be-buyuk-dosya-yukleme kapsamları örtüşür.
- be-sidekiq-isler yalnız Sidekiq/Redis içindir.
- be-emir-eslestirme ve be-cift-kayit-defteri finansal alan özeldir; genel CRUD için değil.

## Üyeler
- ajan (15): be-bellek-sizintisi-avcisi, be-buyuk-dosya-yukleme, be-cift-kayit-defteri, be-coklu-kiraci-veri, be-dayaniklilik-kaliplari, be-dosya-yukleme, be-emir-eslestirme, be-hata-turu-hiyerarsisi, be-hiz-sinirlayici, be-is-calma-zamanlayici, be-mesaj-guvenilirligi, be-onbellek-gecersizlestirme, be-saga-telafi, be-sidekiq-isler, be-yatay-olcekleme
