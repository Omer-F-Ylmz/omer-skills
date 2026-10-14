---
name: departman-backend-dotnet
description: ".NET/backend müdürü: ASP.NET Core API, EF, MSBuild, NuGet sırası. C#, .csproj, Web API ya da derleme sorununda oku."
---

# Departman: backend-dotnet — iş sırası

Katalog: `docs/departmanlar/backend-dotnet.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

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
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- dotnet-aspnetcore (4): configuring-opentelemetry-dotnet, convert-blazor-server-to-webapp, dotnet-webapi, minimal-api-file-upload · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-aspnetcore/0.1.1/skills/<ad>/SKILL.md`
- dotnet-nuget (1): convert-to-cpm · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-nuget/0.1.1/skills/<ad>/SKILL.md`
- wpf-rule-mvvm-constraints (1): wpf-rule-mvvm-constraints · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:dn-async-denetci
ajan:dn-blazor-bilesen
ajan:dn-csproj-sadelestir
ajan:dn-di-ve-config: services or settings need structuring
ajan:dn-dotnet-performans
ajan:dn-efcore-migration
ajan:dn-efcore-modelleme
ajan:dn-efcore-seed-veri
ajan:dn-gozlemlenebilirlik: production behavior is invisible
ajan:dn-identity-auth
ajan:dn-minimal-api-kurucu: minimal API uç nokta (+EF Core)
ajan:dn-msbuild-hata-cozucu
ajan:dn-msbuild-hiz
ajan:dn-nuget-yonetici
ajan:dn-nullable-gecis
ajan:dn-openapi-dokuman
ajan:dn-razor-sayfa
ajan:dn-signalr-gercek-zamanli
ajan:dn-webapi-endpoint: adding controllers or minimal API routes
ajan:dn-xunit-test-yazar
ajan:otm-api-entegrasyon
### yalnız Claude Code
aks-known-issues: quota errors, code-only or bare wrappers, generic symptoms
aks-troubleshooting: : packet capture (use aks-network-capture); GPU or model-serving
check-bin-obj-clash: : builds failing with 'Cannot create a file
ck: Claude Codeの永続的なプロジェクト単位のメモリ。セッション開始時にプロジェクトコンテキストを自動読み込み、gitアクティビティでセッションを追跡し、ネイティブメモリに書き込みます。コマンドは決定的なNode.jsスクリプトを実行します — 動作はモデルバージョン間で一貫しています。
error-handling: TypeScript、Python、Goにわたる堅牢なエラー処理のパターン。型付きエラー、エラー境界、リトライ、サーキットブレーカー、ユーザー向けエラーメッセージをカバーします。
gateguard: API、エージェント、およびLLMエンドポイントのアクセス制御と認可パターン。
mcp:binlog: MSBuild binlog çözümleme, derleme hatası
mcp:mslearn: Microsoft Learn resmi .NET/Azure belgesi
nodejs-keccak256: JavaScriptとTypeScriptにおけるEthereumハッシュバグを防ぐ。NodeのSHA3-256はNIST SHA3であり、Ethereum Keccak-256ではなく、セレクター、署名、ストレージスロット、アドレス導出を静かに破壊する。
omni-providers: Manage provider connections, API keys, OAuth flows, and
<!-- dizin:son -->
