# omni — 23 benzersiz kayıt

**Amaç:** OmniRoute LLM yönlendirme ağ geçidinin yönetimi: kimlik doğrulama, API anahtarları, sağlayıcılar, routing combo'ları, bütçe, önbellek, sıkıştırma, log, yedek ve MCP/A2A erişimi.

**İç yapı:** Tümü [skill], ad kalıbı omni-<alan>; gruplar: erişim (auth, api-keys, budget), yönlendirme (combos-routing, providers, models, proxies, resilience), bağlam (compression, context-rtk, cache), işletim (settings, db-backups, sync-cloud, tunnels, version-manager, usage-logs, webhooks), arayüz (inference, mcp, agents-a2a, cli-tools, github-skills).

## En güçlü parçalar
- `omni-auth` — Başlangıç noktası: Bearer token ve oturum ile isteklerin kimliğini doğrular.
- `omni-combos-routing` — 14 stratejiyle (priority, weighted, round-robin, Auto-combo) routing combo'ları ve fallback kurar.
- `omni-inference` — Çekirdek OpenAI uyumlu uç noktalar: chat, embedding, görsel, ses, moderasyon.
- `omni-resilience` — Sağlayıcı sağlığı, circuit-breaker durumu, p50/p95/p99 gecikme ve bütçe uyarılarını izler.
- `omni-budget` — Anahtar başına ya da global harcama limiti, token kotası ve rate-limit politikası.
- `omni-usage-logs` — Sağlayıcı, model, zaman, durum ve maliyete göre çağrı logu ve kullanım analizi.

## Birlikte kullanım
- omni-auth → omni-providers → omni-combos-routing → omni-inference: kurulumdan çağrıya.
- omni-api-keys + omni-budget + omni-usage-logs: anahtar başına harcama kontrolü ve izleme.
- omni-compression + omni-context-rtk + omni-cache: bağlam ve maliyet azaltma.

## Tuzaklar
- omni-tunnels OmniRoute'u internete açar (ngrok, Cloudflare Tunnel); anahtar kapsamı ve bütçe sınırı kurulmadan açılmamalı.
- omni-db-backups geri yükleme yapar ve SQLite yaşam döngüsünü yönetir; restore öncesi güncel yedek alınmalı.

## Üyeler
- skill (23): omni-agents-a2a, omni-api-keys, omni-auth, omni-budget, omni-cache, omni-cli-tools, omni-combos-routing, omni-compression, omni-context-rtk, omni-db-backups, omni-github-skills, omni-inference, omni-mcp, omni-models, omni-providers, omni-proxies, omni-resilience, omni-settings, omni-sync-cloud, omni-tunnels, omni-usage-logs, omni-version-manager, omni-webhooks
