---
name: departman-backend-dotnet
description: ".NET/backend müdürü: ASP.NET Core API, EF, MSBuild, NuGet sırası. C#, .csproj, Web API ya da derleme sorununda oku."
---

# Departman: backend-dotnet — iş sırası

Katalog: `docs/departmanlar/backend-dotnet.md`.

## Adımlar
1. **Doküman** — API/sürüm sorusu önce `mslearn` (CLI önce: `dotnet`, `gh`).
2. **Tasarım** — uç nokta ve sözleşme: `api-and-interface-design`, ardından `dotnet-webapi`.
3. **Yapım** — minimal API/controller `dotnet-webapi`; CRUD iskeleti `create-datadriven-aspnetcore`; veri erişimi → `departman-veri-db`.
4. **Gözlemlenebilirlik** — `configuring-opentelemetry-dotnet`.
5. **Derleme** — hata `binlog-generation` → `binlog-failure-analysis`; yavaşlık `build-perf-baseline` → `build-perf-diagnostics`; paket sürümleri `convert-to-cpm`.
6. **Test** — `departman-test-qa` (`run-tests`, `rtk dotnet test`).

## Kapılar
- `dotnet test/restore/format` her zaman `rtk dotnet …` ile; `--nologo` yok (DOTNET_NOLOGO).
- Proje dosyası değişikliğinde `msbuild-antipatterns` kontrolü.

## Çakışma
- Derleme sorunu: binlog skill'leri > genel hata ayıklama.
