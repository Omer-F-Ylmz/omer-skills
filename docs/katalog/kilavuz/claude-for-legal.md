# claude-for-legal — 26 benzersiz kayıt

**Amaç:** Hukuk ekipleri için iki eklenti: ticari sözleşme incelemesi (NDA, SaaS, tedarikçi, yenileme) ve gizlilik uyumu (DPA, PIA, DSAR, düzenleme boşluk analizi); hukuk servislerine MCP bağlayıcıları.

**İç yapı:** commercial-legal [plugin] + commercial-legal:<iş> skill'leri, privacy-legal [plugin] + privacy-legal:<iş> skill'leri; 7 [mcp] bağlayıcı (Definely, DocuSign, Google Drive, iManage, Ironclad, Slack, TopCounsel).

## En güçlü parçalar
- `commercial-legal:nda-review` — Gelen NDA'ları GREEN/YELLOW/RED olarak hızlı triyaj eder; avukat zamanı yalnız gerekene harcanır.
- `commercial-legal:vendor-agreement-review` — Gelen tedarikçi sözleşmesini takım playbook'una göre inceler.
- `privacy-legal:dpa-review` — Müşteri DPA'sını (veri işleme eki) inceleyip değerlendirir.
- `privacy-legal:dsar-response` — Erişim/silme/taşıma/düzeltme talebi geldiğinde DSAR yanıtı hazırlar.
- `privacy-legal:use-case-triage` — Bir özelliğin PIA gerektirip gerektirmediğini gizlilik açısından triyaj eder.
- `commercial-legal:cold-start-interview` — İlk kullanımda pratik profilini yazar; diğer skill'lerin playbook temeli.

## Birlikte kullanım
- commercial-legal:cold-start-interview → nda-review / saas-msa-review / vendor-agreement-review → escalation-flagger → stakeholder-summary.
- privacy-legal:use-case-triage → pia-generation; yeni düzenlemede reg-gap-analysis + policy-monitor.
- commercial-legal:renewal-tracker + Ironclad ve Slack MCP: yenileme takibi ve bildirim.

## Tuzaklar
- MCP bağlayıcıları dış hukuk servislerine (Definely, DocuSign, iManage, Ironclad) bağlanır; her biri dar amaçlıdır (ör. DocuSign analiz değil yalnız e-imza).
- Skill'ler takım playbook'una ve ~/.claude/plugins/config altındaki profile dayanır; cold-start yapılmadan çıktı genel kalır.

## Üyeler
- mcp (7): Definely, DocuSign, Google Drive, Ironclad, Slack, TopCounsel, iManage
- plugin (2): commercial-legal, privacy-legal
- skill (17): commercial-legal:amendment-history, commercial-legal:cold-start-interview, commercial-legal:customize, commercial-legal:escalation-flagger, commercial-legal:matter-workspace, commercial-legal:nda-review, commercial-legal:renewal-tracker, commercial-legal:review-proposals, commercial-legal:saas-msa-review, commercial-legal:stakeholder-summary, commercial-legal:vendor-agreement-review, privacy-legal:dpa-review, privacy-legal:dsar-response, privacy-legal:pia-generation, privacy-legal:policy-monitor, privacy-legal:reg-gap-analysis, privacy-legal:use-case-triage
