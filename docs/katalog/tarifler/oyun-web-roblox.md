# Oyun (web / Roblox / motor) — birleşim tarifi
Ne zaman: Tarayıcıda three.js oyunu, Unity/Godot betiği ya da Roblox oyunu.

## Fazlar
1. Tasarım belgesi: `oyn-oyun-dokuman` — tek sayfalık tasarım: çekirdek döngü, mekanik, kapsam · birlikte: `oyn-seviye-tasarim` tempo, zorluk rampası ve seviye akışı.
2. Karşılaşma planı: `design-game-encounters` — arena, düşman dizilimi, ödül ritmi · birlikte: `oyn-dusman-ai` durum makinesiyle düşman davranışı.
3. Uygulama (web): `oyn-three-oyun-sahne` — girdi, döngü, çarpışma, sahne yapısı · birlikte: `threejs` sahne ve performans. Motor işinde `unity` ya da `godot` (MCP) + `oyn-oyun-motoru-script`.
4. Uygulama (Roblox): `roblox-game-development-lifecycle` (kapalı — açılması gerekir) — Roblox yaşam döngüsü şemsiyesi · birlikte: `oyn-lua-betik` hızlı Lua yazar; Roblox'a özgü bilgisi katalogda yazmıyor.
5. Denge: `oyn-oyun-denge` — hasar, maliyet, XP ve ilerleme eğrileri · birlikte: `oyn-uyarlanabilir-zorluk` oyuncu sinyaliyle zorluk.
6. Test: `test-playable-web-games` — oynanış QA, regresyon, kontrol, erişilebilirlik, mobil, performans · birlikte: `optimize-threejs-games` kare süresi ve draw call bütçesi.
7. Yayın: `ship-web-games` — yayın derlemesi, varlık teslimi, üretim smoke testi.

## İnceleme ajanları
- `oyn-oyun-denge`: sayı eğrilerinin ikinci gözü.
- `superpowers:requesting-code-review`: birleştirme öncesi.

## Güvenlik ve kalite kapıları
- Test: `test-playable-web-games` geçti; tarayıcı kanıtı `playwright` (MCP).
- Çok oyunculuda sunucu otoritesi: `oyn-ag-senkronu`.
- Depoda sır yok: `gitleaks`.

## Tartışma konseyi
- Karar: çekirdek döngü ve motor seçimi (web, Unity, Godot, Roblox).
- `ecc:council` — varsayılan Claude personaları: oyun tasarımcısı, oyuncu, teknik lider.

## Jeton bütçesi
- Tasarım: küçük (~8k, tahmini). Plan: orta (~10k). Uygulama: büyük (~50k). Denge: küçük (~6k). Test: orta (~15k); log alt ajana. Yayın: küçük (~5k). Hepsi tahmini.
- Motor dokümanı okuması `okuyucu` alt ajanına.

## Kaçınılacaklar
- Roblox iskeletini kapalı skill açılmadan ona dayandırmak.
- `oyun-gelistirme-paket` ile tekil skill'leri aynı anda yüklemek.
- Performans bütçesi olmadan efekt eklemek.

## Aday (kurulu değil)
- `@react-three/a11y`: R3F sahnelerine odak, klavye ve ekran okuyucu katmanı.
- `@14islands/r3f-scroll-rig`: R3F'yi smooth scroll'a bağlar (oyundan çok landing için).
