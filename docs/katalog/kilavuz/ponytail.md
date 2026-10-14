# ponytail — 13 benzersiz kayıt

**Amaç:** Tembel kıdemli geliştirici modu: tam çözen en küçük değişiklik, YAGNI, stdlib öncelik; aşırı mühendislik incelemesi, repo denetimi, kısayol borç defteri ve kazanç tablosu.

**İç yapı:** ponytail [plugin] + ponytail:<x> skill'leri ve aynı adların öneksiz [skill] kopyaları: ponytail (mod), review (diff), audit (tüm repo), debt (ponytail: yorumları), gain, help.

## En güçlü parçalar
- `ponytail:ponytail` — Görevi tam çözen en küçük değişiklik ve tek okumada anlaşılan yanıt.
- `ponytail:ponytail-review` — Diff/PR'da yalnız aşırı mühendisliğe odaklı inceleme.
- `ponytail:ponytail-audit` — Tüm repoda şişkinlik ve silinebilir kod taraması.
- `ponytail:ponytail-debt` — Kod tabanındaki ponytail: yorumlarını borç defterine toplar.
- `ponytail:ponytail-gain` — Benchmark medyanlarından ölçülmüş etkiyi skor tablosu olarak gösterir.

## Birlikte kullanım
- ponytail:ponytail (yazım) → ponytail:ponytail-review (diff) → ponytail:ponytail-debt (borç).
- inc-ponytail-kod ajanı aynı bakışla diff inceler.

## Tuzaklar
- Çakışan kopyalar: her skill hem ponytail:<x> hem öneksiz <x> olarak var.
- ponytail modu tüm oturuma yayılır; kullanıcı 'stop ponytail' diyene dek aktif.
- ponytail-help kalıcı mod değil, tek seferlik kart.

## Üyeler
- plugin (1): ponytail
- skill (12): ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review, ponytail:ponytail, ponytail:ponytail-audit, ponytail:ponytail-debt, ponytail:ponytail-gain, ponytail:ponytail-help, ponytail:ponytail-review
