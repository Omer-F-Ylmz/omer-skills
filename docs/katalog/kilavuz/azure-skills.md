# azure-skills — 51 benzersiz kayıt

**Amaç:** Microsoft Azure eklentileri ve MCP'leri: kaynak yönetimi, dağıtım, AKS sorun giderme, maliyet, uyum, Kusto analizi, Foundry ve Entra kimlik.

**İç yapı:** İki [mcp] (azure, azure-resource-manager-mcp) + [plugin]'ler (azure, aks-skills, azure-cost, azure-kusto-graph-skills, azure-local-skills, foundry-iq-skills); skill'ler eklenti:ad biçiminde, çoğu 'WHEN:' tetikleyicili.

## En güçlü parçalar
- `azure:azure-diagnostics` — AppLens, Azure Monitor ve kaynak sağlığıyla üretim sorunlarını güvenli triyajla ayıklar.
- `aks-skills:aks-troubleshooting` — Canlı AKS olaylarında salt-okur, kanıt öncelikli inceleme.
- `azure:azure-validate` — Dağıtım öncesi yapılandırma, Bicep/Terraform altyapı ve RBAC derin kontrolü.
- `azure:azure-prepare` — azd tabanlı proje için azure.yaml, altyapı ve Dockerfile üretir.
- `azure:azure-app-onboard` — İş/uygulama fikrinden maliyet tahminli çalışan Azure dağıtımına uçtan uca orkestratör.
- `azure-cost:cost-analysis` — Gerçek Azure harcaması, fatura değişimi, AKS/AI maliyet dökümü.
- `azure:azure-compliance` — azqr ile uyum/güvenlik denetimi ve Key Vault son kullanma kontrolü.
- `azure:azure-resource-lookup` — Abonelik ve kaynak grupları genelinde kaynak listeleme/bulma.

## Birlikte kullanım
- azure:azure-app-onboard-prereq → azure:azure-prepare → azure:azure-validate → azure:azure-deploy: dağıtım hattı.
- azure-cost:cost-analysis + azure-cost:cost-optimization + azure-cost:cost-governance: harca, kıs, bütçele.
- aks-skills:aks-troubleshooting önce; aks-skills:aks-network-capture yalnız salt-okur teşhis sonrası açık paket yakalama niyetiyle.
- azure:azure-kusto + azure-kusto-graph-skills:azure-kusto-irql: KQL telemetri ve güvenlik avı.

## Tuzaklar
- azure:azure-deploy yalnız hazırlanmış (.azure/deployment-plan.md ve altyapısı olan) uygulamalar içindir.
- aks-skills:aks-known-issues yalnız tam katalog imzası ve tüm niteleyicileri varsa kullanılır.
- azure-local-skills:azure-local-multi-rack standart 1-16 düğümlü Azure Local için değil.

## Üyeler
- mcp (2): azure, azure-resource-manager-mcp
- plugin (6): aks-skills, azure, azure-cost, azure-kusto-graph-skills, azure-local-skills, foundry-iq-skills
- skill (43): aks-skills:aks-gpu-inference, aks-skills:aks-known-issues, aks-skills:aks-network-capture, aks-skills:aks-troubleshooting, aks-skills:azure-search-nav, azure-cost:cost-analysis, azure-cost:cost-estimation, azure-cost:cost-governance, azure-cost:cost-optimization, azure-kusto-graph-skills:azure-kusto-graph, azure-kusto-graph-skills:azure-kusto-irql, azure-kusto-graph-skills:azure-kusto-irql-graph, azure-local-skills:azure-local, azure-local-skills:azure-local-multi-rack, azure:airunway-aks-setup, azure:appinsights-instrumentation, azure:azure-ai, azure:azure-aigateway, azure:azure-app-onboard, azure:azure-app-onboard-prereq, azure:azure-cloud-migrate, azure:azure-compliance, azure:azure-compute, azure:azure-deploy, azure:azure-diagnostics, azure:azure-enterprise-infra-planner, azure:azure-kubernetes, azure:azure-kusto, azure:azure-messaging, azure:azure-prepare, azure:azure-quotas, azure:azure-reliability, azure:azure-resource-lookup, azure:azure-resource-visualizer, azure:azure-storage, azure:azure-upgrade, azure:azure-validate, azure:discover-azure-skills, azure:entra-agent-id, azure:entra-app-registration …
