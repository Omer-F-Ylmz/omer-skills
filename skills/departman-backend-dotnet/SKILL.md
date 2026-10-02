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

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `dotnet-aspnetcore:configuring-opentelemetry-dotnet` · Configure OpenTelemetry distributed tracing, metrics, and logging in ASP.NET Core using the .NET OpenTelemetry · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-aspnetcore/0.1.1/skills/configuring-opentelemetry-dotnet/SKILL.md`
- `dotnet-aspnetcore:convert-blazor-server-to-webapp` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-aspnetcore/0.1.1/skills/convert-blazor-server-to-webapp/SKILL.md`
- `dotnet-aspnetcore:dotnet-webapi` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-aspnetcore/0.1.1/skills/dotnet-webapi/SKILL.md`
- `dotnet-aspnetcore:minimal-api-file-upload` · File upload endpoints in ASP.NET minimal APIs (.NET 8+) · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-aspnetcore/0.1.1/skills/minimal-api-file-upload/SKILL.md`
- `dotnet-nuget:convert-to-cpm` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-nuget/0.1.1/skills/convert-to-cpm/SKILL.md`
- `wpf-rule-mvvm-constraints` · WPF MVVM layer-separation rules: no System.Windows in ViewModels, BCL-only types, CommunityToolkit.Mvvm base c · `C:/Users/pc/.claude/skills/wpf-rule-mvvm-constraints/SKILL.md`
<!-- profil-disi:son -->
