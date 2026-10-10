"""ecc'nin claude.ai'ye tek tek yüklenmiş 254 skill'ini kategori paketlerine çevirir.
Girdi: yuklu.txt (yüklenen zip yolları), ecc.tsv (ad \t açıklama). Çıktı: /tmp/claude-0/ecc-paket/*.zip
"""
import re, sys, zipfile, pathlib, io

KOK = pathlib.Path("/mnt/user-data/uploads/y12")
CIK = pathlib.Path("/tmp/claude-0/ecc-paket"); CIK.mkdir(exist_ok=True)
tsv = dict(l.rstrip("\n").split("\t", 1) for l in open("/tmp/claude-0/ecc/ecc.tsv", encoding="utf-8"))
yollar = {pathlib.Path(p).stem: p for p in open("/tmp/claude-0/yuklu.txt").read().split() if "/ecc-" in p}

P = {
 "ecc-ajan-paket": ("Ajan/LLM mühendisliği: ajan tasarımı, değerlendirme, hata ayıklama, bağlam/jeton/maliyet bütçesi, MCP, prompt, güvenlik", """
 agent-architecture-audit agent-eval agent-harness-construction agent-introspection-debugging agent-self-evaluation
 agent-sort agentic-engineering agentic-os ai-first-engineering cc-devfleet continuous-agent-loop context-budget
 cost-aware-llm-pipeline cost-tracking gan-style-harness hookify-rules iterative-retrieval loop-design-check
 mcp-server-patterns enterprise-agent-ops nasiko-control-plane openclaw-persona-forge operator-approval-loop
 prompt-optimizer regex-vs-llm-structured-text safety-guard token-budget-advisor taste-application taste-distillation
 search-first documentation-lookup exa-search hermes-imports agent-payment-x402"""),
 "ecc-orkestrasyon-paket": ("Planlama ve iş akışı: orch-* hattı, plan, council, ekip ajanları, RFC, karar defteri, kod turu, onboarding, benchmark", """
 orch-add-feature orch-build-mvp orch-change-feature orch-fix-defect orch-pipeline orch-refine-code plan-canvas
 plan-orchestrate council council-multi-model dev-team team-agent-orchestration team-builder dynamic-workflow-mode
 ecc-recipes intent-driven-development parallel-execution-optimizer ralphinho-rfc-pipeline recursive-decision-ledger
 santa-method blueprint contract-first product-capability product-lens project-flow-ops code-tour codebase-onboarding
 living-docs-governance inherit-legacy-style benchmark-methodology benchmark-optimization-loop
 data-throughput-accelerator latency-critical-systems"""),
 "ecc-jvm-paket": ("JVM/Android: Java, Kotlin, Spring Boot, Quarkus, JPA, Ktor, Exposed, Compose, Android mimarisi", """
 java-coding-standards jpa-patterns kotlin-coroutines-flows kotlin-exposed-patterns kotlin-ktor-patterns kotlin-patterns
 kotlin-testing springboot-patterns springboot-security springboot-tdd springboot-verification quarkus-patterns
 quarkus-security quarkus-tdd quarkus-verification android-clean-architecture compose-multiplatform-patterns
 tinystruct-patterns"""),
 "ecc-diller-paket": ("Diller: Python, Go, Rust, C++, C#, F#, .NET, Perl, Swift/SwiftUI, Dart/Flutter, PyTorch; desen ve test", """
 cpp-coding-standards cpp-testing csharp-testing fsharp-testing dotnet-patterns golang-patterns golang-testing
 perl-patterns perl-security perl-testing python-patterns python-testing pytorch-patterns rust-patterns rust-testing
 swift-actor-persistence swift-concurrency-6-2 swift-protocol-di-testing swiftui-patterns dart-flutter-patterns
 foundation-models-on-device liquid-glass-design ios-icon-gen generating-python-installer"""),
 "ecc-backend-paket": ("Backend ve veri: Django, Laravel, Rails, FastAPI, NestJS, API tasarımı, Postgres/MySQL/Redis/Prisma, göç, hata yönetimi", """
 django-celery django-patterns django-security django-tdd django-verification laravel-patterns laravel-plugin-discovery
 laravel-security laravel-tdd laravel-verification rails-patterns fastapi-patterns nestjs-patterns nodejs-keccak256
 api-design api-connector-builder database-migrations mysql-patterns postgres-patterns prisma-patterns redis-patterns
 content-hash-cache-pattern error-handling hexagonal-architecture x-api"""),
 "ecc-frontend-paket": ("Frontend: React/Next/Vue/Nuxt/Angular/Vite/RN, motion, erişilebilirlik, tasarım yönü, slaytlar, dashboard, tarayıcı QA/E2E", """
 accessibility angular-developer frontend-a11y frontend-design-direction frontend-slides make-interfaces-feel-better
 motion-advanced motion-foundations motion-patterns nextjs-turbopack nuxt4-patterns react-patterns react-performance
 react-testing react-native-patterns ui-demo ui-to-vue vite-patterns vue-patterns i18n-sync dashboard-builder
 browser-qa click-path-audit windows-desktop-e2e"""),
 "ecc-devops-guvenlik-paket": ("DevOps ve güvenlik: Docker, Kubernetes, dağıtım, git/GitHub, kod sağlığı, repo/güvenlik taraması, terminal, DeFi/EVM güvenliği", """
 deployment-patterns docker-patterns kubernetes-patterns flox-environments git-workflow github-ops canary-watch
 production-audit repo-scan security-bounty-hunter security-scan plankton-code-quality codehealth-mcp
 opensource-pipeline uncloud terminal-opener terminal-ops workspace-surface-audit automation-audit-ops
 defi-amm-security evm-token-decimals llm-trading-agent-security"""),
 "ecc-ag-homelab-paket": ("Ağ ve homelab: Cisco IOS, BGP, arayüz sağlığı, yapılandırma doğrulama, Netmiko SSH, Pi-hole, VLAN, WireGuard", """
 cisco-ios-patterns homelab-network-readiness homelab-network-setup homelab-pihole-dns homelab-vlan-segmentation
 homelab-wireguard-vpn netmiko-ssh-automation network-bgp-diagnostics network-config-validation network-interface-health"""),
 "ecc-icerik-pazarlama-paket": ("İçerik ve pazarlama: makale, marka, SEO, sosyal yayın, video (Remotion/Manim), fal.ai, pazar/rakip analizi, yatırımcı", """
 article-writing blender-motion-state-inspection brand-discovery brand-voice content-engine crosspost fal-ai-media
 manim-video remotion-video-creation seo social-graph-ranker social-publisher video-editing videodb
 connections-optimizer lead-intelligence marketing-campaign market-research competitive-platform-analysis
 competitive-report-structure investor-materials investor-outreach"""),
 "ecc-is-operasyon-paket": ("İş operasyonları: e-posta, mesaj, Google Workspace, Jira, fatura, sözleşme, e-imza, lojistik, tedarik, üretim", """
 carrier-relationship-management counterparty-channel-discipline customer-billing-ops customs-trade-compliance
 email-ops energy-procurement esign-field-placement finance-billing-ops google-workspace-ops inventory-demand-planning
 jira-integration logistics-exception-management mailtrap-email-integration master-agreement-generator messages-ops
 nutrient-document-processing production-scheduling quality-nonconformance research-ops returns-reverse-logistics
 unified-notifications-ops visa-doc-translate data-scraper-agent"""),
 "ecc-ml-bilim-saglik-paket": ("ML, bilim, sağlık: MLE, recsys, ITO, PubMed/USPTO, literatür, EMR/CDSS/HIPAA, tahmin piyasası", """
 healthcare-cdss-patterns healthcare-emr-patterns healthcare-eval-harness healthcare-phi-compliance hipaa-compliance
 ito-baskets ito-compute ito-inference ito-training ml-adoption-playbook mle-workflow recsys-pipeline-architect
 scientific-db-pubmed-database scientific-db-uspto-database scientific-pkg-gget scientific-thinking-literature-review
 scientific-thinking-scholar-evaluation prediction-market-oracle-research prediction-market-risk-review"""),
}

