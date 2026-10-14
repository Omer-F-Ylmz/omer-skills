# universal-modder — 13 benzersiz kayıt

**Amaç:** Sahip olunan hemen her oyunu AI ajanla modlama: motor keşfi, tersine mühendislik, fal ile üretilen sanat/3D/ses, oyun içi test, birleştirme modları ve yayın.

**İç yapı:** universal-modder [plugin] + universal-modder:<adım> skill'leri ve fal [mcp]; akış: keşif (game-recon, game-research-websearch, share-field-notes), iç yapı (reverse-engineering), varlık (fal-assets, asset-pipeline), doğrulama (game-automation), çıktı (publish-mod, showcase-video); giriş noktaları mod-any-game ve mashup-mods.

## En güçlü parçalar
- `universal-modder:mod-any-game` — Oyun modlama, genişletme, tersine mühendislik isteklerinin ana giriş noktası.
- `universal-modder:game-recon` — 'Modlanabilir mi, motoru ne' sorularıyla her mod işinin başında keşif.
- `universal-modder:reverse-engineering` — Boss AI, hasar fonksiyonu, dosya biçimi gibi oyun iç yapısını çözer.
- `universal-modder:game-automation` — Modu oyun içinde doğrular, menüleri otomatik gezer, tekrarlanabilir test/demo kurar.
- `universal-modder:fal-assets` — Mod için yeni sanat, ses ve 3D modeli fal ile üretir.

## Birlikte kullanım
- game-recon → game-research-websearch → reverse-engineering → mod-any-game → game-automation → publish-mod.
- universal-modder:fal-assets → universal-modder:asset-pipeline: üretilen varlıkları sprite/animasyon karesine dönüştürmek.
- oyn ailesindeki oyn-mod-guvenlik-kontrol ile indirilen mod dosyalarını denetlemek.

## Tuzaklar
- fal [mcp] ve fal-assets dış servise (mcp.fal.ai) bağlanır, yerel model değildir; üretim çağrısı sayısı sınırlanmalı.
- universal-modder:share-field-notes notları paylaşmak içindir; paylaşılan notta gizli/özel bilgi olmamalı.

## Üyeler
- mcp (1): fal
- plugin (1): universal-modder
- skill (11): universal-modder:asset-pipeline, universal-modder:fal-assets, universal-modder:game-automation, universal-modder:game-recon, universal-modder:game-research-websearch, universal-modder:mashup-mods, universal-modder:mod-any-game, universal-modder:publish-mod, universal-modder:reverse-engineering, universal-modder:share-field-notes, universal-modder:showcase-video
