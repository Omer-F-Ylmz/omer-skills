# workflow — 4 benzersiz kayıt

**Amaç:** Çalışma akışı kuralları: ilerlemeyi kendiliğinden ekran görüntüsüyle gösterme, 10 üzerinden puanlama ve hedefe ulaşma, korumalı değişiklik yayını, thread yönetimi.

**İç yapı:** Tümü [skill], workflow-<kural>; görsel kanıt (progress-screenshots, ship-change), değerlendirme (score-to-target), koordinasyon (threads-manager).

## En güçlü parçalar
- `workflow-ship-change` — Her değişikliği kullanıcının istediği korumalar ve başlangıç/ana an ekran görüntüleriyle yayınlar.
- `workflow-score-to-target` — 10 üzerinden puanlama ya da hedef puana ne gerektiği sorulduğunda.
- `workflow-threads-manager` — Thread'lerin merge/push durumu ve bitenleri arşivleme.

## Birlikte kullanım
- workflow-progress-screenshots + workflow-ship-change.

## Tuzaklar
- workflow-progress-screenshots sorulmadan ekran görüntüsü alır; ekran/pencere kuralıyla çakışabilir.
- workflow-threads-manager thread kavramının hangi araca ait olduğu katalog metninde belirtilmemiş.

## Üyeler
- skill (4): workflow-progress-screenshots, workflow-score-to-target, workflow-ship-change, workflow-threads-manager
