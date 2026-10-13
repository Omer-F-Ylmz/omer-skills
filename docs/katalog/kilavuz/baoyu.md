# baoyu — 16 benzersiz kayıt

**Amaç:** Baoyu içerik üretim skill'leri: makale illüstrasyonu, kapak, infografik, çizgi roman, diyagram, slayt, görsel üretimi/sıkıştırma, Markdown biçimleme/HTML, çeviri, WeChat/Xiaohongshu içerikleri.

**İç yapı:** Tümü [skill], baoyu-<iş>; görsel (image-gen, cover, comic, infographic, xhs-images, article-illustrator), belge (format-markdown, markdown-to-html, slide-deck), dönüşüm (translate, url-to-markdown, youtube-transcript).

## En güçlü parçalar
- `baoyu-diagram` — Mimari, akış, sekans gibi her türde profesyonel koyu temalı SVG diyagram.
- `baoyu-infographic` — Infografik, görsel özet, yüksek yoğunluklu bilgi görseli.
- `baoyu-article-illustrator` — Makaleye görsel ekleme/üretme.
- `baoyu-compress-image` — Görsel sıkıştırma, webp dönüşümü, dosya boyutu azaltma.
- `baoyu-url-to-markdown` — Web sayfasını Markdown olarak kaydetme.
- `baoyu-youtube-transcript` — YouTube transkripti, altyazı ve kapak indirme.
- `baoyu-translate` — Makale çevirisi, Çinceye çeviri.

## Birlikte kullanım
- baoyu-url-to-markdown → baoyu-translate → baoyu-format-markdown → baoyu-markdown-to-html.
- baoyu-article-illustrator + baoyu-cover-image + baoyu-compress-image.

## Tuzaklar
- Tetikleyicilerin çoğu Çince ve Çin platformları (WeChat, 小红书) odaklı.
- baoyu-paket 14 skill'i derler; tekil skill'lerle çakışır.
- baoyu-image-gen hangi görüntü modelini/anahtarını kullandığı katalog metninde belirtilmemiş.

## Üyeler
- skill (16): baoyu-article-illustrator, baoyu-comic, baoyu-compress-image, baoyu-cover-image, baoyu-diagram, baoyu-format-markdown, baoyu-image-gen, baoyu-infographic, baoyu-markdown-to-html, baoyu-paket, baoyu-slide-deck, baoyu-translate, baoyu-url-to-markdown, baoyu-wechat-summary, baoyu-xhs-images, baoyu-youtube-transcript
