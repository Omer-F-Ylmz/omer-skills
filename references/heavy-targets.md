# REA ağır hedefler (parçalı mod)

Ne zaman: `analyze_web_bundle` / `inspect_web_page` büyük SPA'da (excalidraw, react.dev ...) OOM (exit 134, 2 GB tavan) ya da RAM ≥%85 getiriyorsa. Normal mod tüm betikleri tek süreçte biriktirir; parçalı mod betik başına taze süreç kullanır.

Komut (ham veri diske, modele yalnız özet):
`python tools/rea_parcali.py <url> <dizin> [--bekle 20]` → `<dizin>/ozet.json`, `analiz.json`, `olcum.json`.
Kalite kapısı (normal ↔ parçalı örtüşme): `python tools/rea_parcali_kapi.py <url> <dizin>` → `kapi.json`.

Kademeler: (1) betik başına süreç → (2) başarısızsa wakaru ile modüllere aç → (3) hâlâ başarısız modül `bol` modu ile üst düzey deyimlerden ≤40 KB parçalara bölünür (`rea_parcali_isci.mjs bol`).

RAM kuralı: node `--max-old-space-size=2048`; sistem RAM ≥%85 → yeni süreç bekler, ≥%88 → çalışan öldürülür; işçi ≤800 MB hedef. Başka işler RAM'i şişirirse yakalama yeniden denenir (4 deneme).

Kök neden (ölçüldü): sorun yakalama değil `analyzeScript` anlamsal evresi; tek büyük betik/modülde süperlineer. react.dev `framework-*.js` (181 KB) tek başına 2 GB'ı aşar; wakaru ile açılan 407 KB'lık `module-1247.js` tek süreçte OOM, 13 parçaya (≤40 KB) bölününce hepsi geçti (en yavaş parça 24 sn).

Not: normal mod react.dev'de 85 sn'de OOM'a düşer → o hedefte normal↔parçalı örtüşme ölçülemez (referans yok).

Otomatik düşüş: `python tools/rea_oto.py <url> <dizin> [--bekle 20]` normal `analyze_web_bundle` dener (2 GB tavan); OOM (exit 134) ya da RAM bekçisi durdurursa `rea_parcali.py`'a düşer (`oto.json`: yol + neden). MCP sunucusuna sarmalayıcı konmadı (stdio sunucu; araç yanıtını ortasında değiştirmek riskli) — ağır hedefte giriş noktası rea_oto.py.
Ölçüm (REA-AGIR-2, işçi tepe RSS ≤2.2 GB tavan, sistem RAM tepe ≤%79): excalidraw 10 betik 238-250 sn, modül 154/155 (kalan 1 birim 16 KB tek fonksiyon, 5 KB bölmede de OOM → `atlanan_birim`); figma.com 108/108 betik %100, 132 sn; notion.so 53/54 %98.1, 108 sn; Obsidian asar (en büyük 5 JS, 3.8 MB'a kadar) 5/5, tepe 840 MB, prism.min.js 539 sn (yavaş ama geçti).
figma yakalaması stdio yanıt bütçesine takılıyordu → rea_mcp_cagri.py `REA_MCP_MAX_RESPONSE_BYTES=400000000` verir.
