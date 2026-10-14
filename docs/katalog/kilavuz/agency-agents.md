# agency-agents — 82 benzersiz kayıt

**Amaç:** Rol adlı uzman ajan kadrosu: mühendislik (backend, veri, mobil, gömülü), güvenlik, uyum, tasarım/UX, içerik, platform/operasyon ve bölgeye özel (Çin ağı, Feishu, WeChat) uzmanlar.

**İç yapı:** Tümü [ajan], ad İngilizce rol unvanı (ör. Backend Architect); gruplar: mimari, veri/ML, güvenlik, mobil/masaüstü, tasarım/UX, operasyon, niş platformlar; okuyucu salt-okur alt ajan.

## En güçlü parçalar
- `Minimal Change Engineer` — Yalnız isteneni düzelten, kapsam kaymasını reddeden minimum diff.
- `Code Reviewer` — Doğruluk, bakım, güvenlik odaklı uygulanabilir inceleme geri bildirimi.
- `Software Architect` — Sistem tasarımı, DDD, mimari kalıplar ve teknik karar.
- `Security Architect` — Tehdit modelleme, güven sınırı analizi, secure-by-design mimari.
- `RAG Pipeline Engineer` — Chunking, hibrit arama, re-ranking ve eval güdümlü üretim RAG.
- `Database Optimizer` — Şema tasarımı, sorgu optimizasyonu ve indeksleme.
- `Codebase Onboarding Engineer` — Kaynak kodu okuyarak yeni mühendise yabancı kod tabanını hızla anlatır.
- `Incident Response Commander` — Üretim olay yönetimi, yapılandırılmış müdahale, post-mortem.
- `okuyucu` — Salt-okur analiz alt ajanı: transcript karşılaştırma, resmi doküman araştırması; dosya yazmaz.
- `UI Finish-Gate Reviewer` — Jenerik, birbirinin yerine geçebilir UI'ı yayından önce yakalar.

## Birlikte kullanım
- Software Architect → Backend Architect → Code Reviewer → Minimal Change Engineer.
- Security Architect + Senior SecOps Engineer + AI-Generated Code Security Auditor.
- Database Optimizer + Database Reliability Engineer: performans ve yüksek erişilebilirlik.
- okuyucu alt ajanı diğer ajanların araştırma/karşılaştırma işini salt-okur yapar.

## Tuzaklar
- Çakışan roller: Incident Responder ile Incident Response Commander, Security Architect ile Cloud Security Architect.
- Penetration Tester yalnız yetkili testler içindir.
- Bölgeye özel ajanlar (China Network Engineer, GaussDB, Feishu, WeChat) Çin platformlarına bağlı.
- USWDS Developer açıklaması kesik ('Expert U.S.'); kapsamı katalog metninde belirtilmemiş.

## Üyeler
- ajan (82): AI Data Remediation Engineer, AI Engineer, AI-Generated Code Security Auditor, API Platform Engineer, ATS Validator Architect, Autonomous Optimization Architect, Backend Architect, Blockchain Security Auditor, Brand Guardian, CMS Developer, China Network Engineer, Cloud Security Architect, Code Reviewer, Codebase Onboarding Engineer, Compliance Auditor, Data Engineer, Data Visualization Engineer, Database Optimizer, Database Reliability Engineer, Desktop App Engineer, DevOps Automator, Developer Tooling Engineer, Drupal Performance Engineer, Drupal Shopping Cart Engineer, Email Intelligence Engineer, Embedded Firmware Engineer, Feishu Integration Developer, Filament Optimization Specialist, FinOps Engineer, Frontend Developer, GaussDB Expert Engineer, Git Workflow Master, IT Service Manager, Identity & Access Engineer, Image Prompt Engineer, Incident Responder, Incident Response Commander, Inclusive Visuals Specialist, IoT Fleet Engineer, Knowledge Graph Engineer …
