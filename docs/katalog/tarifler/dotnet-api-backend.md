# .NET API / backend — birleşim tarifi
Ne zaman: ASP.NET Core Web API, EF Core veri katmanı ve xUnit testli backend işi.

## Fazlar
1. Keşif: `departman-backend-dotnet` — ASP.NET Core API, EF, MSBuild, NuGet sırası · birlikte: `graphify` kod tabanı ilişkilerini sorgular.
2. Plan: `superpowers:writing-plans` — çok adımlı işi koda dokunmadan planlar · birlikte: `dotnet-webapi` doğru HTTP semantiği, OpenAPI ve hata yönetimini belirler.
3. Veri modeli: `dn-efcore-modelleme` — entity, ilişki ve Fluent API · birlikte: `dn-efcore-migration` veri koruyan yeniden adlandırma ve NOT NULL sütun göçü.
4. Uygulama: `dn-aspnet-core` — minimal API ya da controller, middleware sırası, problem details · birlikte: `superpowers:test-driven-development` önce test; kimlik gerekiyorsa `dn-identity-auth`.
5. Test: `dotnet-test:run-tests` — doğru test komutu ve filtre · birlikte: `dn-xunit-test-yazar` arrange-act-assert testleri; zaman/dosya bağımlılığı için `testability-obstacle`.
6. Performans: `dotnet-data:optimizing-ef-core-queries` — yavaş EF sorgusu · birlikte: `db-efcore-sql-gecis` üretilen SQL'i inceler.
7. Teslim: `departman-surec-git-yayin` — commit, PR, CI sırası.

## İnceleme ajanları
- `pr-review-toolkit`: yorum, test, hata yönetimi, tip tasarımı ve sadeleştirme ajanları.
- `ponytail-review`: aşırı mühendislik avı.
- `engineering-backend-architect`: ölçeklenebilir tasarım ikinci görüşü.

## Güvenlik ve kalite kapıları
- Testler yeşil (`dotnet` CLI); yeni davranışın testi var.
- `semgrep` ve `gitleaks` temiz; bağımlılık: `sec-bagimlilik-acik`.
- Kişisel veri varsa KVKK: `sec-kvkk-gdpr-kontrol`.
- Hata izleme: `sentry-dotnet-sdk`.

## Tartışma konseyi
- Karar: minimal API mi controller mı, şema göç stratejisi.
- `ecc:council` — varsayılan Claude personaları: mimar, bakımcı, güvenlik.

## Jeton bütçesi
- Keşif: küçük (~6k, tahmini); geniş dosya taraması `okuyucu` alt ajanına.
- Plan: orta (~10k). Veri + uygulama: büyük (~40k). Test: orta (~15k); log okuma alt ajana. Performans: orta (~10k). Teslim: küçük (~3k). Hepsi tahmini.

## Kaçınılacaklar
- Aynı skill'in iki kopyasını çağırmak (`dotnet-webapi` ile `dotnet-aspnetcore:dotnet-webapi`); birini seç.
- Veri kaybettiren migration'ı incelemeden uygulamak.
- Node odaklı `backend-patterns` ile .NET kararı vermek.

## Aday (kurulu değil)
yok
