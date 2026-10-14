# claude-plugins-official — 55 benzersiz kayıt

**Amaç:** Resmi Claude eklenti pazarı: superpowers (TDD, hata ayıklama, plan), plugin-dev, skill-creator, mcp-server-dev, CLAUDE.md yönetimi, Adobe for creativity, Playwright, C# LSP.

**İç yapı:** [plugin] girişleri + eklenti:skill alt skill'leri; büyük gruplar superpowers:*, plugin-dev:*, adobe-for-creativity:* (PDF/Office/foto/video), mcp-server-dev:*; bir [mcp] (Adobe).

## En güçlü parçalar
- `superpowers:systematic-debugging` — Her hata, test başarısızlığı ya da beklenmedik davranışta düzeltme önermeden önce.
- `superpowers:verification-before-completion` — 'Bitti/geçti' demeden, commit/PR öncesi doğrulama komutu koşturmayı zorunlu kılar.
- `superpowers:writing-plans` — Spesifikasyonlu çok adımlı işte koda dokunmadan önce plan.
- `skill-creator:skill-creator` — Skill oluşturma, düzenleme, eval koşturma ve performans ölçümü.
- `plugin-dev:hook-development` — PreToolUse/PostToolUse/Stop hook'u oluşturma ve doğrulama.
- `mcp-server-dev:build-mcp-server` — MCP sunucusu kurma, entegrasyon sarmalama.
- `claude-md-management:claude-md-improver` — Tüm CLAUDE.md dosyalarını tarar, kaliteyi değerlendirip düzeltir.
- `adobe-for-creativity:adobe-anypdf` — Her PDF işi (sıkıştırma, birleştirme, bölme, sayfa işlemleri) için zorunlu.
- `superpowers:dispatching-parallel-agents` — Paylaşımsız 2+ bağımsız görevi paralel ajanlara dağıtmak.
- `claude-code-setup:claude-automation-recommender` — Kod tabanına özel hook, skill, MCP, alt ajan otomasyonu önerir.

## Birlikte kullanım
- superpowers:brainstorming → writing-plans → executing-plans / subagent-driven-development → verification-before-completion → finishing-a-development-branch.
- superpowers:requesting-code-review + receiving-code-review.
- plugin-dev:plugin-structure + skill-development + hook-development + mcp-integration: eklenti iskeleti.
- adobe-for-creativity:adobe-anypdf + adobe-anydocx/anyexcel/anypptx: PDF kaynaklı Office dönüşümleri.

## Tuzaklar
- Çakışan kopyalar: superpowers:brainstorming yerel-diger'deki brainstorming ile, superpowers:test-driven-development test ailesiyle aynı.
- adobe-for-creativity Adobe hesabı/bağlayıcı ister; adobe-paket ile çakışır.
- superpowers:using-superpowers her konuşma başında skill çağrısını zorunlu kılar; bağlam maliyeti.
- plugin-dev:skill-development ile skill-creator ve superpowers:writing-skills kapsamı örtüşür.

## Üyeler
- mcp (1): Adobe for creativity
- plugin (10): adobe-for-creativity, claude-code-setup, claude-md-management, csharp-lsp, frontend-design, mcp-server-dev, playwright, plugin-dev, skill-creator, superpowers
- skill (44): adobe-for-creativity:adobe, adobe-for-creativity:adobe-anydocx, adobe-for-creativity:adobe-anyexcel, adobe-for-creativity:adobe-anypdf, adobe-for-creativity:adobe-anypptx, adobe-for-creativity:adobe-batch-edit-photos, adobe-for-creativity:adobe-create-pdfs-from-data, adobe-for-creativity:adobe-create-social-variations, adobe-for-creativity:adobe-design-from-template, adobe-for-creativity:adobe-design-to-pdf, adobe-for-creativity:adobe-document-review, adobe-for-creativity:adobe-edit-quick-cut, adobe-for-creativity:adobe-fonts, adobe-for-creativity:adobe-resize-photos-and-videos, adobe-for-creativity:adobe-retouch-portraits, claude-code-setup:claude-automation-recommender, claude-md-management:claude-md-improver, frontend-design:frontend-design, mcp-server-dev:build-mcp-app, mcp-server-dev:build-mcp-server, mcp-server-dev:build-mcpb, plugin-dev:agent-development, plugin-dev:command-development, plugin-dev:hook-development, plugin-dev:mcp-integration, plugin-dev:plugin-settings, plugin-dev:plugin-structure, plugin-dev:skill-development, skill-creator:skill-creator, superpowers:brainstorming, superpowers:diagnosing-superpowers, superpowers:dispatching-parallel-agents, superpowers:executing-plans, superpowers:finishing-a-development-branch, superpowers:receiving-code-review, superpowers:requesting-code-review, superpowers:subagent-driven-development, superpowers:systematic-debugging, superpowers:test-driven-development, superpowers:using-git-worktrees …
