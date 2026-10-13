# dn — 24 benzersiz kayıt

**Amaç:** .NET geliştirme ajanları: ASP.NET Core API, Blazor/Razor, EF Core modelleme/migration/seed, DI ve yapılandırma, async denetimi, performans, Native AOT, MSBuild/NuGet, xUnit.

**İç yapı:** Tümü [ajan], dn-<konu>; web (aspnet-core, minimal-api, webapi-endpoint, signalr, blazor, razor), veri (efcore-*), kalite (async, nullable, performans), derleme (msbuild-*, csproj, nuget).

## En güçlü parçalar
- `dn-async-denetci` — Bloklayan çağrı, eksik iptal, fire-and-forget; takılma ve deadlock'ta.
- `dn-efcore-migration` — Veri koruyan yeniden adlandırma, tip değişimi, yeni NOT NULL kolonlu migration.
- `dn-msbuild-hata-cozucu` — Binary log ile MSBuild/dotnet build hatası ve hata kodu açıklaması.
- `dn-dotnet-performans` — Allocation, sıcak yol, GC baskısı; üretimde CPU/bellek artışı.
- `dn-identity-auth` — Identity, cookie, JWT ve policy tabanlı yetkilendirme.
- `dn-di-ve-config` — Doğru yaşam süreleriyle DI ve typed options.
- `dn-native-aot` — Reflection ve serileştirme uyarılarını düzelterek Native AOT/trimming.
- `dn-xunit-test-yazar` — Arrange-act-assert ve açık adlarla xUnit testleri.

## Birlikte kullanım
- dn-efcore-modelleme → dn-efcore-migration → dn-efcore-seed-veri.
- dn-aspnet-core + dn-webapi-endpoint + dn-openapi-dokuman.
- dn-msbuild-hata-cozucu + dotnet-agent-skills dotnet-msbuild:binlog-failure-analysis + binlog MCP.

## Tuzaklar
- dotnet-agent-skills skill'leriyle çakışır (msbuild, nuget, test, webapi).
- dn-blazor-bilesen ile dn-razor-sayfa Blazor bileşen kapsamında örtüşür.
- dn-eski-kod-modernize .NET Framework göçü için; mevcut modern .NET'e uygulanmaz.

## Üyeler
- ajan (24): dn-aspnet-core, dn-async-denetci, dn-blazor-bilesen, dn-csproj-sadelestir, dn-di-ve-config, dn-dotnet-performans, dn-efcore-migration, dn-efcore-modelleme, dn-efcore-seed-veri, dn-eski-kod-modernize, dn-gozlemlenebilirlik, dn-identity-auth, dn-minimal-api-kurucu, dn-msbuild-hata-cozucu, dn-msbuild-hiz, dn-native-aot, dn-nuget-yonetici, dn-nullable-gecis, dn-openapi-dokuman, dn-razor-sayfa, dn-signalr-gercek-zamanli, dn-system-text-json, dn-webapi-endpoint, dn-xunit-test-yazar
