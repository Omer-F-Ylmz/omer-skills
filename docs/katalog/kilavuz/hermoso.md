# hermoso — 7 benzersiz kayıt

**Amaç:** Kodlama ajanı içinde AI pazarlama ajanı: kazanan reklamları araştırma, markaya uygun görsel/video reklam ve ürün çekimi üretme, kampanya yayınlama.

**İç yapı:** hermoso [plugin] + hermoso:hermoso-<iş> skill'leri (ad-from-brand, generate, marketing, product-photoshoot, research); ayrıca 5 skill'lik hermoso-paket (Hermoso MCP ve CLI iş akışları).

## En güçlü parçalar
- `hermoso:hermoso-research` — Rakipleri ve nişte işe yarayan reklamları bulup markanın reklamlarını çeker.
- `hermoso:hermoso-ad-from-brand` — Alan adı/marka verildiğinde o şirket için reklam ya da lansman reklamı kurar.
- `hermoso:hermoso-generate` — Görsel ya da video reklam ve ürün çekimi üretir.
- `hermoso:hermoso-marketing` — Haftalık reklamlar, kampanya başlatma ve her yerde yayınlama.
- `hermoso:hermoso-product-photoshoot` — Ürün çekimi, yaşam tarzı görselleri ve hero banner.

## Birlikte kullanım
- hermoso:hermoso-research → hermoso:hermoso-ad-from-brand → hermoso:hermoso-generate → hermoso:hermoso-marketing.
- hermoso:hermoso-product-photoshoot + hermoso:hermoso-generate: ürün görseli ve reklam varyantları.
- hermoso-paket MCP/CLI iş akışlarında tekil skill'lerin yerine kullanılır.

## Tuzaklar
- hermoso-paket ile hermoso:* skill'leri örtüşür; ikisi birden yüklenmemeli.
- hermoso:hermoso-marketing 'post this everywhere' ile yayın yapar; yayın öncesi onay alınmalı.

## Üyeler
- plugin (1): hermoso
- skill (6): hermoso-paket, hermoso:hermoso-ad-from-brand, hermoso:hermoso-generate, hermoso:hermoso-marketing, hermoso:hermoso-product-photoshoot, hermoso:hermoso-research
