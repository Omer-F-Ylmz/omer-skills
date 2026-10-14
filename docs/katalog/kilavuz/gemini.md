# gemini — 4 benzersiz kayıt

**Amaç:** Google Gemini API ile kod geliştirme: metin/çok modlu üretim, Live API ile gerçek zamanlı akış ve Omni Flash ile video üretimi/düzenleme.

**İç yapı:** Ad kalıbı gemini-<konu>: gemini-api-dev, gemini-live-api-dev, gemini-omni-flash-api ve bunları toplayan 3 skill'lik gemini-api-paket.

## En güçlü parçalar
- `gemini-api-dev` — Gemini API'yi metin üretimi, çok turlu sohbet ve çok modlu anlama için çağıran kod.
- `gemini-live-api-dev` — Gemini Live API ile gerçek zamanlı çift yönlü akış uygulamaları ve eskiden göç.
- `gemini-omni-flash-api` — Üretken video düzenleme, metinden video ve görsel referanslı video üretimi.

## Birlikte kullanım
- gemini-api-dev + gemini-live-api-dev: aynı uygulamada istek-yanıt ve canlı akış.
- gemini-omni-flash-api + remotion ailesi: üretilen videoyu kodla kurgulamak.
- gemini-api-paket tekil skill'ler yerine tek giriş noktası olarak.

## Tuzaklar
- gemini-api-paket tekil gemini-* skill'leriyle örtüşür; ikisi birden yüklenmemeli.
- Video üretimi (gemini-omni-flash-api) API çağrısı gerektirir; çağrı sayısı sınırlanmalı.

## Üyeler
- skill (4): gemini-api-dev, gemini-api-paket, gemini-live-api-dev, gemini-omni-flash-api
