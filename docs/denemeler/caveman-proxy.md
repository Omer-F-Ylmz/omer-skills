# Deneme: caveman-proxy

video ? · 15 · 20b-devam: caveman-mcp kolu (Max/OAuth: mcp + CAVEMAN_SUBSCRIPTION_COMPRESS olmadan sıkıştırma yapısal olarak kapalı)

## Hipotez
caveman proxy (compress kipi, abonelik sıkıştırması açık) + o çağrıya özel caveman-mcp, okuma görevlerinde girdi tokenını bugünkü Headroom bağlanmasından belirgin azaltır, doğruluk düşmez.

## Metrik
girdi token (provider-reported) · sıcak koşu $ (karar) · soğuk $ (bilgi) · görev başarısı · Jev kalite · caveman-mcp araç çağrısı (transkript; 0 → karar yok).

## Bütçe
`video dene caveman-proxy --gorevler okuma --tavan 16 --istek-tavan 20`: 4 görev × 2 kol × 2 koşu = 16 claude -p, Jev ≤20.

## Proxy
Deneme başında: `CAVEMAN_MODE=compress CAVEMAN_SUBSCRIPTION_COMPRESS=true CAVEMAN_LISTEN=127.0.0.1:8788 video koru -- caveman start` (arka planda; yalnız süreç env'i, caveman.yaml yazılmaz). Bitince süreç numarasıyla durdurulur, 8788 boş mu bakılır. Zincir yok: caveman kolu yukarı akışa doğrudan gider (Headroom'suz).

## Geri alma
Proxy süreci durdurulur; global MCP/settings değişmez (mcp yalnız `--mcp-config docs/denemeler/caveman-mcp.json`).

## Başarı eşiği
girdi token −%15 (Headroom'a göre) ve kalite kapısı (18).

## Kollar
- headroom: temel · env ANTHROPIC_BASE_URL=http://127.0.0.1:6767
- caveman-mcp: env ANTHROPIC_BASE_URL=http://127.0.0.1:8788 · mcp docs/denemeler/caveman-mcp.json
