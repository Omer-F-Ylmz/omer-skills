# sentry — 35 benzersiz kayıt

**Amaç:** Sentry hata izleme: platforma özel SDK kurulumu (Android'den TanStack Start'a), sorun ayıklama ve düzeltme, uyarı, sürüm takibi, log/OTel enstrümantasyonu, AI çağrısı izleme.

**İç yapı:** Tümü [skill], sentry-<x>; platform SDK skill'leri (sentry-*-sdk), yönlendiriciler (get-started, sdk-setup, instrument), sorun işleri (debug/fix-issues, fix-stack-traces), sentry-paket 34 skill.

## En güçlü parçalar
- `sentry-get-started` — Mevcut kurulumu tanır, yeni projede Sentry'yi ajan üzerinden rehberli kurar.
- `sentry-sdk-setup` — Sentry ekleme/SDK kurma isteğinde platforma yönlendiren genel giriş.
- `sentry-fix-issues` — Sentry hatalarını düzeltme, üretim sorunu ve istisna araştırması.
- `sentry-fix-stack-traces` — Minify ad, bundle yolu, hex adres, 'unknown' gösteren frame'leri düzeltir.
- `sentry-instrumentation-guide` — Log mu span mı metrik mi kararsızlığında.
- `sentry-setup-ai-monitoring` — OpenAI/Anthropic/Vercel AI/LangChain LLM çağrılarını ve ajanları izler.
- `sentry-setup-releases` — Release/deploy takibi; bilinmeyen release ya da şüpheli commit yokken.
- `sentry-sdk-upgrade` — Sentry sürüm göçü, deprecated API ve kırıcı değişiklikler.
- `sentry-dotnet-sdk` — .NET/C#'ta hata izleme, tracing, profiling, logging kurulumu.

## Birlikte kullanım
- sentry-get-started → sentry-<platform>-sdk → sentry-setup-releases → sentry-create-alert.
- sentry-debug-issue → sentry-fix-issues → sentry-fix-stack-traces.
- sentry-otel-exporter-setup + ops ailesinden ops-dagitik-izleme.

## Tuzaklar
- sentry-paket 34 skill'i derler; tekil skill'lerle çakışır.
- sentry-sdk-setup, sentry-instrument ve sentry-get-started giriş noktası olarak örtüşür.
- Sentry hesabı/DSN gerekir; ücret katalog metninde belirtilmemiş.

## Üyeler
- skill (35): sentry-android-sdk, sentry-browser-sdk, sentry-cloudflare-sdk, sentry-cocoa-sdk, sentry-create-alert, sentry-debug-issue, sentry-dotnet-sdk, sentry-elixir-sdk, sentry-fix-issues, sentry-fix-stack-traces, sentry-flutter-sdk, sentry-get-started, sentry-go-sdk, sentry-instrument, sentry-instrument-logging, sentry-instrumentation-guide, sentry-nestjs-sdk, sentry-nextjs-sdk, sentry-node-sdk, sentry-otel-exporter-setup, sentry-paket, sentry-php-sdk, sentry-python-sdk, sentry-react-native-sdk, sentry-react-router-framework-sdk, sentry-react-sdk, sentry-ruby-sdk, sentry-sdk-setup, sentry-sdk-skill-creator, sentry-sdk-upgrade, sentry-setup-ai-monitoring, sentry-setup-releases, sentry-snapshots-cocoa, sentry-svelte-sdk, sentry-tanstack-start-sdk
