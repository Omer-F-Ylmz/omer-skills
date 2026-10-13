# chrome-devtools-plugins — 9 benzersiz kayıt

**Amaç:** Chrome DevTools MCP ile tarayıcı hata ayıklama: ağ/konsol/performans izleme, LCP optimizasyonu, bellek sızıntısı, çerez/auth sorunları, erişilebilirlik, CLI betikleri.

**İç yapı:** chrome-devtools [mcp] + chrome-devtools-mcp [plugin] ve chrome-devtools-mcp:<x> skill'leri; konuya özel hata ayıklama skill'leri ve bağlantı sorun giderme.

## En güçlü parçalar
- `chrome-devtools-mcp:chrome-devtools` — Sayfa hata ayıklama, etkileşim otomasyonu, performans ve ağ isteği inceleme.
- `chrome-devtools-mcp:debug-optimize-lcp` — Largest Contentful Paint hata ayıklama ve optimizasyonu.
- `chrome-devtools-mcp:memory-leak-debugging` — Yüksek bellek/OOM'da heap snapshot alma ve karşılaştırma.
- `chrome-devtools-mcp:cookie-debugging` — 401/403, auth yönlendirme, oturum süresi, Set-Cookie sorunları.
- `chrome-devtools-mcp:a11y-debugging` — Semantik HTML, ARIA, odak, klavye, dokunma hedefi, kontrast testi.

## Birlikte kullanım
- chrome-devtools-mcp:debug-optimize-lcp + web ailesinden web-perf.
- chrome-devtools-mcp:troubleshooting → diğer skill'ler: önce bağlantı/hedef sorunu.
- fe-cerez-oturum-hata ajanı ile cookie-debugging.

## Tuzaklar
- chrome-devtools [mcp] e2e test aracı değil.
- yerel-diger'deki chrome-devtools-paket ile çakışan kopya.
- Bağlantı/hedef bulunamazsa troubleshooting skill'i gerekir.

## Üyeler
- mcp (1): chrome-devtools
- plugin (1): chrome-devtools-mcp
- skill (7): chrome-devtools-mcp:a11y-debugging, chrome-devtools-mcp:chrome-devtools, chrome-devtools-mcp:chrome-devtools-cli, chrome-devtools-mcp:cookie-debugging, chrome-devtools-mcp:debug-optimize-lcp, chrome-devtools-mcp:memory-leak-debugging, chrome-devtools-mcp:troubleshooting
