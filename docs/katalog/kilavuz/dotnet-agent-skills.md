# dotnet-agent-skills — 53 benzersiz kayıt

**Amaç:** Microsoft'un .NET ajan skill'leri: MSBuild derleme teşhisi/performansı, .NET test yazma-çalıştırma-kalite analizi, ASP.NET Core, EF Core veri erişimi, NuGet yönetimi.

**İç yapı:** Beş eklenti (dotnet-msbuild, dotnet-test, dotnet-aspnetcore, dotnet-data, dotnet-nuget) ve önekli alt skill'leri (dotnet-test:run-tests vb.) + binlog MCP sunucusu.

## En güçlü parçalar
- `dotnet-test:run-tests` — .NET testlerini koşmadan ya da test komutu/bayrağı vermeden önce her zaman kullanılır.
- `dotnet-msbuild:binlog-failure-analysis` — Konsoldan anlaşılmayan derleme hatalarını MSBuild binlog'dan teşhis eder.
- `dotnet-test:code-testing-agent` — Mevcut koda birim testi yazma/ekleme isteklerinde zorunlu giriş.
- `dotnet-test:test-anti-patterns` — Hiçbir şey doğrulamayan testleri bulup önem sıralı teşhis raporu üretir.
- `dotnet-test:testability-obstacle` — DateTime/Task.Delay/File/Environment gerektiren deterministik testler için en küçük üretim dikişi.
- `dotnet-data:optimizing-ef-core-queries` — Yavaş EF Core/DbContext sorgu ya da veri erişim yolunu hızlandırır.
- `dotnet-msbuild:build-perf-baseline` — Yavaş derlemede önce performans tabanı kurar; build-perf-diagnostics sonra gelir.
- `dotnet-test:platform-detection` — Test platformu, çerçeve, komut modu ve SDK-style/klasik proje tespiti.
- `dotnet-aspnetcore:dotnet-webapi` — Doğru HTTP semantiği, OpenAPI metadata ve hata yanıtıyla Web API uç noktası.
- `dotnet-nuget:convert-to-cpm` — Proje/çözümü Directory.Packages.props ile Central Package Management'a çevirir.

## Birlikte kullanım
- dotnet-msbuild:binlog-generation → binlog MCP → dotnet-msbuild:binlog-failure-analysis: binlog üret, analiz et.
- dotnet-test:platform-detection → dotnet-test:filter-syntax → dotnet-test:run-tests: platform tespiti sonrası filtreli koşu.
- dotnet-test:detect-static-dependencies → dotnet-test:migrate-static-to-wrapper: statik bağımlılığı bulup sarmalayıcıya taşımak.
- dotnet-test:coverage-analysis + dotnet-test:crap-score + dotnet-test:test-gap-analysis: kapsam, risk ve mutasyon boşluğu.

## Tuzaklar
- Sıra kuralları var: build-perf-diagnostics yalnız baseline sonrası; filter-syntax yalnız platform tespitinden sonra.
- generate-testability-wrappers hedef zaten IFileSystem/TimeProvider gibi soyutlama kullanıyorsa kullanılmaz.
- test-gap-analysis yalnız sözde-mutasyon analizi yapar; test-smell-detection akademik/atıflı inceleme içindir.
- convert-blazor-server-to-webapp yalnız .NET 8 öncesi Blazor Server göçü; minimal-api-file-upload .NET 8+.

## Üyeler
- mcp (1): binlog
- plugin (5): dotnet-aspnetcore, dotnet-data, dotnet-msbuild, dotnet-nuget, dotnet-test
- skill (47): dotnet-aspnetcore:configuring-opentelemetry-dotnet, dotnet-aspnetcore:convert-blazor-server-to-webapp, dotnet-aspnetcore:dotnet-webapi, dotnet-aspnetcore:minimal-api-file-upload, dotnet-data:create-datadriven-aspnetcore, dotnet-data:optimizing-ef-core-queries, dotnet-msbuild:binlog-failure-analysis, dotnet-msbuild:binlog-generation, dotnet-msbuild:build-parallelism, dotnet-msbuild:build-perf-baseline, dotnet-msbuild:build-perf-diagnostics, dotnet-msbuild:check-bin-obj-clash, dotnet-msbuild:copy-to-output-directory, dotnet-msbuild:directory-build-organization, dotnet-msbuild:eval-performance, dotnet-msbuild:extension-points, dotnet-msbuild:including-generated-files, dotnet-msbuild:incremental-build, dotnet-msbuild:item-management, dotnet-msbuild:msbuild-antipatterns, dotnet-msbuild:msbuild-modernization, dotnet-msbuild:property-patterns, dotnet-msbuild:resolve-project-references, dotnet-msbuild:target-authoring, dotnet-nuget:convert-to-cpm, dotnet-test:assertion-quality, dotnet-test:code-testing-agent, dotnet-test:code-testing-extensions, dotnet-test:coverage-analysis, dotnet-test:crap-score, dotnet-test:detect-static-dependencies, dotnet-test:filter-syntax, dotnet-test:find-untested-sources, dotnet-test:generate-testability-wrappers, dotnet-test:grade-tests, dotnet-test:migrate-static-to-wrapper, dotnet-test:mtp-hot-reload, dotnet-test:platform-detection, dotnet-test:run-tests, dotnet-test:scaffold-dotnet-test-project …
