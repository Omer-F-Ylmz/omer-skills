# mob — 8 benzersiz kayıt

**Amaç:** Mobil uygulama ajanları: çalışma izinleri, derin bağlantı, push bildirim, React Native navigasyon/performans/yerel modül, uygulama boyutu ve mağaza ekran görüntüleri.

**İç yapı:** Tümü [ajan], ad kalıbı mob-<iş>; gruplar: platform (calisma-izni, derin-baglanti, push-bildirim), React Native (rn-navigasyon, rn-performans, yerel-modul-koprusu), yayın (uygulama-boyutu, magaza-ekran-goruntusu).

## En güçlü parçalar
- `mob-rn-performans` — Liste sanallaştırma, Hermes, yeniden render ve JS thread yükünü azaltarak RN takılmasını düzeltir.
- `mob-push-bildirim` — APNs/FCM token, izin zamanlaması ve payload ile başarısız ya da yok sayılan push'ları ele alır.
- `mob-derin-baglanti` — Universal link, Android App Links ve ertelenmiş derin bağlantı; uygulama yerine tarayıcı açılma sorunu.
- `mob-calisma-izni` — iOS/Android'de kamera, konum, fotoğraf, bildirim izinleri ve reddedilme durumları.
- `mob-rn-navigasyon` — React Navigation stack, tab, tipli parametre ve auth akışları.

## Birlikte kullanım
- mob-calisma-izni + mob-push-bildirim: bildirim izni zamanlaması ve token akışı.
- mob-rn-navigasyon + mob-derin-baglanti: bağlantıdan doğru ekrana yönlendirme.
- mob-uygulama-boyutu + mob-magaza-ekran-goruntusu: mağaza yayını hazırlığı.

## Tuzaklar
- Üç ajan React Native'e özgü (rn-navigasyon, rn-performans, yerel-modul-koprusu); yerel iOS/Android ya da başka çerçevede doğrudan geçerli değil.
- mob-yerel-modul-koprusu ve mob-magaza-ekran-goruntusu yalnız plan üretir; uygulama/derleme yapmaz.

## Üyeler
- ajan (8): mob-calisma-izni, mob-derin-baglanti, mob-magaza-ekran-goruntusu, mob-push-bildirim, mob-rn-navigasyon, mob-rn-performans, mob-uygulama-boyutu, mob-yerel-modul-koprusu
