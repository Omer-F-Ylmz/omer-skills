---
iddia: caveman proxy Claude Max (OAuth) oturumunu, caveman-mcp ajanın kalıcı MCP kaydında yoksa bayt bayt geçirir; o çağrıya özel --mcp-config ve CAVEMAN_SUBSCRIPTION_COMPRESS=true sıkıştırmayı açmaz.
kaynak: caveman-proxy 1.3.4 açılış çıktısı ("subscription and OAuth logins stay byte-identical pass-through … run `caveman mcp install <agent>`"), caveman stats --json, github.com/JuliusBrussee/caveman docs/technical/architecture.md "Recovery paths"
guven: yüksek
dogrulama: docs/denemeler/caveman-proxy-sonuc.md (20b-devam: 4 görev × 2 kol × 2, $6.26)
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: token, caveman, proxy, olcum
---
caveman proxy Max/OAuth oturumunu caveman-mcp kalıcı kayıtlı değilse sıkıştırmaz.

- stats: 32 istek, before = after = 2028741 token, saved 0 (auth_mode subscription).
- ölçüm (sonnet, sıcak $): headroom 219880 girdi / $0.354 / başarı 1.00 · caveman-mcp (8788, compress, abonelik sıkıştırma açık, o çağrıya özel mcp) 351549 / $0.429 / 0.88; mcp çağrısı 0 → karar yok.
- Headroom ile zincirlenemez; caveman kolu Headroom sıkıştırmasını kaybeder, girdi artar.
- açmanın tek yolu `caveman mcp install claude` (global MCP kaydı): omer-kurallar ve 20b-devam TAVİZ gereği Ömer onayı olmadan yapılmaz.
