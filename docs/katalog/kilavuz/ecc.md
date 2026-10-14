# ecc — 305 benzersiz kayıt

**Amaç:** Mühendislik ekipleri için harness-yerli ECC eklentisi: 68 ajan, 293 skill, 94 eski komut şimi, hook ve kurallar; ajan mühendisliği, kod kalitesi, dil kalıpları, maliyet ve döngü yönetimi.

**İç yapı:** ecc [plugin] + ecc:<konu> skill'leri; gruplar: ajan altyapısı (agent-*, autonomous-*, council), kalite/test, dil/çerçeve kalıpları (cpp, django, dart), içerik/marka, iş alanı (gümrük, navlun), ECC bakımı.

## En güçlü parçalar
- `ecc:agent-sort` — Tüm paketi yüklemek yerine ECC'yi projenin gerçekten ihtiyaç duyduğuna indirger.
- `ecc:context-budget` — Bağlam hızla doluyorsa onu tüketen ajan, skill, MCP, kuralları budar.
- `ecc:agent-introspection-debugging` — Ajan çalışması başarısızsa yeniden deneme yerine tekrarlanabilir teşhis.
- `ecc:blueprint` — Birden çok PR/oturuma yayılan özellik, refactor, yol haritası planı; tek PR için değil.
- `ecc:delivery-gate` — Kalite kontrolleri ve öğrenme kaydı bitmeden 'bitti' denmesini mekanik olarak engeller.
- `ecc:database-migrations` — Büyük tabloya kolon/indeks ekleme, rollback planı ile şema/veri göçü.
- `ecc:cost-aware-llm-pipeline` — LLM harcamasını düşürme, model katmanları ve bütçelerle yönlendirme.
- `ecc:council` — Birden çok geçerli yol varsa seçmeden önce yapılandırılmış itiraz.
- `ecc:click-path-audit` — Sistematik hata ayıklama bir şey bulmadı ama kullanıcı bozuk buton bildiriyorsa.
- `ecc:config-gc` — Şişmiş .claude, çok fazla skill, kurulum denetimi istendiğinde temizlik.

## Birlikte kullanım
- ecc:configure-ecc → ecc:agent-sort → ecc:context-budget: kur, buda, bağlamı ölç.
- ecc:council + ecc:council-multi-model: yüksek sonuçlu belirsiz kararda ayrı model görüşü.
- ecc:continuous-agent-loop + ecc:delivery-gate + ecc:agent-self-evaluation.
- ecc:benchmark + ecc:canary-watch + ecc:browser-qa: yayın öncesi/sonrası doğrulama.

## Tuzaklar
- ecc:continuous-learning kullanımdan kaldırıldı; continuous-learning-v2 kullanılmalı.
- Paket çok büyük (293 skill); tamamını yüklemek bağlamı tüketir, agent-sort ile kırpılmalı.
- Çakışan kopyalar: ecc:backend-patterns ve ecc:clickhouse-io yerel-diger'de; ecc:deep-research daymade-skills'te.
- ecc:agent-payment-x402 ajana harcama yaptırır; bütçe ve harcama kontrolü şart.

## Üyeler
- plugin (1): ecc
- skill (304): ecc-ag-homelab-paket, ecc-ajan-paket, ecc-backend-paket, ecc-devops-guvenlik-paket, ecc-diller-paket, ecc-frontend-paket, ecc-icerik-pazarlama-paket, ecc-is-operasyon-paket, ecc-jvm-paket, ecc-ml-bilim-saglik-paket, ecc-orkestrasyon-paket, ecc:accessibility, ecc:agent-architecture-audit, ecc:agent-eval, ecc:agent-harness-construction, ecc:agent-introspection-debugging, ecc:agent-payment-x402, ecc:agent-self-evaluation, ecc:agent-sort, ecc:agentic-engineering, ecc:agentic-os, ecc:ai-first-engineering, ecc:ai-regression-testing, ecc:android-clean-architecture, ecc:angular-developer, ecc:api-connector-builder, ecc:api-design, ecc:architecture-decision-records, ecc:article-writing, ecc:automation-audit-ops, ecc:autonomous-agent-harness, ecc:autonomous-loops, ecc:backend-patterns, ecc:benchmark, ecc:benchmark-methodology, ecc:benchmark-optimization-loop, ecc:blender-motion-state-inspection, ecc:blueprint, ecc:brand-discovery, ecc:brand-voice …