atanan = {}
for pk, (_, adlar) in P.items():
    for a in adlar.split():
        assert a not in atanan, f"çift: {a}"
        atanan[a] = pk
hepsi = {k[4:] for k in tsv}
eksik, fazla = hepsi - set(atanan), set(atanan) - hepsi
assert not eksik and not fazla, (sorted(eksik), sorted(fazla))

for pk, (konu, adlar) in P.items():
    adlar = adlar.split()
    acik = f"{len(adlar)} skill'lik paket ({konu}). Konu bu alandaysa önce bu dizini aç, uygun alt skill'in SKILL.md'sini oku ve uygula."
    if len(acik) > 200:
        acik = f"{len(adlar)} skill'lik paket ({konu}). İlgili alt skill'in SKILL.md'sini oku ve uygula."
    assert len(acik) <= 200, (pk, len(acik))
    satir = []
    with zipfile.ZipFile(CIK / f"{pk}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for a in adlar:
            src = zipfile.ZipFile(KOK / yollar["ecc-" + a])
            for n in src.namelist():
                if n.endswith("/"):
                    continue
                ic = n.split("/", 1)[1]
                z.writestr(f"{pk}/skills/{a}/{ic}", src.read(n))
            ne = tsv["ecc-" + a].strip().strip('"').replace("|", "/")
            satir.append(f"| {a} | {ne} | `skills/{a}/SKILL.md` |")
        md = (f"---\nname: {pk}\ndescription: \"{acik}\"\n---\n\n# {pk}\n\n"
              f"Bu paket everything-claude-code'un {len(adlar)} skill'ini tek girişte toplar (claude.ai 1000 skill sınırı ve jeton tasarrufu). "
              "Kullanım: aşağıdan işe uyan alt skill'i seç, dosyasını oku, talimatını uygula. Birden çok alt skill gerekebilir.\n\n"
              "| skill | ne zaman | dosya |\n|---|---|---|\n" + "\n".join(satir) + "\n")
        z.writestr(f"{pk}/SKILL.md", md)
    print(pk, len(adlar), len(acik), (CIK / f"{pk}.zip").stat().st_size)
print("toplam", len(atanan))
