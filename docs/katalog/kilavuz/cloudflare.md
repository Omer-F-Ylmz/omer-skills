# cloudflare — 4 benzersiz kayıt

**Amaç:** Cloudflare ürün seçimi ve mimari, e-posta gönderme/yönlendirme, Cloudflare One Zero Trust/SASE kurulumu ve mevcut VPN/SWG/SASE'den göç.

**İç yapı:** Tümü [skill]; genel yönlendirici cloudflare + ürün skill'leri (email-service, cloudflare-one, cloudflare-one-migrations).

## En güçlü parçalar
- `cloudflare` — Ürün adı verilmeden ihtiyaç anlatıldığında mimari ve ürün seçimi.
- `cloudflare-one` — Zero Trust/SASE dağıtımı tasarlama, yapılandırma, sorun giderme.
- `cloudflare-one-migrations` — VPN/SWG/SASE'den göçte politika eşleme ve eşlik planı.

## Birlikte kullanım
- cloudflare → cloudflare-one → cloudflare-one-migrations.
- daymade-skills cloudflare-troubleshooting ile API kanıtlı sorun giderme.

## Tuzaklar
- cloudflare-one ile cloudflare-one-migrations ayrı; göç işi için ikincisi.
- Hesap ve plan gereksinimi katalog metninde belirtilmemiş.

## Üyeler
- skill (4): cloudflare, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations
