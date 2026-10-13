# hyperframes — 25 benzersiz kayıt

**Amaç:** HeyGen HyperFrames: HTML yazıp video render etme; kompozisyon, GSAP animasyonu, altyazı, seslendirme, ürün tanıtım/açıklayıcı/PR videoları ve slayt gösterileri.

**İç yapı:** İki eşdeğer eklenti (core-skills, hyperframes) + hyperframes:<x> skill'leri: zorunlu giriş hyperframes:hyperframes, çekirdek/cli/registry/studio araçları ve format skill'leri (explainer, launch, slideshow).

## En güçlü parçalar
- `hyperframes:hyperframes` — Video/animasyon yapma, düzenleme, render isteklerinde önce okunacak zorunlu giriş.
- `hyperframes:hyperframes-core` — Kompozisyon yapısı, data-* zamanlama nitelikleri, track, alt kompozisyon, değişken.
- `hyperframes:hyperframes-cli` — init, add, lint, check, snapshot, compare, preview geliştirme döngüsü.
- `hyperframes:hyperframes-registry` — Adlandırılmış bileşeni elle kurmadan önce registry bloklarını arar ve bağlar.
- `hyperframes:product-launch-video` — Ürün tanıtma/lansman; ticari URL için varsayılan.
- `hyperframes:pr-to-video` — GitHub PR'ını kod değişikliği açıklayıcı videoya çevirir.
- `hyperframes:faceless-explainer` — Konu açıklayıcı, kavram, nasıl yapılır, liste videoları.
- `hyperframes:talking-head-recut` — Konuşan kafa/röportaj/podcast videosuna zamanlı grafik overlay kartları.
- `hyperframes:media-use` — BGM, SFX, görsel, ikon, logo, ses, LUT'u projeye çözer.

## Birlikte kullanım
- hyperframes:hyperframes → hyperframes-registry → hyperframes-core → hyperframes-cli (lint/check).
- hyperframes-animation + hyperframes-keyframes: hareket kuralları ve kamera/zoom.
- hyperframes:remotion-to-hyperframes ile remotion ailesinden göç.
- vid ailesinin vid-hyperframes-kompozisyon ajanı aynı işi ajan olarak yapar.

## Tuzaklar
- Çakışan kopyalar: core-skills ile hyperframes eklentisi aynı açıklama; hyperframes-paket ve hyperframes-studio [skill] ayrıca var.
- remotion-to-hyperframes yalnız açık port/dönüştürme isteğinde kullanılmalı.
- faceless-explainer web sitesinden video için değil; o iş product-launch-video.
- HeyGen hesabı/ücret gereksinimi katalog metninde belirtilmemiş.

## Üyeler
- plugin (2): core-skills, hyperframes
- skill (23): hyperframes-paket, hyperframes-studio, hyperframes:embedded-captions, hyperframes:faceless-explainer, hyperframes:figma, hyperframes:general-video, hyperframes:hyperframes, hyperframes:hyperframes-animation, hyperframes:hyperframes-audio, hyperframes:hyperframes-cli, hyperframes:hyperframes-core, hyperframes:hyperframes-creative, hyperframes:hyperframes-keyframes, hyperframes:hyperframes-registry, hyperframes:hyperframes-studio, hyperframes:media-use, hyperframes:motion-graphics, hyperframes:music-to-video, hyperframes:pr-to-video, hyperframes:product-launch-video, hyperframes:remotion-to-hyperframes, hyperframes:slideshow, hyperframes:talking-head-recut
