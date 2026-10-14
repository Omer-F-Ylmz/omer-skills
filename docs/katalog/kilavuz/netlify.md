# netlify — 15 benzersiz kayıt

**Amaç:** Netlify platformu üzerinde site/uygulama kurma: deploy, yapılandırma, functions/edge functions, blobs, veritabanı, kimlik, formlar, önbellek, görsel CDN, AI Gateway ve MCP sunucuları.

**İç yapı:** Tümü [skill], netlify-<özellik>; her biri tek Netlify ürününe karşılık gelir; netlify-access-control üç ayrı 'auth' kavramını ayırır.

## En güçlü parçalar
- `netlify-deploy` — Git sürekli deploy, CLI deploy ve deploy yönetimi.
- `netlify-config` — Build komutu, publish dizini, redirect/rewrite/proxy ve SPA fallback.
- `netlify-functions` — API uç noktası, form işleyici, auth/Identity bağlama.
- `netlify-frameworks` — Next.js, Astro, Nuxt, SvelteKit, Remix, TanStack Start deploy kurma/düzeltme.
- `netlify-access-control` — Doğru site koruma katmanını seçer, karıştırılan üç auth kavramını ayırır.
- `netlify-ai-gateway` — OpenAI, Claude, Gemini ve OpenRouter modellerini tek gateway'den çağırır.
- `netlify-database` — Veritabanı, iletişim formu/CRUD API, SQL migration ve Drizzle.
- `netlify-caching` — Cache-control, TTL, stale-while-revalidate ayarı.

## Birlikte kullanım
- netlify-config + netlify-frameworks + netlify-deploy: ilk yayın.
- netlify-functions + netlify-blobs + netlify-database: arka uç katmanı.
- netlify-identity + netlify-access-control + netlify-edge-functions (auth middleware).
- cli ailesindeki netlify-cli ile birlikte.

## Tuzaklar
- Üç 'auth' kavramı karıştırılır (netlify-access-control açıkça uyarır).
- netlify-ai-gateway dış model sağlayıcılarına çağrı yapar; ücret katalog metninde belirtilmemiş.
- netlify-forms ile netlify-functions form işleyicisi örtüşür.

## Üyeler
- skill (15): netlify-access-control, netlify-agent-runner, netlify-ai-gateway, netlify-blobs, netlify-caching, netlify-config, netlify-database, netlify-deploy, netlify-edge-functions, netlify-forms, netlify-frameworks, netlify-functions, netlify-identity, netlify-image-cdn, netlify-mcp-servers
