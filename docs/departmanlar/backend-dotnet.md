# Departman: backend-dotnet

> .NET/C#/ASP.NET Core/MSBuild/NuGet ve sunucu tarafı API geliştirme.

Müdür: `departman-backend-dotnet`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| dotnet | cli | - | - | Tasarım |
| csharp-lsp | plugin | - | - | - |
| dotnet-aspnetcore | plugin | ASP.NET Core web development skills including middleware, endpoints, real-time communicat… | - | - |
| dotnet-data | plugin | Skills for .NET data access and Entity Framework related tasks. | - | - |
| dotnet-msbuild | plugin | Comprehensive MSBuild and .NET build skills: failure diagnosis, performance optimization,… | - | - |
| dotnet-nuget | plugin | NuGet and .NET package management skills: dependency management and modernization. | - | - |
| agent-skills:api-and-interface-design | skill | Guides stable API and interface design. | Use when designing APIs, module boundaries, or any public interface | Yapım |
| agent-skills:observability-and-instrumentation | skill | Instruments code so production behavior is visible and diagnosable. | Use when adding logging, metrics, tracing, or alerting | - |
| anthropic-skills:departman-backend-dotnet | skill | .NET/backend müdürü: ASP.NET Core API, EF, MSBuild, NuGet sırası. | - | - |
| dotnet-aspnetcore:configuring-opentelemetry-dotnet | skill | Configure OpenTelemetry distributed tracing, metrics, and logging in ASP.NET Core using t… | Use when adding observability, setting up OTLP exporters, creating custom metrics/sp | Derleme |
| dotnet-aspnetcore:convert-blazor-server-to-webapp | skill | Guides conversion of a pre-.NET 8 Blazor Server app into a .NET 8+ Blazor Web App. | USE FOR: migrating apps that use AddServerSideBlazor and MapBlazorHub to the AddRazorComp… | - |
| dotnet-aspnetcore:dotnet-webapi | skill | Guides creation and modification of ASP.NET Core Web API endpoints with correct HTTP sema… | USE FOR: adding new API endpoints (controllers or minimal APIs), w | Yapım |
| dotnet-aspnetcore:minimal-api-file-upload | skill | File upload endpoints in ASP.NET minimal APIs (.NET 8+) | - | - |
| dotnet-data:create-datadriven-aspnetcore | skill | Generate or scaffold ASP.NET Core code — Razor Pages, Blazor components, MVC controllers,… | Use when | Gözlemlenebilirlik |
| dotnet-msbuild:binlog-failure-analysis | skill | Analyze MSBuild binary logs to diagnose build failures. | USE FOR: build errors that are unclear from console output, diagnosing cascading failures… | Test |
| dotnet-msbuild:binlog-generation | skill | Generate MSBuild binary logs (binlogs) for build diagnostics and analysis. | USE FOR: adding /bl:{} to any dotnet build, test, pack, publish, or restore command to ca… | Test |
| dotnet-msbuild:build-parallelism | skill | Diagnose and fix under-parallelized MSBuild builds. | USE WHEN a multi-project solution build is slower than expected, doesn't speed up when yo… | - |
| dotnet-msbuild:build-perf-baseline | skill | Establish build performance baselines and apply systematic optimization techniques. | USE FOR: diagnosing slow builds, establishing before/after measurements (cold, warm, no-o… | Test |
| dotnet-msbuild:build-perf-diagnostics | skill | Diagnose MSBuild build performance bottlenecks using binary log analysis. | USE FOR: identifying why builds are slow by analyzing binlog performance summaries, detec… | Test |
| dotnet-msbuild:check-bin-obj-clash | skill | Detects MSBuild projects with conflicting OutputPath or IntermediateOutputPath. | USE FOR: builds failing with 'Cannot create a file when that file already exists', 'The p… | - |
| dotnet-msbuild:copy-to-output-directory | skill | Choosing an MSBuild CopyToOutputDirectory / CopyToPublishDirectory mode: Never, PreserveN… | USE FOR: removing the | - |
| dotnet-msbuild:directory-build-organization | skill | Guide for organizing MSBuild infrastructure with Directory.Build.props, Directory.Build.t… | USE FOR: structuring multi-project repos, centralizi | - |
| dotnet-msbuild:eval-performance | skill | Guide for diagnosing and improving MSBuild project evaluation performance. | USE FOR: builds slow before any compilation starts, high evaluation time in binlog analys… | - |
| dotnet-msbuild:extension-points | skill | Guide for MSBuild extensibility: CustomBefore/CustomAfter hooks, wildcard imports with al… | - | - |
| dotnet-msbuild:including-generated-files | skill | Fix MSBuild targets that generate files during the build but those files are missing from… | USE FOR: generated source files not compiling (CS0246 for a type that should exist), cu | - |
| dotnet-msbuild:incremental-build | skill | Guide for optimizing MSBuild incremental builds. | USE FOR: builds slower than expected on subsequent runs, 'nothing changed but it rebuilds… | - |
| dotnet-msbuild:item-management | skill | Patterns for managing MSBuild item groups: Include/Remove/Update semantics, item metadata… | USE FOR: diag | - |
| dotnet-msbuild:msbuild-antipatterns | skill | Detect and fix MSBuild anti-patterns in project and build files. | USE WHEN asked to review, audit, lint, clean up, or code-review a | - |
| dotnet-msbuild:msbuild-modernization | skill | Guide for modernizing and migrating MSBuild project files to SDK-style format. | USE FOR: converting legacy | - |
| dotnet-msbuild:property-patterns | skill | MSBuild property definition patterns: conditional defaults, composition/concatenation, pa… | USE FOR: diagnosing and | - |
| dotnet-msbuild:resolve-project-references | skill | Guide for interpreting ResolveProjectReferences time in MSBuild performance summaries. | Activate when ResolveProjectReferences appears as the most expensive target and developer… | - |
| dotnet-msbuild:target-authoring | skill | Canonical patterns for writing custom MSBuild targets. | USE FOR: diagnosing and fixing custom target authoring anti-patterns; broken SDK target c… | - |
| dotnet-nuget:convert-to-cpm | skill | Convert .NET projects and solutions (.sln, .slnx) to NuGet Central Package Management (CP… | USE FOR: converting to CPM, centralizing or aligning NuGet package versions | Test |
| everything-claude-code:backend-patterns | skill | Backend architecture patterns, API design, database optimization, and server-side best pr… | - | - |

## Elle
