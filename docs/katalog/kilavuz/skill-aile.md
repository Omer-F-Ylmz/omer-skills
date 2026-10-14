# skill — 5 benzersiz kayıt

**Amaç:** Skill oluşturma, düzenleme, test etme, güvenlik taraması ve mevcut skill'leri keşfetme araçları.

**İç yapı:** Tümü [skill], ad kalıbı skill-<iş>: yazım (skill-creator, skill-development, skill-writer), güvenlik (skill-scanner), keşif (skill-ui-cli).

## En güçlü parçalar
- `skill-creator` — Sıfırdan skill oluşturma, düzenleme, optimize etme, eval koşturma ve benchmark.
- `skill-scanner` — Skill'i enjeksiyon ve güvenlik açısından tarar, SKILL.md'yi doğrular.
- `skill-writer` — Kaynakları sentezleyerek skill yazar; olumlu/olumsuz örneklerden iyileştirir.
- `skill-ui-cli` — Ajan ya da masaüstü AI istemcisinin mevcut skill'leri listeleyip görevle karşılaştırması.

## Birlikte kullanım
- skill-writer / skill-creator → skill-scanner: yazılan skill'i yayın öncesi taramak.
- skill-development + plugin-dev ailesi: eklenti içine skill eklemek.
- writing ailesindeki writing-skills ile skill doğrulama.

## Tuzaklar
- skill-creator, skill-development ve skill-writer kapsamı örtüşür; tek biri seçilmeli.
- skill-development eklentiye skill eklemeye yöneliktir; bağımsız skill için skill-creator daha uygun.

## Üyeler
- skill (5): skill-creator, skill-development, skill-scanner, skill-ui-cli, skill-writer
