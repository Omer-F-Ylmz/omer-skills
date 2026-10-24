# REA-AGIR-2 — KISMEN (kapı HN %100; react.dev referansı yok; MCP içi otomatik düşüş yok)
1. Kalite kapısı: HN normal↔parçalı %100 (zayıf kanıt, tek 5 KB betik). react.dev normal mod OOM → örtüşme ÖLÇÜLEMEDİ.
2. excalidraw: 154/155 modül (kalan 1 birim = 16 KB tek fonksiyon, 5 KB bölmede de OOM; `atlanan_birim`'e yazılır), %100 DEĞİL. `modul_coz` artık özyinelemeli (40→5 KB). 20 sn canlı yakalama ile koşuldu, 240-250 sn.
3. Tablo (işçi tepe ≤2.2 GB tavan, sistem RAM ≤%79): figma.com 108/108 %100 132 sn · notion.so 53/54 %98.1 108 sn · Obsidian asar en büyük 5 JS (≤3.8 MB) 5/5, tepe 840 MB, 562 sn (prism.min.js tek başına 539 sn).
4. figma düzeltme: stdio yanıt bütçesi yakalamayı düşürüyordu → REA_MCP_MAX_RESPONSE_BYTES verildi (rea_mcp_cagri.py). heavy-targets.md güncel. Otomatik düşüş: `tools/rea_oto.py` (normal→OOM/bekçi→parçalı), 4 birim test TDD kırmızı→yeşil, excalidraw'da canlı doğrulandı (exit 134 → parcali). MCP sunucusuna sarmalayıcı KONMADI (giriş noktası rea_oto.py). Katalog satırı eklenmedi.
5. semgrep: yeni bulgu yok (yalnız eski localhost urlopen uyarısı); gitleaks değişen dosyalarda temiz. Push yok.
Maliyet ≈$0.85 (hedef $0.50 aşıldı: excalidraw/notion/figma/asar canlı koşuları).
