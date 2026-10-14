# build — 17 benzersiz kayıt

**Amaç:** Üst düzey web deneyimleri ve three.js tabanlı oyunlar kurma skill'leri: Awwwards kalitesi site, scroll dünyaları, parçacık/wireframe efektleri, izometrik ARPG sistemleri ve oyun varlıkları.

**İç yapı:** Tümü [skill], ad kalıbı build-<konu>; gruplar: web deneyimi (awwwards-quality-sites, daily-inspiration-sites, threejs-scroll-worlds, interactive-particle-trail, wireframe-scan-reveal), oyun sistemleri (isometric-arpg, game-camera-controls, game-inventory, game-audio-feedback, threejs-enemy-systems, game-monster-system, mobile-threejs-games), varlık hattı (hybrid-game-assets, rigged-game-assets, vesperfall-review-assets), araç (game-map-editor, game-changelog).

## En güçlü parçalar
- `build-awwwards-quality-sites` — Premium, sinematik, hareket odaklı web sitesi istendiğinde ana skill.
- `build-threejs-scroll-worlds` — Scroll güdümlü WebGL dünyaları, kamera yolculukları ve 3D ürün hikayeleri.
- `build-isometric-arpg` — Oyun döngüsü mimarisi, kamera, bölge, savaş, ilerleme ve kayıtları kapsar.
- `build-hybrid-game-assets` — İçe aktarılan mesh, prosedürel geometri, AI referans görseli, sprite ve VFX arasında seçim yapar.
- `build-game-inventory` — Eşya şeması, yığın kuralı, ekipman slotu, atomik takas ve kayıt göçünü kayıpsız kurar.
- `build-mobile-threejs-games` — Dokunmatik hareket, hedef seçimi, güvenli alan ve dikey/yatay düzenler.

## Birlikte kullanım
- build-isometric-arpg + build-game-camera-controls + build-threejs-enemy-systems + build-game-audio-feedback: oyun çekirdeği.
- build-rigged-game-assets + build-game-monster-system + build-vesperfall-review-assets: karakter/canavar varlık hattı.
- build-awwwards-quality-sites + build-threejs-scroll-worlds + gsap-skills:gsap-scrolltrigger: hareketli site.

## Tuzaklar
- Bazı skill'ler Codex'e ve belirli projeye bağlı (build-vesperfall-review-assets Vesperfall kataloğu, build-game-changelog/map-editor 'Codex needs'); genel kullanımda uyarlanmalı.
- build-daily-inspiration-sites tarihli *-ui-inspiration paketlerine dayanır; o girdi yoksa uygulanamaz.

## Üyeler
- skill (17): build-awwwards-quality-sites, build-daily-inspiration-sites, build-game-audio-feedback, build-game-camera-controls, build-game-changelog, build-game-inventory, build-game-map-editor, build-game-monster-system, build-hybrid-game-assets, build-interactive-particle-trail, build-isometric-arpg, build-mobile-threejs-games, build-rigged-game-assets, build-threejs-enemy-systems, build-threejs-scroll-worlds, build-vesperfall-review-assets, build-wireframe-scan-reveal
