# addy-agent-skills — 25 benzersiz kayıt

**Amaç:** AI kodlama ajanları için speften yayına tüm yazılım geliştirme yaşam döngüsünü kapsayan üretim düzeyi mühendislik skill'leri.

**İç yapı:** agent-skills [plugin] + agent-skills:<konu> skill'leri; gruplar: planlama (spec-driven, planning-and-task-breakdown, idea-refine, interview-me), uygulama (incremental-implementation, api-and-interface-design, frontend-ui-engineering), kalite (code-review, debugging, security, performance), yayın (ci-cd, shipping-and-launch, deprecation); yönlendirici using-agent-skills.

## En güçlü parçalar
- `agent-skills:using-agent-skills` — Oturum başında hangi skill/iş akışının uygulanacağına karar veren yönlendirici.
- `agent-skills:spec-driven-development` — Spesifikasyon yokken yeni proje/özellik için PRD taslağıyla başlatır.
- `agent-skills:debugging-and-error-recovery` — Test/build kırıldığında ya da beklenmedik davranışta sistematik kurtarma.
- `agent-skills:code-review-and-quality` — Her değişiklikte merge öncesi kendi, ajan ya da insan kodunu inceler.
- `agent-skills:incremental-implementation` — Birden çok dosyaya dokunan işte plandan sıradaki görevi adım adım uygular.
- `agent-skills:source-driven-development` — Uygulamadan önce yaklaşımı resmi dokümana karşı doğrular.

## Birlikte kullanım
- agent-skills:idea-refine / interview-me → spec-driven-development → planning-and-task-breakdown → incremental-implementation.
- agent-skills:code-review-and-quality + security-and-hardening + performance-optimization: merge öncesi kalite turu.
- agent-skills:ci-cd-and-automation + shipping-and-launch + observability-and-instrumentation: üretime çıkış.

## Tuzaklar
- agent-skills:security-and-hardening, security ailesindeki security-and-hardening ile aynı açıklamaya sahip; çift kopya.
- Bazı skill'lerin tetikleyicisi çok geniş ('Use when making any code change': git-workflow-and-versioning); gereksiz yüklenebilir.

## Üyeler
- plugin (1): agent-skills
- skill (24): agent-skills:api-and-interface-design, agent-skills:browser-testing-with-devtools, agent-skills:ci-cd-and-automation, agent-skills:code-review-and-quality, agent-skills:code-simplification, agent-skills:constraint-driven-development, agent-skills:context-engineering, agent-skills:debugging-and-error-recovery, agent-skills:deprecation-and-migration, agent-skills:documentation-and-adrs, agent-skills:doubt-driven-development, agent-skills:frontend-ui-engineering, agent-skills:git-workflow-and-versioning, agent-skills:idea-refine, agent-skills:incremental-implementation, agent-skills:interview-me, agent-skills:observability-and-instrumentation, agent-skills:performance-optimization, agent-skills:planning-and-task-breakdown, agent-skills:security-and-hardening, agent-skills:shipping-and-launch, agent-skills:source-driven-development, agent-skills:spec-driven-development, agent-skills:using-agent-skills
