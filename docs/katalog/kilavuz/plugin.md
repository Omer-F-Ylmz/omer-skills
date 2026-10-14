# plugin — 6 benzersiz kayıt

**Amaç:** Claude Code eklenti geliştirme: uçtan uca eklenti oluşturma, yapı iskeleti, ajan üretimi, eklenti doğrulama, skill incelemesi ve hazır ECC yapılandırma derlemesi.

**İç yapı:** Bir [plugin] (everything-claude-code) + plugin-dev-* ve plugin-structure [skill]'leri; açıklamalarda 'Use this agent' ifadesi ajan kökenini gösterir.

## En güçlü parçalar
- `plugin-dev-create-plugin` — Bileşen tasarımı, uygulama, doğrulamalı rehberli uçtan uca eklenti oluşturma.
- `plugin-dev-plugin-validator` — Eklenti yapısını doğrulama ve kontrol.
- `plugin-dev-skill-reviewer` — Oluşturulan/değiştirilen skill'in kalite incelemesi.
- `plugin-dev-agent-creator` — Yeni ajan oluşturma istekleri.

## Birlikte kullanım
- plugin-structure → plugin-dev-create-plugin → plugin-dev-plugin-validator.
- plugin-dev-skill-reviewer + ajn-skill-test.

## Tuzaklar
- claude-plugins-official plugin-dev:* skill'leriyle çakışan kopyalar.
- everything-claude-code ecc ailesiyle örtüşür; tek amaçlı değil.

## Üyeler
- plugin (1): everything-claude-code
- skill (5): plugin-dev-agent-creator, plugin-dev-create-plugin, plugin-dev-plugin-validator, plugin-dev-skill-reviewer, plugin-structure
