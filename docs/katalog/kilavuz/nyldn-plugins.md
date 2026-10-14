# nyldn-plugins — 61 benzersiz kayıt

**Amaç:** Claude Octopus (octo) çoklu-AI iş akışı eklentisi ve GPT Image 2 / Gemini ile görsel üreten img eklentisi.

**İç yapı:** İki [plugin] (img, octo); octo:flow-* Double Diamond aşamaları (discover/define/develop/deliver), octo:octopus-* geniş işler, octo:skill-* tekil teknikler, octo:sys-configure kurulum.

## En güçlü parçalar
- `octo:skill-debug` — Tekrarlanabilir belirtiyi sınırlı geri bildirim döngüsü ve orijinal senaryo doğrulamasıyla ayıklar.
- `octo:skill-tdd` — Gözlenen kırmızı, minimum yeşil ve ölçülü test birleştirmeyle davranış değişikliği.
- `octo:skill-verify` — Önemsiz olmayan değişikliği commit/ship öncesi uçtan uca doğrular.
- `octo:skill-pressure-test` — Planı ya da kararı tek tek sorularla dayanıncaya kadar sorgular.
- `octo:skill-code-review` — Satır içi PR yorumlu çoklu-AI kod incelemesi.
- `octo:skill-work-slicing` — Planı her biri engelini bildiren dikey dilimlere böler.
- `octo:skill-cost-projections` — Aşama ortalamalarından kalan iş maliyetini öngörür, bütçe tavanı aşımında uyarır.
- `octo:skill-resume` — Bağlam sıfırlanması/compaction sonrası önceki oturumdan devam.

## Birlikte kullanım
- octo:flow-discover → octo:flow-define → octo:flow-develop → octo:flow-deliver: Double Diamond akışı.
- octo:skill-intent-contract + octo:skill-work-slicing + octo:skill-writing-plans: kapsam kaymasına karşı plan.
- octo:skill-council / octo:skill-debate + octo:skill-cost-projections: kritik kararda bütçe tavanlı çoklu model.
- octo:skill-staged-review + octo:skill-review-response: spesifikasyon ve kalite incelemesi, ardından geri bildirimi işleme.

## Tuzaklar
- flow-* ve council/debate harici sağlayıcı çağırır; maliyet ve bütçe tavanı izlenmeli.
- octo:flow-develop basit kod düzenlemesi için değil; küçük işte octo:octopus-quick.
- img eklentisinde sağlayıcı yedeği yok (No provider fallback).

## Üyeler
- plugin (2): img, octo
- skill (59): img:img, octo:flow-define, octo:flow-deliver, octo:flow-develop, octo:flow-discover, octo:flow-parallel, octo:flow-spec, octo:octopus-architecture, octo:octopus-quick, octo:octopus-research, octo:octopus-security-audit, octo:octopus-ui-ux-design, octo:skill-agent-topology, octo:skill-audit, octo:skill-authoring, octo:skill-code-review, octo:skill-content-pipeline, octo:skill-context-detection, octo:skill-copilot-provider, octo:skill-cost-projections, octo:skill-council, octo:skill-coverage-audit, octo:skill-debate, octo:skill-debug, octo:skill-decision-support, octo:skill-deck, octo:skill-design-lineage, octo:skill-doc-delivery, octo:skill-doc-sync, octo:skill-doctor, octo:skill-extract, octo:skill-factory, octo:skill-finish-branch, octo:skill-intake, octo:skill-intent-contract, octo:skill-issues, octo:skill-iterative-loop, octo:skill-knowledge-work, octo:skill-meta-prompt, octo:skill-native-escalation-routing …
