# ios — 5 benzersiz kayıt

**Amaç:** gstack iOS araçları: SwiftUI uygulamalarında canlı cihaz QA, gerçek donanımda görsel tasarım denetimi, otonom hata düzeltme ve DebugBridge yönetimi.

**İç yapı:** Tümü [skill], gstack etiketli; QA/denetim (ios-qa, ios-design-review), düzeltme (ios-fix), köprü bakımı (ios-sync, ios-clean).

## En güçlü parçalar
- `ios-qa` — SwiftUI uygulamaları için canlı cihazda QA.
- `ios-design-review` — Gerçek donanımda iOS görsel tasarım denetimi.
- `ios-fix` — Otonom iOS hata düzelticisi.
- `ios-clean` — DebugBridge SPM paketini ve #if DEBUG kablolamasını kaldırır.

## Birlikte kullanım
- ios-sync → ios-qa → ios-fix → ios-clean (yayın öncesi köprüyü sökmek).
- gstack ailesinin diğer skill'leriyle aynı şablonlar.

## Tuzaklar
- Gerçek cihaz/macOS gerekir; Windows'ta çalışma katalog metninde belirtilmemiş.
- ios-clean çalıştırılmadan DebugBridge yayına kalabilir.

## Üyeler
- skill (5): ios-clean, ios-design-review, ios-fix, ios-qa, ios-sync
