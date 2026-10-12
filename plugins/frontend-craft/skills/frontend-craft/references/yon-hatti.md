# Yön keşfi hattı — hangi adımda hangi skill/MCP

SKILL.md SIRA'sının (Bölüm 11 → 7 → 8 → 2/9 → 12) her adımında çağrılacak araç. Yalnız kuruluysa çağrılır; yoksa adım frontend-craft'ın kendi kuralıyla koşar, ayrıca kurulum istenmez. Çakışmada frontend-craft > impeccable > ui-ux-pro-max > taste-*.

| Adım | Önce (yerel, ücretsiz) | Sonra (kuruluysa) | Çıktı |
|---|---|---|---|
| 0 geçmiş | `scripts/yakinsama.mjs --gecmis` | — | yasaklı font/zemin/düzen (Bölüm 3a) |
| 11 referans | `tasarim-katalog` (17 ölçülü site, teknik çıkarım) | 21st `get_inspiration` · `design-dna` (görselden token) | 3 yönün her biri farklı kaynaktan |
| 11 üç yön | Bölüm 3a madde 3 (brief sözcüğü → font/zemin) | Stitch ekran varyantı · `taste-skill` stil skill'i (brutalist/minimalist) yalnız seçilen yön tonunda | `.screens/yon/<n>.html` + 1440 PNG |
| 7 DESIGN.md | ÇEKİRDEK 1–7 | `create-design-md` (mevcut site/repodan) · Figma değişkenleri (tasarım dosyası varsa) · 21st `get_theme` | `font ← · zemin ←` satırı |
| 8 iki-pass | yasak listesi + `slop.mjs` bayrakları | `impeccable` critique · `ui-ux-pro-max` palet/tip eşleşmesi | token planı |
| kod | Bölüm 3/4 | 21st `search` → seçilen tek bileşen `get_component` · Figma kod bağlantısı · `scroll-craft`/`threejs-3d-paket` (hareket/3D yönündeyse) | index.html |
| 2/9 döngü | puppeteer screenshot + `slop.mjs` (≤4 tur, sayıyla diff) | `baseline-ui` cila · `fixing-accessibility` | bayrak 0 |
| 12 teslim | Bölüm 4 kabul | `design:design-critique` + `design:accessibility-review` · claude-design (Claude Design projesine aktarım istenirse) | tur raporu |

Jeton kuralı: MCP'ler yalnız adımı koşan oturumda açılır (CC: MCP-HAFIF `mcp_sec` ile yalnız gereken sunucu); okuma uçları (21st `get_*`, `search_logo`, `get_theme`) ücretsiz, `get_component` ve üretim uçları kota düşer (`references/21st-akis.md`). Referans sitelerden yalnız teknik çıkarım; birebir klon ve izinsiz varlık yok.
