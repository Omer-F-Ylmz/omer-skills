# REA-AGIR-2 — KISMEN (kapı HN'de geçti; 3 madde yapılmadı)

1. Kalite kapısı: news.ycombinator.com normal ↔ parçalı örtüşme %100 (edge/bundle/route/endpoint/webmcp/inference; tam ve basis'siz). HN tek betik (5 KB) → zayıf kanıt. Orta SPA olarak react.dev denendi: normal mod 85 sn'de OOM (2207 MB, exit 134) → referans yok, örtüşme ÖLÇÜLEMEDİ. İlk react.dev koşusu eski Chrome portundan HN yakaladı (sahte %100) → rea_mcp_cagri.py boş port seçiyor (düzeltildi).
2. Başarısız modül (react.dev): wakaru `module-1247.js` (407 KB, 1/12). Yeni `bol` modu (üst düzey deyimler ≤40 KB) → 13 parçanın 13'ü 2 GB altında geçti (en yavaş 24 sn). rea_parcali.py `modul_coz` ile entegre. Entegre koşu (uçtan uca) YAPILMADI. excalidraw'daki 1 modül + 20 sn canlı yakalama YAPILMADI (araç çağrısı tavanı 45).
3. figma / notion / Electron asar tepe-RAM tablosu YAPILMADI (aynı neden).
4. references/heavy-targets.md yazıldı. REA MCP otomatik parçalı moda düşme: TASARLANMADI/test yok (öneri: rea-mcp-compact.mjs'e analyze_web_bundle sarmalayıcı, OOM'da rea_parcali.py'ı çağır).
5. semgrep+gitleaks, commit: aşağıdaki satır. Push yok.

Yeni dosyalar: tools/rea_parcali_kapi.py, rea_parcali_isci.mjs (normal, bol), rea_parcali.py (yakalama yeniden deneme, modul_coz), rea_mcp_cagri.py (boş port).
Devam: `python tools/rea_parcali.py https://excalidraw.com <dizin> --bekle 20`; ardından figma/notion/asar; sonra otomatik düşüş sarmalayıcısı.
