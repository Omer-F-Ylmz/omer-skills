# phoenix-security — 32 benzersiz kayıt

**Amaç:** Phoenix Security'nin güvenlik öncelikli eklentileri: tehdit istihbaratı arama, SAST kural üretimi, AppSec incelemesi, 10 rollü PRD/spec hattı, hazırlık incelemeleri, dokümantasyon.

**İç yapı:** Altı eklenti (cti-search, docs-research, prd-pipeline, readiness-reviews, sast-rules, security-review) ve önekli skill'ler; prd-pipeline 01–10 numaralı rol zinciri ve orchestrator.

## En güçlü parçalar
- `phoenix-readiness-reviews:plan-readiness-review` — PRD/spec/RFC'nin icat gerektirmeden uygulanabilir olup olmadığını build öncesi sorgular.
- `phoenix-readiness-reviews:production-readiness-review` — 'Bitti mi, yayınlanabilir mi' sorusunda son inceleme kapısı.
- `phoenix-security-review:security-reviewer` — Yeni uç nokta, auth/RBAC, render, dış HTTP değişikliklerinde 8 noktalı çok dilli inceleme.
- `phoenix-security-review:tm-quick-security-assessment` — Dal/worktree diff'inde hızlı merge öncesi güvenlik duruşu kontrolü.
- `phoenix-sast-rules:opengrep-rule-generator` — 30+ dil için opengrep/semgrep pattern ve taint kuralı üretir.
- `phoenix-prd-pipeline:prd-generator` — Düz dil özellik tanımından tehdit modelli tam PRD yazar.
- `phoenix-prd-pipeline:phoenix-orchestrator` — 01–10 rollerini zincirleyip ham bağlamdan yayına hazır PRD çıkarır.
- `phoenix-docs-research:project-documenter` — Kademeli modlarla üretim seviyesi proje dokümantasyon paketi.
- `phoenix-cti-search:cti-domain-research` — Küratörlü güvenlik alan adlarında CVE, zararlı yazılım, ihlal raporu arama.

## Birlikte kullanım
- prd-generator → plan-readiness-review → (uygulama) → production-readiness-review.
- security-reviewer + opengrep-rule-generator: bulguyu tekrar eden kurala çevirmek.
- threat-modeling + tm-security-review: ajan/LLM/MCP kod tabanlarında derin inceleme.
- cli ailesinden semgrep ile opengrep kuralları birlikte koşulabilir.

## Tuzaklar
- prd-pipeline rolleri Phoenix Security'ye özgü başarısızlık modları/kanıt yöntemleri için yazılmış; genel projeye uyarlama gerekir.
- phoenix-research-pipeline Brave API ister; notebooklm Google NotebookLM hesabı gerektirir.
- 0day-scanner ve security-assessment yerel-diger'deki 0day-scanner ile çakışan kopya.
- Yalnız yetkili kod tabanlarında kullanım; saldırı senaryosu kapsamı katalog metninde sınırlanmamış.

## Üyeler
- plugin (6): phoenix-cti-search, phoenix-docs-research, phoenix-prd-pipeline, phoenix-readiness-reviews, phoenix-sast-rules, phoenix-security-review
- skill (26): phoenix-cti-search:cti-domain-research, phoenix-docs-research:notebooklm, phoenix-docs-research:phoenix-research-pipeline, phoenix-docs-research:project-documenter, phoenix-prd-pipeline:phoenix-ambiguity-hunter, phoenix-prd-pipeline:phoenix-batch-planner, phoenix-prd-pipeline:phoenix-constraint-distiller, phoenix-prd-pipeline:phoenix-context-curator, phoenix-prd-pipeline:phoenix-contract-architect, phoenix-prd-pipeline:phoenix-final-gate, phoenix-prd-pipeline:phoenix-orchestrator, phoenix-prd-pipeline:phoenix-pipeline-navigator, phoenix-prd-pipeline:phoenix-requirements-engineer, phoenix-prd-pipeline:phoenix-scope-cutter, phoenix-prd-pipeline:phoenix-security-engineer, phoenix-prd-pipeline:phoenix-verification-matrix, phoenix-prd-pipeline:prd-generator, phoenix-readiness-reviews:plan-readiness-review, phoenix-readiness-reviews:production-readiness-review, phoenix-sast-rules:opengrep-rule-generator, phoenix-security-review:0day-scanner, phoenix-security-review:security-assessment, phoenix-security-review:security-reviewer, phoenix-security-review:threat-modeling, phoenix-security-review:tm-quick-security-assessment, phoenix-security-review:tm-security-review
