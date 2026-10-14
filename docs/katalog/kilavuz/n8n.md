# n8n — 14 benzersiz kayıt

**Amaç:** n8n iş akışı skill'leri: AI ajan düğümleri, Code (JS/Python), ifade sözdizimi, düğüm yapılandırması, doğrulama, hata yönetimi, alt akışlar, n8n-mcp araçları, kendi sunucunda barındırma.

**İç yapı:** Tümü [skill], n8n-<konu>; kod (code-javascript, code-python, code-tool, expression-syntax), yapı (workflow-patterns, subworkflows, node-configuration), kalite (validation, error-handling), MCP/altyapı.

## En güçlü parçalar
- `n8n-workflow-patterns` — Yeni akış, akış yapısı ve mimari kalıp seçimi.
- `n8n-mcp-tools-expert` — n8n-mcp ile düğüm arama, yapılandırma doğrulama, şablon, akış yönetimi.
- `n8n-error-handling` — Webhook/API, zamanlanmış ya da gözetimsiz akışlarda sessiz hatayı önler.
- `n8n-expression-syntax` — {{}} sözdizimi, $json/$node değişkenleri ve ifade hataları.
- `n8n-code-javascript` — $input/$json/$node ve this.helpers ile JS Code düğümü.
- `n8n-validation-expert` — Doğrulama hata/uyarıları, yanlış pozitifler, operatör yapısı.
- `n8n-agents` — @n8n/n8n-nodes-langchain AI Agent, LLM chain, sınıflandırıcı düğümleri.
- `n8n-subworkflows` — Paylaşılan mantık ya da ~10 düğümü aşan akışları alt akışa ayırma.

## Birlikte kullanım
- n8n-workflow-patterns → n8n-node-configuration → n8n-validation-expert → n8n-error-handling.
- n8n-agents + n8n-code-tool: AI ajanına LLM'in çağırdığı kod aracı.
- otm ailesinin n8n ajanları ve pinecone-n8n ile.

## Tuzaklar
- n8n-code-python yalnız açıkça Python istendiğinde; varsayılan JS.
- n8n-multi-instance yalnız n8n_instances aracı varken anlamlı.
- n8n-mcp-tools-expert n8n-mcp sunucusu ister; n8n sunucusu değildir.

## Üyeler
- skill (14): n8n-agents, n8n-binary-and-data, n8n-code-javascript, n8n-code-python, n8n-code-tool, n8n-error-handling, n8n-expression-syntax, n8n-mcp-tools-expert, n8n-multi-instance, n8n-node-configuration, n8n-self-hosting, n8n-subworkflows, n8n-validation-expert, n8n-workflow-patterns
