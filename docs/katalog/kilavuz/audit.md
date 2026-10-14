# audit — 4 benzersiz kayıt

**Amaç:** Proje/kod tabanı denetimi, AI tasarım slop'u incelemesi, referans özgünlüğü karşılaştırması ve değişiklik doğrulama/açıklama skill'leri.

**İç yapı:** Tümü [skill], ad kalıbı audit-<konu>: audit (/audit ile proje bootstrap), audit-ai-design-slop, audit-reference-originality, audit-verify-explain-grade-5.

## En güçlü parçalar
- `audit` — Yeni proje, dokümanı eksik kod tabanı ya da tek alan (/audit src/auth) için başlangıç denetimi.
- `audit-ai-design-slop` — Kanıta dayalı tasarım geri bildirimi, anti-slop incelemesi ve kaldırma öncelikli temizlik planı.
- `audit-verify-explain-grade-5` — Değişikliği gözden geçirme, doğrulama, düzeltmeyi açıklama ve test sonucunu özetleme.
- `audit-reference-originality` — Site çıktısını referans sayfa, ekran görüntüsü ve metinle karşılaştırıp özgünlüğü denetler.

## Birlikte kullanım
- audit-ai-design-slop + design ailesindeki design-review: görsel slop temizliği.
- audit-verify-explain-grade-5 değişiklik bitiminde doğrulama ve açıklama adımı olarak.
- audit + document ailesi: denetimde bulunan eksik dokümanı üretmek.

## Tuzaklar
- audit-reference-originality 'Codex must' ile başlar; Codex akışına yazılmış, uyarlama gerekebilir.
- audit-verify-explain-grade-5 tetikleyicisi çok geniş (review, audit, check, verify); başka inceleme skill'leriyle çakışabilir.

## Üyeler
- skill (4): audit, audit-ai-design-slop, audit-reference-originality, audit-verify-explain-grade-5
