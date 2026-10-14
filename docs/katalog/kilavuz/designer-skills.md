# designer-skills — 300 benzersiz kayıt

**Amaç:** Tasarımcılar için geniş eklenti paketi: erişilebilirlik, araştırma, UI/etkileşim tasarımı, tasarım sistemi, AI ürün tasarımı, ekip liderliği ve program yönetimi.

**İç yapı:** Konu başına [plugin] (ör. design-systems, prototyping-testing, visual-critique) + eklenti:skill alt skill'leri; açıklamalar 'Use when … For X use Y' kalıbıyla kardeş skill'e yönlendirir.

## En güçlü parçalar
- `design-systems:accessibility-audit` — Elde olan tasarım ya da yapıyı şimdi değerlendiren ürün çapında erişilebilirlik denetimi.
- `cognitive-accessibility:cognitive-load-assessment` — Çok adımlı süreç, karmaşık form, yoğun pano gibi ekranlarda bilişsel yükü ölçer.
- `design-systems:component-spec` — Kütüphane bileşenini tanımlamak için spesifikasyon.
- `ui-design:color-system` — Rengi sıfırdan tanımlama ya da yeniden kurma.
- `prototyping-testing:a-b-test-design` — Ölçeklenebilir, nicel ölçülebilir değişiklikler için A/B test tasarımı.
- `design-research:affinity-diagram` — Birden çok oturum ya da kaynaktan araştırma bulgularını sentezler.
- `prototyping-testing:concept-selection` — Birden çok yön canlıyken birini seçtirir.
- `ux-strategy:competitive-analysis` — Rakiplerin gerçekte ne yaptığını çıkarır.

## Birlikte kullanım
- design-research:affinity-diagram → prototyping-testing:concept-selection → prototyping-testing:a-b-test-design: sentez, seçim, doğrulama.
- design-systems:accessibility-audit + prototyping-testing:accessibility-test-plan: kendi değerlendirmen ile gerçek yardımcı teknoloji kullanıcılarıyla test ayrımı.
- ui-design:color-system + visual-critique:critique-color: rengi kur, sonra tek ekranda eleştir.
- interaction-design:animation-principles + design-systems motion-system: tek animasyonun hissi ve ürün çapı süre/easing token'ları.

## Tuzaklar
- Aile 300 üyeli; girdide yalnız ilk ~80 satır görünür, kalan üyeler bu özette yok.
- Kardeş skill'ler örtüşür (ör. accessibility-audit / accessibility-test-plan, color-system / critique-color); açıklamadaki 'For X use Y' yönlendirmesine uyulmalı.
- Liderlik/ekip eklentileri (people-management, team-building, org-influence) kod işine katkı vermez; yüklemek bağlamı şişirir.

## Üyeler
- plugin (33): accessibility-decisions, accessible-content, adaptive-interfaces, ai-alignment-reasoning, cognitive-accessibility, cross-functional-alignment, delivery-execution, design-agent-orchestration, design-ops, design-research, design-strategy, design-systems, designer-toolkit, evaluation, inclusive-interaction, inclusive-personas, interaction-design, leadership-craft, measurement-ops, model-interaction-design, operating-cadence, org-influence, people-management, process-design, program-planning, prompt-architecture, prototyping-testing, stakeholder-comms, system-behavior-shaping, team-building, ui-design, ux-strategy, visual-critique
- skill (267): accessibility-decisions:accessibility-debt-tracking, accessibility-decisions:accessibility-testing-strategy, accessibility-decisions:compliance-mapping, accessibility-decisions:decision-documentation, accessibility-decisions:document, accessibility-decisions:stakeholder-communication, accessibility-decisions:tradeoff-analysis, accessible-content:alt-text-design, accessible-content:form-labelling, accessible-content:heading-structure, accessible-content:link-text-design, accessible-content:multimedia-accessibility, accessible-content:readable-content, accessible-content:rewrite, accessible-content:structure, accessible-content:table-accessibility, adaptive-interfaces:colour-independence, adaptive-interfaces:flexible-typography, adaptive-interfaces:information-density, adaptive-interfaces:preference-audit, adaptive-interfaces:responsive-accessibility, adaptive-interfaces:responsive-review, adaptive-interfaces:simplified-views, adaptive-interfaces:specify, adaptive-interfaces:user-preference-respect, ai-alignment-reasoning:bias-detection-design, ai-alignment-reasoning:consent-and-agency, ai-alignment-reasoning:escalation-design, ai-alignment-reasoning:guardrail-design, ai-alignment-reasoning:harm-anticipation, ai-alignment-reasoning:transparency-patterns, ai-alignment-reasoning:trust-calibration, ai-alignment-reasoning:value-specification, cognitive-accessibility:assess-load, cognitive-accessibility:cognitive-load-assessment, cognitive-accessibility:contextual-help-design, cognitive-accessibility:error-prevention-recovery, cognitive-accessibility:focus-attention-design, cognitive-accessibility:memory-load-reduction, cognitive-accessibility:plain-language-design …
